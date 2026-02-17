# Claude Code Plugins Marketplace

First-principles workflows for Claude Code. Built by developers who understand LLM limitations.

## Who This Is For

Experienced developers frustrated by hype-driven AI coding tools. If you're tired of chasing the latest "game-changing" prompt that produces code you spend hours debugging, these plugins offer a grounded alternative.

**Our approach:**
- Workflows designed around how LLMs actually work, not how we wish they worked
- Quality over speed—invest upfront, ship with confidence
- Simple to use, sophisticated under the hood

## Installation

Add the marketplace:

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
```

Browse and install:

```bash
/plugin list
/plugin install vibe-extras@claude-code-plugins-marketplace
```

## Available Plugins

### consultant

Multi-provider LLM consultations via Python/LiteLLM. Get perspectives from different models (OpenAI, Anthropic, Google, local models) without leaving Claude Code.

- `/review` - PR review with severity-tagged findings
- `/analyze-code` - Architectural and security analysis
- `/investigate-bug` - Root cause analysis via external model
- `/ask` - Single-model consultation
- `/ask-council` - Multi-model ensemble (3 models in parallel)

Requires Python 3.9+ and [uv](https://docs.astral.sh/uv/). Supports any provider via [LiteLLM](https://docs.litellm.ai/docs/providers).

### vibe-extras

Standalone utilities for codebase exploration, web research, git operations, and code maintenance.

**Research & exploration:**
- `/explore-codebase` - Structural overview with prioritized file list (quick/medium/thorough/very-thorough)
- `/research-web` - Deep web research with parallel investigators and multi-wave synthesis

**Git utilities:**
- `/rebase-on-main` - Safe rebasing with conflict resolution guidance
- `/rewrite-history` - Restructure commits for clean, reviewer-friendly PRs

**Code maintenance:**
- `/clean-slop` - Remove AI-generated noise (redundant comments, verbose patterns)
- `/update-claude-md` - Create or maintain CLAUDE.md project instructions

**Code review:**
- `/build-review-persona` - Mine GitHub review history to generate a calibrated review-as-me skill

> **See also:** [manifest-dev](https://github.com/doodledood/manifest-dev) for manifest-driven development—define acceptance criteria, let the verify-fix loop handle the rest.

### solo-dev

Foundational documents for solo developers and small teams. Define once, reference consistently.

**Customer & brand:**
- `define-customer-profile` - Create CUSTOMER.md (foundation for all other decisions)
- `define-brand-guidelines` - Communication style and voice
- `define-design-guidelines` - UI/UX patterns for your audience
- `define-seo-strategy` - Traditional SEO + AI citation optimization

**Other:**
- `/audit-ux` - Check UI changes against your design guidelines

### prompt-engineering

Craft, analyze, and optimize prompts from first principles.

- `/prompt-engineering` - Craft or update prompts from first principles (WHAT/WHY not HOW)
- `/review-prompt` - Analyze against 10-Layer Architecture framework (read-only)
- `/optimize-prompt-token-efficiency` - Iteratively optimize for token efficiency
- `/compress-prompt` - Compress into single dense paragraph for context injection

### frontend-design

Frontend design patterns for distinctive, non-generic UI experiences.

- `scrollytelling` - Scroll-driven storytelling with pinned sections, progressive reveals, and parallax effects

### life-ops

Personal decision-making advisor. Understands your situation first, then researches and recommends.

- `/decide` - Situation discovery → targeted research → decision framework → ranked recommendation

### writing

All writing skills in one place. Research-backed anti-AI prose, author voice capture, and voice-matched generation.

- `human-writing` - Base knowledge with vocabulary kill-list, four-layer editing, craft fundamentals (auto-invoked for prose)
- `/write` - Full workflow: gather context → write → review → auto-fix → loop until clean
- `craft-author-voice` - Capture your writing style into AUTHOR_VOICE.md
- `/write-as-me` - Generate content in your voice (requires AUTHOR_VOICE.md)

## Repository Structure

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── claude-plugins/
│   ├── consultant/            # Multi-provider LLM consultations
│   ├── vibe-extras/           # Research, git, docs, cleanup utilities
│   ├── solo-dev/              # Customer profiles, brand, design docs
│   ├── prompt-engineering/    # Prompt analysis and refinement
│   ├── frontend-design/       # Frontend design patterns
│   ├── life-ops/              # Personal decision-making advisor
│   └── writing/               # Writing toolkit (anti-AI prose, voice, generation)
└── README.md
```

## Contributing

See [claude-plugins/README.md](./claude-plugins/README.md) for plugin development.

## License

MIT
