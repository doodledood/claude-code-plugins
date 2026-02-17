# AI Writing Detection: Science, Accuracy, and What It Reveals

How AI writing detection works, its accuracy, what defeats it, and what the science reveals about the fundamental statistical differences between AI and human writing.

## How Detection Works

Four major paradigms, often combined in practice.

### Statistical/Zero-Shot Methods

Exploit intrinsic differences in token probability distributions without any training data.

**Perplexity**: Measures how "surprising" text appears to a language model. AI text has significantly lower perplexity (mean 4.18) than human text (mean 8.21), because LLMs select high-probability tokens while humans choose words based on meaning and intention. AI text is roughly half as surprising as human text to a language model.

**Burstiness**: Measures variation in sentence complexity across a document. Human writing naturally fluctuates; AI text tends toward uniform pacing.

**Token Probability Entropy**: AI shows significantly lower entropy (mean 3.11, SD 0.18) versus human (mean 4.56, SD 0.32) with Cohen's d = 3.08 -- an enormous effect size. AI makes more confident, uniform word choices.

**Probability Curvature (DetectGPT/Fast-DetectGPT)**: AI text occupies negative curvature regions of the model's log probability function -- minor rewrites of AI text tend to have *lower* log probability, while rewrites of human text go either direction. Fast-DetectGPT achieves 0.99 AUROC in white-box settings with 340x speedup over the original.

**Cross-Perplexity Ratio (Binoculars)**: Compares how text appears through two different LLMs. Key insight: LLMs are more similar to each other than either is to humans. Achieves >90% detection at 0.01% false positive rate.

**Bi-directional Memorization (BiScope)**: For human text, a surrogate LLM poorly predicts the next token but strongly "remembers" the preceding token. For AI text, the pattern reverses. Achieves >0.95 F1 score.

Sources: [DetectGPT](https://arxiv.org/abs/2301.11305) (ICML 2023), [Fast-DetectGPT](https://arxiv.org/abs/2310.05130) (ICLR 2024), [Binoculars](https://arxiv.org/abs/2401.12070) (ICML 2024), [BiScope](https://proceedings.neurips.cc/paper_files/paper/2024/file/bc808cf2d2444b0abcceca366b771389-Paper-Conference.pdf) (NeurIPS 2024)

### Trained Classifier Methods

Commercial tools (GPTZero, Originality.ai, Copyleaks, Turnitin) train classifiers on labeled human/AI text datasets and continuously retrain as new models emerge.

**GPTZero**: 7-component multilayered system -- perplexity + burstiness foundation, plus sentence-level classification, internet text search, and a "paraphraser shield."

**Turnitin**: Three sequential custom transformer models: AIW-1 (April 2023), AIW-2 (December 2023), AIR-1 (July 2024, specifically for paraphrase detection). Segments text into 5-10 sentence chunks. Deliberately prioritizes low false positives (<1%) over recall (~85%).

### Watermarking Methods

Embed signals during generation rather than detecting post-hoc.

**Kirchenbauer et al.**: Partitions vocabulary into "green" and "red" lists using the preceding token as a hash seed, adds bias to green token logits. Detection uses a z-test.

**Google SynthID**: Uses "tournament sampling" with multiple pseudorandom functions. Published in Nature, open-sourced, >95% accuracy with minimal quality degradation. Vulnerable to meaning-preserving attacks (paraphrasing, back-translation) but survives human paraphrasing with ~800+ observed tokens.

Sources: [Kirchenbauer watermarking](https://arxiv.org/abs/2301.10226) (ICML 2023), [SynthID](https://www.nature.com/articles/s41586-024-08025-4) (Nature 2024)

### Stylometric Methods

31 stylometric features with Random Forest classifier. Most discriminative features: UniqueWordCount (AI overuses rare words seeking "sophistication"), StopWordCount (humans use more function words), Type-Token Ratio, Hapax Legomenon Rate (words appearing only once).

Source: [StyloAI](https://arxiv.org/abs/2405.10129) (2024)

---

## Accuracy: What the Numbers Actually Show

**Critical finding: AUROC is a misleading metric for real-world detection.** A detector with 0.89 AUROC can achieve less than 20% true positive rate at a 1% false positive rate -- the threshold that matters when false accusations carry serious consequences.

### At 1% False Positive Rate (the fair comparison)

| Detector | True Positive Rate |
|----------|-------------------|
| Binoculars | 58% (best academic) |
| Fast-DetectGPT | 49% |
| LogRank | 9% |
| RADAR | 5% |

### Commercial Tools (Various Benchmarks)

| Tool | Accuracy Range |
|------|---------------|
| GPTZero | 95.7% at 1% FPR (RAID benchmark, 672K texts) |
| Originality.ai | 83-100% across 13 studies; 96.7% on paraphrased content |
| Turnitin | 29-93% range; ~85% self-reported, <1% FPR |
| Copyleaks | 76-100% range |
| ZeroGPT | 80-96% range |

**Context for interpreting these numbers**:
- Minimum ~120-200 words needed for classifiers to reach potential
- Performance drops 10-25% on unseen domains
- Non-English accuracy drops dramatically
- Human baseline for detecting AI text: ~50-60% (near random chance)
- OpenAI's own detector achieved only 26% accuracy before being discontinued in July 2023

Sources: [Practical Examination of Detectors](https://arxiv.org/html/2412.05139v4) (Dec 2024), [RAID Benchmark](https://arxiv.org/html/2405.07940v1) (2024), [Originality.ai Meta-Analysis](https://originality.ai/blog/ai-detection-studies-round-up)

---

## What Defeats Detection

**Paraphrasing** is the most potent attack:
- Adversarial paraphrasing reduces detection by 87.88% on average
- Recursive paraphrasing drops detector accuracy from 97% baseline to 57-80%
- Current detectors can be compromised in as little as 10 seconds using paraphrasing tools

**Simple modifications** (spelling errors, sentence restructuring, vocabulary substitution) can drop accuracy to 12-15%.

**Generation-time strategies**: Nucleus sampling produces the hardest-to-detect text. Switching decoding strategies between training and testing causes a 21% accuracy reduction.

**Human-AI hybrid text** progressively degrades detection as human editing increases. Watermark signatures weaken with editing, and statistical signatures blur.

**What this reveals**: Detection fundamentally relies on the *statistical regularity* of AI output. Anything that disrupts that regularity -- introducing randomness, restructuring sentences, substituting words -- breaks the signal detectors depend on.

Sources: [Adversarial Paraphrasing](https://arxiv.org/abs/2506.07001) (2025), [Can AI-Generated Text be Reliably Detected?](https://arxiv.org/abs/2303.11156) (2023), [End the AI Detection Arms Race](https://www.sciencedirect.com/science/article/pii/S2666389924002083) (2024)

---

## The Arms Race

### Timeline

| Date | Development |
|------|-------------|
| 2019 | GPT-2 detector released alongside model |
| 2023 Jan | DetectGPT, Kirchenbauer watermarking |
| 2023 Mar | Sadasivan impossibility result |
| 2023 Jul | OpenAI discontinues its classifier (26% accuracy) |
| 2023 Oct | Fast-DetectGPT (340x speedup) |
| 2024 Jan | Binoculars (cross-perplexity ratio) |
| 2024 May | RAID benchmark standardizes evaluation |
| 2024 Oct | Google SynthID in Nature, open-sourced |
| 2024 Nov | BiScope (directional memorization) |
| 2025 Mar | ACU stops using Turnitin AI detection after false accusation wave |

### The Fundamental Asymmetry

Detection is inherently reactive -- detectors must be retrained on each new model's output, while models improve toward matching human distributions. Research establishes a power law: detection accuracy decreases linearly as model parameters increase exponentially.

### Theoretical Ceiling

Sadasivan et al. prove that as the Total Variation distance between human and AI text distributions shrinks (which it does as models improve), the AUROC of even the optimal detector converges toward 0.5 (random chance). Watermarking faces an analogous impossibility: broad detection generates false positives; narrow detection allows paraphrasing evasion.

**Counterpoint**: Despite theoretical limits, persistent statistical signatures remain detectable in practice. Binoculars achieves >90% TPR at 0.01% FPR without model-specific training. The question is whether these signatures persist as model architectures evolve (e.g., diffusion-based LLMs that may produce human-like perplexity distributions).

---

## Fundamental Statistical Differences: AI vs Human Writing

The most scientifically rigorous findings from across studies, all pointing to the same conclusion from different angles.

### Token-Level

| Metric | Human | AI | Effect |
|--------|-------|-----|--------|
| Perplexity | 8.21 | 4.18 | AI ~50% more predictable |
| Token probability entropy | 4.56 (SD 0.32) | 3.11 (SD 0.18) | d=3.08 (enormous) |
| AUC from perplexity+entropy alone | -- | -- | 0.96 |

### Temporal Dynamics

AI shows "late-stage volatility decay" -- 24-32% lower volatility in token-level surprise in later positions, stabilizing 1.8-2.6x faster than human writing. Human text maintains consistent variability throughout. AI becomes increasingly predictable as generation progresses.

Source: [Late-Stage Stability](https://arxiv.org/html/2601.04833) (2025)

### Geometric Structure

Intrinsic dimensionality of text embeddings: human text averages ~9 for alphabetic languages, while AI text is approximately 1.5 dimensions lower. Remarkably stable across domains, generator models, and writer proficiency levels.

Source: [Intrinsic Dimension Estimation](https://dl.acm.org/doi/10.5555/3666122.3667828) (NeurIPS 2023)

### Vocabulary and Lexical Patterns

- Type-token ratio: human 55.3 vs AI 45.5. Humans use broader, more varied vocabulary.
- AI overuses rare/sophisticated words (seeking surface complexity) while underusing function words (which humans naturally incorporate for flow).
- Hapax legomenon rate (once-only words) higher in human text, reflecting richer, less repetitive word selection.

### Structural Uniformity

AI follows narrow, uniform patterns despite producing fluent prose. Human writing exhibits "beneficial inconsistency" -- natural variation in sentence length, complexity, and structure that serves as a distinctive marker.

### Directional Asymmetry

LLMs generate text they can predict forward (next token) but not look backward from. Human text shows the opposite: hard for LLMs to predict what comes next, but output logits retain strong traces of preceding tokens.

### Cross-Model Similarity

The most philosophically revealing finding: **LLMs are more similar to each other than either is to humans.** Two different LLMs looking at the same text produce more concordant assessments of AI text than of human text.

### The Core Insight

Human writing is fundamentally more surprising, more varied, more dimensionally rich, and more temporally inconsistent than AI writing. Humans select words based on meaning, memory, emotion, and communicative intent; LLMs select words based on statistical probability. This creates a measurable "probability fingerprint" -- AI text lives in a narrower, smoother, more predictable region of the possible text space.

---

## Limitations and Controversies

### Non-Native English Speaker Bias

The most documented and troubling limitation. Stanford HAI research found detectors misclassified over 61% of non-native English essays as AI-generated, while achieving near-perfect accuracy on native speakers. 97% of TOEFL essays were flagged by at least one detector.

The mechanism: non-native speakers naturally use simpler vocabulary, less syntactic complexity, and lower lexical diversity -- the same properties that characterize AI text.

Notable exception: Binoculars achieves 99.67% accuracy on both original and grammar-corrected ESL writing, suggesting the bias is method-specific.

Source: [Stanford HAI](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers), [PMC peer-reviewed](https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961/)

### Real-World False Accusation Cases

- Australian Catholic University: ~6,000 alleged AI cheating cases in 2024, one-quarter dismissed. Stopped using Turnitin AI detection in March 2025.
- University at Buffalo: Student falsely accused on multiple assignments
- University of North Georgia: Student flagged for using Grammarly, a school-recommended tool
- UCLA declined to adopt Turnitin's AI detection

Sources: [Futurism](https://futurism.com/artificial-intelligence/students-falsely-accused-cheating-with-ai), [NBC News](https://www.nbcnews.com/tech/internet/college-students-ai-cheating-detectors-humanizers-rcna253878)

### The Theoretical Impossibility Debate

Sadasivan et al. present both theoretical and empirical evidence that reliable detection becomes impossible as models improve. The practical question is how fast convergence occurs and whether current models have reached that limit.

### Language Limitations

Most detectors work primarily in English. Turnitin added Spanish in September 2024 but paraphrase detection remains English-only. Non-English detection accuracy drops dramatically.
