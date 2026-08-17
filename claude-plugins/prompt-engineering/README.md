# Prompt Engineering

Optimization passes over a prompt you already have — convergence, token efficiency, and compression.

Authoring and review are not here. `/prompt-engineering` and `/review-prompt` live in [manifest-dev](https://github.com/doodledood/manifest-dev), which maintains them; this repository consumes them rather than keeping a parallel copy.

## What It Does

Three complementary workflows:

- **`/auto-optimize-prompt`** - Iteratively auto-optimize a prompt until no high-confidence issues remain. Loops the reviewer, asks the user to resolve ambiguities, and applies fixes until converged.
- **`/optimize-prompt-token-efficiency`** - Iteratively optimize a prompt for token efficiency. Reduces verbosity, removes redundancy, tightens phrasing while preserving semantic content.
- **`/compress-prompt`** - Compress a prompt into a single dense paragraph for AI-readable context injection. Maximizes information density using a preservation hierarchy.

## Components

### Skills
- `/auto-optimize-prompt` - Auto-optimize until converged, asks user for ambiguities (modifies file)
- `/optimize-prompt-token-efficiency` - Iteratively optimize for token efficiency (modifies file)
- `/compress-prompt` - Compress into dense paragraph (non-destructive)

### Agents
- `prompt-reviewer` - Deep analysis for review; invokes the unscoped `prompt-engineering` skill for its principles
- `prompt-token-efficiency-verifier` - Checks for redundancy, verbosity, compression opportunities
- `prompt-compression-verifier` - Verifies compression preserves essential semantic content

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install prompt-engineering@claude-code-plugins-marketplace
```

## License

MIT
