# .dev System - uHomeNest

The development coordination system for uHomeNest, aligned with uDevFramework standards.

## Structure

- `agents/` - Agent configurations and capabilities (aligned with uDevFramework agent contract)
- `flows/` - Automated workflow definitions (compatible with universal spine)
- `integration/` - Cross-system integration components (GitHub, CI/CD)
- `reports/` - Generated reports and metrics (standardized format)
- `roadmap/` - Development roadmap and planning (v4 roadmap synchronized)
- `safety/` - Safety rules and exceptions (uDevFramework compliant)
- `tasks/` - Task management and tracking (epic-based organization)

## Usage

### Running Flows

```bash
# Run a specific flow (uDevFramework compatible)
python dev/flows/run_flow.py <flow_name>

# List available flows
python dev/flows/list_flows.py

# Execute CI/CD flow
python dev/flows/run_flow.py ci-cd
```

### Agent Management

```bash
# Start the coordinator agent (uDevFramework agent contract)
python dev/agents/start_coordinator.py

# Run a specific agent
python dev/agents/run_agent.py <agent_name>

# Test multi-agent coordination
python dev/agents/test_coordination.py
```

### Roadmap Synchronization

```bash
# Synchronize with v4 roadmap
python dev/roadmap/sync_roadmap.py

# Update epic status
python dev/roadmap/update_epics.py
```

## Configuration

Edit `config.yaml` to customize the development system behavior:

```yaml
# Agent configurations (uDevFramework compliant)
agents:
  codegen:
    enabled: true
    model: "devstral-2"
  tester:
    enabled: true
    model: "devstral-2"
  reviewer:
    enabled: true
    model: "devstral-2"

# Flow configurations
flows:
  dev_cycle: "flows/dev-cycle.flow.yaml"
  review: "flows/review.flow.yaml"
  release: "flows/release.flow.yaml"
  ci_cd: "flows/ci-cd.flow.yaml"
  doc_sync: "flows/doc-sync.flow.yaml"

# Roadmap synchronization
roadmap:
  current_milestone: "milestones.yaml"
  v4_sync: "roadmap/v4-sync.yaml"
```

## Integration with uDevFramework

### Universal Spine Compliance
- Directory structure follows uDevFramework universal spine specification
- Agent contracts compatible with uDevFramework agent system
- Flow definitions use standardized YAML format
- Reporting follows uDevFramework documentation standards

### Cross-Repository Workflows
1. **Specification Development**: Aligned with uDevFramework spec process
2. **Feature Implementation**: Follows uDevFramework implementation status tracking
3. **Release Coordination**: Compatible with uDevFramework release management

### Agent Integration
- **Mastra Agents**: Code generation and task management
- **DSC2**: Validation and compliance checking
- **Hivemind**: Task coordination and workflow management

## Development Workflow

### Daily Operations
1. **Standup**: Review `.dev/tasks/in-progress.md`
2. **Task Assignment**: Update `.dev/tasks/epics/` files
3. **Flow Execution**: Run automated workflows
4. **Report Review**: Check `.dev/reports/` for metrics

### Weekly Planning
1. **Roadmap Review**: Update `.dev/roadmap/v4-sync.yaml`
2. **Epic Planning**: Create/update `.dev/tasks/epics/*.md`
3. **Dependency Check**: Verify cross-repo dependencies
4. **Risk Assessment**: Update safety rules if needed

### Sprint Review
1. **Status Update**: Update `.dev/reports/` with progress
2. **Task Completion**: Move completed work to `.dev/tasks/completed/`
3. **Roadmap Sync**: Run full synchronization
4. **Next Sprint**: Plan in `.dev/tasks/backlog.md`

## Best Practices

### Epic Management
- One epic per major feature/track
- Clear task breakdown with status tracking
- Link to GitHub issues for full traceability
- Regular synchronization with v4 roadmap

### Agent Coordination
- Use coordinator for complex workflows
- Define clear capabilities for each agent
- Implement proper error handling
- Monitor coordination metrics

### Reporting
- Generate reports after each major operation
- Use standardized report templates
- Include metrics and success criteria
- Archive reports for historical reference

## Troubleshooting

### Common Issues

**Agent Connection Failed**
- Verify agent configuration in `agents/*.yaml`
- Check API keys and permissions
- Test with `python dev/agents/test_agent.py`

**Flow Execution Error**
- Check flow definition in `flows/*.yaml`
- Validate YAML syntax
- Review execution logs in `.dev/logs/`

**Roadmap Sync Conflict**
- Review conflict in `.dev/reports/roadmap-sync-*.md`
- Manual resolution may be required
- Update `v4-sync.yaml` with resolution

## Support

- **Documentation**: See `docs/` directory
- **Specs**: Refer to `specs/` for detailed specifications
- **uDevFramework**: Check parent framework for standards
- **GitHub Issues**: Report bugs in uHomeNest repository

## Roadmap

### Q2 2026 - Foundation Stabilization
- Complete core specifications
- Stabilize runtime and CLI
- Implement agent contract
- Complete Matter/HA integration

### Q3 2026 - Feature Completion
- Implement layer composition
- Add Ventoy promotion
- Add agent automation
- Complete sonic-home

### Q4 2026 - Ecosystem Maturity
- Add registry and UI
- Production hardening
- IDE integration
- Fleet management

See `.dev/roadmap/DEV-FLOW-ROADMAP.md` for detailed planning.
