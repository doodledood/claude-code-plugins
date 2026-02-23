---
name: promote-on-x
description: 'Promote a product by finding high-signal posts on X and crafting value-first replies. Uses Claude in Chrome for browser interaction and writing plugin for human-quality prose. Triggers: promote on twitter, promote on x, post replies on x, social media promotion.'
user-invocable: true
---

**User request**: $ARGUMENTS

Promote a product on X by finding relevant conversations and contributing replies that genuinely help while naturally referencing the product. Every reply must be worth posting even without the product link.

If no arguments: auto-detect the product from the current working directory (read README, package.json, or similar). If nothing detectable, ask what to promote.

## Prerequisites

Before starting, verify:

1. **Claude in Chrome browser tools** (`claude-in-chrome` MCP) are available. If not: stop and tell the user "This skill requires the Claude in Chrome extension for browser interaction. Enable it with `claude --chrome` or `/chrome` and try again."
2. **writing plugin** is installed (writing:human-writing skill and writing:writing-reviewer agent). If not: stop and tell the user "This skill requires the writing plugin. Install with: /plugin install writing@claude-code-plugins-marketplace"

## Input Parsing

Extract from $ARGUMENTS (with defaults):

| Input | Default | Notes |
|-------|---------|-------|
| **Product** | Auto-detect from CWD | URL, file path, or inline description |
| **Target count (N)** | 10 | Number of high-signal posts to find |
| **Feed source** | `https://x.com/home` | Also accepts X list URL or community URL |
| **X tier** | Ask user if unknown | "free" (280 chars) or "premium" (25K chars) |

If tier is unknown, ask via AskUserQuestion: "What's your X subscription tier?" with options Free (280 char limit) and Premium (25K char limit).

## Log File (Memento Pattern)

Create `/tmp/promote-on-x-{timestamp}.md` immediately at start. This log survives context compaction during long browsing sessions.

**Disciplines:**
- Write to log IMMEDIATELY after inspecting every post opened in a new tab — before closing the tab
- Never batch log writes or defer to "later" — context compaction erases unlogged findings
- Read full log before crafting replies (Phase 3)
- Read full log before presenting the approval plan (Phase 5)

## Phase 0: Reply Style Calibration (Optional)

Ask the user via AskUserQuestion: "Want me to review your recent replies on X to calibrate tone and learn what's worked?" with options:
- **Yes — check my replies** (Recommended): Navigate to `https://x.com/{username}/with_replies` (ask for their X handle if not known). Browse their recent replies to understand: what topics they engage with, their natural voice and tone, which replies got engagement (likes, replies) and which didn't, patterns that work vs fall flat. Log findings to the session file — this calibrates the reply crafting phase.
- **No — skip this**: Proceed directly to product familiarization.

## Phase 1: Product Familiarization

Deeply understand the product before browsing X. Reply quality depends entirely on product knowledge.

**Understand:**
- Value proposition and key differentiators
- Target audience and their pain points
- Key features and how they solve problems
- Project URL / link to include in replies

Read the product's README, docs, landing page, or whatever the user provided. Internalize what makes this product valuable, not just what it does. Write a product summary to the log file.

**Ask the user** via AskUserQuestion for 1-2 personal anecdotes or micro-stories related to the product (e.g., "What problem were you facing when you built this?", "Can you share a specific moment where this tool saved you?"). These ground replies in lived experience that the LLM cannot fabricate. Log the anecdotes in the product summary.

## Phase 2: Opportunity Discovery

Read the reference file at `references/X_INTERFACE.md` before browsing. It contains X character limits, browser interaction patterns, and critical workarounds (especially for typing in reply fields).

### Browsing Strategy

**Preserve scroll position on the main feed at all times.** Navigate to the feed source (home page, or the user-provided list/community URL) and keep scrolling through it to evaluate posts. When inspecting a specific post, open it in a new tab so the main feed stays in place. After capturing details, close the inspection tab and continue scrolling where you left off.

### Evaluation Criteria

Evaluate each post against:
- **Relevance**: Does the post discuss a problem the product solves, or a topic where the product provides insight?
- **Engagement**: Does the post have enough visibility (likes, views, replies) to be worth replying to?
- **Reply gap**: Is there room to add value that existing replies haven't covered?
- **Fit**: Can you write a reply that helps the poster/readers AND naturally references the product without forcing it?

### Log Every Post You Click On (Critical)

This phase is extremely context-intensive. Context compaction WILL happen during long browsing sessions and will erase your memory of earlier posts. **The log file is the only reliable memory.**

**Before logging, make sure you actually understand the post.** Read it carefully — posts are often sarcastic, referencing prior context, or making a subtle point that isn't obvious from the text alone. Scroll through the top replies to see how people are interpreting it. If the post is part of a thread, read the parent tweets. Misreading the post's intent means your reply angle will be off, which is worse than skipping it entirely.

**Every post you open in a new tab gets logged immediately** — before closing the tab. Write a full structured entry:
- **URL**: full permalink
- **Author**: handle and display name
- **Post content**: full text (and image description if applicable)
- **Engagement**: likes, retweets, replies, views
- **Verdict**: relevant (with reply angle) or not relevant (brief reason)

Write to the log **immediately after inspecting each post** in the new tab. Do NOT batch. Do NOT defer. Do NOT mark as "TBD" to fill later. If you opened it, log it — the URL alone is worth preserving even if the post turns out to be irrelevant.

### Continue Until

Scroll and evaluate until N high-signal posts are logged.

### Insufficient Results

If you've evaluated ~100 posts without finding N high-signal opportunities, present the user with options via AskUserQuestion:
- Lower the quality bar and continue scanning
- Continue scrolling deeper in the feed
- Switch to a different feed source (ask for URL)
- Proceed with the posts found so far

## Phase 3: Reply Crafting

Read the full log file to restore context on all discovered posts.

Invoke `writing:human-writing` to apply anti-AI prose principles during reply generation.

### Structural Variety (Critical)

The most damaging AI tell is uniformity across a batch of replies. Anyone seeing two or more replies with the same structure will identify them as bot-generated.

**Vary across the batch:**
- **Opening style**: Direct opinion, question, agreement-then-diverge, micro-anecdote, reframe, counterpoint
- **Link placement**: Inline within a sentence, mid-reply, end of reply, or omit entirely in 1-2 replies (mention product by name without linking)
- **Self-attribution phrasing**: Never repeat the same "I built X for this" formulation. Use at most once. Alternatives: reference the project in third person, let the link speak for itself, describe what the tool does without claiming authorship, just drop the link with context
- **Tone register**: Some replies conversational, some authoritative, some provocative, some empathetic
- **Length**: Vary significantly. Some replies are two sentences. Others are a full paragraph.

**Use the user's anecdotes** (gathered in Phase 1) in 1-2 replies where they fit naturally. Personal micro-stories grounded in lived experience are the strongest differentiator from bot-generated content.

### Character Limits

Respect the user's X tier limit. Count each URL as 23 characters (t.co shortening). Show character count for each draft.

### Product Link

Include the product link in every reply where it fits naturally. If a reply can't reference the product without forcing it, the post wasn't a high-signal opportunity; drop it from the batch and note why in the log.

## Phase 4: Review

Review each draft reply using the `writing:writing-reviewer` agent. Launch reviews in parallel where possible.

Fix CRITICAL and HIGH severity issues and re-review until clean. Surface remaining MEDIUM and LOW findings in the approval plan (informational, not blocking). If the reviewer flags structural uniformity across the batch, revise to break the pattern before proceeding.

**Convergence guard**: If fixes introduce new HIGH+ issues (count increases), stop and present the situation to the user.

## Phase 5: Approval Plan

Read the full log file to restore context.

Present a numbered list for user approval. For each reply:

1. **Tweet URL** (clickable link)
2. **Original post summary** (author, key content; include image description if the post contained images/media)
3. **Engagement metrics** (likes, views, replies)
4. **Draft reply text**
5. **Character count** (and tier limit)
6. **Review notes** (any remaining MEDIUM/LOW findings)

Present all replies as a single batch for approval. The user can approve the batch or provide feedback on individual replies for revision. If feedback is given, revise those replies, re-run the review loop on revised ones, and re-present the full plan.

## Phase 6: Posting

Only proceed after explicit user approval.

Post each approved reply to its target tweet and verify each was posted successfully. Refer to `references/X_INTERFACE.md` for the posting workflow, especially the JS injection workaround for X's keyboard shortcut conflicts.

Log each result (success or failure with reason). If a post fails, continue to the next one.

**Report at the end**: Number of replies posted successfully, any failures with reasons, and links to the posted replies.

## Error Handling

Detect non-functional X states during any browser interaction:
- **Login wall**: Page shows sign-in prompt or redirects to login
- **Rate limit**: "Rate limit exceeded" message or 429 responses
- **Error page**: "Something went wrong", "Try again" messages
- **CAPTCHA**: Challenge prompt, "verify you're human"
- **Protected/deleted posts**: "These posts are protected", "This post is unavailable"

On encountering any of these: stop the current phase and present the issue to the user via AskUserQuestion with options to retry, skip, or abort.

## Key Principles

| Principle | Rule |
|-----------|------|
| Value first | Every reply must genuinely help the conversation. The product link is supplementary, not the point. If a reply can't add genuine insight, the post isn't a valid opportunity. |
| Log every click immediately | Write to log after inspecting every post opened in a new tab. Context compaction WILL erase browser session details. The log is the only memory that survives. |
| Refresh before synthesis | Read full log before phases 3 and 5. |
| Variety over consistency | Replies that look like siblings are worse than no replies at all. |
| Detect and escalate | Never fail silently. Surface browser issues, rate limits, and insufficient results to the user. |

## Never Do

- Post a reply without user approval
- Use the same structural template for more than one reply in a batch
- Repeat the same self-attribution phrasing ("I built X for this") across replies
- Place the product link in the same position (e.g., always last line) across all replies
- Continue browsing when X shows error states, login walls, or CAPTCHAs
- Skip the log file or defer logging to "later"
- Craft replies without reading the product deeply first
- Use kill-list vocabulary (delve, landscape, leverage, seamless, robust, etc.)
