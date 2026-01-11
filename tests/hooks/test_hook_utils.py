"""
Tests for hook_utils.py - shared utilities for vibe-workflow hooks.
"""

from __future__ import annotations

from hook_utils import (
    CODEBASE_EXPLORER_REMINDER,
    WEB_RESEARCHER_REMINDER,
    TranscriptState,
    build_session_reminders,
    build_system_reminder,
    count_block_marker_in_line,
    get_incomplete_todos,
    is_implement_skill_call,
    is_implement_workflow,
    parse_transcript,
)


class TestBuildSystemReminder:
    """Tests for build_system_reminder function."""

    def test_wraps_content_in_tags(self):
        result = build_system_reminder("test content")
        assert result == "<system-reminder>test content</system-reminder>"

    def test_handles_empty_string(self):
        result = build_system_reminder("")
        assert result == "<system-reminder></system-reminder>"

    def test_handles_multiline_content(self):
        content = "line 1\nline 2\nline 3"
        result = build_system_reminder(content)
        assert result == f"<system-reminder>{content}</system-reminder>"

    def test_handles_special_characters(self):
        content = "Special chars: <>&\"'"
        result = build_system_reminder(content)
        assert content in result


class TestBuildSessionReminders:
    """Tests for build_session_reminders function."""

    def test_contains_codebase_explorer_reminder(self):
        result = build_session_reminders()
        assert CODEBASE_EXPLORER_REMINDER in result

    def test_contains_web_researcher_reminder(self):
        result = build_session_reminders()
        assert WEB_RESEARCHER_REMINDER in result

    def test_wraps_in_system_reminder_tags(self):
        result = build_session_reminders()
        assert "<system-reminder>" in result
        assert "</system-reminder>" in result

    def test_contains_two_system_reminders(self):
        result = build_session_reminders()
        assert result.count("<system-reminder>") == 2
        assert result.count("</system-reminder>") == 2


class TestIsImplementWorkflow:
    """Tests for is_implement_workflow function."""

    def test_detects_implement_command_string_content(
        self, user_message_implement_command
    ):
        assert is_implement_workflow(user_message_implement_command) is True

    def test_detects_implement_command_array_content(
        self, user_message_implement_command_array
    ):
        assert is_implement_workflow(user_message_implement_command_array) is True

    def test_returns_false_for_regular_message(self, user_message_regular):
        assert is_implement_workflow(user_message_regular) is False

    def test_returns_false_for_assistant_message(self, assistant_message_regular):
        assert is_implement_workflow(assistant_message_regular) is False

    def test_returns_false_for_empty_content(self):
        data = {"type": "user", "message": {"content": ""}}
        assert is_implement_workflow(data) is False

    def test_returns_false_for_missing_message(self):
        data = {"type": "user"}
        assert is_implement_workflow(data) is False

    def test_returns_false_for_non_dict_blocks(self):
        data = {
            "type": "user",
            "message": {"content": ["not a dict", 123, None]},
        }
        assert is_implement_workflow(data) is False

    def test_detects_implement_inplace_variant(self):
        data = {
            "type": "user",
            "message": {
                "content": "<command-name>/vibe-workflow:implement-inplace</command-name>"
            },
        }
        assert is_implement_workflow(data) is True


class TestIsImplementSkillCall:
    """Tests for is_implement_skill_call function."""

    def test_detects_implement_skill_call(self, assistant_message_skill_implement):
        assert is_implement_skill_call(assistant_message_skill_implement) is True

    def test_detects_implement_inplace_skill_call(
        self, assistant_message_skill_implement_inplace
    ):
        assert (
            is_implement_skill_call(assistant_message_skill_implement_inplace) is True
        )

    def test_returns_false_for_user_message(self, user_message_regular):
        assert is_implement_skill_call(user_message_regular) is False

    def test_returns_false_for_other_skill_calls(self):
        data = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Skill",
                        "input": {"skill": "vibe-workflow:plan"},
                    }
                ]
            },
        }
        assert is_implement_skill_call(data) is False

    def test_returns_false_for_non_skill_tool_calls(self):
        data = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Bash",
                        "input": {"command": "ls"},
                    }
                ]
            },
        }
        assert is_implement_skill_call(data) is False

    def test_returns_false_for_string_content(self):
        data = {
            "type": "assistant",
            "message": {"content": "Just text, no tool calls"},
        }
        assert is_implement_skill_call(data) is False

    def test_returns_false_for_missing_input(self):
        data = {
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "name": "Skill"}]},
        }
        assert is_implement_skill_call(data) is False


class TestGetIncompleteTodos:
    """Tests for get_incomplete_todos function."""

    def test_extracts_incomplete_todos(self, assistant_message_todo_write_incomplete):
        result = get_incomplete_todos(assistant_message_todo_write_incomplete)
        assert result is not None
        assert len(result) == 2
        statuses = [t["status"] for t in result]
        assert "in_progress" in statuses
        assert "pending" in statuses
        assert "completed" not in statuses

    def test_returns_empty_list_when_all_complete(
        self, assistant_message_todo_write_all_complete
    ):
        result = get_incomplete_todos(assistant_message_todo_write_all_complete)
        assert result is not None
        assert len(result) == 0

    def test_returns_none_for_non_todowrite(self, assistant_message_regular):
        result = get_incomplete_todos(assistant_message_regular)
        assert result is None

    def test_returns_none_for_user_message(self, user_message_regular):
        result = get_incomplete_todos(user_message_regular)
        assert result is None

    def test_returns_none_for_string_content(self):
        data = {
            "type": "assistant",
            "message": {"content": "Just text"},
        }
        result = get_incomplete_todos(data)
        assert result is None

    def test_handles_empty_todos_list(self):
        data = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "TodoWrite",
                        "input": {"todos": []},
                    }
                ]
            },
        }
        result = get_incomplete_todos(data)
        assert result is not None
        assert len(result) == 0

    def test_handles_missing_todos_key(self):
        data = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "TodoWrite",
                        "input": {},
                    }
                ]
            },
        }
        result = get_incomplete_todos(data)
        assert result is not None
        assert len(result) == 0


class TestCountBlockMarkerInLine:
    """Tests for count_block_marker_in_line function."""

    def test_counts_single_marker_array_content(
        self, assistant_message_with_block_marker
    ):
        result = count_block_marker_in_line(assistant_message_with_block_marker)
        assert result == 1

    def test_counts_multiple_markers_string_content(
        self, assistant_message_with_multiple_block_markers
    ):
        result = count_block_marker_in_line(
            assistant_message_with_multiple_block_markers
        )
        assert result == 2

    def test_returns_zero_for_no_markers(self, assistant_message_regular):
        result = count_block_marker_in_line(assistant_message_regular)
        assert result == 0

    def test_returns_zero_for_user_message(self, user_message_regular):
        result = count_block_marker_in_line(user_message_regular)
        assert result == 0

    def test_custom_marker(self):
        data = {
            "type": "assistant",
            "message": {"content": "CUSTOM_MARKER here and CUSTOM_MARKER again"},
        }
        result = count_block_marker_in_line(data, marker="CUSTOM_MARKER")
        assert result == 2

    def test_returns_zero_for_empty_content(self):
        data = {
            "type": "assistant",
            "message": {"content": ""},
        }
        result = count_block_marker_in_line(data)
        assert result == 0


class TestParseTranscript:
    """Tests for parse_transcript function."""

    def test_parses_empty_transcript(self, temp_transcript):
        path = temp_transcript([])
        result = parse_transcript(path)
        assert result.in_implement_workflow is False
        assert result.incomplete_todos == []
        assert result.prior_block_count == 0

    def test_detects_implement_workflow_from_user_command(
        self, temp_transcript, user_message_implement_command
    ):
        path = temp_transcript([user_message_implement_command])
        result = parse_transcript(path)
        assert result.in_implement_workflow is True

    def test_detects_implement_workflow_from_skill_call(
        self, temp_transcript, assistant_message_skill_implement
    ):
        path = temp_transcript([assistant_message_skill_implement])
        result = parse_transcript(path)
        assert result.in_implement_workflow is True

    def test_extracts_latest_incomplete_todos(
        self, temp_transcript, assistant_message_todo_write_incomplete
    ):
        path = temp_transcript([assistant_message_todo_write_incomplete])
        result = parse_transcript(path)
        assert len(result.incomplete_todos) == 2

    def test_uses_latest_todo_write(self, temp_transcript):
        first_todos = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "TodoWrite",
                        "input": {
                            "todos": [
                                {
                                    "content": "Old task",
                                    "status": "pending",
                                    "activeForm": "Old",
                                },
                            ]
                        },
                    }
                ]
            },
        }
        second_todos = {
            "type": "assistant",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "TodoWrite",
                        "input": {
                            "todos": [
                                {
                                    "content": "New task 1",
                                    "status": "pending",
                                    "activeForm": "New 1",
                                },
                                {
                                    "content": "New task 2",
                                    "status": "in_progress",
                                    "activeForm": "New 2",
                                },
                            ]
                        },
                    }
                ]
            },
        }
        path = temp_transcript([first_todos, second_todos])
        result = parse_transcript(path)
        assert len(result.incomplete_todos) == 2
        assert result.incomplete_todos[0]["content"] == "New task 1"

    def test_counts_block_markers(
        self, temp_transcript, assistant_message_with_block_marker
    ):
        path = temp_transcript(
            [
                assistant_message_with_block_marker,
                assistant_message_with_block_marker,
            ]
        )
        result = parse_transcript(path)
        assert result.prior_block_count == 2

    def test_handles_file_not_found(self):
        result = parse_transcript("/nonexistent/path/transcript.jsonl")
        assert result.in_implement_workflow is False
        assert result.incomplete_todos == []
        assert result.prior_block_count == 0

    def test_handles_invalid_json_lines(self, temp_transcript, tmp_path):
        transcript_file = tmp_path / "bad_transcript.jsonl"
        with open(transcript_file, "w") as f:
            f.write("not valid json\n")
            f.write('{"type": "user", "message": {"content": "valid"}}\n')
            f.write("also invalid\n")
        result = parse_transcript(str(transcript_file))
        # Should not crash, just skip invalid lines
        assert result.in_implement_workflow is False

    def test_handles_empty_lines(self, temp_transcript, tmp_path):
        transcript_file = tmp_path / "with_empty.jsonl"
        with open(transcript_file, "w") as f:
            f.write('{"type": "user", "message": {"content": "test"}}\n')
            f.write("\n")
            f.write("   \n")
            f.write('{"type": "assistant", "message": {"content": "response"}}\n')
        result = parse_transcript(str(transcript_file))
        # Should not crash on empty lines
        assert isinstance(result, TranscriptState)

    def test_full_workflow_scenario(self, temp_transcript):
        """Test a realistic workflow with implement command, todos, and blocks."""
        lines = [
            {
                "type": "user",
                "message": {
                    "content": "<command-name>/vibe-workflow:implement</command-name> feature X"
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
            {
                "type": "assistant",
                "message": {"content": "HOLD: You have 2 pending todos"},
            },
        ]
        path = temp_transcript(lines)
        result = parse_transcript(path)

        assert result.in_implement_workflow is True
        assert len(result.incomplete_todos) == 2
        assert result.prior_block_count == 1
