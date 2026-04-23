# Code Repository Structure and Setup

## Overview

This document defines the proper structure for the `~/Code/` directory, which serves as the home for all AgentDigitalOK-owned repositories and personal projects.

## Directory Structure

```
~/Code/
├── Apps/               # Public applications (AgentDigitalOK)
│   ├── Marksmith/      # ✅ Git repo - Markdown processor
│   └── McSnackbar/     # ✅ Git repo - Notification system
├── Dev/                # Development repositories
│   └── Framework/      # ✅ Git repo - Development framework
├── Vendor/             # Vendor/AgentDigitalOK repositories
│   ├── AgentDigitalOK/ # AgentDigitalOK organization
│   │   └── Hivemind/   # ✅ Git repo - Multi-agent system
│   ├── airpaint/       # ✅ Git repo
│   ├── edit.tf/        # ✅ Git repo
│   ├── nextchat/       # ✅ Git repo
│   ├── themes/         # Directory
│   │   └── monaspace/ # ✅ Git repo - Theme
│   ├── markdownify-mcp/# ✅ Git repo
│   ├── masquerain/     # ✅ Git repo
│   └── milkdown/       # ✅ Git repo
├── Private/            # ✅ NEW - Personal projects (non-AgentDigitalOK)
├── wpmudev-agent/      # ✅ Git repo
└── Documentation files (MD) - Various spec sheets
```

## Repository Status

### AgentDigitalOK Owned Repositories

#### 1. Apps/
- **Marksmith** (`git@github.com:AgentDigitalCo/Marksmith.git`)
  - Status: ✅ Committed and pushed
  - Type: Public application
  - Purpose: Markdown processing framework

- **McSnackbar** (`git@github.com:AgentDigitalCo/McSnackbar.git`)
  - Status: ✅ Committed and pushed
  - Type: Public application
  - Purpose: Notification system

#### 2. Dev/
- **Framework** (needs remote setup)
  - Status: ❌ No remote configured
  - Type: Development framework
  - Action: Set up remote to `git@github.com:AgentDigitalOK/Framework.git`

#### 3. Vendor/AgentDigitalOK/
- **Hivemind** (`git@github.com:AgentDigitalOK/Hivemind.git`)
  - Status: ✅ Moved from uDosGo, needs push verification
  - Type: Multi-agent coordination system
  - Purpose: Core agent coordination

#### 4. Vendor/Other
- **airpaint** - needs remote setup
- **edit.tf** - needs remote setup
- **nextchat** - needs remote setup
- **monaspace** - theme repository
- **markdownify-mcp** - needs remote setup
- **masquerain** - needs remote setup
- **milkdown** - needs remote setup

#### 5. Root Level
- **wpmudev-agent** - needs remote setup

### Migration Plan

#### From AgentDigitalCo to AgentDigitalOK

The following repositories need to be migrated from `github.com/AgentDigitalCo` to `github.com/AgentDigitalOK`:

1. **Marksmith** - ✅ Already migrated
2. **McSnackbar** - ✅ Already migrated
3. **Hivemind** - Needs verification
4. **Framework** - Needs migration
5. **airpaint** - Needs migration
6. **edit.tf** - Needs migration
7. **nextchat** - Needs migration
8. **markdownify-mcp** - Needs migration
9. **masquerain** - Needs migration
10. **milkdown** - Needs migration
11. **wpmudev-agent** - Needs migration

## Setup Instructions

### 1. Remove Git from Code Directory (COMPLETED)

```bash
cd ~ && rm -rf Code/.git
```

### 2. Verify Existing Repositories

```bash
# Check all git repositories
find ~/Code -name ".git" -type d
```

### 3. Set Up Remotes for Unconfigured Repos

For each repository that needs remote setup:

```bash
cd /path/to/repo
git remote add origin git@github.com:AgentDigitalOK/RepoName.git
git push -u origin main
```

### 4. Migrate from AgentDigitalCo to AgentDigitalOK

For repositories still on AgentDigitalCo:

```bash
# Change remote URL
cd /path/to/repo
git remote set-url origin git@github.com:AgentDigitalOK/RepoName.git
git push -u origin main
```

### 5. Create New Repositories

For new repositories:

```bash
cd ~/Code
mkdir NewRepo
cd NewRepo
git init
git remote add origin git@github.com:AgentDigitalOK/NewRepo.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

## Repository Organization Rules

### AgentDigitalOK Owned

**Location**: `~/Code/Vendor/AgentDigitalOK/` or `~/Code/Apps/`
**Access**: Organization members
**Purpose**: Core frameworks and applications
**Remote**: `git@github.com:AgentDigitalOK/*`

### Third-Party Vendors

**Location**: `~/Code/Vendor/`
**Access**: Varies by vendor
**Purpose**: External dependencies and tools
**Remote**: Varies by vendor

### Personal Projects

**Location**: `~/Code/Private/`
**Access**: Personal/private
**Purpose**: Non-AgentDigitalOK projects
**Remote**: Personal GitHub or private

## Action Plan

### Immediate Actions

1. ✅ Remove git from `~/Code/` directory
2. ✅ Create `~/Code/Private/` directory
3. ✅ Verify Marksmith and McSnackbar pushes
4. ❌ Set up remotes for unconfigured repos
5. ❌ Migrate from AgentDigitalCo to AgentDigitalOK

### Short-Term Actions

1. Audit all repositories for proper remotes
2. Set up CI/CD for all repositories
3. Document all repositories
4. Create contribution guidelines

### Long-Term Actions

1. Consolidate under AgentDigitalOK organization
2. Standardize repository structure
3. Implement uniform CI/CD pipelines
4. Set up monitoring and alerts

## Repository Health Check

### Healthy Repositories

- **Marksmith**: ✅ Remote set, committed, pushed
- **McSnackbar**: ✅ Remote set, committed, pushed
- **Hivemind**: ✅ Remote set, needs push verification

### Needs Attention

- **Framework**: ❌ No remote
- **airpaint**: ❌ No remote
- **edit.tf**: ❌ No remote
- **nextchat**: ❌ No remote
- **markdownify-mcp**: ❌ No remote
- **masquerain**: ❌ No remote
- **milkdown**: ❌ No remote
- **wpmudev-agent**: ❌ No remote

## Migration Checklist

### For Each Repository

- [ ] Verify repository purpose
- [ ] Set up proper remote
- [ ] Push to AgentDigitalOK
- [ ] Set up CI/CD
- [ ] Add to documentation
- [ ] Configure permissions

### Organization Setup

- [ ] Create AgentDigitalOK organization (if needed)
- [ ] Add team members
- [ ] Set up teams and permissions
- [ ] Configure organization settings

## Summary

The `~/Code/` directory is now properly structured with:
- `Apps/` for AgentDigitalOK applications
- `Vendor/` for dependencies and tools
- `Private/` for personal projects
- Documentation files at root level

**Next Steps**: Set up remotes and migrate repositories to AgentDigitalOK organization.

**Status**: Structure complete, migration in progress ✅
**Date**: April 23, 2024
