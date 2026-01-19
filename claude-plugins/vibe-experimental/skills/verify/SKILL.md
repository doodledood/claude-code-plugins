---
name: verify
description: 'Manifest verification runner. Spawns parallel verifiers for Global Invariants and Acceptance Criteria. Called by /do, not directly by users.'
user-invocable: false
---

# /verify - Manifest Verification Runner

## Goal

Run all verification methods from a Manifest. Spawn one verifier agent per criterion in parallel. Report results grouped by type.

## Input

`$ARGUMENTS` = "<manifest-file-path> <execution-log-path> [--scope=files]"

## Principles

1. **Don't run checks yourself** - Spawn criteria-checker or reviewer agents. You orchestrate, they verify.

2. **Single parallel launch** - All criteria in one call, slow ones first (tests, builds, reviewers before lint/typecheck).

3. **Global failures are critical** - Highlight prominently. Task can't succeed while these fail.

4. **Actionable feedback** - Pass through file:line, expected vs actual, fix hints.

## What to Do

**Parse inputs** - Extract all criteria with verification methods from manifest. Read execution log for context.

**Categorize by method:**
- `bash`: Shell commands (tests, lint, typecheck)
- `subagent`: Reviewer agents
- `codebase`: Code pattern checks
- `manual`: Set aside for human verification

**Launch verifiers** - One Task per criterion, all in parallel. Pass criterion ID, description, verification method, and relevant context.

**Collect and report results** - Group by Global Invariants first, then by Deliverable.

## Decision Logic

```
if any Global Invariant failed:
    → Return ALL failures, globals highlighted prominently

elif any AC failed:
    → Return failures grouped by deliverable

elif all automated pass AND manual exists:
    → Return manual criteria, hint to call /escalate

elif all pass:
    → Call /done
```

## Output Format

**On failure:**
```markdown
## Verification Results

### Global Invariants

#### Failed (N)
- **INV-G1**: [description]
  Method: [method]
  [failure details with location, expected/actual, fix hint]

#### Passed (M)
- INV-G2, INV-G3

---

### Deliverable 1: [Name]

#### Failed
- **AC-1.2**: [description]
  [failure details]

#### Passed
- AC-1.1

---

**Summary:**
- Global Invariants: X/Y failed (fix first)
- Deliverable 1: A/B ACs failed
```

**On success with manual:**
```markdown
## Verification Results

All automated criteria pass.

### Manual Verification Required
- **AC-1.3**: [description] - How to verify: [from manifest]

Call /escalate to surface for human review.
```

**On full success:**
Call `/done`.

## Criterion Types

| Type | Pattern | Failure Impact |
|------|---------|----------------|
| Global Invariant | INV-G{N} | Task fails |
| Acceptance Criteria | AC-{D}.{N} | Deliverable incomplete |
