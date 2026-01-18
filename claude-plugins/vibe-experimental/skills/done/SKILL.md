---
name: done
description: 'Internal completion marker. Called by /verify when all criteria pass. Outputs summary and allows stop.'
user-invocable: false
---

# /done - Completion Marker

You mark successful completion of a /do workflow. Called by /verify when all automated criteria pass.

## Input

`$ARGUMENTS` = completion context (optional, passed by /verify)

## Process

### 1. Acknowledge Completion

This skill's existence in the transcript signals completion.

### 2. Output Summary

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

Execution verified complete. You may now stop or continue with other work.
```

### 3. Read Execution Log

If execution log path available, read it to populate:
- What was attempted
- Key decisions
- Files modified

## Critical Rules

1. **Not user-invocable** - only called by /verify
2. **Summary required** - provide useful summary of what was accomplished
3. **After verification** - only reached when all automated criteria pass
