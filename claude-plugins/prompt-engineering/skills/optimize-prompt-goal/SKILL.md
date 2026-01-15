---
name: optimize-prompt-goal
description: 'Optimizes prompts for goal effectiveness - ensures instructions serve the stated goal, prevents missteps, improves efficiency. Use when asked to optimize a prompt for its goal, improve goal alignment, or make a prompt more effective at achieving its purpose.'
---

# Optimize Prompt Goal

Iteratively optimize prompt for alignment with stated goal and likelihood of achieving intended outcomes through analysis and verification loops.

## Overview

This skill transforms goal-misaligned prompts into effective ones through:
1. **Goal Inference** - Extract or infer the prompt's goal/mission
2. **Analysis** - Identify goal optimization issues (misalignment, misstep risks, inefficiencies)
3. **Optimization** - Apply targeted fixes
4. **Verification** - `prompt-goal-verifier` agent checks for remaining issues
5. **Iteration** - If issues found, optimize again (max 5 iterations - sufficient for convergence in practice)
6. **Output** - Atomic replacement only after optimization complete

**Loop**: Read → Infer Goal → Optimize → Verify → (Iterate if issues) → Output

**Required tools**: This skill requires Task tool to launch the verifier agent. If Task is unavailable, report error: "Task tool required for verification loop." This skill uses TodoWrite to track progress. If TodoWrite is unavailable, track progress internally and proceed without external todo tracking.

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases. Todos represent areas of work that may expand during execution.

**Starter todos**:
```
- [ ] Input validation
- [ ] Goal inference and initial analysis
- [ ] Optimization iteration 1
- [ ] (expand on ISSUES_FOUND: iteration 2, 3...)
- [ ] Output optimized prompt
```

### Phase 1: Input Validation

**Mark "Input validation" todo `in_progress`.**

**Step 1.1: Parse arguments**

Extract input from `$ARGUMENTS`. Determine if file path or inline prompt.

**Step 1.2: Handle input type**

| Input Type | Detection | Action |
|------------|-----------|--------|
| File path | Path contains `/` or `\`, OR ends with `.md`, `.txt`, `.yaml`, `.yml` | Read file content |
| Inline prompt | Does not match file path criteria above | Write to `/tmp/prompt-{timestamp}.md` |

**Priority**: If input could match both (e.g., text containing `/`), treat as file path first; if file not found, treat as inline.

**Step 1.3: Validate content**

- If detected as file path: Attempt to read file using Read tool.
  - If file exists and has content: Use file content
  - If file exists but empty: Error: "Cannot optimize empty prompt. File contains no content: {path}"
  - If file not found: Re-classify as inline prompt and write to temp file
- If inline: Write to temp file, note original was inline
- Error only if no input provided at all: "Usage: /optimize-prompt-goal <file-path> OR /optimize-prompt-goal <inline prompt text>"

**Step 1.4: Store metadata**

- `original_path`: Source file path (or temp path for inline)
- `is_inline`: Boolean (affects output messaging)
- `original_content`: Full prompt text
- `working_path`: `/tmp/optimized-{YYYYMMDDHHMMSS}-{4-lowercase-alphanumeric}.md` where timestamp is local time formatted as digits only (e.g., `20240115143022`)

**Mark "Input validation" todo `completed`.**

### Phase 2: Initial Analysis with Goal Inference

**Mark "Goal inference and initial analysis" todo `in_progress`.**

**Step 2.1: Read and understand prompt**

Read the prompt and document:
1. **Structure**: Organization (sections, rules, examples, workflow)
2. **Instructions**: Actions/behaviors specified
3. **Constraints**: Limitations or rules imposed

**Step 2.2: Infer goal**

Extract the prompt's goal using this hierarchy (stop at first match):

1. **Explicit goal** - Look for "Goal:", "Purpose:", "Mission:", "Objective:" sections
   - If found, use verbatim
   - If multiple goal sections exist, synthesize into single coherent statement. If goal sections conflict: prefer the most specific statement; if equally specific, prefer the statement appearing earlier in the prompt (for items at the same structural level, use document order - top-to-bottom, left-to-right); note the conflict in the inferred goal.

2. **Inferred from structure** - If no explicit goal, answer:
   - What is this prompt trying to accomplish?
   - What outcomes does it optimize for?
   - What would success look like?
   - Synthesize answers into a goal statement

3. **Low-confidence inference** - If the prompt contains no explicit goal AND answers to the inference questions above are speculative rather than supported by prompt content:
   - Use `[INFERRED WITH LOW CONFIDENCE: {goal}]`
   - Proceed with best-effort inference

**Step 2.3: Display inferred goal**

Show user the detected goal, then proceed immediately:

```
Inferred Goal: {goal statement}
Proceeding with optimization...
```

**Step 2.4: Initial assessment**

Document:
- Goal clarity: explicit / inferred / low-confidence
- Obvious issues identifiable without deep analysis: explicit contradictions between instructions, missing handling for stated scenarios, instructions that clearly work against the stated goal
- Areas likely to need optimization

**Mark "Goal inference and initial analysis" todo `completed`.**

### Phase 3: Optimization Loop

**Mark "Optimization iteration 1" todo `in_progress`.**

For each iteration from 1 to 5:

1. **Apply fixes**: For each issue type, use Optimization Techniques (see below). Write optimized version to working_path using Write tool.
   - If Write tool fails: display error "Failed to save optimization iteration {iteration}: {error}" and proceed to Phase 4 using the most recent successfully written version (or original_content if none)

2. **Verify**: Launch prompt-goal-verifier agent via Task tool:
   - subagent_type: "prompt-engineering:prompt-goal-verifier"
   - prompt: "Verify prompt goal optimization. File: {working_path}. Check for goal misalignment, misstep risks, failure mode gaps, contradictory guidance, unsafe defaults, unnecessary overhead, indirect paths, and redundant instructions. Report VERIFIED or ISSUES_FOUND with specific details."

3. **Handle response**:
   - If "VERIFIED": mark todo completed, exit loop, proceed to Phase 4
   - If "ISSUES_FOUND" and iteration < 5: mark todo completed, add "Optimization iteration {next}" todo, continue to next iteration
   - If "ISSUES_FOUND" and iteration = 5: mark todo completed with note about unresolved issues, proceed to Phase 4 with warning
   - If verifier fails or returns unexpected format: display error to user, retry the verifier Task call once with identical parameters. If retry fails, proceed to Phase 4 with warning: "Verification incomplete - manual review recommended."
   - If Task tool becomes unavailable during workflow: proceed to Phase 4 with warning: "Verification unavailable - manual review recommended."

## Optimization Techniques

Apply these techniques to fix goal optimization issues:

### Goal Achievement Fixes

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Goal Misalignment** | Remove/rewrite instructions that explicitly contradict the goal statement or produce outcomes opposite to stated success criteria | Remove "format output as JSON" from prompt whose goal is readable explanations |
| **Missing/Vague Goal** | Add explicit goal section with verifiable outcomes (e.g., "user receives working code" not "user is satisfied") | Add "Goal: Help users debug code by identifying root causes and suggesting fixes" |
| **Goal Dilution** | Establish priority order. If secondary goal conflicts with primary: remove if it undermines primary in most cases, otherwise subordinate with explicit "if conflict, primary wins" clause | "Primary: accuracy. Secondary: speed. If conflict, choose accuracy." |
| **Unmeasurable Success** | Add success criteria with verifiable outcomes (actions completed, outputs produced, states achieved) | Add "Success: User can reproduce the fix independently" |

### Error Prevention Fixes

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Misstep Risk** | Add guardrails, clarify scope, require confirmation for destructive actions | "Delete only files in /tmp/, confirm before deleting multiple files" |
| **Failure Mode Gaps** | Add explicit handling for common failures | Add "If API unavailable: retry 3x with backoff, then report error" |
| **Contradictory Guidance** | Resolve conflict with priority or conditional logic | "Be thorough for complex queries, brief for simple ones" |
| **Unsafe Defaults** | Make safe behavior explicit, require opt-in for risky actions | "Default: dry-run mode. Require --execute flag for actual changes" |

### Efficiency Fixes

| Issue Type | Technique | Example |
|------------|-----------|---------|
| **Unnecessary Overhead** | Remove steps that don't impact goal achievement | Remove mandatory summary step if summaries aren't consumed |
| **Indirect Path** | Remove intermediate steps that don't add information, validation, or safeguards (keep multi-step processes if each step serves a distinct purpose) | Collapse redundant confirmation dialogs into single confirmation |
| **Redundant Instructions** | Consolidate repeated guidance into single clear statement | Merge 3 sections saying "be concise" into one |

### Resolution Strategy

For each issue, follow this decision tree:

```
Issue detected
    │
    ▼
Can fix be inferred from prompt context?
    │
    │  Check these sources in order:
    │  1. Prompt's stated goal/purpose
    │  2. Existing patterns in the prompt
    │  3. Domain conventions (conventions typical for the prompt's subject area -
    │     e.g., API prompts follow REST conventions, code review prompts follow
    │     software engineering practices)
    │  4. Sensible defaults in priority order: (1) safety - confirm destructive actions,
    │     (2) completeness - handle errors and edge cases, (3) clarity - explicit over implicit
    │
    ├─ YES (at least one source provides clear guidance)
    │       → Apply inferred fix directly
    │       Examples:
    │       - Misstep risk in file deletion → infer safe defaults from prompt's cautious tone
    │       - Missing goal in code review prompt → infer "identify bugs and improvements"
    │       - Redundant instructions → consolidate using prompt's existing style
    │
    └─ NO (no source provides clear guidance, or sources conflict)
           → Make conservative fix: add safeguards, clarify ambiguity, document assumptions
```

**Never ask user to clarify goal** - always infer and proceed.

### Phase 4: Output

**Mark "Output optimized prompt" todo `in_progress`.**

**Step 4.1: Apply changes**

After optimization complete (verification passed or max iterations reached):
- For file input: Use Write tool to replace original file with optimized content
- For inline input: Keep at working_path, report location to user

**Step 4.2: Display results**

If verification passed:
```
Optimized: {path}
Iterations: {count}
Status: Goal-optimized

Inferred Goal: {goal statement}

Changes applied:
- {List each fix as a separate bullet, prefixed with category: "Goal Achievement:", "Error Prevention:", or "Efficiency:". Combine multiple fixes of same category into one bullet if they modify the same section or address the same issue type.}
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
| **Always infer goal** | Never ask user to clarify goal; infer from context and proceed |
| **Display goal** | Show inferred goal to user, but don't wait for confirmation |
| **Preserve intent** | Don't change what prompt is trying to do; only remove/rewrite instructions that explicitly contradict the goal or produce outcomes opposite to success criteria. When an instruction's purpose is unclear but it does not explicitly contradict the goal, keep it and optimize its integration. |
| **High-confidence focus** | Only fix clear issues with demonstrable goal impact. For detected issues where the fix is unclear, apply minimal conservative safeguards rather than skipping. |
| **Verification required** | Never output without verifier checking |
| **Atomic output** | Original untouched until optimization complete. For file input, original is replaced with optimized content after all iterations (even if warnings remain). |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No input provided | Error: "Usage: /optimize-prompt-goal <file-path> OR /optimize-prompt-goal <inline prompt text>" |
| File not found | Re-classify as inline prompt and write to temp file |
| Empty file | Error: "Cannot optimize empty prompt. File contains no content: {path}" |
| Already optimized | Report: "Prompt is already goal-optimized. No changes needed." |
| Cannot infer goal | Use best-effort inference, note `[INFERRED WITH LOW CONFIDENCE: {goal}]` |
| Severely misaligned | Make best effort over 5 iterations; output with warnings |
| Very large prompt (>50KB) | Process normally as single unit; no special handling needed |
| Verifier agent fails | Display error, retry once with identical parameters; if retry fails, output with warning: "Verification incomplete - manual review recommended." |
| Task tool unavailable mid-workflow | Proceed to output with warning: "Verification unavailable - manual review recommended." |
| Write tool fails | Display error, proceed to output with most recent successful version or original_content |

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
- Goal Achievement: Added explicit goal section (was missing); removed "format as markdown tables" instruction (didn't serve goal); added success criteria
- Error Prevention: Added failure handling for empty input and large files
- Efficiency: Consolidated 3 redundant "be thorough" statements into one
```
