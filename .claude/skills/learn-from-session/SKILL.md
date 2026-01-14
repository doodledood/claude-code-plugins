---
name: learn-from-session
description: 'Analyze Claude Code sessions to learn what went right/wrong and suggest high-confidence improvements to skills. Use when asked to analyze a session, learn from a session, or review workflow effectiveness.'
user-invocable: true
---

**User request**: $ARGUMENTS

Analyze a Claude Code session to identify what went well and what could be improved, then suggest high-confidence fixes to skills in this repository (primarily vibe-workflow).

**Input formats**:
- Session ID (UUID): `184078b7-2609-46e0-a1f2-bb42367a8d34`
- Session file path: `~/.claude/projects/.../session-id.jsonl`
- Inline commentary: Text description of what happened

**Output**: High-confidence issues only with evidence-based suggestions for skill improvements.

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
- [ ] Extract session overview (user intent, workflow used, outcome)
- [ ] Detect iteration patterns (retries, corrections)
- [ ] Detect workflow deviations (skipped steps, out-of-order)
- [ ] Detect missing questions / thin requirements
- [ ] Identify post-implementation fixes
- [ ] Read relevant skill definitions
- [ ] Compare actual vs documented behavior
- [ ] (expand: specific skill comparisons as needed)
- [ ] Refresh context: read full analysis log
- [ ] Synthesize high-confidence issues only
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
- `/plan` without `/spec` when requirements were ambiguous
- `/implement` without `/plan` for multi-file changes
- Chunks executed out of dependency order
- Verification skipped before approval

**Log format**:
```markdown
### Workflow Deviation: {what was skipped/reordered}
- Expected flow: {standard workflow}
- Actual flow: {what happened}
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

### 4.1 Identify relevant skills

Based on session content, identify which skills to compare:

| Session Pattern | Relevant Skills |
|-----------------|-----------------|
| Used `/spec` | `vibe-workflow/skills/spec/SKILL.md` |
| Used `/plan` | `vibe-workflow/skills/plan/SKILL.md` |
| Used `/implement` | `vibe-workflow/skills/implement/SKILL.md` |
| Used `/implement-inplace` | `vibe-workflow/skills/implement-inplace/SKILL.md` |
| Code review happened | `vibe-workflow/skills/review*/SKILL.md` |
| Bug investigation | `vibe-workflow/skills/bugfix/SKILL.md` |

### 4.2 Read skill definitions

For each relevant skill:
1. Read the SKILL.md file
2. Extract key rules, phases, and decision points
3. Note required questions and validation steps

### 4.3 Compare documented vs actual

For each skill used in the session:

| Aspect | Documented | Actual | Gap? |
|--------|------------|--------|------|
| Questions asked | {from skill} | {from session} | {Y/N} |
| Phases followed | {from skill} | {from session} | {Y/N} |
| Validations run | {from skill} | {from session} | {Y/N} |
| Outputs produced | {from skill} | {from session} | {Y/N} |

### 4.4 Log skill gaps

```markdown
### Skill Gap: {skill name}
- Documented behavior: {what skill says to do}
- Actual behavior: {what happened in session}
- Evidence: {specific session content showing gap}
- Confidence: HIGH | MEDIUM | LOW
```

**Only log HIGH confidence gaps** - where evidence is clear and gap is unambiguous.

---

## Phase 5: Synthesize Recommendations

### 5.1 Refresh context

**CRITICAL**: Read full analysis log before synthesis to restore all findings.

### 5.2 Filter to high-confidence only

An issue is HIGH confidence when:
1. **Clear evidence**: Specific session content demonstrates the problem
2. **Reproducible pattern**: Not a one-off edge case
3. **Actionable fix**: Clear change to skill that would address it
4. **Not already covered**: Skill doesn't already handle this case

Discard issues that are:
- Speculative (might have helped, but unclear)
- One-off (unusual situation unlikely to recur)
- Already documented (skill covers it, just wasn't followed)
- Low impact (wouldn't have changed outcome significantly)

### 5.3 Format recommendations

For each HIGH confidence issue:

```markdown
## Issue: {short title}

**Confidence**: HIGH
**Evidence**: {specific session content or pattern}

### What Happened
{Brief description of the problem}

### Root Cause
{Why the current skill didn't prevent this}

### Suggested Fix
**File**: {skill file path}
**Change**: {specific change to make}

{Code block showing the change if applicable}

### Expected Impact
{How this would have changed the session outcome}
```

---

## Phase 6: Output

### 6.1 Final report structure

```markdown
# Session Analysis: {session id or description}

## Summary
- **Session outcome**: {success/partial/rework needed}
- **Workflow used**: {skills invoked}
- **Issues found**: {count} high-confidence issues

## What Went Well
{List of things that worked correctly}

## High-Confidence Issues

### Issue 1: {title}
{Full issue format from 5.3}

### Issue 2: {title}
...

## Deferred (Medium/Low Confidence)
{Brief mention of patterns noticed but not confident enough to recommend changes}

---
Analysis log: {log file path}
```

### 6.2 Return report

Output the final report. User can then decide which fixes to implement.

---

## Key Principles

| Principle | Rule |
|-----------|------|
| Evidence-based | Every issue must cite specific session content |
| High confidence only | Don't suggest speculative improvements |
| Actionable | Each issue has a concrete fix suggestion |
| Skill-focused | Goal is improving skills, not critiquing the session |
| Memento | Write findings to log as you go, refresh before synthesis |

## Confidence Criteria

| Level | Criteria | Action |
|-------|----------|--------|
| HIGH | Clear evidence + reproducible + actionable + not covered | Include in report |
| MEDIUM | Some evidence but pattern unclear or edge case | Mention in "Deferred" |
| LOW | Speculative or one-off | Omit from report |

## Never Do

- Suggest changes without clear session evidence
- Include medium/low confidence issues in main recommendations
- Skip reading the full analysis log before synthesis
- Critique user behavior (focus on skill gaps, not user mistakes)
- Suggest fixes that would break other documented behavior
