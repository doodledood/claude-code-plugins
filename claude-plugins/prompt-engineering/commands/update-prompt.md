---
description: Refine and improve LLM prompts with balanced optimization. Analyzes prompt structure, identifies weaknesses, and proposes targeted updates that avoid overfitting.
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write"]
arguments:
  - name: prompt_path
    description: Path to the prompt file to update
    required: true
  - name: context
    description: Additional context, reference prompts, or specific issues to address
    required: false
---

# Prompt Update Request

Update the prompt at: `$ARGUMENTS`

---

## Prompt Engineering Principles

Apply these principles when analyzing and updating prompts. **Balance is key—every change should be justified.**

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Clarity Over Cleverness** | Instructions should be unambiguous. If it can be misinterpreted, it will be. |
| **Appropriate Emphasis** | Repeat critical instructions strategically (start, middle, end) but avoid over-repetition that dilutes impact. |
| **Avoid Overfitting** | Don't add rules for edge cases that rarely occur. General principles beat enumerated exceptions. |
| **Structural Balance** | Match instruction density to importance. Critical sections deserve more space; minor details less. |
| **Explicit Boundaries** | Define what TO do and what NOT to do. Omission invites hallucination. |
| **Actionable Language** | Use imperative verbs. "Analyze X" not "You should try to analyze X if possible." |
| **Consistent Voice** | Pick a framing (you are X, your task is Y) and stick with it throughout. |

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| **Kitchen Sink** | Adding every possible instruction | Focus on the 20% of rules that handle 80% of cases |
| **Contradictory Rules** | Instructions that conflict | Review holistically, resolve conflicts explicitly |
| **Over-Specification** | Enumerating every case | Use principles that generalize |
| **Weak Language** | "Try to", "if possible", "maybe" | Direct imperatives: "Do X", "Never Y" |
| **Buried Critical Info** | Important rules hidden in walls of text | Surface critical instructions prominently |
| **Redundant Repetition** | Same instruction 5 times identically | Strategic variation: same concept, different angles |
| **Missing Examples** | Abstract rules without grounding | Add 1-2 concrete examples for complex behaviors |
| **Scope Creep** | Prompt tries to do everything | Define clear boundaries, defer out-of-scope items |

---

## Analysis Framework

### 1. Structural Analysis

Evaluate the prompt's architecture:
- **Information hierarchy**: Are the most important instructions prominent?
- **Logical flow**: Does the structure guide the model through the task?
- **Section balance**: Do section lengths match their importance?
- **Redundancy audit**: Is repetition strategic or accidental?

### 2. Clarity Analysis

Check for ambiguity:
- **Vague terms**: Words like "appropriate", "good", "properly" without definition
- **Implicit assumptions**: Knowledge the model won't have
- **Conflicting instructions**: Rules that contradict each other
- **Missing context**: Information needed but not provided

### 3. Robustness Analysis

Assess generalization:
- **Edge case enumeration**: Are we listing exceptions instead of principles?
- **Overfitting signals**: Rules that apply to one specific scenario
- **Brittleness**: Will small input variations break the prompt?
- **Coverage gaps**: Common scenarios not addressed

### 4. Emphasis Analysis

Review instruction weighting:
- **Critical instruction placement**: Start, end, and strategic middle positions
- **Repetition strategy**: Key concepts reinforced at decision points
- **Visual emphasis**: Headers, bullets, bold for scanability
- **Density calibration**: More words for important concepts, fewer for minor ones

---

## Output Format

Structure your analysis and recommendations as follows:

```markdown
## Prompt Health Assessment

| Dimension | Score | Notes |
|-----------|-------|-------|
| Clarity | X/10 | [Assessment] |
| Structure | X/10 | [Assessment] |
| Balance | X/10 | [Assessment] |
| Robustness | X/10 | [Assessment] |

## Key Issues Found

### [Issue 1 Name]
- **Location**: [Where in the prompt]
- **Problem**: [What's wrong]
- **Impact**: [Why it matters]
- **Recommendation**: [Specific fix]

### [Issue 2 Name]
...

## Proposed Changes

### Change 1: [Description]
**Rationale**: [Why this change improves the prompt]

**Before**:
```
[Original text]
```

**After**:
```
[Proposed text]
```

### Change 2: [Description]
...

## Changes NOT Made (and why)

- [Potential change]: [Why it would cause overfitting/imbalance]
- ...

## Summary

[1-2 sentences on overall improvement and remaining considerations]
```

---

## Process

1. **Read** the target prompt file completely
2. **Analyze** against the framework above
3. **Identify** issues ranked by impact
4. **Propose** minimal, targeted changes that address root causes
5. **Justify** each change with clear rationale
6. **Note** changes you considered but rejected to avoid overfitting
7. **Apply** the changes using Edit tool after presenting the analysis

**Important**: Present the full analysis BEFORE making any edits. Wait for user confirmation if the changes are substantial.
