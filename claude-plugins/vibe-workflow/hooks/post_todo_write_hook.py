#!/usr/bin/env python3
"""
Post-tool-use hook that reminds Claude to update log files after task completion.

Registered under PostToolUse with "TaskUpdate" matcher.

This hook:
1. Detects if session may be in an implement workflow
2. Checks if a task was just marked completed (via TaskUpdate)
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
    "If you're in a vibe-workflow:implement or implement-inplace workflow and just completed a task, "
    "consider updating your progress/log file in /tmp/ (implement-*.md or implement-progress.md) "
    "to reflect this completion. This helps maintain external memory for session recovery."
)


def has_completed_task(tool_name: str, tool_input: dict[str, Any]) -> bool:
    """Check if the task tool call indicates a completed task.

    TaskUpdate with status=completed indicates task completion.
    """
    if tool_name == "TaskUpdate":
        return tool_input.get("status") == "completed"
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

    # Verify this is a task-related call (TaskUpdate for completion)
    tool_name = hook_input.get("tool_name", "")
    if tool_name not in ("TaskUpdate",):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    transcript_path = hook_input.get("transcript_path", "")

    # Check if a task was marked completed
    if not has_completed_task(tool_name, tool_input):
        sys.exit(0)

    # Check if we're potentially in an implement workflow
    if not transcript_path:
        sys.exit(0)

    state = parse_transcript(transcript_path)
    if not state.in_implement_workflow:
        sys.exit(0)

    # We're in an implement workflow with a completed task - add reminder
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
