---
description: Run all code review agents in parallel (bugs, coverage, maintainability, type-safety if typed, CLAUDE.md adherence, docs).
allowed-tools: ["Task", "Read", "Glob", "Grep", "Bash"]
argument-hint: [file paths, or empty for branch diff]
---

Run a comprehensive code review. First detect the codebase type, then launch appropriate agents.

## Step 1: Detect Typed Language

Before launching agents, check if this is a typed language codebase:

**TypeScript/JavaScript with types:**
- `tsconfig.json` exists, OR
- `.ts`/`.tsx` files in scope

**Python with type hints:**
- `py.typed` marker exists, OR
- `mypy` or `pyright` in `pyproject.toml`/`setup.cfg`, OR
- Type annotations visible in `.py` files (`: str`, `-> None`, `Optional[`, `List[`, etc.)

**Statically typed languages (always typed):**
- Java (`.java`), Kotlin (`.kt`), Go (`.go`), Rust (`.rs`), C# (`.cs`), Swift (`.swift`), Scala (`.scala`)

Quick detection commands:
```bash
# TypeScript
ls tsconfig.json 2>/dev/null || git ls-files '*.ts' '*.tsx' | head -1

# Python types
ls py.typed 2>/dev/null || grep -l "mypy\|pyright" pyproject.toml setup.cfg 2>/dev/null | head -1

# Other typed languages
git ls-files '*.java' '*.kt' '*.go' '*.rs' '*.cs' '*.swift' '*.scala' | head -1
```

## Step 2: Launch Agents

**Always launch these 5 core agents IN PARALLEL:**

1. **code-bugs-reviewer** - Audit for logical bugs, race conditions, edge cases
2. **code-coverage-reviewer** - Verify test coverage for code changes
3. **code-maintainability-reviewer** - Check for DRY violations, dead code, complexity
4. **claude-md-adherence-reviewer** - Verify compliance with CLAUDE.md project standards
5. **docs-reviewer** - Audit documentation and code comments accuracy

**Conditionally launch (only if typed language detected):**

6. **type-safety-reviewer** - Audit type safety, any/unknown abuse, invalid states
   - **Primary:** TypeScript, Python with type hints (agent is optimized for these)
   - **Also useful for:** Java, Kotlin, Go, Rust, C#, Swift, Scala (core principles apply)
   - **Skip for:** Plain JavaScript, Ruby, PHP, shell scripts, untyped Python

Scope: $ARGUMENTS

If no arguments provided, all agents should analyze the git diff between the current branch and main/master branch.

## Execution

1. Run detection commands first (can be parallel)
2. Based on results, launch either 5 or 6 agents simultaneously in a single message
3. Do NOT run agents sequentially—always parallel
