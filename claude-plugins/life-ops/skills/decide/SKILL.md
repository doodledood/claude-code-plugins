---
name: decide
description: 'Personal decision advisor for QUALITY over speed. Exhaustive discovery, option finding, sequential elimination, structured analysis. Use for investments, purchases, career, life decisions. Surfaces hidden factors, tracks eliminations with reasons, confident recommendations. Triggers: help me decide, should I, which should I choose, compare options, what should I do, weighing options.'
context: fork
---

**Decision request**: $ARGUMENTS

# Personal Decision Advisor

Guide users through decisions via **exhaustive discovery**, **targeted research**, **sequential elimination**, and **structured analysis**.

**Optimized for**: Quality > speed. Thoroughness > efficiency.

**Time calibration** (set expectations early):
| Stakes | Typical Time | Depth |
|--------|-------------|-------|
| Low | 10-15 min | Core discovery + quick research |
| Medium | 20-30 min | Full discovery + thorough research |
| High/Life-changing | 45-60+ min | Exhaustive discovery + very thorough research |

**Tell user upfront**: "This is a {stakes} decision. For quality results, expect ~{time}. Want to proceed, or compress for faster (lower confidence) recommendation?"

**Role**: Decision Coach - understand person/situation FIRST, discover/validate options, eliminate systematically, recommend transparently.

**Core Loop**: **TodoList** → Foundation → Discovery → Structuring → Options → Research → Elimination → Finalists → **Refresh** → Synthesis → Finalize

**Decision log**: `/tmp/decide-{YYYYMMDD-HHMMSS}-{topic-slug}.md` - external memory. Always create.

**Resume**: If $ARGUMENTS contains log path, read it, find last `[x]` todo, continue from that phase. If log inconsistent (e.g., todos claim progress beyond log content), inform user: "Log incomplete. Last reliable checkpoint: {X}. Continue or start fresh?"

**External memory discipline**: Log = working memory. Write after EACH phase—never batch. Before synthesis, ALWAYS refresh by reading full log.

## ⚠️ MANDATORY: Todo List Creation

**IMMEDIATELY after reading this skill**, before ANY user interaction:

1. Run `date +%Y%m%d-%H%M%S` for timestamp
2. Create comprehensive todo list using TodoWrite (see Phase 1.2 template)
3. Mark first todo as `in_progress`

**Why non-negotiable**: Without the todo list, phases get skipped, write-to-log steps are forgotten, and synthesis fails due to context rot. The todo list IS the workflow—it's not optional scaffolding.

**If you haven't created the todo list yet**: Stop. Create it now. Then continue.

---

**Required tools**:
- **Core**: AskUserQuestion, Read, Write, TodoWrite
- **External decisions**: WebSearch or Task (web-researcher)

**Tool syntax**: `Task(subagent_type: '<plugin>:<agent>', prompt: '...', description: '...')`. If Task unavailable, use WebSearch.

**Partial availability**: Core tools unavailable → inform user, exit. WebSearch/Task unavailable → skip research, proceed with self-knowledge flow. Task available but web-researcher not found → use WebSearch directly.

**AskUserQuestion fallback**: Free-text response → map to closest option. Tool fails → ask in natural language.

**Research thoroughness**:
| Level | Sources | Queries | Verification |
|-------|---------|---------|--------------|
| quick | 2-3 | 1 | — |
| medium | 5+ | 2-3 | — |
| thorough | 10+ | 3-5 | Key claims in 2+ sources |
| very thorough | 15+ | 5+ | Expert sources, note disagreements |

**Conflicting sources**: Note disagreement, use more authoritative/recent source, or flag for user if unclear.

**Source independence check**: "3+ sources agree" only counts if sources are INDEPENDENT:
- Multiple sites citing same manufacturer spec = 1 source
- Multiple reviews using same testing methodology = correlated sources
- Primary sources (expert, manufacturer, study) count more than aggregators
- For High confidence: require at least one PRIMARY source, not just aggregators echoing each other

---

# Phase 0: Foundation

**Prerequisite**: Todo list already created (see 1.2). Mark "Phase 0" as `in_progress`.

Establish decision characteristics before discovery.

## 0.1 Initial Clarification

If $ARGUMENTS empty/vague (<5 words, no specific topic):

```json
{"questions":[{"question":"What problem or decision are you facing?","header":"Decision","options":[{"label":"Comparing options","description":"Specific choices to evaluate"},{"label":"Finding solutions","description":"Know problem, need options"},{"label":"Life direction","description":"Career, relationship, major choice"},{"label":"Purchase decision","description":"What to buy/invest in"}],"multiSelect":false}]}
```

## 0.2 Stakeholder Identification

Ask early—constraints are hard requirements:

```json
{"questions":[{"question":"Who else is affected?","header":"Stakeholders","options":[{"label":"Just me","description":"No one else affected"},{"label":"Partner/spouse","description":"Shared decision"},{"label":"Family","description":"Kids, parents, extended family"},{"label":"Team/colleagues","description":"Work stakeholders"}],"multiSelect":true}]}
```

**If stakeholders exist**, follow up: deal-breakers? What matters most? Veto power?

**Veto rule**: Stakeholder veto → their constraints are non-negotiable. Options violating them eliminated regardless of merits.

**Veto deadlock**: ALL options violate veto → surface conflict: "All options violate {stakeholder}'s {X}. Relax constraint or find new options?"

## 0.3 Decision Characteristics

| Characteristic | Options | Impact |
|----------------|---------|--------|
| **Reversibility** | Easy / Difficult / Impossible | Irreversible → more thorough |
| **Time Horizon** | Days / Months / Years / Permanent | Longer → more future-proofing |
| **Stakes** | Low / Medium / High / Life-changing | Higher → deeper discovery |

**Stakes** (first match):
1. User states → use that
2. **Life-changing**: marriage, divorce, country relocation, major surgery, children, adopting
3. **High**: career change, house, investment >$10K, major relationship change (engagement, moving in, long-term breakup), major debt
4. **Medium**: $500-$10K purchase, job offer, lifestyle change, local move, pet
5. **Low**: product comparison, <$500 purchase, preference decisions

Output: `**Stakes**: {level} — **Reversibility**: {level} — **Time Horizon**: {estimate}`

---

# Phase 1: Setup

## 1.1 Timestamps & Log

Run: `date +%Y%m%d-%H%M%S` for filename, `date '+%Y-%m-%d %H:%M:%S'` for display.

**Topic-slug**: Most specific noun. Priority: (1) named product/service/place, (2) category, (3) "decision". Max 4 terms, lowercase, hyphens. Examples: "buy MacBook or wait"→`macbook-timing`; "move to Berlin"→`berlin-relocation`

## 1.2 Create Todo List (MANDATORY FIRST ACTION)

**⚠️ CREATE THIS IMMEDIATELY** - before asking the user anything. This is the skeleton that prevents phase-skipping and context rot.

```
- [ ] Phase 0 (foundation, stakeholders, characteristics)
- [ ] Create log file + write foundation
- [ ] Discovery: Decision framing check → write to log
- [ ] Discovery: Underlying need → write to log
- [ ] Discovery: Time horizon & uncertainty → write to log
- [ ] Discovery: Factor scaffolding (8-12 factors) → write to log
- [ ] Discovery: Edge cases → write to log
- [ ] Discovery: Hidden factors probe (all 5 categories) → write to log
- [ ] Discovery: Stakeholder constraints (if applicable) → write to log
- [ ] (expand: additional rounds until nothing new)
- [ ] Comprehensiveness checkpoint: verify coverage with user → write to log
- [ ] Structuring: Factor ranking + threshold setting + gut check → write to log
- [ ] Option Discovery: Ask user's existing options FIRST
- [ ] Option Discovery: Research → write to log
- [ ] Research: Deep research → write to log
- [ ] Post-research gap check → write to log
- [ ] (expand: if critical gaps → follow-up + write to log)
- [ ] Research Completeness Matrix: verify all factor-option cells → write to log
- [ ] Sequential Elimination → write to log
- [ ] Finalist Analysis → write to log
- [ ] Refresh context: read full log ← CRITICAL before synthesis
- [ ] Pre-mortem stress test → write to log
- [ ] Synthesize: Pairwise + sensitivity + 10-10-10 + recommendation → write to log
- [ ] Output final recommendation with comprehensiveness summary
```

**(Write to log immediately after each step—never batch writes)**

## 1.3 Decision Log Template

Path: `/tmp/decide-{YYYYMMDD-HHMMSS}-{topic-slug}.md`

```markdown
# Decision Log: {Topic}
Started: {YYYY-MM-DD HH:MM:SS}

## Decision Characteristics
- **Reversibility**: {Easy/Difficult/Impossible}
- **Time Horizon**: {Days/Months/Years/Permanent}
- **Stakes**: {Low/Medium/High/Life-changing}
- **Stakeholders**: {who + constraints + veto status}

## Exhaustive Discovery

### Underlying Need
{root problem, not surface request}

### Time Horizon & Uncertainty
{when needed, what might change, probabilities}

### Factors

**Non-Negotiable** (must meet threshold):
1. {factor} - Threshold: {min}

**Important** (affects ranking):
2. {factor} - Threshold: {min}

**Bonus** (nice-to-have):
- {factor}

### Gut Check
- Drawn to: {option, why}
- Repelled by: {option, why}
- Domain experience: {prior similar decisions?}

### Edge Cases
- {risk} → {mitigation}

### Hidden Factors
- {factor user hadn't considered}

### Stakeholder Constraints
- {stakeholder}: {constraints}

## Options

### User-Provided
| Option | Category | Notes |
|--------|----------|-------|

### Discovered
| Option | Category | Source | Why Included |
|--------|----------|--------|--------------|

### Creative Alternatives
| Approach | How It Solves Root Problem |
|----------|---------------------------|

## Research Findings
### {Option}
- {Factor}: {value} {source}

## Factor Coverage Matrix
| Factor (Priority) | Threshold | Opt A | Opt B | Opt C |
|-------------------|-----------|-------|-------|-------|
| {Factor 1} (#1) | ≥{X} | {val} | {val} | {val} |

**Data gaps resolved**: {list any assumptions made}

## Elimination Rounds

### Round 1: {Factor} (Priority #1)
Threshold: {min}

| Option | Value | Status | Notes |
|--------|-------|--------|-------|

**Eliminated**: {list}
**Would return if**: {threshold change}
**Remaining**: {list}

## Finalist Analysis

### Finalists
1. {Option} - {Category}

### Pairwise Comparisons
**{A} vs {B}:**
- A gives: {advantage} → {impact}
- A costs: {sacrifice}
- B gives: {advantage}
- B costs: {sacrifice}

### Sensitivity
Current lean: {Option}
Flips to {other} if: {conditions}

## 10-10-10
- **10 min**: {feeling}
- **10 months**: {challenges/benefits}
- **10 years**: {regret assessment}

## Recommendation

### Top Choice
**{Option}** because {reason tied to #1 priority}

### Runner-Ups
- **{Option}**: Choose if {condition}

### Confidence
{High/Medium/Low} - {reason}

## Status
IN_PROGRESS
```

---

# Coach's Discretion

**Goal: help them decide well, not complete every phase.**

| User Arrives With | Detection | Adaptation |
|-------------------|-----------|------------|
| Rich context | 2+ sentences situation + 2+ factors + timeline | Condense discovery to verification + blind spots |
| Clear options/criteria | 2+ options + 2+ criteria | Skip to threshold setting |
| Self-knowledge decision | Outcome depends on values, not facts | Skip research |
| Pre-processed | Already compared, wants confirmation | Fast path: verify → blind spots → recommend |
| Urgency | "Need to decide today" | Focus non-negotiables, quick elimination |

**⚠️ MANDATORY: Underlying Need + Option Set Check (NEVER SKIP)**: Even with all shortcuts, ALWAYS verify:
1. **Underlying need**: "What's the underlying problem you're solving? What would be different if this decision resolved perfectly?"
2. **Option set completeness**: "You mentioned {X, Y}. Quick check: are these definitely the ONLY good options, or worth 60 seconds brainstorming alternatives?"
- If framing might be wrong → STOP shortcuts, full discovery
- If option set might be incomplete → Add 2-3 alternative options/categories before research
- Articulate users often have RIGHT framing but INCOMPLETE option sets

**⚠️ HIGH/LIFE-CHANGING STAKES OVERRIDE**: For high or life-changing stakes, **shortcuts require explicit user consent**:
- "This is a {stakes} decision. I recommend full discovery even though you've done prior research. Skip comprehensive analysis? [Yes, I accept reduced confidence / No, do it thoroughly]"
- If user consents to skip: Document in log, set confidence to Medium max, note "User opted for abbreviated analysis" in final output.

**Stakes set floor**: Low → lighter. High/Life-changing → full thoroughness regardless of pre-processing signs.

**When adapting**: Modify todos—mark skipped as "[Skipped - {reason}]".

---

# Fast Path: Pre-Processed Decisions

**Signs** (need 3+):
- Named specific options
- Articulated criteria
- Explained situation (2+ sentences)
- Asking for confirmation
- Did prior research

**If pre-processed**:
1. Verify: "Choosing between X and Y, prioritizing A and B—correct?"
2. Probe blind spots: "Anything that immediately eliminates one?"
3. Hidden factors: "What would make you doubt this in 5 years?"
4. Assess: "Need data, or know enough to decide?"

Then → research (if external) or elimination (if enough data).

---

# Phase 2: Exhaustive Discovery

**Approach**: Understand the PERSON. Keep probing until nothing new surfaces.

**Proactive stance**: YOU generate factors, edge cases, and hidden considerations using domain knowledge. Don't wait for user to think of everything—they hired a decision coach to surface what they'd miss on their own.

**Question style**: Default AskUserQuestion. Switch to natural language if: (1) user requests conversational, (2) 2+ free-text responses, (3) question about personal history/emotions.

## 2.1 Decision Framing & Underlying Need (MUST COMPLETE BEFORE 2.3)

**This section must be DEEPLY explored before generating any factors.** Factor scaffolding (2.3) MUST be tailored to the underlying need discovered here, not the surface request.

**Framing check**: Is user asking the right question? Common reframes:
- "Which X should I buy?" → "Do I need X at all?" / "Buy vs rent/lease?"
- "Should I take job A or B?" → "Should I change jobs?" / "What do I actually want?"
- "Where should I move?" → "Should I move?" / "What problem does moving solve?"

**Ask**: "Before we go deep: is '{user's framing}' the right question, or might there be a better way to frame this decision?"

**Goal**: WHY, not WHAT. Probe until you understand the ROOT problem, not the surface request.

**Probe sequence**:
1. "What's driving this decision? What problem are you trying to solve?"
2. "If this decision magically resolved perfectly, what would be different in your life?"
3. "What's driving that? Flexibility if alternative serves underlying need better?"

**Anti-anchoring check**: If user arrived with specific options (e.g., "MacBook vs Dell"), explicitly ask: "You mentioned {options}—but stepping back, what underlying need would either of these serve? Are there other ways to meet that need?"

**⚠️ Sunk cost probe (ASK EARLY)**: Before factor generation, check for prior investment:
- "Have you already invested significant time/money researching any specific option? (Test drives, applications, site visits, etc.)"
- If yes: Document which option. Throughout analysis, watch for bias toward this option. In gut check (3.4), explicitly note: "You mentioned investing heavily in {X}—let's verify your preference isn't anchoring bias."
- Purpose: Catching sunk cost EARLY prevents it from contaminating factor generation, thresholds, and research framing

**Only proceed to 2.2 when**: You can articulate the underlying need in a sentence that doesn't reference the surface options (e.g., "Need: reliable tool for software development that projects professionalism" not "Need: laptop").

## 2.2 Time Horizon & Uncertainty

- When decide? When need outcome?
- What might change in 1/5/10 years?
- How certain? (probabilities if appropriate)

**Probabilities**: 30-70% uncertainty → recommend reversible. Lower → commit to optimized.

## 2.3 Factor Scaffolding

**Prerequisite**: Underlying need (2.1) must be articulated before this section. Factors must serve the UNDERLYING NEED, not the surface request.

**Don't ask "what matters?"** - YOU propose factors first. Use domain knowledge to generate 8-12 concrete factors for this specific decision type.

**Tailor to underlying need**: If underlying need is "reliable tool for software development that projects professionalism," factors should include "professional appearance in client meetings" even though user asked about laptops.

**Proactive scaffolding** (generate these AFTER understanding underlying need):
```
"For {specific decision}, these factors typically matter:

**Usually Critical:**
- {Concrete factor 1}: {Why it matters for THIS decision}
- {Concrete factor 2}: {Specific impact}

**Often Important:**
- {Factor 3-5}: {Decision-specific reasoning}

**Commonly Overlooked:**
- {Factor 6-8}: {Why people miss this}

Which resonate? Which don't apply? What's missing?"
```

**Factor generation sources**: Your knowledge of this domain, common regrets in similar decisions, expert frameworks, long-term considerations users forget.

**After user responds**: Probe each selected factor for threshold. Then ask: "Anything else that would make you regret this decision?" Add 2-3 more rounds until nothing new.

## 2.4 Edge Cases (medium+ stakes)

**Goal**: Surface what could go wrong.

Questions: What could go wrong? What would make this fail? Most worried about? Worst case each path?

**Probe each**: How likely? How bad? How mitigate?

## 2.5 Hidden Factors (medium+ stakes)

**YOU surface these proactively** - don't wait for user to think of them:

| Category | Proactively Check |
|----------|-------------------|
| Financial | Ongoing costs, exit costs, opportunity cost, tax implications, insurance |
| Lock-in | Switching costs, contracts, ecosystem dependencies, resale value |
| Time | Maintenance burden, learning curve, time-to-value, depreciation |
| Risk | Regulatory changes, market shifts, technology obsolescence |
| Second-order | Impact on other goals, relationship effects, lifestyle constraints |

**Ask**: "I want to surface factors you might not have considered: {list 3-4 relevant from above}. Any of these matter?"

**Then**: "What would make you doubt this in 5 years?"

**Follow-up**: "How important is {factor} vs others? Minimum acceptable?"

## 2.6 Stakeholder Constraints

For each with veto: deal-breakers → non-negotiable. Strong preferences → important factors. Document conflicts.

## 2.7 Comprehensiveness Checkpoint (ACTIVE VERIFICATION)

**Don't passively wait for "nothing new"—actively verify coverage.**

**Checklist** (must confirm ALL before proceeding):
| Area | Verified? | How |
|------|-----------|-----|
| Decision framing | ☐ | Asked if right question |
| Underlying need | ☐ | Know WHY, not just WHAT |
| Time horizon | ☐ | When needed, what changes |
| Factors (8-12) | ☐ | Proactively generated + user additions |
| Factor thresholds | ☐ | Minimums for each important factor |
| Edge cases | ☐ | What could go wrong |
| Hidden factors | ☐ | Financial/lock-in/time/risk/second-order |
| Stakeholder constraints | ☐ | If applicable |

**Explicit verification ask**:
```
"Before we move to options, let me verify we've covered everything:
- Decision framing: {confirmed question}
- Core need: {underlying why}
- Key factors: {list top 5-7}
- Must-haves: {non-negotiables with thresholds}
- Risks considered: {edge cases}
- Hidden factors checked: {which categories}

**Is anything missing?** Any factor that, if we ignored it, you'd regret later?"
```

**Only proceed when user confirms** or explicitly says "that's comprehensive enough."

**User wants to skip**: "I understand urgency. But skipping discovery → wrong recommendation. Let me ask the 3 most critical questions—takes 2 minutes, prevents wasted analysis." Ask those, document assumptions, note reduced confidence.

---

# Phase 3: Structuring

## 3.1 Factor Ranking

Get explicit ranking:

```json
{"questions":[{"question":"If you could only optimize ONE factor, which?","header":"Top Priority","options":[{"label":"{factor 1}","description":"{brief}"},{"label":"{factor 2}","description":"{brief}"}],"multiSelect":false}]}
```

Then: "With {#1} secured, what's second?"

Continue until "they're all nice-to-haves."

**If stakeholders**: Get user's ranking, then stakeholder's. Surface discrepancies: "Your ranking differs on {factor}. Whose takes precedence, or find compromise?" If compromise impossible: "No option satisfies both. Which to optimize?" Default: user's ranking.

## 3.2 Threshold Setting WITH Market Context

For EACH important factor, provide context first:

```
"For {factor}, market reality:
- **Basic**: {min options offer}
- **Solid**: {good options}
- **Premium**: {best-in-class}

Your minimum acceptable? Not ideal—what you could live with."
```

**Threshold = elimination criterion**: Below → eliminated regardless of other strengths.

**⚠️ Qualitative factors**: Not all factors can be meaningfully quantified. For factors like "work-life balance," "company culture," "aesthetic appeal":
- Use **descriptive thresholds** instead: "Must feel welcoming when I visit" / "Must not require regular weekend work"
- Ask user to describe their minimum in their own words, not numbers
- In elimination, evaluate against the descriptive threshold, not a false numeric proxy

**Qualitative evaluation decision rule**:
- **Clear pass**: >80% of signals suggest option meets threshold → PASS
- **Clear fail**: >80% of signals suggest option fails threshold → FAIL
- **Ambiguous** (20-80%): Flag for user with specific evidence: "Option A has mixed signals on {factor}: {evidence for pass} vs {evidence for fail}. Your call?"
- Don't ask user for EVERY qualitative evaluation—only when genuinely ambiguous

**Research context if needed**:
```
Task(subagent_type:"vibe-workflow:web-researcher",prompt:"quick - Typical ranges for {factor} in {category}? Basic/mid/premium benchmarks.",description:"Market context")
```

## 3.3 Categorize Factors

- **Non-Negotiable**: Must meet threshold (top 2-3)
- **Important**: Affects ranking (next 2-4)
- **Bonus**: Breaks ties (rest)

Write to log.

## 3.4 Gut Check

Before elimination, capture intuition:

```json
{"questions":[{"question":"Before analysis, what does your gut say?","header":"Gut Check","options":[{"label":"Drawn to {A}","description":"Feels right"},{"label":"Drawn to {B}","description":"Feels right"},{"label":"Repelled by {X}","description":"Feels off"},{"label":"No strong feeling","description":"Neutral"}],"multiSelect":true}]}
```

**Use as data, not conclusion**: If analysis contradicts gut, surface: "Analysis → {A}, but you felt {B}. Worth exploring what intuition picked up."

**Weight intuition more**: If user has domain experience (prior decisions with outcome feedback).

**Sunk cost check integration**: If sunk cost was detected in 2.1 (prior investment) AND user is now drawn to that same option:
- Explicitly note: "In discovery you mentioned investing heavily in {X}, and your gut leans toward {X}. Let's verify this isn't anchoring bias—what specifically makes {X} feel right beyond your prior research investment?"
- Don't re-ask about investment (already captured in 2.1)

---

# Phase 4: Option Discovery

## 4.1 Check User's Existing Options (BEFORE Research)

**FIRST**, ask what user already has in mind:

```json
{"questions":[{"question":"Are there specific options you're already considering?","header":"Your Options","options":[{"label":"Yes, specific ones","description":"Particular options in mind"},{"label":"A few ideas","description":"Some possibilities"},{"label":"No, start fresh","description":"Research what's available"},{"label":"Mix - mine + discover","description":"Include mine and find others"}],"multiSelect":false}]}
```

**If has options** ("Yes"/"A few"/"Mix"): Ask which, record in log BEFORE research. Research MUST include them.

**If "No, start fresh"**: Proceed to 4.2.

**Why**: Users often have options but don't mention unprompted. Missing them → wasted research.

**Category assignment**: Group by fundamental approach (laptop→brand/tier; career→industry/role; investment→asset class). If unclear, ask. Skip if all same type.

## 4.2 Option Discovery

```
Task(subagent_type:"vibe-workflow:web-researcher",prompt:"medium - Find options for {decision}.

REQUIREMENTS:
- Must have: {non-negotiables}
- Important: {factors}
- Context: {situation}

FIND: (1) Direct solutions, (2) Alternative approaches, (3) Creative options

Return by category with descriptions.",description:"Discover options")
```

## 4.3 Present Options

```markdown
**Options worth considering:**

**Perfect Matches** (meet all non-negotiables):
- {Option}: {why}

**Borderline** (eliminated by strict thresholds—show if asked or no perfects):
- {Option}: Strong on {X}, eliminated because {Y}={value} vs threshold {T}

**Creative** (different approach):
- {Option}: {how solves root problem}

**Categories Eliminated**:
- {Category}: All fail {#1 priority}
```

## 4.4 Validate Option Set

Before research: "Right options to research? Add or remove any?"

**Option interdependence check**: Many decisions have options that aren't independent:
- "Can any of these be combined? (e.g., component from A + component from B)"
- "Does knowing Option A's terms affect Option B's negotiating leverage?"
- "Is there a 'wait and see' option that preserves flexibility?"

If interdependence exists: Note in log, consider hybrid options, adjust analysis to account for leverage/sequencing.

---

# Phase 5: Research

## 5.1 Deep Research

**CRITICAL**: Use Task (not Skill) to preserve todo state.

```
Task(subagent_type:"vibe-workflow:web-researcher",prompt:"{thoroughness} - Research options for {decision}.

OPTIONS: {list}

EVALUATE ON:
1. {Factor #1}: meets threshold {X}?
2. {Factor #2}: meets threshold {Y}?

CONTEXT: {situation}

FOR EACH: values with sources, strengths/weaknesses, hidden costs, best for / worst for",description:"Research options")
```

**Thoroughness by stakes**: Low→medium, Medium→thorough, High→very thorough

## 5.2 Post-Research Gap Check

Scan for factors that: are important (multiple sources), NOT discussed in discovery, could change recommendation.

**If found**:
```json
{"questions":[{"question":"Research revealed {factor} is important. How important to you?","header":"New Factor","options":[{"label":"Critical","description":"Could change decision"},{"label":"Important","description":"Should affect ranking"},{"label":"Minor","description":"Nice to know"},{"label":"Not relevant","description":"Doesn't apply"}],"multiSelect":false}]}
```

**If Critical**: Get threshold, follow-up research, repeat gap check.

**Loop terminates** (first met): No new factors | All minor/not relevant | User has enough | 3 rounds done

## 5.3 Research Insufficient

1. Acknowledge limitations
2. Reason from principles
3. Set confidence Medium
4. Be explicit about uncertainty

## 5.4 Research Completeness Matrix (REQUIRED before Elimination)

**Before elimination, verify data exists for every option × important factor combination.**

```markdown
## Factor Coverage Matrix
| Factor (Priority) | Threshold | Opt A | Opt B | Opt C |
|-------------------|-----------|-------|-------|-------|
| {Factor 1} (#1) | ≥{X} | ✓ {val} | ✓ {val} | ? |
| {Factor 2} (#2) | ≥{Y} | ✓ {val} | ? | ✓ {val} |
```

**If ANY cell is missing for Non-Negotiable or Important factors**:
1. Targeted follow-up research: `Task(subagent_type:"vibe-workflow:web-researcher", prompt:"quick - Find {Factor} value for {Option} specifically", description:"Fill matrix gap")`
2. If still unavailable after follow-up:
   ```json
   {"questions":[{"question":"No reliable data for {Option}'s {Factor}. How should I proceed?","header":"Data Gap","options":[{"label":"Assume meets threshold","description":"Optimistic - keep in consideration"},{"label":"Assume fails threshold","description":"Conservative - eliminate option"},{"label":"Skip this option entirely","description":"Can't evaluate without this data"}],"multiSelect":false}]}
   ```
3. Document user's choice in log with rationale
4. **CRITICAL**: Mark assumed values as `{value}*` in matrix with footnote: `*assumed, not verified`

**In elimination rounds**: When an option's PASS relies on assumed value, flag it: "Option B passes {Factor} threshold based on ASSUMPTION (unverified). This elimination decision rests on unverified data. [Proceed / Get real data first]"

**Write matrix to log before proceeding to elimination.**

---

# Phase 6: Sequential Elimination

**EBA methodology**: Eliminate by most important factor first, then second, etc.

## 6.1 Elimination Rounds

```markdown
**Round {N}: {Factor} (Priority #{N})**
Threshold: {min}

| Option | Value | Status | Notes |
|--------|-------|--------|-------|
| A | {v} | ✓ PASS | Exceeds |
| B | {v} | ✗ ELIMINATED | Below by {gap} |

**Eliminated**: B
**Reason**: {Factor}={X} below min {Y}
**Would return if**: threshold {Y}→{X}
**Remaining**: A
```

## 6.2 Narrate Each Elimination

Explain: "Eliminating {Option} because {factor}={value}, below your min of {threshold}. Leaves us with {list}."

## 6.3 Near-Miss Protection (PREVENTS EBA FLAW)

**Problem EBA creates**: Option marginally below threshold on Factor #1 gets eliminated even if vastly superior on Factors 2-10. This systematically excludes potentially best options.

**Near-miss rule**: If an option is within 10-15% of threshold on the eliminating factor:
1. Flag as "Near-Miss" instead of immediate elimination
2. Before proceeding: "Option {X} missed your {Factor} threshold by {small margin}. But it's strong on {other factors}. Worth keeping for holistic comparison, or strict threshold?"
3. If user keeps: Include in finalists for pairwise comparison, explicitly noting the threshold violation
4. Document: "Near-miss on {Factor}, kept for holistic comparison per user preference"

**When to apply**: Only for quantitative factors with clear margins. Qualitative factors don't have "near-miss" - they either meet descriptive threshold or don't.

## 6.4 Finalist Count Edge Cases

| Count | Action |
|-------|--------|
| 0 | Show which threshold eliminated most; ask which flexible; relax; re-run |
| 1 | Winner by elimination; abbreviated synthesis; still do 10-10-10 |
| 2-4 | Ideal; proceed to finalist analysis |
| 5-6 | Use Important factors to narrow until 2-4 |
| 7+ | Ask to tighten thresholds; if declined, proceed noting less detail |

## 6.4 Target: 2-4 Finalists

If more after non-negotiables, use important factors.

---

# Phase 7: Finalist Analysis

**Consideration set quality > evaluation sophistication.** Verify: different categories represented? Stopped search too early?

## 7.1 Deep Dive

For each finalist (same thoroughness as Phase 5 for stakes): strengths/weaknesses, reviews/complaints, hidden costs, best for / worst for.

## 7.2 Cross-Category Representation

If finalists same category: include best from each major category, even if lower-ranked. User may have unstated category preference.

## 7.3 Pairwise Comparisons

```markdown
**{A} vs {B}:**

A gives: {advantage} → {concrete impact}
A costs: {sacrifice}

B gives: {advantage}
B costs: {sacrifice}

**Which trade-off aligns with your priorities?**
```

## 7.4 Sensitivity Analysis

```markdown
**Current lean**: {A}

**Flips to {B} if:**
- {Condition 1}
- {Condition 2}

**Likelihood**: Condition 1: {Low/Med/High}...

**Stability**: {Stable (all Low) / Moderate (some Med) / Fragile (any High)}

If fragile: "Significant uncertainty. Consider: (1) wait, (2) choose reversible option, (3) accept risk if upside justifies."
```

---

# Phase 8: Synthesis

## 8.1 Refresh Context (MANDATORY - NEVER SKIP)

**Read FULL log** before ANY synthesis.

**Why**: Earlier findings degraded (context rot). Log contains ALL findings. Reading moves them to context END (highest attention). Never skip—synthesis accuracy depends on it.

If log exceeds context: prioritize (1) Characteristics, (2) Ranked Factors, (3) Elimination, (4) Finalist research.

## 8.2 Temporal Perspective (10-10-10)

Grounded in Construal Level Theory—distant futures processed abstractly, counters present bias.

```markdown
**Regret check:**

**10 min after {A}**: Relief? Excitement? Doubt?
**10 months in**: Challenges? Benefits?
**10 years**: Wish you'd been bolder? Value security?

**Which regret worse**: {risk of A} or {risk of not-A}?
```

**Affective forecasting**: Direction accurate, but intensity (~50%) and duration overestimated. "Catastrophic" outcomes feel more manageable than predicted.

**Using results**:
- Strong negative ANY timeframe → flag concern
- 10-year "wish bolder" → bias higher-risk/reward
- 10-year "wish safer" → bias conservative
- Conflicting timeframes (short pain, long gain) → explicitly note trade-off

## 8.3 Pre-Mortem Stress Test (REQUIRED for medium+ stakes)

**Before recommending, actively try to BREAK the recommendation.**

**Pre-mortem prompt** (imagine it's 1 year later and the decision failed):
```
"Let me stress-test my emerging recommendation ({Option}):

**If this choice fails, the most likely reasons are:**
1. {Concrete failure mode}
2. {Hidden assumption that could be wrong}
3. {External factor that could change}

**What would have to be true for {Option} to be WRONG?**
- {Condition 1}
- {Condition 2}

**Devil's advocate for #2 ({runner-up}):**
- {Strongest argument for #2 over #1}
- {What #1 advocates might be missing}
"
```

**If pre-mortem reveals serious vulnerability**: Surface to user before finalizing. "My analysis leans {A}, but the pre-mortem revealed {risk}. How do you weigh this?"

**⚠️ Resurrection check**: If pre-mortem reveals a vulnerability that an ELIMINATED option would have avoided:
1. Check the Eliminated Options Audit - which option avoided this failure mode?
2. Ask user: "Pre-mortem revealed {vulnerability}. {Eliminated Option X} would avoid this but was eliminated because {reason}. Worth reconsidering? [Resurrect X for comparison / Accept vulnerability / Adjust threshold]"
3. If resurrect: **Do FULL finalist analysis for resurrected option** (same depth as Phase 7.1) before comparison—otherwise comparison is unfair (A has deep research, X doesn't)

**⚠️ Resurrection limits** (prevent infinite loops):
- Maximum 1 resurrection per decision
- After resurrection + re-analysis, if new pre-mortem reveals ANOTHER vulnerability: document but don't offer second resurrection. Say: "Pre-mortem revealed {new issue}. Since we already resurrected one option, proceeding with current recommendation. The logged vulnerabilities can inform your post-decision monitoring."

**Purpose**: Catches overconfidence, surfaces assumptions, builds trust through transparency. Resurrection mechanism ensures pre-mortem can actually change the recommendation, not just surface concerns too late.

## 8.4 Subjective Evaluation Guidance

For unresearchable factors:
```markdown
**For {factor}:**
- **Action**: {what to do}
- **Ask**: {questions}
- **Watch for**: {signals}
- **Red flags**: {warnings}
```

## 8.5 Final Synthesis

**Structure optimized for TRUST**: User should see everything considered, why options were eliminated, and what could change the recommendation.

```markdown
## Decision Analysis: {Topic}

### What We Analyzed (Comprehensiveness Summary)
- **Decision framing**: {confirmed question}
- **Factors evaluated**: {count} ({list top 5-7})
- **Options considered**: {count total} ({count} eliminated, {count} finalists)
- **Research depth**: {thoroughness level}, {source count} sources
- **Data coverage**: {X}/{Y} factor-option cells verified (see matrix)

### Hidden Factors Discovered
| Factor | Category | Impact on Decision |
|--------|----------|-------------------|
| {e.g., Ecosystem lock-in} | Lock-in | {e.g., Eliminated Option A} |
| {e.g., Ongoing maintenance cost} | Financial | {e.g., Added to Important factors} |

*(If no hidden factors surfaced: "Hidden factors probe (all 5 categories) found no additional concerns beyond stated factors.")*

### Recommendation
**#1: {Option}**
{2-3 sentences tied to #1 priority}

### Eliminated Options Audit
| Option | Eliminated By | Value vs Threshold | Would Return If |
|--------|---------------|-------------------|-----------------|
| {B} | {Factor #1} | {X} vs min {Y} | Threshold → {Z} |
| {C} | {Factor #2} | {X} vs min {Y} | {condition} |

### Top 3 Comparison
| Factor | #1: {A} | #2: {B} | #3: {C} |
|--------|---------|---------|---------|
| Category | {cat} | {cat} | {cat} |
| {Priority 1} | {v} | {v} | {v} |

### Why #1 Wins
- Best on {X}
- Meets {Y}
- {Stakeholder} alignment

### Pre-Mortem Results
**If #1 fails, likely because**: {top failure mode}
**#1 is WRONG if**: {condition that would invalidate}
**Devil's advocate for #2**: {strongest counter-argument}

### Trade-Offs Accepted
- Choosing #1 means accepting {weakness}
- Trading {#2 offers} for {#1 offers}

### Sensitivity & Stability
- **Changes if**: {conditions}
- **Stability**: {Stable/Moderate/Fragile}

### Gut Check Reconciliation
- **Initial intuition**: {Drawn to X / Repelled by Y / Neutral}
- **Analysis result**: {Aligned with gut / Contradicted gut}
- **Resolution**: {If aligned: "Analysis confirms intuition." / If contradicted: "Analysis favors {A} over gut preference {B} because {specific factor/data}. Your gut may be picking up on {possible unlisted factor}—worth examining before finalizing."}

### Confidence Assessment
**{High/Medium/Low}**

| Criterion | Met? |
|-----------|------|
| 3+ sources agree on key facts | {Y/N} |
| User priorities clear and stable | {Y/N} |
| Pre-mortem found no critical vulnerabilities | {Y/N} |
| No major data gaps | {Y/N} |

**High** = All 4 met. **Medium** = 2-3 met. **Low** = 0-1 met.

### What We Didn't Fully Explore
- {Area}: {why - time/data unavailable/user chose to skip}
- {Impact on confidence}: {how this affects certainty}

### 10-10-10
- **10 min**: {prediction}
- **10 months**: {prediction}
- **10 years**: {prediction}

### Final Check
**Anything missing?** If you think of a factor we didn't consider, or an option we should have evaluated, say so now—better to revisit than regret.
```

## 8.6 Tie-Breaking

If top 2 close (<10% numeric diff on #1 priority, or similar on subjective factors):

```json
{"questions":[{"question":"{A} and {B} very close. What matters more: {Factor A wins} or {Factor B wins}?","header":"Tie-Breaker","options":[{"label":"{Factor X}","description":"Favors {A}"},{"label":"{Factor Y}","description":"Favors {B}"},{"label":"Gut says A","description":"Intuition reflects unarticulated priorities"},{"label":"Gut says B","description":"Intuition reflects unarticulated priorities"}],"multiSelect":false}]}
```

---

# Phase 9: Finalize

## 9.1 Update Log

```markdown
## Status
COMPLETE

## Final Recommendation
{#1 with rationale}

## Decision Completed
{timestamp}
```

## 9.2 Mark All Todos Complete

## 9.3 Output

Present: #1 recommendation, Top 3 comparison, why #1 wins (+ category), trade-offs, confidence, 10-10-10.

---

# Decision Type Handling

| Type | Examples | Approach |
|------|----------|----------|
| **External** | Product, investment | Full research |
| **Self-knowledge** | Career direction, values | Skip research—answer internal |
| **Hybrid** | Career change, relocation | Research facts; note what needs judgment |

**Self-knowledge**: Skip Phases 5-6. Use discovery for values, framework for structured reflection.

---

# Edge Cases

| Scenario | Action |
|----------|--------|
| No options | Run discovery research |
| All eliminated | Show which threshold eliminated most; ask which flexible |
| Single survivor | Winner by elimination; abbreviated synthesis |
| 5+ survivors | Continue with Important factors until 2-4 |
| Research insufficient | Reasoning mode, Medium confidence, explicit uncertainty |
| User skips | 2-3 critical questions, document assumptions |
| Stakeholders disagree | Surface conflict, ask whose preference precedent |
| Veto deadlock | Ask: relax constraint or new options? |
| User corrects | Update log; constraints changed → re-research; priorities → re-rank |
| Interrupted | Resume from checkpoint |
| Empty $ARGUMENTS | Ask what decision |
| "Just decide for me" | Still ask Core 3 (need, timeline, constraints) |
| Self-knowledge | Skip research; discovery for values |
| **User not ready to decide** | Valid outcome. Document: "Decision deferred pending {what}. When ready, resume from log: {path}" |
| **User rejects reframe but is destabilized** | "You've said you want to stick with {original question}. Proceeding—but noting this uncertainty may affect confidence." |
| **Analysis reveals "wait" is best** | "Wait and see" can be the recommendation. Document triggers for when to re-engage |

---

# Key Principles

| Principle | Rule |
|-----------|------|
| Quality > speed | Better slow and right |
| Exhaustive discovery | Probe until nothing new |
| Market context | User can't set thresholds without context |
| Find options | If not provided, discover them |
| Sequential elimination | Most important factor first, narrate each |
| Pairwise comparisons | "A vs B" clearer than scoring |
| Sensitivity analysis | Know what changes mind |
| 10-10-10 | Catches temporal blind spots |
| External memory | Write everything; refresh before synthesis |

---

# Generally Avoid

| Avoid | Unless |
|-------|--------|
| Accepting first answer | 3+ pre-processed signs |
| Thresholds without context | User claims prior research OR shows domain knowledge |
| Skipping elimination narration | Only 2 options |
| Synthesizing without refresh | Never skip |
| Claiming High confidence | 3+ sources agree AND priorities clear |

**The test**: Would skilled human coach do this? If yes, you can too.
