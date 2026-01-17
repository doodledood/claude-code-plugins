# vibe-experimental

Experimental verification-first workflows. Every criterion has explicit verification; implementation can't stop without verification passing or proper escalation.

## Overview

This plugin implements a verification-first approach to Claude Code workflows. The core thesis: invest heavily in specification with verification built-in, then let the LLM execute autonomously with enforced verification gates.

## Skills

### User-Invocable

| Skill | Description |
|-------|-------------|
| `/spec` | Verification-first requirements builder with proactive LLM-driven interview |
| `/implement` | Autonomous implementation from spec file with enforced verification |

### Internal (Not User-Invocable)

| Skill | Called By | Purpose |
|-------|-----------|---------|
| `/verify` | `/implement` | Runs all verification methods against codebase |
| `/done` | `/verify` | Completion marker that enables stop |
| `/escalate` | `/implement` | Structured escalation with evidence |

## Agents

| Agent | Purpose |
|-------|---------|
| `spec-verifier` | Unified verifier for /spec output (27 acceptance criteria) |
| `implement-verifier` | Unified verifier for /implement behavior (23 acceptance criteria) |
| `criteria-checker` | Generic checker for code patterns against spec criteria |

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `stop_implement_hook.py` | Stop | Blocks stop unless /done or /escalate after /implement |
| `pretool_escalate_hook.py` | PreToolUse | Blocks /escalate unless /verify called first |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  /spec "add notification system"                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      /spec SKILL                                 │
│  - Proactive LLM-driven interview (12 techniques)               │
│  - Every criterion has verification method                       │
│  - Meta-verification before finalize                            │
│  - Output: /tmp/spec-{timestamp}.md                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  /implement /tmp/spec-{timestamp}.md                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    /implement SKILL                              │
│  - Works toward criteria (no plan decomposition)                │
│  - Memento pattern mandatory                                    │
│  - Calls /verify when ready                                     │
│  - Can call /escalate when genuinely stuck                      │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│       /verify           │       │      /escalate          │
│  Runs all verifications │       │  Structured evidence    │
│  → failures: continue   │       │  → allows stop          │
│  → all pass: call /done │       └─────────────────────────┘
└─────────────────────────┘
            │
            ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│        /done            │       │      STOP HOOK          │
│  Completion marker      │──────▶│  Allows stop when       │
│  Enables stop           │       │  /done or /escalate     │
└─────────────────────────┘       └─────────────────────────┘
```

## Key Design Principles

### Verification-First
Every criterion must have an explicit verification method (bash command, subagent check, or manual flag). No vague criteria like "code should be clean."

### Enforced Flow
Hooks prevent premature stopping:
- Can't stop after `/implement` without `/done` or `/escalate`
- Can't `/escalate` without calling `/verify` first
- Forces genuine verification before completion

### Memento Pattern
All skills write to log files before proceeding. This prevents context loss on compaction and enables verification to understand what was attempted.

### Criteria-Driven (Not Plan-Driven)
`/implement` works toward acceptance criteria directly, not through plan decomposition. No "Chunk 1", "Chunk 2" - instead "satisfy AC-1", "satisfy AC-2".

## Specs

Design specifications for this plugin:

- `specs/spec-skill-redesign.md` - 27 acceptance criteria for /spec skill
- `specs/implement-skill-spec.md` - 23 acceptance criteria for /implement system
- `specs/spec-skill-redesign-subagents.md` - Subagent definitions for spec verification
- `specs/implement-skill-subagents.md` - Subagent definitions for implement verification

## Status

**Experimental** - Works in progress. These workflows are more rigorous than the standard vibe-workflow but also more demanding. Use when you want to invest upfront in specification for autonomous execution.
