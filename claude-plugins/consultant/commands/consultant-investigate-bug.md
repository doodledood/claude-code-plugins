---
description: Deep bug investigation using consultant-consulter agent. Identifies root causes, traces execution flow, assesses blast radius, and provides concrete fix suggestions with regression test recommendations using any LiteLLM-compatible model.
---

# Consultant Investigate Bug Command

## Usage

```bash
/consultant-investigate-bug [SYMPTOM="error description"] [MODEL=model-name] [BASE_URL=http://localhost:8000]
```

## Parameters

- `SYMPTOM` (optional): Bug symptom or error message (if not provided, agent will infer from context)
- `MODEL` (optional): Specific LLM model to use (default: auto-select best model)
- `BASE_URL` (optional): Custom LiteLLM base URL (default: use default provider)

## What It Does

This command invokes the consultant-consulter agent to perform deep bug investigation using powerful LLM models via LiteLLM. The agent will:

1. Gather bug symptoms from context or user description
2. Collect relevant files and recent changes
3. Trace execution flow from symptom to potential root causes
4. Assess blast radius and affected systems
5. Provide concrete fix suggestions
6. Recommend regression tests to prevent recurrence

## Output

The investigation provides:

- **Root Cause Analysis**: Specific file locations and logic errors
- **Execution Flow Trace**: Step-by-step path from symptom to source
- **Blast Radius Assessment**: What systems and users are affected
- **Fix Recommendations**: Concrete code changes with rationale
- **Regression Test Plan**: Test scenarios to catch similar bugs

## Examples

### Basic Usage

```bash
/consultant-investigate-bug
```

Analyzes context (recent errors, test failures, conversation) to infer bug.

### Explicit Symptom

```bash
/consultant-investigate-bug SYMPTOM="API returns 500 on user profile update with error: Cannot read property 'id' of undefined"
```

Investigates specific error message.

### Custom Model

```bash
/consultant-investigate-bug SYMPTOM="Race condition in order processing" MODEL=claude-3-5-sonnet-20241022
```

Uses specific Claude model for investigation.

### Custom LiteLLM Server

```bash
/consultant-investigate-bug BASE_URL=http://localhost:8000
```

Uses local LiteLLM instance with automatic model selection.

## What Gets Investigated

The consultant-consulter agent analyzes:

1. **Error Context**: Stack traces, error messages, logs
2. **Recent Changes**: Git history, recent commits, PRs
3. **Affected Code**: Files involved in execution path
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

## Environment Variables

- `LITELLM_API_KEY` or `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: API key for the provider
- `CONSULTANT_MODEL`: Default model if not specified in command
- `CONSULTANT_BASE_URL`: Default base URL if not specified in command

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

**Tip**: Provide as much context as possible in the SYMPTOM parameter for best results.

## Session Management

The consultant-consulter agent runs the investigation asynchronously. You can:

- View progress in real-time (agent waits for completion)
- Check session status: `python3 {consultant_scripts_path}/oracle_cli.py session <slug>`
- Review investigation report after completion

## Troubleshooting

**Issue**: "Not enough context to investigate"

**Solution**: Provide more details in SYMPTOM parameter or ensure relevant error logs/stack traces are in conversation context.

**Issue**: "Context limit exceeded"

**Solution**: Investigation is gathering too much code. Agent will automatically reduce scope and focus on most relevant files.

**Issue**: "No API key provided"

**Solution**: Set one of: `LITELLM_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`

## Implementation

This command invokes the Task tool with `subagent_type='consultant-consulter'` and provides the bug symptom, model, and base URL as context. The agent adapts its workflow for bug investigation vs PR review.
