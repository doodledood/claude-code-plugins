# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code plugins marketplace - a curated collection of plugins that extend Claude Code with specialized agents, skills, commands, and hooks.

## Development Commands

### Python Linting & Formatting

```bash
# Run ruff linter
ruff check claude-plugins/

# Auto-fix ruff issues
ruff check --fix claude-plugins/

# Format with black
black claude-plugins/

# Type check with mypy (strict mode)
mypy
```

### Testing Plugins Locally

```bash
# Add local marketplace to Claude Code
/plugin marketplace add /path/to/claude-code-plugins

# Install a specific plugin
/plugin install consultant@claude-code-plugins-marketplace
/plugin install planning@claude-code-plugins-marketplace

# List available plugins
/plugin marketplace list
```

### Running the Consultant CLI

The consultant plugin's Python CLI uses uv for automatic dependency management:

```bash
# Always use --upgrade to get latest litellm
uv run --upgrade claude-plugins/consultant/skills/consultant/scripts/consultant_cli.py --help

# Example invocation
uv run --upgrade claude-plugins/consultant/skills/consultant/scripts/consultant_cli.py \
  --prompt "Review this code" \
  --file src/*.py \
  --slug "review-session"
```

## Architecture

### Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins in this marketplace
- `claude-plugins/` - Individual plugins, each with its own `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling configuration (ruff, black, mypy)

### Plugin Components

Each plugin can contain:
- `agents/` - Specialized agent definitions (markdown)
- `commands/` - Slash command definitions (markdown with frontmatter)
- `skills/` - Contextual skills with `SKILL.md` files
- `hooks/` - Event handlers triggered by Claude Code events

### Consultant Plugin Architecture

The consultant plugin (`claude-plugins/consultant/`) provides multi-provider LLM consultations:

```
consultant/
├── skills/consultant/scripts/     # Python CLI implementation
│   ├── consultant_cli.py          # Main entry point
│   ├── litellm_client.py          # LiteLLM wrapper
│   ├── model_selector.py          # Auto model selection
│   ├── session_manager.py         # Async session handling
│   └── config.py                  # Configuration constants
├── agents/consultant-consulter.md # Agent that orchestrates the CLI
└── commands/                      # Slash commands (/consultant-review, etc.)
```

The CLI uses PEP 723 inline script metadata for automatic dependency installation via uv.

### Planning Plugin Architecture

The planning plugin (`claude-plugins/planning/`) provides planning skills:
- `plan` skill - Mini-PR based implementation plans
- `execplan` skill - Comprehensive execution plans following PLANS.md methodology
- `hooks/check-planning-keywords.py` - Auto-detects planning keywords in prompts

## Python Code Style

- Target Python 3.9+
- Strict mypy type checking enabled
- Line length: 88 (black default)
- Import order managed by ruff isort
