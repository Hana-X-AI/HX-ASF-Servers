# GOAL-DSH-IMPL-001 — DeepSeek Harness full implementation

- Status: active — commissioned 2026-08-28 (owner-approved plan)
- Owner: Agent Zero · Governor: Kimi-K3
- Plan (controlling): `agent-zero-docs/projects/Deepseek/2026-08-28-dsh-full-implementation-plan.md`

## Contract

Complete, full-feature/capability install of DeepSeek Harness (`dsh` 0.1.1-rc.2,
pinned source `/opt/tkv-local/deepseek-harness-master`) as the HX agent harness,
on hxs-15. Morpheus builds and repairs (KDD-0009); Gordon qualifies independently
(KDD-0010), pipelined in parallel; the governor reviews Gordon's evidence and
signs off each phase; the owner holds the checkpoint before install and the
cutover word at close.

## Phases

- **Phase A — Baseline:** runtime core + CLI + OmniRoute routing (Gordon Gates 0–5).
- **Phase B — Intermediate:** agent workflow + web UI + integration surfaces
  (Gates 6–7).
- **Phase C — Advanced:** interop, sandboxing, remote + experimental, platform
  proof (Gates 8–10).
- **Close:** operations cutover on the owner's word, rollback exercised.

## Boundaries

- No deployment sandbox; no staging documents beyond this goal + the state log.
- Codification of HX conventions into dsh: OUT of this arc (owner 2026-08-28).
- Carol frozen (owner 2026-08-28): catalog pauses; the state log is the
  authoritative record.
- Local-model-first: no cloud keys or external services without explicit owner
  word (e2b / web-search rows disposition accordingly).
- rr zero-tolerance gate reviews every push.
