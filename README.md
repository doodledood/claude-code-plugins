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

Structured development workflow that front-loads requirements to reduce iteration cycles. Phases build on each other: spec → plan → implement.

**Core workflow:**
- `/spec` - Interactive requirements builder with structured interview
- `/plan` - Create implementation plans with codebase research
- `/implement` - Execute plans via subagents with verification loops
- `/implement-inplace` - Single-agent implementation for simpler tasks

**Code review:**
- `/review` - Parallel review agents (bugs, types, maintainability, coverage, docs)
- `/review-bugs` - Focused bug detection
- `/review-type-safety` - Type safety analysis
- `/review-maintainability` - Code quality and maintainability
- `/review-coverage` - Test coverage gaps
- `/review-docs` - Documentation completeness
- `/review-claude-md-adherence` - Check adherence to project instructions
- `/fix-review-issues` - Address findings from review

**Research & debugging:**
- `/bugfix` - Root cause analysis with test-driven verification
- `/research-web` - Deep web research with parallel investigators (quick/medium/thorough/very-thorough)
- `/explore-codebase` - Structural overview with prioritized file list

**Hooks** (automatic behaviors):
- Session start reminders for agent preferences
- Post-compaction recovery for implement workflows
- Stop enforcement to prevent premature completion

### consultant

Multi-provider LLM consultations via Python/LiteLLM. Get perspectives from different models (OpenAI, Anthropic, Google, local models) without leaving Claude Code.

- `/review` - PR review with severity-tagged findings
- `/analyze-code` - Architectural and security analysis
- `/investigate-bug` - Root cause analysis via external model
- `/ask` - Single-model consultation
- `/ask-council` - Multi-model ensemble (3 models in parallel)

Requires Python 3.9+ and [uv](https://docs.astral.sh/uv/). Supports any provider via [LiteLLM](https://docs.litellm.ai/docs/providers).

### vibe-extras

Standalone utilities for common development tasks.

**Git utilities:**
- `/rebase-on-main` - Safe rebasing with conflict resolution guidance
- `/rewrite-history` - Restructure commits for clean, reviewer-friendly PRs

**Code maintenance:**
- `/clean-slop` - Remove AI-generated noise (redundant comments, verbose patterns)
- `/update-claude-md` - Create or maintain CLAUDE.md project instructions
- `maximize-info-density` - Compress docs/prompts losslessly (auto-invoked)

### solo-dev

Foundational documents for solo developers and small teams. Define once, reference consistently.

**Customer & brand:**
- `define-customer-profile` - Create CUSTOMER.md (foundation for all other decisions)
- `define-brand-guidelines` - Communication style and voice
- `define-design-guidelines` - UI/UX patterns for your audience
- `define-seo-strategy` - Traditional SEO + AI citation optimization

**Content creation:**
- `craft-author-voice` - Capture your writing style for AI replication
- `/write-as-me` - Generate content in your voice (requires AUTHOR_VOICE.md)
- `/audit-ux` - Check UI changes against your design guidelines

### prompt-engineering

Analyze and refine prompts for clarity and precision.

- `/review-prompt` - Analyze against 10-Layer Architecture framework (read-only)
- `/refine-prompt` - Iteratively refine for precision, eliminating ambiguities

## Repository Structure

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── claude-plugins/
│   ├── vibe-workflow/         # Spec → plan → implement with code review
│   ├── consultant/            # Multi-provider LLM consultations
│   ├── vibe-extras/           # Git, docs, cleanup utilities
│   ├── solo-dev/              # Customer profiles, brand, design docs
│   └── prompt-engineering/    # Prompt analysis and refinement
└── README.md
```

## Contributing

See [claude-plugins/README.md](./claude-plugins/README.md) for plugin development.

## License

MIT
