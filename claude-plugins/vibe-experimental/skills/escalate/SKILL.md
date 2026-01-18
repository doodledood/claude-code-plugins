---
name: escalate
description: 'Internal escalation handler. Called by /do when genuinely stuck after verification. Requires structured evidence of attempts.'
user-invocable: false
---

# /escalate - Structured Escalation

You handle escalation when /do is genuinely stuck on a criterion. Requires /verify to have been called first.

## Input

`$ARGUMENTS` = escalation context

Example: "AC-4 blocking after 3 attempts" or "Manual criteria AC-10, AC-11 need human review"

## Process

### 1. Identify Escalation Type

**Blocking Criterion:**
- Automated criterion that can't be satisfied after multiple attempts
- Requires structured evidence

**Manual Criteria:**
- All automated pass, manual criteria need human review
- Less evidence required

### 2. Read Execution Log

Read `/tmp/do-log-*.md` to find:
- What was attempted for the blocking criterion
- Why each attempt failed
- Pattern of failures

### 3. Output Structured Escalation

#### For Blocking Criterion

```markdown
## Escalation: Criterion [AC-N] ([description])

### Summary
Unable to satisfy [criterion] after [N] attempts. Requesting human decision.

### Attempts (from execution log)

1. **[Approach 1]**
   What: [what was tried]
   Result: [what happened]
   Why failed: [specific reason]

2. **[Approach 2]**
   What: [what was tried]
   Result: [what happened]
   Why failed: [specific reason]

3. **[Approach 3]**
   What: [what was tried]
   Result: [what happened]
   Why failed: [specific reason]

### Hypothesis

[Theory about why this criterion may be problematic]

Examples:
- "Criterion assumes API exists that doesn't"
- "Criterion conflicts with AC-2"
- "Codebase architecture prevents this approach"

### Possible Resolutions

1. **[Option A]**: [description]
   Tradeoff: [what this changes]

2. **[Option B]**: [description]
   Tradeoff: [what this changes]

3. **[Option C]**: Amend criterion
   Suggested change: [new criterion wording]

### Requesting

Human decision on which path to take.

---

Escalation documented. You may now stop and review, or provide guidance to continue.
```

#### For Manual Criteria

```markdown
## Escalation: Manual Criteria Require Human Review

All automated criteria verified passing. The following require human verification:

### Manual Criteria

- **AC-10**: [description]
  How to verify: [instructions from definition]

- **AC-11**: [description]
  How to verify: [instructions from definition]

### Automated Results Summary

Passed: [N] criteria
- AC-1, AC-2, AC-3, ...

### What Was Executed

[Brief summary of changes]

---

Please review the manual criteria and confirm completion, or provide feedback for adjustments.
```

## Evidence Requirements

For blocking criterion escalation, MUST include:
1. **Which criterion** - specific AC-N
2. **At least 3 attempts** - what was tried
3. **Why each failed** - not just "didn't work"
4. **Hypothesis** - theory about root cause
5. **Options** - possible paths forward

Lazy escalations are NOT acceptable:
- "I can't figure this out"
- "Can you help?"
- "This is hard"

## Critical Rules

1. **Not user-invocable** - only called by /do
2. **Requires /verify first** - must attempt verification before escalating
3. **Structured evidence** - not lazy "help me" requests
4. **Options provided** - give human actionable choices
