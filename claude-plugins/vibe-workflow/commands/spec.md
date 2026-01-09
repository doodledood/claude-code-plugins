---
description: 'Builds requirements specification through structured discovery interview. Use when defining scope, gathering requirements, or specifying WHAT any work should accomplish - features, bugs, refactors, infrastructure, migrations, performance, documentation, or any other work type.'
argument-hint: Optional - work name or topic
---

**User request**: $ARGUMENTS

Build requirements spec through structured discovery interview. Defines WHAT and WHY - not technical implementation (architecture, APIs, data models come in planning phase).

**Loop**: Research → Expand todos → Ask questions → Write findings → Repeat until complete

**Role**: Senior Product Manager - smart, non-obvious questions that reduce ambiguity and cognitive load.

**Spec file**: `/tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - updated after each iteration.

**Interview log**: `/tmp/spec-interview-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - external memory.

**Timestamp**: Generate once at Phase 1 start. Use same timestamp for both files. Running /spec again creates new files (no overwrite).

## Phase 1: Initial Setup

### 1.1 Create todo list (TodoWrite immediately)

Todos = **areas to discover**, not interview steps. Each todo reminds you what conceptual area needs resolution. List continuously expands as user answers reveal new areas. "Finalize spec" is fixed anchor; all others are dynamic.

**Starter todos** (just seeds - actual list grows organically):

```
- [ ] Initial context research
- [ ] Scope & target users
- [ ] Core requirements
- [ ] (expand continuously as answers reveal new areas)
- [ ] Finalize spec
```

### Todo Evolution Example

Query: "Add user notifications feature"

Initial:
```
- [ ] Initial context research
- [ ] Scope & target users
- [ ] Core requirements
- [ ] Finalize spec
```

After user says "needs to work across mobile and web":
```
- [x] Initial context research → found existing notification system for admin alerts
- [ ] Scope & target users
- [ ] Core requirements
- [ ] Mobile notification delivery (push vs in-app)
- [ ] Web notification delivery (browser vs in-app)
- [ ] Cross-platform sync behavior
- [ ] Finalize spec
```

After user mentions "also needs email digest option":
```
- [x] Initial context research
- [x] Scope & target users → all active users, v1 MVP
- [ ] Core requirements
- [x] Mobile notification delivery → push + in-app
- [ ] Web notification delivery
- [ ] Cross-platform sync behavior
- [ ] Email digest frequency options
- [ ] Email vs real-time preferences
- [ ] Finalize spec
```

**Key**: Todos grow as user reveals complexity. Never prune prematurely.

### 1.2 Create interview log

Path: `/tmp/spec-interview-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` (use SAME path for ALL updates)

```markdown
# Interview Log: {work name}
Started: {timestamp}

## Research Phase
(populated incrementally)

## Interview Rounds
(populated incrementally)

## Decisions Made
(populated incrementally)

## Unresolved Items
(populated incrementally)
```

## Phase 2: Initial Context Gathering

### 2.1 Launch codebase-explorer

Use Task tool with `subagent_type: "vibe-workflow:codebase-explorer"` to understand context. Launch multiple in parallel (single message) for cross-cutting work. Max 3 parallel researchers; if findings conflict, note both perspectives and ask user to resolve.

Explore: product purpose, existing patterns, user flows, terminology, product docs (CUSTOMER.md, SPEC.md, PRD.md, BRAND_GUIDELINES.md, DESIGN_GUIDELINES.md, README.md), existing specs in `docs/` or `specs/`. For bug fixes: also explore bug context, related code, potential causes.

### 2.2 Read recommended files

Read ALL files from researcher prioritized reading lists - no skipping.

### 2.3 Launch web-researcher (if needed)

Use Task tool with `subagent_type: "vibe-workflow:web-researcher"` for knowledge gaps: domain concepts, user expectations, industry standards, compliance requirements, competitor approaches (UX perspective). Returns all findings in response - no additional file reads needed. Continue launching throughout interview as gaps emerge.

### 2.4 Update interview log

After EACH research step, append to interview log:

```markdown
### {timestamp} - {what researched}
- Explored: {areas/topics}
- Key findings: {list}
- New areas identified: {list}
- Questions to ask: {list}
```

### 2.5 Write initial draft

Write first draft with `[TBD]` markers for unresolved items. Use same file path for all updates.

### Phase 2 Complete When
- All codebase-explorer tasks finished
- All recommended files read
- Initial draft written with `[TBD]` markers
- Interview log populated with research findings

## Phase 3: Iterative Discovery Interview

**CRITICAL**: Use AskUserQuestion tool for ALL questions - never plain text.

**Example AskUserQuestion call**:
```
questions: [{
  question: "Who should receive these notifications?",
  header: "User Scope",
  options: [
    { label: "All active users (Recommended)", description: "Broadest reach, simplest logic" },
    { label: "Premium users only", description: "Limited scope, may need upgrade prompts" },
    { label: "Users who opted in", description: "Requires preference system first" }
  ],
  multiSelect: false
}]
```

### Memento Loop

For each step:
1. Mark todo `in_progress`
2. Research OR ask question (AskUserQuestion)
3. **Write findings immediately** to interview log
4. Expand todos for: new areas revealed, follow-up questions, dependencies discovered
5. Update spec file (replace `[TBD]` markers)
6. Mark todo `completed`
7. Repeat until no pending todos

**NEVER proceed without writing findings first** — interview log is external memory.

### Interview Log Update Format

After EACH question/answer, append (Round = one AskUserQuestion call, may contain batched questions):

```markdown
### Round {N} - {timestamp}
**Todo**: {which todo this addresses}
**Question asked**: {question}
**User answer**: {answer}
**Impact**: {what this revealed/decided}
**New areas**: {list or "none"}
```

After EACH decision (even implicit), append to Decisions Made:

```markdown
- {Decision area}: {choice} — {rationale}
```

### Todo Expansion Triggers

| Discovery Reveals | Add Todos For |
|-------------------|---------------|
| New affected area | Requirements for that area |
| Integration need | Integration constraints |
| Compliance/regulatory | Compliance requirements |
| Multiple scenarios/flows | Each scenario's behavior |
| Error conditions | Error handling approach |
| Performance concern | Performance constraints/metrics |
| Existing dependency | Dependency investigation |
| Rollback/recovery need | Recovery strategy |
| Data preservation need | Data integrity requirements |

### Interview Rules

**Unbounded loop**: Keep iterating (research → question → update spec) until ALL completion criteria are met. No fixed round limit.

1. **Prioritize by information gain** - Ask questions where the answer would change what other questions you need to ask, or would eliminate entire branches of requirements. If knowing X makes Y irrelevant, ask X first.

2. **Interleave discovery and questions**:
   - User answer reveals new area → launch codebase-explorer
   - Need domain knowledge → launch web-researcher
   - Update spec after each iteration, replacing `[TBD]` markers

3. **Question priority order**:

   | Priority | Type | Purpose | Examples |
   |----------|------|---------|----------|
   | 1 | Scope Eliminators | Eliminate large chunks of work | V1/MVP vs full? All users or segment? |
   | 2 | Branching | Open/close inquiry lines | User-initiated or system-triggered? Real-time or async? |
   | 3 | Hard Constraints | Non-negotiable limits | Regulatory requirements? Must integrate with X? |
   | 4 | Differentiating | Choose between approaches | Pattern A vs B? Which UX model? |
   | 5 | Detail Refinement | Fine-grained details | Exact copy, specific error handling |

4. **Always mark one option "(Recommended)"** - put first with reasoning in description. Question whether each requirement is truly needed—don't pad with nice-to-haves. When options are equivalent AND easily reversible, decide yourself (lean simpler). When options are equivalent BUT have different user-facing tradeoffs, ask user.

5. **Be thorough via technique**:
   - Cover everything relevant - don't skip to save time
   - Reduce cognitive load through HOW you ask: concrete options, good defaults
   - **Batching**: Up to 4 related questions per AskUserQuestion call; max 6-8 options per question
   - Make decisions yourself when context suffices
   - Complete spec with easy questions > incomplete spec with fewer questions

6. **Ask non-obvious questions** - User motivations, edge cases affecting UX, business rules, user expectations vs delivery, tradeoffs

7. **Ask vs Decide** - User is authority for business decisions; codebase/standards are authority for implementation details.

   **Ask user when**:
   | Category | Examples |
   |----------|----------|
   | Business rules | Pricing logic, eligibility criteria, approval thresholds |
   | User segments | Who gets this? All users, premium, specific roles? |
   | Tradeoffs with no winner | Speed vs completeness, flexibility vs simplicity |
   | Scope boundaries | V1 vs future, must-have vs nice-to-have |
   | External constraints | Compliance, contracts, stakeholder requirements |
   | Preferences | Opt-in vs opt-out, default on vs off |

   **Decide yourself when**:
   | Category | Examples |
   |----------|----------|
   | Existing pattern | Error format, naming conventions, component structure |
   | Industry standard | HTTP status codes, validation rules, retry strategies |
   | Sensible defaults | Timeout values, pagination limits, debounce timing |
   | Easily changed later | Copy text, colors, specific thresholds |
   | Implementation detail | Which hook to use, event naming, internal state shape |

   **Test**: "If I picked wrong, would user say 'that's not what I meant' (ASK) or 'that works, I would have done similar' (DECIDE)?"

## Phase 4: Finalize & Summarize

### 4.1 Final interview log update

```markdown
## Interview Complete
Finished: {timestamp} | Questions: {count} | Decisions: {count}
## Summary
{Brief summary of discovery process}
```

### 4.2 Finalize specification

Final pass: remove `[TBD]` markers, ensure consistency. Use this **minimal scaffolding** - add sections dynamically based on what discovery revealed:

```markdown
# Requirements: {Work Name}

Generated: {date}

## Overview
### Problem Statement
{What is wrong/missing/needed? Why now?}

### Scope
{What's included? What's explicitly excluded?}

### Affected Areas
{Systems, components, processes, users impacted}

### Success Criteria
{Observable outcomes that prove this work succeeded}

## Requirements
{Verifiable statements about what's true when this work is complete. Each requirement should be specific enough to check as true/false.}

### Core Behavior
- {Verifiable outcome}
- {Another verifiable outcome}

### Edge Cases & Error Handling
- When {condition}, {what happens}

## Constraints
{Non-negotiable limits, dependencies, prerequisites}

## Out of Scope
{Non-goals with reasons}

## {Additional sections as needed based on discovery}
{Add sections relevant to this specific work - examples below}
```

**Dynamic sections** - add based on what discovery revealed (illustrative, not exhaustive):

| Discovery Reveals | Add Section |
|-------------------|-------------|
| User-facing behavior | Screens/states (empty, loading, success, error), interactions, accessibility |
| API/technical interface | Contract (inputs/outputs/errors), integration points, versioning |
| Bug context | Current vs expected, reproduction steps, verification criteria |
| Refactoring | Current/target structure, invariants (what must NOT change) |
| Infrastructure | Rollback plan, monitoring, failure modes |
| Migration | Data preservation, rollback, cutover strategy |
| Performance | Current baseline, target metrics, measurement method |
| Data changes | Schema, validation rules, retention |
| Security & privacy | Auth/authz requirements, data sensitivity, audit needs |
| User preferences | Configurable options, defaults, persistence |
| External integrations | Third-party services, rate limits, fallbacks |
| Observability | Analytics events, logging, success/error metrics |

**Specificity**: Each requirement should be verifiable. "User can log in" is too vague; "on valid credentials → redirect to dashboard; on invalid → show inline error, no page reload" is right.

### 4.3 Mark all todos complete

### 4.4 Output summary

```
## Spec Summary

**Work**: {name}
**File**: /tmp/spec-{...}.md

### What We're Doing
{1-2 sentences}

### Key Decisions Made
- {Decision}: {choice}

### Core Requirements ({count})
- {Top 3 requirements}

### Out of Scope
- {Key non-goals}

---
Review full spec and let me know adjustments.
```

## Key Principles

| Principle | Rule |
|-----------|------|
| Memento style | Write findings BEFORE next question (interview log = external memory) |
| Todo-driven | Every discovery needing follow-up → todo (no mental notes) |
| WHAT not HOW | Requirements only - no architecture, APIs, data models, code patterns. Self-check: if thinking "how to implement," refocus on "what should happen/change" |
| Observable outcomes | Focus on what changes when complete. Ask "what is different after?" not "how does it work internally?" Edge cases = system/business impact |
| Dynamic structure | Spec sections emerge from discovery. No fixed template beyond core scaffolding. Add sections as needed to fully specify the WHAT |
| Complete coverage | Spec covers EVERYTHING implementer needs: behavior, UX, data, errors, edge cases, accessibility - whatever the work touches. If they'd have to guess, it's underspecified |
| Define much, ask smart | Spec is comprehensive. Ask all questions needed for important decisions, but don't ask what you can infer or research. Every question should matter - no fluff, no redundancy |
| No open questions | Resolve everything during interview - no TBDs in final spec |
| Question requirements | Don't accept requirements at face value. Ask "is this truly needed for v1?" Don't pad specs with nice-to-haves |
| Reduce cognitive load | Recommended option first, multi-choice over free-text. Free-text only when: options are infinite/unpredictable, asking for specific values (names, numbers), or user needs to describe own context. User accepting defaults should yield solid result |
| Incremental updates | Update interview log after EACH step (not at end) |

### Completion Checklist

Interview complete when ALL true (keep iterating until every box checked):
- [ ] Problem/trigger defined - why this work is needed
- [ ] Scope defined - what's in, what's explicitly out
- [ ] Affected areas identified - what changes
- [ ] Success criteria specified - observable outcomes
- [ ] Core requirements documented (3+)
- [ ] Edge cases addressed
- [ ] Constraints captured
- [ ] Out of scope listed with reasons
- [ ] No `[TBD]` markers remain
- [ ] Passes completeness test (below)

### Completeness Test (before finalizing)

Simulate three consumers of this spec:

1. **Implementer**: Read each requirement. Could you code it without guessing? If you'd think "I'll ask about X later" → X is underspecified.

2. **Tester**: For each behavior, can you write a test? If inputs/outputs/conditions are unclear → underspecified.

3. **Reviewer**: For each success criterion, how would you verify it shipped correctly? If verification method is unclear → underspecified.

Any question from these simulations = gap to address before finalizing.

### Never Do

- Proceed without writing findings to interview log
- Keep discoveries as mental notes instead of todos
- Skip todo list
- Write specs to project directories (always `/tmp/`)
- Ask about technical implementation
- Finalize with unresolved `[TBD]`
- Skip summary output
- Ask questions without AskUserQuestion tool
- Proceed past Phase 2 without initial draft
- Forget to expand todos on new areas revealed

### Edge Cases

| Scenario | Action |
|----------|--------|
| User declines to answer | Note `[USER SKIPPED: reason]`, flag in summary |
| Insufficient research | Ask user directly, note uncertainty |
| Contradictory requirements | Surface conflict before proceeding |
| User corrects earlier decision | Update spec, log correction with reason, check if other requirements affected |
| Interview interrupted | Spec saved; add `[INCOMPLETE]` at top. To resume: provide existing spec file path as argument |
| "Just build it" | Push back with 2-3 critical questions (questions where guessing wrong = significant rework). If declined, document assumptions clearly |
