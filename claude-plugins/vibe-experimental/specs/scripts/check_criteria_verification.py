#!/usr/bin/env python3
"""
Checks that every criterion in a spec has a verification method defined.

Usage: python check_criteria_verification.py <spec_file>
Exit code 0 = all have verification, non-zero = some missing
"""

import sys
import re
from pathlib import Path


def extract_criteria(content: str) -> list[dict]:
    """Extract criteria from spec content."""
    criteria = []

    # Pattern 1: AC-N format with description
    ac_pattern = re.compile(
        r"#{2,4}\s+(AC-\d+):\s*(.+?)(?=\n(?:#{2,4}|$))",
        re.DOTALL
    )

    for match in ac_pattern.finditer(content):
        criteria_id = match.group(1)
        criteria_block = match.group(2)

        has_verify = bool(re.search(
            r"(verification:|verify:|method:|```yaml[\s\S]*?method:)",
            criteria_block,
            re.IGNORECASE
        ))

        criteria.append({
            "id": criteria_id,
            "has_verification": has_verify,
            "block_preview": criteria_block[:100].strip()
        })

    # Pattern 2: YAML-style id: field
    yaml_pattern = re.compile(
        r"-\s*id:\s*([^\n]+)[\s\S]*?(?=-\s*id:|$)",
        re.MULTILINE
    )

    for match in yaml_pattern.finditer(content):
        criteria_id = match.group(1).strip()
        criteria_block = match.group(0)

        # Skip if already found via AC-N pattern
        if any(c["id"] == criteria_id for c in criteria):
            continue

        has_verify = bool(re.search(
            r"verify:",
            criteria_block,
            re.IGNORECASE
        ))

        criteria.append({
            "id": criteria_id,
            "has_verification": has_verify,
            "block_preview": criteria_block[:100].strip()
        })

    return criteria


def check_criteria_verification(filepath: str) -> tuple[bool, list[dict], list[dict]]:
    """
    Check all criteria have verification.
    Returns (all_have_verification, criteria_with_verification, criteria_without)
    """
    path = Path(filepath)
    if not path.exists():
        return False, [], [{"id": "FILE_NOT_FOUND", "has_verification": False}]

    content = path.read_text()
    criteria = extract_criteria(content)

    with_verification = [c for c in criteria if c["has_verification"]]
    without_verification = [c for c in criteria if not c["has_verification"]]

    all_have = len(without_verification) == 0 and len(criteria) > 0

    return all_have, with_verification, without_verification


def main():
    if len(sys.argv) != 2:
        print("Usage: python check_criteria_verification.py <spec_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    all_have, with_v, without_v = check_criteria_verification(filepath)

    print(f"Criteria verification check: {filepath}")
    print(f"  Total criteria found: {len(with_v) + len(without_v)}")
    print(f"  With verification: {len(with_v)}")
    print(f"  Without verification: {len(without_v)}")

    if without_v:
        print("\nCriteria missing verification:")
        for c in without_v:
            print(f"  - {c['id']}")

    if all_have:
        print("\n✓ All criteria have verification methods")
        sys.exit(0)
    else:
        print("\n✗ Some criteria missing verification methods")
        sys.exit(1)


if __name__ == "__main__":
    main()
