# human-writer

Research-backed toolkit for writing prose that doesn't sound or feel AI-generated. Distills findings from 70+ sources across peer-reviewed studies, professional writing coaches, and practitioner workflows into actionable skills.

## Architecture

Mirrors the `prompt-engineering` plugin pattern:

```
human-writer/
├── skills/
│   ├── human-writing/          # Base knowledge (like prompt-engineering)
│   │   ├── SKILL.md            # Distilled principles + reference navigation
│   │   └── references/         # Full research files (4 documents)
│   └── write/                  # Workflow skill (like auto-optimize-prompt)
│       └── SKILL.md
└── agents/
    └── writing-reviewer.md     # Review agent (like prompt-reviewer)
```

**Component flow:**
- `human-writing` (base) ← invoked by both `writing-reviewer` and `write`
- `writing-reviewer` (agent) ← invoked by `write` for review loop
- `write` (workflow) ← user-invoked or auto-triggered for prose tasks

## Skills

### human-writing

Base knowledge skill containing distilled AI writing research. Auto-invoked for prose/content writing tasks.

Covers: vocabulary kill-list, four-layer editing system, seven craft fundamentals AI structurally cannot produce, structural/rhetorical/tonal anti-patterns, prompting techniques, workflow principles, statistical signatures, detection science.

### write

Full writing workflow with iterative review loop:

1. Gathers your context (key points, opinions, experiences — the 70%)
2. Writes content applying human-writing principles
3. Reviews via writing-reviewer agent
4. Auto-fixes HIGH+ severity issues
5. Loops until reviewer finds no HIGH+ issues
6. Delivers clean draft with completion report

Handles flexible input: topic only, outline, rough draft, or finished text for editing.

## Agents

### writing-reviewer

Reviews prose against research-backed criteria. Reports findings with severity (CRITICAL/HIGH/MEDIUM/LOW) and fixability tags (AUTO_FIXABLE/NEEDS_HUMAN_INPUT). Never modifies files.

Categories: vocabulary, structure, tone, rhetoric, craft, negative space.

## Usage

```bash
# Invoke the full writing workflow
/write Write a blog post about why AI-generated content fails with readers

# Apply writing principles to current task (auto-invoked or manual)
/human-writing

# Review existing text for AI tells
# (writing-reviewer is invoked by /write, not directly)
```

## Research Foundation

Based on comprehensive research covering:
- **AI tells and fingerprints** — vocabulary, structural, rhetorical, tonal, and statistical patterns
- **Humanizing playbook** — editing systems, voice development, craft fundamentals, professional workflows
- **Prompting and workflow** — prompt engineering techniques, hybrid workflows, tool-specific strategies
- **Detection science** — how detection works, accuracy data, evasion methods, theoretical limits

Full research documents available in `skills/human-writing/references/`.
