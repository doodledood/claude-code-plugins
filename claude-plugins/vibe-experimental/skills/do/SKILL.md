---
name: do
description: 'Manifest executor. Respects hierarchical structure: checks Global Invariants as guardrails, iterates through Deliverables checking Local Invariants, satisfies Acceptance Criteria. Use when you have a manifest from /define.'
user-invocable: true
---

# /do - Manifest Executor

You execute a **Manifest** respecting its hierarchical structure:
1. **Global Invariants** - check before starting (guardrails)
2. **Deliverables** - iterate through each
   - **Local Invariants** - constraints to respect while building
   - **Acceptance Criteria** - positive verification of completion
3. **Final Verification** - all ACs pass AND all Global Invariants still pass

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
  - Local Invariants (INV-L*.*)
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

## Global Invariants Status
- [ ] INV-G1: [description]
- [ ] INV-G2: [description]
...

## Deliverables Status

### Deliverable 1: [Name]
**Local Invariants:**
- [ ] INV-L1.1: [description]
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
- [ ] Pre-flight: verify global invariants
- [ ] Deliverable 1: [name]
  - [ ] Check INV-L1.1 holds→log; done when verified
  - [ ] Satisfy AC-1.1→log; done when implemented + verified
  - [ ] Satisfy AC-1.2→log; done when implemented + verified
- [ ] Deliverable 2: [name]
  - [ ] Check INV-L2.1 holds→log; done when verified
  - [ ] Satisfy AC-2.1→log; done when implemented + verified
- [ ] (expand: sub-tasks as discovered)
- [ ] Final: call /verify for comprehensive check
- [ ] (expand: fix failures from /verify—loop until pass)
- [ ] Refresh log + output summary; done when user sees final status
```

### 3. Pre-flight: Check Global Invariants

Before starting any work, verify Global Invariants.

**Why**: If a global invariant is already violated (e.g., tests already failing), the user should know before we begin.

For each INV-G*:
1. Run its verification method
2. Record result in log

**If any Global Invariant fails pre-flight:**
```markdown
## Pre-flight Warning

The following Global Invariants are already failing:

- **INV-G1**: Tests must pass
  Status: FAILING
  Evidence: [output from verification]

This means the task starts in a violated state. Options:
1. Fix these first, then continue
2. Proceed anyway (task will fail final verification unless fixed)
3. Amend the manifest to change these invariants
```

Ask the user how to proceed using AskUserQuestion.

**If all pass**: Log success and continue.

### 4. Execute Deliverables

For each Deliverable in order:

#### 4a. Pre-check Local Invariants

Before working on a deliverable, understand its constraints.

Log the Local Invariants you'll need to respect:
```markdown
### Starting Deliverable 1: [Name]

**Local Invariants to respect:**
- INV-L1.1: [constraint]
- INV-L1.2: [constraint]

**Acceptance Criteria to satisfy:**
- AC-1.1: [what success looks like]
- AC-1.2: [what success looks like]
```

#### 4b. Work Toward Acceptance Criteria

Work to satisfy the ACs. You decide HOW—the ACs define success, not the path.

**While working:**
- Actively consider Local Invariants as guardrails
- If you're about to violate an INV-L*, stop and find another approach
- Log significant decisions, especially when Local Invariants constrain your choices

**Log format during work:**
```markdown
### AC-1.1: [description]
- Approach: [what you're trying]
- Local Invariant consideration: INV-L1.1 requires [constraint], so [how you're respecting it]
- Result: [outcome]
```

#### 4c. Verify Deliverable Complete

When you believe all ACs for this deliverable are satisfied:

1. Quick-check Local Invariants still hold
2. Quick-check ACs are met
3. Log completion

```markdown
### Deliverable 1: [Name] - COMPLETE

**Local Invariants:**
- [x] INV-L1.1: Verified [evidence]

**Acceptance Criteria:**
- [x] AC-1.1: Satisfied [evidence]
- [x] AC-1.2: Satisfied [evidence]
```

Move to next deliverable.

### 5. Call /verify When All Deliverables Complete

When all deliverables are addressed:

```
Use the Skill tool to verify: Skill("vibe-experimental:verify", "/tmp/manifest-{ts}.md /tmp/do-log-{ts}.md")
```

### 6. Handle Verification Results

**/verify returns failures:**

Failures are categorized:
- **Global Invariant failure**: Task-level failure, must fix
- **Local Invariant failure**: Specific deliverable invalid
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

### 7. Escalation (When Genuinely Stuck)

If you've tried 3+ approaches and can't satisfy a criterion:

```
Use the Skill tool to escalate: Skill("vibe-experimental:escalate", "[criterion ID] blocking after 3 attempts")
```

Escalation requires /verify to have been called first.

**Escalation scenarios:**
- Global Invariant seems impossible to satisfy
- Local Invariant conflicts with AC (can't satisfy both)
- AC requires something the codebase can't support

## Example Flow

```
1. /do /tmp/manifest-123.md
2. Read manifest, create log, create todos
3. Pre-flight: check Global Invariants
   - All pass → continue
   - Failures → warn user, get decision
4. Deliverable 1:
   - Note Local Invariants as guardrails
   - Work toward AC-1.1, AC-1.2
   - Verify deliverable complete
5. Deliverable 2:
   - Note Local Invariants
   - Work toward AC-2.1
   - Verify deliverable complete
6. Skill("vibe-experimental:verify", "...")
7. If failures → fix specific criterion → retry verify
8. All pass → /verify calls /done
9. Refresh log → output summary → stop allowed
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
2. **Hierarchical respect** - Global Invariants > Local Invariants > ACs
3. **Pre-flight check** - verify Global Invariants before starting
4. **Local Invariants are guardrails** - actively consider while working
5. **Log attempts** - each todo includes `→log` discipline
6. **Must call /verify** - can't declare done without verification
7. **Target failures** - on failure, fix specific criterion, don't restart
8. **Proper escalation** - /escalate only after /verify, with evidence

## Log Structure

The execution log should maintain this structure:

```markdown
# Execution Log

Manifest: [path]
Started: [timestamp]

## Intent
**Goal:** [from manifest]
**Mental Model:** [key concepts]

## Pre-flight Check
- [x] INV-G1: PASS
- [x] INV-G2: PASS

## Deliverable 1: [Name]

### Local Invariants
- [x] INV-L1.1: Respected throughout

### Work Log

#### AC-1.1: [description]
- Attempt 1: [approach]
  - Local Invariant consideration: [how INV-L1.1 affected approach]
  - Result: [outcome]

#### AC-1.2: [description]
- Attempt 1: [approach]
  - Result: [outcome]

### Status: COMPLETE
- All Local Invariants held
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
