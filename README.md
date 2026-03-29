# Claude Code Plugins by Carlos Lezama

A collection of Claude Code plugins for systematic development workflows and productivity enhancement.

## Available Plugins

### Research-Design-Implement

A systematic workflow plugin that guides Claude through three structured phases for code changes:

1. **Research** - Thoroughly explore and understand the codebase
2. **Design** - Create detailed implementation roadmap with success criteria
3. **Implement** - Execute plan with automated and manual verification

**Use cases:**
- Complex features touching multiple files
- Refactoring with significant scope
- Features requiring architectural decisions
- Tasks needing careful planning

**Documentation:** [plugins/rdi/README.md](plugins/rdi/README.md)

## Installation

### From GitHub

Install this marketplace directly from GitHub:

```bash
/plugin marketplace add clzmj/claude-code-plugins
```

### Install Individual Plugins

Once the marketplace is added, install specific plugins:

```bash
/plugin install rdi@clzmj
```

## Plugin Structure

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace configuration
├── plugins/
│   └── rdi/                         # RDI workflow plugin
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── commands/
│       │   └── rpi.md           # Main workflow command
│       ├── agents/               # Custom agents
│       ├── hooks/                # Utility hooks
│       └── README.md            # Plugin documentation
├── LICENSE                       # Apache 2.0 License
└── README.md                     # This file
```

## Quick Start

### Using Research-Design-Implement

1. Install the plugin:
   ```bash
   /plugin install rdi@lezcodes
   ```

2. Start the workflow:
   ```bash
   /rpi
   ```

3. Follow the interactive prompts through research, planning, and implementation.

### Example Workflow

```
User: /rpi

Claude: I'll guide you through a systematic Research → Plan → Implement workflow...
        What would you like to work on?

User: Add user authentication with JWT

Claude: [Research Phase]
        Analyzing current auth implementation...

        [Plan Phase]
        Here are the implementation options...

        [Implement Phase]
        Phase 1: Add JWT service
        Automated ✓ | Manual testing needed...
```

## Contributing

Contributions are welcome! To add a new plugin or improve existing ones:

1. Fork this repository
2. Create your plugin in `plugins/your-plugin-name/`
3. Add plugin entry to `.claude-plugin/marketplace.json`
4. Include comprehensive README.md with examples
5. Submit a pull request

### Plugin Guidelines

- Use clear, descriptive names
- Include frontmatter in command files with `description` and `model`
- Provide detailed documentation with examples
- Follow the standard plugin structure
- Test thoroughly before submitting

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details

## Author

**Carlos Lezama**
- Email: carlos@carrots.sh

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check plugin-specific README files
- Review examples in documentation

## Version History

### 1.0.0 (2025-12-07)
- Initial marketplace release
- Research-Design-Implement plugin v1.0.0
  - Three-phase workflow (Research, Design, Implement)
  - Parallel research agents
  - Interactive design/planning
  - Phased implementation with verification
  - Hook-based directory creation
  - File-based workflow (research.md → plan.md)
  - Comprehensive documentation with examples
