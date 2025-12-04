# Vibe Workflow Plugin

Autonomous feature development workflow for Claude Code.

## Overview

This plugin enables Claude to develop features as autonomously as possible - from planning through implementation to review.

## Components

### Agents

#### `code-implementor`
Implements well-defined coding tasks using a strict incremental workflow. Makes small changes (5-30 lines), runs quality gates (Typecheck → Tests → Lint) after every change, and proceeds only when green.

#### `code-maintainability-reviewer`
Performs comprehensive maintainability audits identifying DRY violations, dead code, YAGNI violations, unnecessary complexity, and consistency issues. Use after implementing features or before PRs.

#### `test-coverage-auditor`
Analyzes diffs between your branch and main to ensure all new/modified logic has adequate test coverage. Provides specific test recommendations for coverage gaps.

#### `bug-fixer`
Investigates and fixes bugs with deep root cause analysis. Creates tests to reproduce issues, implements fixes, and verifies through a test-driven loop.

#### `prompt-reviewer`
Analyzes LLM prompts against the 10-Layer Architecture framework. Provides detailed assessment reports with strengths, problem areas, and prioritized recommendations. Review-only—does not modify files.

#### `slop-cleaner`
Finds and removes AI-generated code slop: useless comments, verbose patterns, unnecessary abstractions, and filler phrases. Conservative by default—only removes clearly unnecessary content.

### Commands

| Command | Description |
|---------|-------------|
| `/implement` | Launch code-implementor agent |
| `/review-maintainability` | Launch code-maintainability-reviewer agent (defaults to git diff scope) |
| `/audit-coverage` | Launch test-coverage-auditor agent (defaults to git diff scope) |
| `/bugfix` | Launch bug-fixer agent |
| `/clean-slop` | Remove AI-generated slop (useless comments, verbose patterns) |
| `/update-claude-md` | Create or update CLAUDE.md with best practices |

### Command: `/update-claude-md`

Create or update CLAUDE.md with best practices.

**Usage:**
```bash
# Create or update CLAUDE.md
/update-claude-md

# Focus on specific area
/update-claude-md add testing commands

# Address specific issue
/update-claude-md fix outdated build instructions
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
/plugin install vibe-workflow@claude-code-plugins-marketplace
```

## License

MIT
