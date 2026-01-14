# Frontend Design

Frontend design patterns and implementation skills for distinctive, non-generic UI experiences.

## Why

AI-generated frontend code often falls into predictable patterns—generic animations, template-looking layouts, safe color choices. This plugin provides skills for implementing distinctive frontend patterns that avoid the "AI slop" aesthetic.

## Components

**Skills** (auto-invoked when relevant):
- `scrollytelling` - Scroll-driven storytelling with pinned sections, progressive reveals, parallax, and scroll-linked animations

## Scrollytelling Patterns

The scrollytelling skill supports multiple patterns:

| Pattern | Use Case |
|---------|----------|
| **Pinned narrative** | Text scrolls while visual stays fixed (NYT, Pudding.cool style) |
| **Progressive reveal** | Content fades in as it enters viewport |
| **Scroll-linked** | Animations tied to scroll progress (0-100%) |
| **Parallax** | Depth through differential scroll speeds |
| **Step sequence** | Discrete sections with transitions |

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install frontend-design@claude-code-plugins-marketplace
```

## License

MIT
