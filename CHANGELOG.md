# Changelog

All notable changes to plugins in this repository.

Format: `[plugin-name] vX.Y.Z` - Brief description

## [Unreleased]

## 2026-01-14

- [vibe-workflow] v2.7.0 - Plan quality improvements:
  - New `plan-verifier` agent validates plans before approval (dependency consistency, spec coverage, TBD markers, circular deps)
  - `/plan` now runs verification loop (up to 5 attempts) with automatic fix suggestions
  - `/plan` offers to launch `/spec` when requirements are thin (<2 concrete requirements)
- Initial changelog started. Prior history not retroactively documented.
