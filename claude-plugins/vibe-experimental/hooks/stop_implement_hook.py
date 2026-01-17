#!/usr/bin/env python3
"""
Stop hook that enforces verification-first workflow for /implement.

Blocks stop attempts unless /done or /escalate was called after /implement.
This prevents the LLM from declaring "done" without verification.

Decision matrix:
- No /implement: ALLOW (not in flow)
- /implement + /done: ALLOW (verified complete)
- /implement + /escalate: ALLOW (properly escalated)
- /implement only: BLOCK (must verify first)
- /implement + /verify only: BLOCK (verify returned failures, keep working)
"""
from __future__ import annotations

import json
import sys

from hook_utils import parse_implement_flow


def main() -> None:
    """Main hook entry point."""
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except (json.JSONDecodeError, OSError):
        # On any error, allow stop (fail open)
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path:
        sys.exit(0)

    state = parse_implement_flow(transcript_path)

    # Not in /implement flow - allow stop
    if not state.has_implement:
        sys.exit(0)

    # /done was called - verified complete, allow stop
    if state.has_done:
        sys.exit(0)

    # /escalate was called - properly escalated, allow stop
    if state.has_escalate:
        sys.exit(0)

    # /implement was called but neither /done nor /escalate
    # Block with guidance
    output = {
        "decision": "block",
        "reason": "Implementation not verified",
        "systemMessage": (
            "Cannot stop - /implement workflow is incomplete. "
            "Run /verify to check acceptance criteria. "
            "If all criteria pass, /verify will call /done. "
            "If genuinely stuck after /verify, call /escalate with evidence."
        ),
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
