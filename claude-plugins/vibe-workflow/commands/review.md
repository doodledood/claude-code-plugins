---
description: Run all code review agents in parallel (bugs, coverage, maintainability, CLAUDE.md adherence, docs).
allowed-tools: ["Task", "Read", "Glob", "Grep"]
argument-hint: [file paths, or empty for branch diff]
---

Run a comprehensive code review by launching these 5 agents IN PARALLEL using the Task tool:

1. **code-bugs-reviewer** - Audit for logical bugs, race conditions, edge cases
2. **code-coverage-reviewer** - Verify test coverage for code changes
3. **code-maintainability-reviewer** - Check for DRY violations, dead code, complexity
4. **claude-md-adherence-reviewer** - Verify compliance with CLAUDE.md project standards
5. **docs-reviewer** - Audit documentation and code comments accuracy

Scope: $ARGUMENTS

If no arguments provided, all agents should analyze the git diff between the current branch and main/master branch.

IMPORTANT: Launch all 5 agents simultaneously in a single message with 5 Task tool calls. Do NOT run them sequentially.
