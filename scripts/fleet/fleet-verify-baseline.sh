#!/usr/bin/env bash
# fleet-verify-baseline.sh — READ-ONLY actual-vs-declared fleet verification
# (fleet library v0.1, owner directive 2026-08-27: "base verification rick can
# execute now across the fleet"; hxs-2 state log row 44).
#
# Runs fleet-inventory.sh per host and diffs the result against
# fleet-standard.yaml: PASS/FAIL per host per enforce-rule, REPORT lines for
# declared-direction rules awaiting an owner call, NOT-ESTABLISHED when a fact
# cannot be determined from read-only evidence.
#
# CREDENTIAL BOUNDARY: this script NEVER handles credentials. SSH transport is
# the caller's via FLEET_SSH (single executable path; default: ssh).
#
# MUTATION CLASS: none. Every local and remote command is read-only.
set -uo pipefail

SCRIPT_NAME="fleet-verify-baseline.sh"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: fleet-verify-baseline.sh [host ...] [--standard <file>]

Verifies each host against the declared expected state in fleet-standard.yaml
and prints a PASS/FAIL/REPORT/NOT-ESTABLISHED matrix plus per-host and overall
summary lines.

Options:
  --standard <file>   standards file (default: fleet-standard.yaml next to
                      this script)
  -h, --help          this text

Environment:
  FLEET_SSH     SSH executable/wrapper for transport (default: ssh).
  FLEET_KV_DIR  test hook: read "<dir>/<host>.kv" fixtures instead of running
                live inventory (used by fleet-selftest.sh; not for production).

Verdicts: PASS/FAIL (enforce rules), REPORT (declared direction, owner call
pending), NOT-ESTABLISHED (fact not determinable read-only), SKIP (host has
no class in the standards file).

Exit status: 0 when no host has an enforce-rule FAIL; 1 otherwise or on usage
error.
EOF
}

standard="$SCRIPT_DIR/fleet-standard.yaml"
hosts=()
while [ $# -gt 0 ]; do
  case "$1" in
    --standard) shift; standard="${1:-}"; [ -z "$standard" ] && { printf '%s: --standard needs a file\n' "$SCRIPT_NAME" >&2; exit 1; } ;;
    -h|--help) usage; exit 0 ;;
    -*) printf '%s: unknown option %s\n' "$SCRIPT_NAME" "$1" >&2; usage >&2; exit 1 ;;
    *) hosts+=("$1") ;;
  esac
  shift
done
[ ${#hosts[@]} -eq 0 ] && { usage >&2; exit 1; }
[ -f "$standard" ] || { printf '%s: standards file not found: %s\n' "$SCRIPT_NAME" "$standard" >&2; exit 1; }

FLEET_SSH="${FLEET_SSH:-ssh}"
export FLEET_SSH

# ---- parse fleet-standard.yaml (awk; the file documents its own grammar) ----
parse_out="$(awk '
  /^host_classes:/ { section="classes"; next }
  /^rules:/        { section="rules"; next }
  section == "classes" && /^  [^ ]/ {
    line=$0; sub(/^  /, "", line)
    host=line; sub(/:.*/, "", host)
    class=line; sub(/.*:[ ]*/, "", class)
    if (host != "" && class != "") printf "CLASS\t%s\t%s\n", host, class
    next
  }
  section == "rules" && /^  - class:/ {
    if (rclass != "" && rpath != "") printf "RULE\t%s\t%s\t%s\t%s\t%s\n", rclass, rpath, rop, rval, rlevel
    rclass=$3; rpath=""; rop=""; rval=""; rlevel=""
    next
  }
  section == "rules" && /^    path:/  { rpath=$2; next }
  section == "rules" && /^    op:/    { rop=$2; next }
  section == "rules" && /^    value:/ { rval=$2; next }
  section == "rules" && /^    level:/ { rlevel=$2; next }
  END {
    if (rclass != "" && rpath != "") printf "RULE\t%s\t%s\t%s\t%s\t%s\n", rclass, rpath, rop, rval, rlevel
  }
' "$standard")"
[ -z "$parse_out" ] && { printf '%s: no classes/rules parsed from %s\n' "$SCRIPT_NAME" "$standard" >&2; exit 1; }

declare -A HOST_CLASS=()
RULE_CLASS=(); RULE_PATH=(); RULE_OP=(); RULE_VALUE=(); RULE_LEVEL=()
while IFS=$'\t' read -r kind a b c d e; do
  case "$kind" in
    CLASS) HOST_CLASS[$a]="$b" ;;
    RULE) RULE_CLASS+=("$a"); RULE_PATH+=("$b"); RULE_OP+=("$c"); RULE_VALUE+=("$d"); RULE_LEVEL+=("$e") ;;
  esac
done <<< "$parse_out"

kv_lookup() {
  # kv_lookup <kv-file> <path>
  awk -F'\t' -v p="$2" '$1 == p {print $2; exit}' "$1"
}

workdir="$(mktemp -d)" || exit 1
trap 'rm -rf "$workdir"' EXIT

total_fail_hosts=0

for host in "${hosts[@]}"; do
  class="${HOST_CLASS[$host]:-}"
  if [ -z "$class" ]; then
    printf '%s: SKIP (no class declared in %s)\n\n' "$host" "$standard"
    continue
  fi

  kvfile="$workdir/$host.kv"
  if [ -n "${FLEET_KV_DIR:-}" ]; then
    if [ -f "$FLEET_KV_DIR/$host.kv" ]; then
      cp "$FLEET_KV_DIR/$host.kv" "$kvfile"
    else
      printf '%s (%s): ERROR — fixture %s/%s.kv not found\n\n' "$host" "$class" "$FLEET_KV_DIR" "$host" >&2
      total_fail_hosts=$((total_fail_hosts + 1))
      continue
    fi
  else
    if ! "$SCRIPT_DIR/fleet-inventory.sh" "$host" --kv > "$kvfile" 2>"$workdir/$host.err"; then
      printf '%s (%s): ERROR — inventory failed: %s\n\n' "$host" "$class" "$(cat "$workdir/$host.err")" >&2
      total_fail_hosts=$((total_fail_hosts + 1))
      continue
    fi
  fi

  n_pass=0; n_fail=0; n_report=0; n_ne=0
  printf '%s (%s):\n' "$host" "$class"
  for i in "${!RULE_CLASS[@]}"; do
    [ "${RULE_CLASS[$i]}" = "$class" ] || continue
    path="${RULE_PATH[$i]}"; op="${RULE_OP[$i]}"; expect="${RULE_VALUE[$i]}"; level="${RULE_LEVEL[$i]}"
    actual="$(kv_lookup "$kvfile" "$path")"
    if [ "$level" = "report" ]; then
      printf '  REPORT          %-38s actual="%s" (declared direction: %s %s — owner call pending)\n' "$path" "$actual" "$op" "$expect"
      n_report=$((n_report + 1))
      continue
    fi
    if [ -z "$actual" ] || [ "$actual" = "unknown" ]; then
      printf '  NOT-ESTABLISHED %-38s actual="%s"\n' "$path" "${actual:-empty}"
      n_ne=$((n_ne + 1))
      continue
    fi
    ok=1
    case "$op" in
      eq) [ "$actual" = "$expect" ] && ok=0 ;;
      ne) [ "$actual" != "$expect" ] && ok=0 ;;
      contains) case "$actual" in *"$expect"*) ok=0 ;; esac ;;
      in) case ",$expect," in *,"$actual",*) ok=0 ;; esac ;;
      *) printf '  ERROR           %-38s unknown op "%s" in standards file\n' "$path" "$op"; n_fail=$((n_fail + 1)); continue ;;
    esac
    if [ $ok -eq 0 ]; then
      printf '  PASS            %-38s = "%s"\n' "$path" "$actual"
      n_pass=$((n_pass + 1))
    else
      printf '  FAIL            %-38s expected %s "%s", actual "%s"\n' "$path" "$op" "$expect" "$actual"
      n_fail=$((n_fail + 1))
    fi
  done
  printf 'Summary: %s: %d PASS, %d FAIL, %d REPORT, %d NOT-ESTABLISHED\n\n' "$host" "$n_pass" "$n_fail" "$n_report" "$n_ne"
  [ $n_fail -gt 0 ] && total_fail_hosts=$((total_fail_hosts + 1))
done

printf 'OVERALL: hosts=%d, hosts-with-FAIL=%d\n' "${#hosts[@]}" "$total_fail_hosts"
[ $total_fail_hosts -gt 0 ] && exit 1
exit 0
