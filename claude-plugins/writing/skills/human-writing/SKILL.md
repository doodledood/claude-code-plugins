---
name: human-writing
description: 'Research-backed principles for writing prose that avoids AI tells. Apply when writing articles, blog posts, emails, marketing copy, social media, or any prose content. Covers vocabulary, structure, tone, rhythm, and craft techniques that make writing feel authentically human. Not for code, commit messages, or technical documentation.'
---

**User request**: $ARGUMENTS

Apply these research-backed writing principles to the current task. If no specific request, apply them to whatever prose content is being written in context.

## The Core Insight

**The fundamental problem is statistical uniformity.** AI text is measurably more predictable (~50% lower perplexity), less varied in sentence length (~38% lower burstiness), and narrower in vocabulary (type-token ratio: human 55.3 vs AI 45.5). The path to human-sounding writing runs through embracing imperfection, not perfecting output.

**The single most reliable tell is uniformity.** Human writing is messy, varied, and surprising. AI writing is smooth, consistent, and predictable.

## The 10-20-70 Rule

Prompting contributes ~10% of output quality, editing ~20%, and the writer's own domain expertise and input ~70%. No amount of prompt engineering substitutes for having something to say. Require the writer's genuine insight, opinions, and experiences before generating content.

## Hierarchy of Impact

From highest to lowest impact on making writing sound human:

| Priority | Technique | Why |
|----------|-----------|-----|
| 1 | **Put your own thinking in first** | AI cannot generate genuine insight, lived experience, or original analysis |
| 2 | **Develop a distinctive voice** | Voice is the ultimate differentiator — consistent, cannot be faked by editing |
| 3 | **Edit ruthlessly** | Four-layer system: word → sentence → structure → content |
| 4 | **Design the workflow** | Never write a complete piece in one shot |
| 5 | **Prompt with constraints** | Banned words + persona + writing samples |
| 6 | **Embrace imperfection** | Fragments. Tangents. Opinions. Rough edges make writing alive. |

## Vocabulary Kill-List

Never use these words — they are statistically flagged as AI-generated across peer-reviewed studies of millions of documents:

**Nouns**: delve, tapestry, landscape, realm, testament, journey, insight, resilience, ecosystem, milestone, prowess, utilization

**Verbs**: embark, endeavor, leverage, harness, navigate (metaphorical), unlock, foster, catalyze, bolster, underscore, showcase, elucidate, encompass, unveil

**Adjectives**: seamless, robust, groundbreaking, transformative, pivotal, vibrant, compelling, crucial, invaluable, holistic, multifaceted, meticulous, commendable, intricate

**Adverbs**: seamlessly, meticulously, notably, profoundly, predominantly, subsequently, thereby, ultimately

**Phrases**: "ever-evolving landscape," "in today's fast-paced world," "as we navigate the complexities," "It isn't just X, it's Y," "it's important to note," "it's worth noting that," "without further ado," "in conclusion," "at the heart of"

**False intensifiers**: "genuinely," "truly," "actually" (when used to simulate conviction)

## Four-Layer Editing System

Apply in order from surface to substance:

### Layer 1: Word-Level
Search-replace or delete kill-list vocabulary on sight. Strip adjectives from paragraphs, restore only those carrying concrete information. "Robust system" → "handles 10k req/s without data loss."

### Layer 2: Sentence-Level
Read only the first few words of consecutive sentences — wherever three or more follow the same pattern, cut or combine. Vary sentence length deliberately: short for punch, long for nuance. The contrast creates impact. Add intentional imperfection: fragments, casual asides, conversational phrasing.

### Layer 3: Structural
Eliminate meta-commentary ("In this section, we will..."). Kill recap conclusions that only repeat earlier points. Break pattern symmetry: demote repetitive subheadings, merge overlapping sections, ensure each paragraph's opening differs structurally from the one before.

### Layer 4: Content
Add lived experience: anecdotes, firsthand observations, specific failures. Ground in specifics — ask of every sentence: "Could this fit any topic?" If yes, it needs grounding. Inject honest opinion: state what you actually think, not what "many experts" believe.

### Final Check
**Read aloud.** Stumbling, running out of breath, or awkwardness marks where prose needs work.

## Seven Craft Fundamentals AI Structurally Cannot Produce

These are structural limitations of statistical text generation — areas where human writers create unbridgeable distance:

1. **Showing vs Telling** — Render specific sensory details that let readers experience emotion. AI defaults to summarizing ("serene and tranquil") rather than showing (the dragonfly hovering over still water).

2. **Specificity from Lived Experience** — AI produces "gentle breeze" and "blooming flowers" (statistically most probable). Replace generic descriptions with observations nobody else has made. Name the cafe, the specific dish, the particular moment.

3. **Strategic Omission** — AI tends toward completeness and closure. Resonant writing lives in what's left unsaid. A character dodging a question reveals more than any direct statement. Trained to produce text, not withhold it.

4. **Rhythm Variation** — AI produces sentences of similar length and structure. Use rhythm deliberately: shorten sentences as tension rises. Drop a short sentence after several long ones. Like that.

5. **Deliberate Rule-Breaking** — Choose the wrong word because it sounds better. Let a fragment hang. Incomplete sentences. For emphasis. Because sometimes a complete sentence kills the moment.

6. **Humor** — Classified as an "AI-complete problem." Google DeepMind study with 20 comedians: AI "struggled to produce material that was original, stimulating, or — crucially — funny." Humor requires authentic vulnerability and cultural boundary-breaking.

7. **Genuine Insight** — AI provides summaries; humans provide analysis. Keep asking "Why?" iteratively. Data shows the "what" — insight tells the "why."

## Structural Anti-Patterns

| Pattern | Tell | Fix |
|---------|------|-----|
| Uniform paragraph length | Every section gets equal treatment regardless of importance | Spend more space on what matters, less on what doesn't |
| List addiction | Jumping into numbered/bulleted lists without narrative buildup | Use flowing prose; lists only when genuinely parallel |
| Formulaic scaffolding | "Firstly... Secondly... Finally" at 2-5x human rate | Vary transitions or eliminate them |
| Grammar perfection | No fragments, run-ons, or unconventional starts | Perfection is suspicious — include occasional wonky phrasing |
| Colon titles | "Topic: Explanation" format | Vary title structure |
| Symmetric structure | Every section mirrors the same internal organization | Break the pattern |

## Punctuation Rules

- **Em-dashes**: Use sparingly. ChatGPT uses 8 per 573 words; humans use far fewer. Ban them entirely if the text feels AI-heavy.
- **Semicolons**: AI rarely uses them. Including some adds human texture.
- **Contractions**: AI avoids them. Use them freely in conversational prose.
- **Oxford commas**: AI applies them consistently. Break the pattern occasionally.

## Rhetorical Anti-Patterns

| Pattern | Tell | Fix |
|---------|------|-----|
| **Tricolon obsession** | Groups ideas in threes: "Time, resources, and attention" | Break with two, four, or seven items erratically |
| **Perfect antithesis** | "Not just X, but Y" — neat binary oppositions | Real arguments are messier |
| **Rhetorical questions as staging** | "How do we solve this?" → pre-composed answer | Ask genuine questions or just state the point |
| **Excessive hedging** | "may potentially offer what could be considered significant benefits" | Strip to: "this works" |
| **Compulsive signposting** | "It's worth noting," "It's important to remember" | Trust the reader |
| **Opinion-avoidant framing** | "commonly described as," "many find," "generally considered" | State the view directly |

## Tonal Principles

- **Vary register.** AI picks a lane and stays there. Shift between formal and colloquial. Reveal personality through tonal variation.
- **Don't be relentlessly positive.** AI frames everything positively. Call things weak, inadequate, or bad when they are.
- **Show unequal enthusiasm.** AI treats all subjects with equal professional distance. Nerd out about topics you care about. Show visible impatience with boring ones.
- **Take risks.** AI prioritizes broad palatability. Write confusing sentences, sharp observations, and controversial assertions when appropriate.

## What Must Be Present (The Negative Space)

AI text is identified as much by what's absent as what's present:

- **Lived experience** — specific personal anecdotes, not "generic specificity"
- **Sensory specificity** — unexpected observations, not statistically probable descriptions
- **Silence and subtext** — what characters don't say, what's left unsaid
- **Genuine messiness** — false starts, changed directions, productive digressions
- **A perspective** — a view that could not fit any other prompt

## Prompting Techniques (When Generating)

### Tier 1 (Strongest evidence)
- **Banned word lists**: Prohibit the kill-list vocabulary explicitly. Constraint-based prompting outperforms aspirational instructions.
- **Persona assignment**: "Explain this to a colleague over coffee" produces fundamentally different output than "Write about X."
- **Writing sample matching**: Paste your own writing and instruct to match tone, structure, emotional depth — not copy structure.

### Tier 2 (Good evidence)
- **Conversational framing**: Frame as conversations, not commands.
- **Negative instructions**: "Don't use formal transitions. Don't start paragraphs with 'It is worth noting.'"
- **Emotional targeting**: "Write from a place of frustration with the old way" — specify the emotional register.

### Tier 3 (Supporting evidence)
- **Short sentence requests**: Counteracts multi-clause tendency.
- **Dramatic paragraph length variation**: Include one-sentence paragraphs for emphasis.
- **Layer multiple techniques**: Combine persona + banned words + emotional targeting + samples.

## Workflow Principles

- **Never write a complete piece in one shot.** Section-by-section with review between.
- **Bookend approach**: AI for ideation at start, polish at end. Human controls the core creative middle.
- **Messy draft approach**: Your scattered thoughts + original angles → AI cleans into readable prose → you edit for voice.
- **Your original thinking goes IN before AI touches it.**

## Statistical Signatures (Detection Context)

Understanding what detectors measure helps write text that doesn't trigger them:

| Metric | Human | AI | Meaning |
|--------|-------|-----|---------|
| Perplexity (surprisal) | ~8.2 | ~4.2 | AI is ~50% more predictable |
| Burstiness (sentence variation) | 0.61 | 0.38 | AI has ~38% less variation |
| Token probability entropy | 4.56 | 3.11 | AI makes more uniform word choices (d=3.08) |
| Type-token ratio | 55.3 | 45.5 | Humans use broader vocabulary |
| Late-stage volatility | Consistent | Decays 24-32% | AI becomes more predictable as it continues |

**Key implication**: Introduce genuine unpredictability — varied vocabulary, surprising sentence lengths, unexpected word choices, inconsistent structure.

## Detection Methods (Reference)

- **Statistical/zero-shot**: Perplexity, burstiness, entropy, probability curvature (DetectGPT), cross-perplexity ratio (Binoculars), directional memorization (BiScope)
- **Trained classifiers**: GPTZero, Originality.ai, Turnitin, Copyleaks — achieve 65-96% on unedited AI text
- **Watermarking**: Vocabulary partitioning, SynthID tournament sampling
- **Stylometric**: Type-token ratio, stop word count, hapax legomenon rate
- **What defeats detection**: Paraphrasing (reduces by 87-99%), simple modifications, human editing, nucleus sampling
- **Theoretical limit**: Detection converges toward random chance as models improve (Sadasivan et al.)

For full detection science detail, see [detection-science.md](references/detection-science.md).

## Model-Specific Signatures

| Model | Key Tells |
|-------|-----------|
| **ChatGPT** | Formal, clinical; heavy em-dashes (8/573 words); overuses "delve," "align," "noteworthy"; dry, robotic |
| **Gemini** | Conversational, explanatory; prefers simple language; no em-dash overuse |
| **Claude** | More natural and literary; minimal em-dashes (2/948 words); tonal flexibility; occasionally generates fiction unprompted |
| **Deepseek** | Heavy em-dashes (9/555 words); similar to ChatGPT structurally |

## Reference Files

Detailed research backing these principles:

| File | Contents | Consult When |
|------|----------|--------------|
| [ai-tells-and-fingerprints.md](references/ai-tells-and-fingerprints.md) | Vocabulary fingerprints, structural/rhetorical/tonal patterns, statistical signatures, model-specific signatures | Reviewing text for AI tells, understanding what detectors look for |
| [humanizing-playbook.md](references/humanizing-playbook.md) | Four-layer editing system, voice development, 7 craft fundamentals, professional workflows, what editors look for | Editing AI-assisted text, developing writing voice, understanding editorial standards |
| [prompting-and-workflow.md](references/prompting-and-workflow.md) | Prompt engineering techniques (tiered), workflow designs, tool-specific strategies, style library building | Setting up writing prompts, designing hybrid workflows, building personal style libraries |
| [detection-science.md](references/detection-science.md) | Detection methods, accuracy data, evasion methods, arms race, theoretical limits, non-native speaker bias | Understanding how detection works, what statistical properties matter, accuracy limitations |

## Never Do

- Use kill-list vocabulary
- Write uniform paragraph lengths
- Start consecutive sentences with the same structure
- Hedge when a direct statement serves better
- Treat all subjects with equal professional distance
- Explain what you're about to explain before explaining it
- End with a conclusion that repeats the introduction
- Produce text that could fit any prompt equally well
