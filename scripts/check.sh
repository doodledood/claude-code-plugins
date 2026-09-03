#!/usr/bin/env bash
#
# The one command to run before opening a pull request. CI runs this same script, so a green run
# here is the same evidence CI produces.
#
#   ./scripts/check.sh                 check everything, change nothing
#   ./scripts/check.sh --fix           apply the lint and format fixes first, then check the rest
#   ./scripts/check.sh --base <ref>    compare the version gate against <ref> (CI passes the
#                                      pull request's base commit; the default is origin/main)
#
# Tool versions come from the `dev` dependency group in pyproject.toml. Nothing here installs a
# tool at a floating version, and nothing here is skipped when a tool is absent.

set -euo pipefail

cd "$(dirname "$0")/.."

FIX=0
BASE_ARGS=()
while [ $# -gt 0 ]; do
    case "$1" in
        --fix) FIX=1; shift ;;
        --base) BASE_ARGS=(--base "${2:?--base needs a git ref}"); shift 2 ;;
        -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "error: unknown argument '$1'" >&2; exit 2 ;;
    esac
done

if ! command -v uv >/dev/null 2>&1; then
    cat >&2 <<'MSG'
error: uv is not installed, and it is how this repository provisions its checks.

  macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
  Homebrew:    brew install uv

See https://docs.astral.sh/uv/ for other platforms.
MSG
    exit 2
fi

echo "==> uv sync --group dev"
uv sync --group dev --quiet
PY=.venv/bin/python
RUFF=.venv/bin/ruff
MYPY=.venv/bin/mypy

FAILED=()

step() {
    local name="$1"
    shift
    echo
    echo "==> ${name}"
    if "$@"; then
        return 0
    fi
    FAILED+=("${name}")
    return 0
}

if [ "${FIX}" -eq 1 ]; then
    step "ruff check --fix" "${RUFF}" check --fix .
    step "ruff format" "${RUFF}" format .
else
    step "ruff check" "${RUFF}" check .
    step "ruff format --check" "${RUFF}" format --check .
fi

step "mypy" "${MYPY}"
step "unit tests" "${PY}" -m unittest discover --start-directory tests --top-level-directory . --verbose
# The ${a[@]+"${a[@]}"} form expands an empty array to nothing under `set -u`, which bash 3.2 —
# the version macOS ships — otherwise treats as an unbound variable.
step "plugin versions" "${PY}" scripts/check_plugin_versions.py ${BASE_ARGS[@]+"${BASE_ARGS[@]}"}

echo
if [ ${#FAILED[@]} -eq 0 ]; then
    echo "All checks passed."
    exit 0
fi

echo "FAILED: ${FAILED[*]}" >&2
exit 1
