---
name: plan
description: Create implementation plans using the Planning Playbook methodology. Use when user asks to "plan", "create a plan", "make a plan", or needs a structured implementation roadmap. ALSO use by default when in Planning Mode, even if user doesn't mention "plan". Do NOT use if user explicitly requests "execplan" or "exec plan".
---

Create an implementation plan using the Planning Playbook methodology.

If the user specifically requests "execplan", use the execplan skill instead.

## Planning Workflow

Planning is optional but recommended for complex tasks. Follow this workflow:

1. Create plan using the structure template (chunks, dependencies, files)
2. Present via ExitPlanMode tool (even if not in plan mode); if unavailable, present in text format
3. Get explicit user approval
4. Persist the approved plan (unchanged) to `ai-plans/<feature-name>.md` as permanent record
5. Create todos from plan chunks
6. Execute via todo system (not file updates)

## 1. Principles

- **Safety**: Never skip gates; every chunk includes tests and demos independently
- **Clarity**: Full paths, numbered chunks, rationale for context files, line ranges for large files
- **Minimalism**: Prefer 1–3 chunks; ship today's requirements only; parallelize when possible
- **Forward focus**: Do not prioritize backward compatibility by default; only maintain it if explicitly requested or if breaking it would violate system boundaries (in which case, ask the user)
- **Conflicts**: Safety > Clarity > Minimalism > Forward focus
- **Cognitive load**: Ruthlessly minimize extraneous cognitive load across plans, code, and architecture. Prefer deep modules with simple interfaces over many shallow parts; reduce choices; keep the happy path obvious.

**Values**: Mini‑PR chunks over monolithic changes; parallel work streams over sequential waterfalls; function‑level planning over code details; dependency clarity over implicit coupling; ship‑ready increments over half‑built features

## 2. Mini‑PR Chunks

Each chunk must:

1. Ship complete value (demo independently)
2. Pass all gates (type checks, tests, lint)
3. Be mergeable on its own (typically 1–3 functions, <200 LOC)
4. Include its tests (specific cases, not "write tests")

## 3. Chunk Sizing

- **Simple**: 1–2 chunks (1–3 functions each)
- **Medium**: 3–5 chunks (<200 LOC per chunk)
- **Complex**: 5–8 chunks (each demo‑able)
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
- **Not**: code snippets, extra features, future‑proofing, perf tuning, assumed knowledge, implicit files

## 6. Planning Process

1. **Understand**: read provided context and requirements; extract MUSTs and constraints
   - Identify major components and map data flow between them
2. **Clarify ambiguities**: research exhaustively (files, codebase, docs, web), then ask strategic questions if needed
   - Use AskUserQuestion tool (if available, if not - stop and ask in chat)
   - See section 11 for comprehensive guidance on when/how to ask
3. **Map codebase**: list files to touch; pick reference files; explain WHY each helps; add line ranges for large files
4. **Chunk + order**: create mini‑PRs with tests; order by true deps; mark parallel work
5. **Define scope per chunk**: function names/purpose; files to modify/create; context files with WHY; line ranges for large files

## Cognitive Load in Planning

- **Deep modules first**: Aim for fewer, deeper modules with simple, powerful interfaces. Hide complexity inside a module rather than scattering tiny wrappers across files.
- **Minimize indirection**: Only add layers when there's a concrete extension point. Favor dependency inversion over ceremony-heavy architectures.
- **Composition root**: Provide one obvious wiring point (e.g., main composition function, application setup, dependency injection container like `composeApp()` / `registerRoutes()`), so newcomers can read how the system fits together in a single place.
- **Decide late**: Add indirection or abstractions only when this PR needs a concrete extension point. Avoid speculative layers.
- **Framework at the edges**: Keep core business logic framework-agnostic; plan thin adapters at boundaries (HTTP, DB, UI).
- **Reduce choices**: Prefer one idiomatic approach per concern (logging, config, DI). Document the choice in the plan to prevent re-litigating.
- **Measure confusion**: If a reviewer spends >40 minutes confused, simplify the plan or reshape chunk boundaries to reduce concurrent concepts.

## Common Planning Patterns

- **Sequential**: Model → Logic → API → Error handling
- **Parallel after foundation**: Model → CRUD operations (parallel) → Integration
- **Pipeline**: Types → Parse/Transform (parallel) → Format → Error handling
- **Authentication**: User model → Login endpoint → Auth middleware → Logout
- **Search**: Data structure → Search algorithm → API endpoint → Ranking

## 7. Plan Structure Template

Use this structure for all plans - both when presenting for approval and when persisting to files. The approved plan and persisted file should be identical.

```markdown
# IMPLEMENTATION PLAN: [Feature Name]

[1–2 sentences on what we're building]

Gates per chunk: Type checks (0 errors), Tests (pass), Lint (clean)

---

## 1. [Descriptive Name]

Depends on: - | Parallel: -

[What this chunk delivers in 1–2 sentences]

Files to modify:

- apps/.../path.ts – [what changes]

Files to create:

- apps/.../new.ts – [purpose]

Related files for context:

- libs/.../reference.ts – [why relevant]

Notes (optional):

- Assumptions, risks, blockers
- Alternatives considered or rationale
- Links/references useful for implementation
- Anything else to help implementor if meaningful and non-trivial

Implementation tasks:

- Implement functionName() – [purpose]
- Tests – [cases]
- Run gates

Key functions: functionName(), helper()
Types: TypeName
```

## 8. Output Discipline

**Before presenting plans:**

- Follow the Planning Process (section 6): understand → clarify ambiguities → map → chunk → scope
- Resolve strategic ambiguities through research + questions (see section 11 for guidance)
- Document remaining assumptions explicitly in plan notes

**Plan presentation:**

- Always use ExitPlanMode tool to present plans (even if not in plan mode)
- If ExitPlanMode is not available, present plan in text format following the structure template
- Only present after ambiguities are resolved or documented
- Do not write files during planning phase
- Plans must follow the template structure identically whether presented for approval or persisted to files
- Do not include code in the plan; function names only
- ALWAYS wait for explicit user approval before implementation
- After plan iterations/feedback, still wait for user's explicit signal to start implementation (e.g., "proceed", "implement", "start coding")
- After approval: persist the approved plan (unchanged) to `ai-plans/<descriptive-feature-name>.md` as permanent record
- Create todos from approved plan chunks (one todo per chunk minimum)
- Do not commit ai-plans/ files unless explicitly requested
- Do not commit code chunks; the user will commit if approved
- Track execution via todo system, not file updates

## 9. File Manifest & Context Selection

- List every file to modify/create; specify what changes and purpose
- Assume zero prior knowledge; include full paths
- For context files, explain WHY each is relevant; include line ranges for >500‑line files

## 10. Plan Quality Criteria

- **Good**: each chunk ships value; deps ordered; parallel work identified; files explicit; context has reasons; tests in todos; gates listed
- **Excellent**: adds optimal parallelization, line numbers for large files, clear integration points, risk notes, alternatives, and explicitly reduces extraneous cognitive load (deep modules, simple interfaces, minimal layers)

## 11. Problem Scenarios & Strategic Clarification

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

### When to use strategic questions

**DO ask** (after research) when:

- Multiple architecturally significant paths exist with different trade-offs
- Scope unclear and materially affects chunk count/structure
- Technology choice lacks precedent and impacts system design
- Business context needed (speed vs quality, MVP vs complete, cost vs performance)
- User expectations ambiguous (UX patterns, error handling strategy, edge cases)
- Breaking change would violate system boundaries or affect external consumers (ask if backward compatibility is needed; default is to proceed without it)

**DON'T ask** (proceed with research-informed decision):

- Established patterns exist in codebase (follow them)
- Implementation details that don't affect public APIs
- Minor library/tool choices with similar capabilities
- Standard best practices well-documented
- Tactical decisions that can be adjusted later without architectural changes

**Question format** (when AskUserQuestion available):

- 1-4 questions maximum per planning session
- Present options clearly with trade-offs
- Use multiSelect when choices aren't mutually exclusive
- Keep headers short (<12 chars); questions focused; descriptions informative

**Fallback** (when tool unavailable):

- Stop planning immediately when strategic question arises
- Explain situation and options clearly in chat
- Wait for user response before resuming planning
- Resume from where you left off after clarification

## Planning Mantras

Before finalizing:

1. What's the smallest shippable increment?
2. Does it pass all quality gates?
3. Can we ship with less?
4. Is this explicitly required?
5. Do dependencies determine order?
6. Have I researched first, then asked strategically?
7. Does this reduce or increase cognitive load?

## Recognize & Adjust

- Chunk too big (>200 LOC)? Split by concern
- No clear value? Merge or refocus
- Dependencies unclear? Make explicit and number
- Context missing? Add related files with line numbers

---

Gather requirements from the user, then follow this methodology to create the plan.
