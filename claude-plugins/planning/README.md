# Planning Plugin

Implementation planning tools with automatic keyword detection.

## What It Does

- **Implementation Plans** - Mention "plan" in your message for mini-PR based plans optimized for iterative development
- **Execution Plans** - Mention "execplan" for comprehensive, self-contained plans for complex features

The plugin includes a hook that automatically detects planning keywords and activates the appropriate methodology.

Use `/help` after installation to see all available skills.

## Requirements

- Python 3 (for hook script)

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install planning@claude-code-plugins-marketplace
```

## License

MIT
