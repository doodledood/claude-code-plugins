# Plugin Name Template

Use this template as a starting point for creating your own Claude Code plugin.

## Plugin Structure

```
your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin metadata
├── commands/                 # Optional: Custom slash commands
│   └── example.md
├── agents/                   # Optional: Custom agents
│   └── example-agent.md
├── skills/                   # Optional: Agent skills
│   └── example-skill/
│       └── SKILL.md
├── hooks/                    # Optional: Event handlers
│   └── hooks.json
└── README.md                # This file
```

## Setup Instructions

1. **Copy this template:**
   ```bash
   cp -r claude-plugins/PLUGIN_TEMPLATE claude-plugins/your-plugin-name
   ```

2. **Edit plugin.json:**
   Update `.claude-plugin/plugin.json` with your plugin details:
   ```json
   {
     "name": "your-plugin-name",
     "description": "What your plugin does",
     "version": "1.0.0",
     "author": {
       "name": "Your Name",
       "email": "your.email@example.com"
     }
   }
   ```

3. **Add components:**
   - Commands: Create `.md` files in `commands/`
   - Agents: Create `.md` files in `agents/`
   - Skills: Create skill folders with `SKILL.md` in `skills/`
   - Hooks: Add `hooks.json` configuration

4. **Register in marketplace:**
   Add entry to `.claude-plugin/marketplace.json`

5. **Test locally:**
   ```bash
   /plugin marketplace add /path/to/claude-code-plugins
   /plugin install your-plugin-name@claude-code-plugins-marketplace
   ```

## Component Examples

### Command (commands/example.md)

```markdown
---
description: Brief description of what this command does
---

# Command Instructions

Your detailed instructions here. This content becomes part of Claude's context when the command is invoked.

You can include:
- Step-by-step instructions
- Code examples
- Best practices
- Expected outputs
```

### Agent (agents/example-agent.md)

```markdown
---
description: Specialized agent for specific tasks
tools: [Bash, Read, Write, Grep]  # Tools this agent can use
---

# Agent Instructions

Define the agent's:
- Purpose and capabilities
- Workflow and approach
- Tools it should use
- Output format
```

### Skill (skills/example-skill/SKILL.md)

```markdown
# Skill Name

Brief description of what this skill provides.

## When to Use

Describe when Claude should invoke this skill.

## Capabilities

Detail what the skill enables Claude to do.

## Usage Examples

Provide clear examples.
```

### Hooks (hooks/hooks.json)

```json
{
  "user-prompt-submit": {
    "command": "echo 'Hook triggered!'",
    "description": "Runs when user submits a prompt"
  }
}
```

## Testing Checklist

- [ ] Plugin installs without errors
- [ ] Commands appear and execute correctly
- [ ] Agents are accessible and functional
- [ ] Skills activate in appropriate contexts
- [ ] Hooks trigger at correct events
- [ ] README documentation is clear
- [ ] Version number follows semver

## Publishing

1. Ensure all tests pass
2. Update version in plugin.json
3. Add entry to marketplace.json
4. Create pull request
5. Wait for review and merge

## Resources

- [Plugin Development Guide](./README.md)
- [Claude Code Docs](https://code.claude.com/docs)
- [Example Plugins](https://github.com/claudecodeplugins)
