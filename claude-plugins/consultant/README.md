# Consultant Plugin

Multi-provider LLM consultations using Python/LiteLLM for deep AI-powered code analysis.

## What It Does

- **PR Reviews** - Run `/consultant:review` for production-level code review with severity-tagged findings
- **Bug Investigation** - Run `/consultant:investigate-bug` for root cause analysis
- **Code Analysis** - Run `/consultant:analyze-code` for architectural and security review
- **General Consultation** - Run `/consultant:ask` for single-model queries or `/consultant:ask-counsil` for multi-model ensemble

Supports 100+ LLM providers through LiteLLM: OpenAI, Anthropic, Google, Azure, Bedrock, local models (Ollama, vLLM, LM Studio), and any OpenAI-compatible API.

Use `/help` after installation to see all available commands.

## Requirements

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (for automatic dependency management)
- API key for your chosen provider

## Installation

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Set API key
export OPENAI_API_KEY="your-key"  # or ANTHROPIC_API_KEY, etc.

# Install plugin
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install consultant@claude-code-plugins-marketplace
```

## License

MIT
