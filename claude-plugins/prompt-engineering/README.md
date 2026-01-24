# Prompt Engineering

Craft, analyze, and optimize prompts for clarity, precision, goal effectiveness, and token efficiency.

## What It Does

Four complementary workflows:

- **`/prompt-engineering`** - Craft or update prompts from first principles. Guides creation of new prompts or targeted updates to existing ones. Ensures prompts define WHAT and WHY, not HOW.
- **`/review-prompt`** - Analyze a prompt against the 10-Layer Architecture framework. Reports issues without modifying files.
- **`/optimize-prompt-token-efficiency`** - Iteratively optimize a prompt for token efficiency. Reduces verbosity, removes redundancy, tightens phrasing while preserving semantic content.
- **`/compress-prompt`** - Compress a prompt into a single dense paragraph for AI-readable context injection. Maximizes information density using preservation hierarchy.

## Components

### Skills
- `/prompt-engineering` - Craft or update prompts from first principles
- `/review-prompt` - Analyze a prompt file (read-only)
- `/optimize-prompt-token-efficiency` - Iteratively optimize a prompt for token efficiency (modifies file)
- `/compress-prompt` - Compress a prompt into a single dense paragraph (non-destructive)

### Agents
- `prompt-reviewer` - Deep 10-layer analysis for review (uses `/prompt-engineering` principles)
- `prompt-token-efficiency-verifier` - Checks for redundancy, verbosity, compression opportunities
- `prompt-compression-verifier` - Verifies compression preserves essential semantic content

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install prompt-engineering@claude-code-plugins-marketplace
```

## License

MIT
