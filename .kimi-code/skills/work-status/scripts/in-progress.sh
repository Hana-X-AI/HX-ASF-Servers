#!/usr/bin/env bash
# in-progress.sh — goals currently being worked.
# Adapted from automazeio/ccpm (MIT). Reads the factory goal tree.
# Usage: bash .kimi-code/skills/work-status/scripts/in-progress.sh
set -u

GOALS_DIR=""
for cand in "governace/goals" "goals"; do
  if [ -d "$cand" ]; then GOALS_DIR="$cand"; break; fi
done
[ -z "$GOALS_DIR" ] && { echo "No goals directory found."; exit 0; }

echo "🔄 In-Progress Goals"
echo "===================="
echo ""

status_of() {
  grep -m1 -oiE '^\s*-\s*Status:\s*\**?(draft|approved|in-progress|blocked|done|complete|abandoned)' "$1" 2>/dev/null \
    | sed -E 's/.*Status:\s*\**//' \
    | tr '[:upper:]' '[:lower:]'
}

found=0
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue

  status=$(status_of "$gf")
  if [ "$status" = "in-progress" ]; then
    gid=$(grep -m1 -E '^\-\s*Goal ID:\s*' "$gf" | sed -E 's/^\-\s*Goal ID:\s*//' | sed -E 's/[[:space:]].*$//')
    [ -z "$gid" ] && gid="$base"
    lane=$(grep -m1 -E '^-\s*Agent lane\(s\):' "$gf" | sed -E 's/^-\s*Agent lane\(s\):\s*//' | sed 's/^[[:space:]]*//')
    echo "📝 $gid"
    [ -n "$lane" ] && echo "   Lane: $lane"
    echo ""
    found=$((found + 1))
  fi
done

if [ "$found" -eq 0 ]; then
  echo "No in-progress goals found."
  echo "  • Ready to dispatch: bash .kimi-code/skills/work-status/scripts/next.sh"
else
  echo "📊 Total in progress: $found"
fi
exit 0
