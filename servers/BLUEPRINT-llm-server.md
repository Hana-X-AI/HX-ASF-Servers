# BLUEPRINT — LLM Server Configuration (owner standing instruction, 2026-08-26)

> hxs-1 is the proven blueprint; hxs-2 joins it at its M8. Every future LLM
> server deployment follows this blueprint instead of re-deriving configuration.
> Some of this configuration **directly shapes how other ecosystem components are
> configured at deployment** — see §8, the downstream-consumer contract. Retrieve
> this document before designing anything that consumes an HX LLM endpoint.
> Owner instruction 2026-08-26; governor-maintained; cataloged per convention.

## 1. Identity plane

- Registry assigns the role and workload (`SERVER-REGISTRY.md`); the server
  records contract governs: `discovery.md` (as-found, preserved) →
  `configuration.md` (as-configured, at sign-off).
- Model identity = **exact tag + full local digest**, frozen at acceptance.
  Aliases follow `hx-<model>-<ctx>k` profile naming with digest equality proven;
  ambiguous bare aliases are retired, never left floating.
- Baseline sampling = **native defaults** (the A01 rule): no sampling parameters
  in the Modelfile unless measured evidence justifies them; thinking ON.

## 2. OS plane

- Ubuntu 24.04 LTS, HWE kernel; NVIDIA driver 580.173.02 retain-and-validate
  with DKMS for every installed kernel; suspend targets masked (×4); Secure
  Boot disabled (standing, never enable); Wi-Fi formalized as an rfkill soft
  block with boot persistence (systemd-rfkill), inverse documented.
- Model store on root ext4 (blueprint default); storage headroom recorded.

## 3. Service plane

- Ollama pinned install; `ollama.service` + `ollama-preload.service`.
- Preload contract: bounded API probes (~208 s) → single-attempt model load
  (`--max-time 300`) → exact alias+digest `/api/ps` assertion (`--max-time 30`);
  unit `TimeoutStartSec=600`; script worst-case ≤ 538 s — always under the 900 s
  D5 recovery SLO. `OLLAMA_NO_CLOUD=1`.
- Admission control: `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`.

## 4. Context plane

- Ladder runs on the **exact digest** — never transfer another model's results
  (CX-R13). Baked/default first, then the target rung with capacity + latency
  evidence. hxs-1 proof points: 32K recovery baseline, 64K operating, 128K
  qualified extended (explicitly selected); KV measured f16, exactly linear
  (45,056 B/token there — re-measure per model).
- Effective context is proven by `/api/ps context_length`, not configuration
  claims (SC-08 pattern).

## 5. Exposure plane (as amended 2026-08-26, owner directive)

- **Fleet-scoped LAN**: `OLLAMA_HOST=0.0.0.0` with loopback preserved (preload
  and fixtures depend on 127.0.0.1). Reachability is limited to the private LAN
  (192.168.50.0/24); the LAN itself is the boundary — **no host firewalls (ufw
  or equivalent) anywhere on HX hosts** (owner rule 2026-08-26). No service-layer
  auth; no component may widen the boundary (gateway, port-forward, external
  exposure) without an owner decision. (Supersedes the original loopback-only
  posture — SC-07a on the hxs-1 goal; the brief ufw enablement of 2026-08-26 was
  reverted the same day under this rule.)
- **Web search vs cloud models — the honest enforcement shape** (2026-08-26,
  review batch 12): web search is enabled fleet-wide (owner decision; NO_CLOUD
  removed — verified `disable_ollama_cloud` absent from `~/.ollama/server.json`
  and `/usr/share/ollama/.ollama/server.json` on all hosts at enablement; that
  file is inspected at every future cloud-state change and any modification to
  it requires owner authorization plus a rollback note). **There is no
  config-level flag that permits web search while denying cloud-model remote
  inference** — Ollama's only class switch is NO_CLOUD (verified against
  `envconfig/config.go`; `:cloud` gating is name-suffix filtering, not an
  allowlist). What actually enforces "no cloud models": (1) store policy — no
  `:cloud` tag is ever pulled, created, or aliased, and any appearance in a
  store, a catalog backend record, or `ollama list` output is an automatic
  finding with escalation; (2) process — pulling or running any `:cloud` model
  is an operator-level action requiring an explicit owner-directed work order,
  journaled at the host; (3) the residual surface is named honestly: the
  LAN-open Ollama API (including `/api/pull`) has no caller authorization, so a
  LAN client could attempt a cloud pull — the monitoring rule above is the
  tripwire until an authenticating gateway (owner decision) fronts the
  backends. Web search queries themselves leave the LAN to Ollama's cloud by
  owner acceptance.

## 6. Recovery plane

- D5 SLO: detect ≤ 2 min, recover ≤ 15 min, one bounded attempt. Boot-to-ready
  budget < 900 s; measured 56–60 s at hxs-1 (incl. an unplanned power-cut proof).
  `NRestarts=0` expectation; rollback = smallest affected layer (13-esme layers
  A–D) + kernel GRUB previous-entry path.

## 7. Validation plane

- Alias-parameterized fixtures (required per run; preflight verifies the alias):
  coding, tool (schema/denial/adversarial), needle/retrieval, and vision where
  qualified. Owner confirms quality thresholds before the suite runs.
- Recovery proof: service restart + 3 cold reboots (per-cycle owner approval),
  warm known-answer per cycle.

## 8. Downstream-consumer contract (deployment-shaping facts)

**Fleet capability call-signs** (owner, 2026-08-26). Every LLM backend carries a
capability-level call-sign, resolved through its Second Brain
backend-capability record — never a bare Ollama tag (the bare-alias ambiguity
was retired on hxs-1). Status `candidate` until the host's M8 sign-off. **The
X in a call-sign is always capital** (owner, 2026-08-26).

| Call sign | Host (IP) | Backend | Endpoint | Model profile alias | Catalog record |
| --- | --- | --- | --- | --- | --- |
| **Qwen-X** | hxs-1 (192.168.50.200) | Deep reasoning & synthesis — Qwen 3.8 27B | `http://192.168.50.200:11434` | `-64k` operating (resident); `-32k` recovery; `-128k` extended | `DOC-backend-qwen-x` (active) |
| **Coder-X** | hxs-2 (192.168.50.201) | Coding inference — Qwen3.6-27B-A3B CoderX | `http://192.168.50.201:11434` | `hx-qwen3.6-coderx-64k` operating (resident); `-32k` baseline; `-128k` extended (all frozen 2026-08-26, needle-proven) | `DOC-backend-coder-x` (candidate) |
| **Meta-X** | hxs-3 (192.168.50.202) | Tooling agent — Muse Glimmer 30B | `http://192.168.50.202:11434` | `hx-muse-glimmer-64k` operating (resident); `-32k` baseline; `-128k` extended (all frozen 2026-08-26, needle-proven) | `DOC-backend-meta-x` (candidate) |
| **Chat-X** | hxs-4 (192.168.50.203) | Basic chat utility — Qwen 3.5 9B | loopback-only today (LAN posture per owner decision) | `hx-qwen3.5-9b-64k` default reference; `-32k` baseline (**A-1: needle-proven to 89.5% — thinking-model headroom, not ~95%**); `-128k` extended (frozen 2026-08-26) | `DOC-backend-chat-x` (active — owner-provisioned, not pilot-track) |

`Chat-X` is owner-provisioned and working (2026-08-26): qwen3.5:9b-q4_K_M
resident on demand, ctx 65536, loopback-only, idle-unloads (no preload yet).
Blueprint alignment items (version pin to 0.32.15, preload/persistence, LAN
posture, qualification) apply when the role grows beyond basic chat — owner
decision at that time.

Consumers address backends by call-sign and resolve endpoint + profile + limits
from the catalog record behind it.

**Picker FAQ — the "Recommended" row (2026-08-26, source-verified).** The
interactive picker's Recommended section is upstream content **compiled into
the Ollama binary**, not local state: a server-fed list with a hardcoded
fallback (`cmd/launch/models.go`). `OLLAMA_NO_CLOUD=1` filters it to local
entries — in 0.32.15 that is `gemma4` and `qwen3.5`; older binaries (0.32.9)
show older or no recommendations. The row is **not installed, not governed,
and not a finding** — it is the picker's own advertising, marked
"(not downloaded)" by upstream. Judge hosts only by `ollama list` and the
catalog. Ignore the row permanently; there is no config flag to suppress it.

Ecosystem components (gateways, routers, agent presets, clients) MUST configure
from this section and the live catalog record — never from assumptions or
hardcoded values:

- **Endpoint**: `http://<host-ip>:11434` (Ollama API: `/api/generate`,
  `/api/chat`, `/api/ps`, `/api/tags`). Reachable only from 192.168.50.0/24.
  No service-layer auth; the network scope IS the boundary — no component may
  widen it (gateway, port-forward, or external exposure) without an owner
  decision.
- **Model reference**: always the hx profile alias (which pins digest + ctx);
  never upstream tag names, never `:latest`.
- **Context**: clients do NOT send `num_ctx` (the server profile governs);
  budget prompt + thinking + output inside the profile's context (64K
  operating default).
- **keep_alive**: never send `keep_alive: 0` (that unloads the model). The
  server preloads with `keep_alive: -1` (Forever) at boot only.
- **Timeouts**: connect 5 s; read/inference 900 s; first-content 240 s for
  extended-context profiles (cold deep ingest ≈158 s at 128K). Track warm vs
  cold latency separately; progress telemetry required so slow ingest is not
  misread as a hang.
- **Concurrency**: serialize consumer requests (server admits one at a time).
- **Capabilities**: thinking ON by default; tool calling per model validation;
  vision only where explicitly qualified (hxs-2: deferred per D8).
- **Registration**: every LLM server carries a backend-capability record in the
  Second Brain catalog (endpoint, exact tag + digest, capabilities, runtime
  profile, health/evidence contracts, owner). Consumers resolve endpoints from
  the catalog — the catalog is the capability registry (KDD-0005/0006).

## 9. Change management

- Blueprint-level changes are versioned work orders with evidence and rollback
  (post-closure changes follow the SC-07a pattern: living records amended with
  provenance, signed evidence preserved).
- This blueprint updates at each new LLM-host sign-off (hxs-2 at its M8) and
  when a consumer-integration lesson earns a place in §8.

## Provenance

hxs-1 pilot package (M0–M8, closed PASS 2026-08-26); hxs-1 exposure change
(owner directive 2026-08-26); owner standing instruction 2026-08-26 (blueprint
and downstream impact). Catalog record: `DOC-blueprint-llm-server` (registered;
§8 record-ID column live 4/4).
