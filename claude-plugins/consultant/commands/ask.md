---
description: Single-model consultation. Sends a prompt to the consultant agent using one model. Defaults to gpt-5-pro if no model is specified.
---

Perform a consultation using the consultant agent with a single model. Simple and direct - take the user's question and get an answer.

## What to Do

Invoke the consultant agent to run analysis with one LLM model:

1. Take the user's request from $ARGUMENTS
2. Construct a prompt for the analysis
3. Invoke the consultant CLI with the specified (or default) model
4. Monitor the session until completion
5. Save the output to a file
6. Relay the output verbatim

## Default Model

**If the user does NOT explicitly specify a model, use:**

- **OpenAI**: `gpt-5-pro`

Only use a different model if the user explicitly names one (e.g., "use claude-opus-4-5-20251101 to..." or "ask gemini/gemini-3-pro-preview about...").

**How to detect if user specified a model:**
- User DID specify: "use gpt-5.1", "with claude-opus", "ask gemini/gemini-3-pro-preview"
- User DID NOT specify: "what does this code do", "explain the architecture", "how should I refactor this"

When in doubt, use gpt-5-pro.

## Output

Provide:

- **Verbatim analysis**: The model's complete response exactly as returned
- **Metadata**: Model name, reasoning effort, tokens consumed, cost
- **Saved file path**: `/tmp/consultant-ask-<slug>-<timestamp>/consultant_response.md`

## Important Notes

- **Always use gpt-5-pro unless user explicitly specifies otherwise**
- Relay the output **verbatim**
- Run CLI in background mode for efficiency
- Poll session every 30 seconds until completion

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'`. The agent will:

1. Run `--help` on the CLI to learn current arguments
2. **Check if user specified a model** - if NOT, use default: `gpt-5-pro`
3. Gather context and construct the prompt from $ARGUMENTS
4. **Launch CLI call in background mode** (`run_in_background: true`)
5. **Poll session every 30 seconds** using BashOutput until completion
6. Save output to a file
7. Relay output with file path back to user


## User Request
$ARGUMENTS
