---
description: Run all code review agents in parallel (bugs, coverage, maintainability, type-safety if typed, CLAUDE.md adherence, docs).
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

## Step 3: Verification Agent (Final Pass)

After all review agents complete, launch an **opus verification agent** to reconcile and validate findings:

**Purpose**: The review agents run in parallel and are unaware of each other's findings. This can lead to:
- Conflicting recommendations (one agent suggests X, another suggests opposite)
- Duplicate findings reported by multiple agents
- Low-confidence or vague issues that aren't actionable
- False positives that would waste time fixing

**Verification Agent Task**:

Use the Task tool with `model: opus` to launch a verification agent with this prompt:

```
You are a Review Reconciliation Expert. Analyze the combined findings from all review agents and produce a final, consolidated report.

## Input
[Include all agent reports here]

## Your Tasks

1. **Identify Conflicts**: Find recommendations that contradict each other across agents. Resolve by:
   - Analyzing which recommendation is more appropriate given the context
   - Noting when both perspectives have merit (flag for user decision)
   - Removing the weaker recommendation if clearly inferior

2. **Remove Duplicates**: Multiple agents may flag the same underlying issue. Consolidate into single entries, keeping the most detailed/actionable version.

3. **Filter Low-Confidence Issues**: Remove or downgrade issues that:
   - Are vague or non-actionable ("could be improved" without specifics)
   - Rely on speculation rather than evidence
   - Would require significant effort for minimal benefit
   - Are stylistic preferences not backed by project standards

4. **Validate Severity**: Ensure severity ratings are consistent and justified:
   - Critical: Will cause production failures or data loss
   - High: Significant bugs or violations that should block release
   - Medium: Real issues worth fixing but not blocking
   - Low: Nice-to-have improvements

5. **Flag Uncertain Items**: For issues where you're uncertain, mark them as "Needs Human Review" rather than removing them.

## Output

Produce a **Final Consolidated Review Report** with:
- Executive summary (overall code health assessment)
- Issues by severity (Critical → Low), deduplicated and validated
- Conflicts resolved (note any that need user decision)
- Items removed with brief reasoning (transparency)
- Recommended fix order (dependencies, quick wins first)
```

## Execution

1. Run detection commands first (can be parallel)
2. Based on results, launch either 5 or 6 agents simultaneously in a single message
3. Do NOT run agents sequentially—always parallel
4. After all agents complete, launch the verification agent with all findings
5. Present the final consolidated report to the user
