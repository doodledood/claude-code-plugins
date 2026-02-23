# marketing

Value-first marketing workflows for promoting products on social platforms. Uses browser automation (Claude in Chrome) and the writing plugin for human-quality prose.

## Architecture

```
marketing/
├── skills/
│   └── promote-on-x/          # Browse X, find relevant posts, craft & post replies
│       ├── SKILL.md
│       └── references/
│           └── X_INTERFACE.md  # X character limits, chrome interaction patterns
└── README.md
```

## Skills

### promote-on-x

Promotes a product by finding high-signal posts on X and crafting value-first replies that genuinely help the conversation while naturally referencing your product. Uses memento pattern (log file) for context resilience during long browsing sessions.

**Workflow**: Product familiarization → Feed browsing → Opportunity logging → Reply crafting with writing review → User approval → Posting

## Prerequisites

- **Claude in Chrome extension** — required for browser interaction with X
- **writing plugin** — used for anti-AI prose principles (`human-writing`) and review (`writing-reviewer`)

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install marketing@claude-code-plugins-marketplace
```

## Usage

```bash
# Promote current project on X home feed (default: 10 replies)
/promote-on-x

# Promote with specific product and target count
/promote-on-x Promote https://github.com/user/repo, find 5 posts

# Use a specific X list as feed source
/promote-on-x Feed: https://x.com/i/lists/123456, promote my SaaS product at example.com
```
