# Subagent Definitions for Implement Skill Verification

These subagents verify the acceptance criteria for the /implement and /done skills.

---

## input-handler-checker

**Purpose**: Verifies /implement skill correctly handles spec file input.

**Context Files**:
- Skill invocation transcript
- $ARGUMENTS value

**Checks**:
```yaml
- id: reads-file-path
  check: "Skill interprets $ARGUMENTS as file path"
  how: "First action should be Read tool on the path"

- id: validates-existence
  check: "Validates file exists before proceeding"
  how: "Error reported if file not found, doesn't proceed with missing file"

- id: parses-structure
  check: "Parses spec structure correctly"
  how: "Criteria and verification methods extracted and referenced in subsequent work"

- id: clear-error
  check: "Reports clear error on invalid input"
  how: "If file invalid, error message explains what's wrong (not found, invalid format, missing sections)"
```

**Output**: Pass/Fail with details on input handling behavior.

---

## spec-parser-checker

**Purpose**: Verifies all criteria extracted from spec.

**Context Files**:
- Spec file
- Session file showing extracted criteria

**Checks**:
```yaml
- id: all-ids-extracted
  check: "All criterion IDs from spec present in session"
  how: "Compare spec criteria list to session.criteria keys"

- id: verification-methods-preserved
  check: "Verification methods stored for each criterion"
  how: "Each session.criteria entry has method info"

- id: examples-available
  check: "Accepted/rejected examples loaded for reference"
  how: "Examples section parsed and accessible"

- id: subagents-loaded
  check: "Task-specific subagent definitions available"
  how: "Subagent definitions from spec accessible for /done execution"
```

**Output**: Extraction completeness report.

---

## execution-pattern-checker

**Purpose**: Verifies implementation follows criteria-driven pattern, not plan-driven.

**Context Files**:
- Implementation transcript

**Checks**:
```yaml
- id: no-plan-file
  check: "No plan file created (e.g., /tmp/plan-*.md)"
  how: "Grep for plan file creation in transcript"

- id: no-chunk-decomposition
  check: "No explicit chunking like 'Chunk 1', 'Chunk 2'"
  how: "Transcript doesn't show chunk-based progression"

- id: criteria-directed
  check: "Work references criteria IDs"
  how: "Actions mention 'for AC-1' or 'to satisfy criterion X'"

- id: internal-reasoning-ok
  check: "Internal reasoning about approach is fine"
  how: "LLM can think about how to achieve criteria, just not external plan artifact"
```

**Output**: Pattern analysis showing criteria-driven vs plan-driven indicators.

---

## todo-pattern-checker

**Purpose**: Verifies TodoWrite entries are criteria-based.

**Context Files**:
- Transcript with TodoWrite calls

**Checks**:
```yaml
- id: references-criteria-ids
  check: "Todo items reference criterion IDs (AC-N)"
  how: "Parse TodoWrite inputs, check for AC-N or criterion names"

- id: completion-tied-to-verification
  check: "Todos marked complete only after verification"
  how: "Completion follows /done verification, not just 'I did the work'"

- id: no-step-based
  check: "No generic step-based todos"
  bad_patterns:
    - "Write code for X"
    - "Implement Y"
    - "Fix Z"
    - "Clean up"
  how: "Todos should be 'Verify AC-N: description', not implementation steps"
```

**Output**: Todo pattern analysis with specific violations.

---

## transcript-analyzer

**Purpose**: Analyzes transcript for proper /done invocation before completion.

**Context Files**:
- Full transcript

**Checks**:
```yaml
- id: done-before-complete
  check: "/done skill invoked before any completion declaration"
  how: "Find /done call, then find any 'done', 'complete', 'finished' - /done must come first"

- id: results-processed
  check: "Verification results received and referenced"
  how: "After /done output, transcript shows LLM processing results"

- id: failures-continued
  check: "If /done shows failures, implementation continues"
  how: "Failed verification followed by more implementation work, not stop"
```

**Output**: Timeline showing /done calls relative to completion attempts.

---

## loop-behavior-checker

**Purpose**: Verifies proper handling of verification failures.

**Context Files**:
- Transcript showing verification failure and subsequent work

**Checks**:
```yaml
- id: failures-identified
  check: "Failed criteria identified from /done output"
  how: "LLM references specific failing criteria after /done"

- id: targeted-work
  check: "Work targets specific failures"
  how: "Actions after failure mention the failing criterion"

- id: no-restart
  check: "Does not restart from scratch"
  how: "No re-reading spec, no re-initializing session"

- id: preserves-passing
  check: "Already passing criteria not re-implemented"
  how: "Work focuses on failures, doesn't touch verified-passing areas"
```

**Output**: Loop behavior analysis with targeting accuracy.

---

## escalation-checker

**Purpose**: Verifies escalation requests meet evidence requirements.

**Context Files**:
- Escalation message in transcript

**Checks**:
```yaml
- id: criterion-identified
  check: "Specifies which criterion is blocking"
  how: "Escalation mentions specific AC-N or criterion name"

- id: attempts-documented
  check: "At least 3 different approaches documented"
  how: "Numbered list of attempts with what was tried"

- id: failures-explained
  check: "Each attempt has failure reason"
  how: "Not just 'tried X', but 'tried X, failed because Y'"

- id: hypothesis-provided
  check: "Clear hypothesis about why criterion may be problematic"
  how: "Escalation includes theory about root cause"

- id: not-lazy
  check: "Not a lazy 'help me' request"
  bad_patterns:
    - "I can't figure this out"
    - "Can you help?"
    - "This is hard"
  how: "Escalation is evidence-based, not complaint-based"
```

**Output**: Escalation quality score with specific gaps.

---

## escalation-counter-checker

**Purpose**: Verifies escalation counter tracked correctly.

**Context Files**:
- Session file

**Checks**:
```yaml
- id: counter-in-session
  check: "Escalation counts stored in session.escalation_counts"
  how: "Session JSON has escalation_counts object"

- id: increments-on-same
  check: "Counter increments on same-criterion failure"
  how: "Repeated failure on AC-N increases escalation_counts['AC-N']"

- id: resets-on-change
  check: "Counter resets when working on different criterion"
  how: "Switching to AC-M doesn't carry AC-N's count"

- id: resets-on-success
  check: "Counter resets on successful verification"
  how: "After AC-N passes, escalation_counts['AC-N'] goes to 0"

- id: threshold-configurable
  check: "Threshold respected (default 3)"
  how: "Escalation only allowed when count >= threshold"
```

**Output**: Counter tracking analysis.

---

## verification-completeness-checker

**Purpose**: Verifies /done runs all verifications.

**Context Files**:
- Spec file (list of all criteria)
- /done output

**Checks**:
```yaml
- id: all-criteria-attempted
  check: "Every criterion ID from spec has verification attempted"
  how: "Compare spec criteria list to /done results list - must match"

- id: none-skipped
  check: "No criteria skipped"
  how: "All criteria in spec appear in results, none missing"

- id: methods-correct
  check: "Verification methods match spec definitions"
  how: "Bash criteria ran bash, subagent criteria spawned subagent"
```

**Output**: Coverage report showing verified vs missing criteria.

---

## subagent-execution-checker

**Purpose**: Verifies subagent verifications executed correctly.

**Context Files**:
- /done execution transcript

**Checks**:
```yaml
- id: correct-agent
  check: "Subagent spawned matches spec definition"
  how: "Task tool call uses correct agent type"

- id: context-provided
  check: "Context files provided if specified in spec"
  how: "Task prompt includes context file contents"

- id: checks-passed
  check: "Checks list passed to subagent"
  how: "Subagent prompt includes specific checks to perform"

- id: results-returned
  check: "Subagent returns pass/fail per check"
  how: "Subagent output parsed into pass/fail"
```

**Output**: Subagent execution trace.

---

## manual-flag-checker

**Purpose**: Verifies manual criteria handled correctly.

**Context Files**:
- /done output

**Checks**:
```yaml
- id: marked-requires-human
  check: "Manual criteria have status 'requires-human'"
  how: "Status field is 'requires-human', not 'pass' or 'fail'"

- id: doesnt-block
  check: "Manual criteria don't fail automated verification"
  how: "all_automated_pass can be true with manual criteria present"

- id: listed-for-review
  check: "Manual criteria listed in output for human review"
  how: "Separate section showing what human should check"

- id: instructions-clear
  check: "Clear instructions for what human should verify"
  how: "Each manual criterion has human-readable verification steps"
```

**Output**: Manual criteria handling report.

---

## feedback-quality-checker

**Purpose**: Verifies failure feedback is specific and actionable.

**Context Files**:
- /done output with failures

**Checks**:
```yaml
- id: location-specific
  check: "Each failure has specific location"
  how: "File path, line number where applicable"

- id: expected-vs-actual
  check: "Explains expected vs actual"
  how: "Not just 'failed' but 'expected X, got Y'"

- id: references-examples
  check: "References accepted/rejected examples if available"
  how: "Points to spec examples to clarify expectation"

- id: actionable
  check: "Feedback is actionable"
  how: "Clear what needs to change, not vague 'fix this'"
```

**Output**: Feedback quality score per failure.

---

## resume-checker

**Purpose**: Verifies session can be resumed from file.

**Context Files**:
- Session file
- Resume attempt transcript

**Checks**:
```yaml
- id: state-complete
  check: "Session file contains all state needed"
  how: "All fields present: criteria status, escalation counts, verification history"

- id: can-read
  check: "Skill can read existing session and continue"
  how: "Providing session file as input resumes, doesn't restart"

- id: no-duplicate-work
  check: "Verified criteria not re-verified"
  how: "Resume focuses on unverified/failed, not all"

- id: counts-preserved
  check: "Escalation counts preserved"
  how: "Resume has correct escalation_counts from session"
```

**Output**: Resume capability assessment.

---

## cleanup-checker

**Purpose**: Verifies session cleanup on completion.

**Context Files**:
- Post-completion filesystem state

**Checks**:
```yaml
- id: completion-triggers
  check: "Completion triggers cleanup option"
  how: "After all pass, cleanup logic runs"

- id: archive-or-delete
  check: "Files archived or deleted based on config"
  how: "Session files moved to logs/ or removed"

- id: commits-preserved
  check: "Git commits made during implementation preserved"
  how: "Git history shows implementation commits"
```

**Output**: Cleanup behavior report.

---

## git-pattern-checker

**Purpose**: Verifies git commits are incremental and descriptive.

**Context Files**:
- Git log from implementation session

**Checks**:
```yaml
- id: incremental-commits
  check: "Multiple commits during implementation"
  how: "Git log shows multiple commits, not one at end"

- id: references-criteria
  check: "Commit messages reference criteria"
  how: "Messages mention AC-N or criterion descriptions"

- id: no-huge-commits
  check: "No single commit with all changes"
  how: "Largest commit is reasonable size, not entire implementation"
```

**Output**: Git pattern analysis.

---

## verifier-meta

**Purpose**: Master verifier for implement skill - orchestrates all checks.

**Process**:
```yaml
1. Run input-handler-checker
2. Run spec-parser-checker
3. Run execution-pattern-checker
4. Run todo-pattern-checker
5. Run transcript-analyzer
6. Run loop-behavior-checker
7. Run escalation-checker (if escalations present)
8. Run verification-completeness-checker
9. Run feedback-quality-checker
10. Aggregate results
11. Report gaps
12. Determine pass/fail
```

**Output**:
```yaml
status: pass | fail
summary:
  passed: [list]
  failed: [list with details]
gaps:
  - description: "..."
    severity: critical | important | minor
    recommendation: "..."
```
