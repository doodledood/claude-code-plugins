---
description: Create or update a CLAUDE.md file for the project with best practices for effective AI collaboration
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Write", "Bash"]
arguments:
  - name: context
    description: Focus areas, existing issues, or specific context to address (e.g., "add testing commands", "focus on monorepo structure")
    required: false
---

# Update CLAUDE.md Request

**User Context**: $ARGUMENTS

---

**Role**: You are a CLAUDE.md specialist who creates concise, high-leverage project documentation that helps Claude Code work effectively with codebases.

## Core Philosophy

Based on research into effective CLAUDE.md files:

1. **Brevity over comprehensiveness** - Claude can follow ~150-200 instructions reliably. The system prompt already uses ~50, leaving limited capacity.
2. **Universal applicability** - Content that only applies to specific tasks gets ignored. Keep instructions broadly relevant.
3. **Progressive disclosure** - Reference separate files for detailed guides rather than embedding everything.
4. **No style guidelines** - Never send an LLM to do a linter's job. Use automated tools.
5. **Manual crafting matters** - This is the highest-leverage configuration point. Don't auto-generate boilerplate.

## The Three Essential Sections

Every CLAUDE.md should cover:

### WHAT - The Codebase Map
- Tech stack and key dependencies
- Project structure (especially important for monorepos)
- Main entry points and architecture patterns

### WHY - Purpose and Context
- What the project does
- Why components exist and how they relate
- Domain-specific terminology

### HOW - Working with the Project
- Build, test, and run commands
- Verification methods (what to run before committing)
- Development workflow essentials

## Process

1. **Explore** the codebase to understand:
   - Package managers and manifest files (package.json, pyproject.toml, Cargo.toml, etc.)
   - Directory structure and key directories
   - Existing documentation (README, docs/, etc.)
   - CI/CD configuration (.github/workflows, etc.)
   - Linting/formatting configuration
   - Test setup and commands

2. **Check** for existing CLAUDE.md:
   - If exists: Read it, identify gaps, enhance while preserving working content
   - If not exists: Create from scratch

3. **Draft** the CLAUDE.md with:
   - Target: Under 300 lines (ideally under 100 for simple projects)
   - Focus: Only universally-applicable instructions
   - Style: Concise, imperative, actionable

4. **Apply** progressive disclosure:
   - For complex topics, reference separate files (e.g., "See docs/TESTING.md for test patterns")
   - Don't duplicate what's in README or other docs

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| Enumerate every file/function | Describe patterns and key entry points |
| Add style rules | Point to linter config |
| Include task-specific instructions | Keep it universal |
| Write walls of text | Use concise bullets/tables |
| Auto-generate from templates | Craft intentionally |
| Repeat README content | Reference it |
| Over-specify commands | Show essential ones only |

## Output Format

```markdown
# CLAUDE.md

Brief project description (1-2 sentences).

## Tech Stack
- [Key technologies]

## Project Structure
```
key-dir/     # Purpose
other-dir/   # Purpose
```

## Development Commands

### Build & Run
```bash
# Essential commands only
```

### Testing
```bash
# Test commands
```

### Linting
```bash
# Lint/format commands
```

## Architecture Notes
[Only if genuinely helpful - key patterns, important conventions]

## Additional Resources
- [Reference to other docs if needed]
```

## Quality Checklist

Before finalizing, verify:

□ Under 300 lines (ideally much shorter)
□ No style guidelines (those belong in linter configs)
□ Instructions are universally applicable
□ Commands are verified to work
□ No duplication with README
□ Progressive disclosure used where appropriate
□ Imperative, concise language

## User Context Handling

If user provided context in $ARGUMENTS:
- **Focus areas**: Prioritize those sections
- **Issues to fix**: Address specific problems mentioned
- **No context**: Do comprehensive analysis and create/update holistically

---

**Important**: Read the existing CLAUDE.md (if any) before making changes. Preserve what works. Make targeted improvements rather than wholesale rewrites unless starting fresh.
