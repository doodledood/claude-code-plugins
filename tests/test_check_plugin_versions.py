"""Tests for the version-bump gate's decision function.

The gate's failure mode is silence: passing a change it should have failed. These exercise
:func:`evaluate` directly, over constructed inputs, so every branch is reachable without building
repositories.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from check_plugin_versions import ManifestError, evaluate, parse_manifest

CHANGELOG = """# Changelog

## [Unreleased]

- [consultant] v1.9.3 - Something changed
- [plugin-template] v1.3.0 - Template gained a section

## 2026-01-17

- [writing] v1.0.0 - New plugin: consolidated writing toolkit
"""


def manifest(name: str, version: str) -> str:
    return f'{{"name": "{name}", "version": "{version}"}}'


class NoPluginFilesChanged(unittest.TestCase):
    def test_change_outside_claude_plugins_is_ignored(self) -> None:
        changed = ["CLAUDE.md", "scripts/check.sh", ".claude/skills/foo/SKILL.md"]
        self.assertEqual(evaluate(changed, {}, {}, CHANGELOG), [])

    def test_the_plugins_index_readme_is_not_inside_a_plugin(self) -> None:
        self.assertEqual(evaluate(["claude-plugins/README.md"], {}, {}, CHANGELOG), [])


class BumpRequired(unittest.TestCase):
    def test_edited_plugin_without_a_bump_fails(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9.2")},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("consultant", violations[0])
        self.assertIn("version bump", violations[0])
        self.assertIn("v1.9.2", violations[0])

    def test_bumped_and_logged_passes(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9.3")},
            CHANGELOG,
        )
        self.assertEqual(violations, [])

    def test_bumped_without_a_changelog_line_fails(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9.9")},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("CHANGELOG.md", violations[0])
        self.assertNotIn("version bump", violations[0])

    def test_a_lowered_version_is_not_a_bump(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "2.0.0")},
            {"consultant": manifest("consultant", "1.9.3")},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("below the merge base's v2.0.0", violations[0])

    def test_the_changelog_line_must_match_the_new_version_exactly(self) -> None:
        """A prefix match would let v1.9.3's entry satisfy a bump to v1.9.30."""
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9.30")},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("v1.9.30", violations[0])

    def test_the_plugin_name_comes_from_the_manifest_not_the_directory(self) -> None:
        """claude-plugins/PLUGIN_TEMPLATE/ declares the name plugin-template."""
        violations = evaluate(
            ["claude-plugins/PLUGIN_TEMPLATE/skills/example/SKILL.md"],
            {"PLUGIN_TEMPLATE": manifest("plugin-template", "1.2.0")},
            {"PLUGIN_TEMPLATE": manifest("plugin-template", "1.3.0")},
            CHANGELOG,
        )
        self.assertEqual(violations, [])


class ReadmeExemption(unittest.TestCase):
    def test_readme_only_change_needs_no_bump(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/README.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9.2")},
            CHANGELOG,
        )
        self.assertEqual(violations, [])

    def test_a_nested_readme_is_still_a_readme(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/README.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9.2")},
            CHANGELOG,
        )
        self.assertEqual(violations, [])

    def test_a_readme_beside_a_real_change_does_not_exempt_the_plugin(self) -> None:
        violations = evaluate(
            [
                "claude-plugins/consultant/README.md",
                "claude-plugins/consultant/skills/consultant/SKILL.md",
            ],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9.2")},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("version bump", violations[0])


class PluginLifecycle(unittest.TestCase):
    def test_a_new_plugin_needs_a_changelog_line(self) -> None:
        violations = evaluate(
            ["claude-plugins/newthing/skills/x/SKILL.md"],
            {"newthing": None},
            {"newthing": manifest("newthing", "1.0.0")},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("new plugin at v1.0.0", violations[0])

    def test_a_new_plugin_with_a_changelog_line_passes(self) -> None:
        violations = evaluate(
            ["claude-plugins/writing/skills/x/SKILL.md"],
            {"writing": None},
            {"writing": manifest("writing", "1.0.0")},
            CHANGELOG,
        )
        self.assertEqual(violations, [])

    def test_a_removed_plugin_has_no_version_left_to_bump(self) -> None:
        violations = evaluate(
            ["claude-plugins/gone/skills/x/SKILL.md"],
            {"gone": manifest("gone", "1.0.0")},
            {"gone": None},
            CHANGELOG,
        )
        self.assertEqual(violations, [])

    def test_a_directory_that_is_not_a_plugin_is_reported(self) -> None:
        violations = evaluate(
            ["claude-plugins/scratch/notes.md"],
            {"scratch": None},
            {"scratch": None},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("no .claude-plugin/plugin.json", violations[0])


class FailsLoudOnUnreadableManifests(unittest.TestCase):
    def test_a_missing_version_is_a_violation_not_a_pass(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": '{"name": "consultant"}'},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn('missing a string "version"', violations[0])

    def test_a_non_semver_version_is_a_violation_not_a_pass(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": manifest("consultant", "1.9")},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("not three dot-separated integers", violations[0])

    def test_broken_json_is_a_violation_not_a_pass(self) -> None:
        violations = evaluate(
            ["claude-plugins/consultant/skills/consultant/SKILL.md"],
            {"consultant": manifest("consultant", "1.9.2")},
            {"consultant": "{not json"},
            CHANGELOG,
        )
        self.assertEqual(len(violations), 1)
        self.assertIn("not valid JSON", violations[0])

    def test_parse_manifest_rejects_an_empty_name(self) -> None:
        with self.assertRaises(ManifestError):
            parse_manifest("consultant", "HEAD", manifest("", "1.0.0"))


class SeveralPluginsAtOnce(unittest.TestCase):
    def test_each_offending_plugin_is_named(self) -> None:
        violations = evaluate(
            [
                "claude-plugins/consultant/skills/a/SKILL.md",
                "claude-plugins/writing/skills/b/SKILL.md",
            ],
            {
                "consultant": manifest("consultant", "1.9.2"),
                "writing": manifest("writing", "1.3.0"),
            },
            {
                "consultant": manifest("consultant", "1.9.2"),
                "writing": manifest("writing", "1.3.0"),
            },
            CHANGELOG,
        )
        self.assertEqual(len(violations), 2)
        self.assertTrue(any("consultant" in v for v in violations))
        self.assertTrue(any("writing" in v for v in violations))


if __name__ == "__main__":
    unittest.main()
