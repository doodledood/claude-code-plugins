---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

## Goal

Execute a Manifest: satisfy all Deliverables' Acceptance Criteria, then verify everything passes (including Global Invariants).

## Input

`$ARGUMENTS` = manifest file path (REQUIRED)

If no arguments: Output error "Usage: /do <manifest-file-path>"

## Principles

1. **ACs define success, not the path** - Work toward acceptance criteria however makes sense. The manifest says WHAT, you decide HOW.

2. **Target failures specifically** - On verification failure, fix the specific failing criterion. Don't restart from scratch. Don't touch passing criteria.

3. **Respect tradeoffs** - When values conflict, check the manifest's "Tradeoffs & Preferences" section and apply.

## Constraints

**Create todo list immediately** - Track deliverables and their ACs. Use `D{N}:` prefix to indicate which deliverable. Expand as work reveals sub-tasks.

**Create execution log** - Write to `/tmp/do-log-{timestamp}.md`. Log what you're working on, approaches tried, results. This is your working memory.

**Write to log as you go** - After each significant action, update the log. Don't wait until the end.

**Must call /verify** - Can't declare done without verification. When all deliverables addressed:
```
Skill("vibe-experimental:verify", "/tmp/manifest-{ts}.md /tmp/do-log-{ts}.md")
```

**Refresh before completion** - Read the full log before outputting final summary.

## What to Do

**Read the manifest** - Extract intent, global invariants, deliverables with their ACs, tradeoffs.

**Work through deliverables** - For each, satisfy its acceptance criteria. Log your work.

**Call /verify** - When all deliverables addressed, verify everything passes.

**Handle failures** - Fix specific failing criteria, call /verify again. Loop until pass.

**Escalate when stuck** - If you've tried 3+ approaches on a criterion and can't satisfy it:
```
Skill("vibe-experimental:escalate", "[criterion ID] blocking after 3 attempts")
```

## Log Structure

```markdown
# Execution Log

Manifest: [path]
Started: [timestamp]

## Intent
**Goal:** [from manifest]

## Deliverable 1: [Name]

### AC-1.1: [description]
- Approach: [what you tried]
- Result: [outcome]

### Status: [COMPLETE/IN PROGRESS]

## Verification Attempts

### Attempt 1
- Results: [summary]
- Action: [what to fix]
```

## Flow

```
1. Read manifest
2. Create todos + log
3. For each deliverable: work toward ACs, log progress
4. Call /verify
5. If failures: fix specific criteria, /verify again
6. All pass: /verify calls /done
```
