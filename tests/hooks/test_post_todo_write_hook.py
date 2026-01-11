"""
Tests for post_todo_write_hook.py - PostToolUse hook for log file reminders after todo completion.
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


def run_post_todo_write_hook(
    tool_name: str = "TodoWrite",
    tool_input: dict[str, Any] | None = None,
    transcript_lines: list[dict[str, Any]] | None = None,
    transcript_path: str | None = None,
    tmp_path: Path | None = None,
) -> subprocess.CompletedProcess:
    """Helper to run the post-todo-write hook with given input."""
    # Create transcript file if lines provided
    if transcript_lines is not None and tmp_path is not None:
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w", encoding="utf-8") as f:
            for line in transcript_lines:
                f.write(json.dumps(line) + "\n")
        transcript_path = str(transcript_file)

    # Prepare stdin input (PostToolUse format)
    hook_input = {
        "hook_event_name": "PostToolUse",
        "tool_name": tool_name,
        "tool_input": tool_input or {},
        "tool_response": {"success": True},
        "transcript_path": transcript_path or "",
    }
    stdin_data = json.dumps(hook_input)

    result = subprocess.run(
        [sys.executable, str(HOOKS_DIR / "post_todo_write_hook.py")],
        input=stdin_data,
        capture_output=True,
        text=True,
        cwd=str(HOOKS_DIR),
    )
    return result


class TestPostTodoWriteHookBasicBehavior:
    """Tests for basic hook behavior."""

    def test_exits_silently_for_non_todowrite_tool(self):
        """Hook should exit silently for non-TodoWrite tools."""
        result = run_post_todo_write_hook(tool_name="Bash")
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_silently_for_read_tool(self):
        """Hook should exit silently for Read tool."""
        result = run_post_todo_write_hook(tool_name="Read")
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_silently_for_invalid_json_stdin(self):
        """Hook should exit silently for invalid JSON input."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_todo_write_hook.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_silently_for_empty_stdin(self):
        """Hook should exit silently for empty stdin."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_todo_write_hook.py")],
            input="",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        assert result.stdout == ""


class TestPostTodoWriteHookNoCompletedTodo:
    """Tests for TodoWrite calls without completed todos."""

    def test_exits_silently_when_no_completed_todos(self, tmp_path):
        """Should exit silently when no todos are completed."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "pending", "activeForm": "T1"},
                {"content": "Task 2", "status": "in_progress", "activeForm": "T2"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_silently_when_all_pending(self, tmp_path):
        """Should exit silently when all todos are pending."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "pending", "activeForm": "T1"},
                {"content": "Task 2", "status": "pending", "activeForm": "T2"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_silently_when_empty_todos(self, tmp_path):
        """Should exit silently when todos list is empty."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {"todos": []}
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        assert result.stdout == ""


class TestPostTodoWriteHookNotImplementWorkflow:
    """Tests for completed todos outside implement workflow."""

    def test_exits_silently_when_not_in_implement_workflow(self, tmp_path):
        """Should exit silently when completed todo but no implement workflow."""
        transcript_lines = [
            {"type": "user", "message": {"content": "Help me with something"}},
            {"type": "assistant", "message": {"content": "Sure!"}},
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_silently_without_transcript_path(self):
        """Should exit silently when no transcript path provided."""
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(tool_input=tool_input, transcript_path="")
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_silently_with_nonexistent_transcript(self):
        """Should exit silently when transcript file doesn't exist."""
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_path="/nonexistent/transcript.jsonl"
        )
        assert result.returncode == 0
        assert result.stdout == ""


class TestPostTodoWriteHookWithReminder:
    """Tests for when reminder should be shown."""

    def test_shows_reminder_when_implement_with_completed_todo(self, tmp_path):
        """Should show reminder when in implement workflow with completed todo."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
                {"content": "Task 2", "status": "pending", "activeForm": "T2"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
        assert output["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
        assert "additionalContext" in output["hookSpecificOutput"]

    def test_reminder_mentions_log_file(self, tmp_path):
        """Reminder should mention log/progress file."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "progress/log file" in context or "implement-" in context

    def test_reminder_mentions_tmp_directory(self, tmp_path):
        """Reminder should mention /tmp/ directory."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "/tmp/" in context

    def test_reminder_uses_hedging_language(self, tmp_path):
        """Reminder should use hedging language (consider, may, if)."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        # Should use hedging language, not assertive
        assert "consider" in context.lower() or "if you" in context.lower()

    def test_reminder_wrapped_in_system_reminder_tags(self, tmp_path):
        """Reminder should be wrapped in system-reminder tags."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        output = json.loads(result.stdout)
        context = output["hookSpecificOutput"]["additionalContext"]
        assert "<system-reminder>" in context
        assert "</system-reminder>" in context


class TestPostTodoWriteHookImplementVariants:
    """Tests for different implement workflow detection scenarios."""

    def test_detects_implement_inplace(self, tmp_path):
        """Should detect implement-inplace variant."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement-inplace</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output

    def test_detects_skill_call_implement(self, tmp_path):
        """Should detect implement via Skill tool call."""
        transcript_lines = [
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
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output

    def test_detects_skill_call_implement_inplace(self, tmp_path):
        """Should detect implement-inplace via Skill tool call."""
        transcript_lines = [
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
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output


class TestPostTodoWriteHookMultipleCompletedTodos:
    """Tests for TodoWrite with multiple completed todos."""

    def test_shows_reminder_with_multiple_completed_todos(self, tmp_path):
        """Should show reminder when multiple todos are completed."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
                {"content": "Task 2", "status": "completed", "activeForm": "T2"},
                {"content": "Task 3", "status": "pending", "activeForm": "T3"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output

    def test_shows_reminder_when_all_completed(self, tmp_path):
        """Should show reminder when all todos are completed."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
                {"content": "Task 2", "status": "completed", "activeForm": "T2"},
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output


class TestPostTodoWriteHookEdgeCases:
    """Edge case tests for the post-todo-write hook."""

    def test_handles_malformed_todos(self, tmp_path):
        """Should handle malformed todos gracefully."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {
            "todos": [
                {"content": "Task 1"},  # Missing status
                "not a dict",
                None,
            ]
        }
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        # Should exit silently since no valid completed todo
        assert result.stdout == ""

    def test_handles_missing_todos_key(self, tmp_path):
        """Should handle missing todos key gracefully."""
        transcript_lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
        ]
        tool_input = {}  # Missing todos
        result = run_post_todo_write_hook(
            tool_input=tool_input, transcript_lines=transcript_lines, tmp_path=tmp_path
        )
        assert result.returncode == 0
        assert result.stdout == ""

    def test_handles_malformed_transcript(self, tmp_path):
        """Should handle transcript with malformed lines."""
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w") as f:
            f.write("not json\n")
            f.write(
                '{"type": "user", "message": {"content": "<command-name>/vibe-workflow:implement</command-name>"}}\n'
            )
            f.write("also not json\n")

        tool_input = {
            "todos": [
                {"content": "Task 1", "status": "completed", "activeForm": "T1"},
            ]
        }
        hook_input = {
            "hook_event_name": "PostToolUse",
            "tool_name": "TodoWrite",
            "tool_input": tool_input,
            "tool_response": {"success": True},
            "transcript_path": str(transcript_file),
        }
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "post_todo_write_hook.py")],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0
        # Should still detect implement workflow and show reminder
        output = json.loads(result.stdout)
        assert "hookSpecificOutput" in output
