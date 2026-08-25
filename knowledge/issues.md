# Issues and action items

One file until it hurts. Newest first. Date every entry. Close items with a
resolution note, never by deleting.

## Open

| Date | Item | Owner | Next action |
| ---- | ---- | ----- | ----------- |
| 2026-08-24 | Draft HX file-naming convention (no tool-name prefixes such as `codex_`) and apply it to new files going forward | Kimi-K3 | Draft convention, record it in the repo conventions, then rename existing non-conforming files, e.g. `agents/john/codex_20260824_0205_ollama-directory-reconnaissance-inventory.md` |
| 2026-08-24 | D1: OmniRoute remote-consumption mechanism (open since 2026-08-14 per PILOT-002) | Agent-Zero | Decide the mechanism; required before any network exposure of hxs-4 Ollama |
| 2026-08-24 | D2: Ollama source baseline for hxs-4 — corpus has 0.32.11, installed is 0.32.9 | Agent-Zero | Acquire 0.32.9-matched source or authorize a deliberate pinned upgrade |
| 2026-08-24 | D3: default-context contract — OLLAMA_CONTEXT_LENGTH=65536 did not change observed num_ctx default of 4096 | Agent-Zero | Document the contract: num_ctx set explicitly per workload |
| 2026-08-25 | M7b 24-hour soak (AC-008/AC-016) — deferred to backlog by owner directive; soak evidence absent = deferred, not waived; M8 acceptance scope adjusted accordingly | Agent-Zero | Owner's word to schedule; do not raise proactively |

## Closed

| Date | Item | Resolution |
| ---- | ---- | ---------- |
| 2026-08-24 | Possible OpenRouter API key in local doc `ox-alpha.md` | Owner confirmed the key is not exposed; local file left as-is, no action |
