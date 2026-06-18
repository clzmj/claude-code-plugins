# Python Version Management with uv

## Quick Start

```bash
# Pin Python 3.12 for current project
uv python pin 3.12

# Install Python if needed
uv python install 3.12

# Run script with specific Python
uv run --python 3.11 python script.py
```

## The .python-version File

uv uses `.python-version` to specify which Python version(s) a project supports.

### Creating the file
```bash
uv python pin 3.12
cat .python-version  # Shows: 3.12
```

### File format
```
3.12          # Single version
3.11 3.12 3.13  # Multiple versions (spaces)
```

### Multiple versions
Used for projects that support multiple Python versions:
```bash
# Set in pyproject.toml:
requires-python = ">=3.10,<3.13"

# Pin both for testing:
uv python pin 3.10 3.11 3.12
cat .python-version  # 3.10 3.11 3.12
```

## Installing Python

### Check installed versions
```bash
uv python list
```

Output:
```
cpython-3.12.1
cpython-3.11.8
cpython-3.10.13 (in use)
```

### Install a version
```bash
uv python install 3.12
```

### Install multiple
```bash
uv python install 3.11 3.12 3.13
```

### Uninstall
```bash
uv python uninstall 3.11
```

### Install pre-release
```bash
uv python install 3.13.0a5
```

## Version Selection

### Project's preferred version
When `.python-version` is set, uv uses that automatically:
```bash
uv python pin 3.12
uv venv          # Creates .venv with Python 3.12
uv run python    # Uses Python 3.12
```

### Override for one command
```bash
uv run --python 3.11 python script.py
```

### Check what Python will be used
```bash
uv python find 3.12
# Output: /path/to/python3.12
```

## Specifying Version Constraints

### In pyproject.toml
```toml
[project]
requires-python = ">=3.10"  # Supports 3.10 and above
requires-python = ">=3.10,<4"  # Supports 3.10-3.x
requires-python = "~=3.11"  # Supports 3.11.x (not 3.12)
requires-python = "3.10 | 3.11 | 3.12"  # Exact versions
```

### Version specifier syntax
| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Exact version | `==3.12.1` |
| `!=` | Not this version | `!=3.9.*` |
| `>` | Greater than | `>3.10` |
| `>=` | Greater or equal | `>=3.10` |
| `<` | Less than | `<4.0` |
| `<=` | Less or equal | `<=3.12` |
| `~=` | Compatible release | `~=3.11` (matches 3.11.x only) |
| `*` | Wildcard | `3.1*` (any 3.1.x) |

## Testing Across Versions

### Manual testing
```bash
uv python install 3.10 3.11 3.12

# Test each version
for v in 3.10 3.11 3.12; do
  echo "Testing Python $v..."
  uv run --python $v pytest
done
```

### In CI (GitHub Actions)
```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]

steps:
  - uses: astral-sh/setup-uv@v2
  - run: uv python install ${{ matrix.python-version }}
  - run: uv sync --frozen
  - run: uv run --python ${{ matrix.python-version }} pytest
```

## Version Resolution

### How uv picks Python

1. **Explicit `--python` flag**: `uv run --python 3.11 ...`
2. **Project's `.python-version`**: If set
3. **`requires-python` in pyproject.toml**: Uses compatible version
4. **System default**: Latest installed matching constraint

### Debugging version selection
```bash
# See which Python will be used:
uv python find

# With constraint:
uv python find 3.11
```

## Common Patterns

### Support multiple versions in library
```toml
[project]
requires-python = ">=3.10"

[tool.uv]
# Default for development
python = "3.12"

# But test against all supported versions in CI
```

### Pin exact version in application
```bash
uv python pin 3.12.5  # Application requires this exact version
uv venv
uv sync --frozen
```

### Upgrade Python without breaking deps
```bash
# Update Python version
uv python install 3.13
uv python pin 3.13

# Update lockfile with new version
uv lock --upgrade
uv sync
```

### Environment-specific Python
```bash
# Development: Python 3.12
uv python pin 3.12
uv sync --all-extras

# Production: Python 3.11 (more stable)
uv python pin 3.11
uv sync --no-dev
```

## Troubleshooting

### "Python X.Y not found"
```bash
# Install it:
uv python install 3.12

# Or use system Python:
uv python find /usr/bin/python3.12
```

### Version conflicts
```bash
# Check current selection:
uv python find

# Check what's available:
uv python list

# Change pin:
uv python pin 3.12
```

### Old Python in venv
```bash
# Delete and recreate:
rm -rf .venv
uv python pin 3.12  # Update pin first
uv venv
uv sync
```

## Best Practices

1. **Always pin a version** in projects: `uv python pin 3.12`
2. **Commit `.python-version`** to version control
3. **Test against all supported versions** in CI
4. **Use `requires-python`** in `pyproject.toml` to declare support
5. **Update lockfile** when changing Python versions: `uv lock --upgrade`
6. **Use `uv run --python X.Y`** for one-off tasks with different versions
