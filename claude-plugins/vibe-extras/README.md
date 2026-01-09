# Vibe Extras

Standalone utilities for common development tasks.

## Commands

**Git utilities:**
- `/rebase-on-main` - Safe rebasing with conflict resolution guidance
- `/rewrite-history` - Restructure commits for clean, reviewer-friendly PRs (automatic backup)

**Code maintenance:**
- `/clean-slop` - Remove AI-generated noise (redundant comments, verbose patterns)
- `/update-claude-md` - Create or maintain CLAUDE.md project instructions

**Skills** (auto-invoked):
- `maximize-info-density` - Compress docs/prompts losslessly for reduced token usage

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-extras@claude-code-plugins-marketplace
```

## License

MIT
