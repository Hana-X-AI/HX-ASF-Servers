# Fleet Baseline Wave — 2026-08-27

| Field | Value |
| --- | --- |
| Task ID | rick-fleet-baseline-20260827-01 |
| Agent | Rick (Ubuntu Server Engineer) |
| Commission | WO-02-fleet-baseline (`pilots/PILOT-FLEET-BASELINE-001/02-work-order-rick-baseline.yaml` + CP-03), governor Kimi-K3 on owner GO 2026-08-27; goal `goals/2026-08-27-fleet-baseline-deployment.md` |
| Targets | FRESH (7): hxs-6 .205, hxs-9 .208, hxs-10 .209, hxs-12 .211, hxs-13 .212, hxs-14 .213, hxs-15 .214 — RE-VERIFY (5): hxs-1 .200, hxs-2 .201, hxs-3 .202, hxs-4 .203, hxs-8 .207 |
| Excluded | hxs-5 (control plane), hxs-7 (replaced by hxs-20), hxs-20/hxs-21 (provisioning), hxs-11 (owner flag unreachable — not probed) |
| Executor host | hxs-5 (192.168.50.204) |
| Scope | Verify identity/OS vs TKV discovery; `fleet-verify-baseline.sh` vs `fleet-standard.yaml`; NTP pin + sleep-mask align (the ONLY two sanctioned mutation classes); selftest green; TKV records refreshed |
| Boundaries | Everything else read-only; any other mutation need → record, skip, escalate; hxs-6 Secure Boot record-only; zero secret values in any artifact |
| Execution window | 2026-08-27T19:55Z – 2026-08-27T20:21Z (all times UTC) |
| Result | **PASS — TASK COMPLETE** (12/12 in-scope hosts carry verdicts: 10 PASS, 2 REPORT with declared closing directions, 0 FAIL) |

## 1. Knowledge review receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu surveyed 2026-08-27T19:55-19:58Z (ubuntu.com-main
        corpus + ubuntu_mcp_server-master + refs-ubuntu-24.04 — the
        release-matched reference set for THIS task: man1-timedatectl,
        man5-timesyncd.conf, man8-systemd-timesyncd.service, man8-systemd-sleep,
        man5-systemd.unit, man8-ufw, server-guide-about-time-synchronisation)
Target Host/Scope: 12 in-scope fleet hosts (7 fresh + 5 re-verify) — baseline
  verification + the two sanctioned mutation classes
Reviewed At: 2026-08-27T19:55-19:58Z
Relevant Files: agents/rick/charter.md + profile.md; AGENTS.md (owner rules:
  no host firewalls, Secure Boot posture, no-Docker, local-model-first);
  servers/AGENTS.md + /opt/tkv-local/servers/AGENTS.md (records contracts);
  goals/2026-08-27-fleet-baseline-deployment.md;
  pilots/PILOT-FLEET-BASELINE-001/01-state-log.md, 02-work-order, 03-context-packet;
  scripts/fleet/ (README, fleet-standard.yaml, all seven scripts);
  servers/SERVER-REGISTRY.md (IP manifest);
  servers/2026-08-26-fleet-time-and-mask-pass.md (proven pattern + doc shape);
  /opt/tkv-local/servers/<host>/discovery.md machine-ids ×12;
  /opt/tkv-local/servers/<host>/pre-work-results.md (08-27 16:29Z refreshes);
  pilots/PILOT-OMNIROUTE-LAYER0-001/01-rick-l1-node-runtime.md + state log
  row 34 (hxs-8 NTP pin provenance, 16:05:59Z);
  be-great skill (standing-directive survey method)
Ubuntu Release/Kernel Identified: all 12 hosts Ubuntu 24.04.4 LTS, kernel
  7.0.0-30-generic, x86_64 (proven live, Sections 4 and 6)
Applicable Authority/Runbooks/Tests: WO-02 (controlling contract); CP-03;
  profile §8.9 (time sync class), §16 (fleet execution discipline);
  scripts/fleet/README.md usage contracts
Configuration Owners Identified: systemd-timesyncd owns NTP (no competing
  daemon on any host); timedatectl owns timezone; systemd unit masks own
  sleep-target state; /etc/ufw/ufw.conf owns the firewall switch (OFF everywhere)
Contradictions or Gaps: one apparent — hxs-8 live NTP already pinned vs the
  08-26 record ("ntp.ubuntu.com, owner call pending"); reconciled to L1-M1
  authorization (Section 2), no escalation required. fleet-standard.yaml
  comment staleness recorded as F-4 (governor lane).
Task May Proceed: YES
```

Local-model-first rule (owner standing directive): (1) this work order is **not model-required** — deterministic fleet administration executed by the script library with scripted verification; no model inference produced any work product. (2) Backend: n/a. The session substrate is orchestration mechanics per the rule's stated exception. No cloud contact occurred.

## 2. Authority and target confirmation

- Work order: WO-02-fleet-baseline (2026-08-27T19:40Z) — controlling contract; CP-03 execution-time facts; owner GO recorded in pilot state log row 1.
- Target manifest: 12 hosts by registry IP (`.N = 199+N`); identities verified live at 20:00-20:01Z — `hostname` and `machine-id` on all 12 MATCH `/opt/tkv-local/servers/<host>/discovery.md` (hxs-1 d23f871d…, hxs-2 0c249b9a…, hxs-3 d02a8e3a…, hxs-4 a3244b92…, hxs-6 0b899c56…, hxs-8 91086d52…, hxs-9 a6c24677…, hxs-10 4448cf54…, hxs-12 3b1e05cd…, hxs-13 20f3a647…, hxs-14 abc587eb…, hxs-15 62cc8758…). Host keys pre-pinned in hxs-5 `~/.ssh/known_hosts`; every connection ran `StrictHostKeyChecking=yes`; fleet DNS carries no `hx.local.arpa` records (registry IPs used throughout).
- Credential handling: `SSH_ASKPASS` helper (mode 0700) read the credential record row (`awk -F'|'` on the 'SSH password' row of the governed record) at execution time only, via `SSH_ASKPASS_REQUIRE=force` + `DISPLAY`; remote privilege via the scripts' `sudo -S` stdin passthrough (all 12 hosts additionally confirmed passwordless-sudo live via `sudo -n dmidecode`). The value was never printed, logged, stored, or placed in argv. Helpers deleted at session end (Section 8, seq 35-37).
- hxs-8 NTP provenance (reconciliation): live state `NTP=time.cloudflare.com` with conf sha256 `e2b94d4b…` and file mtime 2026-08-27T16:06:00Z exactly matches `pilots/PILOT-OMNIROUTE-LAYER0-001/01-rick-l1-node-runtime.md` seq 10-11 and OmniRoute state log row 34 — the pin was applied under that authorized work order at 16:05:59Z. Live state is consistent with current authority; the 08-26 "owner call pending" note was closed by that pass.
- hxs-6 reachability confirmed first (20:00:18Z) per CP-03 (host was briefly DOWN 2026-08-24, since recovered).

## 3. Test and recovery plan (recorded before first mutation)

| Test ID | Property | Procedure | Expected | Pass rule | Rollback (exact inverse) |
| --- | --- | --- | --- | --- | --- |
| T-ID-1 | Identity per host | `hostname` + `cat /etc/machine-id` vs discovery.md | exact match ×12 | all match before any mutation | n/a (read-only) |
| T-LIB-1 | Library integrity | `fleet-selftest.sh` at start and end | 42/42 green both times | 0 failures | n/a (offline) |
| T-VER-1 | Baseline matrix | `fleet-verify-baseline.sh <hosts>` | enforce-rules PASS; REPORT lines honest | 0 hosts with FAIL | n/a (read-only) |
| T-NTP-1 | One NTP source, per drifted host | `fleet-ntp-pin.sh <host> --dry-run` reviewed, then `--apply` | staged diff = exactly the two-line pin; post-apply `server-contacted` cloudflare + `NTPSynchronized=yes` | script PASS line | restore stock all-commented `[Time]` file + `systemctl restart systemd-timesyncd` |
| T-NTP-2 | Canary discipline | hxs-6 full sequence first (no workloads) | hxs-6 green on both classes before hosts 9/10/12/13/14/15 mutations | canary PASS before fleet progression | stop; restore hxs-6 if needed |
| T-MASK-1 | 4-target mask set | `fleet-sleepmasks.sh <host> verify` then `apply` where DIVERGED | post-apply verdict ALIGNED; symlinks → /dev/null | script PASS line | `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` |
| T-WL-1 | Workload caution (hxs-9/10) | pre-probe `postgresql`/`redis-server`/`open-webui` + listener ports before mutation; re-probe after | state identical before/after | no state change introduced | n/a (detection only) |
| T-REG-1 | No failed units introduced | `systemctl list-units --failed` per mutated host | 0 before and after | 0 after | investigate; roll back implicated change |
| T-SB-1 | hxs-6 Secure Boot recorded | `mokutil --sb-state` | value recorded | record present in evidence | n/a (read-only; never changed) |

Access preservation: mutations touch no SSH/network/PAM/sudo/storage path; every connection was an independent fresh SSH session; executor remained on hxs-5. Restart impact: `systemd-timesyncd` only on the 7 fresh hosts (commission-sanctioned). No reboot required or performed. Pre-change state for rollback: all 7 fresh hosts carried the stock all-commented `[Time]` timesyncd.conf (identical staged diff ×7, Section 5) and all-static sleep targets (before-evidence in every apply log).

## 4. Baseline (before) — collected 2026-08-27T20:01-20:08Z

All 12 hosts: Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic; timezone already **Etc/UTC ×12**; ufw `ENABLED=no` ×12 (owner no-firewall rule satisfied); 0 failed units ×12; ollama absent on all fresh hosts (expected — none are LLM backends); passwordless sudo confirmed ×12.

| Host | Class | NTP server (before) | Sleep masks (before) | Secure Boot | Notes |
| --- | --- | --- | --- | --- | --- |
| hxs-1 | llm-host | 162.159.200.1 (time.cloudflare.com) | proven ×4 masked | disabled | proven posture holds |
| hxs-2 | llm-host | 162.159.200.123 (time.cloudflare.com) | proven ×4 masked (+sleep, documented superset) | disabled | proven posture holds |
| hxs-3 | llm-host | 162.159.200.123 (time.cloudflare.com) | proven ×4 masked | disabled | proven posture holds |
| hxs-4 | llm-host | 162.159.200.1 (time.cloudflare.com) | proven ×4 masked | disabled | proven posture holds |
| hxs-8 | server-default | 162.159.200.123 (time.cloudflare.com) — pinned 16:05:59Z under L1-M1 | **all static (diverged)** | disabled | mask drift = sanctioned class → fixed this wave |
| hxs-6 | server-default | 185.125.190.57 (ntp.ubuntu.com) | all static | **ENABLED (record-only, F-5)** | second NVMe + LVM vs 08-13 discovery (F-1) |
| hxs-9 | server-default | 185.125.190.56 (ntp.ubuntu.com) | all static | disabled | postgresql/redis-server installed, **inactive** (F-3) |
| hxs-10 | server-default | 91.189.91.157 (ntp.ubuntu.com) | all static | disabled | 1 DIMM detected vs 2 recorded (F-2); open-webui inactive (F-3) |
| hxs-12 | server-default | 91.189.91.157 (ntp.ubuntu.com) | all static | disabled | zero drift |
| hxs-13 | server-default | 185.125.190.58 (ntp.ubuntu.com) | all static | disabled | zero drift |
| hxs-14 | server-default | 91.189.91.157 (ntp.ubuntu.com) | all static | disabled | zero drift |
| hxs-15 | server-default | 185.125.190.56 (ntp.ubuntu.com) | all static | disabled | zero drift |

Verify-baseline at baseline: hxs-1..4 each 10 PASS / 0 FAIL; server-default hosts each 1 PASS (Etc/UTC) + 1 REPORT (report-level NTP rule); OVERALL 0 hosts with FAIL.

## 5. Changes (execution order; all timestamps UTC 2026-08-27)

Exactly two mutation classes were executed, via the commissioned library, one host at a time, hxs-6 canary first. Identical staged two-line diff on all 7 fresh hosts (stock → pin):

```diff
 [Time]
-#NTP=
-#FallbackNTP=ntp.ubuntu.com
+NTP=time.cloudflare.com
+FallbackNTP=
 #RootDistanceMaxSec=5
```

| Host | Class 1 — NTP pin (`fleet-ntp-pin.sh --apply`) | Class 2 — mask align (`fleet-sleepmasks.sh apply`) | Post-apply |
| --- | --- | --- | --- |
| hxs-8 (re-verify) | not needed — already pinned 16:05:59Z (L1-M1) | **20:03:42Z** — 4 symlinks → /dev/null; ALIGNED | ALIGNED; 0 failed units |
| hxs-6 (**canary**) | **20:04:39Z** — server contacted ~0 s: 162.159.200.123; NTPSynchronized=yes | **20:04:59Z** — ALIGNED | verify-baseline 0 FAIL; masks ALIGNED; conf sha256 `e2b94d4b…`; 0 failed units |
| hxs-12 | **20:06:36Z** — ~0 s, 162.159.200.123, sync yes | **20:06:37Z** — ALIGNED | as above |
| hxs-13 | **20:06:39Z** — ~0 s, 162.159.200.1, sync yes | **20:06:40Z** — ALIGNED | as above |
| hxs-14 | **20:07:05Z** — ~0 s, 162.159.200.123, sync yes | **20:07:06Z** — ALIGNED | as above |
| hxs-15 | **20:07:08Z** — ~0 s, 162.159.200.1, sync yes | **20:07:09Z** — ALIGNED | as above |
| hxs-9 | **20:09:00Z** — ~0 s, 162.159.200.123, sync yes | **20:09:01Z** — ALIGNED | as above; workload re-probe unchanged |
| hxs-10 | **20:09:03Z** — ~0 s, 162.159.200.1, sync yes | **20:09:04Z** — ALIGNED | as above; workload re-probe unchanged |

`FallbackNTP=` is explicitly empty per the one-source directive (clears the compiled-in `ntp.ubuntu.com` fallback). Each apply: remote `mktemp` staging, fail-closed awk guard, diff reviewed, `install -m 0644 -o root -g root`, `systemctl restart systemd-timesyncd`, poll-verify; staged files removed by the flow (rc 0 everywhere). Mask applies created exactly four `/dev/null` symlinks per host — no service restarts.

## 6. Post-change verification — final fleet sweep 2026-08-27T20:09-20:10Z

- `fleet-verify-baseline.sh` ×12: **OVERALL hosts=12, hosts-with-FAIL=0** (hxs-1..4: 10 PASS each; server-default hosts: 1 PASS + 1 REPORT each — the report-level rule's actual now satisfies the declared direction on every host).
- `fleet-sleepmasks.sh verify` ×8 mutated hosts: **ALIGNED ×8** (proven 4-target set).
- `/etc/systemd/timesyncd.conf` sha256 = `e2b94d4b1fbdd15a0c026a97ee37d9937f8457d0a28cba1c3a0eee8c0a349dc2` on **all 12 in-scope hosts** — the file-level one-source proof now covers the whole in-scope fleet. Effective lines ×12: `NTP=time.cloudflare.com`, `FallbackNTP=`.
- Failed units: 0 on all 8 mutated hosts (T-REG-1 PASS).
- Workload re-probe (T-WL-1): hxs-9 `postgresql=inactive redis-server=inactive`; hxs-10 `open-webui=inactive` — identical to pre-mutation state (they were inactive before; nothing was disturbed and nothing was started).
- hxs-6 Secure Boot: `mokutil --sb-state` → `SecureBoot enabled` — recorded (T-SB-1), unchanged per owner directive (BIOS is an owner call).
- `fleet-selftest.sh`: 42/42 PASS at session start (19:59Z) and 42/42 PASS at session end (T-LIB-1 PASS).
- Persistence: `timesyncd.conf` and mask symlinks are on-disk state effective immediately and at boot; timesyncd enablement unchanged (enabled, active); no reboot persistence test performed (reboots outside scope); the per-host timesyncd restart on 7 hosts exercised the running-config path.

## 7. Findings and observations

- **F-1 (REPORT, hxs-6 storage drift vs 08-13 discovery):** discovery records a single 238.5 GB NVMe, no LVM. Live: root on `nvme0n1` (unchanged) plus second device `nvme1n1` 238.5 GB with an `LVM2_member` hosting `ubuntu-vg/ubuntu-lv` (100G ext4, not mounted). Both values kept in `/opt/tkv-local/servers/hxs-6/pre-work-results.md`. Closing direction: owner confirms the second drive is expected; discovery record catches up at the next authorized refresh.
- **F-2 (REPORT, hxs-10 memory drift):** discovery records 32 GB (2×16 GB dual channel). Live (second independent reading; the 16:29Z refresh saw the same): 15.5 GiB visible, **1 DIMM populated** (16 GB Hynix `HMA82GS6CJR8N-VK`, DIMM1). One recorded module is not detected. Closing direction: owner hardware inspection (physical lane; no OS action exists).
- **F-3 (record-only, workload state):** hxs-9 `postgresql`/`redis-server` and hxs-10 `open-webui` units exist but are **inactive** with nothing on their service ports (5432/6379, 3000/8000/8080). Workload start/stop is outside this WO (service owners' lane); recorded for the governor.
- **F-4 (record-only, standards-file staleness, governor lane):** `fleet-standard.yaml` still comments "hxs-8 currently on ntp.ubuntu.com — do not change without that call" (superseded by the authorized L1-M1 pin, 16:05:59Z), and the server-default class carries no sleep-target rules while the goal declares the 4-target set fleet-wide. Editing the standards-as-data file is outside this WO's two sanctioned classes; queued for the governor.
- **F-5 (record-only, hxs-6 Secure Boot ENABLED):** matches the owner flag; BIOS remediation remains an owner decision. Recorded, never changed.
- **F-6 (record-only, maintenance lane):** upgradable packages pending: hxs-6=21, hxs-9=18, hxs-10=18, hxs-12=18, hxs-13=21, hxs-14=18, hxs-15=21 (from current apt lists; `apt update` not run — read-only).
- **hxs-11:** skipped per owner flag (unreachable) — not probed. hxs-5/hxs-7/hxs-20/hxs-21 untouched.

Second Brain statement (standing directive): (1) opportunity identified: no new capability — this wave consumes the already-implemented standards-as-data verification pattern (cataloged 2026-08-27); (2) capability: catalog-adjacent verification evidence, already in place; (3) disposition: deferred — no new artifact class beyond the commissioned evidence; the Carol catalog wave for this handoff is governor dispatch; (4) reasoning: executing an existing pattern is not a new Second Brain capability, and the wave's boundaries prohibited uncommissioned additions.

## 8. Sequential command log (sanitized)

All local commands ran as hxsa@hxs-5 (cwd `~/opt/HX-ASF-Servers` unless noted); remote commands ran as hxsa@<host> over independent fresh SSH connections via the FLEET_SSH wrapper (password via execution-time askpass, never in argv/history/logs; `sudo -S` stdin passthrough for applies). Read-tool inspections listed as `Read`/`Grep`. Credential value appears nowhere.

| Seq | Timestamp (UTC) | User/Host | Command (sanitized) | Exit | Evidence |
| ---: | --- | --- | --- | --- | ---: |
| 1 | 19:55 | hxsa@hxs-5 | Read `agents/rick/charter.md`, `profile.md`, `AGENTS.md`, WO-02, CP-03, goal | 0 | §1 |
| 2 | 19:55-58 | hxsa@hxs-5 | `ls scripts/fleet`; `hostname; date`; TKV dir checks; `ls /opt/tkv-local{,/servers}`; `ls agents/`; keydoc existence; known_hosts listing; corpus `find` survey | 0 | §1 |
| 3 | 19:56-58 | hxsa@hxs-5 | Read `fleet-standard.yaml`, `README.md`, `SERVER-REGISTRY.md`, 3 fleet scripts, `servers/AGENTS.md`, `/opt/tkv-local/servers/AGENTS.md`, 08-26 pass doc, pilot state log, hxs-6/hxs-10 pre-work records, be-great skill | 0 | §1 |
| 4 | 19:58 | hxsa@hxs-5 | `grep "Machine ID" /opt/tkv-local/servers/hxs-*/discovery.md` (12 expected values) | 0 | §2 |
| 5 | 19:59 | hxsa@hxs-5 | **START GATE** `fleet-selftest.sh` → 42 checks, 0 failures | 0 | §6 |
| 6 | 19:59 | hxsa@hxs-5 | Create `/tmp/rick-fleet-baseline-askpass.sh` + `-ssh.sh` (mode 700); extraction smoke test `\| wc -c` → 10 | 0 | §2 |
| 7 | 20:00:18 | hxsa@hxs-6 | Identity probe: hostname / peer / machine-id / date — MATCH | 0 | §2 |
| 8 | 20:00-20:01 | hxsa@hxs-{1,2,3,4,8,9,10,12,13,14,15} | Identity + uptime sweep ×11 — machine-ids MATCH ×11 (×12 total), uptimes captured | 0 | §2, §4 |
| 9 | 20:01-02 | hxsa@hxs-{1,2,3,4,8} | `fleet-verify-baseline.sh` ×5 → 0 FAIL (hxs-1..4 10 PASS; hxs-8 1 PASS + 1 REPORT) | 0 | §4 |
| 10 | 20:02 | hxsa@hxs-8 | `sha256sum`/`stat`/`grep` timesyncd.conf → `e2b94d4b…`, mtime 16:06:00Z; Grep repo → L1-M1 provenance | 0 | §2 |
| 11 | 20:02-03 | hxsa@hxs-{1,2,3,4,8} | `fleet-sleepmasks.sh verify` ×5 → ALIGNED ×4, DIVERGED hxs-8 | 0 (1 on hxs-8, expected) | §4 |
| 12 | 20:03:42 | hxsa@hxs-8 | **MUTATION** `askpass \| fleet-sleepmasks.sh hxs-8 apply` → 4 symlinks, ALIGNED | 0 | §5 |
| 13 | 20:04:06 | hxsa@hxs-6 | Pre: `fleet-inventory.sh --human`; verify-baseline; ntp-pin `--dry-run`; sleepmasks verify | 0 | §4 |
| 14 | 20:04:39 | hxsa@hxs-6 | **MUTATION (canary)** `askpass \| fleet-ntp-pin.sh hxs-6 --apply` → PASS (~0 s, sync yes) | 0 | §5 |
| 15 | 20:04:5x | hxsa@hxs-5 | Grep hxs-6 discovery storage → drift identified (F-1) | 0 | §7 |
| 16 | 20:04:59 | hxsa@hxs-6 | **MUTATION** `askpass \| fleet-sleepmasks.sh hxs-6 apply` → ALIGNED | 0 | §5 |
| 17 | 20:05:1x | hxsa@hxs-6 | Post: verify-baseline (0 FAIL); masks ALIGNED; conf sha256 `e2b94d4b…`; `mokutil --sb-state` → enabled; failed=0 | 0 | §6 |
| 18 | 20:05:50-20:06:03 | hxsa@hxs-{12,13,14,15} | Pre ×4: inventory; verify-baseline; ntp dry-run; masks verify | 0 | §4 |
| 19 | 20:06:36/37 | hxsa@hxs-12 | **MUTATIONS** ntp `--apply` PASS; sleepmasks `apply` ALIGNED | 0 | §5 |
| 20 | 20:06:39/40 | hxsa@hxs-13 | **MUTATIONS** ntp `--apply` PASS; sleepmasks `apply` ALIGNED | 0 | §5 |
| 21 | 20:07:05/06 | hxsa@hxs-14 | **MUTATIONS** ntp `--apply` PASS; sleepmasks `apply` ALIGNED | 0 | §5 |
| 22 | 20:07:08/09 | hxsa@hxs-15 | **MUTATIONS** ntp `--apply` PASS; sleepmasks `apply` ALIGNED | 0 | §5 |
| 23 | 20:07:3x | hxsa@hxs-{9,10} | Workload probes (T-WL-1): postgresql/redis/open-webui inactive; ports empty; failed=0 | 0 | §4, §7 |
| 24 | 20:07:58-20:08:02 | hxsa@hxs-{9,10} | Pre ×2: inventory; verify-baseline; ntp dry-run; masks verify | 0 | §4 |
| 25 | 20:08:1x | hxsa@hxs-5 | Grep hxs-10 discovery + earlier refresh → memory drift confirmed (F-2, both values) | 0 | §7 |
| 26 | 20:09:00/01 | hxsa@hxs-9 | **MUTATIONS** ntp `--apply` PASS; sleepmasks `apply` ALIGNED | 0 | §5 |
| 27 | 20:09:03/04 | hxsa@hxs-10 | **MUTATIONS** ntp `--apply` PASS; sleepmasks `apply` ALIGNED | 0 | §5 |
| 28 | 20:09-20:10 | hxsa@hxs-{all 12} | FINAL sweep: verify-baseline ×12 (0 FAIL); masks verify ×8 (ALIGNED); conf sha256 ×8 (`e2b94d4b…`); failed=0 ×8; workload re-probe unchanged | 0 | §6 |
| 29 | 20:10-20:14 | hxsa@hxs-5 | Prepend dated re-verification sections to `/opt/tkv-local/servers/<host>/pre-work-results.md` ×7 | 0 | deliverable |
| 30 | 20:14-20:19 | hxsa@hxs-5 | Write this evidence doc; append pilot state-log row 2 | 0 | deliverable |
| 31 | 20:19:25 | hxsa@hxs-5 | **END GATE** `fleet-selftest.sh` → 42 checks, 0 failures | 0 | §6 |
| 32 | 20:20:1x | hxsa@hxs-5 | Literal-credential sweep of all produced artifacts (process-substitution pattern scan — value never in argv/output) → 0 matches | 1 (no matches, expected) | §9 |
| 33 | 20:20:2x | hxsa@hxs-5 | `rm -f /tmp/rick-fleet-baseline-askpass.sh /tmp/rick-fleet-baseline-ssh.sh`; `ls` verify absent | 0 | §2 |
| 34 | 20:20:3x-46 | hxsa@hxs-{1..15 in-scope} | BatchMode auth probe ×12 (password path closed; no pubkey on hxs-5) | 1 ×12 (expected) | §2 |

Session evidence directory: `/tmp/rick-fleet-baseline-evidence/` (hxs-5, transient; command output only, no secrets): `reverify-verify-baseline.txt`, `reverify-sleepmasks.txt`, `hxs-8-mask-apply.txt`, `hxs-6-pre.txt`, `hxs-6-ntp-apply.txt`, `hxs-6-mask-apply.txt`, `hxs-6-post.txt`, `fresh-12131415-pre.txt`, `fresh-1213-apply.txt`, `fresh-1415-apply.txt`, `fresh-0910-pre.txt`, `fresh-0910-apply.txt`, `final-sweep.txt`.

## 9. Validation summary

- **What changed:** (a) `/etc/systemd/timesyncd.conf` on the 7 fresh hosts → `NTP=time.cloudflare.com`, `FallbackNTP=` + `systemd-timesyncd` restart (timestamps §5); (b) sleep-mask 4-target set applied on 8 hosts (hxs-6/8/9/10/12/13/14/15). Exactly the two sanctioned classes; nothing else.
- **What did not change:** packages (none), firewall (off everywhere, per owner rule), SSH/network/PAM/sudo, timezones (already Etc/UTC ×12, untouched), hxs-1..4 (read-only re-verify — zero mutations), hxs-8 timesyncd.conf (pinned under L1-M1, verified byte-identical), hxs-6 Secure Boot (recorded only), workload services on hxs-9/10 (inactive before and after), hxs-5/7/11/20/21 (untouched). No reboots.
- **Current target state:** one timezone (Etc/UTC ×12); one NTP source (`time.cloudflare.com` ×12, identical conf sha256 ×12, synchronized ×12); proven 4-target sleep-mask set on all 12 in-scope hosts (hxs-2 additionally masks `sleep.target`, its documented harmless superset); library selftest green at both gates.
- **Tests:** T-ID-1 PASS ×12, T-LIB-1 PASS ×2 gates, T-VER-1 PASS (0 FAIL ×12), T-NTP-1 PASS ×7, T-NTP-2 PASS (canary held), T-MASK-1 PASS ×8, T-WL-1 PASS (hxs-9/10 unchanged), T-REG-1 PASS (0 failed units ×8), T-SB-1 PASS (recorded). Failed/blocked/not-run: none.
- **Access and recovery state:** all access via independent SSH sessions with pinned host keys; helpers deleted and verified absent (seq 33); password auth path closed (seq 34). Rollback readiness: (a) per-host NTP — restore the stock all-commented `[Time]` file + `systemctl restart systemd-timesyncd`; (b) per-host masks — `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target`. No rollback was needed; nothing was rolled back.
- **Remaining risks/decisions:** F-1 (hxs-6 second drive — owner confirmation), F-2 (hxs-10 missing DIMM — owner hardware inspection), F-3 (hxs-9/10 workloads inactive — service owners), F-4 (standards-file comment/rules refresh — governor), F-5 (hxs-6 Secure Boot — owner BIOS decision), F-6 (pending updates — owner maintenance lane). Resilience note carried from the 08-26 pass: `FallbackNTP=` deliberately empty per the one-source directive — a cloudflare outage leaves no fallback (directive-consistent).
- **Handoff note:** per repo governance this material handoff requires Carol's catalog receipt; dispatch is the governor's lane. Pilot state-log rows appended. No git commit performed (owner gate: commits in governor waves).

`PASS — TASK COMPLETE`
