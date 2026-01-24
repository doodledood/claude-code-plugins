#!/usr/bin/env python3
"""
Post-compact hook that re-anchors the session after compaction.

Registered under SessionStart with "compact" matcher since PostCompact doesn't exist yet.

This hook:
1. Injects the same reminders as session start (agent preferences)
2. If in the middle of an implement workflow, reminds Claude to read plan/log files
"""

from __future__ import annotations

import json
import sys

from hook_utils import (
    build_session_reminders,
    build_system_reminder,
    parse_transcript,
)

IMPLEMENT_RECOVERY_REMINDER = (
    "This session may have been in the middle of a vibe-workflow:implement workflow before compaction. "
    "If you were implementing a plan and haven't already read your working files in full, "
    "check for implementation log files in /tmp/ matching the implement-*.md pattern. If found, "
    "read the FULL log file to recover your progress - it typically contains a reference to "
    "the associated plan file (plan-*.md) which you should also read in full if not already "
    "loaded. Check your todo list for incomplete items, then resume from where you left off. "
    "Do not restart work that was already completed."
)


def main() -> None:
    """Main hook entry point."""
    # Read hook input from stdin
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        hook_input = {}

    transcript_path = hook_input.get("transcript_path", "")

    # Start with standard session reminders
    context_parts = [build_session_reminders()]

    # If we have transcript access, check for implement workflow
    if transcript_path:
        state = parse_transcript(transcript_path)

        if state.in_implement_workflow:
            # Add implement recovery reminder
            context_parts.append(build_system_reminder(IMPLEMENT_RECOVERY_REMINDER))

    context = "\n".join(context_parts)

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
