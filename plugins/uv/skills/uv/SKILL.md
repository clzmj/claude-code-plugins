---
name: uv
description: Use this skill whenever the user is working with Python projects, dependencies, virtual environments, or package management — regardless of what tool originally created the project. Triggers include any mention of 'uv', 'pip', 'poetry', 'pipenv', 'conda', 'venv', 'virtualenv', 'requirements.txt', 'setup.py', 'setup.cfg', 'pyproject.toml', 'Pipfile', 'environment.yml', Python dependency management, Python version management, or migrating between Python packaging tools. Use this skill even when the project uses legacy tooling — uv has compatibility paths for all of them. If a Python project or package is involved, use this skill.
---

# uv — Universal Python Project & Package Management

uv is an extremely fast Python package installer and resolver written in Rust. It replaces pip, pip-tools, poetry, pyenv, and virtualenv with a single tool that is 10–100x faster.

## Quick Decision: What Kind of Project Am I Looking At?

Before doing anything, identify the project type by its files:

| Files present                              | Project type             | Action                              |
|--------------------------------------------|--------------------------|-------------------------------------|
| `pyproject.toml` with `[project]`          | PEP 621 (modern)         | `uv sync` or `uv pip install -e .`  |
| `pyproject.toml` with `[tool.poetry]` only | Poetry                   | See migration guide                 |
| `Pipfile` / `Pipfile.lock`                 | Pipenv                   | See migration guide                 |
| `setup.py` and/or `setup.cfg`             | Legacy setuptools        | `uv pip install -e .`               |
| `requirements.txt` only                    | Flat deps                | `uv pip install -r requirements.txt`|
| `environment.yml`                          | Conda                    | See migration guide                 |
| Nothing yet                                | New project              | `uv init`                           |

For legacy/non-standard project formats, refer to the migration guides in the supporting documentation.

## Core Workflows

### New Project Setup

```bash
uv init my-project        # Creates pyproject.toml, .python-version, README, .gitignore
cd my-project
uv python pin 3.12        # Pin Python version
uv add fastapi uvicorn    # Add dependencies (creates venv, edits pyproject.toml, generates uv.lock)
uv add --dev pytest ruff  # Add dev dependencies
uv sync                   # Install everything from lockfile
```

### Adding & Removing Dependencies

```bash
uv add requests                          # Add to [project.dependencies]
uv add "django>=4.0,<5.0"               # With version constraints
uv add --dev pytest pytest-cov           # Dev dependencies
uv add --optional docs sphinx            # Optional dependency group
uv add git+https://github.com/user/repo  # From git
uv add -e ./local-package                # Editable local package
uv add -r requirements.txt              # Bulk import from requirements.txt

uv remove requests                       # Remove dependency
uv remove --dev pytest                   # Remove dev dependency
```

### Virtual Environments

```bash
uv venv                   # Create .venv (auto-created by most uv commands anyway)
uv venv --python 3.12     # Specific Python version
uv run python app.py      # Run in venv without activating (preferred)
uv run pytest             # Run any tool in the venv
source .venv/bin/activate  # Traditional activation still works
```

### Python Version Management

```bash
uv python install 3.12           # Install a Python version
uv python install 3.11 3.12 3.13 # Install multiple
uv python list                   # List installed
uv python pin 3.12               # Pin for current project (.python-version)
uv run --python 3.11 python script.py  # One-off run with different version
```

### Lockfile Workflows

```bash
uv lock                         # Create/update uv.lock
uv lock --upgrade               # Upgrade all deps in lock
uv lock --upgrade-package requests  # Upgrade specific package
uv lock --check                 # Verify lock is up to date
uv sync --frozen                # Install exact locked versions (CI-safe)
uv export --format requirements-txt > requirements.txt  # Export for compatibility
uv export --format requirements-txt --hash > requirements.txt  # With hashes
```

### Running Tools Without Installing

```bash
uvx ruff check .           # Run ruff without adding it as a dependency
uvx black .                # Run black ephemerally
uvx poetry export ...      # Run legacy tools without installing them
```

## Project Configuration

### pyproject.toml (standard PEP 621)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My project"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.4.0", "ruff>=0.1.0"]
docs = ["sphinx>=7.0.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = ["pytest>=7.4.0", "ruff>=0.1.0"]

[tool.uv.sources]
my-package = { git = "https://github.com/user/repo.git" }

[tool.uv.workspace]
members = ["packages/*"]  # For monorepos
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
        with:
          enable-cache: true
      - run: uv python install 3.12
      - run: uv sync --all-extras --dev
      - run: uv run pytest
      - run: uv run ruff check .
```

### Docker

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
CMD ["uv", "run", "python", "app.py"]
```

Multi-stage optimized build:

```dockerfile
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "app.py"]
```

## Monorepo / Workspace Support

```
monorepo/
  packages/
    package-a/pyproject.toml
    package-b/pyproject.toml
  pyproject.toml  # root
```

Root `pyproject.toml`:
```toml
[tool.uv.workspace]
members = ["packages/*"]
```

```bash
uv sync                              # Install all workspace packages
uv add --path ./packages/package-a   # Add workspace dependency
```

## Performance & Cache

```bash
# Cache locations (automatic):
#   Linux:  ~/.cache/uv
#   macOS:  ~/Library/Caches/uv
#   Windows: %LOCALAPPDATA%\uv\cache

uv cache clean    # Clear cache
uv cache dir      # Show cache location

# Offline mode (install from cache only)
uv sync --frozen --offline
```

## Best Practices

1. Use `uv init` for all new projects — start native.
2. Commit `uv.lock` to version control for reproducibility.
3. Pin Python version with `.python-version`.
4. Prefer `uv run` over manual venv activation.
5. Use `--frozen` in CI for exact reproduction.
6. Separate dev from production deps (`--dev`).
7. Use workspaces for monorepos.
8. Export `requirements.txt` only when downstream compatibility requires it.
9. Use `uvx` for ephemeral tools and for running legacy tooling (poetry, pipenv, pdm).
10. For legacy projects, prefer `uv pip install -e .` (PEP 517 path) before resorting to export hacks.

## Need more details?

Refer to the supporting reference documents:
- **uv-quick-ref.md** - Command reference table
- **uv-workflows.md** - Detailed workflows
- **python-versions.md** - Version management guide
- **uv-monorepo.md** - Workspace setup
- **uv-legacy-compat.md** - Migration guides
- **python-ci-cd.md** - CI/CD patterns
- **troubleshooting.md** - Common issues and fixes

Or use the agents:
- **uv-project-analyzer** - Analyze your project setup
- **uv-migration-planner** - Plan a migration to uv
- **python-dep-resolver** - Resolve dependency conflicts
