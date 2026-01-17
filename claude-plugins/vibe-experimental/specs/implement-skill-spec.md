# Acceptance Criteria Spec: /implement Skill System

Generated: 2026-01-17
Status: Final (from interview)
Plugin: vibe-experimental
Interview Log: implement-interview-log.md

---

## Overview

### Problem Statement
Current implementation workflows allow the LLM to declare "done" without verifying all acceptance criteria actually pass. The gap between "I think I'm done" and "all criteria verified passing" leads to incomplete or incorrect implementations.

### Solution
A verification-first skill system with enforced flow:

```
/implement (user-invocable)
    → works toward criteria using memento pattern
    → calls /verify when thinks ready

/verify (NOT user-invocable)
    → runs all verifications against codebase
    → returns failures OR calls /done if all pass

/done (NOT user-invocable)
    → marker in transcript
    → triggers completion summary

/escalate (NOT user-invocable)
    → structured evidence of being stuck
    → allows stop without /done

HOOKS:
    PreToolUse on /escalate: blocks unless /verify was called first
    Stop: blocks unless /done OR /escalate called after /implement
```

### Success Measure
User runs `/implement <spec-file>`, goes to sleep, wakes up to either:
- All criteria verified passing (actually done)
- Escalation with clear evidence of what's blocking (genuinely stuck)

Never: LLM declares done with unverified or failing criteria.

---

## Core Concepts

### State Model

**Critical distinction:**
- **STATE = Codebase (files on disk)** - the source of truth
- **Git history = log** - helps understand state faster
- **Implementation log = log** - helps understand attempts faster

/verify checks actual files, not git history. Logs are proxies for understanding, not the state itself.

### Memento Pattern (MANDATORY)

All skills MUST use the full memento pattern as documented in CLAUDE.md:

1. **Create log file immediately** with areas to work on
2. **Write findings to log BEFORE proceeding** to next step
3. **Expand todos dynamically** as work reveals new areas
4. **Read full log before synthesis** (refresh context)

This prevents context loss on compaction and enables /verify to read implementation history.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  /implement /tmp/spec-xyz.md                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      /implement SKILL                            │
│  - Reads spec file from $ARGUMENTS (required)                   │
│  - Creates /tmp/implement-log-{timestamp}.md                    │
│  - Works toward criteria (no plan decomposition)                │
│  - Tracks attempts in log: "Tried X for AC-5, failed because Y" │
│  - Makes meaningful git commits                                 │
│  - Calls /verify when thinks ready                              │
│  - Can call /escalate when genuinely stuck                      │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│    /verify SKILL        │       │    /escalate SKILL      │
│  (not user-invocable)   │       │  (not user-invocable)   │
│                         │       │                         │
│  - Reads spec file      │       │  - Structured evidence  │
│  - Reads impl log       │       │  - Free-form context    │
│  - Checks codebase      │       │  - Allows stop          │
│  - Parallel subagents   │       │                         │
│  - Returns failures OR  │       │  PreToolUse hook:       │
│    calls /done          │       │  blocks if no /verify   │
└─────────────────────────┘       └─────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│  VERIFICATION RESULTS                                            │
│                                                                  │
│  Automated failures? → Return failures only (hide manual)       │
│                        → /implement continues working            │
│                                                                  │
│  All automated pass + manual exists? → Return manual criteria   │
│                                        → Hint: call /escalate   │
│                                                                  │
│  All pass (no manual)? → Call /done                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       /done SKILL                                │
│  (not user-invocable)                                           │
│                                                                  │
│  - Marker in transcript (just exists)                           │
│  - Triggers completion summary output                           │
│  - Stop hook sees this → allows stop                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hooks

### Stop Hook

**Purpose:** Prevent premature stopping - only allow when /done or /escalate called.

**Logic:**
```python
def stop_hook(transcript):
    # Scan transcript backwards
    last_implement = find_last("/implement", transcript)

    if not last_implement:
        return ALLOW  # Not in implement flow

    # Check for /done or /escalate AFTER last /implement
    done_after = exists_after("/done", last_implement, transcript)
    escalate_after = exists_after("/escalate", last_implement, transcript)

    if done_after or escalate_after:
        return ALLOW
    else:
        return BLOCK("Cannot stop - run /verify first. If stuck, /escalate after /verify.")
```

**Stack behavior:**
- Each /implement starts fresh
- Second /implement abandons first flow
- Hook tracks most recent /implement only

### PreToolUse Hook on /escalate

**Purpose:** Prevent lazy escalation - must attempt verification first.

**Logic:**
```python
def pre_escalate_hook(transcript):
    last_implement = find_last("/implement", transcript)

    if not last_implement:
        return BLOCK("No /implement in progress")

    verify_after = exists_after("/verify", last_implement, transcript)

    if verify_after:
        return ALLOW
    else:
        return BLOCK("Must call /verify before /escalate")
```

---

## Skills

### /implement

**User-invocable:** YES

**Input:** `$ARGUMENTS` = spec file path (required)

**Behavior:**
1. Read and parse spec file
2. Create implementation log: `/tmp/implement-log-{timestamp}.md`
3. Create TodoWrite with criteria to satisfy
4. Work toward criteria (no plan decomposition)
5. Log all attempts: "Tried X for criterion Y, result: Z"
6. Make meaningful git commits with descriptive messages
7. When thinks ready → call /verify
8. On verification failure → continue working on failures
9. On verification success → /verify calls /done
10. When genuinely stuck → call /escalate (after /verify)

**Memento pattern:** MUST write to log before each major action.

### /verify

**User-invocable:** NO (only called by /implement)

**Input:** Spec file path + implementation log path (piped from /implement)

**Behavior:**
1. Parse spec for all criteria
2. Read implementation log for attempt context
3. Run automated verifications:
   - Bash commands (npm test, tsc, etc.) with retries, higher timeout
   - Subagents for code pattern checks (parallel, waves of 5)
4. Check results:
   - Any automated fail → return failures only (hide manual)
   - All automated pass + manual exists → return manual (hint to escalate)
   - All pass → call /done

**Output format:**
```
## Verification Results

### Failed (2)
- AC-3: tests-pass
  Method: bash (npm test)
  Location: src/notifications.test.ts:45
  Expected: 'queued'
  Actual: 'sent'

- AC-7: error-pattern
  Method: subagent (pattern-checker)
  Location: src/handlers/notify.ts:23
  Issue: Raw Error() throw, expected AppError

### Passed (5)
- AC-1: no-type-errors ✓
- AC-2: lint-clean ✓
- AC-4: file-structure ✓
- AC-5: naming-conventions ✓
- AC-6: no-console-logs ✓

Continue working on failed criteria, then call /verify again.
```

### /done

**User-invocable:** NO (only called by /verify)

**Input:** None (called when all verifications pass)

**Behavior:**
1. Exists in transcript as marker
2. Output completion summary:
   - What was implemented
   - All criteria verified
   - Key decisions made
3. Stop hook sees /done → allows stop

### /escalate

**User-invocable:** NO (only called by /implement)

**Input:** Structured evidence + free-form context

**Behavior:**
1. PreToolUse hook checks /verify was called
2. Output structured escalation:
   - Which criterion is blocking
   - What was tried (from implementation log)
   - Why each attempt failed
   - Hypothesis about root cause
3. Stop hook sees /escalate → allows stop

**Output format:**
```
## Escalation: Criterion AC-4 (pubsub-pattern)

### Attempts (from implementation log)
1. Direct import of src/events/bus.ts
   Result: bus.publish not exported (private)

2. Created new EventEmitter
   Result: Subagent rejected - must use existing PubSub

3. Extended bus.ts to export publish
   Result: Breaks 12 tests that mock internals

### Hypothesis
Criterion assumes bus.publish is available, but codebase keeps it private.

### Possible Resolutions
1. Update criterion to allow new EventEmitter
2. Refactor bus.ts to export publish (breaking change)
3. Use different integration pattern

### Requesting
Human decision on which path to take.
```

---

## Verification Methods

### Bash Commands
- Run shell commands (npm test, tsc --noEmit, etc.)
- Higher timeout (configurable, default 5 minutes)
- Automatic retries on transient failures
- Pass condition: exit code 0 (or spec-defined)

### Subagent Checks
- Spawn subagents to review code patterns
- Parallel execution in waves (max 5 concurrent, configurable)
- Queue style: new ones start as previous complete
- Input: criterion + implementation log + relevant code
- Output: pass/fail + specific issues with file:line locations

### Manual (Flagged)
- Criteria requiring human verification
- Don't block automated flow
- Only surfaced AFTER all automated criteria pass
- Hint to /implement to call /escalate

---

## Acceptance Criteria

### Category: /implement Skill

#### AC-1: Requires Spec File
**Description:** /implement requires spec file path in $ARGUMENTS, fails clearly if missing.

**Verification:**
```yaml
method: subagent
agent: input-checker
checks:
  - "Error message if no $ARGUMENTS"
  - "Error message if file not found"
  - "Proceeds only with valid spec file"
```

#### AC-2: Creates Implementation Log
**Description:** Creates /tmp/implement-log-{timestamp}.md at start.

**Verification:**
```yaml
method: bash
command: "ls /tmp/implement-log-*.md | head -1"
pass_condition: "file exists"
```

#### AC-3: Uses Memento Pattern
**Description:** Writes to log before each major action, per CLAUDE.md.

**Verification:**
```yaml
method: subagent
agent: memento-checker
checks:
  - "Log updated before proceeding to next step"
  - "Attempts documented with outcomes"
  - "TodoWrite tracks criteria, not steps"
```

#### AC-4: No Plan Decomposition
**Description:** Works toward criteria directly, no plan file or chunks.

**Verification:**
```yaml
method: subagent
agent: pattern-checker
checks:
  - "No /tmp/plan-*.md created"
  - "No 'Chunk 1', 'Chunk 2' in transcript"
  - "Work references criteria IDs (AC-N)"
```

#### AC-5: Calls /verify When Ready
**Description:** Invokes /verify skill when thinks implementation is complete.

**Verification:**
```yaml
method: subagent
agent: transcript-analyzer
checks:
  - "/verify called before any 'done' statement"
  - "/verify receives spec file path"
```

#### AC-6: Continues on Failure
**Description:** When /verify returns failures, continues working on those criteria.

**Verification:**
```yaml
method: subagent
agent: loop-checker
checks:
  - "After failure, work targets specific failed criteria"
  - "Does not restart from scratch"
  - "Does not touch passing criteria"
```

#### AC-7: Meaningful Commits
**Description:** Makes git commits during implementation with descriptive messages.

**Verification:**
```yaml
method: bash
command: "git log --oneline -10"
pass_condition: "multiple commits with criterion references"
```

### Category: /verify Skill

#### AC-8: Not User-Invocable
**Description:** /verify cannot be invoked directly by user.

**Verification:**
```yaml
method: subagent
agent: skill-config-checker
checks:
  - "user-invocable: false in frontmatter"
  - "description indicates internal only"
```

#### AC-9: Reads Implementation Log
**Description:** /verify reads implementation log for attempt context.

**Verification:**
```yaml
method: subagent
agent: verify-input-checker
checks:
  - "Implementation log path received"
  - "Log content used in verification context"
```

#### AC-10: Parallel Subagent Execution
**Description:** Runs subagent verifications in parallel waves.

**Verification:**
```yaml
method: subagent
agent: execution-analyzer
checks:
  - "Multiple subagents launched in single message"
  - "Wave size respects limit (default 5)"
  - "Queue continues as previous complete"
```

#### AC-11: Prioritizes Automated
**Description:** Returns only automated failures, hides manual until automated pass.

**Verification:**
```yaml
method: subagent
agent: output-analyzer
checks:
  - "On automated failure: manual criteria NOT mentioned"
  - "On automated pass: manual criteria surfaced"
```

#### AC-12: Calls /done on Success
**Description:** When all automated pass (and no manual), calls /done.

**Verification:**
```yaml
method: subagent
agent: flow-checker
checks:
  - "/done called only when all automated pass"
  - "/done NOT called when any automated fail"
```

#### AC-13: Actionable Failure Feedback
**Description:** Failure output includes specific locations and expected vs actual.

**Verification:**
```yaml
method: subagent
agent: feedback-checker
checks:
  - "Each failure has file:line location"
  - "Each failure explains expected vs actual"
  - "Feedback is actionable, not vague"
```

### Category: /done Skill

#### AC-14: Not User-Invocable
**Description:** /done cannot be invoked directly by user.

**Verification:**
```yaml
method: subagent
agent: skill-config-checker
checks:
  - "user-invocable: false in frontmatter"
```

#### AC-15: Outputs Completion Summary
**Description:** Outputs summary of what was implemented and verified.

**Verification:**
```yaml
method: subagent
agent: output-checker
checks:
  - "Summary includes what was implemented"
  - "Summary lists verified criteria"
```

### Category: /escalate Skill

#### AC-16: Not User-Invocable
**Description:** /escalate cannot be invoked directly by user.

**Verification:**
```yaml
method: subagent
agent: skill-config-checker
checks:
  - "user-invocable: false in frontmatter"
```

#### AC-17: Requires Structured Evidence
**Description:** Outputs structured evidence of attempts and failures.

**Verification:**
```yaml
method: subagent
agent: escalation-checker
checks:
  - "Specifies which criterion is blocking"
  - "Lists attempts from implementation log"
  - "Explains why each attempt failed"
  - "Provides hypothesis about root cause"
```

### Category: Stop Hook

#### AC-18: Blocks Without /done or /escalate
**Description:** Stop hook blocks if /implement started but no /done or /escalate after.

**Verification:**
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_blocks_without_done -v"
pass_condition: "exit code 0"
```

#### AC-19: Allows With /done
**Description:** Stop hook allows stop when /done exists after /implement.

**Verification:**
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_allows_with_done -v"
pass_condition: "exit code 0"
```

#### AC-20: Allows With /escalate
**Description:** Stop hook allows stop when /escalate exists after /implement.

**Verification:**
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_allows_with_escalate -v"
pass_condition: "exit code 0"
```

#### AC-21: Fresh Stack Per /implement
**Description:** Second /implement resets tracking, first flow abandoned.

**Verification:**
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_fresh_stack -v"
pass_condition: "exit code 0"
```

### Category: PreToolUse Hook on /escalate

#### AC-22: Blocks Without /verify
**Description:** PreToolUse blocks /escalate if /verify not called first.

**Verification:**
```yaml
method: bash
command: "pytest tests/hooks/test_escalate_pretool_hook.py::test_blocks_without_verify -v"
pass_condition: "exit code 0"
```

#### AC-23: Allows After /verify
**Description:** PreToolUse allows /escalate after /verify was called.

**Verification:**
```yaml
method: bash
command: "pytest tests/hooks/test_escalate_pretool_hook.py::test_allows_after_verify -v"
pass_condition: "exit code 0"
```

---

## Rejection Criteria

The PR will be REJECTED if:

1. **Any skill is user-invocable that shouldn't be** - /verify, /done, /escalate must have `user-invocable: false`
2. **Stop hook allows premature stop** - must block without /done or /escalate
3. **LLM can bypass verification** - any path to "done" without /verify running
4. **Lazy escalation possible** - /escalate without /verify first
5. **Memento pattern not used** - skills must write to log before proceeding
6. **Plan decomposition used** - must work toward criteria, not steps
7. **Vague failure feedback** - must have specific file:line and expected vs actual
8. **Manual criteria block automation** - must only surface after automated pass

---

## Pre-mortem Risks

| Risk | Preventive Criterion |
|------|---------------------|
| Redundant work / loops | AC-3, AC-6 - log attempts, target specific failures |
| Premature stopping | AC-18, AC-19, AC-20 - stop hook enforcement |
| LLM calls /done directly | AC-14, stop hook detects /done without /verify |
| Lazy escalation | AC-22 - PreToolUse blocks without /verify |
| Context loss on compaction | AC-3 - memento pattern mandatory |
| Subagent says pass but code broken | Review criteria in spec, multiple verification methods |

---

## Disappointed Scenarios

| Scenario | Preventive Criterion |
|----------|---------------------|
| "LLM said done but tests failing" | AC-12, AC-18 - /done only after /verify passes |
| "Code is sloppy" | Spec includes review criteria (user's responsibility) |
| "Messy git history" | AC-7 - meaningful commits |
| "Escalated without really trying" | AC-22 - must /verify before /escalate |
| "Lost progress on compaction" | AC-3 - memento pattern |

---

## Files to Create

```
claude-plugins/vibe-experimental/
├── skills/
│   ├── implement/
│   │   └── SKILL.md              # Main skill (user-invocable)
│   ├── verify/
│   │   └── SKILL.md              # Verification runner (not user-invocable)
│   ├── done/
│   │   └── SKILL.md              # Completion marker (not user-invocable)
│   └── escalate/
│       └── SKILL.md              # Escalation (not user-invocable)
├── hooks/
│   ├── stop_implement_hook.py    # Stop enforcement
│   ├── pretool_escalate_hook.py  # Escalation gate
│   └── hook_utils.py             # Shared utilities
└── tests/
    └── hooks/
        ├── test_implement_stop_hook.py
        └── test_escalate_pretool_hook.py
```

---

## Out of Scope

- /spec skill changes (separate spec)
- UI/rendering
- Cloud/remote execution
- Multi-repo support

---

## Appendix: Stop Hook Decision Matrix

| /implement | /verify | /done | /escalate | Decision |
|------------|---------|-------|-----------|----------|
| No | - | - | - | ALLOW (not in flow) |
| Yes | No | No | No | BLOCK |
| Yes | Yes | No | No | BLOCK |
| Yes | Yes | Yes | - | ALLOW |
| Yes | Yes | - | Yes | ALLOW |
| Yes | No | Yes | - | BLOCK (suspicious) |
| Yes | No | - | Yes | BLOCK (PreToolUse should have caught) |
