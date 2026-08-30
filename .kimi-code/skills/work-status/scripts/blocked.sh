#!/usr/bin/env bash
# blocked.sh — goals in a blocked state.
# Adapted from automazeio/ccpm (MIT). Reads the factory goal tree.
# Usage: bash .kimi-code/skills/work-status/scripts/blocked.sh
set -u

GOALS_DIR=""
for cand in "governace/goals" "goals"; do
  if [ -d "$cand" ]; then GOALS_DIR="$cand"; break; fi
done
[ -z "$GOALS_DIR" ] && { echo "No goals directory found."; exit 0; }

echo "🚫 Blocked Goals"
echo "================"
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
  if [ "$status" = "blocked" ]; then
    gid=$(grep -m1 -E '^\-\s*Goal ID:\s*' "$gf" | sed -E 's/^\-\s*Goal ID:\s*//' | sed -E 's/[[:space:]].*$//')
    [ -z "$gid" ] && gid="$base"
    # Optional: - Blocked by: <reason>
    reason=$(grep -m1 -E '^-\s*Blocked by:\s*' "$gf" | sed -E 's/^-\s*Blocked by:\s*//' | sed 's/^[[:space:]]*//')
    echo "⏸️ $gid"
    [ -n "$reason" ] && echo "   Blocked by: $reason"
    echo ""
    found=$((found + 1))
  fi
done

if [ "$found" -eq 0 ]; then
  echo "No blocked goals found."
else
  echo "📊 Total blocked: $found"
fi
exit 0
