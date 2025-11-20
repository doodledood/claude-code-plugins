---
name: oracle
description: 'Consult with a more powerful AI model via the oracle CLI tool for complex analysis, architectural reviews, security audits, or comprehensive code understanding that benefits from extended reasoning time. Use when you need deeper insights beyond your own analysis, especially for: (1) Complex architectural decisions, (2) Security vulnerability analysis, (3) Comprehensive code reviews across large codebases, (4) Understanding intricate patterns or relationships in unfamiliar code, (5) Expert-level domain analysis. The tool runs asynchronously by default - start the query, continue other work, and reattach when complete.'
---

# Oracle

## Overview

Oracle is a CLI tool that provides access to more powerful AI models for complex analysis tasks. It accepts file globs and prompts, runs asynchronously, and returns detailed insights after extended reasoning time.

**Key advantages:**

- Access to more powerful models with longer reasoning chains
- Asynchronous operation - start queries without blocking your workflow
- Accepts extensive file context via globs
- Persistent sessions for reattachment

## Getting Started

**IMPORTANT: Always run `npx -y @steipete/oracle@latest --help` first to understand current capabilities and command syntax.**

The tool's help output is the source of truth for:

- Available options and flags
- Current command syntax
- Session management commands
- Examples and usage patterns

**Requirement:** `OPENAI_API_KEY` environment variable must be set (or use `--engine browser` mode).

## When to Use Oracle

Consult oracle when you need:

1. **Deep architectural analysis** - Understanding complex system designs or evaluating architectural decisions
2. **Security audits** - Comprehensive vulnerability analysis requiring extensive reasoning
3. **Large-scale code review** - Analyzing patterns, anti-patterns, or quality across many files
4. **Unfamiliar codebase exploration** - Understanding intricate relationships in code you're new to
5. **Complex refactoring decisions** - Evaluating trade-offs for significant code changes
6. **Expert domain analysis** - Tasks requiring specialized knowledge beyond general capabilities

**Don't use oracle for:**

- Simple code edits or fixes you can handle directly
- Questions answerable by reading 1-2 files
- Tasks requiring immediate responses (oracle takes minutes)
- Repetitive operations better suited to scripts

## Workflow

### Step 1: Check Help Output

Run `npx -y @steipete/oracle@latest --help` to see current options, commands, and examples.

### Step 2: Formulate the Question

Create a clear, specific prompt with a focused objective and expected deliverable.

**Good prompts (specific, focused, actionable):**

- "Identify SQL injection vulnerabilities in the authentication module. For each finding, provide the vulnerable code location, attack vector, and recommended fix."
- "List all public API endpoints that lack rate limiting. For each endpoint, assess the risk level and recommend appropriate rate limit configurations."
- "Map the data transformation pipeline from the /checkout endpoint to database persistence. Document each validation, transformation, and potential data loss point."

**Poor prompts (vague, unfocused):**

- "Review the code" - No focus or deliverable specified
- "Is this good?" - No evaluation criteria
- "Check for security issues" - Too broad, no prioritization

### Step 3: Select Relevant Files

Choose file globs that optimize for **recall** (include everything relevant) over precision. Oracle can handle extensive context.

See [references/glob-patterns.md](references/glob-patterns.md) for common patterns by query type.

**Key principles:**

- Use glob patterns to include entire directories
- Prefix with `!` to exclude patterns (e.g., `!**/*.test.ts`)
- Oracle handles large file sets - prioritize completeness over precision

### Step 4: Start the Query

Oracle runs asynchronously by default. The command outputs a session ID for reattachment.

**Check help for:**

- Current flag syntax (`-p`, `-f`, `--model`, etc.)
- Preview options to validate before running
- Available models and how to select them

### Step 5: Continue Other Work

The query runs in background. Continue with other tasks while processing.

### Step 6: Check Status and Reattach

Use the session management commands (see `npx -y @steipete/oracle@latest --help` for current syntax) to:

- List all sessions and their status
- Reattach to completed sessions
- View results

**Use the insights:** Apply oracle's analysis to complete your original task.

## Session Management

Run `npx -y @steipete/oracle@latest --help` and check the `session` and `status` commands for current syntax.

**Key capabilities:**

- List recent sessions with status and timestamps
- Reattach to any session (running or completed)
- Clean old sessions
- Sessions persist in `~/.oracle/sessions/<slug>`

## Model Selection

Oracle uses a default model suitable for most complex analysis tasks. For critical analysis requiring maximum reasoning capability, more powerful models may be available.

Check `npx -y @steipete/oracle@latest --help` for:

- Available models
- Current default model
- How to select different models via the `--model` flag

## Example Use Cases

See [references/glob-patterns.md](references/glob-patterns.md) for file selection patterns.

**Security audit:**

- Prompt: "Identify authentication bypass vulnerabilities. For each issue: specify the vulnerable endpoint/function, describe the exploit path, assess severity (Critical/High/Medium/Low), and provide a code fix."
- Files: auth modules, middleware, session management

**Architectural review:**

- Prompt: "Identify the top 5 highest-impact architectural issues causing tight coupling or hindering testability. For each: explain the problem, show affected components, estimate refactoring effort, and recommend a solution."
- Files: all source code, exclude tests, include README

**Data flow analysis:**

- Prompt: "Document the complete request lifecycle for POST /api/orders. Create a numbered sequence showing: 1) entry point, 2) each validation layer, 3) business logic transformations, 4) database operations, 5) response construction. Flag any validation gaps."
- Files: API routes, services, models, database layers

## Automation & Resource Management

When using oracle in automated workflows or agent scripts:

1. **Polling**: If waiting for completion, use `sleep 30` between status checks.
2. **Cleanup**: If running in a persistent shell session, explicitly terminate it (e.g., using `KillShell`) when the task is complete.
3. **Context**: Trust oracle's token limit reporting; don't prematurely optimize context size.

## Troubleshooting

**Environment issues:**

- Ensure `OPENAI_API_KEY` is set, or use `--engine browser` mode
- Run `npx -y @steipete/oracle@latest --help` to verify available engines and options

**Session management:**

- Use the `status` command to see available sessions
- Sessions persist in `~/.oracle/sessions/` until explicitly cleared
- Some queries can take several minutes - check status periodically

**For detailed examples and current syntax:** Always consult `npx -y @steipete/oracle@latest --help`
