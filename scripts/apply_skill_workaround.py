#!/usr/bin/env python3
"""
Apply workaround for Claude Code issue #17271.

Plugin skills don't appear in slash command autocomplete because the `name`
field in frontmatter causes Claude Code to strip the plugin namespace prefix.

Workaround:
1. git mv SKILL.md to <skillname>.md (preserves rename history)
2. Remove the `name` field from frontmatter in the new file
3. Create symlink: SKILL.md -> <skillname>.md
"""

import re
import subprocess
import sys
from pathlib import Path


def extract_name_from_frontmatter(content: str) -> str | None:
    """Extract the name field from YAML frontmatter."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    frontmatter = match.group(1)
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    if not name_match:
        return None

    name = name_match.group(1).strip()
    # Remove quotes if present
    if (name.startswith("'") and name.endswith("'")) or (name.startswith('"') and name.endswith('"')):
        name = name[1:-1]
    return name


def remove_name_from_frontmatter(content: str) -> str:
    """Remove the name field from YAML frontmatter."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return content

    frontmatter = match.group(1)
    # Remove the name line
    new_frontmatter = re.sub(r"^name:\s*.+\n?", "", frontmatter, flags=re.MULTILINE)
    # Clean up any leading/trailing whitespace in frontmatter
    new_frontmatter = new_frontmatter.strip()

    return f"---\n{new_frontmatter}\n---{content[match.end():]}"


def apply_workaround(skill_md_path: Path, dry_run: bool = False, no_symlink: bool = False) -> bool:
    """Apply the workaround to a single SKILL.md file."""
    # Skip if already a symlink
    if skill_md_path.is_symlink():
        print(f"  SKIP (already symlink): {skill_md_path}")
        return False

    content = skill_md_path.read_text()
    name = extract_name_from_frontmatter(content)

    if not name:
        print(f"  SKIP (no name field): {skill_md_path}")
        return False

    target_name = f"{name}.md"
    target_path = skill_md_path.parent / target_name

    # Check if target already exists
    if target_path.exists() and not target_path.is_symlink():
        print(f"  SKIP (target exists): {skill_md_path} -> {target_name}")
        return False

    new_content = remove_name_from_frontmatter(content)

    if dry_run:
        print(f"  DRY RUN: {skill_md_path}")
        print(f"    -> git mv to: {target_path}")
        if not no_symlink:
            print(f"    -> Create symlink: SKILL.md -> {target_name}")
        return True

    # Step 1: git mv SKILL.md to <name>.md (preserves rename history)
    subprocess.run(
        ["git", "mv", str(skill_md_path), str(target_path)],
        check=True,
        capture_output=True,
    )

    # Step 2: Update the content in the new file to remove the name field
    target_path.write_text(new_content)

    # Step 3: Stage the content change
    subprocess.run(
        ["git", "add", str(target_path)],
        check=True,
        capture_output=True,
    )

    # Step 4: Create symlink SKILL.md -> <name>.md (unless --no-symlink)
    if not no_symlink:
        skill_md_path.symlink_to(target_name)
        subprocess.run(
            ["git", "add", str(skill_md_path)],
            check=True,
            capture_output=True,
        )

    print(f"  APPLIED: {skill_md_path.parent.name}/SKILL.md -> {target_name}")
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    no_symlink = "--no-symlink" in sys.argv

    if dry_run:
        print("=== DRY RUN MODE ===\n")
    if no_symlink:
        print("=== NO SYMLINK MODE ===\n")

    repo_root = Path(__file__).parent.parent

    # Find all SKILL.md files in claude-plugins and .claude directories
    skill_files = list(repo_root.glob("claude-plugins/**/skills/**/SKILL.md"))
    skill_files.extend(repo_root.glob(".claude/skills/**/SKILL.md"))

    print(f"Found {len(skill_files)} SKILL.md files\n")

    applied = 0
    for skill_path in sorted(skill_files):
        if apply_workaround(skill_path, dry_run, no_symlink):
            applied += 1

    print(f"\n{'Would apply' if dry_run else 'Applied'} workaround to {applied} skills")


if __name__ == "__main__":
    main()
