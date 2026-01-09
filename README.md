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
/plugin install vibe-workflow@claude-code-plugins-marketplace
```

## Available Plugins

### vibe-workflow

Structured development workflow: spec → plan → implement. Reduces iteration cycles by front-loading requirements gathering and breaking work into verifiable chunks.

- `/spec` - Interactive requirements builder
- `/plan` - Create implementation plans with codebase research
- `/implement` - Execute plans via subagents with verification loops
- `/review` - Parallel code review agents (bugs, types, maintainability)
- `/bugfix` - Root cause analysis with test-driven verification

### consultant

Multi-provider LLM consultations via Python/LiteLLM. Get perspectives from different models (OpenAI, Anthropic, Google, local models) without leaving Claude Code.

- `/review` - Production-level PR reviews with severity-tagged findings
- `/ask` - Single-model consultation
- `/ask-counsil` - Multi-model ensemble (3 models in parallel)

### vibe-extras

Standalone utilities for common development tasks.

- `/rebase-on-main` - Safe rebasing with conflict resolution
- `/rewrite-history` - Restructure commits for clean PRs
- `/clean-slop` - Remove AI-generated noise from code
- `/update-claude-md` - Maintain project instructions

### solo-dev

Foundational documents for solo developers and small teams.

- Define customer profiles, brand guidelines, design systems
- Capture your writing voice for consistent AI-generated content
- Audit UI changes against your guidelines

### prompt-engineering

Analyze prompts against structured frameworks. Reports only—identifies improvement opportunities without modifying files.

## Repository Structure

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── claude-plugins/
│   ├── vibe-workflow/         # Spec → plan → implement
│   ├── consultant/            # Multi-provider LLM consultations
│   ├── vibe-extras/           # Git, docs, cleanup utilities
│   ├── solo-dev/              # Business toolkit
│   └── prompt-engineering/    # Prompt analysis
└── README.md
```

## Contributing

See [claude-plugins/README.md](./claude-plugins/README.md) for plugin development.

## License

MIT
