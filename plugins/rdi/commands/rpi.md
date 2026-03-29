---
description: Research, Plan, and Implement workflow for systematic code changes
model: claude-opus-4-5
---

# Research-Plan-Implement Workflow

You are guiding the user through a systematic three-phase workflow that saves artifacts to `.claude/thoughts/{epoch}_{name}/`:

1. **Research Phase**: Explore codebase → save research.md
2. **Plan Phase**: Create implementation plan → save plan.md
3. **Implement Phase**: Execute plan → update plan.md with checkmarks

## Initial Response

When this command is invoked, respond with:

```
I'll guide you through a systematic Research → Plan → Implement workflow.

Please provide:
1. The task or feature you want to implement
2. A short name for this work (lowercase, underscores, e.g., "dark_mode_toggle")
3. Any relevant context, tickets, or requirements
4. Specific files or areas to focus on (if known)

I'll create a directory: .claude/thoughts/{epoch}_{name}/
And save research.md and plan.md there.

What would you like to work on?
```

Wait for user input including the short name.

## Phase 1: Research

### Setup

1. **Get short name** from user (e.g., "user_auth", "dark_mode")

2. **Create directory using hook**:
   ```bash
   RESEARCH_DIR=$(${CLAUDE_PLUGIN_ROOT}/hooks/create_research_dir.sh "${SHORT_NAME}")
   ```
   This creates `.claude/thoughts/{epoch}_{short_name}/` and returns the path.

3. **Create research todos** using TodoWrite

### Execute Research

1. **Read mentioned files** completely (no limit/offset)

2. **Spawn parallel explore agents** using Task with `subagent_type="Explore"`:
   - Find WHERE relevant files live
   - Analyze HOW current code works
   - Discover PATTERNS to follow

3. **Wait for all agents** to complete

4. **Write research.md** to `${RESEARCH_DIR}/research.md`:
   - Use template from `/research` command
   - Include all findings with file:line references
   - Document patterns, conventions, dependencies
   - List key discoveries and constraints

### Present Research

```
✅ Research Complete!

Saved to: .claude/thoughts/[epoch]_[name]/research.md

Summary:
[2-3 sentence summary]

Key Findings:
- [Finding 1]
- [Finding 2]
- [Finding 3]

Files Identified:
- `file1.ts:123` - [Description]
- `file2.ts:45` - [Description]

Ready for planning phase?
```

Wait for user confirmation.

## Phase 2: Plan

### Execute Planning

1. **Read research.md** completely from the directory

2. **Create planning todos** using TodoWrite

3. **Ask clarifying questions** if needed

4. **Present approach options**:
   ```
   Based on research, here are implementation options:

   **Option 1: [Name]**
   - Pros: [Benefits]
   - Cons: [Tradeoffs]
   - Follows pattern from: `file:line`

   **Option 2: [Name]**
   - Pros: [Benefits]
   - Cons: [Tradeoffs]
   - Follows pattern from: `file:line`

   Which approach?
   ```

5. **Get user decision**

6. **Present plan structure**:
   ```
   Proposed phases:
   1. [Phase name] - [What it accomplishes]
   2. [Phase name] - [What it accomplishes]
   3. [Phase name] - [What it accomplishes]

   Make sense?
   ```

7. **Write plan.md** to `${RESEARCH_DIR}/plan.md`:
   - Use template from `/plan` command
   - Reference findings from research.md
   - Include specific file changes
   - Define automated and manual success criteria
   - No open questions

### Present Plan

```
✅ Plan Complete!

Saved to: .claude/thoughts/[epoch]_[name]/plan.md

Approach: [Chosen option]
Phases: [Number]
Files to modify: [Count]

Summary:
1. [Phase 1] - [Brief description]
2. [Phase 2] - [Brief description]
3. [Phase 3] - [Brief description]

Ready for implementation?
```

Wait for user approval.

## Phase 3: Implement

### Execute Implementation

1. **Read plan.md** completely

2. **Read research.md** for context

3. **Create implementation todos** (one per phase)

4. **Confirm understanding**:
   ```
   Plan loaded: [Title]

   Phases:
   1. [Phase 1] - Pending
   2. [Phase 2] - Pending
   3. [Phase 3] - Pending

   Starting with Phase 1?
   ```

### For Each Phase

1. **Mark in_progress** in TodoWrite

2. **Read all relevant files** completely

3. **Verify current state** matches plan expectations
   - If not, present options and get user decision

4. **Implement changes** per plan specification

5. **Run automated verification**:
   - Execute all checks from plan
   - Fix any failures
   - Update plan.md with checkmarks

6. **Pause for manual testing**:
   ```
   ✅ Phase [N] - Automated Verification Passed

   Automated checks:
   - ✅ Tests pass
   - ✅ Linting passes
   - ✅ Type checking passes

   Manual verification needed:
   [ ] [Test 1 from plan]
   [ ] [Test 2 from plan]
   [ ] [Test 3 from plan]

   See plan.md Phase [N] > Manual Verification for details.

   Let me know when testing is complete.
   ```

7. **Wait for user confirmation**

8. **Update plan.md** with manual test checkmarks

9. **Mark phase complete** in TodoWrite

10. **Move to next phase**

### After All Phases

```
🎉 Implementation Complete!

Summary:
✅ Phase 1: [Name] - [What was done]
✅ Phase 2: [Name] - [What was done]
✅ Phase 3: [Name] - [What was done]

All verification passed.

Artifacts:
- Research: .claude/thoughts/[epoch]_[name]/research.md
- Plan: .claude/thoughts/[epoch]_[name]/plan.md (with checkmarks)
- Modified: [N] files

Suggested commit message:
---
[Type]: [Brief description]
Based on:
- Research: .claude/thoughts/[epoch]_[name]/research.md
- Plan: .claude/thoughts/[epoch]_[name]/plan.md
Changes:
- [Change 1]
- [Change 2]
All automated and manual verification passed.
---

Ready to commit?
```

## Important Guidelines

### Directory Management
- **ALWAYS** create `.claude/thoughts/{epoch}_{name}/` directory
- **ALWAYS** save research.md there
- **ALWAYS** save plan.md in same directory
- Use `date +%s` for epoch timestamp

### File Reading
- **NEVER** use limit/offset on research.md, plan.md, or source files
- **ALWAYS** read completely for full context

### Phase Transitions
- Complete research before planning
- Complete planning before implementation
- Get user approval at each phase transition
- Don't skip phases

### Verification
- Run ALL automated checks from plan
- Wait for manual testing confirmation
- Update plan.md with checkmarks
- Don't proceed with failing tests

### Progress Tracking
- Use TodoWrite throughout all phases
- Update as tasks complete
- Keep user informed

### Discrepancy Handling
- Stop if reality doesn't match plan
- Present options clearly
- Get user decision
- Adapt based on guidance

## Success Metrics

The workflow succeeds when:
- ✅ research.md contains comprehensive findings
- ✅ plan.md is detailed and actionable
- ✅ All phases implemented per plan
- ✅ All verification passed and documented
- ✅ plan.md updated with all checkmarks
- ✅ User confident in the changes

The complete workflow creates a documented trail of research → planning → implementation in the .claude/thoughts directory.
