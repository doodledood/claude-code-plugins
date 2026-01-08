---
description: 'Single-agent implementation: executes plans in-place without subagents. Use /implement (default) for complex features; use this for simpler tasks or when subagent overhead is unwanted.'
argument-hint: plan path | inline task | (empty for recent plan or interactive)
---

**User request**: $ARGUMENTS

Autonomously execute implementation in-place. Supports plan files, inline tasks, or interactive mode.

**Fully autonomous**: No pauses except truly blocking issues.

## Workflow

### Phase 1: Resolve Input & Setup

**Priority order:**
1. **File path** (ends in `.md` or starts with `/`) → use plan file, optionally with `--spec <path>`
2. **Inline task** (any other text) → create ad-hoc single chunk:
   ```
   ## 1. [Task summary - first 50 chars or natural break]
   - Depends on: -
   - Tasks: [user's description]
   - Files: (discover during implementation)
   - Acceptance criteria: gates pass
   ```
3. **Empty** → search `/tmp/plan-*.md` (most recent); if none found, **ask user** what they want to implement

**For plan files**, parse each chunk (`## N. [Name]` headers):
- Dependencies (`Depends on:` field, `-` = none)
- Files to modify/create with descriptions
- Context files (paths, optional line ranges)
- Implementation tasks (bullet list)
- Key functions/types

**Build dependency graph**: No-dependency chunks first, then topological order.

**Create flat todo list** (Memento pattern—granular progress, resumable):
```
[ ] Read context for [Chunk]
[ ] [Task 1]...[ ] [Task N]
[ ] Run gates for [Chunk]
```
All todos created at once via TodoWrite, status `pending`.

### Phase 2: Execute Chunks

**CRITICAL**: Execute continuously without pauses.

Per chunk:
1. Read context files (related + files-to-modify), respect line ranges
2. Implement each task, marking `in_progress`→`completed` immediately
3. Run quality gates (Phase 3)
4. Track created/modified files for summary

**Spec file** (`--spec`): Read before implementation for requirements/acceptance criteria.

### Phase 3: Auto-Fix Gates

**Run gates** (typecheck→tests→lint). Detect commands from CLAUDE.md first, then package.json/pyproject.toml.

**On failure—iterate**:
1. Analyze: parse errors, identify files/lines, understand root cause
2. Fix cleanly (no workarounds)
3. Re-run gates
4. Repeat until pass, track attempts to avoid loops

**Pause ONLY when**: 3+ failed iterations, need external info, requires out-of-scope breaking changes, fundamental conflict.

Report: what tried, why failed, what's needed.

### Phase 4: Completion

```
## Implementation Complete
Chunks: N | Todos: M | Created: [list] | Modified: [list]
### Notes: [warnings/assumptions/follow-ups]
Run `/review` for quality verification.
```

## Edge Cases

| Case | Action |
|------|--------|
| Invalid plan | Error with path + expected structure |
| Missing context file | Warn, continue (non-blocking) |
| Chunk fails completely | Leave todos pending, skip dependents, continue independents, report in summary |
| Inline task provided | Create ad-hoc single chunk, proceed normally |
| No input + no recent plan | Ask user what they want to implement |
| Interrupted | Todos reflect exact progress (Memento), manual cleanup needed for re-run |

## Principles

- **Autonomous**: No prompts/pauses/approval needed except blocking issues
- **Memento todos**: One todo per action, granular visibility, resumable
- **Persistent auto-fix**: Iterate until gates pass, escalate only when stuck
- **Dependency order**: Execute in order, skip failed chunk's dependents
- **Gates non-negotiable**: Fix now, not later

## Gate Detection

**Priority**: CLAUDE.md → package.json scripts → Makefile → config detection

**Fallback** (if CLAUDE.md doesn't specify):
- TS/JS: `tsconfig.json`→`tsc --noEmit`, `eslint.config.*`→`eslint .`, `jest/vitest.config.*`→`npm test`
- Python: `pyproject.toml`→`mypy`/`ruff check`, pytest config→`pytest`
