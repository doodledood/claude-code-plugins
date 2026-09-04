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
| **Standard markdown only** | Output uses ordinary markdown headers, `- ` bullets, and `<!-- date -->` HTML comments. No custom syntax, no YAML, no special parsing. |
| **Ask write target** | Ask the user which CLAUDE.md to write to: project CLAUDE.md, user `~/.claude/CLAUDE.md`, or both. Never assume. |
| **Resolve the target first** | Either CLAUDE.md may be a symlink onto a differently-named file. Resolve it, write through to the resolved file, and name that path in the diff preview, so the user approves a change to the file it actually lands in. |
| **Diff preview before write** | Show the user exactly what will be added or changed in the resolved target before writing. |
| **Clean up temp files** | Delete per-session analysis files from `/tmp/` after aggregation is complete. |

# Session Discovery

Session transcripts are JSONL files, one per session, grouped into a directory per project. Where your harness keeps them varies — on Claude Code they are `~/.claude/projects/{encoded-project-path}/{session-id}.jsonl`. Where you cannot find the store, ask the user for the directory rather than guessing at one.

Search every project directory, not the one whose name looks like this project. These preferences describe the user, not one repository, and they may be written to a user-level CLAUDE.md — so a `/define` interview run anywhere counts. Do not reconstruct an encoded directory name from a project path either: the encoding collapses `/` and `.` to the same character, so two different projects can produce one name. A session's id is its filename without the `.jsonl` extension; the `cwd` field carried on most lines tells you which project a session was working in, if you want to report that.

**A session qualifies** on two conditions, and it needs both.

*It invoked the define family.* Look for two signals, because harnesses use both and a rule covering one finds nothing on a machine using the other:

- A `<command-name>` value, such as `/manifest-dev:define`.
- An assistant `tool_use` named `Skill` whose `input.skill` names the skill, such as `openclaw-skills:just-define`.

Match on the final segment after any plugin namespace, and accept `just-define` alongside `define`.

*And a person spoke in it.* A `/define` invocation alone means nothing: the goal-based variants run unattended inside autonomous chains, and a subagent session carries its parent's dispatch brief in the user slot. Require at least one real human turn, as `define-session-analyzer/SKILL.md` defines one under **What counts as a human turn** — the same test the workers use. This is also what keeps subagent transcripts out, including the sidecar ones stored under a parent session's own directory; excluding them by where they sit misses the subagent sessions that sit at the top level.

Match nothing looser. The characters `/define` appear in this skill's own text, in directory listings, and in file paths — across this store, raw string hits outnumber real invocations by more than ten to one, and `<command-name>` itself appears as prose inside quoted tool descriptions.

Take the most recent qualifying sessions by their latest `timestamp`. `$ARGUMENTS` is substituted by whoever invokes this skill; where it names a session count use that, and where it arrives empty or unsubstituted take 10.

**No sessions found**: Tell the user: "No /define sessions found in recent session history. Run a few /define sessions first, then try again."

**Malformed files**: Skip with a warning noting which files were skipped and why.

# Per-Session Analysis

Each session is analyzed in its own fresh worker. Dispatch one worker per session file and give it, as its whole instructions, `define-session-analyzer/SKILL.md`. It sits beside this skill — `define-session-analyzer/SKILL.md` in the same skills directory, reachable as `.agents/skills/define-session-analyzer/SKILL.md` or `.claude/skills/define-session-analyzer/SKILL.md` from the root of the repository holding this file, which are the same file. Resolve it to an absolute path before handing it over; a worker starts somewhere you did not choose. Where your harness cannot hand a worker a file to follow, read the file yourself and pass its full contents instead — it is self-contained and refers to no other file.

Then give each worker the two inputs that skill's `## Input` section names: the session file path, and `/tmp/define-learn-{session-id}.md` as its output path. A worker needs to be able to read its session file and write that output file; give it whatever your harness calls those.

The separate context is the point: a worker that has read one session cannot carry another session's framing into it, so give each session its own worker even where one worker could carry several.

Each worker writes its report to the output path and returns that path with a pattern count. Wait for every worker to finish, then aggregate from the written files rather than from whatever a worker reported on the way out — the written file is the deliverable, and a returned count says which files hold patterns, not what those patterns are. A report fills empty categories with "None identified."; that is not a pattern, so do not carry it into the aggregate or count it as one.

Once they have all finished, look for a file at each worker's output path. A worker that left none there failed, whatever it returned on the way out. Treat that as an error and say so in the summary, counted separately from the sessions that ran fine and yielded nothing — fold the two together and a crashed worker reads as an ordinary empty session, which silently narrows the aggregate to whichever sessions happened to survive. Sessions with zero extractable patterns are themselves normal; count those in the final summary too.

# Aggregated Output

The final output is a unified set of user preferences derived from all analyzed sessions.

**Quality criteria for the aggregated output:**
- Patterns organized by the 5+1 categories (Probing Hints, Trade-off Defaults, Recurring Invariants, Process Guidance, Quality Gate Adjustments, Other)
- Semantically equivalent patterns across sessions consolidated into one, with frequency noted
- Contradictions between sessions surfaced with evidence from each side — user resolves
- Each pattern classified as "project-specific" (references specific files/variables/entities) or "generalizable" (references categories/principles/domains) — user decides which to keep. The per-session reports do not carry this classification; make the call yourself from each pattern statement and its evidence

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

Where the section does not exist yet, append it at the end of the file — but match the level the file uses for the sections it is divided into, and put the subcategories one level below that. Where a single `#` title sits above everything, that title is not a section; match its `##` siblings instead. The format block above shows `##` and `###` because that is the common case, not because the levels are fixed: appending a `##` heading to a file whose own sections are `#` nests these preferences inside whatever section happens to be last.

**Precedence**: When future `/define` sessions encounter a conflict between built-in task file guidance and patterns in `## /define Preferences`, the user's patterns represent intentional preferences and take precedence.

**Traceability**: Each pattern includes an inline `<!-- YYYY-MM-DD -->` date comment carrying the date it was written, not the date of the session it came from — a pattern seen across several sessions has no single session date. Users remove patterns by editing CLAUDE.md directly — no special tooling needed.

# Summary

After writing, output a summary: sessions analyzed, sessions with patterns (and sessions with zero patterns), workers that finished without leaving an analysis file, patterns extracted, patterns approved, contradictions found, and which CLAUDE.md was written to.
