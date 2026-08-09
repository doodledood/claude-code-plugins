# claude-code-plugins

A marketplace of Claude Code plugins, several of which are synced from upstream manifest-dev rather than authored here.

## Language

**Layout verdict**:
A repository's single storage arrangement for skills — *plain* (`.claude/skills/` holds the real directories, `.agents/skills/` mirrors them) or *inverted* (the reverse) — decided once per repository rather than per skill.
_Avoid_: Skill layout (that reads as a per-skill property, which is the defect this replaced).

**Mirror**:
The side holding symlinks that point at the real directories, rather than the content itself.
_Avoid_: Sync, copy.

**Tracked set**:
The record of items a previous sync wrote, held in `.claude/.manifest-dev-sync.json`; the only items a sync may delete.
_Avoid_: Synced directory, managed content.

**Fleet**:
The set of repositories `sync-manifest-dev` runs across, as opposed to this repository alone.

## Relationships

- A **Layout verdict** is taken once per repository and governs every skill in it; one skill stored `.agents`-real settles it.
- The **Mirror** is whichever side the **Layout verdict** did not choose as real; writing through a mirror that points outside the skill tree is how another plugin's source gets corrupted.
- Only members of the **Tracked set** are eligible for deletion, which is what lets project-local plugins share the same directories as synced ones.
- A change to the sync tool is judged against the whole **Fleet**, not against this repository alone.

## Flagged ambiguities

_None yet._
