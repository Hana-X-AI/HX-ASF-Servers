#!/usr/bin/env bash
# fleet-hostkey-pin.sh — verified SSH host-key pinning ceremony (fleet library
# v0.1; F-05 discipline: pin strict, never accept-new, never disable checking).
#
# Ceremony: (1) strict BatchMode connection attempt — the expected "Host key
# verification failed" for an unpinned host is kept as evidence; (2) fetch the
# live host key (ssh-keyscan); (3) compare its fingerprint EXACTLY against the
# caller-supplied fingerprint record (owner-approved or trusted console
# evidence); (4) pin only on exact match; (5) re-verify strict. An
# already-pinned host is verified against the record and NOT re-pinned.
#
# MUTATION CLASS: appends to the executor's known_hosts ONLY on verified
# exact match. No change to any remote host. No credentials are handled:
# the probe connection runs BatchMode (all authentication disabled — it is a
# key check, not a login).
set -uo pipefail

SCRIPT_NAME="fleet-hostkey-pin.sh"

usage() {
  cat <<'EOF'
Usage: fleet-hostkey-pin.sh <host> <fingerprint-record-file>

Pins <host>'s SSH host key into known_hosts ONLY after the live key's
fingerprint exactly matches a fingerprint extracted from
<fingerprint-record-file> (a text record carrying a "SHA256:..." fingerprint,
e.g. an owner pre-work console record).

<host> must be the exact address to pin (an IP is recommended): known_hosts
entries are per-address and this tool probes the address directly — it does
not resolve fleet names. Pin each address you will connect to.

Steps (all evidence printed):
  1. strict BatchMode ssh attempt (expected to fail for unpinned hosts)
  2. ssh-keyscan of the live key (ed25519, then rsa/ecdsa fallback)
  3. exact fingerprint comparison against the record
  4. pin on match (skip when already pinned — verify instead)
  5. strict re-verification

NEVER accept-new. NEVER disables host-key checking. On any mismatch: no pin,
exit 1 — stop and escalate with the evidence printed.

Environment:
  FLEET_KNOWN_HOSTS   known_hosts file to pin into (default: ~/.ssh/known_hosts)

Exit status: 0 pinned-and-verified (new or existing); 1 on mismatch/failure.
EOF
}

host=""
record=""
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    -*) printf '%s: unknown option %s\n' "$SCRIPT_NAME" "$1" >&2; usage >&2; exit 1 ;;
    *) if [ -z "$host" ]; then host="$1"; elif [ -z "$record" ]; then record="$1"; else printf '%s: unexpected extra argument %s\n' "$SCRIPT_NAME" "$1" >&2; exit 1; fi ;;
  esac
  shift
done
{ [ -z "$host" ] || [ -z "$record" ]; } && { usage >&2; exit 1; }
[ -f "$record" ] || { printf '%s: fingerprint record not found: %s\n' "$SCRIPT_NAME" "$record" >&2; exit 1; }

KH="${FLEET_KNOWN_HOSTS:-$HOME/.ssh/known_hosts}"
[ -f "$KH" ] || : >> "$KH" || { printf '%s: cannot write %s\n' "$SCRIPT_NAME" "$KH" >&2; exit 1; }

# Fingerprint from the record file (first SHA256:... token).
record_fp="$(grep -oE 'SHA256:[A-Za-z0-9+/=]{20,}' "$record" | head -1)"
[ -z "$record_fp" ] && { printf '%s: no SHA256 fingerprint found in %s\n' "$SCRIPT_NAME" "$record" >&2; exit 1; }
printf 'record fingerprint (%s): %s\n' "$record" "$record_fp"

# Step 1: strict BatchMode attempt (expected failure for unpinned = evidence).
probe_out="$(ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=8 \
  -o UserKnownHostsFile="$KH" "$host" true 2>&1)"
probe_rc=$?
printf 'strict probe: rc=%d: %s\n' "$probe_rc" "$(printf '%s\n' "$probe_out" | head -1)"

already_pinned=0
case "$probe_out" in
  *"Host key verification failed"*) already_pinned=0 ;;
  *) already_pinned=1 ;;  # key accepted (auth then refused under BatchMode, or rc=0)
esac

# Step 2: fetch the live key.
live_keys="$(ssh-keyscan -t ed25519 -T 8 "$host" 2>/dev/null)"
[ -z "$live_keys" ] && live_keys="$(ssh-keyscan -t rsa,ecdsa -T 8 "$host" 2>/dev/null)"
[ -z "$live_keys" ] && { printf '%s: could not fetch a host key from %s\n' "$SCRIPT_NAME" "$host" >&2; exit 1; }

# Step 3: exact fingerprint comparison.
live_fp="$(printf '%s\n' "$live_keys" | ssh-keygen -lf - 2>/dev/null | awk '{print $2}' | head -1)"
live_type="$(printf '%s\n' "$live_keys" | awk '{print $2}' | head -1)"
printf 'live key (%s) fingerprint: %s\n' "$live_type" "$live_fp"
if [ "$live_fp" != "$record_fp" ]; then
  printf '%s: MISMATCH — live key does NOT match the record. NO PIN. Stop and escalate.\n' "$SCRIPT_NAME" >&2
  exit 1
fi
printf 'comparison: EXACT MATCH\n'

if [ $already_pinned -eq 1 ]; then
  # Verify the pinned entry itself matches the record (no re-pin).
  pinned_fp="$(ssh-keygen -F "$host" -f "$KH" 2>/dev/null | grep -v '^#' | ssh-keygen -lf - 2>/dev/null | awk '{print $2}' | head -1)"
  if [ "$pinned_fp" = "$record_fp" ]; then
    printf '%s: ALREADY-PINNED-VERIFIED — %s entry in %s matches the record; not re-pinned\n' "$SCRIPT_NAME" "$host" "$KH"
    exit 0
  fi
  printf '%s: pinned entry for %s does NOT match the record (%s). NO CHANGE. Stop and escalate.\n' "$SCRIPT_NAME" "$host" "${pinned_fp:-none}" >&2
  exit 1
fi

# Step 4: pin only the verified key line.
printf '%s\n' "$live_keys" | head -1 >> "$KH"
printf 'pinned: %s -> %s\n' "$host" "$KH"

# Step 5: strict re-verification.
verify_out="$(ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=8 \
  -o UserKnownHostsFile="$KH" "$host" true 2>&1)"
case "$verify_out" in
  *"Host key verification failed"*)
    printf '%s: FAIL — key still not accepted after pin: %s\n' "$SCRIPT_NAME" "$verify_out" >&2
    exit 1 ;;
esac
printf '%s: PINNED-NEW-VERIFIED — %s now passes strict checking (auth refusal under BatchMode is expected: the key check passed)\n' "$SCRIPT_NAME" "$host"
exit 0
