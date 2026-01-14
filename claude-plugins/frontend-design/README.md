# Frontend Design

Frontend design patterns and implementation skills for distinctive, non-generic UI experiences.

## Why

AI-generated frontend code often falls into predictable patterns—generic animations, template-looking layouts, safe color choices. This plugin provides skills for implementing distinctive frontend patterns that avoid the "AI slop" aesthetic.

## Components

**Skills** (auto-invoked when relevant):
- `scrollytelling` - Comprehensive scroll-driven storytelling implementation with 5 standard techniques, 4 layout patterns, accessibility-first design, and modern CSS/JS approaches

## Scrollytelling

The scrollytelling skill provides research-backed guidance for implementing scroll-driven narrative experiences.

### The 5 Standard Techniques

| Technique | Description |
|-----------|-------------|
| **Graphic Sequence** | Discrete visuals that change at scroll thresholds |
| **Animated Transition** | Smooth morphing between states |
| **Pan and Zoom** | Scroll controls visible portion of content |
| **Moviescroller** | Frame-by-frame video-like progression |
| **Show-and-Play** | Interactive elements activate at waypoints |

### Layout Patterns

| Pattern | Use Case |
|---------|----------|
| **Side-by-Side Sticky** | Data viz, step-by-step explanations (most common) |
| **Full-Width Sections** | Immersive brand storytelling, portfolios |
| **Layered Parallax** | Atmospheric narratives (requires motion fallback) |
| **Multi-Directional** | Timelines, unconventional showcases |

### Technical Coverage

- **Native CSS** (2025+): `animation-timeline: scroll()`, `animation-timeline: view()`
- **GSAP ScrollTrigger**: Complex timelines, pinning, cross-browser
- **Motion/Framer Motion**: React ecosystem
- **IntersectionObserver**: Viewport-triggered effects
- **Lenis**: Smooth scrolling integration

### Accessibility-First

- Mandatory `prefers-reduced-motion` support
- WCAG 2.2 compliance guidance
- Vestibular disorder considerations
- Keyboard navigation patterns
- Screen reader strategies

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install frontend-design@claude-code-plugins-marketplace
```

## License

MIT
