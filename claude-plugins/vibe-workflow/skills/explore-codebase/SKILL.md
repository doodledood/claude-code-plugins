---
name: explore-codebase
description: 'Find all files relevant to a query with orthogonal exploration for comprehensive coverage. Returns topic-specific overview + file list with line ranges. Uses parallel agents for thorough+ levels to ensure nothing is missed.'
context: fork
---

**User request**: $ARGUMENTS

Find all files relevant to a specific query so you can master that topic without further searching.

## Thoroughness Level

**FIRST**: Determine thoroughness before exploring. Parse from natural language or auto-select.

**Auto-selection**:
- Single entity lookup ("where is X?") → quick
- Single bounded feature/bug → medium
- Multi-area feature, interaction queries → thorough
- "comprehensive"/"all"/"architecture"/"audit" → very-thorough

| Level | Exploration Strategy |
|-------|---------------------|
| **quick** | Single agent, no orchestration |
| **medium** | Single agent, no orchestration |
| **thorough** | Orthogonal agents (2-3), cross-reference, optional gap-fill |
| **very-thorough** | Orthogonal agents (3-4), cross-reference, gap-fill wave |

State: `**Thoroughness**: [level] — [reason]` then proceed.

---

## Quick / Medium Flow

### 1. Launch single agent

```
Task(subagent_type: "vibe-workflow:codebase-explorer", prompt: "$ARGUMENTS")
```

### 2. Read recommended files

When agent returns, read ALL files from the prioritized list.

### 3. Return to original task

---

## Thorough / Very-Thorough Flow

### 1. Decompose into orthogonal angles

Before launching agents, identify non-overlapping exploration angles. Each agent explores a distinct dimension.

**Standard angles for codebase exploration:**

| Angle | Focus | Example Scope |
|-------|-------|---------------|
| **Implementation** | Core logic files | "Files that implement {topic} behavior" |
| **Usage** | Callers, integration points | "Files that call/use {topic}" |
| **Tests** | Test files, fixtures | "Test files for {topic}" |
| **Config** | Configuration, environment | "Config files affecting {topic}" |

**Decomposition rules:**
- thorough: 2-3 angles (usually Implementation + Usage + Tests)
- very-thorough: 3-4 angles (all four)
- Each angle gets explicit boundaries to prevent overlap

### 2. Launch parallel agents

Launch all agents in a **single message** with multiple Task tool calls.

**Agent prompt template:**
```
{Specific exploration focus for this angle}

YOUR ASSIGNED SCOPE:
- {what to explore}
- {specific file patterns or areas}

DO NOT EXPLORE (other agents cover these):
- {angles assigned to other agents}

Thoroughness within scope: medium
```

**Example for "authentication" query (thorough):**

Agent 1 (Implementation):
```
Find core authentication implementation files.

YOUR ASSIGNED SCOPE:
- Auth service/module files
- Token generation, validation logic
- Session management implementation
- Password hashing, credential verification

DO NOT EXPLORE (other agents cover these):
- Files that CALL auth (usage patterns)
- Test files
- Config files
```

Agent 2 (Usage):
```
Find files that use/call authentication.

YOUR ASSIGNED SCOPE:
- Route handlers that require auth
- Middleware that checks auth
- Services that depend on auth context
- Integration points with auth

DO NOT EXPLORE (other agents cover these):
- Core auth implementation files
- Test files
- Config files
```

Agent 3 (Tests):
```
Find authentication test files.

YOUR ASSIGNED SCOPE:
- Unit tests for auth
- Integration tests for auth flows
- Test fixtures and mocks for auth
- E2E tests involving authentication

DO NOT EXPLORE (other agents cover these):
- Core auth implementation
- Files that use auth
- Config files
```

### 3. Collect and cross-reference

After all agents return, analyze for gaps:

**Cross-reference checklist:**
- [ ] Files mentioned by 2+ agents but not deeply explored by any?
- [ ] Any agent report "found reference to X but out of scope"?
- [ ] Core entry points covered?
- [ ] Error handling paths covered?
- [ ] Configuration dependencies identified?

**Gap indicators:**
- File appears in multiple agents' REFERENCE sections
- Agent noted "out of scope" discoveries
- Obvious category missing (e.g., no error handling files found)

### 4. Gap-fill wave (if needed)

**Launch gap-fill only if:**
- Cross-reference identified specific missed areas
- thorough: only for obvious gaps
- very-thorough: for any identified gaps

**Gap-fill prompt:**
```
Fill exploration gap: {specific gap identified}

Context from initial exploration:
- Already found: {summary of files from initial agents}
- Gap identified: {what's missing}

Focus narrowly on this gap. Don't re-explore already-covered areas.
```

**Limit:** Maximum 1-2 gap-fill agents. If more gaps exist, note them in output rather than launching unbounded agents.

### 5. Merge into unified reading list

Combine all agent outputs into single prioritized list:

```markdown
## OVERVIEW

[Merged overview combining insights from all agents. 150-400 words.
Describe: file organization, relationships between areas, entry points, data flow.
Note which angles were explored and key discoveries from each.]

## FILES TO READ

MUST READ:
- path/file.ext:lines - [reason] (from: {which agent})
...

SHOULD READ:
- path/file.ext:lines - [reason] (from: {which agent})
...

REFERENCE:
- path/file.ext - [reason] (from: {which agent})
...

## EXPLORATION SUMMARY

| Angle | Agent | Files Found | Key Discovery |
|-------|-------|-------------|---------------|
| Implementation | 1 | N | {1-liner} |
| Usage | 2 | N | {1-liner} |
| Tests | 3 | N | {1-liner} |
| Gap-fill | 4 | N | {1-liner} |

Gaps noted but not explored: {list or "none"}
```

**Deduplication rules:**
- Same file from multiple agents → keep highest priority, note "(multiple agents)"
- Overlapping line ranges → merge into single range
- Conflicting priorities → use higher priority

### 6. Read recommended files

Read ALL files from merged MUST READ and SHOULD READ sections.

### 7. Return to original task

---

## Key Principles

| Principle | Rule |
|-----------|------|
| Thoroughness first | Determine level before any exploration |
| Orthogonal angles | Each agent has distinct, non-overlapping scope |
| Parallel launch | All initial agents in single message |
| Cross-reference | Check for gaps after agents return |
| Limited gap-fill | At most 1-2 gap-fill agents, not unbounded |
| Merge carefully | Deduplicate, preserve priorities |

## Never Do

- Launch agents sequentially when they could be parallel
- Skip cross-reference step for thorough+
- Launch unbounded gap-fill waves
- Let agents explore overlapping areas
- Skip reading the files after exploration completes
