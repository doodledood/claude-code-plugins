# Acceptance Criteria Spec: Verification-First /spec Skill Redesign

Generated: 2026-01-16
Status: Draft for review

## Overview

### Problem Statement
Current `/spec` skill produces requirements documents that lack verification methods, leading to ambiguity about when work is "done." The gap between "what was specified" and "what was actually wanted" causes rework and iteration during implementation.

### Solution
Redesign `/spec` to be verification-first: every criterion must have an explicit verification method, and the interview process must be exhaustive enough to surface tacit knowledge before implementation begins.

### Success Measure
User can run `/spec`, complete the interview, go to sleep, and wake up to implementation that requires only minor tweaks - not major rework.

---

## Acceptance Criteria

### Category: Interview Process

#### AC-1: LLM-Driven Proactive Interview
**Description**: The LLM drives the interview proactively, surfacing questions the user wouldn't think to ask. User should not have to proactively think of all acceptance criteria.

**Verification**:
```yaml
method: subagent
agent: interview-quality-reviewer
checks:
  - "LLM asks questions before user volunteers information"
  - "LLM surfaces edge cases user didn't mention"
  - "LLM proposes criteria based on codebase exploration"
  - "Interview is not just reactive Q&A"
```

#### AC-2: Recommended Options Always Provided
**Description**: Every AskUserQuestion call includes a recommended option with rationale.

**Verification**:
```yaml
method: subagent
agent: interview-format-checker
checks:
  - "Every question has 2-4 options"
  - "First option marked as recommended OR explicit rationale for no recommendation"
  - "Options have descriptions explaining tradeoffs"
  - "No open-ended questions without options (unless explicitly needed)"
```

#### AC-3: Codebase Exploration Interlaced
**Description**: Codebase exploration happens AS NEEDED during interview, not as separate upfront phase. Findings inform questions and criteria.

**Verification**:
```yaml
method: subagent
agent: interview-flow-analyzer
checks:
  - "Exploration tasks launched in response to user answers"
  - "Exploration findings lead to follow-up questions"
  - "Existing patterns discovered become criteria or reference examples"
  - "Not all exploration happens at start"
```

#### AC-4: Positive Criteria Gathered
**Description**: Interview covers what must be true when work is complete - feature behavior, quality standards, architecture fit.

**Verification**:
```yaml
method: subagent
agent: criteria-coverage-checker
checks:
  - "Feature behavior criteria present"
  - "Code quality criteria present"
  - "Architecture/location criteria present"
  - "Each criterion is specific (not vague)"
```

#### AC-5: Negative Criteria Gathered (Rejection-First)
**Description**: Interview explicitly asks what would cause PR rejection. Surfaces implicit standards.

**Verification**:
```yaml
method: subagent
agent: criteria-coverage-checker
checks:
  - "Explicit 'rejection criteria' section in output"
  - "At least 3 rejection criteria captured"
  - "Rejection criteria are distinct from inverted positive criteria"
```

#### AC-6: Exhaustive Edge Cases
**Description**: Interview systematically walks through edge cases until no new criteria emerge.

**Verification**:
```yaml
method: subagent
agent: edge-case-analyzer
checks:
  - "Multiple edge case questions asked"
  - "Edge cases cover: empty input, null, large input, concurrent access, failure modes"
  - "Interview continues until user says 'I think we covered it'"
  - "Each edge case has corresponding criterion or explicit 'out of scope'"
```

#### AC-7: Adversarial Examples
**Description**: LLM generates synthetic implementations and asks user to accept/reject, surfacing tacit preferences.

**Verification**:
```yaml
method: subagent
agent: interview-technique-checker
checks:
  - "At least 2 synthetic examples generated during interview"
  - "User asked 'would you accept this?'"
  - "Rejection reasons captured as criteria"
  - "Accepted examples stored as reference for verification"
```

#### AC-8: Contrast Pairs
**Description**: LLM presents alternative approaches and asks user to choose, with reasoning becoming criteria.

**Verification**:
```yaml
method: subagent
agent: interview-technique-checker
checks:
  - "At least 1 contrast pair presented"
  - "User's preference captured"
  - "User's reasoning ('why') captured as criterion"
```

#### AC-9: Pre-mortem Question
**Description**: Interview asks user to imagine failure: "This shipped and it was a disaster. What went wrong?"

**Verification**:
```yaml
method: subagent
agent: interview-technique-checker
checks:
  - "Pre-mortem question asked"
  - "At least 2 risks identified"
  - "Each risk has corresponding preventive criterion"
```

#### AC-10: Disappointed Question
**Description**: Interview asks: "All criteria pass but you're disappointed. What would cause that?"

**Verification**:
```yaml
method: subagent
agent: interview-technique-checker
checks:
  - "Disappointed question asked"
  - "Responses captured"
  - "Each disappointment scenario has corresponding criterion"
  - "Question repeated until user can't think of more"
```

#### AC-11: Persona Simulation
**Description**: Interview asks: "If [respected dev] reviewed this, what would they critique?"

**Verification**:
```yaml
method: subagent
agent: interview-technique-checker
checks:
  - "Persona simulation question asked"
  - "User identifies a persona (real or archetype)"
  - "Critiques captured as criteria"
```

#### AC-12: Progressive Concreteness
**Description**: Vague criteria are refined through follow-up until they're specific and verifiable.

**Verification**:
```yaml
method: subagent
agent: criteria-specificity-checker
checks:
  - "No criteria contain vague terms: 'clean', 'good', 'proper', 'appropriate' without definition"
  - "Each criterion can be checked as true/false"
  - "Numeric thresholds where applicable (e.g., 'functions under 30 lines' not 'small functions')"
```

---

### Category: Output Artifact

#### AC-13: Structured Format
**Description**: Output follows consistent, parseable structure with all required sections.

**Verification**:
```yaml
method: bash
command: "python scripts/validate_spec_structure.py $SPEC_FILE"
pass_condition: "exit code 0"
checks:
  - "Has overview section"
  - "Has criteria section with IDs"
  - "Has verification methods section"
  - "Has examples section"
  - "Has pre-mortem risks section"
  - "Has rejected patterns section"
```

#### AC-14: Every Criterion Has Verification Method
**Description**: No criterion exists without an explicit verification method (bash, subagent, or manual with flag).

**Verification**:
```yaml
method: bash
command: "python scripts/check_criteria_verification.py $SPEC_FILE"
pass_condition: "All criteria have verification methods"
```

#### AC-15: No Unresolved Conflicts
**Description**: Spec contains no conflicting criteria. Any tensions surfaced during interview must be resolved.

**Verification**:
```yaml
method: subagent
agent: conflict-detector
checks:
  - "No two criteria contradict each other"
  - "No criterion makes another impossible"
  - "Tradeoffs explicitly resolved (not left open)"
```

#### AC-16: No Placeholders
**Description**: Spec contains no TBD, TODO, "figure out later", or vague language.

**Verification**:
```yaml
method: bash
command: |
  ! grep -iE '(TBD|TODO|figure out|later|maybe|probably|might|unclear)' $SPEC_FILE
pass_condition: "exit code 0 (no matches)"
```

#### AC-17: Examples Included
**Description**: Spec includes accepted and rejected examples from adversarial interview as reference for verification.

**Verification**:
```yaml
method: subagent
agent: example-coverage-checker
checks:
  - "At least 2 accepted examples present"
  - "At least 2 rejected examples present"
  - "Examples are concrete (actual code/behavior, not abstract)"
  - "Examples linked to relevant criteria"
```

#### AC-18: Pre-mortem Risks Documented
**Description**: Risks from pre-mortem are documented with corresponding preventive criteria.

**Verification**:
```yaml
method: subagent
agent: premortem-checker
checks:
  - "Pre-mortem section exists"
  - "Each risk has linked criterion"
  - "No orphan risks (risk without prevention)"
```

#### AC-19: Disappointed Scenarios Documented
**Description**: Scenarios from disappointed question are documented with corresponding criteria.

**Verification**:
```yaml
method: subagent
agent: disappointed-checker
checks:
  - "Disappointed scenarios section exists"
  - "Each scenario has linked criterion"
```

#### AC-20: Task-Specific Subagents Defined
**Description**: Where generic verification isn't sufficient, task-specific subagents are defined with clear checks.

**Verification**:
```yaml
method: subagent
agent: subagent-definition-checker
checks:
  - "Task-specific subagents have clear purpose"
  - "Each subagent has specific checks listed"
  - "Subagents reference context files where needed"
  - "No vague subagent definitions ('check if good')"
```

---

### Category: Meta-Verification

#### AC-21: Meta-Verification Runs
**Description**: After spec is drafted, meta-verification subagent reviews for completeness and quality.

**Verification**:
```yaml
method: subagent
agent: meta-verifier
checks:
  - "All AC-13 through AC-20 pass"
  - "Interview covered all required techniques (AC-1 through AC-12)"
  - "No gaps identified"
```

#### AC-22: Gaps Trigger Continuation
**Description**: If meta-verification finds gaps, interview continues to fill them. Spec not finalized until meta-verification passes.

**Verification**:
```yaml
method: subagent
agent: interview-flow-analyzer
checks:
  - "Meta-verification runs before finalizing"
  - "Failed meta-verification leads to more questions"
  - "Final output only produced after meta-verification passes"
```

---

### Category: Integration

#### AC-23: Works With Implementation Phase
**Description**: Output format is consumable by implementation phase. Criteria and verification methods can be executed.

**Verification**:
```yaml
method: bash
command: "python scripts/validate_spec_executable.py $SPEC_FILE"
pass_condition: "All verification methods are executable"
checks:
  - "Bash commands are valid"
  - "Subagent references are resolvable"
  - "Manual verifications are flagged"
```

#### AC-24: Supports Escalation
**Description**: Spec format supports implementation escalation - criteria can be amended if implementation reveals genuine gaps.

**Verification**:
```yaml
method: subagent
agent: spec-format-checker
checks:
  - "Criteria have unique IDs for reference"
  - "Format supports adding new criteria"
  - "Format supports amending existing criteria"
  - "Amendment history can be tracked"
```

---

### Category: User Experience

#### AC-25: Interview Doesn't Feel Like Interrogation
**Description**: Despite thoroughness, interview feels collaborative, not exhausting. Batches related questions, provides context.

**Verification**:
```yaml
method: subagent
agent: ux-reviewer
checks:
  - "Related questions batched (not one at a time)"
  - "Context provided for why questions matter"
  - "Recommendations reduce cognitive load"
  - "Interview has logical flow (not random jumping)"
```

#### AC-26: Progress Visible
**Description**: User can see interview progress - what's been covered, what's remaining.

**Verification**:
```yaml
method: subagent
agent: ux-reviewer
checks:
  - "Todo list tracks interview phases"
  - "Completed areas visible"
  - "Remaining areas visible"
```

#### AC-27: Resumable
**Description**: If interview is interrupted, it can be resumed from where it left off.

**Verification**:
```yaml
method: subagent
agent: interview-flow-analyzer
checks:
  - "Interview state saved to file"
  - "Resume instructions in skill"
  - "Partial spec preserved on interruption"
```

---

## Rejection Criteria

The PR will be REJECTED if:

1. **Interview is reactive**: LLM waits for user to provide all information instead of proactively probing
2. **Vague criteria accepted**: Output contains criteria that can't be verified as true/false
3. **Missing verification methods**: Any criterion lacks explicit verification
4. **Skipped interview techniques**: Pre-mortem, disappointed question, or adversarial examples not used
5. **No meta-verification**: Spec finalized without meta-verification pass
6. **Examples are abstract**: Accepted/rejected examples are descriptions, not concrete code/behavior
7. **Conflicts unresolved**: Spec contains criteria that contradict each other
8. **Placeholders remain**: TBD, TODO, or "figure out later" in final output

---

## Examples

### Accepted Example: Criterion with Verification

```yaml
- id: error-handling-uses-app-error
  description: "All errors thrown use AppError class with correlationId"
  category: code-quality
  verify:
    method: subagent
    agent: pattern-checker
    context_files:
      - "src/utils/errors.ts"
    checks:
      - "New throw statements use AppError"
      - "AppError includes correlationId field"
      - "No raw Error() throws"
    reference:
      accepted: |
        throw new AppError({
          message: "Failed to process",
          correlationId: ctx.correlationId,
          cause: originalError
        });
      rejected: |
        throw new Error(`[${correlationId}] Failed to process`);
```

### Rejected Example: Vague Criterion

```yaml
# BAD - would be rejected
- id: code-quality
  description: "Code should be clean and well-organized"
  verify:
    method: subagent
    agent: code-reviewer
    checks:
      - "Code is good"  # Too vague
```

### Accepted Example: Interview Question with Recommendation

```
questions: [
  {
    question: "How should the notification system handle delivery failures?",
    header: "Failure Handling",
    options: [
      {
        label: "Retry with exponential backoff (Recommended)",
        description: "3 retries, 1s/2s/4s delays. Matches existing patterns in src/queue/"
      },
      {
        label: "Dead letter queue",
        description: "Failed notifications stored for manual review. More complex."
      },
      {
        label: "Silent drop",
        description: "Log and continue. Simplest but notifications may be lost."
      }
    ],
    multiSelect: false
  }
]
```

### Rejected Example: Open-Ended Question

```
# BAD - would be rejected
"What should happen when delivery fails?"
# No options, no recommendation, requires user to think of everything
```

---

## Pre-mortem Risks

| Risk | Preventive Criterion |
|------|---------------------|
| Interview takes too long, user abandons | AC-25 (batching, recommendations reduce fatigue) |
| LLM misses important area | AC-21 (meta-verification catches gaps) |
| Criteria look complete but are actually vague | AC-12 (progressive concreteness), AC-16 (no placeholders) |
| User accepts spec but didn't really engage | AC-7, AC-8 (adversarial examples force engagement) |
| Implementation can't execute verification | AC-23 (validation script checks executability) |
| Spec too rigid, can't handle implementation surprises | AC-24 (supports amendment) |

---

## Disappointed Scenarios

| Scenario | Preventive Criterion |
|----------|---------------------|
| "Interview felt like a checklist, not a conversation" | AC-25 (collaborative feel, logical flow) |
| "I answered questions but LLM didn't probe deeper" | AC-1 (proactive), AC-12 (progressive concreteness) |
| "Spec looks thorough but I still don't know if I'd accept the output" | AC-7, AC-8 (adversarial examples make acceptance concrete) |
| "I can't tell what's most important" | Criteria should have priority/category |
| "The verification methods seem made up" | AC-23 (validation of executability) |

---

## Verification Infrastructure Required

### Scripts

#### `scripts/validate_spec_structure.py`
Validates spec YAML/MD structure has required sections.

#### `scripts/check_criteria_verification.py`
Ensures every criterion has a verification block.

#### `scripts/validate_spec_executable.py`
Checks that bash commands are valid, subagent references exist.

### Subagents

#### `interview-quality-reviewer`
Reviews interview transcript for proactive LLM behavior, thoroughness.

#### `interview-format-checker`
Checks AskUserQuestion calls have proper format (options, recommendations).

#### `interview-technique-checker`
Verifies all required techniques used (pre-mortem, disappointed, adversarial examples, etc.).

#### `criteria-coverage-checker`
Checks criteria cover feature, quality, architecture categories.

#### `criteria-specificity-checker`
Ensures no vague criteria, all are true/false verifiable.

#### `conflict-detector`
Analyzes criteria pairs for contradictions.

#### `example-coverage-checker`
Verifies accepted/rejected examples present and concrete.

#### `meta-verifier`
Master verifier that runs all other checks, reports gaps.

#### `ux-reviewer`
Reviews interview experience: batching, flow, cognitive load.

---

## Out of Scope

- Implementation phase changes (separate spec)
- Subagent implementation details (separate task)
- UI/rendering of spec output
- Integration with external tools

---

## Open Questions

None - all resolved during design conversation.

---

## Appendix: Fixed Meta-Criteria

These are the criteria that apply to ALL specs produced by this skill:

1. Every criterion has verification method
2. No unresolved conflicts
3. No placeholders (TBD, TODO, etc.)
4. Comprehensive coverage (feature, quality, architecture)
5. Rejection criteria included
6. Verification methods are concrete and executable
7. Examples included (accepted and rejected)
8. Pre-mortem risks documented with preventive criteria
9. Disappointed scenarios documented with preventive criteria
