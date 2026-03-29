---
name: python-lsp
description: Configure and optimize Python LSP servers for code intelligence, type checking, linting, and diagnostics. Covers tool selection, setup, and troubleshooting for ruff, ty, pyright, pylance, and other Python language servers.
---

# Python LSP Configuration & Setup

This plugin includes LSP server configurations for Python code intelligence. Python LSP servers provide:
- **Real-time diagnostics**: Errors and warnings as you type
- **Code navigation**: Go to definition, find references
- **Type information**: Hover for type hints and documentation
- **Completions**: Auto-completion and intelligent suggestions

## Configured LSP Servers

This plugin comes with configurations for:

### **ruff** (Linting + formatting)
- **Type**: Fast linter and formatter
- **Speed**: ⚡⚡⚡ Extremely fast
- **Best for**: Projects wanting fast linting feedback, modern Python codebases
- **Setup**: Runs via `uvx ruff server` with bundled `ruff.toml` configuration

### **ty** (Type checking)
- **Type**: Lightweight type checker
- **Speed**: ⚡⚡⚡ Very fast
- **Best for**: Quick type-aware development
- **Setup**: Runs via `uvx ty server`, auto-discovers `.venv`

## Enabling LSP Servers

The plugin automatically provides LSP configurations. To use them:

1. **Install the plugin**:
   ```bash
   /plugin install python-dev@clzmj
   ```

2. **Enable it**:
   - The plugin activates LSP servers automatically

3. **Install language server binaries**:
   ```bash
   # ruff and ty use uvx, so no separate installation needed
   # They're run automatically via: uvx ruff server and uvx ty server

   # Just ensure uv is installed:
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

## Your LSP Setup: ruff + ty

This plugin is configured with **ruff** (linting) and **ty** (type checking) — a fast, modern Python LSP combination.

**ruff** provides:
- Ultra-fast linting (10-100x faster than traditional linters)
- Comprehensive rules (400+)
- Code formatting
- Security checks

**ty** provides:
- Quick type-aware development
- Minimal startup overhead
- Type hint validation
- Code completions based on types

Both run via `uvx`, so they're always up-to-date with no system-wide installation needed.

## Customizing LSP Configuration

The plugin provides ruff and ty with bundled configurations. Both are enabled by default.

To customize in Claude Code (`~/.claude/settings.json`):
```json
{
  "lsp": {
    "ruff": {
      "enabled": true
    },
    "ty": {
      "enabled": true
    }
  }
}
```

To override ruff configuration, create a `ruff.toml` in your project root. The plugin's bundled `ruff.toml` will be used if no project-specific one exists.

## Troubleshooting LSP

### "LSP server not starting"
1. Ensure uv is installed:
   ```bash
   uv --version
   ```

2. Verify uvx works:
   ```bash
   uvx --version
   uvx ruff --version
   uvx ty --version
   ```

3. Restart Claude Code or reload the plugin

### "Ruff and ty not detecting issues"
1. Check that the project has a `.venv` or Python installation
2. Verify `uv sync` was run to install dependencies
3. Try: `uv run ruff check .` and `uv run ty` manually to test

### "Want stricter or more lenient checking"
- **Ruff**: Modify `ruff.toml` in your project root
- **Ty**: Configure in `ty.toml` if needed

## Supporting Documentation

Refer to the supporting reference document for detailed information:
- **lsp-tools.md** - In-depth comparison and setup for each tool

## Using with uv

The uv skill in this plugin provides Python project management. Use them together:
1. Set up project with uv: `uv init`, `uv add`
2. Configure LSP servers from this skill
3. Get both fast package management + code intelligence

### Example workflow
```bash
# Initialize with uv
uv init my-project
cd my-project
uv add fastapi uvicorn

# Now you have LSP diagnostic for your Python code
# and uv managing your dependencies
```

## Quick Reference

| Task | Command/Action |
|------|--------|
| Restart LSP | Reload editor or run `/plugin reload` |
| Change LSP tool | Edit LSP configuration in settings |
| Verify installation | `which <tool>` or use agent help |
| Debug issues | Check editor logs and LSP output |

## Best Practices

1. **Pin LSP tool** in your project if team-wide setup
2. **Use `pyright` or `ruff`** for consistency across CI and local
3. **Configure strictness** to match your team's standards
4. **Combine with linting** - ruff catches issues faster, pyright catches type issues
5. **Document choices** - note which LSP in README or CONTRIBUTING.md
