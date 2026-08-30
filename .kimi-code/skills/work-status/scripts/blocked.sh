#!/usr/bin/env bash
# blocked.sh — blocked goals with reasons
# THIN WRAPPER. All goal-state parsing lives in scripts/work_state.py (O1); this
# script must never reimplement it. Before consolidation, work-status and
# goal-decompose each grepped goal prose with their own regex and both were
# wrong: a COMPLETE goal recorded in an append-only correction block parsed as
# <none>, and a goal completed in its pilot state log still read "in-progress".
set -u
# Locate the engine. These wrappers are copied VERBATIM into every mirror
# (KDD-0020 requires byte-identical mirrors), and one runtime mirror lives
# OUTSIDE the repo at ~/.kimi-code/skills/, where "four levels up" resolves to
# $HOME and the engine is not found. Resolution order: explicit override, then
# an upward search from this script and from $PWD, and only a clear error if
# neither finds it — a status tool must fail loudly, never report nothing.
_hx_root() {
  if [ -n "${HX_REPO_ROOT:-}" ] && [ -f "$HX_REPO_ROOT/scripts/work_state.py" ]; then
    printf '%s' "$HX_REPO_ROOT"; return 0
  fi
  local d
  for d in "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" "$PWD"; do
    while [ "$d" != "/" ]; do
      if [ -f "$d/scripts/work_state.py" ]; then printf '%s' "$d"; return 0; fi
      d="$(dirname "$d")"
    done
  done
  return 1
}
if ! ROOT="$(_hx_root)"; then
  echo "work-status: cannot locate scripts/work_state.py — run from inside the HX repo, or set HX_REPO_ROOT" >&2
  exit 2
fi
exec python3 "$ROOT/scripts/work_state.py" blocked "$@"
