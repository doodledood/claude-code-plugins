---
description: Single-model consultation. Sends a prompt to the consultant agent using one model. Defaults to gpt-5-pro if no model is specified.
---

Perform a consultation using the consultant agent with a single model.

## Default Model

If the user does NOT explicitly specify a model in $ARGUMENTS, use `gpt-5-pro`.

Only use a different model if the user explicitly names one (e.g., "use claude-opus-4-5-20251101 to..." or "ask gemini/gemini-3-pro-preview about...").

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'`. Pass along the user's request from $ARGUMENTS, specifying that this is a single-model consultation defaulting to gpt-5-pro.

## User Request
$ARGUMENTS
