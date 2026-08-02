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
| Source plugins | `/tmp/manifest-dev/claude-plugins/manifest-dev/` and `/tmp/manifest-dev/claude-plugins/manifest-dev-tools/` |
| Target | `.claude/` in this repo |
| Tracking file | `.claude/.manifest-dev-sync.json` |

Both plugins are synced into the same `.claude/` target and recorded in one tracking file. `manifest-dev-tools` ships `prompt-engineering` skill and `prompt-reviewer.md` agent that may also be tracked by `sync-claude-code-plugins`; both syncs will overwrite each other's copies for those items.

## Fetching the source

Get a clean copy of `doodledood/manifest-dev` at `/tmp/manifest-dev` before syncing. Default branch is `main`.

**Get a real clone first.** The CDN fallback below reconstructs the tree from a *cached index* that can silently under-list, so it is a degraded source, not an equivalent one. Before running the helper, call the `add_repo` MCP tool for `doodledood/manifest-dev` (public, read access) and clone it — despite what the fallback rationale below says about GitHub being gated, `add_repo` is exactly the mechanism for widening that gate, and it works:

```bash
# after add_repo succeeds
git clone --depth 1 https://github.com/doodledood/manifest-dev /workspace/manifest-dev
```

The helper picks up a clone at `/workspace/manifest-dev` (or `$MANIFEST_DEV_CLONE`) automatically and skips the CDN path entirely. Only if `add_repo` is unavailable or denied should you rely on reconstruction.

```bash
bash .claude/skills/sync-manifest-dev/stage-source.sh
```

**Why the clone matters.** A sync from the CDN path once shipped `skills/do/` with its `SKILL.md` and none of its four `references/` files. Nothing failed — `/do` simply could not load its verification-mode reference and silently fell back to in-session self-verification, so runs reported a verification mode they were not actually performing. Missing files here degrade behavior quietly rather than erroring, which is what makes an incomplete source worse than a failed one. The helper now chases companion files named in staged text to repair under-listing, but that is a backstop; a clone is the fix.

On success it leaves `/tmp/manifest-dev/claude-plugins/manifest-dev{,-tools}/` populated and (in CDN mode) hash-verifies every file. The clone has no `.git/`, which is fine: this sync only reads files, never runs git inside it.

**How it fetches, and why (context for when the script needs changing):**

In Claude Code on the web / remote execution, GitHub itself is gated to the session's authorized repos. `manifest-dev` is out of scope, so **every GitHub-authenticated route to it returns HTTP 403** — `git clone`/`git pull` (rewritten through the repo-scoped relay `http://local_proxy@127.0.0.1:<port>/git/...`, see `git config --get-regexp insteadof`), `codeload.github.com` tarballs, `api.github.com`, and `github.com/.../archive` all fail with `{"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access."}`. The egress proxy is *not* the blocker (its `CONNECT` succeeds and it logs no relay failure); GitHub's session-access layer is. This is a policy denial, **not** a transient error — never retry it or apply backoff.

But `manifest-dev` is **public**, and public CDNs sit outside that GitHub gate:

- `raw.githubusercontent.com/<repo>/<ref>/<path>` serves file bodies (HTTP 200).
- `data.jsdelivr.com/v1/packages/gh/<repo>@<ref>?structure=flat` serves the full file tree **with sha256 hashes** (base64), so the reconstruction is integrity-checked, not trusted blind.

So the script tries the single-tarball fast path first (works locally, or if the session's GitHub access ever includes the repo), and on a 403 falls back to enumerating the tree from jsDelivr and pulling each `claude-plugins/` file from raw, verifying every hash. If the repo is ever made private, the CDN path 403s too — then it genuinely needs `add_repo` access and you should report that, not route around it.

## Sync scope

| Component | Source dirs (merged across both plugins) | Target dir |
|-----------|------------------------------------------|------------|
| Agents | `manifest-dev/agents/` + `manifest-dev-tools/agents/` | `.claude/agents/` |
| Hooks | `manifest-dev/hooks/` (manifest-dev-tools has no hooks) | `.claude/hooks/` |
| Skills | `manifest-dev/skills/` + `manifest-dev-tools/skills/` | `.claude/skills/` |

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

- **Build the combined source listing** by unioning the component dir from both plugins (`manifest-dev/<component>/` ∪ `manifest-dev-tools/<component>/`). If the same name appears in both, `manifest-dev-tools` wins (tools plugin is the later/extending source).
- **Copy** every source item over its target path. Skip if target is a symlink.
- **Delete** items in `tracked − combined-source` from target. Skip if target is a symlink, doesn't exist, or is the `sync-manifest-dev` skill itself.
- **Refresh** `.claude/.manifest-dev-sync.json` with the combined source listing.

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
- Copy plugin metadata (`.claude-plugin/`, `README.md`) or either plugin's own `.claude/` directory
- Modify the source repo
