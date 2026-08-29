# hxs-1 — Configuration

**Phase:** 1 (owner-accepted deployment)
**Configuration date:** 2026-08-27 (owner disposition #1)
**Discovery:** `discovery.md` (2026-08-11, COMPLETE)
**Authority:** `servers/SERVER-REGISTRY.md` hxs-1 row; owner disposition 2026-08-27 #1

## As-configured state

| Field | Value |
|---|---|
| Hostname | hxs-1 |
| IP | 192.168.50.200 |
| Role | Deep reasoning & synthesis (LLM server) |
| Model | Qwen 3.8 27B (`hx-qwen3.8-27b-64k`) |
| Status | READY — owner-accepted (disposition 2026-08-27 #1) |
| GPU | 2x NVIDIA RTX 4070 Ti SUPER, 16376 MiB each, 32752 MiB total |
| GPU driver | nvidia-driver-580-server-open, module 580.173.02 |
| CUDA | 13.0 (driver-reported) |
| Serving runtime | Ollama |
| Owner | john (Ollama lane) |
| Blueprint | `servers/BLUEPRINT-llm-server.md` |

## Notes

- Owner disposition 2026-08-27 #1 superseded the original "unreleased, slot
  reserved" registry entry — the model is deployed and owner-accepted.
- This configuration record is derived from the registry and discovery
  record, not a live host probe. A live probe can refresh these values
  under a governor-issued work order.
- Secure Boot: disabled (owner directive)
- No host firewall (owner rule 2026-08-26)
