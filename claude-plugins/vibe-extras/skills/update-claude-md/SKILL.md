---
name: update-claude-md
description: "Create or update CLAUDE.md project instructions with best practices for brevity, universal applicability, and progressive disclosure. Handles structure (tech stack, purpose, commands), length budgets (30-300 lines), and pointer-over-copy patterns. Use when the user asks to create, update, edit, or improve their CLAUDE.md, project instructions, or Claude Code configuration file."
---

Update my CLAUDE.md based on: $ARGUMENTS

Current CLAUDE.md:
@CLAUDE.md

---

Make targeted updates based on the request. Only explore the codebase if essential info is missing.

If the request conflicts with best practices below, still apply the update but note the tradeoff.

## Best Practices

CLAUDE.md is the highest-leverage config point for Claude Code.

### Structure — cover these if creating or missing critical sections

- **WHAT**: Tech stack, project structure, key entry points (critical for monorepos)
- **WHY**: Project purpose, component relationships, domain terminology
- **HOW**: Build/test/run commands, verification steps

### Length budget

LLMs follow ~150 instructions reliably; system uses ~50.

| Complexity | Lines |
|------------|-------|
| Simple | 30–60 |
| Standard | 60–150 |
| Complex | 150–300 max |

### Progressive disclosure

For complex projects, create separate docs and reference them:
```
docs/testing.md, docs/architecture.md, docs/conventions.md
```
Then in CLAUDE.md: `See docs/testing.md for test patterns`

### Prefer pointers over copies

Use `file:line` references instead of pasting code snippets (avoids staleness).

### Do

- Universal instructions (apply to every task)
- Imperative language
- Verified, runnable commands
- Reference (don't copy) README

### Don't

- Style rules → use linters, formatters, or Claude Code hooks instead
- Task-specific instructions → ignored when irrelevant to current task
- File/function enumeration → describe patterns instead
- Auto-generated boilerplate

### Examples

Bad: `Always use camelCase. Document with JSDoc.`
Good: `npm test  # Required before PR`

## Verification checklist

- [ ] Under 300 lines
- [ ] No style rules (use linters instead)
- [ ] All instructions are universal
- [ ] Commands tested and runnable
