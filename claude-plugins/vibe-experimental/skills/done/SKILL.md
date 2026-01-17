---
name: done
description: 'Internal completion marker. Called by /verify when all criteria pass. Outputs summary and allows stop.'
user-invocable: false
---

# /done - Completion Marker

You mark successful completion of a /do workflow. You are called by /verify when all automated criteria pass, not directly by users or /do.

## Input

`$ARGUMENTS` = completion context (optional, passed by /verify)

## Purpose

1. **Marker in transcript** - stop hook looks for /done after /do
2. **Completion summary** - tell user what was accomplished
3. **Enable stop** - without /done, stop is blocked

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
2. **Signals completion** - stop hook allows stop when /done exists
3. **Summary required** - don't just exist, provide useful summary
4. **After verification** - only reached when all automated criteria pass

## Stop Hook Behavior

The stop hook checks:
```
if /do exists in transcript:
    if /done exists after /do:
        ALLOW stop
    elif /escalate exists after /do:
        ALLOW stop
    else:
        BLOCK stop
```

By existing in the transcript after /do, /done enables stopping.
