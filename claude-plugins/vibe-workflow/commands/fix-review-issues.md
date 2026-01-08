---
description: 'Orchestrate fixing issues found by /review. Handles issue discovery, user confirmation, plan creation, and execution via /implement.'
argument-hint: Optional - --severity critical,high --category <from-review>
---

**User request**: $ARGUMENTS

Systematically address issues found from `/review` runs. Orchestrates the multi-step workflow: discover issues, confirm scope with user, create fix plan, execute fixes, and verify.

## Workflow

### Phase 0: Parse Arguments

Parse `$ARGUMENTS` to determine scope:

| Argument | Effect |
|----------|--------|
| (none) | Fix ALL issues from review |
| `--severity <level>` | Filter by severity (critical, high, medium, low) |
| `--category <type>` | Filter by category (use categories found in review output) |
| File paths | Focus on specific files only |

Multiple filters combine: `--severity critical,high --category <cat1>,<cat2>`

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

Present multi-select with categories found in the review output (dynamically generated from Phase 1 parsing).

**If "Only specific files"**:

```
header: "Specify Files"
question: "Which files or directories should I focus on?"
freeText: true
placeholder: "e.g., src/auth/ or src/utils.ts, src/helpers.ts"
```

### Phase 3: Create Fix Plan

Use the Skill tool to create the implementation plan: Skill("vibe-workflow:plan", "Fix these review issues: [summary of issues within confirmed scope]")

Once the plan is approved, note the plan file path (typically `/tmp/plan-*.md`) and proceed to execution.

### Phase 4: Execute Fixes

Use the Skill tool to execute the plan: Skill("vibe-workflow:implement", "<plan-file-path>")

The `/implement` skill handles dependency-ordered execution, progress tracking, and auto-fixing gate failures.

### Phase 5: Next Steps

After `/implement` completes, ask the user:

```
header: "Fixes Complete"
question: "Implementation finished. What would you like to do next?"
options:
  - "Run /review again - verify fixes are complete (Recommended)"
  - "Show diff - see all changes made"
  - "Done - I'll verify manually"
```

## Key Principles

- **User Control**: Confirm scope before making changes
- **Reduce Cognitive Load**: Use AskUserQuestion for decisions, recommended option first