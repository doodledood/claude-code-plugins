---
name: research-web
description: 'Deep web research with parallel investigators, multi-wave exploration, and structured synthesis. Spawns multiple web-researcher agents to explore different facets of a topic simultaneously, launches additional waves when gaps are identified, then synthesizes findings. Use when asked to research, investigate, compare options, find best practices, or gather comprehensive information from the web.\n\nThoroughness: quick for factual lookups | medium for focused topics | thorough for comparisons/evaluations (waves continue while critical gaps remain) | very-thorough for comprehensive research (waves continue until satisficed). Auto-selects if not specified.'
context: fork
---

**Research request**: $ARGUMENTS

# Thoroughness Level

**FIRST**: Determine thoroughness before researching. Parse from natural language or auto-select.

**Auto-selection logic**:
- Single fact/definition/date → quick
- Focused question about one topic → medium
- Comparison, evaluation, or "best" questions → thorough
- "comprehensive"/"all options"/"complete analysis"/"deep dive" → very-thorough

**Explicit user preference**: Honor user-specified level regardless of other triggers.

**Trigger conflicts (auto-selection only)**: Use highest level indicated.

| Level | Agents/Wave | Wave Policy | Behavior | Triggers |
|-------|-------------|-------------|----------|----------|
| **quick** | 1 | Single wave | Single web-researcher, no orchestration file, direct answer | "what is", "when did", factual lookups, definitions |
| **medium** | 1-2 | Single wave | Orchestration file, focused research on 1-2 angles | specific how-to, single technology, focused question |
| **thorough** | 2-4 | Continue while critical gaps remain | Full logging, parallel agents, cross-reference, follow-up waves | "compare", "best options", "evaluate", "pros and cons" |
| **very-thorough** | 4-6 | Continue until comprehensive OR diminishing returns | Multi-wave until all significant gaps addressed | "comprehensive", "complete analysis", "all alternatives", "deep dive" |

**Multi-wave**: For thorough/very-thorough, waves continue until satisficing criteria are met. No hard maximum — waves continue as long as productive and gaps remain.

**Agent count scaling**: Match agent count to genuine research facets, not perceived thoroughness. Each agent should have a distinct domain justifying dedicated research. Over-spawning wastes resources; under-spawning misses facets.

| Task Complexity | Agents | Rationale |
|----------------|--------|-----------|
| Simple fact-check | 1 | Single angle sufficient |
| Direct comparison (2-3 options) | 2-3 | One per option or dimension |
| Multi-facet evaluation | 3-5 | One per orthogonal facet |
| Comprehensive landscape | 5-7 | Cover all major dimensions |

**Ambiguous queries**: If thoroughness cannot be determined AND query is complex, ask:

```
I can research this at different depths:
- **medium**: Focused research on core aspects (~3-5 min)
- **thorough**: Multi-angle investigation with cross-referencing (~8-12 min)
- **very-thorough**: Comprehensive analysis covering all facets (~15-20 min)

Which level would you prefer?
```

State: `**Thoroughness**: [level] — [reason]` then proceed.

---

# Orchestration

Orchestrate parallel web researchers through iterative waves, then synthesize findings.

**Loop**: Determine thoroughness → Decompose → Launch Wave 1 → Collect → Cross-reference → Evaluate gaps → [If gaps + productive: next wave] → Synthesize → Output

**Orchestration file**: `/tmp/research-orchestration-{topic-slug}-{YYYYMMDD-HHMMSS}.md` — external memory for tracking multi-wave progress.

- **Topic-slug**: 2-4 key terms (nouns/adjectives), lowercase, hyphens. Exclude articles, prepositions, generic words.
- **Timestamp**: `YYYYMMDD-HHMMSS` via `date +%Y%m%d-%H%M%S`.

---

# Satisficing Criteria

## Wave Continuation

| Level | Continue When | Stop When (Satisficed) |
|-------|---------------|------------------------|
| quick | N/A | Always single wave |
| medium | N/A | Always single wave |
| thorough | Critical gaps remain AND previous wave productive AND ≤50% source overlap | No critical gaps OR diminishing returns OR >50% source overlap |
| very-thorough | Significant gaps remain AND previous wave productive AND ≤50% source overlap | No significant gaps OR diminishing returns OR >50% source overlap |

**Source overlap**: % of sources in current wave also cited in prior waves. >50% = cycling through same sources.

## Gap Classification

| Gap Type | Definition | Triggers New Wave? |
|----------|------------|-------------------|
| **Critical** | Core question unanswered, major conflict unresolved, key comparison missing | Yes (thorough, very-thorough) |
| **Significant** | Important facet unexplored, partial answer needs depth, newly discovered area | Yes (very-thorough only) |
| **Minor** | Nice-to-have detail, edge case, tangential | No — note in limitations |

## Satisficing Evaluation

**Definitions**:
- **Finding**: Distinct information answering part of the question, with source citation.
- **Substantive finding**: New information not already established in prior waves.
- **High-authority source**: Official docs, peer-reviewed research, established publications, recognized domain experts.
- **Independent sources**: Different underlying information origins. Two articles citing the same study = one source.
- **High confidence**: ≥3 independent sources OR ≥2 high-authority sources.
- **Medium confidence**: 2 independent sources OR 1 high-authority source.
- **Low confidence**: Single non-authoritative source, no corroboration.

**Satisficed when ANY true**:
- All critical gaps addressed (thorough) OR all significant gaps addressed (very-thorough)
- Diminishing returns: <2 new substantive findings AND no confidence increased AND no new areas
- User requested stopping
- All facets at medium+ confidence

**Continue when ALL true**:
- Gaps at triggering threshold (thorough: critical; very-thorough: significant)
- Previous wave productive (≥2 findings OR confidence improved OR new areas)
- ≤50% source overlap with prior waves

---

# Phase 1: Initial Setup (skip for quick)

## 1.1 Get timestamp & create todos

Run `date +%Y%m%d-%H%M%S` and `date '+%Y-%m-%d %H:%M:%S'`.

Todos = research areas + write-to-log operations. List grows during decomposition.

```
- [ ] Create orchestration file
- [ ] Topic decomposition→log
- [ ] (expand: research facets as decomposition reveals)
- [ ] Launch Wave 1 agents
- [ ] Collect Wave 1 findings→log
- [ ] Cross-reference→log
- [ ] Evaluate gaps→log
- [ ] (expand: Wave 2+ if continuing)
- [ ] Refresh: read full orchestration file
- [ ] Synthesize→final output
```

**Critical todos** (never skip): `→log` after each phase/agent; `Refresh:` before synthesis.

## 1.2 Create orchestration file

```markdown
# Web Research Orchestration: {topic}
Timestamp: {YYYYMMDD-HHMMSS}
Started: {YYYY-MM-DD HH:MM:SS}
Thoroughness: {level}
Wave Policy: {single wave | continue while critical gaps | continue until comprehensive}

## Research Question
{Clear statement}

## Topic Decomposition
(populated in Phase 2)

## Wave Tracking
| Wave | Agents | Focus | Status | New Findings | Decision |
|------|--------|-------|--------|--------------|----------|
| 1 | {count} | Initial investigation | Pending | - | - |

## Research Assignments
(populated in Phase 2)

## Collected Findings
(populated as agents return)

## Cross-Reference Analysis
(populated after each wave)

## Gap Evaluation
(populated after each wave)

## Synthesis Notes
(populated in final phase)
```

# Phase 2: Topic Decomposition & Agent Assignment

## 2.1 Decompose into ORTHOGONAL facets

Analyze the query to identify **non-overlapping** research angles. Each agent gets a distinct domain with clear boundaries.

1. **Core question**: What is fundamentally being asked?
2. **Facets**: What distinct aspects need investigation? (technical, comparison, practical, current state, limitations)
3. **Orthogonality check**: Each facet covers a distinct domain. No two facets would naturally run the same queries. Boundaries are explicitly statable.

**Bad** (overlapping): Agent 1 = "Research Firebase", Agent 2 = "Research real-time databases"
**Good** (orthogonal): Agent 1 = "Firebase — features, pricing, limits", Agent 2 = "Non-Firebase alternatives: Supabase, Convex, PlanetScale"

**Orthogonality strategies**: by entity, by dimension, by time horizon, by perspective.

## 2.2 Plan agent assignments with explicit boundaries

| Facet | Research Focus | Explicitly EXCLUDE |
|-------|----------------|-------------------|
| {facet 1} | "{scope}" | "{what others cover}" |
| {facet 2} | "{scope}" | "{what others cover}" |

**If more facets than agents allow**: prioritize by (1) directly answers core question, (2) enables comparison, (3) addresses user-specified concerns. Combine related facets. Schedule remaining for Wave 2.

## 2.3 Update orchestration file with decomposition and assignments

# Phase 3: Launch Parallel Researchers

## 3.1 Launch web-researcher agents

Launch `vibe-extras:web-researcher` agents in parallel (single message with multiple invocations).

**Wave 1 prompt template** — uses neutral framing to avoid biasing agent findings:
```
Investigate the relationship between {topic} and {facet area}. Include evidence both supporting and contradicting common assumptions about {topic}.

YOUR ASSIGNED SCOPE:
- Focus areas: {specific aspect 1}, {specific aspect 2}, {specific aspect 3}
- This is YOUR domain — go deep on these topics

DO NOT RESEARCH (other agents cover these):
- {facet assigned to Agent 2}
- {facet assigned to Agent 3}

Current date context: {YYYY-MM-DD} — prioritize recent sources.

---
Research context:
- Wave: 1 (initial investigation)
- Mode: Broad exploration within your assigned scope
- Report gaps or conflicts for potential follow-up waves
```

**Wave 2+ prompt template** — targeted gap-filling with established context:
```
{Specific gap or conflict to resolve}

Context from previous waves:
- Previous findings: {summary of relevant findings}
- Gap being addressed: {specific gap}
- Established facts: {what Wave 1 found}

YOUR ASSIGNED SCOPE:
- Focus narrowly on: {targeted aspect 1}, {targeted aspect 2}
- This gap was identified because: {why previous research was insufficient}

DO NOT RESEARCH:
- Topics well-covered in Wave 1
- {areas other Wave 2 agents handle}

Current date context: {YYYY-MM-DD} — prioritize recent sources.

---
Research context:
- Wave: {N} (gap-filling)
- Mode: Targeted investigation — focus on the gap above
- Build on previous findings, don't repeat broad exploration
- Flag if gap cannot be resolved
```

**Sycophancy guard**: Agent prompts must avoid implying expected findings. Use "investigate the relationship between X and Y" not "research how X improves Y." Include "evidence both supporting and contradicting" to elicit balanced research.

**Batching**: thorough → all 2-4 agents in one batch. very-thorough → batches of 3-4 (5 agents: 3+2; 6 agents: 3+3). Wave 2+ → 1-3 focused agents.

## 3.2 Update orchestration file after each agent completes

Record agent status, key findings, confidence levels, source citations. Preserve all source URLs.

## 3.3 Handle agent failures

If agent times out or returns incomplete:
- **Retry** if: covers critical gap, explicitly required for comparison, or user-requested
- **Mark as gap** if: significant/minor priority, partially covered by others, or synthesis viable without
- Never block synthesis for single failed agent
- If ALL agents fail: Wave 1 → retry simpler decomposition; Wave 2+ → proceed with prior findings

# Phase 4: Cross-Reference, Evaluate & Iterate

## 4.1 Analyze findings across agents

Identify:
- **Agreements**: Multiple agents reach similar conclusions
- **Conflicts**: Findings contradict (includes "Contested" findings from agents)
- **Inconclusive**: Agents couldn't determine answers
- **Gaps**: Not covered by any agent
- **Surprises**: Unexpected findings warranting attention

**Disagreement classification** — classify conflicts before resolution:
- *Factual conflicts* (equal-authority sources): investigate deeper, favor higher authority, split if unresolvable
- *Open-question conflicts* (ongoing investigation): preserve both positions — never force false consensus
- *Authority asymmetry*: weight toward higher authority unless specific reasons to doubt

## 4.2 Update orchestration file with cross-reference analysis

Record agreements, conflicts (with classification), gaps, and key insights.

## 4.3 Key Assumptions Check (for thorough/very-thorough)

After cross-referencing, surface hidden assumptions:
1. What must be true for the emerging conclusions to hold?
2. Which assumptions are load-bearing (failure collapses most conclusions)?
3. What information would test weakened assumptions?

Common hidden assumptions: first authoritative source is reliable, topic boundaries correctly drawn, absence of contrary evidence means consensus, search results represent full landscape.

## 4.4 Linchpin analysis (for thorough/very-thorough)

Identify 3-5 claims whose failure would collapse the most conclusions. Focus any adversarial or follow-up effort on these linchpin claims first — they have the highest verification ROI.

## 4.5 Evaluate gaps and decide next wave (skip for quick/medium)

Classify each gap (critical/significant/minor). Assess wave productivity. Apply satisficing criteria.

```markdown
## Gap Evaluation (Wave {N})

### Critical Gaps
- [ ] {Gap}: {Why critical}

### Significant Gaps
- [ ] {Gap}: {Why significant}

### Minor Gaps (note, don't pursue)
- {Gap}: {Why minor}

### Wave Productivity
- Substantive findings: {count}
- Confidence improvements: {which areas}
- New areas: {list or "none"}
- Diminishing returns: {yes/no}

### Decision
**{CONTINUE to Wave N+1 | SATISFICED}** — {reason}
```

## 4.6 Launch next wave (if continuing)

1. Update Wave Tracking table
2. Design targeted prompts for specific gaps (narrower than Wave 1)
3. Launch 1-3 focused `vibe-extras:web-researcher` agents
4. Collect findings → return to 4.1

# Phase 5: Synthesize & Output

## 5.1 Refresh context (MANDATORY)

Read the FULL orchestration file. Verify access to: all agent findings, cross-references, gap evaluations, wave tracking, all citations.

```
- [x] Refresh: read full orchestration file  ← Must complete before synthesis
- [ ] Synthesize→final output
```

## 5.2 Outside view check (for thorough/very-thorough)

Before finalizing, apply reference class reasoning: "How often does research of this type produce reliable conclusions?" Consider whether the research domain is well-covered by high-quality web sources, or if it's a niche area where available evidence may be systematically incomplete.

## 5.3 Generate output

Synthesize ALL agent findings. Use structural confidence — source agreement and evidence quality tiers, not verbal self-reports. Both overconfidence and underconfidence degrade quality.

```markdown
## Research Findings: {Topic}

**Thoroughness**: {level} | **Waves**: {count} | **Researchers**: {total} | **Sources**: {aggregate}
**Overall Confidence**: High/Medium/Low
**Satisficing**: {why research concluded}

### Executive Summary
{4-8 sentences. Key takeaway for the user.}

### Detailed Findings

#### {Finding Area 1}
{Synthesized insights with inline citations from multiple agents}
{State warrant: reasoning connecting evidence to conclusion}

#### {Finding Area 2}
{...}

### Comparison/Evaluation (if applicable)
| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| {opt 1} | {evidence} | {evidence} | {synthesis} |

### Recommendations
{Evidence-based suggestions. State conditions under which they would not hold.}

### Confidence Notes
- **High confidence**: {strong multi-source agreement}
- **Medium confidence**: {some support}
- **Contested**: {high-authority sources contradicted — both positions presented}
- **Inconclusive**: {couldn't determine despite searching}
- **Low confidence**: {single source or weak agreement}

### Key Assumptions
{Load-bearing assumptions that must hold for conclusions to be valid}

### Research Progression (multi-wave)
| Wave | Focus | Agents | Key Contribution |
|------|-------|--------|------------------|
| 1 | Initial investigation | {N} | {established} |
| 2 | {Gap focus} | {N} | {resolved} |

### Gaps & Limitations
- {Unanswered questions}
- {Areas needing more research}
- {Source biases}
- {Minor gaps not pursued}
- {Protocol deviations from initial plan}

### Source Summary
| Source | Authority | Confidence | Date | Used For | Wave |
|--------|-----------|------------|------|----------|------|
| {url} | High/Med | {GRADE-adjusted} | {date} | {finding} | 1 |

---
Orchestration file: {path}
Research completed: {timestamp}
```

## Quick Mode Flow

For quick (single-fact) queries:
1. State: `**Thoroughness**: quick — [reason]`
2. Launch single `vibe-extras:web-researcher` agent with the query
3. Return findings directly (no synthesis overhead)

# Principles

| Principle | Rule |
|-----------|------|
| Thoroughness first | Determine level before any research |
| Facet-driven scaling | Match agent count to genuine orthogonal facets, not thoroughness level alone |
| Write after each phase | Update orchestration file after EVERY phase/agent |
| Parallel execution | Launch agents simultaneously when possible |
| Neutral framing | Agent prompts avoid implying expected findings |
| Cross-reference | Compare findings across agents; classify disagreements before resolving |
| Gap evaluation | Classify gaps (critical/significant/minor) after each wave |
| Key Assumptions Check | Surface hidden assumptions after cross-referencing |
| Linchpin focus | Target verification at claims whose failure collapses most conclusions |
| Outside view (thorough+) | Apply reference class reasoning before finalizing |
| Wave iteration | Continue until satisficed OR diminishing returns |
| **Context refresh** | **Read full orchestration file BEFORE synthesis — non-negotiable** |
| Source preservation | Maintain citations through synthesis |
| Structural confidence | Assess via source agreement and evidence tiers, not verbal reports |
| Gap honesty | State what couldn't be answered despite effort |

## Never Do

- Launch agents without determining thoroughness
- Skip write-to-log todos or orchestration file updates
- Synthesize without refreshing from orchestration file
- Present findings without source citations
- Ignore conflicts between agents (especially "Contested" findings)
- Frame agent prompts to imply expected findings
- Skip gap evaluation for thorough/very-thorough
- Continue waves when diminishing returns detected
- Stop when critical/significant gaps remain and waves are still productive
- Over-spawn agents beyond genuine facet count
