---
description: Address issues found by /review. Fixes all issues by default, or filter by severity/category/file.
argument-hint: Optional filters - severity level (critical, high, medium, low), category (bugs, maintainability, types, docs, coverage, claude-md), or specific file paths
---

Use the Skill tool to fix issues from a recent /review run: Skill("vibe-workflow:fix-review-issues", "$ARGUMENTS")

Examples:
`/fix-review-issues` - Fix all issues
`/fix-review-issues only critical and high severity` - Filter by severity
`/fix-review-issues just the bugs` - Filter by category
`/fix-review-issues in src/auth/` - Filter by file path
