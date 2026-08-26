#!/usr/bin/env bash
# validate-changed.sh — PostToolUse advisory validation hook (U3, owner UD3,
# 2026-08-25; registered 2026-08-26). Runs the ratified single validator
# (scripts/validate.py, UD1/UD2) scoped to the file just edited and surfaces
# failures into context with the exact reproduction command.
# Advisory ONLY: never blocks, never mutates, never contacts hosts or network;
# exit 0 always (hook framework is fail-open by design — this is feedback, not a gate).
set -u

payload="$(cat)"
path="$(printf '%s' "$payload" | sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
[ -z "$path" ] && exit 0
case "$path" in
  /home/hxsa/opt/HX-ASF-Servers/*) ;;
  *) exit 0 ;;
esac

ROOT="/home/hxsa/opt/HX-ASF-Servers"
cd "$ROOT" || exit 0
rel="${path#$ROOT/}"
out="$(PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate.py --changed "$rel" 2>&1)"
code=$?
if [ "$code" -ne 0 ]; then
  printf 'validate-changed: %s\n%s\n(reproduce: cd %s && python3 scripts/validate.py --changed %s)\n' "$rel" "$out" "$ROOT" "$rel"
fi
exit 0
