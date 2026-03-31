---
name: babysit-pr
description: 'Babysit a PR until merge-ready, then ask before merging. Runs pr-merge-prep on a 10-minute loop, monitors readiness (CI, reviews, conflicts), auto-stops when ready, and requires explicit user confirmation to merge. Never merges autonomously. Use when: "babysit this pr", "watch pr until ready", "keep fixing pr until mergeable".'
user-invocable: true
---

**User request**: $ARGUMENTS

## Goal

Thin orchestration wrapper: start a recurring pr-merge-prep loop, monitor the PR until it reaches merge-ready state, stop the loop, and ask the user whether to merge. **Never merge without explicit user confirmation.**

## Flow

### 1. Detect PR

If PR number/URL is in $ARGUMENTS, use it. Otherwise detect from the current branch via `gh pr view --json number,url,title,isDraft`.

If no PR found, report and stop.
If PR is draft, report "PR is draft — nothing to babysit" and stop.

### 2. Start the Loop

Invoke the loop skill with: "10m /pr-merge-prep $PR_IDENTIFIER"

This starts pr-merge-prep running every 10 minutes in the background.

### 3. Monitor for Merge Readiness

After starting the loop, immediately run a readiness check (don't wait 10 minutes for the first one). Then continue checking after each loop iteration.

**Readiness check** — run `gh pr view $PR_NUMBER --json mergeable,reviewDecision,statusCheckRollup,reviewRequests,comments` and evaluate:

| Condition | Ready? |
|-----------|--------|
| All CI/status checks pass (no pending, no failing) | Required |
| No unresolved review threads | Required |
| No merge conflicts (mergeable != CONFLICTING) | Required |
| Review decision is APPROVED or no reviewers assigned | Required |

If **all conditions met**: PR is merge-ready. Proceed to step 4.
If **not ready**: Log what's still blocking and let the loop continue. The next pr-merge-prep iteration will work on remaining blockers.

### 4. Stop the Loop

When the PR is merge-ready, stop the cron schedule that was created in step 2. Use CronDelete to remove it.

### 5. Ask User to Merge

**CRITICAL: Never merge automatically. Always ask.**

Report the PR status summary to the user:
- PR title and URL
- All checks passing
- Review status
- Any remaining open (uncertain) comment threads that pr-merge-prep left for human review

Then ask the user: **"PR is ready to merge. Would you like me to merge it?"**

- If user says **yes**: merge via `gh pr merge $PR_NUMBER --merge` (or `--squash`/`--rebase` if user specifies)
- If user says **no** or **not yet**: acknowledge and stop. Do not merge.
- If user doesn't respond: do nothing. The PR stays open.
