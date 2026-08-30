#!/usr/bin/env bash
# test-log-append.sh — PostToolUse advisory hook (QA-audit ST-7, 2026-08-29).
# Fires after a write to a test-evidence file or the test log itself and
# reminds the session to append a dated row to governace/testing/test-log.md.
# Fail-open: never blocks; exit 0 always (feedback, not a gate).
set -u

payload="$(cat 2>/dev/null || true)"
path="$(printf '%s' "$payload" | sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
[ -z "$path" ] && exit 0

ROOT="/home/hxsa/opt/HX-ASF-Servers"
LOG="$ROOT/governace/testing/test-log.md"

# Relevant when a test/evidence artifact or the test log itself changed.
# *test* covers */governace/testing/* and */tests/* (SC2221/SC2222-clean).
case "$path" in
  *test*|*evidence*) ;;
  *) exit 0 ;;
esac

# If the write was to the log itself, nothing to remind about.
case "$path" in
  */governace/testing/test-log.md) exit 0 ;;
esac

if [ ! -f "$LOG" ]; then
  printf 'test-log: %s does not exist — create it and append this run.\n' "$LOG"
  exit 0
fi

printf 'test-log: remember to append a dated row (system, test, PASS/FAIL/SKIP, evidence, notes) to %s after this run, then re-render + validate.\n' "$LOG"
exit 0
