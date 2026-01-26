# BLOG Task Guidance

Task-specific guidance for blog deliverables: blog posts, articles, tutorials, newsletters.

## Blog Quality Gates

Surface which quality aspects matter. Mark recommended defaults based on task context.

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Readability | general-purpose | Accessible to target audience, scannable |
| Engagement | general-purpose | Opening hook, maintained interest throughout |
| Actionability | general-purpose | Reader knows what to do or think differently |
| SEO | general-purpose | Title, meta description, keyword usage optimized |

**Encoding**: Add selected gates as Global Invariants with subagent verification:
```yaml
verify:
  method: subagent
  agent: general-purpose
  model: opus
  prompt: "Review blog post for [quality aspect] issues"
```

## Blog-Specific AC Patterns

**Structure**
- "Title under 60 characters"
- "Opening hook in first paragraph"
- "Subheadings enable scanning"

**Content**
- "Includes [N] actionable takeaways"
- "Examples illustrate key points"
- "Technical concepts explained for [audience level]"

**Engagement**
- "Ends with clear call-to-action"
- "Meta description under 160 characters"
- "Internal/external links where relevant"
