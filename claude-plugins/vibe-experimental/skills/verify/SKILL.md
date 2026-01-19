---
name: verify
description: 'Manifest verification runner. Spawns parallel verifiers for Global Invariants and Acceptance Criteria. Called by /do, not directly by users.'
user-invocable: false
---

# /verify - Manifest Verification Runner

You run all verification methods from a Manifest file. You spawn one verifier agent per criterion in parallel—you don't run checks yourself.

## Input

`$ARGUMENTS` = "<manifest-file-path> <execution-log-path> [--scope=files]"

- `--scope=files`: Comma-separated file paths for reviewer scope override (optional)

Examples:
- `/tmp/manifest-123.md /tmp/do-log-123.md`
- `/tmp/manifest-123.md /tmp/do-log-123.md --scope=src/auth.ts,src/session.ts`

## Process

### 1. Parse Inputs

Read both files:
- Manifest file: extract all criteria with verification methods
- Execution log: context for verifiers

Parse `--scope=files` if provided (optional, for reviewer scope override).

### 2. Extract All Criteria

From the Manifest, extract:

**Global Invariants (INV-G*):**
```yaml
- id: INV-G1
  type: global-invariant
  description: "Tests must pass"
  verify:
    method: bash
    command: "npm test"
```

**Acceptance Criteria (AC-{D}.{N}):**
```yaml
- id: AC-1.1
  type: acceptance-criteria
  deliverable: 1
  description: "User can log in"
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Verify login flow works as specified"

- id: AC-1.2
  type: acceptance-criteria
  deliverable: 1
  description: "Passwords are hashed, not plaintext"
  verify:
    method: codebase
    check: "No password storage without hashing"
```

### 3. Categorize by Verification Method

Group criteria by verification type (from `verify.method`):
- **bash**: Shell commands
- **codebase**: Code pattern checks
- **subagent**: Reviewer agents
- **manual**: Require human verification (set aside)

Then sort by expected duration (slow first):
- **Slow** (30s+): test suites, builds, reviewer agents
- **Fast** (seconds): lint, typecheck, simple codebase patterns

### 4. Launch All Verifiers in Parallel

Launch ONE verifier per criterion in a single parallel call, **slow ones first**. Claude Code caps at ~10 concurrent and queues the rest.

```
// Single message with multiple Task calls - slow first

// Global Invariants (often slow - tests, builds)
Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: INV-G1 (global-invariant)
Description: Tests must pass
Verification method: bash
Command: npm test")

// Subagent checks (slow)
Task(subagent_type="vibe-experimental:code-bugs-reviewer", prompt="
Criterion: INV-G2 (global-invariant)
Description: No HIGH or CRITICAL bugs
Scope: git diff against origin/main")

// Acceptance Criteria
Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: AC-1.1 (acceptance-criteria, Deliverable 1)
Description: User can log in with valid credentials
Verification method: bash
Command: npm run test:auth")

Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: AC-1.2 (acceptance-criteria, Deliverable 1)
Description: Passwords are hashed, not plaintext
Verification method: codebase
Files: src/auth/
Check: Password storage must use bcrypt or similar hashing")

// Fast checks last
Task(subagent_type="vibe-experimental:criteria-checker", prompt="
Criterion: INV-G3 (global-invariant)
Description: Linting passes
Verification method: bash
Command: npm run lint")
```

**Scope override**: If /do provides explicit scope, pass to reviewers:
```
Task(subagent_type="vibe-experimental:code-bugs-reviewer", prompt="
Criterion: INV-G2 (global-invariant)
Review these files for bugs: src/auth.ts, src/session.ts
Focus on HIGH and CRITICAL severity issues only.")
```

### 5. Collect Results

#### For bash/codebase results (from criteria-checker)

Standard structure:
```json
{
  "passed": ["INV-G1", "INV-L1.1", "AC-1.1"],
  "failed": [
    {
      "id": "AC-1.2",
      "type": "acceptance-criteria",
      "deliverable": 1,
      "method": "bash",
      "location": "src/auth.test.ts:45",
      "expected": "'authenticated'",
      "actual": "'pending'",
      "fix_hint": "Check token validation logic"
    }
  ],
  "manual": ["AC-2.3"]
}
```

#### For subagent results (from reviewer agents)

Parse based on criterion's `prompt` field which specifies pass conditions:

Examples:
- `prompt: "Pass if no HIGH or CRITICAL severity issues"` → FAIL if any HIGH/CRITICAL found
- `prompt: "Pass if no MEDIUM+ issues"` → FAIL if any MEDIUM/HIGH/CRITICAL found

Convert to same structure:
```json
{
  "id": "INV-G2",
  "type": "global-invariant",
  "method": "subagent",
  "agent": "code-bugs-reviewer",
  "issues": [
    {
      "severity": "HIGH",
      "title": "Race condition in auth flow",
      "location": "src/auth.ts:45-52",
      "description": "Token validation not atomic",
      "fix_hint": "Add mutex or use atomic compare-and-set"
    }
  ]
}
```

### 6. Decision Logic

```
if any Global Invariant failed:
    → Return ALL failures (global failures are critical)
    → Highlight global failures prominently
    → /do must fix global issues first

elif any AC failed:
    → Return failures grouped by deliverable
    → /do continues working on specific deliverables

elif all automated pass AND manual exists:
    → Return manual criteria
    → Hint to call /escalate for human review

elif all pass (no manual):
    → Call /done
```

### 7. Output Format

#### On Failure

```markdown
## Verification Results

### Global Invariants

#### Failed (N)

- **INV-G1**: Tests must pass
  Method: bash (`npm test`)
  Location: `src/auth.test.ts:45`
  Expected: `'authenticated'`
  Actual: `'pending'`
  Fix: Check token validation in AuthService

- **INV-G2**: No HIGH or CRITICAL bugs
  Method: subagent (code-bugs-reviewer)
  Issues: 1

  1. [HIGH] Race condition in auth flow
     Location: `src/auth.ts:45-52`
     Description: Token validation not atomic
     Fix: Add mutex or use atomic compare-and-set

#### Passed (M)
- INV-G3, INV-G4

---

### Deliverable 1: User Authentication

#### Failed (1)
- **AC-1.2**: Session persists across page reload
  Method: bash (`npm run test:session`)
  Location: `src/session.test.ts:23`
  Issue: Session cookie not set with correct flags
  Fix: Add `httpOnly` and `secure` flags

#### Passed (1)
- AC-1.1

---

### Deliverable 2: Password Reset

- **AC-2.1**: User receives reset email - PASS
- **AC-2.2**: Reset link works - PASS

---

**Summary:**
- Global Invariants: 2/4 failed (CRITICAL - fix first)
- Deliverable 1: 1/2 ACs failed
- Deliverable 2: All pass

Continue working on failed criteria, then call /verify again.
```

#### On Success with Manual

```markdown
## Verification Results

### All Automated Criteria Pass

**Global Invariants:** 4/4 pass
**Deliverable 1:** 2/2 ACs pass
**Deliverable 2:** 2/2 ACs pass

### Manual Verification Required

- **AC-1.3**: UX feels intuitive (Deliverable 1)
  How to verify: [from manifest]

- **AC-2.3**: Email tone is appropriate (Deliverable 2)
  How to verify: [from manifest]

---

Call /escalate to surface for human review.
```

#### On Full Success

Call /done:
```
Use the Skill tool to complete: Skill("vibe-experimental:done", "all criteria verified")
```

## Critical Rules

1. **Don't run checks yourself** - spawn criteria-checker or reviewer agents
2. **Single parallel launch** - all criteria in one call, slow ones first
3. **Preserve hierarchy** - report results grouped by type and deliverable
4. **Global failures are critical** - highlight them prominently
5. **Actionable feedback** - pass through file:line, expected vs actual
6. **Call /done on success** - trigger completion
7. **Parse prompt for pass condition** - subagent criteria specify conditions in natural language
8. **Return all issues** - for failed criteria, include all issues so /do can fix them

## Criterion Types Reference

| Type | ID Pattern | Scope | Failure Impact |
|------|------------|-------|----------------|
| Global Invariant | INV-G{N} | Entire task | Task fails |
| Acceptance Criteria | AC-{D}.{N} | Deliverable D | Deliverable incomplete |
