# Vibe Workflow

Structured development workflow that front-loads requirements gathering to reduce iteration cycles.

## The Problem

LLMs produce better output when they have clear, complete context upfront. But most developers jump straight into "build this feature" and end up iterating through multiple rounds of corrections. This wastes tokens and time.

## The Approach

Break development into phases that match how LLMs work best:

1. **Spec** - Gather requirements through structured interview before any code
2. **Plan** - Research codebase, create mini-PR implementation chunks
3. **Implement** - Execute chunks with verification at each step

Each phase produces artifacts that inform the next. More upfront investment, better first-pass output.

## When to Use What

| Situation | Entry Point |
|-----------|-------------|
| Single function, clear scope | Ask Claude directly |
| 1-2 files, requirements clear | `/implement-inplace` |
| Multi-file, approach unclear | `/plan` → `/implement` |
| Scope ambiguous, needs discovery | `/spec` → `/plan` → `/implement` |

Start simple. Escalate if you hit ambiguity.

## Components

### Core Workflow Skills
- `spec` - Interactive requirements builder with structured interview
- `plan` - Create implementation plans with codebase research
- `implement` - Execute plans via subagents with verification loops
- `implement-inplace` - Single-agent implementation for simpler tasks

### Code Review Skills
- `review` - Parallel code review (runs all review types)
- `review-bugs` - Focused bug detection
- `review-type-safety` - Type safety analysis
- `review-maintainability` - Code quality and maintainability
- `review-coverage` - Test coverage gaps
- `review-docs` - Documentation completeness
- `review-claude-md-adherence` - Check adherence to project instructions
- `fix-review-issues` - Address findings from review

### Research & Debugging Skills
- `bugfix` - Root cause analysis with test-driven verification
- `research-web` - Deep web research with parallel investigators (quick/medium/thorough/very-thorough)
- `web-research` - External research with hypothesis tracking
- `explore-codebase` - Structural overview with prioritized file list

### Agents
- `codebase-explorer` - Context gathering, prefer over built-in Explore
- `chunk-implementor` - Implements single plan chunks
- `chunk-verifier` - Runs verification gates
- `bug-fixer` - Root cause analysis agent
- `web-researcher` - Web research with source tracking
- `code-bugs-reviewer` - Bug detection agent
- `code-maintainability-reviewer` - Maintainability analysis
- `code-coverage-reviewer` - Coverage gap analysis
- `type-safety-reviewer` - Type safety analysis
- `docs-reviewer` - Documentation review
- `claude-md-adherence-reviewer` - Project instruction adherence

### Hooks
- `SessionStart` - Reminds Claude to prefer codebase-explorer and web-researcher agents
- `PostCompact` - Re-anchors session after compaction; adds implement workflow recovery
- `PostToolUse (TodoWrite)` - Reminds to update progress/log files during implement workflows
- `Stop` - Prevents premature stops during `/implement` when todos are incomplete

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-workflow@claude-code-plugins-marketplace
```

## License

MIT
