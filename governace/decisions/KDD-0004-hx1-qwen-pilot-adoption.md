# KDD-0004: Adopt the HX-1 Qwen pilot with qwen3.8:27b as the approved baseline

- Date: 2026-08-24
- Status: ratified
- Decider: Agent-Zero
- Related goals: `goals/2026-08-24-hx1-ollama-qwen38-27b.md`

## Context

A production-grade pilot plan (767 lines) for deploying a Qwen 27B-class model on
hxs-1 via Ollama was reviewed against SERVER-REGISTRY, the live Ollama library, a
live pre-flight of hxs-1, and PILOT-002 evidence. The plan's executive decision
proposed `qwen3.5:27b` on the grounds that the requested tags were invalid. Live
verification on 2026-08-24 showed `qwen3.5:27b`, `qwen3.5:27b-mlx`, `qwen3:30b`,
and `qwen3.8:27b` all exist — and the registry's ratified hxs-1 workload ("Qwen 3.8
27B — unreleased, slot reserved", 2026-08-13) is now released.

## Options considered

1. Adopt with `qwen3.5:27b` per the document — rejected: deviates from the ratified
   registry workload and would require a later registry amendment.
2. Adopt with `qwen3.8:27b` — chosen: matches the ratified registry role, newest
   available tag, no registry amendment needed.
3. Hold adoption until agent naming, quality thresholds, and SLO were settled —
   rejected: adoption proceeds with those recorded as proposed-pending; only the
   model choice blocked alignment.

## Decision

Adopt the pilot at `pilots/PILOT-HX1-OLLAMA-QWEN27B-001/plan.md` with
`qwen3.8:27b` (non-MLX, GGUF) as the approved baseline, and these amendments:

- Executive decision rewritten for the approved baseline with live tag evidence.
- Phase M dispatch note (governor runs no probes; specialists execute as
  profile-briefed sub-agents).
- Host table populated with the 2026-08-24 pre-flight evidence.
- Context-length evidence note from PILOT-002 (Modelfile `num_ctx` is the contract;
  the drop-in variable may be inert).
- Open-decisions table: model and TKV paths resolved; agent naming resolved as
  roster names with pilot call signs (Esme=john, KK3=kimi-k3); quality thresholds
  and readiness SLO recorded as proposed-pending owner confirmation.
- Goal file created at `goals/2026-08-24-hx1-ollama-qwen38-27b.md`.

Execution (M0) is NOT authorized by this KDD; it is the first mutating pilot and
starts on explicit owner instruction. Each cold reboot is individually approved.

## Consequences

- Registry and pilot are aligned on `qwen3.8:27b`; no registry amendment required.
- `qwen3.5:27b` remains available as a fallback candidate if the pilot discovers a
  blocking defect in `qwen3.8:27b`; switching requires a KK3 gate decision.
- Proposed quality thresholds and SLO must be confirmed by the owner before M5/M4
  respectively.

## Provenance

- Source document:
  `/home/hxsa/opt/local-tkv/agent-zero-docs/pilots/qwen/codex_20260824_1945_hx-1-ollama-qwen-27b-pilot-project.md`
  (767 lines), SHA-256
  `cbe90fb04fbe16e17aecfc2e175ec49b0fea0b477113021063d76ac8058342b7`.
- Evidence reviewed: source in full; SERVER-REGISTRY; ollama.com library tag checks
  (live); hxs-1 pre-flight (live, 2026-08-24); PILOT-002 audit evidence.
