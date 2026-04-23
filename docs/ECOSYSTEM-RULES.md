# uDosGo Ecosystem Rules and Path Structure

## Overview

This document defines the rules and path structure for the uDosGo ecosystem, including the relationships between `~/uDosGo`, `~/Code`, and `~/Code/Apps` directories.

## Ecosystem Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                        uDosGo Ecosystem                        │
├─────────────────┬─────────────────┬─────────────────────────────┐
│    ~uDosGo     │    ~Code        │    ~Code/Apps              │
│  (Core System)  │  (Code Home)   │  (Applications)           │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

## Directory Structure

### 1. `~/uDosGo` - Core System

The main uDosGo directory containing all core components:

```
~/uDosGo/
├── --dev/              # Development environment
├── 3dWorld/            # 3D world and visualization
├── Connect/            # Connect ecosystem
│   └── SeedVault/      # Backup and seed management (MOVED)
├── dev/                # Development tools
├── Docs/               # Documentation
├── Home/               # Home automation
├── Memory/             # State and memory management
├── scripts/            # Utility scripts
├── SonicScrewdriver/   # Development tools
├── Users/              # User management
└── Vendor/             # Third-party dependencies
```

### 2. `~/Code` - Code Home

Central location for code repositories and development:

```
~/Code/
├── Apps/               # Application repositories
│   ├── Marksmith/      # Markdown processing
│   └── McSnackbar/     # Notification system
├── Dev/                # Development resources
├── html/               # Web resources
├── Vendor/             # Vendor repositories
│   └── AgentDigitalOK/ # AgentDigitalOK-owned repos
│       └── Hivemind/   # Multi-agent system (MOVED)
├── wp-sites/           # WordPress sites
└── wpmudev-agent/      # WP management
```

### 3. `~/Code/Apps` - Applications

Application-specific repositories and tools:

```
~/Code/Apps/
├── Marksmith/          # Markdown processing application
│   ├── src/            # Source code
│   ├── tests/          # Test suite
│   └── docs/           # Documentation
└── McSnackbar/         # Notification system
    ├── src/            # Source code
    ├── tests/          # Test suite
    └── docs/           # Documentation
```

## Ecosystem Rules

### 1. Path Resolution Rules

#### Absolute Paths
- `~/uDosGo` - Core system root
- `~/Code` - Code home root
- `~/Code/Apps` - Applications root

#### Relative Paths
- From `~/uDosGo`: Use `../Code` to access Code home
- From `~/Code`: Use `../uDosGo` to access core system
- From `~/Code/Apps`: Use `../..` to access uDosGo

### 2. Repository Organization Rules

#### AgentDigitalOK Repositories
- **Location**: `~/Code/Vendor/AgentDigitalOK/`
- **Examples**: Hivemind, other owned repositories
- **Rule**: All AgentDigitalOK-owned repositories belong here

#### Connect Modules
- **Location**: `~/uDosGo/Connect/`
- **Examples**: SeedVault, other Connect components
- **Rule**: Connect-related modules and templates belong here

#### Applications
- **Location**: `~/Code/Apps/`
- **Examples**: Marksmith, McSnackbar
- **Rule**: Standalone applications belong here

### 3. Dependency Management Rules

#### Core System Dependencies
- Core system (`~/uDosGo`) can depend on:
  - `~/Code/Vendor/` repositories
  - `~/Code/Apps/` applications
  - Internal components

#### Application Dependencies
- Applications (`~/Code/Apps`) can depend on:
  - `~/uDosGo/Vendor/` for shared libraries
  - Other applications in `~/Code/Apps/`
  - Core system components (carefully)

#### Vendor Dependencies
- Vendor repositories (`~/Code/Vendor`) should be:
  - Self-contained
  - Minimal external dependencies
  - Well-documented APIs

### 4. Import/Reference Rules

#### Python Imports
```python
# Import from core system
from uDosGo.Home import HomeAutomation
from uDosGo.Connect import ConnectManager

# Import from Code home
from Code.Vendor.AgentDigitalOK import Hivemind
from Code.Apps import Marksmith
```

#### File Path References
```python
# Reference core system files
core_config = "~/uDosGo/Home/config.yaml"

# Reference code home files
hivemind_path = "~/Code/Vendor/AgentDigitalOK/Hivemind"

# Reference application files
marksmith_path = "~/Code/Apps/Marksmith"
```

### 5. Development Workflow Rules

#### Branch Strategy
- `main` - Production-ready code
- `dev` - Development branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `release/*` - Release candidates

#### Commit Rules
- Follow conventional commits
- Include issue references
- Sign commits when required
- Write meaningful commit messages

#### Pull Request Rules
- Require at least 1 approval
- Must pass all tests
- Must be up-to-date with target branch
- Include documentation updates

### 6. Build and Deployment Rules

#### Build Artifacts
- Core system: `~/uDosGo/build/`
- Applications: `~/Code/Apps/*/build/`
- Shared libraries: `~/Code/Vendor/*/build/`

#### Deployment Targets
- Core system: `/opt/uDosGo/`
- Applications: `/opt/uDosGo/apps/`
- Configurations: `/etc/uDosGo/`

### 7. Testing Rules

#### Test Locations
- Unit tests: `*/tests/unit/`
- Integration tests: `*/tests/integration/`
- E2E tests: `*/tests/e2e/`
- Performance tests: `*/tests/performance/`

#### Test Coverage
- Core system: Minimum 90% coverage
- Applications: Minimum 85% coverage
- Critical components: 95%+ coverage

### 8. Documentation Rules

#### Documentation Locations
- Core system: `~/uDosGo/Docs/`
- Component docs: `*/docs/`
- API docs: `*/docs/api/`
- Architecture: `*/docs/architecture/`

#### Documentation Formats
- `.md` - Markdown for general documentation
- `.rst` - reStructuredText for API docs
- `.drawio` - Diagrams and architecture
- `.plantuml` - UML diagrams

## Path Mapping

### Common Path Mappings

| Logical Path | Physical Path | Purpose |
|-------------|--------------|---------|
| `~/uDosGo` | `/Users/fredbook/uDosGo` | Core system root |
| `~/Code` | `/Users/fredbook/Code` | Code home root |
| `~/Code/Apps` | `/Users/fredbook/Code/Apps` | Applications root |
| `Hivemind` | `~/Code/Vendor/AgentDigitalOK/Hivemind` | Multi-agent system |
| `SeedVault` | `~/uDosGo/Connect/SeedVault` | Backup system |
| `Connect` | `~/uDosGo/Connect` | Connect ecosystem |
| `Home` | `~/uDosGo/Home` | Home automation |

### Environment Variables

```bash
# Recommended environment variables
export UDOSGO_ROOT="~/uDosGo"
export CODE_ROOT="~/Code"
export APPS_ROOT="~/Code/Apps"
export VENDOR_ROOT="~/Code/Vendor"

# Path additions
export PATH="$PATH:$CODE_ROOT/Vendor/AgentDigitalOK/Hivemind/bin"
export PATH="$PATH:$APPS_ROOT/Marksmith/bin"
```

## Ecosystem Integration

### 1. Hivemind Integration

**Location**: `~/Code/Vendor/AgentDigitalOK/Hivemind/`

**Integration Points**:
- Connects to `~/uDosGo/Connect` for messaging
- Uses `~/uDosGo/Memory` for state management
- Interfaces with `~/uDosGo/Home` for automation

**Dependencies**:
- Core system APIs
- Connect protocols
- Memory interfaces

### 2. SeedVault Integration

**Location**: `~/uDosGo/Connect/SeedVault/`

**Integration Points**:
- Part of Connect ecosystem
- Uses Connect messaging
- Integrated with backup systems

**Dependencies**:
- Connect core
- Backup APIs
- Storage interfaces

### 3. Applications Integration

**Location**: `~/Code/Apps/`

**Integration Points**:
- Can use core system APIs
- Can extend functionality
- Should be loosely coupled

**Dependencies**:
- Core system (optional)
- Vendor libraries (as needed)

## Migration Guide

### From Old Structure

```bash
# Old Hivemind location
cd ~/uDosGo/Hivemind

# New Hivemind location
cd ~/Code/Vendor/AgentDigitalOK/Hivemind

# Old SeedVault location
cd ~/uDosGo/SeedVault

# New SeedVault location
cd ~/uDosGo/Connect/SeedVault
```

### Update Scripts

```bash
# Update path references in scripts
sed -i 's|/uDosGo/Hivemind|/Code/Vendor/AgentDigitalOK/Hivemind|g' script.sh
sed -i 's|/uDosGo/SeedVault|/uDosGo/Connect/SeedVault|g' script.sh
```

## Best Practices

### 1. Path Management
- Use environment variables for paths
- Avoid hardcoding absolute paths
- Use relative paths when possible
- Document path dependencies

### 2. Cross-Repository Development
- Define clear interfaces
- Use versioned APIs
- Document dependencies
- Test integration points

### 3. Code Organization
- Keep related code together
- Separate concerns clearly
- Use consistent naming
- Document architecture

### 4. Dependency Management
- Minimize cross-repo dependencies
- Use semantic versioning
- Document breaking changes
- Test dependency updates

## Troubleshooting

### Common Issues

1. **Path Not Found**
   - Verify environment variables
   - Check path references
   - Use absolute paths temporarily

2. **Permission Issues**
   - Check directory permissions
   - Verify user ownership
   - Adjust as needed

3. **Dependency Conflicts**
   - Check version compatibility
   - Isolate dependencies
   - Use virtual environments

### Debugging Tips

```bash
# Check current paths
echo $UDOSGO_ROOT
echo $CODE_ROOT

# Verify directory existence
ls -la ~/uDosGo
ls -la ~/Code
ls -la ~/Code/Apps

# Test path resolution
cd ~/uDosGo && pwd
cd ~/Code && pwd
cd ~/Code/Apps && pwd
```

## Future Evolution

### Planned Enhancements

1. **Unified Build System**
   - Single build script for all repos
   - Consistent build outputs
   - Cross-repo dependency management

2. **Monorepo Option**
   - Evaluate monorepo structure
   - Shared dependencies
   - Unified testing

3. **Improved Tooling**
   - Cross-repo search
   - Dependency visualization
   - Impact analysis tools

### Growth Strategy

1. **Add New Applications**
   - Place in `~/Code/Apps/`
   - Follow existing patterns
   - Document interfaces

2. **Add New Vendors**
   - Place in `~/Code/Vendor/`
   - Maintain isolation
   - Clear ownership

3. **Extend Core System**
   - Add to `~/uDosGo/`
   - Maintain stability
   - Backward compatibility

## Conclusion

This document establishes the rules and structure for the uDosGo ecosystem across `~/uDosGo`, `~/Code`, and `~/Code/Apps`. Following these rules ensures:

- Consistent organization
- Clear dependencies
- Easy maintenance
- Scalable growth
- Team collaboration

**Last Updated**: April 23, 2024
**Status**: Active
**Owner**: Ecosystem Architecture Team
