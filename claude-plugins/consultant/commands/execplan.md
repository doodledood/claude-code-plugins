---
description: Create comprehensive execution plans using consultant agent for deep analysis and specification design.
---

Create a comprehensive execution plan using the consultant agent with the following prompt:

---

# Execution Plan Prompt

## Planning Focus

1. **Architecture**: How to integrate with existing systems
2. **Implementation**: Step-by-step breakdown of work
3. **Validation**: How to verify correctness at each step
4. **Testing**: Comprehensive test strategy
5. **Risk Mitigation**: Edge cases, rollback plan

## Plan Quality

Ensure the execution plan is:

- **Detailed**: Specific files, functions, and code patterns
- **Ordered**: Clear dependencies and sequencing
- **Testable**: Each step has validation criteria
- **Practical**: Implementable with current codebase
- **Risk-Aware**: Identifies potential issues and mitigations

---

*End of consultant prompt.*

## Implementation Note

Use the Task tool with `subagent_type='consultant:consultant'`. The agent will gather codebase context, append it to the prompt above, invoke the consultant CLI, and report the detailed plan.
