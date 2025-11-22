# Oracle Plugin

Comprehensive code analysis plugin using the oracle CLI tool for deep AI-powered reviews, architectural analysis, bug investigation, and execution planning.

## Overview

Oracle is a CLI tool that provides access to more powerful AI models for complex analysis tasks. This plugin bundles the complete oracle workflow including agent, commands, and skills for code review, bug investigation, and execution planning.

## Components

### Agent: oracle-consulter

Expert agent for leveraging high-token AI analysis through the oracle CLI tool. Handles the full workflow from context gathering to findings synthesis.

**Use when you need:**
- Comprehensive PR reviews before production deployment
- Deep architectural validation
- Complex bug root cause analysis

### Commands

#### `/oracle-review`
Production-level PR reviews with severity-tagged findings, regression test guidance, and security validation.

**Usage:**
```bash
/oracle-review
# Or with custom PR reference:
/oracle-review PR_REF=origin/main...feature-branch
```

**What it does:**
- Reviews code changes comprehensively
- Provides severity-tagged findings (BLOCKER/HIGH/MEDIUM/LOW/INFO)
- Suggests specific fixes with file references
- Recommends regression tests
- Validates security and architectural concerns

#### `/oracle-investigate-bug`
Deep bug investigation with root cause analysis and fix recommendations.

**Usage:**
```bash
/oracle-investigate-bug
# The command will infer bug details from context or ask for clarification
```

**What it does:**
- Identifies root cause of bugs
- Traces execution flow from symptom to source
- Assesses blast radius and impact
- Provides concrete fix suggestions
- Recommends regression tests to prevent recurrence

#### `/oracle-execplan`
Create comprehensive execution plans using oracle CLI tool for deep analysis and specification design.

**Usage:**
```bash
/oracle-execplan
# Infers feature context from branch name and git history

# Or with explicit parameters:
/oracle-execplan FEATURE="Add rate limiting" GOAL="Prevent API abuse"
```

**What it does:**
- Invokes oracle-consulter agent for deep planning analysis
- Gathers comprehensive codebase context
- Creates detailed, self-contained execution plans following PLANS.md methodology
- Provides living document structure with decision logs and discovery tracking
- Breaks down work into small, shippable chunks with clear dependencies

### Skill: oracle

Contextual skill providing oracle CLI knowledge and best practices.

**Activated automatically when:**
- Discussing complex analysis needs
- Questions about oracle capabilities
- Architectural review requirements
- Security audit planning

**Provides:**
- Oracle CLI usage patterns
- File glob patterns for different analysis types
- Session management guidance
- Best practices for prompt engineering

## Installation

```bash
# Add marketplace
/plugin marketplace add https://github.com/doodledood/claude-code-plugins

# Install oracle plugin
/plugin install oracle@claude-code-plugins-marketplace
```

## Requirements

- `OPENAI_API_KEY` environment variable must be set
- OR use oracle's `--engine browser` mode
- Node.js/npx available for running oracle CLI

## Quick Start

### 1. Review a Pull Request

```bash
/oracle-review
```

The command will automatically:
- Determine your PR reference (origin/master...HEAD)
- Gather all changed files with context
- Invoke oracle for comprehensive analysis
- Monitor the session until completion
- Provide actionable findings

### 2. Investigate a Bug

```bash
/oracle-investigate-bug
```

Provide bug details when prompted, or let it infer from:
- Recent test failures
- Error messages in conversation
- Git history and recent changes

### 3. Create an Execution Plan

```bash
/oracle-execplan
```

Creates a comprehensive execution plan with oracle's deep analysis capabilities:
- Analyzes codebase patterns and architecture
- Identifies dependencies and integration points
- Provides detailed implementation steps
- Includes validation criteria and testing strategies

## Example Workflows

### Production PR Review

```bash
# On your feature branch:
git checkout feature/user-authentication

# Run comprehensive review:
/oracle-review

# Oracle will analyze and provide:
# - Must-fix items (BLOCKER + HIGH)
# - Follow-up suggestions (MEDIUM + LOW)
# - Regression test recommendations
# - Overall risk assessment
```

### Bug Investigation

```bash
# After discovering a bug:
/oracle-investigate-bug

# Provide symptoms like:
# "API returns 500 on user profile update with error: Cannot read property 'id' of undefined"

# Oracle will:
# - Identify root cause with file:line references
# - Trace execution flow
# - Assess blast radius
# - Suggest concrete fixes
# - Recommend regression tests
```

### Execution Planning

```bash
# Planning a complex feature:
/oracle-execplan FEATURE="Add rate limiting to API" GOAL="Prevent API abuse"

# Oracle will:
# - Gather comprehensive codebase context
# - Analyze existing patterns and architecture
# - Create detailed execution plan following PLANS.md methodology
# - Break down work into small, testable chunks
# - Provide validation steps and acceptance criteria
# - Include decision logs for key architectural choices
```

## How Oracle Works

1. **Context Gathering**: Collects relevant files, diffs, and documentation
2. **Artifact Organization**: Creates structured, numbered attachments
3. **Prompt Engineering**: Constructs detailed analysis prompts
4. **Oracle Invocation**: Runs via `npx -y @steipete/oracle@latest`
5. **Session Monitoring**: Polls every 30s until completion
6. **Findings Synthesis**: Transforms output into actionable recommendations

## When to Use Oracle

**Perfect for:**
- Complex architectural decisions
- Security vulnerability analysis
- Comprehensive code reviews across large codebases
- Understanding intricate patterns in unfamiliar code
- Expert-level domain analysis

**Not needed for:**
- Simple code edits or fixes
- Questions answerable by reading 1-2 files
- Tasks requiring immediate responses
- Repetitive operations better suited to scripts

## Advanced Usage

### Custom PR Reference

```bash
/oracle-review PR_REF=origin/develop...feature/my-branch PR_URL=https://github.com/org/repo/pull/123
```

### Focus Areas

```bash
/oracle-review FOCUS="ensure auth interceptors unchanged, validate migration rollback"
```

## File Glob Patterns

The oracle skill includes comprehensive glob patterns for different analysis types:

- Security audits (auth, API, data access)
- Architectural reviews (services, APIs, overall)
- Data flow analysis (end-to-end, events)
- Performance analysis (queries, caching)
- Testing & quality

See the oracle skill references for complete patterns.

## Troubleshooting

### Environment Issues

Ensure `OPENAI_API_KEY` is set:
```bash
export OPENAI_API_KEY=your-key-here
```

Or use browser mode:
```bash
# Oracle commands will use --engine browser automatically if needed
```

### Session Management

Check oracle help for current session commands:
```bash
npx -y @steipete/oracle@latest --help
```

View session status:
```bash
npx -y @steipete/oracle@latest session <slug>
```

## Resources

- [Oracle CLI Documentation](https://github.com/steipete/oracle)
- [Oracle Skill Reference](./skills/oracle/SKILL.md)
- [Glob Patterns Guide](./skills/oracle/references/glob-patterns.md)

## License

MIT
