# Vibe Workflow Plugin

Autonomous development workflow with code review agents and quality gates.

## What It Does

- **Code Review** - Run `/review` to audit your changes for bugs, maintainability issues, type safety problems, documentation gaps, and test coverage
- **Bug Fixing** - Run `/bugfix` for systematic investigation with root cause analysis and test-driven verification
- **Product Specs** - Run `/spec-feature` for interactive PRD building using EARS syntax
- **Git Workflow** - Run `/rebase-on-main` for safe rebasing with conflict resolution
- **Code Cleanup** - Run `/clean-slop` to remove AI-generated noise
- **CLAUDE.md Management** - Run `/update-claude-md` to create or maintain project instructions

Use `/help` after installation to see all available commands.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-workflow@claude-code-plugins-marketplace
```

## License

MIT
