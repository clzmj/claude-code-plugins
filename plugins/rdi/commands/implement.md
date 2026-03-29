---
description: Implementation phase - execute plan with verification
model: claude-opus-4-5
---

# Plan Implementation

You are implementing an approved plan by reading plan.md and executing it phase by phase with verification.

## Initial Response

When this command is invoked, respond with:

```
I'll implement your plan systematically.

Please provide the path to your plan.md file:
Example: .claude/thoughts/1234567890_dark_mode/plan.md

I'll execute the plan phase by phase with full verification.
```

Then wait for the plan.md path.

## Implementation Process

### Setup

1. **Read plan.md COMPLETELY**:
   - Use Read tool WITHOUT limit/offset parameters
   - Extract the research directory path
   - Understand ALL phases
   - Note all success criteria
   - Check for existing checkmarks (resume capability)

2. **Read research.md** (in same directory):
   - Get full context from research
   - Understand patterns and conventions
   - Reference for implementation details

3. **Create implementation todos** using TodoWrite:
   - One todo per phase from the plan
   - Mark any already-completed phases (if resuming)

4. **Confirm understanding**:

```
Plan loaded: [plan title]
Location: [path to plan.md]

**Phases to implement**:
1. [Phase 1 name] - [Status: Pending/In Progress/Complete]
2. [Phase 2 name] - [Status: Pending/In Progress/Complete]
3. [Phase 3 name] - [Status: Pending/In Progress/Complete]

**Files to modify**: [Count] files

Ready to start with [First uncompleted phase]?
```

### For Each Phase

#### 1. Prepare

- **Mark phase as in_progress** in TodoWrite
- **Read all files** mentioned in this phase COMPLETELY (no limit/offset)
- **Understand the changes** from the plan
- **Verify current state** matches plan's expectations

If current state doesn't match plan:
```
⚠️ Discrepancy Found in Phase [N]

**Plan expected**:
[What the plan says should exist]

**Actually found**:
[What's actually in the code]

**Impact**:
[Why this matters for the implementation]

**Options**:
1. [Adaptation approach A - with reasoning]
2. [Adaptation approach B - with reasoning]
3. Update plan to reflect reality

How should I proceed?
```

Wait for user decision before continuing.

#### 2. Implement

- **Make the changes** exactly as specified in the plan
- **Follow patterns** identified in research.md
- **Adapt when needed** based on user guidance
- **Write clean code** that matches codebase conventions

For each file change:
```
Implementing: [Component name]
File: path/to/file.ext
Changes: [Brief description]
```

#### 3. Automated Verification

Run ALL automated checks from the plan's success criteria:

```bash
# Example - use actual commands from plan
npm test
npm run lint
npm run typecheck
npm run build
```

If any check fails:
- **STOP immediately**
- Show the error
- Fix the issue
- Re-run the checks
- Only proceed when ALL checks pass

Update plan.md with checkmarks for passing automated checks:
```markdown
#### Automated Verification
- [x] Tests pass: `npm test`
- [x] Linting passes: `npm run lint`
- [x] Type checking passes: `npm run typecheck`
```

#### 4. Pause for Manual Verification

After automated checks pass:

```
✅ Phase [N] Implementation Complete - Ready for Manual Testing

**Automated verification passed**:
- ✅ Tests pass
- ✅ Linting passes
- ✅ Type checking passes
- ✅ [Other automated checks]

**Manual verification required**:

Please complete these manual tests from the plan:

[ ] [Manual test 1 from plan]
[ ] [Manual test 2 from plan]
[ ] [Manual test 3 from plan]
[ ] [Edge case test from plan]

Instructions for each test are in: [path to plan.md] under Phase [N] > Manual Verification

Let me know when manual testing is complete, or if any issues were found.
```

**WAIT for user confirmation** - do not proceed to next phase.

#### 5. Complete Phase

After user confirms manual testing passed:

- **Update plan.md** with checkmarks for manual verification:
```markdown
#### Manual Verification
- [x] Feature works in UI
- [x] Performance acceptable
- [x] Edge cases handled
```

- **Mark phase completed** in TodoWrite

- **Summarize what was done**:
```
✅ Phase [N] Complete: [Phase name]

**Changes made**:
- [File 1]: [What was changed]
- [File 2]: [What was changed]

**Verification**:
- ✅ All automated checks passed
- ✅ All manual tests confirmed

Moving to Phase [N+1]...
```

### After All Phases Complete

```
🎉 Implementation Complete!

**Summary**:
✅ Phase 1: [Phase name] - [What was accomplished]
✅ Phase 2: [Phase name] - [What was accomplished]
✅ Phase 3: [Phase name] - [What was accomplished]

**Files modified**: [Count] files
**All automated verification**: ✅ Passed
**All manual verification**: ✅ Confirmed

**Final checks** (from plan):
Running final verification...
```

Run any final verification steps from the plan.

```
✅ Final verification passed

**Implementation artifacts**:
- Research: [path to research.md]
- Plan: [path to plan.md] (updated with checkmarks)
- Modified files: [list of files]

Ready to commit? Here's a suggested commit message:

---
[Feature/Fix]: [Brief description]
Implemented based on research and plan:
- Research: .claude/thoughts/[epoch]_[name]/research.md
- Plan: .claude/thoughts/[epoch]_[name]/plan.md
Changes:
- [Change 1]
- [Change 2]
- [Change 3]
All automated and manual verification passed.
---

Would you like me to create the commit, or do you need any adjustments?
```

## Important Guidelines

### Read Completely
- **ALWAYS** read plan.md completely (no limit/offset)
- **ALWAYS** read research.md completely
- **ALWAYS** read all files being modified completely
- Get full context before making changes

### Follow the Plan Exactly
- The plan is your specification
- Make changes as described in the plan
- Reference research.md for patterns
- Adapt only when reality differs (with user approval)

### Update plan.md with Progress
- Check off automated verification items
- Check off manual verification items
- Update as you complete each phase
- Plan becomes the record of what was done

### Verify Thoroughly
- Run ALL automated checks from plan
- Don't skip any verification
- Fix failures immediately
- Don't proceed with failing tests

### Pause for Manual Testing
- After each phase's automated verification
- List exact tests from the plan
- Wait for explicit user confirmation
- Don't guess or assume tests passed

### One Phase at a Time
- Complete phase N fully before phase N+1
- Don't jump ahead
- Don't batch phases without user request
- Maintain clear progress

### Handle Discrepancies
- Stop immediately if code doesn't match plan
- Explain the issue clearly
- Present adaptation options
- Get user decision before proceeding

### Track Progress
- Use TodoWrite throughout
- Update todos as phases complete
- Keep user informed
- Mark complete immediately

## Resume Capability

If plan.md has existing checkmarks:

```
Resuming implementation from existing plan:

**Completed phases**:
✅ Phase 1: [name]
✅ Phase 2: [name]

**Next phase**:
⏭️ Phase 3: [name]

I'll start with Phase 3. Phases 1 and 2 appear complete.
Should I verify the previous work, or proceed with Phase 3?
```

Default: trust completed work, start with first uncompleted phase.

## Verification Checklist

For each phase:
- [ ] Plan.md read completely
- [ ] Research.md read for context
- [ ] All relevant files read completely
- [ ] Changes match plan specification
- [ ] All automated checks pass
- [ ] Plan.md updated with automated checkmarks
- [ ] User completed manual testing
- [ ] Plan.md updated with manual checkmarks
- [ ] TodoWrite updated
- [ ] Ready for next phase

## Error Handling

### Tests Failing
```
❌ Automated verification failed: Tests

Error:
[Show the test failure]

I'll fix this issue before proceeding.
[Fix the problem]
[Re-run tests]
✅ Tests now passing

Continuing with verification...
```

### Build Failing
```
❌ Build failed

Error:
[Show the build error]

This needs to be fixed before proceeding.
[Fix the issue]
[Re-run build]
✅ Build successful
```

### Manual Testing Found Issues
```
User reported issue during manual testing:
[Issue description]

I'll address this before moving to the next phase.
[Fix the issue]
[Re-run automated verification]

Please re-test:
[Manual test that found the issue]
```

## Success Metrics

Implementation is successful when:
- ✅ All phases completed per plan
- ✅ All automated verification passes
- ✅ All manual verification confirmed
- ✅ Plan.md updated with all checkmarks
- ✅ Code follows patterns from research
- ✅ Code is clean and maintainable
- ✅ User confident in the changes

The implementation literally executes the plan.md phase by phase with rigorous verification at each step.
