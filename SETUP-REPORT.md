# Project setup report

Wiring installed: `docs/adr/CONVENTIONS.md`, `docs/adr/README.md`, `CONTEXT.md`, and a
Project Language and Decision Records section in `CLAUDE.md` (`AGENTS.md` is a symlink to it,
so both harnesses read the same file).

## Seeded from history

Sources read: `CLAUDE.md`, `CHANGELOG.md`, `README.md`, `CONTRIBUTING.md`, `docs/`, the plugin
tree, 426 commits, and the pull requests behind the structural ones. The clone was shallow and was
unshallowed first — a seed built on one commit would have found nothing.

Four records written, and they differ in provenance on purpose:

| Record | Rationale |
|---|---|
| `20260807-layout-verdict-is-per-repo-not-per-skill` | **Recovered in full** from PR #118 — the defect, the fix, the rejected probe design, and the corruption mode it avoids. |
| `20260802-defer-prompt-engineering-to-manifest-dev` | **Recovered** from the CHANGELOG's v3.0.0 entry and PR #114. |
| `20260430-tracked-set-deletion-protects-coexisting-plugins` | **Recovered** from the commit message, which states what the old model would have destroyed. |
| `20260723-agents-and-hooks-consolidated-into-skills` | **Not recovered.** Commit subject only; no body, no changelog entry, no discussion found. The record says so in its Context and its Alternatives section reads `_Not recovered._` rather than sitting empty. |

Not recorded: the plugin-by-plugin feature history in `CHANGELOG.md`. It is long and well kept, but
version bumps and feature additions constrain nothing downstream, so they fail the bar in
`docs/adr/CONVENTIONS.md`. The four above were chosen because each still governs how the repository
works today.

## Glossary candidates — awaiting ratification

Nothing has been written to `CONTEXT.md`. Accept the ones you want; the rest are dropped.

| Term | Proposed definition | Why it earns entry |
|------|--------------------|--------------------|
| **Layout verdict** | A repository's single storage arrangement for skills — *plain* (`.claude/skills/` holds the real directories, `.agents/skills/` mirrors) or *inverted* (the reverse) — decided once per repository rather than per skill. | Decides where sync writes. Reading it as a per-skill property is the exact defect PR #118 fixed, and it left one repo silently split. |
| **Mirror** | The side that holds symlinks pointing at the real directories, rather than the content itself. | Confusable with "sync" and with the real side. Writing through a mirror that points into another plugin's source is the corruption the classification rules exist to prevent. |
| **Tracked set** | The record of items a previous sync wrote, held in `.claude/.manifest-dev-sync.json`; the only items sync may delete. | Reading it as "everything in the synced directories" is precisely the model that would have deleted this repository's own plugins. |
| **Fleet** | The set of repositories `sync-manifest-dev` runs across, as opposed to this repository alone. | A change to the sync tool is judged against all of them — "verified" means verified fleet-wide, which is a different claim from "works here". |

**Considered and dropped** — accurate but not load-bearing, so not worth a permanent per-session
cost: `plugin`, `skill`, `agent`, `hook`, `marketplace`, `component`, `adopt`, `flip`,
`plain write`, `plugin.json`. Misreading any of these does not change what someone builds.
