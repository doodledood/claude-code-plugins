---
name: define
description: 'Manifest builder with verification criteria. Converts known requirements into Deliverables + Invariants. Use when you need done criteria, acceptance tests, quality gates—not for requirements discovery. Outputs executable manifest.'
user-invocable: true
---

# /define - Manifest Builder

## Goal

Build a **comprehensive Manifest** that captures:
- **What we build** (Deliverables with Acceptance Criteria)
- **How we'll get there** (Approach - validated direction)
- **Rules we must follow** (Global Invariants)

**Why thoroughness matters**: Every criterion discovered NOW is one fewer rejection during implementation/review. The goal is a PR that passes on first submission—no "oh, I also needed X" after the work is done.

Comprehensive means surfacing **latent criteria**—requirements the user doesn't know they have until probed. Users know their surface-level needs; your job is to discover the constraints and edge cases they haven't thought about.

100% upfront is impossible—some criteria only emerge during implementation. Aim for high coverage. The manifest supports amendments for what's discovered later.

Output: `/tmp/manifest-{timestamp}.md`

## Input

`$ARGUMENTS` = task description, optionally with context/research

If no arguments provided, ask: "What would you like to build or change?"

## Principles

1. **Verifiable** - Every Invariant and AC has a verification method (bash, subagent, manual). Constraints that can't be verified from output go in Process Guidance.

2. **Validated** - You drive the interview. Generate concrete candidates; learn from user reactions.

3. **Domain-grounded** - Before probing for criteria, understand the domain: explore codebase for patterns/constraints, research unfamiliar domains, ask for business context. Latent criteria emerge from domain understanding—you can't surface what you don't know.

4. **Complete** - Surface hidden requirements through outside view (what typically fails in similar projects?), pre-mortem (what could go wrong?), and non-obvious probing (what hasn't user considered?).

5. **Directed** - For complex tasks, establish validated implementation direction (Approach) before execution. Architecture defines direction, not step-by-step script. Trade-offs enable autonomous adjustment.

6. **Efficient** - Maximize information per question, not minimize questions. One missed criterion costs more than one extra question. Prioritize questions that eliminate the most uncertainty. Mark recommended option(s): for single-select questions, mark exactly one option "(Recommended)"; for multi-select, mark zero or more based on context (none if all equally valid, or sensible defaults if applicable).

## Constraints

**Discoverable unknowns — search first** - Facts about the codebase or system (file locations, API shapes, existing patterns, config values) are discoverable. Exhaust codebase search before asking the user. Only ask about discoverable facts when: multiple plausible candidates exist, searches yield nothing but the fact is needed, or the ambiguity is actually about intent not fact. When asking, present what you found and recommend one option.

**Preference unknowns — ask early** - Trade-offs, priorities, scope decisions, and style preferences cannot be discovered from code. Ask these directly. Provide concrete options with a recommended default. If genuinely low-impact and the user signals "enough", proceed with the recommended default and record as a Known Assumption in the manifest.

**Confirm before encoding** - When you discover constraints from codebase analysis (technical limits, architecture patterns, API boundaries), present them to the user before encoding as invariants. "I found X in the codebase—should this be a hard constraint?" Discovered ≠ confirmed.

**Encode explicit constraints** - When users state preferences, requirements, or constraints (not clarifying remarks or exploratory responses), these must map to an INV or AC. "Manual optimization only" → process invariant. "Target < 1500" → acceptance criterion. Don't let explicit constraints get lost in the interview log.

**Probe for approach constraints** - Beyond WHAT to build, ask HOW it should be done. Tools to use or avoid? Methods required or forbidden? Automation vs manual? These become process invariants.

**Probe input artifacts** - When input references external documents (file paths, URLs), ask: "Should [document] be a verification source?" If yes, encode as Global Invariant.

**Log after every action** - Write to `/tmp/define-discovery-{timestamp}.md` immediately after each discovery (domain findings, interview answers, codebase insights). Goal: another agent reading only the log could resume the interview. Read full log before synthesis.

**Confirm understanding periodically** - Before transitioning to a new topic area or after resolving a cluster of related questions, synthesize your current understanding back to the user: "Here's what I've established so far: [summary]. Correct?" This catches interpretation drift early—a misunderstanding in round 2 compounds through round 8 if never checked.

**Stop when converged** - Err on more probing. Convergence requires: pre-mortem checked, domain understood, edge cases probed, and no obvious areas left unexplored. Only then, if very confident further questions would yield nothing new, move to synthesis. Remaining low-impact unknowns that don't warrant further probing are recorded as Known Assumptions in the manifest. User can signal "enough" to override.

**Verify before finalizing** - After writing manifest, verify completeness using the manifest-verifier agent with the manifest and discovery log as input. If status is CONTINUE, ask the outputted questions, log new answers, update manifest, re-verify. Loop until COMPLETE or user signals "enough".

**Insights become criteria** - Outside view findings, pre-mortem risks, non-obvious discoveries → convert to INV-G* or AC-*. Don't include insights that aren't encoded as criteria.

**Prefer automated verification** - Automated methods (commands, subagent review) before manual. Reserve manual verification for criteria that no automated method can validate.

## Approach Section (Complex Tasks)

After defining deliverables, probe for implementation direction. Skip for simple tasks with obvious approach.

**Architecture** - Generate concrete architectural options based on codebase patterns. "Given the intent, here are approaches: [A], [B], [C]. Which aligns with your codebase?" Architecture is direction (components, patterns, data flow), not step-by-step script.

**Execution Order** - Propose order based on dependencies. "Suggested order: D1 → D2 → D3. Rationale: [X]. Adjust?" Include why (dependencies, risk reduction, etc.).

**Risk Areas** - Pre-mortem outputs. "What could cause this to fail? Candidates: [R1], [R2], [R3]." Each risk has detection criteria. Not exhaustive—focus on likely/high-impact.

**Trade-offs** - Decision criteria for competing concerns. "When facing [tension], priority? [A] vs [B]?" Format: `[T-N] A vs B → Prefer A because X`. Enables autonomous adjustment during /do.

**When to include Approach**: Multi-deliverable tasks, unfamiliar domains, architectural decisions, high-risk implementations. The interview naturally reveals if it's needed.

**Architecture vs Process Guidance**: Architecture = structural decisions (components, patterns). Process Guidance = methodology constraints (tools, manual vs automated). "Add AuthService wrapping token logic" is Architecture. "No ORM, raw SQL only" is Process Guidance.

## What the Manifest Needs

Three categories, each covering **output** or **process**:

- **Global Invariants** - "Don't do X" (negative constraints, ongoing, verifiable). Output: "No breaking changes to public API." Process: "Don't edit files in /legacy."
- **Process Guidance** - Non-verifiable constraints on HOW to work. Approach requirements, methodology, tool preferences that cannot be checked from the output alone (e.g., "manual optimization only" - you can't tell from the final code whether it was manually written or generated). These guide the implementer but aren't gates.
- **Deliverables + ACs** - "Must have done X" (positive milestones). Three types:
  - *Functional*: "Clicking Login redirects to Dashboard"
  - *Non-Functional*: "Response time < 200ms", "All handlers follow Repository pattern"
  - *Process*: "README.md contains section 'Authentication'"

### Code Quality Gates (for coding tasks)

For coding tasks, surface which quality aspects matter: bugs, type safety, maintainability, simplicity, coverage, testability, documentation, CLAUDE.md adherence. Note: AskUserQuestion limits to 4 options per question. Mark the most appropriate option(s) as "(Recommended)" based on task context. Map selections to corresponding reviewer agents with "no HIGH/CRITICAL" thresholds (docs uses "no MEDIUM+").

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

For coding tasks, extract verifiable commands from project configuration (typecheck, lint, test, format). Add as Global Invariants with bash verification:
```yaml
verify:
  method: bash
  command: "[command from CLAUDE.md]"
```

**Probe e2e verification** - For coding tasks, surface e2e verification opportunities: endpoints, services, test data. If actionable, encode as Global Invariant with bash verification.

## The Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]

## 2. Approach (Complex Tasks Only)
*Validated implementation direction. Omit for simple tasks.*

- **Architecture:** [High-level HOW - validated direction, not step-by-step]

- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: [why this order - dependencies, risk reduction, etc.]

- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
  - [R-2] [What could go wrong] | Detect: [how you'd know]

- **Trade-offs:**
  - [T-1] [Priority A] vs [Priority B] → Prefer [A] because [reason]
  - [T-2] [Priority X] vs [Priority Y] → Prefer [Y] because [reason]

## 3. Global Invariants (The Constitution)
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Description: ... | Verify: [Method]
  ```yaml
  verify:
    method: bash | codebase | subagent | research | manual
    command: "[if bash]"
    agent: "[if subagent]"
    prompt: "[if subagent or research]"
  ```

## 4. Process Guidance (Non-Verifiable)
*Constraints on HOW to work. Not gates—guidance for the implementer.*

- [PG-1] Description: ...

## 5. Known Assumptions
*Low-impact items where a reasonable default was chosen without explicit user confirmation. If any assumption is wrong, amend the manifest.*

- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables (The Work)
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: ... | Verify: ...
  ```yaml
  verify:
    method: bash | codebase | subagent | research | manual
    [details]
  ```

### Deliverable 2: [Name]
...
````

## ID Scheme

| Type | Format | Example | Used By |
|------|--------|---------|---------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 | /verify (verified) |
| Process Guidance | PG-{N} | PG-1, PG-2 | /do (followed) |
| Risk Area | R-{N} | R-1, R-2 | /do (watched) |
| Trade-off | T-{N} | T-1, T-2 | /do (consulted) |
| Known Assumption | ASM-{N} | ASM-1, ASM-2 | /verify (audited) |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1, AC-2.3 | /verify (verified) |

## Amendment Protocol

Manifests support amendments during execution:
- Reference original ID: "INV-G1.1 amends INV-G1"
- Track in manifest: `## Amendments`

## Complete

```text
Manifest complete: /tmp/manifest-{timestamp}.md

To execute: /do /tmp/manifest-{timestamp}.md
```
