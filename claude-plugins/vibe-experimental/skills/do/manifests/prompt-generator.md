# Definition: Prompt Generator

## 1. Intent & Context

- **Goal:** Produce a prompt-specific manifest (M2) that, when executed via `/do`, creates or updates LLM prompts with verification-first methodology. Replaces ad-hoc prompt writing with define→do→verify rigor.
- **Mental Model:** Prompts are manifests — clear goal, clear constraints, freedom in execution. Define what the prompt must achieve *before* writing it. The prompt-engineering skill's principles become verifiable invariants in M2, not aspirational guidelines. Discovery depth determines prompt quality — every requirement surfaced now prevents a prompt failure later.

**Reference artifact:** `claude-plugins/prompt-engineering/skills/prompt-engineering/SKILL.md` — source of truth for principles, anti-patterns, validation checklist, and structure templates.

## 2. Approach

### Architecture

Two-phase pipeline: **Discovery → Synthesis**

**Phase 1 — Context Discovery (D1):** Full interview with the user covering domain knowledge, user types, success criteria, edge cases, constraints, and integration context. If updating an existing prompt, analyze it against the anti-patterns table first. All findings logged to discovery file. This phase mirrors the prompt-engineering skill's Context Discovery section but produces structured findings rather than jumping to writing.

**Phase 2 — Manifest Synthesis (D2):** Read the full discovery log, then produce M2 — a `/do`-executable manifest where each prompt is a deliverable with specific ACs derived from discovery, and prompt-engineering principles are Global Invariants verified by the `prompt-reviewer` agent.

### Execution Order

- D1 → D2
- Rationale: D2 depends entirely on D1's output. Context discovery must complete before synthesis.

### Risk Areas

- [R-1] Discovery too shallow — M2 ACs use vague language ("good", "clear", "appropriate") instead of specific criteria | Detect: ACs contain adjectives without measurable meaning
- [R-4] Bad assumptions encoded — constraints inferred during interview but not confirmed with user before encoding in M2 | Detect: M2 contains constraints not traceable to explicit user statements or confirmed inferences

### Trade-offs

- [T-1] Discovery thoroughness vs interview fatigue → Prefer thoroughness. Every requirement discovered now is one fewer prompt failure later. User can signal "enough" to override.
- [T-2] M2 specificity vs generality → Prefer specificity. M2 is one-time, tailored to exact prompt needs. Generic ACs produce generic prompts.

## 3. Global Invariants (The Constitution)

- [INV-G1] M2 follows `/define` manifest schema and is executable by `/do` — includes Intent, Deliverables with ACs, Global Invariants, and verification methods | Verify:
  ```yaml
  verify:
    method: subagent
    agent: manifest-verifier
    prompt: "Manifest: {m2_path} | Log: {discovery_log_path}"
  ```

- [INV-G2] Every user-stated constraint from D1 interview is encoded in M2 as INV, AC, or PG — no lost requirements | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Compare discovery log at {discovery_log_path} against manifest at {m2_path}. List any user-stated constraints, preferences, or requirements in the log that have no corresponding INV, AC, or PG in the manifest. If all are encoded, output PASS."
  ```

- [INV-G3] M2 ACs are specific and measurable — two reviewers would agree on pass/fail for each | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review manifest at {m2_path}. Flag any AC that uses vague adjectives (good, clear, appropriate, proper, well-structured, correct) without defining what qualifies. Every AC must be specific enough that two independent reviewers would agree on pass/fail."
  ```

- [INV-G4] M2 encodes prompt-engineering principles as verifiable Global Invariants — both the validation checklist (goals not steps, no arbitrary values, direct imperatives, critical rules prominent, complexity matches task, information density, memento if multi-phase) and anti-pattern prohibitions (no prescriptive HOW, no arbitrary limits, no capability instructions, no rigid checklists, no weak language, no buried critical info, no over-engineering). Each verified by `prompt-reviewer` agent. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read manifest at {m2_path}. Verify it has Global Invariants covering ALL of: (1) goals stated not steps prescribed, (2) no arbitrary values, (3) direct imperatives, (4) critical rules prominent, (5) complexity matches task, (6) information density maximized, (7) memento if multi-phase, (8) no prescriptive HOW steps, (9) no capability instructions, (10) no rigid checklists, (11) no buried critical info, (12) no over-engineering. Each must use prompt-reviewer agent for verification. List any missing."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Begin D1 by asking the user: "What prompt(s) would you like to create or update? Describe the goal and any context." Then drive discovery using the prompt-engineering skill's interview method: generate concrete candidates with recommended options, use outside view ("what typically fails in prompts like this?"), run pre-mortem ("if this prompt failed in production, what would cause it?"), encode explicit statements immediately.
- [PG-2] Context discovery covers all 6 types from the prompt-engineering skill: domain knowledge, user types, success criteria, edge cases, constraints, integration context. Surface each through targeted questions, not open-ended probing.
- [PG-3] Determine prompt type and format early in interview. Common types in the plugin ecosystem include Skills (SKILL.md with frontmatter), Agents (agent .md with tools/model frontmatter), and System instructions (Role/Approach/Constraints/Output) — but prompts can be anything: API system prompts, chat templates, tool descriptions, evaluation rubrics, etc. Discover the format requirements from the user. Confirm with user.
- [PG-4] Ask user for target file path(s) for prompt output. Don't assume standard paths.
- [PG-5] For update flows: read existing prompt first, analyze against the 7 anti-patterns (prescriptive HOW, arbitrary limits, capability instructions, rigid checklists, weak language, buried critical info, over-engineering). Surface findings to user: "I found these issues: [list]. Should I encode fixes for these in the manifest?"
- [PG-6] Confirm inferred constraints before encoding: "I'm inferring X — should this be a hard constraint?" Discovered ≠ confirmed. Ambiguous scope: list in/out assumptions and confirm.
- [PG-7] For batch prompts (multiple prompts in one run): identify relationships between prompts (shared principles, invocation chains, common domain). Encode as shared INVs in M2. Each prompt is a separate deliverable in M2.

## 5. Known Assumptions

- [ASM-1] `prompt-reviewer` agent exists in prompt-engineering plugin and is available for M2 verification | Default: available at `claude-plugins/prompt-engineering/agents/prompt-reviewer.md` | Impact if wrong: M2 verification must fall back to general-purpose subagent with opus model and explicit prompt-engineering principles in the prompt
- [ASM-2] User will specify target file path(s) during interview — no assumed directory structure | Default: ask during D1 (covered by PG-4) | Impact if wrong: none, path is always confirmed

## 6. Deliverables (The Work)

### Deliverable 1: Context Discovery

Interview user and explore codebase to surface all requirements for the prompt(s) being built or updated. Output: discovery log capturing all findings.

**Acceptance Criteria:**

- [AC-1.1] User's prompt goal captured — what to create or update and why | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read discovery log at {discovery_log_path}. Confirm it records a clear prompt goal (what to create/update and why) attributed to the user."
  ```

- [AC-1.2] Prompt type and format determined and confirmed with user — includes structure requirements, frontmatter needs (if any), and output format conventions | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read discovery log at {discovery_log_path}. Confirm it records a prompt type/format with explicit user confirmation, including any structural requirements (frontmatter, sections, format conventions)."
  ```

- [AC-1.3] All 6 context types covered with substantive findings: domain knowledge, user types, success criteria, edge cases, constraints, integration context | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read discovery log at {discovery_log_path}. For each of these 6 context types, confirm the log contains substantive findings (not just 'N/A' or placeholder): (1) domain knowledge, (2) user types, (3) success criteria, (4) edge cases, (5) constraints, (6) integration context. List any missing or superficial."
  ```

- [AC-1.4] Pre-mortem completed with specific failure modes identified | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read discovery log at {discovery_log_path}. Confirm it includes a pre-mortem section with specific failure modes (not generic 'could fail' or 'might not work')."
  ```

- [AC-1.5] Target file path(s) for prompt output recorded | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read discovery log at {discovery_log_path}. Confirm it records specific file path(s) where prompt(s) will be written or updated."
  ```

- [AC-1.6] If updating: existing prompt analyzed against anti-patterns with findings logged. If creating: this AC passes automatically. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read discovery log at {discovery_log_path}. If this is an update flow (existing prompt path referenced), confirm the log includes analysis against these anti-patterns: prescriptive HOW, arbitrary limits, capability instructions, rigid checklists, weak language, buried critical info, over-engineering. If create flow (no existing prompt), output PASS."
  ```

- [AC-1.7] Discovery log written to `/tmp/define-discovery-{timestamp}.md` and contains substantive content | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -s {discovery_log_path} && wc -l < {discovery_log_path} | awk '{if ($1 > 10) print \"PASS\"; else print \"FAIL: log too short\"}'"
  ```

### Deliverable 2: Manifest Synthesis (M2)

Read full discovery log, then produce M2 — a prompt-specific manifest executable by `/do`. Each prompt becomes a deliverable with ACs derived from discovery. Prompt-engineering principles become Global Invariants verified by `prompt-reviewer`.

**Acceptance Criteria:**

- [AC-2.1] Full discovery log read before synthesis (refresh step — restores context) | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read M2 at {m2_path} and discovery log at {discovery_log_path}. Verify M2's deliverable ACs reference specific findings from the discovery log — not generic prompt-engineering advice. If ACs could have been written without the discovery log, output FAIL."
  ```

- [AC-2.2] One deliverable per prompt file, with target path specified in each | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read M2 at {m2_path}. Confirm each deliverable corresponds to exactly one prompt file with target path specified. No deliverable should cover multiple files."
  ```

- [AC-2.3] Each prompt deliverable includes structural requirements for its type as ACs or Process Guidance — format, sections, frontmatter, conventions discovered during D1. For known plugin types (Skill, Agent, System instruction), use the prompt-engineering skill's Prompt Structure Reference. For other prompt types, encode the format requirements discovered from the user. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read M2 at {m2_path}. For each prompt deliverable, confirm ACs or Process Guidance specify structural requirements (format, sections, frontmatter, conventions). These must be specific to the prompt type, not generic."
  ```

- [AC-2.4] M2 Global Invariants encode prompt-engineering validation checklist and anti-pattern prohibitions, each verified by `prompt-reviewer` agent | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read M2 at {m2_path}. Confirm Global Invariants cover: validation items (goals not steps, no arbitrary values, direct imperatives, critical rules prominent, complexity matches task, information density, memento if applicable) AND anti-patterns (no prescriptive HOW, no capability instructions, no rigid checklists, no weak language, no buried critical info, no over-engineering). Each must specify prompt-reviewer as verification agent."
  ```

- [AC-2.5] For prompt types that have a description or discovery mechanism (e.g., Skill descriptions, Agent descriptions, API prompt metadata), M2 includes an AC requiring a strong description following the What + When + Triggers pattern. If the prompt type has no description field, this AC passes automatically. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read M2 at {m2_path}. For any deliverable whose prompt type includes a description or metadata field, confirm there is an AC requiring a description that states what it does, when to use it, and trigger terms. If no deliverables have description fields, output PASS."
  ```

- [AC-2.6] M2 written to `/tmp/prompt-manifest-{timestamp}.md` | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -s {m2_path} && echo PASS || echo FAIL"
  ```
