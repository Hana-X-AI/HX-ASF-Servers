# Fleet Time and Mask Pass — 2026-08-26

| Field | Value |
| --- | --- |
| Task ID | rick-fleet-time-mask-2026-08-26 |
| Agent | Rick (Ubuntu Server Engineer) |
| Commission | Owner directive 2026-08-26: "they should all use one source"; fleet consistency is Rick's lane (hxs-3 state log row 18) |
| Targets | hxs-1 192.168.50.200, hxs-2 192.168.50.201, hxs-3 192.168.50.202, hxs-4 192.168.50.203 |
| Executor host | hxs-5 (192.168.50.204) |
| Scope | Exactly three bounded items: (1) Etc/UTC on all four; (2) `NTP=time.cloudflare.com` on all four; (3) hxs-2 `hybrid-sleep.target` mask |
| Boundaries | No other config, no packages, no reboots, no service changes beyond `systemd-timesyncd` restart, no firewall, ollama undisturbed |
| Execution window | 2026-08-26T23:39:24Z – 2026-08-26T23:58Z (all times UTC) |
| Result | **PASS — TASK COMPLETE** |

## 1. Knowledge review receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (ubuntu.com-main corpus surveyed 2026-08-26T23:40Z:
        no timedatectl/timesyncd/timezone runbook exists in the corpus — it is the
        ubuntu.com web application source, not OS documentation)
Target Host/Scope: hxs-1/hxs-2/hxs-3/hxs-4 — fleet time + hxs-2 mask pass
Reviewed At: 2026-08-26T23:39-23:46Z
Relevant Files: profile agents/rick/profile.md; servers/AGENTS.md (records contract);
  AGENTS.md (no-host-firewall rule, communication contract);
  servers/SERVER-REGISTRY.md (IP manifest confirmed);
  /home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md (credential record,
  fleet access map, agent access procedure);
  pilots/PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md row 6 (mask-set divergence);
  pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/01-state-log.md row 18 (NTP audit facts;
  hxs-3 LAN loss explained as owner maintenance; this pass commissioned);
  pilots/PILOT-HX1-OLLAMA-QWEN27B-001/07-rick-os-readiness.md (hxs-1 proven mask set);
  pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/04-rick-hxs3-os-readiness.md (hxs-3 mask
  set; F-08 timezone drift Etc/UTC -> America/Panama, record-class);
  knowledge/network.md (no NTP/time guidance present)
Ubuntu Release/Kernel Identified: all four Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic,
  systemd 255.4-1ubuntu8.17 (proven live, Sections 4 and 6)
Applicable Authority/Runbooks/Tests: owner directive 2026-08-26; profile §8.9
  (time synchronization class), §16 (fleet execution discipline); ssh-info.md agent
  access procedure
Configuration Owners Identified: systemd-timesyncd owns NTP (no competing daemon on
  any host — chrony/ntp/openntpd not installed, units inactive); timedatectl owns
  timezone (/etc/localtime symlink); systemd unit masks own sleep-target state
Contradictions or Gaps: none material. Corpus gap on timesyncd noted; per profile §4
  the release-matched installed man pages and live state govern.
Task May Proceed: YES
```

## 2. Authority and target confirmation

- Work order: owner directive via governor (hxs-3 state log row 18, 2026-08-26T23:36Z) — three bounded items, background session.
- Target manifest: four hosts by registry IP; identities verified live at 2026-08-26T23:46:20-21Z — `hostname`, SSH peer IP, and `machine-id` all match `servers/<host>/discovery.md` (hxs-1 d23f871d…, hxs-2 0c249b9a…, hxs-3 d02a8e3a…, hxs-4 a3244b92…). Host keys pinned in hxs-5 `~/.ssh/known_hosts` (F-05 class); every connection ran `StrictHostKeyChecking=yes`.
- Credential handling: `SSH_ASKPASS` helper on hxs-5 read the credential record row (`awk -F'|'`, 'SSH password' row) at execution time; the value was never printed, logged, or stored; remote privilege via `sudo -S` with the same stdin mechanism. Both helpers deleted at task end and verified absent (Section 8, seq 39-40).

## 3. Test and recovery plan (recorded before first mutation)

| Test ID | Property | Procedure | Expected | Pass rule | Rollback (exact inverse) |
| --- | --- | --- | --- | --- | --- |
| T-TZ-1 | hxs-1/2/4 timezone already Etc/UTC | `timedatectl` (read-only) | Time zone: Etc/UTC | Matches; no mutation (idempotent — report only) | n/a (no change) |
| T-TZ-2 | hxs-3 timezone Etc/UTC | `sudo timedatectl set-timezone Etc/UTC` | Time zone Etc/UTC (UTC, +0000); `/etc/localtime` -> `/usr/share/zoneinfo/Etc/UTC`; Local time == Universal time | All three views agree | `sudo timedatectl set-timezone America/Panama` |
| T-NTP-1 | One named NTP source, per host | Edit `/etc/systemd/timesyncd.conf` [Time]: `NTP=time.cloudflare.com`, `FallbackNTP=` (explicit empty); `systemctl restart systemd-timesyncd` | `timedatectl timesync-status` Server: `time.cloudflare.com` (162.159.200.x); `NTPSynchronized=yes`; `NTP=yes` | Server line shows the named source AND synchronized within 45 s of restart | Restore captured pre-change file (Section 4) + `systemctl restart systemd-timesyncd` |
| T-NTP-2 | Canary discipline | hxs-1 first; fleet progression only after hxs-1 T-NTP-1 PASS | — | hxs-1 PASS before hxs-2/3/4 mutation | Stop; restore hxs-1 if needed |
| T-MASK-1 | hxs-2 mask set alignment | `sudo systemctl mask hybrid-sleep.target` | `hybrid-sleep.target` = masked; final set suspend/hibernate/hybrid-sleep/suspend-then-hibernate masked (+ sleep.target masked, known harmless superset) | `list-unit-files` view shows masked | `sudo systemctl unmask hybrid-sleep.target` |
| T-REG-1 | Ollama undisturbed, per host | `curl -sS -m 5 localhost:11434/api/version` before and after each host's mutations | HTTP JSON version reply | Same version string before/after | n/a (detection only; stop on failure) |
| T-REG-2 | No failed units introduced | `systemctl --failed` per host after changes | 0 loaded units listed | 0 | Investigate; roll back the implicated change |

Access preservation: changes touch no SSH/network/PAM/sudo/storage path; SSH sessions were independent fresh connections; executor remained on hxs-5. Restart impact: `systemd-timesyncd` only (commission-approved). No reboot required or performed.

## 4. Baseline (before) — collected 2026-08-26T23:47:36-41Z

All four hosts: Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic; `systemd-timesyncd` active and the only time daemon (chrony/chronyd/ntp/ntpd/secntp/openntpd all `inactive`; no chrony/openntpd/ntp/ntpdate packages installed); no `/etc/systemd/timesyncd.conf.d/` and no `systemd-timesyncd.service.d/` drop-ins; `/etc/systemd/timesyncd.conf` was the stock file with every `[Time]` entry commented; 0 failed units; ollama `{"version":"0.32.15"}` answering on `localhost:11434`.

| Host | Time zone (before) | NTP (before) | timesyncd server (before) | Sleep-target masks (before) | Ollama (before) |
| --- | --- | --- | --- | --- | --- |
| hxs-1 | Etc/UTC (UTC, +0000) — already target | yes / synchronized | 185.125.190.58 (ntp.ubuntu.com) | suspend, hibernate, hybrid-sleep, suspend-then-hibernate masked; sleep.target static (proven set) | 0.32.15 OK |
| hxs-2 | Etc/UTC — already target | yes / synchronized | 91.189.91.157 (ntp.ubuntu.com) | suspend, hibernate, suspend-then-hibernate, sleep masked; **hybrid-sleep static (divergent)** | 0.32.15 OK |
| hxs-3 | **America/Panama (EST, -0500) — the real change** | yes / synchronized | 185.125.190.57 (ntp.ubuntu.com) | proven set masked ×4; sleep.target static | 0.32.15 OK |
| hxs-4 | Etc/UTC — already target | yes / synchronized | 185.125.190.57 (ntp.ubuntu.com) | **all four sleep targets static (unmasked)** — out of scope, see F-1 | 0.32.15 OK |

Baseline facts corroborate the governor's 2026-08-26 audit note (hxs-3 state log row 18): all four were already NTP-enabled and synchronized via distro defaults (ntp.ubuntu.com); item 2 pinned ONE named source and was not a repair.

**Verification-command note (systemd 255):** the commissioned verifier `timedatectl show -p NTP,NTPSynchronized,Timezone` prints nothing on this fleet's systemd (255.4-1ubuntu8.17) — a single comma-joined `-p` value is not split (reproduced on hxs-5: empty output, rc=0; `timedatectl show -p NTP` works). The semantically identical working form `timedatectl show -p NTP -p NTPSynchronized -p Timezone` was used throughout and is flagged here per evidence discipline.

## 5. Changes (execution order; exact change timestamps per host)

### Item 1 — one timezone (Etc/UTC)

- hxs-1, hxs-2, hxs-4: already Etc/UTC at baseline (T-TZ-1 PASS) — idempotent, not touched, per the commission.
- hxs-3 (T-TZ-2 PASS): `sudo timedatectl set-timezone Etc/UTC` — exit 0, **changed 2026-08-26T23:52:40Z** (hxs-3 universal clock and hxs-5 clock agree). Post-change 23:53:16Z: `Time zone: Etc/UTC (UTC, +0000)`; Local time == Universal time; `/etc/localtime -> /usr/share/zoneinfo/Etc/UTC` (symlink mtime 23:52 = change time); `NTP=yes`, `NTPSynchronized=yes`.
- **EST-class end (commissioned note):** hxs-3's historical evidence timestamps are EST-labeled (America/Panama). From **2026-08-26T23:52:40Z** forward, hxs-3's local/journal timestamps are UTC-labeled; that class ends at this timestamp. Pre-change EST-labeled records remain historical fact and are not rewritten.

### Item 2 — one NTP source (time.cloudflare.com)

Identical two-line change on all four hosts. Staged via `awk` (fail-closed guard: abort unless both stock keys matched), diff reviewed before apply, applied with `install -m 0644 -o root -g root` + `systemctl restart systemd-timesyncd`. Unified diff (identical on all four):

```diff
--- /etc/systemd/timesyncd.conf	2025-11-25 18:16:31.000000000 +0000
+++ /tmp/timesyncd.conf.rick-new	(staged)
@@ -17,8 +17,8 @@
 [Time]
-#NTP=
-#FallbackNTP=ntp.ubuntu.com
+NTP=time.cloudflare.com
+FallbackNTP=
 #RootDistanceMaxSec=5
 #PollIntervalMinSec=32
 #PollIntervalMaxSec=2048
```

| Host | Role | Apply timestamp (UTC) | Result |
| --- | --- | --- | --- |
| hxs-1 | **canary** (T-NTP-2) | 2026-08-26T23:54:27Z | PASS — Server 162.159.200.123 (time.cloudflare.com), contacted ~0 s after restart; NTPSynchronized=yes; stratum 3, root distance 18.6 ms, leap normal |
| hxs-2 | fleet | 2026-08-26T23:55:27Z | PASS — Server 162.159.200.123 (time.cloudflare.com); NTPSynchronized=yes |
| hxs-3 | fleet | 2026-08-26T23:55:28Z | PASS — Server 162.159.200.123 (time.cloudflare.com); NTPSynchronized=yes |
| hxs-4 | fleet | 2026-08-26T23:55:29Z | PASS — Server 162.159.200.1 (time.cloudflare.com); NTPSynchronized=yes |

`FallbackNTP=` is set explicitly empty per the one-source directive (an empty value clears the compiled-in `ntp.ubuntu.com` fallback; a comment would have left it active). Fleet progression proceeded only after the hxs-1 canary PASS.

### Item 3 — hxs-2 sleep-mask alignment

- `sudo systemctl mask hybrid-sleep.target` on hxs-2 — exit 0, **changed 2026-08-26T23:56:20Z**; `Created symlink /etc/systemd/system/hybrid-sleep.target → /dev/null`.
- Post: `is-enabled` = masked; symlink verified `-> /dev/null` (root root).
- Final hxs-2 set: suspend, hibernate, hybrid-sleep, suspend-then-hibernate **masked** (matches the proven hxs-1/hxs-3 set) plus `sleep.target` masked — the known harmless superset carried from the hxs-2 M1 work order, retained per the commission.

## 6. Post-change verification — final fleet sweep 2026-08-26T23:57:11-15Z

| Host | Timezone | NTP / Synchronized | Current server | timesyncd.conf sha256 | Mask set (targets) | Ollama (after) | Failed units |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hxs-1 | Etc/UTC | yes / yes | 162.159.200.123 (time.cloudflare.com) | e2b94d4b…a349dc2 | proven ×4 masked; sleep static | 0.32.15 OK | 0 |
| hxs-2 | Etc/UTC | yes / yes | 162.159.200.123 (time.cloudflare.com) | e2b94d4b…a349dc2 | proven ×4 masked + sleep masked (superset) | 0.32.15 OK | 0 |
| hxs-3 | Etc/UTC | yes / yes | 162.159.200.123 (time.cloudflare.com) | e2b94d4b…a349dc2 | proven ×4 masked; sleep static | 0.32.15 OK | 0 |
| hxs-4 | Etc/UTC | yes / yes | 162.159.200.1 (time.cloudflare.com) | e2b94d4b…a349dc2 | all static (F-1, out of scope) | 0.32.15 OK | 0 |

Full sha256 (identical on all four — the "one source" file-level proof): `e2b94d4b1fbdd15a0c026a97ee37d9937f8457d0a28cba1c3a0eee8c0a349dc2`. Effective lines on all four: `NTP=time.cloudflare.com`, `FallbackNTP=`. `systemd-timesyncd` active on all four; systemd 255.4-1ubuntu8.17 on all four.

Ollama reachability proofs (T-REG-1): `curl -sS -m 5 localhost:11434/api/version` returned `{"version":"0.32.15"}` on every host — 4 baseline probes, 6 post-mutation probes, and 4 final-sweep probes: 10 post-change and 14 total, with zero failures. No ollama service was restarted or reconfigured; the owner's interactive use of hxs-3 was not waited on and not disturbed.

Uptime continuity: no host rebooted by this pass (hxs-1 up 1d7h34m, hxs-2 up 1d8h47m, hxs-4 up 1d7h33m, hxs-3 up ~40 min — hxs-3's uptime matches the day's SECOND reboot at 18:16:40 EST = 23:17Z (orderly systemd-reboot, journal-verified; initiator not on record). The 19:50Z reboot was the owner maintenance move; both predate this pass. Batch-13 note: the review finding's ~4h7m figure used the 19:50Z reboot and was superseded by the 23:17Z reboot evidence (F-M5-1 in the hxs-3 M5 deliverable; preload re-asserted residency 49 s after that boot).

Persistence: timezone (`/etc/localtime` symlink), `timesyncd.conf`, and the mask symlink are all on-disk persistent state, effective immediately and at boot; `systemd-timesyncd` enablement unchanged (enabled, active). No reboot persistence test was performed (reboots outside scope); persistence is by construction of the mechanisms, all of which survived the per-host service restart performed in item 2.

## 7. Findings and observations

- **F-1 (record-only, out of scope):** hxs-4 carries NO sleep-target masks (all four targets `static`). The blueprint/hxs-1/hxs-3 proven set is masked ×4. This pass was bounded to hxs-2's mask alignment; hxs-4 alignment is reported, not performed. Recommend the governor queue it for a future authorized hxs-4 session.
- **F-2 (record-only):** systemd 255 comma-joined `timedatectl show -p a,b,c` prints nothing; repeated `-p` flags required. See Section 4 note.
- **F-3 (historical-timestamp note, commissioned):** hxs-3 evidence timestamps before 2026-08-26T23:52:40Z are EST-labeled (America/Panama). Item 1 ends that class from that timestamp forward; pre-change EST-labeled records remain historical fact and are not rewritten.
- **F-4 (hygiene, no action taken):** `ssh-info.md` file mode is now `0600` (its "required owner security action" item 1 stands remediated); the guide's plaintext-password rotation recommendation remains an owner decision (already pending per hxs-2 state log row 4). Not touched here — outside the three items.

## 8. Sequential command log (sanitized)

All local commands ran as hxsa@hxs-5 (cwd `~` unless noted); remote commands ran as hxsa@<host> over independent fresh SSH connections (password via askpass helper, never in argv/history/logs). Read-tool file inspections are listed as `Read`/`Grep`. Credential value appears nowhere. `~` timestamps are approximate within the stated minute.

| Seq | Timestamp (UTC) | User/Host | Command (sanitized) | Exit | Evidence |
| ---: | --- | --- | --- | --- | ---: |
| 1 | 23:39:24 | hxsa@hxs-5 | `hostname; date --iso-8601=seconds; test -d /opt/tkv-local/ubuntu && ls /opt/tkv-local` | 0 | §1 |
| 2 | 23:39~ | hxsa@hxs-5 | Read `agents/rick/profile.md`; Read `AGENTS.md`; Read `servers/AGENTS.md` | 0 | §1 |
| 3 | 23:40~ | hxsa@hxs-5 | `ls opt/local-tkv; ls servers; ls servers/hxs-{1,2,3,4}` | 0 | §1 |
| 4 | 23:40~ | hxsa@hxs-5 | Grep `hybrid-sleep\|suspend-then-hibernate` repo-wide → located pilot state logs | 0 | §1 |
| 5 | 23:41~ | hxsa@hxs-5 | Read `pilots/PILOT-HXS2-CODERX-BACKEND-001/01-state-log.md` (row 6 mask divergence) | 0 | §1 |
| 6 | 23:41~ | hxsa@hxs-5 | `awk -F'\|'` label-only structure scan of `ssh-info.md` (no values printed) | 0 | §2 |
| 7 | 23:41~ | hxsa@hxs-5 | `ls -la ~/.ssh; awk '{print $1}' ~/.ssh/known_hosts; which sshpass ssh; ssh -V` (sshpass absent; no ssh config) | 1 | §2 |
| 8 | 23:42~ | hxsa@hxs-5 | Sanitized two-pass awk read of `ssh-info.md` lines 40-239 (credential self-redacted in awk memory) | 0 | §2 |
| 9 | 23:42~ | hxsa@hxs-5 | Grep registry rows hxs-1..4 (IP manifest); grep corpus `timedatectl\|timesyncd` (no runbook) | 0 | §1 |
| 10 | 23:43~ | hxsa@hxs-5 | Grep timezone/mask in `07-rick-os-readiness.md` (hxs-1) and `04-rick-hxs3-os-readiness.md`; tail hxs-3 state log (row 18) | 0 | §1 |
| 11 | 23:44~ | hxsa@hxs-5 | `grep -i 'ntp\|time\|timezone' knowledge/network.md` (no hits); `ls knowledge/` | 0 | §1 |
| 12 | 23:44~ | hxsa@hxs-5 | `grep -i machine-id servers/hxs-{1,2,3,4}/discovery.md` | 0 | §2 |
| 13 | 23:45 | hxsa@hxs-5 | Create `/tmp/rick-fleet-askpass.sh` + `/tmp/rick-fleet-ssh.sh` (mode 700); extraction smoke test `\| wc -c` → 10 | 0 | §2 |
| 14 | 23:46:20-21 | hxsa@hxs-{1..4} | Identity verify ×4: `hostname; $SSH_CONNECTION peer; cat /etc/machine-id; date -u` | 0 ×4 | §2 |
| 15 | 23:47:36-41 | hxsa@hxs-{1..4} | Baseline audit ×4 (os-release, kernel, timedatectl, localtime, timesync-status, timesyncd.conf, drop-ins, competing daemons, ntp packages, masks, ollama, failed units) | 0 ×4 | §4 |
| 16 | 23:47:4x | hxsa@hxs-{1..4} | sudo pre-flight ×4: askpass → ssh `sudo -S -p "" true` → SUDO_OK | 0 ×4 | §3 |
| 17 | 23:48~ | hxsa@hxs-5 | `timedatectl show -p NTP,NTPSynchronized,Timezone` quirk reproduction; `systemctl --version` | 0 | §4 F-2 |
| 18 | 23:52:40 | hxsa@hxs-3 | **MUTATION** `sudo -S timedatectl set-timezone Etc/UTC` (timestamps bracketed) | 0 | §5 |
| 19 | 23:53:15 | hxsa@hxs-3 | Verify: timedatectl; show (working form); localtime; ollama; failed | 0 | §5 |
| 20 | 23:54:09 | hxsa@hxs-1 | Stage timesyncd.conf via guarded awk → `/tmp/timesyncd.conf.rick-new`; `diff -u` reviewed | 0 | §5 |
| 21 | 23:54:27 | hxsa@hxs-1 | **MUTATION (canary)** `sudo -S install -m 0644 -o root -g root … /etc/systemd/timesyncd.conf && rm staged && systemctl restart systemd-timesyncd` | 0 | §5 |
| 22 | 23:54:47 | hxsa@hxs-1 | Canary verify: server poll (cloudflare ~0 s); timesync-status; show; conf; ollama; failed | 0 | §5 |
| 23 | 23:55:26 | hxsa@hxs-2 | Stage + diff (identical two-line change) | 0 | §5 |
| 24 | 23:55:27 | hxsa@hxs-2 | **MUTATION** install + restart systemd-timesyncd | 0 | §5 |
| 25 | 23:55:2x | hxsa@hxs-2 | Verify: server poll (~0 s); status; show; conf; ollama; failed | 0 | §5 |
| 26 | 23:55:27 | hxsa@hxs-3 | Stage + diff | 0 | §5 |
| 27 | 23:55:28 | hxsa@hxs-3 | **MUTATION** install + restart systemd-timesyncd | 0 | §5 |
| 28 | 23:55:3x | hxsa@hxs-3 | Verify: server poll (~0 s); status; show; conf; ollama; failed | 0 | §5 |
| 29 | 23:55:28 | hxsa@hxs-4 | Stage + diff | 0 | §5 |
| 30 | 23:55:29 | hxsa@hxs-4 | **MUTATION** install + restart systemd-timesyncd | 0 | §5 |
| 31 | 23:55:4x | hxsa@hxs-4 | Verify: server poll (~0 s); status; show; conf; ollama; failed | 0 | §5 |
| 32 | 23:56:20 | hxsa@hxs-2 | **MUTATION** `sudo -S systemctl mask hybrid-sleep.target` (symlink → /dev/null created) | 0 | §5 |
| 33 | 23:56:20 | hxsa@hxs-2 | Verify: is-enabled=masked; symlink; list-unit-files; ollama; failed | 0 | §5 |
| 34 | 23:57:11-15 | hxsa@hxs-{1..4} | Final fleet sweep ×4: show; server; localtime; conf sha256; masks; ollama; failed; uptime; systemd version | 0 ×4 | §6 |
| 35 | 23:58~ | hxsa@hxs-5 | `rm -f /tmp/rick-fleet-askpass.sh /tmp/rick-fleet-ssh.sh`; `ls` verify absent | 0 | §2 |
| 36 | 23:58~ | hxsa@hxs-5 | BatchMode auth probe ×4 (password path closed; no pubkey fallback exists) | 1 ×4 (expected) | §2 |

Staging-file disposal: each apply command chained `install && rm -f /tmp/timesyncd.conf.rick-new && systemctl restart` and returned rc=0 on all four hosts — remote staging files are therefore proven removed (seq 21/24/27/30). Local staging: `/tmp/rick-fleet-evidence/` (hxs-5, transient; contains command output only, no secrets).

## 9. Validation summary

- **What changed:** hxs-3 timezone America/Panama → Etc/UTC (23:52:40Z); `/etc/systemd/timesyncd.conf` on all four → `NTP=time.cloudflare.com`, `FallbackNTP=` + `systemd-timesyncd` restart (23:54:27Z / 23:55:27Z / 23:55:28Z / 23:55:29Z); hxs-2 `hybrid-sleep.target` → masked (23:56:20Z). Exactly the three commissioned items; nothing else.
- **What did not change:** packages (none installed/removed), firewall (none anywhere, per owner rule), ollama services and resident models (reachability proven before/after on all four), SSH/network/PAM/sudo, enablement states (timesyncd enabled throughout), hxs-1/2/4 timezone (already target; untouched), hxs-1/3 mask sets (already proven set; untouched), hxs-4 masks (F-1, reported only). No reboots.
- **Current target state:** one timezone (Etc/UTC ×4), one NTP source (`time.cloudflare.com` ×4, identical file sha256 ×4, synchronized ×4), hxs-2 mask set aligned to the proven hxs-1/hxs-3 set plus the noted sleep.target superset.
- **Tests:** T-TZ-1 PASS (×3, read-only), T-TZ-2 PASS, T-NTP-1 PASS (×4), T-NTP-2 PASS (canary discipline held), T-MASK-1 PASS, T-REG-1 PASS (10 post-change probes; 14 total including 4 baseline), T-REG-2 PASS (0 failed units ×4). Failed/blocked/not-run: none. The only unexpected result was the F-2 verifier-syntax quirk, handled with the equivalent working form and disclosed.
- **Access and recovery state:** all access via independent SSH sessions with pinned host keys; credential helpers deleted and verified absent (seq 35); the password auth path is closed (seq 36). Rollback readiness: (a) hxs-3 timezone — `sudo timedatectl set-timezone America/Panama`; (b) per-host NTP — restore the stock all-commented `[Time]` file (exact pre-change content captured in baseline evidence; the change is two lines) + `systemctl restart systemd-timesyncd`; (c) hxs-2 mask — `sudo systemctl unmask hybrid-sleep.target`. No rollback was needed; nothing was rolled back.
- **Remaining risks/decisions:** F-1 hxs-4 has no sleep masks (governor to queue a future authorized hxs-4 session); F-4 credential rotation remains a pending owner decision; resilience note — with FallbackNTP deliberately empty per the one-source directive, a cloudflare outage leaves no fallback source (directive-consistent; flagged for the record).
- **Handoff note:** per repo governance this material handoff requires Carol's catalog receipt; dispatch is the governor's lane. No git commit performed (owner gate: commits happen in governor waves).

`PASS — TASK COMPLETE`

---

## Addendum — hxs-4 mask alignment (owner-authorized 2026-08-27)

| Field | Value |
| --- | --- |
| Commission | Follow-up work order via governor, 2026-08-27: F-1 (above) owner-authorized for execution |
| Target | hxs-4 (192.168.50.203) ONLY |
| Authorized change (verbatim) | `sudo systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` |
| Boundaries | No packages, no reboots, no other units, no firewall, no endpoint changes; Chat-X parked posture otherwise untouched |
| Result | **PASS** — F-1 closed |

**Startup re-check:** knowledge directory `/opt/tkv-local/ubuntu` and credential record re-confirmed present at 2026-08-27T01:39:58Z; prior Knowledge Review Receipt (Section 1) stands — same release (Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic, proven live below), same configuration owner (systemd unit masks), same authority chain plus the 2026-08-27 owner authorization. Askpass/ssh helpers re-created (identical execution-time-only design), host identity re-verified live at 01:40:15Z: `host=hxs-4`, peer `192.168.50.203`, machine-id `a3244b92b98448ad83da8ecad6511889` (matches `servers/hxs-4/discovery.md`), pinned host key enforced.

**Before (2026-08-27T01:40:15Z):** all five sleep-family targets `static` (unmasked) — suspend, hibernate, hybrid-sleep, suspend-then-hibernate, sleep; no mask symlinks under `/etc/systemd/system/` (only stock `*.target.wants` dirs, the same pre-change shape hxs-1/hxs-3 exhibited); ollama `curl -sS -m 5 localhost:11434/api/version` → `{"version":"0.32.15"}` (probe run on hxs-4; it is loopback-only); 0 failed units.

**Change:** the authorized command ran at **2026-08-27T01:40:43Z** (hxs-4 clock; hxs-5 clock agrees), exit 0. systemd output: `Created symlink` → `/dev/null` for each of the four targets.

**After (2026-08-27T01:40:57Z):**

- `is-enabled` per target: suspend **masked**, hibernate **masked**, hybrid-sleep **masked**, suspend-then-hibernate **masked**;
- symlinks verified: `/etc/systemd/system/{suspend,hibernate,hybrid-sleep,suspend-then-hibernate}.target -> /dev/null` (root root, mtime 01:40 = change time);
- final `systemctl list-unit-files | grep -E 'suspend|hibernate|sleep'`: `hibernate.target masked`, `hybrid-sleep.target masked`, `suspend-then-hibernate.target masked`, `suspend.target masked`, `sleep.target static` — hxs-4 now carries the exact proven hxs-1/hxs-3 set (sleep.target untouched, matching those hosts; hxs-2's extra `sleep.target` mask remains its documented harmless superset);
- ollama after: `{"version":"0.32.15"}` — undisturbed;
- 0 failed units; uptime 1 day 9 h 17 m (no reboot).

**Fleet mask posture after this addendum:** all four LLM hosts masked on the proven 4-target set; hxs-2 additionally masks `sleep.target` (superset, previously noted). F-1 is closed.

**Command log (sanitized; all remote commands as hxsa@hxs-4, independent fresh SSH sessions, password via execution-time askpass only; A1 and A6 ran LOCALLY on hxs-5 — credential-helper lifecycle only, no remote contact):**

| Seq | Timestamp (UTC) | Command | Exit |
| ---: | --- | --- | ---: |
| A1 | 01:39:58 | hxs-5: re-check knowledge dir + credential record; create helpers (mode 700); extraction smoke test `\| wc -c` → 10 | 0 |
| A2 | 01:40:15 | hxs-4: identity (hostname/peer/machine-id); os-release/kernel; masks before; symlink listing; ollama before; failed units | 0 |
| A3 | 01:40:1x | hxs-4: sudo pre-flight (`sudo -S true`) → SUDO_OK | 0 |
| A4 | 01:40:43 | hxs-4: **MUTATION** `sudo -S systemctl mask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` | 0 |
| A5 | 01:40:57 | hxs-4: is-enabled ×4; symlink listing; final list-unit-files; ollama after; failed; uptime | 0 |
| A6 | 01:41:3x | hxs-5: `rm -f` both helpers; `ls` verify absent | 0 |

**Rollback (exact inverse, ready, not needed):** `sudo systemctl unmask suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target` — restores the captured before-state (all `static`, no mask symlinks) exactly. Persistence: mask symlinks are on-disk state, effective immediately and at boot; no reboot performed or required.

**Validation:** every commissioned check PASS (is-enabled ×4, symlinks ×4, final list-unit-files, ollama before/after identical). Failed/blocked/not-run: none. No other state on hxs-4 was modified; Chat-X's parked posture (preload/persistence/LAN) is untouched. Original document body above this addendum is preserved unchanged per the records contract (a governor-lane correction to the Section 9 probe count, landed 2026-08-27T00:58Z, is retained as-is). No git commit (governor wave follows). Helpers deleted and verified absent (A6). Credential value appears nowhere in this record.
