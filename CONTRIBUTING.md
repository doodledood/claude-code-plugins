# Contributing to Claude Code Plugins Marketplace

Thank you for your interest in contributing! This guide will help you add plugins to our Claude Code marketplace.

## 🚀 Quick Start

1. **Fork and clone** the repository
2. **Create a branch**: `git checkout -b plugin/your-plugin-name`
3. **Use the template**: Copy `claude-plugins/PLUGIN_TEMPLATE` as your starting point
4. **Develop your plugin** following the structure below
5. **Test locally** before submitting
6. **Submit a PR** with your plugin

## 📋 Plugin Development Process

### Step 1: Copy the Template

```bash
cd claude-plugins
cp -r PLUGIN_TEMPLATE your-plugin-name
cd your-plugin-name
```

### Step 2: Update Plugin Metadata

Edit `.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin-name",
  "description": "Clear, concise description of what your plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "homepage": "https://github.com/doodledood/claude-code-plugins",
  "repository": {
    "type": "git",
    "url": "https://github.com/doodledood/claude-code-plugins.git"
  },
  "license": "MIT",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "category": "utilities"
}
```

#### Available Categories
- `utilities` - General purpose tools
- `development` - Development workflows
- `architecture` - Architecture & design
- `knowledge` - Knowledge management
- `testing` - Testing & QA
- `deployment` - DevOps & deployment
- `ai-tools` - AI/ML utilities

### Step 3: Add Plugin Components

Choose the components your plugin needs:

#### Commands (Slash Commands)
Create markdown files in `commands/`:

```markdown
---
description: Brief description shown in command list
---

# Command Name

Detailed instructions for Claude to follow when this command is invoked.

## Steps
1. First action
2. Second action
3. Final output

## Examples
...
```

**Example use cases:**
- Custom code generation patterns
- Specialized analysis workflows
- Project setup automation
- Documentation generation

#### Agents (Specialized Agents)
Create markdown files in `agents/`:

```markdown
---
description: What this agent specializes in
tools: [Bash, Read, Write, Grep, Glob]
---

# Agent Purpose

Define the agent's specialized capabilities and workflow.

## Approach
- How it should work
- What tools to use
- Expected outcomes
```

**Example use cases:**
- Code review automation
- Security analysis
- Performance optimization
- Refactoring assistance

#### Skills (Contextual Skills)
Create skill directories in `skills/` with `SKILL.md`:

```markdown
# Skill Name

Brief description of capabilities this skill provides.

## When to Use
Describe the contexts where Claude should activate this skill.

## Capabilities
- Feature 1
- Feature 2
- Feature 3

## Usage
Detailed usage instructions and examples.
```

**Example use cases:**
- Domain-specific knowledge
- Framework-specific patterns
- Language-specific best practices
- Tool integrations

#### Hooks (Event Handlers)
Add `hooks/hooks.json`:

```json
{
  "user-prompt-submit": {
    "command": "your-script.sh",
    "description": "What this hook does"
  },
  "before-tool-call": {
    "command": "validation-script.sh",
    "description": "Validates before tool execution"
  }
}
```

**Available hooks:**
- `user-prompt-submit` - Before processing user input
- `before-tool-call` - Before executing tools
- `after-tool-call` - After tool execution
- See [docs](https://code.claude.com/docs) for complete list

### Step 4: Register in Marketplace

Add your plugin to `.claude-plugin/marketplace.json`:

```json
{
  "name": "your-plugin-name",
  "source": "./claude-plugins/your-plugin-name",
  "description": "Brief description matching your plugin.json",
  "version": "1.0.0",
  "category": "utilities",
  "keywords": ["keyword1", "keyword2"]
}
```

### Step 5: Test Locally

```bash
# Add marketplace
/plugin marketplace add /path/to/claude-code-plugins

# Install your plugin
/plugin install your-plugin-name@claude-code-plugins-marketplace

# Test commands
/your-command

# Verify all components work
```

### Step 6: Documentation

Update your plugin's README.md:
- Clear description
- Installation instructions
- Usage examples
- Command reference
- Configuration options (if any)

## ✅ Pre-Submission Checklist

Before submitting your PR:

- [ ] Plugin name follows kebab-case convention
- [ ] `plugin.json` has all required fields
- [ ] Version follows semantic versioning (1.0.0)
- [ ] Commands have clear descriptions
- [ ] All components tested locally
- [ ] README.md is comprehensive
- [ ] Added to `marketplace.json`
- [ ] No sensitive information (API keys, secrets)
- [ ] License is compatible (MIT preferred)
- [ ] Code follows existing style
- [ ] Examples work as documented

## 🎯 Plugin Quality Guidelines

### Good Plugin Design
- **Single Responsibility**: Each plugin should do one thing well
- **Clear Naming**: Use descriptive, intuitive names
- **Good Documentation**: Include examples and use cases
- **Error Handling**: Provide helpful error messages
- **Composability**: Work well with other plugins

### Command Best Practices
- Start with clear intent statement
- Provide step-by-step instructions
- Include examples
- Specify expected outputs
- Handle edge cases

### Agent Best Practices
- Define clear scope and purpose
- Specify which tools to use
- Provide workflow structure
- Include success criteria

## 🔒 Security Guidelines

- Never include hardcoded secrets or API keys
- Validate and sanitize inputs
- Don't execute arbitrary code
- Follow principle of least privilege
- Document security considerations

## 📝 Pull Request Process

1. **Title**: `plugin: Add [plugin-name]` or `plugin: Update [plugin-name]`

2. **Description** should include:
   - What the plugin does
   - Why it's useful
   - How to test it
   - Screenshots/examples (if applicable)

3. **Review Process**:
   - Maintainers will review functionality
   - Test installation and usage
   - Provide feedback or request changes
   - Merge when approved

## 🐛 Reporting Issues

Found a bug? Please include:
- Plugin name and version
- Steps to reproduce
- Expected vs actual behavior
- Error messages
- Environment details

## 💡 Getting Help

- Check [existing plugins](./claude-plugins/) for examples
- Read [Claude Code docs](https://code.claude.com/docs)
- Ask in [GitHub Discussions](https://github.com/doodledood/claude-code-plugins/discussions)
- Review [Plugin Template](./claude-plugins/PLUGIN_TEMPLATE/)

## 🌟 Plugin Ideas

Looking for inspiration? Consider creating plugins for:

- **Code Generation**: Framework scaffolding, boilerplate generation
- **Analysis**: Code quality, security scanning, dependency analysis
- **Documentation**: API docs, README generation, changelog automation
- **Testing**: Test generation, coverage analysis, fixture creation
- **Deployment**: CI/CD workflows, environment setup, release automation
- **Knowledge**: Team standards, best practices, architecture patterns

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the work, not the person
- Help others learn and grow

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Claude Code Plugins marketplace! 🎉
