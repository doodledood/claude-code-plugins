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

### D1: Primary Use Case
**Decision**: AI-readable context injection
**Rationale**: User wants a token-efficient version that preserves maximum detail. LLMs perform worse as context grows, so this compression enables using full prompt semantics in constrained contexts.
**Implication**: Optimize for AI parseability over human scannability. Dense notation acceptable.

### D2: Paragraph Definition
**Decision**: Flexible density - no hard word/sentence limit
**Rationale**: "One paragraph" = single cohesive block, length determined by content complexity.
**Implication**: No arbitrary truncation. Compression quality > arbitrary length constraint.

### D3: Lossy Framing
**Decision**: Prioritized preservation + Semantic compression (both)
**Rationale**:
- Prioritized: Define what MUST vs CAN be lost
- Semantic: Encode densely so AI can "decompress" meaning
**Implication**: Hierarchical importance filtering + dense encoding techniques. Not distillation (which loses details).

---

## Open Questions

(To be populated)

---

## Spec Evolution

### Draft v2

---
**name**: compress-prompt
**description**: [TBD - need trigger words and when-to-use clarity]

# Compress Prompt

Compress a full prompt or skill into a single dense paragraph for AI-readable context injection. Maximizes information density so LLMs can "decompress" the full meaning from minimal tokens.

## Purpose

**Primary**: Create token-efficient versions of prompts/skills that preserve maximum semantic content. Addresses LLM performance degradation with growing context.

**Use cases**:
- Inject prompt context into other prompts without consuming full token budget
- Provide compressed skill summaries for agent decision-making
- Enable long prompts to fit in constrained contexts

## Constraints

- **Output format**: Single cohesive paragraph (no hard word limit - length follows content complexity)
- **Compression approach**: Prioritized preservation + semantic encoding
  - MUST preserve: [TBD - hierarchy]
  - CAN lose: [TBD - hierarchy]
- **Target audience**: AI-readable (dense notation acceptable, human readability secondary)

## Preservation Hierarchy

[TBD - what elements get priority?]
1. Core goal/purpose?
2. Hard constraints/rules?
3. Edge cases?
4. Examples?
5. Explanations?
6. Formatting hints?

## Compression Techniques

[TBD - specific techniques]:
- Abbreviations and shorthand?
- Implicit context assumptions?
- Notation systems (arrows, semicolons)?
- Reference compression ("like X but Y")?

## Input/Output

- **Input**: [TBD - file path only? inline? both?]
- **Output**: [TBD - display only? save to file? both?]

## Verification

[TBD - need verification loop? or simpler single-pass?]

## Edge Cases

[TBD]

---
