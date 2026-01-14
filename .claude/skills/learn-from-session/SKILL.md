---
name: learn-from-session
description: 'Analyze Claude Code sessions to learn what went right/wrong and suggest high-confidence improvements to skills. Use when asked to analyze a session, learn from a session, or review workflow effectiveness.'
user-invocable: true
---

**User request**: $ARGUMENTS

Analyze a Claude Code session to identify what went well and what could be improved, then suggest high-confidence fixes to skills in this repository.

**Input formats**:
- Session ID (UUID): `184078b7-2609-46e0-a1f2-bb42367a8d34`
- Session file path: `~/.claude/projects/.../session-id.jsonl`
- Inline commentary: Text description of what happened

**Output**: High-confidence issues only with evidence-based suggestions for skill improvements.

**Signal quality bar**: Only recommend changes that would have **measurably changed the session outcome**. A fix is high-signal if you can answer: "If this change existed, what specific iteration/correction/rework would NOT have happened?"

---

## Phase 1: Parse Input & Setup

### 1.1 Identify input type

| Input Pattern | Type | Action |
|---------------|------|--------|
| UUID format (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) | Session ID | Find and read session file |
| Path ending in `.jsonl` | Session file | Read directly |
| Other text | Commentary | Analyze inline, may reference sessions |

### 1.2 Locate session file (if session ID)

Session files are stored at:
```
~/.claude/projects/{project-path-encoded}/{session-id}.jsonl
```

Use Bash to find:
```bash
find ~/.claude/projects -name "*{session-id}*" -type f 2>/dev/null
```

### 1.3 Create analysis log (Memento pattern)

Path: `/tmp/session-analysis-{session-id-short}-{timestamp}.md`

```markdown
# Session Analysis Log

Session: {id or "inline commentary"}
Started: {timestamp}
Status: IN_PROGRESS

## Session Overview
(populated after parsing)

## Pattern Detection
(populated during analysis)

## Skill Comparison
(populated during comparison)

## Issues Found
(populated as issues identified)

## Final Recommendations
(populated at end)
```

### 1.4 Create todo list

```
- [ ] Parse session / read commentary
- [ ] Write session overview to log (user intent, skills used, outcome)
- [ ] Detect iteration patterns (retries, corrections)
- [ ] Write iteration findings to log
- [ ] Detect workflow deviations (skipped steps, out-of-order)
- [ ] Detect missing questions / thin requirements
- [ ] Identify post-implementation fixes
- [ ] Write all pattern detection findings to log
- [ ] Discover skills used in session
- [ ] (expand: read and analyze each skill as discovered)
- [ ] (expand: write skill comparison findings to log)
- [ ] Refresh context: read full analysis log    ← CRITICAL before synthesis
- [ ] Apply counterfactual test to each potential fix
- [ ] Write final recommendations
```

---

## Phase 2: Parse Session

### 2.1 Session file structure

Claude Code sessions are JSONL files with these record types:

| Type | Contains |
|------|----------|
| `user` | User messages, `message.content` field |
| `assistant` | Claude responses, tool calls, thinking |
| `system` | System events, commands, hooks |
| `file-history-snapshot` | File state tracking |

### 2.2 Extract key events

Use `jq` to parse:

```bash
# User messages
cat {session-file} | jq -r 'select(.type == "user") | .message.content' 2>/dev/null

# Tool calls
cat {session-file} | jq -r 'select(.type == "assistant") | .message.content | if type == "array" then .[] | select(.type == "tool_use") | .name else empty end' 2>/dev/null

# Skill invocations
grep -o '"skill":"[^"]*"' {session-file} | sort | uniq -c
```

### 2.3 Build session overview

Extract and log:
- **Initial request**: First user message (the goal)
- **Workflow used**: Which skills invoked (`/spec`, `/plan`, `/implement`, etc.)
- **Workflow skipped**: Expected skills NOT invoked based on task complexity
- **Outcome**: Success, partial, or required rework
- **Session length**: Message count, duration if available

---

## Phase 3: Pattern Detection

Analyze the session for these patterns. Each pattern has evidence requirements.

### 3.1 Iteration patterns (things that didn't work first time)

**Evidence required**: Same file edited multiple times, OR error → fix → retry sequence

Look for:
- TypeScript errors followed by fixes
- Test failures followed by code changes
- Lint errors followed by formatting changes
- Same function/file touched 3+ times

**Log format**:
```markdown
### Iteration: {description}
- Files affected: {list}
- Attempts: {count}
- Root cause: {why it didn't work first time}
- Potential skill gap: {what could have prevented this}
```

### 3.2 User corrections ("no, I meant...")

**Evidence required**: User message containing correction language

Correction indicators:
- "no", "not what I meant", "actually", "instead", "I meant"
- "let's go back", "undo", "revert"
- "that's wrong", "incorrect"

**Log format**:
```markdown
### User Correction: {what was corrected}
- Original action: {what Claude did}
- User feedback: {correction text}
- Missing context: {what Claude should have asked/known}
```

### 3.3 Workflow deviations

**Evidence required**: Expected workflow step skipped or out-of-order

Check for:
- Multi-phase skill invoked but phases skipped (read skill to know expected phases)
- Skill with prerequisites invoked without those prerequisites (e.g., implementation without planning)
- Ordered steps executed out of order
- Verification/validation steps skipped before proceeding

**How to detect**: Compare skill's documented phases against actual session sequence.

**Log format**:
```markdown
### Workflow Deviation: {what was skipped/reordered}
- Skill: {which skill's workflow}
- Expected flow: {phases from skill definition}
- Actual flow: {what happened in session}
- Impact: {did this cause issues later?}
```

### 3.4 Missing questions

**Evidence required**: Information discovered during implementation that should have been asked upfront

Look for:
- Design decisions made mid-implementation
- Assumptions that were later corrected
- "The user confirmed..." appearing late in session
- Post-implementation "actually, let's change..." patterns

**Log format**:
```markdown
### Missing Question: {what should have been asked}
- Discovered at: {phase where it came up}
- Impact: {rework required}
- Skill gap: {which skill should have asked this}
```

### 3.5 Post-implementation fixes

**Evidence required**: Changes made AFTER "implementation complete" or PR creation

Look for:
- Commits/changes after PR URL appears
- Refactoring after "done" or "complete" messages
- Review findings that required code changes
- User requesting changes after seeing "finished"

**Log format**:
```markdown
### Post-Implementation Fix: {what was fixed}
- Original implementation: {what was done}
- Fix required: {what changed}
- Should have been caught by: {which phase/skill}
```

---

## Phase 4: Skill Comparison

### 4.1 Discover skills used in session

Extract skill invocations from session:

```bash
# Find all Skill tool invocations
grep -o '"skill":"[^"]*"' {session-file} | sort | uniq -c

# Find slash command patterns in user messages
grep -oE '/(spec|plan|implement|review|bugfix|[a-z-]+)' {session-file} | sort | uniq -c
```

For each skill name found, locate the SKILL.md:

```bash
# Search across all plugins in the repo
find claude-plugins -path "*/skills/*/SKILL.md" -exec grep -l "name: {skill-name}" {} \;

# Also check repo-level skills
find .claude/skills -name "SKILL.md" 2>/dev/null
```

**Log discovered skills**:
```markdown
## Skills Used in Session
- {skill-name}: {plugin}/{path} - invoked {count} times
```

### 4.2 Extract actionable rules from each skill

For each skill file, extract:

**Rule indicators** (look for these patterns):
- `must`, `should`, `never`, `always` → mandatory behaviors
- `## Phase N:` or `### Step N:` → workflow phases
- `questions:` or `AskUserQuestion` → required user prompts
- `| Condition | Action |` tables → decision rules
- `**CRITICAL**`, `**IMPORTANT**` → high-priority rules
- `- [ ]` todo templates → expected workflow steps
- `Acceptance:` or `Validation:` → verification requirements

**Extract and log**:
```markdown
### Skill: {name}
**File**: {path}

**Mandatory behaviors**:
- {rule with line number}

**Workflow phases**:
1. {phase name} - expected outputs: {list}

**Required questions** (when applicable):
- {question topic}

**Verification steps**:
- {what should be checked}
```

### 4.3 Compare documented vs actual

For each skill used in the session:

| Aspect | Documented | Actual | Gap? | Impact |
|--------|------------|--------|------|--------|
| Questions asked | {from skill} | {from session} | {Y/N} | {would have prevented X} |
| Phases followed | {from skill} | {from session} | {Y/N} | {would have caught Y} |
| Validations run | {from skill} | {from session} | {Y/N} | {would have avoided Z} |
| Outputs produced | {from skill} | {from session} | {Y/N} | {required later but missing} |

**Key comparison questions**:
1. Did the skill ask all documented questions? If not, did missing answers cause issues?
2. Were all phases executed in order? If skipped, did it matter?
3. Were validations run? If skipped, did bugs slip through?
4. Did outputs match documented format? If not, did downstream steps suffer?

### 4.4 Log skill gaps with impact

```markdown
### Skill Gap: {skill name}
- **Rule violated**: {what skill says to do, with line reference}
- **What happened**: {actual behavior in session}
- **Evidence**: {specific session content showing gap}
- **Impact**: {did this cause iteration/correction/rework?}
- **Counterfactual**: {if rule was followed, would outcome differ?}
- **Confidence**: HIGH | MEDIUM | LOW
```

**Only log gaps where**:
1. Evidence is clear (specific session content)
2. Impact is documented (caused measurable problem)
3. Counterfactual is plausible (fix would have helped)

---

## Phase 5: Synthesize Recommendations

### 5.1 Refresh context

**CRITICAL**: Read full analysis log before synthesis to restore all findings.

### 5.2 Counterfactual analysis (the high-signal filter)

For each potential issue, apply this test:

```
IF this skill change existed BEFORE the session:
  WOULD a specific iteration/correction/rework NOT have happened?
  CAN you name the exact moment it would have intervened?
  WOULD the change have been triggered (conditions met)?
```

**Scoring**:
| Score | Criteria | Action |
|-------|----------|--------|
| 3/3 | All yes → definite causal link | HIGH confidence |
| 2/3 | Likely would have helped | MEDIUM confidence |
| 1/3 or 0/3 | Speculative | Discard |

**Example counterfactual**:
```
Issue: Plan skill should ask about time filtering
Counterfactual:
  - WOULD iteration have been avoided? YES - 90-day filter added post-implementation
  - CAN I name exact moment? YES - during "Files to modify" phase, should have asked
  - WOULD change have triggered? YES - requirement mentioned "recent refunds"
Score: 3/3 → HIGH confidence
```

### 5.3 Additional disqualifiers

Even with 3/3 counterfactual score, discard if:
- **Compliance failure**: Skill already documents this; it just wasn't followed
- **One-off context**: Unusual situation unlikely to recur (e.g., user typo)
- **Scope creep**: Fix would make skill too complex for marginal benefit
- **Side effects**: Fix would break other documented behavior

### 5.4 Format recommendations

For each HIGH confidence issue:

```markdown
## Issue: {short title}

**Confidence**: HIGH
**Counterfactual score**: 3/3

### Evidence
{Quote or describe specific session content}

### What Happened
{Brief description of the problem}

### Root Cause
{Why the current skill didn't prevent this - be specific about what's missing}

### Counterfactual
- **Iteration avoided**: {which rework/correction would NOT have happened}
- **Intervention point**: {exact moment the fix would have triggered}
- **Trigger condition**: {why the fix would have applied to this session}

### Suggested Fix
**File**: {skill file path}
**Section**: {phase/section name}
**Line**: ~{approximate line number}

**Current behavior**:
{What the skill does now}

**Proposed behavior**:
{What the skill should do instead}

```{code block showing the diff if applicable}```

### Risk Assessment
- **Side effects**: {could this break other flows? NO/LOW/MEDIUM/HIGH}
- **Complexity added**: {minimal/moderate/significant}
- **Test approach**: {how to verify the fix works}
```

---

## Phase 6: Output

### 6.1 Final report structure

```markdown
# Session Analysis: {session id or description}

## Summary
- **Session outcome**: {success/partial/rework needed}
- **Workflow used**: {skills invoked}
- **Iterations observed**: {count of retry/fix cycles}
- **High-signal fixes**: {count} (3/3 counterfactual score)

## What Went Well
{List of things that worked correctly - be specific about which skill behaviors succeeded}

## Iteration Timeline
{Chronological list of corrections/retries observed, with timestamps if available}

1. {time}: {what was attempted}
2. {time}: {what went wrong}
3. {time}: {how it was fixed}

## High-Confidence Improvements

### Fix 1: {title}
{Full format from 5.4}

### Fix 2: {title}
...

## Deferred (Partial Counterfactual Match)
{Issues that scored 2/3 - might help but not definitively causal}

| Issue | Missing Criterion | Why Deferred |
|-------|-------------------|--------------|
| {title} | {which of the 3 failed} | {brief explanation} |

## Not Actionable
{Issues that scored 1/3 or 0/3, or hit disqualifiers - briefly note for transparency}

---
Analysis log: {log file path}
```

### 6.2 Return report

Output the final report. User can then decide which fixes to implement.

---

## Key Principles

| Principle | Rule |
|-----------|------|
| Counterfactual-driven | Every fix must pass the 3/3 counterfactual test |
| Evidence-based | Quote or cite specific session content |
| Iteration-focused | Primary signal = things that required retry/correction |
| Skill-focused | Goal is improving skills, not critiquing user or session |
| Memento | Write findings to log as you go, refresh before synthesis |

## Confidence Criteria (Counterfactual-Based)

| Score | Test Results | Action |
|-------|--------------|--------|
| 3/3 | Would avoid iteration + Name exact moment + Conditions would trigger | HIGH → Include |
| 2/3 | Two of three | MEDIUM → Deferred section |
| 1/3 | One of three | LOW → Not Actionable section |
| 0/3 | None | Discard entirely |

## Disqualifiers (Even at 3/3)

| Disqualifier | Why It Filters Out |
|--------------|--------------------|
| Compliance failure | Skill already covers this - LLM didn't follow |
| One-off context | Unusual situation unlikely to recur |
| Scope creep | Fix adds complexity disproportionate to benefit |
| Side effects | Fix would break other documented behaviors |

## Never Do

- Suggest changes without specific session evidence
- Include fixes that score <3/3 in main recommendations
- Skip the counterfactual test ("it seems like it would help")
- Skip reading the full analysis log before synthesis
- Critique user behavior (focus on skill gaps, not user mistakes)
- Suggest fixes that would break other documented behavior
- Recommend changes to skills that weren't used in the session
