---
description: Optimize LLM prompts using the 10-Layer Architecture. Balanced improvements that avoid overfitting.
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write"]
argument-hint: [file path to prompt, or inline prompt text]
---

Optimize prompt: $ARGUMENTS

---

**Input handling**:
- **File path**: Read file → Analyze → Apply edits
- **Inline text**: Analyze → Output improved version
- **Empty**: Ask user to provide prompt

## Philosophy: Pragmatic Optimization

Before suggesting changes:
1. **ASSESS** if prompt already works well
2. **IDENTIFY** genuine gaps, not theoretical imperfections
3. **WEIGH** improvement value against complexity
4. **PRESERVE** what works—only optimize where >20% improvement exists

**Core tenets**: Functional elegance > theoretical completeness | Simplicity is a feature | Every added complexity must earn its place

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Clarity Over Cleverness** | If it can be misinterpreted, it will be |
| **Appropriate Emphasis** | Repeat critical instructions strategically (start, middle, end) |
| **Avoid Overfitting** | General principles beat enumerated exceptions |
| **Explicit Boundaries** | Define what TO do and NOT to do |
| **Actionable Language** | "Analyze X" not "You should try to analyze X if possible" |

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Kitchen sink (every instruction) | 20% rules for 80% cases |
| Weak language ("try to", "maybe") | Direct: "Do X", "Never Y" |
| Contradictory rules | Resolve conflicts explicitly |
| Buried critical info | Surface important rules prominently |
| Missing examples | Add 1-2 concrete examples for complex behaviors |

## The 10-Layer Architecture

Evaluate against these layers. **Not every prompt needs all 10—use only what adds value.**

1. **Identity & Purpose** - Role clarity, mission, values, approach
2. **Capabilities & Boundaries** - Can-do, cannot-do, scope, expertise bounds
3. **Decision Architecture** - IF-THEN logic, thresholds, routing, fallbacks
4. **Output Specifications** - Format, length, required elements, examples
5. **Behavioral Rules** - Priority levels (MUST > SHOULD > PREFER), conflict resolution
6. **Examples** - Perfect execution, edge cases, anti-patterns with explanations
7. **Meta-Cognitive Instructions** - Thinking process, quality checks, uncertainty handling
8. **Complexity Scaling** - Simple/moderate/complex query handling, triggers
9. **Constraints & Guardrails** - NEVER/ALWAYS, flexible guidelines, exceptions
10. **Quality Standards** - Minimum viable, target, exceptional quality

## Power Techniques

**Redundant Critical Instructions**: Repeat critical rules at start, middle, end
**Cascading Specificity**: Universal → Domain → Task → Edge case
**Threshold Precision**: Replace "be concise" with "Simple: 50-150 words, Complex: 500-2000"
**Behavioral Anchors**: "Like a senior engineer conducting code review..."
**Decision Trees**: `IF confidence < 70% THEN add caveat ELSE provide direct answer`

## Output Format

### For Excellent Prompts
```markdown
## Assessment: Excellent Prompt ✓
**Why This Works**: [Specific strengths with layer references]
**Optional Enhancements**: [Only if genuinely valuable—otherwise "None needed"]
```

### For Prompts Needing Optimization
```markdown
## Assessment: Optimization Opportunities

**Layer Analysis**: [Status ✓/△/✗ for relevant layers]

**Proposed Changes**:
### Change 1: [Description]
**Rationale**: [Why this improves the prompt]
**Before**: [Original]
**After**: [Proposed]

**Changes NOT Made**: [Potential changes rejected to avoid overfitting]
```

## Quality Checks

Before suggesting changes:
□ Is this change truly necessary?
□ Will it improve performance by >20%?
□ Am I preserving the prompt's strengths?
□ Am I avoiding over-engineering?

Present full analysis BEFORE making edits. Celebrate excellent prompts rather than forcing unnecessary changes.
