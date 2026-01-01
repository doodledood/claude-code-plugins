---
name: plan
description: 'Create implementation plans from a spec through iterative codebase research and strategic questions. Produces mini-PR based plans optimized for iterative development.'
---

# Plan Skill

Build implementation plan through structured discovery. Takes spec (from `/spec` or inline) and iteratively researches codebase + asks strategic questions to produce detailed plan.

**Focus on HOW, not WHAT**: Spec defines what to build. This skill defines how - architecture, files, functions, chunks, dependencies, tests.

**Loop**: Research → Expand todos → Ask questions → Write findings → Repeat until complete

**Plan file**: `/tmp/plan-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - updated after each iteration.

**Research log**: `/tmp/plan-research-{name-kebab-case}-{YYYYMMDD-HHMMSS}.md` - external memory.

## Boundaries

- Spec defines requirements; this skill defines architecture, files, chunks, tests
- Don't modify spec; flag gaps for user
- If research reveals infeasibility, surface to user before proceeding
- Stay focused on planning; don't implement until approved

## Phase 1: Initial Setup

### 1.1 Create todo list (TodoWrite immediately)

Todos = **areas to research/decide**, not planning steps. Each todo reminds you what architectural question needs resolution. List is **never fixed** - continuously expands as research reveals complexity.

**Starter todos** (just seeds - actual list grows organically):

```
- [ ] Read/infer spec requirements
- [ ] Codebase research (existing patterns, files to modify)
- [ ] Architecture decisions
- [ ] (expand continuously as research reveals new areas)
- [ ] Finalize chunks
```

### Todo Evolution Example

Spec: "Add real-time notifications"

Initial:
```
- [ ] Read spec requirements
- [ ] Codebase research
- [ ] Architecture decisions
- [ ] Finalize chunks
```

After researching codebase, found existing WebSocket setup:
```
- [x] Read spec requirements → 3 notification types, mobile + web
- [ ] Codebase research
- [ ] WebSocket integration approach (extend existing vs new)
- [ ] Architecture decisions
- [ ] Finalize chunks
```

After user says "needs to work offline too":
```
- [x] Read spec requirements
- [x] Codebase research → found ws.ts, notification-service.ts
- [x] WebSocket integration approach → extend existing
- [ ] Architecture decisions
- [ ] Offline storage strategy (IndexedDB vs localStorage)
- [ ] Sync conflict resolution
- [ ] Service worker integration
- [ ] Finalize chunks
```

**Key**: Todos grow as research reveals complexity. Never prune prematurely.

### 1.2 Create research log

Path: `/tmp/plan-research-{name-kebab-case}-{YYYYMMDD-HHMMSS}.md` (use SAME path for ALL updates)

```markdown
# Research Log: {feature name}
Started: {timestamp} | Spec: {spec file path or "inline"}

## Codebase Research
(populated incrementally)

## Architecture Decisions
(populated incrementally)

## Questions & Answers
(populated incrementally)

## Unresolved Items
(populated incrementally)
```

## Phase 2: Context Gathering

### 2.1 Read or infer spec

Read spec file path if provided, or use inline spec content.

**If no formal spec**: Infer requirements from conversation history, tool/agent outputs, or user request itself. Many planning sessions start from reviews, bug reports, or ad-hoc requests.

Extract: requirements, user stories, acceptance criteria, constraints, out of scope.

### 2.2 Launch codebase-explorer

Use Task tool with `subagent_type: "vibe-workflow:codebase-explorer"` to find exact files/patterns for THIS spec. Launch multiple in parallel (single message) for cross-cutting work.

Explore: existing implementations, files to modify, patterns/conventions, integration points, test patterns.

### 2.3 Read recommended files

Read ALL files from researcher prioritized reading lists - no skipping. Gives firsthand knowledge of code patterns, architecture, integration points, test structure.

### 2.4 Update research log

After EACH research step, append to research log:

```markdown
### {timestamp} - {what researched}
- Explored: {areas/topics}
- Key findings: {files, patterns, integration points}
- New areas identified: {list}
- Architectural questions: {list}
```

### 2.5 Write initial draft

Write first draft with `[TBD]` markers for unresolved items. Use same file path for all updates.

## Phase 3: Iterative Discovery Interview

**CRITICAL**: Use AskUserQuestion tool for ALL questions. If unavailable, ask in chat but mark as requiring user input.

### Memento Loop

For each step:
1. Mark todo `in_progress`
2. Research (codebase-explorer) OR ask question (AskUserQuestion)
3. **Write findings immediately** to research log
4. Expand todos for: new architectural questions, integration points, dependencies discovered
5. Update plan file (replace `[TBD]` markers)
6. Mark todo `completed`
7. Repeat until no pending todos

**NEVER proceed without writing findings first** — research log is external memory.

### Research Log Update Format

After EACH research or question, append:

```markdown
### {timestamp} - {what researched/asked}
**Todo**: {which todo this addresses}
**Finding/Answer**: {result}
**Impact on plan**: {what this revealed/decided}
**New areas**: {list or "none"}
```

After EACH architectural decision (even implicit), append to Architecture Decisions:

```markdown
- {Decision area}: {choice} — {rationale}
```

### Todo Expansion Triggers

| Research Reveals | Add Todos For |
|------------------|---------------|
| Existing similar code | Integration approach |
| Multiple valid patterns | Pattern selection |
| External dependency | Dependency strategy |
| Complex state management | State architecture |
| Cross-cutting concern | Concern isolation |
| Performance-sensitive area | Performance strategy |
| Migration needed | Migration path |

### Interview Rules

**Unbounded loop**: Keep iterating (research → question → update plan) until ALL completion criteria are met. No fixed round limit.

1. **Research first, ask strategically** - Exhaust codebase research before asking. Only ask when:
   - Multiple architecturally significant paths with different trade-offs
   - Scope boundaries unclear, materially affecting chunk structure
   - Technology choices lack precedent, impact system design
   - Business context needed (speed vs quality, MVP vs complete)
   - User preferences ambiguous

   **Interleave discovery and questions**: User answer reveals new area → launch codebase-explorer. Update plan after each iteration.

2. **Don't ask when research provides answer**:
   - Established patterns exist (follow them)
   - Standard best practices documented
   - Implementation details don't affect public APIs
   - Minor tool/library choices
   - Tactical decisions adjustable later

3. **Always mark one option "(Recommended)"** - first with reasoning

4. **Be thorough via technique**:
   - Cover everything relevant - don't skip to save time
   - Reduce cognitive load through HOW you ask: concrete options, batching (up to 4), good defaults
   - Make decisions yourself when research suffices
   - Complete plan with easy questions > incomplete plan with fewer questions

5. **Question priority order**:

   | Priority | Type | Examples |
   |----------|------|----------|
   | 1 | Scope Eliminators | V1/MVP vs full? Core flow only? Single vs batch? |
   | 2 | Architectural | Which pattern for X? Sync vs async? Existing vs new? |
   | 3 | Hard Constraints | Must integrate with X? Performance requirements? Backward compatibility? |
   | 4 | Detail Refinement | Error handling? Test coverage? Naming? |

6. **Iterate until complete** - Keep interviewing until architectural decisions made, chunks well-defined, file manifests complete, no `[TBD]` markers.

## Phase 4: Finalize & Present

### 4.1 Final research log update

```markdown
## Planning Complete
Finished: {timestamp} | Research steps: {count} | Decisions: {count}
## Summary
{Brief summary of planning process and key decisions}
```

### 4.2 Finalize plan

Final pass: remove `[TBD]` markers, ensure chunk consistency, verify dependency ordering, add line ranges for large files (>500 lines).

### 4.3 Mark all todos complete

### 4.4 Present summary

```
## Plan Summary

**Plan file**: /tmp/plan-{...}.md

### What We're Building
{1-2 sentences}

### Chunks ({count})
1. {Name} - {one-line description}
...

### Key Decisions
- {Decision}: {choice}

### Execution Order
{Dependencies, parallel opportunities}

---
Review full plan. Adjust anything, or approve to start implementation.
```

### 4.5 Wait for approval

Do NOT start implementation until user explicitly approves. After approval: create todos from chunks, execute via todo system.

---

# Planning Methodology

## 1. Principles

| Principle | Description |
|-----------|-------------|
| **Safety** | Never skip gates; every chunk includes tests and demos independently |
| **Clarity** | Full paths, numbered chunks, rationale for context files, line ranges for large files |
| **Minimalism** | Prefer 1-3 chunks; ship today's requirements only; parallelize when possible |
| **Forward focus** | Don't prioritize backward compatibility unless explicitly requested or system boundaries violated (ask user) |
| **Cognitive load** | Ruthlessly minimize - deep modules with simple interfaces over many shallow parts; reduce choices; keep happy path obvious |
| **Conflicts** | Safety > Clarity > Minimalism > Forward focus |

### Code Quality Principles (P1-P10)

Plans must produce code that passes rigorous review. **All are guidelines - user's explicit intent takes precedence.**

| # | Principle | Planning Implication |
|---|-----------|---------------------|
| P1 | Correctness Above All | Every chunk must demonstrably work. Prove behavior, not compilation. |
| P2 | Diagnostics & Observability | Plan logging and error visibility. No silent failures. |
| P3 | Make Illegal States Unrepresentable | Design types that prevent bugs at compile-time. Types before implementations. |
| P4 | Single Responsibility | Each chunk does ONE thing. If need "and" to describe, split. |
| P5 | Explicit Over Implicit | Clear APIs. No hidden behaviors, magic values, implicit config. |
| P6 | Minimal Surface Area | Solve today's problem. YAGNI. |
| P7 | Prove It With Tests | Specific test cases per chunk, not "add tests". |
| P8 | Safe Evolution | Public API/schema changes need migration paths. Internal changes break freely. |
| P9 | Fault Containment | Plan failure isolation. Include retry/fallback strategies. |
| P10 | Comments Tell Why | Document complex logic - why, not what. |

**Values**: Mini-PR chunks > monolithic; parallel work > sequential waterfalls; function-level planning > code details; dependency clarity > implicit coupling; ship-ready increments > half-built features

## 2. Mini-PR Chunks

Each chunk must:
1. Ship complete value (demo independently)
2. Pass all gates (type checks, tests, lint)
3. Be mergeable alone (typically 1-3 functions, <200 LOC)
4. Include its tests (specific cases)

## 3. Chunk Sizing

| Complexity | Chunks | Guidance |
|------------|--------|----------|
| Simple | 1-2 | 1-3 functions each |
| Medium | 3-5 | <200 LOC per chunk |
| Complex | 5-8 | Each demo-able |
| Integration | +1 final | Connect prior work |

**Decision guide**: New model/schema → start with types chunk | >3 files or >5 functions → split by concern | Complex integration (>5 deps) → foundation then integration | All in one module <200 LOC → single chunk OK

## 4. Dependency Ordering

- **True deps**: uses types, calls functions, extends from another
- **False deps**: same feature but no interaction (parallelize)
- Minimize chains: A→B and A→C, then B,C→D (not A→B→C→D)
- Number chunks; mark parallel opportunities

## 5. What Belongs vs. Not

| Belongs | Not |
|---------|-----|
| Numbered chunks, gates per chunk, todo descriptions | Code snippets |
| File manifests (modify/create/context) with reasons | Extra features, future-proofing |
| Function names only (no code) | Perf tuning, assumed knowledge |

## 6. Cognitive Load in Planning

- **Deep modules first**: Fewer, deeper modules with simple interfaces. Hide complexity inside.
- **Minimize indirection**: Add layers only for concrete extension points.
- **Composition root**: One obvious wiring point (main setup, DI container).
- **Decide late**: Add abstraction only when this PR needs extension point. No speculative layers.
- **Framework at edges**: Core logic framework-agnostic; thin adapters at boundaries.
- **Reduce choices**: One idiomatic approach per concern. Document choice.
- **Measure confusion**: If reviewer >40 min confused, simplify.

## 7. Common Patterns

| Pattern | Flow |
|---------|------|
| Sequential | Model → Logic → API → Error handling |
| Parallel after foundation | Model → CRUD ops (parallel) → Integration |
| Pipeline | Types → Parse/Transform (parallel) → Format → Error handling |
| Authentication | User model → Login → Auth middleware → Logout |
| Search | Data structure → Algorithm → API → Ranking |

## 8. Plan Structure Template

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
- Alternatives, rationale
- Links/references

Implementation tasks:
- Implement functionName() - [purpose]
- Tests - [cases]
- Run gates

Key functions: functionName(), helper()
Types: TypeName
```

### Good Chunk Example

```markdown
## 2. Add User Validation Service

Depends on: 1 (User types) | Parallel: 3

Implements email/password validation with rate limiting before user creation.

Files to modify:
- src/services/user.ts - Add validateUserInput()

Files to create:
- src/services/validation.ts - Validation logic with rate limiter

Related files for context:
- src/services/auth.ts:45-80 - Existing validation patterns
- src/types/user.ts - User type definitions from chunk 1

Implementation tasks:
- Implement validateEmail() - RFC 5322 format check
- Implement validatePassword() - Min 8 chars, 1 number, 1 special
- Implement rateLimit() - 5 attempts/min/IP
- Tests: valid email, invalid formats, password edges, rate limit trigger
- Run gates

Key functions: validateUserInput(), validateEmail(), rateLimit()
Types: ValidationResult, RateLimitConfig
```

### Bad Chunk Anti-Example

```markdown
## 2. User Stuff
Add validation for users.
Files: user.ts
Tasks: Add validation, Add tests
```

**Why bad**: No dependency info, vague description, missing file paths, no context files, generic tasks, no function names, can't execute without clarification.

## 9. File Manifest & Context

- List every file to modify/create; specify what changes and purpose
- Assume zero prior knowledge; full paths
- Context files: explain WHY relevant; line ranges for >500-line files

## 10. Plan Quality Criteria

| Level | Criteria |
|-------|----------|
| Good | Each chunk ships value; deps ordered; parallel identified; files explicit; context has reasons; tests in todos; gates listed |
| Excellent | + optimal parallelization, line numbers for large files, clear integration points, risk notes, alternatives, explicitly reduces cognitive load |

### Quality Checklist per Chunk

**MUST verify (critical):**
- [ ] Correctness: boundaries, null/empty, error paths (not just happy path)
- [ ] Type Safety: types prevent invalid states; validation at boundaries
- [ ] Tests: critical + error paths + boundaries tested

**SHOULD verify:**
- [ ] Observability: errors logged with context; failures visible
- [ ] Resilience: external calls have timeouts; retries with backoff; resource cleanup
- [ ] Clarity: descriptive names; no magic values; explicit control flow
- [ ] Modularity: single responsibility; <200 LOC; minimal coupling
- [ ] Evolution: public API/schema changes have migration paths

### Test Coverage Priority

| Priority | What | Requirement |
|----------|------|-------------|
| 9-10 | Data mutations, money, auth, state machines | MUST test |
| 7-8 | Business logic, API contracts, error paths | SHOULD test |
| 5-6 | Edge cases, boundaries, integration points | GOOD to test |
| 1-4 | Trivial getters, pass-through | OPTIONAL |

### Error Handling in Plans

For chunks touching external systems or user input, specify:
1. What can fail (explicit failure modes)
2. How failures surface (logging, user messages)
3. Recovery strategy (retry, fallback, fail-fast)

Avoid: empty catch, catch-and-return-null, silent fallbacks, broad exception catching.

## 11. Problem Scenarios

| Scenario | Action |
|----------|--------|
| No detailed requirements | Research first → if fundamentals unclear: ask via tool (scope, must-haves, approach) or stop planning → for non-critical details: make assumptions, document |
| Extensive requirements | Extract MUSTs first → research similar scope → if scope ambiguous: ask priority trade-offs → defer SHOULD/MAY explicitly |
| Multiple valid approaches | Research first (codebase patterns, docs, best practices) → ask only when significantly different implications (state mgmt, auth, data modeling, API design) → don't ask when research provides clear answer |
| Everything appears dependent | Start from data model/types → question each assumed dep → look for false deps → truly sequential: foundation → parallel builds → integration |

## Planning Mantras

**Memento (always do):**
1. Write findings BEFORE next research/question (research log = external memory)
2. Every discovery needing follow-up → todo (no mental notes)
3. Update research log after EACH step (not at end)

**Primary (always check):**
4. What's the smallest shippable increment?
5. Does it pass all quality gates?
6. Is this explicitly required?
7. Will this pass code review on first submission?

**Secondary:**
8. Can we ship with less?
9. Do dependencies determine order?
10. Have I researched first, then asked strategically?
11. Does this reduce or increase cognitive load?
12. Does each chunk satisfy P1-P10?
13. Are error paths planned, not afterthoughts?

### Never Do

- Proceed without writing findings to research log
- Keep discoveries as mental notes instead of todos
- Skip todo list
- Write plans to project directories (always `/tmp/`)
- Ask about scope/requirements (that's spec phase)
- Finalize with unresolved `[TBD]`
- Start implementation without explicit approval
- Forget to expand todos on new architectural areas revealed

## Recognize & Adjust

| Symptom | Action |
|---------|--------|
| Chunk >200 LOC | Split by concern |
| No clear value | Merge or refocus |
| Dependencies unclear | Make explicit and number |
| Context missing | Add related files with line numbers |
