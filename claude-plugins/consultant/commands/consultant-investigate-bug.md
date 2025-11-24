---
description: Deep bug investigation using consultant-consulter agent. Identifies root causes, traces execution flow, assesses blast radius, and provides concrete fix suggestions with regression test recommendations.
---

# Consultant Investigate Bug Command

Performs deep bug investigation using the consultant-consulter agent.

## What It Does

Invokes the consultant-consulter agent to investigate a bug:

1. Gathers bug symptoms from context or user description
2. Collects relevant files, error logs, and recent changes
3. Traces execution flow from symptom to potential root causes
4. Assesses blast radius and affected systems
5. Invokes the consultant CLI (agent will run --help first to learn current arguments)
6. Provides concrete fix suggestions and regression tests

## Output

The investigation provides:

- **Root Cause Analysis**: Specific file locations and logic errors causing the bug
- **Execution Flow Trace**: Step-by-step path from trigger to failure point
- **Blast Radius Assessment**: What systems, users, and data are affected
- **Fix Recommendations**: Concrete code changes with rationale
- **Regression Test Plan**: Test scenarios to catch similar bugs in the future
- **Metadata**: Model used, reasoning effort, tokens consumed, cost

## What Gets Investigated

The consultant-consulter agent analyzes:

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

## When to Use

**Perfect for:**

- Intermittent bugs that are hard to reproduce
- Production incidents requiring rapid root cause analysis
- Bugs in unfamiliar codebases
- Race conditions and concurrency issues
- Performance degradations with unclear causes
- Security vulnerabilities discovered in production

**Not needed for:**

- Simple syntax errors or typos
- Bugs with obvious fixes (e.g., null pointer with clear source)
- Issues easily debuggable with standard tools
- Bugs already fully understood

## Information Gathering

The agent may gather:

- Recent git commits and changes
- Error logs and stack traces
- Test failure outputs
- Related issues/tickets
- System architecture documentation
- Recent deployments or config changes

**Tip**: Provide as much context as possible about the bug symptoms for best results.

## Environment Variables

The consultant CLI reads these environment variables (run the CLI with --help for full details):
- `LITELLM_API_KEY` or `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: API key for the provider

## Troubleshooting

**Issue**: "Not enough context to investigate"
**Solution**: Provide more details about the bug symptoms or ensure relevant error logs/stack traces are available.

**Issue**: "Context limit exceeded"
**Solution**: Agent will automatically reduce scope and focus on most relevant files.

**Issue**: "No API key provided"
**Solution**: Set one of: `LITELLM_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`

## Implementation

This command invokes the Task tool with `subagent_type='consultant-consulter'` for a bug investigation task. The agent will:
1. Run `--help` on the CLI to learn current arguments
2. Gather bug symptoms and related files
3. Construct an investigation prompt with appropriate role and focus areas
4. Invoke the CLI and parse the structured output
5. Report root cause analysis and fix recommendations with metadata back to user
