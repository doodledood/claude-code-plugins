# ADR: Agents and hooks were consolidated into skills

## Status
Accepted

## Area
Plugin structure

## Context

**Rationale not recovered.** This record was reconstructed from commit `24fa05a` ("Sync manifest-dev plugin: consolidate agents/hooks into skills (#111)") and the tree it produced. The change and its date are evidenced; the reasoning behind it, and the alternatives weighed at the time, were not found in the commit, the changelog, or the repository's documentation, and are not reconstructed here.

What is evidenced: components that had been distributed as agents and hooks were folded into skills, and the synced plugin payload afterwards carries skills where it previously carried all three component types.

## Decision

Synced manifest-dev components are distributed as skills. Agents and hooks are not used as separate component types for that payload.

## Alternatives Considered

_Not recovered._

## Consequences

### Positive
- One component type to install, document and version for the synced payload.

### Negative
- Behavior that genuinely wants a hook's lifecycle trigger has no home in this payload.

## Source
- Retroactive — reconstructed from commit 24fa05a / PR #111 during project setup; no originating discussion found
- Session: (no session — captured post-hoc)
