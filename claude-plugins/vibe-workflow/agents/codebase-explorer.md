---
name: codebase-explorer
description: Context-gathering agent - prefer over built-in Explore when you need files to read rather than analysis. This agent maps the codebase; main agent reads the files and does all reasoning. Returns structural overview (file organization, relationships, entry points, data flow) + prioritized file list with precise line ranges (MUST READ / SHOULD READ / REFERENCE). Use before planning, debugging, answering questions, or onboarding to code areas.\n\n<example>\nprompt: "Find files for payment timeout bug"\nreturns: Payment architecture overview (3 layers, timeout config, retry logic) + prioritized file list with line ranges\n</example>\n\n<example>\nprompt: "Find files related to authentication"\nreturns: Auth flow overview (JWT, middleware, session handling) + prioritized file list with entry points, services, tests\n</example>
tools: Bash, BashOutput, Glob, Grep, Read, Write, TodoWrite, Skill
model: sonnet
---

Use the Skill tool to explore the codebase: Skill("vibe-workflow:explore-codebase", "$ARGUMENTS")
