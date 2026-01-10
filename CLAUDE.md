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

## Foundational Documents

Read before building plugins:

- **@docs/CUSTOMER.md** - Who we build for, messaging guidelines
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

### Plugin Components

Each plugin can contain:
- `agents/` - Specialized agent definitions (markdown)
- `skills/` - Skills with `SKILL.md` files in subdirectories (e.g., `skills/review/SKILL.md`)
- `hooks/` - Event handlers for Claude Code events

**Naming convention**: Use kebab-case (`-`) for all file, skill, and agent names (e.g., `bug-fixer.md`, `/clean-slop`).

### Skills (Unified Model - Claude Code 2.1.3+)

As of Claude Code 2.1.3, skills and commands are unified. All skills:
- Appear in the `/` menu by default (opt-out with `user-invocable: false`)
- Can be auto-invoked by Claude based on semantic matching with the description
- Can be explicitly invoked via `/skill-name`

**Required frontmatter fields:**
```yaml
---
name: skill-name        # Lowercase, hyphens, max 64 chars
description: '...'      # What it does + when to use (max 1024 chars)
argument-hint: '...'    # Optional - hint for arguments
---
```

**File structure:** `skills/{skill-name}/SKILL.md`

### Skill Description Best Practices

Skill descriptions drive auto-invocation. Claude uses semantic matching to decide when to invoke a skill based on its description.

**Pattern**: What it does + When to use it + Trigger terms

| Do | Don't |
|----|-------|
| Third person: "Compresses documents..." | First/second person: "I can help you..." |
| Include trigger terms users say: "debug, troubleshoot, fix bug" | Use jargon users won't say: "EARS-syntax" |
| Specify when to use: "Use when asked to..." | Vague purpose: "Helps with documents" |
| Keep under 1024 chars | Verbose implementation details |

**Example**:
```yaml
# Bad - vague, no triggers
description: 'Helps with bugs'

# Good - specific + triggers + when to use
description: 'Investigates and fixes bugs systematically. Use when asked to debug, troubleshoot, fix a bug, or find why something is broken.'
```

### Tool Definitions

**Skills**: Omit `tools` frontmatter to inherit all tools from the invoking context (recommended default).

**Agents**: MUST explicitly declare all needed tools in frontmatter—agents run in isolation and won't inherit tools.

### Invoking Skills from Skills

When a skill needs to invoke another skill, use the explicit Skill tool pattern:

```markdown
Use the Skill tool to <action>: Skill("<plugin>:<skill>", "$ARGUMENTS")
```

Examples:
- `Use the Skill tool to build a requirements spec: Skill("vibe-workflow:spec", "$ARGUMENTS")`
- `Use the Skill tool to craft a CUSTOMER.md document: Skill("solo-dev:define-customer-profile")`

**Why**: Natural language like "Use the X skill" is ambiguous—Claude may just read the skill file instead of invoking it. The explicit `Skill(...)` pattern ensures the Skill tool is actually called.

**Common agent patterns**:
- Has `Bash` → add `BashOutput` (for long-running commands)
- Uses todo tracking → add `TodoWrite`
- Writes files (logs, notes) → add `Write`
- Invokes other skills → add `Skill`
- Spawns sub-agents → add `Task`
- Searches files → add `Glob`, `Grep`

**Agent audit**: Read the skill/prompt the agent follows, identify every tool mentioned (explicit or implicit), verify all are in frontmatter.

### Memento Pattern for Non-Trivial Workflows

Skills and agents with multi-phase workflows MUST use the memento pattern:
- **Create todo list immediately** (TodoWrite) - areas to discover, not fixed steps
- **Include expansion placeholder** - e.g., `- [ ] (expand as discovery reveals new areas)`
- **External memory file** - log file in `/tmp/` updated after EACH step
- **Never proceed without writing findings** - log is external memory
- **Expand todos dynamically** - as user answers or research reveals new areas

See `vibe-workflow/skills/spec/SKILL.md` or `vibe-workflow/skills/plan/SKILL.md` for reference implementations.

See each plugin's README for architecture details.

## Plugin Versioning

When updating plugin files, bump version in `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new commands/agents
- **Major** (x.0.0): Breaking changes

README-only changes don't require version bumps.

## Adding New Components

When adding skills, agents, or hooks:
1. Create the component file in the appropriate directory
2. Bump plugin version (minor for new features)
3. Update affected plugin's `README.md` and repo root `README.md`
4. Update `plugin.json` description/keywords if the new component adds significant capability

**README sync checklist** (when adding/renaming/removing components):
- `README.md` (root) - Available Plugins section, directory structure
- `claude-plugins/README.md` - Plugin table
- `claude-plugins/<plugin>/README.md` - Component lists

**README Guidelines**: Keep READMEs high-level (overview, what it does, how to use). Avoid implementation details that require frequent updates—readers can explore code for specifics.

## Before PR

```bash
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy
```

Bump plugin version if plugin files changed.
