#!/usr/bin/env bash
# secret-boundary.sh — PreToolUse hook, pilot (owner UD4 2026-08-25, state log row 60)
#
# Intercepts secret-shaped content in tool payloads (Write/Edit/Bash) BEFORE it
# lands in a file or a command. Two detection layers:
#   1. generic credential patterns (PEM blocks, cloud/chat tokens, password
#      assignments) with an explicit REDACTED/withheld allowance for sanitized
#      evidence text;
#   2. the literal HX SSH credential, READ AT EXECUTION from the protected source
#      (the HX Fleet SSH Access Guide — credential record table) and never printed,
#      logged, stored, or copied anywhere — same discipline as the ratified askpass
#      pattern (state log row 53). If the protected file is unreadable, the literal
#      layer is skipped silently (fail-open).
#
# Mode: scripts/hooks/secret-boundary.mode contains "warn" (default; exit 0 with a
# stdout warning that lands in context) or "block" (exit 2 = the operation is
# stopped). Graduation warn -> block is a one-word edit after the pilot week.
# Hook framework is fail-open by design: this script is an interception layer,
# never the sole barrier (CAT-05 + protected-resource convention remain).
set -u

MODE_FILE="$(dirname "$0")/secret-boundary.mode"
MODE="warn"
[ -f "$MODE_FILE" ] && MODE="$(head -n1 "$MODE_FILE" | tr -d '[:space:]')"

payload="$(cat)"

hit=""

# Layer 1: generic patterns (REDACTED/withheld markers are explicitly allowed)
if printf '%s' "$payload" | grep -Eq 'BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|ghp_[0-9A-Za-z]{36}'; then
  hit="generic credential pattern (key/token)"
fi
# The value must look like a CREDENTIAL, not like an English word. Every
# recorded false positive was a word standing where a value would go — `field`,
# `assignment`, `supplied`, `set` — and twice that forced an append-only state
# log to be edited in place to clear the gate (DSH row 5, OMNIROUTE row 40).
# A credential carries a digit or punctuation, or is long.
#
# The allowance applies to the VALUE ONLY, and candidates are extracted BEFORE
# it runs. An earlier revision filtered the whole payload first: a tool payload
# is a single JSON line, so one occurrence of `askpass` anywhere in a Write
# would have disabled password detection for that entire write. That is a worse
# failure than the one it was fixing, and it is why the order below matters —
# extract, strip the key, then judge the value on its own.
#
# "password: supplied by the askpass helper" is not caught by the allowance at
# all; it is caught because `supplied` is not a live-looking value. The
# allowance exists only for explicit sanitizing values like REDACTED.
#
# STATED BOUND, matching scripts/validate.py: an all-lowercase passphrase under
# 16 characters with no digit or punctuation is not caught here. Flagging prose
# is the worse failure — layer 2 below is the backstop for the real credential.
if [ -z "$hit" ] && printf '%s' "$payload" \
    | grep -Eo 'password[[:space:]]*[:=][[:space:]]*[A-Za-z0-9!@#$%^&*._-]{6,}' \
    | sed -E 's/^[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd][[:space:]]*[:=][[:space:]]*//' \
    | grep -viE '^(REDACTED|withheld|askpass)$' \
    | grep -qE '[0-9]|[!@#$%^&*._-]|^.{16,}$'; then
  hit="password assignment with a live-looking value"
fi

# Layer 2: literal credential (read at execution; never stored or printed)
if [ -z "$hit" ]; then
  CRED_FILE="/home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md"
  if [ -r "$CRED_FILE" ]; then
    literal="$(awk -F'|' '/^\| SSH password \|/ {gsub(/[ `]/,"",$3); print $3; exit}' "$CRED_FILE" 2>/dev/null || true)"
    if [ -n "$literal" ] && printf '%s' "$payload" | grep -qF "$literal"; then
      hit="the literal protected credential"
    fi
    literal=""
  fi
fi

# Layer 3: protected-source copy-by-path (cat/cp/dd/tee/scp/rsync/tar taking the
# protected file as an argument). Read-at-execution patterns (awk/sed/grep/head)
# are NOT in the verb set — the ratified askpass and verification patterns pass.
if [ -z "$hit" ]; then
  if printf '%s' "$payload" | grep -Eiq '(cat|cp|dd|tee|scp|rsync|tar)[^|;&]*ssh-info\.md'; then
    hit="protected credential source referenced as a copy/read-verb argument (copy-by-path is out of policy; use read-at-execution patterns only)"
  fi
fi

if [ -n "$hit" ]; then
  msg="secret-boundary: BLOCK-CLASS content detected — $hit. Do not persist secrets; use REDACTED markers and the protected-resource convention (existence, owner, mechanism only)."
  if [ "$MODE" = "block" ]; then
    printf '%s\n' "$msg" >&2
    exit 2
  fi
  printf '%s\n' "$msg"
fi
exit 0
