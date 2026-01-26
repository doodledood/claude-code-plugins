# RESEARCH Task Guidance

Task-specific guidance for research deliverables: investigations, analyses, comparisons, competitive reviews.

## Research Quality Gates

Surface which quality aspects matter. Mark recommended defaults based on task context.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Source credibility | general-purpose | All sources authoritative and verifiable |
| Coverage breadth | general-purpose | Multiple perspectives represented |
| Recency | general-purpose | Sources current within relevant timeframe |
| Objectivity | general-purpose | Balanced presentation, biases acknowledged |

**Encoding**: Add selected gates as Global Invariants with subagent verification:
```yaml
verify:
  method: subagent
  agent: general-purpose
  model: opus
  prompt: "Review research for [quality aspect] issues"
```

## Research-Specific AC Patterns

**Coverage**
- "Covers [topic] from [N]+ independent sources"
- "Includes [perspective/viewpoint]"
- "Addresses counterarguments to [thesis]"

**Rigor**
- "All claims cite primary sources"
- "Methodology described and justified"
- "Limitations explicitly stated"

**Synthesis**
- "Findings synthesized into actionable insights"
- "Comparison matrix covers [dimensions]"
- "Recommendation supported by evidence"
