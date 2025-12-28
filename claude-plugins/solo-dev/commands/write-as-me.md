---
description: Generate text in your voice using your AUTHOR_VOICE.md document. Provide a topic or prompt as argument.
allowed-tools: ["Read", "Glob", "Task", "AskUserQuestion", "Skill"]
argument-hint: [topic or writing prompt, e.g., "a tweet about productivity" or "blog intro on AI tools"]
---

Use the **voice-writer** agent to generate content in the user's voice.

1. Find AUTHOR_VOICE.md (check cwd, then ~/, then glob search)
2. If no topic in $ARGUMENTS, ask what to write
3. Launch voice-writer agent with the voice doc path and content request
4. Present output, iterate if needed

Topic/prompt: $ARGUMENTS
