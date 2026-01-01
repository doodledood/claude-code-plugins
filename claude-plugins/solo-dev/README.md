# Solo Dev Plugin

Toolkit for solo developers to build, manage, and grow their business.

## What It Does

**Skills** (auto-invoked by Claude when relevant):
- **define-customer-profile** - Create your foundational CUSTOMER.md that all other decisions flow from
- **define-brand-guidelines** - Define how to communicate with your customer (requires CUSTOMER.md)
- **define-design-guidelines** - Create UI/UX guidelines that resonate with your customer (requires CUSTOMER.md)
- **define-seo-strategy** - Traditional SEO + AI citation optimization (requires CUSTOMER.md)
- **craft-author-voice** - Capture your unique writing style for AI replication

**Commands** (invoke explicitly):
- `/write-as-me <topic>` - Generate content in your voice (requires AUTHOR_VOICE.md)
- `/audit-ux <area>` - Check UI changes against design guidelines

Use `/help` after installation to see all available commands.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install solo-dev@claude-code-plugins-marketplace
```

## License

MIT
