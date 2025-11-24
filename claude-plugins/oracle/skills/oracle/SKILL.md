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

**CRITICAL: The oracle tool evolves rapidly. The only source of truth for commands and arguments is the help output.**

Always start by running:

```bash
npx -y @steipete/oracle@latest --help
```

**Do not rely on memory or previous documentation for flag syntax.** The help output provides:

- The exact flags to pass prompts and files
- How to manage sessions (list, reattach, view)
- Available models and selection syntax
- Current command structure

**Requirement:** `OPENAI_API_KEY` environment variable must be set (or use the browser engine if supported).

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

Run `npx -y @steipete/oracle@latest --help` to determine the current syntax for:

- Providing a prompt
- Providing file patterns/globs
- Selecting a model
- Managing background sessions

### Step 2: Formulate the Question

Create a clear, specific prompt with a focused objective and expected deliverable.

**Good prompts (specific, focused, actionable):**

- "Identify SQL injection vulnerabilities in the authentication module. For each finding, provide the vulnerable code location, attack vector, and recommended fix."
- "List all public API endpoints that lack rate limiting. For each endpoint, assess the risk level and recommend appropriate rate limit configurations."
- "Map the data transformation pipeline from the /checkout endpoint to database persistence. Document each validation, transformation, and potential data loss point."

### Step 3: Select Relevant Files

Choose file globs that optimize for **recall** (include everything relevant) over precision. Oracle can handle extensive context.

**Key principles:**

- Use glob patterns to include entire directories
- Exclude irrelevant files (like tests or styles) if the tool supports exclusion patterns
- Prioritize completeness over precision

### Step 4: Start the Query

Construct your command based on the **current help output**.

**Look for flags that allow you to:**

1. Pass your formulated prompt
2. Pass your selected file globs
3. (Optional) Select a specific model if needed

### Step 5: Continue Other Work

The query typically runs in the background or returns a session ID. Continue with other tasks while processing.

### Step 6: Check Status and Reattach

Refer to the `--help` output for commands to:

- List active/completed sessions
- Reattach to a specific session
- Retrieve the output

**Use the insights:** Apply oracle's analysis to complete your original task.

## Session Management

Session management syntax may change. **Always check `--help`** to find commands for:

- Listing recent sessions
- Reattaching to a running session
- Viewing results of a completed session
- Clearing/pruning old sessions

Sessions typically persist locally until explicitly cleared.

## Model Selection

**Default Recommendation:** Always use the default model provided by the tool unless you have a specific reason not to (e.g., user explicitly requests a different model, or you encounter specific errors requiring a different capability).

Oracle uses a capable default model suitable for most tasks. If you need specific reasoning capabilities (e.g., a model with a larger context window or stronger reasoning), check `--help` to see:

- Which models are currently available
- The flag or syntax to specify a model
- The default model being used

## Example Use Cases

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

- **Polling**: If automating, verify via help if there are flags for waiting or if polling is required.
- **Cleanup**: Manage session artifacts as described in the help documentation to avoid disk clutter.
- **Context**: Trust the tool's handling of context limits; providing broad context is usually better than manually pruning.

## Troubleshooting

- **Environment**: Ensure required API keys are set. Check help for alternative engines (like browser-based) if keys are an issue.
- **Syntax Errors**: If a command fails, it is likely because flags have changed. **Run `--help` immediately to see the valid syntax.**
