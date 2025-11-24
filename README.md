# Claude Code Plugins Marketplace
A curated marketplace of Claude Code plugins for agentic development workflows, featuring tools for architecture, knowledge management, and development automation.

## 🎯 What is This?

This is a **Claude Code plugins marketplace** - a curated collection of plugins that enhance your development workflow with Claude Code, focusing on agentic development, code analysis, and planning tools.

## 🚀 Quick Start - Using the Marketplace

### Install the Marketplace

Add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
```

For local development:

```bash
/plugin marketplace add /path/to/claude-code-plugins
```

### Browse & Install Plugins

```bash
# List available marketplaces
/plugin marketplace list

# List all plugins
/plugin list

# Install a specific plugin
/plugin install consultant@claude-code-plugins-marketplace
```

## 📦 Available Plugins

All plugins are located in `claude-plugins/`:

#### consultant (v1.0.0)
Flexible multi-provider LLM consultations using Python/LiteLLM for deep AI-powered code analysis across 100+ models.

**Components:**
- **Agent:** `consultant-consulter` - Expert agent for multi-provider AI analysis with automatic model selection
- **Commands:**
  - `/consultant-review` - Production-level PR reviews with severity-tagged findings
  - `/consultant-investigate-bug` - Deep bug investigation with root cause analysis
  - `/consultant-execplan` - Comprehensive execution planning with architectural analysis
- **Skill:** `consultant` - Python/LiteLLM CLI knowledge and best practices
- **Category:** development
- **Key Features:**
  - 100+ LLM provider support (OpenAI, Anthropic, Google, Azure, local models)
  - Custom base URLs for local LLM deployments
  - Automatic model discovery and selection
  - Token management with context validation
  - Async execution with session reattachment

#### planning (v1.0.0)
Comprehensive planning tools with automatic keyword detection via hooks.

**Components:**
- **Skills:**
  - `plan` - Mini-PR based implementation plans
  - `execplan` - Comprehensive execution plans following PLANS.md
- **Hook:** `check-planning-keywords.py` - Auto-detects planning keywords and activates skills
- **Category:** development

> More plugins coming soon!

## 🛠️ Development

### Repository Structure

```
claude-code-plugins/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace configuration
├── claude-plugins/            # Claude Code plugins directory
│   ├── README.md             # Plugin development guide
│   ├── PLUGIN_TEMPLATE/      # Template for creating new plugins
│   ├── consultant/           # Consultant plugin (Python/LiteLLM)
│   └── planning/             # Planning plugin
├── CONTRIBUTING.md            # Contributing guidelines
└── README.md                  # This file
```

### Contributing Plugins

See [claude-plugins/README.md](./claude-plugins/README.md) for detailed instructions on:
- Creating new plugins
- Plugin structure and components
- Testing locally
- Submitting contributions

## 🎓 Learn More

- [Claude Code Documentation](https://code.claude.com/docs)
- [Plugin Marketplaces Guide](https://code.claude.com/docs/en/plugin-marketplaces)
- [Model Context Protocol](https://modelcontextprotocol.io)

## 📄 License

MIT

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Add your tool or plugin
4. Submit a pull request

For plugin contributions, see the [plugin development guide](./claude-plugins/README.md).
