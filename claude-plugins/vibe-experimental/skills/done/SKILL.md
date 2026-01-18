---
name: done
description: 'Completion marker. Outputs execution summary.'
user-invocable: false
---

# /done - Completion Marker

Output a summary of what was accomplished.

## Input

`$ARGUMENTS` = completion context (optional)

## Output Summary

```markdown
## Execution Complete

All acceptance criteria verified passing.

### What Was Executed
- [Brief description of changes made]
- [Key files modified]

### Verified Criteria
- AC-1: [description]
- AC-2: [description]
- ...

### Key Decisions Made
- [Decision 1]: [rationale]
- [Decision 2]: [rationale]

### Git Commits
- [commit hash]: [message]
- [commit hash]: [message]

---

Execution verified complete.
```

Read execution log (`/tmp/do-log-*.md`) to populate the summary.
