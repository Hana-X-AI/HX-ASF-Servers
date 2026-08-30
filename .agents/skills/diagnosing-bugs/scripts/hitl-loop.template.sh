#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# Copy this file, edit the steps below, and run it.
# The agent runs the script; the user follows prompts in their terminal.
#
# Usage:
#   bash hitl-loop.template.sh
#
# Two helpers:
#   step "<instruction>"          → show instruction, wait for Enter
#   capture VAR "<question>"      → show question, read ONE LINE into VAR
#   capture_multi VAR "<question>" → show question, read MANY LINES into VAR
#
# Use `capture` for short answers (y/n, a version, a filename). Use
# `capture_multi` for anything the user pastes — stack traces, logs, diffs —
# because `capture` reads a single line and would silently drop everything
# after the first newline.
#
# At the end, captured values are printed as KEY=VALUE for the agent to parse.
#
# `capture` prints its value back to the terminal, where the agent reads it,
# so capture observations, and leave signing in to the user as a `step`.

# Provenance: mattpocock/skills @ 6654f6b60cd9d5be8b54c6fafe44346dabeb3b76 (MIT,
# Copyright (c) 2026 Matt Pocock), adopted 2026-08-30 under KDD-0020
# (Amendment 1). Correction at intake: upstream captured every answer with a
# single-line `read`, so a pasted stack trace silently lost everything after the
# first newline. `capture_multi` was added and the error-message prompt switched
# to it; `sanitize` still collapses newlines, so the KEY=VALUE contract holds.

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [Enter when done] " _
}

# Single-line answer. Anything after the first newline is NOT captured — use
# capture_multi for pasted, multi-line text.
capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# Multi-line answer: reads until a line containing only "." or until EOF
# (Ctrl-D), preserving every pasted line. The value still passes through
# sanitize() before it is echoed, which collapses the newlines to spaces, so the
# KEY=VALUE contract at the bottom of this script is unchanged.
capture_multi() {
  local var="$1" question="$2" line answer=""
  printf '\n>>> %s\n' "$question"
  printf '    (paste, then a line containing only "." — or press Ctrl-D)\n'
  while IFS= read -r line; do
    [ "$line" = "." ] && break
    answer="${answer}${line}"$'\n'
  done
  printf -v "$var" '%s' "$answer"
}

# Sanitize captured terminal text before it is echoed: remove complete ANSI
# control sequences — CSI (7-bit ESC [ and 8-bit C1 0x9B), OSC including OSC-8
# hyperlink payloads (7-bit ESC ] and 8-bit 0x9D), DCS/SOS/PM/APC (7-bit ESC
# P/X/^/_ and 8-bit 0x90/0x98/0x9E/0x9F) — plus remaining C0/C1 controls, then
# collapse newlines/whitespace. Emits only readable text content; the raw
# captured bytes (which may carry control/escape sequences that break parsing
# or leak into the terminal/agent log) are never emitted.
sanitize() {
  printf '%s' "$1" | perl -0777 -pe '
    s/\e\[[0-?]*[ -\/]*[@-~]//g;              # CSI (7-bit)
    s/\x9b[0-?]*[ -\/]*[@-~]//g;              # CSI (8-bit)
    s/\e\][^\a\e]*(?:\a|\e\\)//g;             # OSC incl. hyperlink (7-bit)
    s/\x9d[^\x07\x9c]*(?:\x07|\x9c)//g;       # OSC (8-bit)
    s/\e[PX^_][^\a\e]*(?:\a|\e\\)//g;         # DCS/SOS/PM/APC (7-bit)
    s/[\x90\x98\x9e\x9f][^\x07\x9c]*(?:\x07|\x9c)//g;  # DCS/SOS/PM/APC (8-bit)
    s/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F\x80-\x9F]//g;    # remaining C0/C1 controls
    s/[\r\n]+/ /g;
    s/[ \t]+/ /g;
    s/^ | $//g;
  '
}

# --- Self-test (CSI/OSC/C1 regression coverage) --------------------------
# Run with: bash hitl-loop.template.sh --selftest
if [ "${1:-}" = "--selftest" ]; then
  pass=0; fail=0
  t() { # t <label> <expected> <actual>
    if [ "$2" = "$3" ]; then
      printf 'ok   %s\n' "$1"; pass=$((pass + 1))
    else
      printf 'FAIL %s\nexpected: [%s]\nactual:   [%s]\n' "$1" "$2" "$3"
      fail=$((fail + 1))
    fi
  }
  t "plain"         "plain text"  "$(sanitize "plain text")"
  t "csi-sgr"       "red"         "$(sanitize "$(printf '\033[31mred\033[0m')")"
  t "csi-cursor"    "moved"       "$(sanitize "$(printf '\033[2J\033[10;10Hmoved')")"
  t "osc-title"     "title"       "$(sanitize "$(printf '\033]0;title\atitle')")"
  # shellcheck disable=SC1003  # `\\` is a literal backslash in the printf format:
  # ESC \ is the OSC-8 string terminator this case must inject. Not a quote escape.
  t "osc-hyperlink" "Click"       "$(sanitize "$(printf '\033]8;;https://evil\x1b\\Click\x1b]8;;\x1b\\')")"
  t "c1-csi"        "c1clean"     "$(sanitize "$(printf '\23331m\220c1clean')")"
  t "c1-osc"        "osc"         "$(sanitize "$(printf '\2350;title\007osc')")"
  t "c1-dcs"        "dcs"         "$(sanitize "$(printf '\220q1;2\234dcs')")"
  t "newlines"      "line1 line2" "$(sanitize "$(printf 'line1\nline2')")"
  printf '%d pass, %d fail\n' "$pass" "$fail"
  exit $(( fail == 0 ? 0 : 1 ))
fi

# --- edit below ---------------------------------------------------------

step "Open the app at http://localhost:3000 and sign in."

capture ERRORED "Click the 'Export' button. Did it throw an error? (y/n)"

capture_multi ERROR_MSG "Paste the error message, including any stack trace (or 'none'):"

# Sanitize the captured error before any subsequent output (including the
# final print below) so the raw value is never emitted.
ERROR_MSG=$(sanitize "$ERROR_MSG")

# --- edit above ---------------------------------------------------------

printf '\n--- Captured ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
