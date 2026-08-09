# ADR: The sync tool deletes only what it previously wrote

## Status
Accepted

## Area
Plugin sync

## Context

Reconstructed from commit `7143d03` and its message.

`sync-manifest-dev` originally treated the upstream manifest-dev repository as the source of truth for the directories it managed. Under that model anything present in `agents/`, `hooks/` or `skills/` that upstream did not have was, by definition, stale — and a sync would remove it. That is safe only if those directories hold nothing but synced content, which is not true here: this repository's own `prompt-engineering` plugin, its knowledge-base skills, and other project-local material live in the same tree.

## Decision

Sync records what it wrote in a tracking file, `.claude/.manifest-dev-sync.json`, and only entries in that tracked set are eligible for deletion. Content the tool never wrote is invisible to it and survives a sync untouched, even when it shares a directory with synced items.

## Alternatives Considered

- **Keep the source-of-truth model and reserve directories for synced content**: Simplest rule to state, and deletion needs no bookkeeping — Rejected: it requires project-local content to live somewhere else, which it does not, and getting that wrong destroys work that has no upstream copy to restore from.

## Consequences

### Positive
- Project-local plugins and skills coexist with synced ones in the same directories without risk.
- A dropped upstream item is still removed, so the tree does not accumulate stale content.

### Negative
- Correct deletion now depends on a tracking file staying accurate; if it is lost or hand-edited, previously synced items become undeletable by the tool.

## Source
- Retroactive — reconstructed from commit 7143d03 during project setup
- Session: (no session — captured post-hoc)
