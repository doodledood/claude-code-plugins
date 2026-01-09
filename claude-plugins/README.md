# Claude Code Plugins

First-principles workflows for Claude Code.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin list
/plugin install <plugin-name>@claude-code-plugins-marketplace
```

## Available Plugins

| Plugin | What It Does |
|--------|--------------|
| `vibe-workflow` | Structured spec → plan → implement workflow. Front-loads requirements to reduce iteration cycles. |
| `consultant` | Multi-provider LLM consultations. Get perspectives from different models without context switching. |
| `vibe-extras` | Git utilities, documentation maintenance, AI slop cleanup. |
| `solo-dev` | Foundational documents: customer profiles, brand guidelines, design systems. |
| `prompt-engineering` | Prompt analysis against structured frameworks. Reports only. |

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
