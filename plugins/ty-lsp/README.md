# ty-lsp

Registers the **ty** language server for Python in Claude Code, providing fast real-time type checking and type-aware navigation on `.py`/`.pyi` files.

## Installation

```bash
/plugin marketplace add clzmj/claude-code-plugins
/plugin install ty-lsp@clzmj
```

Requires [uv](https://docs.astral.sh/uv/) — the server runs via `uvx ty server`, so there's no separate ty install:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## What you get

- Type-hint validation and type-error diagnostics
- Go to definition, find references, hover for types
- Minimal startup (~50ms), diagnostics pushed to Claude after each edit

The LSP config is declared inline in [`plugin.json`](.claude-plugin/plugin.json) under `lspServers`.

## Configuration

ty auto-discovers your project's virtual environment and reads `ty.toml` (or `[tool.ty]` in `pyproject.toml`) from the project root. A sample [`ty.toml`](ty.toml) is bundled — copy it into your project and adjust. See the `ty-lsp` skill for setup and troubleshooting.

## Note on running ruff + ty together

Claude Code uses **one LSP server per file extension**. If you install both `ty-lsp` and `ruff-lsp`, both claim `.py`/`.pyi` and only one is used (you'll see a plugin note). Pick the one you want live and run the other on demand (`uvx ruff check`).

## License

Apache-2.0 — Carlos Lezama (carlos@carrots.sh)
