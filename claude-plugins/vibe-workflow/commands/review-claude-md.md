---
description: Verify code changes comply with CLAUDE.md instructions and project standards.
allowed-tools: ["Task", "Read", "Glob", "Grep"]
argument-hint: [file paths, or empty for branch diff]
---

Use the claude-md-adherence agent to audit code for CLAUDE.md compliance: $ARGUMENTS

If no arguments provided, analyze the git diff between the current branch and main/master branch.
