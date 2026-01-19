# CLAUDE.md

## Project Overview

Claude Code plugins marketplace - a curated collection of plugins with agents, skills, and hooks.

## Development Commands

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Test hooks (run after ANY hook changes)
pytest tests/hooks/ -v

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
- `skills/` - Skills with `SKILL.md` files (replaces deprecated commands)
- `hooks/` - Event handlers for Claude Code events
- `tests/hooks/` - Test suite for hooks (at repo root)

**Naming convention**: Use kebab-case (`-`) for all file and skill names (e.g., `bug-fixer.md`, `clean-slop`).

### Hooks

Hooks are Python scripts in `hooks/` that respond to Claude Code events. Shared utilities live in `hook_utils.py`.

**Hook structure** (vibe-workflow):
- `hook_utils.py` - Shared transcript parsing, reminder strings, state extraction
- `session_start_reminder.py` - Injects agent preference reminders at session start
- `post_compact_hook.py` - Re-anchors after compaction with session reminders + implement recovery
- `post_todo_write_hook.py` - Reminds to update log files after todo completion during implement workflows
- `stop_todo_enforcement.py` - Blocks premature stops during implement workflows

**When modifying hooks**:
1. Run tests: `pytest tests/hooks/ -v`
2. Run linting: `ruff check --fix claude-plugins/vibe-workflow/hooks/ && black claude-plugins/vibe-workflow/hooks/`
3. Run type check: `mypy claude-plugins/vibe-workflow/hooks/`

**Test coverage**: Tests in `tests/hooks/` cover edge cases (invalid JSON, missing files, malformed transcripts), workflow detection, todo state extraction, and hook output format. Add tests for any new hook logic.

### Skills

Skills are the primary way to extend Claude Code. Each skill lives in `skills/{skill-name}/SKILL.md`.

**Invocation modes**:
- **Auto-invoked**: Claude discovers and invokes skills based on semantic matching with the description
- **User-invoked**: Users can explicitly invoke via `/skill-name` (controlled by `user-invocable` frontmatter, defaults to `true`)
- **Programmatic**: Other skills invoke via `Skill("plugin:skill-name", "$ARGUMENTS")`

**Skill frontmatter**:
```yaml
---
name: skill-name           # Required: lowercase, hyphens, max 64 chars
description: '...'         # Required: max 1024 chars, drives auto-discovery
user-invocable: true       # Optional: show in slash command menu (default: true)
---
```

### Writing Skill and Agent Prompts

A prompt should act as a manifest for the agent: clear goal, clear constraints, freedom in execution.

**Principles:**

1. **Define WHAT and WHY, not HOW** - State goals and constraints. Don't prescribe steps the model knows how to do. No rigid phase ordering, no heuristics tables that become checklists.

2. **Operate under the memento pattern** - For non-trivial workflows, the agent should create a todo list immediately, write findings to a log file as it works, and refresh context before synthesis. This isn't optional structure—it's a constraint that makes the agent work better.

3. **Trust capability, enforce discipline** - The model knows how to search, analyze, generate. What it needs are guardrails: "write to log before proceeding", "refresh before synthesis", "don't skip verification".

4. **Output structure when needed** - If the artifact has a specific format (manifest schema, report template), define it. Otherwise let the agent decide.

**The test**: Is this prompt a manifest? Clear goal, clear constraints, clear output—but the agent decides how to get there.

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

Skills and agents with multi-phase workflows MUST use the memento pattern. This pattern directly addresses documented LLM limitations (see `docs/LLM_CODING_CAPABILITIES.md`).

**Important**: When implementing this pattern in skills/agents, DO NOT mention the pattern by name (e.g., "memento pattern", "memento loop"). Simply follow the pattern—use descriptive labels like "Write findings to log", "Discovery Loop", "Refresh context" without referencing pattern terminology. The pattern should be invisible to users.

#### Why: The LLM Limitations

| Limitation | Research Finding | Pattern Response |
|------------|------------------|------------------|
| **Context rot** | Information in the middle of context gets "lost"—U-shaped attention curve with >20% accuracy degradation for middle-positioned content | Write findings to external file after EACH step; file persists where conversation content degrades |
| **Working memory** | LLMs reliably track only 5-10 variables; beyond this, state management fails | TodoWrite externalizes all tracked areas; each todo = one "variable" in external memory |
| **Holistic synthesis failure** | <50% accuracy on synthesis tasks at 32K tokens; models excel at needle retrieval but fail at aggregation across full context | Read full log file BEFORE synthesis—converts degraded scattered context into concentrated recent content |
| **Recency bias** | Models pay highest attention to content at context end | Refresh step moves ALL findings to context end where attention is strongest |
| **Premature completion** | Agents mark tasks "done" without verification; later instances see partial progress and "declare the job done" | Expansion placeholders signal incompleteness; explicit write-to-log todos ensure nothing is skipped |

#### Todos as Micro-Prompts

Each todo is a micro-prompt. Apply compression—goal + acceptance criteria + discipline:
- **Goal**: WHAT to achieve, not HOW (model knows how to investigate)
- **Acceptance criteria**: WHAT defines success—models are RL-trained to satisfy these (e.g., `; done when X`)
- **Discipline markers**: `→log` after collection; `refresh:` before synthesis
- **Drop capability**: Model knows what to capture, how to search, what's relevant
- **Novel constraints inline**: Only counter-intuitive rules model wouldn't guess

#### The Pattern: Full Specification

**1. Create todo list immediately** with areas to discover, not fixed steps:

```
- [ ] Create log /tmp/{workflow}-*.md
- [ ] Decompose $ARGUMENTS→areas→log; done when all areas identified
- [ ] Investigate [primary area]→log; done when key findings captured
- [ ] (expand: areas as discovered)
- [ ] Refresh: read full log    ← CRITICAL: never skip
- [ ] Synthesize→final artifact; done when artifact complete + validated
```

**2. Write to log after each investigation** (discipline, not capability):

```
- [x] Investigate auth flow→log; done when flow documented
- [x] Investigate error handling→log; done when patterns identified
- [ ] Investigate caching layer→log; done when cache strategy understood
```

**3. Expand todos dynamically** as work reveals new areas:

```
Before:
- [ ] Investigate API layer→log; done when architecture understood
- [ ] (expand: areas as discovered)

After (discovered 3 sub-areas):
- [x] Investigate API layer→log; found: auth, validation, rate-limiting
- [ ] Investigate auth middleware→log; done when auth flow mapped
- [ ] Investigate validation layer→log; done when rules documented
- [ ] Investigate rate-limiting→log; done when limits + behavior understood
- [ ] (expand: additional areas)
```

**4. Refresh context BEFORE synthesis** (non-negotiable):

```
- [x] Investigate [final area]→log; done when findings captured
- [x] Refresh: read full log    ← Must complete BEFORE synthesize
- [ ] Synthesize→final artifact; done when all findings integrated + validated
```

**Why the refresh step is critical**: By the synthesis phase, earlier findings have degraded due to context rot. The log file contains ALL findings written throughout the workflow. Reading the full file immediately before output:
- Moves all findings to context END (highest attention zone)
- Converts holistic synthesis (poor LLM performance) into dense recent context (high LLM performance)
- Restores details that would otherwise be "lost in the middle"

#### Quick Reference

| Phase | Todo Style | Why |
|-------|------------|-----|
| Start | `Create log /tmp/{x}-*.md` | External memory |
| Each step | `Investigate [area]→log; done when X` | Goal + acceptance criteria + discipline |
| Discovery | `(expand: areas as discovered)` | Signals incompleteness |
| Before synthesis | `Refresh: read full log` | Restores context to high-attention zone |
| End | `Synthesize→artifact; done when Y` | Clear output target + success condition |

**Never skip**: The `→log` writes and `refresh: read full log` step. These are the core mechanism that makes synthesis work despite context rot.

**Always include**: Acceptance criteria ("; done when X") so the model knows what success looks like.

See `vibe-workflow/skills/spec/SKILL.md`, `vibe-workflow/skills/plan/SKILL.md`, or `vibe-workflow/skills/research-web/SKILL.md` for reference implementations. Note how these implementations follow the pattern without naming it.

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

## Before PR

```bash
# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Run hook tests if hooks were modified
pytest tests/hooks/ -v
```

Bump plugin version if plugin files changed.
