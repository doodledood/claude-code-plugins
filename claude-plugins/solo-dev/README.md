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

### Agents

| Agent | Description |
|-------|-------------|
| [voice-writer](#voice-writer) | Generate content in your voice using AUTHOR_VOICE.md |

### Skills

| Skill | Description |
|-------|-------------|
| [author-voice](#author-voice) | Iteratively craft an AUTHOR_VOICE.md that captures your unique writing style for AI replication |
| [customer-profile](#customer-profile) | Iteratively craft a CUSTOMER.md that precisely defines your ideal customer profile |

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

## Agents

### voice-writer

Generates content in your authentic voice using your AUTHOR_VOICE.md specification. Used by both `/craft-voice` (for sample generation during calibration) and `/write-as-me` (for content creation).

The agent reads your voice doc and produces content matching your tone, vocabulary, structure, and signature moves.

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
