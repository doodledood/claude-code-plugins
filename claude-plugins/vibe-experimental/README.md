# vibe-experimental

Experimental verification-first workflows. Every criterion has explicit verification; execution can't stop without verification passing or proper escalation.

## Overview

This plugin implements a verification-first approach to Claude Code workflows. The core thesis: invest heavily in definition with verification built-in, then let the LLM execute autonomously with enforced verification gates.

## Skills

### User-Invocable

| Skill | Description |
|-------|-------------|
| `/define` | Verification-first requirements builder with proactive LLM-driven interview |
| `/do` | Autonomous execution from definition file with enforced verification |

### Internal (Not User-Invocable)

| Skill | Called By | Purpose |
|-------|-----------|---------|
| `/verify` | `/do` | Runs all verification methods against codebase |
| `/done` | `/verify` | Completion marker that enables stop |
| `/escalate` | `/do` | Structured escalation with evidence |

## Agents

| Agent | Purpose |
|-------|---------|
| `define-verifier` | Unified verifier for /define output (27 acceptance criteria) |
| `criteria-checker` | Read-only verification agent for single criteria (bash + codebase checks) |

## Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `stop_do_hook.py` | Stop | Blocks stop unless /done or /escalate after /do |
| `pretool_escalate_hook.py` | PreToolUse | Blocks /escalate unless /verify called first |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  /define "add notification system"                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      /define SKILL                               │
│  - Proactive LLM-driven interview (12 techniques)               │
│  - Every criterion has verification method                       │
│  - Meta-verification before finalize                            │
│  - Output: /tmp/define-{timestamp}.md                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  /do /tmp/define-{timestamp}.md                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        /do SKILL                                 │
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
- Can't stop after `/do` without `/done` or `/escalate`
- Can't `/escalate` without calling `/verify` first
- Forces genuine verification before completion

### Memento Pattern
All skills write to log files before proceeding. This prevents context loss on compaction and enables verification to understand what was attempted.

### Criteria-Driven (Not Plan-Driven)
`/do` works toward acceptance criteria directly, not through plan decomposition. No "Chunk 1", "Chunk 2" - instead "satisfy AC-1", "satisfy AC-2".

## Status

**Experimental** - Works in progress. These workflows are more rigorous than the standard vibe-workflow but also more demanding. Use when you want to invest upfront in definition for autonomous execution.
