"""
Tests for vibe-experimental stop_implement_hook.

Tests the stop hook that enforces verification-first workflow for /implement.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

# Add vibe-experimental hooks directory to path
EXPERIMENTAL_HOOKS_DIR = (
    Path(__file__).parent.parent.parent
    / "claude-plugins"
    / "vibe-experimental"
    / "hooks"
)


@pytest.fixture
def experimental_hook_path() -> Path:
    """Path to the stop_implement_hook.py script."""
    return EXPERIMENTAL_HOOKS_DIR / "stop_implement_hook.py"


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
def user_implement_command() -> dict[str, Any]:
    """User message invoking /implement."""
    return {
        "type": "user",
        "message": {
            "content": "<command-name>/vibe-experimental:implement</command-name> /tmp/spec.md"
        },
    }


@pytest.fixture
def assistant_skill_implement() -> dict[str, Any]:
    """Assistant Skill tool call for implement."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "vibe-experimental:implement", "args": "/tmp/spec.md"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_skill_verify() -> dict[str, Any]:
    """Assistant Skill tool call for verify."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "vibe-experimental:verify", "args": "/tmp/spec.md"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_skill_done() -> dict[str, Any]:
    """Assistant Skill tool call for done."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "vibe-experimental:done"},
                }
            ]
        },
    }


@pytest.fixture
def assistant_skill_escalate() -> dict[str, Any]:
    """Assistant Skill tool call for escalate."""
    return {
        "type": "assistant",
        "message": {
            "content": [
                {
                    "type": "tool_use",
                    "name": "Skill",
                    "input": {"skill": "vibe-experimental:escalate", "args": "AC-5 blocking"},
                }
            ]
        },
    }


def run_hook(hook_path: Path, hook_input: dict[str, Any]) -> dict[str, Any] | None:
    """Run the hook script and return parsed output, or None if no output."""
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input=json.dumps(hook_input),
        capture_output=True,
        text=True,
        cwd=str(EXPERIMENTAL_HOOKS_DIR),
    )
    if result.stdout.strip():
        return json.loads(result.stdout)
    return None


class TestStopHookBlocking:
    """Tests for stop hook blocking behavior."""

    def test_blocks_without_done(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_implement_command: dict[str, Any],
    ):
        """Stop should be blocked when /implement started but no /done or /escalate."""
        transcript_path = temp_transcript([user_implement_command])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "block"
        assert "verify" in result["systemMessage"].lower()

    def test_blocks_with_verify_only(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_implement_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
    ):
        """Stop should be blocked when /verify was called but returned failures (no /done)."""
        transcript_path = temp_transcript([user_implement_command, assistant_skill_verify])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is not None
        assert result["decision"] == "block"


class TestStopHookAllowing:
    """Tests for stop hook allowing behavior."""

    def test_allows_with_done(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_implement_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
        assistant_skill_done: dict[str, Any],
    ):
        """Stop should be allowed when /done exists after /implement."""
        transcript_path = temp_transcript([
            user_implement_command,
            assistant_skill_verify,
            assistant_skill_done,
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # None means no output, which means allow (exit 0)
        assert result is None

    def test_allows_with_escalate(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_implement_command: dict[str, Any],
        assistant_skill_verify: dict[str, Any],
        assistant_skill_escalate: dict[str, Any],
    ):
        """Stop should be allowed when /escalate exists after /implement."""
        transcript_path = temp_transcript([
            user_implement_command,
            assistant_skill_verify,
            assistant_skill_escalate,
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_allows_no_implement(
        self,
        experimental_hook_path: Path,
        temp_transcript,
    ):
        """Stop should be allowed when no /implement in transcript."""
        transcript_path = temp_transcript([
            {"type": "user", "message": {"content": "Hello"}}
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None


class TestStopHookFreshStack:
    """Tests for fresh stack behavior per /implement."""

    def test_fresh_stack(
        self,
        experimental_hook_path: Path,
        temp_transcript,
        user_implement_command: dict[str, Any],
        assistant_skill_done: dict[str, Any],
    ):
        """Second /implement should reset flow state."""
        # First /implement with /done, then second /implement without /done
        second_implement = {
            "type": "user",
            "message": {
                "content": "<command-name>/vibe-experimental:implement</command-name> /tmp/spec2.md"
            },
        }
        transcript_path = temp_transcript([
            user_implement_command,
            assistant_skill_done,
            second_implement,  # New /implement, no /done after
        ])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        # Should block because second /implement has no /done
        assert result is not None
        assert result["decision"] == "block"


class TestStopHookEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_transcript(
        self,
        experimental_hook_path: Path,
        temp_transcript,
    ):
        """Should allow stop on empty transcript."""
        transcript_path = temp_transcript([])
        hook_input = {"transcript_path": transcript_path}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_missing_transcript(
        self,
        experimental_hook_path: Path,
    ):
        """Should allow stop on missing transcript."""
        hook_input = {"transcript_path": "/nonexistent/path.jsonl"}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_no_transcript_path(
        self,
        experimental_hook_path: Path,
    ):
        """Should allow stop when no transcript_path provided."""
        hook_input = {}

        result = run_hook(experimental_hook_path, hook_input)

        assert result is None

    def test_malformed_json_in_transcript(
        self,
        experimental_hook_path: Path,
        tmp_path: Path,
    ):
        """Should handle malformed JSON in transcript gracefully."""
        transcript_file = tmp_path / "transcript.jsonl"
        with open(transcript_file, "w") as f:
            f.write("not valid json\n")
            f.write('{"type": "user"}\n')

        hook_input = {"transcript_path": str(transcript_file)}

        result = run_hook(experimental_hook_path, hook_input)

        # Should allow (fail open) on parsing errors
        assert result is None
