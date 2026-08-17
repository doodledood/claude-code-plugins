# ADR: review-prompt is deferred to manifest-dev, like the prompt-engineering skill before it

## Status
Accepted — superseded by 20260817-prompt-engineering-plugin-retired, which retired the plugin this record declined to retire

## Area
Plugin boundaries

## Context

[20260802](20260802-defer-prompt-engineering-to-manifest-dev.md) removed the `prompt-engineering` skill from this repository's plugin and took manifest-dev's instead, on the rule that where a capability exists upstream in a better-maintained form, this repository consumes it. That record listed `review-prompt` among the skills the plugin keeps, because at the time it had no upstream equivalent.

It has one now. manifest-dev ships a `review-prompt` skill, and it moved again when that repository rewrote `prompt-engineering` around provenance — the reviewer leads with that question and no longer treats a missing section as a finding.

The duplication was not merely redundant, it was silently unfixable. This repository's `.claude/skills/review-prompt` was a symlink into `claude-plugins/prompt-engineering/skills/review-prompt`, which the manifest-dev sync classifies as **foreign** and correctly refuses to write, delete, or track. Every sync therefore reported `review-prompt` skipped and left the local copy behind, so the local reviewer drifted from the skill it reviews against with nothing failing to signal it.

## Decision

Remove `review-prompt` from this repository's plugin and take manifest-dev's. With the foreign symlink gone, the sync writes it as ordinary tracked content and it stays current on its own.

The plugin keeps what still has no upstream twin: `auto-optimize-prompt`, `compress-prompt`, `optimize-prompt-token-efficiency`, and all three agents — manifest-dev ships no agents at all. The plugin is not retired.

This is 20260802's rule applied a second time rather than a new one. The rule is now understood to run continuously: a skill kept locally because it had no upstream equivalent is reviewed again when upstream grows one.

## Alternatives Considered

- **Keep the local copy and update it by hand to match upstream.** Rejected: it re-creates the divergence 20260802 removed, and the foreign-symlink skip means nothing would ever report the drift.
- **Retire the whole plugin.** Rejected: three skills and three agents here have no upstream equivalent, and manifest-dev ships no agents, so retiring the plugin would delete working capability to solve a one-skill overlap.
- **Keep the local copy and stop syncing manifest-dev's review-prompt.** Rejected for the same reason 20260802 rejected it: re-implementing upstream improvements by hand is the cost the sync tooling exists to avoid.

## Consequences

### Positive
- One reviewer, and it is the maintained one — kept current by the sync rather than by hand.
- The sync's skipped-item list for this repository is now empty, so a future skip is a real signal rather than a standing exception.

### Negative
- A breaking change for anyone who installed `review-prompt` from this plugin by name.
- One more capability now depends on upstream timing.

## Source
- Session: applied while syncing manifest-dev@6ae6dce across the fleet, when the standing `review-prompt` skip was traced to the foreign symlink
- Related: narrows [20260802-defer-prompt-engineering-to-manifest-dev](20260802-defer-prompt-engineering-to-manifest-dev.md), whose "the plugin keeps `review-prompt`" no longer holds
- Related: [20260807-layout-verdict-is-per-repo-not-per-skill](20260807-layout-verdict-is-per-repo-not-per-skill.md) cites this repository's `review-prompt` foreign symlink as the corruption mode its probe must not fall into. That example no longer exists here; the reasoning and the decision stand.
