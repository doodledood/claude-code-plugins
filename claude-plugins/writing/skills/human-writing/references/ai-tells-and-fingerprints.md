# AI Writing Tells and Fingerprints

What specific patterns make writing identifiable as AI-generated -- both what detection tools measure and what human readers intuitively notice.

## The Vocabulary Fingerprint

AI draws from a specific, identifiable word palette that appears with statistically abnormal frequency. Two peer-reviewed studies of millions of academic papers have quantified this:

**Scale of the signal**: Analysis of 14 million PubMed abstracts found 280 style words with elevated frequency post-ChatGPT, with "delve" showing the highest excess ratio (r=25.2). A separate study of 27.5 million PubMed records confirmed 103 of 135 AI-influenced terms showed meaningful increases by 2024. The word "commendable" saw a 245% increase in academic papers.

**The AI vocabulary catalog**:

| Category | Characteristic AI Words |
|----------|------------------------|
| **Nouns** | delve, tapestry, landscape, realm, testament, journey, insight, resilience, ecosystem, milestone, prowess, utilization |
| **Verbs** | embarked, embraced, enhanced, illuminated, navigated, resonated, transcended, harness, underscore, showcase, encompass, foster, leverage, unveil, bolster, catalyze |
| **Adjectives** | crucial, comprehensive, robust, multifaceted, pivotal, profound, meticulous, nuanced, innovative, invaluable, holistic, commendable, intricate, groundbreaking, transformative |
| **Adverbs** | seamlessly, significantly, profoundly, meticulously, notably, particularly, additionally, predominantly, subsequently, thereby, ultimately |
| **Hedging phrases** | "it's important to note," "it's worth noting that," "it could be argued," "this might suggest" |
| **Generic openers** | "in conclusion," "at the heart of," "in today's fast-paced world," "without further ado" |
| **False intensifiers** | "genuinely," "truly," "actually" (used to simulate conviction rather than convey it) |

### Era-tracked vocabulary (snapshot as of 2026-04-27)

AI vocabulary shifts over time as models are retrained. Wikipedia tracks the eras separately because words that were AI-tells in one era may decay later — "delve" peaked in 2023 and early 2024, became less frequent later in 2024, then dropped sharply in 2025.

**GPT-4 era (2023 – mid-2024)**: words that frequently recurred together in this era —

- delve, tapestry, testament, intricate / intricacies, meticulous / meticulously, pivotal, underscore, interplay, vibrant, bolstered, garner, enduring, crucial, valuable, key, landscape, additionally, boasts, emphasizing

**GPT-4o era (mid-2024 – mid-2025)**: vocabulary shifted to —

- align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant

**Era-stable inflated-symbolism phrases** (high-density across both eras):

- "stands as a testament", "plays a vital role", "underscores its importance", "leaves a lasting impact", "watershed moment", "key turning point", "deeply rooted", "profound heritage", "steadfast dedication", "solidifies", "rich cultural tapestry", "must-see", "stunning natural beauty", "enduring legacy"

**Era-stable editorializing markers**:

- "it's important to note / remember / consider", "it is worth", "no discussion would be complete without", "in this article"

**Reading these eras**: A word's appearance in a recent draft is not on its own a tell. Density and clustered co-occurrence with other era markers is. Era boundaries are approximate.

**Root cause -- RLHF annotation bias**: The "delve" mystery was traced to OpenAI's training process. Human evaluators were disproportionately recruited from Nigeria, where "delve" is common in business English. The model internalized these annotators' vocabulary preferences as markers of "good" output.

**Verb substitution**: AI systematically replaces simple verbs with elaborate alternatives. A peer-reviewed study found over 10% decrease in usage of "is" and "are" in AI-influenced text, replaced by constructions like "serves as a," "features," and "offers."

Sources: [Excess vocabulary in academic writing](https://arxiv.org/html/2406.07016v1) (arxiv, 2024), [AI-Influenced Vocabulary in Medical Writing](https://pmc.ncbi.nlm.nih.gov/articles/PMC12679996/) (PMC/NIH), [Distinguishing academic writing from ChatGPT](https://pmc.ncbi.nlm.nih.gov/articles/PMC10328544/) (PMC/NIH)

## Structural Patterns

AI text follows predictable organizational templates with measurably uniform internal proportions.

**Paragraph and sentence uniformity**: AI produces paragraphs of similar length, with every section receiving equal treatment regardless of importance. Human writers show emphasis bias -- spending more space on what matters and less on what doesn't. Sentence lengths average ~27+ words with remarkably little variation, while human writing alternates between short and long constructions.

**List addiction**: AI jumps into numbered or bulleted lists without narrative buildup, a pattern rarely seen in formal human writing where flowing prose is the norm.

**Formulaic scaffolding**: "Firstly... secondly... finally" and "From X to Y" constructions appear at 2-5x the rate found in human writing. Conclusions invariably begin with "Overall," "In Conclusion," or "In summary."

**Punctuation fingerprints**:
- Em-dashes heavily overused by ChatGPT (8 per 573 words), Copilot (8 per 466 words), Deepseek (9 per 555 words), but NOT Claude (2 per 948 words) or Gemini (0 per 499 words). Root cause: training on digitized late-1800s/early-1900s books which used ~30% more em-dashes than contemporary prose.
- Curly quotation marks ("..." or '...'): ChatGPT and DeepSeek typically produce curly quotes; Gemini and Claude typically produce straight ("..."). Curly quotes alone don't prove LLM use (word processors and typesetting tools also produce them) — the signal lives in clustered co-occurrence with other tells.
- Semicolons and parentheses rarely used
- Oxford commas consistently applied
- Contractions rare

**Heading capitalization**: AI chatbots strongly tend to capitalize all main words in section headings (title case) even when surrounding style is sentence case. The pattern is most visible when the same document mixes a title-cased heading with sentence-case body text.

**Excessive boldface ("key takeaways" pattern)**: AI displays phrases in boldface for emphasis in an excessive, mechanical manner — often emphasizing every instance of a chosen word or phrase. A common variant is bullet points with bolded titles where the bold phrase is then redeclared immediately after:

> "**Scalability:** The system is designed to scale..."

Wikipedia notes this is virtually absent from human-written Wikipedia prose.

**Level-2 heading skipping** *(Context: Wikipedia / encyclopedic prose)*: AI chatbots tend to skip level-2 headings (`==` in MediaWiki, `##` in Markdown) and start sections from the third level (`===` / `###`), against Wikipedia's accessibility and style conventions. Apply only when the target context is Wikipedia / encyclopedic prose; for general prose this is not a tell.

**Grammar perfection as a tell**: AI avoids fragments, run-ons, and unconventional sentence starts. It almost never makes spelling errors. Paradoxically, this perfection is suspicious -- human authenticity includes occasional wonky phrasing and genuine mistakes.

**Colons in titles**: The "Topic: Explanation" format (e.g., "Productivity: A Guide to Getting More Done") correlates with AI generation and became markedly more prevalent post-ChatGPT.

Sources: [Em Dashes and Spotting AI Writing](https://www.plagiarismtoday.com/2025/06/26/em-dashes-hyphens-and-spotting-ai-writing/), [Why do AI models use so many em-dashes?](https://www.seangoedecke.com/em-dashes/), [Indicators of AI writing](https://www.cherryleaf.com/2026/02/indicators-that-suggest-something-was-written-by-ai/)

## Rhetorical Patterns

**Tricolon obsession (Rule of Three)**: AI groups ideas in threes with remarkable consistency -- "Time, resources, and attention." Human writers break this pattern erratically with two, four, or seven items.

**Perfect antithesis**: Binary oppositions like "Not just X, but Y" or "This isn't about A, it's about B." Real arguments are messier and don't fit neat dichotomies.

**Rhetorical questions as staging**: Questions like "How do we solve this?" function as declarative statements disguised as inquiries -- predictable transitions to pre-composed answers rather than genuine explorations.

**Excessive hedging**: AI stacks qualifiers to meaninglessness: "may potentially offer what could be considered significant benefits under certain conditions" strips down to "this works." This stems from safety protocols that program avoidance of absolute statements, producing what one source calls "thesis simulacra" -- statements that look like thesis statements but make no actual claims.

**Compulsive signposting**: "It's worth noting that," "It's important to remember" -- AI announces information before delivering it and labels every logical connection rather than trusting the reader.

**Opinion-avoidant framing**: Instead of stating a view directly, AI distances itself: "commonly described as," "many find," "is generally considered to be effective."

**Conjunctive overuse ("moreover" pattern)**: LLMs over-rely on transition / conjunctive phrases — "moreover", "furthermore", "in addition", "however", "on the other hand", "in contrast" — at AI-typical density. A single use is fine; clustering across paragraphs reads as synthesis-glue rather than argument.

**Negative parallelism ("It's not X, it's Y")**: One of the most prominent AI tells. Binary contrasts via "It's not just X, it's Y" structure to create dramatic effect. Often extends across sentences and even back-to-back constructions: *"It's not just about the beat riding under the vocals; it's part of the aggression."*

**False ranges**: Spectrum-implying structures without actual gradation — "from intimate gatherings to global movements", "from X to Y" — used as scaffolding regardless of whether a real spectrum exists.

**Compulsive summaries**: Excessive recapitulation at the end of sections — "Overall...", "In conclusion...", "To summarize..." — even when no new synthesis occurs.

**"Myths busted" / contrast-and-correct pattern**: When AI describes a subject, it often "clears up a common misconception" or "challenges thinking by pointing out other characteristics." Stereotypically AI-like even though human listicles also use it; treat as a tell only when paired with other patterns.

**Vague attribution / weasel wording**: "Industry reports", "Observers have cited", "Some critics argue", "many experts believe" — authority without sources. AI defaults to authority-flavored hedging because training rewards plausible-sounding citations even when no specific source exists.

**Subject puffery**: AI puffs up subject importance by adding statements about how arbitrary aspects represent broader topics. A small detail becomes "a microcosm of [larger theme]" or "a window into [broader cultural moment]" without earning the elevation.

**Statistical regression to the mean**: AI smooths over specific facts into generic statements. Concrete details — names, numbers, dates, particulars — get blurred into category-level language. The mechanism: autoregressive generation pulls toward statistically most-probable continuations, which are by definition the least specific.

**Superficial -ing word conclusions**: Empty commentary ending in "-ing" words — "ensuring", "highlighting", "emphasizing", "reflecting": *"Consumers benefit from flexibility, **improving convenience**."* The "-ing" clause adds no information; it simulates analysis.

Sources: [AI Content Editor's Handbook](https://www.yarnit.app/post/the-ai-content-editors-handbook-identifying-and-fixing-10-telltale-patterns), [Ten Telltale Signs of AI Text](https://www.theaugmentededucator.com/p/the-ten-telltale-signs-of-ai-generated), [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Tonal Patterns

**Uniform register**: AI picks a lane -- professional-casual, academic-accessible -- and stays there. Every paragraph sounds like it came from the same corporate communications seminar. Human writers naturally shift between registers, slip into colloquialism, and reveal personality through tonal variation.

**Relentless positivity**: Everything receives positive framing. Nothing is weak, inadequate, or simply bad. Abstract approval words like "robust," "holistic," and "nuanced" are distributed without discrimination.

**The enthusiasm gap**: AI treats all subjects with equal professional distance. Quantum physics receives the same measured tone as sandwich recipes. Human writers nerd out about topics they care about and treat boring topics with visible impatience.

**Risk aversion**: AI never writes confusing sentences, offensive jokes, or controversial assertions. It prioritizes broad palatability over authentic expression, creating the writing equivalent of hotel lobby art.

**Emotional overreach without depth**: AI deploys emotional proxies (exclamation marks, enthusiastic phrasing) that feel oddly impersonal -- polished yet hollow, like a greeting card for someone you've never met.

**Encyclopedic-yet-promotional drift**: LLMs have serious problems holding a neutral tone. Even when prompted for an encyclopedic register, output drifts toward advertisement-like writing or travel-guide prose. Cultural and geographic content is especially susceptible — output reads like a tourism website. Common surface markers: "rich cultural heritage", "vibrant traditions", "must-visit", "hidden gem", "breathtaking" (puffery; almost never used by human encyclopedia editors). The drift happens despite explicit prompts because the training data conflates "well-written prose about a place" with promotional travel writing.

**"Breathtaking" puffery**: The word "breathtaking" — and its cousins "stunning", "must-see", "iconic", "world-class" — signals advertisement rather than encyclopedic neutrality. A single instance is forgivable; clustered usage is a strong tell.

## The Negative Space: What's Missing

The most telling AI signatures may be what's absent rather than what's present.

**No lived experience**: AI cannot draw on genuine personal anecdotes. When it fabricates them, they read as "generic specificity" -- plausible-sounding scenarios without naming actual companies, specific cases, or real instances.

**No sensory specificity**: AI uses generic descriptions ("gentle breeze," "blooming flowers") because its algorithm predicts commonly occurring phrase patterns. Strong writing thrives on unexpected, specific sensory observation that AI cannot produce by design.

**No silence or subtext**: "AI is trained to generate phrase patterns; it's not trained to generate silence." Effective dialogue relies on what characters don't say. AI fills every space with exposition.

**No humor, irony, or wit**: A Google DeepMind study with 20 professional comedians found AI "struggled to produce material that was original, stimulating, or -- crucially -- funny." One comedian compared AI comedy to "cruise ship comedy material from the 1950s, but a bit less racist." Humor is classified as an "AI-complete problem."

**No genuine messiness**: AI produces clean prose without false starts, redundancies, or tangents. Human drafts contain self-corrections, changed directions mid-thought, and productive digressions. The absence of mess is itself a tell.

**Perspective collapse**: AI "aggregates so many perspectives that it has none itself," producing bland, consensus-based writing that could fit a wide variety of prompts rather than addressing any specific one with genuine engagement.

Sources: [Show, Don't Tell: What AI Can't Do](https://www.craftliterary.com/2025/03/26/show-dont-tell-what-ai-cant-do/) (CRAFT Literary), [Google DeepMind comedy study](https://www.technologyreview.com/2024/06/17/1093740/what-happened-when-20-comedians-got-ai-to-write-their-routines/) (MIT Technology Review)

## Statistical Signatures

Beneath surface-level tells, AI text occupies a measurably distinct statistical space.

| Metric | Human | AI | Difference |
|--------|-------|-----|-----------|
| **Perplexity** (word-level surprisal) | 57.3 (or 8.21 by another measure) | 37.8 (or 4.18) | AI ~50% more predictable |
| **Burstiness** (sentence variation) | 0.61 | 0.38 | ~38% less variation in AI |
| **Token probability entropy** | 4.56 (SD 0.32) | 3.11 (SD 0.18) | Cohen's d = 3.08 (enormous) |
| **Type-token ratio** | 55.3 | 45.5 | Humans use broader vocabulary |
| **Intrinsic dimensionality** | ~9 | ~7.5 | AI text is geometrically "flatter" |

**Stylometric clustering**: AI texts form "tightly grouped clusters" reflecting uniform patterns, while human texts show "far greater variation and individuality." Even GPT-4 carries a detectable fingerprint.

**Classification accuracy with stylometric features**: XGBoost with stylometric features achieves 100% accuracy; combined logistic regression reaches AUC 0.963; off-the-shelf ML tools on academic writing exceed 99% accuracy.

**Model-specific aidiolects**: Using computational stylistics, researchers confirmed ChatGPT and Gemini have distinct writing signatures -- distance metrics below 1.0 within the same model but above 1.4 between different models, comparable to differences between distinct human authors.

Sources: [Perplexity and Token-Probability Detection](https://www.researchgate.net/publication/398600566), [ChatGPT and Gemini Writing Styles](https://www.scientificamerican.com/article/chatgpt-and-gemini-ai-have-uniquely-different-writing-styles/) (Scientific American), [Unveiling ChatGPT text using writing style](https://pmc.ncbi.nlm.nih.gov/articles/PMC11231544/) (PMC)

## Model-Specific Signatures

| Model | Distinctive Characteristics |
|-------|---------------------------|
| **ChatGPT** | Formal, clinical, academic tone; heavy em-dash use; overuses "delve," "align," "underscore," "noteworthy," "versatile," "commendable"; prefers technical terminology ("glucose" over "sugar"); described as dry, robotic, not warm |
| **Gemini** | Conversational, explanatory; prefers accessible/simple language; uses "sugar" 2x more than "glucose"; information-forward, factual; no em-dash overuse |
| **Claude** | More elegant and natural; literary sensibility; sophisticated humor and tonal flexibility; minimal em-dash use (2 per 948 words vs ChatGPT's 8 per 573); occasionally generates fiction unprompted |
| **Deepseek** | Heavy em-dash use (9 per 555 words); similar to ChatGPT in many structural patterns |

## Wikipedia-Specific Tells

*Context: Wikipedia / encyclopedic prose. These signs apply only when the target context is Wikipedia. For blog posts, articles, marketing copy, emails, or social media, skip this section.*

**Notability-language echoing**: LLMs asked to write Wikipedia articles often echo the exact wording of Wikipedia's notability guidelines — "independent coverage", "significant coverage", "reliable sources" — at higher density than typical Wikipedia editor prose. The model has been trained on Wikipedia's own meta-discussion of notability, so when prompted to write an article it reproduces guideline language as if it were article language.

**Citation pattern mimicry**: LLMs may reproduce Wikipedia citation templates and reference formats with surface accuracy but fabricated content (URLs that don't exist, real journals with non-existent articles, real authors with non-existent papers). The visual structure looks correct; the references don't survive a click.

**Level-2 heading skipping**: Already documented under structural patterns. Repeated here because the convention is Wikipedia-specific: AI tends to skip `==` (level 2) and start at `===` (level 3), against MediaWiki accessibility and style conventions.

Source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

## The Core Insight

No single tell is definitive -- every pattern listed above also appears in some human writing. Em-dashes, formal vocabulary, and structured organization are human conventions that AI amplified, not invented. Detection requires pattern convergence, not individual signal identification.

But the aggregate picture is clear: **AI writing is characterized by what it lacks (surprise, specificity, mess, genuine emotion) as much as by what it contains (uniform structure, predictable vocabulary, relentless hedging)**. The statistical evidence shows these aren't subjective impressions -- they're measurable properties with large effect sizes, rooted in the fundamental mechanics of autoregressive text generation.
