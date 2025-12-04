# Prompt Engineering Plugin

Tools for reviewing and analyzing LLM prompts using the 10-Layer Architecture methodology.

## Overview

This plugin provides systematic prompt review that identifies genuine improvement opportunities while respecting what already works. It analyzes prompts against a comprehensive framework without over-engineering.

## Components

### Command: `/review_prompt`

Review and analyze LLM prompts (does not modify files).

**Usage:**
```bash
# Review a prompt file
/review_prompt path/to/prompt.md

# Review inline text
/review_prompt "Your prompt text here"
```

**What it does:**
- Analyzes prompts against the 10-Layer Architecture
- Identifies genuine gaps (not theoretical imperfections)
- Provides detailed assessment with strengths and problem areas
- Prioritizes recommendations by severity and impact
- Reports only—does not modify files

## Philosophy

**Perfect is the enemy of good.** The plugin follows these tenets:
- Functional elegance beats theoretical completeness
- Simplicity is a feature, not a bug
- Every added complexity must earn its place
- Recognize and preserve what already works

## The 10-Layer Architecture

Prompts are evaluated against these layers (not all layers needed for every prompt):

1. **Identity & Purpose** - Role clarity, mission, values
2. **Capabilities & Boundaries** - Can-do/cannot-do lists, scope
3. **Decision Architecture** - IF-THEN logic, thresholds, routing
4. **Output Specifications** - Format, length, required elements
5. **Behavioral Rules** - Priority levels, conflict resolution
6. **Examples** - Perfect execution, edge cases, anti-patterns
7. **Meta-Cognitive Instructions** - Thinking process, quality checks
8. **Complexity Scaling** - Simple vs complex query handling
9. **Constraints & Guardrails** - NEVER/ALWAYS rules
10. **Quality Standards** - Minimum viable, target, exceptional

## Anti-Patterns Avoided

| Trap | Instead |
|------|---------|
| Kitchen Sink | Focus on 20% rules for 80% cases |
| Weak Language | Direct: "Do X", "Never Y" |
| Over-Specification | Use principles that generalize |
| Feature Creep | Use only layers that add value |
| Complexity Inflation | Preserve elegant simplicity |

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install prompt-engineering@claude-code-plugins-marketplace
```

## License

MIT
