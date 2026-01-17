#!/usr/bin/env python3
"""
Validates that verification methods in a spec are executable:
- Bash commands are syntactically valid
- Subagent references are defined
- Manual verifications are flagged

Usage: python validate_spec_executable.py <spec_file>
Exit code 0 = all executable, non-zero = issues found
"""

import sys
import re
import subprocess
from pathlib import Path


def extract_verification_methods(content: str) -> list[dict]:
    """Extract verification method blocks from spec."""
    methods = []

    # Find verification blocks
    verify_pattern = re.compile(
        r"verify:\s*\n([\s\S]*?)(?=\n\s*(?:-\s*id:|#{2,4}|$))",
        re.MULTILINE
    )

    for match in verify_pattern.finditer(content):
        block = match.group(1)

        # Determine method type
        method_type = None
        if re.search(r"method:\s*bash", block, re.IGNORECASE):
            method_type = "bash"
        elif re.search(r"method:\s*subagent", block, re.IGNORECASE):
            method_type = "subagent"
        elif re.search(r"method:\s*manual", block, re.IGNORECASE):
            method_type = "manual"

        # Extract command for bash
        command = None
        command_match = re.search(r"command:\s*[\"']?(.+?)[\"']?\s*$", block, re.MULTILINE)
        if command_match:
            command = command_match.group(1).strip()

        # Extract agent name for subagent
        agent = None
        agent_match = re.search(r"agent:\s*([^\n]+)", block)
        if agent_match:
            agent = agent_match.group(1).strip()

        methods.append({
            "type": method_type,
            "command": command,
            "agent": agent,
            "block": block[:200]
        })

    return methods


def check_bash_syntax(command: str) -> tuple[bool, str]:
    """Check if a bash command is syntactically valid."""
    if not command:
        return False, "Empty command"

    # Use bash -n for syntax check (doesn't execute)
    try:
        result = subprocess.run(
            ["bash", "-n", "-c", command],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, "Valid"
        else:
            return False, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "Syntax check timed out"
    except Exception as e:
        return False, str(e)


def validate_methods(methods: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Validate verification methods.
    Returns (valid, invalid, manual_flagged)
    """
    valid = []
    invalid = []
    manual_flagged = []

    for method in methods:
        if method["type"] == "bash":
            if method["command"]:
                is_valid, msg = check_bash_syntax(method["command"])
                if is_valid:
                    valid.append({**method, "status": "valid"})
                else:
                    invalid.append({**method, "status": "invalid", "reason": msg})
            else:
                invalid.append({**method, "status": "invalid", "reason": "No command specified"})

        elif method["type"] == "subagent":
            if method["agent"]:
                # Subagents are valid if they have a name (actual existence checked elsewhere)
                valid.append({**method, "status": "valid (agent defined)"})
            else:
                invalid.append({**method, "status": "invalid", "reason": "No agent specified"})

        elif method["type"] == "manual":
            manual_flagged.append({**method, "status": "manual - requires human"})

        elif method["type"] is None:
            invalid.append({**method, "status": "invalid", "reason": "Unknown method type"})

    return valid, invalid, manual_flagged


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_spec_executable.py <spec_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    path = Path(filepath)

    if not path.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    content = path.read_text()
    methods = extract_verification_methods(content)

    print(f"Verification executability check: {filepath}")
    print(f"  Total verification methods found: {len(methods)}")

    valid, invalid, manual = validate_methods(methods)

    print(f"  Valid: {len(valid)}")
    print(f"  Invalid: {len(invalid)}")
    print(f"  Manual (flagged): {len(manual)}")

    if invalid:
        print("\nInvalid verification methods:")
        for m in invalid:
            print(f"  - Type: {m['type']}, Reason: {m['reason']}")
            if m.get('command'):
                print(f"    Command: {m['command'][:80]}")

    if manual:
        print("\nManual verifications (require human):")
        for m in manual:
            print(f"  - {m['block'][:80]}...")

    if invalid:
        print("\n✗ Some verification methods are not executable")
        sys.exit(1)
    else:
        print("\n✓ All verification methods are executable (manual ones flagged)")
        sys.exit(0)


if __name__ == "__main__":
    main()
