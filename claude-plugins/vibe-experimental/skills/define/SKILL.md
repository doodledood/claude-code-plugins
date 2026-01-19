---
name: define
description: 'Work definition builder. Creates exhaustive definitions where every criterion has an explicit verification method. Use when starting new features, refactors, or any work requiring clear done criteria.'
user-invocable: true
---

# /define - Work Definition Builder

You are building a work definition. Every criterion you capture MUST have an explicit verification method (bash command, subagent check, or manual flag).

**Verification method selection**: Prefer bash (fastest, most reliable) > subagent (for subjective/complex checks) > manual (only when automation is impossible, e.g., "feels right to user").

## Input

`$ARGUMENTS` = task description, optionally with context/research

Examples:
- Simple: `/define "Add user authentication"`
- With context: `/define "Add OAuth integration" --context /tmp/oauth-research.md`
- Inline context: `/define "Refactor payment module - must use Stripe v3 API, avoid webhooks per security team decision"`

If no arguments provided, ask: "What would you like to build or change?"

### Handling Provided Context

If $ARGUMENTS contains context (file reference, inline notes, or research findings):

1. **Read and summarize** the context
2. **Ask**: "You provided [summary]. What from this MUST the implementation incorporate? (What would cause rejection if ignored?)"
3. **Turn answers into criteria**:
   ```yaml
   - id: AC-N
     category: rejection
     description: "Must incorporate [specific aspect]"
     verify: [user-specified or manual]
   ```

Don't ask redundant questions about whether context exists—if it's provided, handle it. The question is WHAT from the context is mandatory, not IF context should be used.

**If you find contradictions or conflicts** (e.g., context contradicts codebase, criteria seem incompatible, user's answers contradict earlier answers): Surface as a question. User may not realize the conflict, or may have context you don't. Their resolution becomes a criterion.

## Output

Definition file: `/tmp/define-{timestamp}.md`

## Process

### 1. Initialize

Create todos and log file. The todos below are starting points—add task-specific areas as you discover them:

```
- [ ] Create log /tmp/define-interview-{timestamp}.md
- [ ] Gather positive criteria (feature, quality, architecture)
- [ ] Gather negative criteria (rejection conditions)
- [ ] Explore edge cases relevant to this task
- [ ] Surface latent criteria (use techniques relevant to task type)
- [ ] Ask task-specific questions (security, performance, UX, etc. as relevant)
- [ ] Refine vague criteria to specific
- [ ] Ask code quality gates question (if coding task)
- [ ] Detect project quality gates from CLAUDE.md (if coding task)
- [ ] (expand: add areas as discovered during interview)
- [ ] Refresh: read full interview log
- [ ] Write final definition file
```

**Note**: The interview techniques in Section 2 are tools, not a checklist. Start with rejection criteria, then use concrete choice questions to probe deeper. Use latent discovery techniques when direct questions don't surface what you need.

### 2. Proactive LLM-Driven Interview

YOU drive the interview. Don't wait for the user to volunteer everything. Surface questions they wouldn't think to ask.

**Goal**: A definition so complete that an LLM can execute autonomously without ambiguity.

**Interview Philosophy**:

**Be proactive with concrete choices.** Users often can't articulate criteria until they see options to react to. Present concrete alternatives—code examples, approaches, tradeoffs—and let them accept or reject. Their reactions reveal criteria they couldn't have stated upfront. Use AskUserQuestion with 2-4 options; reserve open-ended questions for initial exploration only.

Start with "What would cause you to reject this?" to prime rejection thinking, then drive the interview with concrete choices based on their answer.

**Know when to stop**: If the user clearly knows what they want and rejection criteria are captured, move on. Don't over-interview simple tasks. Probe deeper when complexity or risk warrants it.

**Interview Techniques (use as needed, not as checklist):**

#### Positive Criteria
Ask about:
- Feature behavior: "What should happen when X?"
- Quality standards: "What code quality expectations apply?"
- Architecture: "Where should this live in the codebase?"
- Integration: "What existing systems does this touch?"

#### Negative Criteria (Rejection-First)
Ask explicitly: "What would cause you to REJECT this output?"
- Capture ALL rejection criteria the user mentions
- These are the most important criteria - everything else is optional
- If user struggles, offer common rejection reasons as options based on task type

#### Edge Cases
Present relevant edge cases as options for the user to confirm handling:
- Empty input / null values
- Large input / scale limits
- Concurrent access / race conditions
- Failure modes / error handling
- Task-specific edge cases (e.g., timezone handling, unicode, permissions)

Use multi-select AskUserQuestion: "Which edge cases need explicit handling?" with task-relevant options.

#### Adversarial Examples
Show 1-3 concrete implementations that vary on relevant dimensions. The goal is to isolate preferences—if the user accepts one but rejects another, the difference reveals a criterion.

```
"Here's a possible implementation. Would you accept this?"

[Show concrete code/behavior]

If rejected: "What specifically makes this unacceptable?"
→ Capture as criterion
```

Dimensions to consider varying (pick what's relevant):
- Structure (flat vs nested, modular vs monolithic)
- Style (verbose vs terse, explicit vs implicit)
- Abstraction level (high vs low)
- Error handling approach
- Naming conventions
- Any dimension relevant to the specific task

Example: If user accepts A (flat, verbose) and C (flat, terse) but rejects B (nested, terse), the issue is nesting—not style.

#### Contrast Pairs
Present alternatives with follow-up options:
```
"Which approach do you prefer?"

Option A: [approach]
Option B: [approach]

If they choose, follow up with concrete options:
"What makes that better for this case?"
- { label: "Simpler", description: "..." }
- { label: "More flexible", description: "..." }
- { label: "Matches existing patterns", description: "..." }
→ Capture reasoning as criterion
```

#### Pre-mortem Question
Ask: "Imagine this shipped and it was a disaster. What went wrong?"
- Capture risks mentioned
- Each risk becomes a preventive criterion
- If user struggles, offer common failure modes as options

#### Disappointed Question
Ask: "All criteria pass but you're disappointed. What would cause that?"
- Capture scenarios mentioned
- Each scenario becomes a criterion
- If user struggles, offer possible disappointments as options (e.g., "too slow?", "hard to extend?", "doesn't match team style?")

#### Persona Simulation
Ask: "If [respected developer/architect] reviewed this, what would they critique?"
- User identifies a persona
- If they struggle to generate critiques, offer common concerns that persona might have
- Capture critiques as criteria

#### Progressive Concreteness
For any vague criterion, offer concrete interpretations:
- Instead of "What does 'clean' mean?", offer: "Which matters most: readability, short functions, minimal dependencies, or consistent style?"
- Instead of "How would we verify 'good performance'?", offer: "What's acceptable: <100ms, <500ms, <1s, or just 'not noticeably slow'?"
- Refine until true/false verifiable
- Use numeric thresholds where applicable

### 2b. Latent Criteria Discovery

These techniques surface criteria users CAN'T articulate until forced to choose or react. They apply to ANY output type - code, research, docs, designs, analysis.

**The only question that matters**: Would violating this criterion cause the user to reject the output?

- **Yes** → Must capture it (obvious or latent)
- **No** → Don't need it

All techniques below exist to surface **hidden rejection criteria** - things the user would reject but wouldn't think to mention upfront.

**Proceed when:**
- You've asked: "What would cause you to reject this?" and captured the answers
- Latent techniques haven't revealed new rejection criteria in the last 2-3 questions
- User signals "I think we've covered it"

**Keep probing when:**
- Core deliverable is still ambiguous (guaranteed rejection)
- You haven't tested any latent techniques yet
- A technique just revealed a new rejection criterion - probe that area deeper
- You sense there's something important the user hasn't articulated

**Goal**: Surface hidden rejection criteria through substantive probing. The techniques below are examples—use whatever approaches reveal what the user would reject but wouldn't think to mention.

#### Tradeoff Forcing
Present competing values, force a choice. Works for ANY domain:

**Coding example:**
```
question: "When file size and conceptual completeness conflict, which wins?"
options:
- { label: "Smaller files", description: "Split to stay under ~200 lines" }
- { label: "Complete concepts", description: "Keep together even if larger" }
```

**Research example:**
```
question: "When depth and breadth conflict, which wins?"
options:
- { label: "Go deep", description: "Thoroughly explore fewer sources" }
- { label: "Go broad", description: "Survey more sources, less depth each" }
- { label: "Depends on topic", description: "Specify in Other" }
```

**Docs example:**
```
question: "When brevity and completeness conflict, which wins?"
options:
- { label: "Keep it short", description: "Readers can ask follow-ups" }
- { label: "Be thorough", description: "Cover edge cases upfront" }
```

Common tradeoffs to probe (examples—identify task-specific tradeoffs):
- Depth vs breadth (research, docs)
- Brevity vs completeness (docs, analysis)
- Speed vs rigor (any)
- Flexibility vs simplicity (code, design)
- Convention vs optimization (code)
- Comprehensive vs focused (research)
- (Task-specific: e.g., "backwards compat vs clean API", "user convenience vs security")

#### Extreme Aversion
Find which direction they'd rather err. Universally applicable:

**Coding:**
```
question: "Which extreme is WORSE?"
options:
- { label: "Over-abstracted", description: "Too many tiny pieces, hard to follow" }
- { label: "Under-abstracted", description: "Long, repetitive, but traceable" }
```

**Research:**
```
question: "Which extreme is WORSE?"
options:
- { label: "Over-hedged", description: "Too many caveats, unclear conclusions" }
- { label: "Over-confident", description: "Strong claims, may miss nuance" }
```

**Docs:**
```
question: "Which extreme is WORSE?"
options:
- { label: "Too technical", description: "Accurate but intimidating" }
- { label: "Too simplified", description: "Accessible but imprecise" }
```

#### Reaction Sampling
Generate concrete artifacts, ask for gut reaction. Show 2-3 examples varying in style:

**Coding:** Show error message styles, function signatures, code structure
**Research:** Show paragraph styles, citation density, conclusion strength
**Docs:** Show explanation approaches, example density, tone

```
"Here's a possible style for [artifact type]:"
> [concrete example]

question: "Your reaction?"
options:
- { label: "Accept as-is", description: "Matches what I want" }
- { label: "Too [X]", description: "Want less of this quality" }
- { label: "Not enough [Y]", description: "Want more of this quality" }
- { label: "Wrong approach", description: "Describe in Other" }
```

#### Boundary Mapping
Multi-select to map hard limits. Adapt to domain:

**Coding:**
```
question: "Which are HARD rejection criteria? (Select all)"
options:
- { label: "Functions > 50 lines", description: "No exceptions" }
- { label: "Missing error handling", description: "On any fallible op" }
- { label: "No tests for new code", description: "Coverage required" }
```

**Research:**
```
question: "Which are HARD rejection criteria? (Select all)"
options:
- { label: "No primary sources", description: "Must have direct evidence" }
- { label: "Missing key papers", description: "Seminal works required" }
- { label: "Unsupported claims", description: "Every claim needs citation" }
```

**Docs:**
```
question: "Which are HARD rejection criteria? (Select all)"
options:
- { label: "No working examples", description: "Must have runnable code" }
- { label: "Assumes expert knowledge", description: "Must define terms" }
- { label: "Missing troubleshooting", description: "Must cover common errors" }
```

#### Pattern Anchoring
Use existing artifacts as preference reference:

```
question: "Which existing [artifact] is closest to what you want?"
options:
- { label: "[Internal reference A]", description: "[Its key characteristics]" }
- { label: "[Internal reference B]", description: "[Its key characteristics]" }
- { label: "External reference", description: "Name it in Other" }
- { label: "Something new", description: "Describe in Other" }
```

Explore codebase/existing docs first to find anchors.

#### Conceptual Grouping Probe
For architecture, organization, or structure decisions:

**Coding:**
```
question: "Should auth and session management be in the SAME module?"
```

**Research:**
```
question: "Should methodology and results be in the SAME section?"
```

**Docs:**
```
question: "Should setup and configuration be in the SAME guide?"
```

Ask 3-5 grouping questions to map mental model. Skip if task has no structural decisions.

#### Spectrum Positioning
Find position on subjective dimensions. Pick 2-3 relevant spectrums (examples below—identify task-specific spectrums):

**Common spectrums:**
- Verbosity: minimal → moderate → explicit
- Formality: casual → professional → academic
- Detail: high-level → balanced → granular

**Domain-specific examples:**
- Code: abstraction level, type strictness, error handling
- Research: hedging, citation density, scope
- Docs: technical depth, example density, assumed knowledge
- (Task-specific: identify spectrums relevant to THIS task)

### 3. Question Format

ALWAYS use AskUserQuestion with:
- 2-4 options (never open-ended unless truly necessary)
- First option = recommended (with "(Recommended)" suffix)
- Descriptions explain tradeoffs
- Batch related questions (don't ask one at a time)
- Provide context for why you're asking (helps user give better answers)
- If user rejects ALL options, ask what's wrong with them—their objection is the criterion

When asking, briefly explain the purpose:
- "I'm asking about edge cases because these often surface implicit requirements..."
- "Rejection criteria help catch issues the LLM might otherwise miss..."
- "This pre-mortem question surfaces risks you might not think of directly..."

Example:
```
questions: [
  {
    question: "How should failures be handled?",
    header: "Failures",
    options: [
      { label: "Retry with backoff (Recommended)", description: "3 retries at 1s/2s/4s. Matches existing queue patterns." },
      { label: "Dead letter queue", description: "Store failed items for manual review. More complex." },
      { label: "Silent drop with logging", description: "Log and continue. Simple but items may be lost." }
    ],
    multiSelect: false
  }
]
```

### 4. Codebase Exploration

Explore AS NEEDED during interview, not upfront:
- When user mentions existing patterns → explore to find examples
- When discussing architecture → check current structure
- When gathering quality criteria → read CLAUDE.md, existing tests

Use findings to:
- Propose criteria based on existing patterns
- Show examples in adversarial questions
- Reference concrete code in options

### 5. Code Quality Gates (For Coding Tasks)

If the task involves writing or modifying code, ask which code quality categories should gate the work.

The categories below are common quality concerns with automated reviewers available. However, some tasks may have additional quality concerns not covered here (e.g., accessibility, security-specific checks, performance benchmarks). If you identify task-specific quality concerns during the interview, capture them as criteria with appropriate verification methods.

**Ask using AskUserQuestion:**

```
questions: [
  {
    question: "Which code quality categories should gate this work? Selected categories will be verified before completion.",
    header: "Quality gates",
    options: [
      { label: "Bugs", description: "Logic errors, race conditions, edge cases, error handling" },
      { label: "Type safety", description: "No any abuse, invalid states unrepresentable, proper narrowing" },
      { label: "Maintainability", description: "DRY, coupling, cohesion, dead code, consistency" },
      { label: "Simplicity", description: "No over-engineering, cognitive complexity, unnecessary abstraction" }
    ],
    multiSelect: true
  },
  {
    question: "More quality categories to verify:",
    header: "Quality gates (cont.)",
    options: [
      { label: "Test coverage", description: "New/changed code has adequate tests" },
      { label: "Testability", description: "Code is designed to be testable (low mock count)" },
      { label: "Documentation", description: "Docs and comments match code changes" },
      { label: "CLAUDE.md adherence", description: "Follows project-specific standards" }
    ],
    multiSelect: true
  }
]
```

**Map selections to criteria:**

For each selected category, add a criterion with sequential `AC-N` ID and `category: quality-gate`:

| Category | Reviewer Agent | Category Value |
|----------|---------------|----------------|
| Bugs | code-bugs-reviewer | quality-gate |
| Type safety | type-safety-reviewer | quality-gate |
| Maintainability | code-maintainability-reviewer | quality-gate |
| Simplicity | code-simplicity-reviewer | quality-gate |
| Test coverage | code-coverage-reviewer | quality-gate |
| Testability | code-testability-reviewer | quality-gate |
| Documentation | docs-reviewer | quality-gate |
| CLAUDE.md adherence | claude-md-adherence-reviewer | quality-gate |

Example (IDs continue from last AC-N in definition):

```yaml
- id: AC-15
  category: quality-gate
  description: "No HIGH or CRITICAL bugs introduced"
  verify:
    method: subagent
    agent: code-bugs-reviewer
    prompt: "Review for bugs. Pass if no HIGH or CRITICAL severity issues."

- id: AC-16
  category: quality-gate
  description: "Documentation matches code changes"
  verify:
    method: subagent
    agent: docs-reviewer
    prompt: "Check docs accuracy. Pass if no MEDIUM+ issues (docs caps at MEDIUM)."
```

Note: `agent` is the `subagent_type` for the Task tool. Use named agents (like `code-bugs-reviewer`) when available, or `general-purpose` for custom checks.

Write selections to interview log under `## Code Quality Gates`.

### 5b. Project Quality Gates (Auto-Detected)

For coding tasks, detect project-specific quality gates from CLAUDE.md. These are bash-verifiable commands the project defines—whatever the project requires, not a fixed set.

**Detection (no question needed):**

Read CLAUDE.md and look for verifiable commands. Common categories (but not limited to):

| Category | Common Patterns | Example Commands |
|----------|-----------------|------------------|
| Type checking | mypy, tsc, pyright | `mypy`, `tsc --noEmit` |
| Tests | pytest, jest, npm test | `pytest tests/ -v`, `npm test` |
| Linting | ruff, eslint, flake8 | `ruff check`, `npm run lint` |
| Formatting | black, prettier | `black --check`, `prettier --check` |
| Build | build, compile | `npm run build`, `cargo build` |

Projects may have other gates (e.g., `cargo clippy`, `go vet`, security scans, migration checks). Include whatever the project's CLAUDE.md specifies.

**If CLAUDE.md contains verifiable commands:**

Extract and add as criteria with sequential `AC-N` IDs and `category: project-gate`:

```yaml
# Examples - actual gates depend on what CLAUDE.md specifies
# IDs continue from last AC-N in definition
- id: AC-23
  category: project-gate
  description: "Type checking passes"
  verify:
    method: bash
    command: "[extracted command]"

- id: AC-24
  category: project-gate
  description: "Tests pass"
  verify:
    method: bash
    command: "[extracted command]"

- id: AC-25
  category: project-gate
  description: "Linting passes"
  verify:
    method: bash
    command: "[extracted command]"
```

**If no CLAUDE.md or no verifiable commands found:**

Don't invent gates. Only include what the project explicitly requires. Skip this section entirely if nothing is specified.

**Command formatting:**

- Use check-only variants for verification (e.g., `black --check` not `black`)
- Keep commands as close to CLAUDE.md as possible

Write detected gates to interview log under `## Project Quality Gates (Auto-Detected)`.

### 6. Write to Log (After Each Phase)

After each interview phase, write findings to `/tmp/define-interview-{timestamp}.md`:

All criteria use sequential `AC-N` numbering with a `category` field to track origin.

```markdown
## All Criteria (logged sequentially)
- [AC-1] category: feature | description: "..." | verify: method
- [AC-2] category: feature | description: "..." | verify: method
- [AC-3] category: rejection | description: "Will reject if..." | verify: method
- [AC-4] category: edge-case | scenario: "..." | handling: "..." | verify: method
- [AC-5] category: boundary | limit: "..." | verify: method
- [AC-6] category: quality-gate | agent: code-bugs-reviewer | prompt: "Pass if no HIGH+ bugs"
- [AC-7] category: project-gate | command: "npm test" | verify: bash
- ...

## Latent Criteria (from discovery techniques)

### Tradeoffs Documented
| Dimension | When conflicting, prefer | Rationale |
|-----------|-------------------------|-----------|
| [e.g., depth vs breadth] | [preference] | [user's reasoning] |
| [e.g., brevity vs completeness] | [preference] | [user's reasoning] |

### Boundaries (hard limits)
- [e.g., "No unsupported claims" for research]
- [e.g., "Functions max 50 lines" for code]
- [e.g., "Must have working examples" for docs]
- (none if no hard limits specified)

### Extreme Aversions
- More averse to: [extreme A] (prefer erring toward [extreme B])
- [e.g., "over-hedged" → prefer slightly bold over too cautious]

### Pattern References
- Primary reference: [existing artifact] ([key characteristics])
- Anti-reference: [artifact to avoid] ([why])

### Conceptual Groupings
- [concept A] + [concept B] → SAME/SEPARATE
- (capture user's mental model boundaries)
- (skip if no structural decisions in task)

### Spectrum Positions
- [e.g., Formality]: [position]
- [e.g., Detail level]: [position]
- [e.g., Technical depth]: [position]

### Reaction Samples
| Artifact shown | Reaction | Criterion captured |
|---------------|----------|-------------------|
| [concrete example] | [reaction] | [resulting criterion] |

## Adversarial Examples
### Accepted
- [code/behavior]

### Rejected
- [code/behavior] | reason: "..."

## Pre-mortem Risks
- Risk: "..." | Prevention: criterion AC-X

## Disappointed Scenarios
- Scenario: "..." | Prevention: criterion AC-X

## Code Quality Gates
(only for coding tasks; IDs continue from last AC-N)

Selected (with sequential AC-N IDs):
- [ ] Bugs (category: quality-gate, agent: code-bugs-reviewer)
- [ ] Type safety (category: quality-gate, agent: type-safety-reviewer)
- [ ] Maintainability (category: quality-gate, agent: code-maintainability-reviewer)
- [ ] Simplicity (category: quality-gate, agent: code-simplicity-reviewer)
- [ ] Test coverage (category: quality-gate, agent: code-coverage-reviewer)
- [ ] Testability (category: quality-gate, agent: code-testability-reviewer)
- [ ] Documentation (category: quality-gate, agent: docs-reviewer)
- [ ] CLAUDE.md adherence (category: quality-gate, agent: claude-md-adherence-reviewer)

## Project Quality Gates (Auto-Detected)
(only if CLAUDE.md specifies verifiable commands; IDs continue from last AC-N)

| AC-N | Category | Command | Source |
|------|----------|---------|--------|
| AC-N | project-gate | [command] | CLAUDE.md line X |

(include only gates found in CLAUDE.md; omit section if none)

## Open Questions
- (none if all resolved)
```

### 7. Write Final Definition

After refreshing context from the interview log, write `/tmp/define-{timestamp}.md`:

All criteria use sequential `AC-N` numbering. Categories are metadata via the `category` field.

```markdown
# Definition: [Task Description]

Generated: [date]
Interview Log: /tmp/define-interview-{timestamp}.md

## Overview
[1-2 sentences describing what this definition covers]

## Acceptance Criteria

All criteria use sequential AC-N numbering. The `category` field indicates the criterion type.

### Feature Behavior
- id: AC-1
  category: feature
  description: "..."
  verify:
    method: bash | subagent | manual
    [details]

- id: AC-2
  category: feature
  ...

### Rejection Conditions
- id: AC-3
  category: rejection
  description: "PR will be rejected if..."
  verify: ...

### Boundaries (Hard Limits)
- id: AC-4
  category: boundary
  limit: "[hard limit from interview]"
  verify: [method]

### Edge Cases
- id: AC-5
  category: edge-case
  scenario: "..."
  handling: "..."
  verify: ...

## Tradeoffs & Preferences
When criteria conflict, these preferences apply:

| Dimension | Preference | Context |
|-----------|------------|---------|
| [from interview] | [preference] | [when it applies] |

## Pattern References
- Follow: [reference artifact] ([key characteristics])
- Avoid: [anti-pattern] ([why])

## Examples

### Accepted
```[language]
[concrete code that would pass]
```
Passes criteria: AC-1, AC-3

### Rejected
```[language]
[concrete code that would fail]
```
Fails because: [specific reason linked to criterion]

## Pre-mortem Risks
| Risk | Preventive Criterion |
|------|---------------------|
| ... | AC-X |

## Disappointed Scenarios
| Scenario | Preventive Criterion |
|----------|---------------------|
| ... | AC-X |

## Code Quality Gates
(only present if coding task and user selected gates; IDs continue sequentially)

- id: AC-10
  category: quality-gate
  description: "No HIGH or CRITICAL bugs introduced"
  verify:
    method: subagent
    agent: code-bugs-reviewer
    prompt: "Review for bugs. Pass if no HIGH or CRITICAL severity issues."

- id: AC-11
  category: quality-gate
  description: "Documentation matches code changes"
  verify:
    method: subagent
    agent: docs-reviewer
    prompt: "Check docs accuracy. Pass if no MEDIUM+ issues."

[etc. for each selected gate]

## Project Quality Gates
(only present if CLAUDE.md specifies verifiable commands; IDs continue sequentially)

- id: AC-12
  category: project-gate
  description: "Type checking passes"
  verify:
    method: bash
    command: "[command from CLAUDE.md]"

- id: AC-13
  category: project-gate
  description: "Tests pass"
  verify:
    method: bash
    command: "[command from CLAUDE.md]"

[etc. - IDs continue sequentially]

## Task-Specific Verification

[Only if verification requires domain-specific checks that existing reviewers don't cover]

Use `general-purpose` agent with a custom prompt for ad-hoc verification:

```yaml
- id: AC-20
  category: custom
  description: "API response matches contract"
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read api-contract.yaml and check the implementation matches. Pass if all endpoints conform."
```

Or define a reusable subagent if the check is complex:

```yaml
### [agent-name]
Purpose: ...
Context Files: ...
Checks: [natural language description of what passes]
```

### 8. Complete

Output the definition file path:

```text
Definition complete: /tmp/define-{timestamp}.md

To do: /do /tmp/define-{timestamp}.md
```

## Resuming Interrupted Interview

If interview is interrupted, it can be resumed:

1. Check for existing log: `ls /tmp/define-interview-*.md`
2. Read the log to understand what's been covered
3. Update todos to mark completed phases
4. Continue from next incomplete phase

The log file preserves all gathered criteria, examples, and risks.

## Amendment Protocol

Definitions support amendments during execution if genuine gaps are discovered:

- Criteria have unique sequential IDs (AC-1, AC-2, AC-3, etc.)
- Amendments reference original: "AC-3.1 amends AC-3"
- Track amendments in definition with date and reason
- Format: `## Amendments\n- AC-3.1 (2026-01-17): [reason] - [new criterion]`

This allows /do to request definition changes when codebase reality conflicts with criteria.

## Critical Rules

1. **YOU drive the interview** - don't wait for user to think of everything
2. **Every criterion has verification** - no exceptions
3. **No vague terms** - "clean", "good", "proper" must be defined
4. **No placeholders** - no TBD, TODO, "figure out later"
5. **Examples are concrete** - actual code/artifacts, not descriptions
6. **Write to log before proceeding** - memento pattern mandatory
7. **Techniques are starting points** - ask whatever questions surface hidden criteria for THIS task
8. **Concrete choices > open-ended questions** - users reveal criteria by reacting to options
9. **Know when to stop** - if rejection criteria are clear, move on
10. **Invest in definition quality** - thorough upfront criteria discovery enables autonomous execution
