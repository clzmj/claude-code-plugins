---
description: Research phase - explore and understand the codebase
model: claude-opus-4-5
---

# Codebase Research

You are conducting comprehensive research across the codebase to understand the current implementation before making changes.

## Initial Response

When this command is invoked, respond with:

```
I'll research your codebase to understand the current implementation.

Please provide:
1. What feature or area you want to understand
2. A short name for this research (lowercase, underscores, e.g., "dark_mode_toggle")
3. Specific files or components to focus on (if known)

I'll explore the codebase and save detailed findings to a research document.
```

Then wait for the user's research query and short name.

## Research Process

1. **Get short name from user** for the research topic (e.g., "user_auth", "dark_mode", "api_refactor")

2. **Check for codebase context using hook**:
   ```bash
   # Check if current directory has a codebase
   # This prevents searching across entire computer
   HAS_CODEBASE=$(${CLAUDE_PLUGIN_ROOT}/hooks/check_codebase.sh)
   ```

   The hook checks for:
   - Project files (package.json, Cargo.toml, go.mod, etc.)
   - Source directories (src/, lib/, pkg/, etc.)
   - Source code files (*.ts, *.js, *.py, *.go, *.rs, *.java, *.rb, *.php, *.c, *.cpp, and many more)

3. **Create research directory using hook**:
   ```bash
   RESEARCH_DIR=$(${CLAUDE_PLUGIN_ROOT}/hooks/create_research_dir.sh "${SHORT_NAME}")
   ```
   This creates `.claude/thoughts/{epoch}_{short_name}/` and returns the path.

4. **Determine research mode**:
   - If `HAS_CODEBASE="true"`: Proceed with codebase research (search ONLY in current working directory)
   - If `HAS_CODEBASE="false"`: Use WebSearch for research instead of file searches
   - NEVER search in parent directories or other locations on the computer

5. **Read any mentioned files completely** (only if HAS_CODEBASE=true):
   - Use Read tool WITHOUT limit/offset parameters
   - Get full context before spawning sub-tasks

6. **Create research plan** using TodoWrite:
   - List areas to investigate
   - Track exploration progress

7. **Spawn parallel research agents** (only if HAS_CODEBASE=true) using Task tool with `subagent_type="Explore"`:

   **CRITICAL: All searches must be restricted to current working directory only!**

   **Find WHERE files live**:
   ```
   "Find all files related to [feature/component] in the current working directory only.
   Do NOT search parent directories or other locations.
   Focus on: implementation files, tests, configuration, and type definitions.
   Return file paths grouped by purpose."
   ```

   **Understand HOW it works**:
   ```
   "Analyze how [specific feature] is currently implemented in the current working directory.
   Do NOT search parent directories or other locations.
   Trace the data flow, identify key functions, and document patterns.
   Include file:line references."
   ```

   **Discover PATTERNS to follow**:
   ```
   "Find examples of similar features or patterns in the current working directory only.
   Do NOT search parent directories or other locations.
   Look for: naming conventions, testing approaches, and integration patterns.
   Document what exists."
   ```

7a. **Alternative: Web-based research** (only if HAS_CODEBASE=false):

   Use WebSearch tool to research the topic:
   ```
   "Research [topic]: best practices, implementation approaches, common patterns.
   Look for: official documentation, tutorials, example implementations."
   ```

8. **Wait for all agents to complete**

9. **Write research.md** to `${RESEARCH_DIR}/research.md`:

```markdown
# Research: [Topic Name]

**Date**: [Current date and time]
**Epoch**: [Epoch timestamp]
**Research ID**: [epoch]_[short_name]

## Research Question

[Original user query - what they wanted to understand]

## Summary

[High-level overview of findings - 2-3 paragraphs answering the research question]

## Current State

### Architecture Overview
[How the current system is architected]

### Key Components

#### [Component 1 Name]
**Location**: `path/to/file.ts:line`
**Purpose**: [What this component does]
**Key Functions**:
- `functionName()` at line X - [What it does]
- `anotherFunction()` at line Y - [What it does]

#### [Component 2 Name]
**Location**: `path/to/file.ts:line`
**Purpose**: [What this component does]

### Data Flow

1. **Input**: [Where data comes from]
2. **Processing**: [How data is transformed]
   - Step 1: [What happens] (`file.ts:123`)
   - Step 2: [What happens] (`file.ts:145`)
3. **Output**: [Where data goes]

## Relevant Files

### Implementation Files
- `path/to/file.ts:123` - [What this file does]
- `path/to/service.ts:45` - [What this file does]
- `path/to/model.ts:12` - [What this file does]

### Test Files
- `path/to/test.spec.ts:12` - [What this tests]
- `path/to/integration.test.ts:34` - [What this tests]

### Configuration Files
- `config/settings.json` - [What this configures]
- `.env.example` - [Environment variables needed]

### Type Definitions
- `types/feature.d.ts:10` - [Type definitions]

## Patterns and Conventions

### Naming Conventions
- [Pattern 1]: [How it's used]
- [Pattern 2]: [How it's used]

### Code Patterns Found

#### Pattern: [Pattern Name]
**Used in**: [File references]
**Description**: [How this pattern works]

```[language]
// Example from path/to/file.ts:123-145
[code snippet showing the pattern]
```

**Variations**:
- [Variation A]: [When/where used]
- [Variation B]: [When/where used]

### Testing Patterns
- [How tests are structured]
- [Testing utilities used]
- [Common test patterns]

### Integration Patterns
- [How components connect]
- [How external services are used]
- [Common integration approaches]

## Dependencies

### Internal Dependencies
- [Component A] depends on [Component B] (`file:line`)
- [Service X] uses [Utility Y] (`file:line`)

### External Dependencies
- **[Library/Package Name]** - [How it's used, why it's needed]
- **[Another Library]** - [Purpose and usage]

## State Management

[How state is managed in this area]
- State structure: [What the state looks like]
- State updates: [How state is modified]
- State location: `path/to/state.ts:line`

## Error Handling

[How errors are handled in this area]
- Error types: [What errors are caught]
- Error handling: [How they're processed]
- Error location: `path/to/errors.ts:line`

## Configuration

[How this feature/area is configured]
- Configuration files: [List of config files]
- Environment variables: [List of env vars]
- Runtime configuration: [How config is loaded/used]

## Key Discoveries

- ✓ [Important discovery 1]
- ✓ [Important discovery 2]
- ✓ [Important discovery 3]

## Constraints and Limitations

- [Constraint 1]: [Why this exists, impact]
- [Constraint 2]: [Why this exists, impact]

## Technical Debt (if any observed)

- [Technical debt item 1 - just document what exists, no judgment]
- [Technical debt item 2]

## Next Steps for Planning

Based on this research, when planning new features or changes in this area:

1. [Recommendation based on patterns found]
2. [Recommendation based on existing architecture]
3. [Recommendation based on conventions discovered]

## References

- [Link to related documentation]
- [Link to relevant issues/tickets]
- [Link to similar implementations]
```

10. **Present findings to user**:

**For codebase research (HAS_CODEBASE=true):**
```
Research Complete!

I've documented my findings in:
.claude/thoughts/[epoch]_[short_name]/research.md

Summary:
[2-3 sentence summary of key findings]

Key Files:
- `file1.ts:123` - [Brief description]
- `file2.ts:45` - [Brief description]

Ready to design a plan based on this research?
Use: /rdi:design .claude/thoughts/[epoch]_[short_name]/research.md
```

**For web research (HAS_CODEBASE=false):**
```
Research Complete!

I've documented my findings from web research in:
.claude/thoughts/[epoch]_[short_name]/research.md

Summary:
[2-3 sentence summary of key findings from web]

Key Resources:
- [Resource 1] - [Brief description]
- [Resource 2] - [Brief description]

Ready to design a plan based on this research?
Use: /rdi:design .claude/thoughts/[epoch]_[short_name]/research.md
```

## Important Guidelines

- **ALWAYS check for codebase context first** using the bash check
- **NEVER search outside current working directory** - this is critical!
- **ALWAYS create the research directory** with epoch timestamp
- **ALWAYS write research.md** to the directory
- **Use parallel Task agents for codebase exploration** (only if HAS_CODEBASE=true)
- **Use WebSearch for research** if no codebase exists (HAS_CODEBASE=false)
- Read files completely (no limit/offset)
- Include specific file:line references for codebase research
- Document patterns without critique
- Wait for ALL agents before synthesizing
- Present findings clearly with path to research.md
- Explicitly tell agents to search ONLY in current working directory

## Search Scope Safety

**CRITICAL**: To prevent searching across the entire computer:

1. **Always check for codebase presence** before doing file searches
2. **Only search in current working directory** when codebase exists
3. **Never use parent directory references** (like `../`) in searches
4. **Pass explicit instructions to agents** about search scope
5. **Use WebSearch as fallback** when no local codebase exists

The research.md file will be consumed by the `/rdi:design` command to create an implementation plan.
