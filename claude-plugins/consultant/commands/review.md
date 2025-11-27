---
description: Production-level PR review using consultant agent. Provides severity-tagged findings, regression test guidance, and security validation.
---

Perform a comprehensive PR review using the consultant agent.

## Focus Areas

1. **Correctness**: Logic errors, edge cases, invalid state handling
2. **Security**: Auth bypasses, injection risks, data validation gaps
3. **Reliability**: Error handling, retry logic, graceful degradation
4. **Performance**: N+1 queries, unbounded loops, expensive operations
5. **Maintainability**: Code clarity, test coverage, documentation

## Severity Levels

- **BLOCKER**: Production-breaking, data loss, critical security breach
- **HIGH**: Significant malfunction, major bug, auth weakness
- **MEDIUM**: Edge case bug, performance degradation, maintainability concern
- **LOW**: Minor improvement, style issue, optimization
- **INFO**: Observation, architectural note, informational context

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'` for a PR review task. The agent will gather diffs, construct the review prompt, invoke the CLI, and report findings.
