# Prompt Engineering Plugin

Tools for crafting, refining, and improving LLM prompts using the 10-Layer Architecture methodology.

## Overview

This plugin provides systematic prompt optimization that balances improvement with simplicity. It analyzes prompts against a comprehensive framework while avoiding over-engineering.

## Components

### Command: `/update-prompt`

Refine and improve LLM prompts with balanced optimization.

**Usage:**
```bash
# Optimize a prompt file
/update-prompt path/to/prompt.md

# Optimize inline text
/update-prompt "Your prompt text here"

# With additional context
/update-prompt path/to/prompt.md context="Focus on clarity"
```

**What it does:**
- Analyzes prompts against the 10-Layer Architecture
- Identifies genuine gaps (not theoretical imperfections)
- Proposes only high-impact improvements (>20% improvement threshold)
- Preserves what already works well
- Avoids over-engineering and complexity inflation

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
