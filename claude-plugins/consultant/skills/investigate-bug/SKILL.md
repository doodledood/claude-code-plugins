---
name: investigate-bug
description: "Deep bug investigation via the consultant agent and external LLM analysis. Gathers symptoms, traces execution flow, identifies root causes, and proposes targeted fixes with regression test plans. Use when the user asks to debug, troubleshoot, investigate errors, exceptions, crashes, race conditions, or unexpected behavior."
---

Investigate bug: $ARGUMENTS

---

Launch the consultant:consultant agent to perform deep root-cause analysis via external LLM consultation.

## Workflow

1. **Gather symptoms** — collect error messages, stack traces, reproduction steps, and relevant git history from the user's description and codebase
2. **Identify scope** — determine affected files, services, and blast radius
3. **Invoke consultant agent** — the agent gathers full context (diffs, related files, architecture docs), constructs a focused investigation prompt, and delegates analysis to the consultant CLI
4. **Relay findings** — present the root-cause analysis, execution flow trace, and recommended fix verbatim from the consultant output

## Expected output format

The consultant agent produces a structured bug investigation report including:

- **Root cause**: specific file, line range, and explanation of the defect
- **Execution flow**: step-by-step trace from trigger to failure
- **Blast radius**: affected systems, users, and data integrity concerns
- **Recommended fix**: concrete code changes with rationale
- **Regression test plan**: test scenarios to prevent recurrence
