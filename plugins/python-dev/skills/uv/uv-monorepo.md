# Monorepo & Workspace Setup with uv

## Overview

A uv workspace (or monorepo) lets you manage multiple Python packages in a single repository with:
- **Single lockfile** for the entire repo (reproducibility)
- **Unified dependencies** managed at the root
- **Local package dependencies** (package-a depends on package-b)
- **One `uv sync`** installs everything

## Directory Structure

### Simple workspace
```
my-monorepo/
├── pyproject.toml           # Root workspace config
├── uv.lock                  # Single lockfile
├── .python-version
├── packages/
│   ├── api/
│   │   └── pyproject.toml
│   ├── cli/
│   │   └── pyproject.toml
│   └── shared/
│       └── pyproject.toml
└── .gitignore
```

### Complex workspace
```
monorepo/
├── pyproject.toml           # Root
├── uv.lock
├── apps/
│   ├── web/pyproject.toml
│   └── desktop/pyproject.toml
├── packages/
│   ├── sdk/pyproject.toml
│   ├── core/pyproject.toml
│   └── utils/pyproject.toml
└── tools/
    ├── cli/pyproject.toml
    └── test-utils/pyproject.toml
```

## Root Configuration

### Minimal root `pyproject.toml`
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.workspace]
members = ["packages/*"]
```

### With root dependencies
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Shared dependencies for all packages
[project]
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "ruff>=0.1.0"]

[tool.uv.workspace]
members = ["packages/*", "apps/*"]
```

### With root version
```toml
[project]
version = "1.0.0"  # Shared version for all packages

[tool.uv.workspace]
members = ["packages/*"]
```

## Member Packages

### Package structure
```
packages/api/
├── pyproject.toml
├── src/
│   └── my_api/
│       └── __init__.py
└── tests/
    └── test_api.py
```

### Package `pyproject.toml`
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-api"
version = "0.1.0"
description = "API package"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0"]
```

## Inter-Package Dependencies

### Add another workspace package as dependency
```bash
cd packages/cli
uv add --path ../api
```

This updates `packages/cli/pyproject.toml`:
```toml
dependencies = [
    # ... other deps
    "my-api @ {path = \"../api\", editable = true}",
]
```

### Version of workspace packages
Workspace packages are always installed as editable (development mode), regardless of version.

## Workspace Commands

### Install entire workspace
```bash
# Root directory:
uv sync
```

This installs:
- All root dependencies
- All member packages (as editable)
- All their dependencies

### Install specific package only
```bash
cd packages/api
uv sync
```

### Install with extras
```bash
# Install all packages + dev dependencies
uv sync --all-extras --dev

# Install specific extras
uv sync --extra dev
```

### List what's installed
```bash
uv tree
```

### Add dependency to specific package
```bash
cd packages/api
uv add requests
```

## Shared Dependencies

### Approach 1: Root level dependencies
Define shared dependencies at root, inherited by all:

```toml
# Root pyproject.toml
[project]
dependencies = [
    "pydantic>=2.0.0",  # Used by all packages
    "requests>=2.31.0",
]

[tool.uv.workspace]
members = ["packages/*"]
```

Problem: Hard to see which packages actually use what.

### Approach 2: Explicit per-package dependencies
Each package declares its own:

```toml
# packages/api/pyproject.toml
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
]

# packages/cli/pyproject.toml
dependencies = [
    "click>=8.0.0",
    "pydantic>=2.0.0",  # Same version constraint
]
```

Benefit: Clear dependency tree. Single lockfile ensures consistent versions.

### Approach 3: Hybrid
Shared libs at root, specific at packages:

```toml
# Root pyproject.toml
[project]
dependencies = [
    "pydantic>=2.0.0",  # All packages need this
]

# packages/api/pyproject.toml
dependencies = [
    "fastapi>=0.100.0",  # Specific to api
]
```

## Local Path Dependencies

### Reference local package
```bash
cd packages/cli
uv add --path ../api  # Add api as dependency
```

### Reference with extras
```bash
uv add --path ../api[dev]
```

## Testing the Workspace

### Run tests for all packages
```bash
cd /root
uv run pytest packages/*/tests
```

### Run tests for one package
```bash
cd packages/api
uv run pytest
```

### Matrix testing across Python versions
```bash
for v in 3.10 3.11 3.12; do
  uv run --python $v pytest packages/*/tests
done
```

## Lockfile Management

### Single lockfile for everything
```bash
cd /root
uv lock
cat uv.lock  # Contains all packages and their deps
```

### Update specific package's dependencies
```bash
cd packages/api
uv add requests  # Updates root uv.lock
```

### Upgrade all
```bash
cd /root
uv lock --upgrade
```

### Export for compatibility
```bash
uv export --format requirements-txt > requirements.txt
```

## CI/CD for Monorepos

### GitHub Actions
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
      - run: uv sync --frozen --all-extras
      - run: uv run pytest packages/*/tests
      - run: uv run ruff check packages/

  build-and-publish:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        package: ["api", "cli", "sdk"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v2
      - run: uv sync --frozen
      - run: cd packages/${{ matrix.package }} && uv build
      - run: uv publish packages/${{ matrix.package }}/dist/*
```

## Best Practices

1. **Define workspace at root** - `[tool.uv.workspace]` in root `pyproject.toml`
2. **Single lockfile** - commit `uv.lock` from root directory
3. **Explicit dependencies** - each package declares what it needs (even if shared)
4. **Use local paths** - `uv add --path ../package` for inter-dependencies
5. **Version control** - commit `.python-version` and `uv.lock`
6. **Consistent Python** - pin same version across workspace
7. **Test all packages** - run tests for entire workspace in CI
8. **Publish independently** - each package can have independent version/release cycle

## Troubleshooting

### Package not found
```bash
# Verify structure
ls packages/api/pyproject.toml

# Update workspace in root
[tool.uv.workspace]
members = ["packages/*"]
```

### Circular dependency error
```bash
# Check inter-dependencies
cd packages/a && grep "path.*b" pyproject.toml
cd packages/b && grep "path.*a" pyproject.toml

# One must be removed
```

### Lockfile conflicts
```bash
# Regenerate from scratch
rm uv.lock
uv lock
```

### Package not editable in development
```bash
# Make sure it has pyproject.toml with [project] metadata
cd packages/mylib
cat pyproject.toml | grep -A2 "\[project\]"
```
