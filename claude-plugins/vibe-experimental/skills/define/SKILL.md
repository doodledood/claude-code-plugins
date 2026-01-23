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

1. **Verifiable** - Every Invariant and AC has a verification method (bash, subagent, manual). Constraints that can't be verified from output go in Process Guidance.

2. **Validated** - You drive the interview. Generate concrete candidates; learn from user reactions.

3. **Complete** - Surface hidden requirements through outside view (what typically fails in similar projects?), pre-mortem (what could go wrong?), and non-obvious probing (what hasn't user considered?).

4. **Efficient** - Prioritize questions that eliminate the most uncertainty. Minimize cognitive load per exchange. Reduce friction, not coverage.

## Constraints

**When uncertain, ask** - Never assume or infer requirements. If you're unsure, probe—don't produce an answer.

**Confirm before encoding** - When you discover constraints from codebase analysis (technical limits, architecture patterns, API boundaries), present them to the user before encoding as invariants. "I found X in the codebase—should this be a hard constraint?" Discovered ≠ confirmed.

**Encode explicit constraints** - When users state preferences, requirements, or constraints (not clarifying remarks or exploratory responses), these must map to an INV or AC. "Manual optimization only" → process invariant. "Target < 1500" → acceptance criterion. Don't let explicit constraints get lost in the interview log.

**Probe for approach constraints** - Beyond WHAT to build, ask HOW it should be done. Tools to use or avoid? Methods required or forbidden? Automation vs manual? These become process invariants.

**Todo list immediately** - Adapt to task. Required: log file (`/tmp/define-interview-{timestamp}.md`), `→log` after discovery, `(expand: ...)` for emerging areas, `Refresh: read full log` before synthesis, `Verify manifest` → `(fix gaps if CONTINUE)` loop, acceptance criteria ("; done when X"). Update after every action.

**Write to log as you go** - Don't wait until the end.

**Refresh before synthesis** - Read full interview log to restore context.

**Stop when converged** - Before marking any area complete, verify you've challenged it from multiple angles. Prefer "I haven't fully explored X" over premature closure. Move to synthesis when probing genuinely yields no new criteria, or user signals "enough".

**Verify before finalizing** - After writing manifest, spawn manifest-verifier: `Task("manifest-verifier", "Manifest: /tmp/manifest-{ts}.md | Log: /tmp/define-interview-{ts}.md")`. If status is CONTINUE, ask the outputted questions, log new answers, update manifest, re-verify. Loop until COMPLETE or user signals "enough".

**Insights become criteria** - Outside view findings, pre-mortem risks, non-obvious discoveries → convert to INV-G* or AC-*. No standalone value.

**Prefer automated verification** - Use bash commands when possible. For inspections that aren't easily bash-verifiable, use a subagent to review the codebase. Reserve manual verification for criteria that no automated method can validate.

## What the Manifest Needs

Three categories, each covering **output** or **process**:

- **Global Invariants** - "Don't do X" (negative constraints, ongoing, verifiable). Output: "No breaking changes to public API." Process: "Don't edit files in /legacy."
- **Process Guidance** - Non-verifiable constraints on HOW to work. Approach requirements, methodology, tool preferences that cannot be checked from the output alone (e.g., "manual optimization only" - you can't tell from the final code whether it was manually written or generated). These guide the implementer but aren't gates.
- **Deliverables + ACs** - "Must have done X" (positive milestones). Three types:
  - *Functional*: "Clicking Login redirects to Dashboard"
  - *Non-Functional*: "Response time < 200ms"
  - *Process*: "README.md contains section 'Authentication'"

### Code Quality Gates (for coding tasks)

For coding tasks, surface which quality aspects matter: bugs, type safety, maintainability, simplicity, coverage, testability, documentation, CLAUDE.md adherence. Present as multi-select with the first option marked "(Recommended)" to reduce cognitive load. Map selections to corresponding reviewer agents with "no HIGH/CRITICAL" thresholds (docs uses "no MEDIUM+").

**Filter through project preferences**: CLAUDE.md is auto-loaded into context—check it for quality gate preferences. Users may have disabled certain default gates (e.g., "skip documentation checks") or added custom ones (e.g., "always run security scan"). Exclude disabled gates from the selection, and include any custom gates the user has defined.

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

## The Manifest Schema

````markdown
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

## 3. Process Guidance (Non-Verifiable)
*Constraints on HOW to work. Not gates—guidance for the implementer.*

- [PG-1] Description: ...

## 4. Deliverables (The Work)
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
````

## ID Scheme

| Type | Format | Example |
|------|--------|---------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 |
| Process Guidance | PG-{N} | PG-1, PG-2 |
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
