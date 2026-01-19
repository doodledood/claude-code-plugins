# vibe-experimental

Manifest-driven workflows separating **what to build** (Deliverables) from **rules to follow** (Global Invariants).

## Overview

A two-level approach to task definition and execution:

1. **Global Invariants** - Rules that apply to the ENTIRE task (e.g., "tests must pass")
2. **Deliverables** - Specific items to complete, each with **Acceptance Criteria**
   - ACs can be positive ("user can log in") or negative ("passwords are hashed")

## The Manifest Schema

```markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts/architecture]

## 2. Global Invariants (The Constitution)
- [INV-G1] Description | Verify: [method]
- [INV-G2] Description | Verify: [method]

## 3. Deliverables (The Work)

### Deliverable 1: [Name]
- **Acceptance Criteria**:
  - [AC-1.1] Description | Verify: [method]
  - [AC-1.2] Description | Verify: [method]
```

## ID Scheme

| Type | Pattern | Scope | Failure Impact |
|------|---------|-------|----------------|
| Global Invariant | INV-G{N} | Entire task | Task fails |
| Acceptance Criteria | AC-{D}.{N} | Deliverable D | Deliverable incomplete |

## Skills

### User-Invocable

| Skill | Description |
|-------|-------------|
| `/define` | Manifest builder - creates hierarchical definition through proactive interview |
| `/do` | Manifest executor - respects hierarchy, checks invariants, satisfies ACs |

### Internal

| Skill | Purpose |
|-------|---------|
| `/verify` | Runs all verifications, reports by type and deliverable |
| `/done` | Outputs hierarchical completion summary |
| `/escalate` | Structured escalation with type-aware context |

## Agents

| Agent | Purpose |
|-------|---------|
| `criteria-checker` | Verifies a single criterion with type awareness |

## Hooks

| Hook | Purpose |
|------|---------|
| `stop_do_hook.py` | Enforces verification before stopping |
| `pretool_escalate_hook.py` | Enforces /verify before /escalate |

## Workflow

```
/define "task" → Interview → Manifest file
                    │
                    ├─ Intent & Context
                    ├─ Global Invariants
                    └─ Deliverables (with ACs)
                                   ↓
/do manifest.md → For each Deliverable:
                    - Satisfy ACs
                         ↓
                  /verify → (failures) → Fix specific criterion → /verify again
                         ↓
                  All pass → /done
                         ↓
                  (stuck) → /escalate
```

## Execution Semantics

| Phase | Check | Failure Impact |
|-------|-------|----------------|
| After each deliverable | Acceptance Criteria | Deliverable incomplete |
| Final verification | Global Invariants + all ACs | Must all pass for /done |

## Status

**Experimental** - More rigorous than standard workflows. Use when you want quality-focused autonomous execution with clear separation of constraints and deliverables.
