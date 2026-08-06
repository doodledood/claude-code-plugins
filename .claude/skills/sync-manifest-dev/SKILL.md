---
name: sync-manifest-dev
description: 'Sync the manifest-dev plugins from doodledood/manifest-dev into .claude/. Clones the source, copies agents/skills/hooks, removes only previously-synced items that disappeared upstream, and leaves other plugins alone. Pass --all to sync every repo in the fleet and open a PR on each. Use when asked to sync manifest-dev, update manifest-dev, pull latest manifest-dev, or sync manifest across all repos.'
argument-hint: '[--all] [--check]'
user-invocable: true
---

**User request**: $ARGUMENTS

Sync manifest-dev plugin components into a repo's `.claude/` directory. manifest-dev OWNS only the files it ships — other plugins (prompt-engineering, project-local KB skills) coexist in `.claude/agents/`, `.claude/hooks/`, and `.claude/skills/` and must be left alone.

## Modes

| Invocation | Does |
|---|---|
| *(no args)* | Sync this repo only |
| `--all` | Sync every repo in the fleet below, one PR each |
| `--check` | Report what would change, write nothing (works with either) |

## Source

| Role | Path |
|---|---|
| Remote | `https://github.com/doodledood/manifest-dev` (public, default branch `main`) |
| Clone | `/workspace/manifest-dev` |
| Staged source | `/tmp/manifest-dev/claude-plugins/manifest-dev{,-tools}/` |
| Tracking file | `.claude/.manifest-dev-sync.json` (per target repo) |

Both plugins sync into the same `.claude/` target and share one tracking file. `manifest-dev-tools` ships the `prompt-engineering` skill and `prompt-reviewer.md` agent, which `sync-claude-code-plugins` may also track; the two syncs overwrite each other's copies of those.

### Fetching it

Clone it, then stage:

```bash
git clone --depth 1 https://github.com/doodledood/manifest-dev /workspace/manifest-dev
bash .claude/skills/sync-manifest-dev/stage-source.sh
```

Where the session gates GitHub to authorized repos, request read access first — the repo is public, so the request is granted immediately without attaching anything. Treat that as the ordinary path rather than an escalation to avoid.

`stage-source.sh` picks up a clone at `/workspace/manifest-dev` (or `$MANIFEST_DEV_CLONE`) and copies it to `/tmp/manifest-dev`. Record the clone's `git rev-parse HEAD` — it becomes `source_commit` in every tracking file, and diffing it against the previous value gives you the upstream commit list for the PR body.

**Use the clone. The CDN fallback in `stage-source.sh` is a degraded source, not an equivalent one** — it rebuilds the tree from a cached index that can silently under-list. It once shipped `skills/do/` with `SKILL.md` and none of its four `references/` files: nothing errored, `/do` just quietly fell back to self-verification while reporting a mode it was not running. Fall back only if read access is denied, and say so in the PR when you do.

## The fleet

These repos carry a `.claude/.manifest-dev-sync.json` and sync together under `--all`:

| Repo | Layout | Notes |
|---|---|---|
| `doodledood/second-brain` | plain + `.agents/` mirror | |
| `doodledood/aviramk.dev` | plain + `.agents/` mirror | |
| `doodledood/trueelo` | plain, no `.agents/` | no mirror to manage |
| `doodledood/claude-code-plugins` | plain + `.agents/` mirror | `review-prompt` is a foreign symlink, always skipped |
| `doodledood/pi-plugins` | **inverted** | real content in `.agents/skills/`, `.claude/skills/` symlinked to it |

A repo joins the fleet when it gains the tracking file. If one of these no longer has it, drop it and say so rather than recreating it.

Every fleet repo carries this skill, so `--all` runs from any of them. Changing it means changing all the copies in the same pass — they drifted once, and the stale ones skip every skill in the inverted layout while reporting success.

## Sync scope

`agents/`, `hooks/`, and `skills/` from each plugin, into the same-named directory under `.claude/`. Union both plugins; on a name collision `manifest-dev-tools` wins. Exclude `.claude-plugin/` and `README.md` — plugin metadata, not content.

Upstream currently ships no `agents/` or `hooks/` directories at all. That is normal, and it must not be read as everything having been deleted upstream.

## Territory model

**Only items in `tracked` may be deleted.** Anything never tracked is invisible to this sync — that is what keeps project-local content (KB skills, `frontend-design`, `tend-pr`, `sync-pi-setup`) safe.

**`tracked` records what this sync actually wrote, not what upstream ships.** An item skipped because its target belongs to another plugin must stay out of the tracked set. Recording it would license a later run to delete a file this sync never owned.

First run (no tracking file): `tracked` is empty, nothing is deleted, the file is written at the end.

## Repo layout

A repo is **inverted** when at least one skill already keeps its real content in `.agents/skills/<name>` with `.claude/skills/<name>` a symlink onto it. One such skill settles it for the whole repo, and that verdict decides which side a *new* skill's real content goes on. Otherwise the repo is **plain**.

The verdict is per repo because a per-skill reading leaves a repo half inverted: a skill absent from both sides reads as a plain write and lands as a real `.claude/` directory among neighbours stored the other way round. Both arrangements resolve, so nothing fails and the split stays invisible until someone reads the tree — pi-plugins carried two such skills before this was fixed.

`sync.py` prints the verdict in its summary header. Treat a repo you expect to be inverted printing `[plain]` as a finding to check, not a detail: new content will land on the other side from everything already there.

## Symlink classification

Classify every target before touching it:

- **direct** — not a symlink. Write it.
- **mirror** — `.claude/skills/<name>` is a symlink onto real content in *this repo's own* `.agents/skills/<name>` (the inverted layout, pi-plugins). Write through to the resolved path. The symlink stays; both paths keep resolving to the same content.
- **adopt** — a skill absent from an inverted repo. Its real content goes to `.agents/skills/<name>`, with `.claude/skills/<name>` created as a symlink onto it, matching the skills already there.
- **foreign** — a symlink pointing anywhere else. Never write, never delete, never track.

The mirror test needs both halves: the resolved path's parent must be this repo's `.agents/skills/`, **and** the `.agents/skills/<name>` entry must be a real directory rather than a symlink. Testing only that the two sides resolve equal will corrupt a foreign plugin — in `claude-code-plugins`, `.claude/skills/review-prompt` and `.agents/skills/review-prompt` both resolve into `claude-plugins/prompt-engineering/`, because the `.agents` entry is an ordinary mirror symlink pointing back at `.claude/`. The realness of the `.agents` entry is what separates the two layouts.

Skipping every symlink instead fails the other way: in pi-plugins it syncs nothing and reports success.

## The `.agents` mirror

Where `.agents/` exists, every tracked skill is reachable at `.agents/skills/<name>`, so non-Claude agents read the same content. Only skills are mirrored.

- Missing → create a symlink to `../../.claude/skills/<name>`.
- Already a symlink → leave it.
- Exists and is not a symlink → skip, that is project-local content.
- Classified **mirror** or **adopt** → nothing to do, the real content already lives there.
- Skill dropped from `tracked` → remove its symlink. On an inverted repo the real content *is* the `.agents/` side, so removing a skill there deletes both sides; leaving the `.claude/` symlink behind would leave it dangling.

Never create `.agents/` itself. The user opts in by creating it; `trueelo` has none and must stay that way.

On an inverted repo, a skill found sitting the plain way round is flipped back: real content moved to `.agents/skills/<name>`, `.claude/skills/<name>` replaced by a symlink onto it. The summary reports these as `mirror flipped`. It is a move, so expect the diff to show the content deleted on one side and added on the other.

## Running it

```bash
python3 .claude/skills/sync-manifest-dev/sync.py <repo-root> /tmp/manifest-dev/claude-plugins <source-commit> [--check]
```

`sync.py` implements everything above, verifies every synced item against the source after copying, and exits non-zero if any differ. It only rewrites items whose content actually changed, so the diff stays small. The machine-readable report for the PR body goes to `/tmp/manifest-dev-sync-report-<repo>.json`, outside the repo so it cannot be committed.

Do not re-derive the algorithm by hand. The symlink classification above was written after a hand-rolled pass corrupted a foreign plugin's source.

## The `--all` workflow

Stage the source once, then per repo:

1. Ensure a clone with **push** access — these are the user's own repos, and `second-brain`, `aviramk.dev`, and `trueelo` are private. Clone one repo at a time; concurrent clones of the same repo hit a per-repo concurrency cap and 429.
2. Branch. Use one branch name across the fleet so the PRs read as one change, unless the session was handed a designated branch.
3. Run `sync.py`. If it exits non-zero, stop on that repo and report — never commit a failed verification.
4. Read `git status` before committing. This is what caught the foreign-plugin corruption: **any path outside `.claude/` and `.agents/` means the sync wrote somewhere it should not have.**
5. Commit, push, and open a PR stating the upstream commit range, the per-component counts, and anything skipped and why. A skip is a fact the reviewer needs, not an omission to hide.

Close with one fleet table: repo, PR link, counts, anything skipped. `pi-plugins` runs `check-version-bump`, which only fires on `packages/` changes and so passes on a sync.

## Never

- Write through, delete, or descend into a **foreign** symlink
- Record a skipped item in `tracked`
- Replace a non-symlink at `.agents/skills/<name>`
- Create `.agents/` itself
- Delete anything not in `tracked`, even when it is absent from source
- Delete the `sync-manifest-dev` skill
- Copy plugin metadata (`.claude-plugin/`, `README.md`) or either plugin's own `.claude/`
- Modify the source repo
