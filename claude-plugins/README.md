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
| `consultant` | Multi-provider LLM consultations via LiteLLM. Get perspectives from OpenAI, Google, local models without leaving Claude Code. |
| `vibe-extras` | Codebase exploration, web research, git utilities (rebase, history rewrite), documentation maintenance, AI slop cleanup, review persona generation. |
| `solo-dev` | Foundational documents: customer profiles, brand guidelines, design systems. |
| `prompt-engineering` | Prompt analysis and refinement against structured frameworks. |
| `frontend-design` | Frontend design patterns for distinctive, non-generic UI experiences. |
| `life-ops` | Personal decision-making advisor. Situation discovery → targeted research → ranked recommendation. |
| `writing` | Writing toolkit: anti-AI prose principles, iterative review loop, author voice capture, voice-matched content generation. |
| `marketing` | Value-first social media promotion. Browse X, find high-signal posts, craft varied replies with writing review, post after approval. |

> **See also:** [manifest-dev](https://github.com/doodledood/manifest-dev) for manifest-driven development—define acceptance criteria, let the verify-fix loop handle the rest.

## Plugin Details

### consultant
Requires Python 3.9+ and uv. Supports any LiteLLM provider. Includes `/ask` for single-model queries and `/ask-council` for multi-model ensemble.

### vibe-extras
Standalone utilities that work independently. `/explore-codebase` for structural codebase exploration; `/research-web` for deep web research with parallel investigators; `/clean-slop` removes AI-generated noise; `/rewrite-history` restructures commits for clean PRs.

### solo-dev
Define customer profiles and brand guidelines once, reference consistently across sessions.

### prompt-engineering
Three modes: `/review-prompt` (read-only analysis), `/optimize-prompt-precision` (eliminate ambiguities), `/optimize-prompt-goal` (goal effectiveness).

### frontend-design
Frontend design patterns including scrollytelling (scroll-driven storytelling with pinned sections, progressive reveals, parallax effects).

### life-ops
Personal decision-making advisor. `/decide` guides you through situation discovery (underlying needs, time horizons, constraints), conducts targeted research, and applies a decision framework to produce ranked recommendations with tie-breakers.

### writing
All writing skills consolidated. `human-writing` provides research-backed anti-AI principles (vocabulary kill-list, four-layer editing, craft fundamentals, detection science). `/write` runs the full workflow with iterative review. `craft-author-voice` captures your writing style. `/write-as-me` generates content in your voice. `voice-writer` agent applies both your voice and anti-AI principles.

### marketing
Value-first promotion on X (Twitter). `/promote-on-x` browses your feed, finds posts where your product adds genuine value, crafts structurally varied replies using the writing plugin, and posts after user approval. Requires Claude in Chrome extension and writing plugin.

## Contributing

Each plugin lives in its own directory. See [CLAUDE.md](../CLAUDE.md) for development commands and plugin structure.

## License

MIT
