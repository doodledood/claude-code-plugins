---
name: pr-merge-prep
description: 'Autonomously bring a PR to mergeable state. Resolves merge conflicts, fixes CI failures, addresses review comments, syncs PR description, and requests re-review. Designed for unattended cron execution via loop skill. Use when: "prep pr for merge", "make pr mergeable", "fix pr blockers", "autonomous pr maintenance".'
---

**User request**: $ARGUMENTS

**If no PR specified**: Detect PR from current branch. If detection fails, report and stop.

**If PR is draft**: Log "PR is draft, skipping" and stop.

## Goal

Single-pass autonomous pipeline that identifies and resolves PR merge blockers: conflicts, CI failures, review comments. Each invocation handles what's currently blocking — the loop skill handles re-running for iterative convergence across invocations.

## Concurrency Guard

After PR detection and draft check, prevent concurrent runs on the same PR. If another run is currently active, abort and log "Concurrent run detected, skipping." Acquire the lock when starting work, release on every exit path (including early exits and errors).

## Pipeline

Execute phases in order — fixed sequencing ensures predictable, auditable behavior for unattended cron runs. Log findings to `/tmp/pr-merge-prep-log-{pr-number}.md` after each phase (append to existing log if present, enabling cross-invocation continuity).

**Push rule**: Batch all commits from a phase and push once at the phase boundary. CI and downstream phases depend on the pushed state. If a phase-boundary push fails, log the error and discard unpushed local commits — they cannot take effect. Any replies or thread resolutions made during the phase before the push are now orphaned; log them as provisional failures. Continue to the next phase treating this phase as having produced no commits.

**CI wait rule**: After any phase pushes, the next phase that reads CI status must wait for checks to reach terminal status (success or failure). If checks remain pending, log as inconclusive and continue to the next phase — independent phases (comment triage, description sync) should not be blocked by slow CI. Only Phase 6 (re-review) hard-gates on CI terminal status.

**Test discipline**: Every code fix must pass project tests before committing. If tests fail, revert the fix and log it as unresolvable. If no project test commands are discoverable, skip test verification and log the assumption.

### Phase 1: Merge Conflicts

Always update the PR branch to include the latest base branch changes, even when there are no conflicts (the branch may be behind). Auto-resolve only conflicts with a clear, safe resolution. Log all others as unresolved. If the update strategy does not support partial conflict resolution, log all conflicts as unresolved. If the update fails, log as "Phase 1 failed" and continue to Phase 2.

**Phase 1 failure impact**: Phase 2 skips code-caused fixes (only infrastructure re-triggers), CI data may reflect a prior push state. Phase 3 reclassifies actionable comments as uncertain. Phase 6 gating condition is not met.

If the PR targets a non-default base branch, handle normally.

### Phase 2: CI Failures

**Triage before fixing:**
- Compare failing checks against the base branch. Pre-existing failures (also failing on base) are not the PR's responsibility — skip them.
- Infrastructure failures (DNS errors, flaky tests, timeout without code cause) — trigger a CI re-run.
- Code-caused failures — fix the root cause. If the diff is empty or Phase 1 failed, skip code-caused fixes — only handle infrastructure re-triggers.

Each code fix must be an atomic commit with a descriptive message. Local test results approximate CI behavior; if a fix passes locally but fails in CI, the next invocation will catch it.

### Phase 3: Review Comments

Triage all unresolved PR review comments in a single pass. Note: comments marked "outdated" by GitHub due to rebase (positional staleness from Phase 1) are different from the "Outdated" false-positive pattern below — positionally outdated comments may still be valid and should be triaged normally.

**Classification prerequisites**: Every classification requires bot/human labeling (see `references/known-bots.md`) and full thread context. Classify before fixing. Threads with sub-discussions, follow-up questions, or unanswered replies are uncertain regardless of top-level content.

**Classification criteria:**

| Classification | Criteria |
|---------------|----------|
| **Actionable** | Real issue with a clear, safe fix. The fix does not touch core logic or require a large refactor. |
| **False positive** | Matches a false-positive pattern (see below). Premise contradicts actual code behavior. |
| **Uncertain** | Unclear validity, risky fix, low confidence, touches core logic, or requires large refactor. When in doubt, choose uncertain and log the reasoning. |

**False-positive detection patterns:**

| Type | Signal |
|------|--------|
| **Outdated** | Suggested change already exists in code; commit history shows it was addressed |
| **Misread code** | Comment's premise contradicts what code actually does |
| **Wrong context** | Comment references behavior/variables not present in the target code |
| **Style preference** | No functional or readability improvement — naming changes that aid comprehension are actionable, not style |
| **Resolved in thread** | Reply discussion shows issue was already addressed or withdrawn |

See `references/classification-examples.md` for concrete examples of each classification.

**Actions by classification** (every classification includes a reply — bot or human — as audit trail):

| Classification | Action |
|---------------|--------|
| **Actionable** | See actionable flow below |
| **False positive** | Reply with brief reasoning why it's a false positive → resolve full thread |
| **Uncertain** | Reply explaining the uncertainty and what would be needed to resolve → leave thread **open** |

**Actionable flow:**
- If Phase 1 failed, reclassify as uncertain (branch may be stale) and follow the uncertain action above.
- If the diff is empty and the comment targets code that no longer exists, reclassify as false positive.
- Otherwise: fix the issue → test per pipeline discipline → commit atomically → reply explaining the fix → resolve full thread. If tests fail, revert and reclassify as uncertain.

**Resolve full threads**, not individual comments. The only exception is uncertain comments — those threads stay open for human review. If thread resolution fails (API error, permission issue), log the failure and treat the thread as unresolved for Phase 6 gating.

**Phase 3 log entry**: Log classification outcomes (after reclassifications), commit count, count of threads that should have been resolved (actionable + false-positive, by final classification), count actually resolved, and any failed resolutions. Phase 4 uses the commit count. Phase 6 compares "should have resolved" vs "actually resolved."


### Phase 4: Post-Comment CI Check

If Phase 3 produced commits (check the execution log for the commit count), wait for CI per the pipeline CI wait rule, then check whether any new failures appeared. If so, apply the Phase 2 triage-and-fix process for new failures. Defer remaining failures to the next invocation to keep each invocation bounded and auditable. If CI is inconclusive, log it and continue to Phase 5.

### Phase 5: PR Description Sync

Update the PR description and title to accurately reflect the current diff. Preserve content not derivable from the diff (issue references, motivation, deployment notes). For large diffs that exceed context, derive from commit messages and file-level changes. If the diff is empty, preserve the existing description and note that all changes have been reverted.

### Phase 6: Re-Review Request

Only execute if **all** of the following are true:
- Phase 1 completed successfully with no unresolved merge conflicts (if Phase 1 failed, this condition is not met)
- No failing, pending, or inconclusive CI checks remain (excluding pre-existing base-branch failures)
- All actionable and false-positive threads were resolved in Phase 3 (compare "should have resolved" vs "actually resolved" counts in the execution log)
- Reviewers are assigned to the PR

If the diff is empty, skip this phase — requesting re-review of an empty diff is not useful. If CI never reached terminal status during this invocation (logged as inconclusive in Phases 2 or 4), this phase is skipped — the next invocation will re-evaluate with terminal CI status.

Request re-review from reviewers who have a `changes_requested` status. If uncertain comments remain open, note them in the re-review request so the reviewer knows what needs human attention. If no reviewers are assigned, skip this phase and log it.

### Phase 7: Status Report

Append the final status report to the execution log at `/tmp/pr-merge-prep-log-{pr-number}.md`:

- **Actions taken**: fixes applied, comments resolved, commits made
- **Skipped items**: with reasoning for each skip
- **Remaining blockers**: unresolved conflicts, uncertain comments, failing CI
- **PR state**: current merge readiness (ready / blocked by X)

## Gotchas

- **Bot comments repeat after push**: After fixing and pushing, bot reviewers (CodeRabbit, Bugbot) re-scan and may flag new issues. This skill does a single pass — the loop skill handles the next round. Don't chase new bot findings within the same invocation.
- **Thread resolution is permanent**: Once a thread is resolved, it collapses in the GitHub UI. Always reply before resolving so the reasoning is visible in the thread.
- **Rebase rewrites history**: After rebasing, all commit SHAs change. Existing review comments may become "outdated" in GitHub's UI. This is positional staleness, not content staleness — triage these comments normally per Phase 3.
- **PR description rewrite can lose context**: Always read the existing description first and preserve anything that can't be derived from the diff (issue links, motivation, deployment notes).
- **Lock cleanup on crash**: If the concurrency lock is stale (the process that created it is no longer running), claim it and proceed — don't let a crashed prior run permanently block the pipeline.
