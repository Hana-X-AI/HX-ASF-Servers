#!/usr/bin/env bash
# governor-gate.sh — PostToolUse advisory hook (QA-audit R-6, 2026-08-29).
# Fires after a write to a producer deliverable / evidence document and reminds
# the governor to run the mandatory verification-checklist before acceptance.
# The checklist lives at agents/kimi-k3/verification-checklist.md (standing
# governor gate); the gate itself is manual + judgment-based and is enforced by
# the governor, not by this hook. Fail-open: exit 0 always.
set -u

payload="$(cat 2>/dev/null || true)"
path="$(printf '%s' "$payload" | sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
[ -z "$path" ] && exit 0

case "$path" in
  *evidence*|*verdicts*|*receipt*|*step*|*install*|*implementation-plan*|*test-log*) ;;
  *) exit 0 ;;
esac

printf 'governor-gate: before accepting %s, run the mandatory verification-checklist (agents/kimi-k3/verification-checklist.md) — artifact exists, receipt line, token context, secret sweep, integrity, claims-vs-live-state, boundary, completeness, honest limitations, handoff-to-Carol. A deliverable that fails any step goes back with one bounded correction.\n' "$path"
exit 0
