#!/usr/bin/env python3
"""Enforce the Plugin Versioning rule from CLAUDE.md.

A change that edits any file under ``claude-plugins/<dir>/`` must raise that plugin's
``.claude-plugin/plugin.json`` version and add a ``CHANGELOG.md`` line naming the plugin and the
new version. Changes confined to ``README.md`` files are exempt.

The decision lives in :func:`evaluate`, a pure function over the change's contents, so it is
testable without building repositories. :func:`collect` is the only part that talks to git.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path, PurePosixPath

PLUGIN_ROOT = "claude-plugins"
MANIFEST_PATH = ".claude-plugin/plugin.json"
CHANGELOG_PATH = "CHANGELOG.md"
EXEMPT_BASENAME = "README.md"

#: Raised as a violation rather than an exception, so one run reports every problem it found.
Violations = list[str]


class ManifestError(Exception):
    """A ``plugin.json`` could not be read as a versioned plugin manifest."""


def parse_manifest(
    directory: str, revision: str, text: str
) -> tuple[str, tuple[int, int, int]]:
    """Return ``(name, version)`` from a ``plugin.json`` body, or raise :class:`ManifestError`.

    Every failure here is loud. A gate that cannot read a version must not conclude that the
    version is fine.
    """
    where = f"{PLUGIN_ROOT}/{directory}/{MANIFEST_PATH} at {revision}"
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{where}: not valid JSON ({exc})") from exc
    if not isinstance(data, dict):
        raise ManifestError(
            f"{where}: expected a JSON object, found {type(data).__name__}"
        )

    name = data.get("name")
    if not isinstance(name, str) or not name:
        raise ManifestError(f'{where}: missing a non-empty string "name"')

    raw_version = data.get("version")
    if not isinstance(raw_version, str):
        raise ManifestError(f'{where}: missing a string "version"')
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", raw_version)
    if match is None:
        raise ManifestError(
            f"{where}: version {raw_version!r} is not three dot-separated integers"
        )
    major, minor, patch = (int(part) for part in match.groups())
    return name, (major, minor, patch)


def format_version(version: tuple[int, int, int]) -> str:
    return ".".join(str(part) for part in version)


def changelog_mentions(
    changelog: str, name: str, version: tuple[int, int, int]
) -> bool:
    """Whether some line of the changelog names both this plugin and this exact version.

    Placement is not checked. Real history files entries under ``## [Unreleased]``, under a dated
    heading, and under an archive heading, so requiring one of those would fail on the
    repository's own practice. What every entry does share is ``[name]`` and ``vX.Y.Z`` on one
    line, and that is what is required.
    """
    pattern = re.compile(
        rf"\[{re.escape(name)}\].*\bv{re.escape(format_version(version))}(?![\d.])"
    )
    return any(pattern.search(line) for line in changelog.splitlines())


def plugin_directory_of(path: str) -> str | None:
    """The plugin directory a changed path belongs to, or None if it is not inside one.

    ``claude-plugins/README.md`` sits beside the plugins rather than inside one, so it yields None.
    """
    parts = PurePosixPath(path).parts
    if len(parts) < 3 or parts[0] != PLUGIN_ROOT:
        return None
    return parts[1]


def evaluate(
    changed_paths: Iterable[str],
    base_manifests: Mapping[str, str | None],
    head_manifests: Mapping[str, str | None],
    changelog: str,
) -> Violations:
    """Return one message per violation; an empty list means the change is compliant.

    ``base_manifests`` and ``head_manifests`` map a plugin directory name to the text of its
    ``plugin.json`` at that revision, or None where the file does not exist there.
    """
    by_directory: dict[str, list[str]] = {}
    for path in changed_paths:
        directory = plugin_directory_of(path)
        if directory is not None:
            by_directory.setdefault(directory, []).append(path)

    violations: Violations = []
    for directory in sorted(by_directory):
        paths = by_directory[directory]
        if all(PurePosixPath(path).name == EXEMPT_BASENAME for path in paths):
            continue

        head_text = head_manifests.get(directory)
        base_text = base_manifests.get(directory)

        if head_text is None:
            if base_text is not None:
                # The plugin was removed. There is no version left to bump.
                continue
            violations.append(
                f"{PLUGIN_ROOT}/{directory}/: changed, but has no {MANIFEST_PATH} at either "
                f"revision, so it cannot be versioned. Every directory under {PLUGIN_ROOT}/ is a "
                f"plugin and needs one."
            )
            continue

        try:
            name, head_version = parse_manifest(directory, "HEAD", head_text)
        except ManifestError as exc:
            violations.append(str(exc))
            continue

        if base_text is None:
            missing = _missing_changelog(changelog, name, head_version)
            if missing:
                violations.append(
                    f"{name}: new plugin at v{format_version(head_version)} needs {missing}"
                )
            continue

        try:
            _, base_version = parse_manifest(directory, "the merge base", base_text)
        except ManifestError as exc:
            violations.append(str(exc))
            continue

        problems: list[str] = []
        if head_version <= base_version:
            problems.append(
                f"a version bump ({MANIFEST_PATH} is still v{format_version(head_version)}"
                + (
                    ")"
                    if head_version == base_version
                    else f", below the merge base's v{format_version(base_version)})"
                )
            )
        missing = _missing_changelog(changelog, name, head_version)
        if missing:
            problems.append(missing)
        if problems:
            edited = ", ".join(sorted(paths)[:3]) + (
                " and others" if len(paths) > 3 else ""
            )
            violations.append(
                f"{name}: edited {edited} but is missing " + " and ".join(problems)
            )

    return violations


def _missing_changelog(
    changelog: str, name: str, version: tuple[int, int, int]
) -> str | None:
    if changelog_mentions(changelog, name, version):
        return None
    return (
        f"a {CHANGELOG_PATH} line naming [{name}] and v{format_version(version)} "
        f"(any heading; one line carrying both)"
    )


def _git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(
            f"error: `git {' '.join(args)}` failed: {result.stderr.strip()}"
        )
    return result.stdout


def _git_show(revision: str, path: str) -> str | None:
    """File contents at a revision, or None when the path does not exist there."""
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout
    if "does not exist" in result.stderr or "exists on disk" in result.stderr:
        return None
    raise SystemExit(
        f"error: reading {path} at {revision} failed: {result.stderr.strip()}"
    )


def resolve_base(explicit: str | None) -> str:
    """The revision to compare against. Never guesses silently."""
    if explicit:
        _git("rev-parse", "--verify", f"{explicit}^{{commit}}")
        return explicit
    candidate = "origin/main"
    probe = subprocess.run(
        ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        raise SystemExit(
            f"error: no --base given and {candidate} is not present. Pass --base <ref> "
            f"(CI passes the pull request's base commit) or fetch {candidate}."
        )
    return candidate


def _working_tree(path: str) -> str | None:
    """File contents as they stand on disk, or None when the file is not there."""
    candidate = Path(_git("rev-parse", "--show-toplevel").strip()) / path
    if not candidate.is_file():
        return None
    return candidate.read_text(encoding="utf-8")


def collect(
    base: str,
) -> tuple[list[str], dict[str, str | None], dict[str, str | None], str]:
    """Gather the inputs :func:`evaluate` decides on, from git.

    The comparison runs merge base against the *working tree*, not against HEAD. In CI the two are
    the same, because the checkout is clean. Locally they are not, and a contributor who runs the
    gate before committing has to see the change they are about to commit — a gate that reports
    "nothing changed" over a dirty tree teaches people to ignore it.
    """
    merge_base = _git("merge-base", base, "HEAD").strip()
    tracked = _git("diff", "--name-only", "--no-renames", merge_base)
    untracked = _git("ls-files", "--others", "--exclude-standard")
    changed = sorted({line for line in (tracked + untracked).splitlines() if line})

    directories = {
        directory
        for directory in (plugin_directory_of(path) for path in changed)
        if directory is not None
    }
    base_manifests = {
        directory: _git_show(merge_base, f"{PLUGIN_ROOT}/{directory}/{MANIFEST_PATH}")
        for directory in directories
    }
    head_manifests = {
        directory: _working_tree(f"{PLUGIN_ROOT}/{directory}/{MANIFEST_PATH}")
        for directory in directories
    }
    changelog = _working_tree(CHANGELOG_PATH) or ""
    return changed, base_manifests, head_manifests, changelog


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--base",
        help="Revision to compare against. Defaults to origin/main; CI passes the pull "
        "request's base commit.",
    )
    args = parser.parse_args(argv)

    base = resolve_base(args.base)
    changed, base_manifests, head_manifests, changelog = collect(base)
    violations = evaluate(changed, base_manifests, head_manifests, changelog)

    touched = sorted(
        {d for d in (plugin_directory_of(p) for p in changed) if d is not None}
    )
    if not touched:
        print(
            f"plugin versions: no file under {PLUGIN_ROOT}/<plugin>/ changed against {base}"
        )
        return 0

    if violations:
        print(f"plugin versions: FAIL against {base}", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        print(
            "\nCLAUDE.md, Plugin Versioning: editing a plugin's files requires a version bump in "
            f"{MANIFEST_PATH} and a matching {CHANGELOG_PATH} entry. README-only changes are "
            "exempt.",
            file=sys.stderr,
        )
        return 1

    print(f"plugin versions: OK — {', '.join(touched)} changed and accounted for")
    return 0


if __name__ == "__main__":
    sys.exit(main())
