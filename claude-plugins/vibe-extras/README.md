# Vibe Extras

Standalone utilities for codebase exploration, web research, git operations, and code maintenance.

## Commands

**Research & exploration:**
- `/explore-codebase` - Structural overview with prioritized file list (quick/medium/thorough/very-thorough)
- `/research-web` - Deep web research with parallel investigators and multi-wave synthesis

**Git utilities:**
- `/rebase-on-main` - Safe rebasing with conflict resolution guidance
- `/rewrite-history` - Rewrite branch into narrative-quality commits (backup + byte-identical verification)

**Code maintenance:**
- `/clean-slop` - Remove AI-generated noise (redundant comments, verbose patterns)
- `/update-claude-md` - Create or maintain CLAUDE.md project instructions

## Agents

- `codebase-explorer` - Context-gathering agent for finding files to read. Maps codebase structure, returns overview + prioritized file list with line ranges.
- `web-researcher` - Web research analyst using structured hypothesis tracking to gather and synthesize information from online sources.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-extras@claude-code-plugins-marketplace
```

## License

MIT
