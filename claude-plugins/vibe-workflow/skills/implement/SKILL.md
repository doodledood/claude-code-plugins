---
name: implement
description: 'Execute implementation plans autonomously chunk by chunk. Parses plan files, creates comprehensive todo lists (Memento pattern), auto-fixes gate failures, and provides completion summaries.'
---

# Implement Skill

Execute implementation plans with systematic progress tracking. This skill completes the spec → plan → implement pipeline by autonomously executing plan chunks in dependency order.

> **Fully Autonomous**: This skill runs without pauses. It only stops for truly blocking issues that cannot be auto-fixed.

## Overview

This skill:
1. **Parses** the plan file to extract chunks, dependencies, files, and tasks
2. **Creates** a comprehensive flat todo list (Memento pattern for context preservation)
3. **Executes** chunks in dependency order, marking progress in real-time
4. **Auto-fixes** gate failures persistently until resolved
5. **Summarizes** completion with offer to run `/review`

## Workflow

### Phase 1: Parse Plan & Create Todo List

**Step 1.1: Locate and read the plan file**

Accept plan input in these forms:
- File path: `/implement /tmp/plan-auth.md`
- With spec: `/implement /tmp/plan-auth.md --spec /tmp/spec-auth.md`
- Smart parsing: `/implement the auth plan` (infer from context or recent files)

If the plan file path is ambiguous:
1. Check `/tmp/` for recent `plan-*.md` files
2. Check conversation context for plan references
3. If still unclear, ask user to specify the exact path

**Step 1.2: Parse plan structure**

Extract from each chunk:
- **Chunk number and name**: From `## N. [Name]` headers
- **Dependencies**: From `Depends on:` field (parse comma-separated numbers, `-` means none)
- **Files to modify**: Paths and descriptions
- **Files to create**: Paths and purposes
- **Related files for context**: Paths with line ranges if specified
- **Implementation tasks**: The bullet list of tasks
- **Key functions and types**: For reference during implementation

**Step 1.3: Build dependency graph**

1. Parse `Depends on:` for each chunk
2. Identify chunks with no dependencies (execute first)
3. Order remaining chunks by dependency satisfaction
4. Note parallel opportunities (but V1 executes sequentially)

**Step 1.4: Create comprehensive flat todo list**

For each chunk in dependency order, create todos:

```
[ ] Read context files for [Chunk Name]
[ ] [Task 1 from plan]
[ ] [Task 2 from plan]
[ ] ...
[ ] [Task N from plan]
[ ] Run quality gates for [Chunk Name]
```

This Memento-style granularity ensures:
- Context preserved if execution interrupted
- Progress visible at task level
- Resumption continues from exact stopping point

**Example**: For a plan with 2 chunks, 3 tasks each:
```
[ ] Read context files for User Validation Service
[ ] Implement validateEmail() - RFC 5322 format check
[ ] Implement validatePassword() - Min 8 chars, 1 number, 1 special
[ ] Implement rateLimit() - 5 attempts per minute per IP
[ ] Run quality gates for User Validation Service
[ ] Read context files for Auth Middleware
[ ] Implement authMiddleware() - JWT verification
[ ] Implement refreshToken() - Token refresh logic
[ ] Add auth middleware tests
[ ] Run quality gates for Auth Middleware
```

Use TodoWrite to create all todos at once, all in `pending` status.

### Phase 2: Execute Chunks Autonomously

**CRITICAL**: Do NOT pause for user confirmation. Execute continuously until complete or truly blocked.

**Step 2.1: Process chunks in dependency order**

For each chunk:

1. **Mark context todo as in_progress**
2. **Read all context files**:
   - Read files listed in "Related files for context"
   - Read files listed in "Files to modify" (to understand current state)
   - If line ranges specified (e.g., `file.ts:45-80`), focus on those lines
3. **Mark context todo as completed**

4. **For each implementation task**:
   a. Mark task todo as `in_progress`
   b. Implement the task:
      - For "Implement X()" tasks: Write the function/code
      - For "Tests" tasks: Write test cases as specified
      - For file creation: Create with described purpose
      - For file modification: Apply described changes
   c. Mark task todo as `completed` immediately after finishing

5. **Mark gates todo as in_progress**
6. **Run quality gates** (see Phase 3)
7. **Mark gates todo as completed** when gates pass

**Step 2.2: Handle optional spec file**

If a spec file was provided (`--spec` flag or detected):
- Read it before starting implementation
- Use it for additional context on requirements
- Reference acceptance criteria during implementation

**Step 2.3: Track modified files**

Maintain a list of files created and modified during implementation for the completion summary.

### Phase 3: Gate Failure Auto-Fix

After implementing all tasks in a chunk, run quality gates:

**Step 3.1: Run gates**

Execute in order:
1. **Typecheck**: Run the project's type checker (tsc, mypy, etc.)
2. **Tests**: Run the project's test suite
3. **Lint**: Run the project's linter (eslint, ruff, etc.)

Detect the appropriate commands from project configuration (package.json, pyproject.toml, etc.).

**Step 3.2: If gates fail - auto-fix iteratively**

When any gate fails:

1. **Analyze the failure output**:
   - Parse error messages
   - Identify affected files and lines
   - Understand the root cause

2. **Implement a clean fix**:
   - Fix the actual issue, not a workaround
   - Maintain code quality
   - Don't introduce new problems

3. **Re-run gates**

4. **Repeat until gates pass**:
   - Continue iterating through analyze → fix → re-run
   - Each iteration should make progress
   - Track what was tried to avoid loops

**Step 3.3: Only pause if truly blocked**

Pause and ask the user ONLY when:
- Multiple fix attempts have failed (3+ iterations)
- The issue requires external information you don't have
- The fix would require breaking changes outside the chunk's scope
- There's a fundamental conflict with existing code

When pausing, explain:
- What was tried
- Why it didn't work
- What information or decision is needed

### Phase 4: Completion Summary

When all chunks complete successfully:

**Step 4.1: Generate summary**

```
## Implementation Complete

**Chunks implemented**: N
**Todos completed**: M
**Files created**: [list]
**Files modified**: [list]

### Notes
[Any warnings, assumptions made, or follow-up items]

---

Run `/review` to verify code quality before committing.
```

**Step 4.2: Offer review**

End with the suggestion to run `/review` for comprehensive quality verification:
- Code bugs review
- Test coverage review
- Maintainability review
- Type safety review (if typed language)
- CLAUDE.md adherence review

## Edge Cases

### Invalid Plan File

If the plan file doesn't exist or is malformed:
```
Error: Could not parse plan file at [path].
- File not found, OR
- Missing expected structure (## N. chunk headers, Implementation tasks section)

Please provide a valid plan file from `/plan` or check the file path.
```

### Missing Context Files

If a context file referenced in the plan doesn't exist:
- Log a warning: `Warning: Context file [path] not found, skipping`
- Continue with other files
- Context is helpful but not blocking

### Dependency Failure

If a chunk fails completely (not just gates, but fundamentally cannot be implemented):
1. Mark that chunk's remaining todos as blocked (leave in pending)
2. Skip any chunks that depend on the failed chunk
3. Continue with independent remaining chunks
4. Report in summary:
   ```
   ### Skipped Chunks
   - Chunk N: [name] - Failed: [reason]
   - Chunk M: [name] - Skipped: depends on Chunk N
   ```

### No Plan File Specified

If invoked without arguments and no plan can be inferred:
```
No plan file specified. Please provide:
- A path: /implement /tmp/plan-feature.md
- Or run /plan first to create one
```

### Interrupted Execution

If execution is interrupted (user stops, error, etc.):
- Todos reflect exact progress (Memento pattern)
- User can see what completed vs remaining
- Re-running `/implement` with same plan would need manual todo cleanup

## Key Principles

### Fully Autonomous
- No confirmation prompts before starting
- No pauses between chunks
- No approval needed for auto-fixes
- Only human intervention for truly blocking issues

### Memento Pattern for Todos
- Every action gets its own todo item
- Progress is granular and visible
- Context preserved if interrupted
- Resumption point is clear

### Persistent Auto-Fix
- Don't give up after one fix attempt
- Iterate until gates pass
- Seek clean solutions, not workarounds
- Only escalate to user when genuinely stuck

### Dependency Respect
- Execute chunks in correct order
- Skip dependents when dependencies fail
- Report what was skipped and why

### Quality Gates Are Non-Negotiable
- Every chunk must pass gates before moving on
- Type errors, test failures, lint issues must be fixed
- No "we'll fix it later" - fix it now

## Gate Detection

**CLAUDE.md is the source of truth**. Most projects specify their lint/test/typecheck commands there. Check CLAUDE.md first before searching for config files.

**Priority order**:
1. **CLAUDE.md** - Usually contains exact commands (e.g., `ruff check && black && mypy`)
2. **package.json scripts** - Look for `lint`, `test`, `typecheck` scripts
3. **Makefile** - Look for standard targets
4. **Config file detection** - Last resort fallback

**Fallback detection** (only if CLAUDE.md doesn't specify):

*TypeScript/JavaScript*:
- `tsconfig.json` → `tsc --noEmit`
- `eslint.config.*` → `eslint .`
- `jest.config.*` or `vitest.config.*` → `npm test`

*Python*:
- `pyproject.toml` with mypy → `mypy`
- `ruff.toml` or ruff in pyproject → `ruff check`
- pytest config → `pytest`
