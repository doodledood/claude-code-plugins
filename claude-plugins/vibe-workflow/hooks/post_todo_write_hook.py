#!/usr/bin/env python3
"""
Post-tool-use hook that reminds Claude to update log files after todo completion.

Registered under PostToolUse with "TodoWrite" matcher.

This hook:
1. Detects if session may be in an implement workflow
2. Checks if a todo was just marked completed
3. If so, adds a gentle reminder to update the progress/log file
"""

from __future__ import annotations

import json
import sys
from typing import Any

from hook_utils import (
    build_system_reminder,
    parse_transcript,
)

LOG_FILE_REMINDER = (
    "If you're in a vibe-workflow:implement or implement-inplace workflow and just completed a todo, "
    "consider updating your progress/log file in /tmp/ (implement-*.md or implement-progress.md) "
    "to reflect this completion. This helps maintain external memory for session recovery."
)


def has_completed_todo(tool_input: dict[str, Any]) -> bool:
    """Check if the TodoWrite call contains any completed todos."""
    todos = tool_input.get("todos", [])
    for t in todos:
        if not isinstance(t, dict):
            continue
        if t.get("status") == "completed":
            return True
    return False


def main() -> None:
    """Main hook entry point."""
    # Read hook input from stdin
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        # Can't parse input, exit silently
        sys.exit(0)

    # Verify this is a TodoWrite call
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "TodoWrite":
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    transcript_path = hook_input.get("transcript_path", "")

    # Check if any todo was marked completed
    if not has_completed_todo(tool_input):
        sys.exit(0)

    # Check if we're potentially in an implement workflow
    if not transcript_path:
        sys.exit(0)

    state = parse_transcript(transcript_path)
    if not state.in_implement_workflow:
        sys.exit(0)

    # We're in an implement workflow with a completed todo - add reminder
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": build_system_reminder(LOG_FILE_REMINDER),
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
