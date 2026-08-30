#!/usr/bin/env bash
# validate.sh — goal-tree integrity: frontmatter, status values, orphan files.
# Adapted from automazeio/ccpm (MIT). Reads the factory goal tree.
# Usage: bash .agents/skills/work-status/scripts/validate.sh
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

# active_record_of — emit only the goal file's ACTIVE record, excluding the
# labeled historical/correction spans ([OPEN CORRECTION], [LABELED CORRECTION],
# [HISTORICAL], [AMENDMENT]). Append-only history must NOT feed the blocking
# dependency/orphan calculations — references inside those blocks are historical
# provenance, not active links.
active_record_of() {
  perl -0777 -pe 's/\[(?:OPEN CORRECTION|LABELED CORRECTION|HISTORICAL|AMENDMENT)[^][]*(?:\[[^][]*\][^][]*)*\]//g' "$1" 2>/dev/null
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

# Dependency reference check: goal-to-goal references must resolve. Only
# references that point INTO the goal tree (governace/goals/... or goals/...)
# are goal dependencies — references to servers/..., pilots/..., etc. are
# evidence/plan docs, not goal links, and are not validated here.
echo "🔗 Dependency Reference Validation:"
declare -A GOAL_FILES
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue
  GOAL_FILES["$base"]=1
done
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue
  # Only goal-tree path references in the ACTIVE record count as goal
  # dependencies — references inside labeled historical/correction blocks are
  # append-only provenance and must not feed this check.
  refs=$(active_record_of "$gf" | grep -oE "governace/goals/[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+\.md|goals/[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+\.md" 2>/dev/null | sed -E 's#^.*/##' | sort -u)
  [ -z "$refs" ] && continue
  while IFS= read -r r; do
    [ -z "$r" ] && continue
    [ "$r" = "$base" ] && continue
    if [ -z "${GOAL_FILES[$r]+x}" ]; then
      echo "  ❌ $base: references missing goal file '$r'"
      errors=$((errors + 1))
    fi
  done <<< "$refs"
done

# Orphan check (informational): a goal file not referenced by any other goal is
# a disconnected record. Reported as a WARNING, not a failure — in this tree
# most goals are intentional roots with no incoming edge, so disconnection alone
# does not break the healthy summary.
echo "📭 Orphan File Validation:"
orphans=0
for gf in "$GOALS_DIR"/*.md; do
  [ -f "$gf" ] || continue
  base=$(basename "$gf")
  [ "$base" = "README.md" ] && continue
  [ "$base" = "_template.md" ] && continue
  referenced=0
  for ogf in "$GOALS_DIR"/*.md; do
    [ -f "$ogf" ] || continue
    obase=$(basename "$ogf")
    [ "$obase" = "$base" ] && continue
    [ "$obase" = "README.md" ] && continue
    [ "$obase" = "_template.md" ] && continue
    # Only ACTIVE-record references count — a historical/correction-only
    # mention must not mark the goal as non-orphan.
    if active_record_of "$ogf" | grep -qE "governace/goals/${base}|goals/${base}" 2>/dev/null; then
      referenced=1
      break
    fi
  done
  if [ "$referenced" -eq 0 ]; then
    echo "  ⚠️ $base: orphan (not referenced in any other goal's active record)"
    orphans=$((orphans + 1))
  fi
done
[ "$orphans" -eq 0 ] && echo "  ✅ No orphan goal files"

echo ""
if [ "$errors" -eq 0 ]; then
  if [ "$warnings" -eq 0 ] && [ "$orphans" -eq 0 ]; then
    echo "✅ Goal tree is healthy — frontmatter valid, no broken references, no orphans"
  else
    echo "📊 Summary: $errors errors, $warnings warnings, $orphans orphans (informational)"
    echo "  Findings route to the governor for disposition (Mia reports, never fixes)"
  fi
  exit 0
else
  echo "📊 Summary: $errors errors, $warnings warnings, $orphans orphans"
  echo "  Findings route to the governor for disposition (Mia reports, never fixes)"
  exit 1
fi
