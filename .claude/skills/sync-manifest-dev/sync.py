#!/usr/bin/env python3
"""Sync staged manifest-dev plugins into one repo's .claude/ tree.

    python3 sync.py <repo-root> <staged-source> <source-commit> [--check]

<staged-source> is the directory stage-source.sh leaves behind, i.e.
/tmp/manifest-dev/claude-plugins. --check reports without writing.

Prints a human summary and writes the machine-readable report to
/tmp/manifest-dev-sync-report-<repo>.json, which feeds the PR body. It lives
outside the repo on purpose: a report file inside .claude/ is one `git add -A`
away from being committed.

Exits non-zero if post-copy verification finds any synced item differing from
source, so a caller can fail loudly instead of committing a partial sync.
"""
import filecmp, json, os, shutil, sys
from datetime import datetime, timezone

COMPONENTS = ("agents", "hooks", "skills")
PLUGINS = ("manifest-dev", "manifest-dev-tools")  # later wins a name collision
EXCLUDE = {".claude-plugin", "README.md"}
SELF_SKILL = "sync-manifest-dev"


def combined_source(src_root, comp):
    """name -> source path. manifest-dev-tools wins collisions."""
    out = {}
    for plugin in PLUGINS:
        d = os.path.join(src_root, plugin, comp)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name not in EXCLUDE:
                out[name] = os.path.join(d, name)
    return out


def repo_layout(repo):
    """"inverted" if this repo keeps real skill content in .agents/skills/.

    One skill already stored that way settles it for the whole repo, which is
    what lets a NEW skill land on the same side as its neighbours instead of
    leaving the repo half inverted.
    """
    mirror_dir = os.path.join(repo, ".agents", "skills")
    if not os.path.isdir(mirror_dir):
        return "plain"
    for name in sorted(os.listdir(mirror_dir)):
        entry = os.path.join(mirror_dir, name)
        link = os.path.join(repo, ".claude", "skills", name)
        if (os.path.isdir(entry) and not os.path.islink(entry)
                and os.path.islink(link)
                and os.path.realpath(link) == os.path.realpath(entry)):
            return "inverted"
    return "plain"


def wrong_side(repo, comp, name, layout):
    """True when an inverted repo holds this skill the plain way round.

    A previous run created it before the layout was taken into account. Left
    alone it stays a real .claude/ directory with a .agents/ symlink onto it —
    it resolves fine, so nothing ever fails, and the repo quietly accumulates
    skills its own convention does not match.
    """
    if layout != "inverted" or comp != "skills":
        return False
    real = os.path.join(repo, ".claude", "skills", name)
    link = os.path.join(repo, ".agents", "skills", name)
    return (os.path.isdir(real) and not os.path.islink(real)
            and os.path.islink(link)
            and os.path.realpath(link) == os.path.realpath(real))


def flip_to_inverted(repo, name):
    """Move real content to .agents/skills/<name>, leave .claude/ a symlink."""
    real = os.path.join(repo, ".claude", "skills", name)
    link = os.path.join(repo, ".agents", "skills", name)
    os.remove(link)
    shutil.move(real, link)
    os.symlink(os.path.join("../..", ".agents", "skills", name), real)


def classify(repo, comp, name, layout="plain"):
    """Where a component lands, and whether we are allowed to write there.

    direct  - ordinary path under .claude/, write it
    mirror  - inverted layout: .claude/ side is a symlink onto real content in
              this repo's own .agents/skills/, so write through to that content
    adopt   - a skill absent from an inverted repo. The real content belongs in
              .agents/skills/, with a .claude/ symlink onto it, so it matches
              the skills already there.
    foreign - a symlink pointing anywhere else (another plugin's source).
              Never write, never delete, never track.
    """
    target = os.path.join(repo, ".claude", comp, name)
    if layout == "inverted" and comp == "skills" and not os.path.lexists(target):
        return "adopt", os.path.join(repo, ".agents", "skills", name)
    if not os.path.islink(target):
        return "direct", target
    real = os.path.realpath(target)
    mirror_dir = os.path.join(repo, ".agents", "skills")
    entry = os.path.join(mirror_dir, name)
    # The .agents entry must be REAL content, not a symlink. A .agents symlink
    # is the ordinary mirror pointing back at .claude/, so both sides resolve to
    # whatever foreign path .claude/ names and resolved-equality proves nothing.
    if (comp == "skills"
            and os.path.isdir(entry) and not os.path.islink(entry)
            and os.path.dirname(real) == os.path.realpath(mirror_dir)):
        return "mirror", real
    return "foreign", real


def replace(src, dst):
    if os.path.islink(dst) or os.path.isfile(dst):
        os.remove(dst)
    elif os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst, symlinks=True)
    else:
        shutil.copy2(src, dst)


def identical(a, b):
    if not os.path.exists(b):
        return False
    if os.path.isfile(a):
        return filecmp.cmp(a, b, shallow=False)
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    if mismatch or errors:
        return False
    return all(identical(os.path.join(a, d), os.path.join(b, d))
               for d in cmp.common_dirs)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check_only = "--check" in sys.argv
    repo, src_root, source_commit = args[0], args[1], args[2]

    track_path = os.path.join(repo, ".claude", ".manifest-dev-sync.json")
    tracked = {c: [] for c in COMPONENTS}
    if os.path.exists(track_path):
        prev = json.load(open(track_path))
        for c in COMPONENTS:
            tracked[c] = list(prev.get(c, []))

    layout = repo_layout(repo)
    report, failures, flipped = {}, [], []
    for comp in COMPONENTS:
        src = combined_source(src_root, comp)
        added, updated, unchanged, removed, skipped, refused = [], [], [], [], [], []

        for name, spath in sorted(src.items()):
            if wrong_side(repo, comp, name, layout):
                flipped.append(name)
                if not check_only:
                    flip_to_inverted(repo, name)
            kind, target = classify(repo, comp, name, layout)
            if kind == "foreign":
                skipped.append({"name": name,
                                "reason": "symlink -> " + os.path.relpath(target, repo)})
                continue
            if identical(spath, target):
                unchanged.append(name)
                continue
            existed = os.path.exists(target)
            if not check_only:
                replace(spath, target)
                if kind == "adopt":
                    os.symlink(os.path.join("../..", ".agents", "skills", name),
                               os.path.join(repo, ".claude", "skills", name))
            (updated if existed else added).append(name)

        for name in tracked[comp]:
            if name in src:
                continue
            if comp == "skills" and name == SELF_SKILL:
                refused.append({"name": name, "reason": "self"})
                continue
            kind, target = classify(repo, comp, name, layout)
            if kind == "foreign":
                refused.append({"name": name,
                                "reason": "symlink -> " + os.path.relpath(target, repo)})
                continue
            if not os.path.exists(target):
                continue
            if not check_only:
                shutil.rmtree(target) if os.path.isdir(target) else os.remove(target)
                # Inverted layout: the content just deleted was the .agents/ side,
                # so the .claude/ symlink onto it would be left dangling.
                if kind == "mirror":
                    os.remove(os.path.join(repo, ".claude", comp, name))
            removed.append(name)

        # Track only what this sync actually owns here. An item skipped because
        # its target belongs to another plugin was never written by us, so
        # recording it would make a later run eligible to delete it.
        skipped_names = {s["name"] for s in skipped}
        report[comp] = {"tracked": sorted(set(src) - skipped_names),
                        "added": added, "updated": updated, "unchanged": unchanged,
                        "removed": removed, "skipped": skipped, "refused": refused}

        if not check_only:
            for name in sorted(set(src) - skipped_names):
                _, target = classify(repo, comp, name, layout)
                if not identical(src[name], target):
                    failures.append(f"{comp}/{name}")

    # --- .agents/skills mirror ---------------------------------------------
    mirror = {"created": [], "skipped": [], "removed": [], "inverted": [],
              "flipped": flipped}
    mirror_dir = os.path.join(repo, ".agents", "skills")
    if os.path.isdir(os.path.join(repo, ".agents")):
        if not check_only:
            os.makedirs(mirror_dir, exist_ok=True)
        for name in report["skills"]["tracked"]:
            link = os.path.join(mirror_dir, name)
            kind, _ = classify(repo, "skills", name, layout)
            if kind == "mirror":
                mirror["inverted"].append(name)   # real content already lives here
                continue
            if os.path.islink(link):
                continue
            if os.path.exists(link):
                mirror["skipped"].append(name)    # project-local, don't clobber
                continue
            if not check_only:
                os.symlink(os.path.join("../..", ".claude", "skills", name), link)
            mirror["created"].append(name)
        for name in tracked["skills"]:
            if name in report["skills"]["tracked"]:
                continue
            link = os.path.join(mirror_dir, name)
            if os.path.islink(link):
                if not check_only:
                    os.remove(link)
                mirror["removed"].append(name)

    # --- tracking file ------------------------------------------------------
    out = {"version": 1,
           "last_synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "agents": report["agents"]["tracked"],
           "hooks": report["hooks"]["tracked"],
           "skills": report["skills"]["tracked"],
           "source_commit": source_commit}
    if not check_only:
        os.makedirs(os.path.dirname(track_path), exist_ok=True)
        with open(track_path, "w") as fh:
            json.dump(out, fh, indent=2)
            fh.write("\n")
        slug = os.path.basename(os.path.abspath(repo))
        report_path = f"/tmp/manifest-dev-sync-report-{slug}.json"
        with open(report_path, "w") as fh:
            json.dump({"repo": repo, "source_commit": source_commit,
                       "layout": layout, "components": report, "mirror": mirror,
                       "verification_failures": failures}, fh, indent=2)

    # --- summary ------------------------------------------------------------
    name = os.path.basename(os.path.abspath(repo))
    print(f"\n=== {name} [{layout}]{' (check only)' if check_only else ''} ===")
    print(f"{'component':<9}{'added':>7}{'updated':>9}{'same':>6}"
          f"{'removed':>9}{'skipped':>9}{'refused':>9}")
    for comp in COMPONENTS:
        r = report[comp]
        print(f"{comp:<9}{len(r['added']):>7}{len(r['updated']):>9}"
              f"{len(r['unchanged']):>6}{len(r['removed']):>9}"
              f"{len(r['skipped']):>9}{len(r['refused']):>9}")
    for comp in COMPONENTS:
        for key in ("added", "removed"):
            for item in report[comp][key]:
                print(f"  {comp} {key}: {item}")
        for key in ("skipped", "refused"):
            for item in report[comp][key]:
                print(f"  {comp} {key}: {item['name']} ({item['reason']})")
    for key, vals in mirror.items():
        if vals:
            print(f"  mirror {key}: {', '.join(vals)}")
    print(f"  tracked: agents={len(out['agents'])} hooks={len(out['hooks'])} "
          f"skills={len(out['skills'])}")
    if not check_only:
        print(f"  report: {report_path}")

    if failures:
        print("\n!! VERIFICATION FAILED — these differ from source after copy:")
        for f in failures:
            print(f"     {f}")
        return 1
    if not check_only:
        print("  verified: every synced item matches the source tree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
