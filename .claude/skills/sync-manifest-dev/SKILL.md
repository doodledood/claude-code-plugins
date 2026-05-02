---
name: sync-manifest-dev
description: 'Sync the manifest-dev plugin from doodledood/manifest-dev into .claude/ for local development. Clones or pulls the repo, copies agents/skills/hooks, and removes only previously-synced items that disappeared upstream. Other plugins in .claude/ are left alone. Use when asked to sync manifest-dev, update manifest-dev, or pull latest manifest-dev.'
user-invocable: true
---

**User request**: $ARGUMENTS

Sync manifest-dev plugin components into this repo's `.claude/` directory. manifest-dev OWNS only the files it ships — other plugins (e.g. prompt-engineering, project-local KB skills) coexist in `.claude/agents/`, `.claude/hooks/`, and `.claude/skills/` and must be left alone.

## Source & Target

| Role | Path |
|------|------|
| Remote repo | `https://github.com/doodledood/manifest-dev.git` |
| Local clone | `/tmp/manifest-dev` |
| Source components | `/tmp/manifest-dev/claude-plugins/manifest-dev/` |
| Target | `.claude/` in this repo |
| Tracking file | `.claude/.manifest-dev-sync.json` |

## Sync scope

| Component | Source dir | Target dir |
|-----------|-----------|------------|
| Agents | `agents/` | `.claude/agents/` |
| Hooks | `hooks/` | `.claude/hooks/` |
| Skills | `skills/` | `.claude/skills/` |

## Territory model

**Deletion invariant**: only items in `tracked` (the previously-synced set) are eligible for removal when they disappear upstream. Items never in `tracked` are invisible — that's how project-local content (KB skills, prompt-engineering, anything else) stays safe.

The tracked set lives in `.claude/.manifest-dev-sync.json`:

```json
{
  "version": 1,
  "last_synced_at": "ISO-8601 timestamp",
  "agents":  ["change-intent-reviewer.md", "..."],
  "hooks":   ["hook_utils.py", "..."],
  "skills":  ["auto", "define", "..."]
}
```

First run (file missing): `tracked` is empty, no deletions happen, file is written at end.

## Sync algorithm

For each component (agents/hooks/skills):

- **Copy** every source item over its target path. Skip if target is a symlink.
- **Delete** items in `tracked − source` from target. Skip if target is a symlink, doesn't exist, or is the `sync-manifest-dev` skill itself.
- **Refresh** `.claude/.manifest-dev-sync.json` with the current source listing.

Source listing excludes `.claude-plugin/` and `README.md` (plugin metadata, not content).

## .agents mirror

After each sync, ensure `.agents/skills/<name>` is a symlink to `../../.claude/skills/<name>` for every tracked skill, and remove the symlink for any skill removed from `tracked`. This lets non-Claude coding agents (Codex, etc.) read the same skills without duplicating content. Only skills are mirrored — `.agents/agents/` and `.agents/hooks/` are out of scope.

- Create the symlink if missing.
- If `.agents/skills/<name>` exists and is not a symlink, skip it — that's project-local content, don't clobber.
- Create `.agents/skills/` if missing, but never `.agents/` itself (the user opts in by creating it).

## Gotchas

- **Nested skills directory**: Source skills live at `skills/define/`, `skills/do/`, etc. Copy each skill directory into `.claude/skills/<skill-name>/` — don't copy the outer `skills/` folder or you get `.claude/skills/skills/`.
- **Symlinks look like directories to `cp`/`rm`/`find`**: A symlinked target overwritten by `cp -R` corrupts the linked plugin's source files; a symlinked directory deleted by `rm -rf` removes the link, not the plugin, but a recursive find that follows the link will. Use `[ -L path ]` before every overwrite and every delete.

## Output

Summary table per component (agents/hooks/skills): items added, updated, removed, symlinks skipped, and removals refused (e.g. due to symlink). Show the net change to the tracking file.

## Never

- Overwrite, remove, or follow into symlinks under `.claude/` — check `[ -L path ]` before every copy, delete, or recursive descent
- Replace a non-symlink at `.agents/skills/<name>` — leave project-local content alone
- Create `.agents/` itself (only manage `.agents/skills/<name>` entries inside an existing `.agents/`)
- Delete items not in the tracked set — even if they're not in source
- Delete the `sync-manifest-dev` skill
- Copy plugin metadata (`.claude-plugin/`, `README.md`) or manifest-dev's own `.claude/` directory
- Modify the source repo
