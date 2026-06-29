# hermes-tweet

Native Hermes Agent X/Twitter automation guidance for Claude Code users who need a read-first social plugin with explicit action gates.

## Skill

### hermes-tweet

Helps install, enable, configure, and operate [Hermes Tweet](https://github.com/Xquik-dev/hermes-tweet) from Claude Code while keeping X/Twitter writes disabled unless the user explicitly enables them in the Hermes runtime.

## What It Covers

- Install Hermes Tweet with `hermes plugins install Xquik-dev/hermes-tweet --enable`.
- Configure `XQUIK_API_KEY` only in the Hermes runtime environment or `~/.hermes/.env`.
- Use `tweet_explore` before selecting a catalog endpoint.
- Prefer `tweet_read` for public and account reads.
- Use `tweet_action` only after the user confirms the exact endpoint and payload.
- Keep `HERMES_TWEET_ENABLE_ACTIONS=false` unless the session intentionally needs posting, DMs, follows, monitors, webhooks, media, draws, or other state-changing work.

## Installation

```bash
/plugin marketplace add https://github.com/doodledood/claude-code-plugins
/plugin install hermes-tweet@claude-code-plugins-marketplace
```

## Hermes Runtime Install

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

For non-interactive installs, set `XQUIK_API_KEY` before calling `tweet_read`. Without a key, Hermes Tweet should still expose the no-network `tweet_explore` tool.

Action endpoints stay disabled unless `HERMES_TWEET_ENABLE_ACTIONS=true`.
