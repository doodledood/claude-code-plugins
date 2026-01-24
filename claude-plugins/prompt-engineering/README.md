# Prompt Engineering

Craft, analyze, and optimize prompts for clarity, precision, goal effectiveness, and token efficiency.

## What It Does

Seven complementary workflows:

- **`/prompt-engineering`** - Craft or update prompts from first principles. Guides creation of new prompts or targeted updates to existing ones. Ensures prompts define WHAT and WHY, not HOW.
- **`/review-prompt`** - Analyze a prompt against the 10-Layer Architecture framework. Reports issues without modifying files.
- **`/optimize-prompt-precision`** - Iteratively optimize a prompt for precision. Eliminates ambiguities, resolves conflicts, adds missing definitions. Modifies the file after verification passes.
- **`/optimize-prompt-goal`** - Iteratively optimize a prompt for goal effectiveness. Ensures instructions serve the stated goal, prevents missteps, improves efficiency. Modifies the file after verification passes.
- **`/optimize-prompt-token-efficiency`** - Iteratively optimize a prompt for token efficiency. Reduces verbosity, removes redundancy, tightens phrasing while preserving semantic content. Modifies the file after verification passes.
- **`/compress-prompt`** - Compress a prompt into a single dense paragraph for AI-readable context injection. Maximizes information density using preservation hierarchy. Non-destructive (displays output, optional file save).
- **`/apply-prompt-feedback`** - Apply collected feedback to a prompt. Makes targeted changes based on observed issues.

## Components

### Skills
- `/prompt-engineering` - Craft or update prompts from first principles
- `/review-prompt` - Analyze a prompt file (read-only)
- `/optimize-prompt-precision` - Iteratively optimize a prompt for precision (modifies file)
- `/optimize-prompt-goal` - Iteratively optimize a prompt for goal effectiveness (modifies file)
- `/optimize-prompt-token-efficiency` - Iteratively optimize a prompt for token efficiency (modifies file)
- `/compress-prompt` - Compress a prompt into a single dense paragraph (non-destructive)
- `/apply-prompt-feedback` - Apply collected feedback to a prompt

### Agents
- `prompt-reviewer` - Deep 10-layer analysis for review
- `prompt-precision-verifier` - Checks for ambiguities, conflicts, undefined terms
- `prompt-goal-verifier` - Checks for goal misalignment, misstep risks, inefficiencies
- `prompt-token-efficiency-verifier` - Checks for redundancy, verbosity, compression opportunities
- `prompt-compression-verifier` - Verifies compression preserves essential semantic content

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install prompt-engineering@claude-code-plugins-marketplace
```

## License

MIT
