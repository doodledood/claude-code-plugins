# Changelog

All notable changes to plugins in this repository.

Format: `[plugin-name] vX.Y.Z` - Brief description

## [Unreleased]

## 2026-01-15

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
