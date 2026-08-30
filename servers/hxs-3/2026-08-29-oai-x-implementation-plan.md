# hxs-3 — OAI-X implementation plan (PLANNING ONLY — NOT EXECUTED)

| Field | Value |
| --- | --- |
| Product of | Goal `governace/goals/2026-08-29-oai-x-replace-meta-x.md` (draft, 2026-08-29) — this plan operationalizes it |
| Author | Flash (governor) — planning only; no execution, no hxs-3 model mutation, no dispatch |
| Lane this plan serves | john — Ollama engineer, KDD-0013 lane Meta-X → OAI-X transition |
| Target | hxs-3 (192.168.50.202) — Ollama 0.32.15 serving runtime |
| Status | **PLAN — NOT APPROVED / NOT EXECUTED.** [BLOCKERS of record — see §0: (1) no owner ratification for the Meta-X → OAI-X replacement exists in any state log or KDD; (2) KDD-0013 lane amendment PENDING; (3) KDD-0007 retains gpt-oss "as task-shaped control, not the configured workload" — needs labeled supersession; (4) gpt-oss:20b availability on Ollama/hxs-3 UNVERIFIED; (5) immutable-digest + fail-closed identity contract not yet defined for OAI-X.] |
| Governance | Owner rules: native Ollama model pull (no Docker); no host firewall (2026-08-26); Meta-X stays until OAI-X passes full verification (goal SC-05); OmniRoute routing changes are trinity's lane — john only installs the model |

> **Execution prerequisite:** this plan binds nothing. Execution requires (a)
> owner word for the replacement + a labeled KDD-0013 amendment + labeled
> KDD-0007 supersession, (b) gpt-oss:20b availability/digest verified on hxs-3,
> (c) a separate owner-approved execution work order. john's activation for the
> transition additionally requires the immutable-digest contract below and the
> owner's explicit activation word.

## 0. Verified blockers (must clear before execution — from goal review 2026-08-29)

1. **No owner ratification on record.** Meta-X is production-ACTIVE since
   2026-08-27 under KDD-0007 + owner M8 sign-off. No state-log row, KDD
   amendment, or owner directive for "replace Meta-X with gpt-oss:20b" exists.
   Executing without it would silently reverse a ratified decision.
2. **KDD-0013 amendment pending** — the goal's own Notes concede the lane
   amendment is not yet written.
3. **KDD-0007** (line 52) explicitly: "gpt-oss is retained as task-shaped
   control, not the configured workload." A replacement requires a labeled
   supersession, original text preserved.
4. **gpt-oss:20b availability UNVERIFIED** — not in `/opt/tkv-local`, no
   server record of it being pulled/served anywhere. SC-01 assumes
   `ollama list | grep gpt-oss` will show it; must be proven live first.
5. **Premise evidence is thin** — the "Meta-X too slow" claim rests on a single
   OmniRoute 504 (`RATE_LIMIT_EXECUTION_TIMEOUT`) recorded in the LightRAG
   goal's LLM-binding correction; that was a routing-level timeout, already
   mitigated by LightRAG switching to local Chat-X. No same-basis A/B of
   Meta-X vs gpt-oss exists. A same-basis A/B (per
   `DOC-hxs3-gpt-oss-regular-pilot` qualification machinery) is required before
   any decommission.

## Evidence base

| Source | Path | Role |
|---|---|---|
| Goal | `governace/goals/2026-08-29-oai-x-replace-meta-x.md` | Scope, success conditions (SC-01..08), constraints |
| hxs-3 configured state | `servers/hxs-3/configuration.md` (2026-08-27, M8) | Ollama runtime, model store, GPU, services, hashes |
| hxs-3 discovery | `servers/hxs-3/discovery.md` (2026-08-12) | As-found hardware (do not modify) |
| Model lanes | `governace/decisions/KDD-0013-agent-model-lanes.md` | john/rick lanes, immutable-identity discipline |
| Muse pilot adoption | `governace/decisions/KDD-0007-hxs3-muse-glimmer-tooling-adoption.md` | gpt-oss = task-shaped control; Meta-X ratified |
| gpt-oss control context | `knowledge/catalog/documents/DOC-hxs3-gpt-oss-regular-pilot.yaml` | gpt-oss:20b spec (~21B total, 3.6B active MoE, native 128K, Apache-2.0); standing A/B qualification contract |
| LightRAG LLM correction | `governace/goals/2026-08-29-lightrag-hxs4.md` (OPEN CORRECTION) | 504 evidence; already switched to Chat-X local |
| Registry | `servers/SERVER-REGISTRY.md` hxs-3 row | Current-state Meta-X |

## Target host facts (from configuration.md — VERIFIED)

- Hostname hxs-3; Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic; Secure Boot disabled
- 2× PNY RTX 5060 Ti, 16,311 MiB each (32,622 MiB aggregate); PCIe x8 hard ceiling
- Ollama **0.32.15** pinned (`/usr/local/bin/ollama`; binary == server)
- Model store: `/usr/share/ollama/.ollama/models` (ollama:ollama), root ext4, 3.4 TB free
- Listener: `*:11434` (wildcard, loopback preserved); no firewall
- Services: `ollama.service` (enabled/active), `ollama-preload.service`
  (boot pin of `hx-muse-glimmer-64k`, keep_alive=-1)
- Existing aliases: `hx-muse-glimmer[-32k|-64k|-128k]` — all FROM frozen
  artifact `de878ce3…`; operating profile `hx-muse-glimmer-64k` resident
  (digest `9dffb015…`, ctx 65536)

## Plan

### Step 0 — Pre-state verification (V0) — HITL gate

1. SSH to hxs-3 as `hxsa` (askpass pattern, grep-only credential extraction
   from `.local.env`; value never printed/logged).
2. Record identity: `hostname`, `uname -r`, `nvidia-smi` (both cards),
   `ollama --version` (expect 0.32.15), `ollama list`, `df -h`
   (`/usr/share/ollama/.ollama/models` free space ≥ model size + aliases),
   `systemctl is-active ollama ollama-preload`.
3. **Verify gpt-oss:20b availability BEFORE anything else:**
   - Non-mutating registry check (preferred): query the Ollama registry
     manifest for `gpt-oss:20b`, e.g.
     `curl -fsSI https://registry.ollama.ai/v2/library/gpt-oss/manifests/20b`
     (returns 200 when present; no store mutation). Record the returned
     digest, size, and whether it fits in 32,622 MiB aggregate at the
     target context.
   - If a registry manifest check is unsupported or inconclusive on
     Ollama 0.32.15, an explicitly owner-approved **temporary pull
     followed by cleanup** is the only fallback: `ollama pull gpt-oss:20b`,
     record digest/size, then `ollama rm gpt-oss:20b` unless the owner
     authorizes keeping it. This pull is a mutation — it requires owner
     word and must be disclosed as such.
   - **Executable 64K-context feasibility probe (V0, owner-approved):** after
     availability/digest/size are confirmed (and the model is resident, via the
     authorized temporary pull or an owner-authorized keep), run a real 64K
     request against gpt-oss:20b on hxs-3 and measure runtime/resource fit. The
     prompt must be **deterministic and actually consume the 64K window** — not
     a literal placeholder. Build a prompt from a fixed repeating unit until it
     exceeds the target, send it with `num_ctx: 65536`, then **validate that the
     response's `prompt_eval_count` reaches the expected workload size**:
     ```bash
     # Deterministic 64K-token prompt: repeat a fixed unit until the token
     # estimate exceeds 65536 (the unit averages ~1.0 token per word, so
     # 70,000 words ≈ >64K tokens; prompt_eval_count is the authoritative check).
     python3 - <<'PY'
     unit = "The quick brown fox jumps over the lazy dog. "
     # ~9 tokens per unit → ~7,300 units ≈ 65,700 tokens
     prompt = (unit * 7300) + "\nSummarize the paragraph above in one sentence."
     open("/tmp/oai-x-64k-prompt.txt", "w").write(prompt)
     PY
     PROMPT="$(cat /tmp/oai-x-64k-prompt.txt)"
     RESP="$(curl --max-time 1800 http://192.168.50.202:11434/api/generate \
       -d "$(python3 -c 'import json,sys; print(json.dumps({"model":"gpt-oss:20b","prompt":sys.stdin.read(),"options":{"num_ctx":65536}}))' <<< "$PROMPT")")"
     PEC="$(printf '%s' "$RESP" | jq -r '.prompt_eval_count // 0')"
     [ "$PEC" -ge 60000 ] || { echo "OAI-X 64K probe FAIL: prompt_eval_count=$PEC (expected >=60000)"; exit 1; }
     printf 'OAI-X 64K probe OK: prompt_eval_count=%s total_duration=%s eval_count=%s\n' \
       "$PEC" "$(printf '%s' "$RESP" | jq -r '.total_duration // 0')" \
       "$(printf '%s' "$RESP" | jq -r '.eval_count // 0')"
     ```
     Record response success, `prompt_eval_count`, `total_duration`, tokens/sec,
     peak VRAM (from `nvidia-smi` sampling), and confirm no OOM/refusal at the
     64K operating window. A `prompt_eval_count` below the 64K target means the
     window was not actually consumed — that is a FAIL, not a pass. Registry
     metadata (digest/size) and pullability alone do NOT satisfy the 64K
     feasibility requirement.
   - **If availability, pullability, digest, size, or 64K-context feasibility
     (via the executable probe above) cannot be verified — STOP and escalate to
     the governor; do not proceed** (goal SC-01/SC-09 would fail).
4. Confirm Meta-X (`hx-muse-glimmer-64k`, digest `9dffb015…`) is still serving
   and is the only resident model.
5. Record a **same-basis A/B baseline**: run the actual extraction/structured-
   output workload against Meta-X and capture latency + pass/fail, per the
   standing gpt-oss qualification contract — this is the pre-mutation control.
6. **STOP** — present V0 evidence (availability, A/B baseline, GPU headroom) to
   the governor for go/no-go. No mutation occurs before this gate.

### Step 1 — Pull and configure OAI-X (V1–V2)

**1a. Pull the model (john's lane):**
- `ollama pull gpt-oss:20b` (the official pinned identifier resolved in V0; do
  NOT use an unpinned `:latest` — the frozen digest is the identity contract).
- Verify: `ollama show gpt-oss:20b` → digest matches the V0-recorded digest;
  capabilities include `tools` (structured output / tool-calling).

**1b. Create the operating-profile alias (call-sign):**
- Author a Modelfile (or `ollama create`) producing the alias `hx-oai-x-64k`
  (owner-selected call-sign; ctx 64000 / 65536 per owner choice):
  ```dockerfile
  FROM gpt-oss:20b
  PARAMETER num_ctx 65536
  PARAMETER temperature 1
  PARAMETER top_k 64
  PARAMETER top_p 0.95
  ```
  (baked sampling mirrors the A01 rule from Meta-X — native defaults.)
- Record the **alias digest + manifest layer-equality proof** (the KDD-0013
  immutable-identity discipline, same as Meta-X).
- Verify: `ollama show hx-oai-x-64k` → config visible (goal SC-02); digest
  recorded.

### Step 2 — Serve verification (V3) — HITL gate

1. `curl http://192.168.50.202:11434/api/generate -d '{"model":"hx-oai-x-64k","prompt":"Say hello"}'`
   → response generated (goal SC-03).
2. **Tool-calling / structured-output proof (goal SC-05):** send a structured
   prompt requiring JSON output; assert valid JSON returned. Capture the exact
   prompt + output as evidence.
3. **Same-basis A/B:** rerun the Step-0 workload against OAI-X; compare latency
   and pass/fail vs the Meta-X baseline. OAI-X must meet or beat Meta-X on the
   target workload to justify the replacement — otherwise STOP and report.
4. Record VRAM/residency under `MAX_LOADED_MODELS=1`: `ollama ps` shows
   `hx-oai-x-64k` resident with the correct context. Because only one model
   is resident at a time, **the Meta-X alias and frozen artifact must remain
   on disk** (do NOT `ollama rm` any Meta-X artifact before the decommission
   gate), and Meta-X must remain reloadable for rollback — confirm it can be
   reloaded on demand (e.g., a later `ollama run`/route repoint back) without
   requiring simultaneous residency and without preventing OAI-X's eviction
   when the preload swaps. Eviction of Meta-X from VRAM at swap time is
   expected and acceptable; loss of its artifact from the store is not.
5. **STOP** — present V3 evidence (generate + tool-calling + A/B + residency)
   to the governor for the OmniRoute routing decision (trinity's lane).

### Step 3 — OmniRoute routing update (V4) — trinity / governor

1. **Boundary:** john does NOT touch OmniRoute. A trinity (or
   governor-authorized) session updates the OmniRoute route that currently
   points to Meta-X (`hx-muse-glimmer-64k`) to `hx-oai-x-64k`.
2. Verify: `curl http://192.168.50.207:20128/v1/models -H "Authorization:
   Bearer <from .local.env OMNIROUTE key>"` → OAI-X present (goal SC-04);
   a routed inference round-trip succeeds.
3. Update route identity: call-sign, endpoint, alias, role recorded per
   KDD-0013 route-verification discipline (session-start probe + exact
   served-model id).

### Step 4 — Records update (V5)

1. Update, with labeled append-only corrections (never silent rewrites):
   - `AGENTS.md` — john/rick lane references Meta-X → OAI-X
   - `agents/README.md` — roster lane wording
   - `governace/decisions/KDD-0013-agent-model-lanes.md` — **labeled amendment**
     (the standing amendment-8 chain preserved as history)
   - `governace/decisions/KDD-0007-hxs3-muse-glimmer-tooling-adoption.md` —
     **labeled supersession** of the gpt-oss-as-control wording
   - `servers/system-mapping.md` — S03 Meta-X → OAI-X
   - `servers/SERVER-REGISTRY.md` — hxs-3 row current-state
   - `servers/hxs-3/configuration.md` — model/alias/services section
   - `agents/john/profile.md`, `agents/rick/profile.md` — lane lines
2. Re-render affected HTML via `scripts/wiki/render.py`; update the catalog
   receipts (Carol, background-class).

### Step 5 — Meta-X decommission (V6) — ONLY after all gates pass

1. **Do not decommission before SC-05 + A/B pass + owner word.** Containment in
   the goal is explicit: keep Meta-X until OAI-X passes verification.
2. **Update the preload pin BEFORE any `ollama rm`:** edit
   `ollama-preload.service` (via `/usr/local/libexec/hx-ollama-preload`) to pin
   the new resident model (OAI-X digest) with the exact alias+digest `/api/ps`
   assertion (bounded 538 s shape). Verify the updated service references an
   AVAILABLE model (OAI-X still in the store at this point) and passes its
   assertion before touching Meta-X. This ordering keeps restart and rollback
   functional throughout the migration — the enabled preload service never
   points at a model that has been removed.
3. Remove the operating-profile alias + artifact from the Ollama store:
   `ollama rm hx-oai-x-64k` would be the inverse — for decommission, remove
   Meta-X aliases (`hx-muse-glimmer[-32k|-64k|-128k]`) and the frozen artifact
   only after the owner's explicit decommission word.
4. Verify (goal SC-06, complete checks — not merely the alias): `ollama list |
   grep muse-glimmer` → not listed AND the frozen Meta-X artifact's **blob and
   manifest are absent** from the store — `ollama show hx-muse-glimmer-64k`
   fails, and the full digest (recorded from the frozen identity at baseline,
   e.g. `de878ce3…` expanded to the complete manifest digest in
   `/usr/share/ollama/.ollama/models/manifests/…`) is no longer present in
   `/usr/share/ollama/.ollama/models/blobs` — and `ollama-preload.service`
   remains enabled + successful on the new pin.
5. Full rollback path preserved: re-pull Meta-X artifact (digest
   `de878ce3…`), restore preload pin, restore OmniRoute route — each step has
   an exact inverse recorded before mutation.

### Step 6 — Final validation (V7)

1. `python3 scripts/validate.py` → 4/4 PASS (goal SC-08).
2. `render.py --check` → all manifests in sync.
3. All success conditions SC-01..SC-08 pass with evidence; governor accepts;
   handoff receipt written.

## Success conditions (from the goal — reproduced)

| ID | Property | Expected | Gate |
| --- | --- | --- | --- |
| SC-01 | gpt-oss:20b pulled | Model listed | V0/V1a |
| SC-02 | OAI-X Modelfile created | Config visible | V1b |
| SC-03 | OAI-X serves via Ollama | Response generated | V3 |
| SC-04 | OAI-X via OmniRoute | In catalog | V4 |
| SC-05 | Tool-calling works | Valid JSON | V3 |
| SC-06 | Meta-X decommissioned | Not listed | V6 |
| SC-07 | Records updated | All refs updated | V5 |
| SC-08 | Repo validation | 4/4 PASS | V7 |

## Execution controls

- Active charters reviewed: john (Ollama, KDD-0013) — qualified; trinity
  (OmniRoute) — owns routing step; governance: governor.
- Maximum iterations / retries: 3 per step
- Time / token limits: PT1H per session
- Stop conditions: gpt-oss:20b unavailable/infeasible (V0), Ollama not
  responding, A/B does not justify replacement, OmniRoute routing error,
  validate.py FAIL, any digest mismatch (fail closed)
- Rollback / containment: Meta-X kept until SC-05 + A/B pass; exact inverses
  recorded per mutation (see Step 5); no partial decommission
- HITL checkpoints: V0 (availability + A/B baseline), V3 (serve + tool-call +
  A/B), V4 (OmniRoute routing — trinity), decommission word (owner)

## Open items for the owner / governor

- **Owner:** ratification of the Meta-X → OAI-X replacement (or explicit
  rejection — this plan then dies at §0).
- **Owner:** call-sign/context confirmation (`hx-oai-x-64k`, 64K).
- **Owner:** decommission word for Meta-X.
- **Governor:** KDD-0013 amendment + KDD-0007 supersession (labeled) after owner
  word; catalog receipt (Carol).
- **Verification required (V0):** gpt-oss:20b pullability + digest + size, AND
  an **executable 64K-context probe on hxs-3** (runtime/resource fit at
  num_ctx 65536, no OOM/refusal) — registry metadata and pullability alone
  cannot satisfy the 64K feasibility requirement; decommission of Meta-X stays
  blocked until SC-09 passes.

---

*Planning only. No hxs-3 mutation, no model change, no OmniRoute change
performed. While drafting this plan, the governing goal
(`governace/goals/2026-08-29-oai-x-replace-meta-x.md`) and the wiki render manifest
(`scripts/wiki/manifest.txt`) were updated in separate review/fix passes —
no hxs-3 runtime or state files were modified as part of drafting this plan.*
