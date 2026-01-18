---
name: verify
description: 'Internal verification runner. Spawns parallel criteria-checker agents for each criterion. Called by /do, not directly by users.'
user-invocable: false
---

# /verify - Verification Runner

You run all verification methods from a definition file. You spawn criteria-checker agents in parallel—you don't run checks yourself.

## Input

`$ARGUMENTS` = "<definition-file-path> <execution-log-path> [--parallel=N]"

- `--parallel=N`: Max concurrent criteria-checkers (default: 10)

Example: `/tmp/define-123.md /tmp/do-log-123.md --parallel=5`

## Process

### 1. Parse Inputs

Read both files:
- Definition file: extract all criteria and their verification methods
- Execution log: context for criteria-checkers

Parse `--parallel` argument (default 10).

### 2. Categorize Criteria

Group by verification type:
- **bash**: Shell commands (npm test, tsc, lint, etc.)
- **codebase**: Code pattern checks
- **manual**: Require human verification (set aside for later)

### 3. Spawn Criteria-Checkers in Parallel

For each automatable criterion (bash OR codebase), spawn a criteria-checker agent using the Task tool.

Example Task call:
```
Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: AC-1 (tests-pass)
Description: All tests pass
Verification method: bash
Command: npm test")
```

Launch up to N (from --parallel) concurrently. Wait for wave to complete before starting next wave.

### 4. Collect Results

Build results structure:
```
{
  "passed": ["AC-1", "AC-2", ...],
  "failed": [
    {
      "id": "AC-3",
      "method": "bash",
      "location": "src/foo.test.ts:45",
      "expected": "'queued'",
      "actual": "'sent'",
      "fix_hint": "..."
    }
  ],
  "manual": ["AC-10", "AC-11"]
}
```

### 5. Decision Logic

```
if any automated failed:
    → Return failures only (hide manual)
    → /do continues working

elif all automated pass AND manual exists:
    → Return manual criteria
    → Hint to call /escalate for human review

elif all pass (no manual):
    → Call /done
```

### 6. Output Format

#### On Failure

```markdown
## Verification Results

### Failed (N)

- **AC-3**: tests-pass
  Method: bash (`npm test`)
  Location: `src/notifications.test.ts:45`
  Expected: `'queued'`
  Actual: `'sent'`
  Fix: Update status to 'queued' before notification

- **AC-7**: error-pattern
  Method: codebase
  Location: `src/handlers/notify.ts:23`
  Issue: Raw Error() throw, expected AppError
  Fix: Replace with `throw new AppError({...})`

### Passed (M)
- AC-1, AC-2, AC-4, AC-5, AC-6

---

Continue working on failed criteria, then call /verify again.
```

#### On Success with Manual

```markdown
## Verification Results

### All Automated Criteria Pass (N)

### Manual Verification Required (M)

- **AC-10**: ux-feels-right
  How to verify: [from definition]

---

Call /escalate to surface for human review.
```

#### On Full Success

Call /done:
```
Use the Skill tool to complete: Skill("vibe-experimental:done", "all criteria verified")
```

## Critical Rules

1. **Don't run checks yourself** - spawn criteria-checker agents
2. **Parallel waves** - up to --parallel concurrent (default 10)
3. **Hide manual on auto-fail** - focus on fixable issues first
4. **Actionable feedback** - pass through file:line, expected vs actual from agents
5. **Call /done on success** - trigger completion
