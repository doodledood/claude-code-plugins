# Plugin Template

Starting point for creating Claude Code plugins.

## Structure

```
your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: metadata
├── commands/                 # Slash commands (explicit invocation)
│   └── example.md
├── agents/                   # Specialized agents
│   └── example-agent.md
├── skills/                   # Auto-invoked based on context
│   └── example-skill/
│       └── SKILL.md
├── hooks/                    # Event handlers
│   └── hooks.json
└── README.md
```

## Setup

1. Copy this template:
   ```bash
   cp -r claude-plugins/PLUGIN_TEMPLATE claude-plugins/your-plugin-name
   ```

2. Edit `.claude-plugin/plugin.json`:
   ```json
   {
     "name": "your-plugin-name",
     "description": "What it does",
     "version": "1.0.0"
   }
   ```

3. Add components as needed

4. Register in `.claude-plugin/marketplace.json`

5. Test locally:
   ```bash
   /plugin marketplace add /path/to/claude-code-plugins
   /plugin install your-plugin-name@claude-code-plugins-marketplace
   ```

## Commands vs Skills

**Skills** are auto-invoked by Claude based on semantic matching. Use for capabilities Claude should use automatically when relevant.

**Commands** require explicit `/command` invocation. Use for workflows that need user intent.

See [CLAUDE.md](../../CLAUDE.md) for detailed guidelines.

## Testing

- [ ] Plugin installs without errors
- [ ] Commands execute correctly
- [ ] Agents are accessible
- [ ] Skills activate in appropriate contexts

## Resources

- [CLAUDE.md](../../CLAUDE.md) - Development guidelines
- [Claude Code Docs](https://code.claude.com/docs)
