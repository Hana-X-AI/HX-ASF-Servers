#!/usr/bin/env bash
# fleet-selftest.sh — offline self-test for the fleet script library
# (owner directive 2026-08-27; extended for review-batch-17 hardening H1-H4).
# No network, no hosts, no credentials: syntax checks, --help contracts,
# standards-file parsing, rule evaluation against --kv fixtures, fingerprint
# extraction, printf-%q quoting contract, prune-guard refusal matrix, and
# mock-transport tests of the evidence-pull and ntp-pin flows.
# Exit 1 on any failed check.
set -uo pipefail

usage() {
  cat <<'EOF'
Usage: fleet-selftest.sh

Offline self-test for the fleet script library. No network, no hosts, no
credentials: syntax checks, --help contracts, standards-file parsing, rule
evaluation against --kv fixtures (PASS / FAIL / REPORT cases), fingerprint
extraction, quoting and prune-guard hardening checks (mock transport).

Exit status: 0 when all checks pass; 1 on any failed check.
EOF
}

case "${1:-}" in
  -h|--help) usage; exit 0 ;;
  "") ;;
  *) printf 'fleet-selftest.sh: unknown option %s\n' "$1" >&2; usage >&2; exit 1 ;;
esac

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS="fleet-inventory.sh fleet-verify-baseline.sh fleet-ntp-pin.sh fleet-sleepmasks.sh fleet-evidence-pull.sh fleet-hostkey-pin.sh fleet-selftest.sh"

checks=0
failures=0

ok()   { checks=$((checks + 1)); printf 'PASS  %s\n' "$1"; }
bad()  { checks=$((checks + 1)); failures=$((failures + 1)); printf 'FAIL  %s\n' "$1"; }

# --- 1. presence, executability, syntax, --help contract -------------------
for s in $SCRIPTS; do
  p="$SCRIPT_DIR/$s"
  if [ -f "$p" ] && [ -x "$p" ]; then ok "$s exists and is executable"; else bad "$s missing or not executable"; fi
  if bash -n "$p" 2>/dev/null; then ok "$s bash -n clean"; else bad "$s bash -n syntax error"; fi
  if "$p" --help >/dev/null 2>&1 && "$p" --help 2>&1 | grep -q '^Usage:'; then
    ok "$s --help prints usage"
  else
    bad "$s --help broken"
  fi
done

# --- 2. standards file + rule evaluation via fixtures ----------------------
fx="$(mktemp -d)" || exit 1
trap 'rm -rf "$fx"' EXIT

# Fixture A: fully compliant llm-host
cat > "$fx/hxs-1.kv" <<'EOF'
identity.hostname	hxs-1
time.timezone	Etc/UTC
time.ntp_enabled	yes
time.ntp_synchronized	yes
time.ntp_server	162.159.200.123 (time.cloudflare.com)
sleep_targets.suspend	masked
sleep_targets.hibernate	masked
sleep_targets.hybrid_sleep	masked
sleep_targets.suspend_then_hibernate	masked
sleep_targets.sleep	static
firewall.ufw_active	inactive
firewall.ufw_enabled	not-installed
firewall.ufw_conf	no
security.secure_boot	disabled
failed_units	0
ollama.present	true
ollama.active	active
EOF
# Fixture B: llm-host with one divergence (hybrid-sleep unmasked)
sed 's/^sleep_targets.hybrid_sleep	masked$/sleep_targets.hybrid_sleep	static/' "$fx/hxs-1.kv" > "$fx/hxs-2.kv"
# Fixture C: server-default host on the distro NTP default (hxs-8 class case)
cat > "$fx/hxs-8.kv" <<'EOF'
identity.hostname	hxs-8
time.timezone	Etc/UTC
time.ntp_enabled	yes
time.ntp_synchronized	yes
time.ntp_server	185.125.190.58 (ntp.ubuntu.com)
EOF

out_a="$(FLEET_KV_DIR="$fx" "$SCRIPT_DIR/fleet-verify-baseline.sh" hxs-1 2>&1)"; rc_a=$?
if [ $rc_a -eq 0 ] && printf '%s\n' "$out_a" | grep -q '10 PASS, 0 FAIL'; then
  ok "verify-baseline fixture A (compliant llm-host): 10 PASS, 0 FAIL, exit 0"
else
  bad "verify-baseline fixture A (rc=$rc_a): $out_a"
fi

out_b="$(FLEET_KV_DIR="$fx" "$SCRIPT_DIR/fleet-verify-baseline.sh" hxs-2 2>&1)"; rc_b=$?
if [ $rc_b -eq 1 ] && printf '%s\n' "$out_b" | grep -q '9 PASS, 1 FAIL'; then
  ok "verify-baseline fixture B (divergent llm-host): 9 PASS, 1 FAIL, exit 1"
else
  bad "verify-baseline fixture B (rc=$rc_b): $out_b"
fi

out_c="$(FLEET_KV_DIR="$fx" "$SCRIPT_DIR/fleet-verify-baseline.sh" hxs-8 2>&1)"; rc_c=$?
# Amended 2026-08-27 (fleet-standard: server-default NTP + masks now enforce):
# the same unpinned fixture now correctly yields 3 PASS, 1 FAIL (ntp_server),
# 4 NOT-ESTABLISHED (empty mask actuals), exit 1 — previously 1 PASS/1 REPORT/exit 0.
if [ $rc_c -eq 1 ] && printf '%s\n' "$out_c" | grep -q '3 PASS, 1 FAIL, 0 REPORT, 4 NOT-ESTABLISHED'; then
  ok "verify-baseline fixture C (server-default, unpinned NTP): 3 PASS, 1 FAIL, 4 NOT-ESTABLISHED, exit 1 (amended standard)"
else
  bad "verify-baseline fixture C (rc=$rc_c): $out_c"
fi

out_d="$(FLEET_KV_DIR="$fx" "$SCRIPT_DIR/fleet-verify-baseline.sh" hxs-99 2>&1)"
if printf '%s\n' "$out_d" | grep -q 'SKIP'; then
  ok "verify-baseline undeclared host: SKIP"
else
  bad "verify-baseline undeclared host: $out_d"
fi

# --- 3. fingerprint-record extraction (hostkey-pin contract) ---------------
cat > "$fx/record.md" <<'EOF'
ED25519 key fingerprint is SHA256:qtFdqEskYzA8l1nl+E1cW4/Z/TK+mpxWHHpYsGJp2EI.
EOF
fp="$(grep -oE 'SHA256:[A-Za-z0-9+/=]{20,}' "$fx/record.md" | head -1)"
if [ "$fp" = "SHA256:qtFdqEskYzA8l1nl+E1cW4/Z/TK+mpxWHHpYsGJp2EI" ]; then
  ok "fingerprint-record extraction"
else
  bad "fingerprint-record extraction ($fp)"
fi

# --- 4. H1: printf '%q' quoting contract (hostile inputs round-trip) -------
v="/tmp/rick's-test"
if [ "$(printf '%q' "$v")" = "/tmp/rick\'s-test" ]; then
  ok "printf %q single-quote form ($v)"
else
  bad "printf %q single-quote form: $(printf '%q' "$v")"
fi
# Hostile vector; expected output pinned from a LIVE `printf '%q'` run on
# this host's bash (5.2.21, Ubuntu 24.04) — bash-version variance is why the
# live-verified literal is pinned rather than hand-derived. Zero eval in this
# script; remote-shell reuse of the %q form is proven by the mock-transport
# check in section 7 and by the live hostile-path pull/prune proofs (batch 17).
v2="/tmp/a b*\$x\`echo pwn\`?[!z]"
expected_v2="/tmp/a\\ b\\*\\\$x\\\`echo\\ pwn\\\`\\?\\[\\!z\\]"
if [ "$(printf '%q' "$v2")" = "$expected_v2" ]; then
  ok "printf %q hostile vector matches the live-pinned literal (safely reusable form)"
else
  bad "printf %q hostile vector: got [$(printf '%q' "$v2")] want [$expected_v2]"
fi

# --- 5. mock transport for flow tests --------------------------------------
mkdir -p "$fx/mockroot/sub"
echo alpha > "$fx/mockroot/a.txt"
echo beta  > "$fx/mockroot/sub/b.txt"
cat > "$fx/mock-ssh" <<'EOF'
#!/usr/bin/env bash
# fleet-selftest mock transport: records invocations, replays canned flows.
host="$1"; shift; cmd="$*"
printf '%s\t%s\n' "$host" "$cmd" >> "$MOCK_LOG"
case "$cmd" in
  *"mktemp /tmp/.fleet-ntp-pin."*)
    if [ "${MOCK_NTP:-diff}" = "hostile" ]; then
      printf 'STAGED_PATH=/tmp/.fleet-ntp-pin.Ab3xY9z2;id\n'
      printf 'diff-rc=1 (0 = already matches, 1 = differences present)\n'
    elif [ "${MOCK_NTP:-diff}" = "compliant" ]; then
      printf 'STAGED_PATH=/tmp/.fleet-ntp-pin.Ab3xY9z2\n'
      printf 'diff-rc=0 (0 = already matches, 1 = differences present)\n'
    else
      printf 'STAGED_PATH=/tmp/.fleet-ntp-pin.Ab3xY9z2\n'
      printf '%s\n' '--- /etc/systemd/timesyncd.conf' \
                    '+++ /tmp/.fleet-ntp-pin.Ab3xY9z2' \
                    '@@ -17,2 +17,2 @@' \
                    '-#NTP=' \
                    '-#FallbackNTP=ntp.ubuntu.com' \
                    '+NTP=time.cloudflare.com' \
                    '+FallbackNTP=' \
                    'diff-rc=1 (0 = already matches, 1 = differences present)'
    fi
    exit 0 ;;
  "test -d "*) exit 0 ;;
  "cd "*find*) printf './a.txt\n./sub/b.txt\n'; exit 0 ;;
  "cd "*tar*) cd "$MOCK_ROOT" && tar cf - .; exit 0 ;;
  "rm -rf -- "*) exit 0 ;;
  "rm -f "*) exit 0 ;;
esac
exit 0
EOF
chmod +x "$fx/mock-ssh"
export MOCK_LOG="$fx/mock.log" MOCK_ROOT="$fx/mockroot"
: > "$MOCK_LOG"

# --- 6. H2: prune-guard refusal matrix (guard precedes any transport) ------
guard_fail=0
for p in "/" "/tmp" "/tmp/" "/etc" "/etc/" "/opt" ""; do
  : > "$MOCK_LOG"
  out_g="$(FLEET_SSH="$fx/mock-ssh" "$SCRIPT_DIR/fleet-evidence-pull.sh" dummyhost "$p" "$fx/pull-g" --prune 2>&1)"; rc_g=$?
  if [ $rc_g -eq 1 ] && printf '%s\n' "$out_g" | grep -qi 'refusing to prune' && [ ! -s "$MOCK_LOG" ]; then
    ok "prune guard refuses [$p] before any transport"
  else
    guard_fail=1
    bad "prune guard [$p]: rc=$rc_g out=[$out_g] log=[$(cat "$MOCK_LOG")]"
  fi
done
[ $guard_fail -eq 0 ] && ok "prune-guard refusal matrix complete (7 cases, zero transport calls)"

# --- 7. H2 allow-case + H1 hostile-path flow via mock ----------------------
: > "$MOCK_LOG"
out_p="$(FLEET_SSH="$fx/mock-ssh" "$SCRIPT_DIR/fleet-evidence-pull.sh" dummyhost "/tmp/rick's-test" "$fx/pull-h" 2>&1)"; rc_p=$?
if [ $rc_p -eq 0 ] && printf '%s\n' "$out_p" | grep -q 'verified=1'; then
  ok "mock pull succeeds on hostile path /tmp/rick's-test"
else
  bad "mock pull hostile path: rc=$rc_p out=[$out_p]"
fi
if grep -qF "cd /tmp/rick\'s-test" "$MOCK_LOG" && ! grep -qF "cd '/tmp/rick's-test'" "$MOCK_LOG"; then
  ok "H1: remote commands use the %q-quoted path (no raw-quote breakout)"
else
  bad "H1: mock log quoting: [$(cat "$MOCK_LOG")]"
fi

: > "$MOCK_LOG"
out_q="$(FLEET_SSH="$fx/mock-ssh" "$SCRIPT_DIR/fleet-evidence-pull.sh" dummyhost "/tmp/esme-x" "$fx/pull-q" --prune 2>&1)"; rc_q=$?
if [ $rc_q -eq 0 ] && grep -qF 'rm -rf -- /tmp/esme-x' "$MOCK_LOG"; then
  ok "H2 allow-case: /tmp/<dir> stays prunable (verified pull then prune)"
else
  bad "H2 allow-case: rc=$rc_q out=[$out_q] log=[$(cat "$MOCK_LOG")]"
fi

# --- 8. H3/H4: ntp-pin staging contract via mock ---------------------------
: > "$MOCK_LOG"
out_n="$(FLEET_SSH="$fx/mock-ssh" MOCK_NTP=diff "$SCRIPT_DIR/fleet-ntp-pin.sh" dummyhost --dry-run 2>&1)"; rc_n=$?
if [ $rc_n -eq 0 ] && printf '%s\n' "$out_n" | grep -q 'DRY-RUN' && grep -qF 'rm -f /tmp/.fleet-ntp-pin.Ab3xY9z2' "$MOCK_LOG"; then
  ok "H3: dry-run parses STAGED_PATH and cleans up the parsed path"
else
  bad "H3 dry-run: rc=$rc_n out=[$out_n] log=[$(cat "$MOCK_LOG")]"
fi
if printf '%s\n' "$out_n" | grep -q '^STAGED_PATH=/tmp/.fleet-ntp-pin.Ab3xY9z2$'; then
  ok "H3: stage output carries the parseable STAGED_PATH line"
else
  bad "H3 STAGED_PATH line missing: [$out_n]"
fi

# --- 8b. H3b: semicolon-suffixed STAGED_PATH is refused, never re-used -----
: > "$MOCK_LOG"
out_h="$(FLEET_SSH="$fx/mock-ssh" MOCK_NTP=hostile "$SCRIPT_DIR/fleet-ntp-pin.sh" dummyhost --dry-run 2>&1)"; rc_h=$?
if [ $rc_h -eq 1 ] && printf '%s\n' "$out_h" | grep -q 'refusing to use unexpected staged path' && [ "$(grep -cP '^dummyhost\t' "$MOCK_LOG")" -eq 1 ]; then
  ok "H3b: semicolon-suffixed STAGED_PATH refused before any reuse (exactly one transport call — the stage itself)"
else
  bad "H3b hostile staged path: rc=$rc_h out=[$out_h] log=[$(cat "$MOCK_LOG")]"
fi

: > "$MOCK_LOG"
out_c2="$(FLEET_SSH="$fx/mock-ssh" MOCK_NTP=compliant "$SCRIPT_DIR/fleet-ntp-pin.sh" dummyhost --dry-run 2>&1)"; rc_c2=$?
if [ $rc_c2 -eq 0 ] && printf '%s\n' "$out_c2" | grep -q 'already-compliant' && grep -qF 'rm -f /tmp/.fleet-ntp-pin.Ab3xY9z2' "$MOCK_LOG"; then
  ok "H4: empty diff -> already-compliant, cleanup, exit 0"
else
  bad "H4 already-compliant: rc=$rc_c2 out=[$out_c2] log=[$(cat "$MOCK_LOG")]"
fi

# --- summary ---------------------------------------------------------------
printf '\nselftest: %d checks, %d failures\n' "$checks" "$failures"
[ $failures -gt 0 ] && exit 1
exit 0
