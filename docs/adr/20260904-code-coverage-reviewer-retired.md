# ADR: code-coverage-reviewer is retired in favour of the synced test-quality dimension

## Status
Accepted

## Area
Plugin structure

## Context

`code-coverage-reviewer` was a repository-local specialist: it read a diff, derived the test scenarios the code's logic implies, and reported the gaps as concrete inputs and expected outputs. It arrived with a batch of local development files in commit `23cf516` and was never wired to anything.

[20260904-repository-local-specialists-are-skills-not-agents](20260904-repository-local-specialists-are-skills-not-agents.md) converted it from an agent to a skill and recorded two findings about it. First, it has no caller — grep finds the name only in its own file and in a `CHANGELOG.md` line recording a sync that once updated it. Second, retiring it was weighed there and declined, on the ground that deleting working capability deserves its own evidence rather than riding along with a refactor. That record left the decision open and priced it at one `git rm`.

The evidence that was missing then is that the capability is not lost by deleting it — it is duplicated, and the duplicate is the maintained copy. `review-code` ships a `test-quality` dimension whose stated job is the same one: *"reporting scenarios with no test (coverage gaps) and tests that exist but don't actually validate behavior"* (`references/test-quality.md:3`). That dimension is better bounded than the standalone specialist. It draws an explicit line against `code-testability`, which owns the design that makes testing hard, and every other dimension in the set routes coverage findings to it by name. `review-code` is in the tracked set that `.claude/.manifest-dev-sync.json` records, so it is maintained upstream in `manifest-dev` and arrives here by sync. `code-coverage-reviewer` is in no tracked set, so nothing has maintained it since the day it was copied in.

Aviram ruled it retired.

## Decision

`code-coverage-reviewer` is deleted — the skill directory and its `.agents/skills/` mirror symlink. Coverage review in this repository is `review-code`'s `test-quality` dimension.

The `CHANGELOG.md` line naming it stays. It is a dated record of a sync that ran, not a reference to a live component, and rewriting it would falsify history to tidy a grep.

This closes the decision [20260904-repository-local-specialists-are-skills-not-agents](20260904-repository-local-specialists-are-skills-not-agents.md) left open. That record's rule — a component this repository keeps for itself is a skill, dispatched by path and never by naming a harness primitive — is untouched and governs anything added later. What changes is that no repository-local specialist remains for it to govern today.

## Alternatives Considered

- **Wire it into something rather than delete it.** Rejected: there is nothing to wire it to that `review-code` does not already serve. A second coverage reviewer would compete with the `test-quality` dimension for the same finding, and the two would drift, because only one of them is synced.
- **Keep it as a documented orphan, as the previous record did.** Rejected: that position was correct while the retirement lacked its own evidence and an owner's ruling. Both now exist. An orphan kept indefinitely still costs a listing entry and a paragraph of explanation in every record that meets it.
- **Move it upstream to `manifest-dev` so the capability survives somewhere maintained.** Rejected: upstream already has the capability as `review-code`'s `test-quality` dimension. Pushing a redundant standalone specialist there would export this repository's dead weight.

## Consequences

### Positive
- One entry fewer in the skills listing, and it was an entry nobody should have typed.
- Coverage review now has exactly one home in this repository, and it is the one that is maintained by sync rather than by nobody.
- The retirement question three records now discuss is closed, so it stops being restated.

### Negative
- The specialist's own framing is gone: it enumerated the scenarios a change *implies* before looking at the tests, where `test-quality` reviews a change's tests within a broader dimension set. If that difference turns out to matter, it will be rebuilt or asked for upstream, not restored from git.
- `doodledood/second-brain` retired its own hand-copied instance separately in PR #404. Neither deletion propagates to the other; no sync connects the copies.

## Source
- Session: Aviram's ruling, given after the no-caller finding was reported to him twice and left unacted
- Related: closes the open decision in [20260904-repository-local-specialists-are-skills-not-agents](20260904-repository-local-specialists-are-skills-not-agents.md); follows the retirement precedent in [20260817-prompt-engineering-plugin-retired](20260817-prompt-engineering-plugin-retired.md); landed alongside [20260904-define-session-learning-skills-retired](20260904-define-session-learning-skills-retired.md)
