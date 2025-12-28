---
description: Address issues found by /review. Fixes all issues by default, or filter by severity/category/file.
allowed-tools: ["Task", "Read", "Edit", "Write", "Glob", "Grep", "Bash", "TodoWrite"]
argument-hint: [--severity critical|high, --category bugs|maintainability|types|docs|coverage|claude-md, file paths]
---

Address issues found from a recent `/review` run. This command systematically fixes identified problems.

## Arguments

$ARGUMENTS

Parse arguments to determine scope:

- **No arguments**: Fix ALL issues from the review (all severities, all categories)
- **--severity <level>**: Focus on specific severity (critical, high, medium, low, or combinations like "critical,high")
- **--category <type>**: Focus on specific category:
  - `bugs` - Logical bugs, race conditions, edge cases
  - `maintainability` - DRY violations, dead code, complexity
  - `types` - Type safety issues (any abuse, missing narrowing)
  - `docs` - Documentation and comment inaccuracies
  - `coverage` - Missing test coverage
  - `claude-md` - CLAUDE.md compliance violations
- **File paths**: Focus on specific files only

Multiple filters can be combined: `--severity critical,high --category bugs,types`

## Process

### Step 1: Recall Review Results

If the review was run in this conversation, use those results. Otherwise, ask the user to run `/review` first or provide the review output.

### Step 2: Create Fix Plan with Plan Agent

**Use the Plan agent (Task tool with subagent_type=Plan, model=opus)** to design an implementation plan for fixing the issues. The plan should:

1. Analyze all issues from the review within the filter scope
2. Group related fixes (same file, same module, interdependent changes)
3. Identify the optimal fix order considering dependencies
4. Flag any fixes that might conflict or need careful coordination
5. Estimate effort (quick win vs moderate vs significant)

Present the plan to the user for approval before proceeding.

### Step 3: Execute Fixes (after plan approval)

For each issue:

1. **Read the full file** - Understand context before making changes
2. **Apply the fix** - Follow the suggested fix from the review, adapting as needed
3. **Verify** - Ensure the fix doesn't break surrounding code
4. **Mark complete** - Update todo list

### Category-Specific Guidance

**Bugs** (`--category bugs`):
- Fix the root cause, not just the symptom
- Add defensive checks where appropriate
- Consider edge cases the fix might introduce

**Maintainability** (`--category maintainability`):
- Extract duplicated code into shared utilities
- Remove dead code completely (don't comment out)
- Simplify complex conditionals

**Types** (`--category types`):
- Replace `any` with proper types
- Add discriminated unions for state machines
- Use branded types for IDs where suggested
- Add exhaustiveness checks to switch statements

**Docs** (`--category docs`):
- Update documentation to match current code behavior
- Fix or remove stale comments
- Ensure examples are accurate and runnable

**Coverage** (`--category coverage`):
- Create test files if missing
- Add test cases for uncovered scenarios
- Follow existing test patterns in the codebase

**CLAUDE.md** (`--category claude-md`):
- Fix naming convention violations
- Add missing version bumps
- Follow project-specific patterns

### Step 4: Summary

After fixing issues, provide:
- Count of issues fixed by category
- Any issues that couldn't be fixed (with explanation)
- Suggestion to re-run `/review` to verify fixes

## Example Usage

```
/fix-review-issues                           # Fix everything
/fix-review-issues --severity critical,high  # Only critical and high severity
/fix-review-issues --category bugs           # Only bug fixes
/fix-review-issues --category types,docs     # Types and docs only
/fix-review-issues src/auth/                 # Only files in src/auth/
/fix-review-issues --severity high --category maintainability src/utils.ts
```
