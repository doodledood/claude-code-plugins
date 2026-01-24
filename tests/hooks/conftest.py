"""
Shared fixtures for hook tests.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

# Add hooks directory to path for imports
HOOKS_DIR = (
    Path(__file__).parent.parent.parent / "claude-plugins" / "vibe-workflow" / "hooks"
)
sys.path.insert(0, str(HOOKS_DIR))


@pytest.fixture
def temp_transcript(tmp_path: Path):
    """Factory fixture for creating temporary transcript files."""

    def _create_transcript(lines: list[dict[str, Any]]) -> str:
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(json.dumps(line) + "\n")
        return str(transcript_file)

    return _create_transcript


@pytest.fixture
def user_message_implement_command() -> dict[str, Any]:
    """User message with implement command in string format."""
    return {
        "type": "user",
        "message": {
            "content": "Please help me <command-name>/vibe-workflow:implement</command-name> this feature"
        },
    }


@pytest.fixture
def user_message_implement_command_array() -> dict[str, Any]:
    """User message with implement command in array format."""
    return {
        "type": "user",
        "message": {
            "content": [
                {
                    "type": "text",
                    "text": "Please help me <command-name>/vibe-workflow:implement</command-name> this feature",
                }
            ]
        },
    }


@pytest.fixture
def user_message_regular() -> dict[str, Any]:
    """Regular user message without implement command."""
    return {
        "type": "user",
        "message": {"content": "Please help me fix this bug"},
    }


@pytest.fixture
def assistant_message_skill_implement() -> dict[str, Any]:
    """Assistant message with Skill tool call for implement."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "vibe-workflow:implement", "args": "some args"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_message_skill_implement_inplace() -> dict[str, Any]:
    """Assistant message with Skill tool call for implement-inplace."""
    return {
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
    }


@pytest.fixture
def assistant_message_task_create() -> dict[str, Any]:
    """Assistant message with TaskCreate (always creates pending task)."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "TaskCreate",
                    "input": {
                        "subject": "Implement feature X",
                        "description": "Detailed description of the task",
                        "activeForm": "Implementing feature X",
                    },
                }
            ]
        },
    }


@pytest.fixture
def assistant_message_task_update_incomplete() -> dict[str, Any]:
    """Assistant message with TaskUpdate marking task as in_progress."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "TaskUpdate",
                    "input": {
                        "taskId": "task-1",
                        "status": "in_progress",
                    },
                }
            ]
        },
    }


@pytest.fixture
def assistant_message_task_update_complete() -> dict[str, Any]:
    """Assistant message with TaskUpdate marking task as completed."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "TaskUpdate",
                    "input": {
                        "taskId": "task-1",
                        "status": "completed",
                    },
                }
            ]
        },
    }


# Backwards compatibility aliases for tests that still use old names
@pytest.fixture
def assistant_message_todo_write_incomplete(
    assistant_message_task_create,
) -> dict[str, Any]:
    """Deprecated: Use assistant_message_task_create instead."""
    return assistant_message_task_create


@pytest.fixture
def assistant_message_todo_write_all_complete(
    assistant_message_task_update_complete,
) -> dict[str, Any]:
    """Deprecated: Use assistant_message_task_update_complete instead."""
    return assistant_message_task_update_complete


@pytest.fixture
def assistant_message_with_block_marker() -> dict[str, Any]:
    """Assistant message containing the HOLD block marker."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "text",
                    "text": "HOLD: You have 3 pending/in-progress todos",
                }
            ]
        },
    }


@pytest.fixture
def assistant_message_with_multiple_block_markers() -> dict[str, Any]:
    """Assistant message containing multiple HOLD block markers."""
    return {
        "type": "assistant",
        "message": {"content": "HOLD: You have 3 todos. Also HOLD: You have 2 more."},
    }


@pytest.fixture
def assistant_message_regular() -> dict[str, Any]:
    """Regular assistant message without tool calls."""
    return {
        "type": "assistant",
        "message": {"content": [{"type": "text", "text": "I'll help you with that."}]},
    }
