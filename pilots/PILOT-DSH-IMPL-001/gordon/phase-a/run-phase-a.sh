#!/usr/bin/env bash
# Gordon Phase A orchestrator — Gates 0-5 qualification runs on hxs-15.
#
# Authored offline 2026-08-28. Executes only after the governor releases it.
# No secrets: the OmniRoute client key arrives via the environment variable
# named by GORDON_OMNI_KEY_ENV (default OMNIROUTE_CLIENT_KEY); this script
# checks presence only.
#
# Usage:
#   ./run-phase-a.sh [gate ...]        # default: all gates in order 0 1 2 3 4 5
#   GORDON_BOOTSTRAP_VENV=1 ./run-phase-a.sh   # allow pytest venv bootstrap
#
# Gate verdict lines follow Gordon's completion language:
#   [GATE VERDICT — <gate> — <verdict>]
set -u

SUITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRATCH="${GORDON_SCRATCH:-/var/lib/dsh/gordon}"
EVIDENCE="${GORDON_EVIDENCE_DIR:-$SCRATCH/evidence}"
VENV="$SCRATCH/venv"
KEY_ENV_NAME="${GORDON_OMNI_KEY_ENV:-OMNIROUTE_CLIENT_KEY}"

mkdir -p "$EVIDENCE"
PREFLIGHT="$EVIDENCE/preflight.txt"
: > "$PREFLIGHT"

say() { echo "$*" | tee -a "$PREFLIGHT"; }

say "gordon phase-a preflight $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "suite: $SUITE_DIR"
say "scratch: $SCRATCH"
say "evidence: $EVIDENCE"

# --- environment census (names only, never values) -------------------------
say "-- GORDON_* census (set/unset) --"
env | grep '^GORDON_' | cut -d= -f1 | sort | while read -r name; do
  say "  $name=SET"
done
if [ -z "$(env | grep '^GORDON_' || true)" ]; then
  say "  (no GORDON_* variables exported; suite defaults in gordon_util.py apply)"
fi

# --- tooling ----------------------------------------------------------------
PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  say "FATAL: python3 not found (test tooling prerequisite)"
  exit 2
fi
say "python3: $PY ($("$PY" --version 2>&1))"

PYTEST=()
if "$PY" -c 'import pytest' 2>/dev/null; then
  PYTEST=("$PY" -m pytest)
elif [ "${GORDON_BOOTSTRAP_VENV:-0}" = "1" ]; then
  say "pytest absent; bootstrapping venv at $VENV (owner ruling 2026-08-28 permits test tooling)"
  "$PY" -m venv "$VENV" >>"$PREFLIGHT" 2>&1 \
    && "$VENV/bin/pip" install --quiet pytest >>"$PREFLIGHT" 2>&1
  if "$VENV/bin/python" -c 'import pytest' 2>/dev/null; then
    PYTEST=("$VENV/bin/python" -m pytest)
  else
    say "FATAL: venv bootstrap failed (network/registry dependency); install pytest manually"
    exit 2
  fi
else
  say "FATAL: pytest not installed; re-run with GORDON_BOOTSTRAP_VENV=1 to allow venv bootstrap"
  exit 2
fi
say "pytest: ${PYTEST[*]}"

NODE="${GORDON_NODE:-/opt/node-v24.20.0/bin/node}"
if [ -x "$NODE" ]; then
  say "node: $NODE ($("$NODE" --version))"
else
  say "WARN: pinned node absent at $NODE (G0-03 will report)"
fi

# --- key presence (existence only) ------------------------------------------
if [ -n "${!KEY_ENV_NAME:-}" ]; then
  say "credential: $KEY_ENV_NAME present (value never read)"
else
  say "credential: $KEY_ENV_NAME ABSENT (routed rows will record BLOCKED)"
fi

# --- gates ------------------------------------------------------------------
declare -A GATE_FILES=(
  [0]=test_g0_identity.py
  [1]=test_g1_static.py
  [2]=test_g2_entry.py
  [3]=test_g3_providers.py
  [4]=test_g4_sessions.py
  [5]=test_g5_containment.py
)

gates=("$@")
if [ ${#gates[@]} -eq 0 ]; then
  gates=(0 1 2 3 4 5)
fi

overall=0
for gate in "${gates[@]}"; do
  file="${GATE_FILES[$gate]:-}"
  if [ -z "$file" ]; then
    say "unknown gate: $gate"
    overall=2
    continue
  fi
  say "== gate $gate: $file =="
  "${PYTEST[@]}" "$SUITE_DIR/$file" \
    --rootdir="$SUITE_DIR" \
    -p no:cacheprovider \
    --junitxml="$EVIDENCE/gate$gate-junit.xml" \
    -ra
  rc=$?
  case $rc in
    0) verdict="PASS" ;;
    5) verdict="BLOCKED (no tests ran to completion — all rows blocked/skipped)" ;;
    *) verdict="FAIL (pytest rc=$rc)" ; overall=1 ;;
  esac
  # A gate with any FAIL row is FAIL regardless of the pytest summary line.
  echo "[GATE VERDICT — Gate $gate — $verdict]"
done

say "evidence pack: $EVIDENCE"
exit $overall
