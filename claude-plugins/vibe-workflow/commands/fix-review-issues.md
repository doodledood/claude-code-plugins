---
description: 'Orchestrate fixing issues found by /review. Handles issue discovery, user confirmation, prioritized execution, and progress tracking. Works with review output from any category (bugs, maintainability, types, docs, coverage, claude-md).'
argument-hint: Optional - --severity critical,high --category bugs,types
---

**User request**: $ARGUMENTS

Systematically address issues found from `/review` runs. Orchestrates the multi-step workflow: discover issues, confirm scope with user, create fix plan, execute fixes, and verify.

## Categories

This skill supports fixing issues from any review category:
- **bugs** - Logical bugs, race conditions, edge cases
- **maintainability** - DRY violations, dead code, complexity
- **types** - Type safety issues (any abuse, missing narrowing)
- **docs** - Documentation and comment inaccuracies
- **coverage** - Missing test coverage
- **claude-md** - CLAUDE.md compliance violations

## Workflow

### Phase 0: Parse Arguments

Parse `$ARGUMENTS` to determine scope:

| Argument | Effect |
|----------|--------|
| (none) | Fix ALL issues from review |
| `--severity <level>` | Filter by severity (critical, high, medium, low) |
| `--category <type>` | Filter by category (bugs, maintainability, types, docs, coverage, claude-md) |
| File paths | Focus on specific files only |

Multiple filters combine: `--severity critical,high --category bugs,types`

### Phase 1: Discover Review Results

**Step 1**: Check if review results exist in the current conversation context.

**Step 2**: If NO review results found, ask the user:

```
header: "No Review Results Found"
question: "I couldn't find recent /review output in this conversation. What would you like to do?"
options:
  - "Run /review now - perform a fresh review first"
  - "Paste review output - I'll provide the review results"
  - "Cancel - I'll run /review myself first"
```

- If "Run /review now": Inform user to run `/review` first, then return to `/fix-review-issues`
- If "Paste review output": Wait for user to provide the review results
- If "Cancel": End the workflow

**Step 3**: If review results ARE found, extract and categorize all issues:

1. Parse each issue for: severity, category, file path, line number, description, suggested fix
2. Group issues by category
3. Count totals by severity

### Phase 2: Confirm Scope with User

**If arguments were provided** → skip Phase 2, proceed directly to Phase 3 (user already chose scope)

**If NO arguments** (fix all):

```
header: "Review Issues Summary"
question: "Found {N} total issues from the review. What would you like to fix?"
[Display: Issue breakdown by category and severity]
options:
  - "Fix all issues (Recommended)"
  - "Only critical and high severity"
  - "Only specific categories - let me choose"
  - "Only specific files - let me specify"
```

**If "Only specific categories"**:

```
header: "Select Categories"
question: "Which categories should I fix?"
options:
  - "bugs - Logical bugs, race conditions, edge cases"
  - "maintainability - DRY violations, dead code, complexity"
  - "types - Type safety issues"
  - "docs - Documentation inaccuracies"
  - "coverage - Missing test coverage"
  - "claude-md - CLAUDE.md compliance violations"
multiSelect: true
```

**If "Only specific files"**:

```
header: "Specify Files"
question: "Which files or directories should I focus on?"
freeText: true
placeholder: "e.g., src/auth/ or src/utils.ts, src/helpers.ts"
```

### Phase 3: Create Fix Plan

Use the Skill tool to create the implementation plan: Skill("vibe-workflow:plan", "Fix these review issues: [summary of issues within confirmed scope]")

Once the plan is approved, proceed to execution.

### Phase 4: Execute Fixes

For each fix group in the approved plan:

**Step 1: Mark Progress**
- Update todo list with current fix group
- Track: which issues fixed, which remaining

**Step 2: Read Context**
- Read the full file(s) involved
- Understand surrounding code before making changes

**Step 3: Apply Fix**
- Follow the suggested fix from the review
- Adapt as needed based on actual code context

**Step 4: Verify**
- Ensure the fix doesn't break surrounding code
- Check for introduced issues (syntax errors, type errors)

**Step 5: Confirm Significant Changes**

For fixes marked as "significant" effort or that touch multiple files:

```
header: "Significant Change"
question: "This fix involves substantial changes. Review before continuing?"
[Display: Summary of changes made]
options:
  - "Continue - changes look good (Recommended)"
  - "Undo - revert this fix"
  - "Pause - I need to review more carefully"
```

### Category-Specific Guidance

**Bugs** (`bugs`):
- Fix the root cause, not just the symptom
- Add defensive checks where appropriate
- Consider edge cases the fix might introduce

**Maintainability** (`maintainability`):
- Extract duplicated code into shared utilities
- Remove dead code completely (don't comment out)
- Simplify complex conditionals

**Types** (`types`):
- Replace `any` with proper types
- Add discriminated unions for state machines
- Use branded types for IDs where suggested
- Add exhaustiveness checks to switch statements

**Docs** (`docs`):
- Update documentation to match current code behavior
- Fix or remove stale comments
- Ensure examples are accurate and runnable

**Coverage** (`coverage`):
- Create test files if missing
- Add test cases for uncovered scenarios
- Follow existing test patterns in the codebase

**CLAUDE.md** (`claude-md`):
- Fix naming convention violations
- Add missing version bumps
- Follow project-specific patterns

### Phase 5: Summary

After all fixes complete, provide:

```
header: "Fix Summary"
[Display:
  - Count of issues fixed by category
  - Any issues that couldn't be fixed (with explanation)
  - Files modified
]
question: "Would you like to verify the fixes?"
options:
  - "Run /review again - verify fixes are complete (Recommended)"
  - "Done - I'll verify manually"
  - "Show diff - see all changes made"
```

## Key Principles

### User Control
- Always confirm scope before making changes
- Present plan for approval before executing
- Allow modification or cancellation at any step

### Progress Tracking
- Use todo list to track fix progress
- Mark each fix group as in_progress/completed
- Maintain visibility into remaining work

### Reduce Cognitive Load
- Use AskUserQuestion for all decisions
- Put recommended option first with "(Recommended)" suffix
- Group related fixes to minimize context switching

### Safe Execution
- Read full file context before editing
- Verify each fix doesn't break surrounding code
- Confirm significant changes before proceeding

## Integration with /review

This skill is designed to work with output from the `/review` command, which runs these agents:
- `code-bugs-reviewer`
- `code-maintainability-reviewer`
- `type-safety-reviewer`
- `docs-reviewer`
- `code-coverage-reviewer`
- `claude-md-adherence-reviewer`

The review output follows a consistent format with severity levels and suggested fixes that this skill parses and acts upon.
