---
name: codebase-research
description: 'Comprehensive codebase research methodology for gaining deep understanding of code areas. Use this skill when you need to thoroughly understand a code area before planning, implementing, debugging, or answering questions. Returns structured research with prioritized reading list.'
---

# Codebase Research Skill

Gain MAXIMUM understanding of a code area so you can work confidently without re-exploring the codebase.

## When to Use This Skill

- Before planning implementation of a feature
- Before debugging complex issues
- When onboarding to unfamiliar code areas
- When answering questions about how code works
- Before refactoring to map dependencies
- For any task requiring deep code understanding

## Your Mindset

**Imagine you're preparing for an unknown oral exam about this code area.** You don't know what questions will be asked - they could be about functionality, edge cases, history, limitations, extension points, failure modes, or anything else. You must be prepared to answer ANY question with confidence.

After your analysis, no one will read this code again - they'll rely entirely on your understanding. Incomplete understanding = failed implementation.

## Analytical Methodology

### Phase 1: Exhaustive Discovery
- Find ALL entry points (REST APIs, GraphQL resolvers, UI components, CLI commands, event handlers, scheduled jobs, cron tasks, message consumers)
- Identify configuration files, feature flags, environment variables
- Map the boundaries - what's in scope vs out of scope
- Discover ALL callers and usages, not just the obvious ones

### Phase 2: Deep Understanding
- Follow every execution path to completion (not just happy paths)
- Document every function call with `file:line` references
- Track data transformations: input → intermediate states → output
- Identify all side effects (DB writes, API calls, file I/O, cache updates, events)
- Note conditional branches and their triggering conditions
- **Understand the "why"** - look for comments, commit messages, ADRs that explain decisions

### Phase 3: Error & Edge Case Analysis
- Map ALL error handling paths and fallback behaviors
- Identify failure modes - what can go wrong and how is it handled?
- Find validation logic and constraints
- Note race conditions, concurrency concerns, and ordering dependencies
- Understand retry logic, timeouts, and circuit breakers

### Phase 4: Architecture & Patterns
- Identify architectural layers and responsibilities
- Document design patterns in use (Repository, Factory, Strategy, Observer, etc.)
- Map interfaces and contracts between components
- Note cross-cutting concerns: auth, logging, metrics, caching, transactions
- Understand dependency injection and service resolution

### Phase 5: Test & Coverage Analysis
- Read test files to understand expected behavior
- Identify what's well-tested vs poorly tested
- Note test patterns and conventions used
- Find edge cases that tests reveal

### Phase 6: Gap & Debt Identification
- Find TODOs, FIXMEs, and HACKs in the code
- Identify known limitations and missing features
- Note technical debt and improvement opportunities
- Flag areas that seem fragile or under-documented

## Required Output Format

Your analysis MUST include ALL of the following sections. Be exhaustive.

### 1. Overview & Boundaries
- 2-3 sentence summary of what this code area does
- What it IS responsible for
- What it is NOT responsible for (explicit boundaries)
- Key abstractions and concepts

### 2. Entry Points
```
[TYPE] path/to/file.ext:LINE - Description of entry
```
List EVERY way this code area can be triggered. Be exhaustive.

### 3. Execution Flow
Step-by-step trace with:
- Function signatures and file locations (`file:line`)
- Data shape at each step
- Decision points and their conditions
- Side effects produced

### 4. Architecture Map
- Text-based layer diagram
- Design patterns identified with locations
- Component coupling analysis (what depends on what)
- Architectural decisions and rationale (if documented)

### 5. Key Components
For each significant component:
- **Location**: `file:line_start-line_end`
- **Responsibility**: Single sentence
- **Interface**: Public methods/functions exposed
- **Dependencies**: What it consumes

### 6. Dependencies
**External:**
- Library name, version constraint, usage purpose

**Internal:**
- Module name, import path, integration point

### 7. Data Model & Schemas
- Database tables/collections and their relationships
- Key data structures with field explanations
- API request/response shapes
- State shape and structure (for stateful systems)
- Invariants that must be maintained

### 8. Error Handling & Edge Cases
- Failure modes and how they're handled
- Error propagation paths
- Validation requirements and constraints
- Timeout/retry behavior
- Concurrency and race condition concerns

### 9. Configuration & Runtime Behavior
- Feature flags that affect behavior
- Environment variables
- Config files
- Runtime settings that can change behavior

### 10. Test Coverage
- Existing tests and what they cover
- Test patterns and conventions
- Notable gaps in coverage
- Edge cases revealed by tests

### 11. Known Limitations & Tech Debt
- TODOs, FIXMEs, HACKs found in code
- Known issues or limitations
- Technical debt that affects this area
- Things that "smell" but work

### 12. Documentation References
If relevant docs exist (README, docs/, ADRs, inline comments):
- Quote relevant section headers
- Summarize key constraints
- Note discrepancies between docs and implementation

### 13. Patterns & Conventions
Copy-paste ready code examples showing:
- How to add similar functionality
- Naming conventions in use
- Error handling patterns
- Test patterns

### 14. Gotchas & Constraints
Critical warnings about:
- Things that WILL break if ignored
- Non-obvious dependencies
- Order-sensitive operations
- Timing-sensitive code
- Security considerations

### 15. Change Impact Analysis
- What depends on this code (consumers/callers)
- What this code depends on (providers/dependencies)
- What would break if key interfaces changed
- Coupling hotspots where changes ripple widely
- Safe modification points vs dangerous ones

### 16. Essential Files for Handoff
**CRITICAL SECTION** - Ranked list of files you should read:

```
1. [MUST READ] path/to/core.ext:LINE_START-LINE_END
   WHY: Description of what understanding this provides.

2. [MUST READ] path/to/important.ext:LINE_START-LINE_END
   WHY: What this file reveals about the system.

3. [SHOULD READ] path/to/context.ext:LINE_START-LINE_END
   WHY: Additional context that helps but isn't critical.

4. [REFERENCE] path/to/types.ext:LINE_START-LINE_END
   WHY: Useful for type definitions but can be skimmed.
```

**Priority criteria:**
- **MUST READ**: Core business logic, entry points, central abstractions, config that fundamentally changes behavior
- **SHOULD READ**: Implementation details of key interfaces, related but not central files, tests revealing edge cases
- **REFERENCE**: Type definitions, utility functions, boilerplate/infrastructure

### 17. Open Questions & Uncertainties
Be honest about what you couldn't determine:
- Questions that need answering
- Areas with low confidence
- Things that need verification
- Assumptions you made

## Operating Principles

1. **Be Exhaustive**: Missing information causes implementation failures. When in doubt, include it.

2. **Be Precise**: Always include `file:line` or `file:line_start-line_end`. Vague references are useless.

3. **Understand the "Why"**: Don't just document what code does - understand why it was built this way.

4. **Trace Completely**: Follow code paths to termination. Don't stop at abstraction boundaries.

5. **Surface the Non-Obvious**: Explicit code is self-documenting. Your value is revealing implicit knowledge, hidden dependencies, and gotchas.

6. **Be Honest About Uncertainty**: State confidence levels. Flag what needs verification. Don't pretend to know what you don't.

7. **Optimize for Handoff**: Your output feeds into planning, implementation, or debugging. Structure information so those tasks can proceed confidently without re-exploring.

## Tool Usage

- Use Grep/Glob extensively to find ALL usages and references
- Read test files - they document expected behavior and edge cases
- Check configuration files for runtime behavior modifications
- Look for documentation, ADRs, and meaningful comments
- Examine git history if it helps understand "why" (via Bash)

## Internal Notes

For complex research, maintain internal notes in `/tmp/codebase-research-{topic-slug}-{YYYYMMDD-HHMMSS}.md` to track:
- Files explored and their purposes
- Key findings and patterns discovered
- Questions answered and remaining uncertainties
- Recommended reading list being built

These notes are for your internal tracking only. Your response is the deliverable - it must contain all relevant findings.

## After Analysis

Once you complete the analysis:
1. **Read all MUST READ files** yourself using the Read tool
2. **Read SHOULD READ files** for additional context
3. **Reference files** can be skimmed as needed

Your comprehensive understanding enables confident planning and implementation.
