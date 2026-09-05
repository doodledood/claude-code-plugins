# ADR: Use installed Manifest Dev plugins

## Status
Accepted

## Area
Plugin sync

## Context
Repository-local Manifest Dev copies and their mirrors duplicated skills already supplied by installed plugins. The sync tool existed to maintain those copies.

## Decision
Use the installed Manifest Dev plugins for workflow skills. Remove the copied skills, their discovery mirrors, the sync skill, and its tracking file. Keep repository-specific skills and the marketplace plugins published here.

## Alternatives Considered
- **Keep synchronized copies**: preserves availability without plugins, but creates duplicate discovery and a second update mechanism.
- **Remove copies only**: leaves scripts and setup guidance able to recreate them.

## Consequences

### Positive
- Each harness has one installation owner for Manifest Dev skills.
- Repository-specific skills retain their own source and discovery paths.

### Negative
- Repository sessions need the Manifest Dev plugins installed.

## Source
- Supersedes 20260430-tracked-set-deletion-protects-coexisting-plugins
- Supersedes 20260807-layout-verdict-is-per-repo-not-per-skill
