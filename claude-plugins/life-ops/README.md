# life-ops

Personal decision-making and life workflow support.

## Overview

The life-ops plugin helps you make confident personal decisions through structured situation discovery, targeted research, and decision framework application. Instead of jumping straight to criteria collection, it understands YOUR situation first—time horizons, life events, underlying needs—then researches with that context in mind.

## Skills

### /decide

Personal decision advisor that guides you from question to confident recommendation.

**Use when**: Facing any personal decision—investments, purchases, career moves, life changes, relationship decisions.

**What it does**:
1. **Assesses stakes** - Calibrates depth based on decision importance
2. **Discovers your situation** - Understands underlying needs, time horizons, constraints, success criteria, and potential regrets
3. **Generates targeted research brief** - Precise brief with YOUR context for focused research
4. **Executes research** - Conducts web research tailored to your decision
5. **Applies decision framework** - Filters through your constraints, ranks by your priorities
6. **Recommends with confidence** - Top 3 options with clear #1, trade-offs, and tie-breakers when needed

**Examples**:
```
/decide should I buy a MacBook Pro now or wait for M5?
/decide help me choose between job offer A and B
/decide which index fund for long-term investing?
/decide should I rent or buy in my situation?
```

**Key features**:
- Probes underlying needs (not just stated requirements)
- Tracks uncertainty and probability
- Uses 10-10-10 regret framework
- Asks targeted tie-breaker questions when options are close
- Works without vibe-extras (Opus fallback)

## Installation

```bash
/plugin marketplace add /path/to/claude-code-plugins
/plugin install life-ops@claude-code-plugins-marketplace
```

## Integration

Works best with `vibe-extras:research-web` for thorough web research. Falls back to Opus agent with WebSearch if vibe-extras is not installed.

## Design Philosophy

The /decide skill emerged from a real failure mode: using /spec for personal research captured CRITERIA but missed SITUATION. Research executed well but was poorly targeted because the brief lacked decision-relevant context—time horizons, life events, underlying needs, stakeholders.

This plugin takes a "Decision Coach/Advisor" mental model: understand the person first, then derive criteria and research.
