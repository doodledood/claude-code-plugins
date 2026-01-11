---
name: explore-codebase
description: 'Find all files relevant to a query. Returns topic-specific overview + file list with line ranges—NOT a general codebase map.'
context: fork
---

**User request**: $ARGUMENTS

Find all files relevant to a specific query so you can master that topic without further searching.

## Workflow

### 1. Launch codebase-explorer agent

Use Task tool with `subagent_type: "vibe-workflow:codebase-explorer"`:

```
prompt: "$ARGUMENTS"
```

For cross-cutting queries spanning multiple distinct areas (e.g., "authentication and payment integration"), launch multiple agents in parallel—one per area.

### 2. Read recommended files

When the agent returns, read ALL files from the prioritized list:
- **MUST READ**: Read completely
- **SHOULD READ**: Read completely
- **REFERENCE**: Skim or read as needed

### 3. Return to original task

With files read, you now have full context. Continue with whatever task required this exploration.

## When to use multiple agents

| Query Type | Agents |
|------------|--------|
| Single topic (e.g., "authentication") | 1 agent |
| Cross-cutting (e.g., "how auth and payments interact") | 2+ agents in parallel |
| Broad scope (e.g., "onboarding to this codebase") | 1 agent with "very thorough" |

## Notes

- The agent handles all exploration, memento logging, and output compression
- You just launch, read files, and continue your work
- Agent returns research file path if you need to reference exploration details later
