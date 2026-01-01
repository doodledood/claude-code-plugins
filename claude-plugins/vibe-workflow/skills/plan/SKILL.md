---
name: plan
description: 'Create implementation plans from a spec through iterative codebase research and strategic questions. Produces mini-PR based plans optimized for iterative development.'
---

# Plan Skill

Build an implementation plan through structured discovery. This skill takes a spec (from `/spec` or provided inline) and iteratively researches the codebase and asks strategic questions to produce a detailed implementation plan.

> **Focus on HOW, not WHAT**: The spec defines what needs to be built. This skill defines how to build it - architecture, files, functions, chunks, dependencies, and tests.

## Overview

This skill guides you through an **iterative loop** of:
1. **Research** - Launch codebase-researcher agents to find exact files/patterns for the spec
2. **Interview** - Ask strategic questions about approach, trade-offs, constraints
3. **Write** - Update the plan incrementally after each iteration

## Workflow

### Phase 0: Enter Plan Mode

**IMMEDIATELY use the EnterPlanMode tool as your very first action.** This ensures the user knows you're entering a planning phase and prevents any accidental code changes during the planning process.

Do not read files, research, or ask questions before entering plan mode. EnterPlanMode first, then proceed with the rest of the workflow.

### Phase 1: Initial Context Gathering

Before asking any questions, gather codebase context to inform the plan.

**Step 1.1: Read the spec**

If the user provides a spec file path, read it first. If they provide spec content inline, use that. Extract:
- What needs to be built (requirements)
- User stories and acceptance criteria
- Constraints and business rules
- Out of scope items

**Step 1.2: Launch codebase-researcher agent(s) for focused research**

Use the **codebase-researcher agent** (via Task tool with `subagent_type: "vibe-workflow:codebase-researcher"`) to find the exact files and patterns needed for THIS spec.

Launch one or more researchers depending on scope:
- **Single researcher**: For focused work touching one area
- **Multiple researchers in parallel**: For cross-cutting work (e.g., one for data layer, one for API, one for UI) - launch all Task calls in a single message to run them concurrently

Prompt each researcher to explore:
- Existing implementations of similar features
- Files that will need modification
- Patterns and conventions in the codebase
- Integration points and dependencies
- Test patterns for similar functionality

Each researcher returns comprehensive analysis plus a **prioritized reading list** of files.

**Step 1.3: Read all recommended files**

After the researcher(s) complete, read every file from their recommended reading lists. This gives you firsthand knowledge of:
- Code patterns and architecture
- Existing implementations to build upon
- Integration points and APIs
- Test structure and patterns

Do not skip any recommended files - the researchers identified them as important for planning this work.

**Step 1.4: Write initial plan draft**

After initial research, write the first draft to `/tmp/plan-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` with what you know so far. Mark uncertain areas with `[TBD]` - these will be resolved during the interview. Use this same file path for all subsequent updates.

### Phase 2: Iterative Discovery Interview

**IMPORTANT: Use AskUserQuestion tool for ALL questions.** Never ask questions in plain text - always use the tool so the user gets structured options to choose from.

#### Interview Rules

1. **Research first, ask strategically** - Exhaust codebase research before asking. Only ask when:
   - Multiple architecturally significant paths exist with different trade-offs
   - Scope boundaries are unclear and materially affect chunk structure
   - Technology choices lack precedent and impact system design
   - Business context is needed (speed vs quality, MVP vs complete, priorities)
   - User preferences are ambiguous (approach, patterns, constraints)

   **Discovery and questions are an iteration loop** - Don't just research upfront and then ask all questions. Interleave them:
   - User answer reveals new area? → Launch codebase-researcher to understand existing patterns
   - Need to understand how something is implemented? → Research first, then ask
   - Unsure if codebase already has a pattern? → Discover before asking

   **Update plan after each iteration** - After each research/interview round, update the plan file with new information. Replace `[TBD]` markers as decisions are made.

2. **Don't ask when research provides clear answer**:
   - Established patterns exist in codebase (follow them)
   - Standard best practices are well-documented
   - Implementation details don't affect public APIs
   - Minor tool/library choices with similar capabilities
   - Tactical decisions that can be adjusted later without architectural changes

3. **Always mark one option as "(Recommended)"** - Put it first with reasoning in the description

4. **Be thorough, reduce cognitive load through technique**:
   - **Cover everything relevant** - don't skip questions to save time
   - Reduce burden through HOW you ask: concrete options, batching, good defaults
   - Batch related questions together (up to 4 per call)
   - Make reasonable decisions yourself when research/context is sufficient
   - Focus on architectural decisions, not implementation details
   - A complete plan with easy questions > incomplete plan with fewer questions

5. **Ask high-value questions first** - Prioritize by information gain:

   **Priority 1: Scope Eliminators** (ask first)
   - "Is this v1/MVP or mature feature?" → If v1, skip 50%+ of edge cases
   - "Core flow only or full feature?" → Dramatically narrows scope
   - "Single item or batch support?" → Different complexity levels

   **Priority 2: Architectural Choices**
   - "Which pattern should we use for [X]?" → Opens/closes entire approaches
   - "Sync or async?" → Different paradigms
   - "Existing pattern or new approach?" → Build vs extend

   **Priority 3: Hard Constraints**
   - "Must integrate with existing system X?" → Constrains design
   - "Performance/scale requirements?" → Affects feasibility
   - "Backward compatibility needed?" → Migration complexity

   **Priority 4: Detail Refinement** (ask last)
   - Specific error handling strategies
   - Test coverage priorities
   - Function naming conventions

6. **Iterate until complete** - Keep interviewing until:
   - All architectural decisions are made
   - Chunks are well-defined with clear dependencies
   - File manifests are complete
   - Every `[TBD]` is resolved

### Phase 3: Finalize and Present

After the interview is complete and all `[TBD]` markers are resolved:

**Step 3.1: Finalize the plan**

Do a final pass to:
- Remove any remaining `[TBD]` markers
- Ensure consistency across chunks
- Verify dependency ordering
- Add line ranges for large files (>500 lines)

**Step 3.2: Present via ExitPlanMode**

Use the ExitPlanMode tool to present the plan for user approval. If ExitPlanMode is not available, present the plan in text format.

**Step 3.3: Wait for explicit approval**

Do NOT start implementation until the user explicitly approves. After approval:
- Persist the approved plan to the `/tmp/plan-{timestamp}-{name}.md` file (already done incrementally)
- Create todos from plan chunks
- Execute via todo system

---

# Planning Methodology

The following sections define the planning methodology to follow when creating implementation plans.

## 1. Principles

- **Safety**: Never skip gates; every chunk includes tests and demos independently
- **Clarity**: Full paths, numbered chunks, rationale for context files, line ranges for large files
- **Minimalism**: Prefer 1-3 chunks; ship today's requirements only; parallelize when possible
- **Forward focus**: Do not prioritize backward compatibility by default; only maintain it if explicitly requested or if breaking it would violate system boundaries (in which case, ask the user)
- **Conflicts**: Safety > Clarity > Minimalism > Forward focus
- **Cognitive load**: Ruthlessly minimize extraneous cognitive load across plans, code, and architecture. Prefer deep modules with simple interfaces over many shallow parts; reduce choices; keep the happy path obvious.

### Code Quality Principles (P1-P10)

Plans must produce code that passes rigorous review. Apply these principles when designing chunks. **All principles are guidelines, not laws - the user's explicit intent always takes precedence.** If the user deliberately requests an approach that violates a principle, respect that decision.

| # | Principle | Planning Implication |
|---|-----------|----------------------|
| **P1** | **Correctness Above All** | Every chunk must demonstrably work. Prove behavior, not just compilation. |
| **P2** | **Diagnostics & Observability** | Plan logging and error visibility. Silent failures are unacceptable. |
| **P3** | **Make Illegal States Unrepresentable** | Design types that prevent bugs at compile-time. Types before implementations. |
| **P4** | **Single Responsibility** | Each chunk does ONE thing. If you need "and" to describe it, split it. |
| **P5** | **Explicit Over Implicit** | Plan clear APIs. No hidden behaviors, magic values, or implicit config. |
| **P6** | **Minimal Surface Area** | Solve today's problem. Don't plan for hypothetical futures. YAGNI. |
| **P7** | **Prove It With Tests** | Every chunk includes specific test cases, not "add tests". |
| **P8** | **Safe Evolution** | Public API/schema changes need migration paths. Internal changes can break freely. |
| **P9** | **Fault Containment** | Plan for failure isolation. Include retry/fallback strategies. |
| **P10** | **Comments Tell Why** | Plan documentation for complex logic - why, not what. |

**Values**: Mini-PR chunks over monolithic changes; parallel work streams over sequential waterfalls; function-level planning over code details; dependency clarity over implicit coupling; ship-ready increments over half-built features

## 2. Mini-PR Chunks

Each chunk must:

1. Ship complete value (demo independently)
2. Pass all gates (type checks, tests, lint)
3. Be mergeable on its own (typically 1-3 functions, <200 LOC)
4. Include its tests (specific cases, not "write tests")

## 3. Chunk Sizing

- **Simple**: 1-2 chunks (1-3 functions each)
- **Medium**: 3-5 chunks (<200 LOC per chunk)
- **Complex**: 5-8 chunks (each demo-able)
- **Integration**: 1 final chunk to connect prior work

**Decision guide:**

- New model/schema → start with types/schema chunk
- Touches >3 files or >5 functions → split by concern (data, logic, API)
- Complex integration (>5 deps) → foundation chunk, then integration
- All in one module and <200 LOC → single chunk acceptable

## 4. Dependency Ordering

- **True deps**: uses types, calls functions, extends from another
- **False deps**: same feature but no interaction (parallelize)
- Minimize chains: A→B and A→C, then B,C→D (not A→B→C→D)
- Number chunks sequentially; mark parallel opportunities

## 5. What Belongs vs. Not

- **Belongs**: numbered chunks, gates per chunk, todo descriptions, file manifests (modify/create/context) with reasons, function names only (no code)
- **Not**: code snippets, extra features, future-proofing, perf tuning, assumed knowledge, implicit files

## 6. Cognitive Load in Planning

- **Deep modules first**: Aim for fewer, deeper modules with simple, powerful interfaces. Hide complexity inside a module rather than scattering tiny wrappers across files.
- **Minimize indirection**: Only add layers when there's a concrete extension point. Favor dependency inversion over ceremony-heavy architectures.
- **Composition root**: Provide one obvious wiring point (e.g., main composition function, application setup, dependency injection container), so newcomers can read how the system fits together in a single place.
- **Decide late**: Add indirection or abstractions only when this PR needs a concrete extension point. Avoid speculative layers.
- **Framework at the edges**: Keep core business logic framework-agnostic; plan thin adapters at boundaries (HTTP, DB, UI).
- **Reduce choices**: Prefer one idiomatic approach per concern (logging, config, DI). Document the choice in the plan to prevent re-litigating.
- **Measure confusion**: If a reviewer spends >40 minutes confused, simplify the plan or reshape chunk boundaries to reduce concurrent concepts.

## 7. Common Planning Patterns

- **Sequential**: Model → Logic → API → Error handling
- **Parallel after foundation**: Model → CRUD operations (parallel) → Integration
- **Pipeline**: Types → Parse/Transform (parallel) → Format → Error handling
- **Authentication**: User model → Login endpoint → Auth middleware → Logout
- **Search**: Data structure → Search algorithm → API endpoint → Ranking

## 8. Plan Structure Template

Use this structure for all plans - both when presenting for approval and when persisting to files.

```markdown
# IMPLEMENTATION PLAN: [Feature Name]

[1-2 sentences on what we're building]

Gates per chunk: Type checks (0 errors), Tests (pass), Lint (clean)

---

## 1. [Descriptive Name]

Depends on: - | Parallel: -

[What this chunk delivers in 1-2 sentences]

Files to modify:

- apps/.../path.ts - [what changes]

Files to create:

- apps/.../new.ts - [purpose]

Related files for context:

- libs/.../reference.ts - [why relevant]

Notes (optional):

- Assumptions, risks, blockers
- Alternatives considered or rationale
- Links/references useful for implementation
- Anything else to help implementor if meaningful and non-trivial

Implementation tasks:

- Implement functionName() - [purpose]
- Tests - [cases]
- Run gates

Key functions: functionName(), helper()
Types: TypeName
```

## 9. File Manifest & Context Selection

- List every file to modify/create; specify what changes and purpose
- Assume zero prior knowledge; include full paths
- For context files, explain WHY each is relevant; include line ranges for >500-line files

## 10. Plan Quality Criteria

- **Good**: each chunk ships value; deps ordered; parallel work identified; files explicit; context has reasons; tests in todos; gates listed
- **Excellent**: adds optimal parallelization, line numbers for large files, clear integration points, risk notes, alternatives, and explicitly reduces extraneous cognitive load (deep modules, simple interfaces, minimal layers)

### Quality Checklist for Each Chunk

Before finalizing a chunk in the plan, verify it addresses:

- [ ] **Correctness**: Handles boundaries, null/empty, error paths (not just happy path)
- [ ] **Type Safety**: Types prevent invalid states; validation at boundaries
- [ ] **Observability**: Errors logged with context; failures visible, not silent
- [ ] **Resilience**: External calls have timeouts; retries with backoff; resource cleanup
- [ ] **Clarity**: Names descriptive; no magic values; explicit control flow
- [ ] **Modularity**: Single responsibility; <200 LOC; minimal coupling
- [ ] **Tests**: Critical paths tested; error paths tested; boundaries tested
- [ ] **Evolution**: Public API/schema changes have migration paths; internal changes break freely

### Test Coverage Priority

Align test planning with code review expectations:

| Priority | What | Requirement |
|----------|------|-------------|
| 9-10 | Data mutations, money/finance, auth, state machines | MUST test |
| 7-8 | Business logic branches, API contracts, error paths | SHOULD test |
| 5-6 | Edge cases, boundaries, integration points | GOOD to test |
| 1-4 | Trivial getters, simple pass-through | OPTIONAL |

### Error Handling in Plans

For chunks touching external systems or user input, specify:

1. **What can fail**: List failure modes explicitly
2. **How failures surface**: Logging, user-facing messages
3. **Recovery strategy**: Retry, fallback, fail-fast

Avoid planning for:
- Empty catch blocks
- Catch-and-return-null without logging
- Silent fallbacks to defaults
- Broad exception catching

## 11. Problem Scenarios

### No detailed requirements

1. Research: Read related code, search for similar features, check patterns
2. If fundamentals unclear after research:
   - **Tool available**: Ask via AskUserQuestion (scope, must-haves, approach)
   - **Tool unavailable**: Stop planning; ask in chat; resume after clarification
3. For non-critical details: Make reasonable assumptions; document in plan notes

### Extensive requirements

1. Extract MUSTs first; identify what's explicitly required vs. nice-to-have
2. Research existing implementations of similar scope
3. If scope boundaries ambiguous after research:
   - **Tool available**: Ask about priority trade-offs (speed vs. completeness, MVP vs. full)
   - **Tool unavailable**: Stop and clarify in chat
4. Defer SHOULD/MAY items explicitly; focus plan on MUSTs only

### Multiple valid approaches exist

1. Research first:
   - What patterns does this codebase use?
   - What do docs/examples recommend?
   - What are proven best practices?
2. Ask when approaches have significantly different implications:
   - **Examples requiring questions:**
     - State management: Redux vs Context vs Zustand (team preference + complexity)
     - Auth strategy: JWT vs sessions vs OAuth (security + user experience)
     - Data modeling: SQL vs NoSQL vs cache (access patterns + scale)
     - API design: REST vs GraphQL vs tRPC (client needs + team familiarity)
   - **How to ask:**
     - Tool available: Present 2-4 options with trade-offs; let user choose
     - Tool unavailable: Stop planning; explain options in chat
3. Don't ask when research provides clear answer:
   - Codebase consistently uses one approach (follow it)
   - Requirements clearly favor one option
   - Standard best practice exists for the technology

### Everything appears dependent

1. Start from data model/types (foundation)
2. Question each assumed dependency: "Does B truly need A, or just A's types?"
3. Look for parallel opportunities (false dependencies sharing same feature)
4. If truly sequential: foundation → parallel builds → integration chunk

## Planning Mantras

Before finalizing:

1. What's the smallest shippable increment?
2. Does it pass all quality gates?
3. Can we ship with less?
4. Is this explicitly required?
5. Do dependencies determine order?
6. Have I researched first, then asked strategically?
7. Does this reduce or increase cognitive load?
8. Does each chunk satisfy P1-P10? (Correctness, Observability, Types, SRP, Explicit, Minimal, Tests, Evolution, Faults, Comments)
9. Are error paths planned, not afterthoughts?
10. Will this pass code review on first submission?

## Recognize & Adjust

- Chunk too big (>200 LOC)? Split by concern
- No clear value? Merge or refocus
- Dependencies unclear? Make explicit and number
- Context missing? Add related files with line numbers

---

## Key Principles

### Research First, Ask Strategically
- Exhaust codebase research before asking questions
- Use codebase-researcher for internal patterns
- Only ask when multiple valid approaches exist with different trade-offs
- Make reasonable decisions when research provides clear answers

### Iterative Discovery
- Research and questions are an iteration loop, not sequential phases
- Launch researchers after getting answers that reveal new areas
- Update the plan after each iteration
- Use `[TBD]` markers for unresolved items, replace as decisions are made

### Reduce Cognitive Load (Without Leaving Gaps)
- **Be thorough** - cover every relevant architectural decision; don't skip questions to save time
- Reduce burden through HOW you ask: concrete options, batching, good defaults
- **Put recommended option FIRST** with "(Recommended)" suffix
- Present multi-choice questions to minimize typing
- Batch related questions together (up to 4 per call)
- User should be able to accept most defaults and get a solid plan
- ALWAYS use AskUserQuestion tool - never plain text questions
- **No stone left unturned**: A complete plan with easy questions beats an incomplete plan with fewer questions

### Maximize Information Gain
- Ask questions that split the decision space most effectively
- Scope eliminators first → architectural choices → constraints → details last
- If an answer changes what other questions you'd ask, ask it early

## Output Location

Write the plan to `/tmp/plan-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - create after initial research, update incrementally throughout the process.
