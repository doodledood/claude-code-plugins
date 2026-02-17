---
name: write
description: 'Write prose that avoids AI tells through an iterative workflow. Gathers your context, writes using research-backed principles, reviews via writing-reviewer agent, auto-fixes HIGH+ issues, loops until clean. Use for articles, blog posts, emails, marketing copy, social media. Triggers: write content, draft article, write blog post, write email, write copy.'
---

**User request**: $ARGUMENTS

Write prose content that reads as authentically human, not AI-generated.

## Goal

Gather the writer's context (the 70%) → write content applying human-writing principles → review via writing-reviewer → auto-fix HIGH+ issues → loop until reviewer finds no HIGH+ issues → deliver.

## Input Detection

Adapt based on what's provided:

| Input | Entry Point |
|-------|-------------|
| **Topic only** | Gather context → outline → write → review loop |
| **Topic + outline** | Gather context → write from outline → review loop |
| **Rough draft** | Gather context for gaps → rewrite applying principles → review loop |
| **Finished text** | Skip writing, run review loop only (editing mode) |
| **No input** | Ask what to write |

## Gather Context (The 70%)

Before writing anything, gather the writer's substance. This is the primary quality driver — prompting and editing are the remaining 30%.

Ask via AskUserQuestion:
- **What's your take?** Key points, thesis, or argument you want to make
- **Personal experience?** Specific anecdotes, examples, observations to include
- **Opinions?** What do you believe about this? What's your angle?
- **Specifics?** Names, numbers, dates, details that ground the piece
- **Audience?** Who reads this and what should they walk away with?
- **Tone?** How should this feel? (Conversational, authoritative, provocative, casual)

If the user provides a rough draft, extract their existing substance and ask only about gaps.

## Write

Invoke the `human-writer:human-writing` skill to apply research-backed writing principles during generation.

Write the content to `draft-{topic-slug}.md` in the current working directory. Use a slugified version of the topic for the filename.

Incorporate the user's context as the core substance. Apply the principles from human-writing: avoid kill-list vocabulary, vary sentence length and structure, break symmetry, include specificity, take positions, embrace imperfection.

## Review Loop

After writing (or receiving finished text for editing):

1. **Review**: Invoke the `writing-reviewer` agent on the draft file
2. **Auto-fix**: Fix all CRITICAL and HIGH severity `AUTO_FIXABLE` issues
3. **Report**: Present MEDIUM and LOW issues to the user (informational, not blocking)
4. **Present NEEDS_HUMAN_INPUT**: Show HIGH+ `NEEDS_HUMAN_INPUT` issues to user with options; skip if user declines
5. **Loop**: If fixes were applied, re-review. Continue until reviewer finds no HIGH+ issues.

**Convergence guard**: If a fix cycle introduces new HIGH+ issues (total HIGH+ count increases instead of decreasing), stop and present the situation to the user rather than continuing to loop.

## Constraints

| Constraint | Why |
|------------|-----|
| **Context before content** | Never generate prose without the writer's substance first |
| **Converge, don't cap** | No arbitrary iteration limit — run until no HIGH+ issues |
| **Convergence guard** | Stop if fixes create new problems — don't oscillate |
| **DRY** | Delegate principles to human-writing, review to writing-reviewer |
| **File output** | Write to `draft-{topic-slug}.md` in cwd |
| **Atomic** | Working draft updated in place; user sees final clean version |

## Output

Report when done:
- File path
- Review iterations completed
- Issues fixed (auto) vs reported (to user)
- NEEDS_HUMAN_INPUT items presented and their resolution
- Summary of key changes made during review cycles
