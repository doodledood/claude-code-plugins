---
name: verify
description: 'Internal verification runner. Spawns parallel criteria-checker agents for each criterion. Called by /do, not directly by users.'
user-invocable: false
---

# /verify - Verification Runner

You run all verification methods from a definition file. You spawn criteria-checker agents in parallel—you don't run checks yourself.

## Input

`$ARGUMENTS` = "<definition-file-path> <execution-log-path> [--scope=files]"

- `--scope=files`: Comma-separated file paths for reviewer scope override (optional)

Examples:
- `/tmp/define-123.md /tmp/do-log-123.md`
- `/tmp/define-123.md /tmp/do-log-123.md --scope=src/queue.ts,src/batch.ts`

## Process

### 1. Parse Inputs

Read both files:
- Definition file: extract all criteria and their verification methods
- Execution log: context for criteria-checkers

Parse `--scope=files` if provided (optional, for reviewer scope override).

### 2. Categorize Criteria

All criteria use sequential `AC-N` numbering. Group by verification type (from `verify.method`):
- **bash**: Shell commands (npm test, tsc, lint, etc.)
- **codebase**: Code pattern checks
- **subagent**: Reviewer agents (code-bugs-reviewer, type-safety-reviewer, etc.)
- **manual**: Require human verification (set aside for later)

Note: The `category` field (feature, rejection, edge-case, boundary, quality-gate, project-gate) is metadata; grouping is by verification METHOD.

Then sort by expected duration (slow first):

- **Slow** (30s+): test suites, builds, reviewer agents
- **Fast** (seconds): lint, typecheck, simple codebase patterns

### 3. Launch All Verifiers in Parallel

Launch ALL criteria in a single parallel call, **slow ones first** in the array. Claude Code caps at ~10 concurrent and queues the rest—by putting slow ones first, they start immediately and fast ones fill in as slots free up.

```
// Single message with multiple Task calls - slow first
Task(subagent_type="vibe-experimental:code-bugs-reviewer", prompt="
Review the current branch changes for bugs. Focus on HIGH and CRITICAL severity issues only.
Scope: git diff against origin/main")

Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: AC-1 (tests-pass)
Description: All tests pass
Verification method: bash
Command: npm test")

// ... other slow checks ...

// Then fast checks
Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: AC-7 (error-pattern)
Description: All errors use AppError class
Verification method: codebase
Files: src/handlers/
Check: No raw throw new Error() in modified files")

// ... other fast checks ...
```

**Scope override**: If /do provides explicit scope (e.g., specific files changed), pass it to reviewers:
```
Task(subagent_type="vibe-experimental:code-bugs-reviewer", prompt="
Review these files for bugs: src/handlers/notify.ts, src/services/queue.ts
Focus on HIGH and CRITICAL severity issues only.")
```

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

Parse the reviewer's report based on the criterion's `prompt` field which specifies pass conditions in natural language:

Examples:
- `prompt: "Review for bugs. Pass if no HIGH or CRITICAL severity issues."` → FAIL if any HIGH/CRITICAL found
- `prompt: "Check docs accuracy. Pass if no MEDIUM+ issues."` → FAIL if any MEDIUM/HIGH/CRITICAL found

1. Read the `prompt` field from the criterion definition
2. Parse the pass condition (e.g., "Pass if no HIGH or CRITICAL")
3. Look for severity headers in the agent's report
4. Apply the condition: issues violating it → criterion FAILS

Convert to same structure:
```
{
  "id": "AC-15",
  "category": "quality-gate",
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

- **AC-15** (category: quality-gate): No HIGH or CRITICAL bugs
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
2. **Single parallel launch** - all criteria in one call, slow ones first in array
3. **Slow first** - Claude Code queues in order; slow ones get first slots, fast ones fill in
4. **Hide manual on auto-fail** - focus on fixable issues first
5. **Actionable feedback** - pass through file:line, expected vs actual from agents
6. **Call /done on success** - trigger completion
7. **Parse prompt for pass condition** - quality-gate criteria specify pass conditions in natural language
8. **Return all issues** - for failed criteria, include all issues so /do can fix them
