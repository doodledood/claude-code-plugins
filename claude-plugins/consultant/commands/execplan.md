---
description: Create comprehensive execution plans using consultant agent for deep analysis and specification design. Gathers codebase context, analyzes patterns, and provides detailed implementation steps with validation criteria.
---

Create a comprehensive execution plan using the consultant agent.

## What to Do

Invoke the consultant agent to create a detailed implementation plan:

1. Gather comprehensive codebase context
2. Analyze existing patterns and architecture
3. Identify dependencies and integration points
4. Break down work into small, shippable chunks
5. Invoke the consultant CLI (run --help first to learn current arguments)
6. Provide detailed implementation steps with validation criteria

## Output

Provide:

- **Implementation Steps**: Detailed, ordered tasks with dependencies
- **Architecture Analysis**: Existing patterns and integration points to follow
- **File Organization**: Where to make changes and why
- **Validation Criteria**: How to verify correctness at each step
- **Testing Strategy**: Unit tests, integration tests, edge cases
- **Decision Logs**: Key architectural choices and rationale
- **Risks & Mitigations**: Potential issues and how to address them
- **Metadata**: Model used, reasoning effort, tokens consumed, cost

## What Gets Analyzed

Analyze:

1. **Codebase Structure**: Existing architecture, patterns, conventions
2. **Related Features**: Similar implementations, reusable components
3. **Dependencies**: External libraries, internal modules, integrations
4. **Data Models**: Database schemas, API contracts, type definitions
5. **Test Coverage**: Existing test patterns, test infrastructure
6. **Deployment**: CI/CD pipelines, config management, rollout strategy

## Planning Focus Areas

1. **Architecture**: How to integrate with existing systems
2. **Implementation**: Step-by-step breakdown of work
3. **Validation**: How to verify correctness at each step
4. **Testing**: Comprehensive test strategy
5. **Deployment**: Rollout plan and monitoring
6. **Risk Mitigation**: Edge cases, rollback plan, validation

## Output Format

```
# Execution Plan: [Feature Name]

## Overview
[1-paragraph summary of feature and approach]

## Goals
- [Objective 1]
- [Objective 2]

## Architecture Analysis

### Existing Patterns
[How current system works, what patterns to follow]

### Integration Points
[Where this feature touches existing code]

### Dependencies
[External and internal dependencies]

## Implementation Steps

### Phase 1: [Phase Name]
**Goal**: [What this phase accomplishes]

#### Task 1.1: [Task Name]
- **File**: path/to/file.ts
- **Changes**: [Specific code changes]
- **Why**: [Rationale]
- **Validation**: [How to verify]
- **Tests**: [Test scenarios]

[Additional tasks...]

### Phase 2: [Phase Name]
[Similar structure...]

## Testing Strategy

### Unit Tests
- [ ] Test scenario 1
- [ ] Test scenario 2

### Integration Tests
- [ ] Integration scenario 1
- [ ] Integration scenario 2

### Edge Cases
- [ ] Edge case 1
- [ ] Edge case 2

## Validation Criteria

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
- [ ] Performance benchmark met
- [ ] Security review passed

## Deployment Plan

1. [Step 1: e.g., Deploy to staging]
2. [Step 2: e.g., Run smoke tests]
3. [Step 3: e.g., Gradual rollout]
4. [Step 4: e.g., Monitor metrics]

## Decision Log

### Decision 1: [Decision Name]
**Context**: [Why this decision was needed]
**Options Considered**: [Alternatives]
**Choice**: [What was chosen]
**Rationale**: [Why this choice]

## Risks & Mitigations

- **Risk 1**: [Description]
  - **Mitigation**: [How to address]
- **Risk 2**: [Description]
  - **Mitigation**: [How to address]
```

## Plan Quality

Ensure the execution plan is:

- **Detailed**: Specific files, functions, and code patterns
- **Ordered**: Clear dependencies and sequencing
- **Testable**: Each step has validation criteria
- **Practical**: Implementable with current codebase
- **Risk-Aware**: Identifies potential issues and mitigations

## Context Gathering

Gather:

- Current branch name and git history
- Related files and their implementations
- Similar features in the codebase
- Test files and patterns
- Configuration and deployment scripts
- Documentation and architectural notes

## Implementation

Invoke the Task tool with `subagent_type='consultant:consultant'` for an execution planning task. The agent will:
1. Run `--help` on the CLI to learn current arguments
2. Gather codebase context and similar implementations
3. Construct a planning prompt with appropriate role and focus areas
4. Invoke the CLI and parse the structured output
5. Report detailed execution plan with metadata back to user
