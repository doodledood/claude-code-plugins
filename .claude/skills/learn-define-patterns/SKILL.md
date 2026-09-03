---
name: learn-define-patterns
description: 'Analyze recent /define sessions to extract user preference patterns and write them to CLAUDE.md. Use when you want to learn from past define sessions, extract define patterns, improve future defines, or capture define preferences.'
user-invocable: true
---

**User request**: $ARGUMENTS

# Goal

Analyze recent `/define` session transcripts, extract patterns in how the user approaches `/define` interviews (probing preferences, trade-off defaults, recurring invariants, process guidance, quality gate adjustments), and write generalizable patterns to CLAUDE.md as `## /define Preferences`. Future `/define` sessions see these preferences automatically because CLAUDE.md is loaded into context.

# Why This Matters

Every `/define` session, users make the same corrections, add the same invariants, resolve the same trade-offs. Without learning, each session starts from zero. This skill closes the feedback loop: patterns from past sessions become probing hints for future ones.

# Constraints

| Constraint | Rule |
|------------|------|
| **User approval required** | NEVER write to CLAUDE.md without presenting patterns to the user and getting explicit approval. |
| **Merge, never overwrite** | If a `## /define Preferences` section already exists, merge new patterns with existing ones. Never blindly overwrite. |
| **Semantic deduplication** | When merging, identify patterns that say the same thing in different words and consolidate them. Don't just check for exact text matches. |
| **Standard markdown only** | Output uses `##` headers, `###` subheaders, `- ` bullets, and `<!-- date -->` HTML comments. No custom syntax, no YAML, no special parsing. |
| **Ask write target** | Ask the user which CLAUDE.md to write to: project CLAUDE.md, user `~/.claude/CLAUDE.md`, or both. Never assume. |
| **Diff preview before write** | Show the user exactly what will be added or changed in CLAUDE.md before writing. |
| **Clean up temp files** | Delete per-session analysis files from `/tmp/` after aggregation is complete. |

# Session Discovery

Session JSONL files live at `~/.claude/projects/{project-path-encoded}/{session-id}.jsonl`. Find recent sessions containing `/define` activity. If `$ARGUMENTS` specifies a session count, use that; otherwise use enough recent sessions for meaningful pattern signal.

**No sessions found**: Tell the user: "No /define sessions found in recent session history. Run a few /define sessions first, then try again."

**Malformed files**: Skip with a warning noting which files were skipped and why.

# Per-Session Analysis

Analyze each session in its own fresh worker — one worker per session, all running independently.

Each worker's instructions are the `define-session-analyzer` skill, which lives at `.claude/skills/define-session-analyzer/SKILL.md` relative to the repository root. (`.agents/skills/define-session-analyzer/SKILL.md` is a symlink to that same file; either path reaches it.) If your harness can hand a worker a file to follow, give it that path. If it cannot, read the file yourself and pass its full contents as the worker's instructions — it is self-contained and refers to no other file.

Give each worker the two inputs that skill's `## Input` section names: the path to one session `.jsonl` file, and the output path `/tmp/define-learn-{session-id}.md`, where `{session-id}` is that session file's name without the `.jsonl` extension. Each worker needs to be able to read its session file and write that output file; give it whatever your harness calls those.

Aggregate from the written files rather than from whatever a worker reports on finishing — the written file is the deliverable. A worker that leaves no file at its output path failed; treat that as an error and say so in the summary, separately from the sessions that ran fine and yielded nothing.

The separate context is the point: it keeps the patterns found in one session from anchoring how the next one is read. Give every session its own worker even where one worker could carry two.

Sessions with zero extractable patterns are normal — count them in the final summary.

# Aggregated Output

The final output is a unified set of user preferences derived from all analyzed sessions.

**Quality criteria for the aggregated output:**
- Patterns organized by the 5+1 categories (Probing Hints, Trade-off Defaults, Recurring Invariants, Process Guidance, Quality Gate Adjustments, Other)
- Semantically equivalent patterns across sessions consolidated into one, with frequency noted
- Contradictions between sessions surfaced with evidence from each side — user resolves
- Each pattern classified as "project-specific" (references specific files/variables/entities) or "generalizable" (references categories/principles/domains) — user decides which to keep

**What the user sees before approving:**
- Pattern statement, session frequency, project-specific vs generalizable flag, any contradictions
- Batch selection (not per-pattern approval)
- Choice of write target: project CLAUDE.md, user `~/.claude/CLAUDE.md`, or both
- Diff/preview of exact changes before writing

# CLAUDE.md Output Format

```markdown
## /define Preferences

### Probing Hints
- Pattern statement here <!-- 2026-03-01 -->

### Trade-off Defaults
- Pattern statement here <!-- 2026-03-01 -->

### Recurring Invariants
- Pattern statement here <!-- 2026-03-01 -->

### Process Guidance
- Pattern statement here <!-- 2026-03-01 -->

### Quality Gate Adjustments
- Pattern statement here <!-- 2026-03-01 -->

### Other
- Pattern statement here <!-- 2026-03-01 -->
```

When merging with an existing `## /define Preferences` section: preserve all existing patterns and their date comments, deduplicate new patterns against existing ones by meaning (not just text match), add new patterns under the appropriate subcategory headers, and omit empty subcategories.

**Precedence**: When future `/define` sessions encounter a conflict between built-in task file guidance and patterns in `## /define Preferences`, the user's patterns represent intentional preferences and take precedence.

**Traceability**: Each pattern includes an inline `<!-- YYYY-MM-DD -->` date comment. Users remove patterns by editing CLAUDE.md directly — no special tooling needed.

# Summary

After writing, output a summary: sessions analyzed, sessions with patterns (and sessions with zero patterns), patterns extracted, patterns approved, contradictions found, and which CLAUDE.md was written to.
