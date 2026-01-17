#!/usr/bin/env python3
"""
Shared utilities for vibe-experimental hooks.

Contains transcript parsing for skill invocation detection.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any


@dataclass
class ImplementFlowState:
    """State of the /implement workflow from transcript parsing."""

    has_implement: bool  # /implement was invoked
    has_verify: bool  # /verify was called after last /implement
    has_done: bool  # /done was called after last /implement
    has_escalate: bool  # /escalate was called after last /implement


def is_skill_invocation(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if this line contains a Skill tool call for the given skill."""
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
        # Match both "skill-name" and "plugin:skill-name" formats
        if skill == skill_name or skill.endswith(f":{skill_name}"):
            return True

    return False


def is_user_skill_command(line_data: dict[str, Any], skill_name: str) -> bool:
    """Check if this line is a user command invoking the skill."""
    if line_data.get("type") != "user":
        return False

    message = line_data.get("message", {})
    content = message.get("content", [])

    # Handle string content format
    if isinstance(content, str):
        return f"<command-name>/vibe-experimental:{skill_name}" in content

    # Handle array content format
    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") != "text":
            continue
        text = block.get("text", "")
        if f"<command-name>/vibe-experimental:{skill_name}" in text:
            return True

    return False


def parse_implement_flow(transcript_path: str) -> ImplementFlowState:
    """
    Parse transcript to determine the state of /implement workflow.

    Tracks the most recent /implement invocation and what happened after it.
    Each new /implement resets the flow state.
    """
    has_implement = False
    has_verify = False
    has_done = False
    has_escalate = False

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

                # Check for /implement (user command or skill call)
                if is_user_skill_command(data, "implement") or is_skill_invocation(
                    data, "implement"
                ):
                    # New /implement resets the flow
                    has_implement = True
                    has_verify = False
                    has_done = False
                    has_escalate = False

                # Check for /verify after /implement
                if has_implement and is_skill_invocation(data, "verify"):
                    has_verify = True

                # Check for /done after /implement
                if has_implement and is_skill_invocation(data, "done"):
                    has_done = True

                # Check for /escalate after /implement
                if has_implement and is_skill_invocation(data, "escalate"):
                    has_escalate = True

    except FileNotFoundError:
        return ImplementFlowState(
            has_implement=False,
            has_verify=False,
            has_done=False,
            has_escalate=False,
        )
    except OSError:
        return ImplementFlowState(
            has_implement=False,
            has_verify=False,
            has_done=False,
            has_escalate=False,
        )

    return ImplementFlowState(
        has_implement=has_implement,
        has_verify=has_verify,
        has_done=has_done,
        has_escalate=has_escalate,
    )
