---
name: review
description: Run all code review agents in parallel (bugs, coverage, maintainability, simplicity, type-safety if typed, CLAUDE.md adherence, docs). Respects CLAUDE.md reviewer configuration.
---

Run a comprehensive code review. First detect the codebase type, then launch appropriate agents.

**Flags**: `--autonomous` → skip Step 5 user prompt, return report only (for programmatic invocation)

## Step 1: Check CLAUDE.md for Reviewer Preferences

Check loaded CLAUDE.md content for any guidance about which reviewers to run or skip. CLAUDE.md files are auto-loaded—do NOT search for them.

**Users can express preferences however they want.** Examples:
- "Skip the docs reviewer, we don't have documentation requirements"
- "Always run type-safety even though we use plain JS"
- "Don't run coverage checks"
- A dedicated section listing reviewers to include/exclude
- Custom review agents they've defined

**Available reviewers** (use your judgment matching user intent):
- `code-bugs-reviewer` - bugs, logic errors
- `code-coverage-reviewer` - test coverage
- `code-maintainability-reviewer` - DRY, dead code, coupling
- `code-simplicity-reviewer` - over-engineering, complexity
- `code-testability-reviewer` - testability, mocking friction
- `claude-md-adherence-reviewer` - CLAUDE.md compliance
- `docs-reviewer` - documentation accuracy
- `type-safety-reviewer` - type safety (conditional by default)

**If no preferences stated:** Use defaults (all core agents + type-safety if typed codebase).

## Step 2: Detect Typed Language

Unless `type-safety` is in `Skip Reviewers` or `Required Reviewers`, determine if this is a typed codebase.

**Check loaded CLAUDE.md content first** (no commands needed):
- Development commands mention `tsc`, `mypy`, `pyright`, or type-checking
- Tech stack mentions TypeScript, typed Python, Go, Rust, Java, etc.
- File extensions mentioned (`.ts`, `.tsx`, `.go`, `.rs`, `.java`, etc.)

**Typed if any of these are evident from context:**
- TypeScript/TSX project
- Python with type hints (`mypy`, `pyright` in dev commands)
- Statically typed languages: Go, Rust, Java, Kotlin, C#, Swift, Scala

**Skip type-safety for:**
- Plain JavaScript (no TypeScript)
- Untyped Python (no mypy/pyright)
- Ruby, PHP, shell scripts

If CLAUDE.md content doesn't make it clear, use your judgment based on files you've seen in context.

## Step 3: Launch Agents

**Build the agent list based on CLAUDE.md preferences (Steps 1-2):**

### Core Agents (launch IN PARALLEL):

1. **code-bugs-reviewer** - Logical bugs, race conditions, edge cases
2. **code-coverage-reviewer** - Test coverage for code changes
3. **code-maintainability-reviewer** - DRY violations, dead code, coupling
4. **code-simplicity-reviewer** - Over-engineering, complexity
5. **code-testability-reviewer** - Testability, mocking friction
6. **claude-md-adherence-reviewer** - CLAUDE.md compliance
7. **docs-reviewer** - Documentation accuracy

### Conditional:

8. **type-safety-reviewer** - Type safety, any/unknown abuse
   - Include if: typed codebase (Step 2) OR user requested it
   - Skip if: user said to skip it, or untyped codebase

### Custom Agents:

9. **Any custom reviewers the user defined** - Launch with their specified agent/description

**Applying preferences:**
- Skip any reviewers the user said to exclude
- Include any reviewers the user said to always run
- Add any custom reviewers the user defined

**Scope:** $ARGUMENTS

If no arguments provided, all agents should analyze the git diff between the current branch and main/master branch.

## Step 4: Verification Agent (Final Pass)

After all review agents complete, launch an **opus verification agent** to reconcile and validate findings:

**Purpose**: The review agents run in parallel and are unaware of each other's findings. This can lead to:
- Conflicting recommendations (one agent suggests X, another suggests opposite)
- Duplicate findings reported by multiple agents
- Low-confidence or vague issues that aren't actionable
- False positives that would waste time fixing

**Verification Agent Task**:

Launch an opus verification agent with this prompt:

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

## Step 5: Follow-up Action

**If `--autonomous`**: Skip user prompt, end after presenting report. Caller handles next steps.

**Otherwise**, ask the user what they'd like to address:

```
header: "Next Steps"
question: "Would you like to address any of these findings?"
options:
  - "Critical/High only (Recommended)" - Focus on issues that should block release
  - "All issues" - Address everything including medium and low severity
  - "Skip" - No fixes needed right now
```

**Based on selection:**
- **Critical/High only**: Invoke the vibe-workflow:fix-review-issues skill with "--severity critical,high"
- **All issues**: Invoke the vibe-workflow:fix-review-issues skill
- **Skip**: End workflow

## Execution

1. Check loaded CLAUDE.md content for reviewer configuration and typed language info (Steps 1-2)
2. Build final agent list: start with core agents, apply skip/required rules, add custom agents
3. Launch all agents simultaneously in a single message (do NOT run sequentially)
4. After all agents complete, launch the verification agent with all findings
5. Present the final consolidated report to the user
6. Ask user about next steps using AskUserQuestion
7. If user chooses to fix, invoke /fix-review-issues with appropriate scope
