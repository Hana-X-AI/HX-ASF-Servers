# Fleet Baseline — hxs-11, hxs-20, hxs-21 — 2026-08-28

| Field | Value |
| --- | --- |
| Task ID | rick-fleet-baseline-20260828-01 |
| Agent | Rick (Ubuntu Server Engineer) |
| Commission | Governor Kimi-K3 session commission on owner word 2026-08-28: "hxs-11, hxs-20 and hxs-21 are online and ready for Rick"; same scope as `servers/2026-08-27-fleet-baseline-wave.md` (FULL baseline) |
| Targets | hxs-11 .210 (returned from maintenance); hxs-20 (NEW, replaces hxs-7's role) — live **.220**; hxs-21 (NEW, provisioning to eventually replace the hxs-5 machine) — live **.21** (addressing: Section 2) |
| Executor host | hxs-5 (192.168.50.204) |
| Scope | Identity/OS vs discovery; `fleet-verify-baseline.sh` vs `fleet-standard.yaml`; NTP pin + sleep-mask align (the ONLY two sanctioned mutation classes); selftest green at both gates; TKV records refreshed |
| Boundaries | Everything else read-only; any other mutation need → record, skip, escalate; zero secret values in any artifact |
| Execution window | 2026-08-28T01:09Z – 2026-08-28T01:23Z (all times UTC) |
| Result | **PASS — TASK COMPLETE** (3/3 hosts carry verdicts: 1 PASS, 2 REPORT with declared closing directions, 0 FAIL) |

## 1. Knowledge review receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu surveyed 2026-08-28T01:09-01:12Z — the
        release-matched reference set for THIS task:
        refs-ubuntu-24.04 (MANIFEST: 13 files, noble-pinned:
        man1-timedatectl, man5-timesyncd.conf, man8-systemd-timesyncd.service,
        man8-systemd-sleep, man8-systemd-suspend.service, man5-systemd.unit,
        man7-systemd.special, man8-ufw, man8-dmidecode, netplan-yaml-stable,
        server-guide time-synchronisation/netplan/security)
Target Host/Scope: 3 commissioned hosts — baseline verification + the two
  sanctioned mutation classes
Reviewed At: 2026-08-28T01:09-01:12Z
Relevant Files: agents/rick/charter.md + profile.md; AGENTS.md (owner rules:
  no host firewalls, Secure Boot posture, no-Docker, local-model-first);
  servers/AGENTS.md + /opt/tkv-local/servers/AGENTS.md (records contracts);
  scripts/fleet/ (README, fleet-standard.yaml sha256 4c298ea6…, all scripts);
  servers/SERVER-REGISTRY.md (IP manifest); servers/2026-08-27-fleet-baseline-wave.md
  (proven pattern + doc shape); /opt/tkv-local/servers/hxs-11/discovery.md +
  pre-work-results.md (owner console record incl. host-key fingerprint);
  servers/hxs-20/discovery.md + servers/hxs-21/discovery.md (owner-supplied
  interactive evidence, 2026-08-28)
Ubuntu Release/Kernel Identified: all 3 hosts Ubuntu 24.04.4 LTS, kernel
  7.0.0-30-generic, x86_64 (proven live, Sections 2 and 4)
Applicable Authority/Runbooks/Tests: this commission (controlling contract);
  profile §8.9 (time sync), §16 (fleet discipline); scripts/fleet/README.md
  usage contracts; 08-27 wave evidence as proven pattern
Configuration Owners Identified: systemd-timesyncd owns NTP (no competing
  daemon on any host); timedatectl owns timezone; systemd unit masks own
  sleep-target state; /etc/ufw/ufw.conf owns the firewall switch (OFF ×3)
Contradictions or Gaps: two, both resolved with evidence, both values kept —
  (a) WO IPs for hxs-20/hxs-21 (.219/.220) vs live (.220/.21): owner-supplied
  discovery addresses proven real (Section 2); (b) WO states all three hosts
  absent from fleet-standard.yaml host_classes: hxs-11 IS present
  (server-default, since the 08-27 amendment); only hxs-20/hxs-21 are absent
  (Section 6, F-2). No escalation required.
Task May Proceed: YES
```

Local-model-first rule (owner standing directive): (1) this work order is **not model-required** — deterministic fleet administration executed by the commissioned script library with scripted verification; no model inference produced any work product. (2) Backend: n/a. The session substrate is orchestration mechanics per the rule's stated exception. No cloud contact occurred.

## 2. Authority and target confirmation

- Work order: Kimi-K3 commission rick-fleet-baseline-20260828-01 (2026-08-28) on owner word — controlling contract; two sanctioned mutation classes named explicitly.
- **Addressing resolution (the fleet pattern does NOT hold):** WO carried hxs-20 = .219 and hxs-21 = .220 (pattern `199+N`). Live network truth:
  - .219 — no ping response (01:13Z);
  - .220 — answers as hostname `hx-20` (= hxs-20 per the owner-supplied discovery: recorded prompt `hx-20`, recorded eno1 .220; boot 00:23:48Z consistent with the owner session 00:21-00:24Z);
  - .21 — answers as hostname `hxs-21` (MATCH the owner-supplied discovery's recorded prompt and recorded eno1 .21).
  Both values kept; the owner-supplied discovery addresses are proven real. hxs-21's .21 sits **outside the fleet .200–.214 block** (its discovery already flagged registration verification). Closing direction: governor/owner record real addressing at fleet registration.
- Identity verified live at 01:14Z: hxs-11 `machine-id 159714e4ce7042378888410aa03fd3de` MATCH `/opt/tkv-local/servers/hxs-11/discovery.md`; hxs-20 `7b5cd0b865e5462682a619a5b0c9d894` and hxs-21 `773a45171ba5413fa70d4b3215c43f97` — first live readings (owner-supplied discoveries carried none), recorded in the new TKV pre-work files.
- Host-key ceremonies (hxs-5 `~/.ssh/known_hosts`; `StrictHostKeyChecking=yes` on every connection):
  - **hxs-11 .210: PINNED-NEW-VERIFIED** (01:13Z) — `fleet-hostkey-pin.sh` vs the owner pre-work console record (`SHA256:l/PvbuOeocV2GGUscDKS/VuyGZGfOgu2FKhdavZimUo`), EXACT MATCH, strict re-verify passed.
  - **hxs-20 .220: TOFU-with-corroboration (D-record)** — no fingerprint exists in any HX record; precedent rick F-05 (hxs-2/hxs-3). Presented ED25519 **`SHA256:ZUEHfcFL+1Ru070e163g0uJDT7eOwlQh3MW8NZF3Mco`** pinned, identity immediately corroborated vs the owner-supplied discovery (hostname/IP/boot window). Recorded in the TKV pre-work file; a mismatch must halt future sessions.
  - **hxs-21 .21: TOFU-with-corroboration (D-record)** — same basis. Presented ED25519 **`SHA256:3ygj6lZMictGTCBZuq1R04VbnECUN4XS0Lq2Pr3gYk8`** pinned; corroborated (hostname/IP MATCH).
- Credential handling: `SSH_ASKPASS` helper (mode 0700) read the credential record row (`awk -F'|'` on the 'SSH password' row of the governed record) at execution time only, via `SSH_ASKPASS_REQUIRE=force` + `DISPLAY`; remote privilege via the scripts' `sudo -S` stdin passthrough (all 3 hosts additionally confirmed passwordless-sudo live via `sudo -n true`). The value was never printed, logged, stored, or placed in argv. Helpers deleted at session end (Section 8, seq 25). The fleet credential authenticated on all three hosts — no host-access STOP condition triggered.
- Fleet DNS carries no `hx.local.arpa` records; verified IPs used throughout (name→IP map in the transport wrapper: hxs-11→.210, hxs-20→.220, hxs-21→.21).

## 3. Test and recovery plan (recorded before first mutation)

| Test ID | Property | Procedure | Expected | Pass rule | Rollback (exact inverse) |
| --- | --- | --- | --- | --- | --- |
| T-ID-1 | Identity per host | `hostname` + `machine-id` vs discovery | hxs-11 exact match; hxs-20/21 corroborate owner evidence | match/corroboration before any mutation | n/a (read-only) |
| T-ADDR-1 | Real addressing | ping + ssh identity at .219/.220/.21 | determine which host answers where | unambiguous per-host address | n/a (read-only) |
| T-LIB-1 | Library integrity | `fleet-selftest.sh` at start and end | 43/43 green both times | 0 failures | n/a (offline) |
| T-VER-1 | Baseline matrix | `fleet-verify-baseline.sh` per host | enforce-rules PASS after sanctioned classes | 0 hosts with FAIL post-change | n/a (read-only) |
| T-NTP-1 | One NTP source, per drifted host | `--dry-run` reviewed, then `--apply` | staged diff = exactly the two-line pin; post `server-contacted` cloudflare + `NTPSynchronized=yes` | script PASS line | restore stock all-commented `[Time]` file + `systemctl restart systemd-timesyncd` |
| T-MASK-1 | 4-target mask set | `fleet-sleepmasks.sh verify` then `apply` where DIVERGED | post-apply ALIGNED; symlinks → /dev/null | script PASS line | `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` |
| T-REG-1 | No failed units introduced | `systemctl --failed` per mutated host | 0 before and after | 0 after | investigate; roll back implicated change |
| T-SB-1 | Secure Boot posture recorded | inventory `mokutil --sb-state` | value recorded per host; never changed | record present in evidence | n/a (read-only; BIOS is an owner call) |

Access preservation: mutations touch no SSH/network/PAM/sudo/storage path; every connection was an independent fresh SSH session; executor remained on hxs-5. Restart impact: `systemd-timesyncd` only, on the 3 hosts (commission-sanctioned). No reboot required or performed. Pre-change state for rollback: all 3 hosts carried the stock all-commented `[Time]` timesyncd.conf (identical staged diff ×3, Section 5) and all-static sleep targets (before-evidence in every apply log).

## 4. Baseline (before) — collected 2026-08-28T01:14-01:17Z

All 3 hosts: Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic; timezone **Etc/UTC ×3**; ufw `ENABLED=no` ×3 (owner no-firewall rule satisfied); 0 failed units ×3; ollama absent ×3 (expected — none are LLM backends); passwordless sudo ×3.

| Host | Live IP | NTP server (before) | Sleep masks (before) | Secure Boot | Notes |
| --- | --- | --- | --- | --- | --- |
| hxs-11 | .210 | 185.125.190.57 (ntp.ubuntu.com) | all static | **ENABLED (record-only, F-3)** | boot 00:43:32Z (post-maintenance); 5 upgradable pkgs (F-5) |
| hxs-20 | .220 (WO said .219 — F-1) | 91.189.91.157 (ntp.ubuntu.com) | all static | disabled | hostname `hx-20` not `hxs-20` (F-1); 0 upgradable |
| hxs-21 | .21 (WO said .220 — F-1) | 185.125.190.56 (ntp.ubuntu.com) | all static | **ENABLED (record-only, F-3)** | boot 00:43:18Z (after owner session); 0 upgradable live vs 44 recorded (F-4) |

Verify-baseline at baseline: hxs-11 (official standard, class server-default) **3 PASS + 5 FAIL** — the 5 FAILs are exactly the two sanctioned classes (`time.ntp_server` + 4 mask rules). hxs-20/hxs-21: **SKIP** (no class declared — F-2); evaluated against the server-default rule set per the commission (Section 6).

Hardware corroboration (first live readings for the new hosts; hxs-11 MATCH its 08-12 discovery): hxs-11 — i5-7500, 2×16 GB Samsung DDR4 @ 2400, single NVMe 238.5G; hxs-20 — i5-7500, 2×16 GB Samsung DDR4 @ 2400 (M471A2K43DB1-CTD + M471A2K43CB1-CTD), single NVMe 238.5G; hxs-21 — i5-7500, 2×16 GB Hynix DDR4 @ 2400 (HMA82GS6DJR8N-XN + -VK, mixed revisions), single NVMe 238.5G. All root layouts: p1 vfat /boot/efi + p2 ext4 /.

## 5. Changes (execution order; all timestamps UTC 2026-08-28)

Exactly two mutation classes were executed, via the commissioned library, one host at a time, hxs-11 first (its key was verifiable against an owner record — lowest-risk first). Identical staged two-line diff on all 3 hosts (stock → pin):

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
| hxs-11 | **01:15:38Z** — server contacted ~0 s: 162.159.200.123; NTPSynchronized=yes | **01:15:39Z** — 4 symlinks → /dev/null; ALIGNED | 8/8 PASS (official standard); conf sha256 `e2b94d4b…`; 0 failed units |
| hxs-20 | **01:16:51Z** — ~0 s, 162.159.200.123, sync yes | **01:16:52Z** — ALIGNED | 8/8 PASS (run-standard); conf sha256 `e2b94d4b…`; 0 failed units |
| hxs-21 | **01:17:26Z** — ~0 s, 162.159.200.1, sync yes | **01:17:27Z** — ALIGNED | 8/8 PASS (run-standard); conf sha256 `e2b94d4b…`; 0 failed units |

`FallbackNTP=` is explicitly empty per the one-source directive (clears the compiled-in `ntp.ubuntu.com` fallback). Each apply: remote `mktemp` staging, fail-closed awk guard, diff reviewed, `install -m 0644 -o root -g root`, `systemctl restart systemd-timesyncd`, poll-verify; staged files removed by the flow (rc 0 everywhere). Mask applies created exactly four `/dev/null` symlinks per host — no service restarts.

## 6. Post-change verification — final sweep 2026-08-28T01:18Z

- Official `fleet-standard.yaml` (sha256 `4c298ea698abc202a7ce658ca534e1ee45ef8670de0b1000bcffd17d470137a4` — unchanged since the 08-27 amendment): hxs-11 **8 PASS, 0 FAIL**; hxs-20 + hxs-21 **SKIP (no class declared)** — recorded per the commission (governor adds them).
- Session run-standard (official + exactly two `host_classes` lines — hxs-20/hxs-21 as server-default; zero rule changes; diff verified exactly 2 lines; sha256 `d53b7b3ae358ac339aa42a4e26c68b900626d3dfc6e3ce4cb790f056e9b9363a`): **hxs-11 8/8, hxs-20 8/8, hxs-21 8/8; OVERALL hosts=3, hosts-with-FAIL=0.**
- `fleet-sleepmasks.sh verify` ×3: **ALIGNED ×3** (proven 4-target set).
- `/etc/systemd/timesyncd.conf` sha256 = `e2b94d4b1fbdd15a0c026a97ee37d9937f8457d0a28cba1c3a0eee8c0a349dc2` on **all 3 hosts** — the fleet-wide file-level one-source proof now extends to 15 in-scope hosts (12 from the 08-27 wave + these 3).
- Failed units: 0 ×3 (T-REG-1 PASS).
- `fleet-selftest.sh`: **43/43 PASS at session start (01:12Z) and 43/43 PASS at session end (T-LIB-1 PASS)**.
- Persistence: `timesyncd.conf` and mask symlinks are on-disk state effective immediately and at boot; timesyncd enablement unchanged (enabled, active); no reboot persistence test performed (reboots outside scope); the per-host timesyncd restart exercised the running-config path.

## 7. Findings and observations

- **F-1 (REPORT, addressing/identity drift on the new hosts):** WO addressing (.219=hxs-20, .220=hxs-21) does not match live state: **hxs-20 = .220** (hostname `hx-20`), **hxs-21 = .21**; .219 does not answer. The owner-supplied discoveries carried the real addresses. Additionally hxs-20's live hostname is `hx-20` (its discovery flagged this open) and hxs-21's .21 is outside the fleet .200–.214 block. Both values kept everywhere. Closing direction: owner/governor confirm intended addressing + hostname at fleet registration (rename is NOT a sanctioned class; not touched).
- **F-2 (record-only, standards coverage, governor lane):** `fleet-standard.yaml` host_classes carries **hxs-11** (server-default — the WO's "three hosts are NOT in it" holds only for hxs-20/hxs-21); **hxs-20 and hxs-21 are absent → SKIP**; governor will add them. The run-standard used for their matrices is documented in Section 6 (exactly +2 lines, hashes recorded).
- **F-3 (record-only, Secure Boot ENABLED on hxs-11 and hxs-21):** same class as hxs-6 (08-27 F-5). Owner directive: Secure Boot stays disabled; BIOS remediation is an owner decision. Recorded, never changed. hxs-20 is disabled (compliant).
- **F-4 (REPORT, hxs-21 update-state drift):** owner-supplied discovery (evidence 00:20:51Z) records 44 updates immediately available incl. 1 security update; live at 01:17Z reads **0 upgradable** from current apt lists (`apt update` not run — read-only). The host rebooted 00:43:18Z between the readings; the updates were applied in that window by a mechanism not established from read-only evidence. Both values kept. Owner maintenance lane.
- **F-5 (record-only, maintenance lane):** hxs-11 has 5 upgradable packages pending (from current apt lists).
- **F-6 (record-only, new TKV files):** `/opt/tkv-local/servers/hxs-20/` and `hxs-21/` did not exist; created with pre-work-results.md files carrying this wave's re-verification, first-live machine-ids, and the TOFU host-key fingerprints (D-records). hxs-11's pre-work file gained a dated re-verification section prepended (original preserved below it).
- **hxs-7 note:** untouched (role replaced by hxs-20 per owner advisory; not in this commission).

Second Brain statement (standing directive): (1) opportunity identified: no new capability — this wave consumes the already-implemented standards-as-data verification pattern (cataloged 2026-08-27); (2) capability: catalog-adjacent verification evidence, already in place; (3) disposition: deferred — no new artifact class beyond the commissioned evidence; Carol catalog intake is governor dispatch; (4) reasoning: executing an existing pattern is not a new Second Brain capability, and the wave's boundaries prohibited uncommissioned additions.

## 8. Sequential command log (sanitized)

All local commands ran as hxsa@hxs-5 (cwd `~/opt/HX-ASF-Servers` unless noted); remote commands ran as hxsa@<host> over independent fresh SSH connections via the FLEET_SSH wrapper (password via execution-time askpass, never in argv/history/logs; `sudo -S` stdin passthrough for applies). Read-tool inspections listed as `Read`/`Grep`. Credential value appears nowhere.

| Seq | Timestamp (UTC) | User/Host | Command (sanitized) | Exit | Evidence |
| ---: | --- | --- | --- | --- | ---: |
| 1 | 01:09-01:11 | hxsa@hxs-5 | Read charter, profile, repo + servers AGENTS.md, fleet README, fleet-standard.yaml, 08-27 wave doc, SERVER-REGISTRY, TKV records contract, hxs-11 TKV discovery + pre-work, hxs-20/21 owner discoveries; TKV/ ubuntu survey | 0 | §1 |
| 2 | 01:11 | hxsa@hxs-5 | `ssh-keygen -F` ×4 candidate IPs → none pinned; `ls` keydoc; grep selftest structure | 0 | §2 |
| 3 | 01:11-01:12 | hxsa@hxs-5 | Grep repo for hxs-20/21 fingerprint records → none exist (TOFU basis established) | 0 | §2 |
| 4 | 01:12 | hxsa@hxs-5 | ping sweep .210/.219/.220/.21 → .210/.220/.21 answer; .219 silent | 0 | §2, F-1 |
| 5 | 01:12 | hxsa@hxs-5 | **START GATE** `fleet-selftest.sh` → 43 checks, 0 failures | 0 | §6 |
| 6 | 01:13 | hxsa@hxs-5 | Create `/tmp/rick-fleet-baseline-20260828-askpass.sh` + `-ssh.sh` (mode 700); extraction smoke test `\| wc -c` → 10 | 0 | §2 |
| 7 | 01:13 | hxsa@hxs-5 | `fleet-hostkey-pin.sh 192.168.50.210 <hxs-11 pre-work record>` → EXACT MATCH, PINNED-NEW-VERIFIED | 0 | §2 |
| 8 | 01:14 | hxsa@hxs-11 | Identity probe: hostname / machine-id / os / kernel / date / uptime / eno1 / `sudo -n` — MATCH discovery | 0 | §2, §4 |
| 9 | 01:14 | hxsa@hxs-5 | `ssh-keyscan -t ed25519` .220 + .21 → fingerprints recorded (TOFU D-records); appended to known_hosts | 0 | §2 |
| 10 | 01:14 | hxsa@{.220,.21} | Identity probes → .220 = `hx-20` (machine-id 7b5cd0b8…), .21 = `hxs-21` (773a4517…) — corroborated vs owner discoveries | 0 | §2, F-1 |
| 11 | 01:15:08 | hxsa@hxs-11 | `fleet-inventory.sh hxs-11 --human` (baseline) | 0 | §4 |
| 12 | 01:15 | hxsa@hxs-11 | `fleet-verify-baseline.sh hxs-11` → 3 PASS, 5 FAIL (exactly the 2 sanctioned classes); ntp `--dry-run` (staged 2-line diff); masks `verify` DIVERGED | 0 (1 expected) | §4 |
| 13 | 01:15:38 | hxsa@hxs-11 | **MUTATION** `askpass \| fleet-ntp-pin.sh hxs-11 --apply` → PASS (~0 s, 162.159.200.123, sync yes) | 0 | §5 |
| 14 | 01:15:39 | hxsa@hxs-11 | **MUTATION** `askpass \| fleet-sleepmasks.sh hxs-11 apply` → ALIGNED | 0 | §5 |
| 15 | 01:15:5x | hxsa@hxs-11 | Post: verify-baseline 8/8 PASS (official standard); conf sha256 `e2b94d4b…`; failed=0 | 0 | §6 |
| 16 | 01:16:29 | hxsa@hxs-20 | `fleet-inventory.sh hxs-20 --human` (baseline); verify-baseline official → SKIP; ntp `--dry-run`; masks `verify` DIVERGED | 0 (1 expected) | §4 |
| 17 | 01:16:51/52 | hxsa@hxs-20 | **MUTATIONS** ntp `--apply` PASS (~0 s, 162.159.200.123); sleepmasks `apply` ALIGNED | 0 | §5 |
| 18 | 01:17:07 | hxsa@hxs-21 | `fleet-inventory.sh hxs-21 --human` (baseline); ntp `--dry-run`; masks `verify` DIVERGED | 0 (1 expected) | §4 |
| 19 | 01:17:26/27 | hxsa@hxs-21 | **MUTATIONS** ntp `--apply` PASS (~0 s, 162.159.200.1); sleepmasks `apply` ALIGNED | 0 | §5 |
| 20 | 01:18 | hxsa@hxs-5 | Build run-standard (official +2 class lines; diff + sha256 recorded); FINAL sweep: verify-baseline ×3 (8/8 ×3, 0 FAIL); masks verify ×3 ALIGNED; conf sha256 ×3 `e2b94d4b…`; failed=0 ×3 | 0 | §6 |
| 21 | 01:19-01:21 | hxsa@hxs-5 | Prepend dated re-verification to hxs-11 pre-work; create `/opt/tkv-local/servers/hxs-20/` + `hxs-21/` pre-work-results.md | 0 | deliverable |
| 22 | 01:21 | hxsa@hxs-5 | **END GATE** `fleet-selftest.sh` → 43 checks, 0 failures | 0 | §6 |
| 23 | 01:22 | hxsa@hxs-5 | Write this evidence doc | 0 | deliverable |
| 24 | 01:23 | hxsa@hxs-5 | Literal-credential sweep of all produced artifacts (process-substitution pattern scan — value never in argv/output) → 0 matches | 1 (no matches, expected) | §9 |
| 25 | 01:23 | hxsa@hxs-5 | `rm -f /tmp/rick-fleet-baseline-20260828-askpass.sh /tmp/rick-fleet-baseline-20260828-ssh.sh`; `ls` verify absent | 0 | §2 |

Session evidence directory: `/tmp/rick-fleet-baseline-20260828-evidence/` (hxs-5, transient; command output only, no secrets): `hxs-11-inventory.txt`, `hxs-11-verify-pre.txt`, `hxs-11-ntp-dryrun.txt`, `hxs-11-masks-pre.txt`, `hxs-11-ntp-apply.txt`, `hxs-11-masks-apply.txt`, `hxs-11-verify-post.txt`, `hxs-20-inventory.txt`, `hxs20-21-verify-official.txt`, `hxs-20-ntp-dryrun.txt`, `hxs-20-masks-pre.txt`, `hxs-20-ntp-apply.txt`, `hxs-20-masks-apply.txt`, `hxs-21-inventory.txt`, `hxs-21-ntp-dryrun.txt`, `hxs-21-masks-pre.txt`, `hxs-21-ntp-apply.txt`, `hxs-21-masks-apply.txt`, `final-sweep.txt`.

## 9. Validation summary

- **What changed:** (a) `/etc/systemd/timesyncd.conf` on hxs-11, hxs-20, hxs-21 → `NTP=time.cloudflare.com`, `FallbackNTP=` + `systemd-timesyncd` restart (timestamps §5); (b) sleep-mask 4-target set applied on the same 3 hosts; (c) hxs-5 `~/.ssh/known_hosts`: +3 pinned host keys (.210 verified against the owner record; .220/.21 TOFU-with-corroboration, D-records). Exactly the two sanctioned host-mutation classes; nothing else on any host.
- **What did not change:** packages (none), firewall (off ×3, per owner rule), SSH/network/PAM/sudo, timezones (already Etc/UTC ×3, untouched), hostnames (hx-20's rename recorded, not performed), Secure Boot (hxs-11/hxs-21 ENABLED recorded only), the official `fleet-standard.yaml` (sha256 unchanged), discovery records (all preserved; drift recorded with both values in pre-work files). No reboots.
- **Current target state:** Etc/UTC ×3; one NTP source (`time.cloudflare.com` ×3, conf sha256 `e2b94d4b…` ×3 — fleet-identical with the 12 hosts from the 08-27 wave); synchronized ×3; proven 4-target sleep-mask set ×3; library selftest green at both gates (43/43).
- **Tests:** T-ID-1 PASS ×3, T-ADDR-1 PASS (real addressing established), T-LIB-1 PASS ×2 gates, T-VER-1 PASS (0 FAIL post-change ×3), T-NTP-1 PASS ×3, T-MASK-1 PASS ×3, T-REG-1 PASS (0 failed units ×3), T-SB-1 PASS (recorded ×3). Failed/blocked/not-run: none.
- **Access and recovery state:** all access via independent SSH sessions with pinned host keys; helpers deleted and verified absent (seq 25). Rollback readiness: (a) per-host NTP — restore the stock all-commented `[Time]` file + `systemctl restart systemd-timesyncd`; (b) per-host masks — `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target`. No rollback was needed; nothing was rolled back.
- **Remaining risks/decisions:** F-1 (real addressing + hx-20 hostname — owner/governor registration call), F-2 (governor adds hxs-20/hxs-21 to `fleet-standard.yaml`), F-3 (hxs-11/hxs-21 Secure Boot — owner BIOS decision), F-4 (hxs-21 update-application mechanism — owner maintenance lane), F-5 (hxs-11 pending updates — owner maintenance lane). Resilience note carried from prior waves: `FallbackNTP=` deliberately empty per the one-source directive — a cloudflare outage leaves no fallback (directive-consistent).
- **Handoff note:** per repo governance this material handoff requires Carol's catalog receipt; dispatch is the governor's lane. No git commit performed (owner gate: commits in governor waves).

`PASS — TASK COMPLETE`
