---
name: spec
description: 'Interactive requirements builder that interviews you to create a comprehensive spec using EARS syntax. Works for features, bug fixes, doc updates, refactors - any work that needs clear definition.'
---

# Spec Skill

Build a requirements spec through structured discovery interview. This skill conducts an interview to understand WHAT needs to be done and WHY - not technical implementation details.

Works for any type of work:
- **Features** - New functionality to build
- **Bug fixes** - Problems to investigate and resolve
- **Doc updates** - Documentation to create or improve
- **Refactors** - Code improvements with clear goals
- **Any request** - Anything that benefits from clear requirements

> **Focus on WHAT, not HOW**: This skill defines requirements - what needs to be done and why. No technical architecture, APIs, data models, libraries, or implementation approach. Those come in the next phase (implementation planning).

## Overview

This skill guides you through an **iterative loop** of:
1. **Discovery** - Launch codebase-explorer and web-researcher agents as needed
2. **Interview** - Ask smart questions about decisions, needs, edge cases
3. **Write** - Update the spec incrementally after each iteration

The interviewer role is that of a senior product manager: asking smart, non-obvious questions that reduce ambiguity and cognitive load.

**Incremental spec updates**: Write the current spec to `/tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` after each research/interview iteration. This captures progress and allows the user to review at any point.

## Workflow

### Phase 1: Initial Context Gathering

Before asking any questions, gather context to ask informed questions and suggest sensible defaults.

**Step 1.1: Launch codebase-explorer agent(s) for overview**

Use the **codebase-explorer agent** (via Task tool with `subagent_type: "vibe-workflow:codebase-explorer"`) to gain comprehensive understanding of the context for this work.

Launch one or more researchers depending on scope:
- **Single researcher**: For focused work touching one area
- **Multiple researchers in parallel**: For cross-cutting work (e.g., one for auth, one for payments, one for notifications) - launch all Task calls in a single message to run them concurrently

Prompt each researcher to explore:
- What the product does and who uses it
- Existing related code and patterns
- User flows and terminology
- Product docs (CUSTOMER.md, SPEC.md, PRD.md, BRAND_GUIDELINES.md, DESIGN_GUIDELINES.md, README.md)
- Any existing specs or requirements in `docs/`, `specs/`, or similar directories
- For bug fixes: the bug's context, related code, potential causes

Each researcher returns comprehensive analysis plus a **prioritized reading list** of files you should read.

**Step 1.2: Read all recommended files**

After the researcher(s) complete, read every file from their recommended reading lists. This gives you firsthand knowledge of:
- Code patterns and terminology
- Existing implementations to build upon
- Product context and user definitions
- Design and brand guidelines

Do not skip any recommended files - the researchers identified them as important for specifying this work.

**Step 1.3: Launch web-researcher agent(s) for external research (if needed)**

Use the **web-researcher agent** (via Task tool with `subagent_type: "vibe-workflow:web-researcher"`) whenever you lack sufficient knowledge to define WHAT needs to be built. Research:
- Domain-specific concepts, terminology, or standards you're unfamiliar with
- User expectations - what do users expect from this type of feature/solution?
- How other products solve similar problems (from a user experience perspective)
- Regulatory, compliance, or industry requirements that affect what we must build
- Business context that shapes requirements
- Any topic where your knowledge is insufficient to ask good questions or define clear requirements

**Stay focused on WHAT**: Research to understand the problem domain and user needs, not technical implementation approaches.

Launch one or more web researchers depending on scope:
- **Single researcher**: For focused questions
- **Multiple researchers in parallel**: For work needing research on multiple topics - launch all Task calls in a single message to run them concurrently

Each researcher returns all relevant findings in its response - no need to read additional files.

This context lets you ask informed questions and suggest sensible defaults. Continue launching web researchers throughout the interview whenever knowledge gaps emerge.

**Step 1.4: Write initial spec draft**

After initial research, write the first draft to `/tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` with what you know so far. Mark uncertain areas with `[TBD]` - these will be resolved during the interview. Use this same file path for all subsequent updates.

### Phase 2: Iterative Discovery Interview

**IMPORTANT: Use AskUserQuestion tool for ALL questions.** Never ask questions in plain text - always use the tool so the user gets structured options to choose from.

#### Interview Rules

1. **Prioritize by information gain** - Ask questions that split the decision space most. Before each question, ask: *"Does the answer change what other questions I need to ask?"* If yes, ask it early.

   **Discovery and questions are an iteration loop** - Don't just research upfront and then ask all questions. Interleave them:
   - User answer reveals new area? → Launch codebase-explorer to understand existing behavior
   - Need to understand current product behavior? → Research first, then ask
   - Unsure if codebase already handles something? → Discover before asking
   - **Launch web-researcher whenever you lack knowledge** to define requirements:
     - Domain concepts or terminology you don't understand
     - User expectations for this type of feature
     - Regulatory or compliance requirements
     - How similar products handle this (UX perspective, not technical)

   **Remember: WHAT, not HOW** - Research to understand requirements, not implementation.

   **Update spec after each iteration** - After each research/interview round, update the spec file with new information. Replace `[TBD]` markers as decisions are made. This keeps the spec current and lets the user review progress anytime.

   Only ask the user when:
   - The answer requires a business/product decision
   - The codebase doesn't have the answer
   - Multiple valid interpretations exist and the user must choose

   **Priority 1: Scope Eliminators** (ask first)
   Answers eliminate large chunks of work entirely:
   - "Is this v1/MVP or mature feature?" → If v1, skip 50%+ of edge cases
   - "All users or specific segment?" → May eliminate permission considerations
   - "Core flow only or full feature?" → Dramatically narrows scope

   **Priority 2: Branching Questions**
   Answers open/close entire lines of inquiry:
   - "User-initiated or system-triggered?" → Different interaction models
   - "Real-time or async?" → Different UX paradigms
   - "Single item or batch?" → Different complexity levels

   **Priority 3: Hard Constraints**
   Non-negotiable limits that constrain options:
   - "Regulatory/compliance requirements?" → May dictate behaviors
   - "Must integrate with existing system X?" → Constrains design
   - "Performance/scale requirements?" → Affects feasibility

   **Priority 4: Differentiating Questions**
   Choose between remaining viable approaches:
   - "Pattern A vs B for this use case?"
   - "Which UX model fits better?"

   **Priority 5: Detail Refinement** (ask last)
   Fine-grained questions that don't affect other decisions:
   - Exact copy/messaging
   - Specific error handling
   - Edge case behavior details

2. **Always mark one option as "(Recommended)"** - Put it first with reasoning in the description

3. **Be thorough, reduce cognitive load through technique**:
   - **Cover everything relevant** - don't skip questions to save time
   - Reduce burden through HOW you ask: concrete options, batching, good defaults
   - Batch related questions together (up to 4 per call)
   - Make reasonable decisions yourself when research/context is sufficient
   - Focus on business/product decisions, not implementation details
   - A complete spec with easy questions > incomplete spec with fewer questions

4. **Ask non-obvious questions** - Focus on:
   - User motivations and jobs-to-be-done
   - Edge cases that affect user experience
   - Business rules and constraints
   - What users expect vs. what we'll actually deliver
   - Tradeoffs that affect the user

5. **Iterate until complete** - Keep interviewing until:
   - All product decisions are made
   - User-facing edge cases are addressed
   - Scope is crystal clear
   - Every requirement can be written definitively

#### Sample Interview Questions (ordered by priority)

**Priority 1: Scope Eliminators**

```
header: "Feature Scope"
question: "What's the scope for this feature?"
options:
  - "V1/MVP - core flow only, minimal edge cases (Recommended)"
  - "Full feature - comprehensive coverage"
  - "Let me describe the scope"
```

```
header: "Target User"
question: "Who is the primary user for this feature?"
options:
  - "[Inferred from CUSTOMER.md if exists] (Recommended)"
  - "All users - this affects everyone"
  - "Specific user segment - let me specify"
  - "Admin/power users only"
```

**Priority 2: Branching Questions**

```
header: "Interaction Model"
question: "How is this feature triggered?"
options:
  - "User-initiated - user explicitly triggers it (Recommended)"
  - "System-triggered - happens automatically based on conditions"
  - "Both - user can trigger, system can also auto-trigger"
```

**Priority 3: Hard Constraints**

```
header: "Constraints"
question: "Are there hard constraints we must respect?"
options:
  - "No special constraints (Recommended)"
  - "Must integrate with existing system - let me specify"
  - "Regulatory/compliance requirements - let me specify"
  - "Performance/scale requirements - let me specify"
multiSelect: true
```

**Priority 4-5: Refinement Questions**

```
header: "Problem Statement"
question: "What problem are we solving?"
freeText: true
placeholder: "Describe the pain point this feature addresses"
```

```
header: "Success Criteria"
question: "How will we know this feature succeeded?"
options:
  - "User completes the task faster (Recommended)"
  - "User adoption/engagement increases"
  - "Reduction in support tickets"
  - "User satisfaction (NPS/feedback)"
  - "Custom metrics - let me specify"
multiSelect: true
```

```
header: "Edge Cases"
question: "How should we handle [specific edge case]?"
options:
  - "[Best practice default] (Recommended)"
  - "[Alternative approach 1]"
  - "[Alternative approach 2]"
  - "Skip this edge case in v1"
```

### Phase 3: Finalize the Spec & Summarize

After the interview is complete and all `[TBD]` markers are resolved:

**Step 3.1: Finalize the specification**

The spec has been incrementally updated throughout the process. Do a final pass to:
- Remove any remaining `[TBD]` markers
- Ensure consistency across sections
- Add any missing sections based on the work type

Use the EARS (Easy Approach to Requirements Syntax) format. Adapt sections based on work type (feature, bug fix, doc update, etc.):

```markdown
# Requirements: {Work Name}

Generated: {date}
Type: {Feature | Bug Fix | Doc Update | Refactor | Other}

## Overview

### Problem Statement
What problem are we solving? Why does it matter?

### Target Users / Affected Areas
Who is this for? What parts of the system are affected?

### Success Criteria
How do we know this work succeeded?

## User Stories

### {User Story Name}
As a {user type}, I want to {action} so that {benefit}.

**Acceptance Criteria:**
- Given {context}, when {action}, then {outcome}

## Requirements

Use EARS patterns. Organize by sections (not numbers) for easy updates.

### EARS Patterns
- **Ubiquitous**: The system shall {behavior}.
- **Event-Driven**: When {trigger}, the system shall {response}.
- **State-Driven**: While {condition}, the system shall {behavior}.
- **Unwanted Behavior**: If {error/edge case}, then the system shall {handling}.
- **Optional**: Where {feature/config exists}, the system shall {behavior}.

### Core Behavior

#### {Requirement Name}
When the user {action}, the system shall {response}.

#### {Requirement Name}
The system shall {behavior}.

### User Interactions

#### {Interaction Name}
When the user {action}, the system shall {feedback/response}.

### States & Feedback

#### {State Name}
While {state is active}, the system shall {display/behavior}.

### Edge Cases & Errors

#### {Scenario Name}
If {condition occurs}, then the system shall {user-facing handling}.

### Business Rules

#### {Rule Name}
The system shall {enforce constraint/rule}.

## User Experience

### User Flow
Step-by-step flow from user's perspective.

### Key Screens/States
- **Empty state**: What the user sees when {no data/first time}
- **Loading state**: What the user sees while waiting
- **Success state**: What the user sees on success
- **Error state**: What the user sees on failure

### Accessibility
Key accessibility requirements from user perspective.

## Constraints

### Business Constraints
Limits, quotas, permissions, or business rules that affect the user.

### Dependencies
Other features or external factors users should be aware of.

## Out of Scope

Explicit non-goals - what we are NOT building (and why).

- {Non-goal}: {brief reason}
```

Adapt sections based on the work type. Skip irrelevant sections, add custom ones as needed. For bug fixes, include root cause and fix verification. For doc updates, include affected docs and changes.

**Step 3.2: Output a summary**

After finalizing the spec, output a summary so the user can validate without reading the full spec:

```
## Spec Summary

**Work**: {name}
**Type**: {Feature | Bug Fix | Doc Update | Refactor | Other}
**File**: /tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md

### What We're Doing
{1-2 sentence overview}

### Key Decisions Made
- {Decision 1}: {choice made}
- {Decision 2}: {choice made}

### Core Requirements ({count})
- {Most important requirement}
- {Second most important}
- {Third most important}

### Out of Scope
- {Key non-goal 1}
- {Key non-goal 2}

---
Review the full spec and let me know if you'd like to adjust anything.
```

## Key Principles

### Focus on WHAT, not HOW
- Define requirements: what needs to happen, what the user experiences, what success looks like
- No technical implementation: architecture, APIs, data models, libraries, code patterns
- Technical planning comes in the next phase after requirements are clear
- If you catch yourself thinking about "how to implement," refocus on "what should happen"

### User/Outcome Perspective
- Requirements describe observable behavior or outcomes
- Edge cases are about user experience and business impact, not system internals
- Success is measured by user outcomes or problem resolution
- Ask "what does the user see/experience?" not "how does the system work?"

### No Open Questions
- Resolve everything during the interview
- No TBDs or placeholders in the final spec
- If something is unclear, ask during the interview

### Reduce Cognitive Load (Without Leaving Gaps)
- **Be thorough** - cover every relevant aspect; don't skip questions to save time
- Reduce cognitive load through HOW you ask, not by asking less:
  - **Put recommended option FIRST** with "(Recommended)" suffix
  - Present multi-choice questions to minimize typing
  - Batch related questions together (up to 4 per call)
  - Limit options to 6-8 max per question
  - Only use free-text when truly necessary
- User should be able to accept most defaults and get a solid result
- ALWAYS use AskUserQuestion tool - never plain text questions
- **No stone left unturned**: A complete spec with easy questions beats an incomplete spec with fewer questions

### Maximize Information Gain
- Ask questions that split the decision space most effectively
- Scope eliminators first → branching questions → constraints → details last
- If an answer changes what other questions you'd ask, ask it early

### Make Decisions When You Can
- Use research and context to make reasonable defaults
- Interleave discovery and questions throughout the interview
- Launch codebase-explorer for existing behavior, web-researcher for domain knowledge
- User reviews the final spec and can request changes
- Only ask when user input is actually required (decisions, preferences, ambiguity)
- Defer technical decisions to the implementation planning phase

### Iterate Until Complete

Interview is complete when ALL of these are true:
- [ ] Work type and scope defined (v1/MVP vs full)
- [ ] Target users identified
- [ ] Success criteria specified
- [ ] Core requirements (3+ for features) documented
- [ ] Edge cases for core flow addressed
- [ ] Out of scope explicitly listed
- [ ] No `[TBD]` markers remain

Don't rush to finalize with gaps. Better to ask one more question than produce an incomplete spec.

### Incremental Updates
- Write spec to `/tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` after initial research
- Update the same file after each iteration
- Use `[TBD]` markers for unresolved items, replace as decisions are made
- User can review progress at any point

### Always Output the Summary
- Lets user validate quickly without reading the full spec
- Highlights key decisions for confirmation
- Invites iteration - the spec is a draft

### Never Do These
- NEVER write spec files to project directories - always use `/tmp/` to avoid polluting the codebase
- NEVER ask about technical implementation (architecture, APIs, data models, libraries, code patterns)
- NEVER finalize spec with unresolved `[TBD]` markers
- NEVER skip the summary output
- NEVER ask questions in plain text (always use AskUserQuestion tool when available)
- NEVER proceed past Phase 1 without writing the initial spec draft

### Edge Cases & Fallbacks
- **User declines to answer**: Note the gap with `[USER SKIPPED: reason]` and proceed; flag in summary
- **Research returns insufficient info**: Ask user directly; note uncertainty in spec
- **Contradictory requirements**: Surface the conflict explicitly to user before proceeding
- **Interview interrupted**: Spec-in-progress is already saved; note `[INCOMPLETE]` status at top
- **User says "just build it"**: Push back once with top 2-3 critical questions; if declined, document assumptions

## Output Location

Write the spec to `/tmp/spec-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - never to the project directory. Create after initial research, update incrementally throughout the process. Specs are working documents that don't belong in the codebase.
