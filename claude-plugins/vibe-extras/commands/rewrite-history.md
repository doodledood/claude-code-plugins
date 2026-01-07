---
description: 'Restructure messy branch history into clean, reviewer-friendly commits. Analyzes commits since divergence from main, groups by concern, and rewrites with conventional commit messages. Use when branch history is cluttered with WIP commits, fixups, or disorganized changes.'
argument-hint: Optional --auto to skip interactive proposal approval
---

# Rewrite History Command

Restructures messy branch history into a clean, reviewer-friendly progression of logical commits.

## Overview

This command:
1. Analyzes all commits since divergence from main/master
2. Groups changes by single concern
3. Arranges in logical order (foundations first, features second, polish last)
4. Generates commit messages matching repo style (default: Conventional Commits)
5. Rewrites history via soft reset and staged commits

**Modes**:
- **Interactive** (default): Shows proposal, allows adjustment/approval via AskUserQuestion
- **Automatic** (`--auto`): Skips proposal, executes directly

## Steps

### 1. Precondition Checks

Before any destructive operations, verify:

1. **Not on main branch**: Check current branch is not `main` or `master`
   - If on main: Error "Cannot rewrite history on main/master branch. Checkout a feature branch first."

2. **Clean working tree**: Run `git status --porcelain`
   - If uncommitted changes: Error "Uncommitted changes detected. Commit or stash changes before rewriting history."

3. **Has commits to rewrite**: Find merge-base with main/master, count commits
   - Run `git merge-base HEAD main` (or master)
   - Run `git rev-list --count {merge-base}..HEAD`
   - If 0 commits: Error "No commits to rewrite. Branch is up to date with main."

4. **Identify main branch**: Check if `main` or `master` exists
   - Run `git rev-parse --verify main 2>/dev/null` and `git rev-parse --verify master 2>/dev/null`

### 2. Create Backup Branch

**Always create backup before destructive operations.**

```bash
git branch {current-branch}-backup-{YYYYMMDD-HHMM}
```

Report: "Created backup: {backup-branch-name}"

### 3. Analyze Commits

Gather information about all commits since divergence:

1. **Get merge-base**: `git merge-base HEAD {main-branch}`
2. **List commits**: `git log --oneline {merge-base}..HEAD`
3. **Get full diff**: `git diff {merge-base}..HEAD`
4. **Analyze repo commit style**: `git log --oneline -20` to identify message patterns

**Analysis goals**:
- Identify distinct concerns/features in the changes
- Group related changes together
- Determine logical ordering (dependencies, foundations before features)
- Match existing commit message style (Conventional Commits if no clear pattern)

### 4. Generate Proposal

Create a restructuring proposal:

```
Proposed restructuring ({N} commits -> {M} commits):

1. {type}({scope}): {description}
   - Groups: {what this commit combines}
   - Files: {key files affected}

2. {type}({scope}): {description}
   - Groups: {what this commit combines}
   - Files: {key files affected}

[...]
```

**Grouping principles**:
- One concern per commit
- Logical order: setup/config -> core features -> secondary features -> tests -> docs
- Atomic commits that could theoretically be reverted independently

### 5. Interactive Approval (unless --auto)

If `$ARGUMENTS` does NOT contain `--auto`:

Use AskUserQuestion to present proposal and get approval:

```
Proceed with this restructuring?
- [Yes] Execute as proposed
- [Adjust] Describe changes to the proposal
- [Cancel] Abort without changes
```

**If "Adjust"**: Parse user feedback, regenerate proposal, ask again.

**If "Cancel"**: Report "Cancelled. No changes made. Backup branch preserved: {backup-name}" and exit.

**If "Yes"** or `--auto` mode: Proceed to execution.

### 6. Execute Rewrite

Perform the history rewrite:

1. **Soft reset to merge-base**:
   ```bash
   git reset --soft {merge-base}
   ```
   This unstages all commits but keeps changes in working directory.

2. **Create new commits** for each group in the proposal:
   - Stage relevant files: `git add {files}`
   - Commit with new message: `git commit -m "{message}"`
   - Repeat for each logical commit

3. **Verify result**:
   - Run `git log --oneline {merge-base}..HEAD` to show new history
   - Run `git diff {backup-branch}..HEAD` to confirm no code changes (should be empty)

Report: "History rewritten: {old-count} commits -> {new-count} commits"

### 7. Push Prompt

After successful rewrite, prompt about pushing:

Use AskUserQuestion:
```
Push rewritten history to remote?
- [Yes] Push with --force-with-lease (safe force push)
- [No] Keep changes local (you can push manually later)
```

**If "Yes"**:
```bash
git push --force-with-lease
```
Report: "Pushed to remote with --force-with-lease"

**If "No"**:
Report: "Changes kept local. Push manually when ready: git push --force-with-lease"

### 8. Summary

Report final summary:

```
History rewrite complete.

Original: {N} commits
Rewritten: {M} commits
Backup: {backup-branch-name}

New history:
{git log --oneline output}
```

## Important Guidelines

- **Always use `--force-with-lease`** instead of `--force` for push safety
- **Backup branch is permanent** - only delete manually after confirming rewrite is correct
- **Verify no code changes** - diff between backup and new HEAD should be empty
- **Conventional Commits** - use if repo has no clear style (feat, fix, docs, refactor, test, chore)
- **One concern per commit** - resist urge to combine unrelated changes

## Edge Cases

| Scenario | Handling |
|----------|----------|
| On main/master branch | Error: "Cannot rewrite history on main/master branch. Checkout a feature branch first." |
| Uncommitted changes | Error: "Uncommitted changes detected. Commit or stash changes before rewriting history." |
| No commits since main | Error: "No commits to rewrite. Branch is up to date with main." |
| Single commit only | Proceed normally (may just improve commit message) |
| Merge commits in history | Warning: "Branch contains merge commits. Rewrite will linearize history." Proceed if user confirms. |
| Conflicts during commit creation | Should not occur (soft reset preserves all changes). If staging issues, report specific files. |
| Push rejected despite --force-with-lease | Error: "Push rejected. Remote has new commits. Fetch and review before retrying." |
| User cancels mid-execution | Backup branch preserved. User can: `git reset --hard {backup-branch}` to restore. |

## Example Usage

```bash
# Interactive mode (default)
/rewrite-history

# Automatic mode (skip proposal approval)
/rewrite-history --auto
```

## Example Output

**Interactive mode**:
```
Analyzing 23 commits since divergence from main...

Created backup: feature-auth-backup-20260107-1430

Proposed restructuring (23 commits -> 4 commits):

1. feat(auth): add JWT authentication middleware
   - Groups: middleware setup, token validation, error handling
   - Files: src/middleware/auth.ts, src/utils/jwt.ts

2. feat(auth): implement login and logout endpoints
   - Groups: login handler, logout handler, session management
   - Files: src/routes/auth.ts, src/controllers/auth.ts

3. test(auth): add authentication test suite
   - Groups: unit tests, integration tests
   - Files: tests/auth/*.test.ts

4. docs(auth): add authentication documentation
   - Groups: API docs, README updates
   - Files: docs/auth.md, README.md

Proceed with this restructuring?
- [Yes] Execute as proposed
- [Adjust] Describe changes to the proposal
- [Cancel] Abort without changes

> Yes

History rewritten: 23 commits -> 4 commits

Push rewritten history to remote?
- [Yes] Push with --force-with-lease
- [No] Keep changes local

> Yes

Pushed to remote with --force-with-lease

History rewrite complete.

Original: 23 commits
Rewritten: 4 commits
Backup: feature-auth-backup-20260107-1430

New history:
a1b2c3d docs(auth): add authentication documentation
e4f5g6h test(auth): add authentication test suite
i7j8k9l feat(auth): implement login and logout endpoints
m0n1o2p feat(auth): add JWT authentication middleware
```
