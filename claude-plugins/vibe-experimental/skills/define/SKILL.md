---
name: define
description: 'Verification-first requirements builder. Creates exhaustive definitions where every criterion has an explicit verification method. Use when starting new features, refactors, or any work requiring clear done criteria.'
user-invocable: true
---

# /define - Verification-First Requirements Builder

You are building a requirements definition using a verification-first approach. Every criterion you capture MUST have an explicit verification method (bash command, subagent check, or manual flag).

## Input

`$ARGUMENTS` = task description (what the user wants to build/change)

If no arguments provided, ask: "What would you like to build or change?"

## Output

Definition file: `/tmp/define-{timestamp}.md`

## Process

### 1. Initialize

Create todos and log file:

```
- [ ] Create log /tmp/define-interview-{timestamp}.md
- [ ] Gather positive criteria (feature, quality, architecture)
- [ ] Gather negative criteria (rejection conditions)
- [ ] Explore edge cases exhaustively
- [ ] Use adversarial examples (3+ varying on different dimensions)
- [ ] Use contrast pairs (alternative approaches)
- [ ] Ask pre-mortem question
- [ ] Ask disappointed question
- [ ] Ask persona simulation question
- [ ] Surface latent criteria (tradeoffs, boundaries, preferences)
- [ ] Refine vague criteria to specific
- [ ] (expand: areas as discovered)
- [ ] Refresh: read full interview log
- [ ] Run meta-verification via define-verifier agent
- [ ] Write final definition file
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
Generate 3+ synthetic implementations that VARY ON DIFFERENT DIMENSIONS:

| Example | Structure | Style | Abstraction |
|---------|-----------|-------|-------------|
| A | Flat | Verbose | High |
| B | Nested | Terse | High |
| C | Flat | Terse | Low |

```
"Here's a possible implementation. Would you accept this?"

[Show concrete code/behavior]

If rejected: "What specifically makes this unacceptable?"
→ Capture as criterion
```

Varying dimensions isolates preferences. If user accepts A and C but rejects B, the issue is nesting, not style.

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

### 2b. Latent Criteria Discovery

These techniques surface criteria users CAN'T articulate until forced to choose or react. Use ALL of these - they catch what standard interviewing misses.

#### Tradeoff Forcing
Present competing values, force a choice:
```
questions: [
  {
    question: "When these conflict, which wins?",
    header: "Tradeoff",
    options: [
      { label: "Smaller files", description: "Split concepts to stay under ~200 lines" },
      { label: "Complete concepts", description: "Keep related code together, even if larger" },
      { label: "Context-dependent", description: "I'll specify when each applies" }
    ],
    multiSelect: false
  }
]
```

Common tradeoffs to probe:
- File size vs conceptual completeness
- DRY vs explicit/readable
- Flexibility vs simplicity
- Performance vs maintainability
- Strict typing vs pragmatic any/unknown

#### Extreme Aversion
Find which direction they'd rather err:
```
questions: [
  {
    question: "Which extreme is WORSE?",
    header: "Preference",
    options: [
      { label: "Over-abstracted", description: "Too many tiny functions, hard to follow flow" },
      { label: "Under-abstracted", description: "Long functions, repeated patterns" }
    ],
    multiSelect: false
  }
]
```

Reveals implicit preferences when both extremes technically meet criteria.

#### Reaction Sampling
Generate concrete artifacts, ask for gut reaction:
```
"Here's a possible error message style:"
> Error E4012: Connection failed at localhost:5432. Verify database configuration.

questions: [
  {
    question: "Your reaction to this style?",
    header: "Style",
    options: [
      { label: "Accept as-is", description: "This matches what I want" },
      { label: "Too formal/verbose", description: "Want friendlier or shorter" },
      { label: "Too terse", description: "Need more detail or guidance" },
      { label: "Wrong format entirely", description: "Will describe in Other" }
    ],
    multiSelect: false
  }
]
```

Show 2-3 concrete examples varying in style/structure. Reactions reveal preferences that "good error messages" doesn't capture.

#### Boundary Mapping
Multi-select to map rejection boundaries explicitly:
```
questions: [
  {
    question: "Which would cause you to REJECT a PR? (Select all that apply)",
    header: "Boundaries",
    options: [
      { label: "Functions > 50 lines", description: "Without exception" },
      { label: "Files > 400 lines", description: "Without exception" },
      { label: "More than 3 nesting levels", description: "Complexity limit" },
      { label: "Missing error handling", description: "On any fallible operation" }
    ],
    multiSelect: true
  }
]
```

Creates explicit numeric/structural boundaries.

#### Pattern Anchoring
Use existing code as preference reference:
```
questions: [
  {
    question: "Which existing code is closest to what you want here?",
    header: "Reference",
    options: [
      { label: "Like src/auth/", description: "Layered, explicit, heavily typed" },
      { label: "Like src/utils/", description: "Flat, minimal, pragmatic" },
      { label: "Like [external project]", description: "Name it in Other" },
      { label: "Something new", description: "Describe in Other" }
    ],
    multiSelect: false
  }
]
```

Explore codebase first to find pattern anchors. External references (React, Django, etc.) also work.

#### Conceptual Grouping Probe
For architecture/refactoring, test mental model boundaries:
```
questions: [
  {
    question: "Should auth and session management be in the SAME module?",
    header: "Grouping",
    options: [
      { label: "Yes, same module", description: "They're conceptually unified" },
      { label: "No, separate", description: "Distinct responsibilities" },
      { label: "Depends on size", description: "Specify threshold in Other" }
    ],
    multiSelect: false
  }
]
```

Ask 3-5 grouping questions to map the user's conceptual topology. Different people draw different boundaries.

#### Spectrum Positioning
For subjective dimensions, find where they sit:
```
questions: [
  {
    question: "Where on the verbosity spectrum?",
    header: "Verbosity",
    options: [
      { label: "Minimal", description: "Terse names, few comments, implicit" },
      { label: "Moderate", description: "Clear names, comments on non-obvious" },
      { label: "Explicit", description: "Verbose names, thorough JSDoc, defensive" }
    ],
    multiSelect: false
  }
]
```

Use for: verbosity, abstraction level, error handling strictness, test coverage depth.

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

After each interview phase, write findings to `/tmp/define-interview-{timestamp}.md`:

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

## Latent Criteria (from discovery techniques)

### Tradeoffs Documented
| Dimension | When conflicting, prefer | Rationale |
|-----------|-------------------------|-----------|
| File size vs concepts | Complete concepts | "I can scroll, but split concepts confuse me" |
| DRY vs explicit | Explicit | "Hate hunting for abstractions" |

### Boundaries (hard limits)
- Functions: max 50 lines
- Files: max 400 lines
- Nesting: max 3 levels
- (none if no hard limits specified)

### Extreme Aversions
- More averse to: over-abstraction (prefer slightly long over too fragmented)
- More averse to: verbose errors (prefer terse)

### Pattern References
- Primary reference: src/auth/ (layered, explicit style)
- Anti-reference: src/legacy/ (avoid this style)

### Conceptual Groupings
- auth + sessions → SAME module
- validation + schemas → SEPARATE modules
- (capture user's mental model boundaries)

### Spectrum Positions
- Verbosity: moderate
- Error handling: strict
- Test coverage: thorough

### Reaction Samples
| Artifact shown | Reaction | Criterion captured |
|---------------|----------|-------------------|
| Error msg style A | "Too robotic" | AC-12: errors use friendly tone |
| Code structure B | "Accepted" | (validates existing criteria) |

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

Before finalizing, spawn define-verifier agent:

```
Use the Task tool to verify the definition:
Task("vibe-experimental", "define-verifier", read the interview log at /tmp/define-interview-{timestamp}.md and verify all acceptance criteria are met)
```

The define-verifier checks:
- All interview techniques used
- All criteria have verification methods
- No vague terms remain
- Examples are concrete
- Pre-mortem and disappointed documented
- No conflicts between criteria

If gaps found → continue interview to fill them.

### 7. Write Final Definition

Only after meta-verification passes, write `/tmp/define-{timestamp}.md`:

```markdown
# Definition: [Task Description]

Generated: [date]
Interview Log: /tmp/define-interview-{timestamp}.md

## Overview
[1-2 sentences describing what this definition covers]

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

## Tradeoffs & Preferences
When criteria conflict, these preferences apply:

| Dimension | Preference | Context |
|-----------|------------|---------|
| File size vs concepts | Prefer complete concepts | Can exceed 200 lines if keeps concept unified |
| DRY vs explicit | Prefer explicit | Repetition OK if improves readability |

## Boundaries (Hard Limits)
- id: B-1
  limit: "Functions must be ≤50 lines"
  verify: bash | `find . -name "*.ts" -exec awk '/^(export )?(async )?function/{start=NR} /^}$/{if(NR-start>50) print FILENAME":"start}' {} \;`

## Pattern References
- Follow: src/auth/ (layered, explicit, typed)
- Avoid: src/legacy/ (implicit, untyped patterns)

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

Output the definition file path:
```
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

- Criteria have unique IDs (AC-1, R-1, E-1) for reference
- Amendments reference original: "AC-3.1 amends AC-3"
- Track amendments in definition with date and reason
- Format: `## Amendments\n- AC-3.1 (2026-01-17): [reason] - [new criterion]`

This allows /do to request definition changes when codebase reality conflicts with criteria.

## Critical Rules

1. **YOU drive the interview** - don't wait for user to think of everything
2. **Every criterion has verification** - no exceptions
3. **No vague terms** - "clean", "good", "proper" must be defined
4. **No placeholders** - no TBD, TODO, "figure out later"
5. **Examples are concrete** - actual code, not descriptions
6. **Meta-verification before finalize** - definition not done until it passes
7. **Write to log before proceeding** - memento pattern mandatory
8. **Surface latent criteria** - use ALL latent discovery techniques (tradeoffs, boundaries, reactions, etc.)
9. **Vary adversarial examples on multiple dimensions** - don't just show 2 similar alternatives
