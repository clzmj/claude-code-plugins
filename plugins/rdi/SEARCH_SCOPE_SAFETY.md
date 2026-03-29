# Search Scope Safety

This document explains how the RDI (Research-Design-Implement) plugin prevents searching across your entire computer and ensures searches are limited to the current working directory only.

## Problem

Without proper restrictions, the research command could potentially search:
- Parent directories (`../`)
- Your entire home directory
- Other codebases on your computer
- System files

This is both a privacy concern and could return irrelevant results.

## Solution

### 1. Codebase Detection Hook

**File**: `hooks/check_codebase.sh`

This hook intelligently detects if the current directory contains a codebase by checking for:

- **Project files**: package.json, Cargo.toml, go.mod, requirements.txt, Gemfile, pom.xml, build.gradle, etc.
- **Source directories**: src/, lib/, pkg/, app/, components/, pages/, internal/
- **Source code files**: Supports 30+ programming languages including:
  - JavaScript/TypeScript (*.ts, *.tsx, *.js, *.jsx)
  - Python (*.py, *.pyw)
  - Go (*.go)
  - Rust (*.rs)
  - Java (*.java)
  - Kotlin (*.kt, *.kts)
  - Ruby (*.rb)
  - PHP (*.php)
  - C/C++ (*.c, *.cpp, *.cc, *.h, *.hpp)
  - C# (*.cs)
  - Swift (*.swift)
  - Scala (*.scala)
  - Clojure (*.clj, *.cljs)
  - Elixir (*.ex, *.exs)
  - Erlang (*.erl, *.hrl)
  - R (*.r, *.R)
  - Julia (*.jl)
  - Dart (*.dart)
  - Lua (*.lua)
  - Shell scripts (*.sh, *.bash, *.zsh)
  - And more...

**Returns**: "true" if a codebase exists, "false" otherwise

### 2. Two Research Modes

Based on the codebase detection:

#### Mode 1: Codebase Research (HAS_CODEBASE="true")
- Searches are performed using file system tools (Glob, Grep, Read)
- **All searches are restricted to current working directory only**
- Agents receive explicit instructions to NOT search parent directories
- Results include file:line references

#### Mode 2: Web Research (HAS_CODEBASE="false")
- Falls back to WebSearch when no codebase exists
- Researches best practices, documentation, and patterns from the web
- No file system searches are performed

### 3. Agent-Level Restrictions

All three research agents have explicit search scope restrictions:

**`agents/codebase-locator.md`**
- Finds WHERE files live
- Restricted to current directory only

**`agents/codebase-pattern-finder.md`**
- Finds existing patterns and examples
- Restricted to current directory only

**`agents/codebase-analyzer.md`**
- Analyzes HOW code works
- Restricted to current directory only

Each agent's instructions include:

```markdown
## Search Scope

**CRITICAL RESTRICTION**: You MUST only search within the current working directory.

- **NEVER search parent directories** (no `../` or absolute paths outside CWD)
- **NEVER search other locations** on the computer
- **Always use relative paths** from current working directory
- **Stay within project boundaries** - only search the current codebase

When using Grep, Glob, or Read:
- Do NOT specify paths that go outside the current directory
- Use `.` or omit path parameter to search current directory
- NEVER use paths like `../`, `/Users/`, `/home/`, etc.
```

## Usage

When you run `/rdi:research`, the command will:

1. ✅ Check if current directory has a codebase using `check_codebase.sh`
2. ✅ Choose appropriate research mode (codebase vs web)
3. ✅ Restrict all file searches to current working directory
4. ✅ Spawn agents with explicit scope restrictions
5. ✅ Generate research.md with findings

## Safety Guarantees

- **Never searches parent directories**: The `..` pattern is explicitly forbidden
- **Never searches absolute paths**: Paths like `/Users/`, `/home/` are forbidden
- **Never searches other codebases**: Only current working directory is scanned
- **Falls back to web**: If no codebase exists, uses WebSearch instead
- **Language-agnostic**: Detects 30+ programming languages automatically

## Testing the Hook

You can test the codebase detection hook:

```bash
# In a directory with code
cd /path/to/your/project
$CLAUDE_PLUGIN_ROOT/hooks/check_codebase.sh
# Output: true

# In a directory without code (e.g., Downloads)
cd ~/Downloads
$CLAUDE_PLUGIN_ROOT/hooks/check_codebase.sh
# Output: false
```

## Files Modified

1. `commands/research.md` - Added codebase detection and mode selection
2. `agents/codebase-locator.md` - Added search scope restrictions
3. `agents/codebase-pattern-finder.md` - Added search scope restrictions
4. `agents/codebase-analyzer.md` - Added search scope restrictions
5. `hooks/check_codebase.sh` - New hook for codebase detection

## Summary

The RDI plugin now:
- ✅ Detects if current directory is a codebase
- ✅ Restricts all searches to current working directory only
- ✅ Falls back to web search when no codebase exists
- ✅ Supports 30+ programming languages
- ✅ Explicitly forbids parent directory and absolute path searches
- ✅ Provides safety at both command and agent levels
