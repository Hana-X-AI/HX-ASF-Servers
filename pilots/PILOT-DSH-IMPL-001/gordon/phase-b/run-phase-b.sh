#!/usr/bin/env bash
# Gordon Phase B orchestrator — Gates 6-7 qualification runs on hxs-15.
# Authored offline 2026-08-28 (pipelined with Morpheus's Phase B activation).
# Executes only after the governor releases it, with a fresh §8.3 freeze
# (the Phase B activation changes the composition and the frontend dist).
# No secrets: the credential resolves per Phase A mechanics.
set -u

SUITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRATCH="${GORDON_SCRATCH:-/home/hxsa/gordon/scratch}"
EVIDENCE="${GORDON_EVIDENCE_DIR:-/home/hxsa/gordon/evidence}"
KEY_ENV_NAME="${GORDON_OMNI_KEY_ENV:-OMNIROUTE_API_KEY}"

mkdir -p "$EVIDENCE"
PREFLIGHT="$EVIDENCE/preflight-b.txt"
: > "$PREFLIGHT"
say() { echo "$*" | tee -a "$PREFLIGHT"; }

say "gordon phase-b preflight $(date -u +%Y-%m-%dT%H:%M:%SZ)"
PY="$(command -v python3 || true)"
[ -z "$PY" ] && { say "FATAL: python3 missing"; exit 2; }
"$PY" -c 'import pytest' 2>/dev/null || { say "FATAL: pytest missing (Phase A tooling)"; exit 2; }
if [ -n "${!KEY_ENV_NAME:-}" ] || sudo -n -u dsh test -r /var/lib/dsh/.env 2>/dev/null; then
  say "credential: resolvable (name only)"
else
  say "credential: ABSENT (routed rows BLOCKED)"
fi
DIST="${GORDON_DSH_ROOT:-/opt/dsh}/apps/web/dist"
if [ -d "$DIST" ] && [ -n "$(ls -A "$DIST" 2>/dev/null)" ]; then
  say "frontend dist: present"
else
  say "frontend dist: ABSENT (G7 web rows FAIL or BLOCK per plan)"
fi

declare -A GATE_FILES=( [6]=test_g6_orchestration.py [7]=test_g7_surfaces.py )
gates=("$@"); [ ${#gates[@]} -eq 0 ] && gates=(6 7)
overall=0
for gate in "${gates[@]}"; do
  file="${GATE_FILES[$gate]:-}"
  [ -z "$file" ] && { say "unknown gate: $gate"; overall=2; continue; }
  say "== gate $gate: $file =="
  "$PY" -m pytest "$SUITE_DIR/$file" --rootdir="$SUITE_DIR" -p no:cacheprovider \
    --junitxml="$EVIDENCE/gate${gate}-junit.xml" -ra
  rc=$?
  case $rc in
    0) verdict="PASS" ;;
    5) verdict="BLOCKED (no tests ran to completion)" ;;
    *) verdict="FAIL (pytest rc=$rc)"; overall=1 ;;
  esac
  echo "[GATE VERDICT — Gate $gate — $verdict]"
done
say "evidence: $EVIDENCE"
exit $overall
