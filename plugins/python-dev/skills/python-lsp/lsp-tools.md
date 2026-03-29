# Python LSP Tools Reference

## Comparison Table

| Aspect | Ruff | Ty | Pyright | Pylance |
|--------|------|----|---------|---------
| **Type** | Linter + Formatter | Type Checker | Type Checker | Premium Type Checker |
| **Speed** | ⚡⚡⚡ Instant | ⚡⚡⚡ Instant | ⚡⚡ 1-3s | ⚡ 3-5s |
| **Type Checking** | ⭐⭐ Basic | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Excellent |
| **Linting** | ⭐⭐⭐ 400+ rules | ⭐ None | ⭐ Basic | ⭐ Basic |
| **Cost** | Free | Free | Free | $ (free tier available) |
| **Rust-based** | Yes | Yes | No | No |
| **Setup Complexity** | Easy (uvx) | Easy (uvx) | Moderate | Moderate |
| **AI Features** | No | No | No | Yes |
| **Configuration** | Extensive | Simple | Moderate | Extensive |

---

## Ruff

### Overview
A fast linter and formatter written in Rust. Designed as a drop-in replacement for flake8, isort, black, and more.

### Key Features
- **Speed**: 10-100x faster than traditional linters
- **Comprehensive linting**: 400+ rules covering style, complexity, security
- **Formatting**: Automatic code formatting
- **Python support**: Python 3.5+
- **Type hints**: Basic support, focuses on practical linting

### When to use
- ✅ Want fast feedback
- ✅ Using modern Python
- ✅ Prefer practical linting over type checking
- ✅ Want consistent formatting (like black)
- ✅ Need quick setup

### Configuration
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "W", "I"]  # Select rules
ignore = ["E501"]  # Ignore line-length

[tool.ruff.lint]
ignore = ["E402", "F841"]
```

### With plugin
```json
{
  "ruff": {
    "command": "uvx",
    "args": ["ruff", "server"],
    "extensionToLanguage": {
      ".py": "python",
      ".pyi": "python"
    }
  }
}
```

### Common rules

| Code | Category | Example |
|------|----------|---------|
| E | Errors | Line too long, indentation |
| W | Warnings | Whitespace, deprecated |
| F | PyFlakes | Undefined names, imports |
| I | isort | Import sorting |
| C | Complexity | McCabe complexity |
| S | Security | SQL injection, hardcoded passwords |

---

## Ty

### Overview
A lightweight Python type checker focused on practical type checking without the overhead.

### Key Features
- **Speed**: Extremely fast, minimal startup
- **Type checking**: Validates type hints
- **Simple configuration**: Minimal setup needed
- **Python support**: Python 3.5+
- **LSP mode**: Works well as language server

### When to use
- ✅ Want type checking without heavyweight analysis
- ✅ Need fast feedback
- ✅ Project has type hints
- ✅ Want to avoid Pyright complexity
- ✅ Like minimal configuration

### Configuration
```toml
# pyproject.toml - minimal setup needed
[tool.ty]
# Usually no configuration needed
```

### With plugin
```json
{
  "ty": {
    "command": "uvx",
    "args": ["ty", "server"],
    "extensionToLanguage": {
      ".py": "python",
      ".pyi": "python"
    }
  }
}
```

### Strengths
- Starts instantly
- Type-aware completions
- Good hover information
- Minimal dependencies

---

## Pyright

### Overview
A static type checker for Python developed by Microsoft. Implements PEP 484 type hints.

### Key Features
- **Thorough type checking**: Validates type hints rigorously
- **Standards-based**: Follows Python typing specs exactly
- **Multiple modes**: Basic, standard, strict
- **Detailed diagnostics**: Clear error messages
- **Python support**: Python 3.5+
- **py.typed marker**: Supports PEP 561 type hints

### When to use
- ✅ Want rigorous type checking
- ✅ Need to catch type errors early
- ✅ Publishing a typed library
- ✅ Want PEP 484 compliance
- ✅ Prefer open-source solution
- ✅ OK with moderate startup time

### Configuration

```toml
# pyproject.toml
[tool.pyright]
typeCheckingMode = "strict"  # or "basic", "standard"
pythonVersion = "3.10"
reportMissingImports = false
reportMissingTypeStubs = false
include = ["src"]
exclude = ["tests", "build"]
```

### Type checking modes

| Mode | Level | Use for |
|------|-------|---------|
| `off` | No checking | (Not recommended) |
| `basic` | Minimum | Legacy codebases |
| `standard` | Balanced | Most projects |
| `strict` | Maximum | Libraries, critical code |

### Installation
```bash
# npm
npm install -g pyright

# pip
pip install pyright

# uv
uv add --dev pyright
uv run pyright
```

### Common issues caught
- Undefined names: `NameError`
- Type mismatches: `int` assigned to `str` parameter
- Missing required arguments
- Attribute doesn't exist
- Incompatible return types

---

## Pylance

### Overview
A commercial language server built on top of Pyright, adding AI-powered features and premium support.

### Key Features
- **All Pyright features** plus:
- **AI-powered completions**: Intelligent code suggestions
- **Semantic highlighting**: Better visual distinction
- **Premium support**: From Astral
- **Advanced refactoring**: IDE-like capabilities
- **Workspace analysis**: Cross-module understanding

### When to use
- ✅ Want premium LSP features
- ✅ Team can afford license
- ✅ Using VS Code primarily
- ✅ Want AI-powered assistance
- ✅ Need advanced refactoring
- ✅ Prefer commercial support

### Cost
- **Free tier**: Basic features, limited
- **Premium**: Full features, €25-100/month depending on team size

### Installation
```bash
# VS Code
# Install "Pylance" extension from Marketplace

# Standalone
pip install pylance
```

### Configuration
```json
{
  "pylance": {
    "enabled": true,
    "args": ["--stdio"],
    "initializationOptions": {
      "typeCheckingMode": "strict"
    }
  }
}
```

---

## Pylint

### Overview
Classic, highly-configurable linter with extensive rules and plugins.

### Key Features
- **Comprehensive**: 100+ checks for various issues
- **Highly configurable**: Fine-grained control
- **Plugin system**: Extend with custom checkers
- **Legacy support**: Works with older Python
- **Ratings**: Code quality ratings

### When to use
- ✅ Need maximum customization
- ✅ Have legacy Python code
- ✅ Want detailed quality metrics
- ✅ Need plugins for specific checks
- ✅ Prefer traditional linting approach

### Configuration
```ini
# .pylintrc
[MESSAGES CONTROL]
disable=
    missing-docstring,
    too-many-arguments,
    unused-import

[FORMAT]
max-line-length=100
```

### Installation
```bash
pip install pylint
uv add --dev pylint
```

### Drawbacks
- **Slow**: Much slower than Ruff
- **False positives**: More aggressive than modern linters
- **Complex configuration**: Lots of options

---

## Comparison Scenarios

### Scenario 1: Fast Feedback Loop
**Choose**: Ruff + Ty
- Ruff for immediate linting (instant)
- Ty for type awareness (instant)
- Perfect for development

### Scenario 2: Type Safety Priority
**Choose**: Pyright (strict mode)
- Rigorous type checking
- Good error messages
- Moderate performance hit acceptable

### Scenario 3: Enterprise/Team Setting
**Choose**: Pylance + Pyright
- Premium support and features
- AI-powered assistance
- Advanced refactoring

### Scenario 4: Library Publishing
**Choose**: Ruff + Pyright (strict)
- Ruff for code quality
- Pyright (strict) for type correctness
- Both ensure API users catch issues

### Scenario 5: Legacy Codebase
**Choose**: Pylint (permissive) + Pyright (basic)
- Pylint's configurability handles quirks
- Pyright (basic mode) doesn't enforce strictly

---

## Combining Multiple LSP Servers

You can use multiple LSP servers simultaneously:

```json
{
  "ruff": { "enabled": true },      // Linting
  "ty": { "enabled": true },        // Type checking
  "pyright": { "enabled": false }   // Don't duplicate
}
```

**Good combinations**:
- Ruff (linting) + Ty (fast type checking)
- Ruff (linting) + Pyright (thorough type checking)
- Single LSP when editor limits it

**Avoid**:
- Ruff + Pylint together (duplicate linting rules)
- Ty + Pyright together (duplicate type checking)

---

## Migration Between Tools

### From Pylint to Ruff
```bash
# Old
pylint myproject/

# New
uv run ruff check myproject/
uv run ruff format myproject/
```

### From Black + Flake8 to Ruff
```bash
# Old
black myproject/
flake8 myproject/

# New
ruff format myproject/
ruff check myproject/
```

### Adding type checking to lint-only project
```bash
# Install Pyright
pip install pyright

# Run type check
pyright
```

---

## Performance Characteristics

### Startup time (approximate)
- Ruff: 10ms
- Ty: 50ms
- Pyright: 1-3s (first run, then cached)
- Pylance: 2-5s
- Pylint: 500ms

### Memory usage
- Ruff: ~50MB
- Ty: ~100MB
- Pyright: ~300MB
- Pylance: ~500MB
- Pylint: ~150MB

### Checking 1000 files
- Ruff: 100ms
- Ty: 200ms
- Pyright: 5-10s
- Pylint: 30-60s
- Pylance: 10-20s
