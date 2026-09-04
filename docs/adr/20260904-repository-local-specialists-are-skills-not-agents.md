# ADR: This repository's own specialists are skills, not agents

## Status
Accepted — narrowed by [20260904-define-session-learning-skills-retired](20260904-define-session-learning-skills-retired.md), which retired `define-session-analyzer` and its caller; the rule set here still governs `code-coverage-reviewer` and anything added later

## Area
Plugin structure

## Context

[20260723-agents-and-hooks-consolidated-into-skills](20260723-agents-and-hooks-consolidated-into-skills.md) recorded that the *synced* manifest-dev payload distributes its components as skills, and stopped there. It was reconstructed from commit `24fa05a` without its rationale, so it settled the shape of the synced payload and said nothing about the components this repository holds on its own account.

Two of those survived in `.claude/agents/`: `code-coverage-reviewer.md`, and `define-session-analyzer.md`. Both were copied in as part of local development setup (commit `23cf516`) and neither is in the tracked set that `.claude/.manifest-dev-sync.json` records, so no sync would ever have touched them.

Being agents cost them two things. An agent needs a representation per harness — the `tools:` frontmatter key both files carried is read by Claude Code and by nothing else — while a skill is a directory of markdown that any harness can be pointed at. And an agent has to be *named* to be dispatched, so the one live caller said "use the `define-session-analyzer` agent". That sentence is unfollowable anywhere else: `agent` names a primitive the reader may not have, and no path is given that would let them resolve the name to a file and read it themselves.

The manifest-dev `prompt-engineering` skill states the general rule in `references/mechanics.md`: prefer a skill, because a general-purpose worker told to activate a skill reproduces agent behaviour in nearly every case, and the cases that genuinely need an agent are a restricted tool allow-list or an isolated model. Neither of these two needs either.

The sibling repository `doodledood/second-brain` converted its nine specialists on the same reasoning in PR #403, including its own copy of `code-coverage-reviewer`.

## Decision

Components this repository authors or keeps for itself are skills, wherever they run. `.claude/agents/` is deleted; both specialists now live at `.claude/skills/<name>/SKILL.md` with the usual `.agents/skills/` mirror symlink, carrying `user-invocable: false` because they are called by another skill rather than typed by a person.

A caller dispatches a specialist by pointing at its `SKILL.md` path and stating in plain language how many workers to run and why they are separate — never by naming a harness primitive. `learn-define-patterns` is rewritten that way, keeping its per-session fan-out, which is load-bearing: the independent context is what stops one session's patterns from anchoring how the next is read.

This extends [20260723](20260723-agents-and-hooks-consolidated-into-skills.md) from the synced payload to everything else, rather than superseding it — that record's claim about synced components remains true and untouched.

**`code-coverage-reviewer` has no caller in this repository.** Grep finds it only in its own file and in `CHANGELOG.md`, where a 2026-era entry records a sync that updated it. It was converted rather than retired because converting is what was asked for, and because retiring working capability is a decision worth taking on its own evidence rather than as a side effect of a refactor. Its description says so, so nobody has to rediscover it. Retiring it remains available and costs one `git rm`.

## Alternatives Considered

- **Retire `code-coverage-reviewer` instead of converting it.** It has no caller, and [20260817-prompt-engineering-plugin-retired](20260817-prompt-engineering-plugin-retired.md) establishes that this repository will delete unused capability outright. Not chosen here: that record was Aviram's explicit ruling on a named plugin, and it does not reach these two files. Converting keeps the retirement decision open; retiring now would foreclose it on nobody's authority.
- **Fold it into `review-code`'s `references/` directory, the way upstream folded the other nine reviewers.** Rejected: `review-code` is in the tracked set, so a repository-local reference file added under it would be deleted by the next sync that rewrites that skill.
- **Leave both as agents and only rewrite the caller's wording.** Rejected: it fixes the sentence and not the thing the sentence points at. The reader would follow harness-agnostic prose to a file whose frontmatter only one harness can read.

## Consequences

### Positive
- Every component in this repository is now one kind of thing, reachable by path, on any harness.
- The `learn-define-patterns` dispatch can be executed by a reader who has never seen Claude Code.
- The orphan is documented as an orphan rather than carried silently.

### Negative
- `user-invocable: false` skills still appear in a skills directory listing where an agent did not, so two entries that nobody should type are now visible to whoever browses it.
- Anything outside this repository that dispatched either specialist by its agent name is broken, and there is no shim.

## Source
- Session: converted at Aviram's instruction, with the no-caller finding for `code-coverage-reviewer` reported rather than acted on
- Related: extends [20260723-agents-and-hooks-consolidated-into-skills](20260723-agents-and-hooks-consolidated-into-skills.md) from the synced payload to repository-local components; the layout it follows is the one [20260807-layout-verdict-is-per-repo-not-per-skill](20260807-layout-verdict-is-per-repo-not-per-skill.md) settled; mirrors `doodledood/second-brain#403`
