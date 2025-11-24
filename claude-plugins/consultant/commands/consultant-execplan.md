---
description: Create comprehensive execution plans using consultant-consulter agent for deep analysis and specification design. Gathers codebase context, analyzes patterns, and provides detailed implementation steps with validation criteria.
---

# Consultant ExecPlan Command

Creates comprehensive execution plans using the consultant-consulter agent.

## What It Does

Invokes the consultant-consulter agent to create a detailed implementation plan:

1. Gathers comprehensive codebase context
2. Analyzes existing patterns and architecture
3. Identifies dependencies and integration points
4. Breaks down work into small, shippable chunks
5. Invokes the consultant CLI (agent will run --help first to learn current arguments)
6. Provides detailed implementation steps with validation criteria

## Output

The execution plan provides:

- **Implementation Steps**: Detailed, ordered tasks with dependencies
- **Architecture Analysis**: Existing patterns and integration points to follow
- **File Organization**: Where to make changes and why
- **Validation Criteria**: How to verify correctness at each step
- **Testing Strategy**: Unit tests, integration tests, edge cases
- **Decision Logs**: Key architectural choices and rationale
- **Risks & Mitigations**: Potential issues and how to address them
- **Metadata**: Model used, reasoning effort, tokens consumed, cost

## What Gets Analyzed

The consultant-consulter agent analyzes:

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

## When to Use

**Perfect for:**

- Complex features requiring careful planning
- Refactoring large systems
- Architectural changes with broad impact
- Features touching unfamiliar parts of codebase
- Critical production changes requiring validation plan
- Projects needing detailed implementation roadmap

**Not needed for:**

- Simple bug fixes with obvious solutions
- Trivial features (e.g., add new field to form)
- Well-understood changes you've done many times
- Experimental/spike work

## Plan Quality

The execution plan will be:

- **Detailed**: Specific files, functions, and code patterns
- **Ordered**: Clear dependencies and sequencing
- **Testable**: Each step has validation criteria
- **Practical**: Implementable with current codebase
- **Risk-Aware**: Identifies potential issues and mitigations

## Using the Plan

After receiving the plan:

1. **Review**: Ensure it aligns with your understanding
2. **Refine**: Ask consultant for clarification or adjustments
3. **Implement**: Follow steps in order
4. **Validate**: Check validation criteria after each step
5. **Test**: Run tests as described
6. **Iterate**: Update plan based on discoveries

## Context Gathering

The agent will gather:

- Current branch name and git history
- Related files and their implementations
- Similar features in the codebase
- Test files and patterns
- Configuration and deployment scripts
- Documentation and architectural notes

**Tip**: The more context you provide about the feature and goals, the more detailed and accurate the plan.

## Environment Variables

The consultant CLI reads these environment variables (run the CLI with --help for full details):
- `LITELLM_API_KEY` or `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: API key for the provider

## Troubleshooting

**Issue**: "Plan is too high-level"
**Solution**: Provide more details about requirements, constraints, or technical approach.

**Issue**: "Context limit exceeded"
**Solution**: Agent will automatically focus on most relevant files. Consider narrowing the feature scope.

**Issue**: "No API key provided"
**Solution**: Set one of: `LITELLM_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`

## Relationship to Other Commands

- **/consultant-review**: Use AFTER implementation to validate changes
- **/consultant-investigate-bug**: Use BEFORE execplan if fixing complex bugs
- **/consultant-execplan**: Use BEFORE implementation to plan approach

## Implementation

This command invokes the Task tool with `subagent_type='consultant-consulter'` for an execution planning task. The agent will:
1. Run `--help` on the CLI to learn current arguments
2. Gather codebase context and similar implementations
3. Construct a planning prompt with appropriate role and focus areas
4. Invoke the CLI and parse the structured output
5. Report detailed execution plan with metadata back to user
