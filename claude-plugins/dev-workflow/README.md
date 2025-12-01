# Dev Workflow Plugin

Developer workflow tools for maintaining project documentation and setup.

## Overview

This plugin helps maintain high-quality CLAUDE.md files - the highest-leverage configuration point for Claude Code projects. It follows best practices for brevity, universal applicability, and progressive disclosure.

## Components

### Command: `/update_claude_md`

Create or update CLAUDE.md with best practices.

**Usage:**
```bash
# Create or update CLAUDE.md
/update_claude_md

# Focus on specific area
/update_claude_md add testing commands

# Address specific issue
/update_claude_md fix outdated build instructions
```

**What it does:**
- Analyzes your codebase to understand structure and tooling
- Creates/updates CLAUDE.md following best practices
- Ensures brevity (LLMs follow ~150 instructions reliably)
- Uses progressive disclosure for complex projects

## Best Practices Applied

### Structure (WHAT, WHY, HOW)
- **WHAT**: Tech stack, project structure, key entry points
- **WHY**: Project purpose, component relationships, domain terminology
- **HOW**: Build/test/run commands, verification steps

### Length Guidelines
| Project Type | Lines |
|--------------|-------|
| Simple | 30-60 |
| Standard | 60-150 |
| Complex | 150-300 max |

### Do
- Universal instructions (apply to all tasks)
- Imperative language ("Run X" not "You should run X")
- Verified commands (tested, working)
- Reference README (don't copy)

### Don't
- Style rules → use linters/formatters instead
- Task-specific instructions → gets ignored if not relevant
- File/function enumeration → describe patterns instead
- Auto-generated boilerplate

### Progressive Disclosure

For complex projects, create separate docs and reference them:
```
docs/testing.md, docs/architecture.md, docs/conventions.md
```
Then in CLAUDE.md: "See docs/testing.md for test patterns"

## Examples

**Bad:**
```markdown
Always use camelCase. Document with JSDoc. Follow SOLID principles.
```

**Good:**
```markdown
npm test  # Required before PR
```

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install dev-workflow@claude-code-plugins-marketplace
```

## License

MIT
