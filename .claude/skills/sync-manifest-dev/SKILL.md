---
name: sync-manifest-dev
description: 'Sync the manifest-dev plugin from doodledood/manifest-dev into .claude/ for local development. Clones or pulls the repo, copies agents/skills/hooks, removes stale files. Use when asked to sync manifest-dev, update manifest-dev, or pull latest manifest-dev.'
user-invocable: true
---

# /sync-manifest-dev

**User request**: $ARGUMENTS

Sync the manifest-dev plugin components from `doodledood/manifest-dev` into this repo's `.claude/` directory.

## Source

| Role | Path |
|------|------|
| Remote repo | `https://github.com/doodledood/manifest-dev.git` |
| Local clone | `/tmp/manifest-dev` |
| Source components | `/tmp/manifest-dev/claude-plugins/manifest-dev/` |
| Target | `.claude/` in this repo |

## What to sync

| Component | Source | Target |
|-----------|--------|--------|
| Agents | `claude-plugins/manifest-dev/agents/*.md` | `.claude/agents/` |
| Hooks | `claude-plugins/manifest-dev/hooks/` | `.claude/hooks/` |
| Skills | `claude-plugins/manifest-dev/skills/*/` | `.claude/skills/*/` |

## What to preserve

**Never overwrite symlinks.** Some `.claude/` entries are symlinks to other local plugins (e.g., prompt-engineering). Before copying, check if the target path is a symlink. If it is, skip it and note it in the summary.

## Procedure

1. **Clone or pull**: If `/tmp/manifest-dev` exists, `git -C /tmp/manifest-dev pull origin main`. Otherwise, `git clone` the repo to `/tmp/manifest-dev`.

2. **Detect stale files**: List all non-symlink files in `.claude/agents/`, `.claude/hooks/`, and `.claude/skills/` that are managed by this sync (i.e., not symlinks). Compare against source. Delete files/directories in target that no longer exist in source.

3. **Copy components**: For each component type (agents, hooks, skills), copy from source to target. Skip any target path that is a symlink.

4. **Summary**: Report what was added, updated, removed, and skipped (symlinks).

## Never

- Overwrite or remove symlinks in `.claude/`
- Copy `.claude-plugin/` or `README.md` from the plugin (those are plugin metadata, not local dev files)
- Modify the source repo
- Copy the `.claude/` directory from manifest-dev (that's private to that repo)
