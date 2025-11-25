#!/usr/bin/env python3
"""
Hook script to detect planning keywords in user messages and remind Claude to activate planning skills.
"""
import json
import re
import sys


def main() -> None:
    # Read the hook input from stdin
    input_data = sys.stdin.read()

    try:
        # Parse the JSON input
        hook_input = json.loads(input_data)
        user_message = hook_input.get("prompt", "").lower()
    except (json.JSONDecodeError, KeyError):
        # If we can't parse, just pass through
        sys.exit(0)

    # Check for planning keywords
    has_execplan = (
        bool(re.search(r"\bexec\s*plan\b", user_message)) or "execplan" in user_message
    )
    has_plan = bool(re.search(r"\bplan\b", user_message))

    # Output system reminder if planning keywords detected
    if has_execplan:
        print("<system-reminder>")
        print(
            'The user mentioned "execplan" or "exec plan". If you have not already activated the execplan skill and this appears to be a request for creating an execution plan, you should use the Skill tool with skill="execplan" to load the ExecPlan methodology BEFORE beginning any planning work.'
        )
        print("</system-reminder>")
    elif has_plan:
        print("<system-reminder>")
        print(
            'The user mentioned "plan" (without "exec plan" or "execplan"). If you have not already activated the plan skill and this appears to be a request for creating a plan, you should use the Skill tool with skill="plan" to load the Plan methodology BEFORE beginning any planning work.'
        )
        print("</system-reminder>")

    sys.exit(0)


if __name__ == "__main__":
    main()
