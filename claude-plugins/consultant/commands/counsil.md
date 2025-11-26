---
description: Multi-model ensemble consultation. Invokes the consultant agent with one or more models in parallel. Defaults to 3 models (gpt-5-pro, gemini/gemini-3-pro-preview, claude-opus-4-5-20251101) for diverse perspectives.
---

# Counsil Command

Performs a consultation using the consultant agent with one or more models. By default, runs 3 different vendor models in parallel for ensemble diversity.

## What It Does

Invokes the consultant agent to run the same analysis across one or more LLM models:

1. Gathers context based on the user's request
2. Constructs a single prompt for the analysis
3. Invokes the consultant CLI with the specified model(s) - runs in parallel if multiple
4. Monitors all sessions until completion
5. Saves each model's output to a separate file
6. Relays all outputs verbatim without comparison or synthesis

## Default Models

**CRITICAL: If the user does NOT explicitly specify model(s) in their request, you MUST use ALL 3 default models:**

- **OpenAI**: `gpt-5-pro`
- **Google**: `gemini/gemini-3-pro-preview`
- **Anthropic**: `claude-opus-4-5-20251101`

Only use different models if the user explicitly names them (e.g., "use gpt-5.1 to review" or "use claude-sonnet-4-5 and gemini/gemini-2.5-flash").

**How to detect if user specified models:**
- User DID specify: "use gpt-5.1", "with claude-opus", "using gemini/gemini-3-pro-preview and gpt-5"
- User DID NOT specify: "review this PR", "analyze the architecture", "investigate this bug"

When in doubt, use all 3 default models.

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

Default (3 models):

```
/counsil Review this PR for security vulnerabilities
/counsil Analyze the architecture of this authentication system
/counsil Investigate the root cause of this bug
```

Single model:

```
/counsil Use claude-opus-4-5-20251101 to review this code
```

Custom models:

```
/counsil Use gpt-5-pro, claude-opus-4-5-20251101, and gemini/gemini-3-pro-preview to review this code
```

## Important Notes

- **Always use 3 default models unless user explicitly specifies otherwise**
- The consultant agent will **NOT** compare or synthesize results
- Each model's output is relayed **verbatim**
- You (the user) draw conclusions from the results
- All CLI calls run in background mode and in parallel for efficiency
- Sessions are polled every 30 seconds until completion

## Environment Variables

Requires API keys for the providers you're using:

- `OPENAI_API_KEY`: For GPT models
- `GOOGLE_API_KEY` or `GEMINI_API_KEY`: For Gemini models
- `ANTHROPIC_API_KEY`: For Claude models

For the default 3-model ensemble, all 3 keys are required.

## Implementation

This command invokes the Task tool with `subagent_type='consultant:consultant'`. The agent will:

1. Run `--help` on the CLI to learn current arguments
2. **Check if user specified models** - if NOT, use all 3 defaults: `gpt-5-pro`, `gemini/gemini-3-pro-preview`, `claude-opus-4-5-20251101`
3. Gather context and construct the prompt
4. **Launch all CLI calls in background mode** (`run_in_background: true`) - one per model, all in parallel
5. **Poll all sessions every 30 seconds** using BashOutput until completion
6. Save each output to a separate file
7. Relay all outputs with file paths back to user


## Custom User Instructions
$ARGUMENTS