# Prompt Compression Skill - Interview Log

## Session Info
- Date: 2026-01-16
- Goal: Create a skill for compressing prompts/skills into single paragraphs while preserving nuance

---

## Discovery Log

### Initial Request
User wants a skill to compress full prompts or skills into one paragraph in a "lossless" way, capturing as much nuance as possible.

Key phrases:
- "one paragraph" - strict length constraint
- "lossless as possible" - maximize information density
- "capturing nuance" - preserve subtle details, not just main points

---

## Research Findings

### Existing Skills Pattern Analysis

**Plugin context**: prompt-engineering plugin (v1.11.3) - tools for reviewing, analyzing, refining, and optimizing LLM prompts.

**Existing skills**:
1. `/review-prompt` - Read-only analysis against 10-layer framework
2. `/optimize-prompt-precision` - Eliminates ambiguities, resolves conflicts
3. `/optimize-prompt-goal` - Ensures instructions serve stated goal
4. `/optimize-prompt-token-efficiency` - Reduces verbosity while preserving semantic content
5. `/apply-prompt-feedback` - Incorporates user feedback with calibration

**Common patterns**:
- Verification-first with iterative refinement (max 5 iterations)
- Clear phases: Input validation → Verification → Optimization Loop → Output
- TodoWrite for progress tracking
- Atomic output (original untouched until verification passes)
- Working in temp files during iterations

**Token-efficiency skill** (most relevant reference):
- Focus on "lossless" - preserving ALL semantic information
- Compression techniques: redundancy removal, terse phrasing, filler elimination, structural optimization, context-aware abbreviation, dense formatting
- Key principle: "Every fact, instruction, constraint, and example must be present"
- "Preserve nuance and emphasis - Bold, caps, repetition, ordering that signals priority"

### Key Differences for New Skill

The proposed "compress-prompt" skill differs from token-efficiency:
- **Token-efficiency**: Reduce verbosity while keeping full structure (15-40% reduction typical)
- **Compress-prompt**: Extreme compression into ONE PARAGRAPH (~90%+ reduction, lossy by nature)

This is a fundamentally different use case - not optimization but radical summarization.

---

## Decisions Made

(To be populated)

---

## Open Questions

(To be populated)

---

## Spec Evolution

### Draft v1 (Initial)

---
**name**: compress-prompt
**description**: [TBD - need trigger words and when-to-use clarity]

# Compress Prompt

Compress a full prompt or skill into a single dense paragraph, capturing maximum information with minimum tokens.

## Purpose

[TBD - What's the use case?]
- Memory/summarization for long-running conversations?
- Quick reference card?
- Embedding in other prompts as compressed context?
- Human-readable or AI-readable output?

## Constraints

- **Output length**: One paragraph [TBD - word/sentence limit? "paragraph" definition?]
- **Preservation priority**: [TBD - what to prioritize: goal, constraints, edge cases, examples?]
- **Lossy nature**: [TBD - is "lossless as possible" realistic for 90%+ compression? How to frame?]

## Compression Techniques

[TBD - specific techniques for extreme compression]:
- Dense notation systems?
- Abbreviations?
- Implicit context assumptions?
- Hierarchical importance filtering?

## Input/Output

- **Input**: [TBD - file path only? inline? both?]
- **Output**: [TBD - replace original? output to new file? display only?]

## Verification

[TBD - need verification loop like other skills? or simpler single-pass?]

## Edge Cases

[TBD]

---
