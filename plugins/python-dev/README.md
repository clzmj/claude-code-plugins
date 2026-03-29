# Python Development Plugin

Complete Python development environment with LSP code intelligence and uv package management.

## Features

### 🧠 LSP Code Intelligence
Real-time code diagnostics, type checking, and navigation using Python language servers:
- **ruff** - Fast linting and formatting
- **ty** - Lightweight type checking
- **pyright** - Comprehensive type checker
- **pylance** - Premium type checking with AI

### 📦 uv Package Management
Modern Python package management with:
- Project initialization and setup
- Dependency management (add, remove, update)
- Virtual environment management
- Python version management
- Lockfile workflows
- Monorepo/workspace support
- CI/CD integration patterns

### 🤖 Intelligent Agents
Interactive guidance for:
- **Project Analysis** - Detect project type and recommend setup
- **Migration Planning** - Plan migration to uv from legacy tools
- **Dependency Resolution** - Diagnose and resolve version conflicts
- **LSP Configuration** - Choose and configure language servers

### 📚 Comprehensive Documentation
- Quick reference tables
- Step-by-step workflows
- Migration guides from Poetry, Pipenv, setuptools, Conda
- CI/CD patterns (GitHub Actions, Docker, pre-commit)
- Troubleshooting guides

## Installation

```bash
/plugin install python-dev@clzmj
```

## Quick Start

### Setting up a new project with uv

```bash
# Initialize project
uv init my-project
cd my-project

# Pin Python version
uv python pin 3.12

# Add dependencies
uv add fastapi uvicorn
uv add --dev pytest ruff

# Install everything
uv sync

# Run code
uv run python main.py
uv run pytest
```

### Configuring LSP servers

The plugin automatically provides LSP configurations. Install the language server binaries:

```bash
# For ruff and ty (uses uvx, automatic)
# No additional installation needed

# For pyright
pip install pyright
# or
npm install -g pyright

# For pylance
pip install pylance
```

## Using the Plugin

### Skills

**uv Skill** - Auto-triggered by Python keywords
- Type: `uv init` or `pip install requests`
- Get: Instant access to uv workflows and best practices

**python-lsp Skill** - Auto-triggered by LSP-related keywords
- Type: "Configure LSP" or "Type checking"
- Get: LSP tool comparison and setup guidance

### Agents

Invoke agents for interactive help:

```bash
# In Claude Code, ask:
"Analyze my Python project"  # → uv-project-analyzer
"Plan migration to uv"       # → uv-migration-planner
"Resolve dependency conflict" # → python-dep-resolver
"Help configure LSP"         # → lsp-config-advisor
```

## Documentation Structure

### uv Skill References
- **uv-quick-ref.md** - Command reference table
- **uv-workflows.md** - Core workflows (new project, add deps, venv, versions, lockfiles)
- **python-versions.md** - Python version pinning and management
- **uv-monorepo.md** - Workspace and monorepo setup
- **uv-legacy-compat.md** - Migration from Poetry, Pipenv, setuptools, Conda
- **python-ci-cd.md** - GitHub Actions, Docker, pre-commit integration
- **troubleshooting.md** - Common issues and fixes

### LSP Skill References
- **lsp-tools.md** - Detailed comparison of ruff, ty, pyright, pylance, pylint

### Templates
- **pyproject-template.toml** - Modern PEP 621 starter template
- **github-actions-uv.yml** - CI/CD workflow with matrix testing
- **Dockerfile-uv** - Multi-stage Docker build with uv

## Common Tasks

### Migrate from Poetry to uv
```bash
uv init --upgrade
# or manually:
uv add -r <(poetry export -f requirements.txt)
uv add -r <(poetry export -f requirements.txt --with dev) --dev
```

### Test across Python versions
```bash
uv python install 3.10 3.11 3.12
for v in 3.10 3.11 3.12; do
  uv run --python $v pytest
done
```

### Set up Docker build
Copy the `Dockerfile-uv` template:
```bash
cp /path/to/plugin/templates/Dockerfile-uv ./Dockerfile
docker build -t my-app .
```

### Configure LSP for your editor
The plugin provides LSP configs for Claude Code. Configure LSP tools in `opencode.jsonc`:
```json
{
  "lsp": {
    "ruff": { "enabled": true },
    "pyright": { "enabled": true }
  }
}
```

## Requirements

- Claude Code (or opencode.jsonc editor)
- Python 3.10+ (for development)
- uv (installed separately or via `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## LSP Server Installation

Install language servers based on your choice:

```bash
# Ruff (automatic with uvx)
# No additional setup needed

# Ty (automatic with uvx)
# No additional setup needed

# Pyright
pip install pyright
# or
npm install -g pyright

# Pylance
pip install pylance
```

## Troubleshooting

### LSP not starting?
```bash
# Verify installation:
which ruff
which pyright

# For uvx-based servers, verify uv:
uv --version
```

### uv command not found?
```bash
# Install uv:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH:
export PATH="$HOME/.cargo/bin:$PATH"
```

### Dependency conflicts?
Use the **python-dep-resolver** agent:
```
"I'm getting a dependency conflict between package-a and package-b"
```

### Project analysis needed?
Use the **uv-project-analyzer** agent:
```
"Analyze my Python project and recommend setup"
```

## Glossary

- **uv** - Universal Python package installer and project manager
- **LSP** - Language Server Protocol (provides code intelligence)
- **pyproject.toml** - Modern Python project metadata (PEP 621)
- **uv.lock** - Lockfile for reproducible installs
- **.python-version** - Python version specification for project

## Links

- [uv Documentation](https://docs.astral.sh/uv/)
- [Python LSP Specification](https://microsoft.github.io/language-server-protocol/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins)

## Author

Carlos Lezama (@clzmj)
Email: carlos@carrots.sh

## License

Apache License 2.0
