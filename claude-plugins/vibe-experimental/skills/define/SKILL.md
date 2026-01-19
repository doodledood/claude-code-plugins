---
name: define
description: 'Manifest builder. Creates hierarchical definitions separating Deliverables (what to build) from Invariants (rules to follow). Use when starting new features, refactors, or any work requiring clear done criteria.'
user-invocable: true
---

# /define - Manifest Builder

You are building a **Manifest**—a hierarchical definition that separates:
- **What we build** (Deliverables with Acceptance Criteria)
- **Rules we must follow** (Invariants—Global and Local)

Every criterion MUST have an explicit verification method (bash command, subagent check, or manual flag).

**Verification method selection**: Prefer bash (fastest, most reliable) > subagent (for subjective/complex checks) > manual (only when automation is impossible).

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
   - Local Invariants (applies to specific deliverable)
   - Acceptance Criteria (verification of success)

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
- **Local Invariants** (Constraints specific to this item):
  - [INV-L1.1] Description: ... | Verify: ...
- **Acceptance Criteria** (Positive verification of success):
  - [AC-1.1] Description: ... | Verify: ...
  - [AC-1.2] Description: ... | Verify: ...

### Deliverable 2: [Name]
...
```

## Conceptual Framework

### Invariants vs Acceptance Criteria

| Type | Question | Scope | Failure Semantics |
|------|----------|-------|-------------------|
| **Global Invariant** | "What rules must NEVER be violated?" | Entire task | Task FAILS if violated |
| **Local Invariant** | "What constraints apply while building THIS?" | Single deliverable | Deliverable invalid if violated |
| **Acceptance Criteria** | "How do we know THIS is done?" | Single deliverable | Deliverable incomplete if not met |

### Examples Across Domains

**Coding:**
- Global Invariant: "Tests must pass" (INV-G1)
- Deliverable: "Add user authentication"
  - Local Invariant: "No plaintext passwords" (INV-L1.1)
  - AC: "User can log in with valid credentials" (AC-1.1)

**Writing:**
- Global Invariant: "No spelling errors" (INV-G1)
- Deliverable: "Executive summary"
  - Local Invariant: "Max 500 words" (INV-L1.1)
  - AC: "Key findings are summarized" (AC-1.1)

**Research:**
- Global Invariant: "All claims have citations" (INV-G1)
- Deliverable: "Literature review"
  - Local Invariant: "Only peer-reviewed sources" (INV-L1.1)
  - AC: "Covers major approaches" (AC-1.1)

## Process

### 1. Initialize

Create todos and log file:

```
- [ ] Create log /tmp/define-interview-{timestamp}.md
- [ ] Phase 1: Gather intent & context
- [ ] Phase 2: Identify global invariants
- [ ] Phase 3: Identify deliverables
- [ ] Phase 4: For each deliverable, gather local invariants + ACs
- [ ] Phase 5: Quality gates (if coding task)
- [ ] Phase 6: Project gates from CLAUDE.md (if coding task)
- [ ] (expand: refine as needed)
- [ ] Refresh: read full interview log
- [ ] Write final manifest file
```

### 2. Phase 1: Intent & Context

Establish the high-level purpose.

**Ask:**
```
questions: [
  {
    question: "What is the high-level goal? (1-2 sentences)",
    header: "Goal",
    options: [
      { label: "Build new feature", description: "Adding new capability" },
      { label: "Fix/improve existing", description: "Bug fix or enhancement" },
      { label: "Refactor/restructure", description: "Improve code/structure without behavior change" },
      { label: "Research/analysis", description: "Investigate and document findings" }
    ],
    multiSelect: false
  }
]
```

Follow up for specifics based on their selection.

**Then ask about mental model:**
"What key concepts or architecture should I understand before starting? (e.g., existing patterns, domain knowledge, constraints from other systems)"

Write to log:
```markdown
## Phase 1: Intent & Context

**Goal:** [their answer]
**Task Type:** [feature/fix/refactor/research]
**Mental Model:** [key concepts they mentioned]
```

### 3. Phase 2: Global Invariants

Surface rules that apply to EVERYTHING.

**Ask explicitly:**
```
questions: [
  {
    question: "Are there rules that apply to EVERYTHING? Things that if violated at ANY point mean the task has failed?",
    header: "Global rules",
    options: [
      { label: "Tests must pass", description: "No breaking existing tests" },
      { label: "No security vulnerabilities", description: "OWASP top 10, no secrets in code" },
      { label: "Maintain backwards compatibility", description: "Existing APIs/behavior unchanged" },
      { label: "Follow style guide", description: "Linting/formatting must pass" }
    ],
    multiSelect: true
  }
]
```

Adapt options to task type:
- **Coding**: tests, security, linting, typing
- **Writing**: spelling, tone, formatting
- **Research**: citations, methodology, scope

For each global invariant identified:
1. Capture the rule
2. Ask for verification method (or propose one)
3. Assign INV-G{N} ID

Write to log:
```markdown
## Phase 2: Global Invariants

- [INV-G1] Description: Tests must pass | Verify: bash `npm test`
- [INV-G2] Description: No security vulnerabilities | Verify: subagent (code-bugs-reviewer) focusing on security
```

### 4. Phase 3: Identify Deliverables

Break the work into specific deliverables.

**Ask:**
"What are the specific things you need delivered? (Think of these as items you could check off a list)"

**Probing techniques:**
- "Is this one deliverable or multiple?"
- "Could these be done independently?"
- "What's the natural grouping?"

For a task like "Add user authentication":
- Deliverable 1: User registration flow
- Deliverable 2: Login/logout mechanism
- Deliverable 3: Session management
- Deliverable 4: Password reset

Write to log:
```markdown
## Phase 3: Deliverables Identified

1. [Deliverable name]
2. [Deliverable name]
3. [Deliverable name]
```

### 5. Phase 4: Per-Deliverable Details

For EACH deliverable, gather:

#### 4a. Local Invariants

**Ask:**
"For [Deliverable N], are there constraints on HOW you want it built? (Not what it does, but rules for building it)"

Examples:
- "No storing passwords in plaintext" (for auth deliverable)
- "Must use existing ORM, no raw SQL" (for data deliverable)
- "Max 500 words" (for writing deliverable)
- "Only peer-reviewed sources" (for research deliverable)

For each local invariant:
1. Capture the constraint
2. Ask for verification method
3. Assign INV-L{D}.{N} ID

#### 4b. Acceptance Criteria

**Ask:**
"How do we verify [Deliverable N] is done? What specific things must be true?"

Use probing techniques from the original /define:
- Rejection-first: "What would cause you to reject this deliverable?"
- Edge cases: "What edge cases need handling?"
- Adversarial: Show concrete examples, ask if acceptable

For each AC:
1. Capture what success looks like
2. Ask for verification method
3. Assign AC-{D}.{N} ID

Write to log after each deliverable:
```markdown
### Deliverable 1: [Name]

**Local Invariants:**
- [INV-L1.1] Description: ... | Verify: ...
- [INV-L1.2] Description: ... | Verify: ...

**Acceptance Criteria:**
- [AC-1.1] Description: ... | Verify: ...
- [AC-1.2] Description: ... | Verify: ...
```

### 6. Phase 5: Quality Gates (Coding Tasks)

If the task involves code, ask about quality gates.

**These are typically Global Invariants:**

```
questions: [
  {
    question: "Which code quality checks should be global invariants? (Apply to ALL deliverables)",
    header: "Quality gates",
    options: [
      { label: "No HIGH/CRITICAL bugs", description: "Logic errors, race conditions, error handling" },
      { label: "Type safety", description: "No any abuse, proper narrowing" },
      { label: "Maintainability", description: "DRY, low coupling, consistency" },
      { label: "Simplicity", description: "No over-engineering" }
    ],
    multiSelect: true
  }
]
```

Map selections to Global Invariants with subagent verification:

| Selection | INV-G ID | Agent |
|-----------|----------|-------|
| No bugs | INV-G{N} | code-bugs-reviewer |
| Type safety | INV-G{N} | type-safety-reviewer |
| Maintainability | INV-G{N} | code-maintainability-reviewer |
| Simplicity | INV-G{N} | code-simplicity-reviewer |
| Coverage | INV-G{N} | code-coverage-reviewer |
| Testability | INV-G{N} | code-testability-reviewer |
| Documentation | INV-G{N} | docs-reviewer |
| CLAUDE.md | INV-G{N} | claude-md-adherence-reviewer |

### 7. Phase 6: Project Gates (Auto-Detected)

For coding tasks, detect project-specific gates from CLAUDE.md.

Read CLAUDE.md and extract verifiable commands:
- Type checking: mypy, tsc
- Tests: pytest, jest
- Linting: ruff, eslint
- Formatting: black, prettier

Add as Global Invariants:
```markdown
- [INV-G{N}] Description: Type checking passes | Verify: bash `[command from CLAUDE.md]`
- [INV-G{N}] Description: Tests pass | Verify: bash `[command from CLAUDE.md]`
```

### 8. Latent Discovery (Use as Needed)

Apply latent discovery techniques when direct questions don't surface criteria:

**Tradeoff Forcing:**
When working on a deliverable, ask: "When [value A] and [value B] conflict, which wins?"
- Capture as Local Invariant if specific to deliverable
- Capture as Global Invariant if applies everywhere

**Extreme Aversion:**
"Which extreme is WORSE?" → Reveals constraints

**Pre-mortem:**
"Imagine this shipped and was a disaster. What went wrong?"
- Each risk becomes either a Global Invariant or AC

**Reaction Sampling:**
Show concrete examples, capture reactions as criteria.

### 9. Write to Log (After Each Phase)

Write findings to `/tmp/define-interview-{timestamp}.md` after each phase.

Log format:
```markdown
# Interview Log

Task: [title]
Started: [timestamp]

## Phase 1: Intent & Context
...

## Phase 2: Global Invariants
- [INV-G1] ...
- [INV-G2] ...

## Phase 3: Deliverables Identified
1. ...
2. ...

## Phase 4: Deliverable Details

### Deliverable 1: [Name]
**Local Invariants:**
- [INV-L1.1] ...

**Acceptance Criteria:**
- [AC-1.1] ...

### Deliverable 2: [Name]
...

## Phase 5: Quality Gates
(selections and resulting INV-G IDs)

## Phase 6: Project Gates
(auto-detected from CLAUDE.md)

## Latent Discoveries
(tradeoffs, aversions, pre-mortem risks)

## Open Questions
(none if all resolved)
```

### 10. Write Final Manifest

After refreshing context from the interview log, write `/tmp/manifest-{timestamp}.md`:

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
*Specific items to complete.*

### Deliverable 1: [Name]

**Local Invariants** (Constraints specific to this item):
- [INV-L1.1] Description: [constraint] | Verify: [method]
  ```yaml
  verify:
    method: bash | subagent | codebase | manual
    [details]
  ```

**Acceptance Criteria** (Positive verification of success):
- [AC-1.1] Description: [success condition] | Verify: [method]
  ```yaml
  verify:
    method: bash | subagent | codebase | manual
    [details]
  ```
- [AC-1.2] Description: [success condition] | Verify: [method]
  ...

### Deliverable 2: [Name]

**Local Invariants**:
- [INV-L2.1] ...

**Acceptance Criteria**:
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
| [risk] | [INV-G/INV-L/AC that prevents it] |
```

### 11. Complete

Output the manifest file path:

```text
Manifest complete: /tmp/manifest-{timestamp}.md

To execute: /do /tmp/manifest-{timestamp}.md
```

## ID Scheme Reference

| Type | Format | Example | Scope |
|------|--------|---------|-------|
| Global Invariant | INV-G{N} | INV-G1, INV-G2 | Entire task |
| Local Invariant | INV-L{D}.{N} | INV-L1.1, INV-L2.1 | Deliverable D |
| Acceptance Criteria | AC-{D}.{N} | AC-1.1, AC-2.3 | Deliverable D |

Where D = deliverable number, N = sequential within type.

## Question Format

ALWAYS use AskUserQuestion with:
- 2-4 options (concrete choices reveal criteria better than open-ended questions)
- First option = recommended (with "(Recommended)" suffix)
- Descriptions explain tradeoffs
- Batch related questions when possible

Provide context for why you're asking:
- "Global invariants are rules that if violated anywhere mean the task fails..."
- "Local invariants are constraints on how to build this specific deliverable..."

## Amendment Protocol

Manifests support amendments during execution if genuine gaps are discovered:

- Reference original ID: "INV-G1.1 amends INV-G1"
- Track in manifest: `## Amendments\n- INV-G1.1 (2026-01-19): [reason]`

## Critical Rules

1. **YOU drive the interview** - don't wait for user to think of everything
2. **Hierarchical structure** - Global Invariants → Deliverables → Local Invariants + ACs
3. **Every criterion has verification** - no exceptions
4. **No vague terms** - "clean", "good", "proper" must be defined
5. **Domain-agnostic** - adapt questions to task type (coding/writing/research)
6. **Write to log before proceeding** - after each phase
7. **Concrete choices > open-ended** - users reveal criteria by reacting
8. **Know when to stop** - if criteria are clear, move on
