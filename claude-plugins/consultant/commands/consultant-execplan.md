---
description: Create comprehensive execution plans using consultant-consulter agent for deep analysis and specification design. Gathers codebase context, analyzes patterns, and provides detailed implementation steps with validation criteria using any LiteLLM-compatible model.
---

# Consultant ExecPlan Command

## Usage

```bash
/consultant-execplan [FEATURE="feature description"] [GOAL="objective"] [MODEL=model-name] [BASE_URL=http://localhost:8000]
```

## Parameters

- `FEATURE` (optional): Feature or change to plan (if not provided, inferred from context/branch name)
- `GOAL` (optional): High-level objective or success criteria
- `MODEL` (optional): Specific LLM model to use (default: auto-select best model)
- `BASE_URL` (optional): Custom LiteLLM base URL (default: use default provider)

## What It Does

This command invokes the consultant-consulter agent to create comprehensive execution plans using powerful LLM models via LiteLLM. The agent will:

1. Gather comprehensive codebase context
2. Analyze existing patterns and architecture
3. Identify dependencies and integration points
4. Break down work into small, shippable chunks
5. Provide detailed implementation steps
6. Include validation criteria and testing strategies

## Output

The execution plan provides:

- **Implementation Steps**: Detailed, ordered tasks with dependencies
- **Architecture Analysis**: Existing patterns and integration points
- **File Organization**: Where to make changes and why
- **Validation Criteria**: How to verify correctness at each step
- **Testing Strategy**: Unit tests, integration tests, edge cases
- **Decision Logs**: Key architectural choices and rationale

## Examples

### Basic Usage

```bash
/consultant-execplan
```

Infers feature from branch name and git history.

### Explicit Feature

```bash
/consultant-execplan FEATURE="Add rate limiting to API" GOAL="Prevent API abuse"
```

Plans specific feature with clear objective.

### Custom Model

```bash
/consultant-execplan FEATURE="Implement caching layer" MODEL=claude-3-5-sonnet-20241022
```

Uses specific Claude model for planning.

### Custom LiteLLM Server

```bash
/consultant-execplan BASE_URL=http://localhost:8000
```

Uses local LiteLLM instance with automatic model selection.

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

[Additional decisions...]

## Risks & Mitigations

- **Risk 1**: [Description]
  - **Mitigation**: [How to address]
- **Risk 2**: [Description]
  - **Mitigation**: [How to address]
```

## Environment Variables

- `LITELLM_API_KEY` or `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: API key for the provider
- `CONSULTANT_MODEL`: Default model if not specified in command
- `CONSULTANT_BASE_URL`: Default base URL if not specified in command

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

**Tip**: The more context you provide in FEATURE and GOAL, the more detailed and accurate the plan.

## Session Management

The consultant-consulter agent runs the planning asynchronously. You can:

- View progress in real-time (agent waits for completion)
- Check session status: `python3 {consultant_scripts_path}/oracle_cli.py session <slug>`
- Review execution plan after completion

## Troubleshooting

**Issue**: "Plan is too high-level"

**Solution**: Provide more details in FEATURE parameter. Include specific requirements, constraints, or technical approach.

**Issue**: "Context limit exceeded"

**Solution**: Planning is gathering too much code. Agent will automatically focus on most relevant files. Consider narrowing FEATURE scope.

**Issue**: "No API key provided"

**Solution**: Set one of: `LITELLM_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY`

## Relationship to Other Commands

- **/consultant-review**: Use AFTER implementation to validate changes
- **/consultant-investigate-bug**: Use BEFORE execplan if fixing complex bugs
- **/consultant-execplan**: Use BEFORE implementation to plan approach

## Implementation

This command invokes the Task tool with `subagent_type='consultant-consulter'` and provides the feature description, goal, model, and base URL as context. The agent adapts its workflow for execution planning vs PR review.
