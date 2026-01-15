# Prompt Engineering

Analyze, refine, and optimize prompts for clarity, precision, and goal effectiveness.

## What It Does

Three complementary workflows:

- **`/review-prompt`** - Analyze a prompt against the 10-Layer Architecture framework. Reports issues without modifying files.
- **`/refine-prompt`** - Iteratively refine a prompt for precision. Eliminates ambiguities, resolves conflicts, adds missing definitions. Modifies the file after verification passes.
- **`/optimize-prompt-goal`** - Iteratively optimize a prompt for goal effectiveness. Ensures instructions serve the stated goal, prevents missteps, improves efficiency. Modifies the file after verification passes.

## Components

### Skills
- `/review-prompt` - Analyze a prompt file (read-only)
- `/refine-prompt` - Iteratively refine a prompt for precision (modifies file)
- `/optimize-prompt-goal` - Iteratively optimize a prompt for goal effectiveness (modifies file)

### Agents
- `prompt-reviewer` - Deep 10-layer analysis for review
- `prompt-precision-verifier` - Checks for ambiguities, conflicts, undefined terms
- `prompt-goal-verifier` - Checks for goal misalignment, misstep risks, inefficiencies

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install prompt-engineering@claude-code-plugins-marketplace
```

## License

MIT
