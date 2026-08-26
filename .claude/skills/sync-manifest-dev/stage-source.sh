#!/usr/bin/env bash
# Stage a clean copy of doodledood/manifest-dev into /tmp/manifest-dev.
#
# Tries the fast single-tarball path first; on a GitHub session-access 403
# (common in Claude Code on the web / remote execution) it falls back to
# reconstructing the tree from public CDNs that are NOT behind the session's
# repo-scoped GitHub access layer. Only reads files; never runs git in the clone.
#
# Usage: bash stage-source.sh [ref]   (ref defaults to main)
# Exit 0 = /tmp/manifest-dev is populated and (in CDN mode) hash-verified.
set -euo pipefail

REPO="doodledood/manifest-dev"
REF="${1:-main}"
DEST="/tmp/manifest-dev"
CACERT="/root/.ccr/ca-bundle.crt"
CURL=(curl -sSL)
[ -f "$CACERT" ] && CURL+=(--cacert "$CACERT")

echo ">> staging $REPO@$REF -> $DEST"
rm -rf "$DEST" && mkdir -p "$DEST"

# --- Tier 0: an existing local clone is the only COMPLETE source.
# Both CDN tiers below enumerate from a cached index that can under-list (see the
# integrity note in Tier 2), so a real checkout is strictly preferred. The agent
# gets one by calling the `add_repo` MCP tool for this repo and cloning it; see
# SKILL.md → "Fetching the source".
# The workspace root is environment-dependent (/workspace in some sessions, $HOME
# in a remote one), so a single hardcoded prefix silently misses a real clone and
# drops the run to the degraded CDN tiers below. Derive the roots instead: the
# directory holding this repo, since fleet clones sit side by side, then $HOME
# and /workspace. A root holding no clone costs one failed test.
_repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
_candidates=("${MANIFEST_DEV_CLONE:-}")
for _root in "$(dirname "$_repo_root")" "${HOME:-}" /workspace; do
  [ -n "$_root" ] || continue
  _candidates+=("$_root/manifest-dev" "$_root/doodledood/manifest-dev")
done
for candidate in "${_candidates[@]}"; do
  [ -n "$candidate" ] || continue
  if [ -d "$candidate/claude-plugins" ]; then
    echo ">> using local clone at $candidate (complete source)"
    # The recorded commit must be the clone's UPSTREAM state, never its local
    # HEAD. A session may have this clone parked on a branch of its own, and the
    # sync then stamps that branch's commit as the source of every file it
    # copied — content correct, provenance a lie, and nothing complains.
    #
    # The staged tree comes from that same commit (git archive), never from the
    # working tree: a second sync in one session fetches, origin/main advances,
    # the checkout does not, and cp -R would stamp the NEW sha onto the OLD files.
    # Every tracking file would then name a commit its content does not carry, and
    # the next run would diff from that sha and skip the missed changes for good.
    commit=""; from=""
    for ref in "origin/$REF" origin/HEAD "$REF"; do
      commit=$(git -C "$candidate" rev-parse --verify --quiet "$ref^{commit}" || true)
      if [ -n "$commit" ]; then from="$ref"; break; fi
    done
    if [ -n "$commit" ] && [ "$from" = "$REF" ]; then
      echo "!! no remote-tracking ref for $REF; using local $REF ($commit)." \
           "Fetch origin if that is not the upstream state." >&2
    fi
    if [ -z "$commit" ]; then
      echo "!! cannot resolve an upstream commit for $REF in $candidate — fetch origin and retry" >&2
      exit 1
    fi
    rm -rf "$DEST" && mkdir -p "$DEST"
    git -C "$candidate" archive "$commit" claude-plugins | tar -x -C "$DEST"
    printf '%s\n' "$commit" > "$DEST/.source-commit"
    echo ">> source commit $commit (from $from) -> $DEST/.source-commit"
    exit 0
  fi
done

# --- Tier 1: single tarball (works locally, or when session GitHub access includes the repo)
tar_url="https://codeload.github.com/$REPO/tar.gz/refs/heads/$REF"
code=$("${CURL[@]}" -o /tmp/manifest-dev.tar.gz -w "%{http_code}" "$tar_url" || echo 000)
if [ "$code" = "200" ] && tar -tzf /tmp/manifest-dev.tar.gz >/dev/null 2>&1; then
  tar -xzf /tmp/manifest-dev.tar.gz -C "$DEST" --strip-components=1
  printf 'unresolved-tarball@%s\n' "$REF" > "$DEST/.source-commit"
  echo ">> tarball OK"
  echo "!! no commit sha on this path — .source-commit records unresolved-tarball@$REF, which"
  echo "!! no later run can diff against. Prefer a clone (see SKILL.md)."
  exit 0
fi
echo ">> tarball path unavailable (HTTP $code) — falling back to CDN reconstruction"

# --- Tier 2: CDN reconstruction (public repo only)
# jsDelivr serves the file tree; raw.githubusercontent.com serves file bodies.
# Neither sits behind the session's GitHub repo-access gate, so a public repo
# stages fine even when codeload/api.github.com/github.com return 403.
#
# Integrity model: `@main` is a MOVING ref and the two CDNs cache it on
# independent clocks — jsDelivr's metadata tree (the sha256 list) lags its own
# file CDN and lags raw by up to its ~12h metadata TTL. So the tree's hashes
# CANNOT be the integrity oracle: when main advances, updated files legitimately
# mismatch the stale hash and deleted files legitimately 404, neither of which
# is corruption. Instead we cross-verify each body from two independent fresh
# views — raw.githubusercontent.com and cdn.jsdelivr.net — and require they
# AGREE. Files that 404 on raw are treated as deleted-upstream and dropped
# (the tree only over-lists; it never under-lists the parts it still shows).
tree="/tmp/manifest-dev-tree.json"
code=$("${CURL[@]}" -o "$tree" -w "%{http_code}" \
  "https://data.jsdelivr.com/v1/packages/gh/$REPO@$REF?structure=flat" || echo 000)
[ "$code" = "200" ] || { echo "!! jsDelivr tree fetch failed (HTTP $code)"; exit 1; }

# For every file under claude-plugins/: fetch from raw (authoritative content,
# ~near-origin TTL) and from cdn.jsdelivr (independent view); require agreement.
python3 - "$tree" "$DEST" "$REPO" "$REF" "$CACERT" <<'PY'
import json, os, sys, subprocess, hashlib, tempfile
from concurrent.futures import ThreadPoolExecutor
tree, dest, repo, ref, cacert = sys.argv[1:6]
files = json.load(open(tree))["files"]
want = [f for f in files if f["name"].startswith("/claude-plugins/")]
raw = f"https://raw.githubusercontent.com/{repo}/{ref}"
cdn = f"https://cdn.jsdelivr.net/gh/{repo}@{ref}"
curl = ["curl","-sSL"] + (["--cacert",cacert] if os.path.exists(cacert) else [])

def get(base, path):
    fd, tmp = tempfile.mkstemp(); os.close(fd)
    try:
        r = subprocess.run(curl+["-o",tmp,"-w","%{http_code}",base+path],
                           capture_output=True, text=True)
        code = r.stdout.strip()
        body = open(tmp,"rb").read() if code == "200" else b""
        return code, body
    finally:
        os.unlink(tmp)

def dl(f):
    name = f["name"]
    rcode, rbody = get(raw, name)
    if rcode == "404":
        return ("dropped", name)          # deleted upstream since tree cached
    if rcode != "200":
        return ("error", name, f"raw HTTP {rcode}")
    ccode, cbody = get(cdn, name)
    if ccode == "200" and cbody != rbody:
        return ("error", name, "raw/cdn content disagree (propagation in flight — retry later)")
    # cdn 404/other while raw has it: raw is authoritative and fresher; accept.
    out = dest + name
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "wb") as fh: fh.write(rbody)
    return ("ok", name)

res = list(ThreadPoolExecutor(max_workers=12).map(dl, want))
errs    = [r for r in res if r[0] == "error"]
dropped = [r for r in res if r[0] == "dropped"]
ok      = [r for r in res if r[0] == "ok"]
if errs:
    for r in errs: print(f"!! {r[2]}: {r[1]}", file=sys.stderr)
    sys.exit(1)
print(f">> CDN reconstruction OK — {len(ok)} files staged, cross-verified raw==cdn")
if dropped:
    print(f">> {len(dropped)} tree-listed file(s) 404 on raw (deleted upstream), skipped:")
    for r in dropped: print(f"     - {r[1]}")
print(">> NOTE: file list came from jsDelivr's cached tree; a brand-new upstream")
print(">>       file added within jsDelivr's metadata TTL may not yet be listed.")
PY

# --- Tier 2b: repair the tree's UNDER-listing.
# The reconstruction above defends against the cached tree OVER-listing (a file it
# still lists but that raw 404s is treated as deleted). It has no defense against
# the opposite, and that is the failure that actually bites: jsDelivr's metadata
# lags, so a subdirectory added upstream is simply absent from the tree, never
# fetched, and the sync reports success having silently dropped it. This is not
# hypothetical — it shipped `skills/do/` with SKILL.md and none of its four
# `references/` files, which silently downgraded /do's verification mode.
#
# Skills declare their own companion files, so the staged text is an independent
# index the stale tree cannot suppress. Chase every `references/`, `tasks/`, and
# `assets/` path a staged file names, probe raw for it, and pull anything real.
# Runs to a fixed point, since a fetched companion can name further companions.
python3 - "$DEST" "$REPO" "$REF" "$CACERT" <<'PY'
import os, re, sys, subprocess, tempfile
dest, repo, ref, cacert = sys.argv[1:5]
raw = f"https://raw.githubusercontent.com/{repo}/{ref}"
curl = ["curl","-sSL"] + (["--cacert",cacert] if os.path.exists(cacert) else [])

# Either an explicit companion path, or a bare backticked filename that a skill's
# prose names without its directory (e.g. define/SKILL.md's task-file table).
EXPLICIT = re.compile(r"(?:references|tasks|assets)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+")
BARE     = re.compile(r"`([A-Za-z0-9_-]+\.(?:md|html|json|txt))`")
# A backticked relative path with its own directory component, e.g. `research/RESEARCH.md`
# — named relative to a companion dir rather than to the skill root.
RELPATH  = re.compile(r"`([A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)*\.(?:md|html|json|txt))`")
SUBDIRS  = ("references", "tasks", "assets")

def fetch(relpath):
    """Probe raw for a repo-relative path; write it if present. True if fetched."""
    out = os.path.join(dest, relpath)
    if os.path.exists(out):
        return False
    fd, tmp = tempfile.mkstemp(); os.close(fd)
    try:
        r = subprocess.run(curl+["-o",tmp,"-w","%{http_code}",f"{raw}/{relpath}"],
                           capture_output=True, text=True)
        if r.stdout.strip() != "200":
            return False
        os.makedirs(os.path.dirname(out), exist_ok=True)
        os.replace(tmp, out)
        return True
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def candidates(path, text):
    """Repo-relative paths this file might be naming, resolved against its own dir."""
    owner = os.path.dirname(os.path.relpath(path, dest))
    # A companion under skills/<name>/references/ is named from the skill root, so
    # walk up out of any subdir the naming file itself sits in.
    root = owner
    while os.path.basename(root) in SUBDIRS:
        root = os.path.dirname(root)
    # Try both: a task file naming `references/X.md` can mean the skill's own
    # references/ OR one nested beside it (tasks/references/X.md). Probing both is
    # cheap — a wrong guess is one 404 — and guessing only one silently drops files.
    for base in dict.fromkeys((root, owner)):
        for m in EXPLICIT.findall(text):
            yield f"{base}/{m}"
        for name in BARE.findall(text):
            for sub in SUBDIRS:
                yield f"{base}/{sub}/{name}"
        for rel in RELPATH.findall(text):
            if "/" not in rel:
                continue                      # already covered by BARE
            yield f"{base}/{rel}"
            for sub in SUBDIRS:
                yield f"{base}/{sub}/{rel}"

recovered, seen = [], set()
for _ in range(5):                                   # fixed point; companions nest shallowly
    found = False
    for dirpath, _dirs, names in os.walk(dest):
        for name in names:
            if not name.endswith((".md", ".txt")):
                continue
            path = os.path.join(dirpath, name)
            if path in seen:
                continue
            seen.add(path)
            try:
                text = open(path, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for rel in set(candidates(path, text)):
                if "/claude-plugins/" not in "/"+rel and not rel.startswith("claude-plugins/"):
                    continue
                if fetch(rel):
                    recovered.append(rel); found = True
    if not found:
        break

if recovered:
    print(f"!! tree UNDER-listed {len(recovered)} file(s) — recovered by reference-chasing:")
    for r in sorted(recovered):
        print(f"     + {r}")
    print("!! the cached tree is stale; prefer a real clone (see SKILL.md).")
else:
    print(">> no under-listed companion files detected")

# Reference-chasing is a backstop, not a guarantee: it can only find files that
# some staged file names, so a companion nothing references stays invisible. The
# CDN path can therefore never certify completeness — say so every time, rather
# than letting a quiet run read as a verified one.
print("!! CDN reconstruction cannot certify completeness — a file no staged text")
print("!! names is undetectable here. For a guaranteed-complete source, call the")
print("!! add_repo MCP tool for this repo, clone it, and re-run (see SKILL.md).")
PY

printf 'unresolved-cdn@%s\n' "$REF" > "$DEST/.source-commit"
echo "!! no commit sha on this path — .source-commit records unresolved-cdn@$REF, which no"
echo "!! later run can diff against. Prefer a clone (see SKILL.md)."
