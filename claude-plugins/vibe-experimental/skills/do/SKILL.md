---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies all ACs and Global Invariants pass. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

You execute a **Manifest** respecting its structure:
1. **Deliverables** - iterate through each, satisfying their ACs
2. **Final Verification** - all ACs pass AND all Global Invariants pass

## Input

`$ARGUMENTS` = manifest file path (REQUIRED)

Example: `/do /tmp/manifest-1234567890.md`

If no arguments: Output error "Usage: /do <manifest-file-path>"

## Process

### 1. Read and Parse Manifest

Read the manifest file from `$ARGUMENTS`:
- If file not found → output clear error and stop
- If file invalid (missing required sections) → output clear error and stop

Extract:
- **Intent & Context**: Goal, Mental Model
- **Global Invariants**: INV-G* with verification methods
- **Deliverables**: Each with:
  - Name
  - Acceptance Criteria (AC-*.*)
- **Tradeoffs & Preferences**: For conflict resolution
- **Pattern References**: What to follow/avoid

### 2. Initialize

Create execution log: `/tmp/do-log-{timestamp}.md`

Write initial state:
```markdown
# Execution Log

Manifest: [manifest file path]
Started: [timestamp]

## Intent
**Goal:** [from manifest]
**Mental Model:** [from manifest]

## Deliverables Status

### Deliverable 1: [Name]
**Acceptance Criteria:**
- [ ] AC-1.1: [description]
- [ ] AC-1.2: [description]

### Deliverable 2: [Name]
...

## Execution Timeline
(will be filled as work progresses)
```

Create TodoWrite:
```
- [ ] Create log /tmp/do-log-{timestamp}.md
- [ ] D1: Satisfy AC-1.1→log; done when implemented + verified
- [ ] D1: Satisfy AC-1.2→log; done when implemented + verified
- [ ] D2: Satisfy AC-2.1→log; done when implemented + verified
- [ ] (expand: sub-tasks as discovered)
- [ ] Final: call /verify for comprehensive check
- [ ] (expand: fix failures from /verify—loop until pass)
- [ ] Refresh log + output summary; done when user sees final status
```

Use `D{N}:` prefix to indicate which deliverable a todo belongs to.

### 3. Execute Deliverables

For each Deliverable in order:

#### 3a. Understand the Deliverable

Log what you're working on:
```markdown
### Starting Deliverable 1: [Name]

**Acceptance Criteria to satisfy:**
- AC-1.1: [what success looks like]
- AC-1.2: [what success looks like]
```

#### 3b. Work Toward Acceptance Criteria

Work to satisfy the ACs. You decide HOW—the ACs define success, not the path.

**Log format during work:**
```markdown
### AC-1.1: [description]
- Approach: [what you're trying]
- Result: [outcome]
```

#### 3c. Verify Deliverable Complete

When you believe all ACs for this deliverable are satisfied:

1. Quick-check ACs are met
2. Log completion

```markdown
### Deliverable 1: [Name] - COMPLETE

**Acceptance Criteria:**
- [x] AC-1.1: Satisfied [evidence]
- [x] AC-1.2: Satisfied [evidence]
```

Move to next deliverable.

### 4. Call /verify When All Deliverables Complete

When all deliverables are addressed:

```
Use the Skill tool to verify: Skill("vibe-experimental:verify", "/tmp/manifest-{ts}.md /tmp/do-log-{ts}.md")
```

### 5. Handle Verification Results

**/verify returns failures:**

Failures are categorized:
- **Global Invariant failure**: Task-level failure, must fix
- **AC failure**: Specific deliverable incomplete

For each failure:
1. Identify which deliverable it belongs to (or if global)
2. Target fix to that specific area
3. Do NOT restart from scratch
4. Do NOT touch passing criteria
5. Update log with fix attempts
6. Call /verify again when fixed

**/verify returns success:**
- /verify will call /done automatically
- You're finished

**/verify returns manual criteria:**
- All automated criteria pass
- Manual criteria need human verification
- Call /escalate to surface them

### 6. Escalation (When Genuinely Stuck)

If you've tried 3+ approaches and can't satisfy a criterion:

```
Use the Skill tool to escalate: Skill("vibe-experimental:escalate", "[criterion ID] blocking after 3 attempts")
```

Escalation requires /verify to have been called first.

**Escalation scenarios:**
- Global Invariant seems impossible to satisfy
- AC requires something the codebase can't support
- Two ACs conflict (can't satisfy both)

## Example Flow

```
1. /do /tmp/manifest-123.md
2. Read manifest, create log, create todos
3. Deliverable 1:
   - Work toward AC-1.1, AC-1.2
   - Mark deliverable complete
4. Deliverable 2:
   - Work toward AC-2.1
   - Mark deliverable complete
5. Skill("vibe-experimental:verify", "...")
6. If failures → fix specific criterion → retry verify
7. All pass → /verify calls /done
8. Refresh log → output summary → stop allowed
```

## Tradeoff Resolution

When you face a decision where values conflict, check the manifest's "Tradeoffs & Preferences" section.

Example: If manifest says "When brevity and completeness conflict, prefer completeness", use that to guide your approach.

Log tradeoff resolutions:
```markdown
**Tradeoff applied:** Needed to choose between [A] and [B]. Manifest prefers [preference]. Chose [decision].
```

## Critical Rules

1. **Manifest file required** - fail clearly if not provided
2. **Log attempts** - each todo includes `→log` discipline
3. **Must call /verify** - can't declare done without verification
4. **Target failures** - on failure, fix specific criterion, don't restart
5. **Proper escalation** - /escalate only after /verify, with evidence

## Log Structure

The execution log should maintain this structure:

```markdown
# Execution Log

Manifest: [path]
Started: [timestamp]

## Intent
**Goal:** [from manifest]
**Mental Model:** [key concepts]

## Deliverable 1: [Name]

### Work Log

#### AC-1.1: [description]
- Attempt 1: [approach]
  - Result: [outcome]

#### AC-1.2: [description]
- Attempt 1: [approach]
  - Result: [outcome]

### Status: COMPLETE
- All ACs satisfied

## Deliverable 2: [Name]
...

## Verification Attempts

### Attempt 1 (timestamp)
- Global Invariants: 2/2 pass
- Deliverable 1: 2/2 ACs pass
- Deliverable 2: 1/2 ACs pass (AC-2.1 failed)
- Action: Fixing AC-2.1

### Attempt 2 (timestamp)
- All pass
- /done called

## Tradeoff Resolutions
- [timestamp]: Chose [A] over [B] per manifest preference

## Key Decisions
- [decision]: [rationale]
```
