# Prompting and Workflow Strategies for Natural AI Writing

How to get better, more human-sounding output from AI tools through prompt engineering, workflow design, and tool configuration.

## The 10-20-70 Rule

A useful (if approximate) framing: prompting contributes roughly 10% of output quality, editing 20%, and the writer's own domain expertise and personal input 70%. This challenges the idea that prompt engineering alone can produce natural writing. Your knowledge, perspective, and voice are the primary ingredients.

Source: [NestContent](https://nestcontent.com/blog/humanize-chatgpt) (medium authority -- treat as directional, not proven)

---

## Prompt Engineering Techniques

Ranked by evidence strength across independent sources.

### Tier 1: Strongest Evidence (5+ sources)

**Banned word and phrase lists.** Explicitly prohibit AI-associated vocabulary. This is the single highest-impact prompting technique, confirmed across multiple independent practitioners. Treating humanization as a "prohibition problem" (what to avoid) is more reliable than treating it as a stylistic aspiration (what to be).

Example addition to any prompt:
```
Never use these words: delve, tapestry, landscape, realm, robust,
groundbreaking, transformative, seamless, comprehensive, pivotal,
multifaceted, leverage, harness, navigate, foster, catalyze.
Never use: em dashes, semicolons, markdown asterisks.
Never use phrases: "it's worth noting," "in today's fast-paced world,"
"ever-evolving landscape," "It isn't just X, it's Y."
```

**Persona assignment.** Give the AI a specific identity, not just a topic. "Act as if you're explaining [topic] to a colleague over coffee" produces fundamentally different output than "Write about [topic]." The persona changes sentence length, vocabulary, and how it addresses the reader.

**Writing sample matching.** Paste your own writing and instruct: "Analyze this for tone, sentence structure, humor, and emotional depth. Then write about [topic] in the same style. Do not copy the structure verbatim -- use the same style, tone, and emotional depth." Among the most effective techniques when you have existing writing to reference.

### Tier 2: Good Evidence (3-4 sources)

**Conversational framing.** Frame prompts as conversations rather than commands. "Can you tell me some benefits of exercising regularly?" produces more natural text than "List benefits of exercise."

**Negative instructions.** "Don't use formal transitions. Don't start paragraphs with 'It is worth noting.' Don't use more than one semicolon per 500 words." Direct prohibitions give clear boundaries rather than vague aspirations.

**Emotional targeting.** Specify the emotional register: "Write from a place of frustration with the old way of doing things" or "Write with genuine excitement, not manufactured enthusiasm."

### Tier 3: Supporting Evidence (2 sources)

**Short sentence requests.** "Explain [topic] in the simplest way possible. Use short, clear sentences. Break down every idea into a bite-sized chunk." Counteracts AI's tendency toward multi-clause constructions.

**Dramatic paragraph length variation.** Include one-sentence paragraphs for emphasis alongside longer paragraphs. Research confirms human writing has significantly higher burstiness than AI text.

**Layer multiple techniques.** Combine persona + banned words + emotional targeting + writing samples in a single prompt. Individual techniques help; combining them multiplies the effect.

### Temperature and Sampling Settings (API Users)

| Use Case | Temperature | Top_p |
|----------|------------|-------|
| Natural conversational writing | 0.5-0.6 | 0.5-0.6 |
| Creative writing | 0.7 | 0.8 |

Adjust either temperature OR top_p, not both simultaneously.

Sources: [Sabrina Ramonov](https://www.sabrina.dev/p/best-ai-prompt-to-humanize-ai-writing), [Eesel.ai](https://www.eesel.ai/blog/prompts-that-make-ai-write-like-a-human), [Fomo.ai](https://fomo.ai/ai-resources/the-ultimate-copy-paste-prompt-add-on-to-avoid-overused-words-and-phrases-in-ai-generated-content/), [GodOfPrompt](https://www.godofprompt.ai/blog/prompts-that-makes-chatgpt-write-like-a-human), [OpenAI Community](https://community.openai.com/t/cheat-sheet-mastering-temperature-and-top-p-in-chatgpt-api/172683)

---

## Workflow Design

The central principle: **never ask AI to write a complete piece in one shot.**

### The Bookend Approach (Research-Backed)

Use AI at the beginning (ideation, brainstorming) and end (refinement, polishing). The human controls the core creative middle (reasoning, structure, original arguments). Supported by peer-reviewed CHI 2024 research on human-AI co-writing.

### Section-by-Section Iterative Process

1. Have AI develop outline/structure only
2. Draft each section individually with focused prompts
3. Review and provide feedback after each section before proceeding
4. Human provides direction, feedback, and cohesion between iterations

"When you focus the AI on one part of the draft at a time, it can do a better job with each specific task" -- the model doesn't have to split attention across structure, argument, and style simultaneously.

### Six-Stage Professional Workflow (Bronwynne Powell)

1. **Brainstorm** (AI) -- provide detailed context about audience and goals
2. **Outline** (Human only) -- deliberately exclude AI to maintain reasoning control
3. **Research** (Mixed tools) -- use Perplexity, Google Scholar, ChatGPT; always verify AI summaries
4. **Draft** (Flexible) -- write yourself OR co-write; rewrite AI passages in your own voice
5. **Refine** (AI as editor) -- request specific improvements: tighten sections, improve transitions, identify reader objections
6. **Edit** (Mixed) -- Grammarly + ChatGPT + human final review

Philosophy: treat AI as "a small team with different strengths" where the human controls ideas and final decisions.

### The "Messy Draft" Approach

Create a detailed outline with your own scattered thoughts, original angles, and analysis for each section. Feed this substantive-but-rough draft to AI to transform the "80% done, scattered draft into a 100% clean and readable piece." Then edit the cleaned output for voice, accuracy, and strategic alignment.

The key: **your original thinking goes IN before AI touches it.**

### Practical Hybrid Patterns

- AI generates 5-10 ideas; you pick 1-2 and develop them yourself
- You write a rough draft; AI suggests improvements to specific sections
- AI produces a structured outline; you write the prose
- You dictate thoughts (stream of consciousness); AI organizes and cleans up
- AI identifies gaps in your argument; you fill them with original content

Sources: [ACM CHI 2024](https://dl.acm.org/doi/10.1145/3613904.3642134), [Magai](https://magai.co/chatgpt-writing-process-steps/), [Bronwynne Powell](https://bronwynnepowell.com/ai-writing-process/), [Marketer Milk](https://www.marketermilk.com/blog/ai-marketing-workflow)

---

## Tool-Specific Strategies

### Claude

Consistently produces the most natural, publication-ready prose across multiple comparison tests. Handles varied styles well -- conversational, casual, professional, and humorous styles are largely successful.

**Built-in Styles feature**: 4 presets (Normal, Concise, Formal, Explanatory) plus custom styles. Create custom styles by uploading writing samples (PDF, DOC, TXT) or pasting text directly.

**Prompting best practices** (official Anthropic docs):
- Use XML tags for structured prompts
- Provide 3-5 diverse examples wrapped in `<example>` tags
- Be explicit about who, what, audience, constraints, and definition of success
- Explain WHY, not just WHAT

Claude 4.5 models are more concise and natural by default compared to earlier versions.

### ChatGPT

Best for warm marketing copy, emails, and long-form articles. GPT-5 sometimes overshoots toward "too artistic or overly formal."

**Custom Instructions** (persistent): Two text boxes (1,500 chars each). Box 1: personal/professional context. Box 2: response style preferences. Applied to ALL conversations. Save your banned word list and voice preferences here once.

Include: "Never mention you're an AI. Avoid disclaimers. Skip directly to answering."

### Gemini

Best used in research stages of a multi-tool pipeline. Adds factual and web-sourced information naturally.

### Multi-Tool Pipeline

Rather than relying on a single AI tool, use different tools for different stages:
- Perplexity or Google Scholar for research
- ChatGPT or Claude for drafting
- Grammarly for mechanical editing
- Human judgment throughout

Sources: [Claude Help Center - Styles](https://support.claude.com/en/articles/10181068-configure-and-use-styles), [Anthropic Multishot Prompting](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/multishot-prompting), [OpenAI Custom Instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions), [Type.ai comparison](https://blog.type.ai/post/claude-vs-gpt)

---

## Building a Personal Style Library

### Step-by-Step Process

1. **Gather writing samples**: 3-10 pieces, minimum 200-600 words total. Use high-impact pieces that genuinely capture your voice (standout blog posts, key emails, best work).
2. **Analyze your style**: Submit samples to AI with: "Analyze these for tone & voice, vocabulary, sentence structure, and formatting quirks."
3. **Generate outputs**: A style analysis (patterns identified), a style guide (concrete rules), and a reusable prompt template.
4. **Include negative examples**: Provide writing that does NOT match your voice with explanation: "This is NOT my style because it uses formal transitions and passive voice."
5. **Build context-specific prompts**: Different prompts for different contexts -- professional emails vs. blog posts vs. social media.
6. **Iterate**: Treat the AI like a junior writer you're mentoring. Give feedback on what's working and what isn't.

"One perfect example beats a dozen mediocre ones." Too many mixed-quality samples dilute voice consistency.

**Tool integration**: Claude supports direct upload of writing samples for automatic style creation. ChatGPT's Custom Instructions have a 1,500-character limit, so use them for the distilled style guide rather than raw samples.

Sources: [Office Watch](https://office-watch.com/2025/create-ai-writing-style-prompts/), [SEOwind](https://seowind.io/tone-of-voice-examples-ai/), [PressMaster](https://www.pressmaster.ai/article/how-ai-tools-standardize-writing-styles)

---

## Power User Techniques

Techniques that surface repeatedly across forums, newsletters, and practitioner blogs:

**The em-dash ban is surprisingly impactful.** Em dashes are one of the most reliable AI tells. Banning them forces the model to construct sentences differently. Also ban semicolons and markdown asterisks.

**Inject casual language markers.** Explicitly instruct: "Use informal connectors like 'So,' 'Anyway,' 'By the way,' and phrases like 'if I recall correctly,' 'I've found that,' 'in my experience.'" Small markers, disproportionate difference.

**Request imperfection.** "Not every line needs to sound perfect" gives the model permission to write with natural roughness rather than optimizing every sentence.

**Target 7th grade readability.** Pushes the model away from complex, multi-clause sentences that signal AI generation.

**Add opinions.** Instruct to include "I think" or "in my experience" statements. A neutral information bot sounds like AI; a person with views sounds human.

**Research-driven content beats prompt-engineered content.** Feeding actual keyword research, competitor analysis, and domain expertise produces more authentic results than clever prompt tricks alone. This circles back to the 10-20-70 Rule.
