# Consultant Plugin

Flexible multi-provider LLM consultations using Python/LiteLLM for deep AI-powered code analysis across 100+ models.

## Overview

Consultant is a Claude Code plugin that provides access to powerful LLM models for complex analysis tasks through Python and LiteLLM. Unlike solutions tied to specific providers, Consultant supports any LiteLLM-compatible model with custom base URLs, making it perfect for local models, custom deployments, or switching between providers.

## Key Features

✅ **100+ LLM Providers**: OpenAI, Anthropic, Google, Azure, Bedrock, HuggingFace, local models (Ollama, vLLM, LM Studio), and any OpenAI-compatible API

✅ **Automatic Model Selection**: Queries available models and picks the best one based on capabilities

✅ **Custom Base URLs**: Use local LiteLLM servers or custom deployments

✅ **Token Management**: Pre-flight validation, context size checking, and clear overflow errors

✅ **Async Execution**: Background sessions with status tracking and reattachment

✅ **Full-Featured**: Includes consultant agent, review/bug-investigation/execplan commands

## Components

### Agent: consultant

Expert agent for leveraging powerful LLM analysis through Python/LiteLLM. Handles the full workflow from context gathering to findings synthesis.

**Use when you need:**
- Comprehensive PR reviews before production deployment
- Deep architectural validation
- Complex bug root cause analysis
- Execution plan creation for features

### Commands

#### `/consultant-review`

Production-level PR reviews with severity-tagged findings, regression test guidance, and security validation.

**Usage:**
```bash
/consultant-review
# Or with parameters:
/consultant-review PR_REF=origin/main...feature-branch MODEL=claude-sonnet-4-5
```

**What it does:**
- Reviews code changes comprehensively
- Provides severity-tagged findings (BLOCKER/HIGH/MEDIUM/LOW/INFO)
- Suggests specific fixes with file references
- Recommends regression tests
- Validates security and architectural concerns

#### `/consultant-investigate-bug`

Deep bug investigation with root cause analysis and fix recommendations.

**Usage:**
```bash
/consultant-investigate-bug
# Or with symptom:
/consultant-investigate-bug SYMPTOM="API returns 500 on profile update"
```

**What it does:**
- Identifies root cause of bugs
- Traces execution flow from symptom to source
- Assesses blast radius and impact
- Provides concrete fix suggestions
- Recommends regression tests to prevent recurrence

#### `/consultant-execplan`

Create comprehensive execution plans for features and changes.

**Usage:**
```bash
/consultant-execplan
# Or with feature:
/consultant-execplan FEATURE="Add rate limiting" GOAL="Prevent API abuse"
```

**What it does:**
- Gathers comprehensive codebase context
- Analyzes existing patterns and architecture
- Creates detailed implementation steps with validation
- Breaks down work into shippable chunks
- Provides testing strategies and deployment plans

### Skill: consultant

Contextual skill providing consultant CLI knowledge and best practices.

**Activated automatically when:**
- Discussing complex analysis needs
- Questions about consultant capabilities
- Architectural review requirements
- Security audit planning

**Provides:**
- Consultant Python CLI usage patterns
- File glob patterns for different analysis types
- Session management guidance
- Model selection strategies

## Installation

The CLI uses [uv](https://docs.astral.sh/uv/) for automatic dependency management via PEP 723 inline script metadata. No manual `pip install` needed.

If `uv` is not installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Requirements

- Python 3.9+
- uv (installs litellm and requests automatically on first run)
- API key for your chosen provider (or custom base URL)

## Quick Start

### 1. Set API Key

```bash
export LITELLM_API_KEY="your-key-here"
# Or for specific providers:
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```

### 2. Review a Pull Request

```bash
/consultant-review
```

The command will automatically:
- Determine your PR reference (origin/master...HEAD)
- Gather all changed files with context
- Invoke consultant for comprehensive analysis
- Monitor the session until completion
- Provide actionable findings

### 3. Investigate a Bug

```bash
/consultant-investigate-bug SYMPTOM="API timeout on large datasets"
```

Provide bug details when prompted, or let it infer from:
- Recent test failures
- Error messages in conversation
- Git history and recent changes

### 4. Create an Execution Plan

```bash
/consultant-execplan FEATURE="Add caching layer" GOAL="Improve API performance"
```

Creates a comprehensive execution plan with:
- Detailed implementation steps
- Architecture analysis
- Testing strategy
- Validation criteria

## Configuration

### Environment Variables

**API Keys:**
- `LITELLM_API_KEY`: Generic LiteLLM API key
- `OPENAI_API_KEY`: For OpenAI models
- `ANTHROPIC_API_KEY`: For Claude models

**Model & Base URL:**
- `CONSULTANT_MODEL`: Default model to use
- `CONSULTANT_BASE_URL`: Default base URL (for commands)
- `OPENAI_BASE_URL`: Default base URL (for Python CLI)

### Custom Base URL

Use a local LiteLLM instance or custom deployment:

```bash
# For commands (via agent)
export CONSULTANT_BASE_URL="http://localhost:8000"
/consultant-review

# For direct Python CLI usage
export OPENAI_BASE_URL="http://localhost:8000"
uv run {consultant_scripts}/consultant_cli.py --prompt "..." --file ...
```

Or specify per-command/invocation:

```bash
# Commands
/consultant-review BASE_URL=http://localhost:8000

# Python CLI
uv run {consultant_scripts}/consultant_cli.py --base-url "http://localhost:8000" ...
```

### Model Selection

Specify a model explicitly:

```bash
/consultant-review MODEL=claude-sonnet-4-5
```

Or let consultant auto-select:

```bash
/consultant-review  # Will query and pick best model
```

## How Consultant Works

1. **Context Gathering**: Collects relevant files, diffs, and documentation
2. **Artifact Organization**: Creates structured, numbered attachments
3. **Prompt Engineering**: Constructs detailed analysis prompts
4. **Consultant Invocation**: Runs Python CLI via `consultant_cli.py`
5. **Session Management**: Monitors asynchronously until completion
6. **Findings Synthesis**: Transforms output into actionable recommendations

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

## Supported Providers

Through LiteLLM, consultant supports:

- **OpenAI**: GPT-4, GPT-5, o1, o3
- **Anthropic**: Claude Sonnet 4, Opus 4, Haiku
- **Google**: Gemini 3 Pro, 2.5 Flash
- **Azure OpenAI**: All Azure-hosted models
- **AWS Bedrock**: Claude, Llama, Mistral
- **Cohere**: Command models
- **HuggingFace**: Hosted inference endpoints
- **Local Models**: Ollama, vLLM, LM Studio, LocalAI
- **Custom**: Any OpenAI-compatible API

## Model Selection Algorithm

When no model is specified, consultant:

1. Queries available models from provider (via `/v1/models` or known list)
2. Scores each model based on:
   - Version number (GPT-5 > GPT-4 > GPT-3.5)
   - Capability tier (opus/pro > sonnet > haiku)
   - Context size (200k > 128k > 32k)
   - Reasoning capability (o1/o3 models higher)
3. Selects the highest-scoring model
4. Reports which model was chosen

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
uv run {consultant_scripts_path}/consultant_cli.py session <slug>
```

### List Sessions

```bash
uv run {consultant_scripts_path}/consultant_cli.py list
```

## Examples

### Security Audit

```bash
/consultant-review MODEL=claude-sonnet-4-5
```

With custom focus:

```bash
export CONSULTANT_FOCUS="SQL injection vulnerabilities in auth module"
/consultant-review
```

### Architectural Review

```bash
/consultant-review PR_REF=origin/main...feature/new-architecture
```

### Bug Investigation

```bash
/consultant-investigate-bug SYMPTOM="Race condition in order processing causing duplicate charges"
```

### Execution Planning

```bash
/consultant-execplan FEATURE="Implement real-time notifications" GOAL="Notify users of order status changes within 1 second"
```

### Local LLM Usage

```bash
# Start local LiteLLM server
litellm --model ollama/llama3 --port 8000

# Use consultant with local server
export CONSULTANT_BASE_URL="http://localhost:8000"
/consultant-review
```

## Advanced Usage

### Direct CLI Usage

You can also use the consultant Python CLI directly:

```bash
uv run {consultant_scripts_path}/consultant_cli.py \
  --prompt "Analyze this code for performance issues" \
  --file src/**/*.py \
  --slug "perf-analysis" \
  --model "claude-sonnet-4-5" \
  --wait
```

### List Available Models

```bash
uv run {consultant_scripts_path}/consultant_cli.py models \
  --base-url "http://localhost:8000"
```

### Check Session Status

```bash
uv run {consultant_scripts_path}/consultant_cli.py session <slug>
```

## Troubleshooting

### Missing uv

**Issue**: `uv: command not found`

**Solution**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Missing Dependencies

**Issue**: `ImportError: No module named 'litellm'`

**Solution**: This shouldn't happen with `uv run`, but if it does, clear uv cache:
```bash
uv cache clean
```

### Context Limit Exceeded

**Issue**: Input exceeds model's context window

**Solution**:
1. Reduce number of files attached
2. Use a model with larger context (e.g., claude-3-opus has 200k)
3. Shorten the prompt
4. Split into multiple consultations

### Missing API Key

**Issue**: "No API key provided"

**Solution**:
```bash
export LITELLM_API_KEY="your-key"
# Or
export OPENAI_API_KEY="your-key"
# Or
export ANTHROPIC_API_KEY="your-key"
```

### Model Discovery Fails

**Issue**: Cannot query models from base URL

**Solution**:
- Explicitly specify a model with `MODEL=model-name`
- Check base URL is correct: `curl http://localhost:8000/v1/models`
- Verify API key is set correctly

### Session Stuck

**Issue**: Session shows "running" but seems stuck

**Solution**:
- Check session directory: `ls ~/.consultant/sessions/{session-id}/`
- Look for `error.txt`: `cat ~/.consultant/sessions/{session-id}/error.txt`
- Check process: `ps aux | grep consultant_cli.py`

## When to Use Consultant

**Perfect for:**

- Complex architectural decisions
- Security vulnerability analysis
- Comprehensive code reviews across large codebases
- Understanding intricate patterns in unfamiliar code
- Expert-level domain analysis
- Flexibility to use any LLM provider
- Local model deployments
- Custom LiteLLM configurations

**Not needed for:**

- Simple code edits or fixes
- Questions answerable by reading 1-2 files
- Tasks requiring immediate responses
- Repetitive operations better suited to scripts

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Supported Models](https://docs.litellm.ai/docs/providers)
- [Glob Patterns Guide](./skills/consultant/references/glob-patterns.md)
- [Consultant Skill Reference](./skills/consultant/SKILL.md)

## License

MIT

## Contributing

Contributions welcome! This plugin is part of the [claude-code-plugins](https://github.com/doodledood/claude-code-plugins) repository.

## Credits

Created by doodledood, providing multi-provider LLM support through Python and LiteLLM.
