---
name: verify
description: 'Internal verification runner. Executes all verification methods from spec against codebase. Called by /implement, not directly by users.'
user-invocable: false
---

# /verify - Verification Runner

You run all verification methods from a spec file against the current codebase state. You are called by /implement, not directly by users.

## Input

`$ARGUMENTS` = "<spec-file-path> <implementation-log-path>"

Example: `/tmp/spec-123.md /tmp/implement-log-123.md`

## Process

### 1. Parse Inputs

Read both files:
- Spec file: extract all criteria and their verification methods
- Implementation log: understand what was attempted (for context in subagent checks)

### 2. Categorize Criteria

Group by verification method:
- **bash**: Shell commands (npm test, tsc, lint, etc.)
- **subagent**: Code pattern checks via Task tool
- **manual**: Require human verification

### 3. Run Bash Verifications

For each bash criterion:
```bash
# Run with higher timeout (5 minutes default)
# Retry once on transient failures (network, flaky tests)
```

Capture:
- Exit code
- stdout/stderr
- Specific failure location if detectable

### 4. Run Subagent Verifications

Launch in parallel waves (max 5 concurrent):

```
Use the Task tool to check criterion AC-N:
Task("vibe-experimental", "criteria-checker", "Check AC-N: [description]. Context: [relevant files]. Checks: [from spec]")
```

For each subagent:
- Provide criterion definition
- Provide relevant code files
- Provide implementation log excerpt
- Request pass/fail with specific file:line issues

### 5. Collect Results

Build results structure:
```
{
  "passed": ["AC-1", "AC-2", ...],
  "failed": [
    {
      "id": "AC-3",
      "method": "bash",
      "command": "npm test",
      "location": "src/foo.test.ts:45",
      "expected": "'queued'",
      "actual": "'sent'"
    },
    {
      "id": "AC-7",
      "method": "subagent",
      "location": "src/handlers/notify.ts:23",
      "issue": "Raw Error() throw, expected AppError"
    }
  ],
  "manual": ["AC-10", "AC-11"]
}
```

### 6. Decision Logic

```
if any automated failed:
    → Return failures only (hide manual)
    → /implement continues working

elif all automated pass AND manual exists:
    → Return manual criteria
    → Hint to call /escalate for human review

elif all pass (no manual):
    → Call /done
```

### 7. Output Format

#### On Failure

```markdown
## Verification Results

### Failed (N)

- **AC-3**: tests-pass
  Method: bash (`npm test`)
  Location: `src/notifications.test.ts:45`
  Expected: `'queued'`
  Actual: `'sent'`

- **AC-7**: error-pattern
  Method: subagent (criteria-checker)
  Location: `src/handlers/notify.ts:23`
  Issue: Raw Error() throw, expected AppError

### Passed (M)
- AC-1: no-type-errors
- AC-2: lint-clean
- AC-4: file-structure
- AC-5: naming-conventions
- AC-6: no-console-logs

---

Continue working on failed criteria, then call /verify again.
```

#### On Success with Manual

```markdown
## Verification Results

### All Automated Criteria Pass

### Manual Verification Required (N)

These criteria require human review:

- **AC-10**: ux-feels-right
  Verification: Manual review of UI flow

- **AC-11**: performance-acceptable
  Verification: Manual load testing

---

All automated criteria verified. To complete:
- If manual criteria are acceptable: call /escalate to surface for human review
- Human will verify manual criteria and approve completion
```

#### On Full Success

Call /done:
```
Use the Skill tool to complete: Skill("vibe-experimental:done", "all criteria verified")
```

## Verification Quality Requirements

### Actionable Feedback

Every failure MUST include:
- Specific file:line location (where applicable)
- Expected vs actual (what was wrong)
- Actionable fix guidance (not vague "fix this")

### Subagent Instructions

When spawning criteria-checker:
```
Check [criterion description].

Context files:
- [file1]: [what it contains]
- [file2]: [what it contains]

Implementation log excerpt:
[relevant attempts for this criterion]

Specific checks:
1. [check from spec]
2. [check from spec]

Output format:
- PASS or FAIL
- If FAIL: file:line, expected, actual, fix suggestion
```

## Critical Rules

1. **Not user-invocable** - only called by /implement
2. **Check actual files** - state is codebase, not git history
3. **Parallel subagents** - waves of 5 for efficiency
4. **Hide manual on auto-fail** - focus on fixable issues first
5. **Actionable feedback** - specific locations, expected vs actual
6. **Call /done on success** - don't just return, trigger completion
