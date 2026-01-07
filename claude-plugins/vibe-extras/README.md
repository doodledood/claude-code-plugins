# Vibe Extras Plugin

Standalone utilities that complement the core development workflow.

## What It Does

**Skills** (auto-invoked by Claude when relevant):
- **maximize-information-density** - Compress docs/prompts losslessly for reduced token consumption

**Commands** (invoke explicitly):
- `/rebase-on-main` - Safe rebasing with conflict resolution
- `/rewrite-history` - Safely rewrite git history (squash, reorder, edit commits) with automatic backup
- `/clean-slop` - Remove AI-generated noise (useless comments, verbose patterns)
- `/update-claude-md` - Create or maintain project instructions

**Agents**:
- **information-density-verifier** - Verifies lossless compression (used by maximize-information-density skill)

Use `/help` after installation to see all available commands.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-extras@claude-code-plugins-marketplace
```

## License

MIT
