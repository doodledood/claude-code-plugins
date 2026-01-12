# Claude Code Plugins

First-principles workflows for Claude Code. Quality output you can trust.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin list
/plugin install <plugin-name>@claude-code-plugins-marketplace
```

## Available Plugins

| Plugin | What It Does |
|--------|--------------|
| `vibe-workflow` | Structured spec → plan → implement workflow with parallel code review. Front-loads requirements to reduce iteration cycles. Includes hooks for session continuity. |
| `consultant` | Multi-provider LLM consultations via LiteLLM. Get perspectives from OpenAI, Google, local models without leaving Claude Code. |
| `vibe-extras` | Git utilities (rebase, history rewrite), documentation maintenance, AI slop cleanup. |
| `solo-dev` | Foundational documents: customer profiles, brand guidelines, design systems, author voice capture. |
| `prompt-engineering` | Prompt analysis and refinement against structured frameworks. |

## Plugin Details

### vibe-workflow
Core development workflow with hooks for session continuity. Includes specialized review agents for bugs, types, maintainability, coverage, and docs.

### consultant
Requires Python 3.9+ and uv. Supports any LiteLLM provider. Includes `/ask` for single-model queries and `/ask-council` for multi-model ensemble.

### vibe-extras
Standalone utilities that work independently. `/clean-slop` removes AI-generated noise; `/rewrite-history` restructures commits for clean PRs.

### solo-dev
Define customer profiles and brand guidelines once, reference consistently across sessions. Includes author voice capture for content generation.

### prompt-engineering
Two modes: `/review-prompt` (read-only analysis) and `/refine-prompt` (iterative refinement with verification).

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
