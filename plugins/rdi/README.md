# Research-Design-Implement Plugin

A systematic workflow plugin for Claude Code that guides development through three structured phases: Research, Design, and Implementation.

## Overview

This plugin implements a methodical approach to code changes, ensuring thorough understanding, careful planning, and verified implementation. It's designed to help developers tackle complex features by breaking them into manageable, well-thought-out steps.

### Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ /rdi:rpi (or /rdi:research, /rdi:design, /rdi:implement)   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. RESEARCH PHASE                                           │
│    • Get task + short name from user                        │
│    • Hook creates: .claude/thoughts/{epoch}_{name}/         │
│    • Spawn parallel explore agents                          │
│    • Write comprehensive findings                           │
│    • OUTPUT: research.md                                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. PLAN PHASE                                               │
│    • Read research.md                                        │
│    • Present implementation options                          │
│    • Interactive planning with user                          │
│    • Define phases with success criteria                    │
│    • OUTPUT: plan.md (in same directory)                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. IMPLEMENT PHASE                                          │
│    • Read plan.md + research.md                             │
│    • For each phase:                                         │
│      - Implement changes                                     │
│      - Run automated verification                            │
│      - Pause for manual testing                              │
│      - Update plan.md with checkmarks                        │
│    • OUTPUT: Updated plan.md + code changes                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ✅ Complete!

Directory structure created:
.claude/thoughts/1733595123_dark_mode/
├── research.md  (comprehensive findings)
└── plan.md      (implementation plan with ✓ checkmarks)
```

## Installation

### From Marketplace

Add the marketplace and install the plugin:

```bash
/plugin marketplace add clzmj/claude-code-plugins
/plugin install rdi@clzmj
```

### Manual Installation

1. Clone or download this plugin to your local plugins directory
2. Add to your `.claude/settings.json`:

```json
{
  "plugins": [
    {
      "source": "/path/to/research-design-implement"
    }
  ]
}
```

## Usage

### Basic Usage

Invoke the workflow with:

```bash
/rdi:rpi
```

This will start the interactive Research-Design-Implement workflow.

### Workflow Phases

#### Phase 1: Research

The research phase thoroughly explores your codebase to understand:
- Current implementation patterns
- Relevant files and their purposes
- Existing conventions and architecture
- Dependencies and integration points

**Example:**
```
User: /rdi:rpi
Claude: I'll guide you through a systematic Research → Plan → Implement workflow...
        What would you like to work on?

User: I need to add a dark mode toggle to the settings page

Claude: Let me research the current codebase...
        [Spawns parallel explore agents]

        Research Findings:

        ### Current State
        - Theme system exists in src/theme/ThemeProvider.tsx:12
        - Settings page at src/pages/Settings.tsx:45
        - Existing toggle components in src/components/Toggle.tsx:8

        ### Relevant Files
        - `src/theme/ThemeProvider.tsx:12` - Current theme context implementation
        - `src/hooks/useTheme.ts:5` - Theme hook for components
        - `src/components/Toggle.tsx:8` - Reusable toggle component

        Ready to move to planning?
```

#### Phase 2: Plan

The planning phase creates a detailed implementation roadmap:
- Multiple implementation approaches with pros/cons
- Phased breakdown of changes
- Clear success criteria (automated and manual)
- Out-of-scope items to prevent feature creep

**Example:**
```
User: Yes, let's plan

Claude: Based on my research, here are implementation options:

        **Option 1: Extend Existing Theme System**
        - Pros: Follows existing patterns, minimal code changes
        - Cons: Limited to current theme capabilities

        **Option 2: New Theme Management System**
        - Pros: More flexible, better long-term
        - Cons: Larger refactor, more testing needed

        Which approach aligns with your needs?

User: Option 1

Claude: Here's my proposed plan structure:

        ## Implementation Phases
        1. Add dark mode state to ThemeProvider
        2. Create toggle component in Settings
        3. Add CSS variables for dark mode
        4. Update tests

        Does this phasing make sense?

User: Yes

Claude: I've created the detailed implementation plan.

        The plan includes:
        - Specific file changes for each phase
        - Automated verification (tests, linting, type checking)
        - Manual verification steps (UI testing, edge cases)
        - Migration notes for existing themes

        Ready to implement?
```

#### Phase 3: Implement

The implementation phase executes the plan systematically:
- One phase at a time
- Automated verification after each phase
- Manual testing checkpoints
- Clear progress tracking

**Example:**
```
User: Yes, let's implement

Claude: Starting Phase 1: Add dark mode state to ThemeProvider

        [Makes changes to src/theme/ThemeProvider.tsx]
        [Runs automated verification]

        Phase 1 Complete - Ready for Manual Verification

        Automated verification passed:
        - ✓ Tests pass: npm test
        - ✓ Linting passes: npm run lint
        - ✓ Type checking passes: npm run typecheck

        Please perform manual verification:
        - [ ] Theme context provides dark mode state
        - [ ] No console errors when theme changes

        Let me know when testing is complete so I can proceed to Phase 2.

User: Tested, looks good

Claude: Great! Moving to Phase 2: Create toggle component in Settings
        [Continues with next phase...]
```

## Features

### Parallel Research Agents

The research phase uses Claude Code's Task tool with the Explore agent to:
- Find relevant files across the codebase
- Understand current implementations
- Discover existing patterns
- Run multiple searches concurrently for efficiency

### Interactive Planning

Planning is collaborative:
- Multiple approach options presented
- User feedback incorporated at each step
- Clear structure approval before detail work
- Iterative refinement until satisfactory

### Phased Implementation

Implementation is broken into verified phases:
- Automated checks (tests, linting, type checking)
- Manual verification checkpoints
- Progress tracking with TodoWrite
- Adaptation when reality differs from plan

### Discrepancy Handling

When the plan doesn't match reality:
- Clear communication of the issue
- Explanation of why it matters
- Multiple adaptation options presented
- User decision on how to proceed

## Skill Reference

### `/rdi:rpi` - Complete Workflow

**Description:** Start the full Research-Plan-Implement workflow

**Interactive:** Yes - guides you through all three phases with checkpoints

**Phases:**
1. **Research** - Explore and understand the codebase
2. **Plan** - Create detailed implementation roadmap
3. **Implement** - Execute plan with verification

### `/rdi:research` - Research Only

**Description:** Research and understand the codebase without planning or implementation

**Use when:** You want to explore and document the current implementation before deciding on changes

### `/rdi:design` - Planning Only

**Description:** Design a detailed implementation plan (with optional research)

**Use when:** You understand the codebase and want to create an implementation roadmap

**Note:** Named `/rdi:design` to avoid conflicts with Claude Code's native `/plan` command

### `/rdi:implement` - Implementation Only

**Description:** Execute an existing implementation plan with verification

**Use when:** You have an approved plan and want to implement it systematically

## Agents

The plugin includes specialized agents used during the research phase:

### `codebase-locator`

Finds WHERE code lives in the codebase. Locates and categorizes files by:
- Implementation files
- Test files
- Configuration
- Type definitions
- Documentation

### `codebase-analyzer`

Analyzes HOW code works. Provides:
- Data flow tracing
- Function documentation
- Component interactions
- State management patterns
- Error handling approaches

### `codebase-pattern-finder`

Discovers existing PATTERNS to follow. Identifies:
- Similar implementations
- Coding conventions
- Testing approaches
- Integration patterns
- Template structures

## Hooks

The plugin includes utility hooks:

### `create_research_dir.sh`

Creates the research directory with epoch timestamp:
- Input: Short name (e.g., "dark_mode_toggle")
- Output: Directory path (e.g., ".claude/thoughts/1733595123_dark_mode_toggle")
- Validates naming format (lowercase, underscores only)
- Used automatically by the `/rdi:research` and `/rdi:rpi` skills

## Examples

### Example 1: Adding a New Feature

```bash
/rdi:rpi
```

```
User: I need to add user authentication with JWT tokens

Claude: [RESEARCH PHASE]
        Let me research authentication in your codebase...

        Research Findings:
        - Found Express middleware pattern in src/middleware/
        - Existing user model in src/models/User.ts
        - JWT library already in package.json

        [PLAN PHASE]
        Option 1: Add JWT to existing auth
        Option 2: New auth service with JWT

        Which approach?

        [IMPLEMENT PHASE]
        Phase 1: Add JWT signing to auth service
        Automated ✓ | Manual testing needed

        Phase 2: Create JWT middleware
        Automated ✓ | Manual testing needed

        Complete!
```

### Example 2: Refactoring Existing Code

```bash
/rdi:rpi
```

```
User: I want to refactor the data fetching to use React Query

Claude: [RESEARCH PHASE]
        Analyzing current data fetching...

        Found:
        - 15 components using useEffect + fetch
        - Custom hooks in src/hooks/useApi.ts
        - No caching layer

        [PLAN PHASE]
        Phased migration approach:
        1. Install React Query
        2. Create query hooks for API endpoints
        3. Migrate components one by one
        4. Remove old useApi hook

        [IMPLEMENT PHASE]
        Phase 1: Setup React Query
        Phase 2: Create query hooks (5 endpoints)
        Phase 3: Migrate components (15 files)
        Phase 4: Cleanup old code
```

### Example 3: Bug Fix with Investigation

```bash
/rdi:rpi
```

```
User: Users are seeing duplicate items in the list

Claude: [RESEARCH PHASE]
        Investigating list rendering...

        Found:
        - List component in src/components/ItemList.tsx:34
        - Data fetch in src/hooks/useItems.ts:12
        - Key prop using index instead of item.id

        Root cause: Array index keys causing React to rerender incorrectly

        [PLAN PHASE]
        Fix approach:
        1. Update key prop to use item.id
        2. Add unique constraint check
        3. Add test for duplicate prevention

        [IMPLEMENT PHASE]
        Phase 1: Fix key props
        Automated ✓ | Manual ✓

        Phase 2: Add tests
        Automated ✓

        Bug fixed!
```

## Best Practices

### When to Use This Workflow

✅ **Good for:**
- Complex features touching multiple files
- Refactoring with significant scope
- Features requiring architectural decisions
- Tasks needing careful planning
- Changes with unclear requirements initially

❌ **Not needed for:**
- Simple bug fixes with obvious solutions
- Typo corrections
- Minor documentation updates
- One-line changes

### Getting the Most Value

1. **Provide context upfront**: Share tickets, requirements, constraints
2. **Engage in research**: Confirm findings match your understanding
3. **Review the plan**: Don't rush to implementation
4. **Test thoroughly**: Manual verification is crucial
5. **Communicate issues**: If something doesn't match, speak up

### Tips for Success

- **Be specific** about your requirements
- **Ask questions** during planning if anything is unclear
- **Review** each phase before approving next steps
- **Test manually** - automated tests don't catch everything
- **Provide feedback** to improve the plan

## Configuration

The skills are invoked automatically by Claude based on task context, or explicitly via their slash names (`/rdi:rpi`, `/rdi:research`, `/rdi:design`, `/rdi:implement`). No per-skill configuration is required.

## Troubleshooting

### "Too much research, can we skip to implementation?"

The research phase prevents costly mistakes. However, if you're very familiar with the code:
```
User: I already know the codebase well, can we go straight to planning?
Claude: Absolutely, let me create a plan based on what you know...
```

### "The plan doesn't match what I see in the code"

This is expected sometimes - codebases evolve:
```
Claude: Issue in Phase 2:
        Expected: Authentication in src/auth/
        Found: Actually in src/services/auth/

        Should I adapt the plan to match current structure?
```

### "Implementation is taking too long"

Each phase has clear checkpoints. You can pause and resume:
```
User: Let's stop after Phase 2, I need to review
Claude: No problem. Phase 2 complete and verified.
        Resume with Phase 3 whenever you're ready.
```

## Contributing

To contribute improvements to this plugin:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Apache-2.0

## Author

Carlos Lezama (carlos@carrots.sh)

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review example workflows above

## Version History

### 1.0.0 (2025-12-07)
- Initial release
- Research-Plan-Implement workflow
- Parallel agent research
- Interactive planning
- Phased implementation with verification
