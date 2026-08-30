#!/usr/bin/env bash
# claude-payload-shim.sh — payload translator for Claude Code hooks (KDD-0020).
#
# WHY THIS EXISTS
# The five repo hooks were written for Kimi Code, whose hook payload carries the
# edited file as the JSON key "path". They all extract it with:
#     sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p'
# Claude Code's payload names it "tool_input"."file_path" instead. The literal
# string "path" (with its opening quote) never appears in "file_path", so that
# sed matches nothing and every hook exits 0 immediately — a silent no-op, the
# worst failure mode for a guardrail. This shim translates one shape into the
# other so the governed hook scripts stay untouched and single-sourced.
#
# NOT FOR secret-boundary.sh: that hook greps the WHOLE payload for secret
# patterns (Write content, Edit new_string, Bash command), so it must receive
# Claude's raw payload unmodified. Register it directly, never through here.
#
# Usage (from .claude/settings.json):
#     scripts/hooks/claude-payload-shim.sh <target-hook-script>
#
# Fail-open, matching the hooks it wraps: any parse problem exits 0 silently.
# The target's exit status is propagated so a blocking target still blocks.
set -u

TARGET="${1:-}"
[ -z "$TARGET" ] && exit 0
[ -x "$TARGET" ] || exit 0

payload="$(cat 2>/dev/null || true)"
[ -z "$payload" ] && exit 0

# Emit {"path": "<file>"} with proper JSON escaping, or nothing when the payload
# carries no file path (e.g. a Bash tool call, which these hooks do not handle).
translated="$(printf '%s' "$payload" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
if not isinstance(d, dict):
    sys.exit(0)
ti = d.get("tool_input") if isinstance(d.get("tool_input"), dict) else {}
tr = d.get("tool_response") if isinstance(d.get("tool_response"), dict) else {}
p = ti.get("file_path") or ti.get("path") or tr.get("filePath") or ""
if isinstance(p, str) and p:
    sys.stdout.write(json.dumps({"path": p}))
' 2>/dev/null || true)"

[ -z "$translated" ] && exit 0

printf '%s' "$translated" | "$TARGET"
exit $?
