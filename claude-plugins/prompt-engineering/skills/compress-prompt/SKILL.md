---
name: compress-prompt
description: 'Compresses prompts/skills into minimal goal-focused instructions. Applies the Bitter Lesson: trust the model, drop what it already knows, maximize action space. Use when asked to compress, condense, or minimize a prompt.'
---

# Compress Prompt

Compress a full prompt or skill into a **minimal instruction** that preserves the goal while maximizing model freedom. Trust the model's training—it knows more than your constraints.

## Overview

**Goal**: Transform any prompt into the minimal instruction needed. Not "preserve everything densely"—instead, "what's the least I need to say for the model to succeed?"

**Philosophy (The Bitter Lesson)**:
- 99% of the work is in the model itself
- Models are trained on millions of examples—they know patterns you can't anticipate
- Constraints often LIMIT the model rather than help it
- Start with maximal capability, then restrict only what's necessary

This skill compresses prompts through:
1. **Initial Compression** - Aggressively compress, trusting model's training
2. **Verification** - `prompt-compression-verifier` checks goal clarity and flags over-specification
3. **Refinement** - Fix critical issues, remove over-specification (max 5 iterations)
4. **Output** - Display compressed paragraph + stats; optionally write to file

**Loop**: Parse input → Compress → Verify → (Iterate if issues) → Output

**Key principles**:
- **Trust the model**: Don't tell it what it already knows from training
- **Goal over process**: State WHAT, not HOW—let model choose approach
- **Novel constraints only**: Keep only constraints the model wouldn't naturally follow
- **Maximize action space**: Fewer constraints = more model freedom = better results
- **Inline-typable brevity**: Short enough a user could type it verbally

**Required tools**: This skill requires Task tool to launch the verifier agent. If Task is unavailable, report error: "Task tool required for verification loop." This skill uses TodoWrite to track progress. If TodoWrite is unavailable, track progress internally.

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases:

```
- [ ] Input validation
- [ ] Initial compression (compress, then verify)
- [ ] (expand on ISSUES_FOUND: refinement iteration 1, 2, 3...)
- [ ] Output compressed prompt
```

### Phase 1: Input Validation

**Mark "Input validation" todo `in_progress`.**

**Step 1.1: Parse arguments**

Extract from `$ARGUMENTS`:
- Prompt (file path or inline text)
- Optional `--output <path>` flag for file output

**Step 1.2: Determine prompt source**

| Input Type | Detection | Action |
|------------|-----------|--------|
| File path | Contains `/` or `\`, OR ends with `.md`, `.txt`, `.yaml`, `.yml` | Read file content |
| Inline prompt | Does not match file path criteria | Use directly |

**Priority**: If ambiguous, treat as file path first; if not found, treat as inline.

**Step 1.3: Validate inputs**

- If file path exists and has content: Use file content
- If file empty: Error: "Cannot compress empty prompt: {path}"
- If file not found: Re-classify as inline text
- If no prompt: Error: "Usage: /compress-prompt <file-path-or-prompt> [--output path]"
- If binary file detected: Error: "Cannot compress binary file: {path}"

**Step 1.4: Estimate tokens and check length**

- Estimate original tokens: `Math.ceil(content.length / 4)` (approximate)
- If tokens < 100: Warning: "Prompt already concise ({tokens} tokens)" + compress anyway
- Store `original_content`, `original_tokens`, `output_path` (if --output provided)

**Step 1.5: Store metadata**

- `source_path`: Source file path (or "inline" for inline input)
- `original_content`: Full prompt text
- `original_tokens`: Estimated token count
- `original_path`: `/tmp/compress-original-{YYYYMMDDHHMMSS}-{4-lowercase-alphanumeric}.md` (copy for verifier)
- `working_path`: `/tmp/compress-working-{YYYYMMDDHHMMSS}-{4-lowercase-alphanumeric}.md` (compressed version)
- `output_path`: User-specified output path (if --output provided)

**Mark "Input validation" todo `completed`.**

### Phase 2: Initial Compression

**Mark "Initial compression" todo `in_progress`.**

**Step 2.1: Create working copies**

Using Write tool:
1. Copy original content to `original_path` (untouched reference for verifier)
2. Compress and write to `working_path`

**Step 2.2: Apply compression**

**⚠️ CRITICAL**: Output must be ONE dense paragraph short enough to type inline. Not reformatted sections. Not bullet points. ONE paragraph you could reasonably type.

Compress using:

1. **Preservation Hierarchy** (what to KEEP vs DROP):

   | Priority | Content | Action | Rationale |
   |----------|---------|--------|-----------|
   | 1 | Core goal/purpose | KEEP | Model needs to know WHAT to do |
   | 2 | Novel constraints | KEEP | Counter-intuitive rules model wouldn't guess |
   | 3 | Output artifacts | KEEP (brief) | File paths, format names if non-standard |
   | 4 | Obvious constraints | DROP | Model does this naturally from training |
   | 5 | Edge cases | DROP | Model handles edge cases from training |
   | 6 | Process/phases | DROP | Model chooses its own approach |
   | 7 | Examples | DROP | Model knows patterns |
   | 8 | Explanations | DROP | Model can infer rationale |
   | 9 | Formatting/style | DROP | Model knows professional defaults |

2. **The Training Filter** (ask for EACH constraint):

   > "Would a senior developer need to be told this, or would they figure it out?"

   If model's training covers it → DROP. Examples of training-redundant content:
   - "Handle errors gracefully" → model does this
   - "Ask clarifying questions if unclear" → model does this
   - "Be thorough" → model does this
   - "Consider edge cases" → model does this
   - "Structure output logically" → model does this
   - "Use professional tone" → model does this
   - Common workflow patterns → model knows these

3. **Novel vs Obvious Constraints**:

   | Type | Example | Action |
   |------|---------|--------|
   | Novel | "Never suggest implementation during spec phase" | KEEP - counter-intuitive |
   | Novel | "Write findings to file BEFORE proceeding" | KEEP - specific discipline |
   | Novel | "Use AskUserQuestion tool, not inline questions" | KEEP - tool-specific |
   | Obvious | "Be helpful and thorough" | DROP - model default |
   | Obvious | "Handle empty input" | DROP - model default |
   | Obvious | "Validate before proceeding" | DROP - model default |

4. **Compression Techniques**:
   - State goal in first sentence
   - Add only novel constraints
   - Specify output artifact if non-obvious
   - Omit process—let model decide HOW
   - Semicolons chain related statements
   - Use arrows sparingly: only for truly sequential dependencies
   - Drop all structure—flatten to prose

5. **Action Space Check** (before finalizing):
   - Does this leave model FREE to solve the problem its own way?
   - Am I prescribing process, or just stating the goal?
   - Could the model achieve this with LESS instruction?
   - If I removed this constraint, would the model fail? If no → remove it.

**Output format**: Single cohesive paragraph. Goal + novel constraints + output artifact. That's it.

**Step 2.3: Verify compression**

Launch prompt-compression-verifier agent via Task tool:
- subagent_type: "prompt-engineering:prompt-compression-verifier"
- prompt: "Verify compression. Original: {original_path}. Compressed: {working_path}. Check: goal is clear, novel constraints preserved, action space is open, no over-specification. Flag any training-redundant content that should be removed. Report VERIFIED or ISSUES_FOUND."

**Step 2.4: Handle verifier response**

- If "VERIFIED": Mark todo completed, proceed to Phase 4
- If "ISSUES_FOUND": Mark todo completed, save issues, add "Refinement iteration 1" todo, proceed to Phase 3
- If verifier fails: Retry once. If retry fails, proceed to Phase 4 with warning: "Verification failed - manual review recommended."

**Step 2.5: Display findings**

If issues found:
```
Verifier found {count} issues. Proceeding with refinement...
```

**Mark "Initial compression" todo `completed`.**

### Phase 3: Refinement Loop (Verifier-Driven)

**Mark "Refinement iteration 1" todo `in_progress`.**

**Key principle**: All refinements driven by verifier feedback. Only fix issues the verifier reported.

For each iteration from 1 to 5:

1. **Apply fixes from verifier feedback**: For each issue, apply the Suggested Fix. Update `working_path`.
   - Only address issues the verifier identified
   - Maintain single-paragraph format
   - If Write tool fails: display error, proceed to Phase 4 with most recent version

2. **Re-verify**: Launch prompt-compression-verifier agent via Task tool:
   - subagent_type: "prompt-engineering:prompt-compression-verifier"
   - prompt: "Verify compression. Original: {original_path}. Compressed: {working_path}. Check: goal is clear, novel constraints preserved, action space is open, no over-specification. Flag any training-redundant content that should be removed. Report VERIFIED or ISSUES_FOUND."

3. **Handle response**:
   - If "VERIFIED": mark todo completed, exit loop, proceed to Phase 4
   - If "ISSUES_FOUND" and iteration < 5: mark todo completed, save issues, add "Refinement iteration {next}" todo, continue
   - If "ISSUES_FOUND" and iteration = 5: mark todo completed with note, proceed to Phase 4 with warning
   - If verifier fails: display error, retry once. If retry fails, proceed to Phase 4 with warning: "Verification incomplete - manual review recommended."

### Phase 4: Output

**Mark "Output compressed prompt" todo `in_progress`.**

**Step 4.1: Calculate metrics**

- Original token count (from Phase 1)
- Compressed token count: `Math.ceil(compressed_content.length / 4)`
- Reduction percentage: `((original - compressed) / original * 100).toFixed(1)`

**Step 4.2: Output to file (if requested)**

If `--output <path>` was provided:
- Write compressed content to specified path
- Report: "Saved to: {path}"

**Step 4.3: Display results**

If verification passed:
```
Compressed: {source_path}

Original: {original_tokens} tokens
Compressed: {compressed_tokens} tokens ({percentage}% reduction)

---
{compressed paragraph}
---

Verification: PASSED ({iteration_count} iteration(s))
```

If verification failed after 5 iterations:
```
Compressed with warnings: {source_path}

Original: {original_tokens} tokens
Compressed: {compressed_tokens} tokens ({percentage}% reduction)

---
{compressed paragraph}
---

Verification: INCOMPLETE - manual review recommended

Unresolved issues:
- {list from last verification}
```

**Mark "Output compressed prompt" todo `completed`. Mark all todos complete.**

## Key Principles

| Principle | Rule |
|-----------|------|
| **Trust the model** | Don't tell it what it already knows—it's trained on millions of examples |
| **Goal over process** | State WHAT to achieve, not HOW to do it |
| **Novel constraints only** | Keep only counter-intuitive rules model wouldn't naturally follow |
| **Maximize action space** | Fewer constraints = more freedom = better results |
| **Training filter** | "Would a senior dev need to be told this?" If no → drop |
| **Inline-typable** | Short enough to type verbally—like instructing a capable colleague |
| **Non-destructive** | Original file untouched; display output (+ optional file save) |

## Common Mistakes to Avoid

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Preserving "obvious" constraints | Model does these naturally | Apply training filter—drop them |
| Keeping process/phases | Constrains model's approach | State goal only, let model decide how |
| Keeping edge case handling | Model handles edge cases from training | Trust the model |
| Dense but still long | Preserved too much | Ask "would model fail without this?" |
| Prescribing tools/methods | Limits action space | State goal, not implementation |
| "Be thorough/professional" | Training-redundant | Drop entirely |

## Edge Cases

| Scenario | Handling |
|----------|----------|
| No prompt provided | Error: "Usage: /compress-prompt <file-path-or-prompt> [--output path]" |
| Empty file | Error: "Cannot compress empty prompt: {path}" |
| Short prompt (<100 tokens) | Warning: "Prompt already concise" + compress anyway |
| File not found | Re-classify as inline text if plausible, else error |
| Binary/non-text file | Error: "Cannot compress binary file: {path}" |
| Prompt with code blocks | Preserve code blocks as-is; compress surrounding text |
| Prompt with tables | Convert table semantics to dense prose |
| Verification fails 5x | Output with warning: "Manual review recommended" |
| Task tool unavailable | Error: "Task tool required for verification loop" |
| --output path invalid | Error: "Cannot write to: {path}" |

## Example Usage

```bash
# Compress a prompt file
/compress-prompt prompts/code-reviewer.md

# Compress and save to file
/compress-prompt skills/bug-fixer/SKILL.md --output compressed/bug-fixer.txt

# Compress inline text
/compress-prompt "You are a helpful assistant that reviews code for bugs..."
```

## Example Output

**Before (Bitter Lesson approach)**:
```
Compressed: prompts/code-reviewer.md

Original: 1,247 tokens
Compressed: 52 tokens (95.8% reduction)

---
Review code for bugs, security issues, performance problems. Output JSON {file, line, issue, severity, fix}. Never approve code with critical issues.
---

Verification: PASSED (1 iteration)
```

**What was dropped and why**:
- "suggest fixes with code snippets" → model does this naturally when finding issues
- "handle empty input by requesting code" → model handles edge cases from training
- "for large files process in chunks max 500 lines" → model manages context naturally
- "flag severity" → implied by severity field in output format

**The only novel constraint kept**: "Never approve code with critical issues" — counter-intuitive (model might default to always providing approval with caveats).
