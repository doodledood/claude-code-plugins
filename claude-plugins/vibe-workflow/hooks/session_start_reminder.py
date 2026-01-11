#!/usr/bin/env python3
"""
SessionStart hook that reminds Claude to prefer vibe-workflow agents over built-in alternatives.
"""
import json
import sys

from hook_utils import build_session_reminders


def main() -> None:
    context = build_session_reminders()

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
