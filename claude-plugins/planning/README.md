# Planning Plugin

Comprehensive planning tools for Claude Code with automatic keyword detection. Includes plan and execplan skills, oracle-execplan command, and smart hooks that remind Claude to activate planning skills when needed.

## Overview

This plugin provides two complementary planning methodologies:
- **Plan skill**: Mini-PR based implementation plans optimized for iterative development
- **ExecPlan skill**: Comprehensive execution plans for complex features requiring detailed specifications

The plugin includes intelligent hooks that automatically detect planning keywords in your messages and activate the appropriate skill.

## Components

### Skills

#### `plan`
Create implementation plans using the Planning Playbook methodology.

**When to use:**
- User asks to "plan", "create a plan", or needs implementation roadmap
- Default when in Planning Mode
- Optimized for mini-PR chunks, parallel work streams, iterative development

**Methodology:**
- Mini-PR chunks (1-3 functions, <200 LOC each)
- Quality gates per chunk (Type checks, Tests, Lint)
- Dependency ordering with parallel opportunities
- Cognitive load minimization
- Ships complete value incrementally

#### `execplan`
Create comprehensive execution plans following PLANS.md methodology.

**When to use:**
- User explicitly mentions "execplan" or "exec plan"
- Complex features requiring detailed specifications
- Novice-friendly, self-contained execution plans

**Methodology:**
- Fully self-contained living documents
- Observable outcomes and validation steps
- Detailed milestones with acceptance criteria
- Decision logs and discovery tracking
- Proof of concepts for challenging requirements

### Command

#### `/oracle-execplan`
Create comprehensive execution plans using oracle CLI tool for deep analysis.

**Usage:**
```bash
/oracle-execplan
# Infers feature context from branch name and git history
```

**What it does:**
- Invokes oracle-consulter agent for deep planning analysis
- Gathers comprehensive codebase context
- Creates detailed, self-contained execution plans
- Follows PLANS.md methodology with oracle's extended reasoning

### Hook: check-planning-keywords.py

**Automatic activation on user prompt submit**

The hook detects planning keywords in your messages and reminds Claude to activate the appropriate skill:
- Detects "execplan" or "exec plan" → Suggests activating `execplan` skill
- Detects "plan" (without exec) → Suggests activating `plan` skill

**How it works:**
- Runs automatically when you submit a prompt
- No manual configuration needed
- Works transparently in the background
- Uses regex to detect keywords in natural language

## Installation

```bash
# Add marketplace
/plugin marketplace add https://github.com/doodledood/claude-code-plugins

# Install planning plugin
/plugin install planning@claude-code-plugins-marketplace
```

## Requirements

- Python 3 (for hook script)
- Oracle CLI (for `/oracle-execplan` command - requires OPENAI_API_KEY)

## Quick Start

### 1. Create an Implementation Plan

```bash
# Just mention "plan" in your message:
"Can you plan how to implement user authentication?"

# The hook automatically reminds Claude to activate the plan skill
# Claude creates a mini-PR based implementation plan
```

### 2. Create an Execution Plan

```bash
# Mention "execplan" in your message:
"Create an execplan for rate limiting"

# The hook automatically reminds Claude to activate the execplan skill
# Claude creates a comprehensive, self-contained execution plan
```

### 3. Use Oracle for Deep Planning

```bash
/oracle-execplan FEATURE="Add rate limiting" GOAL="Prevent API abuse"

# Invokes oracle-consulter agent with planning focus
# Gathers extensive codebase context
# Creates detailed execution plan with oracle's extended reasoning
```

## Example Workflows

### Quick Feature Implementation

```bash
User: "Plan how to add email notifications"

# Hook detects "plan" keyword
# Claude activates plan skill automatically
# Creates mini-PR based plan with 3-5 chunks
# Each chunk: 1-3 functions, quality gates, parallel opportunities
# Plan presented for approval
# After approval: persisted to ai-plans/email-notifications.md
# Todos created from chunks for execution
```

### Complex Feature Design

```bash
User: "Create an execplan for migrating to new auth system"

# Hook detects "execplan" keyword
# Claude activates execplan skill automatically
# Creates comprehensive execution plan following PLANS.md
# Includes: milestones, validation steps, decision logs
# Novice-friendly, self-contained specification
# Living document updated during implementation
```

### Oracle-Powered Planning

```bash
User: /oracle-execplan

# Oracle-consulter agent activated
# Gathers: code patterns, architecture, dependencies
# Invokes oracle CLI for deep analysis
# Creates execution plan with extended reasoning
# Comprehensive context and recommendations
```

## Planning Methodologies

### Plan Skill (Mini-PR Approach)

**Principles:**
- Safety: Every chunk tested independently
- Clarity: Full paths, numbered chunks, explicit dependencies
- Minimalism: 1-3 chunks preferred; ship today's requirements only
- Forward focus: No backward compatibility by default

**Chunk Structure:**
- 1-3 functions per chunk
- <200 LOC per chunk
- Quality gates: Type checks → Tests → Lint
- Demonstrable value when complete
- Mergeable independently

**Output:**
```markdown
# IMPLEMENTATION PLAN: Feature Name

Gates per chunk: Type checks, Tests, Lint

## 1. Chunk Name
Depends on: - | Parallel: -

Files to modify:
- path/to/file.ts – what changes

Implementation tasks:
- Implement functionName() – purpose
- Tests – specific cases
- Run gates
```

### ExecPlan Skill (Comprehensive Approach)

**Principles per PLANS.md:**
- Fully self-contained (novice can implement without prior knowledge)
- Living document (updated as work progresses)
- Observable outcomes (user can verify working behavior)
- Plain language (define all jargon, no assumed knowledge)

**Structure:**
- Purpose / Big Picture
- Milestones with validation
- Chunk task checklists
- Surprises & Discoveries section
- Decision Log section
- Outcomes & Retrospective section

**Output:**
```markdown
# Short, action-oriented description

## Purpose / Big Picture
[User-visible behavior enabled by this change]

## Milestone 1: Foundation
[Scope, commands to run, acceptance criteria]

### Chunk 1: [Component name]
- [ ] Task with specific function/file
- [ ] Tests proving behavior
- [ ] Validation command

## Surprises & Discoveries
[Updated during implementation]

## Decision Log
[Key decisions and rationale]
```

## Hook Details

The `check-planning-keywords.py` hook:

**Event:** `user-prompt-submit` (runs when you submit a message)

**Logic:**
1. Reads user message from stdin
2. Parses JSON input
3. Checks for planning keywords using regex
4. Outputs `<system-reminder>` if keywords detected
5. Reminder suggests activating appropriate skill

**Patterns detected:**
- `/\bexec\s*plan\b/` or `execplan` → execplan skill
- `/\bplan\b/` (without exec) → plan skill

**Example output:**
```
<system-reminder>
The user mentioned "plan". If you have not already activated
the plan skill and this appears to be a request for creating
a plan, you should use the Skill tool with skill="plan" to
load the Plan methodology BEFORE beginning any planning work.
</system-reminder>
```

## When to Use Which Methodology

### Use `plan` skill when:
- Iterative development preferred
- Mini-PR workflow desired
- Need parallel work streams
- Medium complexity (3-8 chunks)
- Team familiar with codebase

### Use `execplan` skill when:
- Complex features with unknowns
- Novice developers implementing
- Need detailed specifications
- Long-running projects
- Significant architectural changes
- Proof of concepts required

### Use `/oracle-execplan` when:
- Need deep codebase analysis
- Architectural validation required
- Complex dependencies to untangle
- High-stakes planning (production systems)
- Extended reasoning beneficial

## Troubleshooting

### Hook not triggering

Ensure Python 3 is available:
```bash
python3 --version
```

Check hook file is executable:
```bash
chmod +x hooks/check-planning-keywords.py
```

### Skills not activating

After hook reminder, manually activate if needed:
```bash
# For implementation plans:
Skill tool with skill="plan"

# For execution plans:
Skill tool with skill="execplan"
```

### Oracle command not working

Requires oracle CLI and OPENAI_API_KEY:
```bash
export OPENAI_API_KEY=your-key-here
npx -y @steipete/oracle@latest --help
```

## Resources

- [PLANS.md](./skills/execplan/PLANS.md) - Complete ExecPlan methodology
- [Plan Skill](./skills/plan/SKILL.md) - Mini-PR planning methodology
- [ExecPlan Skill](./skills/execplan/SKILL.md) - Comprehensive planning methodology
- [Oracle Plugin](../oracle/) - Oracle CLI integration for deep analysis

## License

MIT
