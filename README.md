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

### ruff-lsp

Registers the **ruff** language server for Python — fast linting and formatting diagnostics on `.py`/`.pyi` files.

**Documentation:** [plugins/ruff-lsp/README.md](plugins/ruff-lsp/README.md)

### ty-lsp

Registers the **ty** language server for Python — type checking and type-aware navigation on `.py`/`.pyi` files.

**Documentation:** [plugins/ty-lsp/README.md](plugins/ty-lsp/README.md)

### uv

Modern Python package and project management with **uv** — dependencies, virtual environments, Python versions, lockfiles, monorepos, CI/CD, and migration from legacy tools.

**Documentation:** [plugins/uv/README.md](plugins/uv/README.md)

> The `ruff-lsp`, `ty-lsp`, and `uv` plugins replace the former `python-dev` plugin, which has been split into focused single-purpose plugins. Claude Code uses one LSP server per file extension, so install `ruff-lsp` **or** `ty-lsp` as your live server (both can be installed, but only one runs per extension).

### api-design

Makes Claude apply **Stripe-style date-based API versioning** and strict backwards-compatibility rules whenever you create a new API or refactor an existing one — additive by default, breaking changes pinned to a new dated version with backward transforms.

**Documentation:** [plugins/api-design/README.md](plugins/api-design/README.md)

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
│   ├── rdi/                      # RDI workflow plugin
│   │   ├── .claude-plugin/plugin.json
│   │   ├── skills/              # rpi, research, design, implement
│   │   ├── agents/             # Custom agents
│   │   ├── hooks/             # Utility hooks
│   │   └── README.md
│   ├── ruff-lsp/                 # ruff language server (inline lspServers)
│   ├── ty-lsp/                   # ty language server (inline lspServers)
│   ├── uv/                       # uv package management skill + agents
│   └── api-design/               # Stripe-style API design + date versioning
├── LICENSE                       # Apache 2.0 License
└── README.md                     # This file
```

## Quick Start

### Using Research-Design-Implement

1. Install the plugin:
   ```bash
   /plugin install rdi@clzmj
   ```

2. Start the workflow:
   ```bash
   /rdi:rpi
   ```

3. Follow the interactive prompts through research, planning, and implementation.

### Example Workflow

```
User: /rdi:rpi

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
2. Create your plugin in `plugins/your-plugin-name/` with a `.claude-plugin/plugin.json`
3. Add a matching plugin entry to `.claude-plugin/marketplace.json` (same `version`)
4. Include comprehensive README.md with examples
5. Submit a pull request

The CI and release tooling **auto-discover** every plugin under `plugins/*/.claude-plugin/plugin.json` — there's no hardcoded plugin list to update in the workflows or scripts.

### Plugin Guidelines

- Use clear, descriptive names
- Include frontmatter in skill files (`SKILL.md`) with `name` and `description`
- Provide detailed documentation with examples
- Follow the standard plugin structure
- Use [date-based versioning](VERSIONING.md) (`YYYY-MM-DD`), matching `plugin.json` and `marketplace.json`
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
