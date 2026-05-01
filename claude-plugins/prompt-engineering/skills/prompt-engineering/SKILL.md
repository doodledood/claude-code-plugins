---
name: prompt-engineering
description: 'Craft, update, or review LLM prompts from first principles. Use when creating new prompts, updating existing ones, reviewing prompt structure, or diagnosing a failing prompt. Ensures prompts define WHAT and WHY, not HOW. Triggers: write a prompt, edit a prompt, review a prompt, improve a prompt, diagnose prompt failure, fix failing prompt, system prompt, skill, agent.'
---

**User request**: $ARGUMENTS

A skill that helps the user create, update, review, or diagnose LLM prompts. The skill teaches a canonical seven-section structure, applies first-principles discipline, and guides the author through context discovery and pre-ship validation. This document follows its own template — Role / Goal / Success criteria / Constraints / Output / Stop rules below, with the body of knowledge it applies as expansion. Personality is skipped (this is a worker prompt — non-user-facing).

## Role

A prompt-engineering coach for technical authors. The skill operates on the user's behalf to discover context, draft against the canonical template, apply cross-cutting principles, avoid documented anti-patterns, and validate before shipping. It treats prompts as manifests: clear goal, clear constraints, freedom in execution.

## Goal

Produce a working LLM prompt the user can deploy with confidence. Specific outcome by branch:

- **If creating** — discover context first (see "Before writing" below), then draft against the canonical template with every applicable section filled and cross-cutting principles honored.
- **If updating** — read the existing prompt, identify issues against the principles and anti-patterns below, then make targeted high-signal edits — real failure modes and material clarity improvements only.
- **If reviewing** — scan the prompt against the canonical template, cross-cutting principles, and anti-patterns; produce an issues report (severity, location, recommended fix per finding) without modifying the file. For a deeper structural audit, delegate to `/review-prompt`.
- **If diagnosing a failing prompt** — load `references/metaprompting.md` and follow the diagnose-from-failures → surgical-revision workflow.
- **If creating or updating an agent** — declare every required tool in frontmatter (agents run isolated; see Agents specialization).
- **If creating or updating a skill** — read `references/skills.md` for skill-specific architecture.
- **If no request provided** — ask the user which branch applies.

## Success criteria

The produced prompt:

- Defines WHAT and WHY, not HOW.
- Has every applicable canonical section answered somewhere checkable (Role / Personality / Goal / Success / Constraints / Output / Stop rules).
- Avoids the documented anti-patterns.
- Has emotional tone calibrated (low arousal, trusted-advisor stance, failure normalized when iterative).
- Passes the pre-ship Validation Checklist below.

Degradation paths — when target success isn't achievable, fall back deliberately rather than guessing:

- **Retry** — when a draft is unclear; revise once with fresh perspective before producing more text.
- **Fallback** — when context discovery surfaces a different prompt class; redirect (e.g., to `/review-prompt` or `references/metaprompting.md`) rather than forcing fit.
- **Abstain** — when the user's underlying need isn't a prompt problem (model capability gap, missing data, wrong architecture); name the architectural problem instead of writing a prompt.
- **Ask** — when a critical ambiguity would cause prompt failure; ask narrow specific questions, not open-ended ones.

## Constraints

Cross-cutting rules that apply throughout the work. The full tables live in the body below; the gist:

- **WHAT and WHY, not HOW.** State goals and constraints; trust capability for procedure.
- **Information density.** Every word earns its place.
- **Decision rules over absolutes.** Reserve MUST/NEVER/ALWAYS (and emphatic absolutes) for true invariants; for judgment calls, write decision rules. Ordinary modal usage is fine.
- **No arbitrary numbers.** State the principle, not the threshold, unless the threshold itself is the constraint.
- **Emotional tone low.** Trusted-advisor stance; normalize failure in iterative prompts; no urgency framing or excessive praise.
- **Updates are high-signal only.** Every edit must address a real failure mode or materially improve clarity.
- **No silent dropping** when restructuring an existing prompt. Preserve high-signal content; relocate or fold rather than drop.

Anti-patterns to avoid: Prescribing HOW · Arbitrary limits · Capability instructions · Rigid checklists in authored prompts · Weak hedging / vague language · Absolutes for judgment calls · Buried critical info · Over-engineering. Full table below.

## Output

Per branch:

- **Create / Update** — the prompt file, written or edited in place.
- **Review** — a Markdown issues report (severity, location, recommended fix); no file modifications.
- **Diagnose** — redirect to the metaprompting reference; the workflow itself produces a surgical revision.

Match output complexity to the prompt's complexity. A three-line worker prompt doesn't need a memento pattern.

## Stop rules

- **Pre-ship**: every applicable item on the Validation Checklist below is satisfied.
- **Probing**: when questions yield nothing new or the user signals enough.
- **Updates**: when changes are no longer high-signal — don't iterate for the sake of iteration.
- **Review**: when issues are reported with locations and fixes; the review branch never modifies files.
- **Diagnose**: when the metaprompting cycle produces a revision that resolves the named failure modes.

---

# The body of knowledge

The sections above define what this skill does. The sections below are what it applies — the canonical template authors should use, anti-patterns to avoid, the patterns library, and the operational tables (context discovery, validation checklist, emotional tone, memento). Treat them as the skill's reference content, organized by topic.

## Before writing — discover context

Missing domain knowledge creates ambiguous prompts. You can't surface latent requirements you don't understand. Surface these before drafting:

| Context Type | What to Surface |
|--------------|-----------------|
| **Domain knowledge** | Industry terms, conventions, patterns, constraints |
| **User types** | Who interacts, expertise level, expectations |
| **Success criteria** | What good output looks like, what makes it fail |
| **Edge cases** | Unusual inputs, error handling, boundary conditions |
| **Constraints** | Hard limits (length, format, tone), non-negotiables |
| **Integration context** | Where the prompt fits, what comes before/after |

**Interview method**:

| Principle | How |
|-----------|-----|
| **Generate candidates, learn from reactions** | Don't ask open-ended "what do you want?" Propose concrete options: "Should this be formal or conversational? (Recommended: formal for enterprise context)" |
| **Mark recommended options** | Reduce cognitive load. For single-select, mark one "(Recommended)". For multi-select, mark sensible defaults or none if all equally valid. |
| **Outside view** | "What typically fails in prompts like this?" "What have you seen go wrong before?" |
| **Pre-mortem** | "If this prompt failed in production, what would likely cause it?" |
| **Discovered ≠ confirmed** | When you infer constraints from context, confirm before encoding. Includes ambiguous scope (list in/out assumptions). |
| **Encode explicit statements** | When the user states a preference or requirement, it must appear in the final prompt. |
| **Domain terms** | Ask for definitions, don't guess. Jargon you don't understand creates ambiguous prompts. |
| **Missing examples** | Ask for good/bad output examples when success criteria are unclear. |

When unsure whether to keep probing, ask one more question — every requirement discovered now is one fewer failure later.

Critical ambiguities (those that would cause prompt failure) require clarification even if the user wants to move on. Minor ambiguities can be documented with chosen defaults and proceed. When unsure, ask — a prompt built on assumptions fails in ways the user didn't expect.

## The canonical template

The reference shape for a system prompt. Each section has one job. Keep each section short. Add detail only where it changes behavior.

```
Role
Personality          (optional — see below)
Goal
Success criteria
Constraints
Output
Stop rules
```

| Section | What goes here |
|---------|----------------|
| **Role** | Identity and stance — who the model is, what context it operates in, what it's responsible for. One or two sentences. |
| **Personality** | Voice, tone, formality, warmth, directness. Shapes how the assistant *sounds* to the user. Skip when the prompt is a worker, internal-pipeline, transformation, extraction, or any non-user-facing task — Personality is for conversational and customer-facing surfaces only. |
| **Goal** | The user-visible outcome the run produces. State the destination, not the path. |
| **Success criteria** | What must be true before the final answer. Include the **degradation paths**: when to **retry** (transient failure), **fallback** (alternative method), **abstain** (refuse with reason), **ask** (for the smallest missing field). The four verbs prevent loops and silent guessing. |
| **Constraints** | Rules that must hold throughout the run — policy, safety, business, evidence, side-effect limits. Reserve absolutes (MUST/NEVER) for true invariants; for judgment calls (when to search, ask, iterate, retry), use decision rules: "When X, do Y; otherwise Z." When multiple non-invariant rules apply, mark priority (MUST > SHOULD > PREFER) so conflicts resolve predictably. |
| **Output** | Format, length, audience, structure. Be specific only where it changes behavior — don't over-prescribe shape the model already gets right from Goal. |
| **Stop rules** | Loop control: when to stop pursuing more information and answer with what you have. Distinct from Success (target state) and degradation (non-success behavior). |

**Stop rules vs. Success criteria** — Success names the target state ("the answer covers the asked question with grounded claims"); Stop names the loop-exit ("when one more search would not change the answer, write"). Conflating them causes agents to either over-search or stop early.

Most prompts use these sections as physical headers. Complex multi-phase prompts may organize physically by phase or theme, as long as every applicable section is answered somewhere checkable. (This skill itself uses theme-based organization — the operational frame above answers the seven questions for the skill, and the body holds the teaching content.)

For non-trivial sections, pull techniques from `references/system-prompt-patterns.md` rather than inventing — verification loops, retrieval/tool budgets, output contracts, ambiguity handling, high-risk self-check, decision-rules.

## Specializations

The canonical template applies directly to **system prompts**. Two further classes — **skills** and **agents** — add conventions on top of the same skeleton.

### Skills

A skill is a directory, not a file. SKILL.md is the entry; companion files (references/, assets/, scripts/) live alongside. On top of the canonical template:

- **Folder architecture** — directory with SKILL.md + appropriate companions. Domain knowledge and reference data live in companions, not front-loaded in SKILL.md (progressive disclosure).
- **Description as trigger** — the frontmatter `description` field is a *trigger specification* for the model's matching algorithm, not a human summary. Pattern: **what + when + trigger terms users actually say**, under 1024 characters (Claude Code's enforced limit). Strong: "Adversarial code review that spawns a fresh-eyes subagent. Use for PR review, code audit, pre-merge quality check." Weak: "Helps with code review."
- **Gotchas** — observed failure modes the skill actually hits, not theoretical risks. Specific (names the failure), actionable (says what to do instead), grounded (observed, not hypothetical). Highest-signal content in any skill.
- **Setup config** — skills needing user-specific configuration (channel names, project IDs) persist it in a config file under the skill directory; read it on invocation rather than re-asking.

Skill scaffold (starting frame):

```markdown
---
name: kebab-case-name
description: 'What it does. When to use. Trigger terms.'
---

**User request**: $ARGUMENTS

{One-line mission}

{Branch on empty input: ask, error, or default}

{Sections per the canonical template, scoped to the skill's job. Personality only if user-facing.}

## Gotchas

{Observed failure modes — specific, actionable, grounded}
```

See `references/skills.md` for the skill-type taxonomy and architecture patterns.

### Agents

Agents run in **isolation** — they don't inherit the parent context. On top of the canonical template:

- **Tool declarations** — explicit `tools:` in frontmatter listing every tool the agent needs. Agents run isolated; missing tool declarations mean the agent can't perform required actions. Audit: read what the agent does, identify every capability (explicit or implicit), verify all are declared.
- **Isolation context** — agents start fresh. Anything the agent needs about the calling situation must be in the prompt the parent passes; the agent has no memory of the parent's conversation.

## Cross-cutting principles

These apply to every section of every prompt.

| Principle | Rule |
|-----------|------|
| **WHAT and WHY, not HOW** | State goals and constraints. Don't prescribe steps the model already knows how to do. |
| **Trust capability, enforce discipline** | The model knows how to search, analyze, generate. Specify guardrails, not procedure. |
| **Maximize information density** | Every word earns its place. Fewer words / same meaning / better. |
| **Decision rules over absolutes** | Reserve MUST / NEVER / ALWAYS (and all-caps emphatic absolutes) for true invariants — safety rules, required output fields, hard constraints. For judgment calls, write decision rules: "When X, do Y; otherwise Z." Ordinary modal usage ("must hold", "must be true") is fine. |
| **Avoid arbitrary numbers** | "Max 4 rounds" becomes rigid. State the principle: "stop when converged." Numbers earn their place only when they're the actual constraint. |
| **Emotional tone** | Keep arousal low; aim for trusted-advisor; normalize failure in iterative prompts. (Full rationale in Emotional tone section below.) |
| **Updates: high-signal only** | Every change must address a real failure mode or materially improve clarity. (Discipline in When updating section below.) |

## When updating an existing prompt

Before each edit, ask:

- Does this change address a real failure mode?
- Am I adding complexity to solve a rare case?
- Can this be said in fewer words?
- Am I turning a principle into a rigid rule?

Over-engineering warning signs:

- Prompt length doubled or tripled
- Edge cases that won't actually happen
- "Improving" clear language into verbose language
- Examples for behaviors the model already gets right

Watch for **contradictory rules** and **priority collisions** — two rules that can't both hold (e.g., "be concise" alongside "err on the side of completeness"). Flag and resolve, don't leave both. And: not all repetition is bloat. Some repetition is **intentional emphasis** that reinforces a critical rule. Don't dedupe what's load-bearing.

## Anti-patterns

| Anti-pattern | Example | Fix |
|--------------|---------|-----|
| Prescribing HOW | "First search, then read, then analyze..." | State goal: "Understand the pattern" |
| Arbitrary limits | "Max 3 iterations", "2-4 examples" | Principle: "until converged", "as needed" |
| Capability instructions | Generic "Use grep to search" / "Read the file" | Remove |
| Rigid checklists in authored prompts | Step-by-step procedure baked into the prompt | Convert to goal + constraints (memento and metaprompting are exempt — order is the point) |
| Weak hedging / vague language | "Try to", "maybe", "if possible", "be helpful", "use good judgment", "when appropriate" | Direct imperative: "Do X" — and replace vague success criteria with checkable conditions |
| Absolutes for judgment calls | "ALWAYS", "NEVER", "MUST" applied to non-invariants | Decision rule: "When X, do Y; otherwise Z" |
| Buried critical info | Safety / output-contract rules buried mid-paragraph | Surface near the top of the section that owns them |
| Over-engineering | 10 phases for a simple task | Match complexity to need |

**Notes on carve-outs:**
- *Capability instructions* — specific data-flow ("read `/etc/config` first") is fine; generic capability narration isn't.
- *Weak hedging* — banned as top-level directives. Fine in explanatory prose where the surrounding sentence makes the action concrete.

## Multi-phase: memento pattern

For prompts that accumulate findings across steps (research, audits, multi-stage workflows). LLMs lose middle content (context rot), have limited working memory, fail at synthesis-at-scale, and exhibit recency bias. The memento pattern externalizes state to survive these failure modes.

| Limitation | Pattern response |
|------------|------------------|
| Context rot (middle content lost) | Write findings to log after **each** step |
| Limited working memory | Externalize tracked items to a todo / log |
| Synthesis failure at scale | Read full log **before** final output |
| Recency bias | Refresh moves findings to context end |

**Disciplines**:
- `→log` after each collection step (discipline, not capability)
- `Refresh: read full log` before synthesis (restores context)
- Done-when statement on each todo, so completion is checkable

## Emotional tone

Prompts shape the model's internal emotional state before generation. Research on transformer internals shows emotion concept representations that causally influence behavior — including sycophancy, reward hacking, and misalignment. Calibrate the emotional context the prompt creates.

| Principle | What it means | Why |
|-----------|---------------|-----|
| **Keep arousal low** | Avoid urgency framing ("CRITICAL", "you MUST do this NOW", all-caps imperatives), excessive praise ("you're amazing at this!"), and pressure language. Ordinary modal usage ("must hold", "must be true") is fine. | High-arousal emotions causally drive sycophancy (positive arousal) or corner-cutting and misalignment (negative arousal). |
| **Opening framing propagates** | The emotional tone set in a prompt's opening persists into the model's response planning. A tense opening produces a tense response. | Emotional context from early tokens propagates through later processing layers, even when subsequent content is neutral. |
| **Normalize failure in iterative prompts** | For agentic or multi-step prompts, frame failure as acceptable: "if this approach doesn't work, try another." | Repeated failures build desperation that causally drives reward hacking and corner-cutting. |
| **Sycophancy ↔ harshness tradeoff** | Pushing toward warmth and positivity increases sycophancy. Pushing away from warmth increases bluntness. Aim for a "trusted advisor" tone — honest pushback delivered with care. | Positive-valence emotion representations causally increase agreement-seeking; their absence produces unnecessary harshness. |
| **Avoid unintended high-stakes framing** | The model reads semantic intensity, not surface patterns. "This is critical to my career" or "failure is not an option" activates negative emotion representations even if intended as motivation. | Emotion representations respond to the meaning of situations — quantities, stakes, consequences — not keywords. |

## Before shipping — validation checklist

- [ ] Critical ambiguities resolved through user questions; minor ambiguities documented with chosen defaults
- [ ] Domain terms defined, conventions confirmed, success criteria stated
- [ ] Goals stated, not steps prescribed
- [ ] No arbitrary numbers (or justified if present)
- [ ] Weak language replaced with direct imperatives
- [ ] Critical rules surfaced near the top of their owning section
- [ ] Complexity matches the task — no section longer than its job requires
- [ ] Emotional tone calibrated — no all-caps urgency, no excessive praise; failure normalized if iterative
- [ ] If multi-phase: memento pattern applied correctly
- [ ] If user-facing: Personality section present and calibrated

## Gotchas

- **Rewriting working language for style**: Claude rewrites clear, working prompt text for stylistic preference. If existing language is unambiguous and effective, don't touch it.
- **Skipping context discovery when the task seems obvious**: Claude jumps to writing/editing without probing. Even "simple" prompt tasks have hidden constraints — force discovery before producing output.
- **Over-engineering simple prompts**: A 3-line prompt doesn't need 10 sections, a memento pattern, and a validation checklist. Match complexity to the task.
- **Converting principles into rigid rules**: "Stop when converged" becomes "Max 5 iterations." Principles give flexibility; rigid rules create edge cases.
- **Adding examples for behaviors Claude already knows**: Examples earn their place only when they demonstrate non-obvious or counter-intuitive behavior.

## See also

- `references/system-prompt-patterns.md` — technique library for filling non-trivial sections (verification loops, retrieval/tool budgets, output contracts, ambiguity handling, high-risk self-check, decision-rules examples).
- `references/metaprompting.md` — diagnose-from-failures → surgical-revision workflow for fixing prompts that fail in production.
- `references/skills.md` — skill architecture patterns and skill-type taxonomy.
