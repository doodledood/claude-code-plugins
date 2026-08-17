# ADR: The prompt-engineering skill is deferred to manifest-dev rather than maintained here

## Status
Accepted — narrowed in part by 20260817-review-prompt-deferred-to-manifest-dev, which applies the same rule to review-prompt after it gained an upstream equivalent

## Area
Plugin boundaries

## Context

Reconstructed from `CHANGELOG.md`'s `[prompt-engineering] v3.0.0` entry and commit `0faa493` (PR #114).

This repository's `prompt-engineering` plugin shipped its own `prompt-engineering` skill: a 242-line monolith with three references. manifest-dev, which this repository already syncs from, had grown a newer version of the same capability — a thin `SKILL.md` using progressive disclosure into seven references. Maintaining both meant two skills answering the same question, diverging.

## Decision

Remove the `prompt-engineering` skill from this repository's plugin and take manifest-dev's instead. The plugin keeps the skills that have no upstream equivalent — `auto-optimize-prompt`, `compress-prompt`, `optimize-prompt-token-efficiency`, `review-prompt` — and the `prompt-reviewer` agent now invokes the unscoped `prompt-engineering` skill, since this plugin no longer supplies one.

The general rule this settles: where a capability exists upstream in a better-maintained form, this repository consumes it rather than keeping a parallel copy.

## Alternatives Considered

- **Keep the local skill and let both exist**: No breaking change, no dependency on upstream timing — Rejected: two skills for one job diverge, and the local one was already the older and larger of the two.
- **Keep the local skill and stop syncing manifest-dev's**: Preserves independence — Rejected: it means re-implementing upstream improvements by hand, which is the cost this repository's sync tooling exists to avoid.

## Consequences

### Positive
- One prompt-engineering skill, and it is the maintained one.
- The plugin shrinks to what it uniquely provides.

### Negative
- A breaking change for anyone who had the local skill installed by name.
- The capability now depends on upstream: if manifest-dev drops or changes it, this repository feels it.

## Source
- Retroactive — reconstructed from CHANGELOG.md and commit 0faa493 / PR #114 during project setup
- Session: (no session — captured post-hoc)
