---
name: consultant
description: 'Consults external AI models (100+ via LiteLLM) for complex analysis. Use for architectural review, security audit, deep code understanding, or when extended reasoning is needed. Runs async with session management.'
---

# Consultant

## Overview

Consultant is a Python-based tool using LiteLLM to provide access to powerful AI models for complex analysis tasks. It accepts file globs and prompts, runs asynchronously, and returns detailed insights after extended reasoning time.

**Key advantages:**

- Supports 100+ LLM providers through LiteLLM (OpenAI, Anthropic, Google, Azure, local models, etc.)
- Custom base URLs for any provider or local LLM server
- Automatic model discovery and selection
- Async operation with session management
- Token counting and context overflow protection
- Cross-platform Python implementation

## Requirements

The CLI uses [uvx](https://docs.astral.sh/uv/guides/tools/) for automatic dependency management. Dependencies (litellm, requests) are installed automatically on first run via PEP 723 inline script metadata - no explicit installation needed.

If `uv` is not installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Getting Started

**IMPORTANT: Always run `uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli --help` first to understand current capabilities.**

Where `{CONSULTANT_SCRIPTS_PATH}` is the path to `claude-plugins/consultant/skills/consultant/scripts/`

## Basic Usage

### Start a Consultation

The consultant script runs synchronously (blocking until completion). For long-running analyses, you should run it in the background using the Bash tool with `run_in_background: true`, then use BashOutput to check progress every 30 seconds until completion.

**Example: Running in background via Bash tool**

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Analyze this code for security vulnerabilities" \
  --file src/**/*.py \
  --slug "security-audit"
```

When calling via the Bash tool:
1. Use `run_in_background: true` parameter
2. Wait at least 30 seconds, then use BashOutput tool with the returned bash_id to check progress
3. If still running, wait another 30 seconds and check again - repeat until completion
4. The script will print output as it completes each step
5. Final results appear after "Waiting for completion..." message

**What you'll see:**
- Token usage summary
- Session ID
- "Waiting for completion..." status
- Streaming output from the LLM
- Final results after completion

### Check Session Status

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli session security-audit
```

This returns JSON with:
- Current status (running/completed/error)
- Full output if completed
- Error details if failed

### List All Sessions

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli list
```

Shows all sessions with status, timestamps, and models used.

## Advanced Features

### Custom Provider with Base URL

```bash
# Use custom LiteLLM endpoint
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Review this PR" \
  --file src/**/*.ts \
  --slug "pr-review" \
  --base-url "http://localhost:8000" \
  --model "gpt-5.2"
```

### List Available Models

#### From Custom Provider (with Base URL)

Query models from a custom LiteLLM endpoint:

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli models \
  --base-url "http://localhost:8000"
```

**What happens:**
- Sends HTTP GET to `http://localhost:8000/v1/models`
- Parses JSON response with model list
- Returns all available models from that endpoint
- Example output:
  ```json
  [
    {"id": "gpt-5.2", "created": 1234567890, "owned_by": "openai"},
    {"id": "claude-opus-4-5", "created": 1234567890, "owned_by": "anthropic"}
  ]
  ```

#### From Known Providers (without Base URL)

Query known models from major providers:

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli models
```

**What happens:**
- Returns hardcoded list of known models (no API call)
- Includes models from OpenAI, Anthropic, Google
- Example output:
  ```json
  [
    {"id": "gpt-5.2", "provider": "openai"},
    {"id": "claude-opus-4-5", "provider": "anthropic"},
    {"id": "gemini/gemini-2.5-flash", "provider": "google"}
  ]
  ```

### Automatic Model Selection

#### Scenario 1: With Base URL (custom provider)

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Architectural review" \
  --file "**/*.py" \
  --slug "arch-review" \
  --base-url "http://localhost:8000"
  # No --model flag
```

**Consultant will:**
1. Query `http://localhost:8000/v1/models` to get available models
2. Select a model based on the task requirements

**For model selection guidance:** Check https://artificialanalysis.ai for up-to-date model benchmarks and rankings to choose the best model for your use case.

#### Scenario 2: Without Base URL (default providers)

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Code review" \
  --file src/*.py \
  --slug "review"
  # No --model flag, no --base-url flag
```

**Consultant will:**
1. Use known models list (OpenAI, Anthropic, Google)
2. Select a model based on task requirements

**For model selection guidance:** Check https://artificialanalysis.ai for up-to-date model benchmarks and rankings. Recommended defaults: `gpt-5.2-pro`, `claude-opus-4-5-20251101`, `gemini/gemini-3-pro-preview`.

#### Scenario 3: Explicit Model (no auto-selection)

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Bug analysis" \
  --file src/*.py \
  --slug "bug" \
  --model "gpt-5.2"
```

**Consultant will:**
1. Skip model querying and scoring
2. Use `gpt-5.2` directly
3. Use default provider for GPT-5 (OpenAI)
4. No "Selected model" message

### Specify API Key

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "..." \
  --file ... \
  --slug "..." \
  --api-key "your-api-key"
```

Or use environment variables (see below).

## Environment Variables

Consultant checks these environment variables:

**API Keys (checked in order):**
- `LITELLM_API_KEY`: Generic LiteLLM API key
- `OPENAI_API_KEY`: For OpenAI models
- `ANTHROPIC_API_KEY`: For Claude models

**Base URL:**
- `OPENAI_BASE_URL`: Default base URL (used if --base-url not provided)

Example:

```bash
# Set API key
export LITELLM_API_KEY="your-key-here"

# Optional: Set default base URL
export OPENAI_BASE_URL="http://localhost:8000"

# Now consultant will use the base URL automatically
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli --prompt "..." --file ... --slug "..."
```

## When to Use Consultant

**Perfect for:**

- Complex architectural decisions requiring deep analysis
- Security vulnerability analysis across large codebases
- Comprehensive code reviews before production deployment
- Understanding intricate patterns or relationships in unfamiliar code
- Expert-level domain analysis (e.g., distributed systems, concurrency)

**Don't use consultant for:**

- Simple code edits or fixes you can handle directly
- Questions answerable by reading 1-2 files
- Tasks requiring immediate responses (consultant takes minutes)
- Repetitive operations better suited to scripts

## Session Management

### Session Storage

Sessions are stored in `~/.consultant/sessions/{session-id}/` with:

- `metadata.json`: Status, timestamps, token counts, model info
- `prompt.txt`: Original user prompt
- `output.txt`: Streaming response (grows during execution)
- `error.txt`: Error details (if failed)
- `file_*`: Copies of all attached files

### Reattachment

Query status anytime:

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli session <slug>
```

The most recent session with that slug will be returned.

### Cleanup

Sessions persist until manually deleted:

```bash
rm -rf ~/.consultant/sessions/{session-id}
```

## Token Management

Consultant automatically:

1. Counts tokens for prompt and each file
2. Validates against model's context size
3. Reserves 20% of context for response
4. Fails fast with clear errors if over limit

Example output:

```
📊 Token Usage:
- Prompt: 1,234 tokens
- Files: 45,678 tokens (15 files)
- Total: 46,912 tokens
- Limit: 128,000 tokens
- Available: 102,400 tokens (80%)
```

If context exceeded:

```
ERROR: Input exceeds context limit!
  Input: 150,000 tokens
  Limit: 128,000 tokens
  Overage: 22,000 tokens

Suggestions:
1. Reduce number of files (currently 25)
2. Use a model with larger context
3. Shorten the prompt
```

## Model Selection

### Automatic Selection Algorithm

When no model is specified, consultant:

1. Queries available models from provider (via `/v1/models` or known list)
2. Scores each model based on:
   - Version number (GPT-5 > GPT-4 > GPT-3.5)
   - Capability tier (opus/pro > sonnet > haiku)
   - Context size (200k > 128k > 32k)
   - Reasoning capability (o1/o3 models higher)
3. Selects the highest-scoring model

### Supported Providers

Through LiteLLM, consultant supports:

- OpenAI (GPT-4, GPT-5, o1, etc.)
- Anthropic (Claude Sonnet 4, Opus 4, etc.)
- Google (Gemini 3, 2.5, etc.)
- Azure OpenAI
- AWS Bedrock
- Cohere
- HuggingFace
- Local models (Ollama, vLLM, LM Studio, etc.)
- Any OpenAI-compatible API

## Error Handling

Consultant provides clear error messages for common issues:

### Missing API Key

```
ERROR: No API key provided.
Set LITELLM_API_KEY environment variable or use --api-key flag.
```

### Context Limit Exceeded

```
ERROR: Input exceeds context limit!
[Details and suggestions]
```

### Model Not Found

```
ERROR: Model 'gpt-7' not found at base URL
Available models: [list]
```

### Network Failure

```
WARNING: Network error connecting to http://localhost:8000
Retrying in 5 seconds... (attempt 2/3)
```

## Troubleshooting

**Issue**: `uvx: command not found`

**Solution**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Issue**: `ImportError: No module named 'litellm'`

**Solution**: This shouldn't happen with `uvx`, but if it does, clear uv cache:
```bash
uv cache clean
```

**Issue**: Session stuck in "running" status

**Solution**:
- Check session directory: `ls ~/.consultant/sessions/{session-id}/`
- Look for `error.txt`: `cat ~/.consultant/sessions/{session-id}/error.txt`
- Check process is running: `ps aux | grep consultant_cli.py`

**Issue**: Context limit exceeded

**Solution**:
1. Reduce number of files attached
2. Use a model with larger context (e.g., claude-3-opus has 200k)
3. Shorten the prompt
4. Split into multiple consultations

**Issue**: Model discovery fails

**Solution**:
- Explicitly specify a model with `--model`
- Check base URL is correct: `curl http://localhost:8000/v1/models`
- Verify API key is set correctly

## Examples

### Security Audit

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Identify SQL injection vulnerabilities in the authentication module. For each finding, provide: vulnerable code location, attack vector, and recommended fix." \
  --file "apps/*/src/**/*.{service,controller}.ts" \
  --slug "security-audit" \
  --model "claude-opus-4-5"
```

### Architectural Review

```bash
uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Identify the top 5 highest-impact architectural issues causing tight coupling. For each: explain the problem, show affected components, and recommend a solution." \
  --file "apps/*/src/**/*.ts" \
  --slug "arch-review"
```

### PR Review

```bash
# Generate diff first
git diff origin/main...HEAD > /tmp/pr-diff.txt

uvx --from {CONSULTANT_SCRIPTS_PATH} consultant-cli \
  --prompt "Review this PR for production deployment. Flag blockers, high-risk changes, and suggest regression tests." \
  --file /tmp/pr-diff.txt \
  --slug "pr-review"
```

## Integration with Consultant Agent

The consultant agent uses this Python CLI automatically. When you invoke:

- `/consultant-review`
- `/consultant-investigate-bug`
- `/consultant-execplan`

The agent constructs the appropriate consultant_cli.py command with all necessary files and prompt.

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Supported Models](https://docs.litellm.ai/docs/providers)
- [Consultant Plugin README](../../README.md)
- [Glob Patterns Guide](./references/glob-patterns.md)
