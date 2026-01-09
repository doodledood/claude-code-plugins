# Prompt Engineering

Analyze and refine prompts for clarity and precision.

## What It Does

Two complementary workflows:

- **`/review-prompt`** - Analyze a prompt against the 10-Layer Architecture framework. Reports issues without modifying files.
- **`/refine-prompt`** - Iteratively refine a prompt for precision. Eliminates ambiguities, resolves conflicts, adds missing definitions. Modifies the file after verification passes.

## Components

### Commands
- `/review-prompt` - Analyze a prompt file (read-only)
- `/refine-prompt` - Iteratively refine a prompt for precision (modifies file)

### Agents
- `prompt-reviewer` - Deep 10-layer analysis for review
- `prompt-precision-verifier` - Checks for ambiguities, conflicts, undefined terms

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install prompt-engineering@claude-code-plugins-marketplace
```

## License

MIT
