---
description: 'Builds requirements specification through structured discovery interview. Use when defining scope, gathering requirements, specifying what a feature should do, or creating a spec for features, bugs, docs, or refactors.'
argument-hint: Optional - work name or topic
---

**User request**: $ARGUMENTS

# Spec Skill

Build requirements spec through structured discovery interview. Defines WHAT and WHY - not technical implementation (architecture, APIs, data models come in planning phase).

**Loop**: Research → Expand todos → Ask questions → Write findings → Repeat until complete

**Role**: Senior PM - smart, non-obvious questions that reduce ambiguity and cognitive load.

**Spec file**: `/tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - updated after each iteration.

**Interview log**: `/tmp/spec-interview-{name-kebab-case}-{YYYYMMDD-HHMMSS}.md` - external memory.

## Phase 1: Initial Setup

### 1.1 Create todo list (TodoWrite immediately)

Todos = **areas to discover**, not interview steps. Each todo reminds you what conceptual area needs resolution. List is **never fixed** - continuously expands as user answers reveal new areas.

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

Path: `/tmp/spec-interview-{name-kebab-case}-{YYYYMMDD-HHMMSS}.md` (use SAME path for ALL updates)

```markdown
# Interview Log: {work name}
Started: {timestamp} | Type: {Feature | Bug Fix | Doc Update | Refactor}

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

Use Task tool with `subagent_type: "vibe-workflow:codebase-explorer"` to understand context. Launch multiple in parallel (single message) for cross-cutting work.

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

## Phase 3: Iterative Discovery Interview

**CRITICAL**: Use AskUserQuestion tool for ALL questions - never plain text.

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

After EACH question/answer, append:

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

| User Answer Reveals | Add Todos For |
|---------------------|---------------|
| New user segment | Target user requirements |
| Integration need | Integration constraints |
| Compliance/regulatory | Compliance requirements |
| Multiple flows | Each flow's UX |
| Error scenarios | Error handling approach |
| Performance concern | Performance constraints |
| Existing feature dependency | Dependency investigation |

### Interview Rules

**Unbounded loop**: Keep iterating (research → question → update spec) until ALL completion criteria are met. No fixed round limit.

1. **Prioritize by information gain** - Ask questions that split decision space most. If answer changes other questions, ask early.

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

4. **Always mark one option "(Recommended)"** - put first with reasoning in description

5. **Be thorough via technique**:
   - Cover everything relevant - don't skip to save time
   - Reduce cognitive load through HOW you ask: concrete options, batching (up to 4), good defaults
   - Make decisions yourself when context suffices
   - Complete spec with easy questions > incomplete spec with fewer questions

6. **Ask non-obvious questions** - User motivations, edge cases affecting UX, business rules, user expectations vs delivery, tradeoffs

7. **Only ask user when**: (a) business/product decision required, (b) codebase lacks answer, (c) multiple interpretations need user choice. Otherwise decide yourself.

### Sample Questions

| Priority | Header | Question | Options (first = recommended) |
|----------|--------|----------|-------------------------------|
| 1 | Feature Scope | What's the scope? | V1/MVP - core only; Full feature; Custom |
| 1 | Target User | Primary user? | [From CUSTOMER.md]; All users; Specific segment; Admin only |
| 2 | Interaction | How triggered? | User-initiated; System-triggered; Both |
| 3 | Constraints | Hard constraints? (multiSelect) | None; Must integrate with X; Regulatory; Performance |
| 4 | Problem | What problem are we solving? | (freeText with placeholder) |
| 4 | Edge Cases | How handle [edge case]? | Best practice default; Alternative 1; Alternative 2; Skip in v1 |
| 5 | Success | How measure success? (multiSelect) | Faster task completion; Adoption increase; Fewer tickets; NPS; Custom |

## Phase 4: Finalize & Summarize

### 4.1 Final interview log update

```markdown
## Interview Complete
Finished: {timestamp} | Questions: {count} | Decisions: {count}
## Summary
{Brief summary of discovery process}
```

### 4.2 Finalize specification

Final pass: remove `[TBD]` markers, ensure consistency. Use EARS format adapted to work type:

```markdown
# Requirements: {Work Name}

Generated: {date}
Type: {Feature | Bug Fix | Doc Update | Refactor | Other}

## Overview
### Problem Statement
### Target Users / Affected Areas
### Success Criteria

## User Stories
### {Story Name}
As a {user}, I want to {action} so that {benefit}.
**Acceptance Criteria:** Given {context}, when {action}, then {outcome}

## Requirements

### EARS Patterns
- **Ubiquitous**: The system shall {behavior}.
- **Event-Driven**: When {trigger}, the system shall {response}.
- **State-Driven**: While {condition}, the system shall {behavior}.
- **Unwanted Behavior**: If {error}, then the system shall {handling}.
- **Optional**: Where {feature exists}, the system shall {behavior}.

### Core Behavior
### User Interactions
### States & Feedback
### Edge Cases & Errors
### Business Rules

## User Experience
### User Flow
### Key Screens/States (Empty, Loading, Success, Error)
### Accessibility

## Constraints
### Business Constraints
### Dependencies

## Out of Scope
- {Non-goal}: {reason}
```

**Section guidance**: Problem Statement (what+why), Target Users (who+affected areas), Success Criteria (how know succeeded), User Flow (step-by-step), Key Screens (what user sees in Empty/Loading/Success/Error states), Accessibility (user-facing requirements), Business Constraints (limits, quotas, permissions), Dependencies (external factors), Out of Scope (non-goals with reasons).

Adapt by work type: bug fixes include root cause/verification; doc updates list affected docs.

### 4.3 Mark all todos complete

### 4.4 Output summary

```
## Spec Summary

**Work**: {name}
**Type**: {type}
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
| WHAT not HOW | Requirements only - no architecture, APIs, data models, code patterns. Self-check: if thinking "how to implement," refocus on "what should happen" |
| User perspective | Observable behavior, user experience, outcomes. Ask "what does user see?" not "how does system work?" Edge cases = UX/business impact |
| No open questions | Resolve everything during interview - no TBDs in final spec |
| Reduce cognitive load | Recommended option first, multi-choice over free-text (free-text only when necessary), batch up to 4, max 6-8 options. User accepting defaults should yield solid result |
| Make decisions | Use research for defaults; only ask when user input required. Defer technical decisions to planning phase |
| Incremental updates | Update interview log after EACH step (not at end) |

### Completion Checklist

Interview complete when ALL true (keep iterating until every box checked):
- [ ] Work type and scope defined (v1/MVP vs full)
- [ ] Target users identified
- [ ] Success criteria specified
- [ ] Core requirements (3+) documented
- [ ] Edge cases for core flow addressed
- [ ] Out of scope explicitly listed
- [ ] No `[TBD]` markers remain

Don't rush - one more question beats incomplete spec.

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
| Interview interrupted | Spec saved; add `[INCOMPLETE]` at top |
| "Just build it" | Push back with top 2-3 critical questions; if declined, document assumptions |
