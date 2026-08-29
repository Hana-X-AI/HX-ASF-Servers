#!/usr/bin/env bash
# agent-creation-check.sh — PostToolUse hook, fires on Write|Edit to agents/
# Checks that new agent directories have the required checklist items.
# Fail-open: warns only, never blocks.

set -euo pipefail

FILE="${1:-}"

# Only check files under agents/
case "$FILE" in
  agents/*)
    ;;
  *)
    exit 0
    ;;
esac

# Extract agent name from path (agents/<name>/...)
AGENT_NAME=$(echo "$FILE" | cut -d/ -f2)

# Skip if it's the _template directory
case "$AGENT_NAME" in
  _template|_templates)
    exit 0
    ;;
esac

# Check if this is a new agent (charter.md or profile.md being created)
case "$(basename "$FILE")" in
  charter.md|profile.md)
    ;;
  *)
    exit 0
    ;;
esac

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
MISSING=""

# Check charter exists
if [ ! -f "$REPO_ROOT/agents/$AGENT_NAME/charter.md" ]; then
  MISSING="$MISSING charter.md"
fi

# Check profile exists
if [ ! -f "$REPO_ROOT/agents/$AGENT_NAME/profile.md" ]; then
  MISSING="$MISSING profile.md"
fi

# Check roster entry
grep -q "|$AGENT_NAME " "$REPO_ROOT/agents/README.md" 2>/dev/null || MISSING="$MISSING roster(README.md)"

# Check AGENTS.md taxonomy
grep -q "$AGENT_NAME" "$REPO_ROOT/AGENTS.md" 2>/dev/null || MISSING="$MISSING AGENTS.md(taxonomy)"

# Check system-mapping
grep -q "$AGENT_NAME" "$REPO_ROOT/servers/system-mapping.md" 2>/dev/null || MISSING="$MISSING system-mapping"

# Check KDD exists
ls "$REPO_ROOT/governace/decisions/"KDD-*"$AGENT_NAME"*.md 2>/dev/null | head -1 >/dev/null 2>&1 || MISSING="$MISSING KDD"

# Check catalog records
ls "$REPO_ROOT/knowledge/catalog/documents/"DOC-agent-"$AGENT_NAME"*.yaml 2>/dev/null | head -1 >/dev/null 2>&1 || MISSING="$MISSING catalog(DOC-agent)"

if [ -n "$MISSING" ]; then
  echo "WARN: agent-creation-check: $AGENT_NAME may be missing:$MISSING" >&2
  echo "WARN: See governace/templates/agent-checklist.md for the full checklist." >&2
fi

exit 0
