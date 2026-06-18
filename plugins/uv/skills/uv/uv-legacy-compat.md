# Migrating to uv from Legacy Tools

## Quick Reference

| From | To | Complexity | Time |
|------|----|-----------|----|
| pip + requirements.txt | uv | Easy | 15 min |
| Poetry | uv | Easy | 30 min |
| Pipenv | uv | Medium | 45 min |
| setuptools/setup.py | uv | Medium | 1 hour |
| Conda | uv | Hard | 2+ hours |

---

## From pip + requirements.txt

### Current setup
```
project/
├── requirements.txt
├── requirements-dev.txt
└── venv/
```

### Migration

1. **Initialize uv project**
```bash
uv init
```

2. **Import dependencies**
```bash
uv add -r requirements.txt
uv add -r requirements-dev.txt --dev
```

3. **Verify**
```bash
uv sync
uv tree
```

4. **Clean up**
```bash
rm requirements.txt requirements-dev.txt
rm -rf venv/
```

### Result
```
project/
├── pyproject.toml
├── uv.lock
├── .python-version
└── .venv/
```

---

## From Poetry

### Current setup
```
project/
├── pyproject.toml        # Poetry format
├── poetry.lock
└── venv/
```

### Migration

1. **Run uv init** (converts existing pyproject.toml)
```bash
uv init --upgrade
```

This converts Poetry's `[tool.poetry]` table to `[project]` format.

2. **Verify conversion**
```bash
cat pyproject.toml | grep -A 10 "\[project\]"
```

3. **Sync with uv**
```bash
uv sync
```

uv reads `poetry.lock` initially, then creates `uv.lock`.

4. **Remove Poetry files**
```bash
rm poetry.lock
pip uninstall poetry  # if installed
```

### Manual conversion (if needed)

**Before (Poetry)**:
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
```

**After (uv/PEP 621)**:
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.10,<4"
dependencies = [
    "requests>=2.31,<3",
]

[project.optional-dependencies]
dev = ["pytest>=7.0,<8"]
```

### Version constraint mapping

| Poetry | uv/PEP 440 | Meaning |
|--------|-----------|---------|
| `^3.10` | `>=3.10,<4` | 3.10.x and 3.11.x, etc |
| `~1.5` | `>=1.5,<2` | 1.5.x only |
| `1.5.*` | `==1.5.*` | 1.5.x only |
| `>=1.5` | `>=1.5` | 1.5 and above |
| `>=1.5,<2` | `>=1.5,<2` | 1.5 to 1.x |

---

## From Pipenv

### Current setup
```
project/
├── Pipfile
├── Pipfile.lock
└── venv/
```

### Migration

1. **Initialize uv**
```bash
uv init
```

2. **Migrate from Pipfile**
```bash
# Extract dependencies from Pipfile manually:
cat Pipfile | grep -A 20 "\[packages\]"
cat Pipfile | grep -A 20 "\[dev-packages\]"
```

3. **Add dependencies**
```bash
# From the Pipfile output, add each:
uv add django requests
uv add --dev pytest black
```

4. **Verify and clean**
```bash
uv sync
rm Pipfile Pipfile.lock
rm -rf .venv/
```

### Pipfile to pyproject.toml mapping

**Pipfile**:
```ini
[packages]
django = ">=3.0"
requests = "*"

[dev-packages]
pytest = "*"
black = "*"

[requires]
python_version = "3.11"
```

**pyproject.toml**:
```toml
requires-python = ">=3.11"
dependencies = [
    "django>=3.0",
    "requests",
]

[project.optional-dependencies]
dev = ["pytest", "black"]
```

---

## From setuptools (setup.py / setup.cfg)

### Current setup
```
project/
├── setup.py
├── setup.cfg
└── pyproject.toml (maybe)
```

### Migration

1. **Modern approach: Create pyproject.toml**
```bash
uv init --package my_project
```

2. **Convert dependencies from setup.py**
```bash
# Look at current setup.py:
grep "install_requires" setup.py
grep "extras_require" setup.py
```

3. **Create new pyproject.toml**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.31.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "black>=22.0.0"]
docs = ["sphinx>=4.0.0"]

[project.scripts]
my-cli = "my_project.cli:main"
```

4. **Install as editable**
```bash
uv pip install -e .
```

or with uv native:
```bash
uv add -e .
```

5. **Clean up**
```bash
rm setup.py setup.cfg
rm -rf build/ dist/ *.egg-info/
```

### Common setup.py to pyproject.toml conversions

**setup.py**:
```python
setup(
    name="my-project",
    version="0.1.0",
    py_modules=["mymodule"],
    install_requires=[
        "requests>=2.31",
    ],
    extras_require={
        "dev": ["pytest"],
    },
    entry_points={
        "console_scripts": [
            "mycli=mymodule:main",
        ],
    },
)
```

**pyproject.toml**:
```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = ["requests>=2.31"]

[project.optional-dependencies]
dev = ["pytest"]

[project.scripts]
mycli = "mymodule:main"
```

---

## From Conda

### Current setup
```
project/
├── environment.yml
└── conda-env/
```

### Migration approach

**Option A: Full migration** (recommended)
1. Convert environment.yml to pyproject.toml
2. Use uv instead of conda

**Option B: Coexistence**
1. Keep conda for scientific packages (numpy, pandas, etc.)
2. Use uv for application dependencies

### Option A: Full Migration

1. **Inspect environment.yml**
```bash
cat environment.yml
```

2. **Create equivalent pyproject.toml**
```toml
[project]
name = "my-project"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.21.0",
    "pandas>=1.3.0",
    "scikit-learn>=1.0.0",
]

[project.optional-dependencies]
dev = ["jupyter", "matplotlib"]
```

3. **Install with uv**
```bash
uv sync
```

### Option B: Coexistence

Keep Conda for scientific packages, uv for application code:

```bash
# Create conda environment with scientific packages
conda env create -f environment.yml

# Activate
conda activate myenv

# Use uv inside the conda environment
uv sync  # Installs remaining deps from pyproject.toml
```

### Migration decision tree

- **Pure Python project?** → Full uv migration
- **Uses numpy, pandas, scipy, torch?** → Consider keeping Conda OR use conda-forge wheels with uv
- **Mixed pure Python + scientific?** → Use Conda for base packages, uv for application deps

### Conda package versions

Some Conda packages have different names or versions than PyPI:

| Conda | PyPI | Note |
|-------|------|------|
| `pytorch::pytorch` | `torch` | Use PyPI version |
| `pandas` | `pandas` | Same |
| `numpy` | `numpy` | Same |
| `scipy` | `scipy` | Same |

Most packages are available on PyPI and work fine with uv.

---

## General Post-Migration Checklist

After migrating from any tool:

- [ ] `uv sync` works without errors
- [ ] `uv tree` shows expected dependency tree
- [ ] Tests pass: `uv run pytest`
- [ ] Linting passes: `uv run ruff check .`
- [ ] `uv lock --check` succeeds
- [ ] `.python-version` is committed
- [ ] `pyproject.toml` and `uv.lock` are committed
- [ ] Old tool files are removed (Pipfile, poetry.lock, setup.py, etc.)
- [ ] CI/CD pipelines updated to use uv
- [ ] Documentation updated

---

## Troubleshooting

### "Package X not found on PyPI"
Some Conda-exclusive packages may not have PyPI equivalents. Either:
1. Find alternative on PyPI
2. Keep using Conda for that package
3. Look for a pure-Python equivalent

### "Version conflict during migration"
```bash
# Let uv resolve:
uv lock --upgrade

# Or lock to compatible versions:
uv lock --upgrade-package problem-package
```

### "Different behavior after migration"
Poetry and setuptools may resolve dependencies differently. If you see issues:
1. Compare lockfile outputs
2. Check if package versions are different
3. Run tests to verify behavior

### "Need to support old tool for team"
Use during transition period:
```bash
# Generate requirements.txt from uv.lock:
uv export --format requirements-txt > requirements.txt

# This allows pip-only users to install temporarily
```
