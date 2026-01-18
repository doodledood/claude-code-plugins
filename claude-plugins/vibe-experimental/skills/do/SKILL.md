---
name: do
description: 'Autonomous execution from definition file. Works toward acceptance criteria, auto-verifies, prevents premature stopping. Use when you have a definition file from /define and want hands-off execution.'
user-invocable: true
---

# /do - Autonomous Criteria-Driven Execution

You are executing a definition file autonomously. Work toward acceptance criteria (not steps), verify before declaring done, and cannot stop until verification passes or you properly escalate.

## Input

`$ARGUMENTS` = definition file path (REQUIRED)

Example: `/do /tmp/define-1234567890.md`

If no arguments: Output error "Usage: /do <definition-file-path>"

## Process

### 1. Read and Validate Definition

Read the definition file from `$ARGUMENTS`:
- If file not found → output clear error and stop
- If file invalid (missing criteria section) → output clear error and stop

Extract:
- All criteria (AC-N, R-N, E-N)
- Verification methods for each
- Examples (accepted/rejected)
- Task-specific subagent definitions

### 2. Initialize

Create execution log: `/tmp/do-log-{timestamp}.md`

Write initial state:
```markdown
# Execution Log

Definition: [definition file path]
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
- [ ] Create log /tmp/do-log-{timestamp}.md
- [ ] Satisfy AC-1: [brief]→log; done when implemented + attempt logged
- [ ] Satisfy AC-2: [brief]→log; done when implemented + attempt logged
- [ ] Satisfy R-1: [brief]→log; done when not violated + attempt logged
- [ ] (expand: sub-tasks as discovered)
- [ ] Refresh: read full log
- [ ] Call /verify; done when all criteria verified
```

### 3. Work Toward Criteria

Work to satisfy the criteria. You decide how—the criteria define success, not the path to it.

Log format for attempts:
```markdown
### AC-1: [description]
- Attempt 1: [what you tried]
  Result: [outcome]
```

### 4. Call /verify When Ready

When you believe all criteria are addressed:

```
Use the Skill tool to verify: Skill("vibe-experimental:verify", "/tmp/define-{ts}.md /tmp/do-log-{ts}.md")
```

### 5. Handle Verification Results

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

### 6. Escalation (When Genuinely Stuck)

If you've tried 3+ approaches and can't satisfy a criterion:

```
Use the Skill tool to escalate: Skill("vibe-experimental:escalate", "AC-N blocking after 3 attempts")
```

/escalate requires /verify to have been called first (enforced by hook).

## Critical Rules

1. **Definition file required** - fail clearly if not provided
2. **Criteria-driven** - criteria define success, you decide how
3. **Log attempts** - each todo includes `→log` discipline
4. **Must call /verify** - can't declare done without verification
5. **Target failures** - on failure, fix specific criteria, don't restart
6. **Proper escalation** - /escalate only after /verify, with evidence

## Stop Hook Enforcement

A stop hook prevents premature stopping:
- Can't stop after /do without /done or /escalate
- /done only comes from /verify on success
- /escalate requires /verify first

If you try to stop prematurely, you'll see:
"Cannot stop - run /verify first. If stuck, /escalate after /verify."

## Example Flow

```
1. /do /tmp/define-123.md
2. Read definition, create log, create todos
3. Work toward criteria (logging attempts as you go)
4. Refresh: read full log
5. Skill("vibe-experimental:verify", "...")
6. If failures → fix specific criteria → retry verify
7. All pass → /verify calls /done → stop allowed
```
