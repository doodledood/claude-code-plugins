---
name: spec
description: 'Interactive requirements builder - interviews you to create EARS-syntax spec for features, bugs, docs, refactors.'
---

# Spec Skill

Build requirements spec through structured discovery interview. Defines WHAT and WHY - not technical implementation (architecture, APIs, data models come in planning phase).

**Core loop**: Discovery (codebase-explorer, web-researcher) → Interview (smart questions) → Write (update spec incrementally)

**Role**: Senior PM - smart, non-obvious questions that reduce ambiguity and cognitive load.

**Output**: `/tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - updated after each iteration.

## Phase 1: Initial Context Gathering

### 1.1 Launch codebase-explorer

Use Task tool with `subagent_type: "vibe-workflow:codebase-explorer"` to understand context. Launch multiple in parallel (single message) for cross-cutting work.

Explore: product purpose, existing patterns, user flows, terminology, product docs (CUSTOMER.md, SPEC.md, PRD.md, BRAND_GUIDELINES.md, DESIGN_GUIDELINES.md, README.md), existing specs in `docs/` or `specs/`. For bug fixes: also explore bug context, related code, potential causes.

### 1.2 Read recommended files

Read ALL files from researcher prioritized reading lists - no skipping.

### 1.3 Launch web-researcher (if needed)

Use Task tool with `subagent_type: "vibe-workflow:web-researcher"` for knowledge gaps: domain concepts, user expectations, industry standards, compliance requirements, competitor approaches (UX perspective). Returns all findings in response - no additional file reads needed. Continue launching throughout interview as gaps emerge.

### 1.4 Write initial draft

Write first draft with `[TBD]` markers for unresolved items. Use same file path for all updates.

## Phase 2: Iterative Discovery Interview

**CRITICAL**: Use AskUserQuestion tool for ALL questions - never plain text.

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

## Phase 3: Finalize & Summarize

### 3.1 Finalize specification

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

### 3.2 Output summary

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
| WHAT not HOW | Requirements only - no architecture, APIs, data models, code patterns. Self-check: if thinking "how to implement," refocus on "what should happen" |
| User perspective | Observable behavior, user experience, outcomes. Ask "what does user see?" not "how does system work?" Edge cases = UX/business impact |
| No open questions | Resolve everything during interview - no TBDs in final spec |
| Reduce cognitive load | Recommended option first, multi-choice over free-text (free-text only when necessary), batch up to 4, max 6-8 options. User accepting defaults should yield solid result |
| Make decisions | Use research for defaults; only ask when user input required. Defer technical decisions to planning phase |
| Incremental updates | Write after research, update after each iteration |

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

- Write specs to project directories (always `/tmp/`)
- Ask about technical implementation
- Finalize with unresolved `[TBD]`
- Skip summary output
- Ask questions without AskUserQuestion tool
- Proceed past Phase 1 without initial draft

### Edge Cases

| Scenario | Action |
|----------|--------|
| User declines to answer | Note `[USER SKIPPED: reason]`, flag in summary |
| Insufficient research | Ask user directly, note uncertainty |
| Contradictory requirements | Surface conflict before proceeding |
| Interview interrupted | Spec saved; add `[INCOMPLETE]` at top |
| "Just build it" | Push back with top 2-3 critical questions; if declined, document assumptions |
