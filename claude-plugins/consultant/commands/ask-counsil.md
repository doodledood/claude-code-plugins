---
description: Multi-model ensemble consultation. Invokes the consultant agent with one or more models in parallel. Defaults to 3 models (gpt-5-pro, gemini/gemini-3-pro-preview, claude-opus-4-5-20251101) for diverse perspectives.
---

Perform a consultation using the consultant agent with one or more models. By default, run 3 different vendor models in parallel for ensemble diversity.

## What to Do

Invoke the consultant agent to run the same analysis across one or more LLM models:

1. Gather context based on the user's request
2. Construct a single prompt for the analysis
3. Invoke the consultant CLI with the specified model(s) - run in parallel if multiple
4. Monitor all sessions until completion
5. Save each model's output to a separate file
6. Relay all outputs verbatim without comparison or synthesis

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

For each model, provide:

- **Verbatim analysis**: The model's complete response exactly as returned
- **Metadata**: Model name, reasoning effort, tokens consumed, cost
- **Saved file path**: `/tmp/consultant-review-<slug>-<timestamp>/consultant_response_<model>.md`

## Important Notes

- **Always use 3 default models unless user explicitly specifies otherwise**
- Do **NOT** compare or synthesize results - relay each verbatim
- Let the user draw conclusions from the results
- Run all CLI calls in background mode and in parallel for efficiency
- Poll sessions every 30 seconds until completion

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'`. The agent will:

1. Run `--help` on the CLI to learn current arguments
2. **Check if user specified models** - if NOT, use all 3 defaults: `gpt-5-pro`, `gemini/gemini-3-pro-preview`, `claude-opus-4-5-20251101`
3. Gather context and construct the prompt
4. **Launch all CLI calls in background mode** (`run_in_background: true`) - one per model, all in parallel
5. **Poll all sessions every 30 seconds** using BashOutput until completion
6. Save each output to a separate file
7. Relay all outputs with file paths back to user


## Custom User Instructions
$ARGUMENTS
