---
description: Production-level PR review using consultant-consulter agent. Provides severity-tagged findings, regression test guidance, and security validation using any LiteLLM-compatible model. Supports custom base URLs and automatic model selection.
---

# Consultant Review Command

## Usage

```bash
/consultant-review [PR_REF=origin/main...feature-branch] [MODEL=model-name] [BASE_URL=http://localhost:8000]
```

## Parameters

- `PR_REF` (optional): Git reference for the PR diff (default: origin/master...HEAD)
- `MODEL` (optional): Specific LLM model to use (default: auto-select best model)
- `BASE_URL` (optional): Custom LiteLLM base URL (default: use default provider)

## What It Does

This command invokes the consultant-consulter agent to perform a comprehensive PR review using powerful LLM models via LiteLLM. The agent will:

1. Gather all changed files and generate extensive diffs
2. Organize code into prioritized attachments
3. Construct a detailed review prompt
4. Invoke consultant Python CLI with all context
5. Monitor the session until completion
6. Synthesize findings into actionable recommendations

## Output

The review provides:

- **Severity-tagged findings**: BLOCKER, HIGH, MEDIUM, LOW, INFO
- **File references**: Exact locations with line numbers
- **Specific fixes**: Actionable recommendations
- **Regression tests**: Test scenarios to prevent issues
- **Overall risk assessment**: Production readiness evaluation

## Examples

### Basic Usage

```bash
/consultant-review
```

Reviews current branch against origin/master using default settings.

### Custom PR Reference

```bash
/consultant-review PR_REF=origin/develop...feature/my-feature
```

Reviews specific branch comparison.

### Specify Model

```bash
/consultant-review MODEL=claude-3-5-sonnet-20241022
```

Uses specific Claude model for review.

### Custom LiteLLM Server

```bash
/consultant-review BASE_URL=http://localhost:8000
```

Uses local LiteLLM instance with automatic model selection.

### Full Configuration

```bash
/consultant-review PR_REF=origin/main...feature/auth MODEL=gpt-4o BASE_URL=http://localhost:8000
```

Reviews specific PR using specific model from custom server.

## Environment Variables

- `LITELLM_API_KEY` or `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: API key for the provider
- `CONSULTANT_MODEL`: Default model if not specified in command
- `CONSULTANT_BASE_URL`: Default base URL if not specified in command

## When to Use

**Perfect for:**

- Pre-merge PR reviews for production deployments
- Security vulnerability assessments
- Architectural validation of large changes
- Performance impact analysis
- Compliance and best practice checks

**Not needed for:**

- Simple typo fixes or documentation updates
- Single-file changes you can review yourself
- Changes already reviewed by multiple senior engineers
- Non-critical experimental branches

## What Gets Reviewed

The consultant-consulter agent analyzes:

1. **Core Logic**: Business rules, algorithms, state machines
2. **Schemas/Types**: Database schemas, API contracts, type definitions
3. **Tests**: Test coverage, test quality, edge case handling
4. **Infrastructure**: Migrations, config changes, deployment scripts
5. **Security**: Auth changes, data validation, injection risks
6. **Performance**: Query patterns, caching, algorithm complexity

## Review Focus Areas

1. **Correctness**: Logic errors, edge cases, invalid states
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

## Session Management

The consultant-consulter agent runs the consultation asynchronously. You can:

- View progress in real-time (agent waits for completion)
- Check session status: `python3 {consultant_scripts_path}/oracle_cli.py session <slug>`
- Review output file after completion

## Troubleshooting

**Issue**: "Context limit exceeded"

**Solution**: The consultant CLI will report this clearly. Reduce the number of files or use a model with larger context (e.g., claude-3-opus with 200k tokens).

**Issue**: "No API key provided"

**Solution**: Set one of: `LITELLM_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`

**Issue**: "Model not found"

**Solution**: Check available models: `python3 {consultant_scripts_path}/oracle_cli.py models --base-url {your_url}`

## Implementation

This command invokes the Task tool with `subagent_type='consultant-consulter'` and provides the PR reference, model, and base URL as context.
