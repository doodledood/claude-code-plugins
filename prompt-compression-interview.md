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

### D4: Preservation Hierarchy
**Decision**: Accepted proposed hierarchy
1. Core goal/purpose
2. Hard constraints/rules
3. Critical edge cases
4. Output format requirements
5. Examples (condensed to pattern)
6. Explanations/rationale (can usually be inferred)
7. Formatting/style hints
**Implication**: Compression algorithm should process in this order, dropping lower tiers when space-constrained.

### D5: Compression Notation
**Decision**: Natural dense prose
**Rationale**: Extremely terse but grammatical English. Readable by both AI and humans with effort.
**Example**: "Validate input; reject empty; return JSON {status, data}; on error include trace."

### D6: Implicit Context
**Decision**: Assume LLM knowledge, BUT keep precise when ambiguous
**Rationale**: Don't explain common concepts, but disambiguate when needed.
**Example**: "WWF (wildlife)" not just "WWF" if context doesn't clarify.
**Implication**: Compression should leverage shared LLM knowledge but not introduce ambiguity.

### D7: Input Format
**Decision**: File path + inline
**Rationale**: More flexible - accept both file paths and inline text.
**Implication**: Need input type detection (file path vs inline content).

### D8: Output Destination
**Decision**: Display + optional file
**Rationale**: Display by default, with optional flag to save to file.
**Implication**: Add `--output path` or similar flag for file output.

### D9: Verification
**Decision**: Agent verification (follow existing plugin pattern)
**Rationale**: Use verification loop like other skills in prompt-engineering plugin.
**Implication**: Need a `prompt-compression-verifier` agent that checks:
- All high-priority elements preserved
- No ambiguity introduced
- Compression is semantically faithful

---

## Open Questions

(To be populated)

---

## Spec Evolution

### Draft v4

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
- **Target audience**: AI-readable (dense notation acceptable, human readability secondary)

## Preservation Hierarchy

Highest to lowest priority (drop from bottom when compressing):

1. **Core goal/purpose** - What the prompt fundamentally does (NEVER drop)
2. **Hard constraints/rules** - Non-negotiable behaviors (NEVER drop)
3. **Critical edge cases** - Behaviors that prevent failure modes
4. **Output format requirements** - Structure of expected output
5. **Examples** - Condensed to pattern, not full text
6. **Explanations/rationale** - Can usually be inferred by AI
7. **Formatting/style hints** - Tone, verbosity preferences (drop first)

## Compression Techniques

**Natural dense prose**: Extremely terse but grammatical English.
- Use semicolons to chain related statements
- Omit articles ("the", "a") where unambiguous
- Use common abbreviations (JSON, API, etc.)
- Assume LLM knowledge of common concepts
- Disambiguate only when multiple meanings possible (e.g., "WWF (wildlife)")
- Condense examples to pattern representation

## Input/Output

**Input**: File path OR inline text
- File path detection: contains `/` or `\`, OR ends with `.md`, `.txt`, `.yaml`, `.yml`
- Inline: write to temp file for processing

**Output**: Display to terminal by default
- Optional `--output <path>` flag to save compressed output to file
- Always show compression stats (original tokens → compressed tokens, ratio)

## Workflow

1. **Input validation** - Parse arguments, detect input type, read content
2. **Initial compression** - Apply compression techniques with preservation hierarchy
3. **Verification loop** (max 5 iterations):
   - Launch `prompt-compression-verifier` agent
   - Check: high-priority elements preserved, no ambiguity introduced, semantic fidelity
   - If VERIFIED: proceed to output
   - If ISSUES_FOUND: refine and re-verify
4. **Output** - Display compressed paragraph + stats; optionally write to file

## Verifier Agent

`prompt-compression-verifier` checks:
- [ ] Core goal/purpose present and accurate
- [ ] Hard constraints/rules preserved
- [ ] No ambiguous terms introduced
- [ ] Semantic meaning faithful to original
- [ ] Critical edge cases captured (if present in original)

Reports: VERIFIED or ISSUES_FOUND with specific missing/problematic elements.

## Edge Cases

[TBD]

---
