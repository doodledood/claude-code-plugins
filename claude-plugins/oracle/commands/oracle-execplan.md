# Oracle ExecPlan Command

Create comprehensive execution plans using oracle CLI tool through the oracle-consulter agent for deep analysis and specification design with extended reasoning.

## What This Does

Invokes the **oracle-consulter agent** to create detailed, self-contained execution plans (ExecPlans) following PLANS.md methodology with:

- Comprehensive context gathering and codebase analysis
- Living document structure with decision logs and discovery tracking
- Small, shippable chunks with clear dependencies
- Detailed validation and acceptance criteria
- Novice-friendly, self-contained specifications

## Inputs with Smart Defaults

| Key       | Default Inference Strategy                 | Example                        | Notes                                       |
| --------- | ------------------------------------------ | ------------------------------ | ------------------------------------------- |
| `FEATURE` | Infer from current branch name or user msg | `Add rate limiting to API`     | Brief description of feature/change to plan |
| `GOAL`    | Infer from user message context            | `Prevent API abuse`            | User-visible purpose and benefit            |
| `SCOPE`   | Empty (no specific constraints)            | `Focus on REST endpoints only` | Boundaries, constraints, or focus areas     |
| `CONTEXT` | Infer from recent commits and git status   | `Existing auth in place`       | Relevant codebase state or dependencies     |

Pass overrides via `$ARGUMENTS` below if needed.

## Default Behavior

When invoked without explicit arguments, the command will:

1. **Infer FEATURE**:

   - Parse current branch name (e.g., `id_12345_add_rate_limiting` → "Add rate limiting")
   - Extract from user's most recent message
   - If unclear, ask user for clarification

2. **Infer GOAL**:

   - Extract from user's message context (e.g., "to prevent API abuse")
   - Look for purpose/benefit statements in recent conversation
   - If unclear, ask user for clarification

3. **Infer SCOPE**:

   - Default to empty (no specific constraints)
   - Can be inferred from explicit user mentions of boundaries

4. **Infer CONTEXT**:
   - Gather from `git log -10 --oneline` (recent work)
   - Check `git status` for current changes
   - Default to empty if no relevant context

## Usage

**Step 1: Infer feature context (run these in parallel if needed):**

- Get current branch: `git branch --show-current`
- Get recent commits: `git log -10 --oneline`
- Check current state: `git status --short`

**Step 2: Parse $ARGUMENTS and user message** to determine:

- FEATURE (from arguments, branch name, or user message)
- GOAL (from arguments or user message)
- SCOPE (from arguments or default to empty)
- CONTEXT (from arguments, git history, or default to empty)

**Step 3: If FEATURE or GOAL unclear**, ask user:

```
I need to understand what you'd like to plan:
1. What feature or change should I create an execution plan for?
2. What's the user-visible goal or benefit?

I can optionally use:
- Scope: [any constraints or boundaries]
- Context: [relevant codebase state - will gather from git if not specified]
```

**Step 4: Invoke oracle-consulter agent** with the following prompt:

```
Please create a comprehensive ExecPlan for the following feature:

Feature: {{FEATURE}}
Goal: {{GOAL}}
Scope: {{SCOPE}} (if provided, otherwise no specific constraints)
Context: {{CONTEXT}} (if inferred or provided, otherwise agent will gather)

IMPORTANT: Before gathering context, use the Skill tool with skill="execplan" to load the ExecPlan methodology and PLANS.md requirements.

After loading the execplan skill, gather comprehensive codebase context and create a detailed execution plan following the PLANS.md methodology.

Provide the complete ExecPlan as a single markdown document ready to persist to ai-plans/<feature-name>.md
```

## What the Agent Will Do

The oracle-consulter agent will automatically:

1. **Load ExecPlan methodology** using Skill tool with skill="execplan"
2. Analyze the feature request and identify scope boundaries
3. Gather comprehensive codebase context (files, patterns, types, tests)
4. Classify context by category (core logic, schemas/types, tests, infrastructure)
5. Create timestamped temp directory with organized, numbered attachments
6. Construct detailed planning prompt with methodology requirements
7. Invoke oracle via `npx -y @steipete/oracle@latest` directly via Bash with structured context
8. Monitor session continuously (30s intervals) until completion
9. Synthesize oracle's output into a complete, self-contained ExecPlan

## Expected Output from Oracle

Oracle will provide a complete, self-contained ExecPlan document following the PLANS.md methodology.

**Format and requirements**: The ExecPlan structure, sections, formatting, and quality standards are defined in the `execplan` skill (`.claude/skills/execplan/PLANS.md`). Refer to that skill for the canonical specification of what an ExecPlan should contain.

The document will be ready to save to `ai-plans/<feature-name>.md` and serve as the sole source of truth during implementation.

## Extra User Instructions

$ARGUMENTS
