# Issues and action items

One file until it hurts. Newest first. Date every entry. Close items with a
resolution note, never by deleting.

## Open

| Date | Item | Owner | Next action |
| ---- | ---- | ----- | ----------- |
| 2026-08-24 | Draft HX file-naming convention (no tool-name prefixes such as `codex_`) and apply it to new files going forward | the governor (via Mia) | Draft convention, record it in the repo conventions, then rename existing non-conforming files, e.g. `agents/john/codex_20260824_0205_ollama-directory-reconnaissance-inventory.md` |
| 2026-08-24 | D1: OmniRoute remote-consumption mechanism (open since 2026-08-14 per PILOT-002) | Agent-Zero | [RESOLVED — see Closed] |
| 2026-08-24 | D2: Ollama source baseline for hxs-4 — corpus has 0.32.11, installed is 0.32.9 | Agent-Zero | [RESOLVED — see Closed] |
| 2026-08-24 | D3: default-context contract — OLLAMA_CONTEXT_LENGTH=65536 did not change observed num_ctx default of 4096 | Agent-Zero | [RESOLVED — see Closed] |
| 2026-08-25 | M7b 24-hour soak (AC-008/AC-016) — deferred to backlog by owner directive; soak evidence absent = deferred, not waived; M8 acceptance scope adjusted accordingly | Agent-Zero | [RESOLVED — see Closed] |

## Closed

| Date | Item | Resolution |
| ---- | ---- | ---------- |
| 2026-08-24 | Possible OpenRouter API key in local doc `ox-alpha.md` | Owner confirmed the key is not exposed; local file left as-is, no action |
| 2026-08-29 | D1: OmniRoute remote-consumption mechanism (open since 2026-08-14 per PILOT-002) | OmniRoute deployed and owner-accepted (L1-M3 COMPLETE, KDD-0008); hxs-4 Chat-X deployed; D1 resolved — OmniRoute IS the remote-consumption mechanism |
| 2026-08-29 | D2: Ollama source baseline for hxs-4 — corpus has 0.32.11, installed is 0.32.9 | hxs-4 Chat-X (Qwen 3.5 9B) deployed via Ollama; source baseline discrepancy is historical — verify against live hxs-4 if a source-matched build is needed |
| 2026-08-29 | D3: default-context contract — OLLAMA_CONTEXT_LENGTH=65536 did not change observed num_ctx default of 4096 | LLM server blueprint (BLUEPRINT-llm-server.md §8) documents the downstream-consumer contract; num_ctx is set explicitly per workload in the Ollama model config |
| 2026-08-29 | M7b 24-hour soak (AC-008/AC-016) — deferred to backlog by owner directive | hxs-1 through hxs-4 are deployed and owner-accepted; M7b soak remains deferred per owner directive |
