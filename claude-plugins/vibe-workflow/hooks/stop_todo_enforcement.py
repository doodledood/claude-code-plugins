#!/usr/bin/env python3
"""
Stop hook that prevents premature stops during /implement and /implement-inplace workflows.

Blocks stop attempts when todos are incomplete, with a safety valve after max blocks.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any


@dataclass
class TranscriptState:
    """State extracted from transcript parsing."""

    in_implement_workflow: bool
    incomplete_todos: list[dict[str, Any]]
    prior_block_count: int


def is_implement_workflow(line_data: dict[str, Any]) -> bool:
    """Check if this line indicates an implement workflow."""
    if line_data.get("type") != "user":
        return False

    message = line_data.get("message", {})
    content = message.get("content", [])

    # Handle string content format - match any implement variant
    if isinstance(content, str):
        return "<command-name>/vibe-workflow:implement" in content

    # Handle array content format
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "text":
            continue
        text = block.get("text", "")
        if "<command-name>/vibe-workflow:implement" in text:
            return True

    return False


def is_implement_skill_call(line_data: dict[str, Any]) -> bool:
    """Check if this line contains a Skill tool call for implement."""
    if line_data.get("type") != "assistant":
        return False

    message = line_data.get("message", {})
    content = message.get("content", [])

    # String content won't contain tool_use blocks
    if isinstance(content, str):
        return False

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        if block.get("name") != "Skill":
            continue
        tool_input = block.get("input", {})
        skill = tool_input.get("skill", "")
        if "implement" in skill or "implement-inplace" in skill:
            return True

    return False


def get_incomplete_todos(line_data: dict[str, Any]) -> list[dict[str, Any]] | None:
    """Extract incomplete todos from a TodoWrite tool call, or None if not a TodoWrite."""
    if line_data.get("type") != "assistant":
        return None

    message = line_data.get("message", {})
    content = message.get("content", [])

    # String content won't contain tool_use blocks
    if isinstance(content, str):
        return None

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "tool_use":
            continue
        if block.get("name") != "TodoWrite":
            continue
        tool_input = block.get("input", {})
        todos = tool_input.get("todos", [])
        return [t for t in todos if t.get("status") in ("pending", "in_progress")]

    return None


def count_block_in_line(line_data: dict[str, Any]) -> int:
    """Count occurrences of our block marker in this line."""
    if line_data.get("type") != "assistant":
        return 0

    message = line_data.get("message", {})
    content = message.get("content", [])

    # Handle string content format
    if isinstance(content, str):
        return content.count("HOLD: You have")

    count = 0
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "text":
            continue
        text = block.get("text", "")
        count += text.count("HOLD: You have")

    return count


def parse_transcript(transcript_path: str) -> TranscriptState:
    """Parse transcript JSONL to extract implementation state."""
    in_implement = False
    latest_incomplete_todos: list[dict[str, Any]] = []
    block_count = 0

    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                if is_implement_workflow(data) or is_implement_skill_call(data):
                    in_implement = True

                todos = get_incomplete_todos(data)
                if todos is not None:
                    latest_incomplete_todos = todos

                block_count += count_block_in_line(data)

    except FileNotFoundError:
        return TranscriptState(
            in_implement_workflow=False,
            incomplete_todos=[],
            prior_block_count=0,
        )
    except OSError:
        return TranscriptState(
            in_implement_workflow=False,
            incomplete_todos=[],
            prior_block_count=0,
        )

    return TranscriptState(
        in_implement_workflow=in_implement,
        incomplete_todos=latest_incomplete_todos,
        prior_block_count=block_count,
    )


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    state = parse_transcript(transcript_path)

    if not state.in_implement_workflow:
        sys.exit(0)

    if not state.incomplete_todos:
        sys.exit(0)

    max_blocks = int(os.environ.get("IMPLEMENT_MAX_BLOCKS", "5"))

    if state.prior_block_count >= max_blocks:
        output = {
            "decision": "approve",
            "reason": "Safety valve triggered",
            "systemMessage": (
                f"Warning: Implementation incomplete but max blocks reached. "
                f"Allowing stop after {state.prior_block_count} blocked attempts."
            ),
        }
        print(json.dumps(output))
        sys.exit(0)

    todo_count = len(state.incomplete_todos)
    output = {
        "decision": "block",
        "reason": f"{todo_count} todos remain incomplete",
        "systemMessage": (
            f"HOLD: You have {todo_count} pending/in-progress todos and an /implement "
            f"workflow was detected in this session. If you're still implementing a plan, "
            f"continue working through the remaining todos autonomously. If the user has "
            f"moved on to different work, you may proceed. Bias toward completion."
        ),
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
