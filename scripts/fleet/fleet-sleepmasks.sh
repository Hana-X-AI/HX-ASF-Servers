#!/usr/bin/env bash
# fleet-sleepmasks.sh — the proven LLM-host 4-target sleep-mask set
# (fleet library v0.1; set proven on hxs-1 2026-08-25, hxs-3 2026-08-26,
# hxs-2 + hxs-4 aligned 2026-08-26/27).
#
# Set: suspend.target hibernate.target hybrid-sleep.target
#      suspend-then-hibernate.target  (sleep.target is deliberately NOT in
#      the set — it is a passive dependency node; hxs-2 carries an extra
#      sleep.target mask as a documented harmless superset.)
#
# MUTATION CLASS: `verify` (DEFAULT) is READ-ONLY. `apply` is MUTATING
# (creates /dev/null mask symlinks) — run it ONLY under an explicit work
# order for the named host.
#
# CREDENTIAL BOUNDARY: this script NEVER handles credentials. SSH transport is
# the caller's via FLEET_SSH (single executable path; default: ssh). `apply`
# uses remote `sudo -S`: feed sudo through this script's stdin or have
# passwordless sudo remotely.
set -uo pipefail

SCRIPT_NAME="fleet-sleepmasks.sh"
TARGETS="suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target"

usage() {
  cat <<'EOF'
Usage: fleet-sleepmasks.sh <host> [verify|apply]

Manages the proven LLM-host sleep-mask set on <host>:
  suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target

Modes:
  verify   (DEFAULT) read-only: report is-enabled per target, mask symlinks,
           and an ALIGNED/DIVERGED verdict against the proven set.
  apply    mask the four targets (sudo systemctl mask ...) with before/after
           evidence. Requires an explicit work order for <host>.

Rollback (exact inverse): sudo systemctl unmask suspend.target hibernate.target
hybrid-sleep.target suspend-then-hibernate.target

Environment:
  FLEET_SSH   SSH executable/wrapper for transport (default: ssh).

Exit status: verify — 0 when ALIGNED, 1 when DIVERGED or on error;
             apply — 0 when post-apply verification is ALIGNED, 1 otherwise.
EOF
}

action="verify"
host=""
while [ $# -gt 0 ]; do
  case "$1" in
    verify|apply) action="$1" ;;
    -h|--help) usage; exit 0 ;;
    -*) printf '%s: unknown option %s\n' "$SCRIPT_NAME" "$1" >&2; usage >&2; exit 1 ;;
    *) if [ -z "$host" ]; then host="$1"; else printf '%s: unexpected extra argument %s\n' "$SCRIPT_NAME" "$1" >&2; exit 1; fi ;;
  esac
  shift
done
[ -z "$host" ] && { usage >&2; exit 1; }

FLEET_SSH="${FLEET_SSH:-ssh}"

# Remote read-only state report (literal target list; $ expands remotely).
STATE_REMOTE="$(cat <<'EOS'
for t in suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target; do
  st=$(systemctl is-enabled "$t" 2>/dev/null)
  printf "%s=%s\n" "$t" "${st:-unknown}"
done
ls -l /etc/systemd/system/suspend.target /etc/systemd/system/hibernate.target /etc/systemd/system/hybrid-sleep.target /etc/systemd/system/suspend-then-hibernate.target 2>/dev/null | awk '{printf "symlink %s -> %s\n", $9, $11}'
EOS
)"

report_state() {
  # report_state <label> — prints per-target state + verdict; returns 0 ALIGNED, 1 DIVERGED
  local label="$1"
  local out t st aligned
  out="$("$FLEET_SSH" "$host" "$STATE_REMOTE" </dev/null 2>&1)"
  printf '%s\n' "$out" | sed "s/^/  [$label] /"
  aligned=0
  for t in $TARGETS; do
    st="$(printf '%s\n' "$out" | sed -n "s/^$t=//p")"
    [ "$st" = "masked" ] || aligned=1
  done
  if [ $aligned -eq 0 ]; then
    printf '  [%s] verdict: ALIGNED with the proven 4-target set\n' "$label"
  else
    printf '  [%s] verdict: DIVERGED from the proven 4-target set\n' "$label"
  fi
  return $aligned
}

if [ "$action" = "verify" ]; then
  printf '%s: verify %s (proven set: suspend hibernate hybrid-sleep suspend-then-hibernate)\n' "$SCRIPT_NAME" "$host"
  report_state "current"
  exit $?
fi

# ---- apply (work-order gated, stdin passthrough to remote sudo -S) ----
printf '%s: apply %s at %s (UTC)\n' "$SCRIPT_NAME" "$host" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
report_state "before" || true
apply_out="$("$FLEET_SSH" "$host" "sudo -S -p \"\" systemctl mask $TARGETS && echo MASKED" 2>&1)"
apply_rc=$?
printf '%s\n' "$apply_out" | sed 's/^/  [apply] /'
if [ $apply_rc -ne 0 ] || ! printf '%s\n' "$apply_out" | grep -q '^MASKED$'; then
  printf '%s: mask command failed on %s (rc=%d)\n' "$SCRIPT_NAME" "$host" "$apply_rc" >&2
  exit 1
fi
report_state "after"
after_rc=$?
[ $after_rc -eq 0 ] && { printf '%s: PASS — %s aligned to the proven 4-target mask set\n' "$SCRIPT_NAME" "$host"; exit 0; }
printf '%s: FAIL — post-apply state on %s is not aligned\n' "$SCRIPT_NAME" "$host" >&2
exit 1
