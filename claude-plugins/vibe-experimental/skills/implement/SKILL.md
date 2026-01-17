---
name: implement
description: 'Autonomous implementation from spec file. Works toward acceptance criteria, auto-verifies, prevents premature stopping. Use when you have a spec file from /spec and want hands-off implementation.'
user-invocable: true
---

# /implement - Autonomous Criteria-Driven Implementation

You are implementing a spec file autonomously. Work toward acceptance criteria (not steps), verify before declaring done, and cannot stop until verification passes or you properly escalate.

## Input

`$ARGUMENTS` = spec file path (REQUIRED)

Example: `/implement /tmp/spec-1234567890.md`

If no arguments: Output error "Usage: /implement <spec-file-path>"

## Process

### 1. Read and Validate Spec

Read the spec file from `$ARGUMENTS`:
- If file not found → output clear error and stop
- If file invalid (missing criteria section) → output clear error and stop

Extract:
- All criteria (AC-N, R-N, E-N)
- Verification methods for each
- Examples (accepted/rejected)
- Task-specific subagent definitions

### 2. Initialize

Create implementation log: `/tmp/implement-log-{timestamp}.md`

Write initial state:
```markdown
# Implementation Log

Spec: [spec file path]
Started: [timestamp]

## Criteria Status
- [ ] AC-1: [description]
- [ ] AC-2: [description]
- [ ] R-1: [description]
...

## Attempts
(will be filled as work progresses)
```

Create TodoWrite with criteria to satisfy:
```
- [ ] Create implementation log
- [ ] Satisfy AC-1: [brief description]; done when verified
- [ ] Satisfy AC-2: [brief description]; done when verified
- [ ] Satisfy R-1: [ensure not rejected]; done when verified
- [ ] (expand: sub-tasks as discovered)
- [ ] Call /verify when all criteria addressed
```

### 3. Work Toward Criteria

**CRITICAL: Work toward criteria, NOT steps.**

NO plan decomposition:
- Do NOT create plan files
- Do NOT chunk into "Chunk 1", "Chunk 2"
- Reference criteria IDs in your work

For each criterion:
1. Read the criterion and its verification method
2. Implement what's needed
3. Log attempt: "Tried X for AC-N, result: Y"
4. Make meaningful git commit referencing criterion
5. Move to next criterion

### 4. Log Before Proceeding

After each significant action, update `/tmp/implement-log-{timestamp}.md`:

```markdown
## Attempts

### AC-1: [description]
- Attempt 1: Created src/foo.ts with handler
  Result: Compiles, untested

- Attempt 2: Added unit tests
  Result: Tests pass locally

### AC-2: [description]
- Attempt 1: ...
```

### 5. Git Commits

Make incremental commits:
- Reference criteria: "feat: implement notification queueing (AC-3)"
- Small, focused changes
- Don't wait until end to commit everything

### 6. Call /verify When Ready

When you believe all criteria are addressed:

```
Use the Skill tool to verify: Skill("vibe-experimental:verify", "/tmp/spec-{ts}.md /tmp/implement-log-{ts}.md")
```

### 7. Handle Verification Results

**/verify returns failures:**
- Read the specific failures
- Target ONLY the failing criteria
- Do NOT restart from scratch
- Do NOT touch passing criteria
- Update log with new attempts
- Call /verify again when fixed

**/verify returns success:**
- /verify will call /done automatically
- You're finished

**/verify returns manual criteria:**
- All automated criteria pass
- Manual criteria need human verification
- Call /escalate to surface them and allow stop

### 8. Escalation (When Genuinely Stuck)

If you've tried 3+ approaches and can't satisfy a criterion:

```
Use the Skill tool to escalate: Skill("vibe-experimental:escalate", "AC-N blocking after 3 attempts")
```

/escalate requires /verify to have been called first (enforced by hook).

## Critical Rules

1. **Spec file required** - fail clearly if not provided
2. **Criteria-driven** - no plan decomposition, reference AC-N in work
3. **Log before proceeding** - memento pattern mandatory
4. **Incremental commits** - small commits with criterion references
5. **Must call /verify** - can't declare done without verification
6. **Target failures** - on failure, fix specific criteria, don't restart
7. **Proper escalation** - /escalate only after /verify, with evidence

## Stop Hook Enforcement

A stop hook prevents premature stopping:
- Can't stop after /implement without /done or /escalate
- /done only comes from /verify on success
- /escalate requires /verify first

If you try to stop prematurely, you'll see:
"Cannot stop - run /verify first. If stuck, /escalate after /verify."

## Example Flow

```
1. /implement /tmp/spec-123.md
2. Read spec, create log, create todos
3. Work on AC-1 → log attempt → commit
4. Work on AC-2 → log attempt → commit
5. ...
6. Skill("vibe-experimental:verify", "...")
7. Verification fails AC-3
8. Fix AC-3 → log attempt → commit
9. Skill("vibe-experimental:verify", "...")
10. All pass → /verify calls /done
11. Stop allowed
```
