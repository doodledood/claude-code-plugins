# Vibe Workflow Plugin

Autonomous feature development workflow for Claude Code.

## Overview

This plugin enables Claude to develop features as autonomously as possible - from planning through implementation to review.

## Components

### Agents

#### `code-maintainability-reviewer`
Performs comprehensive maintainability audits identifying DRY violations, dead code, YAGNI violations, unnecessary complexity, and consistency issues. Use after implementing features or before PRs.

#### `code-coverage-reviewer`
Analyzes diffs between your branch and main to ensure all new/modified logic has adequate test coverage. Provides specific test recommendations for coverage gaps.

#### `bug-fixer`
Investigates and fixes bugs with deep root cause analysis. Creates tests to reproduce issues, implements fixes, and verifies through a test-driven loop.

#### `prompt-reviewer`
Analyzes LLM prompts against the 10-Layer Architecture framework. Provides detailed assessment reports with strengths, problem areas, and prioritized recommendations. Review-only—does not modify files.

#### `slop-cleaner`
Finds and removes AI-generated code slop: useless comments, verbose patterns, unnecessary abstractions, and filler phrases. Conservative by default—only removes clearly unnecessary content.

#### `code-bugs-reviewer`
Audits code changes for logical bugs, race conditions, edge cases, and error handling issues. Performs deep analysis with prioritized bug detection (race conditions, data loss, edge cases, logic errors, etc.). Generates detailed bug reports with severity, impact, and fix recommendations.

#### `claude-md-adherence-reviewer`
Verifies that code changes comply with CLAUDE.md instructions and project standards. Audits pull requests and code for violations of project-specific rules. Issues are categorized by severity (CRITICAL, HIGH, MEDIUM, LOW) with exact CLAUDE.md rule citations.

#### `docs-reviewer`
Audits documentation and code comments accuracy against code changes. Identifies stale docs, missing documentation for new features, incorrect examples, version mismatches, outdated JSDoc/docstrings, and stale TODO/FIXME comments. Produces actionable reports with specific update recommendations. Read-only—does not modify files.

#### `type-safety-reviewer`
Audits TypeScript code to catch bugs through the type system—the cheapest, most consistent bug catcher. Identifies type holes that let bugs through, `any`/`unknown` abuse, opportunities to make invalid states unrepresentable, and ways to push runtime checks into compile-time guarantees. Every bug caught by the compiler never reaches production. Read-only—does not modify files.

### Commands

| Command | Description |
|---------|-------------|
| `/review` | Run all review agents in parallel (5 core + type-safety if typed language) |
| `/review-maintainability` | Launch code-maintainability-reviewer agent (defaults to git diff scope) |
| `/review-bugs` | Launch code-bugs-reviewer agent for logical bug detection (defaults to git diff scope) |
| `/review-coverage` | Launch code-coverage-reviewer agent (defaults to git diff scope) |
| `/review-claude-md-adherence` | Launch claude-md-adherence-reviewer agent for CLAUDE.md compliance (defaults to git diff scope) |
| `/review-docs` | Launch docs-reviewer agent for documentation accuracy (defaults to git diff scope) |
| `/review-type-safety` | Launch type-safety-reviewer agent for TypeScript type safety (defaults to git diff scope) |
| `/bugfix` | Launch bug-fixer agent |
| `/clean-slop` | Remove AI-generated slop (useless comments, verbose patterns) |
| `/update-claude-md` | Create or update CLAUDE.md with best practices |
| `/rebase-on-main` | Update main/master, rebase current branch, resolve conflicts, and push |

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

### Command: `/rebase-on-main`

Update main/master from origin, rebase current branch, resolve conflicts, and push.

**Usage:**
```bash
# Rebase current branch on latest main/master
/rebase-on-main
```

**What it does:**
- Detects whether `main` or `master` is the default branch
- Fetches and updates the main branch from origin
- Rebases current feature branch on top of it
- Resolves merge conflicts intelligently by analyzing code context
- Pushes with `--force-with-lease` for safety

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
