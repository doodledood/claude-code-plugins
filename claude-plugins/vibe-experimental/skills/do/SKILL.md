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

1. **ACs define success, not the path** - Work toward acceptance criteria however makes sense. The manifest says WHAT, you decide HOW.

2. **Architecture is direction, not constraint** - Follow the approach's architecture as your starting direction. Adapt tactics freely when needed—architecture guides, doesn't constrain.

3. **Target failures specifically** - On verification failure, fix the specific failing criterion. Don't restart from scratch. Don't touch passing criteria.

4. **Trade-offs guide adjustment** - When risks materialize or approach needs adjustment, consult trade-offs (T-*) for decision criteria. Log adjustments with rationale.

## Constraints

**Must call /verify** - Can't declare done without verification. When all deliverables addressed, invoke the vibe-experimental:verify skill with the manifest and log paths.

## Memento Pattern

Externalize your progress continuously—this survives context loss and enables recovery.

**Todos**: Create from manifest structure (deliverables → ACs). Follow execution order from Approach. Update after every substantive action. Include completion criteria on each item.

**Execution log**: Write to `/tmp/do-log-{timestamp}.md`. Log:
- Approaches tried and outcomes
- Risk detections: when R-* triggers observed, what was detected
- Approach adjustments: what changed, which T-* informed the decision, why ACs remain achievable
Read the full log before calling /verify to restore context.

## Execution

1. **Extract from manifest**: Intent, approach (architecture, execution order, risks, trade-offs), global invariants, process guidance (PG-*), deliverables with ACs
2. **Follow execution order**: Work through deliverables in the order specified by Approach (if present), or by dependency
3. **Watch for risks**: As you work, watch for risk area (R-*) triggers. If detected, log detection, consult trade-offs, adjust approach
4. **Adjustment logic**: When approach needs adjustment:
   - Can ACs still be met? → Adjust, log change + rationale, continue autonomously
   - ACs can't be met as written? → Invoke vibe-experimental:escalate (contract broken, need user)
5. **Verify**: Invoke vibe-experimental:verify with manifest and log paths
6. **Handle failures**: Fix specific failing criteria, verify again
7. **Escalate when stuck**: Invoke vibe-experimental:escalate with criterion ID and approaches tried
