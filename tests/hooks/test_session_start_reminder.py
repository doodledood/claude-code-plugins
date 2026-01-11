"""
Tests for session_start_reminder.py - SessionStart hook for vibe-workflow best practices.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# Path to the hooks directory
HOOKS_DIR = (
    Path(__file__).parent.parent.parent / "claude-plugins" / "vibe-workflow" / "hooks"
)


class TestSessionStartReminderHook:
    """Tests for the session-start-reminder hook."""

    def test_outputs_valid_json(self):
        """Hook should output valid JSON to stdout."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert isinstance(output, dict)

    def test_output_has_hook_specific_output(self):
        """Output should contain hookSpecificOutput key."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output

    def test_output_has_correct_event_name(self):
        """Output should have hookEventName set to SessionStart."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        output = json.loads(result.stdout)
        assert output["hookSpecificOutput"]["hookEventName"] == "SessionStart"

    def test_output_has_additional_context(self):
        """Output should contain additionalContext with reminders."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert isinstance(context, str)
        assert len(context) > 0

    def test_context_contains_codebase_explorer_reminder(self):
        """Context should mention codebase-explorer agent."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "codebase-explorer" in context

    def test_context_contains_web_researcher_reminder(self):
        """Context should mention web-researcher agent."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "web-researcher" in context

    def test_context_wrapped_in_system_reminder_tags(self):
        """Context should be wrapped in system-reminder tags."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "<system-reminder>" in context
        assert "</system-reminder>" in context

    def test_exits_with_zero(self):
        """Hook should exit with code 0 on success."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0

    def test_no_stderr_output(self):
        """Hook should not produce stderr output on success."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.stderr == ""
