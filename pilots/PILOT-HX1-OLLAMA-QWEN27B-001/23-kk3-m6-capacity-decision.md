# M6 Capacity Decision Record — KK3 gate

| Field | Value |
|---|---|
| Decision | **REVISION 2 (owner directive 2026-08-25) governs — see Revision 2: three qualified context profiles** |
| v1 (superseded) | Freeze `num_ctx 131,072` as the single operating context, conditional on M7; fallback 65,536 — superseded before execution by the owner's profile disposition |
| Authority | plan §8 M6 (KK3 gate); plan §12 context gate; owner directive 2026-08-25 (Alert 1 EAM: 128K into the decision); goal SC-03; A01 §4.3 extended-experiment owner approval |
| Decided by | Kimi-K3 (governor), 2026-08-25 |
| Evidence | `22-esme-m6-capacity-ladder.md` (ladder matrix), `19-esme-m5b-amendment-conformance.md` (32K acceptance), `16-esme-m5-validation.md` (sampled-profile comparison) |

## Ladder results (all rungs: f16 KV, Phase A native sampling, 100% GPU, zero CPU fallback, swap 0)

| Measure | 32,768 (frozen baseline) | 65,536 | 131,072 |
|---|---|---|---|
| Resident | 17.68 GiB | 19.06 GiB | 21.81 GiB (~4.4 GiB headroom) |
| Needle @ ~95% depth | 30,015 tok (91.6%) — found, `stop` (M5b Phase A, per `22-esme-m6-capacity-ladder.md`) | 62,255 tok — found, `stop` | 124,395 tok — found, `stop` |
| D8 quality (AC-010/011/012/013) | PASS | PASS — identical | PASS — identical |
| Warm decode | 51.6–53.7 tok/s | 50.4–55.9 tok/s | 47.5–51.6 tok/s |
| Deepest TTFT-content | 17.4 s @31K | 19.6 s @62K | 59.6 s cache-assisted / ≈158 s cold @124K |
| Cold prefill at depth | ~1,304 tok/s @31K | 1,103.9 tok/s @62K | 786.0 tok/s @124K |
| GPU peaks | ≤64 °C, ≤197 W | ≤71 °C, ≤204 W | ≤74 °C, ≤206 W (of 285 W cap) |
| Xid/OOM | none | none | none |
| KV cache growth | 45,056 B/token, exactly linear (f16) | — | — |

> Correction 2026-08-25 (review finding): the 32K needle cell previously read 31,239 tok — that was the M5 sampled-profile measurement; the ratified Phase A baseline figure is 30,015 tok (M5b), now shown above. Source: `22-esme-m6-capacity-ladder.md` consolidated matrix.

## Rationale

1. Capacity holds at every rung with deterministic, linear KV growth; 128K leaves ~4.4 GiB static headroom (residency is static: `OLLAMA_NUM_PARALLEL=1`, `MAX_LOADED_MODELS=1`).
2. Quality is flat across all rungs — the larger window costs nothing in measured accuracy and serves the pilot's repository-scale coding and RAG objectives.
3. The performance cost is confined to deep-context ingest latency; the goal ranks quality first and latency second.
4. 24-hour stability and boot recovery are unproven at 128K — hence conditional on M7, with the documented fallback.

## Constraints carried forward — REVISION 1 content, SUPERSEDED by Revision 2 below

> The 131,072 operating directive and its fallback in this section are v1, superseded 2026-08-25 by Revision 2: M7 ratifies the always-on 65,536 operating profile; 128K is qualified for explicit selection. Items not about the operating context (262K/1M prohibition, vision-out, Phase A sampling) still stand.

- 262,144 and 1,000,000 remain unauthorized (A01 §4.3); F-M6-5's 262K extrapolation (~29.3 GB) is inference only, untested.
- Vision remains out of the baseline. Phase A native sampling only.
- Configuration to ratify for M7: Phase A Modelfile at `num_ctx 131072` (stage digest `94b83a1e…0dad0260`), `hx1.conf` `OLLAMA_CONTEXT_LENGTH=131072`, `OLLAMA_KV_CACHE_TYPE=f16` — applied as a versioned change at M7 start (host currently restored to the frozen 32K baseline).
- M7 entry conditions: rick pre-M7 session (Wi-Fi disable per owner directive, A01 §7 frozen-build readiness confirmation, NVRM assertion review); exclusive qualification window (F-M6-3 — foreign local client from 192.168.50.220 seen during M6); three individual owner reboot approvals.

## Fallback triggers (M7)

Any OOM, Xid, unexplained GPU→CPU offload, unexplained unload, or restart loop attributable to the 128K configuration → revert to 65,536 and re-run the affected M7 leg (one bounded correction per plan §8).

---

## Revision 2 — owner directive, 2026-08-25 (three qualified profiles)

The owner ratified the ladder evidence and set the architectural disposition below.
Revision 1 is superseded before execution.

### Profile dispositions

| Context | Disposition | Profile alias |
|---|---|---|
| 32,768 | **Frozen, ratified recovery/reference baseline** | `hx-qwen3.8-27b-32k` |
| 65,536 | **Preferred general-purpose operating profile** (always-on default) | `hx-qwen3.8-27b-64k` |
| 131,072 | **Qualified extended-context profile** — explicitly selected, not the universal default | `hx-qwen3.8-27b-128k` |
| 262,144 | Still unproven and outside the current pilot | — |

### Precision of the evidence claim (owner-mandated wording)

The ladder evidence proves that 131,072 caused **no measured accuracy regression in
the needle test and the D8 suites** — not that 128K can never affect accuracy across
every workload. All downstream claims use this sentence's scope.

### Host identity declaration

HX-1 (pilot project designation) and `hxs-1` (authoritative hostname,
192.168.50.200) are the same machine. All host-scoped assertions in this package
refer to `hxs-1`; the authoritative hostname is used in evidence artifacts.

### Harness requirements for the 128K profile (owner-ratified)

1. First-content timeout comfortably above the measured ~158 s cold deep-ingest —
   initially **240 s**; total request timeout sized for ingest + reasoning +
   generation.
2. Progress telemetry so slow ingestion is not misclassified as a hung model.
3. Admission control preventing concurrent deep-context requests from consuming the
   remaining VRAM margin (server side already serialized:
   `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`).
4. Warm-cache and cold-cache latency tracked separately.

### Supersessions recorded

- A01 §4.3's 131,072 row: promoted by the owner from "separate experiment" to
  qualified extended-context profile.
- A01 §4.4's bare-alias monitoring identity (`hx-qwen3.8-27b`): superseded by the
  profile-named aliases; preload and monitoring assertions reference the active
  profile alias (default `hx-qwen3.8-27b-64k`).
- M6 v1 single-context freeze: superseded as noted above.

### M7 implication

M7 (24-hour soak + three owner-approved cold reboots) validates the always-on
service at the **65,536 operating profile** (the resident default), including
boot-ordered preload of `hx-qwen3.8-27b-64k`. The 32K and 128K profiles remain
qualified on the ladder evidence; profile-switch mechanics (explicit selection of
the 128K profile) are verified as part of M7 evidence. Fallback if M7 shows
operating-profile instability: 32K recovery baseline, per the original fallback
logic.

### Evidence

Unchanged: `22-esme-m6-capacity-ladder.md` (ladder matrix),
`19-esme-m5b-amendment-conformance.md`, `16-esme-m5-validation.md`.
