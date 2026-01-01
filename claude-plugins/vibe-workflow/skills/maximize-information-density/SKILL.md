---
name: maximize-information-density
description: 'Transform documents/prompts to maximize information density while preserving all semantic content losslessly. Reduces token consumption for AI-consumed content.'
---

# Maximize Information Density Skill

Rewrite documents to maximize information density while preserving all semantic content. Primary use case: reduce token consumption for AI-consumed content (CLAUDE.md, skills, agent prompts, specs, documentation).

## Overview

This skill transforms verbose documents into dense, information-rich versions through:
1. **Compression** - Apply density techniques to rewrite content
2. **Verification** - Launch Opus agent to verify losslessness
3. **Iteration** - If verification finds issues, re-compress with feedback (max 3x)
4. **Output** - Overwrite original with compressed version, display metrics

## Workflow

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

### Phase 2: Transformation

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

### Phase 3: Verification Loop

Launch the `density-verifier` agent (Opus) to verify lossless compression.

**Iteration Protocol**:

```
iteration = 1
max_iterations = 3

while iteration <= max_iterations:
    1. Launch density-verifier agent via Task tool:
       - subagent_type: "vibe-workflow:density-verifier"
       - model: opus
       - prompt: "Verify compression is lossless.
         Original file: {original_file_path}
         Compressed file: {temp_file_path}

         Compare semantic content. Report VERIFIED if lossless, or ISSUES with specific missing/altered information."

    2. Parse agent response:
       - If "VERIFIED" → exit loop, proceed to Phase 4
       - If "ISSUES" → continue to step 3

    3. If iteration < max_iterations:
       - Read the specific issues reported
       - Re-run Phase 2 transformation with explicit feedback:
         "The following information was lost/altered: {issues}.
          Preserve these while maintaining maximum density."
       - Write new compressed version to temp file
       - iteration += 1

    4. If iteration == max_iterations and still has issues:
       - Proceed to Phase 4 with warning flag
```

### Phase 4: Output

**Step 4.1: Calculate metrics**

- Original token count (from Phase 1)
- Compressed token count: `Math.ceil(compressed_content.length / 4)`
- Reduction percentage: `((original - compressed) / original * 100).toFixed(0)`

**Step 4.2: Apply changes**

Read compressed content from temp file, then overwrite original file using Write tool.

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

## Key Principles

### Losslessness is Paramount
Never sacrifice semantic information for density. Every fact, instruction, constraint, and example from the original must be preserved in the compressed version.

### Aggressive Transformation
Be bold with restructuring. The goal is maximum density, not preserving original style or structure. Tables, lists, and compact notation are preferred over prose.

### Verification is Non-Negotiable
Always run the Opus verification agent. Do not skip verification even if you're confident the compression is lossless.

### Iterate on Feedback
When verification finds issues, use the specific feedback to guide the next transformation. Don't just retry blindly.

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
