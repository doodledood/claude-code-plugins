---
name: pr-merge-prep
description: 'Autonomously bring a PR to mergeable state. Resolves merge conflicts, fixes CI failures, addresses review comments, syncs PR description, and requests re-review. Designed for unattended cron execution via loop skill. Use when: "prep pr for merge", "make pr mergeable", "fix pr blockers", "autonomous pr maintenance".'
user-invocable: true
---

**User request**: $ARGUMENTS

**If no PR specified**: Detect PR from current branch. If detection fails, report and stop.

**If PR is draft**: Log "PR is draft, skipping" and stop.

## Goal

Single-pass autonomous pipeline that identifies and resolves PR merge blockers: conflicts, CI failures, review comments. Each invocation handles what's currently blocking — the loop skill handles re-running for iterative convergence across invocations.

## Concurrency Guard

After PR detection and draft check, prevent concurrent runs on the same PR. If another run is currently active, abort and log "Concurrent run detected, skipping." Acquire the lock when starting work, release on every exit path (including early exits and errors).

## Pipeline

Execute phases in order. Log findings to `/tmp/pr-merge-prep-log-{pr-number}.md` after each phase (append to existing log if present, enabling cross-invocation continuity).

**Push rule**: Batch all commits from a phase and push once at the phase boundary. CI and downstream phases depend on the pushed state.

**CI wait rule**: After any phase pushes, the next phase that reads CI status must wait for checks to reach terminal status (success or failure). If checks remain pending, log as inconclusive and continue to the next phase — independent phases (comment triage, description sync) should not be blocked by slow CI. Only Phase 6 (re-review) hard-gates on CI terminal status.

### Phase 1: Merge Conflicts

Update the PR branch to include the latest changes from the base branch (even if the diff is empty — the branch may be behind). Resolve conflicts where only one side modified the region or where changes are in non-overlapping sections. Log all other conflicts as unresolved. If the update strategy does not support partial conflict resolution, log all conflicts as unresolved. If the branch update itself fails (branch protection, force-pushed base, etc.), log the error as "Phase 1 failed" and continue to Phase 2 — CI triage and comment processing are independent of branch update state. Phase 2 should skip code-caused fixes (branch may be stale) but can still retrigger infrastructure failures. Note that if no push occurred this invocation, CI data reflects the prior push state — triage is still valid for infrastructure re-triggers but code-caused classification may be stale.

If the PR targets a non-default base branch, handle normally.

### Phase 2: CI Failures

**Triage before fixing:**
- Compare failing checks against the base branch. Pre-existing failures (also failing on base) are not the PR's responsibility — skip them.
- Infrastructure failures (DNS errors, flaky tests, timeout without code cause) — trigger a CI re-run.
- Code-caused failures — read the failure logs, identify the root cause, and fix. (If the diff is empty or Phase 1 failed, skip code-caused fixes — only handle infrastructure re-triggers.)

Each code fix must be an atomic commit with a descriptive message. Run project tests before committing to verify no regressions — if tests fail, revert the fix and log it as unresolvable. Local test results approximate CI behavior; if the fix passes locally but fails in CI, the next invocation will catch it.

If no project test commands are discoverable, skip the test verification step and log the assumption.

### Phase 3: Review Comments

Triage all unresolved PR review comments in a single pass. Note: comments marked "outdated" by GitHub due to rebase (positional staleness from Phase 1) are different from the "Outdated" false-positive pattern below — positionally outdated comments may still be valid and should be triaged normally.

**Classification prerequisites**: Bot/human labeling (see `references/known-bots.md`) and full thread context inform every classification. No comment is classified without both. Classify before fixing. Threads with sub-discussions, follow-up questions, or unanswered replies are uncertain regardless of top-level content.

**Classification criteria:**

| Classification | Criteria |
|---------------|----------|
| **Actionable** | Real issue with a clear, safe fix. The fix does not touch core logic or require a large refactor. |
| **False positive** | Matches a false-positive pattern (see below). Premise contradicts actual code behavior. |
| **Uncertain** | Unclear validity, risky fix, touches core logic, or requires large refactor. |

**False-positive detection patterns:**

| Type | Signal |
|------|--------|
| **Outdated** | Suggested change already exists in code; commit history shows it was addressed |
| **Misread code** | Comment's premise contradicts what code actually does |
| **Wrong context** | Comment references behavior/variables not present in the target code |
| **Style preference** | No functional or readability improvement — naming changes that aid comprehension are actionable, not style |
| **Resolved in thread** | Reply discussion shows issue was already addressed or withdrawn |

See `references/classification-examples.md` for concrete examples of each classification.

**Actions by classification:**

| Classification | Action |
|---------------|--------|
| **Actionable** | If Phase 1 failed, reclassify as uncertain (branch may be stale) and follow the uncertain action below. Otherwise: fix the issue → run tests → if tests fail, revert and reclassify as uncertain → commit atomically → reply explaining the fix → resolve full thread. If the diff is empty and the comment targets code that no longer exists, reclassify as false positive. |
| **False positive** | Reply with brief reasoning why it's a false positive → resolve full thread |
| **Uncertain** | Reply explaining the uncertainty and what would be needed to resolve → leave thread **open** |

**Reply on every comment** — bot or human. Replies serve as the audit trail for this autonomous run.

**Resolve full threads**, not individual comments. The only exception is uncertain comments — those threads stay open for human review. If thread resolution fails (API error, permission issue), log the failure and treat the thread as unresolved for Phase 6 gating.

**Phase 3 log entry**: After processing all comments, log: final classification counts (after any reclassifications), number of successfully pushed commits (not reverted attempts), count of threads that should have been resolved (only threads whose final classification is actionable or false-positive), count actually resolved, and any failed resolutions. Phase 4 uses the commit count to gate itself. Phase 6 compares "should have resolved" vs "actually resolved" to evaluate its gating condition.

**Safety boundary**: If a fix would touch core logic, require a large refactor, or the confidence in the fix is not high — classify as uncertain instead. Log the reasoning.

### Phase 4: Final CI Check

If Phase 3 produced commits (check the execution log for the commit count), wait for CI per the pipeline CI wait rule, then check whether any new failures appeared. If so, apply the Phase 2 triage-and-fix process once — no further iterations within this invocation. If CI is inconclusive, log it and continue to Phase 5. The next cron invocation handles any remaining failures.

### Phase 5: PR Description Sync

Read the full current diff and the existing PR description.

- **Preserve** manual context: issue references (`#123`, `Fixes #456`), motivation sections, related PR links, deployment notes, or any content that cannot be derived from the diff alone.
- **Update** the "what changed" sections to accurately reflect the current state of all changes. Write as if creating the PR fresh — not appending "also fixed X." If the diff is empty, preserve the existing description and note that all changes have been reverted.
- **Rewrite the title** if it no longer accurately describes the PR's current scope.

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
- **CI re-run for infra failures**: Triggering a CI re-run (e.g., empty commit) is only appropriate for infrastructure failures, not code failures.
- **PR description rewrite can lose context**: Always read the existing description first and preserve anything that can't be derived from the diff (issue links, motivation, deployment notes).
- **Lock cleanup on crash**: If the concurrency lock isn't released due to a crash, treat it as stale after it exceeds the expected duration of a single run, so subsequent invocations aren't permanently blocked.
- **Test command discovery varies**: Not all projects have obvious test commands. Check CLAUDE.md, pyproject.toml, package.json, Makefile, etc. If nothing found, skip test verification and log it — don't fail the run.
