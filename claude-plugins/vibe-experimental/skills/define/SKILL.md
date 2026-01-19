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

Every criterion MUST have an explicit verification method.

**Verification methods**: Bash for deterministic checks (e.g., lint, test, typecheck) | Subagent for logic/reasoning/judgment | Manual only when automation is impossible.

## Input

`$ARGUMENTS` = task description, optionally with context/research

If no arguments provided, ask: "What would you like to build or change?"

If context is provided (file reference, inline notes), read it and ask what MUST be incorporated.

## Output

Manifest file: `/tmp/manifest-{timestamp}.md`

## Principles

These are non-negotiable:

1. **YOU generate, user validates** - Don't ask open-ended questions. Generate candidates from domain knowledge, present concrete options, learn from reactions.

2. **Only ask what you can't determine** - If you can infer task type, scope, or risk from context, don't ask. Only ask when genuinely ambiguous.

3. **Every criterion has verification** - You propose the method based on what's being verified.

4. **No vague terms** - "clean", "good", "proper" must become measurable criteria.

5. **Write to log as you go** - Capture findings to `/tmp/define-interview-{timestamp}.md` to preserve context.

6. **Know when to stop** - Happy path + errors + edges + constraints = sufficient. Don't over-interview.

## What You Need to Discover

Use your judgment on HOW to discover these. The goal is a complete manifest, not following a script.

### 1. Deliverables

What specific things need to be built or changed?

**Heuristics** (use when helpful):
- Simple/localized tasks → usually 1 deliverable
- Component-level work → 1-3 deliverables
- Cross-cutting changes → 3-5 deliverables
- System-wide changes → 5+ deliverables

### 2. Acceptance Criteria (per deliverable)

How do we know each deliverable is done?

**Coverage areas** (adapt to context):
- Happy path - core functionality works
- Error handling - graceful failures
- Edge cases - boundary conditions
- Constraints - how it must (or must not) be built

ACs can be **positive** ("user can log in") or **negative** ("passwords not stored in plaintext").

### 3. Global Invariants

What rules apply to the ENTIRE task? If violated anywhere, the task fails.

**For coding tasks**, auto-detect from CLAUDE.md:
- Tests, linting, type checking, formatting commands

**Generate candidates based on context**:
- Task type and risk level inform what invariants make sense
- Quality reviewers (subagent-based) for deeper checks when warranted

**For non-coding tasks**, adapt:
- Writing: spelling, tone, word limits
- Research: citations, methodology

## Reference: Conceptual Framework

| Type | Question | Scope | Failure Semantics |
|------|----------|-------|-------------------|
| **Global Invariant** | "What rules must NEVER be violated?" | Entire task | Task FAILS if violated |
| **Acceptance Criteria** | "How do we know THIS deliverable is done?" | Single deliverable | Deliverable incomplete if not met |

### Examples Across Domains

**Coding:**
- Global Invariant: "Tests must pass" (INV-G1)
- Deliverable: "Add user authentication"
  - AC: "User can log in with valid credentials" (AC-1.1)
  - AC: "Passwords are hashed, not stored in plaintext" (AC-1.2)

**Writing:**
- Global Invariant: "No spelling errors" (INV-G1)
- Deliverable: "Executive summary"
  - AC: "Key findings are summarized" (AC-1.1)
  - AC: "Under 500 words" (AC-1.2)

**Research:**
- Global Invariant: "All claims have citations" (INV-G1)
- Deliverable: "Literature review"
  - AC: "Covers major approaches" (AC-1.1)
  - AC: "Only uses peer-reviewed sources" (AC-1.2)

## Reference: Heuristics

Use these when they're helpful, not as checklists.

### AC Generation by Deliverable Type

| Deliverable Type | Typical ACs |
|-----------------|-------------|
| API endpoint | Request/response format, auth, error codes, rate limiting |
| UI component | Renders correctly, handles input, accessibility, responsive |
| Data operation | CRUD works, validation, constraints enforced, idempotent |
| Integration | Connection handling, retry logic, timeout behavior |
| Algorithm | Correctness, performance bounds, edge cases |

### Global Invariant Candidates

| Context | Likely Invariants |
|---------|-------------------|
| High-risk feature | Tests pass, no regressions, security, linting |
| Low-risk feature | Tests pass, linting |
| Bug fix | Tests pass, specific regression test |
| Refactor | Tests pass, behavior unchanged, linting |

### Quality Reviewers (subagent-based)

| Quality Gate | Verification |
|--------------|--------------|
| No HIGH/CRITICAL bugs | subagent: code-bugs-reviewer |
| Type safety | subagent: type-safety-reviewer |
| Maintainability | subagent: code-maintainability-reviewer |
| Simplicity | subagent: code-simplicity-reviewer |

## Reference: Latent Discovery Techniques

Use when your generated candidates weren't sufficient.

**Tradeoff questions** - when you detect competing concerns (speed vs thoroughness, flexibility vs simplicity).

**Pre-mortem** - for high-risk tasks: "If this fails badly, what's the most likely cause?" Selected risks become invariants or ACs.

## Question Format

When you DO need to ask:
- 2-4 concrete options (users reveal criteria by reacting)
- First option = recommended (with "(Recommended)" suffix)
- Descriptions explain tradeoffs
- Batch related questions when possible

## The Manifest Schema

```markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts/architecture to understand]

## 2. Global Invariants (The Constitution)
*Rules that apply to the ENTIRE execution. If these fail, the task is failed.*

- [INV-G1] Description: ... | Verify: [Method]
  ```yaml
  verify:
    method: bash | subagent | manual
    command: "[if bash]"
    agent: "[if subagent]"
    prompt: "[if subagent]"
  ```

## 3. Deliverables (The Work)
*Ordered by dependency, then importance. Execute top-to-bottom.*

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

| Type | Format | Example | Scope |
|------|--------|---------|-------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 | Entire task |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1, AC-2.3 | Deliverable D |

## Amendment Protocol

Manifests support amendments during execution if genuine gaps are discovered:
- Reference original ID: "INV-G1.1 amends INV-G1"
- Track in manifest: `## Amendments\n- INV-G1.1 (date): [reason]`

## Complete

Output the manifest file path:

```text
Manifest complete: /tmp/manifest-{timestamp}.md

To execute: /do /tmp/manifest-{timestamp}.md
```
