---
name: auto-optimize-prompt
description: 'Iteratively auto-optimize a prompt until no issues remain. Uses prompt-reviewer in a loop, asks user for ambiguities, applies fixes via prompt-engineering skill. Runs until converged.'
---

# Auto-Optimize Prompt

**User request**: $ARGUMENTS

Iteratively optimize a prompt until no issues remain.

## Goal

Loop: **review → clarify ambiguities with user → fix → repeat** until prompt-reviewer finds no issues.

- **No path provided**: Ask which file to optimize
- **Working copy**: Use `/tmp/auto-optimize-*.md` during iterations; apply to original only when converged

## Loop

1. **Review**: Use prompt-reviewer agent on working copy
2. **If no issues**: Done → apply working copy to original, report summary
3. **If NEEDS_USER_INPUT issues**: Ask user to resolve ambiguities before fixing
4. **Fix**: Invoke `prompt-engineering:prompt-engineering` to fix each issue
5. **Repeat** from step 1

## User Clarification

For NEEDS_USER_INPUT issues, ask with context: what the issue is, current text, specific question with concrete options. If user declines, skip that issue.

## Constraints

| Constraint | Why |
|------------|-----|
| **Converge, don't cap** | No iteration limits—run until no issues |
| **Atomic output** | Original unchanged until fully converged |
| **DRY** | Delegate review to prompt-reviewer, fixes to prompt-engineering |
| **User-in-the-loop** | Only user can resolve true ambiguities |

## Output

Report: file path, iterations, issues fixed (auto vs user-resolved), issues skipped, summary of changes.
