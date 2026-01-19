---
name: define
description: 'Manifest builder. Creates hierarchical definitions separating Deliverables (what to build) from Invariants (rules to follow). Use when starting new features, refactors, or any work requiring clear done criteria.'
user-invocable: true
---

# /define - Manifest Builder

You are building a **Manifest**—a hierarchical definition that separates:
- **What we build** (Deliverables with Acceptance Criteria)
- **Rules we must follow** (Global Invariants)

Every criterion MUST have an explicit verification method (bash command, subagent check, or manual flag).

**Verification method selection**: Bash for deterministic checks (lint, test, typecheck) | Subagent for logic/reasoning/judgment | Manual only when automation is impossible.

## Input

`$ARGUMENTS` = task description, optionally with context/research

Examples:
- Simple: `/define "Add user authentication"`
- With context: `/define "Add OAuth integration" --context /tmp/oauth-research.md`
- Inline context: `/define "Refactor payment module - must use Stripe v3 API"`

If no arguments provided, ask: "What would you like to build or change?"

### Handling Provided Context

If $ARGUMENTS contains context (file reference, inline notes, or research):

1. **Read and summarize** the context
2. **Ask**: "You provided [summary]. What from this MUST the implementation incorporate?"
3. **Classify answers** as either:
   - Global Invariants (applies to everything)
   - Acceptance Criteria (per-deliverable verification)

## Output

Manifest file: `/tmp/manifest-{timestamp}.md`

## The Manifest Schema

```markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts/architecture to understand]

## 2. Global Invariants (The Constitution)
*Rules that apply to the ENTIRE execution. If these fail, the task is failed.*

- [INV-G1] Description: ... | Verify: [Method]
- [INV-G2] Description: ... | Verify: [Method]

## 3. Deliverables (The Work)
*Specific items to complete.*

### Deliverable 1: [Name]
- **Acceptance Criteria:**
  - [AC-1.1] Description: ... | Verify: ...
  - [AC-1.2] Description: ... | Verify: ...

### Deliverable 2: [Name]
...
```

## Conceptual Framework

### Global Invariants vs Acceptance Criteria

| Type | Question | Scope | Failure Semantics |
|------|----------|-------|-------------------|
| **Global Invariant** | "What rules must NEVER be violated?" | Entire task | Task FAILS if violated |
| **Acceptance Criteria** | "How do we know THIS deliverable is done?" | Single deliverable | Deliverable incomplete if not met |

ACs can be **positive** ("user can log in") or **negative** ("passwords are hashed, not plaintext").

### Examples Across Domains

**Coding:**
- Global Invariant: "Tests must pass" (INV-G1)
- Deliverable: "Add user authentication"
  - AC: "User can log in with valid credentials" (AC-1.1)
  - AC: "Passwords are hashed, not stored in plaintext" (AC-1.2)

**Writing:**
- Global Invariant: "No spelling errors" (INV-G1)
- Deliverable: "Executive summary"
  - AC: "Key findings are summarized" (AC-1.1)
  - AC: "Under 500 words" (AC-1.2)

**Research:**
- Global Invariant: "All claims have citations" (INV-G1)
- Deliverable: "Literature review"
  - AC: "Covers major approaches" (AC-1.1)
  - AC: "Only uses peer-reviewed sources" (AC-1.2)

## Process

### 1. Initialize

Create todos and log file:

```
- [ ] Create log /tmp/define-interview-{timestamp}.md
- [ ] Phase 1: Understand intent (high info-gain questions)
- [ ] Phase 2: Generate candidate deliverables→present for validation
- [ ] Phase 3: For each deliverable, generate candidate ACs→present for validation
- [ ] Phase 4: Global invariants (auto-detect + generate candidates)
- [ ] (expand: refine as needed)
- [ ] Refresh: read full interview log
- [ ] Write final manifest file
```

### Interview Philosophy

**YOU generate, user validates.** Users have surface-level knowledge. Don't ask open-ended questions like "What are your constraints?" - they won't know. Instead:

1. **Generate candidates** from domain knowledge and task context
2. **Present concrete options** for user to react to
3. **Learn from reactions** - acceptance/rejection reveals criteria
4. **Maximize information gain** - ask questions that maximally split the possibility space
5. **Order by importance** - high-stakes decisions first to avoid irrelevant rabbit holes

**AskUserQuestion always has an "Other" option** - user can provide free text if your candidates miss something. But your candidates should be good enough that "Other" is rarely needed.

### 2. Phase 1: Intent & Context (High Info-Gain)

Start with questions that maximally constrain the solution space.

**Question 1: Task type** (determines entire approach)
```
questions: [
  {
    question: "What type of work is this?",
    header: "Task type",
    options: [
      { label: "New feature", description: "Adding new capability to existing system" },
      { label: "Bug fix", description: "Fixing incorrect behavior" },
      { label: "Refactor", description: "Restructure without changing behavior" },
      { label: "Greenfield", description: "Building something new from scratch" }
    ],
    multiSelect: false
  }
]
```

**Question 2: Scope** (high info-gain - constrains everything else)
```
questions: [
  {
    question: "How would you describe the scope?",
    header: "Scope",
    options: [
      { label: "Single file change", description: "Localized to one file" },
      { label: "Single component", description: "Changes within one module/component" },
      { label: "Cross-cutting", description: "Touches multiple parts of the system" },
      { label: "System-wide", description: "Architectural or foundational change" }
    ],
    multiSelect: false
  }
]
```

**Question 3: Risk profile** (determines how many guardrails needed)
```
questions: [
  {
    question: "What's the risk profile?",
    header: "Risk",
    options: [
      { label: "Low risk", description: "Easy to revert, low user impact" },
      { label: "Medium risk", description: "Needs testing, moderate impact" },
      { label: "High risk", description: "Hard to revert, significant impact" },
      { label: "Critical path", description: "Affects core functionality, must not break" }
    ],
    multiSelect: false
  }
]
```

Based on answers, you now know:
- Task type → what patterns to expect
- Scope → how many deliverables likely
- Risk → how thorough verification needs to be

Write to log with inferences:
```markdown
## Phase 1: Intent & Context

**Task:** [from $ARGUMENTS]
**Type:** [feature/fix/refactor/greenfield]
**Scope:** [single-file/component/cross-cutting/system-wide]
**Risk:** [low/medium/high/critical]

**Inferences:**
- [what this combination implies about deliverables]
- [what this implies about invariants needed]
```

### 3. Phase 2: Identify Deliverables

**Generate candidate deliverables from task description, then validate.**

Based on $ARGUMENTS and Phase 1 answers, decompose into deliverables:

**Decomposition heuristics:**
- Single-file scope → usually 1 deliverable
- Component scope → 1-3 deliverables (interfaces, logic, tests)
- Cross-cutting → 3-5 deliverables (by layer or by feature slice)
- System-wide → 5+ deliverables (architectural pieces)

**Example decomposition for "Add user authentication":**
```
questions: [
  {
    question: "I've broken this into deliverables. Which should we include?",
    header: "Deliverables",
    options: [
      { label: "User registration flow", description: "Sign-up form, validation, account creation" },
      { label: "Login/logout", description: "Credential verification, session creation/destruction" },
      { label: "Session management", description: "Token handling, expiry, refresh" },
      { label: "Password reset", description: "Reset request, email, token verification" }
    ],
    multiSelect: true
  }
]
```

**Key: YOU propose the decomposition.** Don't ask "what are the deliverables?" - the user won't know the right granularity. You know from the task type and scope what makes sense.

If user selects "Other", they can describe something you missed, which you then add.

Write to log:
```markdown
## Phase 3: Deliverables

Generated based on: [scope] + [task description]

1. [Deliverable name] - [brief description]
2. [Deliverable name] - [brief description]
```

### 4. Phase 3: Per-Deliverable Acceptance Criteria

**Generate candidate ACs from domain knowledge, then validate.**

For EACH deliverable, generate ACs covering:
1. **Happy path** - core functionality works
2. **Error handling** - graceful failures
3. **Edge cases** - boundary conditions
4. **Constraints** - how it must (or must not) be built

**Example for "Login/logout" deliverable:**
```
questions: [
  {
    question: "For Login/logout - which acceptance criteria should we include?",
    header: "Login ACs",
    options: [
      { label: "Valid credentials → access granted", description: "Core happy path" },
      { label: "Invalid credentials → clear error, no access", description: "Error handling" },
      { label: "Passwords hashed, not plaintext", description: "Security constraint" },
      { label: "Session created on login, destroyed on logout", description: "State management" }
    ],
    multiSelect: true
  }
]
```

**AC generation heuristics by deliverable type:**

| Deliverable Type | Typical ACs |
|-----------------|-------------|
| API endpoint | Request/response format, auth, error codes, rate limiting |
| UI component | Renders correctly, handles input, accessibility, responsive |
| Data operation | CRUD works, validation, constraints enforced, idempotent |
| Integration | Connection handling, retry logic, timeout behavior |
| Algorithm | Correctness, performance bounds, edge cases |

**You propose verification methods:**
- Functional → `bash: npm run test:feature`
- Constraint → `codebase: check pattern exists/doesn't exist`
- Subjective → `manual: human review`

**Don't ask open-ended "what else?"** - if you've covered happy path, errors, edges, and constraints, you've covered it. User can add via "Other" if truly missing something.

Write to log after each deliverable:
```markdown
### Deliverable 1: [Name]

**Acceptance Criteria (generated):**
- [AC-1.1] [description] | Verify: [method]
- [AC-1.2] [description] | Verify: [method]
```

### 5. Phase 4: Global Invariants (Last)

Global invariants are cross-cutting rules verified at the end. Consolidate from three sources:

**1. Auto-detect from CLAUDE.md** (for coding tasks):
Read CLAUDE.md and extract verifiable commands:
- Type checking: mypy, tsc
- Tests: pytest, jest
- Linting: ruff, eslint
- Formatting: black, prettier

**2. Generate candidates based on task type + risk:**

| Task Type | Risk | Likely Invariants |
|-----------|------|-------------------|
| Feature | High/Critical | Tests pass, no regressions, security, linting |
| Feature | Low/Medium | Tests pass, linting |
| Bug fix | Any | Tests pass, specific regression test |
| Refactor | Any | Tests pass, behavior unchanged, linting |
| Greenfield | Any | Tests pass (if tests exist), linting |

**3. Quality reviewers** (if coding task and user wants deeper checks):

| Quality Gate | Verification |
|--------------|--------------|
| No HIGH/CRITICAL bugs | subagent: code-bugs-reviewer |
| Type safety | subagent: type-safety-reviewer |
| Maintainability | subagent: code-maintainability-reviewer |
| Simplicity | subagent: code-simplicity-reviewer |

**Present consolidated candidates for validation:**
```
questions: [
  {
    question: "Which should be global invariants? (If violated anywhere, task fails)",
    header: "Invariants",
    options: [
      { label: "Tests pass (Recommended)", description: "[command from CLAUDE.md or standard]" },
      { label: "Linting/type checks pass", description: "[command from CLAUDE.md or standard]" },
      { label: "No security vulnerabilities", description: "OWASP top 10, no secrets in code" },
      { label: "Code quality review", description: "Subagent checks for bugs, maintainability" }
    ],
    multiSelect: true
  }
]
```

**Adapt to domain:**
- **Coding**: tests, linting, security, quality reviewers
- **Writing**: no spelling errors, consistent tone, word count limits
- **Research**: all claims cited, methodology documented

Write to log:
```markdown
## Phase 4: Global Invariants

Auto-detected from CLAUDE.md:
- [INV-G1] Tests pass | Verify: bash `pytest`
- [INV-G2] Linting passes | Verify: bash `ruff check`

User-selected:
- [INV-G3] No security vulnerabilities | Verify: subagent code-bugs-reviewer (security focus)
```

### 6. Latent Discovery (Only If Needed)

These techniques are for **edge cases where your generated candidates weren't sufficient**. Most tasks won't need them.

**Tradeoff question** (when you detect competing concerns):
```
questions: [
  {
    question: "When speed and thoroughness conflict, which wins?",
    header: "Tradeoff",
    options: [
      { label: "Speed - ship fast, iterate later", description: "Accept some rough edges" },
      { label: "Thoroughness - get it right first", description: "Take time to be complete" },
      { label: "Depends on the specific case", description: "Judge case by case" }
    ],
    multiSelect: false
  }
]
```

**Pre-mortem** (for high-risk tasks only):
```
questions: [
  {
    question: "If this fails badly, what's the most likely cause?",
    header: "Risk",
    options: [
      { label: "Performance issues at scale", description: "Works in dev, fails in prod" },
      { label: "Integration breaks", description: "Downstream systems affected" },
      { label: "Data corruption", description: "Invalid state persisted" },
      { label: "Security vulnerability", description: "Exploitable flaw" }
    ],
    multiSelect: true
  }
]
```
→ Selected risks become either Global Invariants or specific ACs.

**Don't overuse these.** If your Phase 1-3 candidates were good, the manifest is complete.

### 7. Write to Log (After Each Phase)

Write findings to `/tmp/define-interview-{timestamp}.md` after each phase.

Log format:
```markdown
# Interview Log

Task: [title]
Started: [timestamp]

## Phase 1: Intent & Context
...

## Phase 2: Deliverables Identified
1. ...
2. ...

## Phase 3: Deliverable Details

### Deliverable 1: [Name]
**Acceptance Criteria:**
- [AC-1.1] ...
- [AC-1.2] ...

### Deliverable 2: [Name]
...

## Phase 4: Global Invariants
Auto-detected: ...
User-selected: ...

## Latent Discoveries (if any)
(tradeoffs, pre-mortem risks)

## Open Questions
(none if all resolved)
```

### 8. Write Final Manifest

After refreshing context from the interview log, write `/tmp/manifest-{timestamp}.md`.

**Order deliverables by dependency then importance.** /do iterates in order, so:
1. Dependencies first (if D2 needs D1, D1 comes first)
2. Among independent deliverables, higher importance first
3. This lets /do execute top-to-bottom without backtracking

```markdown
# Definition: [Task Description]

Generated: [date]
Interview Log: /tmp/define-interview-{timestamp}.md

## 1. Intent & Context
- **Goal:** [High-level purpose from Phase 1]
- **Mental Model:** [Key concepts/architecture from Phase 1]

## 2. Global Invariants (The Constitution)
*Rules that apply to the ENTIRE execution. If these fail, the task is failed.*

- [INV-G1] Description: [rule] | Verify: [method]
  ```yaml
  verify:
    method: bash | subagent | manual
    command: "[if bash]"
    agent: "[if subagent]"
    prompt: "[if subagent]"
  ```

- [INV-G2] Description: [rule] | Verify: [method]
  ...

## 3. Deliverables (The Work)
*Ordered by dependency, then importance. Execute top-to-bottom.*

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: [criterion] | Verify: [method]
  ```yaml
  verify:
    method: bash | subagent | codebase | manual
    [details]
  ```
- [AC-1.2] Description: [criterion] | Verify: [method]
  ...

### Deliverable 2: [Name]

**Acceptance Criteria:**
- [AC-2.1] ...
- [AC-2.2] ...

## 4. Tradeoffs & Preferences
*When criteria conflict, these preferences apply:*

| Dimension | Preference | Context |
|-----------|------------|---------|
| [from interview] | [preference] | [when it applies] |

## 5. Pattern References
- Follow: [reference artifact] ([key characteristics])
- Avoid: [anti-pattern] ([why])

## 6. Pre-mortem Risks
| Risk | Preventive Measure |
|------|-------------------|
| [risk] | [INV-G/AC that prevents it] |
```

### 9. Complete

Output the manifest file path:

```text
Manifest complete: /tmp/manifest-{timestamp}.md

To execute: /do /tmp/manifest-{timestamp}.md
```

## ID Scheme Reference

| Type | Format | Example | Scope |
|------|--------|---------|-------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 | Entire task |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1, AC-2.3 | Deliverable D |

Where D = deliverable number, N = sequential within deliverable.

## Question Format

ALWAYS use AskUserQuestion with:
- 2-4 options (concrete choices reveal criteria better than open-ended questions)
- First option = recommended (with "(Recommended)" suffix)
- Descriptions explain tradeoffs
- Batch related questions when possible

Provide context for why you're asking:
- "Global invariants are rules that if violated anywhere mean the task fails..."
- "Acceptance criteria can be positive (what must work) or negative (what must not happen)..."

## Amendment Protocol

Manifests support amendments during execution if genuine gaps are discovered:

- Reference original ID: "INV-G1.1 amends INV-G1"
- Track in manifest: `## Amendments\n- INV-G1.1 (2026-01-19): [reason]`

## Critical Rules

1. **YOU generate, user validates** - never ask open-ended "what do you want?"
2. **Maximize information gain** - high-stakes questions first, space-splitting
3. **Concrete options always** - users reveal criteria by reacting, not by inventing
4. **Every criterion has verification** - you propose the method, don't ask
5. **No vague terms** - "clean", "good", "proper" → must be measurable
6. **Domain knowledge drives** - use your knowledge to generate relevant candidates
7. **Write to log before proceeding** - after each phase
8. **Know when to stop** - happy path + errors + edges + constraints = sufficient
