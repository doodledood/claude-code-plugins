# Architecture Decision Records

| Date | ADR | Status | Area |
|------|-----|--------|------|
| 2026-04-30 | [The sync tool deletes only what it previously wrote](20260430-tracked-set-deletion-protects-coexisting-plugins.md) | Accepted | Plugin sync |
| 2026-07-23 | [Agents and hooks were consolidated into skills](20260723-agents-and-hooks-consolidated-into-skills.md) | Accepted | Plugin structure |
| 2026-08-02 | [The prompt-engineering skill is deferred to manifest-dev rather than maintained here](20260802-defer-prompt-engineering-to-manifest-dev.md) | Accepted — superseded by [20260817-prompt-engineering-plugin-retired](20260817-prompt-engineering-plugin-retired.md), which retired the plugin this record kept | Plugin boundaries |
| 2026-08-07 | [The sync tool decides skill layout once per repository, not per skill](20260807-layout-verdict-is-per-repo-not-per-skill.md) | Accepted | Plugin sync |
| 2026-08-17 | [The prompt-engineering plugin is retired from this marketplace](20260817-prompt-engineering-plugin-retired.md) | Accepted | Plugin boundaries |
| 2026-08-17 | [review-prompt is deferred to manifest-dev, like the prompt-engineering skill before it](20260817-review-prompt-deferred-to-manifest-dev.md) | Accepted — superseded by [20260817-prompt-engineering-plugin-retired](20260817-prompt-engineering-plugin-retired.md), which retired the plugin this record declined to retire | Plugin boundaries |
| 2026-09-04 | [The /define session-learning skills are retired](20260904-define-session-learning-skills-retired.md) | Accepted | Plugin structure |
| 2026-09-04 | [This repository's own specialists are skills, not agents](20260904-repository-local-specialists-are-skills-not-agents.md) | Accepted — narrowed by [20260904-define-session-learning-skills-retired](20260904-define-session-learning-skills-retired.md), which retired `define-session-analyzer` and its caller; the rule set here still governs `code-coverage-reviewer` and anything added later | Plugin structure |
