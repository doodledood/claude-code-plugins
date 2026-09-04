# ADR: The /define session-learning skills are retired

## Status
Accepted

## Area
Plugin structure

## Context

`learn-define-patterns` read recent `/define` session transcripts, dispatched one `define-session-analyzer` worker per session, and wrote the aggregated preferences into `CLAUDE.md` under a `## /define Preferences` heading. The pair was a closed loop: `define-session-analyzer` carried `user-invocable: false` and had exactly one caller, and that caller had no other worker.

Both were repository-local. Neither appears in the tracked set that `.claude/.manifest-dev-sync.json` records, so no sync ever wrote or would rewrite them, and grep finds no reference to either name anywhere in this repository outside their own files and the two records named below.

The pair was worked on twice in one day before this. [20260904-repository-local-specialists-are-skills-not-agents](20260904-repository-local-specialists-are-skills-not-agents.md) converted `define-session-analyzer` from an agent to a skill and rewrote the caller's dispatch to name a path instead of a harness primitive. PR #163 then made the caller's Session Discovery step runnable, because it had been naming a session store it never defined.

Aviram ruled the pair superseded: an older approach to a problem he no longer solves this way. That ruling is the whole reason. Nothing in the code failed, and the work in #161 and #163 left it in better shape than it had ever been — which is what makes this worth a record rather than a silent `git rm`. The next reader meets two recent commits improving a thing that is now gone, and needs to know the deletion was a decision about the approach and not a lapse.

## Decision

`learn-define-patterns` and `define-session-analyzer` are deleted outright — the skill directories and their `.agents/skills/` mirror symlinks. Nothing replaces them, and no shim is left behind.

This follows [20260817-prompt-engineering-plugin-retired](20260817-prompt-engineering-plugin-retired.md): when Aviram rules capability superseded, this repository deletes it rather than carrying it deprecated. Git holds the history for anyone who wants the text back.

The removal narrows [20260904-repository-local-specialists-are-skills-not-agents](20260904-repository-local-specialists-are-skills-not-agents.md) without overturning it. That record's rule — components this repository keeps for itself are skills, dispatched by path and never by naming a harness primitive — still governs, and still governs `code-coverage-reviewer`, the one repository-local specialist that remains. Only two of its instances are gone.

`code-coverage-reviewer` stays as that record left it: converted, orphaned, and documented as an orphan, with its retirement an open decision on its own evidence. This retirement rests on a ruling about the `/define` learning loop and reaches nothing else.

## Alternatives Considered

- **Keep `define-session-analyzer` and retire only its caller.** Rejected: it is `user-invocable: false` with one caller. Without `learn-define-patterns` nothing can reach it, so keeping it leaves an unreachable file that a future reader has to re-derive as dead.
- **Deprecate in place — mark both as superseded and leave the files.** Rejected: a skill directory is read by the harness whether or not its prose says it is retired, so a deprecated skill still competes for a match at dispatch time. Deletion is the only marking a harness honours.
- **Move the pair to `manifest-dev` where the `define` skill lives.** Rejected: this would relocate the approach Aviram ruled superseded, not retire it, and it would hand another repository a maintenance burden nobody asked for.

## Consequences

### Positive
- The two entries nobody should type are gone from the skills listing, which is the negative consequence [20260904-repository-local-specialists-are-skills-not-agents](20260904-repository-local-specialists-are-skills-not-agents.md) recorded and accepted.
- The `/define` learning approach is on the record as decided against, so it will not be rebuilt by someone reading #161 and #163 as unfinished work.

### Negative
- There is no longer any mechanism that turns `/define` session history into written preferences. If that capability is wanted again it will be designed fresh, not restored.
- `doodledood/aviramk.dev` held its own hand-copied pair. It is retired in the same round, by a separate pull request, because the copies were independent — no sync connects them, so nothing propagates this deletion.

## Source
- Session: Aviram's ruling that both skills are superseded, given directly and with retirement as the instruction
- Related: narrows [20260904-repository-local-specialists-are-skills-not-agents](20260904-repository-local-specialists-are-skills-not-agents.md); follows the retirement precedent in [20260817-prompt-engineering-plugin-retired](20260817-prompt-engineering-plugin-retired.md)
