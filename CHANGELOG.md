# Changelog

All notable changes to plugins in this repository.

Format: `[plugin-name] vX.Y.Z` - Brief description

## [Unreleased]

- [vibe-experimental] v0.21.0 - Add manifest-verifier agent to /define workflow:
  - New agent reviews manifests for gaps and outputs actionable continuation steps
  - /define now loops verification until COMPLETE status reached

- [vibe-experimental] v0.20.3 - Add "Efficient" principle to /define:
  - Prioritize questions that eliminate the most uncertainty
  - Minimize cognitive load per exchange
  - "Reduce friction, not coverage" - clarifies efficiency doesn't sacrifice completeness

- [vibe-extras] v1.7.0 - Rewrite `/rewrite-history` skill with clean-copy approach:
  - Creates backup branch, reimplements on fresh branch from main, verifies byte-identical, then replaces original
  - Non-negotiable verification: abort if any diff between backup and result
  - Reduced from 252 lines to 64 lines following prompt principles (WHAT not HOW)

- [vibe-experimental] v0.20.2 - Refine /define skill for better interview quality:
  - Add anti-eagerness constraint: ask when uncertain, never assume
  - Simplify code quality gates presentation (remove JSON block)
  - Strengthen convergence check to resist premature closure

- [vibe-experimental] v0.20.1 - Add verification preference constraint to /define:
  - Prefer bash > subagent > manual for verification methods
  - Addresses model defaulting to manual verification unnecessarily

- [vibe-experimental] v0.20.0 - Sync reviewers from vibe-workflow v2.17.0:
  - code-bugs-reviewer: dangerous defaults category, hidden contracts cross-reference
  - code-maintainability-reviewer: hidden contracts, function/type cohesion expansion, extensibility risk
  - code-coverage-reviewer: sync updates

- [vibe-workflow] v2.17.0 - Add "Hidden Contracts" to maintainability-reviewer (moved from bugs-reviewer):
  - Expanded "Temporal coupling" to "Temporal coupling & hidden contracts"
  - Catches cross-boundary implicit dependencies: code relies on side effects of another process rather than explicit data flow
  - Examples: fetching from DB instead of receiving as parameter, relying on order-of-operations
  - Test: "Could a caller know this dependency exists by looking at the function signature?"
  - Root issue is fragility (maintainability), not incorrectness (bugs)—if assumption holds, code works
  - High severity for main API paths, Medium for internal/helper code
  - Added cross-reference note in bugs-reviewer Category 6 pointing to maintainability

- [vibe-workflow] v2.16.0 - Add "Dangerous Defaults" category to code-bugs-reviewer:
  - Catches defaults that cause silent failures, security holes, or unbounded resource consumption
  - Test: "If a tired developer calls this with minimal args, will something bad happen?"
  - Examples: `timeout = 0`, `retries = Infinity`, `secure = false`, `validate = false`, `overwrite = true`
  - Severity based on impact: Critical for security/data loss, High for hangs/unbounded ops, Medium for internal utils

- [vibe-workflow] v2.15.0 - Expand cohesion to cover function and type levels in maintainability reviewer:
  - Module cohesion (existing): module handles unrelated concerns
  - Function cohesion (new): function does multiple things, name doesn't match behavior
  - Type cohesion (new): type accumulates unrelated properties (god type)
  - Unifying test: "Can you give this a clear, accurate name? If not, it's doing too much."
  - Added severity entries and example issue reports for each level

- [vibe-workflow] v2.14.0 - Add "Extensibility Risk" category to code-maintainability-reviewer:
  - Catches responsibilities placed at wrong abstraction level that create "forgettability risk"
  - Key test: "If someone adds another similar component, will they naturally do the right thing?"
  - Common cases: analytics/logging/auth embedded in leaf classes instead of orchestrators
  - High severity when 2+ siblings already manually replicate cross-cutting behavior
  - Medium severity for new code where pattern is likely to extend

- [vibe-experimental] v0.19.0 - /define: Restructure around 3 core principles
  - **Verifiable**: Every criterion has verification method (subsumes "no vague terms")
  - **Validated**: Generate concrete candidates, learn from reactions
  - **Complete**: Surface hidden requirements (outside view, pre-mortem, non-obvious)
  - Consolidate constraints: "Insights become criteria" (no standalone value)
  - 8 principles → 3 principles

- [vibe-experimental] v0.18.0 - Decision-making improvements to /define (inspired by Annie Duke):
  - Add backcasting alongside pre-mortem as discovery tools
  - Add "outside view first" principle: base rates → concrete criteria
  - Key insight: discovery tools must become INV-G*/AC-*—no standalone value
  - Simplified manifest schema to 3 sections: Intent, Invariants, Deliverables

- [solo-dev] v1.20.0 - Add /define-x-strategy skill for personalized X/Twitter growth:
  - Algorithm-derived optimal growth strategy based on X recommendation system analysis
  - Three-phase model: Build R (retrieval alignment) → Build D (engagement density) → Maximize S (content score)
  - Guided interview to create personalized X_STRATEGY.md
  - Includes reference doc with full optimization model

- [vibe-experimental] v0.17.0 - Strengthen todo discipline and goal motivation across skills:
  - /define: Added "Todo Discipline" section with required elements (flexible, not rigid template)
  - /define: Added "Why thoroughness matters" - explicit motivation for first-pass PR approval
  - /do: Added "Why quality execution matters" - verification pass on first attempt
  - /do: Added "Todo Discipline" and "Log Discipline" sections with required elements

- [vibe-experimental] v0.16.0 - /define improvements from session analysis:
  - Added principle 6: "ACs are observable behaviors" with non-engineer verification test
  - Added principle 7: "Explicitly surface edge cases" after core behavior
  - Improved description: "known requirements", "not for requirements discovery"

- [vibe-workflow] v2.13.2 - /spec description update:
  - Clarified /spec is for when WHAT is unclear (discovery phase)
  - Added "not executable manifest" to differentiate from manifest builders

- [vibe-experimental] v0.15.1 - /define now filters quality gates through project preferences:
  - Check CLAUDE.md for quality gate preferences before presenting options
  - Exclude gates users have disabled (e.g., "skip documentation checks")
  - Include custom gates users have defined (e.g., "always run security scan")

- [prompt-engineering] v1.18.0 - Add "avoid arbitrary values" principle to /compress-prompt:
  - Added principle 6: state the principle, not the number
  - Removed arbitrary "iterate up to 5 times" → "iterate until passes or stops improving"

- [vibe-experimental] v0.15.0 - Optimize /define per prompting principles:
  - Restored quality gate multi-select with agent mapping table
  - Added process vs output distinction for invariants and ACs
  - Added pre-mortem constraint, stopping convergence
  - Updated CLAUDE.md with "avoid arbitrary values" guidance

- [prompt-engineering] v1.17.0 - Restructure /compress-prompt and verifier to goal-oriented:
  - `/compress-prompt`: ~90 lines (was ~375)
  - `prompt-compression-verifier`: ~120 lines (was ~495)
  - Removed rigid phase/step structures
  - Core insight preserved: trust capability, enforce discipline

- [vibe-experimental] v0.13.0 - Restructure all skills from rigid phases to goal-oriented:
  - `/define`: Goal → Principles → Constraints → What to Discover → Output Schema
  - `/do`: Goal → Principles → Constraints (memento pattern) → What to Do
  - `/verify`: Goal → Principles → What to Do → Decision Logic → Output Format
  - `/done`: Goal → What to Do → Output Format → Principles
  - `/escalate`: Goal → Principles → Evidence Requirements → Escalation Types
  - All skills now: clear goal, clear constraints, freedom in execution
  - Memento pattern as constraint (todo list, log file, refresh before synthesis)
  - Significantly shorter across all skills

- [vibe-experimental] v0.12.1 - Fix outdated/inaccurate content in /define skill:
  - Removed "Local Invariants" from intro (merged into Acceptance Criteria in v0.11.0)
  - Corrected verification method guidance: bash for deterministic only, subagent for logic/judgment

- [vibe-experimental] v0.12.0 - Proactive interview + consolidated Global Invariants:
  - `/define` now uses proactive candidate generation ("YOU generate, user validates")
  - Phase order changed: Intent → Deliverables → ACs → Global Invariants (rules come last)
  - Global Invariants consolidated into single phase (merged Quality Gates + Project Gates)
  - Auto-detects project gates from CLAUDE.md + generates candidates from task type/risk
  - Questions ordered by information gain (task type, scope, risk split the space early)
  - Removed open-ended questions - users reveal criteria by reacting to concrete options

- [vibe-experimental] v0.11.0 - Major refactor: Manifest-based two-level architecture:
  - New schema: **Global Invariants** (task-level rules) + **Deliverables** with **Acceptance Criteria**
  - **Global Invariants** (INV-G*): Rules that apply to entire task; task fails if violated
  - **Acceptance Criteria** (AC-{D}.*): Per-deliverable verification (can be positive or negative)
  - Removed Local Invariants (merged into ACs - both verified the same way)
  - `/define`: Builds "Manifests" through phased interview (Intent → Deliverables → ACs → Global Invariants)
  - `/do`: Iterates deliverables satisfying ACs (flat todos with D{N}: prefix), then calls /verify
  - `/verify`: Launches one verifier per criterion in parallel, reports by type
  - `/done`: Outputs completion summary
  - `/escalate`: Type-aware escalation (task-level vs deliverable-level)
  - Removed pre-flight checks (Global Invariants only verified at final /verify)
  - **Breaking**: Old flat AC-N definitions incompatible; use new Manifest schema

- [vibe-experimental] v0.10.2 - Simplified /verify: single parallel launch, slow first in array

- [vibe-experimental] v0.10.1 - Subagent verification uses natural language prompts:
  - Changed `pass_if` to `prompt` field for subagent verification (maps to Task tool)
  - Added `general-purpose` agent option for custom checks
  - Clarified `agent` field is `subagent_type` for Task tool

- [vibe-experimental] v0.10.0 - Removed define-verifier, improved interview flow:
  - Removed define-verifier agent (user approval is the quality gate, not meta-verification)
  - Added Interview Philosophy: concrete choices > open-ended questions (users reveal criteria by reacting)
  - Added "Know when to stop" guidance (don't over-interview simple tasks)
  - Critical rules updated: "Concrete choices > open-ended" and "Know when to stop"

- [vibe-experimental] v0.9.0 - Techniques are starting points, not checklists:
  - Changed "Interview Techniques (use ALL)" to "starting points, not exhaustive"
  - Simplified todo template to be more adaptive
  - Added "(adapt to task)" notes throughout
  - Critical rule 8: "Techniques are starting points - ask whatever surfaces hidden criteria"

- [vibe-experimental] v0.8.0 - Terminology and context handling:
  - Reframed from "verification-first" to "definition-driven" (clearer positioning)
  - /define now handles context/research provided via $ARGUMENTS
  - When context is provided, asks what must be incorporated → becomes rejection criteria

- [vibe-experimental] v0.7.0 - Unified criteria prefix to AC-*:
  - All criteria now use sequential `AC-N` numbering (no more R-, E-, B-, QG-*, PQG-*)
  - Category is now metadata via `category` field (feature, rejection, edge-case, boundary, quality-gate, project-gate)
  - Sections organize criteria by type, but IDs are sequential across the entire definition
  - Verification methods unchanged - grouping by verification METHOD (bash, codebase, subagent, manual) still works

- [vibe-experimental] v0.6.0 - /verify three-phase execution for better parallelism:
  - Slow checks (tests, reviewers) launch in background immediately with `run_in_background: true`
  - Fast checks (lint, typecheck, codebase) process in parallel waves
  - Background results collected after fast checks complete
  - No longer blocked waiting for slow tests while fast checks could be running

- [vibe-experimental] v0.5.3 - /define skill improvements:
  - Adversarial examples now flexible (1-3 examples, pick relevant dimensions) instead of rigid 3+ with fixed table
  - Quality gates questions rephrased so second question doesn't sound optional ("More quality categories to verify:" instead of "Additional quality gates?")
  - criteria-checker agent now inherits all tools (removed explicit tool list restriction)

- [vibe-workflow] v2.13.1 - claude-md-adherence-reviewer improvements:
  - Focuses on outcome rules (affect files) not process rules (workflow only)
  - Checks context before reading CLAUDE.md files (may be auto-loaded)
  - The test: "Does the rule affect the FILES being committed?"

- [vibe-experimental] v0.5.2 - claude-md-adherence-reviewer focuses on outcome rules only:
  - Now distinguishes outcome rules (affect files) from process rules (workflow only)
  - Flags: naming conventions, patterns, architecture, file structure, required file updates
  - Ignores: git workflow, verification steps, how to run tests
  - The test: "Does the rule affect the FILES being committed?"

- [vibe-experimental] v0.5.1 - claude-md-adherence-reviewer checks context before reading files:
  - CLAUDE.md content may be auto-loaded into subagent context
  - Agent now checks if rules are already in context before using Read tool
  - Avoids redundant file reads when content is already available

- [vibe-experimental] v0.5.0 - Auto-detect project quality gates from CLAUDE.md:
  - /define now reads CLAUDE.md and extracts project-specific verifiable commands
  - Creates PQG-* criteria with bash verification (no question needed)
  - Flexible: includes whatever the project specifies (tests, lints, type checks, etc.)
  - Separate from code quality gates (QG-*) which use subagent verification
  - Only includes gates explicitly found in CLAUDE.md—doesn't invent commands

- [vibe-experimental] v0.3.2 - Parallel verification via criteria-checker agents:
  - /verify now spawns criteria-checker agents in parallel (up to --parallel=N, default 10)
  - criteria-checker handles BOTH bash and codebase checks (added Bash tool)
  - criteria-checker is read-only—checks, doesn't modify
  - Removed do-verifier agent (unused)
  - Cleaner separation: /verify orchestrates, criteria-checker executes

- [vibe-experimental] v0.3.1 - Trust LLM to work toward criteria:
  - Simplified "Work Toward Criteria" section—criteria define success, LLM decides the path
  - Todos now follow CLAUDE.md pattern: goal + `→log` discipline + `; done when X`
  - Removed prescriptive steps for logging and git commits
  - Consolidated process sections (8 → 6)

- [vibe-experimental] v0.3.0 - Rename skills for clarity and broader applicability:
  - `/spec` → `/define` - Verification-first requirements builder (works for any task, not just code)
  - `/implement` → `/do` - Autonomous execution from definition (task-agnostic naming)
  - Renamed agents: `spec-verifier` → `define-verifier`, `implement-verifier` → `do-verifier`
  - Renamed hook: `stop_implement_hook.py` → `stop_do_hook.py`
  - Updated all internal references (DoFlowState, has_do, parse_do_flow, etc.)
  - Updated tests to reflect new naming
  - All functionality preserved, only terminology changed

- [vibe-experimental] v0.2.0 - Implement verification-first workflow system:
  - 5 skills: `/define` (user-invocable), `/do` (user-invocable), `/verify`, `/done`, `/escalate` (internal)
  - 3 agents: `define-verifier` (27 AC checks), `do-verifier` (23 AC checks), `criteria-checker`
  - 2 hooks: stop hook (blocks without /done or /escalate), PreToolUse hook (blocks /escalate without /verify)
  - Enforced flow: can't stop without verification passing or proper escalation
  - Every criterion must have explicit verification method (bash, subagent, or manual)
  - 19 new tests for hook behavior

## 2026-01-17

- [vibe-workflow] v2.13.0 - Add acceptance criteria to all todo examples across skills:
  - Updated spec, plan, implement, research-web, explore-codebase, bugfix skills
  - Todos now include "; done when X" acceptance criteria
  - Example: `- [ ] Investigate API layer→log; done when architecture understood`
- [solo-dev] v1.19.0 - Add acceptance criteria to todo examples:
  - Updated define-customer-profile and define-seo-strategy skills
- [life-ops] v1.8.0 - Add acceptance criteria to /decide skill todos:
  - All 23 todo items now have explicit success conditions
- [CLAUDE.md] Updated "Todos as Micro-Prompts" section with acceptance criteria:
  - New principle: Acceptance criteria define what success looks like (RL-trained models need these)
  - Updated Quick Reference table and all todo examples
  - New pattern: `- [ ] Goal→log; done when X`
- [prompt-engineering] v1.16.0 - Add acceptance criteria to compress-prompt preservation hierarchy:
  - Acceptance criteria now Priority 1 alongside core goal (models are RL-trained to satisfy goals)
  - Updated prompt-compression-verifier with new "Missing Acceptance Criteria" issue type (1b)
  - Updated examples to show acceptance criteria being preserved
  - Key insight: WHAT (goal) + WHAT defines success (acceptance criteria) must be kept; only HOW is dropped
- [vibe-workflow] v2.12.0 - Orthogonality audit: sharpen reviewer boundaries to reduce overlap:
  - **bugs**: Added deadlocks/livelocks, rewrote Category 7 to focus on observable incorrect behavior, clarified security scope
  - **coverage**: Fixed wrong agent reference, removed TypeScript-only limitation, made suggestions less prescriptive
  - **maintainability**: Removed "testability blockers" category (now fully owned by testability), removed "deep call hierarchies" (simplicity owns)
  - **simplicity**: Added boundary notes for implicit behavior vs bugs, added function length check, clarified indirection scope
  - **testability**: Narrowed "complex async flows" to timing-dependent code only, added "side effects mixed with return values"
  - **type-safety**: Removed boolean blindness (API clarity not type safety), replaced complex generics with type predicate correctness
  - **docs**: Fixed severity contradiction (docs capped at Medium), clarified JSDoc overlap with type-safety
  - **claude-md**: Removed security from Critical (separate concern), eliminated "implied rules" language, added cross-reviewer deference
- [vibe-workflow] v2.10.1 - Plan file now includes spec reference (`Spec: {path or "none"}`) when a spec was used
- [vibe-workflow] v2.10.0 - `/review` now respects CLAUDE.md reviewer configuration:
  - Checks loaded CLAUDE.md files for `## Review Configuration` section
  - `Skip Reviewers` - exclude specific reviewers from running
  - `Required Reviewers` - force-include reviewers (e.g., type-safety for untyped projects)
  - `Custom Reviewers` - add project-specific review agents
  - CLAUDE.md files are auto-loaded into context, no searching required
- [vibe-workflow] v2.9.0 - New `/review-testability` skill and `code-testability-reviewer` agent:
  - Identifies code requiring excessive mocking to test
  - Severity based on: importance of logic × test friction (not pattern compliance)
  - Flags: high mock count, logic buried in IO, non-deterministic inputs, tight coupling
  - Explains WHY testability matters for each specific finding
  - Suggests improvements without mandating specific patterns
  - Added to `/review` parallel agent suite (now 7-8 agents)
- [vibe-workflow] v2.9.0 - `/fix-review-issues` now prioritizes CLAUDE.md adherence:
  - New issue priority order: Bugs > CLAUDE.md Adherence > Type Safety > Coverage > Maintainability > Simplicity > Docs
  - Phase 1.5 now filters findings that conflict with CLAUDE.md rules (not just plan/spec)
  - Conflict resolution: user-defined CLAUDE.md rules take precedence over generic reviewer suggestions
  - Plan creation orders issues by priority for systematic fixing
- [vibe-workflow] v2.8.1 - claude-md-adherence-reviewer now checks ALL CLAUDE.md sources:
  - Enterprise/Managed level (`/etc/claude-code/CLAUDE.md`, etc.)
  - User level (`~/.claude/CLAUDE.md`)
  - Project level (`.claude/CLAUDE.md`, `.claude/rules/*.md`)
  - Local project level (`CLAUDE.local.md`)
  - Import references (`@path/to/file` syntax)
  - Updated pre-output checklist to verify all sources were checked

## 2026-01-16

- [prompt-engineering] v1.15.0 - Execution Discipline preservation category:
  - New distinction: trust model's KNOWLEDGE (drop), don't trust model's DISCIPLINE (keep)
  - Execution discipline = guardrails against laziness, premature completion, context loss, skipping verification
  - Priority 2 alongside Novel Constraints in preservation hierarchy
  - Examples: "write findings BEFORE proceeding", "don't finalize until X verified", "read full log before synthesis"
  - Verifier updated to NOT flag execution discipline as over-specification
  - Key insight: discipline guardrails address model weaknesses, not capability gaps
- [prompt-engineering] v1.14.0 - Trust-the-model compression philosophy:
  - Shift from "semantic preservation" to "capability preservation"
  - New preservation hierarchy: goal + novel constraints only; drop training-redundant content
  - Training filter: "Would a competent person doing this task need to be told this?" If no → drop
  - Action Space Check: verify model is FREE to solve its own way
  - Verifier now flags Over-Specification (recommend removal) and Training-Redundant content
  - New severity model: MEDIUM/LOW issues are about REMOVING content, not adding it back
  - Target even more aggressive compression by trusting model's training
  - Domain-agnostic: works for any prompt type (coding, decisions, writing, research)
- [prompt-engineering] v1.13.0 - Fix compress-prompt to enforce aggressive compression:
  - Explicit target: 85-95% token reduction, ~200-600 tokens max output
  - Clarified output must be ONE dense paragraph (no headers, bullets, structure)
  - Added self-check before writing: is it one paragraph? ~200-600 tokens?
  - New "Common Mistakes to Avoid" section (reformatting vs compressing)
  - Clearer preservation hierarchy table with KEEP vs DROP actions
- [prompt-engineering] v1.12.0 - New `/compress-prompt` skill for extreme prompt compression:
  - Compresses prompts/skills into single dense paragraphs for AI-readable context injection
  - 7-level preservation hierarchy (goal/constraints NEVER drop; explanations/style CAN drop)
  - Natural dense prose compression (semicolon-chained, articles omitted, abbreviations used)
  - New `prompt-compression-verifier` agent checks 5 issue types (Missing Core Goal, Missing Constraint, Missing Edge Case, Semantic Drift, Ambiguity Introduced)
  - Non-destructive output (display + optional file save)
  - Verification loop with max 5 iterations
- [prompt-engineering] v1.11.3 - Use `mv` for atomic file replacement in all optimization skills:
  - `/apply-prompt-feedback`, `/optimize-prompt-goal`, `/optimize-prompt-precision` now use `mv` instead of Write tool for final output
  - Matches existing pattern in `/optimize-prompt-token-efficiency`
- [prompt-engineering] v1.11.2 - Comparison mode for `/optimize-prompt-precision`:
  - `prompt-precision-verifier` now supports comparison mode (original vs modified)
  - Adds 2 comparison-mode issue types: Optimization Regression, Over-Optimization
  - `/optimize-prompt-precision` uses comparison mode for post-optimization verification
- [prompt-engineering] v1.11.1 - Verifier comparison mode for regression detection:
  - `prompt-goal-verifier` now supports comparison mode (original vs modified)
  - Adds 2 comparison-mode issue types: Optimization Regression, Over-Optimization
  - `/optimize-prompt-goal` uses comparison mode for post-optimization verification
  - `/apply-prompt-feedback` verifier compares original vs modified to detect regressions
- [prompt-engineering] v1.11.0 - New `/apply-prompt-feedback` skill for calibrated feedback application:
  - Applies user feedback to prompts without over-fitting or causing regressions
  - New `prompt-feedback-verifier` agent checks 6 issue types across 3 dimensions:
    - Incorporation (2): Feedback Not Addressed, Partial Incorporation
    - Calibration (2): Over-Fitting, Over-Specification
    - Preservation (2): Regression, Information Density Loss
  - Apply-first approach: applies feedback, then verifies for issues
  - Information density maximization: minimal text to achieve change
  - Iterative refinement loop (max 5 iterations) driven by verifier feedback
- [prompt-engineering] v1.10.0 - New `/optimize-prompt-token-efficiency` skill (moved from vibe-extras):
  - Iteratively optimizes prompts for token efficiency while preserving semantic content
  - Verify-first approach: runs verifier before changes, exits early if already efficient
  - New `prompt-token-efficiency-verifier` agent with dual-mode operation:
    - Single-file mode: identifies inefficiencies (redundancy, verbosity, compression opportunities)
    - Two-file mode: verifies compression is lossless by comparing original vs compressed
  - Techniques: redundancy removal, terse phrasing, filler elimination, structural optimization
- [vibe-extras] v1.6.0 - Removed `maximize-info-density` skill (moved to prompt-engineering as `/optimize-prompt-token-efficiency`)
- [prompt-engineering] v1.9.0 - Verify-first approach and rename `/refine-prompt` → `/optimize-prompt-precision`:
  - Rename: `/refine-prompt` → `/optimize-prompt-precision` for consistency with `/optimize-prompt-goal`
  - Run verifier FIRST before any changes - maybe prompt is already optimal
  - All changes driven by verifier feedback only - no independent analysis
  - Early exit if verifier returns VERIFIED on first check

## 2026-01-15

- [prompt-engineering] v1.8.2 - Refine `optimize-prompt-goal` skill for precision:
  - Defined "goal effectiveness" as alignment + likelihood of achieving outcomes
  - Added Required tools section documenting Task and TodoWrite dependencies
  - Clarified input detection priority and file path fallback behavior
  - Added empty file, binary file, and Write tool failure edge cases
  - Replaced pseudocode loop with clearer prose format
  - Added verifier failure retry semantics and Task tool mid-workflow handling
  - Defined sensible defaults priority order (safety > completeness > clarity)
  - Clarified "Preserve intent" with explicit contradiction criteria
  - Added document order clarification for goal conflict resolution
- [prompt-engineering] v1.8.1 - Refine `prompt-goal-verifier` agent for precision:
  - Added explicit priority tier definitions with full type mapping
  - Defined 4-criterion flagging threshold (specific harm, reproducible, actionable, net positive)
  - Added low-confidence goal handling (goal-independent vs goal-dependent issues)
  - Added guidance for edge cases: multiple goals, no-instruction prompts, example-only prompts
  - Replaced vague thresholds with concrete criteria
  - Standardized type names to singular form
- [prompt-engineering] v1.8.0 - New `/optimize-prompt-goal` skill for goal effectiveness optimization:
  - Iteratively optimizes prompts to better achieve their stated goals
  - New `prompt-goal-verifier` agent checks 11 issue types across 3 dimensions:
    - Goal Achievement (4): Misalignment, Missing/Vague Goal, Goal Dilution, Unmeasurable Success
    - Error Prevention (4): Misstep Risk, Failure Mode Gaps, Contradictory Guidance, Unsafe Defaults
    - Efficiency (3): Unnecessary Overhead, Indirect Path, Redundant Instructions
  - Impact-based severity (CRITICAL/HIGH/MEDIUM/LOW)
  - Goal inference: explicit → context-inferred → low-confidence best-effort
  - Complements `/refine-prompt` (precision) with goal optimization
- [life-ops] v1.7.1 - `/decide` skill: optimize information density (16% token reduction):
  - Compressed verbose prose to terse bullets and tables
  - Minified JSON templates while preserving structure
  - Consolidated redundant instructions
  - Verified lossless: all semantic content preserved
- [life-ops] v1.7.0 - `/decide` skill: comprehensive quality/trust hardening (10-round verification):
  - Anti-anchoring: Underlying need probe sequence, sunk cost check moved early (2.1), option set completeness check
  - EBA flaw fix: Near-miss protection (10-15% threshold) prevents best options being eliminated on marginal misses
  - Qualitative factors: Descriptive thresholds, 80% signal decision rule, no false numeric proxies
  - Research integrity: Source independence validation, assumed values flagged in matrix, completeness verification
  - Resurrection mechanism: Pre-mortem can resurface eliminated options with full analysis, max 1 per decision
  - Usability: Time calibration upfront (10-60min by stakes), "decide not to decide" handling, sunk cost deduplication
  - Option interdependence check: Combined options, negotiating leverage, wait-and-see preserved
- [life-ops] v1.6.0 - `/decide` skill: optimize for decision QUALITY and TRUST:
  - Add decision framing check (Phase 2.1): verify user is asking the right question before diving deep
  - Add comprehensiveness checkpoint (Phase 2.7): active verification checklist, explicit user confirmation required
  - Add pre-mortem stress test (Phase 8.3): actively try to break recommendation before finalizing
  - Enhanced final synthesis with trust-building elements: comprehensiveness summary, eliminated options audit, explicit confidence criteria, "what we didn't explore" section
  - High-stakes override: shortcuts require explicit user consent for high/life-changing decisions
  - Updated todo template with new steps (framing check, comprehensiveness checkpoint, pre-mortem)
- [life-ops] v1.5.3 - `/decide` skill: proactive factor discovery:
  - Add "proactive stance" directive: generate factors using domain knowledge, don't wait for user
  - Factor scaffolding now requires 8-12 concrete factors BEFORE asking user
  - Hidden factors section now has category table (financial, lock-in, time, risk, second-order)
  - Explicit instruction to surface factors user would miss on their own
- [life-ops] v1.5.2 - `/decide` skill: enforce mandatory todo list creation:
  - Add prominent ⚠️ MANDATORY section near top requiring todo list before any user interaction
  - Update Core Loop to show TodoList as explicit first step
  - Add prerequisite note to Phase 0 referencing todo list requirement
  - Addresses issue where skill would skip todo list creation, causing phase-skipping and context rot
- [life-ops] v1.5.1 - `/decide` skill: optimize information density (37% token reduction):
  - Compressed verbose prose to terse bullet points and tables
  - Minified JSON examples while preserving structure
  - Combined redundant todo items with write-discipline note
  - Verified lossless: all semantic content preserved (3 verification iterations)
- [life-ops] v1.5.0 - `/decide` skill: strengthen existing options discovery (Phase 4.1):
  - Add explicit AskUserQuestion before research to surface user's existing options
  - Session analysis showed users often have options in mind but don't mention unprompted
  - Prevents wasted research and corrections when user's preferred options weren't included
  - Updated todo list template to split option discovery into "ask user first" + "research" steps
- [life-ops] v1.4.0 - Research-validated improvements to `/decide` skill:
  - Add gut check phase: captures intuition as data before analysis (research shows emotion is essential, not enemy, of good decisions)
  - Reposition 10-10-10 as "Temporal Perspective Check": theoretically grounded in Construal Level Theory (no direct empirical validation exists for 10-10-10 specifically)
  - Add affective forecasting calibration: note that people overestimate emotional intensity ~50%
  - Add consideration set quality check before finalist analysis
- [life-ops] v1.3.0 - Complete rewrite of `/decide` skill for decision QUALITY over speed:
  - Integrates EBA (Elimination By Aspects) methodology with sequential elimination rounds
  - Adds exhaustive /spec-style discovery with edge-case hunting and factor scaffolding
  - Option discovery phase: finds options when user doesn't provide them
  - Market context for threshold setting (basic/solid/premium benchmarks)
  - Pairwise trade-off comparisons for finalists ("A gives X but costs Y")
  - Sensitivity analysis ("recommendation flips if...")
  - 10-10-10 regret framework
  - Maintains memento pattern (external decision log, refresh before synthesis)
  - Cross-category representation rule for comprehensive comparison
- [life-ops] v1.2.0 - Comprehensive discovery improvements for `/decide` skill:
  - Add Hidden Factors Probe ("What would make you doubt this in 5 years?") to surface overlooked considerations
  - Add Phase 4.5 Post-Research Gap Check as iterative loop: research → identify gaps → ask user → if critical factors → follow-up research → repeat (max 3 rounds)
  - Use Task with web-researcher agent instead of Skill to preserve todo state
  - Add cross-category comparison rule: Top 3 must include options from different categories with "Why #1's category wins"
- [life-ops] v1.1.0 - Reduce rigidity in `/decide` skill: add Coach's Discretion section, fast path for pre-processed decisions, self-knowledge decision handling, flexible questioning approach
- [life-ops] v1.0.1 - Precision refinement for `/decide` skill: defined thresholds, clarified edge cases, resolved conflicts
- [life-ops] v1.0.0 - New plugin: Personal decision-making advisor with `/decide` skill for situation discovery, targeted research, and structured decision analysis

## 2026-01-14

- [vibe-workflow] v2.8.0 - /spec now skips codebase research for non-code work (external research, analysis, comparisons)
- [vibe-workflow] v2.7.1 - Refactor: remove explicit "memento pattern" naming from skills/agents; behavior preserved
- [prompt-engineering] v1.7.2 - Refactor: remove explicit "memento pattern" naming; behavior preserved
- [solo-dev] v1.18.2 - Refactor: remove explicit "memento pattern" naming; behavior preserved
- [vibe-extras] v1.5.2 - Refactor: remove explicit "memento pattern" naming; behavior preserved
- [vibe-workflow] v2.7.0 - Plan quality improvements:
  - New `plan-verifier` agent validates plans before approval (dependency consistency, spec coverage, TBD markers, circular deps)
  - `/plan` now runs verification loop (up to 5 attempts) with automatic fix suggestions
  - `/plan` offers to launch `/spec` when requirements are thin (<2 concrete requirements)
- Initial changelog started. Prior history not retroactively documented.
