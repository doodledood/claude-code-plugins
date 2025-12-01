---
description: Create or update CLAUDE.md with best practices - brevity, universal applicability, progressive disclosure
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
argument-hint: [focus area or issue to address]
---

Update my CLAUDE.md based on: $ARGUMENTS

Current CLAUDE.md:
@CLAUDE.md

Project manifest:
@package.json
@pyproject.toml
@Cargo.toml

---

If CLAUDE.md exists, make targeted updates based on my request above. Only explore the codebase if essential information is missing.

If creating from scratch or missing critical sections, ensure it covers:
- **WHAT**: Tech stack, project structure, key entry points
- **WHY**: What the project does, domain context
- **HOW**: Build/test/run commands, verification steps

**Constraints** (Claude follows ~150 instructions max, system uses ~50):
- Simple projects: 30-60 lines
- Standard: 60-150 lines
- Complex/monorepo: 150-300 lines max

**Do**: Imperative language | Verify commands work | Reference README (don't duplicate)

**Don't**: Style rules (use linters) | File enumeration (describe patterns) | Task-specific instructions | Boilerplate

Bad: `Always use camelCase. Document with JSDoc.`
Good: `npm test  # Required before PR`

Template:
```
# CLAUDE.md
[1-2 sentence description]

## Tech Stack
## Project Structure
## Development Commands
## Architecture Notes (only if helpful)
```

Verify before finishing: <300 lines, no style rules, universal instructions, commands tested.
