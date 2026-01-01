---
name: spec
description: 'Interactive product requirements builder that interviews you to create a comprehensive PRD using EARS syntax. Guides through context gathering, discovery interview, and spec generation.'
---

# Product Spec Skill

Build a product requirements document (PRD) through structured discovery interview. This skill conducts a product-focused interview to understand WHAT to build and WHY - not technical implementation details.

> **Product Focus Only**: No technical architecture, APIs, data models, or testing strategy. Those come later from the implementation team.

## Overview

This skill guides you through:
1. **Context Gathering** - Launch researcher agents, read recommended files, research UX patterns
2. **Discovery Interview** - Smart questions about product decisions, user needs, edge cases
3. **Write Spec** - Generate PRD using EARS syntax, output summary for quick validation

The interviewer role is that of a senior product manager: asking smart, non-obvious questions that reduce ambiguity and cognitive load.

## Workflow

### Phase 1: Context Gathering (Before Asking Questions)

Before asking any questions, gather context to ask informed questions and suggest sensible defaults.

**Step 1.1: Launch codebase-researcher agent(s) for overview**

Use the **codebase-researcher agent** (via Task tool with `subagent_type: "vibe-workflow:codebase-researcher"`) to gain comprehensive understanding of the product context for specifying this feature.

Launch one or more researchers depending on scope:
- **Single researcher**: For focused features touching one area
- **Multiple researchers in parallel**: For cross-cutting features (e.g., one for auth, one for payments, one for notifications) - launch all Task calls in a single message to run them concurrently

Prompt each researcher to explore:
- What the product does and who uses it
- Existing similar features and their UX patterns
- User flows and terminology
- Product docs (CUSTOMER.md, SPEC.md, PRD.md, BRAND_GUIDELINES.md, DESIGN_GUIDELINES.md, README.md)
- Any existing specs or requirements in `docs/`, `specs/`, or similar directories

Each researcher returns comprehensive analysis plus a **prioritized reading list** of files you should read.

**Step 1.2: Read all recommended files**

After the researcher(s) complete, read every file from their recommended reading lists. This gives you firsthand knowledge of:
- Code patterns and terminology
- Existing implementations to build upon
- Product context and user definitions
- Design and brand guidelines

Do not skip any recommended files - the researchers identified them as important for specifying this feature.

**Step 1.3: Launch web-researcher agent(s) for UX/product research (if needed)**

Use the **web-researcher agent** (via Task tool with `subagent_type: "vibe-workflow:web-researcher"`) to research:
- How other products solve similar problems
- UX patterns and user expectations for this type of feature
- Common pitfalls and edge cases users care about

Launch one or more web researchers depending on scope:
- **Single researcher**: For focused features with one main UX question
- **Multiple researchers in parallel**: For features needing research on multiple aspects (e.g., one for UX patterns, one for competitor analysis, one for accessibility best practices) - launch all Task calls in a single message to run them concurrently

Each researcher returns all relevant findings in its response - no need to read additional files.

This context lets you ask informed questions and suggest sensible defaults.

### Phase 2: Discovery Interview

**IMPORTANT: Use AskUserQuestion tool for ALL questions.** Never ask questions in plain text - always use the tool so the user gets structured options to choose from.

#### Interview Rules

1. **Prioritize by information gain** - Ask questions that split the decision space most. Before each question, ask: *"Does the answer change what other questions I need to ask?"* If yes, ask it early.

   **Discovery and questions are an iteration loop** - Don't just research upfront and then ask all questions. Interleave them:
   - User answer reveals new area? → Launch codebase-researcher to understand it
   - Need to know existing patterns before asking about approach? → Research first
   - Unsure if codebase already handles something? → Discover before asking
   - Need UX patterns or industry best practices? → Launch web-researcher
   - User mentions competitor or external product? → Web research before asking follow-ups

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

3. **Reduce cognitive load**:
   - Provide concrete options, not open-ended questions
   - Batch related questions together (up to 4 per call)
   - **Only ask when the user adds value** - Make reasonable decisions yourself based on research/context. User reviews the final spec.
   - Focus on business/product decisions, not implementation details

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

### Phase 3: Write the Spec & Summarize

After the interview is complete:

**Step 3.1: Write the specification**

Write the spec to: `/tmp/feature-spec-{YYYYMMDD-HHMMSS}-{feature-name-kebab-case}.md`

Use the EARS (Easy Approach to Requirements Syntax) format:

```markdown
# Product Requirements: {Feature Name}

Generated: {date}

## Overview

### Problem Statement
What problem are we solving? Why does it matter?

### Target Users
Who is this for? What do they care about?

### Success Criteria
How do we know this feature succeeded?

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

Adapt sections based on the feature. Skip irrelevant sections, add custom ones as needed.

**Step 3.2: Output a summary**

After writing the spec, output a summary so the user can validate without reading the full spec:

```
## Spec Summary

**Feature**: {name}
**File**: /tmp/feature-spec-{timestamp}-{name}.md

### What We're Building
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

### Product Focus Only
- No technical implementation details (architecture, APIs, data models, testing)
- Frame everything from what the user experiences, not how it's built
- Those technical decisions come later from the implementation team

### User Perspective
- Requirements describe user-visible behavior
- Edge cases are about user experience, not system internals
- Success is measured by user outcomes

### No Open Questions
- Resolve everything during the interview
- No TBDs or placeholders in the final spec
- If something is unclear, ask during the interview

### Reduce Cognitive Load
- ALWAYS use AskUserQuestion tool when available
- **Put recommended option FIRST** with "(Recommended)" suffix
- User should be able to accept most defaults and get a solid result
- Present multi-choice questions to minimize typing
- Limit options to 6-8 max per question
- Only use free-text for essential context

### Maximize Information Gain
- Ask questions that split the decision space most effectively
- Scope eliminators first → branching questions → constraints → details last
- If an answer changes what other questions you'd ask, ask it early

### Make Decisions When You Can
- Use research and context to make reasonable defaults
- Interleave discovery and questions - launch codebase-researcher or web-researcher whenever needed
- User reviews the final spec and can request changes
- Only ask when user input is actually required (decisions, preferences, ambiguity)

### Iterate Until Complete
- Keep asking until all product decisions are made
- Don't rush to the spec phase with gaps
- Better to ask one more question than produce an incomplete spec

### Always Output the Summary
- Lets user validate quickly without reading the full spec
- Highlights key decisions for confirmation
- Invites iteration - the spec is a draft

## Output Location

Write the spec to `/tmp/feature-spec-{YYYYMMDD-HHMMSS}-{feature-name-kebab-case}.md`
