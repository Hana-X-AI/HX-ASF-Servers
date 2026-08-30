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

# Sanitize captured terminal text before it is echoed: strip ANSI escape
# sequences and control characters, and collapse newlines to spaces, so the
# KEY=VALUE output below never emits the raw captured bytes (which may carry
# control/escape sequences or embedded newlines that break parsing or leak
# into the terminal/agent log). The diagnostic text content is preserved.
sanitize() {
  printf '%s' "$1" \
    | sed 's/\x1b\[[0-9;]*m//g' \
    | tr -d '\000-\010\013\014\016-\037\177' \
    | tr '\n\r' ' ' \
    | sed 's/[[:space:]][[:space:]]*/ /g'
}

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
