# Claude Code Plugins Marketplace

Welcome to the Claude Code plugins marketplace! This is a curated collection of plugins designed to enhance your development workflow with Claude Code.

## 🚀 Quick Start

### Installing the Marketplace

Add this marketplace to your Claude Code:

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
```

Or, for local development:

```bash
/plugin marketplace add /path/to/claude-code-plugins
```

### Installing Plugins

Once the marketplace is added, install any plugin:

```bash
/plugin install consultant@claude-code-plugins-marketplace
/plugin install oracle@claude-code-plugins-marketplace
/plugin install planning@claude-code-plugins-marketplace
```

List available plugins:

```bash
/plugin marketplace list
```

## 📦 Available Plugins

### consultant (v1.0.0)
Flexible multi-provider LLM consultations using Python/LiteLLM for deep AI-powered code analysis across 100+ models.

**Features:**
- `consultant-consulter` agent - Expert agent for multi-provider AI analysis with automatic model selection
- `/consultant-review` command - Production-level PR reviews with severity-tagged findings
- `/consultant-investigate-bug` command - Deep bug investigation with root cause analysis
- `/consultant-execplan` command - Comprehensive execution planning with architectural analysis
- `consultant` skill - Python/LiteLLM CLI knowledge and best practices

**Key Capabilities:**
- 100+ LLM provider support (OpenAI, Anthropic, Google, Azure, Bedrock, local models)
- Custom base URLs for any provider or local LLM server
- Automatic model discovery via `/v1/models` endpoint
- Intelligent model selection with scoring algorithm
- Token counting with pre-flight validation
- Async execution with session management
- OPENAI_BASE_URL environment variable support

**Requirements:**
```bash
pip install litellm requests
```

**Category:** development
**Keywords:** consultant, code-review, analysis, architecture, bug-investigation, ai-analysis, litellm, multi-provider, local-models

---

### oracle (v1.0.0)
Comprehensive code analysis using oracle CLI tool for deep AI-powered reviews and architectural analysis.

**Features:**
- `oracle-consulter` agent - Expert agent for high-token AI analysis workflows
- `/oracle-review` command - Production-level PR reviews with severity-tagged findings
- `/oracle-investigate-bug` command - Deep bug investigation with root cause analysis
- `oracle` skill - Oracle CLI knowledge and best practices

**Category:** development
**Keywords:** oracle, code-review, analysis, architecture, bug-investigation, ai-analysis

---

### planning (v1.0.0)
Comprehensive planning tools with automatic keyword detection via hooks.

**Features:**
- `plan` skill - Mini-PR based implementation plans for iterative development
- `execplan` skill - Comprehensive execution plans following PLANS.md methodology
- `/oracle-execplan` command - Deep planning analysis using oracle CLI
- `check-planning-keywords.py` hook - Auto-detects "plan" or "execplan" keywords and activates appropriate skills

**Category:** development
**Keywords:** planning, execplan, implementation-plan, methodology, hooks

---

## 🛠️ Contributing Your Own Plugin

We welcome contributions! Here's how to add your plugin to this marketplace:

### Plugin Structure

Create your plugin in the `claude-plugins/` directory:

```
claude-plugins/
└── your-plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json          # Required: Plugin metadata
    ├── commands/                 # Optional: Custom slash commands
    ├── agents/                   # Optional: Custom agents
    ├── skills/                   # Optional: Agent skills
    └── hooks/                    # Optional: Event handlers
```

### 1. Create Plugin Metadata

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin-name",
  "description": "Brief description of what your plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "homepage": "https://github.com/doodledood/claude-code-plugins",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "category": "utilities"
}
```

### 2. Add Plugin Components

#### Commands
Create markdown files in `commands/` directory:

```markdown
---
description: Short description of the command
---

# Command Instructions

Your command instructions here. This content will be added to Claude's context when the command is invoked.
```

#### Agents
Create markdown files in `agents/` directory with specialized agent instructions.

#### Skills
Create skill directories in `skills/` with `SKILL.md` files that Claude can invoke contextually.

### 3. Register in Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin-name",
  "source": "./claude-plugins/your-plugin-name",
  "description": "Brief description",
  "version": "1.0.0",
  "category": "utilities",
  "keywords": ["keyword1", "keyword2"]
}
```

### 4. Test Locally

```bash
# Add local marketplace
/plugin marketplace add ./path/to/claude-code-plugins

# Install your plugin
/plugin install your-plugin-name@claude-code-plugins-marketplace

# Test your commands (if any)
/your-command

# Test agents are available (if any)
# Agents will be available when needed based on their description
```

### 5. Submit Pull Request

1. Create a new branch: `git checkout -b plugin/your-plugin-name`
2. Add your plugin files
3. Update `.claude-plugin/marketplace.json`
4. Commit and push
5. Create a pull request

## 📋 Plugin Categories

- **utilities** - General purpose tools and helpers
- **development** - Development workflow enhancements
- **architecture** - Architecture and design tools
- **knowledge** - Knowledge management and documentation
- **testing** - Testing and quality assurance
- **deployment** - Deployment and DevOps tools
- **ai-tools** - AI and machine learning utilities

## 📚 Resources

- [Official Claude Code Documentation](https://code.claude.com/docs)
- [Plugin Marketplace Guide](https://code.claude.com/docs/en/plugin-marketplaces)
- [MCP Server Documentation](https://modelcontextprotocol.io)
- [Example Plugins](https://github.com/claudecodeplugins)

## 🤝 Community & Support

- Report issues: [GitHub Issues](https://github.com/doodledood/claude-code-plugins/issues)
- Discussions: [GitHub Discussions](https://github.com/doodledood/claude-code-plugins/discussions)

## 📄 License

This marketplace and all contributed plugins are licensed under MIT unless otherwise specified.
