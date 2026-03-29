#!/bin/bash
# Hook to create research directory with epoch timestamp
# Usage: Called when research phase starts
# Sets RESEARCH_DIR environment variable for Claude to use

# Get short name from first argument
SHORT_NAME="$1"

# Validate short name
if [[ -z "$SHORT_NAME" ]]; then
    echo "Error: Short name required (e.g., 'dark_mode_toggle')" >&2
    exit 1
fi

# Validate format (lowercase, underscores only)
if [[ ! "$SHORT_NAME" =~ ^[a-z0-9_]+$ ]]; then
    echo "Error: Short name must be lowercase letters, numbers, and underscores only" >&2
    exit 1
fi

# Generate epoch timestamp
EPOCH=$(date +%s)

# Create directory path
RESEARCH_DIR=".claude/thoughts/${EPOCH}_${SHORT_NAME}"

# Create the directory
mkdir -p "$RESEARCH_DIR"

# Output the directory path for Claude to use
echo "$RESEARCH_DIR"
