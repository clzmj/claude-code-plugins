# uv Quick Reference

## Project Initialization

| Command | Purpose |
|---------|---------|
| `uv init my-project` | Create new project |
| `uv init --script app.py` | Create script project |
| `uv init --package my_lib` | Create package project |

## Dependency Management

| Command | Purpose |
|---------|---------|
| `uv add requests` | Add dependency |
| `uv add "django>=4.0,<5.0"` | Add with version constraint |
| `uv add --dev pytest` | Add dev dependency |
| `uv add --optional docs sphinx` | Add optional group |
| `uv add -r requirements.txt` | Import from requirements.txt |
| `uv add git+https://github.com/user/repo` | Add from git |
| `uv add -e ./local-package` | Add local editable |
| `uv remove requests` | Remove dependency |
| `uv remove --dev pytest` | Remove dev dependency |

## Virtual Environments

| Command | Purpose |
|---------|---------|
| `uv venv` | Create .venv |
| `uv venv --python 3.12` | Create with specific Python |
| `uv venv /path/to/venv` | Create at custom location |
| `source .venv/bin/activate` | Activate (Linux/macOS) |
| `.venv\Scripts\activate` | Activate (Windows) |

## Running Code

| Command | Purpose |
|---------|---------|
| `uv run python app.py` | Run script in venv |
| `uv run pytest` | Run tool in venv |
| `uv run --python 3.11 python app.py` | Run with specific Python |
| `uvx ruff check .` | Run tool ephemerally |

## Python Version Management

| Command | Purpose |
|---------|---------|
| `uv python install 3.12` | Install Python version |
| `uv python install 3.11 3.12 3.13` | Install multiple versions |
| `uv python list` | List installed versions |
| `uv python pin 3.12` | Pin for current project |
| `uv python uninstall 3.11` | Uninstall version |

## Sync & Installation

| Command | Purpose |
|---------|---------|
| `uv sync` | Install from uv.lock |
| `uv sync --frozen` | Install exact locked versions (for CI) |
| `uv sync --all-extras` | Include all optional groups |
| `uv sync --no-dev` | Exclude dev dependencies |
| `uv sync --dev` | Include dev dependencies |

## Lockfile Management

| Command | Purpose |
|---------|---------|
| `uv lock` | Create/update lockfile |
| `uv lock --upgrade` | Upgrade all dependencies |
| `uv lock --upgrade-package requests` | Upgrade specific package |
| `uv lock --check` | Verify lockfile is current |

## Export & Compatibility

| Command | Purpose |
|---------|---------|
| `uv export --format requirements-txt > requirements.txt` | Export as requirements.txt |
| `uv export --format requirements-txt --hash` | Export with hashes |
| `uv pip list` | List installed packages |
| `uv pip freeze` | Pip freeze format |

## Cache Management

| Command | Purpose |
|---------|---------|
| `uv cache clean` | Clear package cache |
| `uv cache dir` | Show cache location |
| `uv cache clean ruff` | Clear specific package cache |

## Inspection

| Command | Purpose |
|---------|---------|
| `uv tree` | Show dependency tree |
| `uv tree --outdated` | Show outdated packages |
| `uv tree --depth 2` | Limit tree depth |

## Build & Publish

| Command | Purpose |
|---------|---------|
| `uv build` | Build package (wheel + sdist) |
| `uv build --wheel` | Build wheel only |
| `uv publish` | Publish to PyPI |

## Self Update

| Command | Purpose |
|---------|---------|
| `uv self update` | Update uv itself |
| `uv --version` | Check uv version |
