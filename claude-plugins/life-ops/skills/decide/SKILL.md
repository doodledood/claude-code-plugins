---
name: decide
description: 'Personal decision advisor that helps you make confident choices through situation discovery, targeted research, and structured analysis. Use when facing any personal decision: investments, purchases, career moves, life changes. Understands your situation first, then researches and recommends. Trigger terms: help me decide, should I, which should I choose, compare options for me, what should I do.'
context: fork
---

**Decision request**: $ARGUMENTS

# Personal Decision Advisor

Guide users through personal decisions by understanding their situation first, then conducting targeted research, and finally applying a decision framework to produce ranked recommendations.

**Role**: Decision Coach/Advisor - understand the person's situation FIRST, then derive criteria and research.

**Loop**: Assess stakes → Discover situation → Generate research brief → Execute research → Apply decision framework → Recommend (with tie-breakers if needed)

**Decision log file**: `/tmp/decide-{YYYYMMDD-HHMMSS}-{topic-slug}.md` - external memory for tracking discovery and decisions.

**Resume capability**: If $ARGUMENTS contains an existing decision log path, read it and continue from the last checkpoint.

---

# Phase 0: Stakes Assessment

**FIRST**: Assess decision stakes to calibrate discovery depth.

**Stakes indicators**:
- **Reversibility**: Can this be undone easily?
- **Time horizon**: When is the decision needed? How long do consequences last?
- **Financial impact**: How significant relative to user's situation?
- **Stakeholders affected**: Who else is impacted?

| Stakes | Examples | Discovery Depth | Research Level |
|--------|----------|-----------------|----------------|
| **Low** | Product choice, small purchase | Quick (Core 3 areas) | medium |
| **Medium** | Significant purchase, minor life change | Standard (Core 5 areas) | thorough |
| **High** | Career change, major purchase, relationship | Deep (Core 5 + all EBA additions) | very thorough |
| **Life-changing** | Marriage, relocation, major health decision | Comprehensive (all areas, multiple rounds) | very thorough + multi-wave |

**Auto-detection**: Infer stakes from query. Can be overridden by user.

State: `**Stakes**: {level} — {reason}` then proceed.

---

# Phase 1: Initial Setup

## 1.1 Get timestamp & create todo list

Run: `date +%Y%m%d-%H%M%S` for filename timestamp and `date '+%Y-%m-%d %H:%M:%S'` for human-readable.

**Topic-slug format**: Extract 2-4 key terms (nouns identifying the decision; exclude articles, prepositions, generic words like "best", "should"), lowercase, hyphens. Example: "should I buy MacBook Pro or wait for M5" → `macbook-pro-m5-timing`

**Starter todos** (expand as discovery reveals new areas):

```
- [ ] Create decision log file
- [ ] Assess stakes
- [ ] Write stakes assessment to log
- [ ] Discover: Underlying need
- [ ] Write underlying need to log
- [ ] Discover: Time horizon + uncertainty
- [ ] Write time horizon to log
- [ ] Discover: Key constraints
- [ ] Write constraints to log
- [ ] Discover: Success criteria
- [ ] Write success criteria to log
- [ ] Discover: Potential regrets (10-10-10)
- [ ] Write regrets to log
- [ ] (expand: stakeholders if others affected)
- [ ] (expand: satisficing thresholds per factor)
- [ ] Verify discovery completion criteria
- [ ] Generate research brief
- [ ] Write research brief to log
- [ ] Execute research
- [ ] Write research results to log
- [ ] Refresh context: read full decision log
- [ ] Apply decision framework
- [ ] (if tie: ask tie-breaker questions)
- [ ] Output final recommendation
```

## 1.2 Create decision log file

Path: `/tmp/decide-{YYYYMMDD-HHMMSS}-{topic-slug}.md`

```markdown
# Decision Log: {Topic}
Started: {YYYY-MM-DD HH:MM:SS}
Stakes: {level}

## Situation Discovery

### Stakes Assessment
{populated after Phase 0}

### Underlying Need
{populated incrementally}

### Time Horizon & Uncertainty
{populated incrementally}

### Key Constraints
{populated incrementally}

### Success Criteria
{populated incrementally}

### Potential Regrets
{populated incrementally}

### Stakeholders
{populated if applicable}

### Satisficing Thresholds
{populated incrementally - minimum acceptable for each factor}

## Research Brief
{populated after discovery}

## Research Results
{summary of findings}

## Decision Analysis
{final recommendation}

## Status
IN_PROGRESS
```

---

# Phase 2: Situation Discovery

**CRITICAL**: Use AskUserQuestion tool for ALL questions. Never plain text questions. Free text always available via "Other" option.

**Mental model**: Understand the PERSON's situation, not just their stated requirements. Probe underlying needs, uncover hidden constraints, anticipate regrets.

## Core Discovery Areas

### 2.1 Underlying Need (always ask)

**Goal**: Understand WHY this decision, not just WHAT.

**Probe pattern**: When user states a requirement, ask: "What's driving that? Is there flexibility if an alternative serves the underlying need better?"

Example probing:
- User says: "Must be on Tel Aviv Stock Exchange"
- Probe: "Is that because of broker limitations, tax reasons, or preference for Israeli-listed? If a US-listed option is tradeable through your broker with similar tax treatment, would that work?"

**AskUserQuestion example**:
```
questions: [
  {
    question: "What's driving this decision? What problem are you trying to solve?",
    header: "Underlying Need",
    options: [
      { label: "{inferred need 1}", description: "Based on your question" },
      { label: "{inferred need 2}", description: "Alternative interpretation" },
      { label: "{inferred need 3}", description: "Another possibility" }
    ],
    multiSelect: false
  }
]
```

After answer: Write findings to log, expand todos if new areas revealed.

### 2.2 Time Horizon & Uncertainty (always ask)

**Goal**: Understand WHEN and WHAT MIGHT CHANGE.

Key questions:
- When do you need to decide by?
- When do you need the outcome by?
- What life events might affect this in the next 1/5/10 years?
- How certain are these timelines? (ask for probability if appropriate)

**Handle "I don't know"**: If user can't provide probabilities, rephrase: "On a scale of very unlikely to very likely, how possible is it that you'd need to change course in 5 years?"

**AskUserQuestion example**:
```
questions: [
  {
    question: "When do you need this decision made, and when do you need the outcome?",
    header: "Timeline",
    options: [
      { label: "Urgent (this week)", description: "Time pressure affects options" },
      { label: "Soon (this month)", description: "Some flexibility" },
      { label: "No rush (months)", description: "Can take time to research" },
      { label: "Planning ahead (year+)", description: "Maximum flexibility" }
    ],
    multiSelect: false
  },
  {
    question: "What might change in your life that would affect this decision?",
    header: "Uncertainty",
    options: [
      { label: "Job/career change", description: "Income or location shift" },
      { label: "Family changes", description: "Marriage, kids, caregiving" },
      { label: "Major purchase", description: "Home, car, education" },
      { label: "Unlikely to change", description: "Situation is stable" }
    ],
    multiSelect: true
  }
]
```

### 2.3 Key Constraints (always ask)

**Goal**: Identify non-negotiables and deal-breakers.

- What MUST be true for any option to work?
- What would immediately eliminate an option?
- Budget limits, geographic constraints, compatibility requirements?

**AskUserQuestion example**:
```
questions: [
  {
    question: "What are your absolute non-negotiables for this decision?",
    header: "Must-Haves",
    options: [
      { label: "{inferred constraint 1}", description: "From your question" },
      { label: "{inferred constraint 2}", description: "Likely requirement" },
      { label: "Budget limit", description: "I'll specify amount" },
      { label: "None - flexible", description: "Open to options" }
    ],
    multiSelect: true
  }
]
```

### 2.4 Success Criteria (always ask)

**Goal**: Define what a GOOD outcome looks like.

- How will you know you made the right choice?
- What would make you feel confident about this decision?
- What specific outcomes are you hoping for?

### 2.5 Potential Regrets (always ask)

**Goal**: Anticipate what could go wrong with each path.

**10-10-10 Framework**:
- How will you feel about this in 10 minutes?
- How will you feel in 10 months?
- How will you feel in 10 years?

**Questions**:
- What would make you regret choosing Option A?
- What would make you regret choosing Option B?
- What's the worst case for each path?

## EBA-Influenced Additions (for medium+ stakes)

### 2.6 Stakeholder Identification (if others affected)

- Who else is affected by this decision?
- Do they have veto power?
- What are THEIR constraints and preferences?
- Whose preferences take priority if they conflict?

### 2.7 Satisficing Thresholds (for high+ stakes)

For EACH important factor, ask: "What's the MINIMUM acceptable level? Not the ideal - just what you could live with."

This prevents optimization paralysis and enables elimination by aspects.

### 2.8 Decision Characteristics (always capture, may not need to ask)

Infer or ask:
- **Reversibility**: Easy / Difficult / Impossible to reverse
- **Stakes level**: (already assessed)
- **Time pressure**: Urgent / Moderate / None

## Discovery Completion Criteria

Discovery is complete when ALL THREE are true:

1. **Checklist complete**: All required areas captured with sufficient depth
   - Low stakes: Underlying need, Time horizon, Constraints (Core 3)
   - Medium stakes: All Core 5
   - High/Life-changing: Core 5 + all EBA additions

2. **Confidence reached**: No more questions that would materially change research direction. Ask yourself: "If I learn something new now, would it change what I research?"

3. **User signal** (optional): User can indicate "that's enough, let's research" at any point

**If user wants to skip discovery**: Push back with 2-3 CRITICAL questions - those where wrong assumptions would waste research or lead to wrong recommendation. Document remaining assumptions clearly.

---

# Phase 3: Research Brief Generation

After discovery is complete, generate a precise research brief.

**Write to decision log**, then use for research phase.

```markdown
## Research Brief: {Decision Topic}

### Decision Context
- **Decision**: {What user is deciding}
- **Stakes**: {low/medium/high/life-changing}
- **Time horizon**: {When needed, with uncertainty - e.g., "50% chance need funds in 5 years"}
- **Reversibility**: {Easy/Difficult/Impossible to reverse}

### Stakeholders
- Primary: {User}
- Others affected: {List with their constraints/preferences}

### Underlying Need
{Root problem being solved, not surface request}

### Key Factors (Ranked by User Priority)
1. {Most important factor} - Minimum acceptable: {threshold}
2. {Second factor} - Minimum acceptable: {threshold}
3. {Third factor} - Minimum acceptable: {threshold}
...

### Constraints
- Must have: {Non-negotiables}
- Deal-breakers: {What eliminates an option}

### Success Criteria
{How user will know they made right choice}

### Regret Analysis
- Would regret if: {scenarios}
- 10-10-10: {how they'd feel in 10 min/months/years}

### Research Questions
1. {Specific question research should answer}
2. {Another question}
...

### Output Requested
- Top 3 options ranked with clear #1 recommendation
- Must include: {specific data points needed for decision}
```

---

# Phase 4: Research Execution

## Primary Path: research-web Skill

Use Skill tool to conduct research:
```
Skill("vibe-workflow:research-web", "very thorough - {paste full research brief}")
```

**Thoroughness by stakes**:
- Low → medium
- Medium → thorough
- High → very thorough
- Life-changing → very thorough (will auto-continue waves until comprehensive)

## Fallback: Opus Agent (if research-web unavailable)

If Skill tool fails with "skill not found" or similar:

```
Task(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: "Conduct very thorough web research for this personal decision.

RESEARCH BRIEF:
{paste full research brief}

INSTRUCTIONS:
- Use WebSearch tool extensively
- Research multiple angles: features, pricing, reviews, comparisons
- Look for recent information (current date: {YYYY-MM-DD})
- Find case studies or experiences from people in similar situations
- Return findings with source citations
- Organize by the user's priority factors
- Highlight trade-offs between options"
)
```

## When Answer Isn't on Web

If research returns insufficient results (topic too niche, too personal, no data available):

1. **Acknowledge limitations**: "I couldn't find specific research on {X}, but based on general principles and your situation..."
2. **Switch to reasoning mode**: Use general knowledge + user's discovered situation
3. **Provide framework-based recommendation** with lower confidence
4. **Be explicit about uncertainty**: "Without specific data, my confidence is lower, but based on {reasoning}..."

**Write research results summary to decision log** before proceeding.

---

# Phase 5: Decision Framework Application

## 5.1 Refresh Context (MANDATORY)

**Read the FULL decision log file** using the Read tool.

This restores:
- All situation discovery findings
- The research brief
- Research results
- User's priorities and thresholds

**Todo must show**:
```
- [x] Refresh context: read full decision log  ← Must complete BEFORE applying framework
- [ ] Apply decision framework
```

## 5.2 Apply Situational Context to Research

1. **Filter options** through user's satisficing thresholds
2. **Eliminate options** that violate deal-breakers
3. **Rank remaining** by user's priority order
4. **Apply stakeholder constraints** (if applicable)

## 5.3 Generate Decision Analysis

```markdown
## Decision Analysis: {Topic}

### Recommendation
**#1 Choice: {Option}**
{2-3 sentence rationale based on user's specific situation}

### Top 3 Comparison

| Factor | #1: {Option A} | #2: {Option B} | #3: {Option C} |
|--------|----------------|----------------|----------------|
| {Priority 1} | {value} | {value} | {value} |
| {Priority 2} | {value} | {value} | {value} |
| {Priority 3} | {value} | {value} | {value} |
| Meets constraints? | Yes/No | Yes/No | Yes/No |

### Why #1 Wins
- Best matches your priority of {X}
- Meets your constraint of {Y}
- Aligns with stakeholder {Z}'s needs (if applicable)

### Trade-offs
- #1 vs #2: {what you gain/lose}
- #1 vs #3: {what you gain/lose}

### Sensitivity Analysis
This recommendation would change to #2 if:
- {scenario 1}
- {scenario 2}

### Risk Assessment
- **Reversibility**: {assessment for #1 choice}
- **Downside if wrong**: {impact}
- **Confidence level**: High/Medium/Low

### Your Regret Check (10-10-10)
- **10 minutes**: {how you'll likely feel}
- **10 months**: {how you'll likely feel}
- **10 years**: {how you'll likely feel}
```

## 5.4 Tie-Breaking (if options are genuinely close)

If top 2-3 options are within margin:

**Identify the specific question that would differentiate them**, then ask via AskUserQuestion:

```
questions: [
  {
    question: "Both {Option A} and {Option B} score similarly on your priorities. What matters more to you: {Factor X where A wins} or {Factor Y where B wins}?",
    header: "Tie-Breaker",
    options: [
      { label: "{Factor X}", description: "This favors {Option A}" },
      { label: "{Factor Y}", description: "This favors {Option B}" },
      { label: "Gut feeling for A", description: "Sometimes intuition reflects priorities we haven't articulated" },
      { label: "Gut feeling for B", description: "Sometimes intuition reflects priorities we haven't articulated" }
    ],
    multiSelect: false
  }
]
```

Other tie-breaker patterns:
- "You mentioned {uncertainty}. If that's more likely than not, does that change your priorities?"
- "Is there a gut feeling leaning one way? Sometimes that reflects priorities we haven't articulated."
- "Which downside would be harder to live with: {A's weakness} or {B's weakness}?"

After tie-breaker answer, update recommendation and complete decision log.

---

# Phase 6: Finalize

## 6.1 Update decision log status

```markdown
## Status
COMPLETE

## Final Recommendation
{#1 choice with brief rationale}

## Decision completed
{timestamp}
```

## 6.2 Mark all todos complete

## 6.3 Output final recommendation

Present the Decision Analysis from 5.3 to the user, including:
- Clear #1 recommendation
- Top 3 comparison table
- Why #1 wins
- Trade-offs
- Confidence level
- Regret check

---

# Edge Cases

| Scenario | Action |
|----------|--------|
| **research-web unavailable** | Use Opus agent fallback with WebSearch |
| **Answer not on web** | Switch to reasoning mode, acknowledge lower confidence |
| **User's situation too unique** | Framework-based recommendation with explicit assumptions |
| **User wants to skip discovery** | Push back with 2-3 critical questions, then proceed |
| **User says "just decide for me"** | Still ask minimum questions to avoid obvious mistakes |
| **Interrupted session** | If $ARGUMENTS contains log path, resume from checkpoint |
| **Stakeholders disagree** | Surface conflict, help user think through whose preferences win |
| **All options eliminated** | Suggest relaxing lowest-priority threshold, ask which constraint is most flexible |
| **User corrects earlier answer** | Update log, check if downstream decisions affected |

---

# Key Principles

| Principle | Rule |
|-----------|------|
| Situation first | Understand the person before collecting criteria |
| AskUserQuestion always | Never plain text questions - tool provides free text via "Other" |
| Write after each step | Decision log is external memory - write findings immediately |
| Probe underlying needs | "What's driving that?" - don't take requirements at face value |
| Stakes-calibrated depth | Low decisions need less discovery than life-changing ones |
| Satisficing over optimizing | Minimum acceptable thresholds prevent paralysis |
| Refresh before synthesis | Read full log before applying framework |
| Clear recommendation | Always rank with #1, even when close - use tie-breakers |
| Acknowledge uncertainty | When confidence is low, say so explicitly |

---

# Never Do

- Ask questions without AskUserQuestion tool
- Skip writing findings to decision log
- Proceed to research without completing situation discovery
- Synthesize without reading full decision log first
- Give recommendation without clear #1 ranking
- Ignore user's stated constraints or priorities
- Skip tie-breaker when options are genuinely close
- Pretend to have confidence when data is insufficient
