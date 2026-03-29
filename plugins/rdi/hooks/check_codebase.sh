#!/bin/bash
# Hook to check if current directory contains a codebase
# Returns: "true" if codebase exists, "false" otherwise
# This prevents searching across entire computer

# Check for common indicators of a codebase
# 1. package.json, Cargo.toml, go.mod, requirements.txt, etc.
# 2. src/, lib/, pkg/ directories
# 3. Any programming language source files

HAS_CODEBASE=false

# Check for package/project files
if find . -maxdepth 2 -type f \( \
    -name "package.json" -o \
    -name "Cargo.toml" -o \
    -name "go.mod" -o \
    -name "requirements.txt" -o \
    -name "Gemfile" -o \
    -name "pom.xml" -o \
    -name "build.gradle" -o \
    -name "*.csproj" -o \
    -name "*.sln" -o \
    -name "composer.json" -o \
    -name "pyproject.toml" -o \
    -name "setup.py" -o \
    -name "CMakeLists.txt" -o \
    -name "Makefile" \
  \) 2>/dev/null | head -1 | grep -q .; then
  HAS_CODEBASE=true
fi

# Check for common source directories
if [ "$HAS_CODEBASE" = "false" ]; then
  if find . -maxdepth 2 -type d \( \
      -name "src" -o \
      -name "lib" -o \
      -name "pkg" -o \
      -name "app" -o \
      -name "components" -o \
      -name "pages" -o \
      -name "internal" \
    \) 2>/dev/null | head -1 | grep -q .; then
    HAS_CODEBASE=true
  fi
fi

# Check for source code files (broad detection)
if [ "$HAS_CODEBASE" = "false" ]; then
  # Look for any file with common programming extensions
  if find . -maxdepth 3 -type f \( \
      -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o \
      -name "*.py" -o -name "*.pyw" -o \
      -name "*.go" -o \
      -name "*.rs" -o \
      -name "*.java" -o \
      -name "*.kt" -o -name "*.kts" -o \
      -name "*.rb" -o \
      -name "*.php" -o \
      -name "*.c" -o -name "*.cpp" -o -name "*.cc" -o -name "*.h" -o -name "*.hpp" -o \
      -name "*.cs" -o \
      -name "*.swift" -o \
      -name "*.m" -o -name "*.mm" -o \
      -name "*.scala" -o \
      -name "*.clj" -o -name "*.cljs" -o \
      -name "*.ex" -o -name "*.exs" -o \
      -name "*.erl" -o -name "*.hrl" -o \
      -name "*.r" -o -name "*.R" -o \
      -name "*.jl" -o \
      -name "*.dart" -o \
      -name "*.lua" -o \
      -name "*.vim" -o \
      -name "*.sh" -o -name "*.bash" -o -name "*.zsh" \
    \) 2>/dev/null | head -1 | grep -q .; then
    HAS_CODEBASE=true
  fi
fi

# Output result
echo "$HAS_CODEBASE"
