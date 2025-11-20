# Oracle Bug Investigation Command

Deep bug investigation and root cause analysis using the oracle CLI tool through the oracle-consulter agent for comprehensive reasoning across error traces, logs, and related code.

## What This Does

Invokes the **oracle-consulter agent** to perform thorough bug investigation with:

- Root cause identification through deep code analysis
- Execution flow tracing from symptom to source
- Impact assessment and blast radius analysis
- Concrete fix suggestions with implementation guidance
- Regression test recommendations to prevent recurrence

## Inputs with Smart Defaults

| Key        | Default Inference Strategy                     | Example                                   | Notes                                               |
| ---------- | ---------------------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| `BUG`      | Infer from test failures or user message       | `API returns 500 on user profile update`  | Brief description of the bug/issue                  |
| `SYMPTOMS` | Infer from recent test output or error logs    | `Error: Cannot read property 'id'...`     | Observable symptoms: error messages, logs, behavior |
| `REPRO`    | Empty (will be inferred during investigation)  | `Steps: 1. Login 2. Update email 3. Save` | How to reproduce the issue                          |
| `CONTEXT`  | Infer from recent commits and git status       | `Started after migration deployment`      | When it started, affected environments, users       |
| `LOGS`     | Gather from recent test failures or user input | `[Error trace or log excerpt]`            | Relevant error traces, stack traces, log messages   |

Pass overrides via `$ARGUMENTS` below if needed.

## Default Behavior

When invoked without explicit arguments, the command will:

1. **Infer BUG**:

   - Extract from user's most recent message
   - Look for test failure messages in recent output
   - Look for error descriptions in conversation
   - If unclear, ask user for clarification

2. **Infer SYMPTOMS**:

   - Extract error messages from user's message
   - Parse recent test failure output
   - Look for stack traces or error logs in conversation
   - If unclear, ask user for clarification

3. **Infer REPRO**:

   - Default to empty (oracle will attempt to determine during investigation)
   - Can be inferred from explicit user mentions

4. **Infer CONTEXT**:

   - Gather from `git log -10 --oneline` (recent changes)
   - Check `git status` for current state
   - Look for temporal context in user message ("started after...", "since...")
   - Default to empty if no relevant context

5. **Infer LOGS**:
   - Extract from user's message if present
   - Look for stack traces, error messages, or log excerpts in conversation
   - Default to empty (oracle will work with available information)

## Usage

**Step 1: Gather context (run these in parallel if needed):**

- Check recent commits: `git log -10 --oneline`
- Check current state: `git status --short`
- Parse user message for error traces, stack traces, and symptoms

**Step 2: Parse $ARGUMENTS and user message** to determine:

- BUG (from arguments or user message)
- SYMPTOMS (from arguments, user message, or test output)
- REPRO (from arguments or default to empty)
- CONTEXT (from arguments, git history, or user message)
- LOGS (from arguments or user message)

**Step 3: If BUG or SYMPTOMS unclear**, ask user:

```
I need more information to investigate this bug:
1. What is the bug or issue you're experiencing? (brief description)
2. What are the observable symptoms? (error messages, unexpected behavior, etc.)

Optional (helps with investigation):
- Reproduction steps (if known)
- When this started or what changed
- Any error logs or stack traces you have
```

**Step 4: Invoke oracle-consulter agent** with the following prompt:

```
Please investigate the following bug and identify its root cause:

Bug: {{BUG}}
Symptoms: {{SYMPTOMS}}
Reproduction: {{REPRO}} (if provided, otherwise will be determined during investigation)
Context: {{CONTEXT}} (if inferred or provided)
Error logs/traces: {{LOGS}} (if provided)

Perform comprehensive bug investigation including:
1. Root cause analysis - Trace from symptoms to source
2. Execution flow analysis - How the error propagates through the system
3. Related code examination - All files and dependencies involved
4. Impact assessment - What else might be affected
5. Fix recommendations - Concrete solutions with implementation guidance
6. Prevention strategies - Tests and safeguards to prevent recurrence

Gather comprehensive context:
- Files mentioned in error traces/stack traces (full files + diffs if recently changed)
- Related services, controllers, handlers involved in execution path
- Type definitions, interfaces, schemas used by affected code
- Database queries, migrations that might be relevant
- Configuration files affecting the behavior
- Test files covering (or missing coverage for) the affected area
- Related unchanged files that provide execution context

Provide detailed analysis with specific file references, line numbers, and actionable fix suggestions.
```

## What the Agent Will Do

The oracle-consulter agent will automatically:

1. Parse error messages and stack traces to identify affected files
2. Gather comprehensive context (full files, diffs, related imports, configs)
3. Trace execution flow from entry point to error location
4. Analyze related code that might contribute to the issue
5. Create timestamped temp directory with organized, numbered attachments
6. Construct detailed investigation prompt with focus on root cause
7. Invoke oracle via `npx -y @steipete/oracle@latest` directly via Bash with extensive context
8. Monitor session continuously (30s intervals) until completion
9. Synthesize findings into root cause analysis with fix recommendations

## Expected Output from Oracle

Oracle will provide comprehensive bug analysis with root cause identification and fix recommendations. The output format should be:

### Root Cause Analysis

```
## Root Cause Identified

**Primary Issue:** [Clear statement of what's actually wrong]

**File:** path/to/file.ts:line-range
**Function/Method:** functionName()

**Explanation:**
[Detailed explanation of why the bug occurs, including:]
- What the code is trying to do
- What assumption was violated
- How the error manifests
- Why existing safeguards didn't catch it

**Execution Flow:**
1. Entry point: [where request/execution starts]
2. Through: [intermediate steps and function calls]
3. Error triggered at: [exact location where failure occurs]
4. Propagated as: [how error surfaces to user/logs]
```

### Contributing Factors

```
## Contributing Factors

**Secondary Issues:** (if applicable)

1. [Factor 1 - e.g., Missing validation]
   File: path/to/file.ts:lines
   Issue: [Explanation]

2. [Factor 2 - e.g., Race condition]
   File: path/to/file.ts:lines
   Issue: [Explanation]

**Root Enablers:** (underlying conditions that allowed the bug)
- Missing type checking in [location]
- Unchecked null/undefined in [location]
- Missing error handling in [location]
```

### Impact Assessment

```
## Impact Assessment

**Blast Radius:**
- Affected endpoints: [list]
- Affected user actions: [list]
- Affected environments: [production/staging/all]

**Severity:** [CRITICAL / HIGH / MEDIUM / LOW]
- User impact: [description]
- Data risk: [description]
- Frequency: [always / intermittent / edge case]

**Related Issues:** (other bugs that might stem from same root cause)
- [Related issue 1 - with file reference]
- [Related issue 2 - with file reference]
```

### Fix Recommendations

```
## Recommended Fixes

### Primary Fix (Required)

**Approach:** [Strategy - e.g., Add null check, Fix race condition, Correct validation]

**Implementation:**
File: path/to/file.ts:line-range

Specific changes:
1. [Change 1 with code snippet or clear description]
2. [Change 2 with code snippet or clear description]
3. [Change 3 with code snippet or clear description]

**Why this fixes it:** [Explanation of how this addresses root cause]

**Potential risks:** [Any side effects or considerations]

### Secondary Fixes (Optional but Recommended)

1. **[Fix name - e.g., Add defensive programming]**
   File: path/to/file.ts:lines
   What: [Description]
   Why: [Prevents related issues]

2. **[Fix name - e.g., Improve error handling]**
   File: path/to/file.ts:lines
   What: [Description]
   Why: [Better debugging/recovery]
```

### Test Recommendations

```
## Regression Test Strategy

**Required Tests:** (to prevent this specific bug)

1. **Test: [Test name describing scenario]**
   Purpose: Verify [specific condition that triggered bug]
   Setup: [Test data/state needed]
   Execute: [Actions to perform]
   Assert: [Expected behavior]
   File: path/to/file.test.ts (new or existing)

2. **Test: [Edge case test name]**
   Purpose: Verify [related edge case]
   Setup: [Test setup]
   Execute: [Actions]
   Assert: [Expectations]

**Coverage Gaps:** (broader testing improvements)
- Missing integration test for [scenario]
- Missing edge case coverage for [condition]
- Missing error path testing for [operation]
```

### Prevention Strategies

```
## Prevention Strategies

**Immediate:**
- Add type guards at [locations]
- Add error handling at [locations]
- Add validation at [locations]

**Short-term:**
- Review similar patterns in [related files]
- Add lint rules to catch [this pattern]
- Update team guidelines about [practice]

**Long-term:**
- Consider architectural change: [suggestion]
- Add monitoring/alerting for [metric]
- Improve observability in [area]
```

### When No Root Cause Found

```
## Investigation Results

Unable to identify definitive root cause with current information.

**Findings:**
- Analyzed: [list of files/areas examined]
- Ruled out: [list of potential causes investigated and eliminated]
- Unclear: [list of ambiguities or insufficient information]

**Next Steps for Investigation:**
1. [Additional information needed - e.g., production logs from timeframe X]
2. [Additional reproduction steps - e.g., specific user data or state]
3. [Additional monitoring - e.g., add logging at locations X, Y, Z]

**Hypotheses to Test:**
1. [Hypothesis 1 with testing approach]
2. [Hypothesis 2 with testing approach]
```

### Quality Indicators

Oracle's bug investigation should demonstrate:

- ✅ **Specific root cause**: Exact file, line, and explanation (not "investigate further")
- ✅ **Execution flow**: Clear trace from entry to error
- ✅ **Concrete fixes**: Actionable implementation steps, not vague suggestions
- ✅ **Test guidance**: Specific regression tests to write
- ✅ **Impact awareness**: Blast radius and severity assessment
- ✅ **Prevention focus**: How to avoid similar bugs in future

## Extra User Instructions

$ARGUMENTS
