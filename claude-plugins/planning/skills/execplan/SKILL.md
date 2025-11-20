---
name: execplan
description: Create comprehensive execution plans (ExecPlans) following PLANS.md methodology. Use ONLY when user explicitly mentions "execplan" or "exec plan" in their request.
---

# ExecPlan Creation

You are creating an execution plan following `PLANS.md` methodology.

## Instructions

1. **Read `PLANS.md` first** - This contains all methodology, requirements, structure, and guidelines
2. Follow the process and skeleton defined in PLANS.md to the letter
3. Create a comprehensive, self-contained plan that enables a novice to implement the feature

## Claude Code Integration

### During Planning - Clarify Ambiguities

Research exhaustively first (files, codebase, docs), then use `AskUserQuestion` tool when:

- Multiple architecturally significant approaches exist with different trade-offs
- Scope boundaries are unclear and materially affect chunk structure
- Technology choices lack precedent and impact system design
- Business context is needed (speed vs quality, MVP vs complete, priorities)
- User expectations are ambiguous (UX patterns, error handling strategy)

**Don't ask when:**

- Established patterns exist in codebase (follow them)
- Standard best practices are well-documented
- Implementation details don't affect public APIs
- Minor tool/library choices with similar capabilities

**Question format:**

- 1-4 strategic questions maximum per planning session
- Present options with clear trade-offs
- Use multiSelect when choices aren't mutually exclusive
- Keep focused and actionable

### After Planning - Present and Execute

1. **Present via ExitPlanMode tool** (if available; otherwise present as text)
2. **Wait for explicit user approval** before any implementation
3. After approval:
   - Persist the approved plan to `ai-plans/<descriptive-feature-name>.md`
   - **The ExecPlan is a living document** - update it directly as work progresses
   - Track all progress, status changes, discoveries, and decisions within the plan file itself
   - Do NOT use Claude Code's separate todo system

**Important:** ExecPlans are living documents per PLANS.md. The plan file itself IS your todo system—do NOT create separate todos. Update the persisted plan file directly and continuously as work progresses. It is the sole source of truth for all tracking: progress, status, discoveries, decisions, and task completion. Follow the update guidance in PLANS.md.

---

Begin by gathering requirements from the user, then follow PLANS.md to create the ExecPlan.
