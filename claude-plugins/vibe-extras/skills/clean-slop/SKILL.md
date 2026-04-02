---
name: clean-slop
description: "Find and remove AI-generated code slop — useless comments, verbose patterns, unnecessary abstractions, filler phrases, and redundant documentation. Analyzes target files or git diff, applies conservative surgical edits, and reports a summary of changes. Use when the user asks to clean up code, remove AI artifacts, simplify verbose output, strip obvious comments, or refactor slop from AI-assisted coding sessions."
---

Use the slop-cleaner agent to clean up AI slop in: $ARGUMENTS

---

The slop-cleaner agent identifies and removes four categories of AI-generated noise:

1. **Useless comments** — restating what code does, repeating function names, commented-out code
2. **Verbose documentation** — trivial JSDoc/docstrings on simple getters, redundant type documentation
3. **Filler phrases** — "It is important to note that...", "Successfully completed", overly apologetic error messages
4. **Unnecessary patterns** — empty catch blocks, redundant else-after-return, single-use wrapper abstractions

## Scope

- If file paths are provided as arguments, those files are analyzed
- If no arguments, the agent diffs the current branch against main/master and analyzes changed files

## Decision rule

**Remove** when the comment/pattern restates *what* the code does or adds zero information beyond what code and types already provide. **Keep** when it explains *why*, documents edge cases, or you're uncertain about its value.

## Output

A per-file cleaning report showing removals made, patterns preserved with rationale, and total change counts.
