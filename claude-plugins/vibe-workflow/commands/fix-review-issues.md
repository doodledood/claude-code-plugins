---
description: Address issues found by /review. Fixes all issues by default, or filter by severity/category/file.
argument-hint: [--severity critical|high, --category bugs|maintainability|types|docs|coverage|claude-md, file paths]
---

Address issues found from a recent `/review` run. This command systematically fixes identified problems.

**Invoke the `fix-review-issues` skill** with the provided arguments to orchestrate the fix workflow.

## Arguments

Pass these to the skill:
- `$ARGUMENTS` - User-provided filters (severity, category, file paths)

## Example Usage

```
/fix-review-issues                           # Fix everything
/fix-review-issues --severity critical,high  # Only critical and high severity
/fix-review-issues --category bugs           # Only bug fixes
/fix-review-issues --category types,docs     # Types and docs only
/fix-review-issues src/auth/                 # Only files in src/auth/
/fix-review-issues --severity high --category maintainability src/utils.ts
```
