---
name: define
description: 'Manifest builder. Creates hierarchical definitions separating Deliverables (what to build) from Invariants (rules to follow). Use when starting new features, refactors, or any work requiring clear done criteria.'
user-invocable: true
---

# /define - Manifest Builder

## Goal

Build a **Manifest** that separates:
- **What we build** (Deliverables with Acceptance Criteria)
- **Rules we must follow** (Global Invariants)

Output: `/tmp/manifest-{timestamp}.md`

## Input

`$ARGUMENTS` = task description, optionally with context/research

If no arguments provided, ask: "What would you like to build or change?"

## Principles

1. **YOU generate, user validates** - Don't ask open-ended questions. Generate candidates from domain knowledge, present concrete options, learn from reactions.

2. **Only ask what you can't determine** - If you can infer from context, don't ask. Only ask when genuinely ambiguous.

3. **Every criterion has verification** - Bash for deterministic checks (e.g., lint, test, typecheck). Subagent for logic/reasoning/judgment. Manual only when automation impossible.

4. **No vague terms** - "clean", "good", "proper" must become measurable.

5. **Know when to stop** - Don't over-interview. When you have enough to build the manifest, build it.

## Context Preservation

Write findings to `/tmp/define-interview-{timestamp}.md` as you discover them.

Before writing the final manifest, read the full interview log to restore context.

## What the Manifest Needs

Discover these through interview - use your judgment on how:

### Deliverables
What specific things need to be built or changed? Decompose based on task complexity.

### Acceptance Criteria (per deliverable)
How do we know each deliverable is done? Cover what matters: functionality, error handling, edge cases, constraints. ACs can be positive or negative.

### Global Invariants
What rules apply to the ENTIRE task? If violated anywhere, task fails. For coding tasks, auto-detect from CLAUDE.md (tests, linting, type checks). Adapt to domain.

## Conceptual Framework

| Type | Question | Scope | Failure |
|------|----------|-------|---------|
| **Global Invariant** | "What must NEVER be violated?" | Entire task | Task FAILS |
| **Acceptance Criteria** | "How do we know THIS is done?" | Single deliverable | Incomplete |

## Question Format

When you need to ask:
- 2-4 concrete options (users reveal criteria by reacting)
- First option = recommended (with "(Recommended)" suffix)
- Batch related questions when possible

## The Manifest Schema

```markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]

## 2. Global Invariants (The Constitution)
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Description: ... | Verify: [Method]
  ```yaml
  verify:
    method: bash | subagent | manual
    command: "[if bash]"
    agent: "[if subagent]"
    prompt: "[if subagent]"
  ```

## 3. Deliverables (The Work)
*Ordered by dependency, then importance.*

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: ... | Verify: ...
  ```yaml
  verify:
    method: bash | subagent | codebase | manual
    [details]
  ```

### Deliverable 2: [Name]
...

## 4. Tradeoffs & Preferences (if any)
| Dimension | Preference | Context |
|-----------|------------|---------|

## 5. Pre-mortem Risks (if any)
| Risk | Preventive Measure |
|------|-------------------|
```

## ID Scheme

| Type | Format | Example |
|------|--------|---------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1, AC-2.3 |

## Amendment Protocol

Manifests support amendments during execution:
- Reference original ID: "INV-G1.1 amends INV-G1"
- Track in manifest: `## Amendments`

## Complete

```text
Manifest complete: /tmp/manifest-{timestamp}.md

To execute: /do /tmp/manifest-{timestamp}.md
```
