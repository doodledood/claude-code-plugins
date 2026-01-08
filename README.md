# Claude Code Plugins Marketplace
A curated marketplace of Claude Code plugins for agentic development workflows, featuring tools for architecture, knowledge management, and development automation.

## 🎯 What is This?

This is a **Claude Code plugins marketplace** - a curated collection of plugins that enhance your development workflow with Claude Code, focusing on agentic development, code analysis, and planning tools.

## 🚀 Quick Start - Using the Marketplace

### Install the Marketplace

Add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
```

For local development:

```bash
/plugin marketplace add /path/to/claude-code-plugins
```

### Browse & Install Plugins

```bash
# List available marketplaces
/plugin marketplace list

# List all plugins
/plugin list

# Install a specific plugin
/plugin install consultant@claude-code-plugins-marketplace
```

## 📦 Available Plugins

All plugins are located in `claude-plugins/`:

#### consultant
Flexible multi-provider LLM consultations using Python/LiteLLM for deep AI-powered code analysis across 100+ models.

**Components:**
- **Agent:** `consultant` - Expert agent for multi-provider AI analysis with automatic model selection
- **Commands:**
  - `/review` - Production-level PR reviews with severity-tagged findings
  - `/analyze-code` - Architectural and security code analysis
  - `/investigate-bug` - Deep bug investigation with root cause analysis
  - `/ask` - Single-model consultation (defaults to gpt-5.2-pro)
  - `/ask-counsil` - Multi-model ensemble consultation (3 models in parallel)
- **Skill:** `consultant` - Python/LiteLLM CLI knowledge and best practices
- **Category:** development
- **Key Features:**
  - 100+ LLM provider support (OpenAI, Anthropic, Google, Azure, local models)
  - Custom base URLs for local LLM deployments
  - Automatic model discovery and selection

#### vibe-workflow
Autonomous development workflow with spec→plan→implement pipeline, code review agents, and quality gates.

**Components:**
- **Agents:**
  - `codebase-explorer` - Returns structural overview + prioritized file list (prefer over built-in Explore)
  - `bug-fixer` - Systematic bug investigation with root cause analysis
  - `chunk-implementor` - Implements a single plan chunk, logs progress (used by /implement)
  - `chunk-verifier` - Runs gates and checks acceptance criteria (used by /implement)
  - Code review agents (bugs, coverage, maintainability, type-safety, docs, CLAUDE.md adherence)
- **Commands:**
  - `/spec` - Interactive PRD builder using EARS syntax
  - `/plan` - Create mini-PR implementation plans from specs
  - `/implement` - Execute plans via subagents with verification and fix loops (5 attempts per chunk)
  - `/implement-inplace` - Single-agent implementation without subagent overhead
  - `/review` - Run all code review agents in parallel
  - `/bugfix` - Investigate and fix bugs with test-driven verification
  - `/web-research` - Research external topics with hypothesis tracking
- **Hook:** SessionStart reminder to prefer `codebase-explorer` for context gathering
- **Category:** development

#### vibe-extras
Standalone utilities that complement the core development workflow.

**Components:**
- **Agents:**
  - `slop-cleaner` - AI slop detection and removal
  - `information-density-verifier` - Opus-based semantic verification for lossless compression
- **Commands:**
  - `/rebase-on-main` - Safe git rebasing with conflict resolution
  - `/rewrite-history` - Restructure branch into clean, reviewer-friendly commits
  - `/clean-slop` - Remove AI-generated code noise
  - `/update-claude-md` - Create or maintain CLAUDE.md
  - `/maximize-info-density` - Compress docs/prompts losslessly for reduced tokens
- **Category:** development

#### prompt-engineering
Tools for reviewing and analyzing LLM prompts.

**Components:**
- **Agent:** `prompt-reviewer` - Deep prompt analysis via 10-Layer Architecture framework
- **Commands:**
  - `/review-prompt` - Analyze prompts for improvement opportunities (reports only, non-modifying)
- **Category:** development

#### solo-dev
Toolkit for solo developers to build, manage, and grow their business.

**Components:**
- **Agents:**
  - `design-research` - Research industry design patterns and competitor approaches
  - `design-quality-auditor` - Verify design guidelines align with customer and brand
  - `seo-researcher` - Research SEO and GEO strategies
  - `ux-auditor` - Audit UI/UX changes against design guidelines
  - `voice-writer` - Generate content in user's captured voice
- **Commands:**
  - `/define-customer-profile` - Create foundational CUSTOMER.md document
  - `/define-brand-guidelines` - Define communication guidelines (requires CUSTOMER.md)
  - `/define-design-guidelines` - Create UI/UX guidelines (requires CUSTOMER.md)
  - `/define-seo-strategy` - Traditional SEO + AI citation optimization (requires CUSTOMER.md)
  - `/craft-author-voice` - Capture unique writing style for AI replication
  - `/write-as-me` - Generate content in your voice (requires AUTHOR_VOICE.md)
  - `/audit-ux` - Check UI changes against design guidelines
- **Category:** productivity

## 🛠️ Development

### Repository Structure

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── claude-plugins/            # Claude Code plugins directory
│   ├── README.md             # Plugin development guide
│   ├── PLUGIN_TEMPLATE/      # Template for creating new plugins
│   ├── consultant/           # Multi-provider LLM consultations
│   ├── vibe-workflow/        # Spec→plan→implement, review, bugfix
│   ├── vibe-extras/          # Git, docs, cleanup utilities
│   ├── prompt-engineering/   # LLM prompt review and analysis
│   └── solo-dev/             # Solo developer business toolkit
├── CONTRIBUTING.md            # Contributing guidelines
└── README.md                  # This file
```

### Contributing Plugins

See [claude-plugins/README.md](./claude-plugins/README.md) for detailed instructions on:
- Creating new plugins
- Plugin structure and components
- Testing locally
- Submitting contributions

## 🎓 Learn More

- [Claude Code Documentation](https://code.claude.com/docs)
- [Plugin Marketplaces Guide](https://code.claude.com/docs/en/plugin-marketplaces)
- [Model Context Protocol](https://modelcontextprotocol.io)

## 📄 License

MIT

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add your tool or plugin
4. Submit a pull request

For plugin contributions, see the [plugin development guide](./claude-plugins/README.md).
