# Esme (john) — M7a: Three Cold-Reboot Recovery Cycles at the 64K Operating Profile (hxs-1)

| Field | Value |
| --- | --- |
| Report ID | ESME-M7A-REBOOT-CYCLES-001 |
| Task ID | WO-HX1-JOHN-M7A-001 (`PILOT-HX1-OLLAMA-QWEN27B-001`, milestone M7a, AC-007) |
| Agent | john / Esme (session `john-m7a-20260825-01`) |
| Host | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS; kernel 7.0.0-28-generic → **7.0.0-30-generic at cycle 1** |
| Session host | `hxs-5` (192.168.50.204); all target actions over SSH `hxsa@192.168.50.200` (askpass pattern) |
| Window (UTC) | 2026-08-25T06:34:41Z → 06:52Z; owner reboot window 06:29Z–08:29Z (state log row 40) |
| Reboots used | **3 of 3 pre-approved; 0 additional** (fourth reboot not authorized; none performed) |
| Ollama | 0.32.15 (binary == server; unchanged) |
| Operating profile | `hx-qwen3.8-27b-64k:latest` digest `766cd946…8cc99d8a`, ctx 65536 (frozen, unchanged) |
| GPUs | 2× RTX 4070 Ti SUPER 16376 MiB, driver 580.173.02 (rick's plane, untouched) |

Evidence labels per plan §2.2: FACT / AUTHORITY / INFERENCE / RECOMMENDATION. All secrets excluded: the SSH secret was used only through the askpass helper (0700, reads the value from its owner-file copy at runtime, deleted at task end); it was never printed, logged, or stored in evidence (`grep -F` sweep of all evidence files against the secret = no match). Sudo via NOPASSWD only (`sudo -n`, F-M5-2); no secret-piping. No thinking content retained (A01 §5.2): the known-answer response text and token counts only.

---

## 1. Knowledge review receipt (profile §4.3)

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session host; the profile's remote TKV path resolves locally here, as in M4/M5/M5b/M6/M6b)
Source: /opt/tkv-local/ollama
Reviewed At: 2026-08-25T06:35:54Z → 06:37Z
Relevant Files: 6 reviewed —
  ollama-main/docs/faq.mdx:289-318 (keep_alive semantics: -1 keeps loaded; 0 unloads; env override —
    basis for the keep_alive:-1 known-answer request and the keep_alive:0 prohibition)
  ollama-main/docs/context-length.mdx (VRAM-based defaults 4k/32k/256k; OLLAMA_CONTEXT_LENGTH;
    verify PROCESSOR split via ollama ps)
  ollama-main/envconfig/config.go:229-230,336 (OLLAMA_CONTEXT_LENGTH env surface)
  ollama-main/api/types.go:810,841-843 (/api/ps fields: expires_at, size_vram, context_length)
  ollama-main/docs/api.md:1763-1804 (GET /api/ps semantics — residency source of truth)
  ollama-main/docs/linux.mdx:57-89 (systemd startup service)
Authority/Version Identified: TKV source snapshot (v0.32.11-era) predates installed 0.32.15 — aging
  reference per Carol's catalog; the keep_alive/context/ps-field semantics cited are version-independent.
  Empirical API evidence on hxs-1 remains the authority for qwen3.8-specific behavior (carried gap:
  no qwen3.8 renderer in the snapshot — not exercised this milestone).
Applicable Tests/Runbooks: plan §9.2 reboot test ×3; work order WO-HX1-JOHN-M7A-001 per-cycle
  procedure + first-boot verifications; 26-rick-pre-m7-readiness NVRM escalation triggers;
  plan §4.4/4.5 residency + monitoring semantics.
Contradictions or Gaps: none new; carried TKV-snapshot gap (qwen3.8 renderer) unchanged.
Task May Proceed: YES
```

Teammate roster (profile §4.2): `agents/` contains john, kimi-k3, rick, carol — all current. Target identity verified before any action (FACT, 06:38:01Z): `hostname` = `hxs-1`; `SSH_CONNECTION` = `192.168.50.204 → 192.168.50.200:22`; `sudo -n` OK; known_hosts pin matched (`StrictHostKeyChecking=yes`).

## 2. Pre-reboot state (FACT, 06:38:34Z, evidence 01) — frozen baseline confirmed

| Item | Frozen value | Observed | Verdict |
| --- | --- | --- | --- |
| Kernel | 7.0.0-28 running; 7.0.0-30 installed, DKMS pre-built | 7.0.0-28-generic running; `/boot/vmlinuz-7.0.0-{28,30}` both present | **match** (transition expected at cycle 1) |
| Boot ID / uptime | `ef98be76…8099`, no reboot since 08-17 | identical; up 7 d 7:51 | **match** |
| Units | ollama + ollama-preload enabled/active, `NRestarts=0` | identical, `Result=success` both | **match** |
| Resident identity | `hx-qwen3.8-27b-64k:latest` `766cd946…8cc99d8a` | exact digest `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a` | **match** |
| Residency | ctx 65536, `size_vram == size`, Forever | `size_vram == size == 20,463,789,012 B`; `context_length` 65,536; expires 2318 | **match** |
| GPUs | both UUIDs; runner on both | runner PID 86958: 11,502 + 11,892 MiB; driver 580.173.02 | **match** |
| DKMS | nvidia/580.173.02 for -28 and -30 | both `installed` | **match** |
| Wi-Fi | rfkill1 soft-blocked | `soft=1 state=0` | **match** (see F-M7A-1 for the save-file content correction) |
| wait-online | enabled, `failed` (08-17 residue, D7-explained) | `Result=exit-code`, active=failed | **match** (clears at next boot — recorded only) |
| Sleep masks | ×4 masked | ×4 masked, `/dev/null` symlinks intact | **match** |
| Listener / swap | `127.0.0.1:11434` only; swap 0 B | identical | **match** |
| Ollama version | 0.32.15 binary == server | `ollama --version` 0.32.15; `/api/version` 0.32.15 | **match** |

NO DRIFT. Situational note: 3 users logged in (the owner-identified .220 sessions, F-M6-3 closed per context packet — not a contaminant concern for these cycles).

## 3. Per-cycle evidence (plan §9.2 steps 1–8 ×3)

All timestamps host clock (UTC) unless marked hxs5. "Ready" = preload unit's `/api/ps` assertion of the exact model (`hx-ollama-preload: OK - hx-qwen3.8-27b-64k resident` = `ExecMainExitTimestamp`).

### 3.1 Cycle 1 — boot ID `d643a8d7-…-7d1b6309e022` (evidence 02-cycle1, 03-cycle1, 04-cycle1, 05-cycle1)

| Step | Result (FACT) |
| --- | --- |
| (1) Pre-reboot state | §2 — frozen baseline, no drift |
| (2) Reboot | `sudo -n systemctl reboot` issued 06:43:05Z (hxs5), exit 0 |
| (3) Readiness timeline | SSH return 06:43:37Z hxs5 (+32 s); host boot 06:43:27; NVRM driver banner 06:43:31; `ollama.service` active 06:43:36 (boot+9 s); preload start 06:43:36 (one info-level `curl: (7)` connect retry, F-M6-1 class); **preload OK 06:44:27, `Result=success`**; `/api/ps` resident at first check 06:44:33Z. **Boot→ready 60 s; issue→ready 82 s** |
| (4) Units | both enabled + active; `NRestarts=0`; preload `active (exited)`, `Result=success` |
| (5) `/api/ps` | name `hx-qwen3.8-27b-64k:latest`; digest `766cd9469fb4…8cc99d8a` (exact frozen); `context_length` 65,536; `size_vram == size == 20,463,789,012 B`; expires 2318 (Forever) |
| (6) Known-answer warm inference | `17 × 23` → **391**, `done_reason stop`, wall 0.96 s, `load_duration` 0.63 ms — **no model-reload delay** (a reload would show load_duration in tens of seconds) |
| (7) GPUs + journal | `nvidia-smi -L` both UUIDs; runner PID 1882 holding 11,502 + 11,892 MiB; `ollama ps` 100% GPU / 65536 / Forever. Journal since boot: **0 Xid, 0 OOM**; 44 NVRM lines = 1 driver-load banner + 43 assertions, ALL within the runner-start window 06:43:53–06:44:14; leftover-mapping counts 4,4,4,4,1 (small) |
| (8) Evidence | `02-cycle1-reboot-poll.txt`, `03-cycle1-post-boot.txt`, `04-cycle1-first-boot-extra.txt`, `05-cycle1-preload-final.txt` |

Rick's NVRM escalation triggers evaluated: (a) any Xid — **none**; (b) assertions outside runner lifecycle — **none** (window ends 13 s before residency); (c) growing leftover-mapping counts — **no**; (d) functional symptom — **none**. Monitor-only classification holds.

### 3.2 Cycle 2 — boot ID `c4160062-…-fb441b55ad9a` (evidence 06, 02-cycle2, 03-cycle2, 07)

| Step | Result (FACT) |
| --- | --- |
| (1) Pre-reboot state (06:46:51Z) | steady state from cycle 1: same boot ID, units `success`/`NRestarts=0`, `/api/ps` frozen identity, runner on both GPUs, NVRM count stable at 44 (no spontaneous assertions since the start window) |
| (2) Reboot | issued 06:47:03Z (hxs5), exit 0 |
| (3) Readiness timeline | SSH return 06:47:34Z hxs5 (+31 s); boot 06:47:24; ollama active 06:47:33 (boot+9 s); preload start 06:47:33 (one F-M6-1-class curl retry); **preload OK 06:48:24, `Result=success`**; resident at poll 06:48:31Z. **Boot→ready 60 s; issue→ready 81 s** |
| (4) Units | both enabled + active; `NRestarts=0` |
| (5) `/api/ps` | identical frozen identity: digest `766cd946…8cc99d8a`, ctx 65,536, `size_vram == size == 20,463,789,012`, Forever |
| (6) Known-answer | **391**, stop, wall 1.00 s, `load_duration` 1.1 ms — warm, no reload |
| (7) GPUs + journal | both UUIDs; runner PID 1949 (11,502 + 11,892 MiB); 100% GPU. **0 Xid, 0 OOM**; 46 NVRM lines = banner + 45 assertions within 06:47:39–06:48:11; leftovers 4,4,4,4,1,1,-1 (negative-N variant is the class rick recorded at pre-M7 §5.1; small, not growing) |
| (8) Evidence | `06-cycle2-pre-state.txt`, `02-cycle2-reboot-poll.txt`, `03-cycle2-post-boot.txt`, `07-cycle2-preload-final.txt` |

### 3.3 Cycle 3 — boot ID `d3fc82da-…-233511fe93af` (evidence 08, 02-cycle3, 03-cycle3, 09)

| Step | Result (FACT) |
| --- | --- |
| (1) Pre-reboot state (06:49:29Z) | steady state from cycle 2; NVRM count stable at 46; otherwise as §3.2(1) |
| (2) Reboot | issued 06:49:41Z (hxs5), exit 0 |
| (3) Readiness timeline | SSH return 06:50:12Z hxs5 (+31 s); boot 06:50:02; ollama active 06:50:11 (boot+9 s); preload start 06:50:11 (one F-M6-1-class curl retry); **preload OK 06:51:02, `Result=success`**; resident at poll 06:51:09Z. **Boot→ready 60 s; issue→ready 81 s** |
| (4) Units | both enabled + active; `NRestarts=0` |
| (5) `/api/ps` | identical frozen identity: digest `766cd946…8cc99d8a`, ctx 65,536, `size_vram == size == 20,463,789,012`, Forever |
| (6) Known-answer | **391**, stop, wall 0.95 s, `load_duration` 0.74 ms — warm, no reload |
| (7) GPUs + journal | both UUIDs; runner PID 1943 (11,502 + 11,892 MiB); 100% GPU. **0 Xid, 0 OOM**; 46 NVRM lines = banner + 45 assertions within 06:50:17–06:50:49; leftovers 4,4,4,4,1,1,-1 |
| (8) Evidence | `08-cycle3-pre-state.txt`, `02-cycle3-reboot-poll.txt`, `03-cycle3-post-boot.txt`, `09-cycle3-preload-final-and-sweep.txt` |

### 3.4 Readiness timeline (all cycles, host clock)

```mermaid
flowchart LR
    A["reboot issued<br/>hxs5 clock"] --> B["host down<br/>~20 s"]
    B --> C["boot + driver banner<br/>t0 = uptime -s"]
    C --> D["ollama active<br/>t0 + 9 s"]
    D --> E["preload runs<br/>1 curl retry absorbed"]
    E --> F["runner cold load<br/>NVRM start window"]
    F --> G["preload OK<br/>READY t0 + 60 s"]
```

## 4. First-boot verification block (cycle 1, FACT unless labeled)

| Check | Required | Result | Verdict |
| --- | --- | --- | --- |
| FB1 kernel transition | 7.0.0-30 after reboot 1 (or record -28 persisting) | `uname -r` = **7.0.0-30-generic** (`#30~24.04.1-Ubuntu SMP Fri Aug 7 13:27:52 UTC 2`) | **transitioned** |
| FB2 driver re-proof on running kernel | `nvidia-smi` full + DKMS status; STOP+escalate if fail | `nvidia-smi`: driver 580.173.02, CUDA 13.0, both GPUs (02:00.0 / 81:00.0), llama-server PID 1882 on both; `dkms status`: `nvidia/580.173.02` installed for 7.0.0-28 **and** 7.0.0-30 | **PASS** — no driver work needed, none done |
| FB3 Wi-Fi persistence | rfkill1 still soft-blocked post-boot (systemd-rfkill restore; record only) | post-boot `rfkill1: soft=1 state=0`; `systemd-rfkill.service` ran 06:43:31→37, `Deactivated successfully`; re-verified after cycle 3 (still `soft=1 state=0`) | **PASS — empirically confirmed across 3 boots** |
| FB4 wait-online after boot | residue expected to clear; record only | `systemd-networkd-wait-online.service`: `Result=success`, `active (exited)`; `systemctl --failed` = **0 units** | **PASS — D7 residue cleared as predicted** |
| FB5 sleep masks | ×4 masked | `suspend`, `hibernate`, `hybrid-sleep`, `suspend-then-hibernate` all `masked`; `/dev/null` symlinks intact (Aug 25 00:13) | **PASS** |
| FB6 boundary/memory (added) | loopback-only; no swap use | `127.0.0.1:11434` only (+:22); swap 0 B; RAM 4.0 Gi used | **PASS** |

## 5. Readiness timings vs the D5 SLO (AUTHORITY: owner-confirmed D5 — detect ≤2 min, recover ≤15 min, one bounded recovery attempt)

| Metric | Cycle 1 | Cycle 2 | Cycle 3 | D5 SLO | Margin |
| --- | ---: | ---: | ---: | ---: | --- |
| Reboot-issued → SSH returns (hxs5) | 32 s | 31 s | 31 s | — (SSH liveness) | — |
| Boot → `ollama.service` active | 9 s | 9 s | 9 s | — | — |
| **Boot → model ready (preload OK)** | **60 s** | **60 s** | **60 s** | ≤900 s recovery | **15× under SLO** |
| Reboot-issued → model ready | 82 s | 81 s | 81 s | ≤900 s | ~11× under |
| Ready → known-answer warm inference | 0.96 s | 1.00 s | 0.95 s | approved timeouts | warm; `load_duration` ≤1.1 ms each |

No human intervention occurred **after the operator-issued reboot** in any cycle: once `systemctl reboot` was issued (owner-pre-approved), the boot path (driver → ollama.service → ollama-preload → `/api/ps` assertion) returned the frozen 64K operating profile to ready state autonomously, 3/3, with no action taken on the host between power-on and ready. **AC-007 PASS.** (Wording corrected 2026-08-25 per review finding — the reboot command itself was operator-issued; the recovery after it was autonomous.) Consistency note (INFERENCE): the 60 s boot→ready is dominated by the ~50 s cold runner load of the 19.06 GiB resident set; it is deterministic across cycles (identical to the second in all three).

## 6. Configuration files (profile §11.2)

None. No configuration file was created, modified, or deleted in this milestone (work-order boundary: no config changes). The three reboots are owner-pre-approved state transitions, not configuration mutations; the kernel transition 7.0.0-28 → 7.0.0-30 is the pre-staged, pre-approved boot-target change taking effect, with DKMS pre-built by rick's plane. Pre-state hashes/values were captured read-only (§2); post-boot values verified identical. Rollback, scoped (corrected 2026-08-25 per review finding): the application/configuration baseline is unchanged — nothing to roll back at that layer. The kernel layer did change: the recovery action, had 7.0.0-30 caused driver or workload failure, was rollback to the owner-approved 7.0.0-28-generic (prior GRUB entry; DKMS is built for both), which would itself have required an owner-approved additional reboot — not needed: driver re-proof passed on 7.0.0-30.

## 7. Sequential command log (profile §11.3)

Session host `hxs-5`, user `hxsa`; remote = SSH askpass wrapper (secret never on any command line; `sudo -n` only). Failures and corrections kept.

> Security-process note (corrected 2026-08-25, review finding batch 7): step 2 below extracted the SSH secret to a 0600 temp file under `/tmp/.esme-m7a` (0700 workspace). That deviates from the ratified pattern now in force: the askpass helper must READ the protected credential source at execution time — no extracted secret copy is created; helpers are deleted at task end. Containment held: 0600 file in a 0700 volatile-/tmp workspace, never echoed, deletion verified (step 21), evidence swept (`grep -F` no match — header sanitization note), no remote copies. Recorded as a security-process exception; rotation per owner standing decision (rejected — contained, same class as F-M5-1). Future work orders carry the read-at-execution wording.

```text
 1 06:34:41 exit=0 [local] hostname=hxs-5; date; tools (ssh/jq/curl); TKV dir present;
    known_hosts pin present; ssh-info.md shape probed (values masked)
 2 06:35:2x exit=0 [local] askpass workspace /tmp/.esme-m7a (0700): secret extracted by awk to
    0600 file (never echoed); askpass.sh (0700); hx1 ssh wrapper (0700)
 3 06:35:54 exit=0 [local] TKV reads: faq.mdx keep_alive, context-length.mdx, envconfig/config.go,
    api/types.go, api.md /api/ps, linux.mdx → [KNOWLEDGE REVIEW COMPLETE]
 4 06:36:5x exit=255 [local] FIRST WRAPPER with BatchMode=yes → Permission denied (BatchMode
    suppresses askpass) — my scaffolding defect; wrapper corrected (BatchMode removed,
    PreferredAuthentications=password), disclosure D-M7A-1; no target state touched
 5 06:38:01 exit=0 ssh identity verify: hostname=hxs-1; peer 192.168.50.200; sudo -n OK [evidence 00]
 6 06:38:34 exit=0 ssh cycle-1 pre-state: kernel -28 running / -30 installed; boot ID matches M2;
    units success; /api/ps frozen identity; GPUs+runner; DKMS both kernels; rfkill; wait-online
    failed (residue); masks ×4; loopback; swap 0 [evidence 01]
 7 06:41:14 exit=0 ssh rfkill save-file recheck: wlan save file content "1", mtime 04:32:16 (rick's
    save); bluetooth control pair decodes semantics → F-M7A-1 [evidence 01b]
 8 06:43:05 exit=0 CYCLE 1: sudo -n systemctl reboot; SSH return 06:43:37; new boot ID; kernel -30 [evidence 02-cycle1]
 9 06:44:23 exit=0 ssh post-boot: units; /api/ps resident poll; KA warm 391 (0.96 s, load 0.63 ms);
    GPUs; journal 0 Xid/0 OOM, NVRM 44 lines in start window [evidence 03-cycle1]
10 06:44:34 exit=0 ssh first-boot extras: kernel -30; nvidia-smi full; DKMS; rfkill soft=1/state=0;
    wait-online success; masks ×4; loopback; swap 0 [evidence 04-cycle1]
11 06:45:58 exit=0 ssh preload final: OK 06:44:27, Result=success; runner "model loaded" 06:44:27;
    prev-boot err-level comparison (ACPI/BT noise identical 08-17) [evidence 05]
12 06:46:51 exit=0 ssh cycle-2 pre-state: steady, no drift [evidence 06]
13 06:47:03 exit=0 CYCLE 2: reboot; SSH return 06:47:34; new boot ID; kernel -30 [evidence 02-cycle2]
14 06:47:45 exit=0 ssh post-boot: resident poll; KA 391 (1.00 s, load 1.1 ms); GPUs; journal clean [evidence 03-cycle2]
15 06:48:55 exit=0 ssh preload final: OK 06:48:24, Result=success [evidence 07]
16 06:49:29 exit=0 ssh cycle-3 pre-state: steady, no drift [evidence 08]
17 06:49:41 exit=0 CYCLE 3: reboot; SSH return 06:50:12; new boot ID; kernel -30 [evidence 02-cycle3]
18 06:50:29 exit=0 ssh post-boot: resident poll; KA 391 (0.95 s, load 0.74 ms); GPUs; journal clean [evidence 03-cycle3]
19 06:51:34 exit=0 ssh preload final OK 06:51:02 + final sweep: units enabled/active NRestarts=0;
    frozen identity; loopback; swap 0; rfkill ×2 devices; masks ×4; 0 failed units [evidence 09]
20 06:52-…  exit=0 [local] evidence sanitization sweep (grep -F secret vs all evidence: no match);
    write deliverable 30-esme-m7a-reboot-cycles.md
21 (task end) exit=0 cleanup: askpass helper + secret + wrappers deleted (verified); sanitized
    evidence retained transiently at hxs-5:/tmp/.esme-m7a/evidence (volatile /tmp)
```

Reboot count: exactly 3 (06:43:05Z, 06:47:03Z, 06:49:41Z) — all inside the owner window 06:29Z–08:29Z; no fourth reboot; no soak/long-idle measurement; no config change; no driver/kernel/DKMS work; no BIOS action; no network/firewall/storage change; no `keep_alive:0` client pattern; frozen evidence untouched.

## 8. Findings, risks, decisions surfaced

- **F-M7A-1 (correction to 26-rick-pre-m7-readiness §4.4, FACT):** the systemd-rfkill save file `/var/lib/systemd/rfkill/pci-0000:82:00.0:wlan` contains **`1`**, not the `0` quoted in rick's report (mtime/ctime/birth all 2026-08-25 04:32:16 — the file was never re-saved after rick's session; my read of the same file now shows `1`). Cross-check with the untouched bluetooth pair (live `soft=0` unblocked, save file `0`) and three observed boots decode the semantics: **the save file stores the `soft` value (1 = soft-blocked), which systemd-rfkill writes back to `soft` at boot**. Rick's mechanism conclusion — the Wi-Fi soft-block persists across boots — is therefore **correct and now empirically confirmed ×3** (FB3); only his quoted content digit was wrong. Recorded openly per the server records contract; no rick-plane action needed.
- **F-M7A-2 (F-E2 recurrence, FACT):** the llama-server GPU discovery watchdog WARN lines (`runner.go:584` / `llama_server.go:130`, "context deadline exceeded") recurred once per boot during the cold runner load (06:44:18 / 06:48:14 / 06:50:52), each followed within seconds by successful load and warm service. This is the carried F-E2 class (listener-readiness latency during load), benign in effect — but it is now deterministic at every cold boot on this stack. **RECOMMENDATION (not executed, out of scope):** monitors should treat one watchdog-WARN pair inside the boot load window as expected; escalate only if it repeats, appears outside a load event, or coincides with a failed/slow readiness.
- **Terminology correction (2026-08-25, review finding):** the three cycles are OS-initiated reboots (`sudo systemctl reboot`), not literal power cycles — hxs-1 has no BMC (discovery 2026-08-11) and physical power control is owner-domain. AC-007 as executed proves OS reboot recovery; a literal power-cycle variant would be a separately authorized owner-assisted exercise.
- **D-M7A-1 (disclosed scaffolding defect, corrected pre-evidence):** my first SSH wrapper carried `BatchMode=yes`, which suppresses the askpass prompt; the first connection attempt failed with `Permission denied`. Corrected before any target state was touched (target never saw a mutation attempt). Kept for honesty; analogous class to F-M6B-2.
- **Carried, unchanged:** F-M6-1 preload-vs-listener curl retry (one info-level line per boot, absorbed by bounded retry — expected during service/boot start); NVRM assertion class MONITOR-ONLY (all lines at runner lifecycle boundaries; leftovers small and non-growing across cycles: max 4 per event, cycle 1 → 3 trend flat/declining); ACPI BIOS/Bluetooth err-level boot noise identical to the 08-17 baseline (compared against `journalctl -b -1` — not a regression); R-024 AER not re-scanned this session (rick's plane; zero in his last window).
- **No stop condition triggered; no escalation required; 0 of 1 transient retry used** (no model/host transient occurred; D-M7A-1 was my own wrapper defect). Retry-budget definition (clarified 2026-08-25 per review finding): the transient-retry budget counts governor-level task retries only; the preload contract's in-band curl retries (`--retry 12 --retry-all-errors`, plan §4.3) are by-design bounded behavior, not budget consumption — they fired at most once per boot, within contract (F-M6-1 class).

## 9. Validation summary (profile §11.4)

- **What changed:** hxs-1 was cold-rebooted exactly three times (owner-pre-approved, in-window); the running kernel transitioned 7.0.0-28 → 7.0.0-30 at cycle 1 (pre-staged, DKMS pre-built); the `systemd-networkd-wait-online` D7 residue cleared at cycle 1 (`Result=success`, zero failed units).
- **What did not change:** Ollama 0.32.15 (binary == server); all model identities (base `22130167c4c2…79643`; aliases `…-32k` / `…-64k` `766cd946…8cc99d8a` / `…-128k`); every configuration file (preload script, `hx1.conf`, units — read-only verification only); units enabled+active with `NRestarts=0` every cycle; loopback-only bind; driver 580.173.02 and DKMS (untouched, re-proven); Wi-Fi soft-block (`rfkill1 soft=1 state=0` after every boot); sleep masks ×4; swap 0 B; rick's entire plane. No soak, no fourth reboot, no config/driver/BIOS/network/firewall/storage change, no `keep_alive:0`.
- **What was tested:** plan §9.2 steps 1–8 for each of three consecutive cold reboots (pre-state; approved reboot; readiness timestamps; units + NRestarts; `/api/ps` exact digest/ctx/`size_vram == size`; known-answer warm inference with no-reload proof; both-GPU proof; journal scan vs rick's NVRM triggers) plus the first-boot verification block (kernel transition, driver re-proof on the running kernel, Wi-Fi persistence, wait-online, sleep masks) and D5-SLO comparison.
- **Passed:** every mandatory test, 3/3 cycles clean. **Failed:** no mandatory test. **Disclosed corrections (none concealed):** D-M7A-1 wrapper defect (pre-evidence); F-M7A-1 rick save-file digit correction. No test was re-run to reach a pass; each cycle passed on its single execution.
- **Installed/running:** binary == server 0.32.15; `ollama.service` + `ollama-preload.service` enabled, active, `Result=success`, `NRestarts=0` (final state, cycle 3 boot `d3fc82da…`).
- **Model identity/residency (end state):** `hx-qwen3.8-27b-64k:latest` digest `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a` resident, ctx 65,536, 100% GPU (`size_vram == size == 20,463,789,012 B`), Forever; runner on both GPUs (11,502 + 11,892 MiB).
- **Endpoint/security state:** `127.0.0.1:11434` only, verified pre-state and after cycle 3; loopback remains the boundary; no auth assumed; owner-identified .220 sessions present (F-M6-3 closed).
- **Resource/performance state:** RAM ~4 Gi used; swap 0 B; boot→ready 60 s ×3 (15× under the 900 s D5 recovery SLO); known-answer warm path ~1 s with sub-ms load_duration every cycle.
- **Rollback readiness:** nothing to roll back — no configuration changed; the frozen baseline is the steady state the host now sits in.
- **Remaining risks/decisions:** F-M7A-1 (record correction; no action), F-M7A-2 (F-E2 watchdog WARN deterministic at cold boot → monitoring guidance recommendation to KK3; no config change authorized or made); soak remains owner-delayed (no activity here); 24h soak + idle-residency (AC-008) still open for the later owner window.
- **Budgets:** one session used; transient retry 0 of 1 used; three reboots of three authorized used; no stop condition triggered; no escalation required.

**Completion: `PASS — TASK COMPLETE`** (final gate §18: every applicable question answered yes — TKV reviewed, identity verified, versions reconciled, tests predefined per plan §9.2, pre-state captured, actions authorized/bounded, all mandatory tests executed and passed, residency/digest/context proven, security boundary proven, evidence sanitized, state described truthfully; both corrections disclosed).

---

Sanitization confirmed: no secrets, tokens, cookies, private prompts, user data, or thinking content in this document; the only prompt used is the synthetic known-answer fixture (`17 × 23`); LAN addresses already ratified in plan §3. The askpass helper, secret copy, and SSH wrapper were deleted at task end (deletion verified); sanitized session evidence retained transiently at `hxs-5:/tmp/.esme-m7a/evidence/` (volatile `/tmp`; this deliverable carries the record).

Signed: **john / Esme** — Expert Ollama Engineer
Session `john-m7a-20260825-01` · WO-HX1-JOHN-M7A-001 · 2026-08-25T06:52Z (UTC)
