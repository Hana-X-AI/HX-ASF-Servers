# hxs-2 — Configuration

**Phase:** 1 (ready)
**Configuration date:** 2026-08-13 (registry baseline)
**Discovery:** `discovery.md` (2026-08-12, COMPLETE)
**Authority:** `servers/SERVER-REGISTRY.md` hxs-2 row

## As-configured state

| Field | Value |
|---|---|
| Hostname | hxs-2 |
| IP | 192.168.50.201 |
| Role | Coding (LLM server) |
| Model | Qwen2.5-Coder-32B, AWQ Int4, TP=2, max-model-len 16–24K |
| Status | READY |
| GPU | 2x RTX 5060 Ti, 16311 MiB each, 32622 MiB total |
| GPU driver | NVIDIA (installed per directive) |
| Serving runtime | Ollama |
| Owner | john (Ollama lane) |
| Blueprint | `servers/BLUEPRINT-llm-server.md` |

## Notes

- [Labeled note 2026-08-29: D3 artifact (mannix/qwen3.6-27b-a3b-coderx:vision-Q4_K_M)
  superseded by owner deployment decision; deployed model is Qwen2.5-Coder-32B
  AWQ Int4 per SERVER-REGISTRY. The D3 decision is preserved in the goal file
  and git history.]
- This configuration record is derived from the registry and discovery
  record, not a live host probe. A live probe can refresh these values
  under a governor-issued work order.
- Secure Boot: disabled (owner directive)
- No host firewall (owner rule 2026-08-26)
