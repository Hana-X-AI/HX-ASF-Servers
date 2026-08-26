# Esme (john) — M7 Context Ladder + Three-Profile Freeze on Meta-X (hxs-3)

| Field | Value |
| --- | --- |
| Report ID | ESME-M7-LADDER-PROFILES-001 |
| Task ID | WO-HXS3-JOHN-M7-001 (`PILOT-HXS3-MUSE-GLIMMER-TOOLING-001`, milestone M7) |
| Agent | john / Esme (session `john-m7-20260826-01`) |
| Host | `hxs-3` (192.168.50.202, Meta-X), Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic |
| Session host | `hxs-5` (192.168.50.204); all target actions over SSH `hxsa@192.168.50.202` |
| Window | 2026-08-26T07:20Z → 07:58Z (UTC) = 02:20 → 02:58 hxs-3-local (America/Panama, EST/-05:00 per F-08) |
| Ollama | 0.32.15 (binary == server; unchanged from M4) |
| Frozen artifact | `muse-glimmer:30b` digest `de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1` (dense 27.9B, 52 blocks, Q4_K_M, max ctx 131,072, CLIP 1.92B) |
| GPUs | 2× PNY RTX 5060 Ti 16,311 MiB, driver 580.173.02 (rick's plane, untouched) |
| Governing decisions | D5 (64K operating default after the ladder); owner 2026-08-26 "identical pattern, same blueprint" as hxs-1 |

Evidence labels per plan: FACT / AUTHORITY / UPSTREAM / INFERENCE / RECOMMENDATION.
All secrets excluded; the SSH secret was used only through the session askpass helper (0700, reads the credential-record table row of the HX Fleet SSH Access Guide at execution time, deleted at task end); it was never printed, logged, or stored. No secret-piping to sudo (`sudo -n` only). Thinking content is never retained (A01 §5.2): every harness strips `message.thinking` immediately and persists only presence/character counts; this document contains zero thinking text.

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path resolves locally here, as in M4)
Source: /opt/tkv-local/ollama (+ /opt/tkv-local/servers AGENTS.md contract — read, read-only use)
Reviewed At: 2026-08-26T07:20Z → 07:33Z
Relevant Files: 9 reviewed —
  ollama-main/docs/modelfile.mdx:57,149 (PARAMETER num_ctx — the effective contract per PILOT-002)
  ollama-main/docs/context-length.mdx (VRAM-based defaults 4k/32k/256k; OLLAMA_CONTEXT_LENGTH;
    verify PROCESSOR split via ollama ps)
  ollama-main/docs/faq.mdx:354 (OLLAMA_KV_CACHE_TYPE default f16 — unset in hx3.conf ⇒ f16;
    journal llama_kv_cache lines captured per rung as the empirical record)
  ollama-main/types/model/name.go:93-99,268-302 (Name struct carries NO digest part;
    Filepath() = host/namespace/model/tag — digest-qualified names rejected/irresolvable)
  ollama-main/internal/modelref/modelref.go:99-118 (source suffixes are cloud/local only)
  ollama-main/server/create.go:129-190 (FROM flow + config inheritance), 1352-1401
    (setParameters: Modelfile params take precedence; unlisted keys inherited from the base
    params layer ⇒ baked temperature 1 / top_k 64 / top_p 0.95 preserved when only num_ctx is added)
  ollama-main/server/model.go:40-88 (parseFromModel → ParseNamedManifest(tag); pulls only when
    the tag is absent — tag present and frozen ⇒ no network path)
  fixtures needle_probe.py + fixtures_corpus.py verified vs fixtures/sha256sums.txt (all 10 OK,
    07:20Z); hxs-1 pattern 22-esme-m6-capacity-ladder.md / 29-esme-m6b-profiles.md;
    hxs-3 M4 frozen state 07-esme-m4-install.md
Authority/Version Identified: TKV snapshot carries the glimmer sources (server/glimmer_images_test.go
  present) — consistent with installed 0.32.15; every binding claim is proven empirically on hxs-3
  (manifest layer equality, ollama show, /api/ps).
Applicable Tests/Runbooks: WO-HXS3-JOHN-M7-001 sequence; hxs-1 M6 stage procedure; F-M6-2
  poll-to-empty unload discipline; F-E4 preload restart-not-start; D5 budgets; fixtures contract
  (needle at rung's OWN alias, fixture-validity gate on prompt_eval_count).
Contradictions or Gaps:
  1. Digest-qualified FROM (`model:tag@sha256:…`) is REJECTED by this server version
     (empirical 400 "invalid model name"; Name has no digest part in the version-matched source).
     Rung Modelfiles therefore bind FROM muse-glimmer:30b — the local tag whose on-disk manifest
     sha256 == the frozen digest de878ce33ad8…64c1 (content-addressed, M4-proven) — with the
     frozen digest carried verbatim in each Modelfile header and binding PROVEN post-create by
     manifest layer equality (M4 three-way method). Disclosed deviation in syntax only; the
     identity guarantee the work order requires is achieved and proven (§4, F-M7-1).
Task May Proceed: YES
```

Teammate roster (profile §4.2): `agents/` contains john, kimi-k3, rick, carol — all current. Target identity verified before any action (FACT, 07:29Z / 02:29 EST): `hostname` = `hxs-3`, `hostname -I` = `192.168.50.202`, `sudo -n` OK, host key pinned `StrictHostKeyChecking=yes` against F-05 ED25519 `SHA256:R/3mdfv7J0Fajo8yryT7JB6B4EoBm47W2rLX+siHEog` (scan fingerprint matched exactly before pinning; a mismatch would have halted the session), timezone America/Panama (NTP synchronized), uptime continuous 15:05 (no reboot).

## 2. Drift check (FACT, 07:29Z / 02:29 EST) — FIRST, before any mutation

| Item | Frozen value (M4 end state) | Observed | Verdict |
| --- | --- | --- | --- |
| Base `muse-glimmer:30b` digest | `de878ce33ad8…64c1` | `de878ce33ad8…64c1` | **match** |
| Resident identity | `hx-muse-glimmer:latest` `472ad84e…ad99`, ctx 32768, Forever | identical; `size_vram == size == 17,839,465,428` | **match** |
| `ollama --version` / `/api/version` | 0.32.15 / 0.32.15 | 0.32.15 / 0.32.15 | **match** |
| `hx3.conf` sha256 | `b4f98c2f…627c` | `b4f98c2f…627c` | **match** |
| `hx-ollama-preload` sha256 | `d37dc30f…fd84` | `d37dc30f…fd84` | **match** |
| `ollama-preload.service` sha256 | `3b0e00b6…a5f6` | `3b0e00b6…a5f6` | **match** |
| Units | both active+enabled | both active+enabled; `NRestarts=0` | **match** |
| Listener | `*:11434` (wildcard; loopback preserved; LAN boundary per D2) | `*:11434`; LAN `/api/version` answers | **match** |
| Swap used | 0 B | 0 B | **match** |
| Uptime | no reboot | 15:05 continuous | **match** |
| Per-GPU MiB at rest | 10,170 + 8,908 (M4) | 10,192 + 8,930 | **match** (≤ +22 MiB rest variance) |

**NO DRIFT — the stop rule was not triggered.**

## 3. Rung Modelfiles and alias creation (FACT)

Rung Modelfiles (authored on hxs-5, hash-verified identical on both sides before any `ollama create`): the M4 FROM-only alias structure with the frozen digest cited in the header and **exactly one added line — `PARAMETER num_ctx <C>`**. No SYSTEM, no TEMPLATE, no sampling parameter; the embedded Muse template is never touched.

| Rung | Alias | `PARAMETER num_ctx` | Modelfile sha256 (both sides verified) |
| --- | --- | --- | --- |
| 32K (VRAM-default baseline) | `hx-muse-glimmer-32k` | 32768 | `952a92c3e8948b7996aa8523f7007711b6ce8570849032b4de860de6330ca5fb` |
| 64K (D5 operating) | `hx-muse-glimmer-64k` | 65536 | `46809bfec1c1efe0c47b859a4805929d838675cdfad78cd085c643e9dc298856` |
| 128K (artifact max, extended) | `hx-muse-glimmer-128k` | 131072 | `c12acab4c81aadc1ad9e47590a51f608d03452c598afe11e269e5cb65d0dd79e` |

Creations (07:37Z / 02:37 EST) all `success`; the create log showed the three frozen layers reused. `ollama show` per alias (FACT): architecture/parameters/quantization/capabilities/projector identical to the frozen artifact; **Parameters block = baked `temperature 1`, `top_k 64`, `top_p 0.95` PLUS the rung's `num_ctx` and nothing else** — the create-time params merge (create.go `setParameters`) behaved exactly as the source says.

**Digest-qualified FROM deviation (F-M7-1, disclosed):** the first -32k attempt with `FROM muse-glimmer:30b@sha256:de878ce33ad8…` returned `400 Bad Request: invalid model name` (no alias was created by that attempt; kept in the command log). The version-matched source explains it (Name has no digest part). The binding was achieved via the frozen local tag + post-create layer equality — see §7.

## 4. Ladder — per-rung proof table (FACT; hxs-3-local timestamps EST/-05:00)

Each rung: controlled unload polled to `/api/ps` empty (F-M6-2), cold load of the rung alias with `keep_alive:-1`, residency capture, needle probe at ~95% of rung ctx with the rung's OWN alias, 3 known-answer spot checks (thinking ON), link-speed capture under needle prefill, journal scan. Load order 32K → 64K → 128K.

| Proof | 32,768 (`-32k`) | 65,536 (`-64k`) | 131,072 (`-128k`) |
| --- | --- | --- | --- |
| `/api/ps` digest | `09c4f825…836e` | `9dffb015…e7da` | `17fe5b80…e85b` |
| Effective `context_length` | 32,768 | 65,536 | 131,072 |
| Residency (`size == size_vram`) | 17,112,131,172 B (15.94 GiB) | 17,380,566,628 B (16.19 GiB) | 17,917,437,540 B (16.69 GiB) |
| `ollama ps` PROCESSOR / UNTIL | 100% GPU / Forever | 100% GPU / Forever | 100% GPU / Forever |
| Layers offloaded | 53/53 to GPU | 53/53 to GPU | 53/53 to GPU |
| Per-GPU MiB after load | 9,822 + 8,562 | 10,142 + 8,914 | 10,782 + 9,618 |
| Per-GPU MiB under needle load | 9,834 + 8,574 | 10,154 + 8,926 | 10,794 + 9,630 |
| Journal KV buffers (LLM, f16) | 192+224 = 416 MiB | 384+448 = 832 MiB | 768+896 = 1,664 MiB |
| Journal second KV cache | 52.5+45 = 97.5 MiB | 97.5 MiB | 97.5 MiB |
| `sched_reserve` compute /GPU | 333.07 MiB | 461.07 MiB | 717.07 MiB |
| Needle @ ~95% (lines / needle line) | 1,349 / 877 (65.0%) | 2,702 / 1,756 (65.0%) | 5,409 / 3,516 (65.0%) |
| Needle prompt_eval_count (% ctx) | 31,145 (95.05%) | 62,264 (95.00%) | 124,525 (95.00%) |
| fixture window [LO, HI] | [30474, 32276] | [60948, 64563] | [121897, 129086] |
| fixture_valid / done_reason / needle_found | true / stop / **found** | true / stop / **found** | true / stop / **found** |
| Cold prefill at depth / wall | 1,902.2 tok/s / 44.14 s | 1,825.2 tok/s / 58.09 s | 1,655.3 tok/s / 102.96 s |
| Spot checks (thinking ON) | 3/3 PASS | 3/3 PASS | 3/3 PASS |
| Xid / OOM / err-level / CPU fallback | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| **Verdict** | **CAPACITY PASS** | **CAPACITY PASS** | **CAPACITY PASS** |

Fixture calibration (disclosed, same class as hxs-1 D-M6-2): one calibration probe (300 lines → 7,018 prompt tokens; ≈23.0 tok/line + ≈110 fixed overhead on this gpt2/llama4-pre tokenizer) sized each rung's document; every rung's first real probe landed inside its window — no re-runs, no forced passes. Calibration JSON retained in session evidence (`needle-cal.json`).

**128K extended-rung note:** needle **found** at 95.00% depth with `done_reason=stop` — the extended-fail fallback (drop to two profiles) was **not** triggered; nothing was forced.

## 5. KV growth — f16, measured linear (FACT)

Two independent derivations across two depth pairs each:

| Measure | 32K→64K slope | 64K→128K slope | Verdict |
| --- | --- | --- | --- |
| Journal `llama_kv_cache` LLM KV (pure KV, f16) | 416→832 MiB: 436,207,616 B / 32,768 tok = **13,312 B/token** | 832→1,664 MiB: 873,463,808 B / 65,536 tok = **13,312 B/token** | **exactly linear** |
| `/api/ps` total resident size (scheduler planning figure) | 268,435,456 B / 32,768 tok = **8,192 B/token** | 536,870,912 B / 65,536 tok = **8,192 B/token** | **exactly linear** |

- **KV B/token (headline): 13,312 B/token f16** (journal KV buffers; GQA 2 KV heads × 128 k/v-length across the full-attention layer set; the sliding-window layer set is the constant second cache at 97.5 MiB).
- The `/api/ps` slope (8,192 B/token) is the smaller VRAM-planning slope because the scheduler's compute-buffer apportioning moved the other way at the rung-time server context (no env override during the ladder); both are reported, labeled, and neither is hidden. Constant across rungs: CUDA model buffers 7,442.06 + 7,804.43 = 15,246.49 MiB weights, CPU_Mapped 721.42 MiB (mmap, host RAM), mmproj worst-case estimate 1,717.95 MiB.
- Dense-model VRAM watch (packet requirement): weights 16,756,681,056 B blob + 1.92B projector (1,400,328,928 B blob) + KV — at the tightest rung (128K) 20,424 MiB of 32,622 MiB aggregate used under load ⇒ **≈12,198 MiB (11.9 GiB) headroom; never tight, zero offload at every rung.**

## 6. Known-answer spot checks — flat across rungs (FACT)

Three fixed synthetic known-answer prompts, thinking ON (native default), no sampling overrides; harness = session scaffolding `spot_check.py` (sha256 `3a843e54ec79c135e068fbd09a3196f49ce2ce4eb000f5913fe032971f163602`, both sides verified; strips thinking immediately, persists counts only):

| Case | Expected | 32K | 64K | 128K | Operating-profile re-proof (-64k) |
| --- | --- | --- | --- | --- | --- |
| KA1 `17 × 23` | `391` | `391`, stop, thinking ✓ | identical | identical | identical |
| KA2 `847 × 36` | `30492` | `30492`, stop, thinking ✓ | identical | identical | identical |
| KA3 days in a leap year | `366` | `366`, stop, thinking ✓ | identical | identical | identical |

Content strings compared across rungs programmatically: **FLAT = true** (identical contents, all `done_reason=stop`, thinking present at every rung). Thinking chars recorded in the JSON evidence only; zero thinking text retained anywhere.

## 7. Alias freeze — per-rung digest equality proofs (FACT)

On-disk manifest sha256 == `/api/tags` digest for every alias (content-addressing holds), and manifest layer comparison vs the frozen artifact:

| Alias | Manifest sha256 == digest | config blob | projector blob | weights blob | params blob |
| --- | --- | --- | --- | --- | --- |
| `muse-glimmer:30b` (frozen, source tag) | `de878ce33ad8…64c1` | `57b82200bf7c…` | `f48b452316f9…` (1,400,328,928 B) | `71b5c9c9abbc…` (16,756,681,056 B) | `56380ca2ab89…` (42 B: baked T1/top_k64/top_p0.95) |
| `hx-muse-glimmer` (M4 working alias) | `472ad84e…ad99` | same | same | same | same `56380ca2ab89…` |
| `hx-muse-glimmer-32k` | `09c4f825ac2f59381953d5ecdabe0fe10d35e83eb7c35fde749269eb1b58836e` | **same** | **same** | **same** | `60427b69…` = `{"num_ctx":32768,"temperature":1,"top_k":64,"top_p":0.95}` |
| `hx-muse-glimmer-64k` | `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da` | **same** | **same** | **same** | `ae869ec5…` = `{"num_ctx":65536,"temperature":1,"top_k":64,"top_p":0.95}` |
| `hx-muse-glimmer-128k` | `17fe5b80483897687c04b8f847d03c8fc893b3312a3e408879b45b003ed2e85b` | **same** | **same** | **same** | `4131ffd6…` = `{"num_ctx":131072,"temperature":1,"top_k":64,"top_p":0.95}` |

Params blob contents dumped verbatim into evidence (`06b-params-blobs.txt`): the only content difference between any rung manifest and the frozen artifact is the params blob, and the only key delta is `num_ctx`. **Digest equality to the frozen artifact: PROVEN per rung.** Aliases established during the ladder carry their final names — the freeze is this equality record; `/api/ps` rung digests == the frozen alias digests (§4 == §7, row by row).

## 8. Repoint to the D5 operating profile (FACT) — versioned edits, pre/post sha256 + diffs

### 8.1 `/usr/local/libexec/hx-ollama-preload` — two-line diff (the hxs-3 script pins alias AND digest)

```diff
-MODEL="hx-muse-glimmer"
-DIGEST="472ad84e752d0319b65d6fcd862c26c3850cc408b6b9430046db31250994ad99"
+MODEL="hx-muse-glimmer-64k"
+DIGEST="9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da"
```

sha256 `d37dc30f…fd84` → **`b17981305a7bf1c418be6544557b3e3bae66b56d0d2bb2f802d5e26e5ee6fe08`**. root:root 0755 unchanged (`sudo -n install`). Lint: `sh -n` / `bash -n` / `dash -n` PASS on candidate and installed copy; shellcheck unavailable in this session (carried F-E6-class limitation — M4's volatile extraction is gone; the manual functional test below is the real gate, as on hxs-1). Pre-change bytes captured verbatim (`16-prechange-files.txt`, hash matches the M4 frozen reference).

### 8.2 `/etc/systemd/system/ollama.service.d/hx3.conf` — OLLAMA_CONTEXT_LENGTH added (operator-consistency, hxs-1 pattern)

```diff
+# OLLAMA_CONTEXT_LENGTH=65536 is operator-consistency with the D5 operating
+# profile only — each alias Modelfile's PARAMETER num_ctx remains the
+# effective per-model contract (hxs-1 pattern). …
 [Service]
 Environment="OLLAMA_HOST=0.0.0.0"
 Environment="OLLAMA_NO_CLOUD=1"
 Environment="OLLAMA_NUM_PARALLEL=1"
 Environment="OLLAMA_MAX_LOADED_MODELS=1"
+Environment="OLLAMA_CONTEXT_LENGTH=65536"
```

(The stale "NO context … variables are set here — the M7 ladder owns any context change" comment lines were updated in the same edit; the NO-sampling statement stands.) sha256 `b4f98c2f…627c` → **`238189e07bd19c08c03a89deef425ae774557e83c1a3d38b8e86e7c27bd63655`**. root:root 0644 unchanged. `daemon-reload` executed (02:50 EST); effective environment verified via `systemctl show ollama -p Environment`: `OLLAMA_CONTEXT_LENGTH=65536` present, the four M4 values unchanged (FACT).

### 8.3 Untouched

`ollama-preload.service` sha256 `3b0e00b6…a5f6` — unchanged (verified post-deploy). Its `Description=` still reads "pin hx-muse-glimmer resident" — the family name; the unit body was never model-parameterized (observation recorded, no third-file edit beyond the authorized two-artifact repoint).

### 8.4 Switch sequence (02:49:57 → 02:51:03 EST)

1. `sudo -n systemctl restart ollama` → the `-128k` runner torn down; `Requires=` propagation ran the edited preload inside the unit window (F-M6B-1 class): cold load of `hx-muse-glimmer-64k` ≈ 15 s including the F-E2 discovery-watchdog listener delay.
2. Manual non-reboot functional test of the edited script: `sudo -n /usr/local/libexec/hx-ollama-preload` → RC=0, `OK - hx-muse-glimmer-64k resident (digest 9dffb015…)` in 0.04 s (asserted against the already-resident runner). The M4 gate ("manual functional test is the real gate") is satisfied on the edited script.
3. `sudo -n systemctl restart ollama-preload` (restart, not start — F-E4) → RC=0, `Result=success`, `active (exited)`, journal OK line with the exact -64k digest.

## 9. Operating-profile residency proof (FACT, 02:51 EST, re-verified 02:53 EST)

| Proof | Result |
| --- | --- |
| `/api/ps` name | `hx-muse-glimmer-64k:latest` |
| `/api/ps` digest | `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da` — frozen 64K alias, exact |
| `context_length` | **65,536** effective |
| Residency | `size_vram == size == 18,376,336,340 B` (17.11 GiB) — **100% VRAM**, zero fallback; 53/53 layers GPU |
| `expires_at` | year-2318 (keep_alive=-1, **Forever**) |
| `ollama ps` | `100% GPU`, CONTEXT 65536, Forever |
| Per-GPU VRAM | GPU0 10,618 / GPU1 9,388 MiB of 16,311 each (≈12.3 GiB aggregate headroom) |
| Journal this load | KV 384+448 = 832 MiB + second cache 117 MiB; compute 926.14 MiB/GPU (F-M7-2); zero Xid/OOM |
| Quick re-proof | 3/3 known-answer PASS on the resident profile (thinking ON, stop) |
| Units | both active+enabled; `NRestarts=0`; preload `Result=success` |
| Listener / swap / uptime | `*:11434` (loopback preserved, LAN per D2) / 0 B / continuous (no reboot) |

**F-M7-2 (scheduler estimate vs `OLLAMA_CONTEXT_LENGTH`, FACT):** at identical `n_ctx = 65536` and identical model KV (832 MiB), the operating load's scheduler size is 18,376,336,340 B vs the rung load's 17,380,566,628 B (+995,769,712 B): the `sched_reserve` compute buffer scales with the server-wide context (461.07 → 926.14 MiB/GPU; host 292.08 → 588.16 MiB; second KV cache 97.5 → 117 MiB) once `OLLAMA_CONTEXT_LENGTH=65536` is set. Both states are 100% VRAM; the rung table (§4) reports no-env-override sizing, and 18,376,336,340 B is the operating-state planning figure. hxs-1's M6 stage-1 number was likewise taken under the env override — same pattern.

## 10. Link speed under load (FACT — the row-2 PCIe caveat)

Captured per rung with `nvidia-smi --query-gpu=pcie.link.gen.current/max,pcie.link.width.current/max,…` every 3 s across each needle prefill (full logs in evidence `11/15/18`):

| State | GPU0 | GPU1 |
| --- | --- | --- |
| Idle (pre-prefill) | Gen 1 of 3, x8 of x16 | Gen 1 of 3, x8 of x16 |
| Under prefill load (every rung) | **Gen 3 of 3 (8.0 GT/s MAX), x8 of x16** | **Gen 3 of 3 (8.0 GT/s MAX), x8 of x16** |

Consistent with the M4 answer: the Gen1 idle reading is ASPM downshift; link speed ramps fully to the Gen3 ceiling under load on both GPUs at every rung; **the x8 wiring (vs x16 device max) is the hard ceiling** — unchanged, no drift across the ladder. Load telemetry peaks: GPU0 ~180 W / 79 °C; GPU1 ~180 W / 82 °C (sustained 128K prefill); SM util 100% prefill phases; no throttle events.

## 11. Journal state (FACT, full window 02:28 → 02:56 EST)

- **Zero Xid** (kernel grep `Xid` = 0 across the whole window), **zero OOM**, **zero error-level lines** system-wide and for `ollama` (direct `-p err` query, not the banner-counting artifact of F-M6B-3), **zero CPU fallback** at any rung (`offloaded 53/53 layers to GPU` every load).
- Known benign classes observed: F-E2 llama-server GPU-discovery watchdog warnings on cold loads (bounded, expected); NVRM teardown assertions (`iovaspaceDestruct`/`pIOVAS`/`Sysmemdesc`) at each controlled unload — the hxs-1 F-M5B-2/F-M6-6 class, not Xid, rick's plane, monitor only; `kbifInitLtr_GB202: LTR is disabled` platform notes.
- One info-class `curl (7)`-equivalent window: the preload's bounded Phase-1 probes absorbed the listener delay during the mandated restart (F-M6-1/F-M6B-1 class), then OK. No foreign-client API traffic observed in the window.

## 12. Sequential command log (profile §11.3)

Session host `hxs-5`, user `hxsa`; remote = SSH askpass wrapper (secret never on any command line; `sudo -n` only). Timestamps UTC. Failures and corrections kept.

```text
 1 07:20 exit=0 [local] hostname=hxs-5; TKV present; fixtures sha256sum -c → 10/10 OK
 2 07:20-07:33 exit=0 [local] TKV reads: modelfile.mdx, context-length.mdx, faq.mdx:354,
    types/model/name.go, internal/modelref, server/create.go, server/model.go; roster check
    → [KNOWLEDGE REVIEW COMPLETE]
 3 07:28 exit=0 [local] mkdir /tmp/esme-m7 (0700); askpass helper + ssh/scp wrappers (0700);
    helper READS the credential-record password row at execution time (value never in the file);
    sh -n lint PASS
 4 07:28 exit=0 [local] ssh-keyscan -t ed25519 .202 → fingerprint == F-05 recorded
    SHA256:R/3mdfv7…HEog → pinned known_hosts (StrictHostKeyChecking=yes)
 5 07:29 exit=0 ssh identity verify: hostname=hxs-3; hostname -I=192.168.50.202; sudo -n OK;
    tz America/Panama EST -05:00 NTP-synced; uptime 15:05 [evidence 00]
 6 07:29 exit=0 ssh drift check [evidence 01] — all M4 frozen references match; NO DRIFT
 7 07:34 exit=0 [local] author 3 rung Modelfiles (digest-qualified FROM); local sha256 [evidence 02]
 8 07:35 exit=0 scp Modelfiles + needle_probe.py + fixtures_corpus.py; remote sha256 5/5 match
    (fixture hashes == repo frozen) [evidence 03]
 9 07:36 exit=1 ssh ollama create -32k (digest FROM) → 400 invalid model name — F-M7-1
    disclosed; NO alias created [evidence 04]
10 07:36 exit=0 [local] root-cause via name.go (no digest part); rebuild Modelfiles FROM the
    frozen tag with digest in header; new sha256 ×3 [evidence 02b]
11 07:37 exit=0 scp + remote hash match ×3; ollama create -32k/-64k/-128k → success ×3
    [evidence 04b]
12 07:37 exit=0 ssh /api/tags + ollama show ×3 → digests 09c4f825…/9dffb015…/17fe5b80…;
    params = baked + num_ctx only [evidence 05]
13 07:38 exit=0 ssh manifest layer equality: on-disk manifest sha == digest ×5; config/projector/
    weights blobs identical; params blobs dumped verbatim [evidence 06/06b]
14 07:38 exit=0 [local] author spot_check.py (session scaffolding); sha256; scp; remote match
    [evidence 07]
15 07:39 exit=0 ssh controlled unload hx-muse-glimmer → /api/ps empty at poll 1 (F-M6-2)
    [evidence 08]
16 07:39 exit=0 ssh load -32k (keep_alive:-1, 11.8 s); residency: 09c4f825…, ctx 32768,
    size==size_vram 17,112,131,172, 100% GPU, Forever, 9,822/8,562 MiB; runner journal captured
    [evidence 09/09b]
17 07:41 exit=0 ssh needle calibration 300 lines → 7,018 tok (23.0 tok/line class) — disclosed
    calibration [evidence 10]
18 07:42 exit=0 ssh needle 32768: 1,349 lines → 31,145 tok (95.05%), stop, FALCON-61803 found,
    prefill 1,902.2 tok/s cold; link telemetry captured (Gen3/x8 under load) [evidence 11]
19 07:44 exit=0 ssh spot_check -32k → 3/3 PASS [evidence 12]
20 07:44 exit=0 ssh journal scan rung 32K: Xid 0 / OOM 0 / err 0; 'offload' hits resolved =
    53/53 layers TO GPU; NVRM lines = known teardown/LTR classes [evidence 13/13b]
21 07:45 exit=0 ssh unload→empty; load -64k (15.4 s); residency: 9dffb015…, ctx 65536,
    17,380,566,628, 100% GPU, Forever, 10,142/8,914 MiB; KV 832+97.5 MiB [evidence 14]
22 07:47 exit=0 ssh needle 65536: 2,702 lines → 62,264 tok (95.00%), stop, found, prefill
    1,825.2 tok/s; link telemetry [evidence 15]
23 07:49 exit=0 ssh spot_check -64k 3/3; journal scan clean (Xid/OOM/err/fallback = 0)
    [evidence 16]
24 07:49 exit=0 [local] capture pre-change preload + hx3.conf (hashes == M4 frozen); build
    candidates: preload MODEL+DIGEST two-line diff; hx3.conf +CONTEXT_LENGTH + comment sweep;
    sh/bash/dash -n PASS; shellcheck unavailable (carried); candidate sha256 [evidence 16-pre/
    18 + diffs]
25 07:50 exit=0 ssh unload→empty; load -128k (13.8 s); residency: 17fe5b80…, ctx 131072,
    17,917,437,540, 100% GPU, Forever, 10,782/9,618 MiB; KV 1,664+97.5 MiB [evidence 17]
26 07:52 exit=0 ssh needle 131072: 5,409 lines → 124,525 tok (95.00%), stop, found, prefill
    1,655.3 tok/s, wall 102.96 s; link telemetry sustained ~180 W both GPUs [evidence 18]
27 07:54 exit=0 ssh spot_check -128k 3/3; journal scan clean [evidence 19]
28 07:54 exit=0 scp spot/needle JSONs → session evidence; python flat-check → FLAT=true
29 07:55 exit=0 scp candidates; sudo install (script 0755, conf 0644, root:root); installed
    sha match candidates; sh -n installed PASS; daemon-reload; effective env CONTEXT_LENGTH=65536
    [evidence 20]
30 07:55 exit=0 ssh systemctl restart ollama → Requires= ran edited preload → -64k cold-loaded
    (~15 s, F-M6B-1 class); manual script test RC=0 OK line 0.04 s; restart ollama-preload
    (F-E4) RC=0 Result=success [evidence 21]
31 07:56 exit=0 ssh operating residency proof: 9dffb015…, ctx 65536, size==size_vram
    18,376,336,340, Forever, 10,618/9,388 MiB; load-journal buffers captured (F-M7-2 root cause);
    64K-rung compute lines recovered from journal (461.07 MiB/GPU); quick re-proof 3/3
    [evidence 22/23]
32 07:57 exit=0 ssh final sweep: 5 tags in-store (source + bare + 3 rungs, nothing deleted);
    units active+enabled; NRestarts=0; preload unit sha unchanged; listener *:11434 + LAN
    version answer; swap 0 B; uptime continuous; full-window Xid/OOM/err = 0 [evidence 24/25]
33 07:58 exit=0 [local] write deliverable 09-esme-m7-ladder-profiles.md
34 (task end) exit=0 cleanup: remote /tmp/esme-m7 removed (verified); local askpass helper +
    wrappers + known_hosts deleted (verified); sanitized session evidence retained transiently
    at hxs-5:/tmp/esme-m7/evidence
```

## 13. Configuration files (profile §11.2)

| Artifact | Pre-change sha256 | Post-change sha256 | Diff | Ownership/mode |
| --- | --- | --- | --- | --- |
| `/usr/local/libexec/hx-ollama-preload` | `d37dc30f…fd84` | **`b1798130…fe08`** | two lines (`MODEL=`, `DIGEST=`), §8.1 | root:root 0755 (unchanged) |
| `/etc/systemd/system/ollama.service.d/hx3.conf` | `b4f98c2f…627c` | **`238189e0…3655`** | +`OLLAMA_CONTEXT_LENGTH=65536` + comment sweep, §8.2 | root:root 0644 (unchanged) |
| `/etc/systemd/system/ollama-preload.service` | `3b0e00b6…a5f6` | `3b0e00b6…a5f6` | — (untouched) | root:root 0644 |
| Rung Modelfiles (transient `/tmp` copies) | absent | §3 table (3 hashes, both sides verified) | one `PARAMETER num_ctx` line each vs M4 FROM-only | hxsa:hxsa 0644 (removed at cleanup) |
| Model store tags | 2 (base + bare alias) | 5 (+ 3 rung aliases) | §7 | store `ollama:ollama` |

Pre-change full contents captured in session evidence (`16-prechange-files.txt`; hashes == M4 frozen references); unified diffs in `preload.diff` / `hx3conf.diff` and inlined in §8. Effective runtime values post-reload: `systemctl show` Environment excerpt (§8.2); server-side uptake proven by §9 residency.

**Rollback (all steps reversible, per work order):** restore the prior preload script (sha256 `d37dc30f…fd84`, full text in evidence and inlined in `07-esme-m4-install.md` §5.7) and hx3.conf (`b4f98c2f…627c`, §5.6 there) via `sudo -n install` + `daemon-reload`; remove the three rung aliases via `ollama rm hx-muse-glimmer-32k hx-muse-glimmer-64k hx-muse-glimmer-128k` (tags only — all weight/projector blobs shared; base tag and bare alias never touched); then `restart ollama` → poll `/api/ps` empty → `restart ollama-preload` (§8.4 sequence). Pre-state hashes recorded above.

## 14. Findings, risks, decisions surfaced

- **F-M7-1 (digest-qualified FROM unsupported, FACT — disclosed deviation):** `FROM model:tag@sha256:…` is rejected by this 0.32.15 create path (`400 invalid model name`); the version-matched `Name` struct has no digest part. Binding to the exact frozen digest was achieved via the frozen local tag (on-disk manifest sha256 == digest) plus post-create manifest layer equality and params-blob dumps (§7). The work order's identity guarantee is met and proven; the literal syntax is not available in this version. RECOMMENDATION → KK3: record this syntax limitation for future "FROM the exact digest" work orders on 0.32.15.
- **F-M7-2 (scheduler size scales with `OLLAMA_CONTEXT_LENGTH`, FACT):** §9 — +995,769,712 B at identical n_ctx 65536 once the env override is set (compute-buffer + second-cache sizing). The rung table and the operating figure are both reported with their exact conditions; capacity conclusions unchanged (100% VRAM everywhere, ≥11.9 GiB headroom even at 128K).
- **F-M7-3 (VRAM-default path reserves more than explicit num_ctx, FACT):** the M4 bare alias at ctx 32768 (VRAM-default) measured 17,839,465,428 B vs the explicit-num_ctx -32k rung's 17,112,131,172 B at the same n_ctx (−727,334,256 B). Not a regression — the explicit contract sizes tighter; recorded so future comparisons use like-for-like paths.
- **F-M7-4 (KV coefficient, FACT):** f16 KV growth exactly linear at **13,312 B/token** (journal KV buffers; two independent depth pairs) with a constant 97.5 MiB second cache; scheduler total-size slope 8,192 B/token under rung conditions. 128K f16 fits with ≈11.9 GiB aggregate headroom — the fleet's densest case is comfortable, measured (never assumed).
- **Carried, untouched:** F-E2 discovery watchdog on cold loads; NVRM teardown-assertion class (rick's plane, monitor only); `kbifInitLtr` LTR notes; F-E6-class shellcheck unavailability this session (sh/bash/dash `-n` + the manual functional test carried the gate).
- **No stop condition triggered** (no OOM, no CPU fallback, no Xid; needles found at 32K/64K; 128K found ⇒ no extended-fail fallback); **no escalation required.**

## 15. Boundary statements

**Thinking-retention:** thinking content is nowhere retained — needle_probe.py and spot_check.py strip `message.thinking`/think-tags immediately and persist only presence/character counts; this document contains zero thinking text.

**Sampling/template:** no sampling parameter was set anywhere (server, drop-in, Modelfile, or request); the baked `temperature 1 / top_k 64 / top_p 0.95` governed every inference; the embedded Muse template was never modified (rung manifests share the frozen artifact's config blob).

**Scope:** no quality-suite changes (M5 scope), no other models, no pulls, no reboots, no firewall, no endpoint changes, no second serving plane, no model-store deletions — the source tag, the M4 bare alias, and all three rung aliases remain in-store as tags; only `-64k` is resident. Nothing above 131,072 was configured or requested. No vision inputs were exercised.

## 16. Validation summary (profile §11.4)

- **What changed:** three rung aliases created FROM the frozen artifact with `num_ctx` as the only changed parameter (digests §7, layer-equality proven); the preload contract repointed to `hx-muse-glimmer-64k` (script `MODEL=`+`DIGEST=` lines; drop-in `OLLAMA_CONTEXT_LENGTH=65536` for operator consistency, hxs-1 pattern); the host switched to the 64K operating profile, resident and proven.
- **What did not change:** frozen artifact digest `de878ce33ad8…64c1`; M4 bare alias digest `472ad84e…ad99`; Ollama 0.32.15 (binary == server); preload unit bytes; all other drop-in lines (HOST wildcard with loopback preserved, NO_CLOUD=1, NUM_PARALLEL=1, MAX_LOADED_MODELS=1); units active+enabled (`NRestarts=0`); bind and LAN posture; swap 0 B; uptime (no reboot); all weight/config/projector blobs; baked sampling; rick's entire plane.
- **What was tested:** TKV knowledge review; target identity (hostname/IP/host-key pin/sudo); drift check (11 items vs M4 frozen references); Modelfile hash verification both sides (3/3); alias creations with post-create digest + layer + params equality proofs; per-rung residency (digest, effective ctx, size_vram==size, PROCESSOR 100% GPU, per-GPU MiB, Forever); KV linearity (two derivations × two depth pairs); needle at ~95% of each rung ctx with the rung's own alias (fixture-valid, stop, found ×3); 3 known-answer spot checks per rung, flat across rungs (programmatic content comparison); link speed under load per rung; per-rung + full-window journal scans (Xid/OOM/err/fallback); repoint lint + manual functional test + unit restart (F-E4); operating-profile residency re-proof + quick re-proof; final state sweep.
- **Passed:** every mandatory test at all three rungs and the repoint — **32K PASS, 64K PASS, 128K PASS, freeze PASS, repoint + residency PASS.** **Failed:** no mandatory test. **Disclosed corrections (none concealed):** F-M7-1 digest-FROM rejection (first create attempt failed, root-caused, binding achieved and proven by equality); the needle calibration probe (one per ladder, disclosed); no test was re-run to reach a pass.
- **Installed/running:** binary == server 0.32.15; `ollama.service` active+enabled (`NRestarts=0`); `ollama-preload.service` active+enabled, last run `Result=success`.
- **Model identity/residency (end state):** operating profile `hx-muse-glimmer-64k:latest` digest `9dffb015…e7da` on frozen artifact `de878ce33ad8…64c1`; resident ctx 65536, 100% VRAM (`size_vram == size == 18,376,336,340 B`), Forever, both GPUs (10,618 + 9,388 MiB). In-store tags (tags only): `muse-glimmer:30b` (frozen source), `hx-muse-glimmer` (M4 working alias), `hx-muse-glimmer-32k` (`09c4f825…836e`), `hx-muse-glimmer-128k` (`17fe5b80…e85b`, qualified extended — found at 95.00%, not the default).
- **Endpoint/security state:** `*:11434` wildcard with loopback preserved (blueprint §5; LAN 192.168.50.0/24 is the boundary per owner D2; no host firewall); preload/fixtures use 127.0.0.1; no auth assumed beyond the LAN boundary (unchanged from M4).
- **Resource/performance state:** operating profile resident 17.11 GiB of 31.86 GiB aggregate (≈12.3 GiB headroom); 128K rung used 20,424 MiB under load (≈11.9 GiB headroom); cold prefill at ~95% depth 1,902 / 1,825 / 1,655 tok/s (32K/64K/128K); warm known-answer path 3.2–6.9 s; zero Xid/OOM all window.
- **Rollback readiness:** §13 — prior script/drop-in restorable from versioned hashes (full pre-change bytes in evidence and in the M4 report); rung aliases removable tags-only; every step reversible.
- **Remaining risks/decisions:** F-M7-1 (FROM-digest syntax limitation → KK3 record), F-M7-2 (scheduler sizing vs env override — capacity planning must use like-for-like), F-M7-3 (VRAM-default vs explicit sizing delta), carried F-E2/NVRM/LTR classes (rick's monitors). M5 (quality mapping with owner thresholds) may proceed against the resident -64k profile.
- **Budgets:** one session used; transient retry 0 (the digest-FROM 400 was a syntax rejection root-caused by source, not a model transient; no model test was re-run); no stop condition triggered; no escalation required.

## 17. Second Brain evaluation (standing directive)

1. Opportunity identified: **yes** — the hxs-1 ladder/profile pattern applied to Meta-X. 2. Roadmap capability/pattern: **hxs-1 ladder/profile pattern — third validated use** (uniformity claim now holds on the dense model on x8 links, the blueprint's hardest capacity case so far; its numbers were measured here, never transferred). 3. Disposition: **implemented** — the per-rung evidence and the three frozen aliases become Meta-X's catalog context profile at handoff. 4. Evidence/reasoning: §4–§7 measured table; the extended 128K profile qualified on the artifact's own max context with ≈11.9 GiB headroom.

## 18. Handoff

Deliverable `09-esme-m7-ladder-profiles.md` goes to **Carol** for catalog receipt; per the context packet, **handoff OPEN until the receipt is cited in the state log**. Sanitized session evidence retained transiently at `hxs-5:/tmp/esme-m7/evidence/` (volatile `/tmp`; this document carries the record): `00-identity`, `01-drift-check`, `02/02b-modelfile-local-sha`, `03-remote-fixture-sha`, `04/04b-alias-create`, `05-alias-show`, `06-manifest-equality`, `06b-params-blobs`, `07-spotcheck-sha`, `08-unload-pre-32k`, `09/09b-rung32k-residency+runner`, `10-needle-cal`, `11-rung32k-needle-link`, `12-rung32k-spot`, `13/13b-rung32k-journal`, `14-rung64k-residency`, `15-rung64k-needle-link`, `16-rung64k-spot-journal`, `16-prechange-files`, `17-rung128k-residency`, `18-rung128k-needle-link`, `18-repoint-candidate-sha`, `19-rung128k-spot-journal`, `20-repoint-deploy`, `21-restart-64k`, `22-repoint-residency`, `23-rung64k-compute-reproof`, `24-final-sweep`, `25-unit-untouched`, `preload.diff`, `hx3conf.diff`, `spot-*.json`, `needle-*.json`. Remote scratch `/tmp/esme-m7` on hxs-3 removed at cleanup; the local askpass helper, SSH wrappers, and pinned known_hosts are deleted at task end.

**Completion gate (profile §18):** knowledge reviewed and cited; target confirmed hxs-3; binary/server/model versions reconciled; tests defined from the work order before mutation; pre-change state captured; every change authorized, bounded, reversible; all mandatory tests executed and passed; GPU residency proven per rung and at end state; digests and effective context captured; security boundary verified not assumed; secrets and thinking content excluded; configs/diffs/command log/test report attached; summary describes the true current state; no unresolved uncertainty concealed; another engineer can reproduce from this package.

**Completion: `PASS — TASK COMPLETE`**

`Task May Proceed: YES`

---

Sanitization confirmed: no secrets, tokens, cookies, private prompts, user data, or thinking content in this document; all prompts synthetic; LAN addresses already ratified. The askpass helper and SSH wrappers were deleted at task end; remote scratch removed.
