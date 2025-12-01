---
description: Create or update CLAUDE.md with best practices - brevity, universal applicability, progressive disclosure
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
argument-hint: [focus area or issue to address]
---

Create or update my CLAUDE.md file. $ARGUMENTS

Here's my current CLAUDE.md (if it exists):
@CLAUDE.md

And my project manifest:
@package.json
@pyproject.toml
@Cargo.toml

---

First, explore my codebase to understand the project structure, existing docs, CI config, and linter setup.

If I already have a CLAUDE.md, preserve what works and enhance it. Don't do a wholesale rewrite unless it's really broken.

Keep it **brief**. Claude can only follow ~150-200 instructions reliably, and the system prompt already uses ~50. Aim for:
- Simple projects: 30-60 lines
- Standard projects: 60-150 lines
- Complex/monorepos: 150-300 lines max

Focus on three things:
1. **WHAT** - Tech stack, project structure, key entry points
2. **WHY** - What the project does, why components exist
3. **HOW** - Build/test/run commands, verification steps

**Do**:
- Use imperative, concise language
- Verify commands actually work before including them
- Reference the README instead of duplicating it

**Don't**:
- Add style rules (that's what linters are for)
- Enumerate every file or function (describe patterns instead)
- Include task-specific instructions (keep it universal)
- Generate boilerplate

Here's what bad vs good looks like:

Bad (style-focused):
```
Always use camelCase. Document with JSDoc. Keep files under 200 lines.
```

Good (actionable):
```
## Commands
npm run dev    # Dev server
npm test       # Required before PR

## Architecture
React + TypeScript in src/. API via src/api/client.ts.
```

Structure the output like this:
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
[Only if genuinely helpful]
```

Before you finish, verify: under 300 lines, no style rules, all instructions are universal, commands are verified, no README duplication.
