# Plan: Add Approach Section to Manifest

## Problem Statement

For complex PRs, the gap between "what to build" (manifest) and "just do it" (`/do`) is too large. Models:
- Take wrong architectural paths early, waste tokens, get stuck
- Get lost mid-task, don't know how to proceed
- Stop prematurely because they can't see the path forward

Verification loops (`/verify`) catch problems AFTER committing to a path, but don't prevent architectural dead ends. By then, significant effort may be wasted.

## Solution

Add **Approach** section to the manifest schema. The manifest becomes a complete contract:

| Section | Purpose |
|---------|---------|
| Intent & Context | WHY we're doing this |
| **Approach** | HOW we'll get there (validated direction) - NEW |
| Global Invariants | RULES that must hold throughout |
| Process Guidance | Non-verifiable HOW constraints |
| Deliverables + ACs | WHAT success looks like |

## Design Principles

From `prompt-engineering:prompt-engineering`:

| Principle | Application |
|-----------|-------------|
| WHAT and WHY, not HOW | Approach is direction, not step-by-step script |
| Avoid arbitrary values | Order based on logical dependencies, not "do 3 things" |
| Trust capability | Architecture defines direction, model decides tactics |
| Generate candidates, validate | `/define` generates approach options, user validates |
| Maximize information density | Approach section is lean—architecture, order, risks, trade-offs |

## New Manifest Schema

```markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts/architecture understanding]

## 2. Approach                                              ← NEW SECTION
*Validated implementation direction.*

- **Architecture:** [High-level HOW - the validated direction]

- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: [why this order - dependencies, risk reduction, etc.]

- **Risk Areas:** (pre-mortem outputs)
  - [R-1] [What could go wrong] | Detect: [how you'd know]
  - [R-2] [What could go wrong] | Detect: [how you'd know]

- **Trade-offs:**
  - [T-1] [Priority A] vs [Priority B] → Prefer [A] because [reason]
  - [T-2] [Priority X] vs [Priority Y] → Prefer [Y] because [reason]

## 3. Global Invariants (The Constitution)
- [INV-G1] Description | Verify: [method]
- [INV-G2] Description | Verify: [method]

## 4. Process Guidance
- [PG-1] Description (non-verifiable HOW constraint)

## 5. Deliverables (The Work)

### Deliverable 1: [Name]
- **Acceptance Criteria**:
  - [AC-1.1] Description | Verify: [method]
  - [AC-1.2] Description | Verify: [method]

### Deliverable 2: [Name]
- **Acceptance Criteria**:
  - [AC-2.1] Description | Verify: [method]
```

## ID Scheme

| Type | Pattern | Purpose | Used By |
|------|---------|---------|---------|
| Global Invariant | INV-G{N} | Task-level rules | /verify (verified) |
| Process Guidance | PG-{N} | Non-verifiable HOW constraints | /do (followed) |
| Risk Area | R-{N} | Pre-mortem flags | /do (watched) |
| Trade-off | T-{N} | Decision criteria for adjustment | /do (consulted) |
| Acceptance Criteria | AC-{D}.{N} | Deliverable completion | /verify (verified) |

## Approach Components Explained

### Architecture

High-level implementation direction. NOT a step-by-step script.

**Good:**
- "Add new AuthService that wraps existing token logic, expose via REST endpoint"
- "Extend existing Parser class with new node types, update visitors accordingly"

**Bad:**
- "First create file X, then add function Y, then call Z" (too prescriptive)
- "Implement the feature" (too vague)

### Execution Order

Which deliverable first, and why. Makes dependencies explicit.

**Good:**
- "D1 → D2 → D3 | D1 creates the data model D2 and D3 depend on"
- "D2 → D1 → D3 | D2 is highest risk, validate approach early"

**Bad:**
- "Do them in order" (no rationale)
- "D1, D2, D3" (no indication of dependencies)

### Risk Areas

Pre-mortem outputs. Things that could go wrong, and how to detect them.

**Purpose:**
1. Flags to watch during `/do`
2. Context for adjustment decisions
3. Input for escalation if risks materialize severely

**Example:**
```markdown
- [R-1] Existing API may not support batch operations | Detect: API returns 400 on array input
- [R-2] Test suite may be too slow for iterative verification | Detect: Single test run > 5 min
```

**Not included:** Specific fallback paths. Model adapts using trade-offs as guide.

### Trade-offs

User-validated priorities. Decision criteria when facing competing concerns.

**Purpose:**
1. Guide autonomous adjustment when approach hits reality
2. Capture user preferences before they're needed
3. Enable `/do` to make decisions without escalating

**Example:**
```markdown
- [T-1] Performance vs. Simplicity → Prefer Simplicity because codebase prioritizes readability
- [T-2] Complete solution vs. Incremental → Prefer Incremental because we can iterate
```

## Autonomous Adjustment During /do

When approach hits reality and needs adjustment:

### Decision Flow

```
Risk detected (R-N)?
    │
    ├─ no → Continue with original approach
    │
    └─ yes → Log detection
             Consult trade-offs (T-N)
             Determine adjustment
                    │
                    ▼
             Can ACs still be met?
                    │
                    ├─ yes → Adjust approach
                    │        Log change + rationale
                    │        Continue autonomously
                    │
                    └─ no → /escalate
                            Include: which AC, why unachievable,
                            what would need to change
```

### Escalation Boundary

The line between autonomous adjustment and escalation:

| Situation | Action |
|-----------|--------|
| Tactics change, ACs still achievable | Autonomous - log and continue |
| Architecture shift, ACs still achievable | Autonomous - log and continue |
| ACs can't be met as written | Escalate - contract broken, need user |

**Key insight:** ACs are the contract. As long as they can be satisfied, `/do` has freedom to adapt. When they can't, user input is required.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              /define                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Interview (generate candidates, user validates)                       │
│                                                                         │
│   Phase 1: Intent & Context                                             │
│       - Goal, mental model, task type                                   │
│                                                                         │
│   Phase 2: Approach    ← NEW                                            │
│       - Architecture (generate options, validate)                       │
│       - Execution order (dependencies, rationale)                       │
│       - Risk areas (pre-mortem: what could go wrong?)                   │
│       - Trade-offs (priorities when facing competing concerns)          │
│                                                                         │
│   Phase 3: Deliverables                                                 │
│       - What are we building?                                           │
│       - Acceptance criteria for each                                    │
│                                                                         │
│   Phase 4: Invariants & Process Guidance                                │
│       - Global rules (auto-detect + generate candidates)                │
│       - Non-verifiable constraints                                      │
│                                                                         │
│                          ┌────────────────────┐                         │
│                   ┌─────▶│ manifest-verifier  │◀────┐                   │
│                   │      └────────────────────┘     │                   │
│                   │               │                 │                   │
│                   │      ┌────────┴────────┐        │                   │
│                   │      ▼                 ▼        │                   │
│                   │  COMPLETE           CONTINUE    │                   │
│                   │      │                 │        │                   │
│                   │      ▼                 └────────┘                   │
│                   │  manifest.md        (more questions)                │
│                   │                                                     │
└───────────────────┼─────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                /do                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ Extract from manifest:                                          │   │
│   │   - Architecture, execution order, risks, trade-offs            │   │
│   │   - Invariants, process guidance                                │   │
│   │   - Deliverables with ACs                                       │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ Create log: /tmp/do-log-{timestamp}.md                          │   │
│   │ Initialize todos from deliverables                              │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ For each Deliverable (in execution order):                      │   │
│   │                                                                 │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ Implement, satisfying ACs                               │   │   │
│   │   │ Follow architecture direction                           │   │   │
│   │   │ Respect process guidance (PG-*)                         │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   │                          │                                      │   │
│   │                          ▼                                      │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ Risk detected (R-N)?                                    │   │   │
│   │   │   - no: continue                                        │   │   │
│   │   │   - yes: consult trade-offs, adjust, log change         │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   │                          │                                      │   │
│   │                          ▼                                      │   │
│   │   ┌─────────────────────────────────────────────────────────┐   │   │
│   │   │ Can ACs still be met?                                   │   │   │
│   │   │   - yes: continue autonomously                          │   │   │
│   │   │   - no: /escalate (contract broken)                     │   │   │
│   │   └─────────────────────────────────────────────────────────┘   │   │
│   │                          │                                      │   │
│   │                          ▼                                      │   │
│   │                    Log progress                                 │   │
│   │                                                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│                             ┌────────────┐                              │
│                             │  /verify   │                              │
│                             └────────────┘                              │
│                                    │                                    │
│                  ┌─────────────────┼─────────────────┐                  │
│                  ▼                 ▼                 ▼                  │
│              FAILURES          ALL PASS          STUCK                  │
│                  │                 │                 │                  │
│                  ▼                 ▼                 ▼                  │
│            Fix specific        /done           /escalate                │
│            criteria, retry                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Files to Change

### 1. `skills/define/SKILL.md`

**Changes:**
- Add Approach section to manifest schema
- Add interview phase for Approach (between Intent and Deliverables)
- Add probing for: architecture options, execution order, risk areas (pre-mortem), trade-offs
- Update manifest template

**New interview questions to generate candidates for:**
- Architecture: "Given the intent, here are possible approaches: [A], [B], [C]. Which aligns with your codebase?"
- Execution order: "Suggested order based on dependencies: D1 → D2 → D3. Rationale: [X]. Adjust?"
- Risks: "Pre-mortem: what could cause this to fail? Candidates: [R1], [R2], [R3]"
- Trade-offs: "When facing [tension], what's the priority? [A] vs [B]?"

### 2. `skills/do/SKILL.md`

**Changes:**
- Extract approach components (architecture, order, risks, trade-offs)
- Follow execution order
- Watch for risk area triggers
- Consult trade-offs when adjusting
- Log adjustments with rationale
- Escalation boundary: can ACs still be met?

**New principles:**
- Architecture is direction, not constraint—adapt tactics freely
- Trade-offs guide adjustment decisions
- Escalate when ACs become unachievable, not before

### 3. `agents/manifest-verifier.md`

**Changes:**
- Add gap detection for Approach section:
  - Missing architecture (complex task but no direction)
  - Vague architecture (too generic to guide implementation)
  - No execution order (multi-deliverable but no sequence/rationale)
  - Missing risk areas (no pre-mortem for complex task)
  - Missing trade-offs (competing concerns identified but no priority)
  - Inconsistent order (execution order doesn't match deliverable dependencies)

### 4. `README.md`

**Changes:**
- Update manifest schema section
- Update workflow diagram
- Add Approach section explanation
- Update ID scheme table

### 5. `.claude-plugin/plugin.json`

**Changes:**
- Version bump (minor - new feature)

### 6. `CHANGELOG.md` (repo root)

**Changes:**
- Add entry for this version

## What Approach Is NOT

| Anti-pattern | Why Bad |
|--------------|---------|
| Step-by-step script | Rigid, breaks on contact with reality |
| Task list | That's what deliverables are for |
| Prescriptive micro-HOW | Violates "WHAT not HOW" principle |
| Exhaustive risk enumeration | Over-engineering; focus on likely/high-impact risks |
| Fallback paths | Speculative; let model adapt using trade-offs |

## What Approach IS

| Component | Purpose |
|-----------|---------|
| Architecture | Validated direction—reduces search space |
| Execution Order | Clear sequence—prevents "where do I start?" |
| Risk Areas | Pre-mortem flags—things to watch for |
| Trade-offs | Decision criteria—enables autonomous adjustment |

## Success Criteria for This Change

1. **Reduced wrong-path starts**: Model has validated direction before coding
2. **Fewer mid-task stalls**: Clear execution order and trade-offs for decisions
3. **Maintained autonomy**: `/do` can adjust without escalating (when ACs achievable)
4. **Appropriate escalation**: User pulled in only when contract (ACs) can't be honored
5. **No over-engineering**: Approach section is lean, not exhaustive planning

## Open Questions

1. **Approach complexity scaling**: Should simple tasks (1 deliverable) require full Approach section, or is it optional/minimal?

2. **Trade-off format**: Is "A vs B → Prefer A because X" sufficient, or do we need more structure (weights, conditions)?

3. **Risk area granularity**: How many risks are enough? Too few misses things, too many is noise.

4. **Adjustment logging**: What format for logging approach adjustments? Needs to be useful for context recovery.

---

*Plan version: 1.0*
*Created: 2025-01-24*
