#!/usr/bin/env python3
"""
Integration Test Suite for GitHub Connector

Comprehensive tests for the GitHub integration functionality.
"""

import os
import tempfile
import shutil
import unittest
from unittest.mock import patch, MagicMock
import yaml

# Import the connector module
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from dev.integration.github_connector import GitHubConnector


class TestGitHubConnector(unittest.TestCase):
    """Test suite for GitHub Connector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.epics_dir = os.path.join(self.test_dir, "epics")
        os.makedirs(self.epics_dir)
        
        # Create a test config
        self.config_path = os.path.join(self.test_dir, "test-config.yaml")
        self.test_config = {
            'github_token': 'test_token',
            'default_repo': 'test/repo',
            'sync_interval': 3600,
            'max_retries': 3,
            'timeout': 30,
            'labels': {
                'epic-linked': 'epic-linked',
                'dev-system': 'dev-system',
                'automated': 'automated'
            }
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.test_config, f)
        
        # Create test epic
        self.test_epic_content = """# Test Epic

## Tasks
- [ ] Task 1
- [ ] Task 2
- [x] Completed Task
"""
        self.test_epic_path = os.path.join(self.epics_dir, "test-epic.md")
        with open(self.test_epic_path, 'w') as f:
            f.write(self.test_epic_content)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_config_loading(self):
        """Test configuration loading."""
        connector = GitHubConnector(self.config_path)
        self.assertEqual(connector.config['github_token'], 'test_token')
        self.assertEqual(connector.config['default_repo'], 'test/repo')
    
    def test_config_file_not_found(self):
        """Test handling of missing config file."""
        with self.assertRaises(FileNotFoundError):
            GitHubConnector("nonexistent.yaml")
    
    def test_invalid_config_yaml(self):
        """Test handling of invalid YAML config."""
        invalid_config = os.path.join(self.test_dir, "invalid.yaml")
        with open(invalid_config, 'w') as f:
            f.write("invalid: yaml: content:")
        
        with self.assertRaises(ValueError):
            GitHubConnector(invalid_config)
    
    @patch('requests.Session.get')
    def test_connection_success(self, mock_get):
        """Test successful GitHub connection."""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'login': 'testuser'}
        mock_get.return_value = mock_response
        
        connector = GitHubConnector(self.config_path)
        result = connector.test_connection()
        self.assertTrue(result)
    
    @patch('requests.Session.get')
    def test_connection_failure(self, mock_get):
        """Test failed GitHub connection."""
        # Mock failed response
        mock_get.side_effect = Exception("Connection error")
        
        connector = GitHubConnector(self.config_path)
        result = connector.test_connection()
        self.assertFalse(result)
    
    def test_epic_parsing(self):
        """Test parsing of epic files."""
        connector = GitHubConnector(self.config_path)
        epic = connector._parse_epic_file(self.test_epic_path)
        
        self.assertEqual(epic['id'], 'test-epic')
        self.assertEqual(len(epic['tasks']), 3)
        self.assertEqual(epic['tasks']['task-1']['title'], 'Task 1')
        self.assertEqual(epic['tasks']['task-1']['status'], 'open')
        self.assertEqual(epic['tasks']['task-3']['status'], 'closed')
    
    def test_epic_saving(self):
        """Test saving of epic files."""
        connector = GitHubConnector(self.config_path)
        epic = {
            'id': 'test-epic',
            'title': 'Test Epic',
            'tasks': {
                'task-1': {'title': 'Updated Task 1', 'status': 'closed'},
                'task-2': {'title': 'Task 2', 'status': 'open'},
                'task-3': {'title': 'Task 3', 'status': 'open', 'github_number': 123}
            }
        }
        
        output_path = os.path.join(self.epics_dir, "output-epic.md")
        connector._save_epic_file(output_path, epic)
        
        # Verify the file was created and contains expected content
        self.assertTrue(os.path.exists(output_path))
        with open(output_path, 'r') as f:
            content = f.read()
        
        self.assertIn('# Test Epic', content)
        self.assertIn('- [x] Updated Task 1', content)
        self.assertIn('- [ ] Task 2', content)
        self.assertIn('#123', content)
    
    def test_epic_id_extraction(self):
        """Test extraction of epic IDs from issue bodies."""
        connector = GitHubConnector(self.config_path)
        
        # Test with epic ID present
        body_with_epic = "Some content\n---\n**Linked Epic**: test-epic-123"
        epic_id = connector._extract_epic_id(body_with_epic)
        self.assertEqual(epic_id, "test-epic-123")
        
        # Test without epic ID
        body_without_epic = "Some content without epic link"
        epic_id = connector._extract_epic_id(body_without_epic)
        self.assertIsNone(epic_id)
    
    @patch('requests.Session.get')
    @patch('requests.Session.post')
    def test_issue_creation(self, mock_post, mock_get):
        """Test creation of GitHub issues."""
        # Mock responses
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'number': 1,
            'html_url': 'https://github.com/test/repo/issues/1',
            'title': 'Test Issue',
            'state': 'open'
        }
        mock_post.return_value = mock_response
        mock_get.return_value = MagicMock(json=lambda: [])
        
        connector = GitHubConnector(self.config_path)
        result = connector.create_issue(
            'test/repo',
            'Test Issue',
            'Issue body',
            epic_id='test-epic'
        )
        
        self.assertEqual(result['number'], 1)
        self.assertIn('**Linked Epic**: test-epic', mock_post.call_args[1]['json']['body'])
    
    @patch('requests.Session.patch')
    def test_issue_update(self, mock_patch):
        """Test updating of GitHub issues."""
        # Mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'number': 1,
            'title': 'Updated Issue',
            'state': 'closed'
        }
        mock_patch.return_value = mock_response
        
        connector = GitHubConnector(self.config_path)
        result = connector.update_issue(
            'test/repo',
            1,
            title='Updated Issue',
            state='closed'
        )
        
        self.assertEqual(result['title'], 'Updated Issue')
        self.assertEqual(result['state'], 'closed')
    
    @patch('requests.Session.get')
    def test_issue_retrieval(self, mock_get):
        """Test retrieval of GitHub issues."""
        # Mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = [
            {
                'number': 1,
                'title': 'Test Issue 1',
                'state': 'open',
                'html_url': 'https://github.com/test/repo/issues/1',
                'body': 'Issue body'
            }
        ]
        mock_get.return_value = mock_response
        
        connector = GitHubConnector(self.config_path)
        issues = connector.get_repo_issues('test/repo')
        
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['number'], 1)
    
    def test_webhook_validation(self):
        """Test webhook signature validation."""
        connector = GitHubConnector(self.config_path)
        
        # Test with no secret configured
        result = connector._validate_webhook_signature({}, "test_signature")
        self.assertTrue(result)  # Should pass when no secret is set
        
        # Test with secret configured
        connector.config['webhook'] = {'secret': 'test_secret'}
        # Note: This is a simplified test - actual HMAC validation would need proper setup
        result = connector._validate_webhook_signature({}, "test_signature")
        # Should return False for mismatched signature
        self.assertFalse(result)
    
    def test_webhook_issue_handling(self):
        """Test handling of issue webhook events."""
        connector = GitHubConnector(self.config_path)
        
        # Create a test epic for the webhook to update
        test_epic = """# Webhook Test Epic

## Tasks
- [ ] Existing Task
"""
        epic_path = os.path.join(self.epics_dir, "webhook-test.md")
        with open(epic_path, 'w') as f:
            f.write(test_epic)
        
        # Test issue payload
        issue_payload = {
            'action': 'closed',
            'issue': {
                'number': 42,
                'title': 'Webhook Test Issue',
                'state': 'closed',
                'html_url': 'https://github.com/test/repo/issues/42',
                'body': 'Test issue\n---\n**Linked Epic**: webhook-test'
            }
        }
        
        result = connector.handle_webhook(issue_payload)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['action'], 'epic_updated')
        self.assertEqual(result['epic_id'], 'webhook-test')
        
        # Verify the epic was updated
        updated_epic = connector._parse_epic_file(epic_path)
        self.assertIn('issue-42', updated_epic['tasks'])
        self.assertEqual(updated_epic['tasks']['issue-42']['status'], 'closed')
    
    def test_webhook_label_handling(self):
        """Test handling of label webhook events."""
        connector = GitHubConnector(self.config_path)
        
        # Test label payload with epic-linked label
        label_payload = {
            'action': 'labeled',
            'label': {'name': 'epic-linked'},
            'issue': {
                'number': 43,
                'title': 'Labeled Issue',
                'state': 'open',
                'html_url': 'https://github.com/test/repo/issues/43',
                'body': 'Labeled issue\n---\n**Linked Epic**: label-test'
            }
        }
        
        result = connector.handle_webhook(label_payload)
        self.assertEqual(result['status'], 'success')
    
    def test_webhook_unknown_event(self):
        """Test handling of unknown webhook events."""
        connector = GitHubConnector(self.config_path)
        
        unknown_payload = {
            'action': 'unknown_action',
            'issue': {'number': 1}
        }
        
        result = connector.handle_webhook(unknown_payload)
        self.assertEqual(result['status'], 'ignored')
    
    def test_bidirectional_sync_structure(self):
        """Test the structure of bidirectional sync results."""
        connector = GitHubConnector(self.config_path)
        
        # Mock the individual sync methods
        with patch.object(connector, 'sync_issues_to_epics') as mock_github_to_dev, \
             patch.object(connector, 'sync_epics_to_issues') as mock_dev_to_github:
            
            mock_github_to_dev.return_value = {
                'synced': 5, 'created': 2, 'updated': 1, 'errors': 0
            }
            mock_dev_to_github.return_value = {
                'synced': 3, 'created': 1, 'updated': 0, 'errors': 1
            }
            
            results = connector.full_bidirectional_sync('test/repo')
            
            # Verify structure
            self.assertIn('github_to_dev', results)
            self.assertIn('dev_to_github', results)
            self.assertIn('total', results)
            
            # Verify totals
            self.assertEqual(results['total']['synced'], 8)
            self.assertEqual(results['total']['created'], 3)
            self.assertEqual(results['total']['updated'], 1)
            self.assertEqual(results['total']['errors'], 1)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration scenarios and end-to-end tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.epics_dir = os.path.join(self.test_dir, "epics")
        os.makedirs(self.epics_dir)
        
        # Create test config
        self.config_path = os.path.join(self.test_dir, "config.yaml")
        config = {
            'github_token': 'test_token',
            'default_repo': 'test/repo',
            'labels': {'epic-linked': 'epic-linked'}
        }
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    @patch('requests.Session.get')
    @patch('requests.Session.post')
    @patch('requests.Session.patch')
    def test_full_sync_scenario(self, mock_patch, mock_post, mock_get):
        """Test a complete synchronization scenario."""
        # Setup mock responses
        mock_get_response = MagicMock()
        mock_get_response.raise_for_status.return_value = None
        mock_get_response.json.side_effect = [
            [],  # No existing issues
            []   # Empty for other calls
        ]
        mock_get.return_value = mock_get_response
        
        mock_post_response = MagicMock()
        mock_post_response.raise_for_status.return_value = None
        mock_post_response.json.return_value = {
            'number': 1,
            'html_url': 'https://github.com/test/repo/issues/1',
            'title': 'Test Task',
            'state': 'open'
        }
        mock_post.return_value = mock_post_response
        
        # Create test epic
        epic_content = """# Test Epic

## Tasks
- [ ] Task to sync to GitHub
"""
        epic_path = os.path.join(self.epics_dir, "test-epic.md")
        with open(epic_path, 'w') as f:
            f.write(epic_content)
        
        # Perform sync
        connector = GitHubConnector(self.config_path)
        results = connector.full_bidirectional_sync('test/repo', self.epics_dir)
        
        # Verify results
        self.assertGreater(results['total']['synced'], 0)
        self.assertEqual(results['dev_to_github']['created'], 1)
        
        # Verify epic was updated with GitHub reference
        updated_epic = connector._parse_epic_file(epic_path)
        self.assertIn('github_number', updated_epic['tasks']['task-1'])


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)