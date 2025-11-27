---
description: Deep bug investigation using consultant agent. Identifies root causes, traces execution flow, assesses blast radius, and provides concrete fix suggestions with regression test recommendations.
---

Perform deep bug investigation using the consultant agent.

## What to Do

Invoke the consultant agent to investigate a bug:

1. Gather bug symptoms from context or user description
2. Collect relevant files, error logs, and recent changes
3. Trace execution flow from symptom to potential root causes
4. Assess blast radius and affected systems
5. Invoke the consultant CLI (run --help first to learn current arguments)
6. Provide concrete fix suggestions and regression tests

## Output

Provide:

- **Root Cause Analysis**: Specific file locations and logic errors causing the bug
- **Execution Flow Trace**: Step-by-step path from trigger to failure point
- **Blast Radius Assessment**: What systems, users, and data are affected
- **Fix Recommendations**: Concrete code changes with rationale
- **Regression Test Plan**: Test scenarios to catch similar bugs in the future
- **Metadata**: Model used, reasoning effort, tokens consumed, cost

## What Gets Investigated

Analyze:

1. **Error Context**: Stack traces, error messages, logs
2. **Recent Changes**: Git history, recent commits, PRs that might have introduced the bug
3. **Affected Code**: Files involved in the execution path
4. **Related Systems**: Dependencies, integrations, data flow
5. **Test Coverage**: Existing tests, missing test scenarios
6. **Historical Patterns**: Similar bugs, known issues

## Investigation Focus Areas

1. **Root Cause Identification**: What's actually broken and why
2. **Execution Flow Tracing**: Path from trigger to failure
3. **State Analysis**: Invalid states, race conditions, timing issues
4. **Data Validation**: Input validation gaps, edge cases
5. **Error Handling**: Missing error handlers, improper recovery

## Severity Assessment

- **CRITICAL**: Production down, data corruption, widespread impact
- **HIGH**: Core functionality broken, major user impact
- **MEDIUM**: Feature partially broken, workaround available
- **LOW**: Minor issue, limited impact
- **INFO**: Observation, potential issue, monitoring needed

## Output Format

```
# Bug Investigation Report

## Summary
[One-paragraph overview of root cause]

## Root Cause
- **File**: path/to/file.ts:123-145
- **Issue**: [Specific code/logic problem]
- **Why It Matters**: [Impact and consequences]

## Execution Flow
1. [Step 1: Trigger point]
2. [Step 2: Intermediate state]
3. [Step 3: Failure point]

## Blast Radius
- **Affected Systems**: [List of impacted systems]
- **Affected Users**: [User segments impacted]
- **Data Impact**: [Any data integrity concerns]

## Recommended Fix
[Specific code changes with rationale]

## Regression Test Plan
- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Edge case validation
```

## Information Gathering

Gather:

- Recent git commits and changes
- Error logs and stack traces
- Test failure outputs
- Related issues/tickets
- System architecture documentation
- Recent deployments or config changes

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'` for a bug investigation task. The agent will:
1. Run `--help` on the CLI to learn current arguments
2. Gather bug symptoms and related files
3. Construct an investigation prompt with appropriate role and focus areas
4. Invoke the CLI and parse the structured output
5. Report root cause analysis and fix recommendations with metadata back to user
