---
name: plan
description: 'Create implementation plans from spec via iterative codebase research and strategic questions. Produces mini-PR plans optimized for iterative development.'
---

**User request**: $ARGUMENTS

Build implementation plan through structured discovery. Takes spec (from `/spec` or inline), iteratively researches codebase + asks high-priority technical questions that shape implementation direction → detailed plan.

**Focus**: HOW not WHAT. Spec=what; plan=architecture, files, functions, chunks, dependencies, tests.

**Loop**: Research → Expand todos → Ask questions → Write findings → Repeat until complete

**Output files**:
- Plan: `/tmp/plan-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md`
- Research log: `/tmp/plan-research-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` (external memory)

## Boundaries

- Spec=requirements; this skill=architecture, files, chunks, tests
- Don't modify spec; flag gaps for user
- Surface infeasibility before proceeding
- No implementation until approved

## Phase 1: Initial Setup

### 1.1 Create todos (TodoWrite immediately)

If TodoWrite is unavailable, track todos in the research log under a `## Todos` section using markdown checkbox format, and update status inline (e.g., `- [x] Completed task` or `- [ ] Pending task`).

Todos = **areas to research/decide**, not steps. Expand when research reveals: (a) files/modules to modify beyond those already in todos, (b) 2+ valid implementation patterns with different trade-offs, (c) dependencies on code/systems not yet analyzed, or (d) questions that must be answered before completing an existing todo.

**Starter seeds**:
```
- [ ] Read/infer spec requirements
- [ ] Codebase research (patterns, files to modify)
- [ ] Approach identification (if >1 valid approach exists → trade-off analysis → user decision)
- [ ] Architecture decisions (within chosen approach)
- [ ] (expand as research reveals new areas)
- [ ] Read full research log and spec (context refresh before output)
- [ ] Finalize chunks
```

**Evolution example** - "Add real-time notifications":

Initial → After codebase research → After approach selection → After "needs offline too":
```
- [x] Read spec → 3 types, mobile+web
- [x] Codebase research → found ws.ts, notification-service.ts, also polling pattern in legacy/
- [x] Approach selection → WebSocket vs polling? User chose WebSocket (lower latency, existing infra)
- [ ] Architecture decisions (within WebSocket approach)
- [ ] Offline storage (IndexedDB vs localStorage)
- [ ] Sync conflict resolution
- [ ] Service worker integration
- [ ] Read full research log and spec (context refresh before output)
- [ ] Finalize chunks
```

Note: Approach selection (line 3) shows **user decision**—not auto-decided. Found two valid approaches (WebSocket, polling), presented trade-offs, user chose.

**Key**: Never prune todos prematurely. If todo expansion creates a cycle (new todo depends on incomplete todo that depends on the new todo), merge into a single combined research todo: "- [ ] Research {Area A} + {Area B} (merged: circular dependency)".

**Adapt seeds to scope**: For simple features (1-2 files, single approach), omit "Approach identification" if only one valid approach exists. For complex features (5+ files or 3+ modules), add domain-specific research todos (e.g., "- [ ] Research {specific subsystem}").

### 1.2 Create research log

Path: `/tmp/plan-research-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md`

```markdown
# Research Log: {feature}
Started: {timestamp} | Spec: {path or "inline"}

## Codebase Research
## Approach Trade-offs
## Spec Gaps
## Conflicts
## Risks & Mitigations
## Architecture Decisions
## Questions & Answers
## Unresolved Items
```

## Phase 2: Context Gathering

**Prerequisites**: Requires `vibe-workflow:codebase-explorer` agent. If Task tool fails for any reason (agent not found, timeout error from Task tool, permission error, incomplete results where agent returns without listing files to modify) OR returns fewer than 3 files that would be directly modified or created by the implementation when exploring an area expected to touch multiple modules (expected when: spec requirements explicitly list 3+ distinct components, OR feature description contains any of: "across", "connects", "bridges", "end-to-end", "spans", "links", "integrates", "coordinates", "orchestrates"), perform supplementary codebase research manually using Read, Glob, and Grep tools and note `[SUPPLEMENTED RESEARCH: codebase-explorer insufficient - {reason}]` in research log. Do not retry on timeout—proceed directly to supplementary research.

**If both codebase-explorer AND supplementary research fail** (e.g., no relevant files found, permission errors persist): Log `[RESEARCH BLOCKED: {reason}]` in research log, ask user via AskUserQuestion whether to (a) proceed with assumptions or (b) pause for user to provide context manually.

### 2.1 Read/infer spec

Extract: requirements, user stories, acceptance criteria, constraints, out-of-scope.

**No formal spec?** Infer from conversation, tool outputs, user request. If spec and conversation together provide fewer than 2 concrete requirements (a requirement is concrete if it specifies a behavior or outcome that can be verified by a test, demonstration, or measurable metric—e.g., "user can log in with email/password" is concrete; "system should be fast" is not unless it specifies a latency threshold), ask user via AskUserQuestion: "I need at least 2 concrete requirements to plan. Please provide: [list what's missing]" before proceeding.

### 2.2 Launch codebase-explorer

Task tool with `subagent_type: "vibe-workflow:codebase-explorer"`. Launch multiple in parallel for cross-cutting work (work that spans multiple independent modules or architectural layers—e.g., a feature touching both frontend and backend, or changes affecting authentication and logging simultaneously).

Explore: existing implementations, files to modify, patterns, integration points, test patterns.

### 2.3 Read ALL recommended files

No skipping. Gives firsthand knowledge of patterns, architecture, integration, tests.

### 2.4 Update research log

After EACH step:
```markdown
### {timestamp} - {what researched}
- Explored: {areas}
- Key findings: {files, patterns, integration points}
- New areas: {list}
- Architectural questions: {list}
```

### 2.5 Approach Identification & Trade-off Analysis

**CRITICAL**: Before diving into implementation details, identify whether multiple valid approaches exist. This is THE question that cuts the option space—answering it eliminates entire branches of planning. An approach is "valid" if: (1) it fulfills all spec requirements, (2) it is technically feasible given codebase constraints, and (3) it has at least one condition where it would be preferred over alternatives ("When it wins" is non-empty). Theoretical possibilities that fail any criterion are not valid—do not present them to the user.

**When to do this**: After initial codebase research (2.2-2.4), before writing any implementation details.

**What counts as "multiple approaches"**:
- Different architectural layers (data layer vs presentation layer vs business logic)
- Different implementation patterns (eager vs lazy, push vs pull, centralized vs distributed)
- Different integration points (modify existing function vs create new one)
- Different scopes (filter at source vs filter at consumer)

**Process**:

1. **Identify approaches** from codebase research:
   - Where could this change live? (multiple valid locations = multiple approaches)
   - How could this be implemented? (multiple valid patterns = multiple approaches)
   - Who are the consumers of what we're modifying? (different consumer needs = approach implications)

2. **If only ONE valid approach**: Document why in research log and proceed.

3. **If MULTIPLE valid approaches**: STOP. Do not proceed with planning until user decides.

**Trade-off analysis format** (write to research log under `## Approach Trade-offs`):

```markdown
### Approaches: {what we're deciding}

**Approach A: {name}**
- How: {brief description}
- Pros: {list}
- Cons: {list}
- When it wins: {conditions where this approach is preferred—e.g., latency requirements, team pattern preferences, data volume thresholds, specific constraints}
- Affected consumers: {who uses what we'd modify}

**Approach B: {name}**
- How: {brief description}
- Pros: {list}
- Cons: {list}
- When it wins: {conditions where this approach is preferred—e.g., latency requirements, team pattern preferences, data volume thresholds, specific constraints}
- Affected consumers: {who uses what we'd modify}

**Existing codebase pattern**: {how similar problems are solved elsewhere}
**Recommendation**: {approach} — {why}
**Choose alternative if**: {honest conditions where other approach wins}
```

**Ask user via AskUserQuestion**:

```
questions: [
  {
    question: "Which approach for {requirement}?",
    header: "Approach",
    options: [
      {
        label: "{Recommended approach} (Recommended)",
        description: "{Why it's cleanest}. Choose this unless {condition where alternative wins}."
      },
      {
        label: "{Alternative approach}",
        description: "{What it offers}. Better if {when it wins}."
      }
    ],
    multiSelect: false
  }
]
```

**Recommendation = cleanest approach**, meaning:
1. Follows separation of concerns (changes to presentation logic stay in presentation layer files, data logic stays in data layer files, business rules stay in service/domain files—if unsure which layer, use the layer where similar existing features live)
2. Matches existing codebase patterns for similar problems
3. Minimizes blast radius (fewest consumers affected, easiest to change later)
4. Most reversible (if we're wrong, how hard is it to switch?)

**When criteria conflict**: Prioritize in order listed (1 > 2 > 3 > 4). If criterion 1 is tied, use criterion 2 as tiebreaker, and so on.

**But be honest**: State clearly in the description when the alternative approach wins. User has context you don't (future plans, team preferences, business constraints).

**Only skip asking when**:
- Research shows genuinely ONE valid approach (document why others don't work)
- OR all five measurable skip criteria below are true (if ANY fails, ask the user)

**Measurable skip criteria** (ALL must be true):
1. Same files changed by both approaches
2. No consumer behavior change (grep shows identical call sites)
3. Reversible in <1 chunk of work (where a chunk is 1-3 functions, under 200 lines—see Mini-PR Chunks section)
4. No schema, API, or public interface changes
5. No different error handling or failure modes

If ANY criterion fails, this is a Priority 0 question—ask the user.

### 2.6 Write initial draft

**Precondition**: Approach decided—either (a) single valid approach documented, or (b) user chose/delegated after seeing trade-offs. Do not write draft until Priority 0 resolved.

First draft with `[TBD]` markers. Same file path for all updates.

## Phase 3: Iterative Discovery Interview

**CRITICAL**: Use AskUserQuestion tool for ALL questions—never plain text. If AskUserQuestion is unavailable, present questions in structured markdown with numbered options and wait for user response. For Priority 0 questions when AskUserQuestion is unavailable, the structured markdown MUST include a numbered option for "Planner decides based on recommendation" to satisfy the explicit delegation requirement. If no response after presenting a question: do not proceed with Priority 0 decisions (blocking—after 2 follow-up prompts with no response, inform user: "Planning is blocked pending your decision on [question]. Reply when ready or say 'delegate' to accept the recommendation."); for Priority 1-5, proceed with the recommended option after noting `[USER UNRESPONSIVE: proceeding with recommendation]` in research log.

**Example** (the `questions` array supports 1-4 questions per call—that's batching):
```
questions: [
  {
    question: "Should we build the full implementation or a minimal stub?",
    header: "Phasing",
    options: [
      { label: "Full implementation (Recommended)", description: "Complete feature per spec, production-ready" },
      { label: "Minimal stub", description: "Interface only, implementation deferred" },
      { label: "Incremental", description: "Core first, enhance in follow-up PRs" }
    ],
    multiSelect: false
  },
  {
    question: "Which state management approach?",
    header: "State",
    options: [
      { label: "Extend existing store (Recommended)", description: "Matches codebase pattern in src/store/" },
      { label: "Local component state", description: "Simpler but less shareable" },
      { label: "New dedicated store", description: "Isolated but adds complexity" }
    ],
    multiSelect: false
  }
]
```

### Memento Loop

1. Mark todo `in_progress` (via TodoWrite with status "in_progress")
2. Research (codebase-explorer) OR ask (AskUserQuestion)
3. **Write findings immediately** to research log
4. Expand todos for new questions/integration points/dependencies
5. Update plan (replace `[TBD]`)
6. Mark todo `completed` (via TodoWrite with status "completed")
7. Repeat until no pending todos

**NEVER proceed without writing findings** — research log = external memory.

**If user answer contradicts prior decisions**: (1) Inform user: "This contradicts earlier decision X. Proceeding with new answer." (2) Log in research log under `## Conflicts` with both decisions. (3) Re-evaluate affected todos. (4) Update plan accordingly. If contradiction cannot be resolved, ask user to clarify priority. If user indicates both are equally important or cannot decide, document the contradiction in the research log under `## Unresolved Items`, proceed with the most recently stated answer, and add a risk note: "Unresolved contradiction between [X] and [Y]—implementation follows [most recent]. May need revision."

### Research Log Update Format

```markdown
### {timestamp} - {what}
**Todo**: {which}
**Finding/Answer**: {result}
**Impact**: {what revealed/decided}
**New areas**: {list or "none"}
```

Architecture decisions:
```markdown
- {Area}: {choice} — {rationale}
```

### Todo Expansion Triggers

| Research Reveals | Add Todos For |
|------------------|---------------|
| **Multiple valid implementation locations** | **Approach trade-off analysis → user decision (Priority 0)** |
| **Multiple consumers of modified code** | **Consumer impact analysis → approach implications** |
| Existing similar code | Integration approach |
| Multiple valid patterns | Pattern selection |
| External dependency | Dependency strategy |
| Complex state | State architecture |
| Cross-cutting concern | Concern isolation |
| Performance-sensitive | Performance strategy |
| Migration needed | Migration path |

### Interview Rules

**Unbounded loop**: Iterate until ALL completion criteria met. No fixed round limit. If user says "just decide", "you pick", "I don't care", "skip this", or otherwise explicitly delegates the decision, document remaining decisions with `[INFERRED: {choice} - {rationale}]` markers and finalize. **Priority 0 exception**: Delegation for approach selection requires trade-offs presented first—add explicit option "Planner decides (based on recommendation above)" only after showing alternatives. User cannot delegate Priority 0 without seeing trade-offs.

**User rejects all options**: If user indicates none of the presented options are acceptable, ask follow-up via AskUserQuestion: "What constraints or requirements make these options unsuitable?" Log response in research log under `## Conflicts`, then research alternatives or escalate if none exist.

**Spec-first**: Business scope and requirements belong in spec. Questions here are TECHNICAL only—architecture, patterns, implementation approach. If spec has gaps affecting implementation: (1) flag in research log under `## Spec Gaps`, (2) ask user via AskUserQuestion whether to pause for spec update OR proceed with stated assumption, (3) document choice and continue.

1. **Prioritize questions that eliminate other questions** - Ask questions where the answer changes what other questions you need to ask, or eliminates entire branches of implementation. If knowing X makes Y irrelevant, ask X first.

2. **Interleave discovery and questions**:
   - User answer reveals new area → launch codebase-explorer
   - Need external context (third-party API documentation, external library behavior, industry standards not in codebase) → launch web-researcher via Task tool with subagent_type "vibe-workflow:web-researcher" (if Task tool returns error indicating agent not found, ask user via AskUserQuestion: "I need external context about {topic}. Can you provide: {specific information needed}?")
   - Update plan after each iteration, replacing `[TBD]` markers

3. **Question priority order**:

   | Priority | Type | Purpose | Examples |
   |----------|------|---------|----------|
   | **0** | **Approach Selection** | **Which fundamental approach (see 2.5)** | **Data vs presentation layer? Filter at source vs consumer? Modify existing vs create new?** |
   | 1 | Implementation Phasing | How much to build now vs later | Full impl vs stub? Include migration? Optimize or simple first? |
   | 2 | Branching | Open/close implementation paths | Sync vs async? Polling vs push? In-memory vs persistent? |
   | 3 | Technical Constraints | Non-negotiable technical limits | Must integrate with X? Performance requirements? Backward compatibility? |
   | 4 | Architectural | Choose between patterns | Error strategy? State management? Concurrency model? |
   | 5 | Detail Refinement | Fine-grained technical details | Test coverage scope? Retry policy? Logging verbosity? |

   **Priority 0 is MANDATORY**: If multiple valid approaches exist (per 2.5), you MUST ask before proceeding to Priority 1-5 questions. Approach selection eliminates entire branches of planning—asking Priority 1-5 questions before settling approach wastes effort if user picks different approach. **Exception**: Skip only when all five measurable skip criteria in 2.5 are true. **Dependency exception**: If approach selection depends on a specific technical constraint (Priority 3), ask that constraint question first with context: "Before choosing an approach, I need to understand [constraint] because it determines which approach is viable." Then immediately proceed to approach selection.

4. **Always mark one option "(Recommended)"** - put first with reasoning in description. For Priority 1-5 questions (NOT Priority 0), when options produce the same observable behavior (same inputs yield same outputs, same error handling, same API surface) AND are easily reversible (affects 1-2 files totaling under 100 lines of changes, no modified file is directly imported by >10 other files, no migrations/schema/API changes), decide yourself (lean toward existing codebase patterns).

5. **Be thorough via technique**:
   - Cover technical decisions from each applicable priority category (0-5 in the priority table)—don't skip categories to save time
   - Reduce cognitive load through HOW you ask: concrete options, good defaults
   - **Batching**: Up to 4 questions in `questions` array per call. Only batch questions of the same priority level (e.g., multiple Priority 3 questions) where answers are independent of each other. Never batch Priority 0 with Priority 1-5 questions—Priority 0 must be resolved first as it may eliminate downstream questions. Max 4 options per question (tool limit)
   - Make decisions yourself when codebase research suffices
   - Complete plan with easy questions > incomplete plan with fewer questions

6. **Ask non-obvious questions** - Error handling strategies, edge cases affecting correctness, performance implications, testing approach for complex logic, rollback/migration needs, failure modes

7. **Ask vs Decide** - Codebase patterns and technical standards are authority; user decides trade-offs that affect user-facing or operational outcomes (latency, throughput, resource usage, maintenance burden, API surface area—see table below for categories).

   **Ask user when**:
   | Category | Examples |
   |----------|----------|
   | Trade-offs affecting measurable outcomes | Adds abstraction layer, changes architectural pattern, locks approach for 3+ PRs, changes user-facing behavior, estimated performance change exceeds 2x baseline |
   | No clear codebase precedent | New pattern not yet established |
   | Multiple valid approaches | Architecture choice with different implications |
   | Phasing decisions | Full impl vs stub, migration included or deferred |
   | Breaking changes | API changes, schema migrations |
   | Resource allocation | Cache size, connection pools, batch sizes with cost implications |

   **Decide yourself when**:
   | Category | Examples |
   |----------|----------|
   | Existing codebase pattern | Error format, naming conventions, file structure |
   | Industry standard | HTTP status codes, retry with exponential backoff |
   | Sensible defaults | Timeout 30s, pagination 50 items, debounce 300ms |
   | Easily changed later (affects 1-2 files totaling under 100 lines, no modified file directly imported by >10 others, no migrations/schema/API changes) | Internal function names, log messages, test structure |
   | Implementation detail | Which hook to use, internal state shape, helper organization |
   | Clear best practice | Dependency injection, separation of concerns |

   **Test**: "If I picked wrong, would user say 'that's not what I meant' (ASK) or 'that works, I would have done similar' (DECIDE)?"

## Phase 4: Finalize & Present

### Planning Completion Criteria

Before finalizing, verify ALL criteria are met:

- [ ] **Priority 0 resolved**: Approach decided (single approach documented OR user chose/delegated after trade-offs)
- [ ] **All todos completed**: No pending research or decision todos
- [ ] **Requirements mapped**: Every spec requirement traces to at least one chunk
- [ ] **Risks captured**: Any identified risks logged in research log with mitigations
- [ ] **NFRs addressed**: Security, performance, reliability marked as Required/N/A/Addressed per chunk
- [ ] **Migrations covered**: If schema/API touched, migration and rollback strategy documented

If ANY criterion unmet, do not proceed to 4.1—resolve first.

### 4.1 Final research log update

```markdown
## Planning Complete
Finished: {timestamp} | Research log entries: {count of ### timestamp sections} | Architecture decisions: {count}
## Summary
{Key decisions}
```

### 4.2 Refresh context

Read the full research log file to restore all findings, decisions, and rationale into context before writing the final plan.

### 4.3 Finalize plan

Remove `[TBD]`, ensure chunk consistency, verify dependency ordering, add line ranges for files over 500 lines (500 is the threshold where context becomes unwieldy—for shorter files, full-file reads are acceptable).

### 4.4 Mark all todos complete

### 4.5 Present summary

```
## Plan Summary

**Plan file**: /tmp/plan-{...}.md

### What We're Building
{1-2 sentences}

### Chunks ({count})
1. {Name} - {description}

### Key Decisions
- {Decision}: {choice}

### Execution Order
{Dependencies, parallel opportunities}

---
Review full plan. Adjust or approve to start.
```

### 4.6 Wait for approval

Do NOT implement until user explicitly approves. After approval: create todos from chunks, execute.

---

# Planning Methodology

## 1. Principles

| Principle | Description |
|-----------|-------------|
| **Safety** | Never skip gates (type checks, tests, lint); every chunk tests+demos independently |
| **Clarity** | Full paths, numbered chunks, rationale for context files, line ranges |
| **Minimalism** | Ship today's requirements; parallelize where possible |
| **Forward focus** | Don't prioritize backward compatibility for internal code changes (code used only within the same module/package and not imported by code outside that module); public API/schema changes (any exported function, type, or schema consumed by code outside the module, OR any documented API) always require migration per P8 |
| **Cognitive load** | Deep modules with simple interfaces > many shallow; reduce choices |
| **Conflicts** | Safety (gates: type checks pass, lint clean) > P1 (Correctness: tests pass, chunk works as specified) > Clarity > Minimalism > Forward focus > P2-P10 in order. Note: Safety = code compiles and is formatted; P1 = code is functionally correct |

**Definitions**:
- **Gates**: Quality checks every chunk must pass—type checks (0 errors), tests (pass), lint (clean)
- **Mini-PR**: A chunk sized to be its own small pull request—complete, mergeable, reviewable independently
- **Deep modules**: Modules that hide complexity behind simple interfaces (few public methods, rich internal logic)

### Code Quality (P1-P10)

User's explicit intent takes precedence for implementation choices (P2-P10). P1 (Correctness) and Safety gates (type checks 0 errors, tests pass, lint clean) are non-negotiable—if user requests skipping these, flag as risk but do not skip.

| # | Principle | Planning Implication |
|---|-----------|---------------------|
| P1 | Correctness | Every chunk must demonstrably work |
| P2 | Observability | Plan logging, error visibility |
| P3 | Illegal States Unrepresentable | Design types preventing compile-time bugs |
| P4 | Single Responsibility | Each chunk ONE thing |
| P5 | Explicit Over Implicit | Clear APIs, no hidden behaviors |
| P6 | Minimal Surface Area | YAGNI—don't add features beyond spec |
| P7 | Tests | Specific cases, not "add tests" |
| P8 | Safe Evolution | Public API/schema changes need migration |
| P9 | Fault Containment | Plan failure isolation, retry/fallback |
| P10 | Comments Why | Document logic why (not what) when: algorithm requires domain knowledge beyond the programming language (e.g., mathematical formulas, protocol specs), business rule source is external, or code intentionally deviates from typical patterns |

P1-P10 apply to code quality within chunks. See Conflicts row in principles table for full priority order.

**Values**: Mini-PR > monolithic; parallel > sequential; function-level > code details; dependency clarity > implicit coupling; ship-ready > half-built

## 2. Mini-PR Chunks

Each chunk must:
1. Ship complete value (demo independently—meaning the chunk's functionality can be verified without requiring subsequent chunks: for logic/service chunks via automated tests that pass, for API chunks via a working endpoint callable via curl/Postman, for UI chunks via component rendering correctly in isolation or with mocked dependencies)
2. Pass all gates (type checks, tests, lint)
3. Be mergeable alone (1-3 functions, under 200 lines of code—200 lines is the threshold where a single chunk becomes difficult to review in one sitting)
4. Include its tests (name specific inputs/scenarios, e.g., "valid email accepts user@domain.com", "invalid rejects missing @")

## 3. Chunk Sizing

| Complexity | Chunks | Guidance |
|------------|--------|----------|
| Simple | 1-2 | 1-3 functions each |
| Medium | 3-5 | Under 200 lines of code per chunk |
| Complex | 5-8 | Each verifiable via its own tests |
| Integration | +1 final | Connect prior work |

**Decision guide**: New model/schema → types chunk first | 4+ files or 6+ functions → split by concern | Complex integration → foundation then integration | One module under 200 lines of code → single chunk OK

## 4. Dependency Ordering

- **True dependencies**: uses types, calls functions, extends
- **False dependencies**: same feature, no interaction (parallelize these)
- Minimize chains: A→B and A→C, then B,C→D (not A→B→C→D)
- Circular dependencies: If chunks form a cycle (A needs B, B needs C, C needs A), extract shared interfaces/types into a new foundation chunk that breaks the cycle
- Number chunks; mark parallel opportunities

## 5. What Belongs

| Belongs | Does Not Belong |
|---------|-----------------|
| Numbered chunks, gates, todo descriptions | Code snippets |
| File manifests with reasons | Extra features, future-proofing |
| Function names only | Micro-optimizations, assumed knowledge |

## 6. Cognitive Load

- Deep modules first: fewer with simple interfaces, hide complexity
- Minimize indirection: layers only for concrete extension
- Composition root: one wiring point
- Decide late: abstraction only when PR needs extension
- Framework at edges: core logic agnostic, thin adapters
- Reduce choices: one idiomatic approach per concern
- Measure: if understanding the chunk's purpose requires reading 4+ files or tracing 6+ function calls, simplify it (these thresholds reflect typical human cognitive load limits for holding multiple concepts simultaneously)

## 7. Common Patterns

| Pattern | Flow |
|---------|------|
| Sequential | Model → Logic → API → Error handling |
| Parallel after foundation | Model → CRUD ops (parallel) → Integration |
| Pipeline | Types → Parse/Transform (parallel) → Format → Errors |
| Authentication | User model → Login → Auth middleware → Logout |
| Search | Data structure → Algorithm → API → Ranking |

## 8. Plan Template

```markdown
# IMPLEMENTATION PLAN: [Feature]

[1-2 sentences]

Gates: Type checks (0 errors), Tests (pass), Lint (clean)

---

## Approach Decision (Priority 0)
- **Chosen**: {approach}
- **Alternatives considered**: {list with brief trade-offs}
- **Rationale**: {why chosen}
- **Revisit if**: {conditions that would change decision}

---

## Requirement Coverage
- [Spec requirement] → Chunk N
- [Spec requirement] → Chunk M, Chunk N

---

## 1. [Name]

Depends on: - | Parallel: -

[What this delivers]

Files to modify:
- path.ts - [changes]

Files to create:
- new.ts - [purpose]

Context files:
- reference.ts - [why relevant]

Notes: [Assumptions, risks, alternatives]

Tasks:
- Implement fn() - [purpose]
- Tests - [cases]
- Run gates

Acceptance criteria:
- Gates pass
- [Specific verifiable criterion]

Key functions: fn(), helper()
Types: TypeName
```

### Good Example

```markdown
## 2. Add User Validation Service

Depends on: 1 (User types) | Parallel: 3

Implements email/password validation with rate limiting.

Files to modify:
- src/services/user.ts - Add validateUserInput()

Files to create:
- src/services/validation.ts - Validation + rate limiter

Context:
- src/services/auth.ts:45-80 - Existing validation patterns
- src/types/user.ts - User types from chunk 1

Tasks:
- validateEmail() - RFC 5322
- validatePassword() - Min 8, 1 number, 1 special
- rateLimit() - 5 attempts/min/IP
- Tests: valid email, invalid formats, password edges, rate limit
- Run gates

Acceptance criteria:
- Gates pass
- validateEmail() rejects invalid formats, accepts valid RFC 5322
- validatePassword() enforces min 8, 1 number, 1 special
- Rate limiter blocks after 5 attempts/min/IP

Functions: validateUserInput(), validateEmail(), rateLimit()
Types: ValidationResult, RateLimitConfig
```

### Bad Example

```markdown
## 2. User Stuff
Add validation for users.
Files: user.ts
Tasks: Add validation, Add tests
```

**Why bad**: No dependencies, vague description, missing full paths, no context files, generic tasks, no functions listed, no acceptance criteria.

## 9. File Manifest & Context

- Every file to modify/create; specify changes and purpose
- Full paths; zero prior knowledge assumed
- Context files: explain WHY; line ranges for files over 500 lines

## 10. Quality Criteria

| Level | Criteria |
|-------|----------|
| Good | Each chunk ships value; dependencies ordered; parallel identified; files explicit; context has reasons; tests in todos; gates listed |
| Excellent | + optimal parallelization, line numbers, clear integration, risks, alternatives, reduces cognitive load |

### Quality Checklist

**MUST verify**:
- [ ] Correctness: boundaries, null/empty, error paths
- [ ] Type Safety: types prevent invalid states; validation at boundaries
- [ ] Tests: critical + error + boundary paths

**SHOULD verify**:
- [ ] Observability: errors logged with context
- [ ] Resilience: timeouts, retries with backoff, cleanup
- [ ] Clarity: descriptive names, no magic values
- [ ] Modularity: single responsibility, under 200 lines of code, minimal coupling
- [ ] Evolution: public API/schema changes have migration

### Test Importance (separate scale from P1-P10)

| Score (1-10) | What | Requirement |
|--------------|------|-------------|
| 9-10 | Data mutations, money, auth, state machines | MUST |
| 7-8 | Business logic, API contracts, errors | SHOULD |
| 5-6 | Edge cases, boundaries, integration | GOOD |
| 1-4 | Trivial getters, pass-through | OPTIONAL |

### Error Handling

For external systems/user input, specify:
1. What can fail
2. How failures surface
3. Recovery strategy

Avoid: empty catch, catch-return-null, silent fallbacks, broad catching.

## 11. Problem Scenarios

| Scenario | Action |
|----------|--------|
| No detailed requirements | Research → core requirements/constraints unclear: ask via AskUserQuestion OR stop → non-critical: assume+document |
| Extensive requirements | MUSTs first → research scope → ask priority trade-offs → defer SHOULD/MAY |
| **Multiple approaches** | **STOP. Document trade-offs per 2.5 → ASK user (Priority 0) → proceed only after decision. Never assume "obvious" approach is correct.** |
| Everything dependent | Start from types → question each dependency → find false dependencies → foundation → parallel → integration |

## Planning Mantras

**Memento (always):**
1. Write findings BEFORE next step (research log = external memory)
2. Every discovery needing follow-up → todo
3. Update research log after EACH step

**Primary:**
4. Smallest shippable increment?
5. Passes all gates?
6. Explicitly required?
7. Passes review first submission?

**Secondary:**
8. Ship with less?
9. Dependencies determine order?
10. Researched first, asked strategically?
11. Reduces cognitive load?
12. Satisfies P1-P10?
13. Error paths planned?

### Never Do

- Proceed without writing findings
- Keep discoveries as mental notes
- Skip todos
- Write to project directories (always `/tmp/`; if permission denied, ask user for alternative directory)
- Expand product scope (that's spec phase)—clarification limited to: (1) meeting the 2-requirement minimum per 2.1, or (2) resolving ambiguity that blocks approach selection or chunk definition
- Finalize with `[TBD]`
- Implement without approval
- Forget expanding todos on new areas
- **Commit to any approach without first checking for alternatives and their trade-offs (Priority 0)**
- **Dive into implementation details (Priority 1-5 questions) before approach is decided**
- **Modify data-layer code without analyzing who consumes it and whether they expect current behavior**

## Recognize & Adjust

| Symptom | Action |
|---------|--------|
| Chunk over 200 lines of code | Split by concern |
| No clear value | Merge or refocus |
| Dependencies unclear | Make explicit, number |
| Context missing | Add files + line numbers |
| **After Phase 2.6 (initial draft written), realize alternative approach exists** | **STOP. Go back to 2.5. Document approaches, ask user, may need to restart with chosen approach** |
| **Picked "obvious" location without checking consumers** | **STOP. Grep for usages. If multiple consumers with different needs, this is a Priority 0 question** |
| **User explicitly rejects approach or requests different fundamental approach during/after implementation** | **This should have been a Priority 0 question. Document lesson, present alternatives now** |
