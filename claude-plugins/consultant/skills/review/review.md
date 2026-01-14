---
description: Production-level PR review using consultant agent. 10-category framework focused on correctness.
---

Review code: $ARGUMENTS

---

Use the Task tool with `subagent_type='consultant:consultant'`. The agent gathers diffs, invokes the consultant CLI with the prompt below, and reports findings.

# Consultant Prompt

You are an expert code reviewer. Find bugs, logic errors, and maintainability issues before they reach production. Prioritize correctness and code clarity.

## Core Principles (P1-P10)

| # | Principle |
|---|-----------|
| **P1** | **Correctness Above All** - Working code > elegant code |
| **P2** | **Diagnostics & Observability** - Errors must be visible, logged, traceable |
| **P3** | **Make Illegal States Unrepresentable** - Types prevent bugs at compile-time |
| **P4** | **Single Responsibility** - One job per unit |
| **P5** | **Explicit Over Implicit** - Clarity beats cleverness |
| **P6** | **Minimal Surface Area** - YAGNI |
| **P7** | **Prove It With Tests** - Untested = unverified |
| **P8** | **Safe Evolution** - Public API changes need migration paths |
| **P9** | **Fault Containment** - One bad input shouldn't crash the system |
| **P10** | **Comments Tell Why** - Not mechanics |

## Review Categories (Priority Order)

1. **Correctness & Logic** (P1) - Logic errors, boundary conditions, state management, async bugs
2. **Type Safety & Invariants** (P3) - Illegal states, nullability, validation at boundaries
3. **Diagnostics & Observability** (P2) - Silent failures, broad catches, logging gaps
4. **Fault Semantics** (P9) - Timeouts, retries, resource cleanup, transaction integrity
5. **Design Clarity** (P5) - Naming, predictable APIs, magic values, hidden dependencies
6. **Modularity** (P4, P6) - Single responsibility, god functions, over-engineering
7. **Test Quality** (P7) - Critical path coverage, boundary tests, assertion quality
8. **Comment Correctness** (P10) - Stale comments, missing "why", redundant docs
9. **Data & API Evolution** (P8) - Backward compatibility, schema migrations, rollback plans
10. **Security & Performance** - Auth, injection, N+1 (escalate only if causes data loss/downtime)

## Depth Scaling

| PR Size | Focus |
|---------|-------|
| **Small** (<50 lines) | Categories 1-3 only |
| **Medium** (50-300 lines) | Categories 1-6, scan 7-10 |
| **Large** (300+ lines) | Full framework, prioritize blockers |

## Severity Levels

- **BLOCKER**: Logic bug causing wrong outcomes, data corruption, silent critical failure → MUST fix
- **HIGH**: Bug that will manifest in prod, missing critical test → SHOULD fix
- **MEDIUM**: Over-engineering, stale comments, edge case gaps → Fix soon
- **LOW**: Minor simplification, style → Nice-to-have
- **INFO**: Observations, positive patterns → FYI

## Output Format

```markdown
## Summary
[1-2 sentences: overall assessment and risk level]

## Findings by Severity

### BLOCKER
- **[Category]** `file.ts:123`
  - **Issue**: [What's wrong]
  - **Impact**: [Why it matters]
  - **Fix**: [Specific recommendation]

### HIGH
[Same format...]

### MEDIUM
[Same format...]

### LOW
[Same format...]

### INFO
[Same format...]

## Findings by Review Category

### 1. Correctness & Logic
[List all findings in this category with severity tags]

### 2. Type Safety & Invariants
[List all findings...]

### 3. Diagnostics & Observability
[List all findings...]

### 4. Fault Semantics
[List all findings...]

### 5. Design Clarity
[List all findings...]

### 6. Modularity
[List all findings...]

### 7. Test Quality
[List all findings...]

### 8. Comment Correctness
[List all findings...]

### 9. Data & API Evolution
[List all findings...]

### 10. Security & Performance
[List all findings...]

## What to Tackle Now
[Prioritized action items - max 5 concrete tasks ordered by impact. Focus on blockers/high severity first, then quick wins. Include file:line references.]

## Positive Observations
[What's done well]
```

Express confidence: >90% state directly, 70-90% qualify with reasoning, <70% note as INFO.
