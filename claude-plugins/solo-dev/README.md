# Solo Dev Plugin

Toolkit for solo developers to build, manage, and grow their business.

## Overview

The solo-dev plugin provides tools tailored for indie hackers, solopreneurs, and solo developers who wear many hats. From content creation to business management, these tools help you operate efficiently without a team.

## Components

### Commands

| Command | Description |
|---------|-------------|
| [/craft-voice](#craft-voice) | Start the iterative process to create your AUTHOR_VOICE.md |
| [/write-as-me](#write-as-me) | Generate content in your voice using your AUTHOR_VOICE.md |
| [/define-customer](#define-customer) | Create or refine your CUSTOMER.md ideal customer profile |
| [/define-brand](#define-brand) | Create or refine your BRAND_GUIDELINES.md (requires CUSTOMER.md) |
| [/define-design](#define-design) | Create or refine your DESIGN_GUIDELINES.md (requires CUSTOMER.md) |
| [/audit-ux](#audit-ux) | Audit UI/UX changes in a focus area against design guidelines |
| [/define-seo-strategy](#define-seo-strategy) | Create or refine your SEO_STRATEGY.md covering traditional SEO and AI citations (requires CUSTOMER.md) |
| [/research](#research) | Systematic research with hypothesis tracking for complex investigations |

### Agents

| Agent | Description |
|-------|-------------|
| [voice-writer](#voice-writer) | Generate content in your voice using AUTHOR_VOICE.md |
| [design-research](#design-research) | Analyze customer profile to determine ideal UI/UX design direction |
| [design-quality-auditor](#design-quality-auditor) | Audit DESIGN_GUIDELINES.md for alignment with CUSTOMER.md and BRAND_GUIDELINES.md |
| [ux-auditor](#ux-auditor) | Audit UI/UX changes in a focus area for accessibility, consistency, and usability |
| [seo-researcher](#seo-researcher) | Research SEO and GEO strategies, competitor patterns, and AI platform citation requirements |
| [structured-researcher](#structured-researcher) | Systematic research with hypothesis tracking and confidence calibration |

### Skills

| Skill | Description |
|-------|-------------|
| [author-voice](#author-voice) | Iteratively craft an AUTHOR_VOICE.md that captures your unique writing style for AI replication |
| [customer-profile](#customer-profile) | Iteratively craft a CUSTOMER.md that precisely defines your ideal customer profile |
| [brand-guidelines](#brand-guidelines) | Create BRAND_GUIDELINES.md for voice, tone, and messaging (requires CUSTOMER.md) |
| [design-guidelines](#design-guidelines) | Create DESIGN_GUIDELINES.md for UI/UX design system (requires CUSTOMER.md) |
| [seo-strategy](#seo-strategy) | Create SEO_STRATEGY.md covering traditional SEO and GEO for AI platforms (requires CUSTOMER.md) |

## Commands

### /craft-voice

Start the iterative process to craft your AUTHOR_VOICE.md document for AI-powered content generation in your unique style.

**Usage:**
```bash
/craft-voice
```

**What happens:**
1. Asks 9 multi-choice questions about your voice (content type, personality, vocabulary, etc.)
2. Generates initial AUTHOR_VOICE.md based on your answers
3. Launches voice-writer agent to generate 3 sample texts
4. Collects your ratings and feedback on each sample
5. Updates the document based on feedback
6. Repeats until all samples are perfect or you say it's done

### /write-as-me

Generate content in your authentic voice using your existing AUTHOR_VOICE.md document.

**Usage:**
```bash
/write-as-me a tweet about why most productivity advice is wrong
/write-as-me blog intro on the future of AI coding
/write-as-me  # will ask for topic
```

**What happens:**
1. Locates your AUTHOR_VOICE.md (cwd, home, or searches)
2. Clarifies format if needed
3. Launches voice-writer agent to generate content
4. Iterates based on your feedback until perfect

### /define-customer

Create or refine your CUSTOMER.md document that precisely defines your ideal customer profile (ICP) for product and marketing decisions.

**Usage:**
```bash
/define-customer
```

**What happens:**
1. Checks for existing CUSTOMER.md (refine or start fresh)
2. Asks 10 multi-choice questions about your product, market, and customers
3. Optionally launches parallel research agents to gather ICP data, competitor analysis, and market insights
4. Generates initial CUSTOMER.md based on your answers + research
5. Validates each section with you (ICP definition, pain points, anti-personas)
6. Updates the document based on feedback
7. Repeats until the profile is accurate

### /define-brand

Create or refine your BRAND_GUIDELINES.md that defines how to communicate with your customer. **Requires CUSTOMER.md to exist first.**

**Usage:**
```bash
/define-brand
```

**What happens:**
1. Checks for CUSTOMER.md (stops if not found)
2. Reads CUSTOMER.md to understand who you're talking to
3. Asks questions about brand personality, voice dimensions, language preferences
4. Generates BRAND_GUIDELINES.md with voice, tone, messaging framework, copy patterns
5. Tests with sample copy, collects feedback
6. Iterates until the voice feels right

### /define-design

Create or refine your DESIGN_GUIDELINES.md that defines how to design UI/UX for your customer. **Requires CUSTOMER.md to exist first.** Bakes in the frontend-design skill principles to avoid generic AI aesthetics.

**Usage:**
```bash
/define-design
```

**What happens:**
1. Checks for CUSTOMER.md (stops if not found)
2. Launches design-research agent to analyze CUSTOMER.md and BRAND_GUIDELINES.md (if exists)
3. Agent researches industry design patterns and competitors
4. Presents design direction summary for confirmation
5. Asks targeted questions with agent-informed recommendations pre-filled
6. Generates DESIGN_GUIDELINES.md with full design system tokens
7. Automatic alignment audit (opus agent verifies alignment, fixes issues, repeats until perfect)

### /define-seo-strategy

Create or refine your SEO_STRATEGY.md that defines your complete search optimization strategy—covering both traditional SEO and Generative Engine Optimization (GEO) for AI platforms like ChatGPT, Perplexity, and Google AI Overviews. **Requires CUSTOMER.md to exist first.**

**Usage:**
```bash
/define-seo-strategy
```

**What happens:**
1. Checks for CUSTOMER.md (stops if not found)
2. Checks for existing SEO_STRATEGY.md (update vs start fresh)
3. Collects website URL and product description
4. Launches parallel research agents for industry analysis, competitor structure, and platform requirements
5. Presents research summary for validation
6. Generates SEO_STRATEGY.md with platform-specific sections and effort/impact scoring
7. Validates key sections with you before finalizing

**Output includes:**
- Executive summary with top priority actions
- Customer-aligned strategy (how your ICP searches)
- Traditional SEO foundation (technical, content, authority)
- Platform-specific GEO for Google AI Overviews, ChatGPT, Perplexity, Claude, and Gemini
- Content recommendations with effort/impact matrix
- Implementation roadmap (Quick Wins → Strategic Investments)
- Anti-patterns to avoid

### /audit-ux

Audit UI/UX changes in a specific focus area (e.g., checkout, navigation, forms) against your design guidelines. Checks for accessibility, design system compliance, and usability issues.

**Usage:**
```bash
/audit-ux checkout
/audit-ux navigation
/audit-ux  # will ask for focus area
```

**What happens:**
1. Launches ux-auditor agent with your specified focus area
2. Agent reads DESIGN_GUIDELINES.md and BRAND_GUIDELINES.md
3. Runs `git diff main...HEAD` to identify UI changes in that area
4. Systematically audits each changed file for accessibility, consistency, interaction, layout, and visual issues
5. Produces structured report with prioritized issues (Critical → Low) and recommendations

### /research

Conduct systematic research on complex topics using hypothesis-driven methodology.

**Usage:**
```bash
/research why are our API response times 3x slower after last deployment
/research options for real-time sync between mobile app and backend
/research  # will ask for topic
```

**What happens:**
1. Launches structured-researcher agent with your research question
2. Agent decomposes problem into sub-questions
3. Generates 3-5 competing hypotheses with confidence levels
4. Gathers evidence from codebase, web, and tools
5. Maintains research-notes.md tracking the full investigation
6. Self-critiques at regular intervals to avoid confirmation bias
7. Presents findings with explicit confidence levels and uncertainties

## Agents

### voice-writer

Generates content in your authentic voice using your AUTHOR_VOICE.md specification. Used by both `/craft-voice` (for sample generation during calibration) and `/write-as-me` (for content creation).

The agent reads your voice doc and produces content matching your tone, vocabulary, structure, and signature moves.

### design-research

Analyzes CUSTOMER.md and BRAND_GUIDELINES.md to determine the ideal UI/UX design direction. Used by `/define-design` in Phase 1 (Deep Analysis).

The agent provides comprehensive analysis across 8 areas:
1. **Customer Design Psychology** - Visual preferences, emotional response, frustrations
2. **Recommended Aesthetic Direction** - One decisive pick from 11 aesthetic options with rationale
3. **Typography Recommendation** - Font character, specific suggestions, data vs body treatment
4. **Color Direction** - Theme, accent colors, colors to avoid
5. **Geometry & Motion** - Corners, animation philosophy, information density
6. **Signature Elements** - 2-3 distinctive visual elements
7. **Anti-Patterns** - Design choices that would alienate the ICP
8. **Design Reference Products** - 2-3 products whose aesthetic would resonate

Also performs web research on industry patterns and competitors when applicable.

### design-quality-auditor

Audits DESIGN_GUIDELINES.md for perfect alignment with CUSTOMER.md and BRAND_GUIDELINES.md. Used by `/define-design` for automatic quality verification.

The agent performs systematic checks across 4 categories:
- **Customer Alignment** - Aesthetic direction, information density, motion philosophy match ICP values
- **Brand Alignment** - UI tone, colors, formality match brand guidelines
- **Internal Consistency** - No contradictions, all tokens serve the aesthetic
- **Completeness** - Concrete examples, no gaps

Reports `✅ AUDIT PASSED` or `⚠️ ISSUES FOUND` with specific, actionable fixes prioritized by impact.

### ux-auditor

Audits UI/UX changes in a specific focus area against design guidelines. Used by `/audit-ux` for pre-merge UX reviews, accessibility audits, and design system compliance checks.

The agent performs systematic review across 5 categories:
- **Layout** - Spacing, alignment, grid compliance, responsive breakpoints
- **Accessibility** - WCAG violations, keyboard navigation, ARIA labels, color contrast, focus management
- **Consistency** - Deviations from design system, inconsistent patterns, component misuse
- **Interaction** - Confusing flows, missing feedback, unclear affordances, error handling
- **Visual** - Typography issues, color usage, iconography, visual hierarchy problems

Issues are prioritized as Critical (blocks users), High (significant UX degradation), Medium (noticeable but has workarounds), or Low (polish items).

Read-only operation: produces reports with file:line references and specific recommendations. Does not modify code.

### seo-researcher

Researches SEO and GEO (Generative Engine Optimization) strategies with deep expertise in AI citation patterns. Used by `/define-seo-strategy` to gather current data on industry patterns, competitor structures, and platform requirements.

The agent performs research across three dimensions:
- **Industry Analysis** - SEO best practices specific to the vertical, content formats that perform well, authority signals
- **Competitor Structure** - Content organization, schema markup usage, third-party presence, gaps and opportunities
- **Platform Requirements** - How each AI platform (Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini) selects sources to cite

Key capabilities:
- Uses WebSearch to gather 2025+ data (platforms evolve rapidly)
- Analyzes competitor content structure without accessing private data
- Provides platform-specific optimization tactics
- Flags confidence levels and areas needing validation

Output includes structured findings with specific, actionable recommendations rather than generic SEO advice.

### structured-researcher

Conducts systematic research using hypothesis-driven methodology. Used by `/research` for complex investigations, domain exploration, and debugging unclear issues.

The agent maintains explicit hypothesis trees with confidence levels:
- **Problem Decomposition** - Restates question, identifies sub-questions, defines success criteria
- **Hypothesis Generation** - 3-5 competing hypotheses with initial confidence levels (including contrarian views)
- **Evidence Gathering** - For each evidence: which hypothesis it supports/contradicts, quality assessment, confidence updates
- **Self-Critique** - Regular bias checks, scope assessment, assumption audits

Creates and maintains `research-notes.md` with:
- Research question and hypothesis tree
- Evidence log with confidence updates
- Self-critique log
- Current status, leading hypothesis, and next steps

Confidence scale: 90-100% (near certain), 70-89% (strong belief), 50-69% (leaning), 30-49% (possible), 10-29% (unlikely), 0-9% (eliminated).

## Skills

### author-voice

Create a maximally information-dense AUTHOR_VOICE.md document through iterative refinement. The resulting document enables any LLM to write content that authentically matches your voice.

**Use when you want to:**
- Create a voice profile for consistent content generation
- Train AI to write in your style
- Document your writing preferences for future use

**How it works:**

1. **Discovery** - Multi-choice questions about your voice characteristics and goals
2. **Initial Draft** - Generate first AUTHOR_VOICE.md based on your inputs
3. **Refinement Cycles** - Generate sample texts, rate them, provide feedback, update the doc
4. **Completion** - Final honed document ready for AI content generation

**Usage:**

The skill activates when you mention creating an author voice, writing style guide, or voice profile. Example prompts:

```
Create an author voice document for my writing
Help me capture my writing style for AI
Build a voice profile for my content
```

**Output:**

An `AUTHOR_VOICE.md` file in your working directory that you can feed to any LLM:

```
Read my AUTHOR_VOICE.md, then write a Twitter thread about [topic]
```

**Key features:**
- Multi-choice questions throughout to minimize cognitive load
- voice-writer agent generates sample texts for calibration
- Iterative refinement until samples match your voice
- Information-dense output optimized for LLM consumption

### customer-profile

Create the **foundational** CUSTOMER.md document that precisely defines WHO your customer is. This is the most important document your product will ever have - everything else (features, brand, pricing) derives from it.

**Use when you want to:**
- Define who your ideal customer is (and isn't) from first principles
- Create the foundational doc that all product decisions flow from
- Understand customer problems, behaviors, and what they value
- Build a clear picture before writing code or marketing

**How it works:**

1. **Discovery** - Multi-choice questions about your product and customer understanding (keeps asking until confident)
2. **Research** (optional) - Parallel agents research ICP patterns and competitor positioning
3. **Initial Draft** - Generate first CUSTOMER.md based on inputs + research
4. **Refinement & Completion** - Validate each section, update until accurate

**Usage:**

The skill activates when you mention defining customers, ICP, customer profile, or target audience. Example prompts:

```
Help me define my ideal customer
Create a customer profile for my app
Who should I build this product for?
```

**Output:**

A `CUSTOMER.md` file in your working directory containing:
- ICP definition with specific characteristics
- Anti-personas (who to avoid and why)
- Current state & triggers (what they do today, what makes them seek a solution)
- Pain points in customer voice
- What the ICP values in a solution
- Behavioral and cognitive signals

**Key features:**
- Multi-choice questions throughout to minimize cognitive load
- Keeps asking until gaps are filled (no ambiguity)
- Optional parallel research agents for market data
- Section-by-section validation
- Pure customer definition (no pricing/messaging - save those for downstream docs)

### brand-guidelines

Create the BRAND_GUIDELINES.md document that defines HOW to communicate with your customer. Drives all copy: app UI, marketing, support, emails, everything.

**Prerequisite**: CUSTOMER.md must exist. Run `/define-customer` first.

**Use when you want to:**
- Define your brand's voice and personality
- Create consistent messaging across all touchpoints
- Establish language rules (what to say, what to avoid)
- Build a copy pattern library for different contexts

**How it works:**

1. **Prerequisite Check** - Verifies CUSTOMER.md exists (stops if not)
2. **Discovery** - Questions about brand personality, voice dimensions, language preferences
3. **Draft Generation** - Creates BRAND_GUIDELINES.md
4. **Refinement** - Tests with sample copy, iterates until voice feels right

**Usage:**

The skill activates when you mention brand voice, brand guidelines, messaging, or copy guidelines. Example prompts:

```
Help me define my brand voice
Create brand guidelines for my app
How should my product communicate?
```

**Output:**

A `BRAND_GUIDELINES.md` file containing:
- Voice identity and characteristics
- "We Are / We Are NOT" table
- Tone by context (marketing, UI, errors, support)
- Language rules (USE/AVOID word lists)
- Messaging framework (value props, the hook)
- Copy patterns (headlines, CTAs, errors, empty states)
- Before/after transformations

**Key features:**
- Requires CUSTOMER.md (voice must resonate with WHO you're talking to)
- Tests guidelines with real sample copy
- Tone guidance for different contexts
- Actionable examples, not abstract theory

### design-guidelines

Create the DESIGN_GUIDELINES.md document that defines HOW to design interfaces for your customer. Drives all UI/UX: components, layouts, animations, colors, typography—everything visual. **Bakes in the frontend-design skill to avoid generic AI aesthetics.**

**Prerequisite**: CUSTOMER.md must exist. Run `/define-customer` first.

**Use when you want to:**
- Define your product's visual identity and design system
- Create consistent UI across all screens
- Establish design tokens (colors, typography, spacing, motion)
- Build a component library foundation
- Avoid generic "AI slop" aesthetics

**How it works:**

1. **Prerequisite Check** - Verifies CUSTOMER.md exists (stops if not)
2. **Deep Analysis** - Launches design-research agent to read CUSTOMER.md/BRAND_GUIDELINES.md and research industry patterns
3. **Discovery** - Targeted questions with agent-informed recommendations pre-filled
4. **Generate Document** - Creates DESIGN_GUIDELINES.md with full design system
5. **Automatic Audit** - Opus agent verifies alignment with customer/brand docs, fixes issues, repeats until perfect

**Usage:**

The skill activates when you mention design guidelines, design system, UI guidelines, or visual identity. Example prompts:

```
Help me define my product's design system
Create design guidelines for my app
What should my UI look like?
```

**Output:**

A `DESIGN_GUIDELINES.md` file containing:
- Identity (user, problem, aesthetic direction, signature elements)
- Design tokens (colors, typography, spacing, geometry, shadows, animation)
- Voice & copy in UI context
- Component specifications (cards, buttons, inputs, toasts)
- Layout patterns and visual hierarchy
- Motion philosophy and loading states
- Anti-patterns (what to NEVER do)
- Ship checklist

**Key features:**
- Requires CUSTOMER.md (design must resonate with WHO you're building for)
- Bakes in anti-AI-slop principles (no Inter/Roboto, no purple gradients, no template look)
- Pre-fills recommendations from CUSTOMER.md (speed-focused ICP → terminal aesthetic)
- Tests with sample components before finalizing
- Distinctive design, not generic templates

### seo-strategy

Create the SEO_STRATEGY.md document that defines your complete search optimization strategy—both traditional SEO and Generative Engine Optimization (GEO) for AI platforms.

**Prerequisite**: CUSTOMER.md must exist. Run `/define-customer` first.

**Use when you want to:**
- Define a comprehensive SEO strategy aligned with your ICP
- Optimize for AI citations (not just traditional search rankings)
- Get platform-specific tactics for ChatGPT, Perplexity, Google AI Overviews, Claude, and Gemini
- Prioritize SEO work by effort and impact

**How it works:**

1. **Prerequisite Check** - Verifies CUSTOMER.md exists (stops if not)
2. **Existing Strategy Detection** - Checks for SEO_STRATEGY.md, asks update vs fresh
3. **Input Collection** - Gathers website URL, product description, competitors
4. **Parallel Research** - Launches 3 seo-researcher agents for industry, competitor, and platform analysis
5. **Document Generation** - Creates SEO_STRATEGY.md with prioritized recommendations
6. **Validation Loop** - Reviews sections with you, incorporates feedback

**Usage:**

The skill activates when you mention SEO strategy, GEO, AI citations, or search optimization. Example prompts:

```
Help me create an SEO strategy
How do I get cited by AI platforms?
Build a GEO strategy for my product
```

**Output:**

An `SEO_STRATEGY.md` file containing:
- Executive summary with top 5 priority actions
- Customer-aligned strategy (how your ICP searches)
- Traditional SEO foundation (technical, content, authority)
- Platform-specific GEO sections for each AI platform
- Content recommendations with effort/impact matrix
- Third-party presence strategy
- Implementation roadmap (Quick Wins, Strategic Investments, Maintenance)
- Anti-patterns to avoid

**Key features:**
- Requires CUSTOMER.md (SEO must align with WHO you're targeting)
- Parallel research agents gather current (2025+) data
- Effort/impact scoring for every recommendation
- Platform-specific tactics (each AI platform has different citation patterns)
- Quarterly refresh recommended (platforms evolve rapidly)

## Installation

```bash
/plugin marketplace add /path/to/claude-code-plugins
/plugin install solo-dev@claude-code-plugins-marketplace
```

## Requirements

- Claude Code CLI

## License

MIT

## Contributing

Contributions welcome! This plugin is part of the [claude-code-plugins](https://github.com/doodledood/claude-code-plugins) repository.
