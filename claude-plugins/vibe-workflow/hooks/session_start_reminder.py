#!/usr/bin/env python3
"""
SessionStart hook that reminds Claude to prefer codebase-researcher over built-in Explore agent.
"""
import json
import sys


def main() -> None:
    context = (
        "<system-reminder>"
        "When you need deep understanding of a code area - whether for answering questions, "
        "planning implementation, debugging, or onboarding - prefer using the `codebase-researcher` agent "
        "(subagent_type: vibe-workflow:codebase-researcher) instead of the built-in Explore agent. "
        "It provides MAX understanding with precise file:line references, so you can read its output "
        "and confidently answer questions or plan changes without re-exploring the codebase."
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
