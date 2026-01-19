---
name: done
description: 'Completion marker. Outputs hierarchical execution summary showing Global Invariants respected and all Deliverables completed.'
user-invocable: false
---

# /done - Completion Marker

Output a summary of what was accomplished, organized by the Manifest hierarchy.

## Input

`$ARGUMENTS` = completion context (optional)

## Output Summary

Read execution log (`/tmp/do-log-*.md`) and manifest to populate:

```markdown
## Execution Complete

All invariants respected. All acceptance criteria verified.

### Intent
**Goal:** [from manifest]

### Global Invariants (The Constitution)

All global rules were respected throughout execution:

| ID | Description | Status |
|----|-------------|--------|
| INV-G1 | Tests must pass | PASS |
| INV-G2 | No HIGH/CRITICAL bugs | PASS |
| INV-G3 | Linting passes | PASS |

### Deliverables

#### Deliverable 1: [Name]

**Local Invariants:**
| ID | Constraint | Status |
|----|------------|--------|
| INV-L1.1 | No plaintext passwords | Respected |

**Acceptance Criteria:**
| ID | Description | Status |
|----|-------------|--------|
| AC-1.1 | User can log in | PASS |
| AC-1.2 | Session persists | PASS |

**Key Changes:**
- [file:line] - [what changed]
- [file:line] - [what changed]

---

#### Deliverable 2: [Name]

**Local Invariants:**
| ID | Constraint | Status |
|----|------------|--------|
| INV-L2.1 | Reset tokens expire in 1 hour | Respected |

**Acceptance Criteria:**
| ID | Description | Status |
|----|-------------|--------|
| AC-2.1 | User receives reset email | PASS |
| AC-2.2 | Reset link works | PASS |

**Key Changes:**
- [file:line] - [what changed]

---

### Tradeoffs Applied

| Decision | Manifest Preference | Outcome |
|----------|---------------------|---------|
| [decision context] | [preference from manifest] | [what was chosen] |

### Key Decisions Made

- **[Decision 1]**: [rationale]
- **[Decision 2]**: [rationale]

### Git Commits

- `[hash]`: [message]
- `[hash]`: [message]

### Files Modified

| File | Changes |
|------|---------|
| src/auth.ts | Added login logic |
| src/session.ts | Added session persistence |

---

Manifest execution verified complete.
```

## Process

1. Read the execution log (`/tmp/do-log-*.md`)
2. Read the original manifest for structure
3. Extract:
   - Intent from manifest
   - Global Invariant statuses from verification
   - Per-deliverable results
   - Tradeoff resolutions from log
   - Key decisions from log
   - Git commits made during execution
   - Files modified

4. Output the structured summary

## Summary Levels

Adjust detail based on task complexity:

**Simple task (1 deliverable, few criteria):**
- Condensed single-section output
- Skip empty sections

**Complex task (multiple deliverables):**
- Full hierarchical output
- Include all sections

## Key Points

1. **Hierarchical structure** - Mirror the Manifest organization
2. **Status visibility** - Every criterion shows PASS/Respected
3. **Changes linked** - Show what changed for each deliverable
4. **Tradeoffs documented** - Show how preferences were applied
5. **Git integration** - Link to commits made
