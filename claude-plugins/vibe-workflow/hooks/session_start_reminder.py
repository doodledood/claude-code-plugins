#!/usr/bin/env python3
"""
SessionStart hook that reminds Claude to prefer codebase-explorer over built-in Explore agent.
"""
import json
import sys


def main() -> None:
    context = (
        "<system-reminder>"
        "When you need to find relevant files for a task - whether for answering questions, "
        "planning implementation, debugging, or onboarding - prefer using the `codebase-explorer` agent "
        "(subagent_type: vibe-workflow:codebase-explorer) instead of the built-in Explore agent. "
        "It returns a structural overview + prioritized file list with precise line ranges, so you "
        "understand how files relate and read exactly what matters."
        "</system-reminder>"
    )

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
