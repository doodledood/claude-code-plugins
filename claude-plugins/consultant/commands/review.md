---
description: Production-level PR review using consultant agent. Provides severity-tagged findings, regression test guidance, and security validation using any LiteLLM-compatible model.
---

Perform a comprehensive PR review using the consultant agent.

## What to Do

Invoke the consultant agent to perform a thorough code review:

1. Gather all changed files and generate extensive diffs
2. Organize code into prioritized attachments (core logic, schemas, tests, infrastructure)
3. Construct a detailed review prompt with role, context, and focus areas
4. Invoke the consultant CLI (run --help first to learn current arguments)
5. Monitor session until completion
6. Synthesize findings into actionable recommendations with severity tags

## Output

Provide:

- **Severity-tagged findings**: BLOCKER, HIGH, MEDIUM, LOW, INFO
- **File references**: Exact locations with line numbers (path/to/file.ts:123-145)
- **Specific fixes**: Actionable recommendations or validation steps
- **Regression tests**: Test scenarios to prevent issues from recurring
- **Overall risk assessment**: Production readiness evaluation
- **Metadata**: Model used, reasoning effort, tokens consumed, cost

## What Gets Reviewed

Analyze:

1. **Core Logic**: Business rules, algorithms, state machines, domain models
2. **Schemas/Types**: Database schemas, API contracts, type definitions, interfaces
3. **Tests**: Test coverage, test quality, edge case handling, test fixtures
4. **Infrastructure**: Migrations, config changes, deployment scripts
5. **Security**: Auth changes, data validation, injection risks
6. **Performance**: Query patterns, caching, algorithm complexity

## Review Focus Areas

1. **Correctness**: Logic errors, edge cases, invalid state handling
2. **Security**: Auth bypasses, injection risks, data validation gaps
3. **Reliability**: Error handling, retry logic, graceful degradation
4. **Performance**: N+1 queries, unbounded loops, expensive operations
5. **Maintainability**: Code clarity, test coverage, documentation

## Severity Levels

- **BLOCKER**: Production-breaking, data loss, critical security breach (merge should be blocked)
- **HIGH**: Significant malfunction, major bug, auth weakness (should fix before merge)
- **MEDIUM**: Edge case bug, performance degradation, maintainability concern (fix soon)
- **LOW**: Minor improvement, style issue, optimization (can fix later)
- **INFO**: Observation, architectural note, informational context

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'` for a PR review task. The agent will:
1. Run `--help` on the CLI to learn current arguments
2. Gather diffs and organize into prioritized attachments
3. Construct a review prompt with appropriate role and focus areas
4. Invoke the CLI and parse the structured output
5. Report findings with severity tags and metadata back to user
