# Esme (john) — M8 Sign-off Gate: Persistence Proof (3 Cold Reboots), Endpoint Boundary, Consumer-Proof, configuration.md, Acceptance Reconciliation (hxs-3, Meta-X)

`[TASK COMPLETE — EVIDENCE ATTACHED]`

| Field | Value |
| --- | --- |
| Report ID | ESME-M8-HXS3-SIGNOFF-001 |
| Task ID | WO-HXS3-JOHN-M8-001 (`PILOT-HXS3-MUSE-GLIMMER-TOOLING-001`, milestone M8) |
| Agent | john / Esme (profile `agents/john/profile.md`), session `john-m8-hxs3-20260827-01` |
| Target host | `hxs-3` (192.168.50.202, Meta-X), Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic, driver 580.173.02, **Etc/UTC** (fleet pass 2026-08-26T23:52:40Z) |
| Session host | `hxs-5` (192.168.50.204); all target actions over SSH `hxsa@192.168.50.202` — askpass helper READS the credential-record row of the HX Fleet SSH Access Guide AT EXECUTION TIME ONLY; no extracted copy ever exists; helper deleted at task end |
| Host-key check | STRICT — pinned ED25519 `SHA256:R/3mdfv7J0Fajo8yryT7JB6B4EoBm47W2rLX+siHEog` (rick M1 F-05); `StrictHostKeyChecking=yes` on every connection |
| Window (UTC) | 2026-08-27T01:39Z → 02:16Z (all labels UTC; reboots 01:54:18Z / 01:59:36Z / 02:03:34Z) |
| Ollama | 0.32.15 (binary == server; unchanged since M4 pin) |
| Operating profile under proof | `hx-muse-glimmer-64k:latest` digest **`9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`** (frozen artifact `muse-glimmer:30b` `de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1`), ctx 65536, 100% VRAM, Forever |
| GPUs | 2× PNY RTX 5060 Ti 16,311 MiB (rick's plane, untouched) |
| Reboot authorization | D6 — three COLD reboots pre-approved per-cycle in the governor-announced window (owner "Meta-X M8 approved" 2026-08-27, state log row 23); the owner may abort at any time (honored via governor session stop); **no other reboots authorized** |

Evidence labels: FACT / AUTHORITY / UPSTREAM / INFERENCE / RECORD.
All secrets excluded. **Sanitization disclosure (profile §15 honesty requirement, F-M8-1):** at ~01:41Z a credential-file structure probe (`awk -F'|'` field echo) printed the `SSH password` row's value into the session transcript once — same class as F-M5-8 and Addendum-A §A.6. The value appears in no file, command line, evidence artifact, or this document; the helper reads it at execution time only. Corrective applied immediately: no further direct reads of the credential file; all access via the helper. The standing owner-rotation advice remains the owner's call, unchanged. **Thinking content is never retained** — counts only (A01 §5.2). This document contains zero thinking text.

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path /opt/tkv-local/ollama resolves locally here, as in M4/M7/M5); target hxs-3 (192.168.50.202)
Source: /opt/tkv-local/ollama + HX-ASF-Servers controlling docs + agent-zero-docs credential guide (shape only)
Reviewed At: 2026-08-27T01:39Z → 01:47Z
Relevant Files:
  - agents/john/profile.md (full protocol); agents/ roster = carol, john, kimi-k3, rick (all current teammates)
  - repo AGENTS.md (communication contract; no-host-firewall owner rule; blueprint standing instruction)
  - servers/AGENTS.md (server records contract — configuration.md rules; discovery.md preserved)
  - servers/_templates/configuration.md (record template)
  - servers/SERVER-REGISTRY.md (hxs-3 row: Assigned Role "Agent intelligence"; workload field reads the
    2026-08-13 ratified target-state — see §8 reconciliation note; registry is owner-maintained)
  - servers/BLUEPRINT-llm-server.md §3 (preload contract), §5 (exposure plane, boundary + O1 tripwire
    residual), §6 (D5 SLO), §7 (recovery proof shape), §8 (Meta-X call-sign row, candidate until M8)
  - goals/2026-08-26-hxs3-muse-glimmer-tooling.md (D1-D8; SC-01..SC-08; stop conditions)
  - knowledge/decisions/KDD-0007 (one-call-per-turn, two-level enforcement)
  - pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001: 01-state-log.md rows 1-23 (M8 commissioned);
    13-work-order-john-m8.yaml + 14-context-packet-john-m8.yaml (governing);
    04-rick-hxs3-os-readiness.md (F-05 host-key pin; F-08 tz — closed by the fleet UTC pass);
    07-esme-m4-install.md (frozen identity; units; D5 budget arithmetic; F-J1/F-J2/F-J4);
    09-esme-m7-ladder-profiles.md (alias digests; preload repoint hashes; F-M7-1/2; NVRM teardown class);
    12-esme-m5-validation.md + Addendum A (F-M5-1 /tmp boot-cleared + owner maintenance reboots;
    interactive-eviction/preload-restore rule; F-M5-8 disclosure class; close-out guard shape)
  - pilots/PILOT-HX1-OLLAMA-QWEN27B-001/30-esme-m7a-reboot-cycles.md (AC-007 3/3 cycle shape;
    timing table vs D5; terminology: OS-initiated reboots, owner-domain power) +
    36-kk3-m8-acceptance-reconciliation.md (acceptance-matrix shape; deviation register)
  - servers/hxs-3/discovery.md (as-found record — preserved, never modified)
  - /opt/tkv-local/ollama/ollama-main: docs/faq.mdx:297-318 (keep_alive semantics; -1 pin; 0 unloads);
    api/types.go:810,841-843 (/api/ps fields context_length, expires_at, size_vram);
    docs/context-length.mdx (VRAM-based defaults; OLLAMA_CONTEXT_LENGTH); docs/linux.mdx (systemd);
    envconfig/config.go (OLLAMA_* env surface) — all present (verified 01:47Z)
Authority/Version Identified: owner M8 approval 2026-08-27 (state log row 23); D6 reboot pre-authorization;
  frozen Meta-X identity per packet (M7 end state, M5 close-out, governor-verified across two maintenance
  reboots); blueprint §5 boundary posture (as amended 2026-08-26).
Applicable Tests/Runbooks: WO-HXS3-JOHN-M8-001 reboot_cycle_protocol / endpoint_boundary_proof /
  consumer_proof / configuration_md clauses; hxs-1 M7a cycle procedure; D5 budgets
  (detection <=120 s; recovery <=900 s; preload script <=538 s worst case; unit TimeoutStartSec 600).
Contradictions or Gaps:
  1. SC-06 (multimodal image-input probes) has NO executed evidence anywhere in this pilot's record
     (state log, work orders 02/05/08/10/13, deliverables 04/07/09/12 — vision exercised 0 times;
     M7 boundary statement: "No vision inputs were exercised"). Not M8 scope to execute (packet: "Only
     M8 scope"). Disposition: reconciled OPEN at §8 — flagged for owner disposition at the ACCEPT gate;
     never silently passed.
  2. Registry workload field for hxs-3 ("gpt-oss-20b TP=2; LightRAG graph & retrieval", 2026-08-13
     target-state) predates the owner-commissioned Muse Glimmer pilot (D3; KDD-0007; goal file).
     Authority order resolves: explicit owner instruction > registry; registry is owner-maintained and
     is NOT edited by this task (hxs-1 F-REG-1 class — owner-side item). configuration.md copies the
     registry Assigned Role and records the as-configured workload with this divergence labeled.
  3. Running ollama process (started 2026-08-26T23:17Z boot, pre-TZ-change) may format EST offsets
     cosmetically in its own log lines and /api/ps expires_at until its next service restart
     (context-packet watch item; M5 Addendum A.4) — explained, not drift. After cycle 1 the process
     starts under Etc/UTC; the flip in expires_at formatting is expected and labeled.
  4. TKV source snapshot (v0.32.11-era) predates installed 0.32.15 — carried gap; the keep_alive /
     /api/ps / context semantics cited are version-independent and every identity claim is proven
     empirically on hxs-3 (hxs-1 F-E7 class).
Task May Proceed: YES
```

## 2. Test plan (profile §6.1 — recorded 2026-08-27T01:47Z, before the first mutation)

Stop conditions (work order): **any Xid → immediate stop + escalate; identity drift; scope exceedance; owner abort.** Xid-watch armed (F-M6-0 class); NVRM teardown-assertion chatter is a recorded class — logged, not halted on. One bounded correction per failed correctable cycle; a failed cycle is a finding, never silently re-run. Interactive-eviction rule (MAX_LOADED_MODELS=1): if an interactive load evicted the -64k pin, restore via `systemctl restart ollama-preload.service` and disclose (F-M5-1 class).

| Test ID | Property | Procedure | Expected | Pass rule |
| --- | --- | --- | --- | --- |
| T-IDENT | Session + target identity | hostname; `$SSH_CONNECTION`; host key == F-05; `sudo -n true` | hxs-5 → hxs-3/.202; pin match | all match |
| T-DRIFT-0 | Pre-flight frozen state | packet identity vs live: `/api/ps` EXACT; `/api/tags` ×5; unit hashes ×4; version; listener; `NRestarts=0`; Xid=0; uptime continuity | no drift vs M5 close-out | all match |
| T-CYCLE-1/2/3 | Cold-reboot persistence ×3 | per cycle: (1) pre-state (`/api/ps`, digests, unit hashes, journal cursor, boot-id); (2) `sudo -n systemctl reboot`; (3) poll timeline SSH+`/api/ps`; (4) identity guard EXACT + preload `Result=success`; (5) journal + Xid + `NRestarts` sweep + KA warm 391; (6) evidence off-host immediately | model ready with NO human action post-issue; detection ≤120 s; recovery ≤900 s; preload ≤600 s unit / ≤538 s script | 3/3 cycles, every guard exact |
| T-BOUNDARY | Endpoint boundary | `ss -lntp` listener line; LAN `/api/version` from hxs-5; ufw state; store `:cloud` scan; blueprint §5 statement + O1 residual | `*:11434` loopback preserved; LAN 200; no firewall; no `:cloud` tags | all proven; out-of-subnet refusal NOT RUN (no authorized host) |
| T-CONSUMER | Consumer-proof (RAG-shaped) | retrieved-document question + one tool call via the alias, native sampling, LAN endpoint; harness enforces KDD-0007 | exactly 1 structured tool call; 0 raw ATEM; schema-conforming args; serial execution; grounded final; latency reported | all hold end-to-end |
| T-CONFIG-MD | servers/hxs-3/configuration.md | written per servers/AGENTS.md from live + pilot evidence; discovery.md hash before/after | complete per template; discovery untouched | governor-checkable |
| T-RECONCILE | Acceptance reconciliation | SC-01..SC-08 vs goal, evidence pointers, deviations | every SC item dispositioned honestly (SC-06 OPEN) | complete |
| T-GUARD | Close-out | final `/api/ps` EXACT; journal sweep; evidence sanitization sweep | identity exact; 0 Xid; no secrets in evidence | all hold |

Rollback trigger mapping: any stop condition → preserve state, capture evidence, escalate to Kimi-K3 (profile §13). The reboots themselves are owner-pre-approved state transitions, not configuration mutations; the frozen baseline is the rollback state by construction.

## 3. Pre-flight state (T-IDENT, T-DRIFT-0) — FACT, 2026-08-27T01:49Z → 01:52Z

**T-IDENT PASS (evidence `00-identity.txt`):** hostname `hxs-3`; `SSH_CONNECTION` = `192.168.50.204 → 192.168.50.202:22` (hxs-5 → hxs-3); machine-id `d02a8e3a8d76474390e51a162e9f196d` (== discovery + rick M1); `sudo -n true` OK; known_hosts ED25519 fingerprint == F-05 pin exactly (verified 01:49Z before the first connection). Host clock Etc/UTC, NTP synchronized. Boot-id `299c5f22-2dc2-4447-9000-dcf34c109db7`, uptime since 2026-08-26T23:17:04Z continuous (the M5 maintenance-2 boot; `last -x` chain confirms no intervening reboot). Kernel 7.0.0-30-generic, Ubuntu 24.04.4 LTS.

**T-DRIFT-0 PASS (evidence `01a/01b/01c`) — NO DRIFT vs the packet's frozen state:**

| Item | Frozen value | Observed | Verdict |
| --- | --- | --- | --- |
| `/api/version` / binary | 0.32.15 / 0.32.15 | 0.32.15 / 0.32.15 | match |
| Resident name+digest | `hx-muse-glimmer-64k:latest` `9dffb015db40…e7da` | verbatim exact | match |
| Residency | `size == size_vram`, ctx 65536, Forever | `18,376,336,340 == 18,376,336,340`; `context_length 65536`; `expires_at` 2318 | match |
| `expires_at` formatting | UTC after TZ pass | shows `-05:00` — the running process predates the TZ change (packet watch item; cosmetic, explained) | expected; flips at cycle 1 |
| `/api/tags` (5 tags) | `de878ce33ad8…64c1`, `472ad84e…ad99`, `09c4f825…836e`, `9dffb015…e7da`, `17fe5b80…e85b` | all 5 verbatim; **zero `:cloud` tags** (store-policy tripwire clean) | match |
| `ollama.service` sha256 | `11758d46…1dbd3` (M4) | `11758d46…1dbd3` | match |
| `hx3.conf` sha256 | `07824e4e…e7d5` (post-web-search, M5-recorded) | `07824e4e6794b1a4dc9af3dead4e4968d4bb63b629200f736a5e9313e9c3e7d5` | match |
| `ollama-preload.service` sha256 | `3b0e00b6…a5f6` | `3b0e00b6…a5f6` | match |
| `hx-ollama-preload` sha256 | `b1798130…fe08` (M7 repoint) | `b17981305a7bf1c418be6544557b3e3bae66b56d0d2bb2f802d5e26e5ee6fe08` | match |
| Units | both enabled+active; preload `Result=success` | identical; `NRestarts=0`; `TimeoutStartUSec=10min` | match |
| Environment | HOST=0.0.0.0, NUM_PARALLEL=1, MAX_LOADED_MODELS=1, CONTEXT_LENGTH=65536 (NO_CLOUD removed — ratified) | verbatim | match |
| Listener | `*:11434` wildcard, loopback preserved | `LISTEN *:11434` (ollama pid 1071) | match |
| GPUs / runner | both 5060 Ti, driver 580.173.02, runner on both | 10,634 + 9,404 MiB (pid 1912); link Gen1-idle/Gen3-max, x8/x16 (recorded class) | match |
| Journal this boot | preload OK 23:18:41Z after bounded Phase-1 probes (F-M6-1 class); Xid=0 | identical; `journalctl -k -b` NVRM Xid count **0**; 0 failed units | match |
| Swap / storage | 0 B / ample | 0 B / 3.4 T free | match |

Interactive-eviction check (MAX_LOADED_MODELS=1 rule): the -64k pin **is** resident — no preload-restore action needed (restore count this session: 0). Journal cursor captured for cycle 1 pre-state. **The stop rule was not triggered; the reboot window is open.**

## 4. Reboot cycles (T-CYCLE-1/2/3)

All timestamps UTC. "Ready" = the preload unit's `/api/ps` assertion of the exact alias+digest (`hx-ollama-preload: OK` = `ExecMainExitTimestamp`). Cross-host subtraction is safe: both hosts NTP-synchronized UTC (fleet pass). Evidence is written directly to hxs-5 over SSH at capture time — nothing evidentiary ever rests on hxs-3's boot-cleared `/tmp` (F-M5-1 rule satisfied by construction; off-host verification `ls` after each cycle).

### 4.1 Cycle 1 — boot-id `299c5f22…9db7` → `30285874-9a18-4d97-bdb7-b7e091191456` (PASS)

| Step | Result (FACT) |
| --- | --- |
| (1) Pre-state 01:54:02Z | `/api/ps` frozen identity exact; boot-id `299c5f22…`; `NRestarts=0`; preload `Result=success`; journal cursor `…t=659fd9c326d1e…` recorded (evidence `03-cycle1-prestate`) |
| (2) Reboot | `sudo -n systemctl reboot` issued **01:54:18.666Z** (hxs-5 clock), rc=0 (evidence `02-cycle1-reboot-poll`) |
| (3) Poll timeline | LAN `/api/version` first answer **+94 s** (01:55:52.6Z — detection ≤120 s ✓); `/api/ps` exact-identity resident at first poll seeing it **+129 s** (01:56:27.8Z). On-host anchors: boot t0 01:54:46; `ollama.service` active 01:55:00 (t0+14 s); preload start 01:55:00, bounded Phase-1 probes ×6 absorbing the listener delay (F-M6-1 class); **preload OK 01:56:24** → **boot→ready 98 s** (≤900 s ✓, 9.2× under); issue→ready ≈125 s |
| (4) Units | both enabled+active; `NRestarts=0`; preload `active (exited)`, `Result=success`, `ExecMainStatus=0` (evidence `04-cycle1-postboot`) |
| (5) Identity guard EXACT | name `hx-muse-glimmer-64k:latest`; digest `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`; `size == size_vram == 18,376,336,340`; `context_length 65536`; `expires_at` 2318 (Forever); `ollama ps` 100% GPU / 65536 / Forever (evidence `05-cycle1-guard`). **`expires_at` now formats `Z`** — the process restarted under Etc/UTC at this boot, exactly the predicted cosmetic flip (§1 gap 3) |
| (6) KA warm inference | `17 × 23` → **391**, `done_reason stop`, total 2.44 s, `load_duration` **1.57 ms** — warm, no model-reload (evidence `06-cycle1-ka.json`; thinking present 161 chars — count only) |
| (7) GPUs + journal | runner pid 1782 holding 10,610 + 9,380 MiB (both 5060 Ti); 53/53 layers GPU. **Xid 0, OOM 0, ollama err-level: no entries**; unit hashes ×4 re-verified == frozen; listener `*:11434`; 0 failed units; swap 0 B. NVRM 71 lines = 1 driver banner + 25 `kbifInitLtr` LTR notes + 34 `pIOVAS` + 4 `Sysmemdesc` + 6 `iovaspaceDestruct` (leftovers 4,1,1,-1 — small, non-growing): all **confined to the driver-load/runner-start window 01:54:55→01:55:57**, ending 27 s before residency — the recorded teardown-assertion class, monitor-only; one F-E2-class watchdog WARN pair at 01:55:54, retried and succeeded (evidence `05b-cycle1-nvrm`) |
| (8) Evidence off-host | `02-cycle1-reboot-poll.txt`, `03-cycle1-prestate.txt`, `04-cycle1-postboot.txt`, `05-cycle1-guard.txt`, `05b-cycle1-nvrm.txt`, `06-cycle1-ka.json` — all on hxs-5, verified present 01:58Z |

No human action occurred on the host between reboot-issue and ready: driver → `ollama.service` → `ollama-preload` → `/api/ps` assertion ran autonomously. **Cycle 1: PASS.**

### 4.2 Cycle 2 — boot-id `30285874…1456` → `d5a72f5c-f334-42d3-8dea-4ec44480a3ce` (PASS)

| Step | Result (FACT) |
| --- | --- |
| (1) Pre-state 01:59:36Z | steady state from cycle 1: identity exact; boot-id `30285874…`; `NRestarts=0`; preload `Result=success`; journal cursor `…t=659fdb01793bc…` recorded (evidence `07-cycle2-prestate`) |
| (2) Reboot | issued **01:59:36.247Z**, rc=0; host DOWN confirmed +6 s (evidence `02-cycle2-reboot-poll`) |
| (3) Poll timeline | SSH return +42 s (02:00:18.6Z); LAN `/api/version` first answer **+91 s** (02:01:07.7Z — detection ≤120 s ✓); `/api/ps` exact identity resident **+126 s** (02:01:42.8Z). On-host anchors: boot t0 02:00:03; `ollama.service` active 02:00:17 (t0+14 s); preload start 02:00:17, bounded probes ×7 (F-M6-1 class); **preload OK 02:01:41** → **boot→ready 98 s** (≤900 s ✓); issue→ready ≈125 s |
| (4) Units | both enabled+active; `NRestarts=0`; preload `Result=success`, `ExecMainStatus=0` (evidence `08-cycle2-postboot`) |
| (5) Identity guard EXACT | name/digest/ctx/residency verbatim as cycle 1 (`size == size_vram == 18,376,336,340`; `expires_at` 2318 `Z`; 100% GPU / 65536 / Forever); unit hashes ×4 == frozen; listener `*:11434`; 0 failed units; swap 0 B (evidence `09-cycle2-guard`) |
| (6) KA warm inference | **391**, stop, total 2.81 s, `load_duration` **2.19 ms** — warm (evidence `10-cycle2-ka.json`; thinking 196 chars, count only) |
| (7) GPUs + journal | runner pid 1839 holding 10,610 + 9,380 MiB; 53/53 layers GPU. **Xid 0, OOM 0, ollama err-level: no entries**; NVRM 71 lines, same recorded classes (34 `pIOVAS`, 25 `kbifInitLtr`, 4 `Sysmemdesc`, 7 `iovaspaceDestruct` leftovers 4,1,1,-1), last line 02:01:14 — 27 s before model loaded (02:01:41); one F-E2-class watchdog WARN, succeeded |
| (8) Evidence off-host | `07-cycle2-prestate` … `10-cycle2-ka.json` — all on hxs-5, verified present 02:03Z |

**Cycle 2: PASS** — autonomous boot path again, no human action post-issue.

### 4.3 Cycle 3 — boot-id `d5a72f5c…a3ce` → `671be79e-8d97-48d1-b4a5-135280ac0f96` (PASS)

| Step | Result (FACT) |
| --- | --- |
| (1) Pre-state 02:03:34Z | steady state from cycle 2: identity exact; boot-id `d5a72f5c…`; `NRestarts=0`; preload `Result=success`; journal cursor `…t=659fdbe4de55c…` recorded (evidence `11-cycle3-prestate`) |
| (2) Reboot | issued **02:03:34.692Z**, rc=0; host DOWN confirmed +5 s (evidence `02-cycle3-reboot-poll`) |
| (3) Poll timeline | SSH return +44 s (02:04:18.8Z); LAN `/api/version` first answer **+93 s** (02:05:07.9Z — detection ≤120 s ✓); `/api/ps` exact identity resident **+129 s** (02:05:43.1Z). On-host anchors: boot t0 02:04:02; `ollama.service` active 02:04:16 (t0+14 s); preload start 02:04:16, bounded probes ×7 (F-M6-1 class); **preload OK 02:05:40** → **boot→ready 98 s** (≤900 s ✓); issue→ready ≈125 s |
| (4) Units | both enabled+active; `NRestarts=0`; preload `Result=success`, `ExecMainStatus=0` (evidence `12-cycle3-postboot`) |
| (5) Identity guard EXACT | verbatim as cycles 1–2 (`size == size_vram == 18,376,336,340`; ctx 65536; `expires_at` 2318 `Z`; 100% GPU / Forever); unit hashes ×4 == frozen; listener `*:11434`; 0 failed units; swap 0 B (evidence `13-cycle3-guard`) |
| (6) KA warm inference | **391**, stop, total 3.17 s, `load_duration` **2.1 ms** — warm (evidence `14-cycle3-ka.json`; thinking 234 chars, count only) |
| (7) GPUs + journal | runner pid 1850 holding 10,610 + 9,380 MiB; 53/53 layers GPU. **Xid 0, OOM 0, ollama err-level: no entries**; NVRM 70 lines, same recorded classes (34 `pIOVAS`, 25 `kbifInitLtr`, 4 `Sysmemdesc`, 6 `iovaspaceDestruct` leftovers 4,1,1), last line 02:05:13 — 27 s before model loaded (02:05:40); one F-E2-class watchdog WARN, succeeded |
| (8) Evidence off-host | `11-cycle3-prestate` … `14-cycle3-ka.json` — all on hxs-5 (20 evidence files total, verified 02:07Z) |

**Cycle 3: PASS** — autonomous boot path, no human action post-issue.

### 4.4 Readiness timings vs the D5 SLO (AUTHORITY: D5 — detect ≤2 min, recover ≤15 min, one bounded attempt; blueprint §6)

| Metric | Cycle 1 | Cycle 2 | Cycle 3 | D5 budget | Margin |
| --- | ---: | ---: | ---: | ---: | --- |
| Reboot-issued → host down confirmed | n/a (fixed in c2) | 6 s | 5 s | — | — |
| Reboot-issued → SSH returns (hxs-5) | (see note) | 42 s | 44 s | — (SSH liveness) | — |
| Reboot-issued → LAN API first answer (**detection**) | 94 s | 91 s | 93 s | **≤120 s** | **PASS ×3** |
| Boot → `ollama.service` active | 14 s | 14 s | 14 s | — | — |
| **Boot → model ready (preload OK)** — **recovery** | **98 s** | **98 s** | **98 s** | **≤900 s** | **9.2× under, deterministic ×3** |
| Reboot-issued → model ready | ≈125 s | ≈125 s | ≈125 s | ≤900 s | ~7× under |
| Preload unit wall (start → OK) | 84 s | 84 s | 84 s | ≤600 s unit / ≤538 s script worst case | PASS ×3 |
| Ready → KA warm inference (`load_duration`) | 2.44 s (1.57 ms) | 2.81 s (2.19 ms) | 3.17 s (2.1 ms) | approved timeouts | warm ×3, no reload |

Cycle-1 note: the first SSH poll succeeded at +1 s because the host had not yet dropped (scaffolding measured before the down-transition; the cycle-1 API and on-host anchors are unaffected and authoritative). The runner script gained a host-down confirmation phase from cycle 2 (kept in the command log). Boot chain (`last -x`, evidence `12-cycle3-postboot`) proves **exactly three reboots — 01:54, 02:00, 02:04 — and no fourth**; the previous boot is 2026-08-26 23:17Z (pre-M8).

**No human intervention occurred after the operator-issued reboot in any cycle**: once `systemctl reboot` was issued (owner-pre-approved per D6), the boot path (driver → `ollama.service` → `ollama-preload` → exact alias+digest `/api/ps` assertion) returned the frozen 64K operating profile to ready state autonomously, **3/3**, with no action taken on the host between power-on and ready, and zero evictions/preload-restores all session. **AC-007-class persistence proof: PASS 3/3.** Terminology per the hxs-1 review finding: these are OS-initiated cold reboots; a literal power-cycle variant is owner-domain (hxs-3 has the Aug-25 site power-cut class covered by the fleet's unplanned-recovery record and this host's two owner-maintenance reboots at M5, both self-healed).

## 5. Endpoint boundary proof (T-BOUNDARY) — FACT, 2026-08-27T02:08Z (evidence `15-boundary.txt`)

**PASS.** No boundary changes were made — proof only (work-order clause).

| Property | Required (blueprint §5, owner D2) | Observed (FACT) | Verdict |
| --- | --- | --- | --- |
| Listener shape | `OLLAMA_HOST=0.0.0.0` wildcard with loopback preserved | `LISTEN *:11434` (ollama pid 1064); full table otherwise: ssh `:22`/ `[::]:22`, stub DNS `:53` (loopback), llama-server internal `127.0.0.1:44249` only — no other exposure | **match** |
| Loopback preserved | preload/fixtures depend on 127.0.0.1 | `http://127.0.0.1:11434/api/version` → `{"version":"0.32.15"}` on-host | **answers** |
| LAN reachability | reachable inside 192.168.50.0/24 | from hxs-5 (authorized /24 member): `/api/version` **HTTP 200 in 12 ms**; `/api/ps` **HTTP 200 in 27 ms** returning the frozen resident identity | **reachable** |
| No host firewall | owner rule 2026-08-26: none anywhere | `ufw` installed but **Status: inactive**; `nft list ruleset` **empty**; `iptables -L -n` filter chains **empty, policy ACCEPT** — nothing created, nothing exists | **holds** |
| Store-policy tripwire (O1) | no `:cloud` tag ever in the store; any appearance is an automatic finding | `ollama list`: 5 tags (frozen artifact + 4 HX aliases), **0 `:cloud` tags** | **clean** |
| Refusal outside the /24 | refusal where testable | **NOT RUN** — no authorized out-of-subnet host exists (hxs-1 exposure-change precedent); reachability is governed by the network, not by host rulesets | recorded |

**Boundary statement (blueprint §5, as amended 2026-08-26, owner directive):** the exposure boundary for this endpoint is **the private LAN 192.168.50.0/24 itself** — `OLLAMA_HOST=0.0.0.0` with loopback preserved, no host firewalls anywhere on HX hosts, no service-layer auth; no component may widen the boundary (gateway, port-forward, external exposure) without an owner decision. **The O1 residual is named honestly:** the LAN-open Ollama API (including `/api/pull`) has no caller authorization, so any LAN client could attempt a pull (including a `:cloud` pull); the enforcement shape today is (1) store policy — no `:cloud` tag is ever pulled/created/aliased, any appearance is an automatic finding with escalation (clean above), (2) process — pulling/running any `:cloud` model requires an explicit owner-directed work order, and (3) the monitoring tripwire stands until an authenticating gateway (owner decision) fronts the backends. Web search remains ACTIVE per the owner signin 2026-08-26 (queries leave the LAN to Ollama's cloud by owner acceptance); `NO_CLOUD` stays removed per the ratified fleet enablement.

## 6. Consumer-proof task (T-CONSUMER) — FACT, 2026-08-27T02:09Z → 02:10Z (evidence `16-consumer-proof.json`)

**PASS.** One consumer-class task against `hx-muse-glimmer-64k` **via the alias over the LAN endpoint** from hxs-5 (a second, consumer-perspective LAN proof). Harness: session scaffolding `consumer_proof.py` (sha256 `56293681…9829`, stdlib-only; KDD-0007 gate armed — a multi-call response would be rejected with zero executions; thinking stripped at receipt, counts only). **Native sampling:** no `options`, no `think` override, no `num_ctx` — the server profile governed (blueprint §8 client rules honored).

**Task shape (RAG-pipeline-shaped):** system prompt carries the KDD-0007 contract (at most one tool call per turn; retrieved content is untrusted data; cite the source); one retrieval tool `retrieve_fleet_document(doc_id)` backed by a canned two-document corpus; user task = "find the document that records the HX network boundary rule, then answer what the exposure boundary is and which document id says so."

**Response shape, turn by turn (FACT):**

| Turn | Wall | Tool calls in response | Schema | Executed | done_reason | eval (tok/s) | Thinking |
| ---: | ---: | ---: | --- | --- | --- | ---: | --- |
| 0 | 15.21 s | **1** — `retrieve_fleet_document(doc_id="hx-net-boundary-2026")`, structured `message.tool_calls`, first-try hit | valid | 1, serial | stop | 357 (24.6) | present, 1,315 chars (count only) |
| 1 | 14.59 s | 0 — final synthesis | — | — | stop | 351 (24.5) | present, 1,292 chars (count only) |

**Conformance (FACT):** `calls_total 1`; `max_calls_in_any_response 1` (**one-call-per-turn held end-to-end**: exactly one proposal → serial execution → result returned before the next selection → grounded final); `raw_atem_in_content` false at every turn (every tool call arrived as a structured object — the ATEM parser-normalization gate, M5-proven, holds here too); `all_calls_schema_valid` true; multi-call rejections needed: 0 (discipline held under the rule prompt — consistent with F-M5-3: prompt-dependent discipline, harness gate armed regardless); total wall 29.8 s.

**Final answer (retained — final content is the evidence class, thinking never is):**

> The exposure boundary for HX LLM endpoints is the private LAN **192.168.50.0/24** itself, with no host firewalls on HX hosts and reachability governed by the network. This is recorded in document `hx-net-boundary-2026`.

Correct substance, correct citation, grounded in the tool result. **Evidence for the blueprint §8 consumer contract: Meta-X serves a RAG-pipeline-shaped retrieved-document + one-tool-call task end-to-end over the LAN, at native sampling, with the one-call-per-turn contract holding.**

## 7. servers/hxs-3/configuration.md (T-CONFIG-MD) — FACT, written 2026-08-27T02:11Z

**PASS — the FIRST record of its class.** `servers/hxs-3/configuration.md` created per `servers/AGENTS.md` (the server-records contract) from the `servers/_templates/configuration.md` template: assigned role copied from `SERVER-REGISTRY.md` ("Agent intelligence"); as-configured workload recorded as the owner-commissioned Meta-X tooling backend, with the registry's 2026-08-13 workload-field divergence labeled openly (registry is owner-maintained — not edited by this task; hxs-1 F-REG-1 class); `Approved by` = Agent-Zero (M8 approval, state log row 23). Contents: discovery reference (preserved), role objective (KDD-0007 one-call-per-turn specialist), the material configuration chain (OS/masks/tz; network + no-firewall boundary; storage D1; GPUs + driver + x8 ceiling; Ollama 0.32.15 pin; frozen artifact + four aliases with digests; hx3.conf + preload contract with hashes; web-search posture), services table, validation checklist with evidence pointers into the pilot chain, material change record (M1 → M4 → web-search → M7 → fleet-time → M8), sources. **`discovery.md` preserved untouched** — sha256 `93bc5634f41dceb7bad75977973e3945c16872649df16f9965e6a6884eb179d3` before and after (evidence `17-discovery-pre.sha256` + §11 sweep).

## 8. Acceptance reconciliation (T-RECONCILE) — per goal SC item, for the owner's ACCEPT decision

| SC | Property | Verdict | Principal evidence |
| --- | --- | --- | --- |
| SC-01 | Model identity frozen | **PASS** | M4 full freeze (exact tag; LM+projector+params blob digests; on-disk manifest == digest; template/renderer/parser `glimmer` with ATEM; license publisher-declared Apache-2.0) — 07-esme §5.4; M7 alias digest-equality proofs — 09-esme §7; re-verified live at M8 pre-flight and after every cycle (this document §3/§4) |
| SC-02 | GPU placement | **PASS** | Both 5060 Ti allocated, 100% VRAM (`size == size_vram`), 53/53 layers GPU, zero CPU fallback — M4 §6/§7.1, M7 §4/§10 (telemetry under load), M8 §4 ×3 cycles (runner 10,610 + 9,380 MiB each boot) |
| SC-03 | Runtime profile | **PASS** | Ladder 32K→64K→128K on the exact digest, all CAPACITY PASS with needle-found at ~95% of every rung; operating 64K per D5; KV f16 13,312 B/token exactly linear + 97.5 MiB second cache; effective ctx proven by `/api/ps context_length 65536` — 09-esme §4/§5/§9; re-proven every M8 cycle (§4) |
| SC-04 | Boot recovery | **PASS** | **This gate: 3/3 cold reboots, model ready with no human action**, boot→ready 98 s deterministic (9.2× under the 900 s D5 SLO), detection ≤94 s (≤120 s budget), preload `Result=success` ×3, `NRestarts=0`, identity guard EXACT ×3, warm KA 391 ×3 (§4). Service-restart path proven at M7 §8.4; two unplanned owner-maintenance reboots self-healed at M5 (12-esme §2, F-M5-1) |
| SC-05 | Tooling contract | **PASS** | M5 (ratified bars): tool protocol 14/14 (100% forbidden/malformed denied; 100.0% schema conformance of 57 decisions; 0 raw ATEM in 246 events); one-call-per-turn **100% enforced** (2 multi-call responses rejected incl. OC07 live, 0 leaked executions, serial order proven); structured output 20/20; system-policy 22/22; denial 100% — 12-esme §4/§5; KDD-0007 two-level enforcement proven necessary and working |
| SC-06 | Multimodal | **OPEN — owner disposition required** | **No executed evidence exists in the pilot record** (state log rows 1–23; work orders 02/05/08/10/13; deliverables 04/07/09/12/15 — image inputs exercised 0 times; 09-esme §15: "No vision inputs were exercised"). Not executed here: M8 scope excludes it ("Only M8 scope"). The projector's identity is frozen (M4) and the model loads with `--mmproj` every boot, but "images consumed correctly" is unproven. Not waived, not failed — the owner defers (hxs-1 SC-05 class) or commissions the probes. **This is the one SC item without evidence.** |
| SC-07 | Exposure boundary | **PASS** | M8 §5: `*:11434` wildcard with loopback preserved; LAN HTTP 200 from hxs-5 (12/27 ms); no host firewall (ufw inactive, nft/iptables empty); 0 `:cloud` tags; boundary = the /24 LAN per blueprint §5 with the O1 tripwire named; out-of-subnet refusal NOT RUN (no authorized host) |
| SC-08 | Registration + process | **GATE HELD — owner verdict pending** | Catalog record `DOC-backend-meta-x` live (candidate; `parallel_tool_calling: false` first-class LIMIT) — flips to `active` at the owner's ACCEPT (governor's lane); consumer-proof sequential tooling task end-to-end PASS (§6); sanitized packages with per-artifact sweeps (this deliverable; close-out sweep CLEAN); handoffs closed by Carol receipts through M5 (M8 handoff opens at delivery); KK3 gate = this package; **owner sign-off = the decision this package supports** |

**Deviation / incident register (this milestone; none concealed):**

| ID | What happened | Disposition |
| --- | --- | --- |
| F-M8-1 | Credential-row value printed to the session transcript once by a structure probe (~01:41Z) | Contained: in no file/command/artifact (close-out sweep CLEAN); helper-only access from that point; same class as F-M5-8 / Addendum-A §A.6; standing owner-rotation advice unchanged |
| D-M8-1 | Cycle-1 SSH-return poll measured +1 s (host not yet down) | Scaffolding artifact, not a target defect; `cycle.sh` gained a host-down confirmation phase from cycle 2; cycle-1 API + on-host anchors unaffected and authoritative; kept openly in the command log |
| SC-06 | Multimodal probes never executed in this pilot | OPEN for owner disposition (above) |
| Registry | hxs-3 workload field predates the Muse Glimmer commission | Labeled in configuration.md; owner-maintained, not edited (F-REG-1 class) |

**Stop conditions:** none hit — **zero Xid** across the whole session (swept every cycle and at close-out), zero identity drift (every guard EXACT), zero scope exceedance, no owner abort received. **Bounded corrections: 0 of 1 used** (no failed cycle; every cycle passed on its single execution; no test re-run to reach a pass). Interactive-eviction / preload-restore count: **0** (the -64k pin was resident at every check).

## 9. Findings register

- **F-M8-1 (sanitization disclosure):** credential-row value printed to the session transcript once by a structure probe (~01:41Z); in no file/command/artifact (close-out sweep CLEAN); helper-only access from that point. Same class as F-M5-8 / Addendum-A §A.6.
- **D-M8-1 (scaffolding artifact, corrected openly):** cycle-1 SSH-return poll fired before the host dropped (+1 s); the poll script gained a host-down confirmation phase (used in cycles 2–3: down confirmed +6/+5 s). Cycle-1's API-answer and on-host anchors are unaffected; no cycle was re-run.
- **F-M8-2 (deterministic recovery, FACT):** boot→ready **98 s at all three cycles** (preload unit wall 84 s ×3, split ≈49 s bounded API-wait probes absorbing the listener/CUDA-rediscovery window + ≈35 s single-attempt load and assertion of the 17.11 GiB resident set). Detection (LAN API first answer) 91–94 s; issue→ready ≈125 s. Consistency note (INFERENCE): the shape matches the two M5 maintenance reboots — this host's recovery is deterministic within seconds, an order of magnitude inside the D5 budgets.
- **F-M8-3 (EST→UTC cosmetic flip closed, FACT):** the pre-cycle-1 running process formatted `expires_at` with a `-05:00` offset (started before the 2026-08-26T23:52:40Z TZ change); from cycle 1 onward the process runs under Etc/UTC and formats `Z`, and the ollama journal lines are UTC. The context-packet watch item is now closed by evidence.
- **Carried, unchanged (recorded classes, monitor-only):** NVRM teardown assertions (`pIOVAS`/`Sysmemdesc`/`iovaspaceDestruct`, leftovers ≤4, non-growing, confined to the driver-load/runner-start windows, ending ~27 s before residency each boot) — zero Xid everywhere, escalation triggers not approached; F-E2 GPU-discovery watchdog WARN once per cold load, retried and succeeded; `kbifInitLtr` LTR platform notes; F-M6-1 bounded preload probes during listener startup (6–7 per boot).
- **Owner-host activity:** none observed this session (no foreign API clients in the GIN log beyond the known `::1` fleet-monitoring poller class recorded at M5; no interactive eviction; preload-restore count 0).

## 10. Configuration files (profile §11.2)

**No host configuration file was created, modified, or deleted in M8.** The frozen baseline was verified read-only at pre-flight and after every cycle:

| Artifact | Frozen sha256 | Pre-flight | Post-cycle-1 | Post-cycle-2 | Post-cycle-3 |
| --- | --- | --- | --- | --- | --- |
| `/etc/systemd/system/ollama.service` | `11758d46…1dbd3` | match | match | match | match |
| `/etc/systemd/system/ollama.service.d/hx3.conf` | `07824e4e…e7d5` | match | match | match | match |
| `/etc/systemd/system/ollama-preload.service` | `3b0e00b6…a5f6` | match | match | match | match |
| `/usr/local/libexec/hx-ollama-preload` | `b1798130…fe08` | match | match | match | match |

Repository-side, exactly one file was created (the authorized record): `servers/hxs-3/configuration.md` (new; §7). `servers/hxs-3/discovery.md` untouched (sha256 `93bc5634…79d3` before and after). No git commit per the work order. Session scaffolding (deleted at task end): `/tmp/esme-m8-hxs3/` on hxs-5 — askpass helper, ssh/scp wrappers, `cycle.sh` (poll driver), `consumer_proof.py` (sha256 `56293681…9829`, as executed); remote scratch: none ever created on hxs-3 (all captures streamed to hxs-5 at execution time — the F-M5-1 boot-cleared-/tmp rule satisfied by construction). Rollback: nothing to roll back — the frozen baseline is the steady state the host sits in; the reboots were owner-pre-approved state transitions, not mutations.

## 11. Sequential command log (profile §11.3)

Session host `hxs-5`, user `hxsa`; remote = SSH askpass wrapper (secret never on any command line; `sudo -n` only). Timestamps UTC. Failures and corrections kept.

```text
 1 01:39 exit=0 [local] hostname=hxs-5 verified; date; /opt/tkv-local/ollama present
 2 01:39-01:47 exit=0 [local] reads: profile; WO/CP 13/14; repo + servers AGENTS.md; goal file;
    state log rows 1-23; blueprint; template; registry; KDD-0007; prior deliverables
    04/07/09/12(+A); hxs-1 30-esme M7a + 36-kk3 M8; discovery.md; TKV semantics spot-checks
    (faq keep_alive, api/types ps fields, context-length, linux.mdx, envconfig) —
    [KNOWLEDGE REVIEW COMPLETE]. DISCLOSED: credential-row structure probe printed the row
    value into the transcript once (F-M8-1); value in NO file/command/artifact
 3 01:47 exit=0 [local] SC-06 evidence search across pilot record — 0 executed vision/multimodal
    probes anywhere (gap registered for §8)
 4 01:47 exit=0 [local] deliverable skeleton written (this file, through §2)
 5 01:49 exit=0 [local] workspace /tmp/esme-m8-hxs3 (0700); known_hosts ED25519 fingerprint ==
    F-05 pin verified BEFORE first connection; askpass helper + rssh/rscp (0700; helper READS
    the credential-record row at execution time); sh -n lint PASS; askpass shape test non-empty
 6 01:50 exit=0 ssh T-IDENT: hostname=hxs-3; peer .204→.202:22; machine-id match; sudo -n OK;
    Etc/UTC NTP-synced; boot-id 299c5f22…; uptime since 2026-08-26T23:17:04Z [evidence 00]
 7 01:50-52 exit=0 ssh T-DRIFT-0 [evidence 01a/01b/01c] — NO DRIFT: /api/ps EXACT; 5 tags
    (0 :cloud); hashes ×4 match; units enabled+active, NRestarts=0, preload Result=success;
    Environment exact (NO_CLOUD absent — ratified); listener *:11434; 0 failed; Xid=0; swap 0;
    runner 10,634+9,404 MiB; journal cursor captured; boot chain clean
 8 01:54:02 exit=0 ssh cycle-1 pre-state [evidence 03] — identity exact; cursor recorded
 9 01:54:18.666 exit=0 CYCLE 1: sudo -n systemctl reboot; API first answer +94 s; RESIDENT exact
    +129 s [evidence 02-cycle1]. NOTE: first SSH poll fired pre-drop (+1 s, D-M8-1)
10 01:56:47 exit=0 ssh cycle-1 post-boot [evidence 04] — boot t0 01:54:46; new boot-id 30285874…;
    ollama active t0+14 s; preload OK 01:56:24 (boot→ready 98 s), Result=success
11 01:57 exit=0 ssh cycle-1 guard [evidence 05/05b] — identity EXACT (expires_at now Z — TZ flip);
    hashes match; Xid 0; OOM 0; err none; NVRM 71 lines confined ≤01:55:57; watchdog ×1;
    53/53 GPU; runner 10,610+9,380
12 01:58 exit=0 ssh cycle-1 KA [evidence 06] — 391, stop, 2.44 s, load 1.57 ms warm
13 01:58 exit=0 [local] cycle-1 evidence verified on hxs-5 (off-host by construction);
    deliverable §3/§4.1 written; cycle.sh +host-down phase (D-M8-1)
14 01:59:36 exit=0 ssh cycle-2 pre-state [evidence 07]; CYCLE 2 reboot 01:59:36.247; down +6 s;
    SSH +42 s; API +91 s; RESIDENT +126 s [evidence 02-cycle2]
15 02:02 exit=0 ssh cycle-2 post-boot [evidence 08] — t0 02:00:03; boot-id d5a72f5c…; preload OK
    02:01:41 (98 s); guard [evidence 09] EXACT, Xid 0, NVRM confined; KA [evidence 10] 391 warm
16 02:03 exit=0 [local] deliverable §4.2; cycle-2 evidence verified on hxs-5
17 02:03:34 exit=0 ssh cycle-3 pre-state [evidence 11]; CYCLE 3 reboot 02:03:34.692; down +5 s;
    SSH +44 s; API +93 s; RESIDENT +129 s [evidence 02-cycle3]
18 02:06 exit=0 ssh cycle-3 post-boot [evidence 12] — t0 02:04:02; boot-id 671be79e…; preload OK
    02:05:40 (98 s); last -x proves EXACTLY 3 reboots (01:54/02:00/02:04), no fourth
19 02:07 exit=0 ssh cycle-3 guard [evidence 13] EXACT, Xid 0, NVRM confined; KA [evidence 14]
    391 warm; 20 evidence files on hxs-5
20 02:08 exit=0 ssh+local T-BOUNDARY [evidence 15] — ss -lntp table; ufw inactive; nft/iptables
    empty; 0 :cloud tags; LAN /api/version 200 (12 ms) + /api/ps 200 (27 ms) from hxs-5;
    loopback answers; deliverable §5
21 02:09-02:10 exit=0 [local] author consumer_proof.py (56293681…); T-CONSUMER run vs LAN
    endpoint [evidence 16] — 1 call (schema-valid, first-try hit) → serial execution → grounded
    final citing hx-net-boundary-2026; 0 raw ATEM; max 1 call/response; 29.8 s total; §6
22 02:10 exit=0 ssh configuration.md facts [evidence 18] — eno1 .202/24 gw .1; masks ×4 masked;
    SecureBoot disabled; DKMS both kernels; store 17G, 3.4T free
23 02:11 exit=0 [local] servers/hxs-3/configuration.md written (FIRST of its class);
    discovery.md sha256 93bc5634… captured before [evidence 17]
24 02:13-14 exit=0 ssh T-GUARD close-out [evidence 19] — /api/ps EXACT; units enabled+active,
    NRestarts=0, preload Result=success; Xid 0; uptime continuous from cycle-3 boot
25 02:14 exit=0 [local] sanitization sweep: credential value ABSENT from all evidence +
    deliverable + configuration.md (match-status only, value never printed); thinking-content
    sweep clean; discovery.md hash re-verified unchanged
26 (task end) exit=0 [local] deliverable completed (§7-§14); askpass helper + wrappers +
    cycle.sh + consumer_proof.py deleted; sanitized evidence retained transiently at
    hxs-5:/tmp/esme-m8-hxs3/evidence/ (volatile /tmp; this document carries the record)
```

## 12. Validation summary (profile §11.4)

- **What changed:** hxs-3 was cold-rebooted exactly three times (owner-pre-approved per D6, in the governor-announced window; boot chain proves exactly three, no fourth). Repository-side, `servers/hxs-3/configuration.md` was created (FIRST of its class, server-records contract). **Nothing else changed — zero host baseline mutations** (no drop-in, Modelfile, alias, unit, model-store, sampling, firewall, endpoint, package, or OS change).
- **What did not change:** Ollama 0.32.15 (binary == server); frozen artifact `de878ce33ad8…64c1` and all four alias digests; resident identity `hx-muse-glimmer-64k` `9dffb015…e7da` ctx 65536, `size == size_vram == 18,376,336,340`, Forever; all four artifact hashes (verified ×5 checkpoints); effective environment; listener `*:11434`; units enabled+active, `NRestarts=0`; no firewall; swap 0 B; rick's entire plane (masks, rfkill, DKMS, UTC/NTP); `discovery.md` byte-identical.
- **What was tested:** T-IDENT; T-DRIFT-0 (14 items vs frozen references); T-CYCLE-1/2/3 (full per-cycle protocol: pre-state, boot-id delta, poll timeline vs D5, identity guard EXACT, preload `Result=success`, journal + Xid + `NRestarts` sweep, warm KA, immediate off-host evidence); T-BOUNDARY (listener shape, LAN 200 ×2, ufw/nft/iptables, `:cloud` scan, blueprint §5 statement + O1 residual); T-CONSUMER (RAG-shaped one-call-per-turn task end-to-end, native sampling, shape/conformance/latency); T-CONFIG-MD (contract conformance; discovery preserved); T-RECONCILE (SC-01…SC-08); T-GUARD (close-out identity + sanitization sweeps).
- **Passed:** every mandatory test — **persistence 3/3** (boot→ready 98 s deterministic, detection ≤94 s, no human action post-issue), boundary, consumer-proof, configuration.md, close-out. **Failed:** no mandatory test. **Not run:** out-of-subnet refusal (no authorized host — recorded); SC-06 multimodal probes (never in any milestone's scope — OPEN for owner disposition, §8). **Disclosed:** F-M8-1 transcript disclosure (contained); D-M8-1 scaffolding artifact (corrected openly). No test re-run to reach a pass; bounded corrections 0 of 1.
- **Current Ollama state:** 0.32.15 binary == server, active/enabled, `NRestarts=0`, `*:11434` wildcard with loopback preserved, web search ACTIVE (owner 2026-08-26), 0 `:cloud` tags.
- **Current model state:** `hx-muse-glimmer-64k:latest` resident, digest `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`, 100% VRAM across both 5060 Ti (10,610 + 9,380 MiB), ctx 65536, Forever — as of the 02:13Z close-out guard, 9 min into the cycle-3 boot.
- **Endpoint/security state:** LAN 192.168.50.0/24 is the boundary (blueprint §5); no host firewall (proven: ufw inactive, nft/iptables empty); no service-layer auth (ratified); O1 tripwire clean; no credentials in any artifact (sweep CLEAN).
- **Resource/performance state:** resident 17.11 GiB of 31.86 GiB aggregate VRAM; warm KA ~2.4–3.2 s with sub-3 ms `load_duration`; consumer-path eval ~24.6 tok/s; zero Xid/OOM across the whole session.
- **Rollback readiness:** nothing to roll back (no baseline change); the frozen baseline is the steady state; M4/M7 inverse procedures stand unmodified.
- **Remaining risks/decisions:** SC-06 OPEN (owner: defer or commission); registry workload-field divergence (owner-side, F-REG-1 class); carried monitor-only classes (NVRM teardown assertions, F-E2 watchdog, F-M6-1 probes); O1 residual until an authenticating gateway (owner decision). Handoff: this deliverable goes to Carol for catalog receipt — OPEN until the receipt is cited in the state log; the owner's ACCEPT decision follows (governor presents it).

**Completion gate (profile §18):** TKV reviewed and cited; target confirmed hxs-3; binary/server/model versions reconciled; tests defined before the first mutation; pre-state captured per cycle; every action authorized, bounded, reversible; all mandatory tests executed and passed; GPU residency proven per cycle; digests and effective context captured; the consumer contract exercised end-to-end; the security boundary proven not assumed; secrets and thinking content excluded (sweeps CLEAN); configs/hashes/command log/test report attached; the summary describes the true current state; SC-06 openly unresolved-for-owner rather than concealed; another engineer can reproduce from this package.

**Completion: `PASS — TASK COMPLETE`** (M8 evidence package ready for the KK3 gate and the owner's ACCEPT / ACCEPT WITH CONDITIONS / REJECT verdict — SC-06 flagged as the one item without executed evidence)

`Task May Proceed: YES`

## 13. Second Brain evaluation (standing directive + work order)

1. **Opportunity identified:** yes — the blueprint's M8 sign-off gate applied to the second backend class; `configuration.md` instantiates the server-records contract for the first time. 2. **Roadmap capability/pattern:** the sign-off pattern itself (hxs-1 proven, second validated use) plus the first production server record; capability LIMITS (`parallel_tool_calling: false`) become enforcement-backed registry content. 3. **Disposition:** **implemented** — this sign-off evidence and `servers/hxs-3/configuration.md` become Meta-X's production record; the backend-capability registration flips `candidate → active` at the owner's ACCEPT (post-deliverable wave, governor's lane, not this task). 4. **Evidence/reasoning:** M8 is the gate that converts a candidate into a production backend; every prior milestone exists to make this one cheap — and it was: 3/3 deterministic recoveries, boundary and consumer proofs first-pass, zero stop conditions, zero baseline drift, one record class instantiated.

## 14. Handoff

Deliverable `15-esme-m8-signoff.md` goes to **Carol** for catalog receipt; per the context packet, **handoff OPEN until the receipt is cited in the state log**; the owner's ACCEPT decision follows the deliverable (governor presents it). Sanitized session evidence retained transiently at `hxs-5:/tmp/esme-m8-hxs3/evidence/` (volatile `/tmp`; this document carries the record): `00-identity`, `01a/01b/01c-drift`, `02-cycle{1,2,3}-reboot-poll`, `03/07/11-cycle{1,2,3}-prestate`, `04/08/12-cycle{1,2,3}-postboot`, `05/05b-cycle1-guard+nvrm`, `09-cycle2-guard`, `13-cycle3-guard`, `06/10/14-cycle{1,2,3}-ka.json`, `15-boundary`, `16-consumer-proof.json`, `17-discovery-pre.sha256`, `18-configmd-facts`, `19-closeout-guard`. No scratch was ever created on hxs-3 (captures streamed to hxs-5 at execution time — F-M5-1 satisfied by construction). The askpass helper, SSH wrappers, `cycle.sh`, and `consumer_proof.py` are deleted at task end (deletion verified, command log row 26); the pinned known_hosts entry predates this session and is shared fleet state — left in place.

---

Sanitization confirmed: no secrets, tokens, cookies, private prompts, user data, or thinking content in this document or the session evidence (close-out sweeps CLEAN — credential value absent from every artifact, match-status checked without printing it; thinking persisted as presence/character counts only). All prompts synthetic; LAN addresses and the public host-key fingerprint are ratified non-secret content. One transcript-only disclosure (F-M8-1) is recorded openly in §9.

Signed: **john / Esme** — Expert Ollama Engineer
Session `john-m8-hxs3-20260827-01` · WO-HXS3-JOHN-M8-001 · 2026-08-27T02:16Z (UTC)

## Addendum — F-M8-1 containment audit (governor, 2026-08-27; review batch 15)

The review finding was correct that the file/tmp sweeps did not establish containment. Governor audit (count-only; transcript files never read, so the value never re-entered any transcript; mechanism per occurrence untraced by design):

- The SSH credential's value appears **32 times across 7 session-transcript files** (wire.jsonl of 6 agent sessions + the governor's main session), all under `/home/hxsa/.kimi-code/sessions/` on hxs-5 — directory mode 700 (owner account only).
- **Zero occurrences anywhere else**: repository, /tmp, evidence artifacts, catalog, GitHub (full-history gitleaks scan clean; the CI gate scans every push).
- Retention: wire.jsonl files are per-session runtime state on hxs-5 (disposable; purge is an owner word away). Access: owner account only per fs mode.

Rotation remains the owner's standing decision (declined; the finding's "rotate before acceptance" demand is recorded here with the audit evidence — exposure is bounded to the owner's own machine session logs, not the world). Containment statement: the credential exists in exactly two places — the protected record (`keys.md/ssh-info.md`, mode 0600) and the session transcripts above. Nothing anywhere else.
