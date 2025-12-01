---
description: Create comprehensive execution plans using consultant agent for deep analysis.
allowed-tools: ["Task"]
argument-hint: [feature or task to plan]
---

Create an execution plan for: $ARGUMENTS

---

Use the Task tool with `subagent_type='consultant:consultant'`. The agent gathers codebase context, invokes the consultant CLI, and reports the plan.

**Planning focus**:
1. **Architecture**: Integration with existing systems
2. **Implementation**: Step-by-step breakdown with dependencies
3. **Validation**: Verification criteria at each step
4. **Testing**: Comprehensive test strategy
5. **Risks**: Edge cases, rollback plan

**Plan quality requirements**:
- Specific files, functions, and code patterns
- Clear dependencies and sequencing
- Each step has validation criteria
- Practical with current codebase
- Identifies potential issues and mitigations
