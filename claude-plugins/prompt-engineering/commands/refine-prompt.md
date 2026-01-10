---
description: 'Iteratively refines prompts for precision - eliminates ambiguities, resolves conflicts, adds missing definitions. Use when asked to improve, tighten, clarify, make precise, or refine a prompt.'
argument-hint: Required - file path or inline prompt text
---

# Refine Prompt

Iteratively improve prompt precision through analysis and verification loops. Primary goal: ensure prompt cannot be interpreted in ways the author doesn't expect.

## Overview

This command transforms ambiguous prompts into precise ones through:
1. **Analysis** - Identify precision issues (ambiguities, conflicts, undefined terms, underspecified rules)
2. **Refinement** - Apply targeted fixes (infer from context when possible, ask user when not)
3. **Verification** - `prompt-precision-verifier` agent checks for remaining issues
4. **Iteration** - If issues found, refine again (max 5x)
5. **Output** - Atomic replacement only after verification passes

**Loop**: Read → Refine → Verify → (Iterate if issues) → Output

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases. List reflects areas of work, not fixed steps.

**Starter todos**:
```
- [ ] Input validation
- [ ] Initial analysis
- [ ] Refinement iteration 1
- [ ] (expand if verification fails: iteration 2, 3...)
- [ ] Output refined prompt
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
- Error if no input provided: "Usage: /refine-prompt <file-path> OR /refine-prompt <inline prompt text>"

**Step 1.4: Store metadata**

- `original_path`: Source file path (or temp path for inline)
- `is_inline`: Boolean (affects output messaging)
- `original_content`: Full prompt text
- `working_path`: `/tmp/refined-{timestamp}.md` for iterations

**Mark "Input validation" todo `completed`.**

### Phase 2: Initial Analysis

**Mark "Initial analysis" todo `in_progress`.**

Read the prompt and understand:
1. **Purpose**: What is this prompt trying to accomplish?
2. **Structure**: How is it organized? (sections, rules, examples)
3. **Obvious issues**: Any immediately visible ambiguities or conflicts?

Document findings briefly - this informs refinement strategy.

**Mark "Initial analysis" todo `completed`.**

### Phase 3: Refinement Loop

**Mark "Refinement iteration 1" todo `in_progress`.**

```
iteration = 1
max_iterations = 5

while iteration <= max_iterations:
    1. Apply precision fixes to current content
       - For each issue, use Resolution Strategy (see below)
       - Write refined version to working_path

    2. Launch prompt-precision-verifier agent via Task tool:
       - subagent_type: "prompt-engineering:prompt-precision-verifier"
       - prompt: "Verify prompt precision.
         File: {working_path}

         Check for ambiguities, conflicts, undefined terms, underspecified rules,
         vague thresholds, priority confusion, edge case gaps, and implicit expectations.
         Report VERIFIED or ISSUES_FOUND with specific details."

    3. Parse agent response:
       - If "VERIFIED" → mark current todo `completed`, exit loop, proceed to Phase 4
       - If "ISSUES_FOUND" → continue to step 4

    4. If iteration < max_iterations:
       - Mark current todo `completed`
       - Add new todo: "Refinement iteration {iteration+1}" and mark `in_progress`
       - Read the specific issues reported
       - Apply Resolution Strategy to each issue
       - iteration += 1

    5. If iteration == max_iterations and still has issues:
       - Mark todo `completed` with note about unresolved issues
       - Proceed to Phase 4 with warning flag
```

### Resolution Strategy

For each issue found, follow this decision tree:

```
Issue detected
    │
    ▼
Can resolution be INFERRED from prompt context?
(purpose, goals, existing patterns, domain conventions)
    │
    ├─ YES → Apply inferred fix directly
    │        Examples:
    │        - "Be concise" in a CLI tool prompt → infer "under 100 words"
    │        - Conflict between "brief" and "thorough" → infer based on prompt's stated purpose
    │        - Undefined "standard format" → infer from examples in prompt or domain norms
    │
    └─ NO → Ask user via AskUserQuestion
             (truly ambiguous, multiple valid interpretations, author intent unclear)
```

**Inference sources** (check in order):
1. **Prompt purpose/mission** - What is this prompt trying to accomplish?
2. **Existing patterns** - How does the prompt handle similar cases?
3. **Domain conventions** - What's standard practice in this domain?
4. **Sensible defaults** - What would a reasonable author likely intend?

**When to ask the user**:

| Ask When | Example |
|----------|---------|
| Multiple equally valid interpretations | "Be helpful" - could mean many things |
| Conflict with no clear winner | Two rules that contradict, no priority hints |
| Missing context only author knows | "Use the standard format" with no examples |
| Business/preference decision | Opt-in vs opt-out default |

**AskUserQuestion format**:

```
questions: [
  {
    question: "The prompt says '{ambiguous text}'. What did you intend?",
    header: "Clarify: {brief topic}",
    options: [
      { label: "{interpretation A}", description: "{what this means}" },
      { label: "{interpretation B}", description: "{what this means}" },
      { label: "{interpretation C}", description: "{what this means}" }
    ],
    multiSelect: false
  }
]
```

**Batch related questions** - If multiple issues need user input, ask up to 4 related questions in one AskUserQuestion call.

**After user answers**: Apply their clarification to the prompt, then continue refinement loop.

### Phase 4: Output

**Mark "Output refined prompt" todo `in_progress`.**

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
Refined: {path}
Iterations: {count}
Status: Precise and unambiguous

Changes applied:
- {summary of fixes}
```

If verification failed after 5 iterations:
```
Refined with warnings: {path}
Iterations: 5
Status: Some issues may remain

Unresolved issues:
- {list from last verification}

Review the changes manually.
```

**Mark "Output refined prompt" todo `completed`. Mark all todos complete.**

## Refinement Techniques

Apply these techniques to fix precision issues:

| Technique | Description | Before → After |
|-----------|-------------|----------------|
| **Define terms** | Add explicit definition for vague terms | "Be concise" → "Keep responses under 150 words" |
| **Resolve conflict** | Add priority or rephrase to eliminate contradiction | "Be brief" + "Be thorough" → "Be thorough for complex queries, brief for simple ones" |
| **Add threshold** | Replace subjective judgment with objective criteria | "When appropriate" → "When the user explicitly asks" |
| **Handle edge case** | Add explicit behavior for corner cases | Add "If both X and Y, prioritize X" |
| **Make explicit** | Surface implicit assumptions | Add "Assumes user has basic familiarity with..." |
| **Add priority** | Clarify which rules take precedence | Add "Rule A takes precedence over Rule B when..." |
| **Remove ambiguity** | Rephrase so only one interpretation possible | "Use the tool" → "Use the Read tool" |

## Key Principles

| Principle | Rule |
|-----------|------|
| **Memento** | TodoWrite to track phases; expand todos on iteration |
| **Infer first, ask second** | Try to resolve ambiguity from context before asking user |
| **Preserve intent** | Don't change what prompt is trying to do; only how clearly it says it |
| **Minimal changes** | Fix identified issues, don't rewrite unnecessarily |
| **Minimal questions** | Only ask user when inference is truly impossible |
| **Verification required** | Never output without verifier checking |
| **Atomic output** | Original untouched until verification passes |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No input provided | Error: "Usage: /refine-prompt <file-path> OR /refine-prompt <inline prompt text>" |
| File not found | Error: "File not found: {path}" |
| Already precise | Report success: "Prompt is already precise. No changes needed." |
| Severely ambiguous | Make best effort over 5 iterations; output with warnings |
| Very large prompt (>50KB) | Process as single unit |

## Example Usage

```bash
# Refine a prompt file
/refine-prompt prompts/code-reviewer.md

# Refine inline prompt
/refine-prompt You are a helpful assistant. Be concise but thorough. Use good judgment.

# Refine a skill file
/refine-prompt claude-plugins/my-plugin/skills/my-skill/SKILL.md
```

## Example Output

```
Refined: prompts/code-reviewer.md
Iterations: 2
Status: Precise and unambiguous

Changes applied:
- Defined "significant issues" as errors, security vulnerabilities, or logic bugs (inferred from code review context)
- Resolved conflict between "be thorough" and "keep it brief" by specifying contexts (inferred from prompt purpose)
- Added explicit behavior for empty input case (sensible default)
- Clarified priority when multiple rules apply (asked user - chose "security over style")
```
