---
name: maximize-information-density
description: 'Compresses documents/prompts to maximize information density while preserving semantic content. Use when asked to make content concise, shorten, reduce tokens, tighten, or compress files like CLAUDE.md, skills, or specs.'
---

# Maximize Information Density Skill

Rewrite documents to maximize information density while preserving all semantic content. Primary use case: reduce token consumption for AI-consumed content (CLAUDE.md, skills, agent prompts, specs, documentation).

## Overview

This skill transforms verbose documents into dense, information-rich versions through:
1. **Compression** - Apply density techniques, write to `/tmp` (original untouched)
2. **Verification** - information-density-verifier agent compares original vs compressed for losslessness
3. **Iteration** - If issues found, re-compress with feedback (max 3x)
4. **Output** - Atomic `mv` replaces original only after verification passes

**Loop**: Validate → Compress → Verify → (Iterate if issues) → Output

## Workflow

### Phase 0: Create Todo List (TodoWrite immediately)

Create todos tracking workflow phases. List reflects areas of work, not fixed steps.

**Starter todos**:
```
- [ ] Input validation
- [ ] Initial compression
- [ ] Verification (iteration 1)
- [ ] (expand if verification fails: iteration 2, 3)
- [ ] Output and replace original
```

### Phase 1: Input Validation

**Step 1.1: Parse arguments**

Extract file path from `$ARGUMENTS`. If no path provided, error with usage instructions.

**Step 1.2: Validate file**

- Check file exists using Read tool
- Verify supported type: `.md`, `.txt`, `.yaml`, `.json`
- If unsupported, error: "Unsupported file type. Supported: .md, .txt, .yaml, .json"

**Step 1.3: Read and measure original**

- Read file content
- Estimate token count: `Math.ceil(content.length / 4)` (approximate)
- Store original content and token count for comparison

**Mark "Input validation" todo `in_progress`**, then `completed` when Phase 1 done.

### Phase 2: Transformation

**Mark "Initial compression" todo `in_progress`.**

Apply ALL compression techniques aggressively. Full restructuring is allowed.

**Compression Techniques**:

| Technique | Description | Example |
|-----------|-------------|---------|
| **Redundancy removal** | Eliminate repeated concepts, consolidate overlapping statements | "It is important to note that you should always remember to..." → "Always..." |
| **Terse phrasing** | Replace verbose constructions with compact equivalents | "In order to accomplish this task, you will need to..." → "To do this:" |
| **Filler elimination** | Remove hedging, qualifiers, throat-clearing | "Make sure that you do not forget to include..." → "Include:" |
| **Structural optimization** | Merge/reorganize sections for density | "First X. After that Y. Then Z. Finally W." → "Steps: X → Y → Z → W" |
| **Context-aware abbreviation** | Abbreviate terms after first mention | "Model Context Protocol server" (×10) → "MCP server" (after first) |
| **Dense formatting** | Use lists, tables, compact notation | Prose paragraphs → Tables, bullet lists |

**Transformation Rules**:

1. **Preserve ALL semantic information** - Every fact, instruction, constraint, and example must be present
2. **Full restructuring allowed** - Reorder, merge sections, change hierarchy if it increases density
3. **Format preservation** - Output must be same format as input (markdown stays markdown)
4. **Primary audience is AI** - Optimize for machine parsing, not human aesthetics

**Step 2.1: Analyze content**

Identify:
- Content type (documentation, prompt, spec, config)
- Structure and redundancy patterns
- Compression opportunities

**Step 2.2: Apply transformation**

Rewrite the entire document applying all techniques. Be aggressive - maximize density.

**Step 2.3: Write to temp file**

Write compressed output to `/tmp/compressed-{timestamp}.{ext}` where:
- `{timestamp}` = current time for uniqueness
- `{ext}` = original file extension

**Mark "Initial compression" todo `completed`.**

### Phase 3: Verification Loop

**Mark "Verification (iteration 1)" todo `in_progress`.**

Launch the `vibe-extras:information-density-verifier` agent to verify lossless compression.

**Iteration Protocol**:

```
iteration = 1
max_iterations = 3

while iteration <= max_iterations:
    1. Launch information-density-verifier agent via Task tool:
       - subagent_type: "vibe-extras:information-density-verifier"
       - prompt: "Verify compression is lossless.
         Original file: {original_file_path}
         Compressed file: {temp_file_path}

         Compare semantic content. Report VERIFIED if lossless, or ISSUES with specific missing/altered information."

    2. Parse agent response:
       - If "VERIFIED" → mark current verification todo `completed`, exit loop, proceed to Phase 4
       - If "ISSUES" → continue to step 3

    3. If iteration < max_iterations:
       - Mark current verification todo `completed`
       - **Add new todo**: "Verification (iteration {iteration+1})" and mark `in_progress`
       - Read the specific issues reported
       - Re-run Phase 2 transformation with explicit feedback:
         "The following information was lost/altered: {issues}.
          Preserve these while maintaining maximum density."
       - Write new compressed version to temp file
       - iteration += 1

    4. If iteration == max_iterations and still has issues:
       - Mark todo `completed` with note about unresolved issues
       - Proceed to Phase 4 with warning flag
```

### Phase 4: Output

**Mark "Output and replace original" todo `in_progress`.**

**Step 4.1: Calculate metrics**

- Original token count (from Phase 1)
- Compressed token count: `Math.ceil(compressed_content.length / 4)`
- Reduction percentage: `((original - compressed) / original * 100).toFixed(0)`

**Step 4.2: Apply changes (atomic replacement)**

Original file remains untouched until verification passes. Replace atomically:
```bash
mv /tmp/compressed-{timestamp}.{ext} {original_file_path}
```
This ensures original is preserved if verification fails or process is interrupted.

**Step 4.3: Display results**

If verification passed:
```
✓ Compressed: {file_path}
  Original:   {original_tokens} tokens
  Compressed: {compressed_tokens} tokens
  Reduction:  {percentage}%

  Changes: {brief summary of techniques applied}

  Verification: ✓ Lossless ({iteration_count} iteration(s))
```

If verification failed after 3 iterations:
```
⚠ Compressed with warnings: {file_path}
  Original:   {original_tokens} tokens
  Compressed: {compressed_tokens} tokens
  Reduction:  {percentage}%

  Changes: {brief summary of techniques applied}

  Verification: ⚠ Could not fully verify after 3 iterations
  Potential issues: {list from last verification}

  Review the changes manually to ensure no critical information was lost.
```

**Mark "Output and replace original" todo `completed`. Mark all todos complete.**

## Edge Cases

| Scenario | Handling |
|----------|----------|
| File not found | Error: "File not found: {path}" |
| Unsupported type | Error: "Unsupported file type. Supported: .md, .txt, .yaml, .json" |
| Already dense content | May achieve minimal reduction; still run verification |
| YAML/JSON structure | Preserve structure validity, compress string values only |
| Very large file (>50KB) | Process as single unit |
| 0% reduction | Report: "Content already maximally dense" |
| Verification fails 3x | Output best attempt with warning about potential loss |
| mv fails | Error with temp file path; user can manually review/apply |

## Key Principles

| Principle | Rule |
|-----------|------|
| **Memento** | Use TodoWrite to track phases; expand todos when verification fails; mark progress immediately |
| **Losslessness** | Never sacrifice semantic information for density; every fact must be preserved |
| **Aggressive** | Full restructuring allowed; maximize density, not preserve original style |
| **Verification** | Always run information-density-verifier; never skip; iterate with specific feedback |

## Example Usage

```bash
# Compress a verbose README
/maximize-information-density docs/README.md

# Compress CLAUDE.md
/maximize-information-density CLAUDE.md

# Compress a skill file
/maximize-information-density skills/plan/SKILL.md
```

## Example Output

```
✓ Compressed: docs/README.md
  Original:   4,250 tokens
  Compressed: 2,890 tokens
  Reduction:  32%

  Changes: Removed redundant intro, consolidated examples,
  merged overlapping sections, tersified instructions.

  Verification: ✓ Lossless (1 iteration)
```
