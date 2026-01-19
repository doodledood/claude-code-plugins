# vibe-experimental

Experimental definition-driven workflows. Invest in definition upfront, then execute autonomously with enforced verification.

## Overview

Every criterion has explicit verification. Execution can't complete without verification passing or proper escalation.

## Skills

### User-Invocable

| Skill | Description |
|-------|-------------|
| `/define` | Work definition builder with proactive interview |
| `/do` | Autonomous execution from definition file |

### Internal

| Skill | Purpose |
|-------|---------|
| `/verify` | Runs verification for all criteria |
| `/done` | Completion marker with summary |
| `/escalate` | Structured escalation with evidence |

## Agents

| Agent | Purpose |
|-------|---------|
| `define-verifier` | Verifies definition completeness before /do |
| `criteria-checker` | Verifies a single criterion (bash or codebase check) |

## Hooks

| Hook | Purpose |
|------|---------|
| `stop_do_hook.py` | Enforces verification before stopping |
| `pretool_escalate_hook.py` | Enforces /verify before /escalate |

## Workflow

```
/define "task" → Interview → Definition file
                                   ↓
/do definition.md → Work → /verify → /done
                              ↓
                    (failures) → Fix → /verify again
                              ↓
                    (stuck) → /escalate
```

## Status

**Experimental** - More rigorous than standard workflows. Use when you want quality-focused autonomous execution.
