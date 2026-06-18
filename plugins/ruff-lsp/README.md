# ruff-lsp

Registers the **ruff** language server for Python in Claude Code, providing fast real-time linting and formatting diagnostics on `.py`/`.pyi` files.

## Installation

```bash
/plugin marketplace add clzmj/claude-code-plugins
/plugin install ruff-lsp@clzmj
```

Requires [uv](https://docs.astral.sh/uv/) — the server runs via `uvx ruff server`, so there's no separate ruff install:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## What you get

- 400+ lint rules (pyflakes, pycodestyle, bugbear, security, isort, …)
- black-compatible formatting
- ~10ms startup, diagnostics pushed to Claude after each edit

The LSP config is declared inline in [`plugin.json`](.claude-plugin/plugin.json) under `lspServers`, pointing at the bundled [`ruff.toml`](ruff.toml).

## Configuration

Override the bundled rules per-project with a `ruff.toml` or `[tool.ruff]` section in your project root. See the bundled `ruff.toml` for the default rule set, and the `ruff-lsp` skill for setup and troubleshooting.

## Note on running ruff + ty together

Claude Code uses **one LSP server per file extension**. If you install both `ruff-lsp` and `ty-lsp`, both claim `.py`/`.pyi` and only one is used (you'll see a plugin note). Pick the one you want live and run the other on demand (`uvx ty check`).

## License

Apache-2.0 — Carlos Lezama (carlos@carrots.sh)
