# Solo Dev

Foundational documents for solo developers and small teams.

## Why

AI-assisted development works better when there's documented context about your business, customers, and brand. Instead of re-explaining "who we're building for" every conversation, define it once and let Claude reference it consistently.

## Components

**Skills** (auto-invoked when relevant):
- `define-customer-profile` - Create CUSTOMER.md that all other decisions flow from
- `define-brand-guidelines` - Define how to communicate with your customer
- `define-design-guidelines` - Create UI/UX guidelines that resonate with your customer
- `define-seo-strategy` - Traditional SEO + AI citation optimization
- `craft-author-voice` - Capture your writing style for AI replication

**Commands** (explicit invocation):
- `/write-as-me <topic>` - Generate content in your voice (requires AUTHOR_VOICE.md)
- `/audit-ux <area>` - Check UI changes against your design guidelines

## Recommended Order

1. Start with `define-customer-profile` - everything else depends on knowing who you're building for
2. Then brand guidelines, design guidelines as needed
3. Author voice is independent - create whenever you want consistent content generation

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install solo-dev@claude-code-plugins-marketplace
```

## License

MIT
