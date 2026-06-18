---
name: ty-lsp
description: Set up, configure, and troubleshoot the ty language server for Python type checking in Claude Code. Use when configuring ty diagnostics, working with ty.toml, or debugging type-aware navigation and type errors.
---

# ty Language Server

This plugin registers **ty** as the Python language server for `.py`/`.pyi` files, giving Claude real-time type checking plus type-aware navigation as it edits.

ty provides:
- **Type diagnostics** — validates type hints and flags type errors
- **Code navigation** — go to definition, find references, hover for types
- **Speed** — minimal startup (~50ms), Rust-based

## How it runs

The plugin starts ty via `uvx ty server`. No separate install is needed beyond uv:

```bash
# Ensure uv is installed
curl -LsSf https://astral.sh/uv/install.sh | sh
uvx ty --version   # verify
```

Claude Code allows **one LSP server per file extension**. If you also install `ruff-lsp`, both register `.py`/`.pyi` and only one will be used (you'll see a plugin note). Install whichever you want live; run the other on demand (`uvx ruff check`).

## Configuring ty

ty auto-discovers your project's virtual environment and reads a `ty.toml` (or `[tool.ty]` in `pyproject.toml`) from the **project root**. The plugin bundles a sample `ty.toml`:

```toml
[environment]
python = "./.venv"
```

Copy it into your project and adjust as needed — ty configuration is intentionally minimal.

## Troubleshooting

**Server not starting** — verify uv works: `uv --version`, then `uvx ty --version`. Reload the plugin or restart Claude Code.

**No type errors** — ensure the project has a `.venv` and dependencies installed (`uv sync`), then test manually: `uvx ty check`.

**Missing imports flagged** — confirm `[environment] python` points at the right interpreter/venv in your project `ty.toml`.
