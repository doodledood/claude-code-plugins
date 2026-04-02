---
name: audit-ux
description: "Audit UI/UX changes in a focus area against design guidelines, accessibility standards (WCAG), and design system compliance. Performs read-only analysis of changed UI files, checking layout, accessibility, consistency, interaction patterns, and visual hierarchy. Use when the user asks for a UX review, UI audit, accessibility check, design system compliance review, or wants to validate UI changes before merging."
---

Launch the ux-auditor agent to perform a comprehensive UX audit of the specified focus area.

Focus area: $ARGUMENTS

---

The ux-auditor agent performs a read-only audit scoped to the specified focus area (e.g., "checkout", "navigation", "forms"):

1. **Gather references** — reads design system docs, brand guidelines, and accessibility requirements
2. **Identify changes** — runs `git diff main...HEAD` to scope the audit to recent UI modifications in the focus area
3. **Systematic review** — checks each changed UI file against design documentation, WCAG standards, interaction patterns, responsive behavior, and visual hierarchy
4. **Report findings** — produces a structured report grouped by priority (Critical / High / Medium / Low)

## Issue categories

- **Layout**: spacing, alignment, grid compliance, responsive breakpoints
- **Accessibility**: WCAG violations, keyboard navigation, ARIA labels, color contrast, focus management
- **Consistency**: design system deviations, inconsistent patterns, component misuse
- **Interaction**: confusing flows, missing feedback, unclear affordances
- **Visual**: typography issues, color usage, visual hierarchy problems

## Output

A structured UX Audit Report with issues grouped by priority, each containing file references, category, description, user impact, and a specific fix recommendation. This skill is read-only — it reports findings without modifying files.
