# uv

Modern Python package and project management with [uv](https://docs.astral.sh/uv/) — packaged as a Claude Code plugin with a comprehensive skill, helper agents, and starter templates.

## Installation

```bash
/plugin marketplace add clzmj/claude-code-plugins
/plugin install uv@clzmj
```

Install uv itself:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Features

### 📦 uv skill
Project initialization, dependency management (add/remove/update), virtual environments, Python version pinning, lockfile workflows, monorepo/workspace support, CI/CD patterns, and migration from Poetry, Pipenv, setuptools, and Conda. The skill triggers automatically whenever you work with Python projects, dependencies, or packaging — even on legacy tooling.

### 🤖 Agents
- **uv-project-analyzer** — detect project type and recommend a uv setup
- **uv-migration-planner** — plan a step-by-step migration to uv from legacy tools
- **python-dep-resolver** — diagnose and resolve version conflicts

### 📄 Templates
Bundled under `skills/uv/templates/`:
- **pyproject-template.toml** — modern PEP 621 starter
- **github-actions-uv.yml** — CI workflow with matrix testing
- **Dockerfile-uv** — multi-stage Docker build with uv

```bash
cp "$(dirname "$CLAUDE_PLUGIN_ROOT")/uv/skills/uv/templates/Dockerfile-uv" ./Dockerfile
```

## Quick start

```bash
uv init my-project && cd my-project
uv python pin 3.12
uv add fastapi uvicorn
uv add --dev pytest ruff
uv sync
```

## Code intelligence

This plugin handles packaging only. For Python LSP diagnostics, install the dedicated LSP plugins:
- **ruff-lsp** — linting + formatting
- **ty-lsp** — type checking

## License

Apache-2.0 — Carlos Lezama (carlos@carrots.sh)
