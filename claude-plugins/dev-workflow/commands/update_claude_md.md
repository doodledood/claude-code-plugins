---
description: Create or update CLAUDE.md with best practices - brevity, universal applicability, progressive disclosure
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
argument-hint: [focus area or issue to address]
---

# Update CLAUDE.md

**Context**: $ARGUMENTS

## Current Project State

Existing CLAUDE.md (if any):
@CLAUDE.md

Project manifest (if any):
@package.json
@pyproject.toml
@Cargo.toml

---

**Role**: CLAUDE.md specialist. Create concise, high-leverage documentation for Claude Code.

**Critical**: Preserve what works. Brevity > comprehensiveness.

## Core Principles

| Principle | Rationale |
|-----------|-----------|
| **Brevity** | Claude follows ~150-200 instructions reliably. System prompt uses ~50. Less is more. |
| **Universal** | Task-specific content gets ignored. Keep instructions broadly relevant. |
| **Progressive disclosure** | Reference separate files for details. Don't embed everything. |
| **No style rules** | Never send an LLM to do a linter's job. Point to configs instead. |

## Target Length

| Project Type | Lines | Focus |
|--------------|-------|-------|
| Simple | 30-60 | Commands + brief structure |
| Standard | 60-150 | Full WHAT/WHY/HOW |
| Complex/monorepo | 150-300 | Progressive disclosure + file refs |

## Three Essential Sections

**WHAT** - Tech stack, project structure, entry points, architecture patterns
**WHY** - Purpose, why components exist, domain terminology
**HOW** - Build/test/run commands, verification methods, workflow

## Process

1. **Analyze** project structure, manifest, existing docs, CI config, linter setup
2. **Check** existing CLAUDE.md - enhance if present, create if not
3. **Draft** with constraints below
4. **Verify** commands work before including

## Constraints

**MUST**: Under 300 lines | Imperative language | Verified commands | Reference (don't duplicate) README

**NEVER**: Style rules | File/function enumeration | Task-specific instructions | Boilerplate

## Example

**Bad** (style-focused):
```
Always use camelCase. Document with JSDoc. Keep files under 200 lines.
```

**Good** (actionable):
```
## Commands
npm run dev    # Dev server
npm test       # Required before PR
npm run lint   # Pre-commit hook runs this

## Architecture
React + TypeScript in src/. API via src/api/client.ts. State in src/stores/.
```

## Output Structure

```
# CLAUDE.md

[1-2 sentence description]

## Tech Stack
- [Key technologies]

## Project Structure
dir/    # Purpose

## Development Commands
[Build, test, lint commands]

## Architecture Notes
[Only if helpful - omit if not needed]
```

## Quality Gate

Before finalizing: Under 300 lines | No style rules | Universal instructions | Commands verified | No README duplication
