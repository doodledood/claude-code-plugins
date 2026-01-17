# vibe-experimental

Experimental workflows exploring verification-first specs and acceptance-driven development.

## Overview

This plugin contains experimental approaches to Claude Code workflows that are still being developed and tested. The core thesis: invest heavily in specification with verification built-in, then let the LLM execute autonomously.

## Current Experiments

### Verification-First Spec

A redesigned `/spec` approach where:

- Every criterion has an explicit verification method
- Exhaustive adversarial interview surfaces tacit knowledge
- Pre-mortem, disappointed questions, contrast pairs, and synthetic examples
- Meta-verification ensures spec quality before implementation
- Goal: spec once, sleep, wake up to near-perfection

**Files:**
- `specs/spec-skill-redesign.md` - Acceptance criteria for the skill itself
- `specs/spec-skill-redesign-subagents.md` - Subagent definitions for verification
- `specs/scripts/` - Validation scripts

## Status

**Experimental** - These are works in progress, not production-ready workflows.

## Philosophy

Traditional workflow: Spec → Plan → Implement → Review (multiple checkpoints)

Experimental workflow: Exhaustive Spec (with verification) → Autonomous Implementation → Done

The bet: if you invest enough upfront in defining exactly what you want (and how to verify it), the LLM can figure out how to get there without hand-holding.
