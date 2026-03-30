# Known Bot Identification

Rules for distinguishing bot-generated comments from human comments on PR reviews.

## Known Bot Accounts

| Bot | Identifier |
|-----|-----------|
| CodeRabbit | `coderabbitai[bot]` |
| Bugbot | `bugbot[bot]` |
| Dependabot | `dependabot[bot]` |
| Renovate | `renovate[bot]` |
| Cursor | `cursor[bot]` |
| GitHub Actions | `github-actions[bot]` |
| Copilot | `copilot[bot]` |

## Identification Rules

A comment author is a bot if **any** of the following are true:

1. Username ends with `[bot]`
2. Account type is `Bot` (GitHub API `type` field)
3. Username matches a known bot account from the table above
4. Comment is posted by a GitHub App (not a user)

If none of the above match, treat the author as human.

## Why It Matters

Bot and human comments follow the same classification flow (actionable / false-positive / uncertain) and the same reply-then-resolve pattern. The distinction matters for tone:

- **Bot replies**: Brief and factual. Bots don't read replies, so explanations are purely for human audit trail. Example: "Reviewed — false positive: change already exists in current code."
- **Human replies**: Respectful and explanatory. Humans will read and may respond. Example: "This was already addressed in commit abc123 — the function now uses const instead of let. Resolving this thread."
