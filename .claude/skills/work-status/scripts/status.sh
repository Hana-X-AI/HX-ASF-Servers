#!/usr/bin/env bash
# status.sh — goal/work-order status overview (Mia reporting)
# THIN WRAPPER. All goal-state parsing lives in scripts/work_state.py (O1); this
# script must never reimplement it. Before consolidation, work-status and
# goal-decompose each grepped goal prose with their own regex and both were
# wrong: a COMPLETE goal recorded in an append-only correction block parsed as
# <none>, and a goal completed in its pilot state log still read "in-progress".
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
exec python3 "$ROOT/scripts/work_state.py" status "$@"
