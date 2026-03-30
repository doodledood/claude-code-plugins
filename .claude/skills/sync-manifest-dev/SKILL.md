---
name: sync-manifest-dev
description: 'Sync the manifest-dev plugin from doodledood/manifest-dev into .claude/ for local development. Clones or pulls the repo, copies agents/skills/hooks, removes stale files. Use when asked to sync manifest-dev, update manifest-dev, or pull latest manifest-dev.'
user-invocable: true
---

**User request**: $ARGUMENTS

Sync manifest-dev plugin components into this repo's `.claude/` directory. manifest-dev is the source of truth — `.claude/agents/`, `.claude/hooks/`, and `.claude/skills/` should mirror the plugin's components after sync, except for symlinks.

## Source & Target

| Role | Path |
|------|------|
| Remote repo | `https://github.com/doodledood/manifest-dev.git` |
| Local clone | `/tmp/manifest-dev` |
| Source components | `/tmp/manifest-dev/claude-plugins/manifest-dev/` |
| Target | `.claude/` in this repo |

## Sync scope

| Component | Source dir | Target dir |
|-----------|-----------|------------|
| Agents | `agents/` | `.claude/agents/` |
| Hooks | `hooks/` | `.claude/hooks/` |
| Skills | `skills/` | `.claude/skills/` |

**manifest-dev is source of truth**: After sync, every non-symlink file in the target dirs should match the source. Files in target that don't exist in source get deleted. Files in source that are new get added.

## Symlink preservation

Some `.claude/` entries are symlinks to other local plugins (e.g., prompt-engineering). **Never overwrite, replace, or remove symlinks.** Skip them during both copy and stale-file cleanup. Note skipped symlinks in the summary.

## Excluded from sync

- `.claude-plugin/` and `README.md` (plugin metadata)
- The manifest-dev repo's own `.claude/` directory (private to that repo)

## Gotchas

- **Nested skills directory**: Source skills live at `skills/define/`, `skills/do/`, etc. Copy each skill directory into `.claude/skills/` — don't copy the `skills/` folder itself or you get `.claude/skills/skills/`.
- **learn-from-session exists in both repos**: This skill may exist locally before sync. The manifest-dev version is authoritative — overwrite it.
- **Network failures on clone/pull**: Retry with backoff before failing.

## Output

Summary table: files added, updated, removed, and symlinks skipped.

## Never

- Overwrite or remove symlinks
- Copy plugin metadata (`.claude-plugin/`, `README.md`)
- Modify the source repo
- Copy manifest-dev's `.claude/` directory
