---
description: Multi-model ensemble consultation. Invokes the consultant agent with one or more models in parallel. Defaults to 3 models (gpt-5-pro, gemini/gemini-3-pro-preview, claude-opus-4-5-20251101) for diverse perspectives.
---

Perform a consultation using the consultant agent with multiple models in parallel for ensemble diversity.

## Default Models

**CRITICAL: If the user does NOT explicitly specify model(s) in $ARGUMENTS, use ALL 3 default models:**

- `gpt-5-pro`
- `gemini/gemini-3-pro-preview`
- `claude-opus-4-5-20251101`

Only use different models if the user explicitly names them.

## Implementation Note

Use the Task tool with `subagent_type='consultant:consultant'`. Pass the user's request below as the consultant prompt, specifying multi-model consultation with the default models above (unless user specified otherwise). The agent will handle parallel execution, polling, and output relay.

---

# Consultant Prompt

$ARGUMENTS
