---
description: 'Create implementation plans from spec via iterative codebase research and strategic questions. Produces mini-PR plans optimized for iterative development.'
argument-hint: Optional - path to spec file
---

**User request**: $ARGUMENTS

# Plan Skill

Build implementation plan through structured discovery. Takes spec (from `/spec` or inline), iteratively researches codebase + asks strategic questions → detailed plan.

**Focus**: HOW not WHAT. Spec=what; this skill=architecture, files, functions, chunks, deps, tests.

**Loop**: Research → Expand todos → Ask questions → Write findings → Repeat until complete

**Output files**:
- Plan: `/tmp/plan-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md`
- Research log: `/tmp/plan-research-{name-kebab-case}-{YYYYMMDD-HHMMSS}.md` (external memory)

## Boundaries

- Spec=requirements; this skill=architecture, files, chunks, tests
- Don't modify spec; flag gaps for user
- Surface infeasibility before proceeding
- No implementation until approved

## Phase 1: Initial Setup

### 1.1 Create todos (TodoWrite immediately)

Todos = **areas to research/decide**, not steps. Continuously expands as research reveals complexity.

**Starter seeds**:
```
- [ ] Read/infer spec requirements
- [ ] Codebase research (patterns, files to modify)
- [ ] Architecture decisions
- [ ] (expand as research reveals new areas)
- [ ] Finalize chunks
```

**Evolution example** - "Add real-time notifications":

Initial → After codebase research (found WebSocket) → After "needs offline too":
```
- [x] Read spec → 3 types, mobile+web
- [x] Codebase research → ws.ts, notification-service.ts
- [x] WebSocket approach → extend existing
- [ ] Architecture decisions
- [ ] Offline storage (IndexedDB vs localStorage)
- [ ] Sync conflict resolution
- [ ] Service worker integration
- [ ] Finalize chunks
```

**Key**: Never prune todos prematurely.

### 1.2 Create research log

Path: `/tmp/plan-research-{name-kebab-case}-{YYYYMMDD-HHMMSS}.md`

```markdown
# Research Log: {feature}
Started: {timestamp} | Spec: {path or "inline"}

## Codebase Research
## Architecture Decisions
## Questions & Answers
## Unresolved Items
```

## Phase 2: Context Gathering

### 2.1 Read/infer spec

Extract: requirements, user stories, acceptance criteria, constraints, out-of-scope.

**No formal spec?** Infer from conversation, tool outputs, user request.

### 2.2 Launch codebase-explorer

Task tool with `subagent_type: "vibe-workflow:codebase-explorer"`. Launch multiple in parallel for cross-cutting work.

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

### 2.5 Write initial draft

First draft with `[TBD]` markers. Same file path for all updates.

## Phase 3: Iterative Discovery Interview

**CRITICAL**: Use AskUserQuestion for ALL questions. Unavailable → ask in chat, mark as requiring user input.

### Memento Loop

1. Mark todo `in_progress`
2. Research (codebase-explorer) OR ask (AskUserQuestion)
3. **Write findings immediately** to research log
4. Expand todos for new questions/integration points/deps
5. Update plan (replace `[TBD]`)
6. Mark todo `completed`
7. Repeat until no pending todos

**NEVER proceed without writing findings** — research log = external memory.

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
| Existing similar code | Integration approach |
| Multiple valid patterns | Pattern selection |
| External dependency | Dependency strategy |
| Complex state | State architecture |
| Cross-cutting concern | Concern isolation |
| Performance-sensitive | Performance strategy |
| Migration needed | Migration path |

### Interview Rules

**Unbounded loop**: Iterate until ALL completion criteria met.

1. **Research first, ask strategically** - Only ask when:
   - Multiple architecturally significant paths with different trade-offs
   - Scope boundaries unclear, affecting chunk structure
   - Technology choices lack precedent
   - Business context needed (speed vs quality, MVP vs complete)
   - User preferences ambiguous

   **Interleave**: User answer reveals new area → codebase-explorer → update plan.

2. **Don't ask when research provides answer**:
   - Established patterns exist
   - Standard best practices documented
   - Implementation details don't affect public APIs
   - Minor tool/library choices
   - Tactical decisions adjustable later

3. **Always mark one option "(Recommended)"** first with reasoning

4. **Be thorough**: Don't skip to save time. Reduce cognitive load via HOW: concrete options, batch ≤4, good defaults. Decide when research suffices. Complete+easy > incomplete+fewer.

5. **Question priority**:
   | Priority | Type | Examples |
   |----------|------|----------|
   | 1 | Scope Eliminators | V1/MVP vs full? Core only? Single vs batch? |
   | 2 | Architectural | Pattern for X? Sync vs async? Existing vs new? |
   | 3 | Hard Constraints | Must integrate with X? Perf requirements? Backward compat? |
   | 4 | Detail Refinement | Error handling? Test coverage? Naming? |

6. **Iterate until complete**: Architectural decisions made, chunks defined, manifests complete, no `[TBD]`.

## Phase 4: Finalize & Present

### 4.1 Final research log update

```markdown
## Planning Complete
Finished: {timestamp} | Research steps: {count} | Decisions: {count}
## Summary
{Key decisions}
```

### 4.2 Finalize plan

Remove `[TBD]`, ensure chunk consistency, verify dependency ordering, add line ranges for files >500 lines.

### 4.3 Mark all todos complete

### 4.4 Present summary

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

### 4.5 Wait for approval

Do NOT implement until user explicitly approves. After approval: create todos from chunks, execute.

---

**User request**: $ARGUMENTS

# Planning Methodology

## 1. Principles

| Principle | Description |
|-----------|-------------|
| **Safety** | Never skip gates; every chunk tests+demos independently |
| **Clarity** | Full paths, numbered chunks, rationale for context files, line ranges |
| **Minimalism** | 1-3 chunks preferred; ship today's requirements; parallelize |
| **Forward focus** | Don't prioritize backward compat unless requested or boundaries violated |
| **Cognitive load** | Deep modules with simple interfaces > many shallow; reduce choices |
| **Conflicts** | Safety > Clarity > Minimalism > Forward focus |

### Code Quality (P1-P10)

User's explicit intent takes precedence.

| # | Principle | Planning Implication |
|---|-----------|---------------------|
| P1 | Correctness | Every chunk must demonstrably work |
| P2 | Observability | Plan logging, error visibility |
| P3 | Illegal States Unrepresentable | Design types preventing compile-time bugs |
| P4 | Single Responsibility | Each chunk ONE thing |
| P5 | Explicit Over Implicit | Clear APIs, no hidden behaviors |
| P6 | Minimal Surface Area | YAGNI |
| P7 | Tests | Specific cases, not "add tests" |
| P8 | Safe Evolution | Public API/schema changes need migration |
| P9 | Fault Containment | Plan failure isolation, retry/fallback |
| P10 | Comments Why | Document complex logic why, not what |

**Values**: Mini-PR > monolithic; parallel > sequential; function-level > code details; dependency clarity > implicit coupling; ship-ready > half-built

## 2. Mini-PR Chunks

Each chunk must:
1. Ship complete value (demo independently)
2. Pass all gates (type checks, tests, lint)
3. Be mergeable alone (1-3 functions, <200 LOC)
4. Include its tests (specific cases)

## 3. Chunk Sizing

| Complexity | Chunks | Guidance |
|------------|--------|----------|
| Simple | 1-2 | 1-3 functions each |
| Medium | 3-5 | <200 LOC per chunk |
| Complex | 5-8 | Each demo-able |
| Integration | +1 final | Connect prior work |

**Decision guide**: New model/schema → types chunk first | >3 files or >5 functions → split by concern | Complex integration → foundation then integration | One module <200 LOC → single chunk OK

## 4. Dependency Ordering

- **True deps**: uses types, calls functions, extends
- **False deps**: same feature, no interaction (parallelize)
- Minimize chains: A→B and A→C, then B,C→D (not A→B→C→D)
- Number chunks; mark parallel opportunities

## 5. What Belongs

| Belongs | Not |
|---------|-----|
| Numbered chunks, gates, todo descriptions | Code snippets |
| File manifests with reasons | Extra features, future-proofing |
| Function names only | Perf tuning, assumed knowledge |

## 6. Cognitive Load

- Deep modules first: fewer with simple interfaces, hide complexity
- Minimize indirection: layers only for concrete extension
- Composition root: one wiring point
- Decide late: abstraction only when PR needs extension
- Framework at edges: core logic agnostic, thin adapters
- Reduce choices: one idiomatic approach per concern
- Measure: reviewer >40 min confused → simplify

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

**User request**: $ARGUMENTS

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

**Why bad**: No deps, vague, missing paths, no context, generic tasks, no functions.

## 9. File Manifest & Context

- Every file to modify/create; specify changes and purpose
- Full paths; zero prior knowledge assumed
- Context files: explain WHY; line ranges for >500 lines

## 10. Quality Criteria

| Level | Criteria |
|-------|----------|
| Good | Each chunk ships value; deps ordered; parallel identified; files explicit; context has reasons; tests in todos; gates listed |
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
- [ ] Modularity: single responsibility, <200 LOC, minimal coupling
- [ ] Evolution: public API/schema changes have migration

### Test Priority

| Priority | What | Requirement |
|----------|------|-------------|
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
| No detailed requirements | Research → fundamentals unclear: ask via tool OR stop → non-critical: assume+document |
| Extensive requirements | MUSTs first → research scope → ask priority trade-offs → defer SHOULD/MAY |
| Multiple approaches | Research first → ask only when significantly different implications |
| Everything dependent | Start from types → question each dep → find false deps → foundation → parallel → integration |

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
9. Deps determine order?
10. Researched first, asked strategically?
11. Reduces cognitive load?
12. Satisfies P1-P10?
13. Error paths planned?

### Never Do

- Proceed without writing findings
- Keep discoveries as mental notes
- Skip todos
- Write to project directories (always `/tmp/`)
- Ask scope/requirements (spec phase)
- Finalize with `[TBD]`
- Implement without approval
- Forget expanding todos on new areas

## Recognize & Adjust

| Symptom | Action |
|---------|--------|
| Chunk >200 LOC | Split by concern |
| No clear value | Merge or refocus |
| Dependencies unclear | Make explicit, number |
| Context missing | Add files + line numbers |
