#!/usr/bin/env bash
# render-sync.sh — PostToolUse advisory validation hook (QA-audit ST-4, 2026-08-29).
# Runs the wiki render sync check (scripts/wiki/render.py --check) after a write
# to a Markdown file or the render manifest, and surfaces MISSING/DRIFT entries
# into context with the exact repair command.
# Advisory ONLY: never blocks, never mutates, never contacts hosts/network;
# exit 0 always (hook framework is fail-open by design — this is feedback, not a
# gate). The hard gate is CI's `gates` job + `validate.py`.
set -u

payload="$(cat 2>/dev/null || true)"
path="$(printf '%s' "$payload" | sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"

# Only relevant for repo markdown or the manifest itself
case "$path" in
  /home/hxsa/opt/HX-ASF-Servers/*.md|/home/hxsa/opt/HX-ASF-Servers/scripts/wiki/manifest.txt) ;;
  *) exit 0 ;;
esac

ROOT="/home/hxsa/opt/HX-ASF-Servers"
cd "$ROOT" || exit 0

out="$(PYTHONDONTWRITEBYTECODE=1 python3 scripts/wiki/render.py --check 2>&1)"
if printf '%s' "$out" | grep -qE 'MISSING|DRIFT|FAIL'; then
  printf 'render-sync: manifest drift detected after editing %s:\n%s\n(reproduce: cd %s && python3 scripts/wiki/render.py --check)\n' "$path" "$out" "$ROOT"
fi
exit 0
