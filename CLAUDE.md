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

# Run consultant CLI
uvx --from claude-plugins/consultant/skills/consultant/scripts consultant-cli --help
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

**Naming convention**: Use kebab-case (`-`) for all file, command, and agent names (e.g., `bug-fixer.md`, `/clean-slop`).

### Tool Definitions

**Skills/Commands**: Omit `tools` frontmatter to inherit all tools from the invoking context (recommended default).

**Agents**: MUST explicitly declare all needed tools in frontmatter—agents run in isolation and won't inherit tools.

**Common agent patterns**:
- Has `Bash` → add `BashOutput` (for long-running commands)
- Uses todo tracking → add `TodoWrite`
- Writes files (logs, notes) → add `Write`
- Invokes other skills → add `Skill`
- Spawns sub-agents → add `Task`
- Searches files → add `Glob`, `Grep`

**Agent audit**: Read the skill/prompt the agent follows, identify every tool mentioned (explicit or implicit), verify all are in frontmatter.

See each plugin's README for architecture details.

## Plugin Versioning

When updating plugin files, bump version in `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new commands/agents
- **Major** (x.0.0): Breaking changes

README-only changes don't require version bumps.

## Adding New Components

When adding commands, agents, skills, or hooks:
1. Create the component file in the appropriate directory
2. Bump plugin version (minor for new features)
3. Update affected plugin's `README.md` and repo root `README.md` if needed
4. Update `plugin.json` description/keywords if the new component adds significant capability

**README Guidelines**: Keep READMEs high-level (overview, what it does, how to use). Avoid implementation details that require frequent updates—readers can explore code for specifics.

## Before PR

```bash
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy
```

Bump plugin version if plugin files changed.
