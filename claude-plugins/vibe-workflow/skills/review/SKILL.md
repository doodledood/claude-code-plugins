---
name: review
description: Run all code review agents in parallel (bugs, coverage, maintainability, simplicity, type-safety if typed, CLAUDE.md adherence, docs). Respects CLAUDE.md reviewer configuration.
---

Run a comprehensive code review. First detect the codebase type, then launch appropriate agents.

**Flags**: `--autonomous` → skip Step 5 user prompt, return report only (for programmatic invocation)

## Step 1: Check CLAUDE.md Reviewer Configuration

Before launching agents, check if any loaded CLAUDE.md files contain reviewer configuration. CLAUDE.md files are auto-loaded into context—do NOT search for them.

**Look for a `## Review Configuration` or `## Code Review` section in loaded CLAUDE.md content that specifies:**

```markdown
## Review Configuration

### Skip Reviewers
<!-- Reviewers to never run in this project -->
- type-safety (untyped codebase)
- docs (no documentation requirements)

### Required Reviewers
<!-- Always run these, even if normally conditional -->
- type-safety

### Custom Reviewers
<!-- Project-specific review agents to add -->
- name: security-reviewer
  agent: security-audit-agent
  description: Check for OWASP vulnerabilities
- name: api-consistency
  agent: api-review-agent
  description: Verify API follows REST conventions
```

**Configuration precedence:**
1. `Skip Reviewers` - Remove these from the agent list entirely
2. `Required Reviewers` - Add these even if detection would skip them
3. `Custom Reviewers` - Append these to the agent list

**Valid reviewer names for skip/required:**
- `bugs` or `code-bugs-reviewer`
- `coverage` or `code-coverage-reviewer`
- `maintainability` or `code-maintainability-reviewer`
- `simplicity` or `code-simplicity-reviewer`
- `testability` or `code-testability-reviewer`
- `claude-md-adherence` or `claude-md-adherence-reviewer`
- `docs` or `docs-reviewer`
- `type-safety` or `type-safety-reviewer`

**If no configuration found:** Proceed with default behavior (all core agents + type-safety if typed).

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

**Build the final agent list by applying CLAUDE.md configuration (if found):**

### Default Core Agents (launch IN PARALLEL unless skipped):

1. **code-bugs-reviewer** - Audit for logical bugs, race conditions, edge cases
2. **code-coverage-reviewer** - Verify test coverage for code changes
3. **code-maintainability-reviewer** - Check for DRY violations, dead code, coupling
4. **code-simplicity-reviewer** - Check for over-engineering, premature optimization, cognitive complexity
5. **code-testability-reviewer** - Identify code requiring excessive mocking to test
6. **claude-md-adherence-reviewer** - Verify compliance with CLAUDE.md project standards
7. **docs-reviewer** - Audit documentation and code comments accuracy

### Conditional Agent:

8. **type-safety-reviewer** - Audit type safety, any/unknown abuse, invalid states
   - **Include if:** Listed in `Required Reviewers`, OR typed language detected (Step 2)
   - **Exclude if:** Listed in `Skip Reviewers`
   - **Primary:** TypeScript, Python with type hints (agent is optimized for these)
   - **Also useful for:** Java, Kotlin, Go, Rust, C#, Swift, Scala (core principles apply)
   - **Skip for:** Plain JavaScript, Ruby, PHP, shell scripts, untyped Python

### Custom Agents (from CLAUDE.md):

9. **Any agents listed in `Custom Reviewers`** - Launch these with the specified agent name and description

**Applying configuration:**
- Remove any agent listed in `Skip Reviewers` from the final list
- Add `type-safety-reviewer` if listed in `Required Reviewers` (even if detection would skip it)
- Append all `Custom Reviewers` to the final list

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
- **Critical/High only**: `Skill("vibe-workflow:fix-review-issues", "--severity critical,high")`
- **All issues**: `Skill("vibe-workflow:fix-review-issues")`
- **Skip**: End workflow

## Execution

1. Check loaded CLAUDE.md content for reviewer configuration and typed language info (Steps 1-2)
2. Build final agent list: start with core agents, apply skip/required rules, add custom agents
3. Launch all agents simultaneously in a single message (do NOT run sequentially)
4. After all agents complete, launch the verification agent with all findings
5. Present the final consolidated report to the user
6. Ask user about next steps using AskUserQuestion
7. If user chooses to fix, invoke /fix-review-issues with appropriate scope
