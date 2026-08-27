#!/usr/bin/env bash
# fleet-ntp-pin.sh — staged fail-closed pin of the fleet NTP source
# (fleet library v0.1; codifies the proven 2026-08-26 fleet-pass pattern:
# stage -> diff review -> apply with install -m 0644 -> restart
# systemd-timesyncd -> verify current server).
#
# Sets exactly:  NTP=time.cloudflare.com  and  FallbackNTP=  (explicit empty,
# clearing the compiled-in distro fallback per the one-source directive).
#
# Hardening (review batch 17, 2026-08-27):
#   H3 — the staged file is created by remote `mktemp` (unprivileged, in
#        /tmp, mode 600, owned by the transport user; random suffix). The
#        stage step EMITS `STAGED_PATH=<path>`; the script parses it back,
#        validates its shape, and uses the parsed value for the diff, the
#        apply install, and every cleanup. No fixed path anywhere in the
#        flow. Chosen approach documented here: /tmp mktemp (not /root) so
#        --dry-run staging needs no privilege; residual risk — between
#        diff-review and apply, only the transport user or root can touch
#        the staged file.
#   H4 — an empty diff means the host is already compliant: the script
#        reports `already-compliant`, cleans the staged file, and exits 0
#        instead of aborting. The added-line check still applies to
#        NON-empty diffs, so genuinely missing NTP content still aborts.
#
# MUTATION CLASS: MUTATING with --apply (edits /etc/systemd/timesyncd.conf,
# restarts systemd-timesyncd). Default mode is --dry-run (stage + diff +
# report, ZERO mutation). Run --apply ONLY under an explicit work order for
# the named host.
#
# CREDENTIAL BOUNDARY: this script NEVER handles credentials. SSH transport is
# the caller's via FLEET_SSH (single executable path; default: ssh). The
# --apply step uses `sudo -S` on the remote: feed sudo through this script's
# stdin (e.g. `your-askpass | fleet-ntp-pin.sh <host> --apply`) or have
# passwordless sudo remotely. The script never reads, stores, or logs it.
set -uo pipefail

SCRIPT_NAME="fleet-ntp-pin.sh"

usage() {
  cat <<'EOF'
Usage: fleet-ntp-pin.sh <host> [--dry-run|--apply]

Pins the fleet NTP source on <host>:
  NTP=time.cloudflare.com
  FallbackNTP=            (explicit empty — one source, no fallback)

Modes:
  --dry-run   (DEFAULT) stage the edit remotely (remote mktemp), show the
              unified diff, remove the staged file, report what --apply
              would do. Zero mutation. A host already matching the pin
              reports `already-compliant` and exits 0.
  --apply     execute: stage -> diff -> install -m 0644 root:root ->
              restart systemd-timesyncd -> poll-verify the current server
              (up to 45 s). Requires an explicit work order for <host>.

Rollback (exact inverse): restore the pre-change /etc/systemd/timesyncd.conf
content shown in the diff (stock file has every [Time] entry commented) and
`systemctl restart systemd-timesyncd`.

Environment:
  FLEET_SSH   SSH executable/wrapper for transport (default: ssh).

Exit status: 0 on successful dry-run, already-compliant, or verified apply;
             1 otherwise.
EOF
}

mode="dry-run"
host=""
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) mode="dry-run" ;;
    --apply) mode="apply" ;;
    -h|--help) usage; exit 0 ;;
    -*) printf '%s: unknown option %s\n' "$SCRIPT_NAME" "$1" >&2; usage >&2; exit 1 ;;
    *) if [ -z "$host" ]; then host="$1"; else printf '%s: unexpected extra argument %s\n' "$SCRIPT_NAME" "$1" >&2; exit 1; fi ;;
  esac
  shift
done
[ -z "$host" ] && { usage >&2; exit 1; }

FLEET_SSH="${FLEET_SSH:-ssh}"

# H3: stage remotely via mktemp with a fail-closed awk guard (abort unless
# both stock keys matched). Emits a parseable STAGED_PATH=<path> line.
STAGE_REMOTE="$(cat <<'EOS'
STAGED_PATH=$(mktemp /tmp/.fleet-ntp-pin.XXXXXXXX) || { echo "STAGE-FAILED (mktemp rc=$?)"; exit 1; }
awk "/^#?NTP=/ { print \"NTP=time.cloudflare.com\"; n=1; next }
     /^#?FallbackNTP=/ { print \"FallbackNTP=\"; f=1; next }
     { print }
     END { if (!n || !f) exit 3 }" /etc/systemd/timesyncd.conf > "$STAGED_PATH"
rc=$?
if [ $rc -ne 0 ]; then
  rm -f "$STAGED_PATH"
  echo "STAGE-FAILED (unexpected timesyncd.conf shape; guard rc=$rc)"
  exit $rc
fi
echo "STAGED_PATH=$STAGED_PATH"
diff -u /etc/systemd/timesyncd.conf "$STAGED_PATH"
echo "diff-rc=$? (0 = already matches, 1 = differences present)"
EOS
)"

stage_out="$("$FLEET_SSH" "$host" "$STAGE_REMOTE" </dev/null 2>&1)"
stage_rc=$?
printf '%s\n' "$stage_out"

staged="$(printf '%s\n' "$stage_out" | sed -n 's/^STAGED_PATH=//p' | head -1)"
if [ $stage_rc -ne 0 ] || [ -z "$staged" ]; then
  printf '%s: staging failed on %s — nothing applied (fail-closed)\n' "$SCRIPT_NAME" "$host" >&2
  exit 1
fi
# Validate the parsed path shape before using it anywhere.
case "$staged" in
  /tmp/.fleet-ntp-pin.*) ;;
  *) printf '%s: refusing to use unexpected staged path "%s" on %s\n' "$SCRIPT_NAME" "$staged" "$host" >&2; exit 1 ;;
esac

# H4: empty diff = already compliant — success, after normal cleanup.
if printf '%s\n' "$stage_out" | grep -q '^diff-rc=0 '; then
  "$FLEET_SSH" "$host" "rm -f $staged" </dev/null >/dev/null 2>&1
  printf '%s: already-compliant — /etc/systemd/timesyncd.conf on %s already matches the fleet pin (no changes needed)\n' "$SCRIPT_NAME" "$host"
  exit 0
fi

# Non-empty diff: the expected NTP line must be among the additions.
if ! printf '%s\n' "$stage_out" | grep -q '^+NTP=time.cloudflare.com$'; then
  printf '%s: staged content missing expected NTP line on %s — aborting\n' "$SCRIPT_NAME" "$host" >&2
  "$FLEET_SSH" "$host" "rm -f $staged" </dev/null >/dev/null 2>&1
  exit 1
fi

if [ "$mode" = "dry-run" ]; then
  "$FLEET_SSH" "$host" "rm -f $staged" </dev/null >/dev/null 2>&1
  printf '\nDRY-RUN: would apply the diff above on %s and restart systemd-timesyncd.\n' "$host"
  printf 'Zero mutation performed. Re-run with --apply under an explicit work order.\n'
  exit 0
fi

# ---- apply (work-order gated, stdin passthrough to remote sudo -S) ----
APPLY_REMOTE="$(cat <<EOS
sudo -S -p "" sh -c "install -m 0644 -o root -g root $staged /etc/systemd/timesyncd.conf && rm -f $staged && systemctl restart systemd-timesyncd && echo APPLIED"
EOS
)"

printf '\nAPPLY: installing on %s and restarting systemd-timesyncd at %s (UTC)\n' "$host" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
apply_out="$("$FLEET_SSH" "$host" "$APPLY_REMOTE" 2>&1)"
apply_rc=$?
printf '%s\n' "$apply_out"
if [ $apply_rc -ne 0 ] || ! printf '%s\n' "$apply_out" | grep -q '^APPLIED$'; then
  printf '%s: apply failed on %s (rc=%d). Staged file may remain at %s; rollback per --help.\n' "$SCRIPT_NAME" "$host" "$apply_rc" "$staged" >&2
  exit 1
fi

# Poll-verify the active server (up to 45 s), then show effective state.
VERIFY_REMOTE="$(cat <<'EOS'
for i in $(seq 1 15); do
  srv=$(timedatectl timesync-status 2>/dev/null | sed -n "s/^ *Server: //p")
  case "$srv" in *cloudflare*) echo "server-contacted after ~$(( (i-1)*3 ))s: $srv"; break;; esac
  [ "$i" = 15 ] && echo "TIMEOUT waiting for time.cloudflare.com (last: $srv)"
  sleep 3
done
timedatectl show -p NTP -p NTPSynchronized -p Timezone
grep -E "^NTP=|^FallbackNTP=" /etc/systemd/timesyncd.conf
systemctl is-active systemd-timesyncd
EOS
)"

verify_out="$("$FLEET_SSH" "$host" "$VERIFY_REMOTE" </dev/null 2>&1)"
printf '%s\n' "$verify_out"
if printf '%s\n' "$verify_out" | grep -q '^server-contacted' && printf '%s\n' "$verify_out" | grep -q '^NTPSynchronized=yes$'; then
  printf '%s: PASS — %s pinned to time.cloudflare.com and synchronized\n' "$SCRIPT_NAME" "$host"
  exit 0
fi
printf '%s: FAIL — post-apply verification did not confirm the pinned source on %s\n' "$SCRIPT_NAME" "$host" >&2
exit 1
