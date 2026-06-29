---
name: hermes-tweet
description: 'Install, configure, or operate Hermes Tweet, the native Hermes Agent X/Twitter plugin. Use when asked about Hermes Agent social automation, X/Twitter reads, tweet posting, Xquik-backed Hermes workflows, or approval-gated social actions.'
user-invocable: true
---

Use Hermes Tweet as the native Hermes Agent plugin for X/Twitter automation.

## Identify the Task

Classify the user request:

- **Install or enable**: show Hermes install commands and configuration checks.
- **Discover capability**: use `tweet_explore` first in the Hermes runtime.
- **Read data**: select a catalog endpoint, then use `tweet_read`.
- **Change account or workflow state**: require explicit user confirmation before `tweet_action`.
- **Debug availability**: check whether the plugin is enabled and whether required environment variables are visible to the Hermes runtime.

## Install

Recommend the native Hermes plugin install:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

If Hermes discovers the plugin but does not expose its tools, ask the user to run:

```bash
hermes plugins enable hermes-tweet
hermes plugins list
```

## Configure

Keep credentials outside prompts and tool arguments.

Required for authenticated reads:

```bash
export XQUIK_API_KEY="xq_..."
```

Optional action gate:

```bash
export HERMES_TWEET_ENABLE_ACTIONS="false"
```

If `XQUIK_API_KEY` is missing, expect only `tweet_explore` to be available. That is safe gating, not an install failure.

## Tool Routing

Use this order:

1. Call `tweet_explore` to find supported catalog endpoints.
2. Call `tweet_read` for public or account read routes.
3. Call `tweet_action` only for writes, private reads, monitor changes, webhooks, media, DMs, follows, draws, or other state-changing routes after user confirmation.

Before any `tweet_action`, state:

- Endpoint path.
- Request payload.
- Expected side effect.
- Confirmation that `HERMES_TWEET_ENABLE_ACTIONS=true` is intentionally enabled.

## Safety Rules

- Never ask the user to paste API keys into chat.
- Never pass credentials as tool arguments.
- Never guess endpoint paths.
- Do not call `tweet_action` for endpoint discovery or routine reads.
- Do not treat installation as execution. Hermes Agent requires third-party plugins to be enabled before their tools run.
- For remote gateway profiles, configure the plugin and environment on the host that executes Hermes tools.

## Verification

For a non-mutating smoke test, ask Hermes to use only discovery and reads:

```bash
hermes -z "Use tweet_explore, then read /api/v1/account. Do not call tweet_action." --toolsets hermes-tweet
```

Expected behavior:

- `tweet_explore` works without an API call.
- `tweet_read` requires `XQUIK_API_KEY`.
- `tweet_action` stays hidden or disabled unless `HERMES_TWEET_ENABLE_ACTIONS=true`.
