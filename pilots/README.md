# Pilots

One directory per pilot program: linked goal, plan, validation evidence, and
verdict. Created when the first pilot was approved (KDD-0003).

## Standard evidence package (slim, 2026-08-24)

Goal file (doubles as Intent and Authority Receipt), work order, context packet,
knowledge-review receipt, command log, sanitized raw evidence, audit report (test
matrix pre-registered in the same file, statuses filled during execution), state
log, gate decision, completion record (learning record only when learnings are
substantial), `sha256sums.txt` frozen once at the gate and re-frozen at close if
files changed. No separate test-plan or validation-summary files.

## Pilots

- `PILOT-KK3-JOHN-OLLAMA-AUDIT-001/` — read-only Ollama audit on hxs-5; first
  validation of goal-based Kimi-K3 + John orchestration. Status: plan adopted
  (KDD-0003), awaiting Agent-Zero authorization (readiness gate, plan section 19).
  Goal: `goals/2026-08-24-ollama-audit-hxs5.md`.
