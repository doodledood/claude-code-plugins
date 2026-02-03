---
name: address-pr-comments
description: 'Triage and fix PR review comments. Reads comments, filters false positives (outdated, misread, wrong context, style preference), validates relevance against current diff, and fixes valid ones with confirmation. Use when: "fix pr comments", "address review feedback", "handle pr feedback".'
---

**User request**: $ARGUMENTS

**If no PR specified**: Detect PR from current branch. If detection fails, report and stop.

**Default scope**: All unresolved comments on the PR.

## Goal

Classify all unresolved PR comments against false positive criteria, report triage findings, then fix actionable items with user confirmation per fix.

## False Positive Detection

| Type | Detection Signal |
|------|------------------|
| **Outdated** | Suggested change already exists in code; commit history shows it was addressed |
| **Misread code** | Comment's premise contradicts what code actually does |
| **Wrong context** | Comment references behavior/variables not present in the target code |
| **Style preference** | No functional or readability improvement—evaluate substance, not reviewer's tone |
| **Resolved in thread** | Reply discussion shows issue was already addressed or withdrawn |

**Classification**:
- Strong false-positive signal → `false-positive`
- Real issue with clear fix → `actionable`
- Unclear validity → `uncertain` (report, don't fix)

## Output

**Triage report**: Classification, reasoning, and summary counts for each comment. Format flexibly based on volume.

**Per-fix flow**: For actionable items, show original comment and proposed change, await user confirmation before applying.

## Constraints

| Constraint | Enforcement |
|------------|-------------|
| Verify before classifying | Read actual code and reply threads; never classify from comment text alone |
| Conservative on fixes | Uncertain → report only |
| Explain rejections | Every false-positive needs reasoning |
| Per-fix confirmation | User confirms each fix individually |
