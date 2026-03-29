# uv Troubleshooting Guide

## Installation & Setup

### "uv: command not found"
**Problem**: uv is not in PATH
**Solution**:
```bash
# Reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or use Homebrew (macOS)
brew install uv

# Add to PATH if needed
export PATH=$HOME/.cargo/bin:$PATH
```

### "Python X.Y not found"
**Problem**: Specified Python version isn't installed
**Solution**:
```bash
# Install it:
uv python install 3.12

# Or list available:
uv python list

# Or use system Python:
uv venv --python /usr/bin/python3.12
```

### ".venv already exists"
**Problem**: venv directory already present
**Solution**:
```bash
# Remove and recreate:
rm -rf .venv
uv venv

# Or activate existing:
source .venv/bin/activate
uv sync
```

---

## Dependency Resolution

### "No compatible version found"
**Problem**: Package version constraints can't be satisfied
**Example**: Package A needs `foo>=1.0,<2.0` but Package B needs `foo>=2.0`
**Solution**:
```bash
# See what's happening:
uv lock --verbose

# Try upgrading one:
uv lock --upgrade-package foo

# Or adjust constraints in pyproject.toml manually
```

### "Circular dependency detected"
**Problem**: Package A depends on B, B depends on A
**Solution**:
```bash
# Check dependencies:
uv tree | grep -A5 package-a

# For workspace:
# Check if package-a depends on package-b and vice versa
# Remove one of the circular dependencies

# Example: packages/api depends on packages/core, but core shouldn't depend back on api
```

### "Failed to build wheel"
**Problem**: A package requires compilation but compiler isn't available
**Solution**:
```bash
# Try pre-built wheels:
uv add --prefer-binary package-name

# Or install build tools:
# macOS:
xcode-select --install

# Ubuntu:
sudo apt-get install build-essential python3-dev

# Try again:
uv sync
```

### "Hash mismatch"
**Problem**: Downloaded package hash doesn't match lockfile
**Solution**:
```bash
# Clear cache and retry:
uv cache clean
uv sync

# If still fails, regenerate lock:
rm uv.lock
uv lock
uv sync
```

---

## Virtual Environment Issues

### "Wrong Python version in venv"
**Problem**: venv was created with old Python
**Solution**:
```bash
# Update Python version in project:
uv python pin 3.12

# Delete venv:
rm -rf .venv

# Recreate:
uv venv
uv sync
```

### "Package installed but can't import"
**Problem**: Package is in lockfile but not in .venv
**Solution**:
```bash
# Resync to ensure installation:
uv sync

# Check if it's actually installed:
uv tree | grep package-name

# Or manually inspect:
ls .venv/lib/python*/site-packages/ | grep package-name
```

### "ModuleNotFoundError when running with uv run"
**Problem**: Package missing or venv not created
**Solution**:
```bash
# Make sure dependencies are installed:
uv sync

# Then run:
uv run python script.py

# Or check specific package:
uv run python -c "import package_name; print(package_name.__version__)"
```

---

## Lockfile Issues

### "uv.lock is out of date"
**Problem**: pyproject.toml was modified but uv.lock wasn't updated
**Solution**:
```bash
# Regenerate lockfile:
uv lock

# Or check without updating:
uv lock --check

# In CI, use:
uv lock --check  # Fails if out of sync
```

### "Lockfile conflicts when merging"
**Problem**: Two branches modified uv.lock differently
**Solution**:
```bash
# Regenerate from current pyproject.toml:
uv lock

# Commit the regenerated lock
git add uv.lock
git commit -m "Regenerate uv.lock"
```

### "Can't install from old lockfile"
**Problem**: uv.lock is too old or corrupted
**Solution**:
```bash
# Back up and regenerate:
mv uv.lock uv.lock.bak
uv lock
uv sync
```

---

## Dependency Conflicts

### "Incompatible version constraint"
**Problem**: Two packages require conflicting versions of a third package
**Example**: `foo>=1.0,<2.0` and `foo>=2.0,<3.0` both required
**Solution**:
```bash
# Find which packages require conflicting versions:
uv tree | grep -B5 foo

# Options:
# 1. Update one package to newer version that's compatible
uv lock --upgrade-package bar  # bar might be the newer compatible version

# 2. Use different package that doesn't have this conflict
# 3. Wait for package updates

# 4. Pin specific version and accept constraints
# In pyproject.toml:
# dependencies = ["foo==1.5.0"]  # Accept oldest version
```

### "Python version incompatibility"
**Problem**: A package requires Python 3.11+ but project supports 3.10
**Solution**:
```toml
# Option 1: Raise minimum Python version in pyproject.toml:
[project]
requires-python = ">=3.11"

# Option 2: Use conditional dependency (environment marker):
dependencies = [
    "package-name>=2.0; python_version >= '3.11'",
    "package-name<2.0; python_version < '3.11'",
]

# Option 3: Use optional group:
[project.optional-dependencies]
modern = ["package-name>=2.0"]  # For Python 3.11+
```

---

## Performance

### "Installation is very slow"
**Problem**: Building wheels from source
**Solution**:
```bash
# Use pre-built wheels:
uv add --prefer-binary package-name

# Or use cache:
uv cache dir  # Shows cache location

# Clear corrupted cache:
uv cache clean
uv sync
```

### "Lockfile generation takes forever"
**Problem**: Complex dependency graph
**Solution**:
```bash
# Check what's slow:
uv lock --verbose 2>&1 | tail -20

# Try removing unnecessary dependencies

# Or split into workspace packages to reduce scope
```

---

## Migration Issues

### "Poetry/Pipenv migration failed"
**Problem**: Old tool's format not properly converted
**Solution**:
```bash
# Manually convert:
# 1. Export old tool's dependencies
poetry export -f requirements.txt

# 2. Import into uv
uv init
uv add -r requirements.txt

# 3. Update pyproject.toml with proper metadata
```

### "Git dependencies won't resolve"
**Problem**: Git URL format incompatible
**Solution**:
```bash
# Correct format:
uv add git+https://github.com/user/repo.git@branch-name

# Or for local:
uv add --path ../local-package

# Or with specific ref:
uv add git+https://github.com/user/repo.git@commit-hash
```

---

## Docker Issues

### "uv not found in Docker image"
**Problem**: Forgot to install uv
**Solution**:
```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
```

### "Large Docker image"
**Problem**: Dependencies cached in Docker layer
**Solution**:
```dockerfile
# Use multi-stage build:
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN uv sync --frozen --no-dev
# This layer is small

FROM python:3.12-slim
COPY --from=builder /app/.venv /app/.venv  # Copy built venv
COPY . .
```

---

## Debugging Commands

### See what's happening
```bash
# Verbose output:
uv lock --verbose

# See dependency tree:
uv tree
uv tree --depth 2
uv tree --outdated

# Check specific package:
uv tree --package package-name

# List installed:
uv pip list
uv pip freeze
```

### Test without changes
```bash
# Verify lock is current:
uv lock --check

# Dry run (don't actually install):
# No built-in option, but:
uv sync --frozen  # Would fail if lock is out of date
```

### Clear everything and start fresh
```bash
# Nuclear option:
rm -rf .venv uv.lock
uv python uninstall --all
uv python install 3.12
uv python pin 3.12
uv lock
uv sync
```

---

## Getting Help

1. **Check status**:
   ```bash
   uv --version
   uv --help
   ```

2. **Enable debug mode**:
   ```bash
   RUST_LOG=debug uv sync
   ```

3. **Check uv docs**:
   https://docs.astral.sh/uv/

4. **Report issues**:
   https://github.com/astral-sh/uv/issues
