# Vibe Extras Plugin

Standalone utilities that complement the core development workflow.

## What It Does

- **Git Workflow** - Run `/rebase-on-main` for safe rebasing with conflict resolution
- **Code Cleanup** - Run `/clean-slop` to remove AI-generated noise (useless comments, verbose patterns)
- **CLAUDE.md Management** - Run `/update-claude-md` to create or maintain project instructions
- **Information Density** - Run `/maximize-information-density` to compress docs/prompts losslessly for reduced token consumption

Use `/help` after installation to see all available commands.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-extras@claude-code-plugins-marketplace
```

## License

MIT
