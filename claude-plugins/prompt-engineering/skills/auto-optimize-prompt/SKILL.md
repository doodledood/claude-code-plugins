---
name: auto-optimize-prompt
description: 'Iteratively auto-optimize a prompt until no issues remain. Uses prompt-reviewer in a loop to find high-confidence issues, asks user for clarification on ambiguities, and applies fixes. Runs until converged.'
---

# Auto-Optimize Prompt

Iteratively optimize a prompt through automated review-fix cycles until no high-confidence issues remain.

**User request**: $ARGUMENTS

## Overview

This skill automates the prompt optimization loop:
1. **Review** - Launch prompt-reviewer agent to find HIGH-confidence issues only
2. **Triage** - Separate issues requiring human input from auto-fixable issues
3. **Clarify** - Ask user for missing context or ambiguity resolution
4. **Fix** - Apply fixes for all identified issues
5. **Repeat** - Loop until reviewer finds no high-confidence issues

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

Spawn prompt-reviewer agent via Task tool:
- **subagent_type**: "prompt-engineering:prompt-reviewer"
- **prompt**:
  ```
  Review this prompt file for issues: {working_path}

  CRITICAL: Only report HIGH-CONFIDENCE issues. Skip anything uncertain or marginal.

  High-confidence criteria:
  - Clear violation of prompt-engineering principles (WHAT/WHY not HOW)
  - Unambiguous anti-patterns (prescribing steps, arbitrary limits, capability instructions)
  - Definite clarity issues (multiple valid interpretations, vague language)
  - Obvious conflicts (contradictory rules, priority collisions)
  - Structural problems (buried critical info, no hierarchy)

  Do NOT report:
  - Style preferences
  - Minor wording improvements
  - Uncertain issues ("might be", "could potentially")
  - Low-severity items

  For each issue, indicate if it requires user input:
  - NEEDS_USER_INPUT: Ambiguity that only the author can resolve, missing domain context, unclear intent
  - AUTO_FIXABLE: Clear fix exists based on prompt-engineering principles
  ```

#### Step 1.2: Parse Reviewer Response

Parse the reviewer's report:
- **Assessment: Excellent Prompt** or **Score: 9-10/10 with no issues**: Exit loop, proceed to Output
- **Issues found**: Continue to Step 1.3

#### Step 1.3: Triage Issues

Separate issues into two lists:
1. **needs_user_input**: Issues marked NEEDS_USER_INPUT
2. **auto_fixable**: Issues marked AUTO_FIXABLE

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

1. **Load principles**: Reference prompt-engineering principles for fix approach
2. **Apply fix**: Edit working file to resolve the issue
3. **Log change**: Track what was changed for final report

**Fix approach by issue type**:

| Issue Type | Fix Strategy |
|------------|--------------|
| Prescribes HOW | Remove steps, state goal only |
| Arbitrary limits | Replace with principle ("until converged") |
| Capability instructions | Remove entirely |
| Vague language | Make direct ("try to" → "do") |
| Buried critical info | Move to prominent position |
| Contradictory rules | Resolve based on user input or remove weaker rule |
| Missing context | Add based on user clarification |

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
| **High-confidence only** | Reviewer reports only clear issues, not marginal improvements |
| **User-in-the-loop** | Ambiguities and missing context require human resolution |
| **Converge, don't cap** | No arbitrary iteration limits - run until no issues found |
| **Atomic output** | Original unchanged until optimization complete |
| **Principle-based fixes** | All fixes grounded in prompt-engineering principles |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No input provided | Ask: "Which prompt file should I optimize?" |
| File not found | Error with path |
| Already excellent | Report: "Prompt is already well-optimized. No high-confidence issues found." |
| User declines all clarifications | Proceed with auto-fixable issues only |
| Reviewer returns unexpected format | Retry once; if fails, ask user to review manually |
| Same issue persists across iterations | Ask user for guidance on how to resolve |

## Never Do

- Report low-confidence or uncertain issues
- Apply fixes without loading prompt-engineering principles first
- Skip asking user for genuinely ambiguous issues
- Set arbitrary iteration limits
- Modify original file until fully converged
