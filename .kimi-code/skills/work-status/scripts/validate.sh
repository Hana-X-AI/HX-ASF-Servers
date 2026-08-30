#!/usr/bin/env bash
# validate.sh — goal-tree integrity: frontmatter, status values, orphan files.
# Adapted from automazeio/ccpm (MIT). Reads the factory goal tree.
# Usage: bash .kimi-code/skills/work-status/scripts/validate.sh
set -u

GOALS_DIR=""
for cand in "governace/goals" "goals"; do
  if [ -d "$cand" ]; then GOALS_DIR="$cand"; break; fi
done
[ -z "$GOALS_DIR" ] && { echo "No goals directory found."; exit 0; }

echo "🔍 Validating Goal Tree"
echo "======================="
echo "Source: $GOALS_DIR"
echo ""

errors=0
warnings=0
VALID_STATUS="draft approved in-progress blocked done complete abandoned"

# Extract the status vocabulary token (handles 'COMPLETE 2026-08-28 — ...'
# date suffixes and '**in-progress**' bold by matching the known vocabulary).
status_of() {
  grep -m1 -oiE '^\s*-\s*Status:\s*\**?(draft|approved|in-progress|blocked|done|complete|abandoned)' "$1" 2>/dev/null \
    | sed -E 's/.*Status:\s*\**//' \
    | tr '[:upper:]' '[:lower:]'
}

echo "📁 Directory:"
if [ -d "$GOALS_DIR" ]; then
  echo "  ✅ $GOALS_DIR exists"
else
  echo "  ❌ $GOALS_DIR missing"
  exit 0
fi
echo ""

echo "📝 Goal File Validation:"
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue

  gid=$(grep -m1 -E '^-\s*Goal ID:\s*' "$gf" | sed -E 's/^-\s*Goal ID:\s*//' | tr -d '[:space:]')
  [ -z "$gid" ] && { echo "  ⚠️ $base: missing 'Goal ID' field"; warnings=$((warnings + 1)); }

  status=$(status_of "$gf")
  if [ -z "$status" ]; then
    echo "  ⚠️ $base: missing 'Status' field"; warnings=$((warnings + 1))
  else
    ok=0
    for v in $VALID_STATUS; do [ "$status" = "$v" ] && ok=1; done
    [ "$ok" -eq 0 ] && { echo "  ⚠️ $base: invalid status '$status'"; warnings=$((warnings + 1)); }
  fi

  owner=$(grep -m1 -E '^-\s*Owner:\s*' "$gf" | sed -E 's/^-\s*Owner:\s*//' | tr -d '[:space:]')
  [ -z "$owner" ] && { echo "  ⚠️ $base: missing 'Owner' field"; warnings=$((warnings + 1)); }
done

echo ""
if [ "$warnings" -eq 0 ] && [ "$errors" -eq 0 ]; then
  echo "✅ Goal tree is healthy — all files have required frontmatter"
else
  echo "📊 Summary: $errors errors, $warnings warnings"
  echo "  Findings route to the governor for disposition (Mia reports, never fixes)"
fi
exit 0
