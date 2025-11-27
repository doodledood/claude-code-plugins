---
description: Create comprehensive execution plans using consultant agent for deep analysis and specification design.
---

Create a comprehensive execution plan using the consultant agent.

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

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'` for an execution planning task. The agent will gather codebase context, construct the planning prompt, invoke the CLI, and report the detailed plan.
