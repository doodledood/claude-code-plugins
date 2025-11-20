# Oracle Review Command

Comprehensive PR review using the oracle CLI tool through the oracle-consulter agent for high-token analysis and deep reasoning across full diffs.

## What This Does

Invokes the **oracle-consulter agent** to perform production-level code review with:

- Severity-tagged findings (blocker, high, medium, low, info)
- Regression test guidance
- Security and architectural validation
- Actionable recommendations with file references

## Inputs (All Optional with Smart Defaults)

| Key      | Default Inference Strategy             | Example                               | Notes                                         |
| -------- | -------------------------------------- | ------------------------------------- | --------------------------------------------- |
| `PR_REF` | `origin/master...HEAD`                 | `origin/master...feature/agent-audit` | Commit range/PR branch for `git diff`         |
| `PR_URL` | Infer from git remote + current branch | `https://github.com/.../pull/1234`    | Gives oracle direct context                   |
| `FOCUS`  | Empty (no special focus)               | `ensure auth interceptors unchanged`  | Extra reviewer hints, deadlines, rollout info |

Pass overrides via `$ARGUMENTS` below if needed.

## Default Behavior

When invoked without arguments, the command will:

1. **Determine PR_REF**: Use `origin/master...HEAD` (current branch vs master)
2. **Attempt to infer PR_URL**: Extract from git remote and current branch, or use `gh pr view --json url` if available
3. **Use empty FOCUS**: No special focus unless specified

## Usage

**Step 1: Infer git context (run these in parallel):**

- Get current branch: `git branch --show-current`
- Get git remote: `git remote get-url origin`
- Try to find PR: `gh pr view --json url -q .url 2>/dev/null || echo ""`

**Step 2: Parse $ARGUMENTS if provided** to override defaults:

- If $ARGUMENTS contains `PR_REF=...`, use that instead of `origin/master...HEAD`
- If $ARGUMENTS contains `PR_URL=...`, use that instead of inferred URL
- If $ARGUMENTS contains `FOCUS=...`, use that instead of empty focus

**Step 3: Invoke oracle-consulter agent** with the following prompt:

```
Please review the PR with the following details:
- PR reference: {{PR_REF}} (default: origin/master...HEAD)
- PR URL: {{PR_URL}} (if inferred or provided)
- Special focus areas: {{FOCUS}} (if provided, otherwise general review)

Perform a comprehensive production-level review covering:
1. Behavioral correctness & regression risk
2. Security/auth/data validation
3. Error handling & edge cases
4. Performance impact
5. Test completeness
6. Prompt quality (if applicable): no conflicting instructions, coherent with code changes, clear, well-balanced across objectives, no unnecessary overfitting

Provide severity-tagged findings with file references, suggested fixes, and regression test recommendations.
```

## What the Agent Will Do

The oracle-consulter agent will automatically:

1. Fetch latest refs and analyze the diff scope
2. Classify files by category (core logic, schemas/types, tests, infrastructure)
3. Create timestamped temp directory with organized, numbered diff bundles
4. Construct comprehensive review prompt with focus areas
5. Invoke oracle via `npx -y @steipete/oracle@latest` directly via Bash with structured attachments
6. Monitor session continuously (30s intervals) until completion
7. Synthesize findings into actionable recommendations with severity tags

## Expected Output from Oracle

Oracle will provide severity-tagged findings or confirmation of clean review. The output format should be:

### When Issues Are Found

**Format for each finding:**

```
[Severity] Issue Title

File: path/to/file.ts:123-145
Issue: Clear description of the problem, why it matters, and potential impact
Suggested fix: Specific recommendation or validation steps to resolve
Missing test: Regression test scenario to prevent this issue (if applicable)
```

**Severity levels:**

- **[BLOCKER]** - Production-breaking, must fix before merge
- **[HIGH]** - Significant risk, security concern, or major correctness issue
- **[MEDIUM]** - Important improvement, potential edge case, maintainability concern
- **[LOW]** - Minor improvement, style suggestion, optimization opportunity
- **[INFO]** - Observation, context, or informational note

**Grouping and summary:**

```
## Must-Fix Checklist (Blockers + High)
- [ ] [BLOCKER] Issue title (file.ts:123)
- [ ] [HIGH] Issue title (other.ts:456)

## Follow-Up Items (Medium + Low)
- [MEDIUM] Issue title (helper.ts:789)
- [LOW] Issue title (util.ts:234)

## Regression Test Recommendations
- Test scenario 1: When X happens, verify Y behavior
- Test scenario 2: Edge case with Z input should handle gracefully

## Overall Risk Assessment
Brief summary of production readiness, blast radius, and confidence level.
```

### When No Issues Found

```
## No Problems Found

Reviewed the following areas:
- Core logic changes: [brief summary of what was checked]
- Type definitions: [confirmation of type safety]
- Test coverage: [validation of test completeness]
- Error handling: [verification of edge case coverage]
- Security/auth: [confirmation of no security regressions]
- [Prompts: coherence and balance confirmed] (if applicable)

The PR is production-ready with no blocking concerns.
```

### Special Cases

**Prompt evaluation findings** (when applicable):

```
[MEDIUM] Prompt Instructions May Conflict

File: apps/cxllm/src/prompts/customer-service.ts:45-67
Issue: Instructions for "always be concise" conflict with "provide detailed explanations"
Suggested fix: Clarify intent - perhaps "be concise unless user requests details"
Context: This could lead to inconsistent behavior depending on which instruction the model prioritizes
```

**Architectural concerns:**

```
[HIGH] Missing Rollback Path for Migration

File: apps/cxllm/migrations/20250119-add-index.ts
Issue: Database migration adds index but no down() method to remove it
Suggested fix: Implement down() method to drop index for safe rollback
Missing test: Integration test verifying migration can be rolled back cleanly
```

### Quality Indicators

Oracle's output should demonstrate:

- ✅ **Specific file references**: Line numbers, not vague "somewhere in X"
- ✅ **Clear issue descriptions**: Why it matters, not just what's wrong
- ✅ **Actionable suggestions**: Concrete fixes, not "review this"
- ✅ **Test guidance**: Specific regression test scenarios
- ✅ **Proper severity**: Blockers are truly production-breaking
- ✅ **Balanced perspective**: Not overly conservative or permissive

## Extra User Instructions

$ARGUMENTS
