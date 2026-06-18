---
name: ruff-lsp
description: Set up, configure, and troubleshoot the ruff language server for Python linting and formatting in Claude Code. Use when configuring ruff diagnostics, editing ruff.toml, or debugging why ruff LSP isn't reporting issues.
---

# Ruff Language Server

This plugin registers **ruff** as the Python language server for `.py`/`.pyi` files, giving Claude real-time linting and formatting diagnostics as it edits.

Ruff provides:
- **Instant diagnostics** — 400+ lint rules (pyflakes, pycodestyle, bugbear, security, isort, and more)
- **Formatting** — black-compatible code formatting
- **Speed** — 10–100x faster than traditional linters; ~10ms startup

## How it runs

The plugin starts ruff via `uvx ruff server` with the bundled `ruff.toml`. No separate install is needed beyond uv:

```bash
# Ensure uv is installed
curl -LsSf https://astral.sh/uv/install.sh | sh
uvx ruff --version   # verify
```

Claude Code allows **one LSP server per file extension**. If you also install `ty-lsp`, both register `.py`/`.pyi` and only one will be used (you'll see a plugin note). Install whichever you want live; run the other on demand (`uvx ty check`).

## Configuring ruff

The plugin ships a `ruff.toml` (used via `${CLAUDE_PLUGIN_ROOT}/ruff.toml`). To override it for a project, drop a `ruff.toml` or `[tool.ruff]` section in your project root — your project config takes precedence for your code.

```toml
# pyproject.toml
[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I"]
ignore = ["E501"]
```

## Troubleshooting

**Server not starting** — verify uv works: `uv --version`, then `uvx ruff --version`. Reload the plugin or restart Claude Code.

**No diagnostics** — confirm the file is `.py`/`.pyi` and that ruff runs manually: `uvx ruff check path/to/file.py`.

**Want different rules** — edit `ruff.toml`/`[tool.ruff.lint]` in your project root.
