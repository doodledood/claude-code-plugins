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
| `/verify` | `/do` | Spawns parallel criteria-checker agents for verification |
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
│  - Works toward criteria (LLM decides how)                      │
│  - Logs attempts after each work todo completes                 │
│  - Calls /verify when ready                                     │
│  - Can call /escalate when genuinely stuck                      │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
┌─────────────────────────┐       ┌─────────────────────────┐
│       /verify           │       │      /escalate          │
│  Spawns criteria-checker│       │  Structured evidence    │
│  agents in parallel     │       │  → allows stop          │
│  → failures: continue   │       └─────────────────────────┘
│  → all pass: call /done │
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
Every criterion must have an explicit verification method (bash command, codebase check, or manual flag). No vague criteria like "code should be clean."

### Parallel Verification
`/verify` spawns `criteria-checker` agents in parallel (up to 10 concurrent, configurable via `--parallel=N`). Each agent handles one criterion—either bash command or codebase pattern check.

### Enforced Flow
Hooks prevent premature stopping:
- Can't stop after `/do` without `/done` or `/escalate`
- Can't `/escalate` without calling `/verify` first
- Forces genuine verification before completion

### Criteria-Driven Execution
`/do` trusts the LLM to work toward criteria—criteria define success, the LLM decides how. No prescriptive steps or plans, just todos with embedded logging discipline (`→log`) and success conditions (`; done when X`).

### Logging for Context
Logs capture key decisions, blockers, and solutions after each work todo completes. This enables verification to understand what was attempted and prevents context loss.

## Status

**Experimental** - Works in progress. These workflows are more rigorous than the standard vibe-workflow but also more demanding. Use when you want to invest upfront in definition for autonomous execution.
