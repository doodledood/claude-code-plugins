---
name: build-review-persona
description: Build a personalized PR review skill by mining GitHub review history. Extracts review patterns, communication style, priorities, and blind spots — generates a calibrated review-as-me skill that posts inline comments on PRs. Use for onboarding, cloning review style, or creating a reviewer persona.
---

# Build Review Persona

Generate a `review-as-me.md` skill at `~/.claude/commands/review-as-me.md` that captures how a specific person reviews PRs. Mine their GitHub review history, extract patterns, and synthesize into a reusable review skill.

If no GitHub username is provided via `$ARGUMENTS`, discover it from `git log` or `gh api user`.

## Log

Write all extracted data to `/tmp/review-persona-{username}.md`. Append after each collection batch. Read full log before synthesis.

## What to Extract

Mine every available signal from the person's review history:

| Dimension | Signal |
|-----------|--------|
| **Comment themes** | Recurring concerns — type safety, abstractions, naming, duplication, architecture, performance, etc. These become review lenses. |
| **Silent approvals** | PRs approved without comment. Categories never flagged. This becomes the suppression list. |
| **Selectivity** | Ratio of substantive comments to silent approvals. Calibrates confidence threshold. |
| **Communication style** | Register (casual/formal), framing (questions/directives/suggestions), hedging patterns, use of code references |
| **Comment depth** | One-liners vs multi-paragraph. When does depth increase? |
| **Priority signals** | Which themes get strongest reactions? Which get mild suggestions? Rank by intensity. |
| **File focus** | Which file types/areas attract comments? Which are ignored? |
| **PR size behavior** | Do they review small and large PRs differently? More thorough on smaller? Skim large? |
| **Approval patterns** | What earns immediate approval? What gets "request changes"? What triggers re-review? |
| **Disagreement handling** | How do they respond when the author pushes back? Concede, escalate, or hold firm? |
| **Cross-PR consistency** | Same concern flagged across multiple PRs = high-conviction lens. One-off = noise. |

## Data Collection

Collect review comments from PRs the person reviewed in the last year across the GitHub org. Include inline review comments, review body comments, and conversation comments. Maximize sample size — more data produces sharper pattern extraction.

For each PR, also capture:
- Review verdict (approved / requested changes / commented only)
- Whether the reviewer re-reviewed after changes
- PR size (files changed, lines changed)
- Time between PR creation and review

Log all collected data before analysis.

## Pattern Analysis

Read full log before starting analysis.

Synthesize collected data into:

1. **Review lenses** — group comments by theme. Each recurring theme (confirmed across multiple PRs) becomes a lens with concrete triggering conditions.
2. **Priority ordering** — rank lenses by frequency x intensity. Frequency = how often they comment on it. Intensity = how strongly they react.
3. **Suppression list** — categories consistently absent from comments, plus categories explicitly deprioritized in conversation.
4. **Voice calibration** — select real comments that best represent the person's tone across different lenses and intensity levels (mild suggestion through strong objection). These are the authoritative tone reference.
5. **Precision profile** — selectivity ratio + what threshold of confidence produces a comment vs silence.
6. **Engagement profile** — PR size behavior, file focus patterns, re-review tendencies, disagreement style.

## Output Skill Structure

Write the skill to `~/.claude/commands/review-as-me.md` following this structure:

```markdown
---
description: Review a PR the way {name} would. Use for code review, PR review, review-as-me. {1-line summary of their style}.
---

# Review as Me

{Identity paragraph — who they are, review disposition, precision threshold, engagement profile}

## Core Philosophy
{Distilled from patterns — what they optimize for, what they tolerate}

## Mission
Review all changes on the current branch relative to the main branch. Apply the review lenses below. Every finding must reference specific files and lines.

## Approval Gate
Present findings in plan mode (via `EnterPlanMode`) for approval before posting. If zero findings, post a single LGTM comment on the PR directly without entering plan mode.

## Posting Comments
After approval, post each finding as an inline review comment on the PR at the relevant file and line. Use `gh api` to submit a pull request review with all comments in a single review submission.

## Review Lenses
{Priority-ordered lenses. Each lens has:
- Descriptive name
- Triggering conditions (what specifically causes a comment)
- Intensity calibration (when is this a mild note vs strong objection)
- General-purpose — no codebase-specific jargon in lens definitions}

## What NOT to Comment On
{Suppression list — derived from silent approvals and absent categories}

## Voice & Tone (for final review comments)
{Explicit voice traits extracted from their comments}

### Calibration Examples (Real Comments)
{Real verbatim comments spanning: mild suggestion, standard feedback, strong objection. Cover different lenses. These are the authoritative tone reference — match this voice.}

## Extra User Instructions
User instructions may narrow scope or add context but do not override Core Philosophy or the suppression list.

$ARGUMENTS
```

## Key Principles

| Principle | Rule |
|-----------|------|
| **Data-driven only** | Every lens traces to multiple real comments. No invented concerns. |
| **Verbatim voice** | Calibration examples are actual comments, never paraphrased. |
| **General-purpose lenses** | Lens definitions describe universal concerns. Real comments provide specificity. |
| **Precision over recall** | Capture the person's actual selectivity. If they comment on 30% of PRs, the skill should too. |
| **Signal from silence** | What they DON'T comment on is as informative as what they do. |
| **Cross-PR validation** | A pattern seen once is noise. A pattern seen across PRs is a lens. |

## Never Do

- Invent review concerns the person never demonstrated
- Paraphrase their real comments in calibration examples
- Add lenses backed by only one comment
- Include codebase-specific jargon in lens definitions
- Ignore approval/rejection patterns — they reveal priority

$ARGUMENTS
