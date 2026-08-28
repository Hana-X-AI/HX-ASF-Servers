# hxs-15 — DSH runtime preparation (Node + pnpm + service user)

| Field | Value |
| --- | --- |
| Task | Owner-approved DSH full-implementation plan: prepare hxs-15 as the DeepSeek Harness host (runtime + account scaffolding ONLY — dsh itself is Morpheus's lane) |
| Agent | Rick (Ubuntu OS plane), session rick-hxs15-dsh-prep-20260828-01 |
| Target | hxs-15 (192.168.50.214) — ONLY |
| Executor | hxs-5 (192.168.50.204) |
| Execution window | 2026-08-28T08:25–08:29Z (all times UTC) |
| Owner directive | NATIVE install host — NO sandbox, NO cage (no egress lockdown, no loopback-only constraints, no firewall changes) — complied: nothing network-restricting was configured; no firewall touched |
| Credential handling | SSH via `SSH_ASKPASS` temp helper (mode 0700) extracting the governed credential at execution time only; value never printed/logged/stored; helper deleted at session end. Remote privilege via `sudo -n` (passwordless sudo confirmed live) |
| Host key | Pre-pinned ED25519 known_hosts entry for 192.168.50.214; `StrictHostKeyChecking=yes` |
| Result | **PASS — TASK COMPLETE** |

## 1. Identity (MATCH vs discovery)

| Fact | Live (2026-08-28T08:26:29Z) | discovery.md (2026-08-13) | Verdict |
| --- | --- | --- | --- |
| hostname | `hxs-15` | `hxs-15` | MATCH |
| SSH peer | connected to `192.168.50.214:22` | `192.168.50.214` | MATCH |
| machine-id | `62cc8758d1854524989541c2af1be5b9` | `62cc8758d1854524989541c2af1be5b9` | MATCH |

## 2. Platform envelope

- OS: Ubuntu 24.04.4 LTS (noble); arch x86_64; kernel `7.0.0-30-generic` (discovery had `7.0.0-28-generic` at 2026-08-13 — updated since; consistent with fleet)
- CPU: Intel Core i5-7500 @ 3.40 GHz, 1 socket × 4 cores × 1 thread (4 threads, no SMT)
- Memory: 31 GiB usable (32 GB installed, 2×16 GB, platform maximum), 30 GiB available at task time
- Disk: `/` ext4 on `/dev/nvme0n1p2`, 233 GB total, 210 GB free (6% used)
- Note from discovery (unchanged, informational): VT-x not exposed on this host (iss-011) — irrelevant to a native Node service; no KVM workload in this task

## 3. Node v24.20.0 — artifact authentication (before install)

Exact proven pattern from rick's hxs-8 runtime work (`pilots/PILOT-OMNIROUTE-LAYER0-001/01-rick-l1-node-runtime.md`): official nodejs.org tarball, no package manager, no repo.

- Artifact: `node-v24.20.0-linux-x64.tar.xz` (31,838,904 bytes) from `https://nodejs.org/dist/v24.20.0/`
- sha256 `2f2c0da162318f0de47665410c7c8c2ed3d36c8f3105de4bbc61176c70a7cbf2` — **MATCH** against nodejs.org's published `SHASUMS256.txt` (fetched fresh 2026-08-28T08:25Z)
- **GPG Good signature** on `SHASUMS256.txt.asc`: made 2026-08-26T14:25:36Z, EDDSA key `5BE8A3F6C8A5C01D106C0AD820B1A390B168D356`, "Antoine du Hamel" (Node.js release team), verified against the official `nodejs/release-keys` `gpg/pubring.kbx` keyring (fetched from the org's GitHub). Trust warning is web-of-trust absence only; the keyring is the documented trust path
- Signed payload vs `.txt`: identical except one trailing blank line (same reconciled whitespace delta as the hxs-8 run; the tarball's hash line is identical in both)
- Immutability cross-check: hash and byte size identical to the artifact verified for hxs-8 on 2026-08-27
- Transport to hxs-15 re-hashed on the host: identical sha256 (`2f2c0da1…cbf2`)

## 4. Node install + smoke

- Install (08:27:12Z, single sudo block): extract to `/opt/node-v24.20.0` (`--strip-components=1`), `chown -R root:root`, symlinks `/usr/local/bin/{node,npm,npx,corepack}` → `/opt/node-v24.20.0/bin/…`
- Smoke (08:27:15Z): `node --version` → **v24.20.0**; `npm`/`npx` → 11.19.0; no-write eval → `runtime: v24.20.0 linux x64 | execPath: /opt/node-v24.20.0/bin/node`; tree 208M root:root
- Pin mechanism: immutable per-version artifact + versioned `/opt/node-v24.20.0` directory (nothing auto-updates it — no apt, no snap) + this record's hashes. The npm 12.0.2 upgrade notice was deliberately NOT taken (pinned runtime as commissioned)

## 5. pnpm 11.7.0 — pinned, integrity evidence

- Path decision: `npm install -g pnpm@11.7.0` (system-wide inside the versioned runtime tree `/opt/node-v24.20.0/lib/node_modules/pnpm`, root:root) chosen over corepack — corepack activates per-user via `~/.cache`, the wrong shape for a dedicated service account; npm -g serves all users from the pinned runtime tree
- Registry integrity metadata (fetched 08:27:39Z from registry.npmjs.org, verified by npm during install):
  - tarball `https://registry.npmjs.org/pnpm/-/pnpm-11.7.0.tgz`
  - integrity **sha512** `GcyFLBIMcSV2DyRD7mvgyltA+fUFmN4aCaHxd1A+AQ5Xwjx3ZG4B52HeWb+HT7IqM5jDOrlpH8E+uUa28PTWIA==`
  - shasum (sha1) `bea54364524dadf0a42dae28dbfeeab25ff177e5`
  - registry signature present (`keyid SHA256:DhQ8wR5APBvFHLF/+Tc+AYvPOdTpcIDqOhxsBHRwC7U`) + SLSA provenance attestation URL published
- Smoke: `pnpm --version` → **11.7.0**; installed `package.json` reports `"name": "pnpm", "version": "11.7.0"`; symlinks `/usr/local/bin/{pnpm,pnpx}` → `/opt/node-v24.20.0/bin/…`

## 6. Service user + directories

- `dsh`: system user, uid 999 / gid 988, sole group `dsh`, home `/home/dsh` (0750), shell `/usr/sbin/nologin`, password **locked** (L), created 08:28:09Z
- **NO sudo**: `sudo -l -U dsh` → "User dsh is not allowed to run sudo on hxs-15." (verified live)
- Usability proof: `sudo -u dsh env HOME=/home/dsh sh -c "cd /tmp && pnpm --version && node --version"` → `11.7.0` / `v24.20.0` (an earlier bare `sudo -u dsh pnpm` from hxsa's cwd failed EACCES on `/home/hxsa` — invocation artifact of the test, not an install defect; re-proven correctly)
- Directories: `/opt/dsh` 0755 `dsh:dsh` (app), `/var/lib/dsh` **0750** `dsh:dsh` (data)

## 7. Time source (re-verify only — fleet standard already in force)

- `timedatectl`: `Timezone=Etc/UTC`, `NTP=yes`, `NTPSynchronized=yes`
- Effective config: `NTP=time.cloudflare.com`, `FallbackNTP=` — conf sha256 `e2b94d4b1fbdd15a0c026a97ee37d9937f8457d0a28cba1c3a0eee8c0a349dc2` (fleet-identical pin applied in the 2026-08-27 baseline wave, 20:07:08Z). No change made or needed

## 8. Boundaries compliance

- dsh (the application) NOT installed — Morpheus's lane
- OmniRoute, LLM backends, all other hosts: untouched
- No firewall/egress/loopback changes (owner native directive); no packages installed via any package manager (dpkg state untouched); no services created or restarted; 0 failed units throughout

## 9. Pre/post hashes and documented inverses

| Item | Before | After | Exact inverse |
| --- | --- | --- | --- |
| Node presence | absent (no node/npm/npx/pnpm/corepack, no node-ish dpkg) | `/opt/node-v24.20.0` (208M root:root) + 4 symlinks | `sudo rm /usr/local/bin/{node,npm,npx,corepack} && sudo rm -rf /opt/node-v24.20.0` |
| pnpm | absent | `/opt/node-v24.20.0/lib/node_modules/pnpm` + 2 symlinks, v11.7.0 | `sudo rm /usr/local/bin/{pnpm,pnpx} && sudo npm uninstall -g pnpm` |
| User | `dsh` absent | system user uid 999, nologin, locked, no sudo | `sudo userdel -r dsh` |
| Dirs | absent | `/opt/dsh` 0755, `/var/lib/dsh` 0750, both dsh:dsh | `sudo rm -rf /opt/dsh /var/lib/dsh` (empty at handoff) |
| Time config | fleet pin (sha `e2b94d4b…`) | unchanged | n/a |

## 10. Sanitized sequential command log

All local commands as hxsa@hxs-5; remote as hxsa@hxs-15 over independent SSH sessions; credential via execution-time askpass only; value appears nowhere.

| Seq | UTC | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | ---: |
| 1 | 08:24 | hxs-5 | Read task, hxs-15 discovery, hxs-8 node-runtime evidence doc | 0 |
| 2 | 08:24 | hxs-5 | Create askpass helper (0700); smoke `wc -c` → 10; curl/gpg/xz + known_hosts pin checks | 0 |
| 3 | 08:25 | hxs-5 | `curl` tarball + SHASUMS256.txt + .asc + release-keys pubring.kbx; sha256 vs published sums → MATCH | 0 |
| 4 | 08:25 | hxs-5 | GPG verify → **Good signature** (Antoine du Hamel, EDDSA …D356); payload-vs-txt diff reconciled (trailing blank line only) | 0 |
| 5 | 08:26 | hxs-15 | Identity + pre-state probe (identity MATCH; runtime/user/dirs ABSENT; 0 failed units; NTP already fleet-pinned) | 0 |
| 6 | 08:27 | hxs-5→hxs-15 | Push tarball via ssh stdin; host-side sha256 → MATCH | 0 |
| 7 | 08:27:12 | hxs-15 | **MUTATION** install: mkdir `/opt/node-v24.20.0`, `tar -xJf --strip-components=1`, chown root:root, 4 symlinks | 0 |
| 8 | 08:27:15 | hxs-15 | Smoke: node/npm/npx versions; no-write eval; layout; 0 failed units | 0 |
| 9 | 08:27:39 | hxs-15 | **MUTATION** `npm view pnpm@11.7.0 dist --json` (integrity evidence), `npm install -g pnpm@11.7.0`, 2 symlinks; smoke → 11.7.0 | 0 |
| 10 | 08:28:09 | hxs-15 | **MUTATION** `useradd -r -m -d /home/dsh -s /usr/sbin/nologin dsh`; verify no-sudo, locked, groups; mkdir/chown/chmod `/opt/dsh` (0755) + `/var/lib/dsh` (0750) | 0 |
| 11 | 08:28:31 | hxs-15 | dsh usability: node OK; pnpm EACCES on hxsa cwd (artifact) → re-probe with HOME/cwd → 11.7.0 / v24.20.0 | 0 |
| 12 | 08:28:4x | hxs-15 | Cleanup `/tmp/node-*.tar.xz`; final sweep (commands resolve, versions, NTP state, 0 failed units) | 0 |
| 13 | 08:29 | hxs-5 | Write this evidence doc; delete askpass helper; verify absent | 0 |

## 11. Validation summary

- **What changed on hxs-15:** `/opt/node-v24.20.0` + 4 `/usr/local/bin` symlinks (Node v24.20.0, authenticated); pnpm 11.7.0 global inside the runtime tree + 2 symlinks; system user `dsh` (no sudo, locked, nologin); `/opt/dsh` (0755) + `/var/lib/dsh` (0750), both dsh:dsh. Nothing else.
- **What did not change:** dpkg/apt state, repos, snap, firewall, listeners, services, NTP/time config (already fleet-standard), OmniRoute, backends, all other hosts. dsh application NOT installed.
- **Tests:** identity MATCH ×3; artifact authentication PASS (sha256 + GPG chain + immutability cross-check); smoke PASS (node/pnpm versions; dsh-context run); no-sudo PASS; NTP re-verify PASS (pin + synchronized + fleet-identical hash); 0 failed units throughout.
- **Handoff note for Morpheus:** run dsh as the `dsh` user with `HOME=/home/dsh` (or a login-shell context); runtime is on PATH for all users; `/var/lib/dsh` is the data home (0750).

`PASS — TASK COMPLETE`
