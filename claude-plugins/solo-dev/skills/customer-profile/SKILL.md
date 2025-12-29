---
name: customer-profile
description: 'Iteratively craft a CUSTOMER.md document that precisely defines your ideal customer profile (ICP). This is the foundational document from which everything else (product, features, brand) derives. Uses parallel research agents and multi-choice workflow with feedback cycles.'
---

# Customer Profile Skill

Create the foundational CUSTOMER.md document through iterative refinement. This document precisely defines WHO your customer is, their problems, behaviors, and what they value. **Everything else in the product derives from this document.**

> **This is the most important document your product will ever have.** Product decisions, feature prioritization, and even brand guidelines all flow from understanding the customer. Get this right first.

## Overview

This skill supports both **creating a new customer doc** and **refining an existing one**. Users come back to adjust their ICP as they learn more about their market or pivot their product.

This skill guides you through:
0. **Check Existing** - Look for existing CUSTOMER.md; let user choose to refine or start fresh
1. **Discovery** - Clarifying questions about your product, market, and current understanding (keeps asking until confident)
2. **Research Phase** - Launch parallel agents to research ICP data, market, competitors (optional)
3. **Initial Draft** - Generate first CUSTOMER.md based on inputs + research
4. **Refinement & Completion** - Review sections, validate assumptions, update doc, finalize

**Returning users** can skip to Phase 4 to refine specific sections.

### Where the Value Comes From

The discovery questions give you a solid starting point, but **the real magic happens in Phase 2 (Research) and Phase 4 (Refinement)**:
- Research agents dig into real market data, competitor positioning, and ICP characteristics
- You validate whether the ICP resonates with your actual experience
- Each cycle sharpens the doc until it truly captures YOUR ideal customer

## Workflow

### Phase 0: Check for Existing Document

Before starting discovery, check if the user already has a CUSTOMER.md:

1. **Search for existing doc**: Use Glob to search for `**/CUSTOMER.md` in the current directory and common locations
2. **If found**: Read it and ask the user what they want to do

```
header: "Existing Customer Doc Found"
question: "I found an existing CUSTOMER.md. What would you like to do?"
options:
  - "Refine it - update specific sections based on new learnings"
  - "Start fresh - create a new customer profile from scratch"
  - "Review it - just read through what's there"
```

**If "Refine it"**: Ask which sections need updating, then jump to Phase 4 with targeted questions.

**If "Start fresh"**: Proceed to Phase 1 (Discovery) - will overwrite the existing doc.

**If "Review it"**: Read and display the doc, then ask what they want to do next.

3. **If NOT found**: Proceed directly to Phase 1 (Discovery)

### Phase 1: Discovery

Use AskUserQuestion tool with multi-choice options for EVERY question. **Put the recommended option FIRST** with "(Recommended)" suffix to reduce cognitive load.

**Recommendation Strategy**: Since there's no prior document, recommendations are based on:
- Most common patterns for solo devs/indie hackers
- Product type (once selected, informs subsequent recommendations)
- Sensible defaults that apply to most cases

**Question 1: Product Stage**

```
header: "Product Stage"
question: "Where is your product in its lifecycle?"
options:
  - "Early stage - have some users, finding PMF (Recommended)"
  - "Pre-launch - still building, no customers yet"
  - "Growth stage - PMF found, scaling acquisition"
  - "Mature - established product, optimizing"
```

Recommendation: "Early stage" is most common for solo devs using this tool.

**Question 2: Product Type**

```
header: "Product Type"
question: "What type of product are you building?"
options:
  - "B2B SaaS - software for businesses (Recommended)"
  - "Developer tool - for engineers/developers"
  - "B2C app - consumer application"
  - "Marketplace/Platform - connecting buyers and sellers"
  - "Content/Media - newsletter, course, community"
  - "Physical product - hardware or tangible goods"
```

Recommendation: "B2B SaaS" is most common. Use selected type to inform later recommendations.

**Question 3: Problem Space** (Free text)

```
header: "Problem"
question: "What core problem does your product solve?"
freeText: true
placeholder: "Describe the main pain point (e.g., 'Teams waste hours manually syncing data between tools')"
```

This is essential context that's hard to multiple-choice. Get 1-2 sentences.

**Question 4: Current Customer Knowledge**

```
header: "Current Understanding"
question: "How well do you know your ideal customer today?"
options:
  - "Somewhat - have some customers, seeing some patterns (Recommended)"
  - "Very well - I've talked to many, have clear patterns"
  - "Vaguely - have hypotheses but not validated"
  - "Not at all - need to figure this out from scratch"
```

Recommendation: "Somewhat" - most users have some signal but need help structuring it.

**Question 5: Primary Value Proposition**

```
header: "Value Prop"
question: "What's the PRIMARY value you deliver?"
options:
  - "Save time - automation, efficiency (Recommended)"
  - "Save money - cost reduction, better ROI"
  - "Make money - revenue generation, growth"
  - "Reduce risk - security, compliance, reliability"
  - "Improve quality - better outcomes, fewer errors"
  - "Enable capability - do something previously impossible"
  - "Provide enjoyment - entertainment, satisfaction"
```

Recommendation: "Save time" is the most common value prop for SaaS products.

**Question 6: Purchase Decision**

Recommendation based on product type:
- B2B SaaS → "Team lead" or "Individual user"
- Developer tool → "Individual user"
- B2C → "Individual user"
- Enterprise → "Multiple stakeholders"

```
header: "Buyer Type"
question: "Who makes the purchase decision?"
options:
  - "Individual user - they buy for themselves (Recommended for B2C/dev tools)"
  - "Team lead - buys for their team (Recommended for B2B SaaS)"
  - "Executive/C-suite - strategic purchase"
  - "Procurement/IT - goes through formal process"
  - "Multiple stakeholders - committee decision"
  - "No purchase - free product, other monetization"
```

**Question 7: Known Customer Characteristics**

```
header: "Customer Traits"
question: "What do you know about your best customers? (Select all that apply)"
options:
  - "Pain intensity (desperate vs nice-to-have) (Recommended)"
  - "Specific job title or role (Recommended)"
  - "Behavioral patterns (power users, specific workflows)"
  - "Company size or type"
  - "Technical skill level"
  - "Specific industry or vertical"
  - "Geographic location"
multiSelect: true
```

Recommendation: "Pain intensity" and "Job title/role" are the most actionable traits for targeting.

**Question 7b: Trait Details (Follow-up)**

For EACH trait selected in Q7, ask a targeted follow-up to capture specifics:

| If Selected | Follow-up Question |
|-------------|-------------------|
| Job title/role | "What specific titles? (e.g., 'Engineering Manager', 'Head of Product')" |
| Company size | "What size range? (e.g., '10-50 employees', 'Series A-B startups')" |
| Technical skill | "What skill level? (e.g., 'Can write code', 'Uses no-code tools')" |
| Industry | "Which industries? (e.g., 'Fintech', 'Healthcare SaaS')" |
| Geographic | "Which regions? (e.g., 'US-based', 'English-speaking markets')" |
| Behavioral | "What behaviors? (e.g., 'Uses Slack daily', 'Already has a workflow')" |
| Pain intensity | "How desperate? (e.g., 'Hair on fire', 'Nice efficiency gain')" |

Use free-text for these follow-ups - the specifics matter and are hard to predict.

**Question 8: What They're NOT**

Recommendation based on product type:
- B2B SaaS (small team) → Recommend "Enterprise" as anti-persona
- Developer tool → Recommend "Beginners" as anti-persona
- B2C consumer → Recommend "Enterprise" as anti-persona

```
header: "Anti-Personas"
question: "Who is explicitly NOT your customer? (Select all that apply)"
options:
  - "Enterprise (too slow, complex sales) (Recommended for solo devs)"
  - "Price-sensitive buyers (race to bottom) (Recommended)"
  - "Beginners (need too much hand-holding)"
  - "SMB (can't afford, high churn)"
  - "Experts (don't need the product)"
  - "Specific industry (bad fit)"
  - "Not sure yet - need to figure this out"
multiSelect: true
```

Recommendation: Most solo devs should avoid "Enterprise" (sales cycle too long) and "Price-sensitive" (race to bottom).

**Question 8b: Anti-Persona Details (Follow-up)**

For EACH anti-persona selected in Q8 (except "Not sure yet"), ask why:

| If Selected | Follow-up Question |
|-------------|-------------------|
| Enterprise | "Why avoid enterprise? (e.g., 'Sales cycle too long', '6+ month deals kill us')" |
| SMB | "Why avoid SMB? (e.g., 'Churn too high', 'Can't afford $X/mo')" |
| Beginners | "Why avoid beginners? (e.g., 'Support burden', 'Don't understand the value')" |
| Experts | "Why avoid experts? (e.g., 'Build their own', 'Our solution is too basic')" |
| Price-sensitive | "Why avoid price-sensitive? (e.g., 'Race to bottom', 'High churn')" |
| Specific industry | "Which industries and why? (e.g., 'Healthcare - compliance nightmare')" |

Use free-text - understanding the WHY behind anti-personas is critical.

**Question 9: Research Needs**

Recommendation based on customer knowledge (Q4):
- "Not at all" or "Vaguely" → Recommend "Full research"
- "Somewhat" → Recommend "Light research"
- "Very well" → Recommend "No research"

```
header: "Research"
question: "Do you want me to research your market and competitors to inform the ICP?"
options:
  - "Light research - just validate my assumptions (Recommended)"
  - "Yes, full research - ICP patterns, competitors, market data (takes longer)"
  - "No research - I have enough context, just help me structure it"
```

Default recommendation: "Light research" balances speed with validation.

**Question 10: Additional Context** (Free text)

```
header: "Context"
question: "Anything else I should know?"
freeText: true
placeholder: "Product name, URL, existing customers, specific hypotheses, competitors you know about..."
```

**Question 11: Current State & Triggers** (Free text)

```
header: "Current State"
question: "What does your ICP do TODAY to solve this problem (before your product)?"
freeText: true
placeholder: "e.g., 'They use spreadsheets and manually update them weekly' or 'They don't solve it at all'"
```

```
header: "Triggers"
question: "What triggers them to actively seek a solution?"
freeText: true
placeholder: "e.g., 'When they miss a deadline due to the problem' or 'When a new team member joins and asks why they do it this way'"
```

**Question 12+: Gap-Filling Questions**

After the core questions, assess whether you have enough clarity to proceed. If ANY of these are unclear, ask follow-up questions:

| Gap | Follow-up Needed |
|-----|-----------------|
| Unclear ICP boundaries | "Where exactly is the line between good and bad customers?" |
| Vague pain points | "Can you give me a specific example of when this pain happens?" |
| Unknown current state | "Walk me through what they do today, step by step" |
| Unclear triggers | "What's the moment when they realize they need to solve this?" |
| Missing context | "What else should I know about their world?" |

**Keep asking until you are highly confident** about:
1. Who the ICP is (specific, not vague)
2. Who they are NOT (clear anti-personas)
3. What problem they have (specific pain)
4. What they do today (current state)
5. What triggers them to seek a solution
6. How research should be focused (if requested)

Only proceed to Phase 2/3 when gaps are filled.

### Phase 2: Research Phase (If Requested)

If user requested research, launch 2-3 parallel opus agents to gather data. **Skip this phase if user said "No research"**.

**IMPORTANT**: Use the Task tool to launch these agents IN PARALLEL (single message with multiple Task calls):

**Agent 1: ICP Pattern Researcher**
```
Launch Task agent (subagent_type: general-purpose, model: opus) with prompt:
"Research ideal customer profile patterns for [product type] in the [problem space].
Find:
1. Common job titles and roles of buyers
2. Company characteristics (size, stage, industry)
3. Behavioral indicators of high-intent buyers
4. Pain points that drive purchase decisions
5. Typical objections and concerns

Use WebSearch to find relevant data. Focus on actionable patterns, not generic advice.
Return structured findings."
```

**Agent 2: Competitor/Market Researcher**
```
Launch Task agent (subagent_type: general-purpose, model: opus) with prompt:
"Research the competitive landscape for [product description].
Find:
1. Key competitors and their target customers
2. How competitors position their ICP
3. Gaps in the market (underserved segments)
4. Pricing tiers and what they signal about target customer
5. Customer reviews/complaints that reveal unmet needs

Use WebSearch to find relevant data.
Return structured findings."
```

**Agent 3: Anti-Persona Researcher** (if user was unsure about anti-personas)
```
Launch Task agent (subagent_type: general-purpose, model: opus) with prompt:
"Research who are the WRONG customers for [product type] solving [problem].
Find:
1. Customer segments that typically churn
2. Buyer types that require too much support
3. Use cases that are poor fits
4. Warning signs in the sales process
5. Communities/channels to avoid

Use WebSearch to find relevant data.
Return structured findings."
```

**Fallback Handling**

If research tools are unavailable or agents fail:
1. Inform the user: "Research tools unavailable. Proceeding with discovery data only."
2. Skip to Phase 3 with a note in the document that research was not performed
3. Recommend the user manually research competitors and validate assumptions

**Research Synthesis Step**

After all agents complete, synthesize findings BEFORE generating the document:

1. **Combine agent outputs** into a structured summary:
   - **ICP Patterns Found**: [Key patterns from Agent 1]
   - **Competitive Insights**: [Key findings from Agent 2]
   - **Anti-Persona Signals**: [Key findings from Agent 3]

2. **Present summary to user** for validation:
   ```
   header: "Research Summary"
   question: "Here's what I found. Does this align with your understanding?"
   [Display synthesized findings]
   options:
     - "Yes - this matches my experience"
     - "Partially - some insights are new/surprising"
     - "No - this doesn't match my market"
   ```

3. **If "Partially" or "No"**: Ask what's different and adjust before generating doc:
   ```
   header: "Adjustments"
   question: "What should I adjust based on your real-world experience?"
   freeText: true
   placeholder: "e.g., 'The competitors mentioned aren't our real competition - we compete with spreadsheets'"
   ```

4. **Reconcile research with user knowledge** - user's direct experience trumps generic research. Note discrepancies in the doc as areas to validate.

### Phase 3: Initial Document Generation

After discovery (and optional research), generate the first CUSTOMER.md.

Use this structure:

```markdown
# [Product Name] Ideal Customer Profile

> **THE Guiding Principle**: [One sentence that captures the north star for customer decisions]

---

## The ICP: [Short Label]

**The ICP is NOT "[common misconception]."** It's **[precise definition]**.

| Type | Mindset | Response to [Product] |
|------|---------|----------------------|
| **[ICP Label]** | "[Their worldview]" | "[How they react]" |
| **[Anti-persona Label]** | "[Their worldview]" | "[Why they reject]" |

[Brief explanation of why this distinction matters]

---

## Current State & Triggers

**What they do today** (before your product):
- [Current workflow/tool/process]
- [Workarounds they use]
- [Time/money spent on the problem]

**What triggers them to seek a solution**:
- [Specific event or moment]
- [Pain threshold that tips them over]
- [External pressure (boss, deadline, competitor)]

---

## Profile Data

**Primary Psychographic**: [Core mindset and motivation - what drives them]

**The [ICP] vs [Anti-persona] Split**:

| Trait | [ICP] | [Anti-persona] |
|-------|-------|----------------|
| **Goal** | [What they want] | [What they want] |
| **Mindset** | [How they think] | [How they think] |
| **Response to [product category]** | [Positive signal] | [Negative signal] |

**[Anti-persona] objections (why they're NOT ICP):**
- "[Typical objection 1]"
- "[Typical objection 2]"
- "[Typical objection 3]"

**[ICP] signals:**
- "[Positive indicator 1]"
- "[Positive indicator 2]"
- "[Positive indicator 3]"

**Demographics**:
- **[Key demographic 1]**: [Specifics]
- **[Key demographic 2]**: [Specifics]
- **[Key demographic 3]**: [Specifics]

**Secondary Audience**: [Who else benefits but isn't primary focus]

**Out of Scope**: [Explicit exclusions]

---

## Audiences to Avoid

| Audience | Why | Signs |
|----------|-----|-------|
| **[Segment 1]** | [Reason] | [How to identify] |
| **[Segment 2]** | [Reason] | [How to identify] |
| **[Segment 3]** | [Reason] | [How to identify] |

---

## ICP Characteristics

### Cognitive

| Characteristic | Signal |
|----------------|--------|
| **[Trait 1]** | "[Observable behavior]" |
| **[Trait 2]** | "[Observable behavior]" |
| **[Trait 3]** | "[Observable behavior]" |

### Behavioral

| Characteristic | Signal |
|----------------|--------|
| **[Trait 1]** | "[Observable behavior]" |
| **[Trait 2]** | "[Observable behavior]" |
| **[Trait 3]** | "[Observable behavior]" |

---

## Pain Points (User Voice)

1. **"[Pain point in customer's words]"** - [Brief context]
2. **"[Pain point in customer's words]"** - [Brief context]
3. **"[Pain point in customer's words]"** - [Brief context]
4. **"[Pain point in customer's words]"** - [Brief context]
5. **"[Pain point in customer's words]"** - [Brief context]

---

## What the ICP Values (In a Solution)

These are things the ICP cares about when evaluating solutions. Use these to guide product decisions.

| What They Value | Why It Matters to Them |
|-----------------|----------------------|
| [Value 1] | [Why this matters for their workflow/goals] |
| [Value 2] | [Why this matters for their workflow/goals] |
| [Value 3] | [Why this matters for their workflow/goals] |
| [Value 4] | [Why this matters for their workflow/goals] |

> Example: "Fast interface" matters because "Power users have zero patience - they'll leave if it's slow"

---

## Goals & Success

- **Primary**: [Main outcome they want]
- **Secondary**: [Supporting outcome]
- **Tertiary**: [Nice-to-have outcome]

**Success Metric**: [How they measure success]

---

**The North Star**: [One sentence that summarizes what success looks like for the ICP]

---

## Quick Reference

**One-line ICP summary**: [ICP Label] who [core motivation].

**Product decision checklist**:
- [ ] Does this feature serve [ICP description]?
- [ ] Would this repel or confuse [Anti-persona]? (Good if yes)
- [ ] Does this address a real pain point listed above?
- [ ] Does this align with what the ICP values?
```

**Template Flexibility**

The template above is a starting point. Customize based on the product:

1. **Add product-specific context sections** as needed:
   - Platform/environment context (e.g., skill level tables, tool ecosystem maps)
   - Domain-specific terminology or skill levels
   - Industry-specific pain points or workflows
   - Multiple ICP segments if relevant (but keep it focused)

2. **Use callout blockquotes** for important nuances:
   ```markdown
   > **Nuance**: Even [ICP] sometimes prefer [alternative] when [condition].
   > **Key insight**: [Anti-personas] congregate in [specific places].
   ```

3. **Emphasize user-voice quotes** - use actual customer language:
   ```markdown
   **[ICP] signals:**
   - "If the math is correct, I'll try it"  ← Real customer quote
   - Doesn't argue about principles         ← Observable behavior
   ```

4. **Add comparison tables** wherever ICP vs Anti-persona distinctions exist

**What NOT to include** (save for other docs):
- Pricing strategy → Business Model doc
- Messaging/voice → Brand Guidelines doc
- Go-to-market → Marketing Strategy doc
- Feature roadmap → Product Roadmap doc

Write this file to the current working directory as `CUSTOMER.md`.

### Phase 4: Refinement Cycles & Completion

After generating the initial document, begin iterative refinement.

**Expected cycles**: Most users need **2-3 refinement cycles** to get from "this is okay" to "this captures my customer." Don't rush - each cycle sharpens the doc.

**Step 4.1: Section-by-Section Review**

For each major section, ask for validation:

```
header: "ICP Definition"
question: "Does this ICP definition feel accurate?"
[Display the ICP section]
options:
  - "Yes - this captures my ideal customer"
  - "Mostly - needs minor tweaks"
  - "No - this misses the mark"
```

If not "Yes", follow up:

```
header: "Feedback"
question: "What's wrong with the ICP definition?"
options:
  - "Too broad - needs to be more specific"
  - "Too narrow - excludes valid customers"
  - "Wrong characteristics - missing key traits"
  - "Wrong anti-persona - that's actually a good customer"
  - "Missing a customer segment entirely"
  - "Other - let me explain"
multiSelect: true
```

**Step 4.2: Pain Points Validation**

```
header: "Pain Points"
question: "Do these pain points match what you hear from customers?"
[Display pain points section]
options:
  - "Yes - these are the real pain points"
  - "Mostly - but some are wrong or missing"
  - "No - need to rewrite these"
```

**Step 4.3: Anti-Personas Validation**

```
header: "Anti-Personas"
question: "Are these the right people to avoid?"
[Display anti-personas section]
options:
  - "Yes - avoid these segments"
  - "Mostly - some adjustments needed"
  - "No - wrong exclusions"
```

**Step 4.4: Update Document**

Based on ALL feedback:

1. Identify patterns in feedback (what's consistently wrong?)
2. Update CUSTOMER.md with refined definitions
3. Add specific examples where needed
4. Strengthen anti-persona definitions if issues keep appearing

**Step 4.5: Check Completion**

```
header: "Continue?"
question: "Want to refine more sections?"
options:
  - "Yes - let's review another section"
  - "No - the customer doc is good enough for now"
  - "Almost done - one more pass should perfect it"
```

If "Yes" or "Almost done", return to Step 4.1.

**Step 4.6: Completion** (When user says "No" to more refinement)

When user indicates they're done:

1. Add a "Version History" section noting when created/updated
2. Add a "Usage Instructions" section for how to use the doc
3. Display final document summary
4. Remind user to keep CUSTOMER.md updated as they learn more

**Final additions to append:**

```markdown
---

## Version History

- **v1.0** - [Date] - Initial creation

## Usage Instructions

This is your **foundational document**. Use it to:
- **Feature prioritization**: "Would our ICP want this? Does it address their pain?"
- **Product decisions**: "Does this align with what the ICP values?"
- **Scope control**: "Is this for our ICP or an anti-persona?"
- **User research**: "Are we talking to ICPs or anti-personas?"
- **Validation**: "Does this person match our ICP signals?"

**The single question**: "Does this serve [ICP description]?"

**Downstream docs** (create these AFTER CUSTOMER.md is solid):
- Brand Guidelines (how to talk to them)
- Product Roadmap (what to build for them)
- Business Model (how to charge them)
```

## Key Principles

### Information Density
- Every line must be actionable for decisions
- No fluff, no explanations "for humans"
- Concrete examples over abstract descriptions
- Specific signals over vague guidelines

### Research-Backed (Initially & When Requested)
- Parallel agents gather real market data
- Validate assumptions against competitive landscape
- Find patterns the user might not see

### Iterative Refinement
- Section-by-section validation catches errors
- Real customer conversations surface issues
- Track what changes between versions

### Reduce Cognitive Load
- ALWAYS use AskUserQuestion tool when available
- **Put recommended option FIRST** with "(Recommended)" suffix
- User should be able to accept all defaults and get a solid result
- Present multi-choice questions to minimize typing
- Limit options to 6-8 max per question
- Use multiSelect for non-exclusive choices
- Only use free-text for essential context

### Question Until Confident
- **Never proceed with ambiguity** - if something is unclear, ask
- Keep asking follow-up questions until you have specific, actionable answers
- Gaps in understanding lead to generic, useless output
- Before moving to next phase, verify: "Do I know enough to generate something specific?"
- User's time spent answering questions upfront saves iteration time later

### Ground in Reality, Not Wishes
- **Define the ICP you HAVE, not the one you WISH you had**
- Base the profile on actual customers, real conversations, observable patterns
- Aspirational ICPs (big logos, impressive titles) lead to products nobody buys
- If pre-launch with no customers: define hypotheses, but mark them as unvalidated

## Output Location

Write `CUSTOMER.md` to the current working directory (or user-specified path).
