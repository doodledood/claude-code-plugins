---
name: compress-prompt
description: 'Compresses prompts/skills into single dense paragraphs for AI-readable context injection. Maximizes information density while preserving semantic meaning. Use when asked to compress, condense, summarize, or densify a prompt for token efficiency.'
---

# Compress Prompt

Compress a full prompt or skill into a single dense paragraph **short enough to type inline**. LLMs can "decompress" dense notation back to full meaning.

## Overview

**Goal**: Transform any prompt (even thousands of tokens) into ONE short paragraph a user could reasonably type—like a detailed instruction you'd give verbally.

This skill compresses prompts through:
1. **Initial Compression** - Aggressively compress using preservation hierarchy
2. **Verification** - `prompt-compression-verifier` checks semantic fidelity
3. **Refinement** - Fix issues based on verifier findings, iterate if needed (max 5 iterations)
4. **Output** - Display compressed paragraph + stats; optionally write to file

**Loop**: Parse input → Compress → Verify → (Iterate if issues) → Output

**Key principles**:
- **Inline-typable brevity**: Short enough a user could type it; like a detailed verbal instruction
- **Single paragraph**: ONE dense paragraph, not reformatted sections
- **Prioritized preservation**: Core goal/constraints NEVER drop; everything else CAN drop
- **Semantic encoding**: Dense notation so AI can reconstruct full meaning
- **AI-readable**: Optimize for LLM parseability over human scannability

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

   | Priority | Content | Action |
   |----------|---------|--------|
   | 1 | Core goal/purpose | NEVER drop |
   | 2 | Hard constraints (must/never/always) | NEVER drop |
   | 3 | Critical edge cases | Keep if space; condense to pattern |
   | 4 | Output format requirements | Keep structure, drop examples |
   | 5 | Examples | DROP entirely or condense to "{pattern}" |
   | 6 | Explanations/rationale | DROP (LLM can infer) |
   | 7 | Formatting/style/headers | DROP entirely |

2. **Compression Techniques**:
   - Semicolons chain related statements
   - Omit articles ("the", "a")
   - Use arrows for flow: A→B→C
   - Condense conditionals: "if X→Y; else→Z"
   - Merge phases into flow: "Phase1(do X)→Phase2(do Y)"
   - Drop all headers, bullets, structure—flatten to prose
   - Tables → dense prose: "stakes: low→quick; high→thorough"
   - Examples → pattern only: "e.g., {X}" not full example
   - Assume LLM knowledge of common concepts
   - Code blocks: keep only if essential; otherwise describe pattern

3. **Self-check before writing**:
   - Is it ONE paragraph? (no headers, no bullets, no structure)
   - Is it short enough to type inline? (not pages of text)
   - Would reformatting this back out recover the core workflow?

**Output format**: Single cohesive paragraph. No bullet points, no headers, no newlines. Short enough a user could type it.

**Step 2.3: Verify compression**

Launch prompt-compression-verifier agent via Task tool:
- subagent_type: "prompt-engineering:prompt-compression-verifier"
- prompt: "Verify compression. Original: {original_path}. Compressed: {working_path}. Check: core goal present, hard constraints preserved, no ambiguity introduced, semantic meaning faithful, critical edge cases captured. Report VERIFIED or ISSUES_FOUND with specific details."

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
   - prompt: "Verify compression. Original: {original_path}. Compressed: {working_path}. Check: core goal present, hard constraints preserved, no ambiguity introduced, semantic meaning faithful, critical edge cases captured. Report VERIFIED or ISSUES_FOUND with specific details."

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
| **Inline-typable** | Short enough a user could type it; like a verbal instruction |
| **ONE paragraph** | No headers, no bullets, no structure—flatten everything |
| **Compress then verify** | Compress aggressively first, verifier catches issues |
| **Preservation hierarchy** | Goal/constraints NEVER drop; explanations/examples DROP |
| **AI-readable** | Dense notation acceptable; human readability secondary |
| **Track progress** | TodoWrite for phases; expand on iteration |
| **Non-destructive** | Original file untouched; display output (+ optional file save) |

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Reformatting instead of compressing | DROP structure entirely; one paragraph |
| Keeping phase headers | Merge into flow: "Phase1→Phase2→Phase3" |
| Keeping bullet points | Convert to semicolon-separated prose |
| Keeping full examples | Drop or condense to pattern: "{X}" |
| Output still thousands of tokens | Be more aggressive; drop more |

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

```
Compressed: prompts/code-reviewer.md

Original: 1,247 tokens
Compressed: 156 tokens (87.5% reduction)

---
Code reviewer agent: analyze code for bugs, security issues, performance problems; flag severity (critical/high/medium/low); suggest fixes with code snippets; never approve code with critical issues; output JSON {file, line, issue, severity, fix}; handle empty input by requesting code; for large files process in chunks max 500 lines.
---

Verification: PASSED (2 iterations)
```
