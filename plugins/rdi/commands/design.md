---
description: Design detailed implementation plan from research findings
model: claude-opus-4-5
---

# Design Implementation Plan

You are creating a detailed implementation plan based on research findings. The plan will be interactive, thorough, and saved to the same directory as the research.

## Initial Response

When this command is invoked, respond with:

```
I'll create a detailed implementation plan.

Please provide the path to your research.md file:
Example: .claude/thoughts/1234567890_dark_mode/research.md

Or provide:
1. The task/feature to implement
2. Any relevant context or requirements

I'll create a comprehensive, actionable plan.
```

Then wait for user input.

## Planning Process

### Step 1: Read Research (if provided)

1. **If research.md path is provided**:
   - Read the research.md file COMPLETELY (no limit/offset)
   - Extract the research directory path (e.g., `.claude/thoughts/1234567890_dark_mode`)
   - Note the short name and epoch from the directory
   - Understand all findings, patterns, and constraints

2. **If no research provided**:
   - Ask user for task description
   - Optionally spawn research agents to gather context
   - Determine where to save the plan

### Step 2: Understand Requirements

Ask clarifying questions:

```
Based on [the research | your description], I need to clarify:

1. [Specific question about requirements]
2. [Question about constraints or preferences]
3. [Question about success criteria]

Please provide these details so I can create an accurate plan.
```

### Step 3: Present Approaches

```
Based on the research findings, here are implementation options:

**Option 1: [Approach Name]**
- Pros: [Benefits]
- Cons: [Tradeoffs]
- Fits pattern: [Pattern from research at file:line]
- Complexity: [High/Medium/Low]

**Option 2: [Approach Name]**
- Pros: [Benefits]
- Cons: [Tradeoffs]
- Fits pattern: [Different pattern from research at file:line]
- Complexity: [High/Medium/Low]

Which approach aligns with your goals?
```

Wait for user decision.

### Step 4: Structure the Plan

```
Here's the proposed plan structure:

## Implementation Phases
1. [Phase name] - [What it accomplishes]
2. [Phase name] - [What it accomplishes]
3. [Phase name] - [What it accomplishes]

Each phase will include:
- Specific file changes
- Automated verification steps
- Manual testing checklist

Does this phasing make sense? Any adjustments?
```

Get feedback before proceeding.

### Step 5: Write plan.md

Write to `${RESEARCH_DIR}/plan.md` (same directory as research.md):

```markdown
# Implementation Plan: [Feature Name]

**Date**: [Current date and time]
**Research**: [Link to research.md in same directory]
**Approach**: [Which option was chosen]

## Overview

[Brief description of what we're implementing and why, referencing research findings]

## Current State Analysis

[Summary from research.md - what exists now]

**Key findings from research**:
- [Finding 1 from research.md with file:line]
- [Finding 2 from research.md with file:line]
- [Finding 3 from research.md with file:line]

## Desired End State

[Specification of desired outcome after implementation]

**Success looks like**:
- [Specific, measurable outcome 1]
- [Specific, measurable outcome 2]
- [Specific, measurable outcome 3]

**Verification**:
- [How to verify the implementation is complete]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

- ❌ [Out of scope item 1]
- ❌ [Out of scope item 2]
- ❌ [Out of scope item 3]

## Implementation Approach

**Chosen Approach**: [Option X - Name]

**Rationale**: [Why this approach was selected based on research]

**Follows Pattern**: [Pattern from research.md at file:line]

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes - be specific]

### Changes Required

#### 1. [Component/File Group Name]

**File**: `path/to/file.ext`

**Current State** (from research):
[What currently exists in this file]

**Required Changes**:
[Detailed description of what needs to change]

```[language]
// Example of changes to make
// Based on pattern from [file:line] in research
[code example showing the change]
```

**Why**: [Reason for this change]

#### 2. [Another Component]

**File**: `path/to/another.ext`

**Current State**: [What exists]

**Required Changes**: [What to change]

### Dependencies

**Must be done before Phase 2**:
- [Why this phase must complete first]

**Depends on**:
- [Any external dependencies or prerequisites]

### Success Criteria

#### Automated Verification
- [ ] Tests pass: `npm test` (or specific test command)
- [ ] Linting passes: `npm run lint`
- [ ] Type checking passes: `npm run typecheck`
- [ ] Build succeeds: `npm run build`
- [ ] [Any other automated checks]

#### Manual Verification
- [ ] [Specific manual test 1 - be very explicit]
- [ ] [Specific manual test 2 - include steps]
- [ ] [Specific manual test 3 - expected behavior]
- [ ] [Edge case to verify manually]

**Pause Point**: After automated verification passes, stop and wait for manual testing confirmation before proceeding to Phase 2.

---
## Phase 2: [Descriptive Name]
### Overview
[What this phase accomplishes]
### Changes Required
#### 1. [Component Name]
**File**: `path/to/file.ext`
**Current State**: [After Phase 1 changes]
**Required Changes**: [Specific changes]
```[language]
// Code changes for this phase
```
### Success Criteria
#### Automated Verification
- [ ] [Automated check 1]
- [ ] [Automated check 2]
#### Manual Verification
- [ ] [Manual test 1]
- [ ] [Manual test 2]
**Pause Point**: Wait for manual testing confirmation before Phase 3.
---

## Phase 3: [Descriptive Name]

[Similar structure...]

---
## Testing Strategy
### Unit Tests
**New tests to write**:
#### Test: [Test Name]
**File**: `path/to/test.spec.ts`
**Tests**: [What this test verifies]
```[language]
// Example test structure based on pattern from research
describe('[Feature]', () => {
  it('should [behavior]', () => {
    // Test implementation
  });
});
```
**Edge cases to cover**:
- [ ] [Edge case 1]
- [ ] [Edge case 2]
- [ ] [Edge case 3]
### Integration Tests
**Scenarios to test**:
1. [End-to-end scenario 1]
   - Steps: [Detailed steps]
   - Expected: [Expected outcome]
2. [End-to-end scenario 2]
   - Steps: [Detailed steps]
   - Expected: [Expected outcome]
### Manual Testing Steps
**Complete testing checklist**:
1. **[Test scenario 1]**
   - [ ] Step 1: [Specific action]
   - [ ] Step 2: [Specific action]
   - [ ] Expected: [What should happen]
2. **[Test scenario 2]**
   - [ ] Step 1: [Specific action]
   - [ ] Step 2: [Specific action]
   - [ ] Expected: [What should happen]
3. **Edge Cases**
   - [ ] [Edge case 1 - how to test, expected behavior]
   - [ ] [Edge case 2 - how to test, expected behavior]
## Files to Modify
**Summary of all file changes**:
| File | Phase | Type of Change |
|------|-------|----------------|
| `path/to/file1.ts` | 1 | Modify existing function |
| `path/to/file2.ts` | 1 | Add new component |
| `path/to/test.spec.ts` | 2 | Add tests |
| `path/to/file3.ts` | 3 | Update integration |
## Performance Considerations
[Any performance implications based on research]
- [Consideration 1]: [Impact and mitigation]
- [Consideration 2]: [Impact and mitigation]
## Migration Notes
[If applicable, how to handle existing data/systems/users]
**Migration required**: [Yes/No]
**Migration steps** (if applicable):
1. [Step 1]
2. [Step 2]
3. [Rollback plan if needed]
## Rollback Plan
**If something goes wrong**:
1. [How to revert Phase 3]
2. [How to revert Phase 2]
3. [How to revert Phase 1]
**Data safety**: [How to ensure no data loss]
## Risk Assessment
**Potential risks identified**:
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to mitigate] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to mitigate] |
## References
**From research**:
- Research document: `./research.md`
- Key pattern: `file:line` - [Description]
- Similar implementation: `file:line` - [Description]
**External references**:
- [Documentation link]
- [Related issue/ticket]
## Open Questions
[None - all questions must be resolved before plan is finalized]
**If any questions remain, STOP and ask the user before completing the plan.**
## Implementation Checklist
Before starting implementation with `/implement`:
- [ ] All phases clearly defined
- [ ] All file changes specified
- [ ] All success criteria measurable
- [ ] All dependencies identified
- [ ] Testing strategy complete
- [ ] Rollback plan exists
- [ ] No open questions
- [ ] User approved the plan
```
### Step 6: Present Plan
```
Implementation Plan Complete!
I've created the detailed plan in:
[research_dir]/plan.md
**Plan Summary**:
- Approach: [Chosen approach]
- Phases: [Number] phases
- Files to modify: [Count]
- Estimated complexity: [High/Medium/Low]
**Key phases**:
1. [Phase 1 name] - [Brief description]
2. [Phase 2 name] - [Brief description]
3. [Phase 3 name] - [Brief description]
Please review the plan. Once approved, use:
/implement [research_dir]/plan.md
Would you like me to explain any part of the plan in more detail?
```
### Step 7: Iterate if Needed
If user requests changes:
- Update the plan.md file
- Address feedback
- Re-present the plan
- Continue until approved
## Important Guidelines
### File Location
- **ALWAYS save plan.md** to the same directory as research.md
- Extract directory path from research.md path
- Maintain the directory structure: `.claude/thoughts/{epoch}_{name}/`
### Read Research Completely
- **NEVER** use limit/offset when reading research.md
- Extract ALL relevant information
- Reference specific findings with file:line
- Build on research, don't duplicate it
### No Open Questions
- **STOP if you have questions** - ask the user
- Don't write plan with placeholders
- Every decision must be made
- Plan must be 100% actionable
### Be Specific
- Exact file paths for all changes
- Specific commands for verification
- Detailed manual testing steps
- Clear success criteria
### Interactive Process
- Present options before deciding
- Get feedback on structure
- Iterate until approved
- Work collaboratively
### Track Progress
- Use TodoWrite for planning tasks
- Mark completed when plan is approved
- Keep user informed
The plan.md will be consumed by `/implement` to execute the implementation phase by phase.
Note: This command is named `/design` to avoid conflicts with Claude Code's native `/plan` command.
