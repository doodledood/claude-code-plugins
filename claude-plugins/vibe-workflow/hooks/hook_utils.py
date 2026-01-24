#!/usr/bin/env python3
"""
Shared utilities for vibe-workflow hooks.

Contains transcript parsing, state extraction, and common reminder strings.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class TranscriptState:
    """State extracted from transcript parsing."""

    in_implement_workflow: bool
    incomplete_tasks: list[dict[str, Any]]
    prior_block_count: int

    @property
    def incomplete_todos(self) -> list[dict[str, Any]]:
        """Deprecated: Use incomplete_tasks instead."""
        return self.incomplete_tasks


# Session reminder strings
CODEBASE_EXPLORER_REMINDER = (
    "When you need to find relevant files for a task - whether for answering questions, "
    "planning implementation, debugging, or onboarding - prefer invoking the vibe-workflow:explore-codebase "
    'skill (e.g., "invoke vibe-workflow:explore-codebase with: your query") instead of the built-in Explore agent. '
    "It returns a structural overview + prioritized file list with precise line ranges. For thorough+ "
    "queries, it automatically launches parallel agents to explore orthogonal angles (implementation, "
    "usage, tests, config) and synthesizes a comprehensive reading list."
)

WEB_RESEARCHER_REMINDER = (
    "For non-trivial web research tasks - technology comparisons, best practices, API documentation, "
    "library evaluations, or any question requiring synthesis of multiple sources - prefer invoking "
    'the vibe-workflow:research-web skill (e.g., "invoke vibe-workflow:research-web with: your query") instead of '
    "calling WebSearch directly. For thorough+ queries, it launches parallel investigators across orthogonal "
    "facets, continues waves until satisficed, and synthesizes findings with confidence levels and "
    "source citations."
)


def build_system_reminder(content: str) -> str:
    """Wrap content in a system-reminder tag."""
    return f"<system-reminder>{content}</system-reminder>"


def build_session_reminders() -> str:
    """Build the standard session reminder context string."""
    return (
        build_system_reminder(CODEBASE_EXPLORER_REMINDER)
        + "\n"
        + build_system_reminder(WEB_RESEARCHER_REMINDER)
    )


def is_implement_workflow(line_data: dict[str, Any]) -> bool:
    """Check if this line indicates an implement workflow user command."""
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


def get_incomplete_tasks(line_data: dict[str, Any]) -> list[dict[str, Any]] | None:
    """Extract incomplete tasks from TaskCreate/TaskUpdate tool calls, or None if not a task tool.

    TaskCreate creates tasks with pending status by default.
    TaskUpdate can change task status to pending/in_progress/completed.
    """
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
        tool_name = block.get("name")
        if tool_name not in ("TaskCreate", "TaskUpdate"):
            continue
        tool_input = block.get("input", {})

        if tool_name == "TaskCreate":
            # TaskCreate creates a single task, always starts as pending
            return [
                {
                    "subject": tool_input.get("subject", ""),
                    "description": tool_input.get("description", ""),
                    "activeForm": tool_input.get("activeForm", ""),
                    "status": "pending",
                }
            ]
        elif tool_name == "TaskUpdate":
            # TaskUpdate updates a task's status
            status = tool_input.get("status", "pending")
            if status in ("pending", "in_progress"):
                return [
                    {
                        "taskId": tool_input.get("taskId", ""),
                        "status": status,
                    }
                ]
            # If status is completed, return empty list (no incomplete tasks)
            return []

    return None


# Backwards compatibility alias
def get_incomplete_todos(line_data: dict[str, Any]) -> list[dict[str, Any]] | None:
    """Deprecated: Use get_incomplete_tasks instead."""
    return get_incomplete_tasks(line_data)


def count_block_marker_in_line(
    line_data: dict[str, Any], marker: str = "HOLD: You have"
) -> int:
    """Count occurrences of a block marker in this line."""
    if line_data.get("type") != "assistant":
        return 0

    message = line_data.get("message", {})
    content = message.get("content", [])

    # Handle string content format
    if isinstance(content, str):
        return content.count(marker)

    count = 0
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "text":
            continue
        text = block.get("text", "")
        count += text.count(marker)

    return count


def parse_transcript(transcript_path: str) -> TranscriptState:
    """Parse transcript JSONL to extract implementation state."""
    in_implement = False
    latest_incomplete_tasks: list[dict[str, Any]] = []
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

                tasks = get_incomplete_tasks(data)
                if tasks is not None:
                    latest_incomplete_tasks = tasks

                block_count += count_block_marker_in_line(data)

    except FileNotFoundError:
        return TranscriptState(
            in_implement_workflow=False,
            incomplete_tasks=[],
            prior_block_count=0,
        )
    except OSError:
        return TranscriptState(
            in_implement_workflow=False,
            incomplete_tasks=[],
            prior_block_count=0,
        )

    return TranscriptState(
        in_implement_workflow=in_implement,
        incomplete_tasks=latest_incomplete_tasks,
        prior_block_count=block_count,
    )
