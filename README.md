# uDevFramework Scaffold

## 📁 Universal Project Template

This directory contains the **base template** used by `udev init` to create new projects following the universal spine structure.

## 🏗️ Structure

```
scaffold/
├── base-layers/          # Foundation templates
│   ├── base-node/        # Node.js/TypeScript
│   ├── base-go/          # Go
│   ├── base-python/      # Python
│   └── base-rust/        # Rust
├── custom-layers/        # Feature templates
│   ├── udos/             # uDos CLI
│   ├── mastra/           # AI agents
│   ├── chasis/           # Containers
│   └── wordpress/       # WordPress
├── flavours/             # Platform variants
│   ├── linux-mint/       # Linux Mint
│   ├── mac-arm/          # Mac ARM
│   └── classic-ui/       # Classic UI
├── templates/            # File templates
│   ├── service/          # Service
│   ├── agent/           # Agent
│   └── command/         # Command
└── .udev/                # Framework config
    └── manifest.yaml    # Scaffold manifest
```

## 📄 Base Layers

### base-node (Node.js/TypeScript)

**Structure:**
```
base-node/
├── .eslintrc.json
├── .prettierrc
├── tsconfig.json.template
├── package.json.template
├── README.md.template
└── layer.yaml
```

**Features:**
- ESLint + Prettier configuration
- TypeScript setup
- Jest testing
- GitHub Actions CI/CD
- Standard README template

### base-go (Go)

**Structure:**
```
base-go/
├── go.mod.template
├── Makefile
├── main.go.template
├── .golangci.yml
└── layer.yaml
```

**Features:**
- Go modules
- Makefile with common tasks
- golangci-lint configuration
- Standard project structure

### base-python (Python)

**Structure:**
```
base-python/
├── pyproject.toml.template
├── .pre-commit-config.yaml
├── main.py.template
├── requirements.txt.template
└── layer.yaml
```

**Features:**
- Poetry/Pipenv support
- Pre-commit hooks
- Black + Ruff formatting
- Pytest configuration

### base-rust (Rust)

**Structure:**
```
base-rust/
├── Cargo.toml.template
├── src/
│   └── main.rs.template
├── .rustfmt.toml
└── layer.yaml
```

**Features:**
- Cargo configuration
- Rustfmt formatting
- Clippy linting
- Standard Rust project structure

## 🎨 Custom Layers

### udos (uDos CLI Framework)

**Structure:**
```
udos/
├── src/
│   ├── commands/
│   │   └── example.ts.template
│   ├── core/
│   │   └── engine.ts.template
│   └── types/
│       └── index.ts.template
├── package.json.addition
└── layer.yaml
```

**Features:**
- CLI command structure
- Core engine
- Type definitions
- uDos integration

### mastra (AI Agents)

**Structure:**
```
mastra/
├── services/
│   └── mastra-agent.ts.template
├── config/
│   └── agents.yaml.template
└── layer.yaml
```

**Features:**
- Mastra agent service
- Agent configuration
- Codegen, explain, refactor, test agents

### chasis (Container Runtime)

**Structure:**
```
chasis/
├── docker/
│   ├── Dockerfile.template
│   └── docker-compose.yml.template
├── scripts/
│   └── container.sh.template
└── layer.yaml
```

**Features:**
- Docker configuration
- Container scripts
- SKIN/LENS integration

### wordpress (CMS)

**Structure:**
```
wordpress/
├── wp-config.php.template
├── functions.php.addition
├── plugins/
│   └── required-plugins.txt
└── layer.yaml
```

**Features:**
- WordPress configuration
- Plugin management
- Theme setup

## 🎨 Flavours

### linux-mint

**Customizations:**
- Path adjustments for Linux Mint
- Package manager (apt)
- Service configurations

### mac-arm

**Customizations:**
- Mac ARM specific paths
- Homebrew package manager
- macOS service configurations

### classic-ui

**Customizations:**
- Classic UI themes
- Retro styling
- Traditional layouts

## 📄 Templates

### Service Template

```handlebars
{{{header}}}

/**
 * {{name}}
 * {{description}}
 *
 * @module {{module}}
 * @category {{category}}
 * @subcategory {{subcategory}}
 */

{{{imports}}}

export class {{Name}} {
  {{properties}}
  
  constructor({{params}}) {
    {{constructor}}
  }
  
  {{methods}}
}

export default {{Name}};
```

### Agent Template

```handlebars
{{{header}}}

/**
 * {{name}} Agent
 * {{description}}
 *
 * Capabilities:
 * {{capabilities}}
 */

export class {{Name}}Agent {
  constructor(config: AgentConfig) {
    // Agent initialization
  }
  
  async execute(task: string, context: any): Promise<any> {
    // Task execution
  }
}
```

### Command Template

```handlebars
{{{header}}}

/**
 * {{name}} command
 * {{description}}
 */

export function {{camelName}}(program: Command) {
  program
    .command('{{kebabName}}')
    .description('{{description}}')
    {{options}}
    .action(async (options) => {
      {{action}}
    });
}
```

## 📦 Layer Manifest Format

```yaml
# base-node/layer.yaml
name: base-node
version: 2.1.0
description: Node.js/TypeScript foundation
author: Sonic Family

dependencies: []

flavours:
  - name: node20
    variables:
      NODE_VERSION: 20.20.0
    files:
      - .nvmrc
      - package.json

files:
  - source: .eslintrc.json
    target: .eslintrc.json
    merge: replace
  - source: tsconfig.json.template
    target: tsconfig.json
    template: true

scripts:
  post_install: |
    npm install
    npm run build

compatibility:
  conflicts:
    - base-go
    - base-python
```

## 🔧 Usage

### Create Project from Scaffold

```bash
# Initialize new project
udev init my-project \
  --layers base-node,udos,mastra \
  --flavour linux-mint
```

### Add Layer to Project

```bash
# Add layer to existing project
udev layer add mastra --flavour deepseek
```

### Update Project

```bash
# Update to latest framework
udev update .
```

## 🎯 Implementation Status

| Component | Status | Target |
|-----------|--------|--------|
| Base layers | 🟡 Planned | v1.4.0 |
| Custom layers | 🟡 Planned | v1.4.0 |
| Flavours | 🟡 Planned | v1.4.0 |
| Templates | 🟡 Planned | v1.4.0 |

## 📚 References

- [Universal Spine Specification](../specs/architecture/universal-spine.md)
- [Layer Manifest Format](../specs/templating/TEMPLATING_SYSTEM_BRIEF.md)

---

**Scaffold Directory** — Base templates for uDevFramework projects 🏗️
