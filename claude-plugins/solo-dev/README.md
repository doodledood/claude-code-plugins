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

### Skills

| Skill | Description |
|-------|-------------|
| [author-voice](#author-voice) | Iteratively craft an AUTHOR_VOICE.md that captures your unique writing style for AI replication |

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
3. Launches sonnet agent to generate 3 sample texts
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
2. Reads and internalizes your voice parameters
3. Clarifies format and length if needed
4. Generates content matching your voice
5. Iterates based on your feedback until perfect

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
- Sonnet agent generates sample texts for calibration
- Iterative refinement until samples match your voice
- Information-dense output optimized for LLM consumption

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
