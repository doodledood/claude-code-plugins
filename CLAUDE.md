# CLAUDE.md

## Project Overview

Claude Code plugins marketplace - a curated collection of plugins with agents, skills, commands, and hooks.

## Development Commands

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Test plugin locally
/plugin marketplace add /path/to/claude-code-plugins
/plugin install consultant@claude-code-plugins-marketplace

# Run consultant CLI (always use --upgrade for latest litellm)
uv run --upgrade claude-plugins/consultant/skills/consultant/scripts/consultant_cli.py --help
```

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

### Plugin Components

Each plugin can contain:
- `agents/` - Specialized agent definitions (markdown)
- `commands/` - Slash commands (markdown with frontmatter)
- `skills/` - Contextual skills with `SKILL.md` files
- `hooks/` - Event handlers for Claude Code events

See each plugin's README for architecture details.

## Plugin Versioning

When updating plugin files, bump version in `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new commands/agents
- **Major** (x.0.0): Breaking changes

README-only changes don't require version bumps.

## Before PR

```bash
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy
```

Bump plugin version if plugin files changed.
