---
description: Verify test coverage for code changes. Analyzes diff against main and reports coverage gaps.
allowed-tools: ["Task", "Read", "Glob", "Grep"]
argument-hint: [file paths, or empty for branch diff]
---

Use the code-coverage-reviewer agent to check test coverage for: $ARGUMENTS

If no arguments provided, analyze the git diff between the current branch and main/master branch.
