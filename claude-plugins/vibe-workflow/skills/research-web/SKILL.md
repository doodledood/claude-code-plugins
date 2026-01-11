---
name: research-web
description: 'Deep web research with parallel investigators and structured synthesis. Spawns multiple web-researcher agents to explore different facets of a topic simultaneously, then synthesizes findings. Use when asked to research, investigate, compare options, find best practices, or gather comprehensive information from the web.\n\nThoroughness: quick for factual lookups | medium for focused topics | thorough for comparisons/evaluations | very-thorough for comprehensive research. Auto-selects if not specified.'
context: fork
---

**Research request**: $ARGUMENTS

# Thoroughness Level

**FIRST**: Determine thoroughness before researching. Parse from natural language (e.g., "quick lookup", "thorough research", "comprehensive analysis") or auto-select based on query characteristics.

**Auto-selection logic**:
- Single fact/definition/date → quick
- Focused question about one topic → medium
- Comparison, evaluation, or "best" questions → thorough
- "comprehensive"/"all options"/"complete analysis"/"deep dive" → very-thorough

**Trigger conflicts**: When query contains triggers from multiple levels, use the highest level indicated (very-thorough > thorough > medium > quick).

| Level | Agents | Behavior | Triggers |
|-------|--------|----------|----------|
| **quick** | 1 | Single web-researcher, no orchestration file, direct answer | "what is", "when did", factual lookups, definitions |
| **medium** | 1-2 | Orchestration file, focused research on 1-2 angles | specific how-to, single technology, focused question |
| **thorough** | 2-4 | Full memento, parallel agents for different facets, cross-reference | "compare", "best options", "evaluate", "pros and cons" |
| **very-thorough** | 4-6 | Comprehensive parallel research, all angles explored, deep synthesis | "comprehensive", "complete analysis", "all alternatives", "deep dive" |

**Ambiguous queries**: If thoroughness cannot be determined AND the query is complex (involves comparison, evaluation, or multiple facets), ask the user:

```
I can research this at different depths:
- **medium**: Focused research on core aspects (~3-5 min)
- **thorough**: Multi-angle investigation with cross-referencing (~8-12 min)
- **very-thorough**: Comprehensive analysis covering all facets (~15-20 min)

Which level would you prefer? (Or I can auto-select based on your query)
```

State: `**Thoroughness**: [level] — [reason]` then proceed.

---

# Deep Web Research Skill

Orchestrate parallel web researchers to comprehensively investigate a topic, then synthesize findings into actionable intelligence.

**Loop**: Determine thoroughness → Decompose topic → Launch parallel researchers → Collect findings → Synthesize → Output

**Orchestration file**: `/tmp/research-orchestration-{topic-slug}-{YYYYMMDD-HHMMSS}.md` - external memory for tracking parallel research progress and synthesis.

**Topic-slug format**: Extract 2-4 key terms from query, lowercase, replace spaces with hyphens. Example: "best real-time database options 2025" → `real-time-database-options`

**Timestamp format**: `YYYYMMDD-HHMMSS`. Obtain via `date +%Y%m%d-%H%M%S`.

## Phase 1: Initial Setup (skip for quick)

### 1.1 Get timestamp & create todo list

Run `date '+%Y-%m-%d %H%M%S'` to get current date and timestamp.

Todos = **research areas to investigate**, not fixed steps. Each todo represents a distinct angle or facet of the research. List expands as decomposition reveals new areas.

**Starter todos** (seeds - list grows during decomposition):

```
- [ ] Topic decomposition & research planning
- [ ] (research areas added during decomposition)
- [ ] Collect and cross-reference findings
- [ ] Synthesize final output
```

### 1.2 Create orchestration file (skip for quick)

Path: `/tmp/research-orchestration-{topic-slug}-{YYYYMMDD-HHMMSS}.md`

```markdown
# Web Research Orchestration: {topic}
Timestamp: {YYYYMMDD-HHMMSS}
Started: {YYYY-MM-DD HH:MM:SS}
Thoroughness: {level}

## Research Question
{Clear statement of what needs to be researched}

## Topic Decomposition
- Core question: {main thing to answer}
- Facets to investigate: (populated in Phase 2)
- Expected researcher count: {based on thoroughness level}

## Research Assignments
(populated in Phase 2)

## Agent Status
(updated as agents complete)

## Collected Findings
(populated as agents return)

## Cross-Reference Analysis
(populated in Phase 3)

## Synthesis Notes
(populated in Phase 3)
```

## Phase 2: Topic Decomposition & Agent Assignment

### 2.1 Decompose the research topic

Before launching agents, analyze the query to identify distinct research angles:

1. **Core question**: What is the fundamental thing being asked?
2. **Facets**: What distinct aspects need investigation?
   - Technical aspects (how it works, implementation details)
   - Comparison aspects (alternatives, competitors, trade-offs)
   - Practical aspects (real-world usage, adoption, case studies)
   - Current state (recent developments, 2025 updates)
   - Limitations/concerns (drawbacks, issues, criticisms)

3. **Agent assignments**: Map facets to web-researcher prompts

### 2.2 Plan agent assignments

| Facet | Research Prompt | Priority |
|-------|-----------------|----------|
| {facet 1} | "{specific research question}" | High |
| {facet 2} | "{specific research question}" | High |
| ... | ... | ... |

**Agent count by level**:
- medium: 1-2 agents (core + one related angle)
- thorough: 2-4 agents (core + alternatives + practical + concerns)
- very-thorough: 4-6 agents (comprehensive coverage of all facets)

### 2.3 Expand todos for each research area

Add a todo for each planned agent assignment:

```
- [x] Topic decomposition & research planning
- [ ] Research: {facet 1 description}
- [ ] Research: {facet 2 description}
- [ ] Research: {facet 3 description}
- [ ] ...
- [ ] Collect and cross-reference findings
- [ ] Synthesize final output
```

### 2.4 Update orchestration file

After decomposition, update the file:

```markdown
## Topic Decomposition
- Core question: {main question}
- Facets identified:
  1. {facet 1}: {why this angle matters}
  2. {facet 2}: {why this angle matters}
  ...

## Research Assignments
| Agent | Facet | Prompt | Status |
|-------|-------|--------|--------|
| 1 | {facet} | "{prompt}" | Pending |
| 2 | {facet} | "{prompt}" | Pending |
...
```

## Phase 3: Launch Parallel Researchers

### 3.1 Launch web-researcher agents

Use Task tool with `subagent_type: "vibe-workflow:web-researcher"` for each research angle. **Launch agents in parallel** (single message with multiple Task tool calls) to maximize efficiency.

**Prompt template for each agent**:
```
{Specific research question for this facet}

Focus areas:
- {specific aspect 1}
- {specific aspect 2}
- {specific aspect 3}

Current date context: {YYYY-MM-DD} - prioritize recent sources.
```

**Batching rules**:
- thorough: Launch all 2-4 agents in a single parallel batch
- very-thorough: Launch in batches of 3-4 agents (avoid overwhelming context)

### 3.2 Update orchestration file after each agent completes

After EACH agent returns, immediately update:

```markdown
## Agent Status
| Agent | Facet | Status | Key Finding |
|-------|-------|--------|-------------|
| 1 | {facet} | Complete | {1-sentence summary} |
| 2 | {facet} | Complete | {1-sentence summary} |
...

## Collected Findings

### Agent 1: {facet}
**Confidence**: {High/Medium/Low}
**Sources**: {count}

{Paste key findings from agent - preserve source citations}

### Agent 2: {facet}
...
```

### 3.3 Handle agent failures

If an agent times out or returns incomplete results:
1. Note the gap in orchestration file
2. Decide: retry with narrower prompt, or mark as gap in final output
3. Never block synthesis for a single failed agent

## Phase 4: Collect & Cross-Reference

### 4.1 Mark collection todo in_progress

### 4.2 Analyze findings across agents

Look for:
- **Agreements**: Where do multiple agents reach similar conclusions?
- **Conflicts**: Where do findings contradict?
- **Gaps**: What wasn't covered by any agent?
- **Surprises**: Unexpected findings that warrant highlighting

### 4.3 Update orchestration file

```markdown
## Cross-Reference Analysis

### Agreements (High Confidence)
- {Finding}: Supported by agents {1, 3, 4}
- {Finding}: Confirmed across {count} sources

### Conflicts (Requires Judgment)
- {Topic}: Agent 1 says X, Agent 3 says Y
  - Resolution: {which to trust and why, or present both}

### Gaps Identified
- {What wasn't answered}
- {Areas needing more research}

### Key Insights
- {Synthesis observation 1}
- {Synthesis observation 2}
```

### 4.4 Mark collection todo complete

## Phase 5: Synthesize & Output

### 5.1 Refresh context

**CRITICAL**: Read the full orchestration file to restore all findings, cross-references, and synthesis notes into context before generating output.

### 5.2 Mark synthesis todo in_progress

### 5.3 Generate comprehensive output

Your response must synthesize ALL agent findings into a cohesive answer. Include:

```markdown
## Research Findings: {Topic}

**Thoroughness**: {level} | **Researchers**: {count} | **Total Sources**: {aggregate}
**Overall Confidence**: High/Medium/Low (based on agreement and source quality)

### Executive Summary
{4-8 sentences synthesizing the key takeaway. What does the user need to know?}

### Detailed Findings

#### {Major Finding Area 1}
{Synthesized insights with inline source citations from multiple agents}

#### {Major Finding Area 2}
{...}

### Comparison/Evaluation (if applicable)
| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| {opt 1} | {from agents} | {from agents} | {synthesis} |
| {opt 2} | {from agents} | {from agents} | {synthesis} |

### Recommendations
{Based on synthesized evidence - what should the user consider/do?}

### Confidence Notes
- **High confidence**: {findings with strong multi-source agreement}
- **Medium confidence**: {findings with some support}
- **Contested/Unclear**: {where sources disagreed}

### Gaps & Limitations
- {What couldn't be definitively answered}
- {Areas where more research would help}
- {Potential biases in available sources}

### Source Summary
| Source | Authority | Used For | Agent |
|--------|-----------|----------|-------|
| {url} | High/Med | {finding} | 1 |
...

---
Orchestration file: {path}
Research completed: {timestamp}
```

### 5.4 Mark all todos complete

## Quick Mode Flow

For quick (single-fact) queries, skip orchestration:

1. State: `**Thoroughness**: quick — [reason]`
2. Launch single web-researcher agent: `Task("vibe-workflow:web-researcher", "{query}")`
3. Return agent's findings directly (no synthesis overhead)

## Key Principles

| Principle | Rule |
|-----------|------|
| Thoroughness first | Determine level before any research |
| Parallel execution | Launch multiple agents simultaneously when possible |
| Memento orchestration | Write to orchestration file after EACH agent returns |
| Cross-reference | Compare findings across agents before synthesizing |
| Context refresh | Read full orchestration file before final synthesis |
| Source preservation | Maintain citations through synthesis |
| Gap honesty | Explicitly state what couldn't be answered |

## Never Do

- Launch agents without determining thoroughness level
- Proceed to synthesis without collecting all agent results
- Skip orchestration file updates
- Present synthesized findings without source citations
- Ignore conflicts between agent findings
- Skip context refresh before final output

## Example: Technology Comparison

Query: "Compare the best real-time databases for a collaborative app in 2025"

**Thoroughness**: thorough — comparison query requiring multi-angle investigation

**Decomposition**:
- Facet 1: Real-time database landscape 2025 (what options exist)
- Facet 2: Performance and scalability comparisons
- Facet 3: Collaborative app requirements (conflict resolution, sync)
- Facet 4: Production experiences and case studies

**Agents launched** (parallel):
1. "Real-time database options 2025: Firebase, Supabase, Convex, others. Current market landscape."
2. "Real-time database performance benchmarks and scalability. Latency, throughput, concurrent users."
3. "Conflict resolution and sync strategies for collaborative apps. CRDTs, OT, last-write-wins."
4. "Production case studies using real-time databases. Companies, scale, lessons learned."

**Output**: Synthesized comparison table with recommendations based on use case, backed by cross-referenced sources from all four agents.
