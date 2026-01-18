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
Ask explicitly: "What would cause you to REJECT this output?"
- Capture ALL rejection criteria the user mentions
- These are the most important criteria - everything else is optional
- Keep probing until user can't think of more

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

| Task Type | Priority Techniques |
|-----------|---------------------|
| Code/refactor | Tradeoffs, boundaries, pattern anchoring, conceptual grouping |
| Research/analysis | Tradeoffs, depth spectrum, reaction sampling |
| Documentation | Audience spectrum, reaction sampling, tradeoffs |
| Design/architecture | Conceptual grouping, tradeoffs, extreme aversion |

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

Common tradeoffs to probe (pick relevant ones):
- Depth vs breadth (research, docs)
- Brevity vs completeness (docs, analysis)
- Speed vs rigor (any)
- Flexibility vs simplicity (code, design)
- Convention vs optimization (code)
- Comprehensive vs focused (research)

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
Find position on subjective dimensions. Pick 2-3 relevant spectrums:

**Universal spectrums:**
- Verbosity: minimal → moderate → explicit
- Formality: casual → professional → academic
- Detail: high-level → balanced → granular

**Domain-specific:**
- Code: abstraction level, type strictness, error handling
- Research: hedging, citation density, scope
- Docs: technical depth, example density, assumed knowledge

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

## Open Questions
- (none if all resolved)
```

### 6. Meta-Verification

Before finalizing, spawn define-verifier agent:

```
Use the Task tool to verify the definition:
Task("vibe-experimental", "define-verifier", read the interview log at /tmp/define-interview-{timestamp}.md and verify all acceptance criteria are met)
```

The define-verifier checks the three requirements:
1. Core deliverable is clear (ambiguity = guaranteed rejection)
2. Rejection criteria captured (explicit + latent techniques used)
3. Each rejection criterion has a verification method

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
| [from interview] | [preference] | [when it applies] |

## Boundaries (Hard Limits)
- id: B-1
  limit: "[hard limit from interview]"
  verify: [method]

## Pattern References
- Follow: [reference artifact] ([key characteristics])
- Avoid: [anti-pattern] ([why])

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
5. **Examples are concrete** - actual code/artifacts, not descriptions
6. **Meta-verification before finalize** - definition not done until it passes
7. **Write to log before proceeding** - memento pattern mandatory
8. **Surface latent criteria thoroughly** - use all techniques relevant to task type until diminishing returns
9. **Vary adversarial examples on multiple dimensions** - don't just show 2 similar alternatives
10. **Invest in definition quality** - thorough upfront criteria discovery enables autonomous execution
