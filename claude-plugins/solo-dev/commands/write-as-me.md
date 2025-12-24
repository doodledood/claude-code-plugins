---
description: Generate text in your voice using your AUTHOR_VOICE.md document. Provide a topic or prompt as argument.
allowed-tools: ["Read", "Glob", "AskUserQuestion"]
argument-hint: [topic or writing prompt, e.g., "a tweet about productivity" or "blog intro on AI tools"]
---

Write content in the user's voice based on their AUTHOR_VOICE.md.

Topic/prompt: $ARGUMENTS

1. Find and read AUTHOR_VOICE.md (check cwd, then ~/AUTHOR_VOICE.md, then glob search)
2. If no topic provided, ask what to write about
3. Embody the voice fully - tone, vocabulary, structure, signature moves
4. Generate the content
5. Ask if adjustments needed, iterate until perfect
