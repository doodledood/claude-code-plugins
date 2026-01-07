# Vibe Workflow Plugin

Autonomous development workflow with code review agents and quality gates.

## What It Does

**Skills** (auto-invoked by Claude when relevant):
- **spec** - Build requirements through interactive interview (EARS syntax)
- **plan** - Create mini-PR implementation plans with iterative codebase research
- **implement** - Execute plans autonomously chunk by chunk with auto-fix quality gates
- **bugfix** - Systematic investigation with root cause analysis and test-driven verification
- **fix-review-issues** - Address issues found by /review with prioritized execution
- **explore-codebase** - Returns structural overview + prioritized file list with line ranges

**Commands** (invoke explicitly):
- `/review` - Audit changes for bugs, maintainability, type safety, docs, and coverage
- `/implement-v2` - Execute plans via subagents with automated verification and fix loops (5 attempts per chunk)
- `/web-research` - Research external topics with structured hypothesis tracking

**Agents**:
- **codebase-explorer** - Context-gathering agent, prefer over built-in Explore
- **chunk-implementor** - Implements a single plan chunk, logs progress (used by /implement-v2)
- **chunk-verifier** - Runs gates and checks acceptance criteria (used by /implement-v2)

Use `/help` after installation to see all available commands.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-workflow@claude-code-plugins-marketplace
```

## License

MIT
