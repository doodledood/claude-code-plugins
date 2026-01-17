#!/usr/bin/env python3
"""
Validates that a spec file has all required sections and structure.

Usage: python validate_spec_structure.py <spec_file>
Exit code 0 = valid, non-zero = invalid
"""

import sys
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    "overview",
    "acceptance criteria",
    "rejection criteria",
    "examples",
    "pre-mortem",
    "verification infrastructure",
]

REQUIRED_SUBSECTIONS = {
    "overview": ["problem statement", "solution", "success measure"],
    "examples": ["accepted example", "rejected example"],
}


def normalize(text: str) -> str:
    """Normalize text for comparison."""
    return text.lower().strip()


def extract_headings(content: str) -> list[tuple[int, str]]:
    """Extract markdown headings with their level."""
    headings = []
    for line in content.split("\n"):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headings.append((level, title))
    return headings


def check_required_sections(headings: list[tuple[int, str]]) -> list[str]:
    """Check if all required sections are present."""
    missing = []
    heading_texts = [normalize(h[1]) for h in headings]

    for section in REQUIRED_SECTIONS:
        found = any(section in h for h in heading_texts)
        if not found:
            missing.append(section)

    return missing


def check_subsections(headings: list[tuple[int, str]]) -> list[str]:
    """Check if required subsections are present."""
    missing = []
    heading_texts = [normalize(h[1]) for h in headings]

    for parent, children in REQUIRED_SUBSECTIONS.items():
        for child in children:
            found = any(child in h for h in heading_texts)
            if not found:
                missing.append(f"{parent} -> {child}")

    return missing


def check_criteria_have_ids(content: str) -> bool:
    """Check if criteria have IDs (AC-N format or id: field)."""
    # Look for AC-N pattern or YAML id: field
    has_ac_pattern = bool(re.search(r"AC-\d+", content))
    has_id_field = bool(re.search(r"^\s*-?\s*id:", content, re.MULTILINE))
    return has_ac_pattern or has_id_field


def check_verification_methods(content: str) -> bool:
    """Check if verification methods are defined."""
    # Look for verification blocks
    has_verify = bool(re.search(r"(verify:|verification:|method:)", content, re.IGNORECASE))
    return has_verify


def validate_spec(filepath: str) -> tuple[bool, list[str]]:
    """Validate a spec file. Returns (is_valid, list_of_issues)."""
    issues = []

    path = Path(filepath)
    if not path.exists():
        return False, [f"File not found: {filepath}"]

    content = path.read_text()
    headings = extract_headings(content)

    # Check required sections
    missing_sections = check_required_sections(headings)
    if missing_sections:
        issues.extend([f"Missing section: {s}" for s in missing_sections])

    # Check subsections
    missing_subsections = check_subsections(headings)
    if missing_subsections:
        issues.extend([f"Missing subsection: {s}" for s in missing_subsections])

    # Check criteria have IDs
    if not check_criteria_have_ids(content):
        issues.append("Criteria should have IDs (AC-N format or id: field)")

    # Check verification methods exist
    if not check_verification_methods(content):
        issues.append("No verification methods found")

    return len(issues) == 0, issues


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_spec_structure.py <spec_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    is_valid, issues = validate_spec(filepath)

    if is_valid:
        print(f"✓ Spec structure is valid: {filepath}")
        sys.exit(0)
    else:
        print(f"✗ Spec structure issues found in: {filepath}")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
