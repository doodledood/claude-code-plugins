# ADR: The sync tool decides skill layout once per repository, not per skill

## Status
Accepted

## Area
Plugin sync

## Context

Reconstructed from PR #118, which carries the reasoning in full.

Repositories in this fleet store skills one of two ways: *plain*, where `.claude/skills/` holds the real directories and `.agents/skills/` mirrors them, or *inverted*, where `.agents/skills/` holds the real content. `sync-manifest-dev` decided which layout applied per skill, by looking at what `.claude/skills/` contained for that skill. A skill absent from both sides read as an ordinary plain write.

That produced a silent split in `pi-plugins`: `ticket-up` and `next-ticket` landed as real `.claude/` directories in a repository whose other 17 skills keep their real content in `.agents/skills/`. Both arrangements resolve, so nothing failed and the inconsistency was invisible until someone read the tree.

The probe also has a corruption mode worth recording. This repository has an ordinary `.agents/` mirror whose entries are symlinks back into `.claude/`, one of which — `review-prompt` — is a foreign symlink into `claude-plugins/prompt-engineering/`. A layout probe that accepted resolved-equality would read this repository as inverted and begin writing through that foreign symlink into another plugin's source.

## Decision

The layout verdict is taken once per repository: one skill already stored `.agents`-real settles it for the whole repository. The probe requires the `.agents/skills/` entry to be a real directory, not merely to resolve — the same test the existing `mirror` classification uses — which is what keeps this repository correctly read as plain.

Three behaviors follow: new skills land on the repository's own side; wrong-side skills are flipped back; and removal clears both sides, so deleting a dropped skill on an inverted repository no longer leaves a dangling `.claude/` symlink. The run's summary header prints the verdict, so a repository silently changing sides is visible rather than discovered later.

## Alternatives Considered

- **Keep the per-skill decision and special-case absent skills**: Smaller change — Rejected: the absent-from-both case is exactly where the defect lives, and a per-skill rule cannot express "this repository stores skills the other way".
- **Probe by resolved equality rather than requiring a real directory**: Simpler test, tolerant of more arrangements — Rejected: it reads this repository as inverted and writes through a foreign symlink into another plugin's source, which is the corruption the classification rules were written after.

## Consequences

### Positive
- A repository's skills all sit on the same side, and drift back is repaired rather than accumulated.
- Removal no longer leaves dangling symlinks on inverted repositories.
- The verdict is printed, so a change of sides is visible in the run output.

### Negative
- A repository genuinely wanting mixed storage cannot express it.
- One skill's storage now determines every skill's, so a single mis-stored skill can flip the verdict for the whole repository.

## Source
- Retroactive — reconstructed from PR #118 during project setup
- Session: (no session — captured post-hoc)
