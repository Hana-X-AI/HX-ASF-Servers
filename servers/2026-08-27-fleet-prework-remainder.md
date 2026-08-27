# Fleet Pre-Work — Remainder Hosts (2026-08-27)

| Field | Value |
| --- | --- |
| Task ID | rick-fleet-prework-remainder-2026-08-27 |
| Agent | Rick (Ubuntu OS plane) |
| Commission | Governor 2026-08-27 (owner-directed; hxs-2 state log row 58): fleet pre-work on the reachable remainder, READ-ONLY everywhere |
| Targets (in order) | hxs-6, hxs-9, hxs-10, hxs-11, hxs-12, hxs-13, hxs-14, hxs-15 |
| Excluded per owner | hxs-1..4 (production LLM, assessed), hxs-8 (done), hxs-5 (control plane), hxs-20/21 (provisioning) |
| Executor | hxs-5 |
| Boundary compliance | Zero changes on every target host — no packages, no NTP/TZ, no masks, no services, no firewall. The only writes anywhere: host-key pins in hxs-5's `~/.ssh/known_hosts` (the commissioned identity ceremony) and the refreshed pre-work records under `/opt/tkv-local/servers/` |
| Evidence window | 2026-08-27T16:2x-16:31Z (all times UTC) |
| Result | **PASS — 7 of 8 reachable and processed; 1 unreachable (reported, not forced)** |

## 1. Per-host summary

| Host | Registry IP | Reachable | Identity ceremony | machine-id vs record | Inventory | Baseline (server-default) | Divergences / flags |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hxs-6 | .205 | YES (ping+22) | ALREADY-PINNED-VERIFIED (exact match vs owner record) | MATCH | OK | 1 PASS (Etc/UTC), 1 REPORT (ntp.ubuntu.com) | **F-2: Secure Boot ENABLED** (known fleet state — see flags) |
| hxs-9 | .208 | YES | PINNED-NEW-VERIFIED | MATCH | OK | 1 PASS, 1 REPORT | none |
| hxs-10 | .209 | YES | PINNED-NEW-VERIFIED | MATCH | OK | 1 PASS, 1 REPORT | **F-3: record hygiene** (hxs-9 prompt artifact — see flags) |
| hxs-11 | .210 | **NO** | not attempted (unreachable) | — | — | — | **F-1: UNREACHABLE** (see flags) |
| hxs-12 | .211 | YES | PINNED-NEW-VERIFIED | MATCH | OK | 1 PASS, 1 REPORT | none |
| hxs-13 | .212 | YES | PINNED-NEW-VERIFIED | MATCH | OK | 1 PASS, 1 REPORT | none |
| hxs-14 | .213 | YES | PINNED-NEW-VERIFIED | MATCH | OK | 1 PASS, 1 REPORT | none |
| hxs-15 | .214 | YES | PINNED-NEW-VERIFIED | MATCH | OK | 1 PASS, 1 REPORT | none |

**Reachability count: 7/8.** Every reachable host: hostname + peer IP + machine-id matched the discovery records; host key exactly matched the owner pre-work console fingerprint record; Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic; 0 failed units; `ufw ENABLED=no`; sleep targets `static` (correct for non-LLM hosts); ollama absent (expected); NTP enabled + synchronized via distro default `ntp.ubuntu.com` (REPORT-only per the server-default class — the one-source pin is the owner's per-host call, remediation a separate authorized pass).

## 2. Live state captured (per reachable host)

| Host | CPU | RAM visible | DIMMs | Root fs | Upgradable pkgs | Uptime since (UTC) | NTP server |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hxs-6 | i5-8500T 6t | 15.4 GiB | 2 | 4% used, ~223 GB free | 21 | 2026-08-25 16:23:10 | 185.125.190.57 (ntp.ubuntu.com) |
| hxs-9 | i5-7500 4t | 31.2 GiB | 2 | 6%, ~219 GB | 18 | 2026-08-25 16:22:43 | 185.125.190.56 (ntp.ubuntu.com) |
| hxs-10 | i5-7500 4t | 15.5 GiB | 1 | 6%, ~219 GB | 18 | 2026-08-25 16:22:36 | 91.189.91.157 (ntp.ubuntu.com) |
| hxs-12 | i5-7500 4t | 31.2 GiB | 2 | 6%, ~219 GB | 18 | 2026-08-25 16:22:51 | 91.189.91.157 (ntp.ubuntu.com) |
| hxs-13 | i5-6500 4t | 31.2 GiB | 2 | 6%, ~219 GB | 21 | 2026-08-25 16:22:48 | 185.125.190.58 (ntp.ubuntu.com) |
| hxs-14 | i5-7500 4t | 31.2 GiB | 2 | 6%, ~219 GB | 18 | 2026-08-25 17:44:46 | 91.189.91.157 (ntp.ubuntu.com) |
| hxs-15 | i5-7500 4t | 31.2 GiB | 2 | 6%, ~219 GB | 21 | 2026-08-25 16:22:46 | 185.125.190.56 (ntp.ubuntu.com) |

Passwordless sudo confirmed live on all seven (`sudo -n dmidecode` succeeded — DIMM counts above). Account `hxsa` reachable on all seven. Per-host refreshed records: `/opt/tkv-local/servers/<host>/pre-work-results.md` (refresh-by-prepend — the 2026-08-27 assessment above, the original 2026-08-13 human preparation record preserved verbatim below a marker line; interpretation noted in §5).

## 3. Flags for the governor (records contradictions — never silently fixed)

- **F-1 — hxs-11 UNREACHABLE.** Registry/records IP `192.168.50.210`: ping 100% loss; TCP/22 "No route to host". Fleet DNS: `getent hosts hxs-11` and `hxs-11.hx.local.arpa` both NXDOMAIN (no other address on record; none substituted). Owner to confirm whether the host is offline/moved (hxs-3 maintenance-move precedent) — a future attempt needs only a re-run of this pass's per-host block.
- **F-2 — Secure Boot ENABLED on hxs-6 (live, mokutil).** Both discovery records (tkv + repo) already document hxs-6 and hxs-7 as the fleet's only two SB-enabled hosts — this is known state, not new drift, but it sits against the owner standing directive "Secure Boot stays disabled on HX hosts, now and always" (2026-08-24/25). hxs-7 was outside this pass's target list (excluded set covers only hxs-20/21 as provisioning — hxs-7 simply wasn't commissioned). Remediation is BIOS-level and a separate authorized pass; NOT changed here.
- **F-3 — record hygiene, hxs-10's pre-work file:** its verbatim raw output contains a prompt line reading `hxsa@hxs-9:~$ sudo sh -c 'set -e; tmp=/etc/sudoers.d/90-hx-admin.tmp…'` — an hxs-9 prompt string inside hxs-10's record (copy/paste-era artifact from preparation day). hxs-10's own live identity verified clean this pass (machine-id `4448cf54…` MATCH, fingerprint MATCH). Original left untouched; flagged, not fixed.
- **F-4 (informational):** host-key pins for hxs-9/10/12/13/14/15 were NEW to hxs-5's known_hosts (the 2026-08-13 collector ran elsewhere); hxs-6's entry pre-existed and verified. All pins matched owner console records exactly — zero first-sight acceptances.

## 4. Identity-ceremony evidence (per host)

Each: strict BatchMode probe → (first failure kept where unpinned) → live `ssh-keyscan` fingerprint → exact compare vs the owner pre-work record → pin/verify → strict re-verify. Full outputs: session evidence files `prework-<host>-ceremony.txt`. Fingerprints matched (all ED25519, from the records):

| Host | Record fingerprint (SHA256, prefix) | Ceremony result |
| --- | --- | --- |
| hxs-6 | 22p3IEFqoUBkJGGffuqFq… | ALREADY-PINNED-VERIFIED |
| hxs-9 | Q9G16exXCu3oxx6SR+lYD… | PINNED-NEW-VERIFIED |
| hxs-10 | dzEJtcvAB8Nx/Yp1chaz9… | PINNED-NEW-VERIFIED |
| hxs-12 | rVoitmZi9HHfsk5QwIkaE… | PINNED-NEW-VERIFIED |
| hxs-13 | 19oF9Bk6Vr6U3Rws/f3G5… | PINNED-NEW-VERIFIED |
| hxs-14 | 1TffSIQWjvM20vxzvRBYr… | PINNED-NEW-VERIFIED |
| hxs-15 | 5ROl/UDPCDdyRFQeOC5P3… | PINNED-NEW-VERIFIED |

## 5. Sanitized sequential command log

Local commands as hxsa@hxs-5; remote as hxsa@<host> via the askpass-backed `FLEET_SSH` wrapper (credential read at execution time from the credential-record row; never printed/logged/stored; helpers deleted at end). Every remote command read-only except the executor-side known_hosts pins.

| Seq | Timestamp (UTC) | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | ---: |
| 1 | 16:2x~ | hxs-5 | Records check: existence/size/date of repo+tkv discovery.md and pre-work-results.md ×8; registry rows ×8 (IPs confirmed 192.168.50.20x pattern) | 0 |
| 2 | 16:2x~ | hxs-5 | Extract fingerprint records, machine-ids, account/sudo state from the 8 pre-work files (all present; hxs-10 hxs-9-prompt artifact spotted → F-3) | 0 |
| 3 | 16:2x~ | hxs-5 | Read hxs-8 pre-work-results.md in full (format template) | 0 |
| 4 | 16:25~ | hxs-5 | Create askpass/ssh helpers (mode 700); extraction smoke test `\| wc -c` → 10 | 0 |
| 5 | 16:25:3x | hxs-5 | Reachability sweep in commission order: `ping -c2` + bash `/dev/tcp` TCP/22 per host → 7 UP, hxs-11 DOWN | 0 |
| 6 | 16:25:38 | hxs-5 | hxs-11 addressability: `getent hosts hxs-11` + `.hx.local.arpa` (both NXDOMAIN); ping 100% loss; `/dev/tcp` "No route to host" → recorded, moved on | 0/1 |
| 7 | 16:26:02 | hxs-6 | Ceremony: `fleet-hostkey-pin.sh 192.168.50.205 <record>` → ALREADY-PINNED-VERIFIED | 0 |
| 8 | 16:26:0x | hxs-6 | `fleet-inventory.sh hxs-6 --kv`; machine-id MATCH; `fleet-verify-baseline.sh hxs-6` → 1 PASS + 1 REPORT | 0 |
| 9 | 16:26:4x | hxs-5 | hxs-6 Secure Boot live = enabled; cross-check both discovery records (documented fleet state) → F-2 | 0 |
| 10 | 16:27:20-39 | hxs-9/10/12/13/14/15 | Per host in order: ceremony (6× PINNED-NEW-VERIFIED, exact matches), inventory --kv, machine-id MATCH ×6, baseline → 1 PASS + 1 REPORT each | 0 |
| 11 | 16:2x~ | hxs-5 | Harvest kv facts (hw/OS/time) for the refreshed records | 0 |
| 12 | 16:2x~ | hxs-5 | Write 7 refreshed `pre-work-results.md` (refresh-by-prepend; originals preserved verbatim below a marker); prepend integrity verified (hxs-6 sample: refresh block lines 1-50, original H1 at line 51) | 0 |
| 13 | 16:3x~ | hxs-5 | Write this summary; delete helpers; verify gone | 0 |

## 6. Validation summary

- **What changed:** nothing on any target host. Executor-side: six new host-key pins (verified against owner records); seven refreshed pre-work records (prepend-only, originals preserved); this summary.
- **What did not change:** any host configuration, package, service, firewall, time source, or mask anywhere. hxs-11 untouched (unreachable).
- **Tests:** reachability 7/8; identity ceremonies 7/7 exact-match; machine-ids 7/7 MATCH; baselines 7× (1 PASS + 1 REPORT); 0 unexpected states vs records (F-2/F-3 are pre-existing record state, flagged).
- **Deferred (separate authorized passes):** per-host remediation of the NTP one-source pin and pending package updates (owner calls); hxs-6/hxs-7 Secure Boot disposition (owner/BIOS); hxs-11 offline investigation (owner).

`PASS — TASK COMPLETE (7/8 reachable; 1 reported unreachable)`
