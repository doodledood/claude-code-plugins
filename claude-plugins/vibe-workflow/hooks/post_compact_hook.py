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
    "IMPORTANT: You were in the middle of an /implement workflow when compaction occurred. "
    "Context has been lost. Before continuing, you MUST:\n"
    "1. List files in /tmp/ matching plan-*.md and implement-*.md patterns to find your working files\n"
    "2. Read the FULL plan file (most recent /tmp/plan-*.md) to understand the overall implementation\n"
    "3. Read the FULL implementation log file (/tmp/implement-*.md) to see progress and current state\n"
    "4. Check your todo list for incomplete items\n"
    "Then resume implementation from where you left off. Do not restart work that was already completed."
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
