---
description: Start the iterative process to craft your AUTHOR_VOICE.md document for AI-powered content generation in your unique style.
allowed-tools: ["Read", "Write", "Edit", "Task", "AskUserQuestion"]
---

# Craft Author Voice

You are starting the author voice crafting process. This will create an AUTHOR_VOICE.md document that captures the user's unique writing style for AI replication.

## Process Overview

1. **Discovery Phase**: Ask multi-choice questions to understand voice characteristics
2. **Initial Draft**: Generate the first AUTHOR_VOICE.md
3. **Refinement Cycles**: Generate samples, collect feedback, iterate until perfect
4. **Completion**: Deliver the final polished document

## Phase 1: Discovery

Use **AskUserQuestion** for EVERY question with multi-choice options to minimize cognitive load.

### Question 1: Primary Content Type

Use AskUserQuestion:
- header: "Content Type"
- question: "What's your PRIMARY content format?"
- options:
  - "Twitter/X posts (short-form, punchy)"
  - "LinkedIn posts (professional, insights)"
  - "Blog articles (long-form, detailed)"
  - "Newsletter (conversational, regular)"
  - "Technical documentation (precise, instructional)"
  - "Mixed - I write across multiple formats"

### Question 2: Voice Personality

Use AskUserQuestion:
- header: "Voice Tone"
- question: "How would you describe your voice personality? (pick up to 2)"
- multiSelect: true
- options:
  - "Authoritative expert - confident, direct, no-nonsense"
  - "Friendly mentor - approachable, encouraging, educational"
  - "Provocateur - contrarian, challenges assumptions, bold"
  - "Storyteller - narrative-driven, uses examples, personal"
  - "Analyst - data-driven, logical, objective"
  - "Conversational peer - casual, relatable, human"

### Question 3: Signature Elements

Use AskUserQuestion:
- header: "Signatures"
- question: "What signature elements define your writing?"
- multiSelect: true
- options:
  - "Strong opening hooks"
  - "Numbered lists and frameworks"
  - "Personal anecdotes and stories"
  - "Contrarian takes and hot takes"
  - "Data and research citations"
  - "Metaphors and analogies"
  - "Direct calls-to-action"
  - "Questions to engage readers"

### Question 4: Vocabulary Style

Use AskUserQuestion:
- header: "Vocabulary"
- question: "What's your vocabulary style?"
- options:
  - "Simple and accessible - anyone can understand"
  - "Technical jargon - domain-specific terms expected"
  - "Casual slang - internet-native, memes okay"
  - "Formal professional - polished, corporate-appropriate"
  - "Academic - precise, nuanced, scholarly"

### Question 5: Emotional Range

Use AskUserQuestion:
- header: "Emotion"
- question: "What emotions do you convey in your writing?"
- multiSelect: true
- options:
  - "Enthusiasm and excitement"
  - "Calm confidence"
  - "Urgency and importance"
  - "Humor and wit"
  - "Empathy and understanding"
  - "Skepticism and critical thinking"
  - "Inspiration and motivation"

### Question 6: Target Audience

Use AskUserQuestion:
- header: "Audience"
- question: "Who is your primary audience?"
- options:
  - "Developers/Engineers"
  - "Founders/Entrepreneurs"
  - "Product managers"
  - "Executives/Leaders"
  - "General tech audience"
  - "Non-technical professionals"
  - "Students/Learners"

### Question 7: Writing Goals

Use AskUserQuestion:
- header: "Goals"
- question: "What do you want your writing to achieve?"
- multiSelect: true
- options:
  - "Build authority and thought leadership"
  - "Drive engagement and discussion"
  - "Educate and inform"
  - "Entertain and delight"
  - "Convert/sell (subtly)"
  - "Build community and connection"

### Question 8: Anti-patterns

Use AskUserQuestion:
- header: "Avoid"
- question: "What should your writing NEVER do?"
- multiSelect: true
- options:
  - "Use corporate buzzwords"
  - "Sound robotic or AI-generated"
  - "Be preachy or condescending"
  - "Use excessive emojis"
  - "Be overly promotional"
  - "Use clickbait tactics"
  - "Be wishy-washy or hedging"
  - "Use filler phrases"

### Question 9: Sample Topics

Use AskUserQuestion:
- header: "Topics"
- question: "What topics do you frequently write about?"
- freeform: true (allow text input)
- hint: "List 2-3 topics, or paste examples of your past writing"

## Phase 2: Generate Initial Document

After collecting all answers, generate `AUTHOR_VOICE.md` in the current directory using this structure:

```markdown
# AUTHOR_VOICE.md

> This document defines [Author]'s writing voice for AI content generation.
> Feed this to any LLM before requesting content to match the author's style.

## Voice Identity

[1-2 sentences capturing the core voice essence based on discovery answers]

## Tone Parameters

- **Primary tone**: [derived from voice personality answers]
- **Emotional range**: [from emotional range answers]
- **Formality level**: [1-10 scale based on vocabulary style]
- **Warmth level**: [1-10 scale based on personality]

## Structural Patterns

- **Opening style**: [based on signature elements]
- **Paragraph length**: [inferred from content type]
- **List usage**: [from signature elements]
- **Closing style**: [inferred from goals]

## Vocabulary Rules

### USE:
- [Specific words/phrases based on vocabulary style]
- [Domain terms based on audience]

### AVOID:
- [Based on anti-patterns selected]

## Signature Moves

1. [From signature elements]
2. [From signature elements]
3. [From signature elements]

## Anti-Patterns

NEVER:
- [From anti-patterns selected]

## Quick Reference

**One-line voice summary**: [Concise description]

**Before generating content, ensure**:
- [ ] Matches tone parameters
- [ ] Uses vocabulary rules
- [ ] Includes signature moves
- [ ] Avoids anti-patterns
```

## Phase 3: Refinement Cycles

After writing the initial document:

1. Use the **Task tool** with `model: "sonnet"` to generate 3 sample texts:
   - A short-form post (~280 chars)
   - A medium post opening (2-3 paragraphs)
   - A response to a hypothetical question in the user's domain

2. For EACH sample, use AskUserQuestion:
   - header: "Sample [N]"
   - question: "Rate this sample: [show the text]"
   - options: ["Perfect - captures my voice", "Close - minor tweaks", "Okay - something's off", "Wrong - doesn't sound like me"]

3. If not "Perfect", follow up:
   - header: "Feedback"
   - question: "What needs adjustment?"
   - multiSelect: true
   - options: ["Too formal", "Too casual", "Wrong vocabulary", "Missing signature style", "Tone is off", "Structure wrong", "Too wordy", "Too choppy", "Other"]

4. Update AUTHOR_VOICE.md based on feedback patterns

5. Ask if user wants another cycle:
   - header: "Continue?"
   - question: "Run another refinement cycle?"
   - options: ["Yes - generate more samples", "No - document is good", "One more cycle"]

Repeat until user indicates completion.

## Phase 4: Completion

When done, add version info and usage instructions to the document, then confirm the file location to the user.
