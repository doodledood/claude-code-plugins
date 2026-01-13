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

If TodoWrite unavailable: use research log `## Todos` section with markdown checkboxes.

Todos = **areas to research/decide**, not steps. Expand when research reveals: (a) files/modules beyond current todos, (b) 2+ valid patterns with trade-offs, (c) unanalyzed dependencies, (d) questions blocking existing todos.

**Starter seeds**:
```
- [ ] Read/infer spec requirements
- [ ] Codebase research (patterns, files to modify)
- [ ] Approach identification (if >1 valid approach → trade-off analysis → user decision)
- [ ] Architecture decisions (within chosen approach)
- [ ] (expand as research reveals)
- [ ] Read full research log and spec (context refresh before output)
- [ ] Finalize chunks
```

**Evolution example** - "Add real-time notifications":
```
- [x] Read spec → 3 types, mobile+web
- [x] Codebase research → found ws.ts, notification-service.ts, polling in legacy/
- [x] Approach selection → WebSocket vs polling? User chose WebSocket
- [ ] Architecture decisions (within WebSocket approach)
- [ ] Offline storage (IndexedDB vs localStorage)
- [ ] Sync conflict resolution
- [ ] Service worker integration
- [ ] Read full research log and spec (context refresh)
- [ ] Finalize chunks
```

Note: Approach selection shows **user decision**—not auto-decided. Found two valid approaches, presented trade-offs, user chose.

**Key**: Never prune todos prematurely. Circular dependencies → merge into single todo: "Research {A} + {B} (merged: circular)".

**Adapt to scope**: Simple (1-2 files) → omit approach identification if single valid approach. Complex (5+ files) → add domain-specific todos.

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

**Prerequisites**: Requires `vibe-workflow:codebase-explorer`. If Task tool fails (timeout >120s, agent not found, incomplete) OR returns <3 files when expecting multi-module changes (spec lists 3+ components OR feature description contains "across/connects/bridges/end-to-end/spans/links/integrates/coordinates/orchestrates"): do supplementary research with Read/Glob/Grep, note `[SUPPLEMENTED RESEARCH: codebase-explorer insufficient - {reason}]`. Don't retry timeouts.

**If all research fails**: Log `[RESEARCH BLOCKED: {reason}]`, ask user via AskUserQuestion: (a) proceed with assumptions or (b) pause for manual context.

### 2.1 Read/infer spec

Extract: requirements, user stories, acceptance criteria, constraints, out-of-scope.

**No formal spec?** Infer from conversation. If <2 concrete requirements (concrete = verifiable by test/demo/metric), ask user: "I need at least 2 concrete requirements. Please provide: [missing items]".

### 2.2 Launch codebase-explorer

Task tool with `subagent_type: "vibe-workflow:codebase-explorer"`. Launch multiple in parallel for cross-cutting work (spans modules/layers, e.g., frontend+backend or auth+logging).

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

**CRITICAL**: Before implementation details, identify whether multiple valid approaches exist. This is THE question that cuts option space—answering it eliminates entire planning branches.

Valid approach = (1) fulfills all spec requirements, (2) technically feasible, (3) has at least one "When it wins" condition. Don't present invalid approaches.

**When**: After initial research (2.2-2.4), before any implementation details.

**What counts as multiple approaches**: different architectural layers, implementation patterns (eager/lazy, push/pull), integration points (modify existing vs create new), scopes (filter at source vs consumer). Multiple valid locations = multiple approaches; multiple valid patterns = multiple approaches.

**Process**:
1. From research: Where could this live? How implemented? Who consumes what we're modifying?
2. **One valid approach** → document why in log, proceed
3. **Multiple valid** → STOP until user decides

**Trade-off format** (research log `## Approach Trade-offs`):
```markdown
### Approaches: {what deciding}

**Approach A: {name}**
- How: {description}
- Pros: {list}
- Cons: {list}
- When it wins: {conditions}
- Affected consumers: {list}

**Approach B: {name}**
- How: {description}
- Pros: {list}
- Cons: {list}
- When it wins: {conditions}
- Affected consumers: {list}

**Existing codebase pattern**: {how similar solved}
**Recommendation**: {approach} — {why}
**Choose alternative if**: {honest conditions where other approach wins}
```

**AskUserQuestion**:
```
questions: [{
  question: "Which approach for {requirement}?",
  header: "Approach",
  options: [
    { label: "{Recommended} (Recommended)", description: "{Why cleanest}. Choose unless {alt wins}." },
    { label: "{Alternative}", description: "{What offers}. Better if {wins}." }
  ],
  multiSelect: false
}]
```

**Recommendation = cleanest**: (1) separation of concerns (if unsure: use layer where similar features live), (2) matches codebase patterns, (3) minimizes blast radius, (4) most reversible. Prioritize 1>2>3>4.

**Be honest**: State clearly when alternative wins. User has context you don't (future plans, team preferences, business constraints).

**Skip asking only when**: genuinely ONE valid approach (document why others don't work) OR ALL five measurable skip criteria true:
1. Same files changed by both
2. No consumer behavior change
3. Reversible in <1 chunk (<200 lines)
4. No schema/API/public interface changes
5. No different error/failure modes

If ANY fails → Priority 0, ask user.

### 2.6 Write initial draft

**Precondition**: Approach decided (single documented OR user chose/delegated after trade-offs). Don't write until Priority 0 resolved.

First draft with `[TBD]` markers. Same file path for all updates.

## Phase 3: Iterative Discovery Interview

**CRITICAL**: Use AskUserQuestion for ALL questions—never plain text. If unavailable: structured markdown with numbered options. For Priority 0 without AskUserQuestion: MUST include "Planner decides based on recommendation" option.

**No response handling**: Priority 0 = blocking (after 2 follow-ups: "Planning blocked pending decision. Reply or say 'delegate'."); Priority 1-5 = proceed with recommendation, note `[USER UNRESPONSIVE: proceeding with recommendation]`.

**Example** (1-4 questions per call):
```
questions: [
  {
    question: "Full implementation or minimal stub?",
    header: "Phasing",
    options: [
      { label: "Full implementation (Recommended)", description: "Complete per spec" },
      { label: "Minimal stub", description: "Interface only, defer impl" },
      { label: "Incremental", description: "Core first, enhance later" }
    ],
    multiSelect: false
  }
]
```

### Memento Loop

1. Mark todo `in_progress`
2. Research (codebase-explorer) OR ask (AskUserQuestion)
3. **Write findings immediately** to research log
4. Expand todos for new questions/dependencies
5. Update plan (replace `[TBD]`)
6. Mark todo `completed`
7. Repeat until no pending todos

**NEVER proceed without writing findings** — research log = external memory.

**Contradictions**: (1) Inform user: "Contradicts earlier X. Proceeding with new answer." (2) Log under `## Conflicts`. (3) Re-evaluate todos. (4) Update plan. Unresolvable → ask priority; still blocked → log under `## Unresolved Items`, proceed with most recent, add risk note.

**Log format**:
```markdown
### {timestamp} - {what}
**Todo**: {which}
**Finding/Answer**: {result}
**Impact**: {revealed/decided}
**New areas**: {list or "none"}
```

Architecture decisions: `- {Area}: {choice} — {rationale}`

### Todo Expansion Triggers

| Research Reveals | Add Todos For |
|------------------|---------------|
| **Multiple valid locations** | **Approach trade-off → user decision (P0)** |
| **Multiple consumers** | **Consumer impact → approach implications** |
| Existing similar code | Integration approach |
| Multiple valid patterns | Pattern selection |
| External dependency | Dependency strategy |
| Complex state | State architecture |
| Cross-cutting concern | Concern isolation |
| Performance-sensitive | Performance strategy |
| Migration needed | Migration path |

### Interview Rules

**Unbounded loop**: Iterate until ALL completion criteria met. User delegates ("just decide", "you pick") → document with `[INFERRED: {choice} - {rationale}]`. **Priority 0 exception**: Delegation requires trade-offs shown first with explicit "Planner decides" option. User cannot delegate P0 without seeing trade-offs.

**User rejects all**: Ask "What constraints make these unsuitable?" Log under `## Conflicts`, research alternatives.

**Spec-first**: Questions here are TECHNICAL only. Spec gaps → flag in `## Spec Gaps`, ask user: pause for update OR proceed with assumption.

1. **Prioritize questions that eliminate others** - If knowing X makes Y irrelevant, ask X first

2. **Interleave discovery and questions**: User answer reveals new area → codebase-explorer; need external context → web-researcher via Task (subagent_type: "vibe-workflow:web-researcher"; if unavailable: ask user "Need context about {topic}. Provide: {specific info}"); update plan after each iteration

3. **Question priority**:

| Priority | Type | Purpose | Examples |
|----------|------|---------|----------|
| **0** | **Approach Selection** | **Which fundamental approach** | **Data vs presentation layer? Filter at source vs consumer?** |
| 1 | Phasing | How much now vs later | Full vs stub? Include migration? |
| 2 | Branching | Open/close paths | Sync vs async? Polling vs push? |
| 3 | Technical Constraints | Non-negotiable limits | Must integrate with X? Performance reqs? |
| 4 | Architectural | Choose patterns | Error strategy? State management? |
| 5 | Detail Refinement | Fine-grained details | Test coverage? Retry policy? |

**Priority 0 MANDATORY**: If multiple valid approaches exist → ask before P1-5. **Exception**: Skip only when ALL five skip criteria true. **Dependency exception**: If P0 depends on P3 constraint, ask constraint first with context, then immediately P0.

4. **Always mark "(Recommended)"** first with reasoning. For P1-5 (NOT P0): if same observable behavior AND easily reversible (<100 lines, <5 importers, no migrations) → decide yourself.

5. **Be thorough via technique**: Cover all applicable priority categories; batch up to 4 related same-priority questions; never batch P0 with P1-5

6. **Non-obvious questions**: Error handling, edge cases, performance, testing approach, rollback/migration, failure modes

7. **Ask vs Decide**:

   **Ask when**: Trade-offs affecting outcomes (adds abstraction, changes pattern, locks 3+ PRs, user-facing change, >20% perf change), no codebase precedent, multiple valid approaches, phasing, breaking changes, resource allocation

   **Decide when**: Existing pattern, industry standard, sensible defaults, easily changed (1-2 files, <100 lines, <5 importers, no migrations), implementation detail, clear best practice

   **Test**: "Would user say 'not what I meant' (ASK) or 'works, similar' (DECIDE)?"

## Phase 4: Finalize & Present

### Completion Criteria

Before finalizing, ALL must be met:
- [ ] Priority 0 resolved (single approach OR user chose/delegated after trade-offs)
- [ ] All todos completed
- [ ] Requirements mapped to chunks
- [ ] Risks captured with mitigations
- [ ] NFRs addressed per chunk (Required/N/A/Addressed)
- [ ] Migrations covered if schema/API touched

If ANY unmet → resolve first.

### 4.1 Final research log update

```markdown
## Planning Complete
Finished: {timestamp} | Entries: {count} | Decisions: {count}
## Summary
{Key decisions}
```

### 4.2 Refresh context

Read full research log to restore findings, decisions, rationale before final plan.

### 4.3 Finalize plan

Remove `[TBD]`, ensure chunk consistency, verify dependency ordering, add line ranges for files >500 lines.

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
| **Safety** | Never skip gates (type checks, tests, lint); each chunk tests+demos independently |
| **Clarity** | Full paths, numbered chunks, rationale for context files, line ranges |
| **Minimalism** | Ship today's requirements; parallelize where possible |
| **Forward focus** | Internal code: no backward compat priority; public API/schema: always require migration |
| **Cognitive load** | Deep modules with simple interfaces > many shallow |
| **Conflicts** | Safety (compiles+formatted) > P1 (correct) > Clarity > Minimalism > Forward focus > P2-P10 |

**Definitions**:
- **Gates**: type checks (0 errors), tests (pass), lint (clean)
- **Mini-PR**: chunk sized for independent PR—complete, mergeable, reviewable
- **Deep modules**: few public methods, rich internal logic

### Code Quality (P1-P10)

User intent takes precedence for P2-P10. P1 and Safety gates are non-negotiable.

| # | Principle | Implication |
|---|-----------|-------------|
| P1 | Correctness | Chunk must demonstrably work |
| P2 | Observability | Plan logging, error visibility |
| P3 | Illegal States Unrepresentable | Types prevent compile-time bugs |
| P4 | Single Responsibility | Each chunk ONE thing |
| P5 | Explicit Over Implicit | Clear APIs, no hidden behaviors |
| P6 | Minimal Surface Area | YAGNI |
| P7 | Tests | Specific cases, not "add tests" |
| P8 | Safe Evolution | Public API/schema → migration |
| P9 | Fault Containment | Failure isolation, retry/fallback |
| P10 | Comments Why | Document why when: domain knowledge, external business rule, intentional deviation |

**Values**: Mini-PR > monolithic; parallel > sequential; function-level > code details; dependency clarity > implicit coupling; ship-ready > half-built

## 2. Mini-PR Chunks

Each chunk must:
1. Ship complete value (demo independently without subsequent chunks: logic via tests, API via curl, UI via isolated render)
2. Pass all gates
3. Be mergeable alone (1-3 functions, <200 lines)
4. Include tests (specific inputs/scenarios)

## 3. Chunk Sizing

| Complexity | Chunks | Guidance |
|------------|--------|----------|
| Simple | 1-2 | 1-3 functions each |
| Medium | 3-5 | <200 lines per chunk |
| Complex | 5-8 | Each verifiable via tests |
| Integration | +1 final | Connect prior work |

**Decision guide**: New schema → types first | 4+ files/6+ functions → split by concern | Complex integration → foundation then integration | <200 lines → single chunk OK

## 4. Dependency Ordering

- **True**: uses types, calls functions, extends
- **False**: same feature, no interaction → parallelize
- Minimize chains: A→B, A→C, then B,C→D (not A→B→C→D)
- Circular → extract shared interfaces into foundation chunk
- Number chunks; mark parallel opportunities

## 5. What Belongs

| Belongs | Does Not |
|---------|----------|
| Numbered chunks, gates, todos | Code snippets |
| File manifests with reasons | Extra features, future-proofing |
| Function names only | Micro-optimizations, assumed knowledge |

## 6. Cognitive Load

- Deep modules first: fewer with simple interfaces
- Minimize indirection: layers only for concrete extension
- Composition root: one wiring point
- Decide late: abstraction only when needed
- Framework at edges: core agnostic, thin adapters
- Reduce choices: one idiomatic approach per concern
- Measure: if understanding requires 4+ files or 6+ calls → simplify

## 7. Common Patterns

| Pattern | Flow |
|---------|------|
| Sequential | Model → Logic → API → Errors |
| Parallel after foundation | Model → CRUD (parallel) → Integration |
| Pipeline | Types → Parse/Transform (parallel) → Format → Errors |
| Authentication | User model → Login → Middleware → Logout |
| Search | Structure → Algorithm → API → Ranking |

## 8. Plan Template

```markdown
# IMPLEMENTATION PLAN: [Feature]

[1-2 sentences]

Gates: Type checks (0 errors), Tests (pass), Lint (clean)

---

## Approach Decision (Priority 0)
- **Chosen**: {approach}
- **Alternatives**: {list with trade-offs}
- **Rationale**: {why}
- **Revisit if**: {conditions}

---

## Requirement Coverage
- [Requirement] → Chunk N

---

## 1. [Name]

Depends on: - | Parallel: -

[What delivers]

Files to modify:
- path.ts - [changes]

Files to create:
- new.ts - [purpose]

Context:
- ref.ts - [why relevant]

Notes: [Assumptions, risks]

Tasks:
- Implement fn() - [purpose]
- Tests - [cases]
- Run gates

Acceptance:
- Gates pass
- [Specific criterion]

Functions: fn(), helper()
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

Acceptance:
- Gates pass
- validateEmail() rejects invalid, accepts RFC 5322
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

**Why bad**: No dependencies, vague, missing paths, no context, generic tasks, no functions, no acceptance.

## 9. File Manifest & Context

- Every file to modify/create with changes and purpose
- Full paths; zero assumed knowledge
- Context files: explain WHY; line ranges for >500 lines

## 10. Quality Criteria

| Level | Criteria |
|-------|----------|
| Good | Chunks ship value; ordered dependencies; parallel identified; explicit files; context reasons; tests in todos; gates listed |
| Excellent | + optimal parallelization, line numbers, clear integration, risks, alternatives, reduced cognitive load |

### Quality Checklist

**MUST**: Correctness (boundaries, null/empty, errors), Type safety (prevent invalid states, boundary validation), Tests (critical + error + boundary)

**SHOULD**: Observability (errors with context), Resilience (timeouts, retries, cleanup), Clarity (descriptive names), Modularity (<200 lines, minimal coupling), Evolution (public changes have migration)

### Test Importance

| Score | What | Requirement |
|-------|------|-------------|
| 9-10 | Data mutations, money, auth, state machines | MUST |
| 7-8 | Business logic, API contracts, errors | SHOULD |
| 5-6 | Edge cases, boundaries, integration | GOOD |
| 1-4 | Trivial getters, pass-through | OPTIONAL |

### Error Handling

For external systems/user input: (1) what can fail, (2) how failures surface, (3) recovery strategy. Avoid: empty catch, catch-return-null, silent fallbacks, broad catching.

## 11. Problem Scenarios

| Scenario | Action |
|----------|--------|
| No requirements | Research → unclear: ask OR stop → non-critical: assume+document |
| Extensive requirements | MUSTs first → research → ask priority trade-offs → defer SHOULD/MAY |
| **Multiple approaches** | **STOP. Trade-offs per 2.5 → ASK (P0) → proceed after decision. Never assume "obvious".** |
| Everything dependent | Types first → question dependencies → find false ones → foundation → parallel → integration |

## Planning Mantras

**Memento (always)**:
1. Write findings BEFORE next step
2. Every follow-up discovery → todo
3. Update research log after EACH step

**Primary**: 4. Smallest shippable? 5. Passes gates? 6. Explicitly required? 7. Passes review first time?

**Secondary**: 8. Ship with less? 9. Dependencies order? 10. Research first, ask strategically? 11. Reduces cognitive load? 12. Satisfies P1-P10? 13. Error paths planned?

### Never Do

- Proceed without writing findings
- Keep discoveries as mental notes
- Skip todos
- Write to project dirs (always `/tmp/`; if denied: ask for alternative)
- Expand scope (spec phase; exception: 2-req minimum or blocking ambiguity)
- Finalize with `[TBD]`
- Implement without approval
- Forget expanding todos
- **Commit to approach without checking alternatives (P0)**
- **P1-5 before approach decided**
- **Modify data-layer without analyzing consumers**

## Recognize & Adjust

| Symptom | Action |
|---------|--------|
| Chunk >200 lines | Split by concern |
| No clear value | Merge or refocus |
| Dependencies unclear | Make explicit, number |
| Context missing | Add files + line numbers |
| **Alternative approach after draft** | **STOP. Back to 2.5. Document, ask, may restart** |
| **"Obvious" location without checking consumers** | **STOP. Grep usages. Multiple consumers → P0** |
| **User rejects approach during/after impl** | **Should have been P0. Document lesson, present alternatives** |
