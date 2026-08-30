#!/usr/bin/env bash
# standup.sh — daily standup: today's activity, in-progress, next, stats.
# Adapted from automazeio/ccpm (MIT). Reads the factory goal tree.
# Usage: bash .kimi-code/skills/work-status/scripts/standup.sh
set -u

GOALS_DIR=""
for cand in "governace/goals" "goals"; do
  if [ -d "$cand" ]; then GOALS_DIR="$cand"; break; fi
done
[ -z "$GOALS_DIR" ] && { echo "No goals directory found."; exit 0; }

# Extract the status vocabulary token (handles 'COMPLETE 2026-08-28 — ...'
# date suffixes and '**in-progress**' bold by matching the known vocabulary).
status_of() {
  grep -m1 -oiE '^\s*-\s*Status:\s*\**?(draft|approved|in-progress|blocked|done|complete|abandoned)' "$1" 2>/dev/null \
    | sed -E 's/.*Status:\s*\**//' \
    | tr '[:upper:]' '[:lower:]'
}

echo "📅 Daily Standup - $(date '+%Y-%m-%d')"
echo "================================"
echo ""

echo "📝 Today's Activity (files modified in the last 24h):"
echo "===================================================="
recent=$(find "$GOALS_DIR" -name "*.md" -mtime -1 2>/dev/null)
if [ -n "$recent" ]; then
  changed=$(printf '%s\n' "$recent" | grep -cvE 'README|_template' || true)
  echo "  • $changed goal file(s) touched in the last 24h"
else
  echo "  No goal activity recorded today"
fi
echo ""

echo "🔄 Currently In Progress:"
echo "========================="
ip=0
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue
  status=$(grep -m1 -E '^-\s*Status:\s*' "$gf" | sed -E 's/^-\s*Status:\s*//' | tr -d '[:space:]')
  if [ "$status" = "in-progress" ]; then
    gid=$(grep -m1 -E '^\-\s*Goal ID:\s*' "$gf" | sed -E 's/^\-\s*Goal ID:\s*//' | sed -E 's/[[:space:]].*$//')
    [ -z "$gid" ] && gid="$base"
    echo "  • $gid"
    ip=$((ip + 1))
  fi
done
[ "$ip" -eq 0 ] && echo "  (none)"
echo ""

echo "⏭️ Ready Next:"
echo "=============="
next=0
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue
  status=$(status_of "$gf")
  if [ "$status" = "approved" ] || [ -z "$status" ]; then
    gid=$(grep -m1 -E '^-\s*Goal ID:\s*' "$gf" | sed -E 's/^-\s*Goal ID:\s*//' | tr -d '[:space:]')
    [ -z "$gid" ] && gid="$base"
    echo "  • $gid"
    next=$((next + 1))
    [ "$next" -ge 3 ] && break
  fi
done
[ "$next" -eq 0 ] && echo "  (none)"
echo ""

echo "📊 Quick Stats:"
echo "==============="
total=0; done_c=0; blocked_c=0
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue
  total=$((total + 1))
  status=$(status_of "$gf")
  if [ "$status" = "done" ] || [ "$status" = "complete" ]; then
    done_c=$((done_c + 1))
  fi
  [ "$status" = "blocked" ] && blocked_c=$((blocked_c + 1))
done
echo "  Goals: $total total, $done_c done, $blocked_c blocked"
exit 0
