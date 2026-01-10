---
name: review-coverage
description: Verify test coverage for code changes. Analyzes diff against main and reports coverage gaps.
argument-hint: Optional - specific files to check coverage for. Leave empty to check all changes on current branch
---

Use the code-coverage-reviewer agent to check test coverage for: $ARGUMENTS

If no arguments provided, analyze the git diff between the current branch and main/master branch.
