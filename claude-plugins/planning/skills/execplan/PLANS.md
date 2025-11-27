# Execution Plans (ExecPlans):

This document describes the requirements for an execution plan ("ExecPlan"), a design document that a coding agent can follow to deliver a working feature or system change. Treat the reader as a complete beginner to this repository: they have only the current working tree and the single ExecPlan file you provide. There is no memory of prior plans and no external context.

## How to use ExecPlans and PLANS.md

When authoring an executable specification (ExecPlan), follow PLANS.md _to the letter_. If it is not in your context, refresh your memory by reading the entire PLANS.md file. Be thorough in reading (and re-reading) source material to produce an accurate specification. When creating a spec, start from the skeleton and flesh it out as you do your research.

When implementing an executable specification (ExecPlan), do not prompt the user for "next steps"; simply proceed to the next milestone. Keep each chunk section up to date—add or split chunks at natural stopping points so the plan always reflects the remaining work. Resolve ambiguities autonomously, and structure work into frequent commit-sized increments; do not run git commands unless explicitly requested by the user.

ExecPlans rely on small, independent chunks. Each chunk must be demonstrably shippable and pass the quality gates in order—Typecheck → Tests → Lint—before you mark it complete. Treat this document as the sole planning surface; do not maintain a separate todo list while an ExecPlan is active. When a chunk changes state or scope, update its status line and task checklist in the plan immediately.

When discussing an executable specification (ExecPlan), record decisions in a log in the spec for posterity; it should be unambiguously clear why any change to the specification was made. ExecPlans are living documents, and it should always be possible to restart from _only_ the ExecPlan and no other work.

When researching a design with challenging requirements or significant unknowns, use milestones to implement proof of concepts, "toy implementations", etc., that allow validating whether the user's proposal is feasible. Read the source code of libraries by finding or acquiring them, research deeply, and include prototypes to guide a fuller implementation.

## Requirements

NON-NEGOTIABLE REQUIREMENTS:

- Every ExecPlan must be fully self-contained. Self-contained means that in its current form it contains all knowledge and instructions needed for a novice to succeed.
- Every ExecPlan is a living document. Contributors are required to revise it as progress is made, as discoveries occur, and as design decisions are finalized. Each revision must remain fully self-contained.
- Every ExecPlan must enable a complete novice to implement the feature end-to-end without prior knowledge of this repo.
- Every ExecPlan must produce a demonstrably working behavior, not merely code changes to "meet a definition".
- Every ExecPlan must define every term of art in plain language or do not use it.
- Implementation work must never commit or push changes; leave all version-control actions to the user unless they explicitly request otherwise.
- Backward compatibility is not required by default for internal implementation details. Prefer straightforward migrations over compatibility layers unless otherwise specified.
- Caveat: Public boundaries must remain backward compatible by default (HTTP controller request/response signatures, database entity schemas and migrations, and exported library functions/types). Breaking these requires explicit user approval and a clear migration path.
- Keep scope contained and bias toward the simplest, well-architected, non-hackish solution that achieves the goal. Avoid ambitious expansions by default; prefer the smallest change that satisfies acceptance using good practices.

Purpose and intent come first. Begin by explaining, in a few sentences, why the work matters from a user's perspective: what someone can do after this change that they could not do before, and how to see it working. Then guide the reader through the exact steps to achieve that outcome, including what to edit, what to run, and what they should observe.

The agent executing your plan can list files, read files, search, run the project, and run tests. It does not know any prior context and cannot infer what you meant from earlier milestones. Repeat any assumption you rely on. Do not point to external blogs or docs; if knowledge is required, embed it in the plan itself in your own words. If an ExecPlan builds upon a prior ExecPlan and that file is checked in, incorporate it by reference. If it is not, you must include all relevant context from that plan.

## Formatting

Format and envelope are simple and strict. Each ExecPlan must be one single fenced code block labeled as `md` that begins and ends with triple backticks. Do not nest additional triple-backtick code fences inside; when you need to show commands, transcripts, diffs, or code, present them as indented blocks within that single fence. Use indentation for clarity rather than code fences inside an ExecPlan to avoid prematurely closing the ExecPlan's code fence. Use two newlines after every heading, use # and ## and so on, and correct syntax for ordered and unordered lists.

Use a single fenced code block labeled as `md` when embedding an ExecPlan within another document or chat. When writing an ExecPlan to a Markdown (.md) file where the content of the file _is only_ the single ExecPlan, omit the triple backticks.

Write in plain prose for narrative sections. Bulleted lists and checkboxes are encouraged where this document explicitly calls for them (chunk manifests and chunk task checklists). Avoid tables and long enumerations elsewhere. Narrative sections should remain prose-first.

## Guidelines

Self-containment and plain language are paramount. If you introduce a phrase that is not ordinary English ("daemon", "middleware", "RPC gateway", "filter graph"), define it immediately and remind the reader how it manifests in this repository (for example, by naming the files or commands where it appears). Do not say "as defined previously" or "according to the architecture doc." Include the needed explanation here, even if you repeat yourself.

Avoid common failure modes. Do not rely on undefined jargon. Do not describe "the letter of a feature" so narrowly that the resulting code compiles but does nothing meaningful. Do not outsource key decisions to the reader. When ambiguity exists, resolve it in the plan itself and explain why you chose that path. Err on the side of over-explaining user-visible effects and under-specifying incidental implementation details.

Anchor the plan with observable outcomes. State what the user can do after implementation, the commands to run, and the outputs they should see. Acceptance should be phrased as behavior a human can verify ("after starting the server, navigating to [http://localhost:8080/health](http://localhost:8080/health) returns HTTP 200 with body OK") rather than internal attributes ("added a HealthCheck struct"). If a change is internal, explain how its impact can still be demonstrated (for example, by running tests that fail before and pass after, and by showing a scenario that uses the new behavior).

Specify repository context explicitly. Name files with full repository-relative paths, name functions and modules precisely, and describe where new files should be created. If touching multiple areas, include a short orientation paragraph that explains how those parts fit together so a novice can navigate confidently. When running commands, show the working directory and exact command line. When outcomes depend on environment, state the assumptions and provide alternatives when reasonable.

Be idempotent and safe. Write the steps so they can be run multiple times without causing damage or drift. If a step can fail halfway, include how to retry or adapt. If a migration or destructive operation is necessary, spell out backups or safe fallbacks. Prefer additive, testable changes that can be validated as you go.

Validation is not optional. Include instructions to run tests, to start the system if applicable, and to observe it doing something useful. Describe comprehensive testing for any new features or capabilities. Include expected outputs and error messages so a novice can tell success from failure. Where possible, show how to prove that the change is effective beyond compilation (for example, through a small end-to-end scenario, a CLI invocation, or an HTTP request/response transcript). State the exact test commands appropriate to the project’s toolchain and how to interpret their results.

Capture evidence. When your steps produce terminal output, short diffs, or logs, include them inside the single fenced block as indented examples. Keep them concise and focused on what proves success. If you need to include a patch, prefer file-scoped diffs or small excerpts that a reader can recreate by following your instructions rather than pasting large blobs.

## Code Quality Principles

Plans must produce code that passes rigorous review. Apply these principles when designing chunks. **All principles are guidelines, not laws—the user's explicit intent always takes precedence.** If the user deliberately requests an approach that violates a principle, respect that decision.

| # | Principle | Planning Implication |
|---|-----------|----------------------|
| **P1** | **Correctness Above All** | Every chunk must demonstrably work. Include validation steps that prove correct behavior, not just compilation. |
| **P2** | **Diagnostics & Observability** | Plan logging, error visibility, and traceability from the start. Silent failures are unacceptable—plan explicit error handling. |
| **P3** | **Make Illegal States Unrepresentable** | Design types and interfaces that prevent bugs at compile-time. Plan type definitions before implementations. |
| **P4** | **Single Responsibility** | Each chunk does ONE thing. If describing a chunk requires "and", split it. |
| **P5** | **Explicit Over Implicit** | Plan clear, predictable APIs. No hidden behaviors or magic. Specify explicit configuration over convention. |
| **P6** | **Minimal Surface Area** | Solve today's problem today. Don't plan for hypothetical futures. YAGNI. |
| **P7** | **Prove It With Tests** | Every chunk includes specific test cases. Untested code is unverified code. |
| **P8** | **Safe Evolution** | Public API/schema changes need migration paths. Internal changes can break freely. |
| **P9** | **Fault Containment** | Plan for failure isolation. One bad input shouldn't crash the system. Include retry/fallback strategies. |
| **P10** | **Comments Tell Why** | Plan documentation for complex logic—why, not what. |

### Quality Checklist for Each Chunk

Before marking a chunk complete, verify:

- [ ] **Correctness**: Logic handles boundaries, null/empty, error paths (not just happy path)
- [ ] **Type Safety**: Types prevent invalid states; validation at boundaries; no `any` escape hatches
- [ ] **Observability**: Errors are logged with context; failures are visible, not silent
- [ ] **Resilience**: External calls have timeouts; retries use backoff; resources are cleaned up
- [ ] **Clarity**: Names are descriptive; no magic values; control flow is explicit
- [ ] **Modularity**: Single responsibility; <200 LOC; minimal coupling
- [ ] **Tests**: Critical paths tested; error paths tested; boundaries tested
- [ ] **Evolution**: Public API/schema changes have migration paths; internal changes break freely

### Test Coverage Priority

Align test planning with review expectations:

| Priority | What | Requirement |
|----------|------|-------------|
| 9-10 | Data mutations, money/finance, auth, state machines | MUST test |
| 7-8 | Business logic branches, API contracts, error paths | SHOULD test |
| 5-6 | Edge cases, boundaries, integration points | GOOD to test |
| 1-4 | Trivial getters, simple pass-through | OPTIONAL |

### Error Handling Requirements

Every chunk touching external systems or user input must specify:

1. **What can fail**: List failure modes explicitly
2. **How failures surface**: Logging, metrics, user-facing messages
3. **Recovery strategy**: Retry, fallback, fail-fast
4. **Resource cleanup**: Connections, handles, locks released

Anti-patterns to avoid in plans:
- Empty catch blocks
- Catch-and-return-null without logging
- Optional chaining hiding bugs (`data?.user?.settings?.theme ?? 'dark'`)
- Broad exception catching hiding unrelated errors

## Chunk sizing and dependency heuristics

- Keep each chunk small enough to ship independently (aim for 1–3 functions or roughly 200 lines of code).
- Identify true dependencies explicitly: if a chunk reuses types or functions produced earlier, list that prerequisite. Avoid long serial chains when siblings can build on the same foundation in parallel.
- Call out parallelizable work so multiple chunks can progress simultaneously without conflict.
- When a chunk carries particular risk or testing emphasis, note it so future readers can adjust boundaries safely.

## Milestones

Milestones are narrative, not bureaucracy. If you break the work into milestones, introduce each with a brief paragraph that describes the scope, what will exist at the end of the milestone that did not exist before, the commands to run, and the acceptance you expect to observe. Keep it readable as a story: goal, work, result, proof. Milestones tell the story; the chunk status lines and task checklists track granular work. Both must exist. Never abbreviate a milestone merely for the sake of brevity, do not leave out details that could be crucial to a future implementation.

Each milestone must be independently verifiable and incrementally implement the overall goal of the execution plan.

## Living plans and design decisions

- ExecPlans are living documents. As you make key design decisions, update the plan to record both the decision and the thinking behind it. Record all decisions in the `Decision Log` section.
- ExecPlans must contain and maintain the `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` sections. These are not optional.
- When you discover optimizer behavior, performance tradeoffs, unexpected bugs, or inverse/unapply semantics that shaped your approach, capture those observations in the `Surprises & Discoveries` section with short evidence snippets (test output is ideal).
- If you change course mid-implementation, document why in the `Decision Log` and reflect the implications in the affected chunk’s status line and task checklist. Plans are guides for the next contributor as much as checklists for you.
- At completion of a major task or the full plan, write an `Outcomes & Retrospective` entry summarizing what was achieved, what remains, and lessons learned.

## Prototyping milestones and parallel implementations

It is acceptable—and often encouraged—to include explicit prototyping milestones when they de-risk a larger change. Examples: adding a low-level operator to a dependency to validate feasibility, or exploring two composition orders while measuring optimizer effects. Keep prototypes additive and testable. Clearly label the scope as “prototyping”; describe how to run and observe results; and state the criteria for promoting or discarding the prototype.

Prefer additive code changes followed by subtractions that keep tests passing. Parallel implementations (e.g., keeping an adapter alongside an older path during migration) are fine when they reduce risk or enable tests to continue passing during a large migration. Describe how to validate both paths and how to retire one safely with tests. When working with multiple new libraries or feature areas, consider creating spikes that evaluate the feasibility of these features _independently_ of one another, proving that the external library performs as expected and implements the features we need in isolation.

## Skeleton of a Good ExecPlan

```md
# <Short, action-oriented description>

This ExecPlan is a living document. Keep each chunk section up to date, and maintain the `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` sections as work proceeds.

If PLANS.md file is checked into the repo, reference the path to that file here from the repository root and note that this document must be maintained in accordance with PLANS.md.

## Purpose / Big Picture

Explain in a few sentences what someone gains after this change and how they can see it working. State the user-visible behavior you will enable.

## Surprises & Discoveries

Document unexpected behaviors, bugs, optimizations, or insights discovered during implementation. Provide concise evidence.

- Observation: …
  Evidence: …

## Decision Log

Record every decision made while working on the plan in the format:

- Decision: …
  Rationale: …
  Date/Author: …

## Outcomes & Retrospective

Summarize outcomes, gaps, and lessons learned at major milestones or at completion. Compare the result against the original purpose.

## Context and Orientation

Describe the current state relevant to this task as if the reader knows nothing. Name the key files and modules by full path. Define any non-obvious term you will use. Do not refer to prior plans.

## Plan of Work

Organize the plan into numbered chunks that each ship an independently verifiable outcome. For every chunk, create a subsection containing the fields below and update them as the work evolves:

### Chunk N – <Short title>

Status: In progress as of 2025-11-02 19:20Z
Depends on: <prior chunks or `-`>
Parallel: <other chunks or `-`>

Outcome:
Describe in 1–2 sentences what behavior exists after this chunk lands.

Files to modify:

- apps/.../file.ts – reason for change (line ranges when helpful)

Files to create:

- libs/.../new-file.ts – purpose and expected contents

Related files for context:

- libs/.../reference.ts – why it is useful to read first

Chunk tasks:

- [ ] (2025-11-02 19:25Z | Pending) Implement `functionName` to ...
- [ ] (2025-11-02 19:40Z | Pending) Add tests covering ...
- [ ] (2025-11-02 19:55Z | Pending) Run gates (Typecheck → Tests → Lint)

Keep each chunk ≤200 lines of code (roughly 1–3 functions). When discoveries require new work, add or split chunks and update their status lines and associated checkboxes so the plan stays accurate.

## Concrete Steps

State the exact commands to run and where to run them (working directory). When a command generates output, show a short expected transcript so the reader can compare. This section must be updated as work proceeds. Do not list `git commit`, `git push`, or similar version-control commands; the user owns those actions.

## Validation and Acceptance

Describe how to start or exercise the system and what to observe. Phrase acceptance as behavior, with specific inputs and outputs. If tests are involved, say "run <project’s test command> and expect <N> passed; the new test <name> fails before the change and passes after>".

## Idempotence and Recovery

If steps can be repeated safely, say so. If a step is risky, provide a safe retry or rollback path. Keep the environment clean after completion.

## Artifacts and Notes

Include the most important transcripts, diffs, or snippets as indented examples. Keep them concise and focused on what proves success.

## Interfaces and Dependencies

Be prescriptive. Name the libraries, modules, and services to use and why. Specify the types, interfaces, classes, and function signatures that must exist at the end of the milestone. Use the naming conventions appropriate to your language and project structure. E.g.:

In src/planner/strategy (with appropriate file extension):

    Define a Planner interface/contract with:
    - plan method that accepts an Observed parameter
    - Returns a collection of Action objects

Clearly state the file path, the contract or type name, and the key method signatures or properties that must exist, using your project's language conventions.
```

If you follow the guidance above, a single, stateless agent -- or a human novice -- can read your ExecPlan from top to bottom and produce a working, observable result. That is the bar: SELF-CONTAINED, SELF-SUFFICIENT, NOVICE-GUIDING, OUTCOME-FOCUSED.

When you revise a plan, you must ensure your changes are comprehensively reflected across all sections, including the living document sections, and you must write a note at the bottom of the plan describing the change and the reason why. ExecPlans must describe not just the what but the why for almost everything.
