---
name: scrollytelling
description: 'Implements scroll-driven storytelling experiences with pinned sections, progressive reveals, and scroll-linked animations. Use when asked to build scrollytelling, scroll-driven animations, parallax effects, narrative scroll experiences, or story-driven landing pages.'
---

# Scrollytelling Skill

Build scroll-driven narrative experiences that reveal content, trigger animations, and create immersive storytelling as users scroll.

## Overview

Scrollytelling combines scrolling with storytelling—content reveals, animations, and transitions tied to scroll position. This skill helps implement:

- **Pinned sections** - Content stays fixed while scroll progresses through steps
- **Progressive reveals** - Text/images fade in as they enter viewport
- **Scroll-linked animations** - Elements animate based on scroll progress (0-100%)
- **Parallax layers** - Depth through differential scroll speeds
- **Step-based narratives** - Discrete content changes at scroll thresholds

## When to Use

- Landing pages telling a product story
- Case studies with visual progression
- Data visualizations that build up
- Feature tours with step-by-step reveals
- Any narrative that unfolds over scroll

## Discovery Questions

Before implementing, clarify with the user:

```
header: "Scrollytelling Pattern"
question: "What scrollytelling pattern fits your narrative?"
options:
  - "Pinned narrative - text changes while visual stays fixed (NYT, Pudding.cool style)"
  - "Progressive reveal - content fades in as you scroll down"
  - "Parallax depth - layers move at different speeds"
  - "Step sequence - discrete sections with transitions between"
  - "Hybrid - multiple patterns combined"
```

```
header: "Tech Stack"
question: "What's your frontend setup?"
options:
  - "React + Tailwind"
  - "React + CSS-in-JS"
  - "Next.js"
  - "Vue"
  - "Vanilla JS"
  - "Other"
```

```
header: "Animation Library"
question: "Any animation library preference?"
options:
  - "CSS-only (scroll-timeline, IntersectionObserver)"
  - "GSAP ScrollTrigger (most powerful)"
  - "Framer Motion (React)"
  - "Lenis + custom (smooth scroll)"
  - "No preference - recommend based on complexity"
```

## Implementation Patterns

### Pattern 1: Pinned Narrative (Text + Visual)

The classic scrollytelling pattern: visual stays pinned while text sections scroll past, each triggering content changes.

**Structure:**
```
┌─────────────────────────────────────┐
│  ┌──────────┐  ┌─────────────────┐  │
│  │  Text    │  │                 │  │
│  │  Step 1  │  │    PINNED       │  │
│  ├──────────┤  │    VISUAL       │  │
│  │  Text    │  │                 │  │
│  │  Step 2  │  │  (changes with  │  │
│  ├──────────┤  │   active step)  │  │
│  │  Text    │  │                 │  │
│  │  Step 3  │  │                 │  │
│  └──────────┘  └─────────────────┘  │
└─────────────────────────────────────┘
```

**Key mechanics:**
- Container has `height: <num-steps> * 100vh`
- Visual uses `position: sticky; top: 0`
- IntersectionObserver tracks which text step is active
- Visual updates based on active step index

**React + GSAP example:**
```tsx
const ScrollytellingSection = ({ steps }) => {
  const containerRef = useRef(null);
  const visualRef = useRef(null);
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const ctx = gsap.context(() => {
      steps.forEach((_, index) => {
        ScrollTrigger.create({
          trigger: `.step-${index}`,
          start: 'top center',
          end: 'bottom center',
          onEnter: () => setActiveStep(index),
          onEnterBack: () => setActiveStep(index),
        });
      });
    }, containerRef);
    return () => ctx.revert();
  }, [steps]);

  return (
    <section ref={containerRef} className="relative">
      <div className="grid grid-cols-2 gap-8">
        {/* Text column - scrolls naturally */}
        <div className="space-y-[100vh]">
          {steps.map((step, i) => (
            <div
              key={i}
              className={`step-${i} min-h-screen flex items-center transition-opacity duration-300 ${
                activeStep === i ? 'opacity-100' : 'opacity-30'
              }`}
            >
              <div className="max-w-md">
                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Visual column - sticky */}
        <div className="relative">
          <div
            ref={visualRef}
            className="sticky top-0 h-screen flex items-center justify-center"
          >
            <StepVisual step={activeStep} data={steps[activeStep]} />
          </div>
        </div>
      </div>
    </section>
  );
};
```

### Pattern 2: Progressive Reveal

Content fades/slides in as it enters the viewport. Simpler than pinned, works well for feature lists.

**CSS-only approach (modern browsers):**
```css
@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.reveal-on-scroll {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}
```

**IntersectionObserver fallback:**
```tsx
const RevealOnScroll = ({ children, delay = 0 }) => {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1, rootMargin: '-50px' }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateY(0)' : 'translateY(30px)',
        transition: `all 0.6s ease ${delay}ms`,
      }}
    >
      {children}
    </div>
  );
};
```

### Pattern 3: Scroll-Linked Progress

Elements animate proportionally to scroll position. Great for progress bars, filling graphics, or continuous transformations.

**Scroll progress hook:**
```tsx
const useScrollProgress = (ref) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const updateProgress = () => {
      const rect = element.getBoundingClientRect();
      const windowHeight = window.innerHeight;

      // 0 when element top enters viewport, 1 when bottom exits
      const start = rect.top - windowHeight;
      const end = rect.bottom;
      const current = -start;
      const total = end - start;

      setProgress(Math.max(0, Math.min(1, current / total)));
    };

    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
    return () => window.removeEventListener('scroll', updateProgress);
  }, [ref]);

  return progress;
};

// Usage
const AnimatedSection = () => {
  const ref = useRef(null);
  const progress = useScrollProgress(ref);

  return (
    <section ref={ref} className="h-[200vh]">
      <div className="sticky top-0 h-screen flex items-center">
        <div
          style={{
            width: `${progress * 100}%`,
            opacity: 0.3 + progress * 0.7,
          }}
          className="h-2 bg-accent"
        />
      </div>
    </section>
  );
};
```

### Pattern 4: Parallax Layers

Multiple layers moving at different speeds create depth.

```tsx
const ParallaxSection = ({ layers }) => {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <section className="relative h-screen overflow-hidden">
      {layers.map((layer, i) => (
        <div
          key={i}
          className="absolute inset-0"
          style={{
            transform: `translateY(${scrollY * layer.speed}px)`,
            zIndex: layer.zIndex,
          }}
        >
          {layer.content}
        </div>
      ))}
    </section>
  );
};

// Usage
<ParallaxSection
  layers={[
    { content: <Background />, speed: 0.1, zIndex: 0 },
    { content: <MidLayer />, speed: 0.3, zIndex: 1 },
    { content: <Foreground />, speed: 0.5, zIndex: 2 },
  ]}
/>
```

## Performance Considerations

### Do
- Use `transform` and `opacity` for animations (GPU-accelerated)
- Add `will-change: transform` sparingly on animated elements
- Use `passive: true` on scroll listeners
- Debounce/throttle scroll handlers if doing heavy calculations
- Use `position: sticky` over JS-based pinning when possible
- Consider `content-visibility: auto` for off-screen sections

### Don't
- Animate `width`, `height`, `top`, `left` (triggers layout)
- Create scroll listeners without cleanup
- Forget to handle reduced-motion preferences
- Load heavy assets until needed (use lazy loading)

### Reduced Motion Support

Always respect user preferences:

```tsx
const prefersReducedMotion = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// In components
const shouldAnimate = !prefersReducedMotion();
```

```css
@media (prefers-reduced-motion: reduce) {
  .reveal-on-scroll {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

## Library Recommendations

| Complexity | Recommendation |
|------------|----------------|
| Simple reveals | CSS `animation-timeline: view()` or IntersectionObserver |
| Pinned narratives | GSAP ScrollTrigger (most battle-tested) |
| React projects | Framer Motion's `useScroll` + `useTransform` |
| Smooth scroll | Lenis + GSAP combination |
| Data viz | D3 + ScrollTrigger integration |

## Anti-Patterns to Avoid

- **Scroll hijacking** - Don't override natural scroll behavior completely
- **Too many effects** - Scrollytelling should enhance narrative, not distract
- **No fallback** - Always ensure content is accessible without JS
- **Ignoring mobile** - Touch scrolling behaves differently; test thoroughly
- **Performance death spiral** - Multiple heavy scroll handlers competing

## Workflow

1. **Understand the narrative** - What story are you telling? What's the sequence?
2. **Choose pattern** - Pinned, progressive, parallax, or hybrid?
3. **Scaffold structure** - Build the HTML/component structure first
4. **Add scroll mechanics** - Implement tracking (IntersectionObserver, ScrollTrigger, etc.)
5. **Wire animations** - Connect scroll state to visual changes
6. **Add polish** - Easing, timing, micro-interactions
7. **Performance audit** - Check for jank, optimize as needed
8. **Accessibility pass** - Reduced motion, keyboard nav, screen readers
9. **Mobile testing** - Touch scroll, viewport changes, performance

## Output

After gathering requirements, implement the scrollytelling experience directly in the codebase. Provide:

1. Component structure with scroll tracking
2. Animation/transition logic
3. Responsive adjustments
4. Reduced-motion fallbacks
5. Any necessary CSS/styles
