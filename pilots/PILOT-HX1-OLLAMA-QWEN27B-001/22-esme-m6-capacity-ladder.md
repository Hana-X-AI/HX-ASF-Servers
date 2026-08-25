# Esme (john) — M6 Capacity Ladder: 65,536 and 131,072 Qualification Evidence (hxs-1)

| Field | Value |
| --- | --- |
| Report ID | ESME-M6-CAPACITY-LADDER-001 |
| Task ID | WO-HX1-JOHN-M6-001 (`PILOT-HX1-OLLAMA-QWEN27B-001`, milestone M6) |
| Agent | john / Esme (session `john-m6-20260825-01`) |
| Host | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic |
| Session host | `hxs-5` (192.168.50.204); all target actions over SSH `hxsa@192.168.50.200` |
| Window | 2026-08-25T03:19Z → 04:15Z (UTC) |
| Ollama | 0.32.15 (binary == server; unchanged from M4/M5/M5b) |
| Base model | `qwen3.8:27b` digest `22130167c4c2…79643` (unchanged) |
| GPUs | 2× RTX 4070 Ti SUPER 16376 MiB, driver 580.173.02 (rick's plane, untouched) |
| Owner directive | 2026-08-25 (Alert 1 EAM): 131,072 tested as part of the M6 capacity decision — all stages tested, results shown |

Evidence labels per plan §2.2: FACT / AUTHORITY / UPSTREAM / INFERENCE / RECOMMENDATION.
All secrets excluded; the SSH secret was used only through the askpass helper (0700, read the value from its owner-file at runtime, deleted at task end); it was never printed, logged, or stored. No secret-piping to sudo (`sudo -n`, F-M5-2). Thinking content is never retained as an audit artifact (A01 §5.2): every harness strips `message.thinking` immediately and persists only presence/character counts; this document contains zero thinking text.

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path resolves locally here, as in M4/M5/M5b)
Source: /opt/tkv-local/ollama
Reviewed At: 2026-08-25T03:19:57Z → 03:25Z
Relevant Files: 7 reviewed —
  ollama-main/docs/context-length.mdx (VRAM-based defaults 4k/32k/256k; OLLAMA_CONTEXT_LENGTH;
    verify PROCESSOR split via ollama ps)
  ollama-main/docs/modelfile.mdx:57,149 (PARAMETER num_ctx — the effective contract per PILOT-002)
  ollama-main/docs/faq.mdx:344-354 (Flash Attention; OLLAMA_KV_CACHE_TYPE default f16;
    KV quantization requires FA)
  ollama-main/envconfig/config.go:222,230,317,336 (OLLAMA_KV_CACHE_TYPE / OLLAMA_CONTEXT_LENGTH
    definitions — version-independent env surface)
  research/hx-research_qwen38-27b-inference-performance_third-party_2026-08-17 (class C claims:
    ~23.5 GiB resident @131K on a 24 GiB card; H1: <26 GiB @128K across both hxs-1 GPUs, hard
    failure at 29.98 GiB usable; prefill peak ~2,359 tok/s, ~72 s cold TTFT @120K)
  research/hx-research_qwen38-27b-ollama-serving-and-capability-fit_synthesis_2026-08-17
    (model card notes — UPSTREAM, not runtime evidence)
  (carried from the M5b receipt 19-esme-m5b-amendment-conformance.md §1: thinking.mdx,
    api/types.go, openai.go mapping, fixtures contract)
Authority/Version Identified: TKV source snapshot predates the installed 0.32.15 for the qwen3.8
  model family (carried gap: no qwen3.8 renderer in the snapshot). Empirical API evidence on the
  actual host is the authority for qwen3.8-specific behavior; snapshot source cited only where
  version-independent (env vars, docs).
Applicable Tests/Runbooks: work order 20 stage procedure; D8 thresholds (AUTHORITY, owner
  2026-08-25); plan 5.4 benchmark protocol; F-M5B-1 controlled unload; F-E4 preload
  restart-not-start; repo fixtures fixtures/ verified against sha256sums.txt before use (all OK).
Contradictions or Gaps:
  1. TKV snapshot has no qwen3.8 renderer/parser source (carried from M5b; disposition unchanged).
  2. The third-party 23.5 GiB@131K figure is a class C UPSTREAM claim; the context packet's
     ~23.5 GB @64K / ~27-28 GB @128K estimates are INFERENCE. Neither was assumed; both are
     superseded by the measurements in this report (actuals are lower: §3/§4).
Task May Proceed: YES
```

Teammate roster (profile §4.2): `agents/` contains john, kimi-k3, rick — all current. Target identity verified before any action: `hostname` = `hxs-1`, `hostname -I` = `192.168.50.200`, `sudo -n` OK (FACT, 03:26:34Z). Fixtures verified: `sha256sum -c fixtures/sha256sums.txt` → all 7 OK (03:19:57Z).

## 2. Base-artifact drift check (FACT) — FIRST, before any mutation

| Item | Frozen value (M5b) | Pre-change 03:26Z | Post-restore 04:08Z |
| --- | --- | --- | --- |
| Base `qwen3.8:27b` digest | `22130167c4c2…79643` | **match** | **match** |
| `ollama --version` / `/api/version` | 0.32.15 | 0.32.15 | 0.32.15 |
| Alias digest resident | `db2c62060efe…f645510`, ctx 32768, vram==size | **match** | **match** (restored, §6) |
| `hx1.conf` sha256 | `36af1c42…60f38` | match | **match** (restored, §6) |
| `hx-ollama-preload` sha256 | `79571d63…7262a` | match | match (never touched) |
| `ollama-preload.service` sha256 | `28c60c7d…52299` | match | match (never touched) |
| Units | both active+enabled | match | match |
| Listener | `127.0.0.1:11434` only | match | match |
| Swap used | 0 B | 0 B | 0 B (entire window) |
| Uptime | no reboot | 7 d 4:39 | 7 d 5:20 (continuous; no reboot) |

**NO DRIFT at entry; the stop rule was never triggered.** `NRestarts` note: M5b ended at `NRestarts=1` (the M5 R01 auto-restart); the three manual `systemctl restart ollama.service` in this session reset the counter — final value `NRestarts=0`, i.e. zero crash/automatic restarts all window (FACT).

## 3. Stage 1 — 65,536 (FACT)

### 3.1 Versioned config change

- Modelfile: Phase A byte-verbatim except `PARAMETER num_ctx 65536`. sha256 **`7593cb69dbabbe532c7f1c36e205d24de044c766d687754fcc1beada8a661ab2`** (verified identical on hxs-5 and hxs-1).
- `ollama create hx-qwen3.8-27b` (03:27:51Z) → new stage alias digest **`766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a`**. `ollama show` confirms `num_ctx 65536`, SYSTEM verbatim, native inherited parameters only — no sampling parameter introduced.
- Drop-in diff (one line): `OLLAMA_CONTEXT_LENGTH=32768` → `65536`. hx1.conf sha256 `36af1c42…60f38` → **`163003b16dbd2a88879e7febd9c3d3a3629b74977e85ff263ccab098a58d96c2`**. `OLLAMA_KV_CACHE_TYPE=f16` unchanged.
- daemon-reload → restart ollama → restart ollama-preload (F-E4) → controlled unload (keep_alive:0, authorized per-stage) → preload reload (RC=0, cold wall **12.23 s**).
- Reload-semantics note (FACT): because `num_ctx` changed, the first preload restart already re-created the runner under the new digest (F-M5B-1's no-swap case does not apply when num_ctx differs); the mandated controlled unload + preload reload was executed anyway and re-proved the digest.

### 3.2 Capacity proof — **PASS (f16)**

| Proof | Result |
| --- | --- |
| `/api/ps` digest | `766cd946…8cc99d8a` (new stage digest) |
| Effective context | 65,536 |
| Residency | `size_vram == size == 20,463,789,012 B` (19.06 GiB) — 100% GPU, zero fallback |
| `ollama ps` | `100% GPU`, CONTEXT 65536, Forever |
| Per-GPU VRAM | GPU0 11,502 / GPU1 11,888 MiB of 16,376 each |
| Needle probe @ ~95% | 62,255 prompt tokens = **95.0% of ctx**, `done_reason stop` (no truncation), needle **found** (`FALCON-61803` at line 1554/2390, 65% depth); cold prefill 1,103.9 tok/s; wall 58.3 s |
| Journal | zero Xid, zero OOM, zero ERROR-level lines in window; only known classes (F-E2 discovery watchdog; NVRM teardown assertions — §8) |
| Cold reload | preload RC=0 in 12.23 s |

Fixture calibration (disclosed, D-M6-2): attempt 1 (2313 lines) landed at 60,253 tokens (91.9%, below the [60948, 64800] window) — needle still found with `stop`; token density measured 26.05 tok/line; final run at 2390 lines. Attempt 1 is preserved in evidence (`needle-65536.json`); calibration is not a model re-run.

### 3.3 Quality re-run (D8) — **PASS**

| AC | Result | Verdict |
| --- | --- | --- |
| AC-009 | version 7 ms; ps digest/ctx/vram match; known-answer `391` (thinking ON, stop) | **PASS** |
| AC-010 recall@5 | 13/13 = 1.000 (≥0.9) | **PASS** |
| AC-011 groundedness | citations 14/14 = 100% (≥90%); no-answer 2/2; poison 1/1; Q16 30,009 tok, stop, correct; evaluator read all 16 answers in full — concur 16/16 | **PASS** |
| AC-012 tools | 52 audit events: 23 executed (100% schema-conformant), 6 denied, 2 timeout (bounded TC06), 1 duplicate-suppressed, 1 loop_limited; **forbidden/malformed executed: 0**; conformance 100% (≥95%) | **PASS** |
| AC-013 coding | 9/10 = 90% (≥80%) + evaluator review (all 10 genuine; `parse_kv` = same frozen-fixture contract mismatch as M5b F-M5B-5 — stands as measured, not re-run) | **PASS** |

EF04 (A01 §5.1, not a D8 case): raw grade `false` — model stopped **voluntarily** at `retry_budget_remaining: 0` after exactly 2 calls with a bounded failure report; same grader-correction class as M5b §7 (D-M6-3, raw output preserved). No model test was re-run or re-graded to reach any pass.

### 3.4 Benchmarks (plan 5.4; native defaults, thinking ON, concurrency 1)

| Metric | 65,536 f16 |
| --- | --- |
| Warm gen ×3 | 50.4 / 55.9 / 51.0 tok/s (decode incl. thinking) |
| Warm TTFT | thinking 0.214–0.330 s; content 6.25–12.14 s |
| Prefill (nested depths) | 11,025 tok @ 1,464.4; 30,918 @ 1,909.7; 46,821 @ 2,860.5; 61,736 @ 3,374.2 tok/s — **cache-assisted beyond first depth (F-M6-4)**; cold reference: 1,103.9 tok/s @ 62,255 (needle) |
| TTFT-content at depth | 8.27 s @11K; 17.25 s @31K; 28.85 s @47K; 19.59 s @61,736 (94.2% ctx) |
| Gen rate at depth | 86.3 @11K → 78.3 @31K → 67.1 @47K → 65.6 tok/s @62K |
| Cold reload | 12.23 s |
| RAM / swap | 11→10 Gi used / 0 B swap (no masking) |
| GPU telemetry (dmon) | GPU0 peak 193 W / 71 °C; GPU1 peak 204 W / 60 °C; SM util 100% peaks; no throttle events; VRAM 11,516/11,910 MiB |
| Processor split | 100% GPU throughout |

### 3.5 Stage 1 verdict

**CAPACITY PASS (f16); QUALITY PASS. f16 retained; q8_0 fallback not required.** Ladder proceeds to 131,072.

## 4. Stage 2 — 131,072 (FACT)

### 4.1 Versioned config change

- Modelfile: Phase A byte-verbatim except `PARAMETER num_ctx 131072`. sha256 **`b0d3fa6d4c5db44f0ae6e36beb1b4558472ebec27dc4313d98d577746eeae13d`** (verified both sides).
- `ollama create` (03:49:28Z) → new stage alias digest **`94b83a1efc3eb82a8009cfc735d59ee8ca28071b01fc4593e2e926ed0dad0260`**. `ollama show` confirms `num_ctx 131072`, native params only.
- Drop-in diff (one line): `OLLAMA_CONTEXT_LENGTH=65536` → `131072`. hx1.conf sha256 → **`3cb5d6a728c3aecfa8332a32d1e4ca312c22164d2e9132500f6a324e4e3aa172`**. KV stayed `f16`.
- daemon-reload → restart ollama → restart preload → controlled unload → preload reload.
- **Procedure correction within the step (evidence kept):** the first unload raced — `keep_alive:0` teardown is asynchronous, and the immediate preload reload (0.033 s) re-pinned the *stopping* runner to Forever (cancel-unload; F-M6-2). The sequence was then completed correctly: unload polled to `/api/ps` empty → cold reload RC=0 in **11.74 s** → polled until `expires_at` year-2318 (Forever). No model test was re-run; this was the mandated reload step completed properly.

### 4.2 Capacity proof — **PASS (f16)**

| Proof | Result |
| --- | --- |
| `/api/ps` digest | `94b83a1e…0dad0260` (new stage digest) |
| Effective context | 131,072 |
| Residency | `size_vram == size == 23,416,568,541 B` (21.81 GiB) — 100% GPU, zero fallback |
| `ollama ps` | `100% GPU`, CONTEXT 131072, Forever |
| Per-GPU VRAM | GPU0 14,298 / GPU1 14,248 MiB of 16,376 each (~4.4 GiB aggregate headroom) |
| Needle probe @ ~95% | 124,395 prompt tokens = **94.9% of ctx**, `done_reason stop` (no truncation), needle **found** (`FALCON-61803` at line 3107/4780, 65% depth); cold prefill 786.0 tok/s; wall 188.8 s |
| Journal | zero Xid, zero OOM; 81 NVRM teardown-assertion lines (known class, §8); one ERROR-level line — a **foreign client's** malformed request (F-M6-3, §8), not a serving fault |
| Cold reload | preload RC=0 in 11.74 s |

Memory-budget reconciliation (FACT vs prior estimates): the context packet's ~27–28 GB inference and the third-party ~23.5 GiB claim were both **pessimistic**; actual f16 residency at 131,072 is **23.42 GB (21.81 GiB)**. Empirical KV coefficient across the three rungs is exactly linear: **45,056 B/token f16** (Δ18,987,394,004 → 20,463,789,012 → 23,416,568,541). Extrapolation to 262,144 native ≈ 29.3 GB against ~29.98 GiB usable — INFERENCE only, not tested, and >131,072 remains unauthorized (work order).

### 4.3 Quality re-run (D8) — **PASS**

| AC | Result | Verdict |
| --- | --- | --- |
| AC-009 | version 6 ms; ps digest/ctx/vram match; known-answer `391` (thinking ON, stop) | **PASS** |
| AC-010 recall@5 | 13/13 = 1.000 (≥0.9) | **PASS** |
| AC-011 groundedness | citations 14/14 = 100% (≥90%); no-answer 2/2; poison 1/1; Q16 30,009 tok, stop, correct; evaluator read all 16 answers — concur 16/16 | **PASS** |
| AC-012 tools | 53 audit events: 24 executed (100% schema-conformant), 6 denied, 2 timeout (bounded TC06), 1 duplicate-suppressed, 1 loop_limited; **forbidden/malformed executed: 0**; conformance 100% (≥95%) | **PASS** |
| AC-013 coding | 9/10 = 90% (≥80%) + evaluator review (all 10 genuine; `parse_kv` same fixture mismatch — stands as measured) | **PASS** |

EF04: raw `false`, same voluntary-bounded-stop class (retries 2 ≤ budget, "retry_budget_remaining is now 0, so I'm not retrying further") — grader correction disclosed (D-M6-3).

### 4.4 Benchmarks (plan 5.4; native defaults, thinking ON, concurrency 1)

| Metric | 131,072 f16 |
| --- | --- |
| Warm gen ×3 | 47.6 / 51.6 / 47.5 tok/s |
| Warm TTFT | thinking 0.213–0.343 s; content 4.00–10.25 s |
| Prefill (nested depths) | 11,025 @ 1,461.0; 30,918 @ 1,905.9; 61,736 @ 1,830.5; 92,554 @ 2,038.4; 123,372 @ 2,137.1 tok/s — **cache-assisted beyond first depth (F-M6-4)**; cold reference: 786.0 tok/s @ 124,395 (needle) |
| TTFT-content at depth | 8.59 s @11K; 16.96 s @31K; 34.58 s @62K; 46.71 s @93K; **59.60 s @123,372 (94.1% ctx)** |
| Gen rate at depth | 88.4 @11K → 83.6 @31K → 69.6 @62K → 59.1 @93K → 48.5 tok/s @124K |
| Cold reload | 11.74 s |
| RAM / swap | 12→15 Gi used / 0 B swap (no masking) |
| GPU telemetry (dmon) | GPU0 peak 206 W / 74 °C; GPU1 peak 202 W / 61 °C; SM util 100% peaks; no throttle events; VRAM 14,300/14,250 MiB |
| Processor split | 100% GPU throughout |

### 4.5 Stage 2 verdict

**CAPACITY PASS (f16); QUALITY PASS. f16 retained; q8_0 fallback not required at either stage.**

## 5. Consolidated results matrix — 32,768 / 65,536 / 131,072

| Dimension | 32,768 (M5b frozen, re-proven) | 65,536 (M6) | 131,072 (M6, owner-directed) |
| --- | --- | --- | --- |
| Alias digest | `db2c6206…f645510` | `766cd946…8cc99d8a` | `94b83a1e…0dad0260` |
| Modelfile sha256 | `4869ce80…3165e` | `7593cb69…61ab2` | `b0d3fa6d…eae13d` |
| KV cache | f16 | f16 | f16 |
| Resident size | 18,987,394,004 B (17.68 GiB) | 20,463,789,012 B (19.06 GiB) | 23,416,568,541 B (21.81 GiB) |
| Residency | 100% GPU (vram==size) | 100% GPU (vram==size) | 100% GPU (vram==size) |
| Per-GPU MiB | 10,364 / 10,502 | 11,502 / 11,888 | 14,298 / 14,248 |
| Aggregate VRAM headroom | ~11.9 GiB | ~9.5 GiB | ~4.4 GiB |
| Needle @ ~95% ctx | 30,015 tok (91.6%), stop, found (M5b) | 62,255 tok (95.0%), stop, found | 124,395 tok (94.9%), stop, found |
| Prefill @ ~95% (cold unless noted; header corrected 2026-08-25 from "Cold prefill") | 1,911.5 tok/s @31,298 (cache-assisted, M5b) | 1,103.9 tok/s @62,255 (cold) | 786.0 tok/s @124,395 (cold) |
| Cold reload (preload wall) | ~12 s (M5b) | 12.23 s | 11.74 s |
| Warm gen tok/s ×3 | 51.6 / 51.8 / 53.5 | 50.4 / 55.9 / 51.0 | 47.6 / 51.6 / 47.5 |
| Warm TTFT-think | 0.215–0.347 s | 0.214–0.330 s | 0.213–0.343 s |
| Warm TTFT-content | 7.19–10.24 s | 6.25–12.14 s | 4.00–10.25 s |
| TTFT-content at deepest bench | 17.4 s @31K | 19.59 s @61,736 | 59.60 s @123,372 |
| Gen rate at deepest bench | ~53 tok/s class | 65.6 tok/s @62K | 48.5 tok/s @124K |
| RAM used / swap | 12 Gi / 0 B | 10–11 Gi / 0 B | 12–15 Gi / 0 B |
| GPU temp / power peaks | (M5b: not re-run here) | 71/60 °C, 193/204 W | 74/61 °C, 206/202 W |
| Xid / OOM / ERROR | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 1 (foreign 500, F-M6-3) |
| AC-009 | PASS | PASS | PASS |
| AC-010 recall@5 | 13/13 | 13/13 | 13/13 |
| AC-011 groundedness | 14/14 · 2/2 · 1/1 | 14/14 · 2/2 · 1/1 | 14/14 · 2/2 · 1/1 |
| AC-012 tools | 0 forbidden of 51 events; 100% | 0 forbidden of 52 events; 100% | 0 forbidden of 53 events; 100% |
| AC-013 coding | 9/10 + review | 9/10 + review | 9/10 + review |
| **Verdict** | frozen baseline (M5b PASS) | **CAPACITY PASS · QUALITY PASS (f16)** | **CAPACITY PASS · QUALITY PASS (f16)** |

Headline readings for the M6 decision (INFERENCE from the FACTs above): (1) capacity is not the binding constraint through 131,072 — f16 fits with ~4.4 GiB aggregate headroom, zero offload, zero Xid/OOM; (2) decode throughput is context-insensitive warm (~48–56 tok/s across rungs) and degrades at depth as expected (48.5 tok/s at 124K); (3) the real cost of 131,072 is cold-ingest latency: ~786 tok/s cold prefill at ~95% depth ⇒ ~158 s TTFT on a cold 124K-class prompt (59.6 s with prefix-cache assistance); (4) quality is flat — every D8 threshold passed identically at all three rungs, including needle retrieval at ~95% of each context.

## 6. End-state restoration (mandatory) — **PROVEN**

Executed 04:06:07–04:08:00Z: re-created the alias from the M5b-frozen Phase A Modelfile (sha256 `4869ce80…3165e`, verified byte-identical both sides) → alias digest reproduced **exactly** `db2c62060efe97e49931d30706874561492a83f5d8171ea8467a94e47f645510` (deterministic rebuild); hx1.conf restored to `OLLAMA_CONTEXT_LENGTH=32768` / `OLLAMA_KV_CACHE_TYPE=f16` — sha256 back to **`36af1c42…60f38`**; daemon-reload; restart ollama + preload; controlled unload polled to empty; preload reload RC=0 in 11.87 s, polled to Forever.

Final residency re-proof (04:07:34Z, re-verified 04:13Z): `/api/ps` digest `db2c6206…f645510`, `context_length 32768`, `size_vram == size == 18,987,394,004` (100% GPU), Forever; `ollama ps` 100% GPU 32768 Forever; GPUs 10,350/10,480 MiB; known-answer `391` with thinking ON, `done_reason stop`; both units active+enabled, preload `Result=success`; listener `127.0.0.1:11434` only; zero Xid/OOM across the whole M6 window; uptime continuous (no reboot).

**hxs-1 ends in the accepted M5b-frozen state.**

## 7. Sequential command log (profile §11.3)

Session host `hxs-5`, user `hxsa`; remote = SSH askpass wrapper (secret never on any command line; `sudo -n` only). Failures kept.

```text
 1 03:19:57 exit=0 [local] fixtures sha256sum -c sha256sums.txt → all OK; hostname=hxs-5; TKV present
 2 03:20-03:25 exit=0 [local] TKV reads: context-length.mdx, modelfile.mdx, faq.mdx,
    envconfig/config.go, research syntheses; roster check → [KNOWLEDGE REVIEW COMPLETE]
 3 03:25:40 exit=0 [local] mkdir /tmp/esme-m6 (0700); askpass helper + ssh/scp wrappers (0700);
    helper reads the secret from its owner-file at runtime (value never in the file)
 4 03:26:34 exit=0 ssh identity verify: hostname=hxs-1; hostname -I=192.168.50.200; sudo -n OK;
    no prior scratch
 5 03:26:54 exit=0 ssh drift check [evidence 01] — all frozen values match M5b; NO DRIFT
 6 03:27:35 exit=0 [local] author Modelfile-65536 (Phase A + num_ctx 65536); sha256 7593cb69…ab2;
    transfer; remote hash match
 7 03:27:51 exit=0 ssh ollama create → stage digest 766cd946…9d8a; ollama show verify (65536;
    native params only) [evidence 02]
 8 03:28:11 exit=0 ssh hx1.conf 32768→65536 (163003b1…96c2); daemon-reload; restart ollama;
    restart preload RC=0; ps shows new digest (num_ctx change forced runner re-create) [evidence 03]
 9 03:29:31 exit=0 ssh controlled unload → ps empty; preload reload RC=0 12.23 s; residency proof:
    766cd946, 65536, vram==size 20,463,789,012, 100% GPU, Forever, 11,502/11,888 MiB [evidence 04]
10 03:31:00 exit=0 ssh journal scan stage 1: no Xid/OOM/ERROR; F-E2 watchdog + NVRM teardown
    classes; preload 'signal' line found → investigated (F-M6-1: Requires= propagation race,
    sudo-audit-trailed to my own scripted restart; benign) [evidence 05]
11 03:33:30 exit=0 ssh needle probe 65536 attempt 1: 60,253 tok (91.9% — below window; needle
    found, stop) — fixture calibration, kept [evidence 06]
12 03:35:47 exit=0 ssh needle probe 65536 final: 62,255 tok (95.0%), stop, FALCON-61803 found,
    prefill 1,103.9 tok/s cold [evidence 07]
13 03:36:00 exit=0 scp fixtures (rag/tool/coding suites); sed re-point scratch paths only (D-M6-1);
    executed-copy hashes recorded
14 03:36:20 exit=0 ssh AC-009 quick re-proof PASS [evidence 08]
15 03:36:40 exit=0 ssh rag_suite.py → recall 13/13; groundedness 14/14; 2/2; 1/1; Q16 30,009 tok
    stop [evidence 09]; evaluator full-read concur 16/16 [evidence 10]
16 03:41:24 exit=0 ssh tool_suite.py → TC01-TC10 handled; 0 forbidden; EF04 raw false
    (voluntary stop; D-M6-3) [evidence 11/12]
17 03:43:36 exit=0 ssh coding_suite.py → 9/10 (parse_kv fixture mismatch); evaluator review
    concur 10/10 authentic [evidence 13/14/15]
18 03:45:32 exit=0 ssh bench 65536 (warm×3; prefill 11/31/47/62K; dmon; RAM/swap; split)
    [evidence 16 + dmon-65536.log]
19 03:49:28 exit=0 [local+ssh] Modelfile-131072 sha256 b0d3fa6d…ae13d; create → digest
    94b83a1e…0260; show verify (131072; native params only) [evidence 17]
20 03:49:53 exit=0 ssh hx1.conf →131072 (3cb5d6a7…a172); daemon-reload; restarts; ps new digest;
    controlled unload RACED (async teardown re-pinned by immediate reload; F-M6-2) [evidence 18]
21 03:51:41 exit=0 ssh reload completed correctly: unload polled to empty; preload reload RC=0
    11.74 s; Forever re-proof: 94b83a1e, 131072, vram==size 23,416,568,541, 100% GPU [evidence 19]
22 03:52:30 exit=0 ssh journal scan stage 2: 0 Xid / 0 OOM; 81 NVRM teardown lines (known class);
    F-E2 watchdog [evidence 20]
23 03:53:07 exit=0 ssh needle probe 131072: 124,395 tok (94.9%), stop, FALCON-61803 found,
    prefill 786.0 tok/s cold, wall 188.8 s [evidence 21]
24 03:56:40 exit=0 ssh AC-009 + rag_suite at 131072 → all PASS [evidence 22/23]
25 03:58:05 exit=0 ssh tool_suite + coding_suite at 131072 → 0 forbidden; 9/10; EF04 same class
    [evidence 24/26/27]
26 04:01:44 exit=0 ssh bench 131072 (warm×3; prefill 11/31/62/93/124K; dmon; RAM/swap; split)
    [evidence 25 + dmon-131072.log]
27 04:02-04:05 exit=0 [local] dmon summaries; foreign-client investigation (F-M6-3): GIN timeline
    proves zero overlap with timed runs; interactive SSH sessions from 192.168.50.220 identified
28 04:06:07 exit=0 [local+ssh] restore: frozen Phase A Modelfile (4869ce80…165e) → create →
    digest db2c6206…f645510 reproduced exactly [evidence 28]
29 04:06:31 exit=0 ssh hx1.conf →32768 (36af1c42…60f38); restarts; polled unload+reload
    (11.87 s); full residency re-proof [evidence 29]
30 04:08:00 exit=0 ssh final verify: known-answer 391; units active+enabled; listener loopback;
    0 Xid/OOM all window; single ERROR line = foreign 500 (explained) [evidence 30/31]
31 04:11:00 exit=0 scp evidence JSONs → hxs-5 transient; ssh rm -rf /tmp/esme-m6 (remote scratch
    removed; verified)
32 04:13:00 exit=0 ssh final ps re-check: restored state holds (db2c6206, 32768, vram==size,
    Forever) [evidence 31]
33 (task end) exit=0 [local] write deliverable 22-esme-m6-capacity-ladder.md; delete askpass
    helper + wrappers (verified)
```

## 8. Configuration files (profile §11.2)

Created/modified this milestone (all versioned, all reverted at end state):

| Artifact | Pre | During | Post (restored) |
| --- | --- | --- | --- |
| Modelfile (alias source) | Phase A `4869ce80…3165e` | 65536: `7593cb69…61ab2`; 131072: `b0d3fa6d…eae13d` (diff: num_ctx line only, each) | Phase A `4869ce80…3165e` (byte-identical) |
| `hx1.conf` drop-in | `36af1c42…60f38` (32768/f16) | 65536: `163003b1…8d96c2`; 131072: `3cb5d6a7…3aa172` (diff: OLLAMA_CONTEXT_LENGTH line only) | `36af1c42…60f38` (32768/f16) |
| Alias digest | `db2c6206…f645510` | `766cd946…9d8a` → `94b83a1e…0260` | `db2c6206…f645510` (reproduced) |

No unit, preload-script, base-tag, OS, driver, network, or firewall change. No sampling parameter introduced at any stage (verified via `ollama show` after each create). Harness executed-copy sha256 (on hxs-1; differ from repo fixture hashes only by the disclosed scratch-path re-point D-M6-1): bench_m6.py `745d50fb…8f6bf8d` (new M6 scaffolding, parameterized depths only — derived from fixture bench.py), coding_suite.py `d512b42d…45c3f02`, fixtures_corpus.py `8df5f031…732a01` (byte-identical to repo fixture), needle_probe.py `42ed2fab…043226` (new M6 scaffolding, parameterized depth), rag_suite.py `266ae8d6…a97ecd`, tool_suite.py `dce581c5…4dfa55`. Session evidence (sanitized) retained transiently at `hxs-5:/tmp/esme-m6/` (volatile; the deliverable carries the numbers); remote scratch removed.

Rollback path: end-state restoration WAS the rollback and it is proven (§6). Every stage change was a versioned, reversible config change.

## 9. Findings, risks, decisions surfaced

- **F-M6-1 (Requires= propagation race, FACT):** `systemctl restart ollama.service` stop/starts `ollama-preload.service` via `Requires=` while the API listener is still down (~38 s this session — the F-E2 GPU-discovery watchdog delays listener readiness on this host); the preload's bounded retries absorb the outage, and a subsequent explicit preload restart SIGTERMs the in-flight instance → journal shows `Failed with result 'signal'`. Benign and fully sudo-audit-trailed to the scripted restarts. RECOMMENDATION → KK3/monitors: treat this class as expected during service restarts; do not alert on a single 'signal' result for ollama-preload in a restart window.
- **F-M6-2 (unload is asynchronous, FACT):** a `keep_alive=-1` load request landing during `keep_alive:0` teardown re-pins the stopping runner (cancel-unload; `ollama ps` shows `Stopping...` then Forever). The mandated digest-swap unload must **poll `/api/ps` to empty** before reloading and poll for Forever after — procedure corrected in-session and applied to stage 2 and the restore. Extends F-M5B-1 reload semantics; monitors asserting digest identity need the same polling discipline.
- **F-M6-3 (foreign local client during stages, FACT → risk):** interactive SSH sessions on hxs-1 from 192.168.50.220 (pts/0 since 01:12, pts/1 since 03:53) interleaved `/api/chat` traffic with the stage windows (bursts 03:47:44–03:53:34 and after 04:08), including one malformed request (HTTP 500 "no user query found" — the window's only ERROR-level line). The GIN request log proves **zero overlap with any timed measurement** (NUM_PARALLEL=1 serializes; my probes/suites ran in clean windows). Loopback is a boundary, not authentication: any local process can drive the model. RECOMMENDATION → KK3: coordinate an exclusive qualification window for M7 (soak) — a concurrent long request would distort soak telemetry and could mask as capacity signals.
- **F-M6-4 (bench prefill cache assistance, FACT):** the nested filler prompts share prefixes, so depths beyond the first are prompt-cache-assisted (rates up to 3,374 tok/s @62K and 2,137 tok/s @124K are NOT cold); cold references are the needle probes (1,103.9 @62,255; 786.0 @124,395). M5b's 31K bench number carried the same class of assistance, so cross-stage comparability is preserved. Label on all future plan-5.4 tables.
- **F-M6-5 (KV math, FACT):** f16 KV cost is exactly linear at 45,056 B/token across the three rungs; 131,072 f16 residency is 23.42 GB — below both the packet inference (~27–28 GB) and the third-party class-C claim (~23.5 GiB @131K on one 24 GiB card; on hxs-1's pair the actual split is ~14.3/14.2 GiB). 262,144-native extrapolation ≈ 29.3 GB vs ~29.98 GiB usable — INFERENCE, untested, and >131,072 remains unauthorized.
- **F-M6-6 (carried, unchanged):** F-E2 discovery watchdog on cold runner starts; NVRM `iovaspaceDestruct`/`pIOVAS` assertions at runner teardown (81 lines stage 2 — same class as M4 F-E3 / F-M5B-2; not an Xid; → rick's plane, monitor only); `parse_kv` fixture-contract mismatch (F-M5B-5) recurred identically at both stages — 9/10 stands as measured.
- **D-M6-1 (fixture path re-point):** executed suite copies re-pointed `/tmp/esme-m5b` → `/tmp/esme-m6` via sed (scaffolding paths only; semantics untouched); hashes recorded in §8. Repo fixture bytes verified against `sha256sums.txt` before use.
- **D-M6-2 (needle fixture calibration):** stage needle documents scaled by the measured 26.05 tok/line; the undersized first 65536 attempt (60,253 tok) is preserved as evidence; calibration is not a model re-run.
- **D-M6-3 (EF04 grader correction):** at both stages the model stopped voluntarily at budget 0 with a bounded failure report — a stricter satisfaction of A01 §5.1 than the grader's forced-stop path; raw outputs preserved; no re-run, no re-grade to reach a pass.

## 10. Boundary statements (A01 §5.2, §5.3)

**Thinking-retention:** thinking content is nowhere retained — every harness strips `message.thinking` and persists only presence/counts; this document contains zero thinking text. Retained: task inputs, tool calls/results (JSONL audit), answers, telemetry, grading decisions — the A01 §5.2 retain list.

**Vision:** no image/audio/multimodal input was exercised anywhere in this milestone (all requests text-only); the vision projector remains out of the baseline pending its separate gate.

**Context ceiling:** nothing above 131,072 was configured or requested; 262K/1M remain reference-only (A01 §4.3). No soak/long-idle test was run (M7 scope). The frozen 32K acceptance evidence was not modified.

## 11. Validation summary (profile §11.4)

- **What changed (during the milestone only):** the alias was rebuilt twice for the ladder (65,536 → digest `766cd946…9d8a`; 131,072 → `94b83a1e…0260`) and the drop-in's `OLLAMA_CONTEXT_LENGTH` moved with it; **end state restored exactly** to the M5b-frozen 32K Phase A baseline (Modelfile `4869ce80…3165e`, digest `db2c6206…f645510`, hx1.conf `36af1c42…60f38` at 32768/f16).
- **What did not change:** base digest `22130167c4c2…79643`; Ollama 0.32.15 (binary == server); preload script/unit hashes; units active+enabled; loopback-only bind; swap 0 B used all window; system uptime (no reboot); rick's entire plane; the frozen 32K acceptance evidence.
- **What was tested:** drift check; per stage — versioned config change, reload with F-M5B-1 controlled unload, capacity proof (digest, effective ctx, size_vram==size, processor split, ~95%-depth needle with stop+found, journal scan, per-GPU allocation, cold reload timing), D8 suites AC-009/010/011/012/013, plan-5.4 benchmarks; then full end-state restoration with residency re-proof.
- **Passed:** every mandatory test at both stages — 65,536 CAPACITY PASS / QUALITY PASS; 131,072 CAPACITY PASS / QUALITY PASS (all f16; q8_0 never needed). **Failed:** no mandatory test. **Disclosed corrections (none concealed):** 65536 needle attempt-1 fixture calibration (§3.2); EF04 grader criterion at both stages (D-M6-3); the raced unload completed correctly (F-M6-2); parse_kv counted as measured (9/10).
- **Installed/running:** binary == server 0.32.15; both units active+enabled; `NRestarts=0` (no auto-restarts all window).
- **Model identity/residency (end state):** Phase A digest `db2c6206…f645510` on base `22130167c4c2…79643`; resident ctx 32768, 100% GPU (size_vram == size == 18,987,394,004 B), Forever, both GPUs.
- **Endpoint/security state:** `127.0.0.1:11434` only (verified pre/post); a foreign local client used the API during the window (F-M6-3) — reported, with proof of zero measurement overlap.
- **Resource/performance state:** see §5 matrix — f16 fits through 131,072 with ~4.4 GiB headroom; decode ~48–56 tok/s warm; cold 124K-class ingest ~158 s TTFT.
- **Rollback readiness:** demonstrated live — the end-state restoration is the rollback and it is proven (§6).
- **Remaining risks/decisions:** F-M6-1 (preload 'signal' class → monitors), F-M6-2 (poll-to-empty unload discipline → procedures/monitors), F-M6-3 (exclusive qualification window for M7; loopback ≠ authentication), F-M6-4 (cache-assist labeling on plan-5.4 tables), F-M6-5 (KV coefficient 45,056 B/token; 262K extrapolation is inference-only and unauthorized), carried F-E2/NVRM (rick), parse_kv fixture defect (→ KK3 fixture decision). The M6 freeze decision itself is KK3's gate.
- **Budgets:** one session used; transient retry **0 of 1** used for model transients (the needle attempt-1 was my own fixture calibration, disclosed; the reload race was a procedure completion, not a test retry); no stop condition triggered; no escalation required.

**Completion: `PASS — TASK COMPLETE`** (final gate §18: every applicable question answered yes; all corrections, calibrations, and the foreign-client finding disclosed; no mandatory-test failure concealed; end state restored and proven).

---

Sanitization confirmed: no secrets, tokens, cookies, private prompts, user data, or thinking content in this document; all prompts synthetic; LAN addresses already ratified in plan §3. The askpass helper and SSH wrappers were deleted at task end; remote scratch removed.
