---
name: escalate
description: 'Structured escalation with evidence. Surfaces blocking issues for human decision, referencing the Manifest hierarchy.'
user-invocable: false
---

# /escalate - Structured Escalation

Surface a blocking issue for human decision with structured evidence, referencing the Manifest hierarchy.

## Input

`$ARGUMENTS` = escalation context

Examples:
- "INV-G1 blocking after 3 attempts"
- "INV-L1.2 conflicts with AC-1.1"
- "Manual criteria AC-2.3 needs human review"

## Escalation Types

### 1. Global Invariant Blocking

A Global Invariant that can't be satisfied—task-level blocker.

Read execution log (`/tmp/do-log-*.md`) to find what was attempted.

Output:

```markdown
## Escalation: Global Invariant [INV-G{N}] Blocking

**Criterion:** [description]
**Type:** Global Invariant (task fails if violated)
**Impact:** Cannot complete task until resolved

### Summary

Unable to satisfy this global invariant after [N] attempts. This is a task-level blocker—no deliverables can be considered complete while this fails.

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

[Theory about why this invariant may be problematic]

Examples:
- "Tests fail due to external dependency issue, not code problem"
- "Invariant conflicts with project reality (tests were already failing)"
- "Requirement is impossible given current architecture"

### Possible Resolutions

1. **Fix the root cause**: [description]
   Effort: [estimate]
   Risk: [what could go wrong]

2. **Amend the invariant**: Relax INV-G{N} to [new wording]
   Rationale: [why this is acceptable]

3. **Remove the invariant**: This rule doesn't apply to this task
   Rationale: [why it's not needed]

### Requesting

Human decision on which path to take.
```

### 2. Local Invariant Blocking

A Local Invariant specific to one deliverable.

```markdown
## Escalation: Local Invariant [INV-L{D}.{N}] Blocking

**Criterion:** [description]
**Type:** Local Invariant for Deliverable {D}: [deliverable name]
**Impact:** Deliverable {D} cannot be completed while constraint violated

### Summary

Unable to respect this constraint while building Deliverable {D}.

### Context

**Deliverable:** [name]
**Goal:** [what this deliverable is trying to achieve]
**Constraint:** [the local invariant that can't be satisfied]

### Attempts

1. **[Approach 1]**
   What: [what was tried]
   How it violated constraint: [specific reason]

2. **[Approach 2]**
   ...

### Conflict Analysis

[If this conflicts with an AC or another invariant, explain]

- INV-L{D}.{N} requires: [constraint]
- But AC-{D}.{M} requires: [conflicting requirement]
- These conflict because: [explanation]

### Possible Resolutions

1. **Prioritize the invariant**: Change approach to AC-{D}.{M}
   Tradeoff: [what changes]

2. **Prioritize the AC**: Amend INV-L{D}.{N} to allow [exception]
   Tradeoff: [what constraint is relaxed]

3. **Redesign the deliverable**: [alternative approach]
   Tradeoff: [scope change]

### Requesting

Human decision on which constraint to prioritize.
```

### 3. Acceptance Criteria Blocking

An AC that can't be satisfied.

```markdown
## Escalation: Acceptance Criteria [AC-{D}.{N}] Blocking

**Criterion:** [description]
**Type:** Acceptance Criteria for Deliverable {D}: [deliverable name]
**Impact:** Deliverable {D} incomplete

### Summary

Unable to satisfy this acceptance criterion after [N] attempts.

### Context

**Deliverable:** [name]
**Local Invariants respected:** [list]
**Other ACs in this deliverable:**
- AC-{D}.1: [status]
- AC-{D}.2: [status]
- AC-{D}.{N}: BLOCKING

### Attempts

1. **[Approach 1]**
   What: [what was tried]
   Result: [what happened]
   Why failed: [specific reason]

2. ...

### Hypothesis

[Theory about root cause]

### Possible Resolutions

1. **Different implementation**: [approach]

2. **Amend the criterion**: Change AC-{D}.{N} to [new wording]
   Rationale: [why original was wrong/unrealistic]

3. **Remove the criterion**: This isn't actually needed
   Rationale: [why]

4. **Descope the deliverable**: Remove this AC, deliverable still valuable
   Impact: [what's lost]

### Requesting

Human decision on path forward.
```

### 4. Manual Criteria Review

All automated criteria pass, manual criteria need human verification.

```markdown
## Escalation: Manual Criteria Require Human Review

All automated criteria verified passing. The following require human verification:

### Global Invariants
All [N] global invariants pass.

### Deliverables Summary

| Deliverable | Local Invariants | Automated ACs | Manual ACs |
|-------------|-----------------|---------------|------------|
| 1: [name] | All respected | [n]/[m] pass | [k] pending |
| 2: [name] | All respected | [n]/[m] pass | [k] pending |

### Manual Criteria Pending

#### Deliverable 1: [Name]

- **AC-1.3**: [description]
  How to verify: [instructions from manifest]

#### Deliverable 2: [Name]

- **AC-2.4**: [description]
  How to verify: [instructions from manifest]

### What Was Executed

[Brief summary of changes made]

### Key Files Changed

| File | Purpose |
|------|---------|
| [file] | [what changed] |

---

Please review the manual criteria and confirm completion.
```

## Evidence Requirements

For blocking criterion escalation, MUST include:

1. **Which criterion** - specific ID (INV-G*, INV-L*.*, AC-*.*)
2. **Criterion type** - global-invariant, local-invariant, or acceptance-criteria
3. **Scope** - task-level or which deliverable
4. **At least 3 attempts** - what was tried
5. **Why each failed** - not just "didn't work"
6. **Hypothesis** - theory about root cause
7. **Options** - possible paths forward with tradeoffs

## Lazy Escalations Are NOT Acceptable

These are rejected:
- "I can't figure this out"
- "Can you help?"
- "This is hard"
- "INV-G1 is failing" (without attempts)

## ID Reference

| Type | Pattern | Example | Scope |
|------|---------|---------|-------|
| Global Invariant | INV-G{N} | INV-G1 | Entire task |
| Local Invariant | INV-L{D}.{N} | INV-L1.2 | Deliverable D |
| Acceptance Criteria | AC-{D}.{N} | AC-2.3 | Deliverable D |
