---
description: Multi-model ensemble consultation. Invokes the consultant agent with 3 different models in parallel for diverse perspectives. Default models are gpt-5-pro, gemini-3-pro-preview, and claude-opus-4-5-20251101.
---

# Counsil Command

Performs a multi-model ensemble consultation using the consultant agent with 3 different vendor models in parallel.

## What It Does

Invokes the consultant agent to run the same analysis across 3 different LLM providers simultaneously:

1. Gathers context based on the user's request
2. Constructs a single prompt for the analysis
3. Invokes the consultant CLI **in parallel** with 3 different models
4. Monitors all sessions until completion
5. Saves each model's output to a separate file
6. Relays all outputs verbatim without comparison or synthesis

## Default Models

The following models are used by default (one from each major vendor for ensemble diversity):

- **OpenAI**: `gpt-5-pro`
- **Google**: `gemini-3-pro-preview`
- **Anthropic**: `claude-opus-4-5-20251101`

Users can override these by specifying different models in their request.

## Output

For each model, you receive:

- **Verbatim analysis**: The model's complete response exactly as returned
- **Metadata**: Model name, reasoning effort, tokens consumed, cost
- **Saved file path**: `/tmp/consultant-review-<slug>-<timestamp>/consultant_response_<model>.md`

## When to Use

**Perfect for:**

- Getting diverse perspectives on complex architectural decisions
- Cross-validating security findings across different model families
- Reducing bias by comparing independent analyses
- High-stakes reviews where consensus matters
- Exploring different reasoning approaches to the same problem

**Not needed for:**

- Simple, straightforward analyses
- Time-sensitive reviews (parallel calls still take time)
- When you trust a single model's judgment
- Cost-sensitive scenarios (3x the API calls)

## Usage

```
/counsil Review this PR for security vulnerabilities
/counsil Analyze the architecture of this authentication system
/counsil Investigate the root cause of this bug
```

To use different models:

```
/counsil Use gpt-4-turbo, claude-sonnet-4, and gemini-2.0-flash to review this code
```

## Important Notes

- The consultant agent will **NOT** compare or synthesize results
- Each model's output is relayed **verbatim**
- You (the user) draw conclusions from the ensemble
- All 3 CLI calls run in parallel for efficiency

## Environment Variables

Requires API keys for all 3 providers:

- `OPENAI_API_KEY`: For GPT models
- `GOOGLE_API_KEY` or `GEMINI_API_KEY`: For Gemini models
- `ANTHROPIC_API_KEY`: For Claude models

## Implementation

This command invokes the Task tool with `subagent_type='consultant:consultant'` for a multi-model consultation. The agent will:

1. Run `--help` on the CLI to learn current arguments
2. Gather context and construct the prompt
3. Invoke the CLI **in parallel** with all 3 models (or user-specified models)
4. Monitor all sessions until completion
5. Save each output to a separate file
6. Relay all outputs with file paths back to user
