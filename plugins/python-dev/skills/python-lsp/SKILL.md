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
- **Setup**: Runs via `uvx ruff server`

### **ty** (Type checking)
- **Type**: Lightweight type checker
- **Speed**: ⚡⚡⚡ Very fast
- **Best for**: Quick type-aware development
- **Setup**: Runs via `uvx ty server`

### **pyright** (Static type checker)
- **Type**: Comprehensive type checker
- **Speed**: ⚡⚡ Moderate
- **Best for**: Rigorous type checking, detailed diagnostics
- **Setup**: Requires `pyright` installation

### **pylance** (Commercial LSP)
- **Type**: Premium type checker (based on Pyright)
- **Speed**: ⚡ Slower (more thorough)
- **Best for**: Maximum features and AI-powered refactoring
- **Setup**: Requires `pylance` installation

## Enabling LSP Servers

The plugin automatically provides LSP configurations. To use them:

1. **Install the plugin**:
   ```bash
   /plugin install python-dev@clzmj
   ```

2. **Enable it**:
   - The plugin activates LSP servers automatically

3. **Install language server binaries** (as needed):
   ```bash
   # For ruff and ty (uses uvx, no install needed):
   # They work automatically

   # For pyright:
   npm install -g pyright
   # or
   pip install pyright

   # For pylance:
   # Install VS Code extension or use pip
   pip install pylance
   ```

## Choosing Your LSP Server

### Decision factors:

**Speed needed?**
- Ruff or ty → Very fast, instant feedback
- Pyright → Good balance
- Pylance → Full-featured but slower

**Type checking required?**
- Want rigorous checking → Pyright or Pylance
- Want basic type hints → Ty
- Don't need type checking → Ruff (linting only)

**Project type?**
- Application → Pyright or Pylance for reliability
- Library → Pyright (catches compatibility issues)
- Scripts → Ruff (fast, practical)
- Data science → Pylance (best with scientific packages)

**Team preference?**
- Minimal setup → Ruff (works out of box with uvx)
- Maximum features → Pylance
- Balance → Pyright

## Customizing LSP Configuration

While this plugin provides sensible defaults, you can customize LSP settings in your editor/Claude Code settings.

### Editor-specific configuration

**Claude Code** (`opencode.jsonc` or settings.json):
```json
{
  "lsp": {
    "ruff": {
      "enabled": true,
      "args": ["server"]
    },
    "pyright": {
      "enabled": true,
      "initializationOptions": {
        "typeCheckingMode": "strict"
      }
    }
  }
}
```

**VS Code** (`.vscode/settings.json`):
```json
{
  "[python]": {
    "defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "linting.enabled": true,
    "linting.pylintEnabled": false
  }
}
```

## Troubleshooting LSP

### "LSP server not starting"
1. Check that the binary is installed:
   ```bash
   which ruff
   which pyright
   ```

2. For uvx-based servers (ruff, ty), ensure uv is installed:
   ```bash
   uv --version
   ```

3. Restart your editor/Claude Code

### "Type checking too strict/lenient"
Adjust LSP initialization options or use `py.typed` marker:
```toml
# pyproject.toml for Pyright strictness
[tool.pyright]
typeCheckingMode = "strict"  # or "basic", "standard"
```

### "LSP conflicts with formatter"
Configure only one formatter:
```json
{
  "lsp": {
    "ruff": { "enabled": true },
    "black": { "enabled": false }
  }
}
```

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
