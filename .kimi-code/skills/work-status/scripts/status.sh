#!/usr/bin/env bash
# status.sh — goal/work-order status overview (Mia reporting).
# Adapted from automazeio/ccpm (MIT). Reads the factory goal tree.
# Usage: bash .kimi-code/skills/work-status/scripts/status.sh
set -u

# Resolve goals dir: governace/goals (S1 target) else goals (current)
GOALS_DIR=""
for cand in "governace/goals" "goals"; do
  if [ -d "$cand" ]; then GOALS_DIR="$cand"; break; fi
done
[ -z "$GOALS_DIR" ] && { echo "No goals directory found (checked governace/goals, goals)."; exit 0; }

# Extract the status vocabulary token (handles 'COMPLETE 2026-08-28 — ...'
# date suffixes and '**in-progress**' bold by matching the known vocabulary).
status_of() {
  grep -m1 -oiE '^\s*-\s*Status:\s*\**?(draft|approved|in-progress|blocked|done|complete|abandoned)' "$1" 2>/dev/null \
    | sed -E 's/.*Status:\s*\**//' \
    | tr '[:upper:]' '[:lower:]'
}

echo "📊 Factory Goal Status"
echo "======================"
echo "Source: $GOALS_DIR"
echo ""

total=0
declare -A counts
counts[draft]=0; counts[approved]=0; counts[in-progress]=0
counts[blocked]=0; counts[done]=0; counts[complete]=0; counts[abandoned]=0

for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue
  total=$((total + 1))
  status=$(status_of "$gf")
  [ -z "$status" ] && status="unknown"
  counts["$status"]=$((counts["$status"] + 1))
done

echo "Goals (total: $total)"
echo "  Draft:        ${counts[draft]}"
echo "  Approved:     ${counts[approved]}"
echo "  In progress:  ${counts[in-progress]}"
echo "  Blocked:      ${counts[blocked]}"
echo "  Done:         ${counts[done]}"
echo "  Complete:     ${counts[complete]}"
echo "  Abandoned:    ${counts[abandoned]}"
unknown=$((total - counts[draft] - counts[approved] - counts[in-progress] - counts[blocked] - counts[done] - counts[complete] - counts[abandoned]))
[ "$unknown" -gt 0 ] && echo "  (no status / other: $unknown)"

echo ""
echo "▶ Open work (not done/complete/abandoned): $((total - counts[done] - counts[complete] - counts[abandoned]))"
exit 0
