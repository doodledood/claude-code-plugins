# Implement Skill Interview Log

Started: 2026-01-17
Status: In Progress

---

## Core Architecture (Confirmed)

### Skill Chain
```
/implement
  → works toward criteria (no plan decomposition)
  → calls /verify when thinks ready

/verify (NOT user-invocable)
  → runs all verifications against current code state
  → if automated failures → return failures only (hide manual)
  → if automated pass + manual exists → return manual (hint to escalate)
  → if all pass → calls /done

/done (NOT user-invocable)
  → marker only - just exists in transcript
  → signals completion, makes agent stop and summarize

/escalate (NOT user-invocable)
  → structured evidence + free-form explanation
  → signals genuinely stuck
```

### Hooks
```
PreToolUse on /escalate:
  → checks /verify was called first in current /implement flow
  → blocks if no /verify → "must attempt verification before escalating"

Stop:
  → /implement started?
    → /done called after? → ALLOW
    → /escalate called after? → ALLOW
    → neither? → BLOCK
```

---

## Decisions Log

| # | Question | Decision | Notes |
|---|----------|----------|-------|
| 1 | What does /verify do | B - auto-call /done if all pass | /verify returns feedback on fail, calls /done on success |
| 2 | /verify user-invocable | No | Only called by /implement |
| 3 | Stack tracking on interrupt | A - each /implement fresh | New flow resets requirement |
| 4 | How /verify returns failures | A - return control flow | /implement stays running, receives feedback |
| 5 | What /done does | A - just exists in transcript | Marker for stop hook |
| 6 | Stop hook logic | Simple | /implement started → /done or /escalate called after? |
| 7 | Escalation path | A - /implement escalates directly | Via /escalate skill |
| 8 | /verify crash handling | A - retry | With escalation path for truly stuck |
| 9 | /done without /verify | B - stop hook catches | Sees /done but no /verify, blocks |
| 10 | Multiple /verify calls | A - fresh each time | Expected flow: implement → verify → fail → implement → verify |
| 11 | State persistence | B - git IS the state | Commits, staged, working tree. Explore to resume |
| 12 | What makes escalation valid | PreToolUse hook | Checks /verify was called before /escalate |
| 13 | /escalate output | A + B | Structured evidence AND free-form context |
| 14 | Stop hook on /escalate | A - just allow | Trust the flow |
| 15 | /verify must fail before /escalate | A - no | /verify must exist, failure not required |
| 16 | Continue after /escalate | B - can continue | Escalation pauses for human, doesn't end flow |
| 17 | Verification method types | D - all | Bash commands, subagents, manual (flagged) |
| 18 | Verification prioritization | A - automated first | Only surface manual when automated done |
| 19 | Impossible automated criteria | A - same flow | Eventually escalate via normal path |
| 20 | /verify state | A - stateless | Fresh check each time |
| 21 | Only manual criteria | A - immediate return | Return manual for escalation |
| 22 | Code state means | A - working tree | Including uncommitted changes |
| 23 | /verify capabilities | A - both | Commands AND parallel subagents |
| 24 | Verification timeout | A - per-criterion | Higher timeout with retries |
| 25 | Pre-mortem concerns | Loops + premature stop | Main worries |
| 26 | Disappointed scenarios | Code quality | Solution: review agents in spec |
| 28 | Review agents in /verify | A - unified | Review criteria IN spec, reviewers ARE verifiers |
| 29 | Standard reviews | A - user decides | Spec specifies which reviews matter |
| 30 | Avoiding redundant work | C - both | Actionable feedback AND track attempts |
| 31 | Files /implement maintains | C - both | Implementation log AND meaningful commits |
| 32 | /verify reads impl log | A - yes | Gives context on what was tried |
| 33 | Tracking attempts | A - impl log | "Tried X for AC-5, failed because Y" |
| 34 | Implementation log location | A - /tmp/ | /tmp/implement-log-{timestamp}.md |

---

## Memento Pattern Requirement

All skills (/spec, /implement, /verify) must:
- Write findings to external files before proceeding
- Prevents context loss on compaction
- /verify can read implementation log + code for fuller picture

### /implement maintains:
- `/tmp/implement-log-{timestamp}.md` - what was done, tried, blockers
- Meaningful git commits with descriptive messages

### /verify reads:
- Spec file (criteria, verification methods)
- Implementation log (attempts, what was tried)
- Current code state (working tree)

---

## /verify Logic (Confirmed)

```python
def verify(spec_file):
    # 1. Parse spec
    criteria = parse_spec(spec_file)
    automated = [c for c in criteria if c.method != 'manual']
    manual = [c for c in criteria if c.method == 'manual']

    # 2. Run automated verifications (parallel where possible)
    # - Bash commands: npm test, tsc, etc. (with retries, higher timeout)
    # - Subagents: code pattern checks (parallel by criterion group)
    results = run_verifications(automated)

    # 3. Check results
    failures = [r for r in results if r.status == 'fail']

    if failures:
        # Return failures only - DON'T mention manual yet
        return VerifyResult(status='fail', failures=failures)

    if manual:
        # All automated pass, manual exists
        # Return manual criteria - hint to /implement to escalate
        return VerifyResult(status='manual_pending', manual=manual)

    # All pass, no manual
    call_done_skill()
    return VerifyResult(status='pass')
```

---

## Key Design Principles

1. **Skills not user-invocable**: /verify, /done, /escalate are internal only
2. **Stateless verification**: /verify checks current state each time, no memory
3. **Git is state**: No session files, codebase (commits, staged, working) IS the state
4. **Prioritize automated**: Manual criteria only surfaced after automated pass
5. **Hooks enforce flow**: PreToolUse blocks premature escalation, Stop blocks premature completion
6. **Parallel verification**: Subagents can run in parallel for efficiency

---

## Pre-mortem Risks (Q25)

User's main concerns:
1. **Redundant work / loops** - getting stuck retrying same thing
2. **Premature stopping** - escape hatches allowing stop before truly done

Other risks identified:
- LLM finds loophole to call /done without real verification
- /verify subagent says "pass" but code actually broken
- Stop hook bug allows stop without /done
- LLM escalates immediately without trying (lazy escalation)

---

## Disappointed Scenarios (Q26)

Even if "works" (all criteria pass), user might be unhappy because:
- Code is sloppy even though it "works"
- Implementation took weird approach
- Messy git history

**User's solution**: /verify should run review agents (like existing /review skill).
Approach, standards, code quality should ALL be in the spec and verified.

---

## Open Questions

- Q27: What would make you reject even if technically meets criteria? (User: not sure)
- Need to explore: verification methods and subagent details
- Need to explore: how review agents integrate with /verify

---

## Next Steps

1. Clarify how review agents integrate with /verify
2. Clarify subagent parallelization
3. Complete adversarial scenarios
4. Write final spec

---

*Last updated: 2026-01-17 during interview*
