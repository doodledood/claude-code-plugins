---
name: auto-optimize-prompt
description: 'Iteratively auto-optimize a prompt until no issues remain. Uses prompt-reviewer in a loop to find high-confidence issues, asks user for clarification on ambiguities, and applies fixes. Runs until converged.'
---

# Auto-Optimize Prompt

Iteratively optimize a prompt through automated review-fix cycles until no high-confidence issues remain.

**User request**: $ARGUMENTS

## Overview

This skill automates the prompt optimization loop:
1. **Review** - Spawn prompt-reviewer agent (only reports high-confidence issues)
2. **Triage** - Separate NEEDS_USER_INPUT from AUTO_FIXABLE issues
3. **Clarify** - Ask user for missing context or ambiguity resolution
4. **Fix** - Invoke prompt-engineering skill to apply fixes
5. **Repeat** - Loop until reviewer finds no issues

**Key principle**: Only stop when converged. No arbitrary iteration limits.

## Workflow

### Phase 0: Input Validation

**Parse arguments**: Extract file path from `$ARGUMENTS`.

- **No path provided**: Ask user: "Which prompt file should I optimize?"
- **File not found**: Error: "File not found: {path}"
- **Unsupported type**: Error: "Unsupported file type. Supported: .md, .txt, .yaml"

**Read the file** and store original content.

**Create working copy**: Copy to `/tmp/auto-optimize-{timestamp}.{ext}` for iterations.

### Phase 1: Review Loop

Loop until no high-confidence issues found:

#### Step 1.1: Launch Reviewer

Spawn prompt-reviewer agent:
```
Review this prompt file: {working_path}
```

The agent only reports high-confidence issues and tags each as NEEDS_USER_INPUT or AUTO_FIXABLE.

#### Step 1.2: Parse Reviewer Response

- **Assessment: Excellent Prompt** or **no issues**: Exit loop → Phase 2
- **Issues found**: Continue to Step 1.3

#### Step 1.3: Triage Issues

Separate issues by tag:
1. **needs_user_input**: Issues tagged NEEDS_USER_INPUT
2. **auto_fixable**: Issues tagged AUTO_FIXABLE

#### Step 1.4: Resolve User-Input Issues

For each issue in `needs_user_input`:

Ask user with clear context:
```
The prompt has an ambiguity I can't resolve without your input:

**Issue**: {issue description}
**Location**: {line/section}
**Current text**: "{exact quote}"

**Question**: {specific question to resolve ambiguity}

Options:
1. {option A}
2. {option B}
3. Tell me your intent so I can fix it appropriately
```

Wait for user response. Store resolution for fix phase.

**If user declines to answer**: Skip this issue with note: "Skipped per user preference"

#### Step 1.5: Apply Fixes

For each issue (both auto-fixable and user-resolved):

Invoke `prompt-engineering:prompt-engineering` with:
```
Update the prompt at {working_path}

Fix this issue: {issue description}
Location: {line/section}
Current text: "{exact quote}"
{If user-resolved: User clarification: {user response}}

Apply the fix following prompt-engineering principles.
```

The prompt-engineering skill contains the fix strategies (WHAT/WHY not HOW, remove arbitrary limits, etc.). Don't duplicate that logic here.

#### Step 1.6: Re-verify

Return to Step 1.1 with updated working file.

**Convergence**: Loop exits when reviewer finds no high-confidence issues.

### Phase 2: Output

**Calculate changes**:
- Count total iterations
- Count issues fixed (auto + user-resolved)
- Count issues skipped

**Apply changes atomically**:
```bash
cp {working_path} {original_path}
```

**Report results**:
```
Auto-optimized: {path}
Iterations: {count}
Issues fixed: {count}
  - Auto-fixed: {count}
  - User-resolved: {count}
Issues skipped: {count} (user declined)

Changes applied:
- {summary of each fix}

Status: Converged - no high-confidence issues remain
```

## Key Principles

| Principle | Rule |
|-----------|------|
| **High-confidence only** | Reviewer only reports definite issues (low-confidence = noise) |
| **User-in-the-loop** | NEEDS_USER_INPUT issues require human resolution |
| **Converge, don't cap** | No arbitrary iteration limits - run until no issues found |
| **Atomic output** | Original unchanged until optimization complete |
| **DRY** | Delegate to prompt-reviewer for review, prompt-engineering for fixes |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No input provided | Ask: "Which prompt file should I optimize?" |
| File not found | Error with path |
| Already excellent | Report: "Prompt is already well-optimized. No high-confidence issues found." |
| User declines all clarifications | Proceed with auto-fixable issues only |
| Same issue persists across iterations | Ask user for guidance on how to resolve |

## Never Do

- Duplicate prompt-engineering principles or fix strategies
- Skip asking user for NEEDS_USER_INPUT issues
- Set arbitrary iteration limits
- Modify original file until fully converged
