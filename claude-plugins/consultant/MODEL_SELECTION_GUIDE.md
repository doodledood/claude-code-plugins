# Consultant Model Selection Guide

Quick reference for how consultant queries and selects models.

---

## TL;DR

### With Base URL
```bash
--base-url http://localhost:8000
```
→ Queries `http://localhost:8000/v1/models` → Scores → Picks best

### Without Base URL
```bash
# No --base-url flag
```
→ Uses known models list → Scores → Picks best (claude-3-5-sonnet or gpt-4o)

### With Explicit Model
```bash
--model gpt-4o
```
→ Uses `gpt-4o` directly → No querying or scoring

---

## Querying Models

### Method 1: Query from Base URL

**Command:**
```bash
python3 oracle_cli.py models --base-url "http://localhost:8000"
```

**What happens:**
1. HTTP GET to `http://localhost:8000/v1/models`
2. Parse JSON response
3. Return list of models

**Response format:**
```json
[
  {"id": "gpt-4o", "created": 1234567890, "owned_by": "openai"},
  {"id": "claude-3-5-sonnet-20241022", "created": 1234567890, "owned_by": "anthropic"}
]
```

**When to use:**
- Custom LiteLLM server
- Local model server (Ollama, vLLM, LM Studio)
- Private endpoint

**Fallback if fails:**
Falls back to known models list (Method 2)

---

### Method 2: Query from Known List

**Command:**
```bash
python3 oracle_cli.py models
```

**What happens:**
1. Return hardcoded list from `model_selector.py`
2. No API call
3. Instant response

**Response format:**
```json
[
  {"id": "gpt-4o", "provider": "openai"},
  {"id": "gpt-4-turbo", "provider": "openai"},
  {"id": "claude-3-5-sonnet-20241022", "provider": "anthropic"},
  {"id": "claude-3-opus-20240229", "provider": "anthropic"},
  {"id": "gemini-2.0-flash-exp", "provider": "google"}
]
```

**When to use:**
- No base URL provided
- Fallback when base URL query fails
- Want to see default providers

**Known providers:**
- OpenAI: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo
- Anthropic: claude-3-5-sonnet, claude-3-opus, claude-3-sonnet
- Google: gemini-2.0-flash-exp, gemini-1.5-pro

---

## Model Scoring Algorithm

When auto-selecting, consultant scores models like this:

```python
score = 0

# Version number
if "gpt-5" or "o1" or "o3" in model_id:
    score += 50
elif "gpt-4" in model_id:
    score += 40
elif "gpt-3.5" in model_id:
    score += 30

# Capability tier
if "pro" or "turbo" or "large" in model_id:
    score += 20

# Context size
if "128k" or "200k" in model_id:
    score += 15
elif "32k" in model_id:
    score += 12

# Anthropic specific
if "claude" in model_id:
    if "opus" in model_id:
        score += 50
    elif "sonnet" in model_id:
        if "3.5" or "3-5" in model_id:
            score += 48
        else:
            score += 45
    elif "haiku" in model_id:
        score += 35

# Google specific
if "gemini" in model_id:
    if "2.0" in model_id:
        score += 45
    elif "pro" in model_id:
        score += 40

# Select highest score
best_model = max(models, key=score_model)
```

**Typical winners:**
- `claude-3-5-sonnet-20241022`: 48 + bonuses (high score)
- `claude-3-opus-20240229`: 50 + bonuses (highest for Anthropic)
- `gpt-4o`: 40 + bonuses (high for OpenAI)
- `gemini-2.0-flash-exp`: 45 + bonuses (high for Google)

---

## Default Behavior Scenarios

### Scenario 1: Nothing Specified

```bash
/consultant-review
# No MODEL, no BASE_URL
```

**Execution:**
1. Check `CONSULTANT_MODEL` env var → Not set
2. Check `CONSULTANT_BASE_URL` env var → Not set
3. Query known models (no API call)
4. Score: claude-3-5-sonnet (48) vs gpt-4o (40) vs others
5. Select: `claude-3-5-sonnet-20241022` (highest score)
6. Use with Anthropic API (requires `ANTHROPIC_API_KEY`)

---

### Scenario 2: Base URL Only

```bash
/consultant-review BASE_URL=http://localhost:8000
# Has BASE_URL, no MODEL
```

**Execution:**
1. Check `CONSULTANT_MODEL` env var → Not set
2. Query `http://localhost:8000/v1/models`
3. Get available models: [gpt-4o, llama-3-70b, mistral-large, ...]
4. Score each model
5. Select highest score (maybe `mistral-large` if available)
6. Report: `Selected model: mistral-large`
7. Use `mistral-large` with `http://localhost:8000`

---

### Scenario 3: Model Only

```bash
/consultant-review MODEL=gpt-4o
# Has MODEL, no BASE_URL
```

**Execution:**
1. Use `gpt-4o` directly (no querying)
2. No base URL → Use OpenAI as provider
3. Requires `OPENAI_API_KEY` env var
4. No "Selected model" message (explicit choice)

---

### Scenario 4: Both Specified

```bash
/consultant-review MODEL=llama-3-70b BASE_URL=http://localhost:8000
# Has both MODEL and BASE_URL
```

**Execution:**
1. Use `llama-3-70b` directly (no querying)
2. Use `http://localhost:8000` as base URL
3. No scoring, no auto-selection
4. Requires authentication for local server

---

## Environment Variables Priority

Priority order for model selection:

1. **`--model` flag** (highest priority)
2. **`CONSULTANT_MODEL` env var** (medium priority)
3. **Auto-selection** (lowest priority, uses querying + scoring)

Priority order for base URL:

1. **`--base-url` flag** (highest priority)
2. **`CONSULTANT_BASE_URL` env var** (medium priority)
3. **Default providers** (lowest priority, no base URL)

**Examples:**

```bash
# Explicit flag wins
export CONSULTANT_MODEL=gpt-4
python3 oracle_cli.py --model claude-3-opus ...
# Uses: claude-3-opus (flag wins)

# Env var as fallback
export CONSULTANT_MODEL=gpt-4
python3 oracle_cli.py ...
# Uses: gpt-4 (env var)

# Auto-select as last resort
python3 oracle_cli.py ...
# Uses: claude-3-5-sonnet or gpt-4o (auto-selected)
```

---

## When Querying Happens

### ✅ Query ALWAYS happens when:
- User provides `--base-url` but NOT `--model`
- Need to auto-select best model from custom provider

### ✅ Query SOMETIMES happens when:
- User provides nothing (queries known models - instant, no API call)

### ❌ Query NEVER happens when:
- User provides `--model` flag (explicit choice)
- `CONSULTANT_MODEL` env var is set (explicit default)

---

## Troubleshooting

### Issue: Wrong model selected

**Likely cause:** Scoring algorithm picked unexpected model

**Solution:**
```bash
# See what models are available
python3 oracle_cli.py models [--base-url http://localhost:8000]

# Pick one explicitly
python3 oracle_cli.py --model "your-chosen-model" ...
```

### Issue: "Model not found"

**Likely cause:** Auto-selected model not available at base URL

**Solution:**
```bash
# Query available models first
python3 oracle_cli.py models --base-url http://localhost:8000

# Use one from the list
python3 oracle_cli.py --model "available-model" --base-url http://localhost:8000 ...
```

### Issue: "No API key provided"

**Likely cause:** Auto-selected model requires API key not set

**Solution:**
```bash
# For OpenAI models
export OPENAI_API_KEY="your-key"

# For Anthropic models
export ANTHROPIC_API_KEY="your-key"

# Or use --api-key flag
python3 oracle_cli.py --api-key "your-key" ...
```

---

## Quick Reference Table

| User Provides | Query Method | Selection | Base URL Used |
|---------------|--------------|-----------|---------------|
| Nothing | Known models | Auto (claude-3-5-sonnet) | Default (Anthropic) |
| BASE_URL only | Query /v1/models | Auto (highest score) | User's BASE_URL |
| MODEL only | None | User's MODEL | Default for MODEL |
| Both | None | User's MODEL | User's BASE_URL |
| CONSULTANT_MODEL env | Known models | CONSULTANT_MODEL | Default |
| CONSULTANT_BASE_URL env | Query /v1/models | Auto | CONSULTANT_BASE_URL |

---

## Code Location

Model selection logic is in:
```
consultant/skills/consultant/scripts/model_selector.py
```

Key functions:
- `list_models(base_url)` - Query models
- `select_best_model(base_url)` - Auto-select
- `_score_model(model_id)` - Scoring algorithm
- `_get_known_models()` - Known models list

---

**Remember:** The consultant CLI is designed to be smart. If you don't specify anything, it will pick the best available model. If you want control, just use `--model` flag!
