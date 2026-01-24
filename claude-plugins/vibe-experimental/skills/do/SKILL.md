---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria while following Process Guidance, then verify everything passes (including Global Invariants).

**Why quality execution matters**: The manifest front-loaded the thinking—criteria are already defined. Your job is implementation that passes verification on first attempt. Every verification failure is rework.

## Input

`$ARGUMENTS` = manifest file path (REQUIRED)

If no arguments: Output error "Usage: /do <manifest-file-path>"

## Principles

1. **ACs define success, not the path** - Work toward acceptance criteria however makes sense. The manifest says WHAT, you decide HOW.

2. **Target failures specifically** - On verification failure, fix the specific failing criterion. Don't restart from scratch. Don't touch passing criteria.

3. **Respect tradeoffs** - When values conflict, check the manifest's "Tradeoffs & Preferences" section and apply.

## Constraints

**Must call /verify** - Can't declare done without verification. When all deliverables addressed, invoke the vibe-experimental:verify skill with the manifest and log paths.

## Memento Pattern

Externalize your progress continuously—this survives context loss and enables recovery.

**Todos**: Create from manifest structure (deliverables → ACs). Update after every substantive action. Include completion criteria on each item.

**Execution log**: Write to `/tmp/do-log-{timestamp}.md`. Log approaches tried and outcomes as you work. Read the full log before calling /verify to restore context.

## Execution

1. **Extract from manifest**: Intent, global invariants, process guidance (PG-* items), deliverables with ACs, tradeoffs
2. **Work through deliverables**: Satisfy acceptance criteria, log progress
3. **Verify**: Invoke vibe-experimental:verify with manifest and log paths
4. **Handle failures**: Fix specific failing criteria, verify again
5. **Escalate when stuck**: Invoke vibe-experimental:escalate with criterion ID and approaches tried
