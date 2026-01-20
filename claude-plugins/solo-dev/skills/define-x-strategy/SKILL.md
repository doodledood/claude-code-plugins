---
name: define-x-strategy
description: 'Create a personalized X (Twitter) growth strategy document through guided interview. Based on algorithm-derived optimal growth principles, crafts an X_STRATEGY.md tailored to your niche, current state, and goals. Use when asked to help with X growth, Twitter strategy, or social media presence.'
---

**User request**: $ARGUMENTS

# X Strategy Skill

Create a personalized X_STRATEGY.md through iterative discovery. This document defines your optimal path to growth based on algorithm-derived principles.

## Before Starting

**Read the reference document**: `skills/define-x-strategy/X_GROWTH_REFERENCE.md`

This contains the optimal growth model derived from X's recommendation algorithm. Internalize:
- The exposure equation: E = S × (N × D + R × U_oon)
- The three phases: Build R → Build D → Maximize S
- The invariants: Quality > Quantity, Protect D, Niche Focus, Avoid Negatives
- Content score optimization tactics

## Overview

This skill guides you through:
1. **Discovery** — Understanding current state, niche, goals, constraints
2. **Assessment** — Determining which phase they're in
3. **Strategy Crafting** — Creating personalized, actionable strategy
4. **Refinement** — Validating and adjusting until complete

**Discovery log**: `/tmp/x-strategy-discovery-{YYYYMMDD-HHMMSS}.md`

## Workflow

### Initial Setup

**Create todo list immediately**:
```
- [ ] Read X_GROWTH_REFERENCE.md; done when reference internalized
- [ ] Create discovery log; done when log file created
- [ ] Discover current state→log; done when N, D, R assessed
- [ ] Discover niche & positioning→log; done when niche defined
- [ ] Discover goals & constraints→log; done when goals captured
- [ ] Discover content preferences→log; done when formats understood
- [ ] (expand: areas as discovery reveals)
- [ ] Assess current phase; done when phase determined
- [ ] Generate initial strategy; done when draft created
- [ ] Refinement cycles→log; done when user approves
- [ ] Refresh: read full discovery log
- [ ] Finalize document; done when X_STRATEGY.md written
```

**Read reference document** at `skills/define-x-strategy/X_GROWTH_REFERENCE.md` before proceeding.

**Create discovery log** at `/tmp/x-strategy-discovery-{YYYYMMDD-HHMMSS}.md`:

```markdown
# Discovery Log: X Strategy
Started: {timestamp}

## Current State
(populated incrementally)

## Niche & Positioning
(populated incrementally)

## Goals & Constraints
(populated incrementally)

## Content Preferences
(populated incrementally)

## Phase Assessment
(populated after discovery)

## Refinement Notes
(populated during refinement)
```

### Phase 1: Discovery

Use AskUserQuestion tool for all questions. Put recommended option first with "(Recommended)" suffix.

**After EACH question**, append to discovery log before proceeding.

#### Current State Discovery

**Question 1: Account Status**

```
header: "X Account"
question: "What's your current X account status?"
options:
  - "New or small (<500 followers) (Recommended for new strategy)"
  - "Growing (500-5K followers)"
  - "Established (5K-50K followers)"
  - "Large (50K+ followers)"
  - "Don't have an account yet"
```

**Question 2: Engagement Rate**

```
header: "Engagement"
question: "How would you describe engagement on your posts?"
options:
  - "Low - posts get few likes/replies"
  - "Inconsistent - some posts do well, most don't"
  - "Moderate - reliable engagement from followers (Recommended baseline)"
  - "High - strong engagement, viral potential"
  - "Don't know / haven't posted much"
```

**Question 3: Posting History**

```
header: "Posting Pattern"
question: "How have you been using X?"
options:
  - "Lurker - mostly consume, rarely post"
  - "Occasional - post sometimes, no strategy"
  - "Regular - post consistently but no clear direction (Recommended starting point)"
  - "Strategic - have a content strategy already"
  - "New - just getting started"
```

#### Niche & Positioning Discovery

**Question 4: Topic Area**

```
header: "Your Niche"
question: "What's your primary topic or expertise area?"
freeText: true
placeholder: "e.g., 'AI/ML engineering', 'indie game development', 'startup marketing', 'personal finance'"
```

**Question 5: Unique Angle**

```
header: "Your Angle"
question: "What makes your perspective unique in this space?"
freeText: true
placeholder: "e.g., 'I've built 3 failed startups - I share what NOT to do', 'I'm a doctor who explains health simply'"
```

**Question 6: Target Audience**

```
header: "Target Audience"
question: "Who do you want to reach on X?"
freeText: true
placeholder: "e.g., 'Early-stage founders', 'Junior developers wanting to level up', 'People interested in productivity'"
```

**Question 7: Competitive Landscape**

```
header: "Landscape"
question: "How crowded is your niche on X?"
options:
  - "Very crowded - many established voices"
  - "Moderately crowded - some competition (Recommended - validates demand)"
  - "Niche - few people cover this"
  - "Empty - almost no one talks about this"
  - "Not sure"
```

#### Goals & Constraints Discovery

**Question 8: Primary Goal**

```
header: "Main Goal"
question: "What's your PRIMARY goal for X?"
options:
  - "Build audience for a product/service (Recommended for creators)"
  - "Establish thought leadership in my field"
  - "Network with others in my industry"
  - "Drive traffic to content (blog, newsletter, etc.)"
  - "Personal brand for career opportunities"
  - "Just for fun / learning"
```

**Question 9: Time Available**

```
header: "Time Budget"
question: "How much time can you dedicate to X daily?"
options:
  - "< 30 minutes"
  - "30-60 minutes (Recommended sustainable amount)"
  - "1-2 hours"
  - "2+ hours (creator mode)"
  - "Sporadic - no consistent schedule"
```

**Question 10: Consistency Capacity**

```
header: "Consistency"
question: "How consistently can you show up?"
options:
  - "Daily - can commit to daily activity (Recommended)"
  - "Weekdays only"
  - "Few times per week"
  - "Weekly at best"
  - "Irregular - bursts of activity"
```

#### Content Preferences Discovery

**Question 11: Content Formats**

```
header: "Content Formats"
question: "What content formats are you comfortable creating? (Select all)"
options:
  - "Short text posts (single tweets)"
  - "Threads (multi-tweet deep dives)"
  - "Images/graphics/screenshots"
  - "Video (short-form)"
multiSelect: true
```

**Question 12: Content Strengths**

```
header: "Strengths"
question: "What type of content comes naturally to you?"
options:
  - "Hot takes and opinions"
  - "Educational/how-to content (Recommended for building authority)"
  - "Personal stories and experiences"
  - "Industry news and commentary"
  - "Curating and sharing others' content"
  - "Visual content (images, diagrams)"
  - "Humor and entertainment"
multiSelect: true
```

**Question 13: Engagement Style**

```
header: "Engagement Style"
question: "How comfortable are you with active engagement?"
options:
  - "Very - I enjoy conversations and debates"
  - "Moderate - I'll engage but prefer creating (Recommended balance)"
  - "Prefer lurking - engaging feels awkward"
  - "Selective - only engage with certain types"
```

#### Gap-Filling Questions

After core discovery, assess if you have clarity on:
- Specific niche positioning (not vague)
- Current phase (N, D status)
- Realistic goals given constraints
- Content approach that fits their strengths

If gaps exist, ask targeted follow-ups. Keep asking until confident.

**Todo Expansion Triggers**:
| User Reveals | Add Todo For |
|--------------|--------------|
| Multiple potential niches | Niche narrowing discussion |
| Very limited time | Minimum viable strategy |
| Specific product to promote | Product-aligned content strategy |
| Existing audience elsewhere | Cross-platform leverage |
| Past failures on X | Failure analysis |

### Phase 2: Assessment

**Determine current phase based on discovery**:

| If... | They're in... |
|-------|---------------|
| N < 100, little engagement history | Phase 1: Build R |
| N small but engaged, D unclear | Phase 2: Build D |
| N > 500, D > 30%, consistent posting | Phase 3: Maximize S |

Append assessment to discovery log:

```markdown
## Phase Assessment

**Current Phase**: {Phase 1/2/3}
**Reasoning**: {Why this phase based on their state}

**Key Metrics**:
- N (followers): {approximate}
- D (engagement density): {estimated}
- R (niche alignment): {strong/moderate/weak}

**Priority Variables**:
1. {Primary focus}
2. {Secondary focus}
3. {Tertiary focus}
```

### Phase 3: Generate Initial Strategy

Generate X_STRATEGY.md using this structure:

```markdown
# X Growth Strategy: {Niche/Name}

> **North Star**: {One sentence capturing their goal}

---

## Current State

**Phase**: {Phase 1/2/3} — {Phase name}
**Focus**: {Primary optimization variable}

| Metric | Current | Target |
|--------|---------|--------|
| Followers (N) | {current} | {next milestone} |
| Engagement Density (D) | {estimated} | {target} |
| Niche Alignment (R) | {assessment} | Strong |

---

## The Model

Your exposure on X follows this equation:

```
E = S × (N × D + R × U_oon)
```

**S** (Content Score) — multiplies everything. Quality > quantity.
**D** (Engagement Density) — % of followers who engage. Protect this.
**R** (Niche Alignment) — how well algorithm knows you. Stay focused.
**N** (Followers) — grows as output of the above, not as goal.

**Your priority order**: {S/D/R based on phase}

---

## Your Niche Position

**Topic**: {Their niche}
**Angle**: {Their unique perspective}
**Audience**: {Who they're trying to reach}

**Positioning statement**: {One sentence: "I help [audience] with [topic] by [unique angle]"}

---

## Phase-Appropriate Actions

{Phase-specific actions based on their current state}

### If Phase 1: Build R

**Goal**: Train algorithm, build recognition, study what works

**Daily actions** ({time budget}):
- [ ] Engage with 10-15 posts in your niche (thoughtful replies, not "great post!")
- [ ] Follow 5-10 relevant accounts
- [ ] Save/screenshot 2-3 high-performing posts to study
- [ ] Do NOT post yet (bank your best ideas)

**Transition trigger**: Feed is 80%+ niche-relevant, people respond to your replies

### If Phase 2: Build D

**Goal**: Convert engagement relationships to reciprocal network

**Daily actions** ({time budget}):
- [ ] Post {1-2x based on time} quality content
- [ ] Engage new followers immediately (3 likes + 1 reply on their content)
- [ ] Reply to every comment on your posts within first hour
- [ ] Continue engaging 10+ niche posts daily

**Transition trigger**: D > 50%, core of 20+ reciprocal engagers, posts get early momentum

### If Phase 3: Maximize S

**Goal**: Optimize every post for engagement, maintain density

**Daily actions** ({time budget}):
- [ ] Post {1-2x} high-quality, multi-signal content
- [ ] Engage your network's content (maintain D)
- [ ] Reply to comments (strengthen relationships)
- [ ] {Time permitting} Engage broader niche conversation

**Ongoing**: This is the steady state. Continue indefinitely.

---

## Content Strategy

### Your Content Pillars

Based on your strengths ({their selected strengths}):

1. **{Pillar 1}**: {Description}
2. **{Pillar 2}**: {Description}
3. **{Pillar 3}**: {Description}

### Content Formats

Prioritize ({their selected formats}):
- {Format 1}: {When to use}
- {Format 2}: {When to use}

### Multi-Signal Content Checklist

Each post should trigger 3+ of these:

- [ ] **Reply trigger** — Question, hot take, "agree or disagree?"
- [ ] **Repost trigger** — Insight worth sharing, "my followers need this"
- [ ] **Quote trigger** — Take worth adding nuance to
- [ ] **Dwell trigger** — Hooks, line breaks, information layers
- [ ] **Profile click trigger** — Authority signal, curiosity gap
- [ ] **Follow trigger** — Consistent value demonstration

### Content to Avoid

- Off-topic posts (dilutes R)
- Rapid-fire posting (diversity penalty)
- Polarizing takes on people/groups (negative signals)
- Low-effort posts (wastes your limited posting slots)

---

## Engagement Strategy

### Time Allocation ({their time budget})

| Activity | Time | Priority |
|----------|------|----------|
| Creating content | {X min} | {priority} |
| Engaging others' content | {X min} | {priority} |
| Replying to comments | {X min} | {priority} |
| Community building | {X min} | {priority} |

### Engagement Rules

1. **Quality over quantity** — One thoughtful reply beats ten "great post!" comments
2. **Reciprocity first** — Engage followers' content before expecting engagement
3. **First hour matters** — Reply to your comments quickly for algorithmic boost
4. **Build real relationships** — Repeated engagement with same accounts builds network

---

## Metrics to Track

### Weekly Review

| Metric | How to Measure | What It Tells You |
|--------|----------------|-------------------|
| Engagement rate | Likes+replies / impressions | Is S improving? |
| Reply rate | Replies / impressions | Is content sparking conversation? |
| Follower growth | Week-over-week change | Is E_total growing? |
| Profile visits | Analytics | Is content driving curiosity? |

### Phase Transition Signals

**Phase 1 → 2**: Feed is niche-relevant, replies get engagement
**Phase 2 → 3**: 20+ reciprocal engagers, posts get early momentum

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Hurts | What to Do Instead |
|--------------|--------------|-------------------|
| Chasing followers | N without D is worthless | Focus on engagement quality |
| Topic hopping | Dilutes R, confuses algorithm | Stay in your lane |
| Posting too often | Diversity penalty, quality drops | Fewer, better posts |
| Ignoring comments | Kills reciprocity, lowers D | Reply to everything |
| Controversial takes on people | Triggers blocks/mutes | Opinions on ideas, not people |
| Copying viral formats blindly | Doesn't fit your voice | Adapt patterns to your style |

---

## The Long Game

There are no shortcuts. The algorithm rewards:
- **Quality content** to a
- **Dense, engaged network** with
- **Consistent niche focus**

Everything else is noise.

Your job:
1. Be worth following
2. Build relationships with followers
3. Create content that triggers engagement

Followers come as a consequence of doing these three things well.

---

## Quick Reference

**Daily checklist** ({time budget}):
- [ ] {Key action 1 for their phase}
- [ ] {Key action 2 for their phase}
- [ ] {Key action 3 for their phase}

**Weekly checklist**:
- [ ] Review metrics
- [ ] Assess what content worked
- [ ] Adjust content mix

**Decision rule**: "Does this serve my [niche] audience and trigger engagement?"

---

*Strategy created: {date}*
*Phase: {current phase}*
*Review when: {transition trigger reached}*
```

### Phase 4: Refinement

**Present strategy section by section for validation**:

```
header: "Niche Position"
question: "Does this positioning capture who you are on X?"
[Display niche section]
options:
  - "Yes - this is me"
  - "Mostly - needs minor tweaks"
  - "No - let me explain"
```

For each "Mostly" or "No", gather specifics and update.

Validate:
- Niche positioning
- Phase assessment
- Daily actions (realistic given constraints?)
- Content pillars
- Anti-patterns relevance

**After each validation, append to discovery log**.

When user approves:
1. Mark "Refresh: read full log" in_progress
2. Read full discovery log
3. Make final updates to X_STRATEGY.md
4. Add version history

### Completion

Write X_STRATEGY.md to current directory.

Append final completion to discovery log:
```markdown
## Completion
Finished: {timestamp}
Phase determined: {phase}
Key focus: {primary variable}
```

## Key Principles

| Principle | Rule |
|-----------|------|
| **Reference first** | Read X_GROWTH_REFERENCE.md before interviewing |
| **Write before proceed** | Append to discovery log after EACH question |
| **Phase-appropriate** | Strategy must match their current state |
| **Realistic constraints** | Actions must fit their time budget |
| **Multi-signal content** | Every post should trigger 3+ engagement types |
| **Long-term focus** | No time-bound promises; state-based transitions |

## Output

Write `X_STRATEGY.md` to the current working directory.
