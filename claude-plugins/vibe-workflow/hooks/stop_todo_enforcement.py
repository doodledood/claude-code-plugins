#!/usr/bin/env python3
"""
Stop hook that prevents premature stops during /implement and /implement-inplace workflows.

Blocks stop attempts when tasks are incomplete, with a safety valve after max blocks.
"""

from __future__ import annotations

import json
import os
import sys

from hook_utils import parse_transcript


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

    if not state.incomplete_tasks:
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

    task_count = len(state.incomplete_tasks)
    output = {
        "decision": "block",
        "reason": f"{task_count} tasks remain incomplete",
        "systemMessage": (
            f"HOLD: You have {task_count} pending/in-progress tasks and an /implement "
            f"workflow was detected in this session. If you're still implementing a plan, "
            f"continue working through the remaining tasks autonomously. If the user has "
            f"moved on to different work, you may proceed. Bias toward completion."
        ),
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
