# ADR: The prompt-engineering plugin is retired from this marketplace

## Status
Accepted

## Area
Plugin boundaries

## Context

The plugin was emptied out over three steps rather than one. [20260802](20260802-defer-prompt-engineering-to-manifest-dev.md) moved the `prompt-engineering` skill to manifest-dev and kept the rest, on the rule that where a capability exists upstream in a better-maintained form this repository consumes it. [20260817-review-prompt-deferred-to-manifest-dev](20260817-review-prompt-deferred-to-manifest-dev.md) applied the same rule to `review-prompt` once upstream grew one, and explicitly declined to retire the plugin, because `auto-optimize-prompt`, `compress-prompt`, `optimize-prompt-token-efficiency` and three agents had no upstream equivalent.

That reasoning weighed one thing — whether a replacement existed — and not whether the remainder was worth carrying. What was left is a plugin whose name describes a capability it no longer provides: prompt authoring and review both come from elsewhere, and the three surviving skills are narrow optimization passes over a prompt someone already has. Their agents exist only to serve them.

## Decision

Retire the plugin. `claude-plugins/prompt-engineering/` is deleted, its marketplace entry removed, and the `.claude/` and `.agents/` symlinks that pointed into it are dropped along with it — three skills (`auto-optimize-prompt`, `compress-prompt`, `optimize-prompt-token-efficiency`) and three agents (`prompt-reviewer`, `prompt-compression-verifier`, `prompt-token-efficiency-verifier`).

This is Aviram's ruling, made after the alternative below was put to him.

Prompt work in this repository is now served entirely by manifest-dev's `prompt-engineering` and `review-prompt`, which arrive through the sync. `CLAUDE.md`'s instruction to run the `prompt-engineering` skill for all prompt work is unaffected — it was already written unscoped, naming no plugin, precisely so it would survive a move like this one.

## Alternatives Considered

- **Keep the plugin for its three unique skills and three agents.** This was the position of 20260817, and it was put to Aviram directly when the removal was proposed — retiring the plugin deletes working capability that has no upstream replacement, since manifest-dev ships no agents at all. Rejected by his ruling: the remainder is not worth carrying.
- **Move the three surviving skills into another plugin here.** Rejected: it preserves the maintenance cost this decision is removing, and no existing plugin is a natural home for them.

## Consequences

### Positive
- One less plugin to maintain, and no plugin named for a capability it does not provide.
- Every prompt-related skill in this repository now comes from one maintained upstream source.

### Negative
- The three optimization skills and three agents are gone with no replacement — this is capability lost, not capability moved. Anyone who installed them by name is broken.
- They exist only in git history from here. Recovering one means reading it out of a past commit rather than reinstalling it.

## Source
- Session: retired at Aviram's explicit instruction, after the keep-the-plugin alternative was raised and declined
- Related: completes what [20260802-defer-prompt-engineering-to-manifest-dev](20260802-defer-prompt-engineering-to-manifest-dev.md) began and [20260817-review-prompt-deferred-to-manifest-dev](20260817-review-prompt-deferred-to-manifest-dev.md) continued; both described a plugin that no longer exists
