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

**Skills** (auto-invoked when relevant):
- `spec` - Interactive requirements builder
- `plan` - Create implementation plans with codebase research
- `implement` - Execute plans via subagents with verification loops
- `bugfix` - Root cause analysis with test-driven verification
- `explore-codebase` - Structural overview with prioritized file list

**Commands** (explicit invocation):
- `/review` - Parallel code review agents
- `/implement-inplace` - Single-agent implementation, no subagent overhead
- `/web-research` - External research with hypothesis tracking

**Agents**:
- `codebase-explorer` - Context gathering, prefer over built-in Explore
- `chunk-implementor` - Implements single plan chunks
- `chunk-verifier` - Runs verification gates

**Hooks**:
- `SessionStart` - Reminds Claude to prefer codebase-explorer and web-researcher agents
- `SessionStart (compact)` - Re-anchors session after compaction; adds implement workflow recovery if mid-implementation
- `Stop` - Prevents premature stops during `/implement` workflows when todos are incomplete

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install vibe-workflow@claude-code-plugins-marketplace
```

## License

MIT
