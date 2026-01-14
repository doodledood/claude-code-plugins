---
name: fix-review-issues
description: 'Orchestrate fixing issues found by /review. Handles issue discovery, user confirmation, plan creation, and execution via /implement.'
---

**User request**: $ARGUMENTS

Systematically address issues found from `/review` runs. Orchestrates: discover issues → confirm scope → plan → execute → verify.

**Flags**: `--autonomous` → skip Phase 2 scope confirmation and Phase 5 next-steps prompt (requires scope args)

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

### Phase 1.5: Validate Findings Against Plan/Spec

**Before confirming scope, check if findings conflict with the implementation plan or spec.**

Search for plan and spec files:
```bash
# Look for plan files
ls /tmp/plan-*.md 2>/dev/null | head -5
find . -name "plan-*.md" -o -name "PLAN.md" 2>/dev/null | head -5

# Look for spec files
ls /tmp/spec-*.md 2>/dev/null | head -5
find . -name "spec-*.md" -o -name "SPEC.md" -o -name "requirements*.md" 2>/dev/null | head -5
```

**If plan/spec files exist:**

1. Read the plan/spec files
2. For each review finding, check if it contradicts planned/specified behavior:
   - **Simplicity issues**: If the plan explicitly requires the pattern (e.g., "use factory pattern for extensibility"), REMOVE the finding
   - **Maintainability issues**: If the plan specifies the structure (e.g., "separate concerns into X files"), REMOVE findings that critique this
   - **Type safety issues**: If the spec requires the flexibility (e.g., "must accept arbitrary JSON"), REMOVE strict typing findings
3. Report filtered findings with explanation:
   ```
   ## Findings Filtered (Justified by Plan/Spec)

   The following issues were removed because they're justified by the implementation plan or spec:
   - [Issue]: Filtered because plan specifies "..."
   - [Issue]: Filtered because spec requires "..."
   ```

**Why this matters:** Review agents run without plan context. A "premature abstraction" finding may actually be an intentional pattern the plan required for future extensibility. Blindly fixing such issues would undo deliberate architectural decisions.

### Phase 2: Confirm Scope with User

**If `--autonomous` OR scope arguments provided** → skip Phase 2, proceed to Phase 3

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

**If `--autonomous`**: Skip prompt, end after implementation completes. Caller handles verification.

**Otherwise**, ask the user:

```
header: "Fixes Complete"
question: "Implementation finished. What would you like to do next?"
options:
  - "Run /review again - verify fixes are complete (Recommended)"
  - "Show diff - see all changes made"
  - "Done - I'll verify manually"
```

## Key Principles

- **Respect the Plan**: Filter out findings that contradict the implementation plan or spec—these are intentional decisions, not mistakes
- **User Control**: Confirm scope before making changes
- **Reduce Cognitive Load**: Use AskUserQuestion for decisions, recommended option first
- **High Confidence Only**: Only fix issues that are clearly unintentional problems, not design decisions