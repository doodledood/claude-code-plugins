# Discovery Log — improve writing skill from Wikipedia:Signs of AI writing

Task: Improve the writing plugin's skills by incorporating content from `https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing`. User said "maybe even save it as source or at least a full Md representation of it."

Domain: PROMPTING (modifying skill markdown files; no executable code changes). Compose with PROMPTING.md only (no CODING.md per task-file rules).

## Context Assessment

ALREADY UNDERSTOOD:
- [x] RESOLVED (from exploration): Writing plugin lives at `claude-plugins/writing/` v1.2.0
- [x] RESOLVED (from exploration): Existing `human-writing/SKILL.md` already covers significant overlap — kill-list vocabulary (delve/tapestry/landscape/etc.), em-dashes, structural anti-patterns, model-specific tells
- [x] RESOLVED (from exploration): Existing `references/ai-tells-and-fingerprints.md` has the deep research catalog
- [x] RESOLVED (from exploration): Branch is clean — no commits ahead of base
- [x] RESOLVED (from CLAUDE.md): Plugin version bump policy (minor for new feature)
- [x] RESOLVED (from CLAUDE.md): README sync checklist (root, plugin-list, plugin-readme)
- [x] RESOLVED (from PROMPTING.md): Defaults — high-signal changes only, progressive disclosure (references vs SKILL.md), description-as-trigger

GAPS IDENTIFIED:
- [x] RESOLVED (user): Source acquisition — user saves article markdown to `/tmp/signs-of-ai-writing.md`
- [x] RESOLVED (user): Placement — fold Wikipedia content into restructured `references/ai-tells-and-fingerprints.md`; no new wikipedia-signs.md file
- [x] RESOLVED (user): Reviewer scope — extend writing-reviewer.md to detect new patterns
- [x] RESOLVED (user): Wikipedia-specific signs — keep all, label context (apply only when context fits)
- [x] RESOLVED (user): Verbatim archive — distill only, don't commit `/tmp/signs-of-ai-writing.md` to repo
- [x] RESOLVED (user): Attribution NOT required — user explicitly said it's not important; skip CC BY-SA encoding as INV
- [x] RESOLVED (user): Top-tier SKILL.md additions — era-tracked vocab note, heading capitalization, curly quotes, 'moreover', encyclopedic-promotional drift, excessive boldface
- [x] RESOLVED (user): Era-tracked vocabulary — keep era labels with date ranges in references; SKILL.md gets unified pointer
- [x] RESOLVED (user): Reviewer calibration — frequency-aware / judgment (not strict-flag-every-instance)
- [x] RESOLVED (user): Mental model alignment — confirmed "yes that's right"
- [x] RESOLVED (user): Skill is for AI consumption — encode PG that content optimizes for LLM-readable structure
- [x] RESOLVED (user): Process risks — encode regression guard (INV) and scope creep guard (PG); skip era date-stamped PG (not selected)

## Wikipedia article content (partial — gathered from WebSearch summaries; full text not directly accessible from this environment)

Distinct additions vs current human-writing/SKILL.md:
- Era-tracked vocabulary (GPT-4 era 2023–mid-2024 vs GPT-4o era mid-2024–mid-2025; "delve" peaked then dropped)
- Encyclopedic-tone-yet-promotional drift; travel-guide prose; "breathtaking" puffery
- Heading capitalization (title case all main words)
- Skipping level-2 headings (start at `===`)
- Excessive boldface as "key takeaways"
- Curly quotes vs straight quotes — ChatGPT/DeepSeek use curly, Gemini/Claude do not
- Statistical regression to mean — smoothing facts to generic
- Subject puffery — arbitrary aspects representing broader topics
- "Moreover" overuse
- "Myths busted" / contrast-and-correct rhetorical pattern
- Wikipedia-specific: echoing notability guideline language ("independent coverage")
- Caveat: combination of signs matters; humans also produce these patterns sometimes

## Pending Resolvable Items (from PROMPTING.md)

Quality gates (auto-included as INV-G*):
- [x] RESOLVED: change-intent-reviewer no LOW+
- [x] RESOLVED: prompt-reviewer no MEDIUM+
- [x] RESOLVED: Folder architecture (skill is directory) — applies if any new skill or reference added
- [x] RESOLVED: Progressive disclosure — references vs front-loaded
- [x] RESOLVED: Description-as-trigger — applies if SKILL.md description changes

PROMPTING Defaults (auto-included as PG-*):
- [x] RESOLVED: High-signal changes only — every addition addresses real gap
- [x] RESOLVED: Calibrate emotional tone — keep prompts at trusted-advisor register
- [x] RESOLVED: Identify skill type — this is a Code Quality / Verification skill (catalog of patterns)

PROMPTING risks/scenarios — resolutions:
- [x] RESOLVED: Context rot — addressed by R-4 (length guard) + AC-2.5 (progressive disclosure check)
- [x] RESOLVED: Regression on update — addressed by INV-G1, INV-G2, INV-G3 (preservation guards on each modified file)
- [x] RESOLVED: Composition conflict — addressed by D3 (reviewer extension wired to D1/D2 patterns)
- [x] RESOLVED: Over-engineering on update — addressed by PG-2 (high-signal additions only) + AC-2.5 (length boundary)
- [x] RESOLVED: Edge case — Wikipedia-specific signs that don't apply to general prose — addressed by PG-4 (context labels) + AC-1.5 (label requirement) + AC-3.3 (reviewer skips for non-encyclopedic context)

## Style Shift Log

User invoked /auto mid-/define and reaffirmed "Go autonomous. Don't ask me stuff unless critical." → switching from thorough to autonomous mode. From this point: resolve open items myself with sensible defaults; auto-approve summary; proceed to /do.

## Autonomous Resolutions (verifier-feedback round 2)

- [x] RESOLVED (auto): AC vocabulary lists are FLOORS — /do may add high-signal patterns from the actual article beyond the enumerated ones, as long as enumerated items are present (encoded as ASM-6).
- [x] RESOLVED (auto): Hard-coded model-attribution wording softened — verify-prompts now require model-specific note "as stated in the source article" rather than hard-coding a particular phrasing.
- [x] RESOLVED (auto): INV-G6 bash command rewritten to print `FAIL: <files>` on scope leak vs `PASS` on clean.
- [x] RESOLVED (auto): File-content validity check added — new AC under D1 makes /do verify `/tmp/signs-of-ai-writing.md` is non-trivial AND contains identifiable Wikipedia:Signs-of-AI-writing structure before proceeding.
- [x] RESOLVED (auto): PG-7 tone calibration — added explicit subagent AC checking tone match across D1/D2/D3 additions.
- [x] RESOLVED (auto): D2 placement — added brief placement-mapping note specifying which existing SKILL.md section each new pattern slots into.
