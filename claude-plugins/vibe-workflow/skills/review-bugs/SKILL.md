---
name: review-bugs
description: Audit code for logical bugs, race conditions, edge cases, and error handling issues.
argument-hint: Optional - specific files to audit. Leave empty to audit all changes on current branch
---

Use the code-bugs-reviewer agent to perform a bug audit on: $ARGUMENTS

If no arguments provided, analyze the git diff between the current branch and main/master branch.
