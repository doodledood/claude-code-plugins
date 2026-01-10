#!/usr/bin/env python3
"""
SessionStart hook that reminds Claude to prefer vibe-workflow agents over built-in alternatives.
"""
import json
import sys


def main() -> None:
    codebase_explorer_reminder = (
        "When you need to find relevant files for a task - whether for answering questions, "
        "planning implementation, debugging, or onboarding - prefer using the `codebase-explorer` agent "
        "(subagent_type: vibe-workflow:codebase-explorer) instead of the built-in Explore agent. "
        "It returns a structural overview + prioritized file list with precise line ranges, so you "
        "understand how files relate and read exactly what matters."
    )

    web_researcher_reminder = (
        "For non-trivial web research tasks - technology comparisons, best practices, API documentation, "
        "library evaluations, or any question requiring synthesis of multiple sources - prefer using "
        "the `web-researcher` agent (subagent_type: vibe-workflow:web-researcher) instead of calling "
        "WebSearch directly. It uses structured hypothesis tracking to systematically gather and "
        "synthesize web-based evidence, producing higher-quality research output."
    )

    context = f"<system-reminder>{codebase_explorer_reminder}</system-reminder>\n<system-reminder>{web_researcher_reminder}</system-reminder>"

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
