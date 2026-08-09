# CLAUDE.md

## Project Overview

Claude Code plugins marketplace - a curated collection of plugins with agents, skills, and hooks.

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
- **@CONTEXT.md** - Project language and relationships
- **docs/LLM_CODING_CAPABILITIES.md** - LLM strengths/limitations, informs workflow design

## Project Language and Decision Records

**The glossary is not optional reading.** `CONTEXT.md` is imported above, so it is already in context. Where a harness does not support imports, read it at the start of every session before doing anything else. It exists to stop silent misreading, and nobody looks up a term they already believe they understand.

**Read `docs/adr/` before re-deciding something.** Open the index at `docs/adr/README.md` when you are about to settle a question this project may already have settled, and when a change contradicts or narrows an existing decision. Outside those two moments, leave it closed.

**Writing a decision record is one act, not three** — the record, the restatus of anything whose standing it changes, and the index, in one change. Step two is the one that gets dropped, and dropping any of them leaves the corpus asserting something untrue. Open `docs/adr/CONVENTIONS.md` before you start: it carries the bar, the template, and what each step actually requires.

The current records are a **seed reconstructed from this repository's own history**, not a complete account of every decision taken. One of the four says outright that its rationale could not be recovered. Treat the corpus as a starting point to grow, and add records as decisions are made rather than assuming the past is fully captured.

## Repository Structure

- `.claude-plugin/marketplace.json` - Registry of all plugins
- `claude-plugins/` - Individual plugins, each with `.claude-plugin/plugin.json`
- `pyproject.toml` - Python tooling config (ruff, black, mypy)

### Plugin Components

Each plugin can contain:
- `agents/` - Specialized agent definitions (markdown)
- `skills/` - Skills with `SKILL.md` files (replaces deprecated commands)
- `hooks/` - Event handlers for Claude Code events

**Naming convention**: Use kebab-case (`-`) for all file and skill names (e.g., `bug-fixer.md`, `clean-slop`).

### Hooks

Hooks are Python scripts in `hooks/` that respond to Claude Code events. Shared utilities live in `hook_utils.py`.

**When modifying hooks**:
1. Run linting: `ruff check --fix claude-plugins/<plugin>/hooks/ && black claude-plugins/<plugin>/hooks/`
2. Run type check: `mypy claude-plugins/<plugin>/hooks/`

### Skills

Skills are the primary way to extend Claude Code. Each skill lives in `skills/{skill-name}/SKILL.md`.

**Invocation modes**:
- **Auto-invoked**: Claude discovers and invokes skills based on semantic matching with the description
- **User-invoked**: Users can explicitly invoke via `/skill-name` (controlled by `user-invocable` frontmatter, defaults to `true`)
- **Programmatic**: Other skills can invoke skills by referencing them (e.g., "invoke the spec skill with arguments")

**Skill frontmatter**:
```yaml
---
name: skill-name           # Required: lowercase, hyphens, max 64 chars
description: '...'         # Required: max 1024 chars, drives auto-discovery
user-invocable: true       # Optional: show in slash command menu (default: true)
---
```

### Writing and Updating Prompts

**Run the `prompt-engineering` skill for all prompt work** - crafting new prompts, updating existing ones, or reviewing prompt structure. The skill encapsulates first-principles guidelines for writing effective prompts. Deliberately unscoped: it is supplied by whichever source is installed (currently synced from manifest-dev-tools), so naming a plugin here would break the moment it moves again.

### Tool Definitions

**Skills**: Omit `tools` frontmatter to inherit all tools from the invoking context (recommended default).

**Agents**: MUST explicitly declare all needed tools in frontmatter—agents run in isolation and won't inherit tools.

### Invoking Skills from Skills

When a skill needs to invoke another skill, use clear directive language:

```markdown
Invoke the <plugin>:<skill> skill with: "<arguments>"
```

Examples:
- `Invoke the vibe-extras:explore-codebase skill with: "$ARGUMENTS"`
- `Invoke the solo-dev:define-customer-profile skill`

**Why**: Vague language like "consider using the X skill" is ambiguous—Claude may just read the skill file instead of invoking it. Clear directives like "Invoke the X skill" ensure the skill is actually called.

**Common agent capabilities to declare in frontmatter**:
- Running commands → needs command execution tools
- Tracking progress → needs todo/task management tools
- Writing files (logs, notes) → needs file writing tools
- Invoking other skills → needs skill invocation tools
- Spawning sub-agents → needs agent spawning tools
- Searching files → needs file search tools

**Agent audit**: Read the skill/prompt the agent follows, identify every capability mentioned (explicit or implicit), verify all are declared in frontmatter.

See each plugin's README for architecture details.

## Plugin Versioning

When updating plugin files, bump version in `.claude-plugin/plugin.json`:
- **Patch** (0.0.x): Bug fixes, typos
- **Minor** (0.x.0): New features, new skills/agents
- **Major** (x.0.0): Breaking changes

README-only changes don't require version bumps.

**After version bump**: Add entry to `CHANGELOG.md`:
```
## YYYY-MM-DD
- [plugin-name] vX.Y.Z - Brief description of change
```

## Adding New Components

When adding agents, skills, or hooks:
1. Create the component file in the appropriate directory
2. Bump plugin version (minor for new features)
3. Update affected plugin's `README.md` and repo root `README.md`
4. Update `plugin.json` description/keywords if the new component adds significant capability

**README sync checklist** (when adding/renaming/removing components):
- `README.md` (root) - Available Plugins section, directory structure
- `claude-plugins/README.md` - Plugin table
- `claude-plugins/<plugin>/README.md` - Component lists

**README Guidelines**: Keep READMEs high-level (overview, what it does, how to use). Avoid implementation details that require frequent updates—readers can explore code for specifics.

## Authoring & Workflow Conventions

**Chunked markdown editing.** When authoring or restructuring a large markdown file (skills, references, prompts, manifests, READMEs), apply changes incrementally — Edit per section or stage the Write across multiple calls — rather than producing one giant Write. Catches drift early, keeps diffs reviewable, survives context interruptions cleanly. A single small Edit is fine for a single small change.

**Missing external source → WebFetch / WebSearch fallback.** When /do (or any task) needs an external source file the user expected to save locally (article markdown, dataset, transcript) and the file is missing, empty, or visibly truncated, attempt to acquire the source via WebFetch on the original URL first, then WebFetch on third-party mirrors / summaries, then WebSearch result excerpts as last resort. Synthesize the acquired content into the expected file path with an explicit provenance header (URL, fetch method, date). Re-run any pre-flight validity check before continuing. Halt via /escalate only when fallback yields nothing usable. Goal: get as close to the original as the environment allows rather than blocking on a missing local file.

## Before PR

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy
```

Bump plugin version if plugin files changed.
