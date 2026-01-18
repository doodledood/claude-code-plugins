---
name: verify
description: 'Internal verification runner. Spawns parallel criteria-checker agents for each criterion. Called by /do, not directly by users.'
user-invocable: false
---

# /verify - Verification Runner

You run all verification methods from a definition file. You spawn criteria-checker agents in parallel—you don't run checks yourself.

## Input

`$ARGUMENTS` = "<definition-file-path> <execution-log-path> [--parallel=N] [--scope=files]"

- `--parallel=N`: Max concurrent criteria-checkers (default: 10)
- `--scope=files`: Comma-separated file paths for reviewer scope override (optional)

Examples:
- `/tmp/define-123.md /tmp/do-log-123.md --parallel=5`
- `/tmp/define-123.md /tmp/do-log-123.md --scope=src/queue.ts,src/batch.ts`

## Process

### 1. Parse Inputs

Read both files:
- Definition file: extract all criteria and their verification methods
- Execution log: context for criteria-checkers

Parse arguments:
- `--parallel=N` (default 10)
- `--scope=files` (optional, for reviewer scope override)

### 2. Categorize Criteria

Group by verification type:
- **bash**: Shell commands (npm test, tsc, lint, etc.)
- **codebase**: Code pattern checks
- **subagent**: Reviewer agents (code-bugs-reviewer, type-safety-reviewer, etc.)
- **manual**: Require human verification (set aside for later)

### 3. Spawn Verifiers in Parallel

#### For bash/codebase criteria → criteria-checker

Spawn a criteria-checker agent using the Task tool.

Example Task call:
```
Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: AC-1 (tests-pass)
Description: All tests pass
Verification method: bash
Command: npm test")
```

#### For subagent criteria → spawn reviewer directly

For Code Quality Gate criteria (QG-*), spawn the reviewer agent directly.

Example Task call:
```
Task(subagent_type="vibe-experimental:code-bugs-reviewer", prompt="
Review the current branch changes for bugs. Focus on HIGH and CRITICAL severity issues only.
Scope: git diff against origin/main")
```

**Scope override**: If /do provides explicit scope (e.g., specific files changed), pass it:
```
Task(subagent_type="vibe-experimental:code-bugs-reviewer", prompt="
Review these files for bugs: src/handlers/notify.ts, src/services/queue.ts
Focus on HIGH and CRITICAL severity issues only.")
```

Launch up to N (from --parallel) concurrently. Wait for wave to complete before starting next wave.

### 4. Collect Results

#### For bash/codebase results (from criteria-checker)

Standard structure:
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

#### For subagent results (from reviewer agents)

Parse the reviewer's report for CRITICAL and HIGH severity issues:

1. Look for `#### [CRITICAL]` or `#### [HIGH]` section headers
2. Extract each issue's location, description, and suggested fix
3. If ANY CRITICAL or HIGH issues found → criterion FAILS
4. If no CRITICAL/HIGH issues → criterion PASSES

Convert to same structure:
```
{
  "id": "QG-BUGS",
  "method": "subagent",
  "agent": "code-bugs-reviewer",
  "issues": [
    {
      "severity": "HIGH",
      "title": "Race condition in queue processing",
      "location": "src/queue.ts:45-52",
      "description": "Async state change without synchronization",
      "fix_hint": "Add mutex or use atomic operations"
    }
  ]
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

- **QG-BUGS**: No HIGH or CRITICAL bugs
  Method: subagent (code-bugs-reviewer)
  Issues found: 2

  1. [HIGH] Race condition in queue processing
     Location: `src/queue.ts:45-52`
     Description: Async state change without synchronization
     Fix: Add mutex or use atomic operations

  2. [CRITICAL] Data loss in batch update
     Location: `src/batch.ts:112`
     Description: Missing error handling causes silent failures
     Fix: Add try-catch and rollback on failure

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

1. **Don't run checks yourself** - spawn criteria-checker or reviewer agents
2. **Parallel waves** - up to --parallel concurrent (default 10)
3. **Hide manual on auto-fail** - focus on fixable issues first
4. **Actionable feedback** - pass through file:line, expected vs actual from agents
5. **Call /done on success** - trigger completion
6. **Subagent threshold** - for QG-* criteria:
   - Most reviewers: FAIL = any CRITICAL or HIGH issues
   - QG-DOCS (docs-reviewer): FAIL = any MEDIUM or higher (docs are capped at MEDIUM severity)
7. **Return all issues** - for failed QG-* criteria, include all failing issues so /do can fix them
