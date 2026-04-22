#!/usr/bin/env python3
"""
GitHub Issues Connector for uHomeNest .dev Flow System

This module provides bidirectional synchronization between GitHub Issues
and the .dev system's epic/task management.
"""

import os
import yaml
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

class GitHubConnector:
    """Main connector class for GitHub Issues integration."""
    
    def __init__(self, config_path: str = ".dev/integration/github-config.yaml"):
        """Initialize the GitHub connector with configuration."""
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.config['github_token']}",
            "User-Agent": "uHomeNest-dev-flow-system"
        })
        
        # Cache for issue-epic mapping
        self.issue_cache = {}
        self.epic_cache = {}
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config: {e}")
    
    def test_connection(self) -> bool:
        """Test the GitHub API connection."""
        try:
            response = self.session.get("https://api.github.com/user")
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Connection test failed: {e}")
            return False
    
    def get_repo_issues(self, repo: str, state: str = "all") -> List[Dict[str, Any]]:
        """Get all issues from a repository."""
        issues = []
        page = 1
        per_page = 100
        
        while True:
            params = {
                "state": state,
                "page": page,
                "per_page": per_page
            }
            
            response = self.session.get(
                f"https://api.github.com/repos/{repo}/issues",
                params=params
            )
            response.raise_for_status()
            
            batch = response.json()
            if not batch:
                break
                
            issues.extend(batch)
            page += 1
            
            # GitHub API has a max of 100 items per page
            if len(batch) < per_page:
                break
        
        return issues
    
    def create_issue(self, repo: str, title: str, body: str, 
                    labels: List[str] = None, epic_id: str = None) -> Dict[str, Any]:
        """Create a new GitHub issue linked to an epic."""
        payload = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        
        # Add epic reference if provided
        if epic_id:
            payload["body"] += f"\n\n---\n**Linked Epic**: {epic_id}"
            payload["labels"].append("epic-linked")
        
        response = self.session.post(
            f"https://api.github.com/repos/{repo}/issues",
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def update_issue(self, repo: str, issue_number: int, 
                     title: str = None, body: str = None, 
                     state: str = None) -> Dict[str, Any]:
        """Update an existing GitHub issue."""
        payload = {}
        if title:
            payload["title"] = title
        if body:
            payload["body"] = body
        if state:
            payload["state"] = state
            
        response = self.session.patch(
            f"https://api.github.com/repos/{repo}/issues/{issue_number}",
            json=payload
        )
        response.raise_for_status()
        
        return response.json()
    
    def sync_issues_to_epics(self, repo: str, epics_dir: str = ".dev/tasks/epics") -> Dict[str, Any]:
        """Synchronize GitHub issues with local epics."""
        results = {
            "synced": 0,
            "created": 0,
            "updated": 0,
            "errors": 0
        }
        
        # Load all epics
        epics = {}
        for epic_file in os.listdir(epics_dir):
            if epic_file.endswith(".md"):
                epic_id = epic_file.replace(".md", "")
                epics[epic_id] = self._parse_epic_file(os.path.join(epics_dir, epic_file))
        
        # Get all issues
        issues = self.get_repo_issues(repo)
        
        # Process each issue
        for issue in issues:
            try:
                # Check if issue is linked to an epic
                epic_id = self._extract_epic_id(issue["body"])
                
                if epic_id and epic_id in epics:
                    # Update epic with issue status
                    epic = epics[epic_id]
                    task_id = f"issue-{issue['number']}"
                    
                    # Update task status in epic
                    if task_id in epic['tasks']:
                        epic['tasks'][task_id]['status'] = issue['state']
                        epic['tasks'][task_id]['github_url'] = issue['html_url']
                        results["updated"] += 1
                    else:
                        # Add new task from issue
                        epic['tasks'][task_id] = {
                            'title': issue['title'],
                            'status': issue['state'],
                            'github_url': issue['html_url'],
                            'created_at': issue['created_at']
                        }
                        results["created"] += 1
                    
                    # Save updated epic
                    self._save_epic_file(os.path.join(epics_dir, f"{epic_id}.md"), epic)
                    results["synced"] += 1
                    
            except Exception as e:
                results["errors"] += 1
                print(f"Error processing issue {issue['number']}: {e}")
        
        return results
    
    def _extract_epic_id(self, issue_body: str) -> Optional[str]:
        """Extract epic ID from issue body."""
        if "**Linked Epic**:" in issue_body:
            lines = issue_body.split("\n")
            for line in lines:
                if "**Linked Epic**:" in line:
                    return line.split(":")[1].strip()
        return None
    
    def _parse_epic_file(self, file_path: str) -> Dict[str, Any]:
        """Parse an epic Markdown file."""
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Simple parsing - in production would use proper Markdown parser
        epic = {
            'id': os.path.basename(file_path).replace('.md', ''),
            'title': content.split('##')[0].replace('#', '').strip(),
            'tasks': {}
        }
        
        # Extract tasks (simplified)
        if '## Tasks' in content:
            tasks_section = content.split('## Tasks')[1]
            for line in tasks_section.split('\n'):
                if line.startswith('- [ ]') or line.startswith('- [x]'):
                    task_title = line[6:].strip()
                    task_id = f"task-{len(epic['tasks']) + 1}"
                    epic['tasks'][task_id] = {
                        'title': task_title,
                        'status': 'open' if line.startswith('- [ ]') else 'closed'
                    }
        
        return epic
    
    def _save_epic_file(self, file_path: str, epic: Dict[str, Any]) -> None:
        """Save an epic back to Markdown file."""
        # Simple implementation - in production would be more sophisticated
        lines = []
        lines.append(f"# {epic['id'].replace('-', ' ').title()}")
        lines.append("")
        
        # Add tasks section
        lines.append("## Tasks")
        for task_id, task in epic['tasks'].items():
            status = " " if task['status'] == 'open' else "x"
            line = f"- [{status}] {task['title']}"
            if 'github_url' in task:
                line += f" ([Issue]({task['github_url']}))"
            if 'github_number' in task:
                line += f" (#{task['github_number']})"
            lines.append(line)
        
        with open(file_path, 'w') as f:
            f.write('\n'.join(lines))
    
    def sync_epics_to_issues(self, repo: str, epics_dir: str = ".dev/tasks/epics") -> Dict[str, Any]:
        """Synchronize local epics to GitHub issues (reverse sync)."""
        results = {
            "synced": 0,
            "created": 0,
            "updated": 0,
            "errors": 0
        }
        
        # Get existing issues for reference
        existing_issues = self.get_repo_issues(repo)
        issue_map = {issue['number']: issue for issue in existing_issues}
        
        # Process each epic
        for epic_file in os.listdir(epics_dir):
            if epic_file.endswith(".md"):
                epic_id = epic_file.replace(".md", "")
                epic_path = os.path.join(epics_dir, epic_file)
                epic = self._parse_epic_file(epic_path)
                
                # Process each task in epic
                for task_id, task in epic['tasks'].items():
                    try:
                        # Check if task is already linked to GitHub
                        github_number = None
                        if 'github_number' in task:
                            github_number = task['github_number']
                        elif 'github_url' in task:
                            # Extract issue number from URL
                            github_number = task['github_url'].split('/')[-1]
                        
                        issue_exists = github_number and int(github_number) in issue_map
                        
                        if issue_exists:
                            # Update existing issue
                            issue = issue_map[int(github_number)]
                            if issue['title'] != task['title'] or issue['state'] != task['status']:
                                self.update_issue(
                                    repo, 
                                    int(github_number),
                                    title=task['title'],
                                    state=task['status']
                                )
                                results["updated"] += 1
                        else:
                            # Create new issue
                            new_issue = self.create_issue(
                                repo, 
                                title=task['title'],
                                body=f"Task from epic: {epic_id}\n\nStatus: {task['status']}",
                                labels=["dev-system", "epic-linked"],
                                epic_id=epic_id
                            )
                            
                            # Update task with GitHub reference
                            task['github_number'] = new_issue['number']
                            task['github_url'] = new_issue['html_url']
                            
                            # Save updated epic
                            self._save_epic_file(epic_path, epic)
                            results["created"] += 1
                        
                        results["synced"] += 1
                        
                    except Exception as e:
                        results["errors"] += 1
                        print(f"Error processing task {task_id} in epic {epic_id}: {e}")
        
        return results
    
    def full_bidirectional_sync(self, repo: str, epics_dir: str = ".dev/tasks/epics") -> Dict[str, Any]:
        """Perform complete bidirectional synchronization between GitHub and .dev system."""
        results = {
            "github_to_dev": {},
            "dev_to_github": {},
            "total": {"synced": 0, "created": 0, "updated": 0, "errors": 0}
        }
        
        # Sync GitHub issues to .dev epics
        results["github_to_dev"] = self.sync_issues_to_epics(repo, epics_dir)
        
        # Sync .dev epics to GitHub issues
        results["dev_to_github"] = self.sync_epics_to_issues(repo, epics_dir)
        
        # Calculate totals
        for key in ["synced", "created", "updated", "errors"]:
            results["total"][key] = (
                results["github_to_dev"].get(key, 0) + 
                results["dev_to_github"].get(key, 0)
            )
        
        return results
    
    def create_github_config(self, token: str, repo: str, output_path: str = ".dev/integration/github-config.yaml") -> None:
        """Create a GitHub configuration file."""
        config = {
            'github_token': token,
            'default_repo': repo,
            'sync_interval': 3600,  # 1 hour
            'max_retries': 3,
            'timeout': 30,
            'labels': {
                'epic-linked': 'epic-linked',
                'dev-system': 'dev-system',
                'automated': 'automated'
            },
            'webhook': {
                'enabled': False,
                'secret': 'optional-webhook-secret-for-validation',
                'port': 8080,
                'endpoint': '/webhook/github'
            }
        }
        
        with open(output_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    def handle_webhook(self, payload: Dict[str, Any], signature: str = None) -> Dict[str, Any]:
        """Handle incoming GitHub webhook payloads."""
        # Validate signature if webhook secret is configured
        if signature and self.config.get('webhook', {}).get('secret'):
            if not self._validate_webhook_signature(payload, signature):
                return {"status": "error", "message": "Invalid signature"}
        
        # Determine event type
        event = payload.get('action', 'unknown')
        issue = payload.get('issue', {})
        
        # Handle different event types
        if event in ['opened', 'edited', 'closed', 'reopened']:
            return self._handle_issue_event(issue)
        elif event == 'labeled':
            return self._handle_label_event(payload)
        else:
            return {"status": "ignored", "message": f"Unsupported event: {event}"}
    
    def _handle_issue_event(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Handle issue-related webhook events."""
        try:
            # Extract epic ID from issue body
            epic_id = self._extract_epic_id(issue.get('body', ''))
            
            if epic_id:
                # Update the corresponding epic
                epic_path = os.path.join(".dev/tasks/epics", f"{epic_id}.md")
                
                if os.path.exists(epic_path):
                    epic = self._parse_epic_file(epic_path)
                    task_id = f"issue-{issue['number']}"
                    
                    # Update or create task
                    if task_id not in epic['tasks']:
                        epic['tasks'][task_id] = {}
                    
                    epic['tasks'][task_id].update({
                        'title': issue['title'],
                        'status': issue['state'],
                        'github_number': issue['number'],
                        'github_url': issue['html_url'],
                        'updated_at': issue.get('updated_at', datetime.now().isoformat())
                    })
                    
                    # Save updated epic
                    self._save_epic_file(epic_path, epic)
                    
                    return {
                        "status": "success",
                        "action": "epic_updated",
                        "epic_id": epic_id,
                        "issue_number": issue['number']
                    }
                else:
                    return {
                        "status": "warning",
                        "message": f"Epic not found: {epic_id}",
                        "issue_number": issue['number']
                    }
            else:
                return {
                    "status": "ignored",
                    "message": "Issue not linked to any epic",
                    "issue_number": issue['number']
                }
                
        except Exception as e:
            return {"status": "error", "message": str(e), "issue_number": issue.get('number')}
    
    def _handle_label_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle label-related webhook events."""
        issue = payload.get('issue', {})
        label = payload.get('label', {}).get('name', '')
        
        # Check if epic-linked label was added
        if label == self.config['labels']['epic-linked']:
            return self._handle_issue_event(issue)
        
        return {"status": "ignored", "message": "Label event not relevant"}
    
    def _validate_webhook_signature(self, payload: Dict[str, Any], signature: str) -> bool:
        """Validate GitHub webhook signature."""
        # In production, implement proper HMAC validation
        # This is a simplified placeholder
        import hmac
        import hashlib
        
        secret = self.config.get('webhook', {}).get('secret', '').encode()
        if not secret:
            return True  # No secret configured, skip validation
        
        try:
            # GitHub sends signature as "sha1=..."
            if signature.startswith("sha1="):
                signature = signature[5:]
            
            # Calculate expected signature
            mac = hmac.new(secret, msg=str(payload).encode(), digestmod=hashlib.sha1)
            expected_signature = mac.hexdigest()
            
            return hmac.compare_digest(expected_signature, signature)
        except Exception:
            return False
    
    def start_webhook_server(self, host: str = "0.0.0.0", port: int = None) -> None:
        """Start a webhook server for real-time updates."""
        from flask import Flask, request, jsonify
        
        port = port or self.config.get('webhook', {}).get('port', 8080)
        endpoint = self.config.get('webhook', {}).get('endpoint', '/webhook/github')
        
        app = Flask(__name__)
        
        @app.route(endpoint, methods=['POST'])
        def webhook_handler():
            """Handle incoming GitHub webhooks."""
            signature = request.headers.get('X-Hub-Signature', '')
            payload = request.get_json()
            
            if not payload:
                return jsonify({"error": "No payload"}), 400
            
            result = self.handle_webhook(payload, signature)
            
            if result.get('status') == 'error':
                return jsonify(result), 400
            
            return jsonify(result), 200
        
        print(f"🚀 Starting webhook server on {host}:{port}{endpoint}")
        print("📡 Waiting for GitHub events...")
        app.run(host=host, port=port)

# Example usage
if __name__ == "__main__":
    print("GitHub Connector for uHomeNest .dev Flow System")
    print("=" * 50)
    
    # Check if config exists
    config_path = ".dev/integration/github-config.yaml"
    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        print("Please create it using create_github_config() method.")
    else:
        try:
            connector = GitHubConnector(config_path)
            
            # Test connection
            if connector.test_connection():
                print("✅ GitHub connection successful!")
                
                # Example: Get issues
                repo = connector.config['default_repo']
                print(f"📋 Fetching issues from {repo}...")
                issues = connector.get_repo_issues(repo, state="open")
                print(f"📊 Found {len(issues)} open issues")
                
                # Example: Sync with epics
                print("🔄 Synchronizing with epics...")
                results = connector.sync_issues_to_epics(repo)
                print(f"📈 Sync results: {results}")
            else:
                print("❌ GitHub connection failed")
                
        except Exception as e:
            print(f"❌ Error: {e}")