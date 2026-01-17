---
name: spec
description: 'Verification-first requirements builder. Creates exhaustive specs where every criterion has an explicit verification method. Use when starting new features, refactors, or any work requiring clear done criteria.'
user-invocable: true
---

# /spec - Verification-First Requirements Builder

You are building a requirements spec using a verification-first approach. Every criterion you capture MUST have an explicit verification method (bash command, subagent check, or manual flag).

## Input

`$ARGUMENTS` = task description (what the user wants to build/change)

If no arguments provided, ask: "What would you like to build or change?"

## Output

Spec file: `/tmp/spec-{timestamp}.md`

## Process

### 1. Initialize

Create todos and log file:

```
- [ ] Create log /tmp/spec-interview-{timestamp}.md
- [ ] Gather positive criteria (feature, quality, architecture)
- [ ] Gather negative criteria (rejection conditions)
- [ ] Explore edge cases exhaustively
- [ ] Use adversarial examples (2+ synthetic implementations)
- [ ] Use contrast pairs (alternative approaches)
- [ ] Ask pre-mortem question
- [ ] Ask disappointed question
- [ ] Ask persona simulation question
- [ ] Refine vague criteria to specific
- [ ] (expand: areas as discovered)
- [ ] Refresh: read full interview log
- [ ] Run meta-verification via spec-verifier agent
- [ ] Write final spec file
```

### 2. Proactive LLM-Driven Interview

YOU drive the interview. Don't wait for the user to volunteer everything. Surface questions they wouldn't think to ask.

**Interview Techniques (use ALL):**

#### Positive Criteria
Ask about:
- Feature behavior: "What should happen when X?"
- Quality standards: "What code quality expectations apply?"
- Architecture: "Where should this live in the codebase?"
- Integration: "What existing systems does this touch?"

#### Negative Criteria (Rejection-First)
Ask explicitly: "What would cause you to REJECT a PR for this work?"
- Capture at least 3 rejection criteria
- These are distinct from inverted positive criteria

#### Edge Cases (Exhaustive)
Walk through systematically:
- Empty input / null values
- Large input / scale limits
- Concurrent access / race conditions
- Failure modes / error handling
- Continue until user says "I think we covered it"

#### Adversarial Examples
Generate 2+ synthetic implementations:
```
"Here's a possible implementation. Would you accept this?"

[Show concrete code/behavior]

If rejected: "What specifically makes this unacceptable?"
→ Capture as criterion
```

#### Contrast Pairs
Present alternatives:
```
"Which approach do you prefer?"

Option A: [approach]
Option B: [approach]

"Why?" → Capture reasoning as criterion
```

#### Pre-mortem Question
Ask: "Imagine this shipped and it was a disaster. What went wrong?"
- Capture at least 2 risks
- Each risk becomes a preventive criterion

#### Disappointed Question
Ask: "All criteria pass but you're disappointed. What would cause that?"
- Repeat until user can't think of more
- Each scenario becomes a criterion

#### Persona Simulation
Ask: "If [respected developer/architect] reviewed this, what would they critique?"
- User identifies a persona
- Capture critiques as criteria

#### Progressive Concreteness
For any vague criterion:
- "What does 'clean' mean specifically?"
- "How would we verify 'good performance'?"
- Refine until true/false verifiable
- Use numeric thresholds where applicable

### 3. Question Format

ALWAYS use AskUserQuestion with:
- 2-4 options (never open-ended unless truly necessary)
- First option = recommended (with "(Recommended)" suffix)
- Descriptions explain tradeoffs
- Batch related questions (don't ask one at a time)
- Provide context for why you're asking (helps user give better answers)

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

### 5. Write to Log (After Each Phase)

After each interview phase, write findings to `/tmp/spec-interview-{timestamp}.md`:

```markdown
## Positive Criteria
- [AC-1] description: "..." | verify: method
- [AC-2] ...

## Negative Criteria (Rejection)
- [R-1] "Will reject if..."
- [R-2] ...

## Edge Cases
- [E-1] scenario: "..." | handling: "..." | verify: method
- ...

## Adversarial Examples
### Accepted
- [code/behavior]

### Rejected
- [code/behavior] | reason: "..."

## Pre-mortem Risks
- Risk: "..." | Prevention: criterion AC-X

## Disappointed Scenarios
- Scenario: "..." | Prevention: criterion AC-X

## Open Questions
- (none if all resolved)
```

### 6. Meta-Verification

Before finalizing, spawn spec-verifier agent:

```
Use the Task tool to verify the spec:
Task("vibe-experimental", "spec-verifier", read the interview log at /tmp/spec-interview-{timestamp}.md and verify all acceptance criteria are met)
```

The spec-verifier checks:
- All interview techniques used
- All criteria have verification methods
- No vague terms remain
- Examples are concrete
- Pre-mortem and disappointed documented
- No conflicts between criteria

If gaps found → continue interview to fill them.

### 7. Write Final Spec

Only after meta-verification passes, write `/tmp/spec-{timestamp}.md`:

```markdown
# Spec: [Task Description]

Generated: [date]
Interview Log: /tmp/spec-interview-{timestamp}.md

## Overview
[1-2 sentences describing what this spec covers]

## Acceptance Criteria

### Feature Behavior
- id: AC-1
  description: "..."
  verify:
    method: bash | subagent | manual
    [details]

### Code Quality
- id: AC-2
  ...

### Architecture
- id: AC-3
  ...

## Rejection Criteria
- id: R-1
  description: "PR will be rejected if..."
  verify: ...

## Edge Cases
- id: E-1
  scenario: "..."
  handling: "..."
  verify: ...

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

## Task-Specific Subagents
[Only if generic verification isn't sufficient]

### [agent-name]
Purpose: ...
Context Files: ...
Checks:
- "..."
- "..."
```

### 8. Complete

Output the spec file path:
```
Spec complete: /tmp/spec-{timestamp}.md

To implement: /implement /tmp/spec-{timestamp}.md
```

## Resuming Interrupted Interview

If interview is interrupted, it can be resumed:

1. Check for existing log: `ls /tmp/spec-interview-*.md`
2. Read the log to understand what's been covered
3. Update todos to mark completed phases
4. Continue from next incomplete phase

The log file preserves all gathered criteria, examples, and risks.

## Amendment Protocol

Specs support amendments during implementation if genuine gaps are discovered:

- Criteria have unique IDs (AC-1, R-1, E-1) for reference
- Amendments reference original: "AC-3.1 amends AC-3"
- Track amendments in spec with date and reason
- Format: `## Amendments\n- AC-3.1 (2026-01-17): [reason] - [new criterion]`

This allows /implement to request spec changes when codebase reality conflicts with criteria.

## Critical Rules

1. **YOU drive the interview** - don't wait for user to think of everything
2. **Every criterion has verification** - no exceptions
3. **No vague terms** - "clean", "good", "proper" must be defined
4. **No placeholders** - no TBD, TODO, "figure out later"
5. **Examples are concrete** - actual code, not descriptions
6. **Meta-verification before finalize** - spec not done until it passes
7. **Write to log before proceeding** - memento pattern mandatory
