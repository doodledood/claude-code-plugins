---
description: 'Executes implementation plans via subagents with automated verification and fix loops. Use after /plan for complex features. Each chunk gets dedicated Implementor + Verifier agents with up to 5 fix attempts.'
argument-hint: Optional - path to plan file, or --progress <file> to resume
---

**User request**: $ARGUMENTS

Autonomously execute plan chunks via Implementor and Verifier subagents. Each chunk is isolated: implemented by one agent, verified by another, with automated fix loops.

**Fully autonomous**: No pauses except truly blocking issues.

## Workflow

```
For each chunk:
  1. Spawn Implementor agent → implements chunk
  2. Spawn Verifier agent → checks gates + acceptance criteria
  3. If FAIL → fix loop (max 5 attempts, escalate on same-error)
  4. If PASS → update progress, next chunk
```

## Phase 1: Parse Plan & Setup

### 1.1 Locate Plan

Accept:
- `/implement-v2 /tmp/plan.md` - explicit path
- `/implement-v2 --progress /tmp/implement-*.md` - resume from progress file
- Infer from context or recent `/tmp/plan-*.md` files

### 1.2 Parse Chunks

For each `## N. [Name]` header, extract:
- Dependencies (`Depends on:` field, `-` = none)
- Files to modify/create with descriptions
- Context files (paths, optional line ranges)
- Implementation tasks (bullet list)
- Acceptance criteria (infer from tasks if missing for backward compat)
- Key functions/types

### 1.3 Build Dependency Graph

Order: No-dependency chunks first, then topological order.

### 1.4 Create Progress File

Path: `/tmp/implement-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md`

```markdown
# Implementation Progress: [Plan Name]

Started: [timestamp]
Plan: [path to plan file]
Status: IN_PROGRESS

## Chunks

### Chunk 1: [Name]
Status: PENDING
Attempts: 0
Implementor log: (none)
Verifier log: (none)
Files created: []
Files modified: []
Notes:

### Chunk 2: [Name]
Status: PENDING
...

## Summary
Completed: 0/N chunks
Last updated: [timestamp]
```

### 1.5 Create Todo List

Build Memento-style todos with 4 items per chunk:
```
[ ] Implement chunk 1: [Name]
[ ] Verify chunk 1: [Name]
[ ] (Fix loop for chunk 1 - expand if needed)
[ ] Commit chunk 1: [Name]
[ ] Implement chunk 2: [Name]
[ ] Verify chunk 2: [Name]
[ ] (Fix loop for chunk 2 - expand if needed)
[ ] Commit chunk 2: [Name]
...
```

All todos created at once via TodoWrite, status `pending`. Fix loop placeholder is expanded into implement/verify pairs during Phase 3.

### 1.6 Handle Resume

If `--progress` argument provided:
1. Read progress file
2. Skip chunks with status `COMPLETE`
3. Resume from first `PENDING` or `IN_PROGRESS` chunk
4. Re-verify `IN_PROGRESS` chunks before continuing

## Phase 2: Execute Chunks (Subagent Orchestration)

**CRITICAL**: Execute continuously without pauses.

For each chunk in dependency order:

### 2.1 Spawn Implementor Agent

1. Mark implement todo `in_progress`
2. **Update progress file**: chunk status → `IN_PROGRESS`, `Last updated` timestamp
3. Use Task tool with `subagent_type: "vibe-workflow:chunk-implementor"`:

```
Implement chunk N: [Name]

## Full Chunk Definition
[Copy the ENTIRE chunk verbatim from the plan, including:
- Depends on / Parallel
- Description
- Files to modify (with descriptions)
- Files to create (with purposes)
- Context files (with line ranges)
- Tasks
- Acceptance criteria
- Key functions / Types]

[If retry: ## Fix Context
Attempt: N/5
Previous verification failed with:
[Verifier's issue list from structured output]
Focus on fixing these specific issues.]
```

4. Wait for completion, parse output:
   - Extract `Log file:` path
   - Extract `Files created:` and `Files modified:` lists
5. **Update progress file**: `Implementor log`, `Files created`, `Files modified`, `Last updated`
6. Mark implement todo `completed`

### 2.2 Spawn Verifier Agent

1. Mark verify todo `in_progress`
2. Use Task tool with `subagent_type: "vibe-workflow:chunk-verifier"`:

```
Verify chunk N: [Name]

## Full Chunk Definition
[Copy the ENTIRE chunk verbatim - same as implementor received]

## Implementor Log File
[Path from implementor's output, e.g., /tmp/implement-chunk-1-20260107-120000.md]

[If retry: ## Previous Errors
[Errors from last verification for same-error detection]]
```

3. Wait for result, parse output:
   - Extract `Status:` (PASS/FAIL)
   - Extract `Log file:` path
   - Extract issues list if FAIL
   - Check `Same as previous:` if retry
4. **Update progress file**: `Verifier log`, `Last updated`

### 2.3 Process Verification Result

**If Status: PASS**
1. Mark verify todo `completed`
2. Mark fix loop placeholder `completed` (not needed)
3. **Update progress file**: chunk status → `COMPLETE`, `Completed: N/M`, `Last updated`
4. Commit chunk (see 2.4)
5. Continue to next chunk

**If Status: FAIL**
1. **Update progress file**: increment `Attempts`, add issues to `Notes`, `Last updated`
2. Check attempt count (max 5 total including initial)
3. Check for same-error condition
4. If can retry → enter fix loop (Phase 3)
5. If max attempts or same-error → escalate (Phase 4)

### 2.4 Commit Chunk (Main Agent Only)

**CRITICAL**: Main agent handles all git operations directly. Subagents NEVER perform git actions.

1. Mark commit todo `in_progress`
2. Stage files from chunk: `git add [files created/modified]`
3. Commit with message: `feat(plan): implement chunk N - [Name]`
4. **Do NOT push** - push happens at end or on user request
5. **Update progress file**: add commit SHA to chunk notes
6. Mark commit todo `completed`

**If git operation fails** (conflicts, dirty state, etc.):
1. Log issue in progress file
2. Report to user with specific error
3. User must resolve before continuing

## Phase 3: Fix Loop

When verification fails and retry is possible:

### 3.1 Expand Fix Loop Placeholder

Replace fix loop placeholder todo with specific items:
```
[x] (Fix loop for chunk N - expand if needed) → completed
[ ] Fix attempt 1: implement chunk N
[ ] Fix attempt 1: verify chunk N
[ ] (Additional fix attempts - expand if needed)
```

### 3.2 Analyze Failure

From verifier output, identify:
- Gate failures (specific errors)
- Acceptance criteria failures
- File:line locations

### 3.3 Respawn Implementor with Fix Context

1. Mark fix implement todo `in_progress`
2. Respawn implementor (same as 2.1 but with fix context)
3. **Update progress file**: new `Implementor log`, updated files, `Last updated`
4. Mark fix implement todo `completed`

### 3.4 Re-verify

1. Mark fix verify todo `in_progress`
2. Respawn verifier with `previous_errors` for same-error detection
3. **Update progress file**: new `Verifier log`, `Last updated`

### 3.5 Process Result

**If PASS**:
1. Mark fix verify todo `completed`
2. Mark additional attempts placeholder `completed`
3. **Update progress file**: status → `COMPLETE`, `Completed: N/M`, `Last updated`
4. Commit chunk (2.4)
5. Continue to next chunk

**If FAIL with different errors**:
1. **Update progress file**: increment `Attempts`, update `Notes`, `Last updated`
2. If attempts < 5 → expand placeholder, repeat fix loop (3.2)

**If FAIL with same errors OR attempts >= 5**:
1. **Update progress file**: status → `FAILED`, `Notes` with reason, `Last updated`
2. Escalate (Phase 4)

## Phase 4: Escalation & Completion

### 4.1 Escalation

When chunk cannot be completed:

1. **Update progress file**: overall status → `FAILED`, chunk status → `FAILED`, `Last updated`
2. Report to user:

```
## Implementation Blocked

Chunk [N]: [Name] failed after [X] attempts.

### Last Verification Result
[Verifier's output]

### Attempts History
1. [Issues from attempt 1]
2. [Issues from attempt 2]
...

### Recommendation
[What might resolve this - needs human input]

Progress saved to: [progress file path]
Resume with: /implement-v2 --progress [path]
```

Stop implementation. User must intervene.

### 4.2 Successful Completion

When all chunks complete:

1. **Update progress file**: overall status → `COMPLETE`, `Completed: N/N`, `Last updated`
2. Report to user:

```
## Implementation Complete

Chunks: N | Files created: [list] | Files modified: [list]

### Chunk Summary
1. [Name] - [files touched]
2. [Name] - [files touched]

### Notes
[Any warnings, assumptions, or follow-ups]

Progress file: [path]
Run `/review` for quality verification.
```

## Progress File Format

```markdown
# Implementation Progress: [Plan Name]

Started: [timestamp]
Plan: [path]
Status: IN_PROGRESS | COMPLETE | FAILED

## Chunks

### Chunk 1: [Name]
Status: COMPLETE | IN_PROGRESS | PENDING | FAILED
Attempts: N
Implementor log: [path or (none)]
Verifier log: [path or (none)]
Files created: [list]
Files modified: [list]
Notes: [issues or warnings]

### Chunk 2: [Name]
...

## Summary
Completed: N/M chunks
Last updated: [timestamp]
```

## Edge Cases

| Case | Action |
|------|--------|
| Invalid plan | Error with path + expected structure |
| Missing context file | Warn, continue (non-blocking) |
| Chunk fails after 5 attempts | Mark FAILED, stop, report which chunk and why |
| Same error detected | Stop immediately, escalate with recommendation |
| No acceptance criteria in plan | Auto-infer from tasks |
| Interrupted mid-chunk | Progress file shows IN_PROGRESS, resume re-starts that chunk |
| Resume with progress file | Skip COMPLETE chunks, start from first non-complete |
| Dependency not met (prior chunk failed) | Skip this chunk, mark as blocked |

## Principles

- **Subagent isolation**: Implementor edits, Verifier only reads, neither does git
- **Git in main agent only**: All git operations (add, commit) happen in main agent, not subagents
- **Commit per chunk**: Each successful chunk gets its own commit (no push until end)
- **Autonomous**: No prompts/pauses/approval except blocking issues
- **Retry heavily**: 5 attempts before giving up, escalation is last resort
- **Same-error aware**: Detect loops, don't wall-slam
- **Progress after every step**: Update progress file after each todo completion
- **Acceptance-focused**: Gates + criteria must pass

## Gate Detection (Verifier Reference)

**Priority**: CLAUDE.md → package.json scripts → Makefile → config detection

**Fallback** (if CLAUDE.md doesn't specify):
- TS/JS: `tsconfig.json`→`tsc --noEmit`, `eslint.config.*`→`eslint .`, `jest/vitest.config.*`→`npm test`
- Python: `pyproject.toml`→`mypy`/`ruff check`, pytest config→`pytest`
