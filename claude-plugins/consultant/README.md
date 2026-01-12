# Consultant

Multi-provider LLM consultations without leaving Claude Code.

## Why

Different models have different strengths. Sometimes you want a second opinion on code, a different perspective on architecture, or to validate an approach across multiple models. This plugin lets you query other LLMs (OpenAI, Google, local models) directly from Claude Code.

## Commands

- `/review` - PR review with severity-tagged findings
- `/analyze-code` - Architectural and security analysis
- `/investigate-bug` - Root cause analysis
- `/ask` - Single-model consultation
- `/ask-council` - Multi-model ensemble (3 models in parallel)
- `consultant` - Direct consultation skill (auto-invoked)

## Requirements

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) for dependency management
- API key for your chosen provider

## Installation

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set API key
export OPENAI_API_KEY="your-key"  # or ANTHROPIC_API_KEY, GOOGLE_API_KEY, etc.

# Install plugin
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install consultant@claude-code-plugins-marketplace
```

## Supported Providers

Any LLM supported by [LiteLLM](https://docs.litellm.ai/docs/providers): OpenAI, Anthropic, Google, Azure, Bedrock, Ollama, vLLM, LM Studio, and any OpenAI-compatible API.

## License

MIT
