# writing

All writing skills in one place. Research-backed anti-AI prose principles, author voice capture, and voice-matched content generation.

## Architecture

```
writing/
├── skills/
│   ├── human-writing/          # Base knowledge — anti-AI writing principles
│   │   ├── SKILL.md            # Distilled principles + reference navigation
│   │   └── references/         # Full research files (4 documents, 70+ sources)
│   ├── write/                  # Workflow — iterative write + review loop
│   │   └── SKILL.md
│   ├── craft-author-voice/     # Voice capture — create AUTHOR_VOICE.md
│   │   └── SKILL.md
│   └── write-as-me/            # Voice generation — write in your style
│       └── SKILL.md
└── agents/
    ├── writing-reviewer.md     # Reviews prose for AI tells
    └── voice-writer.md         # Generates content in author's voice
```

**Component flow:**
- `human-writing` (base) — invoked by `writing-reviewer`, `write`, and `voice-writer`
- `writing-reviewer` (agent) — invoked by `write` for review loop
- `voice-writer` (agent) — invoked by `write-as-me` and `craft-author-voice`
- `write` (workflow) — user-invoked or auto-triggered for prose tasks
- `craft-author-voice` — user-invoked to capture writing style
- `write-as-me` — user-invoked to generate content in your voice

## Skills

### human-writing

Base knowledge skill with distilled AI writing research. Auto-invoked for prose/content writing tasks.

Covers: vocabulary kill-list, four-layer editing system, seven craft fundamentals, structural/rhetorical/tonal anti-patterns, prompting techniques, workflow principles, statistical signatures, detection science.

### write

Full writing workflow with iterative review loop. Gathers your context (the 70%), writes with principles applied, reviews via writing-reviewer agent, auto-fixes HIGH+ issues, loops until clean.

Handles flexible input: topic only, outline, rough draft, or finished text for editing.

### craft-author-voice

Captures your writing style into an AUTHOR_VOICE.md document through iterative refinement with feedback cycles. The resulting document enables voice-matched content generation.

### write-as-me

Generates content in your voice using your AUTHOR_VOICE.md document. Delegates to the voice-writer agent, which applies both your voice profile and anti-AI writing principles.

## Agents

### writing-reviewer

Reviews prose for AI tells. Reports findings with severity (CRITICAL/HIGH/MEDIUM/LOW) and fixability tags (AUTO_FIXABLE/NEEDS_HUMAN_INPUT). Never modifies files.

### voice-writer

Generates content matching the author's voice from AUTHOR_VOICE.md. Applies anti-AI writing principles from human-writing alongside the author's style.

## Usage

```bash
# Write prose with anti-AI review loop
/write Write a blog post about why AI-generated content fails with readers

# Apply writing principles to current task (auto-invoked or manual)
/human-writing

# Capture your writing voice
/craft-author-voice

# Generate content in your voice
/write-as-me Write a tweet about productivity
```

## Research Foundation

Based on 70+ sources covering:
- **AI tells and fingerprints** — vocabulary, structural, rhetorical, tonal, and statistical patterns
- **Humanizing playbook** — editing systems, voice development, craft fundamentals, professional workflows
- **Prompting and workflow** — prompt engineering techniques, hybrid workflows, tool-specific strategies
- **Detection science** — how detection works, accuracy data, evasion methods, theoretical limits

Full research documents in `skills/human-writing/references/`.
