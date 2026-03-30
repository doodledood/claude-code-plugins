# Comment Classification Examples

Concrete examples for classifying PR review comments. Use these as calibration — real comments will vary.

## Actionable

**Example 1 — Missing null check**
> Comment: "This will throw if `user` is null. Add a null check before accessing `user.name`."
>
> Code: `const name = user.name;` (no null check)
>
> Classification: **Actionable** — real bug, clear fix, low risk.

**Example 2 — Typo in error message**
> Comment: "Typo: 'authenication' should be 'authentication'"
>
> Code: `throw new Error("authenication failed")`
>
> Classification: **Actionable** — clear fix, zero risk.

**Example 3 — Missing await**
> Comment: "This async function isn't being awaited. Could cause a race condition."
>
> Code: `fetchUserData(id);` (missing `await`)
>
> Classification: **Actionable** — real bug, clear fix.

## False Positive

**Example 1 — Outdated (already fixed)**
> Comment: "You should use `const` instead of `let` here."
>
> Code (current): `const config = loadConfig();` (already uses `const`)
>
> Classification: **False positive (outdated)** — the change was already made in a subsequent commit.

**Example 2 — Misread code**
> Comment: "This function doesn't handle the error case."
>
> Code: Function has a try-catch block that handles errors, but the reviewer missed the catch block further down.
>
> Classification: **False positive (misread code)** — the error handling exists; comment's premise is wrong.

**Example 3 — Style preference**
> Comment: "I'd prefer using a ternary here instead of if/else."
>
> Code: Standard if/else block, functionally correct, readable.
>
> Classification: **False positive (style preference)** — no functional or readability improvement.

**Example 4 — Resolved in thread**
> Comment: "Should we add rate limiting here?"
> Reply from author: "Good point, I've added it in the middleware layer instead — see commit abc123."
> Reviewer reply: "Ah, that works. Thanks!"
>
> Classification: **False positive (resolved in thread)** — the discussion concluded with resolution.

## Uncertain

**Example 1 — Core logic change needed**
> Comment: "This auth flow should use the new OAuth2 handler instead of the legacy session-based auth."
>
> Classification: **Uncertain** — may be valid, but the fix requires significant refactoring of core authentication logic. Too risky for autonomous fixing.

**Example 2 — Ambiguous intent**
> Comment: "This doesn't feel right."
>
> Classification: **Uncertain** — no specific issue identified, no clear fix possible. Needs human clarification.

**Example 3 — Unresolved sub-discussion**
> Comment: "We should add caching here."
> Reply: "What cache TTL do you suggest?"
> (No further replies)
>
> Classification: **Uncertain** — thread has an unanswered question. The discussion isn't concluded.

**Example 4 — Risky fix**
> Comment: "This database query should use a transaction to prevent partial writes."
>
> Classification: **Uncertain** — likely valid, but wrapping in a transaction touches data integrity logic and could introduce deadlocks if done wrong. Needs human review.
