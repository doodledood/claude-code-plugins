---
name: review-prompt
description: "Review and analyze LLM prompts against first-principles using the 10-Layer Architecture framework. Evaluates identity, capabilities, decision logic, output specs, behavioral rules, examples, meta-cognition, complexity scaling, constraints, and quality standards. Read-only — reports findings without modifying files. Use when the user asks to review, critique, evaluate, assess, or audit an LLM prompt, system prompt, or agent instructions."
---

Use the prompt-reviewer agent to review the following prompt: $ARGUMENTS

---

The prompt-reviewer agent loads the prompt-engineering principles, then evaluates the target prompt against the 10-Layer Architecture:

| Layer | Evaluates |
|-------|-----------|
| 1. Identity & Purpose | Role clarity, mission statement |
| 2. Capabilities & Boundaries | Scope definition, expertise bounds |
| 3. Decision Architecture | IF-THEN logic, routing rules, fallbacks |
| 4. Output Specifications | Format requirements, required elements |
| 5. Behavioral Rules | Priority levels (MUST > SHOULD > PREFER) |
| 6. Examples | Perfect execution samples, edge cases |
| 7. Meta-Cognitive Instructions | Thinking process, uncertainty handling |
| 8. Complexity Scaling | Simple vs complex query handling |
| 9. Constraints & Guardrails | NEVER/ALWAYS rules, exception handling |
| 10. Quality Standards | Minimum viable, target, exceptional |

## Output

A structured report with overall assessment, score, strengths, and an issues table (type, severity, recommended fix). Issues are tagged `AUTO_FIXABLE` or `NEEDS_USER_INPUT`. Only high-confidence findings are reported — style preferences and uncertain issues are skipped.

**This skill is read-only** — it reports findings without modifying any files.
