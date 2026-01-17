# Subagent Definitions for Spec Skill Verification

These subagents verify the acceptance criteria for the redesigned /spec skill.

---

## interview-quality-reviewer

**Purpose**: Reviews interview transcript to verify LLM was proactive, not reactive.

**Context Files**:
- Interview transcript/log file

**Checks**:
```yaml
- id: proactive-questions
  check: "LLM asks questions before user volunteers information"
  how: "Count questions asked vs information user provided unprompted. Ratio should favor LLM questions."

- id: surfaces-edge-cases
  check: "LLM surfaces edge cases user didn't mention"
  how: "Identify edge cases in final spec. Trace which were LLM-initiated vs user-initiated. LLM should initiate majority."

- id: proposes-criteria
  check: "LLM proposes criteria based on codebase exploration"
  how: "Criteria linked to codebase findings should exist. LLM should say 'Based on exploring X, I recommend Y.'"

- id: not-reactive
  check: "Interview is not just reactive Q&A"
  how: "LLM should make statements, propose things, push back - not just ask and record."
```

**Output**: Pass/Fail with specific examples of proactive vs reactive behavior.

---

## interview-format-checker

**Purpose**: Validates AskUserQuestion calls follow proper format.

**Context Files**:
- Interview transcript showing tool calls

**Checks**:
```yaml
- id: options-present
  check: "Every question has 2-4 options"
  how: "Parse AskUserQuestion calls, verify options array has 2-4 items"

- id: recommendation-present
  check: "First option marked as recommended OR explicit rationale for no recommendation"
  how: "Check first option label contains '(Recommended)' or question context explains why no recommendation"

- id: descriptions-present
  check: "Options have descriptions explaining tradeoffs"
  how: "Each option has non-empty description field"

- id: no-naked-open-ended
  check: "No open-ended questions without options (unless explicitly justified)"
  how: "Free-text questions should be rare and justified (e.g., 'What name do you want?')"
```

**Output**: List of compliant/non-compliant questions with details.

---

## interview-technique-checker

**Purpose**: Verifies all required interview techniques were used.

**Context Files**:
- Interview transcript

**Checks**:
```yaml
- id: adversarial-examples-used
  check: "At least 2 synthetic examples generated and user asked to accept/reject"
  how: "Find instances of 'Would you accept this?' or similar with code/behavior examples"

- id: contrast-pairs-used
  check: "At least 1 contrast pair presented"
  how: "Find instances of 'Approach A vs Approach B' or 'Option 1 vs Option 2' comparisons"

- id: premortem-asked
  check: "Pre-mortem question asked"
  how: "Find question about imagining failure/disaster"

- id: disappointed-asked
  check: "Disappointed question asked and repeated"
  how: "Find question about 'criteria pass but disappointed' - should appear at least once"

- id: persona-simulation-asked
  check: "Persona simulation question asked"
  how: "Find question about 'what would [person] critique'"
```

**Output**: Checklist of techniques used/not used with transcript references.

---

## criteria-coverage-checker

**Purpose**: Ensures criteria cover all required categories.

**Context Files**:
- Final spec output

**Checks**:
```yaml
- id: feature-behavior-present
  check: "Feature behavior criteria present"
  how: "Criteria with category 'feature' or describing what the thing does"

- id: code-quality-present
  check: "Code quality criteria present"
  how: "Criteria about code structure, patterns, readability, naming"

- id: architecture-present
  check: "Architecture/location criteria present"
  how: "Criteria about where code lives, what it touches, boundaries"

- id: rejection-criteria-present
  check: "Explicit rejection criteria section with at least 3 items"
  how: "Section titled 'Rejection Criteria' with concrete items"

- id: criteria-specific
  check: "Each criterion is specific (not vague)"
  how: "No criteria with only vague terms like 'good', 'clean', 'proper' without definition"
```

**Output**: Coverage report by category with gaps identified.

---

## criteria-specificity-checker

**Purpose**: Ensures no vague, unverifiable criteria.

**Context Files**:
- Final spec output

**Checks**:
```yaml
- id: no-vague-terms
  check: "No criteria contain undefined vague terms"
  terms_to_flag:
    - "clean" (unless defined)
    - "good" (unless defined)
    - "proper" (unless defined)
    - "appropriate" (unless defined)
    - "reasonable" (unless defined)
    - "well-organized" (unless defined)
  how: "Grep for terms, check if followed by specific definition"

- id: true-false-verifiable
  check: "Each criterion can be checked as true/false"
  how: "For each criterion, can you answer 'Is this satisfied? Yes/No' without ambiguity?"

- id: numeric-where-applicable
  check: "Numeric thresholds where applicable"
  how: "Size/count criteria should have numbers, not 'small', 'few', 'many'"
```

**Output**: List of vague criteria with suggestions for making specific.

---

## edge-case-analyzer

**Purpose**: Verifies edge cases were systematically explored.

**Context Files**:
- Interview transcript
- Final spec output

**Checks**:
```yaml
- id: multiple-edge-cases-asked
  check: "Multiple edge case questions asked during interview"
  how: "Count questions about 'what if', edge cases, boundaries"

- id: standard-edges-covered
  check: "Standard edge cases addressed"
  categories:
    - "Empty/null input"
    - "Large/max input"
    - "Invalid input"
    - "Concurrent access (if applicable)"
    - "Failure/error conditions"
    - "Boundary values"
  how: "Check if each category addressed in criteria or marked out-of-scope"

- id: user-confirmed-complete
  check: "Interview continued until user indicated completeness"
  how: "Find user statement like 'I think we covered it' or similar"
```

**Output**: Edge case coverage matrix with gaps.

---

## conflict-detector

**Purpose**: Identifies conflicting criteria.

**Context Files**:
- Final spec output

**Checks**:
```yaml
- id: no-contradictions
  check: "No two criteria contradict each other"
  how: "For each criterion pair, check if satisfying A makes B impossible"
  examples:
    - "'Must be fast' vs 'Must validate exhaustively'" (potential conflict)
    - "'No external dependencies' vs 'Must send emails'" (conflict)

- id: no-impossible-combinations
  check: "No criterion makes another impossible"
  how: "Transitive check - A requires X, B forbids X"

- id: tradeoffs-resolved
  check: "Tradeoffs explicitly resolved"
  how: "If criteria have tension, resolution should be documented (priority, context-dependent, etc.)"
```

**Output**: List of potential conflicts with resolution status.

---

## example-coverage-checker

**Purpose**: Verifies accepted/rejected examples are present and concrete.

**Context Files**:
- Final spec output

**Checks**:
```yaml
- id: accepted-examples-present
  check: "At least 2 accepted examples present"
  how: "Find examples marked as accepted/good/correct"

- id: rejected-examples-present
  check: "At least 2 rejected examples present"
  how: "Find examples marked as rejected/bad/incorrect"

- id: examples-concrete
  check: "Examples are concrete code/behavior, not abstract descriptions"
  how: "Examples should contain actual code, commands, or specific behavior - not 'the code should be clean'"

- id: examples-linked
  check: "Examples linked to relevant criteria"
  how: "Each example references which criterion it demonstrates"
```

**Output**: Example inventory with concreteness assessment.

---

## premortem-checker

**Purpose**: Verifies pre-mortem risks documented with preventive criteria.

**Context Files**:
- Final spec output

**Checks**:
```yaml
- id: section-exists
  check: "Pre-mortem section exists"
  how: "Find section titled 'Pre-mortem' or 'Risks'"

- id: risks-have-criteria
  check: "Each risk has linked preventive criterion"
  how: "Each risk row/item references a criterion ID"

- id: no-orphan-risks
  check: "No risks without prevention"
  how: "Every risk has corresponding criterion that addresses it"
```

**Output**: Risk-to-criterion mapping with orphans flagged.

---

## disappointed-checker

**Purpose**: Verifies disappointed scenarios documented with criteria.

**Context Files**:
- Final spec output

**Checks**:
```yaml
- id: section-exists
  check: "Disappointed scenarios section exists"
  how: "Find section about disappointment scenarios"

- id: scenarios-have-criteria
  check: "Each scenario has linked criterion"
  how: "Each scenario references a criterion that prevents it"
```

**Output**: Scenario-to-criterion mapping.

---

## subagent-definition-checker

**Purpose**: Verifies task-specific subagents are well-defined.

**Context Files**:
- Final spec output (subagents section)

**Checks**:
```yaml
- id: clear-purpose
  check: "Each subagent has clear purpose statement"
  how: "Purpose field is specific, not generic"

- id: specific-checks
  check: "Each subagent has specific checks listed"
  how: "Checks are concrete actions, not vague ('verify quality')"

- id: context-files-where-needed
  check: "Subagents reference context files where needed"
  how: "If check requires codebase knowledge, context_files specified"

- id: no-vague-definitions
  check: "No vague subagent definitions"
  bad_examples:
    - "check if good"
    - "verify quality"
    - "make sure it's correct"
  how: "Grep for vague terms in check descriptions"
```

**Output**: Subagent quality assessment.

---

## meta-verifier

**Purpose**: Master verifier that orchestrates all checks and reports overall status.

**Context Files**:
- Interview transcript
- Final spec output
- All other subagent reports

**Process**:
```yaml
1. Run interview-quality-reviewer
2. Run interview-format-checker
3. Run interview-technique-checker
4. Run criteria-coverage-checker
5. Run criteria-specificity-checker
6. Run edge-case-analyzer
7. Run conflict-detector
8. Run example-coverage-checker
9. Run premortem-checker
10. Run disappointed-checker
11. Run subagent-definition-checker
12. Aggregate results
13. Report gaps
14. Determine pass/fail
```

**Output**:
```yaml
status: pass | fail
summary:
  passed: [list of passed checks]
  failed: [list of failed checks with details]
gaps:
  - description: "Missing X"
    severity: critical | important | minor
    recommendation: "Add Y during interview"
```

---

## ux-reviewer

**Purpose**: Reviews interview experience for user-friendliness.

**Context Files**:
- Interview transcript

**Checks**:
```yaml
- id: questions-batched
  check: "Related questions batched together"
  how: "Questions about same topic appear together, not scattered"

- id: context-provided
  check: "Context provided for why questions matter"
  how: "LLM explains relevance before asking"

- id: recommendations-reduce-load
  check: "Recommendations reduce cognitive load"
  how: "User can accept defaults and get good result"

- id: logical-flow
  check: "Interview has logical flow"
  how: "Topics progress naturally, no random jumping"
  sequence: "Task understanding → Feature → Quality → Architecture → Edge cases → Verification"
```

**Output**: UX assessment with flow diagram.

---

## interview-flow-analyzer

**Purpose**: Analyzes interview structure and flow.

**Context Files**:
- Interview transcript

**Checks**:
```yaml
- id: exploration-interlaced
  check: "Codebase exploration happens during interview, not just upfront"
  how: "Exploration tasks launched after interview starts, in response to answers"

- id: exploration-informs-questions
  check: "Exploration findings lead to follow-up questions"
  how: "Questions reference 'Based on exploring X...'"

- id: meta-verification-before-finalize
  check: "Meta-verification runs before final output"
  how: "Meta-verifier invoked, results processed"

- id: gaps-trigger-continuation
  check: "Failed meta-verification leads to more questions"
  how: "If meta-verifier finds gaps, interview continues"
```

**Output**: Flow analysis with timeline.
