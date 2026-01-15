---
name: optimize-prompt-goal
description: 'Optimizes prompts for goal effectiveness - ensures instructions serve the stated goal, prevents missteps, improves efficiency. Use when asked to optimize a prompt for its goal, improve goal alignment, or make a prompt more effective at achieving its purpose.'
---

# Optimize Prompt Goal

Iteratively optimize prompt for goal effectiveness through analysis and verification loops. Primary goal: ensure prompt achieves its stated mission effectively and efficiently.

## Overview

This skill transforms goal-misaligned prompts into effective ones through:
1. **Goal Inference** - Extract or infer the prompt's goal/mission
2. **Analysis** - Identify goal optimization issues (misalignment, misstep risks, inefficiencies)
3. **Optimization** - Apply targeted fixes
4. **Verification** - `prompt-goal-verifier` agent checks for remaining issues
5. **Iteration** - If issues found, optimize again (max 5x)
6. **Output** - Atomic replacement only after verification passes

**Loop**: Read → Infer Goal → Optimize → Verify → (Iterate if issues) → Output

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases. List reflects areas of work, not fixed steps.

**Starter todos**:
```
- [ ] Input validation
- [ ] Goal inference and initial analysis
- [ ] Optimization iteration 1
- [ ] (expand if verification fails: iteration 2, 3...)
- [ ] Output optimized prompt
```

### Phase 1: Input Validation

**Mark "Input validation" todo `in_progress`.**

**Step 1.1: Parse arguments**

Extract input from `$ARGUMENTS`. Determine if file path or inline prompt.

**Step 1.2: Handle input type**

| Input Type | Detection | Action |
|------------|-----------|--------|
| File path | Starts with `/`, `./`, `~`, or ends with `.md`, `.txt`, `.yaml` | Read file content |
| Inline prompt | Everything else | Write to `/tmp/prompt-{timestamp}.md` |

**Step 1.3: Validate content**

- If file path: Check file exists using Read tool
- If inline: Write to temp file, note original was inline
- Error if no input provided: "Usage: /optimize-prompt-goal <file-path> OR /optimize-prompt-goal <inline prompt text>"

**Step 1.4: Store metadata**

- `original_path`: Source file path (or temp path for inline)
- `is_inline`: Boolean (affects output messaging)
- `original_content`: Full prompt text
- `working_path`: `/tmp/optimized-{timestamp}.md` for iterations

**Mark "Input validation" todo `completed`.**

### Phase 2: Initial Analysis with Goal Inference

**Mark "Goal inference and initial analysis" todo `in_progress`.**

**Step 2.1: Read and understand prompt**

Read the prompt and understand its structure:
1. **Structure**: How is it organized? (sections, rules, examples, workflow)
2. **Instructions**: What actions/behaviors does it specify?
3. **Constraints**: What limitations or rules does it impose?

**Step 2.2: Infer goal**

Extract the prompt's goal using this hierarchy:

1. **Explicit goal** - Look for "Goal:", "Purpose:", "Mission:", "Objective:" sections
   - Use verbatim if found

2. **Inferred from structure** - If no explicit goal:
   - What is this prompt trying to accomplish?
   - What outcomes does it optimize for?
   - What would success look like?

3. **Best-effort** - If still unclear:
   - Use `[INFERRED WITH LOW CONFIDENCE: {goal}]`
   - Proceed with best-effort inference

**Step 2.3: Display inferred goal**

Show user what goal was detected. Proceed immediately (no wait for confirmation).

```
Inferred Goal: {goal statement}
Proceeding with optimization...
```

**Step 2.4: Initial assessment**

Document:
- Goal clarity (explicit/inferred/low-confidence)
- Obvious issues visible at first read
- Areas likely to need optimization

**Mark "Goal inference and initial analysis" todo `completed`.**

### Phase 3: Optimization Loop

**Mark "Optimization iteration 1" todo `in_progress`.**

```
iteration = 1
max_iterations = 5

while iteration <= max_iterations:
    1. Apply goal-optimization fixes to current content
       - For each issue type, use Optimization Techniques (see below)
       - Write optimized version to working_path

    2. Launch prompt-goal-verifier agent via Task tool:
       - subagent_type: "prompt-engineering:prompt-goal-verifier"
       - prompt: "Verify prompt goal optimization.
         File: {working_path}

         Check for goal misalignment, misstep risks, failure mode gaps,
         contradictory guidance, unsafe defaults, unnecessary overhead,
         indirect paths, and redundant instructions.
         Report VERIFIED or ISSUES_FOUND with specific details."

    3. Parse agent response:
       - If "VERIFIED" → mark current todo `completed`, exit loop, proceed to Phase 4
       - If "ISSUES_FOUND" → continue to step 4

    4. If iteration < max_iterations:
       - Mark current todo `completed`
       - Add new todo: "Optimization iteration {iteration+1}" and mark `in_progress`
       - Read the specific issues reported
       - Apply Optimization Techniques to each issue
       - iteration += 1

    5. If iteration == max_iterations and still has issues:
       - Mark todo `completed` with note about unresolved issues
       - Proceed to Phase 4 with warning flag
```

## Optimization Techniques

Apply these techniques to fix goal optimization issues:

### Goal Achievement Fixes

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Goal Misalignment** | Remove/rewrite instructions that don't serve goal | Remove "format output as JSON" from prompt whose goal is readable explanations |
| **Missing/Vague Goal** | Add explicit goal section with measurable outcomes | Add "Goal: Help users debug code by identifying root causes and suggesting fixes" |
| **Goal Dilution** | Prioritize objectives, remove or subordinate competing goals | "Primary: accuracy. Secondary: speed. If conflict, choose accuracy." |
| **Unmeasurable Success** | Add success criteria with observable outcomes | Add "Success: User can reproduce the fix independently" |

### Error Prevention Fixes

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Misstep Risk** | Add guardrails, clarify scope, require confirmation | "Delete only files in /tmp/, confirm before deleting >10 files" |
| **Failure Mode Gaps** | Add explicit handling for common failures | Add "If API unavailable: retry 3x with backoff, then report error" |
| **Contradictory Guidance** | Resolve conflict with priority or conditional logic | "Be thorough for complex queries, brief for simple ones" |
| **Unsafe Defaults** | Make safe behavior explicit, require opt-in for risky actions | "Default: dry-run mode. Require --execute flag for actual changes" |

### Efficiency Fixes

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Unnecessary Overhead** | Remove steps that don't impact goal | Remove mandatory summary step if no one reads summaries |
| **Indirect Path** | Streamline to most direct approach | Replace 5-step approval process with single confirmation |
| **Redundant Instructions** | Consolidate repeated guidance | Merge 3 sections saying "be concise" into one clear statement |

### Resolution Strategy

For each issue, follow this decision tree:

```
Issue detected
    │
    ▼
Can fix be INFERRED from prompt context?
(goal, purpose, existing patterns, domain conventions)
    │
    ├─ YES → Apply inferred fix directly
    │        Examples:
    │        - Misstep risk in file deletion → infer safe defaults from prompt's cautious tone
    │        - Missing goal in code review prompt → infer "identify bugs and improvements"
    │        - Redundant instructions → consolidate using prompt's existing style
    │
    └─ NO → Make conservative fix
             (add safeguards, clarify ambiguity, document assumptions)
```

**Never ask user to clarify goal** - always infer. Display inferred goal but proceed immediately.

### Phase 4: Output

**Mark "Output optimized prompt" todo `in_progress`.**

**Step 4.1: Apply changes**

If verification passed:
```bash
# For file input: replace original
mv {working_path} {original_path}

# For inline input: keep at working_path, report location
```

**Step 4.2: Display results**

If verification passed:
```
Optimized: {path}
Iterations: {count}
Status: Goal-optimized

Inferred Goal: {goal statement}

Changes applied:
- {summary of fixes}
```

If verification failed after 5 iterations:
```
Optimized with warnings: {path}
Iterations: 5
Status: Some issues may remain

Inferred Goal: {goal statement}

Unresolved issues:
- {list from last verification}

Review the changes manually.
```

If already optimized (VERIFIED on first check):
```
Prompt is already goal-optimized. No changes needed.

Inferred Goal: {goal statement}
```

**Mark "Output optimized prompt" todo `completed`. Mark all todos complete.**

## Key Principles

| Principle | Rule |
|-----------|------|
| **Track progress** | TodoWrite to track phases; expand todos on iteration |
| **Always infer goal** | Never ask user to clarify goal; always infer and proceed |
| **Display goal** | Show inferred goal to user, but don't wait for confirmation |
| **Preserve intent** | Don't change what prompt is trying to do; optimize how effectively it does it |
| **High-confidence focus** | Only fix clear issues with material goal impact |
| **Verification required** | Never output without verifier checking |
| **Atomic output** | Original untouched until verification passes |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No input provided | Error: "Usage: /optimize-prompt-goal <file-path> OR /optimize-prompt-goal <inline prompt text>" |
| File not found | Error: "File not found: {path}" |
| Already optimized | Report success: "Prompt is already goal-optimized. No changes needed." |
| Cannot infer goal | Use best-effort inference, note `[INFERRED WITH LOW CONFIDENCE: {goal}]` |
| Severely misaligned | Make best effort over 5 iterations; output with warnings |
| Very large prompt (>50KB) | Process as single unit |

## Example Usage

```bash
# Optimize a prompt file for its goal
/optimize-prompt-goal prompts/code-reviewer.md

# Optimize inline prompt
/optimize-prompt-goal You are a helpful assistant. Be concise but thorough. Do your best.

# Optimize a skill file
/optimize-prompt-goal claude-plugins/my-plugin/skills/my-skill/SKILL.md
```

## Example Output

```
Optimized: prompts/code-reviewer.md
Iterations: 2
Status: Goal-optimized

Inferred Goal: Help developers identify bugs, security issues, and improvement opportunities in code

Changes applied:
- Added explicit goal section (was missing)
- Removed "format as markdown tables" instruction (didn't serve goal)
- Added failure handling for empty input and large files
- Consolidated 3 redundant "be thorough" statements into one
- Added success criteria: "Review complete when all critical issues identified"
```
