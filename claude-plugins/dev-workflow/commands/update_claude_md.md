---
description: Create or update a CLAUDE.md file with best practices for effective AI collaboration - focuses on brevity, universal applicability, and progressive disclosure
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
arguments:
  - name: context
    description: Focus areas, existing issues, or specific context (e.g., "add testing commands", "focus on monorepo structure")
    required: false
---

# Update CLAUDE.md

**User Context**: $ARGUMENTS

---

**Role**: CLAUDE.md specialist creating concise, high-leverage project documentation for Claude Code.

**Critical**: Read existing CLAUDE.md first. Preserve what works. Brevity > comprehensiveness.

## Core Principles

| Principle | Rationale |
|-----------|-----------|
| **Brevity over completeness** | Claude follows ~150-200 instructions reliably; system prompt uses ~50. Less is more. |
| **Universal applicability** | Task-specific content gets ignored. Keep instructions broadly relevant. |
| **Progressive disclosure** | Reference separate files for details. Don't embed everything. |
| **No style guidelines** | Never send an LLM to do a linter's job. Point to configs instead. |

## Complexity Scaling

| Project Type | Target Lines | Focus |
|--------------|--------------|-------|
| Simple (single-purpose) | 30-60 | Commands + brief structure |
| Standard | 60-150 | Full WHAT/WHY/HOW |
| Complex (monorepo/large) | 150-300 | Progressive disclosure + file references |

## The Three Essential Sections

### WHAT - Codebase Map
Tech stack, project structure, main entry points, architecture patterns.

### WHY - Purpose & Context
What the project does, why components exist, domain terminology.

### HOW - Working with the Project
Build/test/run commands, verification methods, development workflow.

## Process

### 1. Explore the Codebase
Identify: manifest files, directory structure, existing docs, CI/CD config, linter setup, test commands.

### 2. Handle Existing CLAUDE.md

```
IF CLAUDE.md exists
  THEN read it, identify gaps, enhance while preserving working content
ELSE
  THEN create from scratch
```

### 3. Handle User Context

```
IF $ARGUMENTS specifies focus areas
  THEN prioritize those sections
ELSE IF $ARGUMENTS mentions issues to fix
  THEN address those specific problems
ELSE
  THEN do comprehensive analysis
```

### 4. Draft with Constraints

**MUST**:
- Keep under 300 lines
- Use imperative, concise language
- Verify commands actually work
- Reference (not duplicate) README content

**NEVER**:
- Add style rules (point to linter config)
- Enumerate every file/function (describe patterns)
- Include task-specific instructions
- Auto-generate boilerplate

## Example: Good vs Bad

**Bad** (over-specified, style-focused):
```
Always use camelCase for variables. Functions should be
documented with JSDoc. Keep files under 200 lines. Use
4 spaces for indentation. Every component must have...
```

**Good** (actionable, universal):
```
## Development Commands

npm run dev      # Start dev server
npm test         # Run tests (required before PR)
npm run lint     # Fix lint issues (pre-commit hook runs this)

## Architecture

React + TypeScript frontend in src/. API calls go through
src/api/client.ts. State management via Zustand in src/stores/.
```

## Output Template

Structure the CLAUDE.md like this:

```
# CLAUDE.md

Brief project description (1-2 sentences).

## Tech Stack
- [Key technologies only]

## Project Structure
key-dir/     # Purpose
other-dir/   # Purpose

## Development Commands

Build & Run:
[essential commands]

Testing:
[test commands]

Linting:
[lint/format commands]

## Architecture Notes
[Only if genuinely helpful - omit if not needed]

## Additional Resources
- [Reference to other docs if relevant]
```

## Quality Gate

Before finalizing, verify ALL:
- [ ] Under 300 lines
- [ ] No style guidelines embedded
- [ ] All instructions universally applicable
- [ ] Commands verified to work
- [ ] No README duplication
- [ ] Imperative language throughout

---

**Critical**: Read existing CLAUDE.md first. Preserve what works. Make targeted improvements, not wholesale rewrites.
