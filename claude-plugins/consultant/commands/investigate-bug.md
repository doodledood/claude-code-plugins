---
description: Deep bug investigation using consultant agent. Identifies root causes, traces execution flow, assesses blast radius, and provides fix suggestions.
---

Perform deep bug investigation using the consultant agent with the following prompt:

---

# Bug Investigation Prompt

## Investigation Focus

1. **Root Cause Identification**: What's actually broken and why
2. **Execution Flow Tracing**: Path from trigger to failure
3. **State Analysis**: Invalid states, race conditions, timing issues
4. **Data Validation**: Input validation gaps, edge cases
5. **Error Handling**: Missing error handlers, improper recovery

## Severity Assessment

- **CRITICAL**: Production down, data corruption, widespread impact
- **HIGH**: Core functionality broken, major user impact
- **MEDIUM**: Feature partially broken, workaround available
- **LOW**: Minor issue, limited impact
- **INFO**: Observation, potential issue, monitoring needed

---

*End of consultant prompt.*

## Implementation Note

Use the Task tool with `subagent_type='consultant:consultant'`. The agent will gather symptoms, append them to the prompt above, invoke the consultant CLI, and report root cause analysis.
