"""
Tests for stop_todo_enforcement.py - Stop hook that prevents premature stops during implement workflows.
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


def run_stop_hook(
    transcript_lines: list[dict[str, Any]] | None = None,
    transcript_path: str | None = None,
    env_overrides: dict[str, str] | None = None,
    tmp_path: Path | None = None,
) -> subprocess.CompletedProcess:
    """Helper to run the stop hook with given transcript and input."""
    import os

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

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
        [sys.executable, str(HOOKS_DIR / "stop_todo_enforcement.py")],
        input=stdin_data,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(HOOKS_DIR),
    )
    return result


class TestStopHookNoImplementWorkflow:
    """Tests for when no implement workflow is detected."""

    def test_exits_zero_for_regular_messages(self, tmp_path):
        """Should exit 0 when no implement workflow detected."""
        lines = [
            {"type": "user", "message": {"content": "Help me with something"}},
            {"type": "assistant", "message": {"content": "Sure, I'll help"}},
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_zero_for_empty_transcript(self, tmp_path):
        """Should exit 0 for empty transcript."""
        result = run_stop_hook(transcript_lines=[], tmp_path=tmp_path)
        assert result.returncode == 0

    def test_exits_zero_for_nonexistent_transcript(self):
        """Should exit 0 when transcript file doesn't exist."""
        result = run_stop_hook(transcript_path="/nonexistent/path.jsonl")
        assert result.returncode == 0

    def test_exits_zero_for_no_transcript_path(self):
        """Should exit 0 when no transcript_path provided."""
        result = run_stop_hook(transcript_path="")
        assert result.returncode == 0


class TestStopHookImplementWorkflowNoTodos:
    """Tests for implement workflow with no incomplete todos."""

    def test_exits_zero_when_all_todos_complete(self, tmp_path):
        """Should allow stop when all todos are completed."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task 1",
                                        "status": "completed",
                                        "activeForm": "T1",
                                    },
                                    {
                                        "content": "Task 2",
                                        "status": "completed",
                                        "activeForm": "T2",
                                    },
                                ]
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        assert result.returncode == 0
        assert result.stdout == ""

    def test_exits_zero_when_no_todo_writes(self, tmp_path):
        """Should allow stop when implement detected but no TodoWrite calls."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {"content": "I'll start implementing..."},
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        assert result.returncode == 0


class TestStopHookBlocksWithIncompleteTodos:
    """Tests for blocking when todos are incomplete."""

    def test_blocks_with_pending_todos(self, tmp_path):
        """Should block stop when pending todos exist."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task 1",
                                        "status": "completed",
                                        "activeForm": "T1",
                                    },
                                    {
                                        "content": "Task 2",
                                        "status": "pending",
                                        "activeForm": "T2",
                                    },
                                ]
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        assert result.returncode == 0
        output = json.loads(result.stdout)
        assert output["decision"] == "block"
        assert "1 todos remain incomplete" in output["reason"]

    def test_blocks_with_in_progress_todos(self, tmp_path):
        """Should block stop when in_progress todos exist."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task 1",
                                        "status": "in_progress",
                                        "activeForm": "T1",
                                    },
                                ]
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert output["decision"] == "block"

    def test_block_message_contains_hold_marker(self, tmp_path):
        """Block message should contain HOLD marker for counting."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task",
                                        "status": "pending",
                                        "activeForm": "T",
                                    }
                                ],
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert "HOLD: You have" in output["systemMessage"]

    def test_counts_multiple_incomplete_todos(self, tmp_path):
        """Should correctly count multiple incomplete todos."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task 1",
                                        "status": "pending",
                                        "activeForm": "T1",
                                    },
                                    {
                                        "content": "Task 2",
                                        "status": "in_progress",
                                        "activeForm": "T2",
                                    },
                                    {
                                        "content": "Task 3",
                                        "status": "pending",
                                        "activeForm": "T3",
                                    },
                                ]
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert "3 todos remain incomplete" in output["reason"]


class TestStopHookSafetyValve:
    """Tests for the safety valve after max blocks."""

    def test_approves_after_max_blocks_reached(self, tmp_path):
        """Should approve stop after max block attempts."""
        # Create transcript with 5 prior blocks (default max)
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task",
                                        "status": "pending",
                                        "activeForm": "T",
                                    }
                                ],
                            },
                        }
                    ]
                },
            },
        ]
        # Add 5 block markers
        for _ in range(5):
            lines.append(
                {
                    "type": "assistant",
                    "message": {"content": "HOLD: You have pending todos"},
                }
            )

        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert output["decision"] == "approve"
        assert "Safety valve triggered" in output["reason"]

    def test_respects_custom_max_blocks_env(self, tmp_path):
        """Should respect IMPLEMENT_MAX_BLOCKS environment variable."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task",
                                        "status": "pending",
                                        "activeForm": "T",
                                    }
                                ],
                            },
                        }
                    ]
                },
            },
            # Add 2 block markers
            {"type": "assistant", "message": {"content": "HOLD: You have 1"}},
            {"type": "assistant", "message": {"content": "HOLD: You have 2"}},
        ]

        # With max_blocks=2, should approve
        result = run_stop_hook(
            transcript_lines=lines,
            tmp_path=tmp_path,
            env_overrides={"IMPLEMENT_MAX_BLOCKS": "2"},
        )
        output = json.loads(result.stdout)
        assert output["decision"] == "approve"

    def test_blocks_before_max_reached(self, tmp_path):
        """Should still block before max blocks reached."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task",
                                        "status": "pending",
                                        "activeForm": "T",
                                    }
                                ],
                            },
                        }
                    ]
                },
            },
            # Add 4 block markers (less than default 5)
            {"type": "assistant", "message": {"content": "HOLD: You have 1"}},
            {"type": "assistant", "message": {"content": "HOLD: You have 2"}},
            {"type": "assistant", "message": {"content": "HOLD: You have 3"}},
            {"type": "assistant", "message": {"content": "HOLD: You have 4"}},
        ]

        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert output["decision"] == "block"


class TestStopHookImplementDetection:
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
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task",
                                        "status": "pending",
                                        "activeForm": "T",
                                    }
                                ],
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert output["decision"] == "block"

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
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task",
                                        "status": "pending",
                                        "activeForm": "T",
                                    }
                                ],
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert output["decision"] == "block"

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
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task",
                                        "status": "pending",
                                        "activeForm": "T",
                                    }
                                ],
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        output = json.loads(result.stdout)
        assert output["decision"] == "block"


class TestStopHookEdgeCases:
    """Edge case tests for the stop hook."""

    def test_handles_invalid_json_stdin(self):
        """Should handle invalid JSON in stdin gracefully."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "stop_todo_enforcement.py")],
            input="not valid json",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0

    def test_handles_empty_stdin(self):
        """Should handle empty stdin gracefully."""
        result = subprocess.run(
            [sys.executable, str(HOOKS_DIR / "stop_todo_enforcement.py")],
            input="",
            capture_output=True,
            text=True,
            cwd=str(HOOKS_DIR),
        )
        assert result.returncode == 0

    def test_uses_latest_todo_state(self, tmp_path):
        """Should use the latest TodoWrite state, not accumulate."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name>"
                },
            },
            # First TodoWrite with pending
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task 1",
                                        "status": "pending",
                                        "activeForm": "T1",
                                    },
                                    {
                                        "content": "Task 2",
                                        "status": "pending",
                                        "activeForm": "T2",
                                    },
                                ]
                            },
                        }
                    ]
                },
            },
            # Second TodoWrite - all complete
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {
                                "todos": [
                                    {
                                        "content": "Task 1",
                                        "status": "completed",
                                        "activeForm": "T1",
                                    },
                                    {
                                        "content": "Task 2",
                                        "status": "completed",
                                        "activeForm": "T2",
                                    },
                                ]
                            },
                        }
                    ]
                },
            },
        ]
        result = run_stop_hook(transcript_lines=lines, tmp_path=tmp_path)
        # Should allow stop since latest state is all complete
        assert result.returncode == 0
        assert result.stdout == ""
