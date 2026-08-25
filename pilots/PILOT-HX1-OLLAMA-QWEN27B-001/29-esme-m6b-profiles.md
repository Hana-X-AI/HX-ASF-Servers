# Esme (john) — M6b Context Profiles: Named Aliases + 64K Operating Default (hxs-1)

| Field | Value |
| --- | --- |
| Report ID | ESME-M6B-PROFILES-001 |
| Task ID | WO-HX1-JOHN-M6B-001 (`PILOT-HX1-OLLAMA-QWEN27B-001`, milestone M6b) |
| Agent | john / Esme (session `john-m6b-20260825-01`) |
| Host | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-28-generic |
| Session host | `hxs-5` (192.168.50.204); all target actions over SSH `hxsa@192.168.50.200` |
| Window | 2026-08-25T05:00:14Z → 05:12Z (UTC) |
| Ollama | 0.32.15 (binary == server; unchanged from M4/M5/M5b/M6) |
| Base model | `qwen3.8:27b` digest `22130167c4c2…79643` (unchanged) |
| Governing decision | `23-kk3-m6-capacity-decision.md` **Revision 2** (owner directive 2026-08-25): three qualified context profiles |
| GPUs | 2× RTX 4070 Ti SUPER 16376 MiB, driver 580.173.02 (rick's plane, untouched) |

Evidence labels per plan §2.2: FACT / AUTHORITY / UPSTREAM / INFERENCE / RECOMMENDATION.
All secrets excluded; the SSH secret was used only through the askpass helper (0700, reads the value from its owner-file at runtime, deleted at task end); it was never printed, logged, or stored. No secret-piping to sudo (`sudo -n`, F-M5-2). Thinking content is never retained as an audit artifact (A01 §5.2): only presence/character counts were recorded; this document contains zero thinking text.

**Precision rule (owner-mandated wording, Revision 2):** the ladder evidence proves that 131,072 caused **no measured accuracy regression in the needle test and the D8 suites** — not that 128K can never affect accuracy across every workload. All claims in this deliverable use this sentence's scope.

**Host identity declaration (Revision 2):** HX-1 (pilot project designation) and `hxs-1` (authoritative hostname, 192.168.50.200) are the same machine. All host-scoped assertions herein refer to `hxs-1`.

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path resolves locally here, as in M4/M5/M5b/M6)
Source: /opt/tkv-local/ollama
Reviewed At: 2026-08-25T05:00:14Z → 05:03Z
Relevant Files: 6 reviewed —
  ollama-main/docs/modelfile.mdx:57,149 (PARAMETER num_ctx — the effective contract per PILOT-002)
  ollama-main/docs/context-length.mdx (VRAM-based defaults 4k/32k/256k; OLLAMA_CONTEXT_LENGTH;
    verify PROCESSOR split via ollama ps)
  ollama-main/envconfig/config.go:126,131,230,275,277 (OLLAMA_KEEP_ALIVE / OLLAMA_CONTEXT_LENGTH /
    OLLAMA_NUM_PARALLEL / OLLAMA_MAX_LOADED_MODELS — version-independent env surface)
  ollama-main/server/routes.go:1229-1280 (DeleteHandler: m.Remove() then m.RemoveLayers())
  ollama-main/manifest/manifest.go:61-110 (Remove deletes the tag manifest + prunes; RemoveLayers
    deletes ONLY blobs not referenced by any other manifest → `ollama rm <tag>` is tags-only in
    effect when layers are shared — the bare-alias retirement safety basis)
  (carried from M5b/M6 receipts: thinking.mdx, api/types.go, faq.mdx keep_alive/unload semantics;
   qwen3.8 renderer gap unchanged)
Authority/Version Identified: TKV source snapshot predates the installed 0.32.15 for the qwen3.8
  model family (carried gap: no qwen3.8 renderer in the snapshot). Env/manifest semantics cited are
  version-independent; empirical API evidence on the actual host is the authority for qwen3.8-specific
  behavior.
Applicable Tests/Runbooks: work order 27 sequence; frozen references per 19/22; F-M5B-1/F-M6-2
  unload discipline (poll /api/ps to empty); F-E4 preload restart-not-start; D8 AC-009 quick re-proof.
Contradictions or Gaps:
  1. TKV snapshot has no qwen3.8 renderer/parser source (carried; disposition unchanged — empirical
     probes are the authority; not exercised this milestone).
Task May Proceed: YES
```

Teammate roster (profile §4.2): `agents/` contains john, kimi-k3, rick, carol — all current (carol added per the 2026-08-25 documentation-steward amendment; no task dependency this milestone). Target identity verified before any action: `hostname` = `hxs-1`, `hostname -I` = `192.168.50.200`, `sudo -n` OK (FACT, 05:03:23Z).

## 2. Drift check (FACT) — FIRST, before any mutation

Executed 05:03:43Z against the frozen references:

| Item | Frozen value (M5b/M6 end state) | Observed 05:03:43Z | Verdict |
| --- | --- | --- | --- |
| Base `qwen3.8:27b` digest | `22130167c4c2…79643` | `22130167c4c2…79643` (size 17,741,872,154) | **match** |
| Resident identity | `hx-qwen3.8-27b:latest` `db2c6206…f645510`, ctx 32768 | identical; `size_vram == size == 18,987,394,004`; Forever | **match** |
| `ollama --version` / `/api/version` | 0.32.15 | 0.32.15 / 0.32.15 | **match** |
| `hx1.conf` sha256 | `36af1c42…60f38` | `36af1c42…60f38` | **match** |
| `hx-ollama-preload` sha256 | `79571d63…7262a` | `79571d63…7262a` | **match** |
| `ollama-preload.service` sha256 | `28c60c7d…52299` | `28c60c7d…52299` | **match** |
| Units | both active+enabled | both active+enabled; `NRestarts=0` | **match** |
| Listener | `127.0.0.1:11434` only | `127.0.0.1:11434` only | **match** |
| Swap used | 0 B | 0 B | **match** |
| Uptime | no reboot | 1 wk 6:15 (continuous from M6's 7 d 5:20) | **match** |

**NO DRIFT — the stop rule was not triggered.** Situational note (F-M6-3 carried): the two interactive SSH sessions from 192.168.50.220 (pts/0 since 01:12, pts/1 since 03:53) were still present; no foreign API traffic occurred during this milestone's window (journal §8).

## 3. The three profile aliases (FACT) — byte-exact Modelfiles, digest-verified

Modelfiles: the frozen byte-exact Phase A family (Phase A content otherwise unchanged; **no sampling parameters**). Local source copies hash-verified, transferred, and remote hashes re-verified identical on both sides before any `ollama create`:

| Profile | Alias | Modelfile sha256 (frozen) | Remote verify |
| --- | --- | --- | --- |
| 32K recovery baseline | `hx-qwen3.8-27b-32k` | `4869ce80…3165e` | **match** |
| 64K operating default | `hx-qwen3.8-27b-64k` | `7593cb69…61ab2` | **match** |
| 128K extended (selected) | `hx-qwen3.8-27b-128k` | `b0d3fa6d…eae13d` | **match** |

Creations (05:04:44Z) and digest verification against the frozen references (`/api/tags`):

| Alias | Created digest | Frozen reference | Verdict |
| --- | --- | --- | --- |
| `hx-qwen3.8-27b-32k:latest` | `db2c62060efe97e49931d30706874561492a83f5d8171ea8467a94e47f645510` | `db2c6206…f645510` | **MATCH** |
| `hx-qwen3.8-27b-64k:latest` | `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a` | `766cd946…8cc99d8a` | **MATCH** |
| `hx-qwen3.8-27b-128k:latest` | `94b83a1efc3eb82a8009cfc735d59ee8ca28071b01fc4593e2e926ed0dad0260` | `94b83a1e…0dad0260` | **MATCH** |

**NO DRIFT on any creation.** The 32K alias digest is byte-identical to the (then-resident) bare alias digest — the same Phase A manifest content under a profile name, as designed.

`ollama show` per alias (FACT): `num_ctx` 32768 / 65536 / 131072 respectively; inherited native parameters only (temperature 1, top_p 0.95, top_k 20, min_p 0, presence_penalty 0, repeat_penalty 1, draft_num_predict 4) — no sampling parameter introduced. `ollama show --modelfile hx-qwen3.8-27b-64k` confirms the Phase A SYSTEM prompt verbatim, `TEMPLATE {{ .Prompt }}`, `RENDERER qwen3.8`, `PARSER qwen3.5`.

## 4. Preload contract repoint (FACT) — versioned edits

### 4.1 `/usr/local/libexec/hx-ollama-preload` — one-line diff

```diff
-MODEL="hx-qwen3.8-27b"
+MODEL="hx-qwen3.8-27b-64k"
```

The `/api/ps` assertion (`grep -q "\"name\":\"$MODEL:"`) is parameterized by `$MODEL`, so the exact-model load **and** the residency assertion repoint together with this single line. sha256 `79571d63…7262a` → **`01c2a096e5b416f33d95d25c01af30a94845877ded4e95ce21ee5aea3c9b29f2`** (new). Ownership/mode unchanged: root:root 0755 (installed via `sudo install -o root -g root -m 0755`). Lint: `sh -n`, `bash -n`, `dash -n` all PASS on the candidate **and** on the installed copy; `shellcheck` unavailable (carried limitation F-E6; the manual functional test is the real gate).

### 4.2 `/etc/systemd/system/ollama.service.d/hx1.conf` — one-line diff

```diff
-Environment="OLLAMA_CONTEXT_LENGTH=32768"
+Environment="OLLAMA_CONTEXT_LENGTH=65536"
```

Operator-consistency only — the Modelfile remains the effective contract (PILOT-002). sha256 `36af1c42…60f38` → **`163003b16dbd2a88879e7febd9c3d3a3629b74977e85ff263ccab098a58d96c2`**, which is byte-identical to the M6 stage-1 drop-in content (cross-check against `22-esme-m6-capacity-ladder.md` §3.1 — PASS). root:root 0644. `OLLAMA_KV_CACHE_TYPE=f16` and all other lines unchanged. `daemon-reload` executed (05:06:58Z); effective environment verified via `systemctl show ollama -p Environment`: `OLLAMA_CONTEXT_LENGTH=65536` (FACT).

### 4.3 Untouched

`ollama-preload.service` sha256 `28c60c7d…52299` — unchanged (verified post-deploy).

## 5. Bare-alias retirement (FACT) — tags only

Executed 05:07:31Z, after all three profile aliases verified: `ollama rm hx-qwen3.8-27b` → `deleted 'hx-qwen3.8-27b'`.

Proof of tags-only effect (semantics per version-independent snapshot source `routes.go:1229` → `manifest.go:74-110` — RemoveLayers deletes only blobs unreferenced by any remaining manifest; all layers are shared):

- `/api/tags` post-rm: exactly `hx-qwen3.8-27b-32k` / `-64k` / `-128k` / `qwen3.8:27b` — all four digests **unchanged** from §3.
- Weights blob `sha256-f5f1dd89…2ad57d` (16,810,714,464 B) present before and after (`sudo ls`, both captures in evidence).
- Manifests directory post-rm: `hx-qwen3.8-27b` gone; `hx-qwen3.8-27b-32k`, `hx-qwen3.8-27b-64k`, `hx-qwen3.8-27b-128k`, `qwen3.8` intact. **Base tag never touched; no blob deleted.**

**Inverse (rollback, recorded):** `ollama create hx-qwen3.8-27b -f ./Modelfile-32768` (Phase A Modelfile, sha256 `4869ce80…3165e`) → digest reproduces exactly `db2c62060efe…f645510` (deterministic rebuild, already proven at M6 §6). The naming ambiguity the owner flagged is eliminated: only profile-named aliases and the upstream base tag remain.

## 6. Switch to the 64K operating profile (FACT)

Sequence per work order (05:07:57 → 05:08:34Z):

1. `sudo systemctl restart ollama` (05:07:57Z) → polled `/api/ps`: API up at poll 2, **models=0** (F-M6-2 empty-proof discipline; the service stop performed the teardown — no client `keep_alive:0` was needed).
2. The `Requires=ollama.service` propagation ran the edited preload via the unit during the restart window: one info-level `curl: (7)` connect retry while the listener was still coming up (F-M6-1 class — bounded retry absorbed it), then **`hx-ollama-preload: OK - hx-qwen3.8-27b-64k resident`** at 05:08:07Z (~10 s cold load inside the unit window).
3. **Manual non-reboot test** of the edited script (05:08:15Z): `sudo /usr/local/libexec/hx-ollama-preload` → RC=0, `OK - hx-qwen3.8-27b-64k resident` (0.014 s — asserted against the already-resident runner). The M4 gate ("manual functional test is the real gate") is satisfied on the edited script.
4. `sudo systemctl restart ollama-preload` (05:08:34Z — **restart, not start**, F-E4) → RC=0, `Result=success`, `active (exited)`, journal `OK - hx-qwen3.8-27b-64k resident`.

## 7. Operating-profile residency proof (FACT, 05:08:34Z)

| Proof | Result |
| --- | --- |
| `/api/ps` name | `hx-qwen3.8-27b-64k:latest` |
| `/api/ps` digest | `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a` — **frozen 64K reference, exact** |
| `context_length` | **65,536** |
| Residency | `size_vram == size == 20,463,789,012 B` (19.06 GiB) — 100% GPU, zero fallback; identical to the M6 stage-1 measurement |
| `expires_at` | `2318-12-05T…` (keep_alive=-1, Forever; polled per F-M6-2) |
| `ollama ps` | `100% GPU`, CONTEXT 65536, Forever |
| Per-GPU VRAM | GPU0 **11,502** / GPU1 **11,888** MiB of 16,376 each — identical to M6 stage-1 |
| Units | both active+enabled; `NRestarts=0`; preload `Result=success` |
| Listener | `127.0.0.1:11434` only |
| Swap / uptime | 0 B used; continuous (no reboot) |

## 8. Known-answer + AC-009 quick re-proof (FACT, 05:08:55Z) — **PASS**

- `/api/version`: 0.32.15, 6 ms.
- `/api/ps` identity/digest/ctx/vram assertions: per §7 — all match.
- Known-answer (`17 × 23`, native Phase A defaults, thinking ON): content **`391`**, thinking present (130 chars), `done_reason stop`, 1.01 s wall, eval 68 tokens, zero `<think>` leakage into content.

## 9. Journal state (FACT, window 05:03:00Z → 05:12Z)

- **Zero Xid, zero OOM, zero NVRM kernel lines** in the window (the runner teardown at the service restart produced no NVRM assertions this time).
- **Zero error-level journal lines** for `ollama`/`ollama-preload` and system-wide (`journalctl -p err` → "No entries"). Disclosure (F-M6B-3): my first count form (`-p err | wc -l` → 1) counted the `-- No entries --` banner itself; the direct query proves zero error-level entries. Method note recorded.
- One **info-priority** line: `curl: (7) Failed to connect … port 11434` at 05:07:57 — the F-M6-1 preload-vs-listener race during the mandated restart; absorbed by the script's bounded retry; `OK` 10 s later. Not a serving fault.
- No foreign-client API traffic in the window (F-M6-3 sessions idle).

## 10. Ratified 128K harness requirements (AUTHORITY — recorded only; NO client build in this milestone)

Per `23-kk3-m6-capacity-decision.md` Revision 2 (owner-ratified 2026-08-25), for the `hx-qwen3.8-27b-128k` profile's future client harness:

1. **First-content timeout** comfortably above the measured ~158 s cold deep-ingest — initially **240 s**; **total request timeout** sized for ingest + reasoning + generation.
2. **Progress telemetry** so slow ingestion is not misclassified as a hung model.
3. **Admission control** preventing concurrent deep-context requests from consuming the remaining VRAM margin (server side already serialized: `OLLAMA_NUM_PARALLEL=1`, `OLLAMA_MAX_LOADED_MODELS=1`).
4. **Warm-cache and cold-cache latency tracked separately.**

Recorded as ratified requirements. No harness/client was designed, built, or tested in this milestone (work-order boundary).

## 11. Sequential command log (profile §11.3)

Session host `hxs-5`, user `hxsa`; remote = SSH askpass wrapper (secret never on any command line; `sudo -n` only). Failures and corrections kept.

```text
 1 05:00:14 exit=0 [local] hostname=hxs-5; date; TKV dir present
 2 05:00:14 exit=0 [local] sha256sum Modelfile-32768/65536/131072 → 3/3 frozen hashes match
 3 05:00-05:03 exit=0 [local] TKV reads: modelfile.mdx, context-length.mdx, envconfig/config.go,
    routes.go DeleteHandler, manifest.go Remove/RemoveLayers; roster check → [KNOWLEDGE REVIEW COMPLETE]
 4 05:03:0x exit=0 [local] mkdir /tmp/esme-m6b (0700); askpass helper + ssh/scp wrappers (0700);
    helper reads the secret from its owner-file at runtime (value never in the file)
 5 05:03:23 exit=0 ssh identity verify: hostname=hxs-1; hostname -I=192.168.50.200; sudo -n OK;
    uptime continuous [evidence 00]
 6 05:03:43 exit=0 ssh drift check [evidence 01] — all frozen references match; NO DRIFT
 7 05:04:05 exit=0 ssh capture pre-change preload script + hx1.conf/unit content [evidence 02]
 8 05:04:44 exit=0 scp 3 Modelfiles; remote sha256 3/3 frozen match [evidence 03]
 9 05:04:44 exit=0 ssh ollama create ×3 → digests db2c6206…f510 / 766cd946…9d8a / 94b83a1e…0260
    == frozen references [evidence 04]
10 05:04:5x exit=0 ssh ollama show ×3 (num_ctx 32768/65536/131072; native params only);
    show --modelfile 64k (SYSTEM verbatim) [evidence 05/05b]
11 05:05:41 exit=0 [local] preload edit → one-line diff; sh/bash/dash -n PASS; shellcheck
    unavailable (F-E6 carried) [evidence 06-preload.diff]
12 05:06:02 exit=1 [local] hx1.conf first construction TRUNCATED (sed range dropped LimitNOFILE;
    diff exit 1) — caught by hash cross-check; corrected: pre sha == 36af1c42…60f38, new sha ==
    163003b1…8d96c2 (== M6 stage-1) — disclosure F-M6B-2 [evidence 06-hx1conf.diff]
13 05:06:58 exit=0 scp both; sudo install (script 0755, conf 0644, root:root); installed sha match;
    sh -n installed PASS; daemon-reload; effective env CONTEXT_LENGTH=65536 [evidence 06-deploy]
14 05:07:31 exit=0 ssh ollama rm hx-qwen3.8-27b → tags-only (tags list, weights blob, manifests
    dir, base tag verified intact) [evidence 07]
15 05:07:57 exit=0 ssh systemctl restart ollama; poll /api/ps → API up, models=0 [evidence 08]
16 05:08:07 exit=0 (unit) preload auto-run via Requires= → OK - hx-qwen3.8-27b-64k resident (~10 s;
    one info-level curl(7) retry, F-M6-1 class) [evidence 09/12]
17 05:08:15 exit=0 ssh manual non-reboot test: sudo /usr/local/libexec/hx-ollama-preload → RC=0,
    OK line, 0.014 s [evidence 09]
18 05:08:34 exit=0 ssh systemctl restart ollama-preload (F-E4) → RC=0, Result=success; ps Forever
    proof: digest 766cd946…, ctx 65536, vram==size 20,463,789,012; ollama ps 100% GPU;
    GPUs 11,502/11,888 MiB [evidence 10]
19 05:08:55 exit=0 ssh AC-009 quick re-proof: version 6 ms; known-answer 391 (thinking ON, stop,
    no leak) [evidence 11]
20 05:09:0x exit=0 ssh journal scan: 0 Xid/OOM/NVRM; err-level count artifact investigated →
    banner line; zero err-level entries proven (F-M6B-3) [evidence 12/12b]
21 05:09:49 exit=0 ssh final sweep: units active+enabled; NRestarts=0; listener loopback-only;
    swap 0 B; uptime continuous; hashes/tags/ps [evidence 13]
22 05:10-…  exit=0 [local] write deliverable 29-esme-m6b-profiles.md
23 (task end) exit=0 cleanup: remote /tmp/esme-m6b removed (verified); local askpass helper +
    wrappers deleted (verified); sanitized local evidence retained transiently at hxs-5:/tmp/esme-m6b
```

## 12. Configuration files (profile §11.2)

| Artifact | Pre-change | Post-change | Diff | Ownership/mode |
| --- | --- | --- | --- | --- |
| `/usr/local/libexec/hx-ollama-preload` | `79571d63…7262a` | **`01c2a096…b29f2`** | one line (`MODEL=`), §4.1 | root:root 0755 (unchanged) |
| `/etc/systemd/system/ollama.service.d/hx1.conf` | `36af1c42…60f38` | **`163003b1…8d96c2`** (== M6 stage-1 bytes) | one line (`OLLAMA_CONTEXT_LENGTH=65536`), §4.2 | root:root 0644 (unchanged) |
| `/etc/systemd/system/ollama-preload.service` | `28c60c7d…52299` | `28c60c7d…52299` | — (untouched) | root:root 0644 |
| Model tags | bare `hx-qwen3.8-27b` + base | `…-32k` / `…-64k` / `…-128k` + base | §3/§5 | store `ollama:ollama` |

Pre-change full contents captured in session evidence (`02-preload-pre.txt`, `02-hx1conf-unit-pre.txt`); post-change contents are the pre-change bytes with exactly the diffs in §4. Effective runtime values post-reload: `systemctl show` Environment excerpt in §4.2; server startup uptake proven by the §7 residency (Modelfile is the effective contract — `/api/ps context_length 65536`).

**Rollback (all steps reversible):** restore the prior preload script (sha256 `79571d63…7262a`, full text in evidence and in `12-esme-m4-install-evidence.md` §4.7) and hx1.conf (`OLLAMA_CONTEXT_LENGTH=32768`, sha256 `36af1c42…60f38`) via `sudo install` + `daemon-reload`; re-create the bare alias per the §5 inverse; then `restart ollama` → poll `/api/ps` empty → `restart ollama-preload` (this report's §6 sequence).

Sanitized session evidence retained transiently at `hxs-5:/tmp/esme-m6b/` (volatile `/tmp`; the deliverable carries the record): `00-identity`, `01-drift-check`, `02-preload-pre`, `02-hx1conf-unit-pre`, `03-modelfile-{local,remote}-sha`, `04-alias-create`, `05-alias-show`, `05b-alias-64k-modelfile`, `06-preload.diff`, `06-hx1conf.diff`, `06-new-local-sha`, `06-deploy`, `07-bare-alias-retire`, `08-restart-ps-empty`, `09-manual-preload-test`, `10-preload-restart-residency`, `11-ac009`, `12-journal`, `12b-journal-priority-recheck`, `13-final-sweep`.

## 13. Findings, risks, decisions surfaced

- **F-M6B-1 (Requires= propagation loaded the operating profile first, FACT):** the mandated `restart ollama` bounced `ollama-preload` via `Requires=`; the edited script cold-loaded `hx-qwen3.8-27b-64k` inside the unit window (~10 s, one absorbed info-level curl retry). The subsequent manual test and unit restart were residency assertions, not loads. Journal class per F-M6-1 — expected during service restarts; monitors should not alert on it.
- **F-M6B-2 (disclosed construction defect, corrected pre-deployment):** my first local hx1.conf candidate silently dropped the last line (`LimitNOFILE=65535`) via a `sed -n '1,13p'` range error. The frozen-hash cross-check (pre `36af1c42…` / M6-stage-1 `163003b1…`) caught it before any deployment; the truncated file never left the build directory. The deployed file is byte-identical to the M6 stage-1 drop-in. Kept as evidence that hash-verified versioned edits are the real gate.
- **F-M6B-3 (journal-count artifact, FACT):** `journalctl -p err | wc -l` counts the `-- No entries --` banner as one line; only the direct query form proves an empty error set. Recorded as a method correction for future journal-cleanliness claims.
- **Carried, untouched:** F-M6-3 foreign sessions (idle all window; M7 exclusive-qualification-window recommendation stands); F-E2 discovery watchdog (listener-readiness latency — the §6 curl retry is its benign face); F-E6 shellcheck unavailable; NVRM teardown-assertion class (zero occurrences this window); F-M6-5 KV math (45,056 B/token; >131,072 remains unauthorized and unconfigured); parse_kv fixture defect (→ KK3 fixture decision; not exercised this milestone).
- **No decisions required escalation; no stop condition triggered.**

## 14. Validation summary (profile §11.4)

- **What changed:** three profile-named aliases created from the frozen byte-exact Modelfiles with digests exactly matching the frozen references; the preload contract repointed to `hx-qwen3.8-27b-64k` (script `MODEL=` line; drop-in `OLLAMA_CONTEXT_LENGTH=65536` for operator consistency); the ambiguous bare alias retired (tags only); the host switched to the 64K operating profile, resident and proven.
- **What did not change:** base digest `22130167c4c2…79643`; Ollama 0.32.15 (binary == server); preload unit bytes; all other drop-in lines (KV f16, FA on, NUM_PARALLEL=1, MAX_LOADED_MODELS=1, KEEP_ALIVE=-1, NO_CLOUD=1, CUDA UUIDs); units active+enabled (`NRestarts=0`); loopback-only bind; swap 0 B; system uptime (no reboot); all weight/config blobs; rick's entire plane. No soak, no reboot, no M7 activity, no sampling parameters, no new pulls, no base-tag/blob deletion, no OS/driver/network/firewall change, no vision inputs, no `keep_alive:0` client pattern (the empty-state was reached by the mandated service restart).
- **What was tested:** TKV knowledge review; target identity; drift check (10 items vs frozen references); Modelfile hash verification both sides (3/3); alias creations with digest equality vs frozen references (3/3); `ollama show` parameter/SYSTEM verification; preload script lint (sh/bash/dash, candidate + installed); manual non-reboot functional test of the edited script; unit restart (F-E4); operating-profile residency (digest, ctx 65536, size_vram == size, Forever, per-GPU MiB); known-answer + AC-009 quick re-proof; journal scan (Xid/OOM/error-level/NVRM); final state sweep (units, listener, swap, uptime, hashes, tags).
- **Passed:** every mandatory test above. **Failed:** no mandatory test. **Disclosed corrections (none concealed):** F-M6B-2 hx1.conf construction truncation caught pre-deployment; F-M6B-3 journal-count artifact. No test was re-run to reach a pass.
- **Installed/running:** binary == server 0.32.15; `ollama.service` active+enabled (`NRestarts=0`); `ollama-preload.service` active+enabled, last run `Result=success`.
- **Model identity/residency (end state):** operating profile `hx-qwen3.8-27b-64k:latest` digest `766cd946…8cc99d8a` on base `22130167c4c2…79643`; resident ctx 65536, 100% GPU (`size_vram == size == 20,463,789,012 B`), Forever, both GPUs (11,502 + 11,888 MiB). Also tagged: `hx-qwen3.8-27b-32k` (`db2c6206…f645510`, frozen recovery baseline) and `hx-qwen3.8-27b-128k` (`94b83a1e…0dad0260`, qualified extended — explicitly selected, not the default).
- **Endpoint/security state:** `127.0.0.1:11434` only (verified pre/post); loopback remains the boundary; no auth assumed; foreign sessions idle all window (F-M6-3 carried).
- **Resource/performance state:** operating profile resident 19.06 GiB of 31.98 GiB (~9.5 GiB aggregate headroom); known-answer warm path 1.01 s; RAM 4.6 Gi used; swap 0 B; zero Xid/OOM all window.
- **Rollback readiness:** §12 — prior script/drop-in restorable from the versioned diffs; bare alias re-creatable from the 32K Modelfile (deterministic digest); every step reversible.
- **Remaining risks/decisions:** F-M6B-1 (preload auto-load during restarts — expected class → monitors), F-M6-3 (exclusive M7 window → KK3/rick), carried findings per §13. M7 validates the always-on service at this 65,536 operating profile; 128K profile-switch mechanics are M7 evidence, not this milestone.
- **Budgets:** one session used; transient retry **0 of 1** used (no model transient occurred; the two disclosed corrections were my own scaffolding/method defects, fixed before any test claim); no stop condition triggered; no escalation required.

**Completion: `PASS — TASK COMPLETE`** (final gate §18: every applicable question answered yes; both corrections disclosed; no mandatory-test failure concealed; end state is the ratified 64K operating profile, resident and proven).

---

Sanitization confirmed: no secrets, tokens, cookies, private prompts, user data, or thinking content in this document; all prompts synthetic; LAN addresses already ratified in plan §3. The askpass helper and SSH wrappers were deleted at task end; remote scratch removed.
