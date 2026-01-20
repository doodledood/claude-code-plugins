---
name: define
description: 'Manifest builder with verification criteria. Converts known requirements into Deliverables + Invariants. Use when you need done criteria, acceptance tests, quality gates—not for requirements discovery. Outputs executable manifest.'
user-invocable: true
---

# /define - Manifest Builder

## Goal

Build a **comprehensive Manifest** that captures:
- **What we build** (Deliverables with Acceptance Criteria)
- **Rules we must follow** (Global Invariants)

**Why thoroughness matters**: Every criterion discovered NOW is one fewer rejection during implementation/review. The goal is a PR that passes on first submission—no "oh, I also needed X" after the work is done.

Comprehensive means surfacing **latent criteria**—requirements the user doesn't know they have until probed. Users know their surface-level needs; your job is to discover the constraints and edge cases they haven't thought about.

You can't get to 100% upfront—some criteria only emerge during implementation. But strive for high coverage. The manifest supports amendments for what's discovered later.

Output: `/tmp/manifest-{timestamp}.md`

## Input

`$ARGUMENTS` = task description, optionally with context/research

If no arguments provided, ask: "What would you like to build or change?"

## Principles

1. **YOU generate, user validates** - Don't ask open-ended questions. Generate concrete candidates; learn from reactions.

2. **Only ask what you can't determine** - If you can infer from context, don't ask. Only ask when genuinely ambiguous.

3. **Every criterion has verification** - Bash for deterministic checks (e.g., lint, test, typecheck). Subagent for logic/reasoning/judgment. Manual only when automation impossible.

4. **No vague terms** - "clean", "good", "proper" must become measurable.

5. **Diminishing returns, not premature stop** - Be thorough in surfacing latent criteria, but recognize when additional probing isn't yielding new insights.

6. **ACs are observable behaviors** - "User sees X" not "Code does Y". Test: could a non-engineer verify this by looking at the result?

7. **Explicitly surface edge cases** - After core behavior, ask about edge cases. Generate concrete scenarios (empty states, null inputs, boundaries, concurrent access) as options.

## Constraints

**Create todo list immediately** - Track what needs to be discovered. Expand as you learn more.

**Write to log as you go** - Capture findings to `/tmp/define-interview-{timestamp}.md` after each discovery. Don't wait until the end.

**Refresh before synthesis** - Before writing the final manifest, read the full interview log to restore context.

**Stop when converged** - When probing yields no new criteria, or user signals "enough", move to synthesis.

**Pre-mortem every task** - Generate concrete failure scenarios as choices. User selects real risks → become preventive criteria.

## Todo Discipline

**Create todo list immediately** based on what THIS task needs—not a fixed template. Adapt structure to the specific requirements being defined.

**Required elements:**
- Log file creation (`/tmp/define-interview-{timestamp}.md`)
- `→log` after discovery steps (externalizes findings)
- `(expand: ...)` placeholder when areas will emerge
- `Refresh: read full log` before synthesis (restores context)
- Acceptance criteria on each todo ("; done when X")

**Update todos after every substantive action**—no batching completions.

## What the Manifest Needs

Surface latent criteria through generation, not interrogation. Generate candidates; learn from user reactions.

Both can cover **output** or **process**:

- **Global Invariants** - "Don't do X" (negative constraints, ongoing). Output: "No breaking changes to public API." Process: "Don't edit files in /legacy."
- **Deliverables + ACs** - "Must have done X" (positive milestones). Three types:
  - *Functional*: "Clicking Login redirects to Dashboard"
  - *Non-Functional*: "Response time < 200ms"
  - *Process*: "README.md contains section 'Authentication'"

### Code Quality Gates (for coding tasks)

For tasks involving code, ask users to **multi-select** which quality aspects they care about. Present both questions together.

**Filter through project preferences**: CLAUDE.md is auto-loaded into context—check it for quality gate preferences. Users may have disabled certain default gates (e.g., "skip documentation checks") or added custom ones (e.g., "always run security scan"). Exclude disabled gates from the selection, and include any custom gates the user has defined.

```
questions: [
  {
    question: "Which code quality checks should apply as global invariants?",
    header: "Quality",
    options: [
      { label: "No HIGH/CRITICAL bugs (Recommended)", description: "Logic errors, race conditions, error handling" },
      { label: "Type safety", description: "No any abuse, proper narrowing, invalid states unrepresentable" },
      { label: "Maintainability", description: "DRY, low coupling, consistency, no dead code" },
      { label: "Simplicity", description: "No over-engineering, appropriate complexity" }
    ],
    multiSelect: true
  },
  {
    question: "Additional quality checks:",
    header: "More quality",
    options: [
      { label: "Test coverage", description: "New/changed code has adequate tests" },
      { label: "Testability", description: "Code structure allows easy testing (low mock count)" },
      { label: "Documentation", description: "Docs and comments match code" },
      { label: "CLAUDE.md adherence", description: "Follows project-specific standards" }
    ],
    multiSelect: true
  }
]
```

**Map selections to reviewer agents:**

| Quality Aspect | Agent | Threshold |
|---------------|-------|-----------|
| No bugs | code-bugs-reviewer | no HIGH/CRITICAL |
| Type safety | type-safety-reviewer | no HIGH/CRITICAL |
| Maintainability | code-maintainability-reviewer | no HIGH/CRITICAL |
| Simplicity | code-simplicity-reviewer | no HIGH/CRITICAL |
| Test coverage | code-coverage-reviewer | no HIGH/CRITICAL |
| Testability | code-testability-reviewer | no HIGH/CRITICAL |
| Documentation | docs-reviewer | no MEDIUM+ (max severity is MEDIUM) |
| CLAUDE.md adherence | claude-md-adherence-reviewer | no HIGH/CRITICAL |

Add selected quality gates as Global Invariants with subagent verification:
```yaml
verify:
  method: subagent
  agent: [agent-name-from-table]
  prompt: "Review for [quality aspect] issues in the changed files"
```

### Project Gates (auto-detect from CLAUDE.md)

For coding tasks, read CLAUDE.md and extract verifiable commands (typecheck, lint, test, format). Add as Global Invariants with bash verification:
```yaml
verify:
  method: bash
  command: "[command from CLAUDE.md]"
```

## Conceptual Framework

| Type | Question | Scope | Failure |
|------|----------|-------|---------|
| **Global Invariant** | "What must NEVER be violated?" | Entire task | Task FAILS |
| **Acceptance Criteria** | "How do we know THIS is done?" | Single deliverable | Incomplete |

## Question Format

When presenting options, mark the first as "(Recommended)" to reduce cognitive load.

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

## 5. Pre-mortem Risks
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
