# Acceptance Criteria Spec: Verification-First /implement Skill

Generated: 2026-01-17
Status: Draft for review
Plugin: vibe-experimental

## Overview

### Problem Statement
Current implementation workflows allow the LLM to declare "done" without verifying all acceptance criteria actually pass. The gap between "I think I'm done" and "all criteria verified passing" leads to incomplete or incorrect implementations that require rework.

### Solution
A verification-first `/implement` skill that:
1. Takes an acceptance criteria spec as input
2. Works toward criteria (no traditional plan)
3. Cannot declare "done" until ALL criteria are verified passing
4. Integrates with stop hooks to enforce verification before stopping
5. Escalates to human only when genuinely stuck (not as escape hatch)

### Success Measure
User runs `/implement` with spec, goes to sleep, wakes up to either:
- All criteria verified passing (actually done)
- Escalation with clear evidence of what's blocking (genuinely stuck)

Never: LLM declares done with unverified or failing criteria.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ACCEPTANCE CRITERIA SPEC                     │
│  (input - from /spec skill)                                     │
│  - criteria with verification methods                            │
│  - examples, rejection criteria, subagent definitions           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      /implement SKILL                            │
│  - reads spec                                                    │
│  - works toward criteria (no plan decomposition)                │
│  - tracks progress via TodoWrite                                │
│  - calls /done to verify before completion                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        /done SKILL                               │
│  - runs ALL verifications from spec                             │
│  - outputs structured pass/fail per criterion                   │
│  - writes verification-status.json to /tmp/                     │
│  - returns: all pass → DONE | any fail → specific feedback      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STOP HOOK                                   │
│  - parses transcript for /implement workflow                    │
│  - checks verification-status.json exists and all pass          │
│  - blocks stop if: no verification run OR any criterion failed  │
│  - allows stop if: all criteria verified passing                │
│  - safety valve: max blocks before escalation to human          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. /implement Skill
Takes acceptance criteria spec, works toward criteria, verifies via /done.

### 2. /done Skill
Runs all verifications from spec, outputs structured results, writes status file.

### 3. implement-stop-hook
Parses transcript, checks verification status, blocks premature stops.

### 4. Verification Status File
JSON file in /tmp/ tracking verification results - the source of truth for stop hook.

---

## Acceptance Criteria

### Category: /implement Skill - Input Handling

#### AC-1: Accepts Spec File Path
**Description**: Skill accepts path to acceptance criteria spec file as primary input.

**Verification**:
```yaml
method: subagent
agent: input-handler-checker
checks:
  - "Skill reads $ARGUMENTS as file path"
  - "Validates file exists before proceeding"
  - "Parses spec structure (criteria, verification methods)"
  - "Reports clear error if file not found or invalid format"
```

#### AC-2: Extracts All Criteria
**Description**: Skill extracts all criteria from spec, including verification methods.

**Verification**:
```yaml
method: subagent
agent: spec-parser-checker
checks:
  - "All criteria IDs extracted"
  - "Verification methods preserved for each criterion"
  - "Examples (accepted/rejected) available for reference"
  - "Task-specific subagent definitions loaded"
```

#### AC-3: Creates Implementation Session
**Description**: Skill creates session artifacts for tracking (status file, log).

**Verification**:
```yaml
method: bash
command: |
  test -f /tmp/implement-session-*.json &&
  test -f /tmp/implement-log-*.md
pass_condition: "exit code 0"
```

---

### Category: /implement Skill - Execution

#### AC-4: Works Toward Criteria Without Plan
**Description**: LLM works toward satisfying criteria without requiring explicit plan decomposition. Internal reasoning is allowed, but progress is measured by criteria passing, not steps completed.

**Verification**:
```yaml
method: subagent
agent: execution-pattern-checker
checks:
  - "No plan file created"
  - "No chunk decomposition"
  - "Work is directed at criteria, not arbitrary steps"
  - "LLM can internally reason about approach"
```

#### AC-5: Tracks Progress via TodoWrite
**Description**: Uses TodoWrite to track which criteria are being worked on, but todos are criteria-based, not step-based.

**Verification**:
```yaml
method: subagent
agent: todo-pattern-checker
checks:
  - "Todos reference criteria IDs"
  - "Todo completion tied to criterion verification, not just 'I did the work'"
  - "Incomplete todos = unverified criteria"
```

**Example - Accepted**:
```
- [ ] Verify AC-1: error-handling-pattern
- [ ] Verify AC-2: tests-pass
- [x] Verify AC-3: no-type-errors (verified passing)
```

**Example - Rejected**:
```
# BAD - step-based, not criteria-based
- [x] Write error handling code
- [x] Add tests
- [ ] Clean up
```

#### AC-6: Calls /done Before Completion
**Description**: Before declaring implementation complete, skill MUST call /done to run all verifications.

**Verification**:
```yaml
method: subagent
agent: transcript-analyzer
checks:
  - "/done skill invoked before any 'complete' or 'done' declaration"
  - "Verification results received and processed"
  - "If any fail, implementation continues (not stops)"
```

#### AC-7: Loops on Verification Failure
**Description**: When /done reports failures, skill continues working on failing criteria with specific feedback.

**Verification**:
```yaml
method: subagent
agent: loop-behavior-checker
checks:
  - "Failed criteria identified from /done output"
  - "Work continues targeting specific failures"
  - "Does not restart from scratch"
  - "Does not abandon passing criteria"
```

---

### Category: /implement Skill - Escalation

#### AC-8: Escalation Requires Evidence
**Description**: Skill can only escalate to human after N consecutive failures on same criterion with different approaches tried.

**Verification**:
```yaml
method: subagent
agent: escalation-checker
checks:
  - "Escalation includes: which criterion, what was tried, why it failed"
  - "At least 3 different approaches attempted before escalation"
  - "Escalation is not used for 'this is hard'"
  - "Clear hypothesis about why criterion may be problematic"
```

**Example - Accepted Escalation**:
```
ESCALATION REQUEST:
Criterion: AC-5 (notifications-queued-via-pubsub)
Attempts:
  1. Used EventEmitter → failed: existing code uses different pattern
  2. Used src/events/bus.ts → failed: bus.publish not exported
  3. Tried importing internals → failed: circular dependency
Hypothesis: The criterion assumes PubSub pattern exists, but
            src/events/bus.ts doesn't export publish().
            May need to update the spec or the bus module.
```

**Example - Rejected Escalation**:
```
# BAD - no evidence of attempts
I'm having trouble with the notification system. Can you help?
```

#### AC-9: Escalation Counter
**Description**: Tracks consecutive failures per criterion. Resets on different criterion or successful verification.

**Verification**:
```yaml
method: subagent
agent: escalation-counter-checker
checks:
  - "Counter stored in session file"
  - "Incremented on same-criterion failure"
  - "Reset on criterion change or success"
  - "Threshold configurable (default 3)"
```

---

### Category: /done Skill - Verification Execution

#### AC-10: Runs All Verifications
**Description**: /done skill runs every verification method defined in the spec.

**Verification**:
```yaml
method: subagent
agent: verification-completeness-checker
checks:
  - "Every criterion ID from spec has verification attempted"
  - "No criteria skipped"
  - "Verification methods executed as defined (bash/subagent/manual)"
```

#### AC-11: Bash Verification Execution
**Description**: For bash verification methods, executes command and checks pass condition.

**Verification**:
```yaml
method: bash
command: "python scripts/test_bash_verification.py"
pass_condition: "exit code 0"
checks:
  - "Command executed in correct directory"
  - "Exit code captured"
  - "Output captured for failure diagnosis"
  - "Timeout handling (default 60s)"
```

#### AC-12: Subagent Verification Execution
**Description**: For subagent verification methods, spawns subagent with defined checks.

**Verification**:
```yaml
method: subagent
agent: subagent-execution-checker
checks:
  - "Subagent spawned with correct agent definition"
  - "Context files provided if specified"
  - "Checks list passed to subagent"
  - "Subagent returns pass/fail per check"
```

#### AC-13: Manual Verification Flagged
**Description**: Manual verifications are flagged but don't block automated flow.

**Verification**:
```yaml
method: subagent
agent: manual-flag-checker
checks:
  - "Manual criteria marked as 'requires-human'"
  - "Don't fail automated verification"
  - "Listed in output for human review"
  - "Clear instructions for what human should check"
```

#### AC-14: Structured Output
**Description**: /done outputs structured pass/fail for each criterion.

**Verification**:
```yaml
method: bash
command: "python scripts/validate_done_output.py"
pass_condition: "exit code 0"
```

**Expected Output Format**:
```yaml
verification_run:
  timestamp: "2026-01-17T10:30:00Z"
  spec_file: "/tmp/spec-xyz.md"

results:
  - criterion_id: "AC-1"
    status: "pass"
    method: "bash"
    details: "npm test exited 0"

  - criterion_id: "AC-2"
    status: "fail"
    method: "subagent"
    details: "pattern-checker found: raw Error() throw at line 45"

  - criterion_id: "AC-3"
    status: "requires-human"
    method: "manual"
    details: "Please verify: notification appears within 5s"

summary:
  total: 10
  pass: 7
  fail: 2
  manual: 1

all_automated_pass: false
```

#### AC-15: Writes Verification Status File
**Description**: /done writes results to /tmp/verification-status-{session}.json for stop hook consumption.

**Verification**:
```yaml
method: bash
command: |
  test -f /tmp/verification-status-*.json &&
  python -c "import json; json.load(open('/tmp/verification-status-*.json'))"
pass_condition: "exit code 0"
```

#### AC-16: Returns Actionable Feedback
**Description**: On failures, /done returns specific, actionable feedback for each failing criterion.

**Verification**:
```yaml
method: subagent
agent: feedback-quality-checker
checks:
  - "Each failure has specific location (file, line if applicable)"
  - "Each failure explains what was expected vs actual"
  - "Each failure references the criterion's accepted/rejected examples if available"
  - "Feedback is actionable, not just 'failed'"
```

---

### Category: Stop Hook - Enforcement

#### AC-17: Detects Implement Workflow
**Description**: Stop hook correctly identifies when /implement skill is active.

**Verification**:
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_detects_workflow -v"
pass_condition: "exit code 0"
```

#### AC-18: Reads Verification Status File
**Description**: Stop hook reads /tmp/verification-status-{session}.json to determine if all criteria pass.

**Verification**:
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_reads_status_file -v"
pass_condition: "exit code 0"
```

#### AC-19: Blocks If No Verification Run
**Description**: If verification-status file doesn't exist, stop is blocked with message to run /done first.

**Verification**:
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_blocks_no_verification -v"
pass_condition: "exit code 0"
```

**Expected Block Message**:
```
HOLD: Cannot stop - verification not run.
Run /done to verify all acceptance criteria before completing.
Criteria remaining: [list from spec]
```

#### AC-20: Blocks If Any Criterion Failed
**Description**: If verification-status shows any failures, stop is blocked with specific failures listed.

**Verification**:
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_blocks_on_failure -v"
pass_condition: "exit code 0"
```

**Expected Block Message**:
```
HOLD: Cannot stop - 2 criteria failed verification.

Failed:
  - AC-2: pattern-checker found raw Error() throw at line 45
  - AC-5: npm test exited with code 1

Continue working on failing criteria, then run /done again.
```

#### AC-21: Allows If All Criteria Pass
**Description**: If verification-status shows all automated criteria pass, stop is allowed.

**Verification**:
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_allows_all_pass -v"
pass_condition: "exit code 0"
```

#### AC-22: Safety Valve
**Description**: After N consecutive blocks, stop is allowed with warning (prevents infinite loops).

**Verification**:
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_safety_valve -v"
pass_condition: "exit code 0"
```

**Safety Valve Behavior**:
- Configurable via `IMPLEMENT_MAX_BLOCKS` env var (default 5)
- Counts "HOLD: Cannot stop" markers in transcript
- After max: allows stop with warning
- Warning includes: which criteria still failing, recommendation to review

#### AC-23: Handles Manual Criteria
**Description**: Criteria marked 'requires-human' don't block automated stop, but are listed for review.

**Verification**:
```yaml
method: bash
command: "pytest tests/hooks/test_implement_stop_hook.py::test_manual_criteria -v"
pass_condition: "exit code 0"
```

---

### Category: Session Management

#### AC-24: Session File Structure
**Description**: Implementation session tracked in JSON file with all state.

**Verification**:
```yaml
method: bash
command: "python scripts/validate_session_file.py"
pass_condition: "exit code 0"
```

**Session File Structure**:
```json
{
  "session_id": "implement-20260117-103000-feature-name",
  "spec_file": "/tmp/spec-xyz.md",
  "started_at": "2026-01-17T10:30:00Z",
  "status": "in_progress",
  "criteria": {
    "AC-1": {"status": "unverified", "attempts": 0},
    "AC-2": {"status": "verified-pass", "attempts": 1},
    "AC-3": {"status": "verified-fail", "attempts": 2, "last_error": "..."}
  },
  "escalation_counts": {
    "AC-3": 2
  },
  "verification_runs": [
    {"timestamp": "...", "results": {...}}
  ]
}
```

#### AC-25: Session Resumable
**Description**: If interrupted, session can be resumed from session file.

**Verification**:
```yaml
method: subagent
agent: resume-checker
checks:
  - "Session file contains all state needed to resume"
  - "Skill can read existing session and continue"
  - "No duplicate work on already-verified criteria"
  - "Escalation counts preserved"
```

#### AC-26: Session Cleanup
**Description**: On successful completion (all criteria pass), session files can be archived/cleaned.

**Verification**:
```yaml
method: subagent
agent: cleanup-checker
checks:
  - "Completion triggers optional cleanup"
  - "Files archived to logs/ or deleted based on config"
  - "Git commits made during implementation preserved"
```

---

### Category: Integration

#### AC-27: Works With Spec From /spec Skill
**Description**: Output from redesigned /spec skill is valid input for /implement.

**Verification**:
```yaml
method: bash
command: |
  # Run /spec → get output path → validate with /implement
  python scripts/test_spec_implement_integration.py
pass_condition: "exit code 0"
```

#### AC-28: Git Integration
**Description**: Implementation changes are committed incrementally (not one big commit at end).

**Verification**:
```yaml
method: subagent
agent: git-pattern-checker
checks:
  - "Commits made during implementation (not just at end)"
  - "Commit messages reference criteria being addressed"
  - "No huge commits with all changes"
```

#### AC-29: Existing Tests Not Broken
**Description**: Implementation doesn't break existing tests (unless spec explicitly allows).

**Verification**:
```yaml
method: bash
command: "npm test"  # or project-specific test command
pass_condition: "exit code 0"
```

---

## Rejection Criteria

The PR will be REJECTED if:

1. **LLM can declare done without verification**: Any path where "done" is declared without /done skill running all verifications
2. **Stop allowed without verification**: Stop hook allows stop when verification-status file missing or has failures
3. **Vague escalation**: Escalation to human without specific evidence of attempts and failure reasons
4. **Plan-based execution**: Implementation uses traditional plan/chunk decomposition instead of criteria-driven
5. **Silent failures**: Verification failures not surfaced with specific, actionable feedback
6. **No safety valve**: Infinite blocking with no escape hatch
7. **Session not resumable**: Interruption loses progress
8. **Criteria skipped**: Any criterion from spec not verified

---

## Examples

### Accepted: Criteria-Based TodoWrite
```
Todos:
- [x] Verify AC-1: error-handling-pattern ✓
- [ ] Verify AC-2: tests-pass (in progress - fixing test failures)
- [ ] Verify AC-3: no-type-errors
- [ ] Verify AC-4: follows-pubsub-pattern
- [ ] Run /done for full verification
```

### Rejected: Step-Based TodoWrite
```
# BAD - steps, not criteria
- [x] Implement error handling
- [x] Write tests
- [ ] Fix lint errors
- [ ] Review code
```

### Accepted: /done Output
```
Verification Results (2026-01-17 10:45:00)
==========================================

✓ AC-1: error-handling-pattern     PASS
  Method: subagent (pattern-checker)
  Details: All error throws use AppError with correlationId

✗ AC-2: tests-pass                 FAIL
  Method: bash (npm test)
  Details: 2 tests failed
    - notification.test.ts:45 - expected 'queued' got 'sent'
    - notification.test.ts:78 - timeout waiting for event

✓ AC-3: no-type-errors             PASS
  Method: bash (tsc --noEmit)
  Details: Exit code 0

Summary: 2/3 automated criteria pass

Action Required:
  Fix failing tests in notification.test.ts
  Then run /done again to re-verify
```

### Rejected: Vague /done Output
```
# BAD - no actionable details
Some tests failed. Please fix and try again.
```

### Accepted: Escalation Request
```
ESCALATION: Criterion AC-4 (follows-pubsub-pattern)

I've attempted to satisfy this criterion 3 times:

Attempt 1: Direct import of src/events/bus.ts
  Result: bus.publish is not exported (private function)

Attempt 2: Created new event emitter in notification module
  Result: Subagent rejected - "must use existing PubSub, not new emitter"

Attempt 3: Tried to extend bus.ts to export publish
  Result: Breaks 12 existing tests that mock bus internals

Hypothesis: The criterion assumes bus.publish is available, but the
current codebase keeps it private. Options:
  1. Update criterion to allow new event emitter
  2. Refactor bus.ts to export publish (breaking change)
  3. Use different integration pattern

Requesting human decision on which path to take.
```

### Rejected: Lazy Escalation
```
# BAD - no evidence of attempts
I can't figure out the PubSub pattern. Can you help?
```

---

## Pre-mortem Risks

| Risk | Preventive Criterion |
|------|---------------------|
| LLM finds loophole to skip verification | AC-6, AC-17, AC-19 enforce verification required |
| Stop hook too aggressive, blocks legitimately done work | AC-21 allows stop when all pass, AC-22 safety valve |
| Verification runs slow, LLM impatient | AC-11 has timeout handling, subagents are fast |
| Subagent verifiers unreliable | Examples in spec provide ground truth reference |
| Session file corrupted | AC-25 session resumable, validation on read |
| Criteria impossible to satisfy | AC-8, AC-9 escalation path with evidence |
| Manual criteria block automation | AC-13, AC-23 manual criteria flagged but don't block |

---

## Disappointed Scenarios

| Scenario | Preventive Criterion |
|----------|---------------------|
| "LLM said done but tests were failing" | AC-6, AC-17, AC-20 - can't stop with failures |
| "I woke up to escalation spam, not real progress" | AC-8, AC-9 - escalation requires evidence |
| "Verification took forever to run" | AC-11 timeouts, subagent execution is bounded |
| "I couldn't tell what was passing or failing" | AC-14, AC-16 - structured, actionable output |
| "It kept working on already-done criteria" | AC-5, AC-24 - session tracks verified criteria |
| "Hook blocked me even after everything passed" | AC-21 - explicit allow on all pass |

---

## Verification Infrastructure Required

### Scripts

#### `scripts/validate_done_output.py`
Validates /done output follows expected structure.

#### `scripts/validate_session_file.py`
Validates session JSON structure and state consistency.

#### `scripts/test_spec_implement_integration.py`
End-to-end test: /spec output → /implement input.

#### `scripts/test_bash_verification.py`
Tests bash verification execution (timeouts, exit codes, output capture).

### Tests

#### `tests/hooks/test_implement_stop_hook.py`
Tests for stop hook:
- `test_detects_workflow` - identifies /implement skill active
- `test_reads_status_file` - parses verification-status.json
- `test_blocks_no_verification` - blocks when no verification run
- `test_blocks_on_failure` - blocks when criteria fail
- `test_allows_all_pass` - allows when all pass
- `test_safety_valve` - allows after max blocks
- `test_manual_criteria` - handles requires-human criteria

### Subagents

#### `execution-pattern-checker`
Verifies implementation follows criteria-driven pattern, not plan-driven.

#### `todo-pattern-checker`
Verifies TodoWrite entries reference criteria IDs.

#### `escalation-checker`
Verifies escalation requests include required evidence.

#### `feedback-quality-checker`
Verifies /done failure feedback is specific and actionable.

#### `resume-checker`
Verifies session can be resumed from file.

---

## Files to Create

```
claude-plugins/vibe-experimental/
├── skills/
│   ├── implement/
│   │   └── SKILL.md              # Main implement skill
│   └── done/
│       └── SKILL.md              # Verification runner skill
├── hooks/
│   ├── implement_stop_hook.py    # Stop hook enforcement
│   └── hook_utils.py             # Shared utilities
├── agents/
│   └── (subagent definitions)
├── scripts/
│   ├── validate_done_output.py
│   ├── validate_session_file.py
│   └── test_spec_implement_integration.py
└── tests/
    └── hooks/
        └── test_implement_stop_hook.py
```

---

## Out of Scope

- Spec skill changes (covered in separate spec)
- UI/rendering of progress
- Cloud/remote execution
- Multi-repo support
- Parallelization of verification

---

## Open Questions

None - all resolved during design conversation.

---

## Appendix: Stop Hook Decision Matrix

| Verification Status File | Automated Criteria | Block Count | Decision |
|-------------------------|-------------------|-------------|----------|
| Missing | - | < max | BLOCK: "Run /done first" |
| Missing | - | >= max | ALLOW: Safety valve + warning |
| Exists | All pass | - | ALLOW |
| Exists | Any fail | < max | BLOCK: List failures |
| Exists | Any fail | >= max | ALLOW: Safety valve + warning |
| Exists | All pass (some manual) | - | ALLOW: List manual for review |
