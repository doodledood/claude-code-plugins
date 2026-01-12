"""
Tests for post_compact_hook.py - SessionStart hook (compact matcher) for session recovery after compaction.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# Path to the hooks directory
HOOKS_DIR = (
    Path(__file__).parent.parent.parent / "claude-plugins" / "vibe-workflow" / "hooks"
)


def run_post_compact_hook(
    transcript_lines: list[dict[str, Any]] | None = None,
    transcript_path: str | None = None,
    tmp_path: Path | None = None,
) -> subprocess.CompletedProcess:
    """Helper to run the post-compact hook with given transcript."""
    # Create transcript file if lines provided
    if transcript_lines is not None and tmp_path is not None:
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w", encoding="utf-8") as f:
            for line in transcript_lines:
                f.write(json.dumps(line) + "\n")
        transcript_path = str(transcript_file)

    # Prepare stdin input
    hook_input = {"transcript_path": transcript_path or ""}
    stdin_data = json.dumps(hook_input)

    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
        input=stdin_data,
        capture_output=True,
        text=True,
        cwd=str(HOOKS_DIR),
    )
    return result


class TestPostCompactHookBasicOutput:
    """Tests for basic hook output structure."""

    def test_outputs_valid_json(self):
        """Hook should output valid JSON to stdout."""
        result = run_post_compact_hook()
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert isinstance(output, dict)

    def test_output_has_hook_specific_output(self):
        """Output should contain hookSpecificOutput key."""
        result = run_post_compact_hook()
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output

    def test_output_has_correct_event_name(self):
        """Output should have hookEventName set to SessionStart."""
        result = run_post_compact_hook()
        output = json.loads(result.stdout)
        assert output["hookSpecificOutput"]["hookEventName"] == "SessionStart"

    def test_output_has_additional_context(self):
        """Output should contain additionalContext."""
        result = run_post_compact_hook()
        output = json.loads(result.stdout)
        assert "additionalContext" in output["hookSpecificOutput"]
        assert isinstance(output["hookSpecificOutput"]["additionalContext"], str)

    def test_exits_with_zero(self):
        """Hook should exit with code 0."""
        result = run_post_compact_hook()
        assert result.returncode == 0

    def test_no_stderr_output(self):
        """Hook should not produce stderr output on success."""
        result = run_post_compact_hook()
        assert result.stderr == ""


class TestPostCompactHookSessionReminders:
    """Tests for standard session reminders (always included)."""

    def test_contains_codebase_explorer_reminder(self):
        """Should always include explore-codebase reminder."""
        result = run_post_compact_hook()
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "explore-codebase" in context

    def test_contains_web_researcher_reminder(self):
        """Should always include research-web reminder."""
        result = run_post_compact_hook()
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "research-web" in context

    def test_reminders_wrapped_in_system_reminder_tags(self):
        """Reminders should be wrapped in system-reminder tags."""
        result = run_post_compact_hook()
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "<system-reminder>" in context
        assert "</system-reminder>" in context

    def test_reminders_present_without_transcript(self):
        """Should include reminders even without transcript path."""
        result = run_post_compact_hook(transcript_path="")
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "explore-codebase" in context
        assert "research-web" in context


class TestPostCompactHookImplementRecovery:
    """Tests for implement workflow recovery reminder."""

    def test_includes_recovery_reminder_when_in_implement(self, tmp_path):
        """Should include recovery reminder when implement workflow detected."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            in context
        )

    def test_no_recovery_reminder_without_implement(self, tmp_path):
        """Should not include recovery reminder for regular sessions."""
        lines = [
            {"type": "user", "message": {"content": "Help me with something"}},
            {"type": "assistant", "message": {"content": "Sure!"}},
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            not in context
        )

    def test_recovery_reminder_mentions_plan_files(self, tmp_path):
        """Recovery reminder should mention plan files."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "plan-*" in context

    def test_recovery_reminder_mentions_implement_files(self, tmp_path):
        """Recovery reminder should mention implement log files."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "implement-*" in context

    def test_recovery_reminder_mentions_todo_list(self, tmp_path):
        """Recovery reminder should mention checking todo list."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "todo list" in context.lower()

    def test_recovery_reminder_wrapped_in_system_reminder(self, tmp_path):
        """Recovery reminder should be wrapped in system-reminder tags."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        # Should have at least 3 system-reminder tags (2 for session + 1 for recovery)
        assert context.count("<system-reminder>") >= 3


class TestPostCompactHookImplementDetection:
    """Tests for various implement workflow detection scenarios."""

    def test_detects_implement_inplace(self, tmp_path):
        """Should detect implement-inplace variant."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement-inplace</command-name>"
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            in context
        )

    def test_detects_skill_call_implement(self, tmp_path):
        """Should detect implement via Skill tool call."""
        lines = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {"skill": "vibe-workflow:implement"},
                        }
                    ]
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            in context
        )

    def test_detects_skill_call_implement_inplace(self, tmp_path):
        """Should detect implement-inplace via Skill tool call."""
        lines = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Skill",
                            "input": {"skill": "vibe-workflow:implement-inplace"},
                        }
                    ]
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            in context
        )

    def test_detects_array_content_format(self, tmp_path):
        """Should detect implement in array content format."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "text",
                            "text": "<command-name>/vibe-workflow:implement</command-name>",
                        }
                    ]
                },
            },
        ]
        result = run_post_compact_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            in context
        )


class TestPostCompactHookEdgeCases:
    """Edge case tests for the post-compact hook."""

    def test_handles_invalid_json_stdin(self):
        """Should handle invalid JSON in stdin gracefully."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        # Should still output session reminders
        output = json.loads(result.stdout)
        assert "explore-codebase" in output["hookSpecificOutput"]["additionalContext"]

    def test_handles_empty_stdin(self):
        """Should handle empty stdin gracefully."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
            input="",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        # Should still output session reminders
        output = json.loads(result.stdout)
        assert "explore-codebase" in output["hookSpecificOutput"]["additionalContext"]

    def test_handles_nonexistent_transcript(self):
        """Should handle nonexistent transcript path gracefully."""
        result = run_post_compact_hook(transcript_path="/nonexistent/path.jsonl")
        assert result.returncode == 0
        # Should output session reminders but no recovery reminder
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "explore-codebase" in context
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            not in context
        )

    def test_handles_empty_transcript(self, tmp_path):
        """Should handle empty transcript file."""
        result = run_post_compact_hook(transcript_lines=[], tmp_path=tmp_path)
        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "explore-codebase" in context
        # No implement workflow in empty transcript
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            not in context
        )

    def test_handles_malformed_transcript_lines(self, tmp_path):
        """Should handle transcript with some malformed lines."""
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w") as f:
            f.write("not json\n")
            f.write(
                '{"type": "user", "message": {"content": "<command-name>/vibe-workflow:implement</command-name>"}}\n'
            )
            f.write("also not json\n")

        hook_input = {"transcript_path": str(transcript_file)}
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_compact_hook.py")],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        # Should still detect implement workflow from valid line
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            in context
        )


class TestPostCompactHookVsSessionStartReminder:
    """Tests comparing post-compact hook to session-start-reminder."""

    def test_both_have_same_session_reminders_without_implement(self, tmp_path):
        """Both hooks should have same basic reminders when no implement workflow."""
        # Run session-start-reminder
        session_result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        session_output = json.loads(session_result.stdout)
        session_context = session_output["hookSpecificOutput"]["additionalContext"]

        # Run post-compact hook without implement
        lines = [{"type": "user", "message": {"content": "Hello"}}]
        compact_result = run_post_compact_hook(
            transcript_lines=lines, tmp_path=tmp_path
        )
        compact_output = json.loads(compact_result.stdout)
        compact_context = compact_output["hookSpecificOutput"]["additionalContext"]

        # Both should have same session reminders
        assert "explore-codebase" in session_context
        assert "explore-codebase" in compact_context
        assert "research-web" in session_context
        assert "research-web" in compact_context

    def test_post_compact_has_extra_recovery_reminder_with_implement(self, tmp_path):
        """Post-compact should have extra recovery reminder when implement detected."""
        # Run session-start-reminder
        session_result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "session_start_reminder.py")],
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        session_output = json.loads(session_result.stdout)
        session_context = session_output["hookSpecificOutput"]["additionalContext"]

        # Run post-compact hook with implement
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        compact_result = run_post_compact_hook(
            transcript_lines=lines, tmp_path=tmp_path
        )
        compact_output = json.loads(compact_result.stdout)
        compact_context = compact_output["hookSpecificOutput"]["additionalContext"]

        # Session start should not have recovery reminder
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            not in session_context
        )

        # Post-compact should have recovery reminder
        assert (
            "This session may have been in the middle of a vibe-workflow:implement workflow"
            in compact_context
        )
