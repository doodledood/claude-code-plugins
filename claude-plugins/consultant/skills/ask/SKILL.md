---
name: ask
description: Single-model consultation using consultant agent. Defaults to gpt-5.2-pro.
---

Consult an external model about: $ARGUMENTS

---

Use the Task tool with `subagent_type='consultant:consultant'`. Pass the question/topic above as the consultant prompt.

**Defaults**:
- Model: `gpt-5.2-pro` (unless user specifies another, e.g., "use claude-opus-4-5-20251101 to...")
- Single-model mode

The agent handles context gathering, CLI invocation, and response relay.
