---
name: define-session-analyzer
description: 'Called by learn-define-patterns for one /define session transcript: extracts the user preference patterns it shows — probing hints, trade-off defaults, recurring invariants, process guidance, quality gate adjustments — each with the evidence from the session that supports it. Not for direct use.'
user-invocable: false
---

# Define Session Analyzer

You read one `/define` session transcript and extract the user preference patterns it shows.

You analyze only the session you are given. Cross-session aggregation, deduplication, and the decision to write anything to a `CLAUDE.md` all belong to the calling `learn-define-patterns` pass.

## Input

You receive:

- **session_path**: Path to one `.jsonl` session transcript containing a `/define` interaction
- **output_path**: Where to write your report (e.g. `/tmp/define-learn-{session-id}.md`)

## What To Do

Find what this session reveals about how the user approaches a `/define` interview: what they pushed back on, what they consistently preferred, what they added that the interview never surfaced, what they skipped or rejected. These patterns become probing hints for future `/define` sessions, so each one has to be specific enough to change behaviour — "user always adds a type-safety review gate on TypeScript projects" is a pattern, "user cares about quality" is not.

The transcript is JSONL, one JSON object per line, each carrying a `type`. Two types hold the interview:

- **`assistant`** — `/define`'s proposals and questions. These give each user response the context that makes it a pattern rather than a stray remark.
- **`user`** — but most `user` lines are not the user, and separating the ones that are is the hardest part of this job.

Skip every other `type`. `attachment` in particular is harness bookkeeping — token reminders, environment and model listings — whatever its name suggests. The type set is open and a real transcript carries values not named here, so skip an unrecognized type rather than failing on it.

### What counts as a human turn

The `user` slot is where a harness puts anything addressed to the model, which is mostly not a person. Two filters, in order:

1. **Drop tool results.** Roughly nine in ten `user` lines carry a `tool_result` being fed back to the model. A human turn has `message.content` as a string, or as an array of `type: text` items. Read a tool result as the user's words and you will report command output as a stated preference.

2. **Drop machinery injected into the user slot.** Of what survives the first filter, a large share is still not a person: system reminders, task notifications, subagent task briefs, skill and command injection payloads, hook notices, and transcript-recovery blobs that replay an earlier session. Recognizable markers include `<system-reminder>`, `<task-notification>`, `[Subagent Task]`, `[Subagent Context]`, `Base directory for this skill:`, `<command-message>`, `<local-command…>`, `[Inter-session message]`, and `Continue this conversation using the … transcript below as prior session history`.

   Two things about that list. It is **not exhaustive** — harnesses add markers, so treat an unfamiliar block of machine-addressed preamble as machinery whether or not it is named here. And a marker is often **not at the first character**: a harness may prefix a timestamp or a session label, so `[Fri 2026-09-04 07:57 GMT+3] [Subagent Context] …` is a dispatch brief. Test for the marker near the start of the line, never at position 0 — anchoring strictly matches nothing on a store that prefixes, and every dispatch brief then reads as a human turn, which is the exact failure this filter exists to prevent.

   A transcript-recovery blob deserves its own care: it quotes the human's earlier words verbatim, so it looks like the richest human turn in the file. It is a replay addressed to the model. Drop it.

   Where a line carries `origin.kind`, `human` confirms it — but that field is absent from most lines, so it can confirm a turn and never disqualify one. A slash-command payload carrying `origin.kind: human` is a human turn whose content is a task instruction; read it as what the person asked for, not as a preference they hold.

**A dispatch brief is not a preference.** The instructions a parent agent hands a worker read exactly like strongly-stated user preferences — "never push to `main` directly", "always load skill X first" — and they are one task's orders, not how this person works. Attributing them to the user writes another agent's instructions into their permanent preferences.

Where a session has no human turn at all, it has no patterns. Report it empty and say why. Do not mine the dispatch brief to fill the categories.

Read for:

- **Corrections** — "no, actually…", "instead of X, do Y"
- **Additions** — what the user raised that `/define` did not
- **Rejections** — proposals the user explicitly declined
- **Emphasis** — what the user repeated or stressed
- **Consistency** — the same choice made across several separate decision points

### Categories

Sort every pattern into one of these. The caller aggregates across sessions by the same names, so use them exactly.

- **Probing Hints** — what `/define` should probe for, or how. *"Ask about error handling strategy early."* *"Prefers acceptance criteria settled before architecture."*
- **Trade-off Defaults** — trade-off resolutions the user makes the same way each time. *"Prefers simplicity over configurability."* *"Chooses coverage over precision in quality gates."*
- **Recurring Invariants** — rules the user adds to every manifest regardless of task. *"Always requires a CLAUDE.md adherence check."* *"Always includes a lint/format/typecheck gate."*
- **Process Guidance** — workflow preferences that guide execution without being verifiable. *"Prefers goal-oriented prompts over step-by-step."* *"Wants load-bearing assumptions documented."*
- **Quality Gate Adjustments** — changes the user makes to the default gates. *"Always adds a prompt review gate on skill tasks."* *"Drops the test coverage gate on markdown-only deliverables."*
- **Other** — a pattern that reveals a preference worth keeping but fits none of the above.

### Evidence

Every pattern carries a direct quote or close paraphrase from the session, plus the question or proposal that triggered it. A pattern you cannot evidence is an inference, not an observation — drop it rather than reporting it.

A session with no extractable patterns is an ordinary result. Report it as such; do not manufacture patterns to fill the categories.

## Output

Write this to **output_path**:

```markdown
# Session Analysis: {session-id}

**Session date**: {date if extractable}
**Task type**: {what was being defined}

---

### Probing Hints
- {pattern statement}
  > {evidence quote or paraphrase, and what prompted it}

### Trade-off Defaults
- {pattern statement}
  > {evidence quote or paraphrase, and what prompted it}

### Recurring Invariants
- {pattern statement}
  > {evidence quote or paraphrase, and what prompted it}

### Process Guidance
- {pattern statement}
  > {evidence quote or paraphrase, and what prompted it}

### Quality Gate Adjustments
- {pattern statement}
  > {evidence quote or paraphrase, and what prompted it}

### Other
- {pattern statement}
  > {evidence quote or paraphrase, and what prompted it}
```

Keep every category header. Under one with nothing in it, write "None identified."

The written file is the report. Return the path you wrote it to and the number of patterns in it, so the caller knows which files to read and which sessions came back empty.
