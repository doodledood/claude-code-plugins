---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance and Approach direction, then verify everything passes (including Global Invariants).

**Why quality execution matters**: The manifest front-loaded the thinking—criteria are already defined. Your job is implementation that passes verification on first attempt. Every verification failure is rework.

## Input

`$ARGUMENTS` = manifest file path (REQUIRED)

If no arguments: Output error "Usage: /do <manifest-file-path>"

## Principles

| Principle | Rule |
|-----------|------|
| **ACs define success** | Work toward acceptance criteria however makes sense. Manifest says WHAT, you decide HOW. |
| **Architecture is direction** | Follow approach's architecture as starting direction. Adapt tactics freely—architecture guides, doesn't constrain. |
| **Target failures specifically** | On verification failure, fix the specific failing criterion. Don't restart. Don't touch passing criteria. |
| **Trade-offs guide adjustment** | When risks (R-*) materialize, consult trade-offs (T-*) for decision criteria. Log adjustments with rationale. |

## Constraints

**Must call /verify** - Can't declare done without verification. Invoke vibe-experimental:verify with manifest and log paths.

**Escalation boundary** - Escalate only when ACs can't be met as written (contract broken). If ACs remain achievable, adjust and continue autonomously.

**Refresh before verify** - Read full execution log before calling /verify to restore context.

## Memento Pattern

Externalize progress continuously—survives context loss, enables recovery.

**Todos**: Create from manifest (deliverables → ACs). Follow execution order from Approach. Update after each AC completed. Include completion criteria on each item.

**Execution log**: Write to `/tmp/do-log-{timestamp}.md`. Log:
- Approaches tried and outcomes
- Risk detections: when R-* triggers observed, what was detected
- Approach adjustments: what changed, which T-* informed the decision, why ACs remain achievable
