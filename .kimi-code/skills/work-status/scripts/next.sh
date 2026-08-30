#!/usr/bin/env bash
# next.sh — goals ready to be picked up next (approved, not started).
# Adapted from automazeio/ccpm (MIT). Reads the factory goal tree.
# Usage: bash .kimi-code/skills/work-status/scripts/next.sh
set -u

GOALS_DIR=""
for cand in "governace/goals" "goals"; do
  if [ -d "$cand" ]; then GOALS_DIR="$cand"; break; fi
done
[ -z "$GOALS_DIR" ] && { echo "No goals directory found."; exit 0; }

echo "📋 Next Available Goals"
echo "======================="
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
  # Ready = approved (scope-lock confirmed, awaiting dispatch) or no status set
  if [ "$status" = "approved" ] || [ -z "$status" ]; then
    gid=$(grep -m1 -E '^\-\s*Goal ID:\s*' "$gf" | sed -E 's/^\-\s*Goal ID:\s*//' | sed -E 's/[[:space:]].*$//')
    [ -z "$gid" ] && gid="$base"
    lane=$(grep -m1 -E '^-\s*Agent lane\(s\):' "$gf" | sed -E 's/^-\s*Agent lane\(s\):\s*//' | sed 's/^[[:space:]]*//')
    echo "✅ Ready: $gid"
    [ -n "$lane" ] && echo "   Lane: $lane"
    echo ""
    found=$((found + 1))
  fi
done

if [ "$found" -eq 0 ]; then
  echo "No approved/ready goals found."
  echo "  • Check blocked: bash .kimi-code/skills/work-status/scripts/blocked.sh"
  echo "  • Check in progress: bash .kimi-code/skills/work-status/scripts/in-progress.sh"
else
  echo "📊 Summary: $found goal(s) ready to dispatch"
fi
exit 0
