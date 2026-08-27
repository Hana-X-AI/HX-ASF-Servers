# L1-M1 — Node Runtime + NTP Pin on hxs-8 (rick)

| Field | Value |
| --- | --- |
| Work order | WO-L1-RICK-NODE-001 (`07-work-order-rick-node.yaml` + `08-context-packet-rick-node.yaml`) |
| Goal | GOAL-OMNIROUTE-L1-SECURE-CORE (`goals/2026-08-27-omniroute-layer1-secure-core.md`) |
| Agent | Rick (Ubuntu OS plane), session rick-l1-node-20260827-01 (1 of 1 budgeted) |
| Target | hxs-8 (192.168.50.207) — ONLY |
| Executor | hxs-5 (192.168.50.204) |
| Execution window | 2026-08-27T15:5xZ – 16:07Z (all times UTC) |
| Result | **PASS — TASK COMPLETE** |

## 1. Knowledge review receipt

```text
[KNOWLEDGE REVIEW COMPLETE]
Agent: Rick
Source: /opt/tkv-local/ubuntu (present, re-confirmed 2026-08-27T15:5xZ; incl. the new
        refs-ubuntu-24.04/ pack) + agents/rick/quirks.md (7 entries, standing input —
        read; quirk #7's no-restart rule applied to the NTP pin: timesyncd restart
        only, ollama-class daemons untouched)
Target Host/Scope: hxs-8 — L1-M1 Node runtime + one-source NTP pin
Reviewed At: 2026-08-27T15:5x-16:00Z
Relevant Files: 07-work-order-rick-node.yaml; 08-context-packet-rick-node.yaml;
  goals/2026-08-27-omniroute-layer1-secure-core.md (OD-04/OD-12/OD-13 parameters);
  04-rick-hxs8-readiness.md (host baseline); servers/hxs-8/discovery.md (identity);
  servers/2026-08-26-fleet-time-and-mask-pass.md (proven pin pattern);
  scripts/fleet/fleet-ntp-pin.sh (WO-authorized with --apply);
  /opt/tkv-local/OmniRoute-release-v3.8.51/package.json (engines, READ-ONLY:
  ">=22.22.2 <23 || >=24.0.0 <27")
Ubuntu Release/Kernel Identified: Ubuntu 24.04.4 LTS noble, 7.0.0-30-generic (live)
Applicable Authority/Runbooks/Tests: WO owner_authorizations (OD-12/OD-03/OD-04 +
  NTP one-source rule) and boundaries; stop conditions per WO
Configuration Owners Identified: systemd-timesyncd (NTP); manual runtime tree under
  /opt + /usr/local/bin symlinks (Node) — no package manager owns either
Contradictions or Gaps: none (pre-state matched the readiness baseline exactly;
  stop condition "unexpected host state" not triggered)
Task May Proceed: YES
```

## 2. Authority, identity, pre-state (before any mutation)

Identity verified live 16:00:59Z against `servers/hxs-8/discovery.md`: `host=hxs-8`, peer `192.168.50.207`, machine-id `91086d5265a74450b7c2047b3b7ca2ae` (all MATCH). Host key: pinned per the readiness-run ceremony (known_hosts entry verified against the owner's pre-work fingerprint record). Credential: askpass helper reading the credential-record row at execution time only; deleted at end.

Pre-state (16:00:59Z) vs readiness baseline — consistent, no unexpected state:

- OS Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic; boot continuity since 2026-08-27 01:40:06 (up 14h20m); 0 failed units; listeners only `0.0.0.0:22`, `[::]:22`, stub DNS `127.0.0.53/54:53`; 46 GiB RAM; `/` 2% used (436 GB free)
- Runtime: `node`, `nodejs`, `npm`, `npx` **ABSENT**; no node-ish dpkg packages; xz + gzip present (only documented prerequisites for the tarball path)
- `snap` binary present on host — NOT used (snap rejected out-of-lane per WO)
- `/etc/systemd/timesyncd.conf` sha256 **e6734751f8aaf19fddfff891ad246387f5f59bd9ff1a5f0cac2c34bc81941c62** (stock, 0 effective lines); NTP server `185.125.190.58 (ntp.ubuntu.com)`; Timezone Etc/UTC

## 3. Install-path decision (on evidence)

| Option | Evidence | Decision |
| --- | --- | --- |
| (a) Official nodejs.org binary tarball | Exact-version pin **by construction** (immutable per-version artifact + published SHASUMS256 + GPG-signed sums); adds ZERO apt/repo trust surface (no new source, no signing key); single-command inverse (remove dir + 3 symlinks); prerequisites already present (xz/gzip). Con: updates are manual — which is precisely what a *pinned* runtime wants | **CHOSEN** |
| (b) NodeSource apt repo (22 LTS) | Adds a third-party apt source + signing key (new trust surface); version floats with `apt upgrade` — the pin then needs a second mechanism (`apt-mark hold`); more moving parts for the same runtime. Pro (apt-managed updates) is anti-goal for a pinned runtime | Rejected for this work order |
| (c) snap | Out-of-lane surface | REJECTED by the WO outright |

**Chosen version: `v24.20.0`** (linux-x64), selected live from `https://nodejs.org/dist/index.json` (sha256 `46f40ad32ffae9c4c3760bb8044c20de8acec5d65af7cea1c17da7345e5ae865`, retrieved 16:02Z): newest in-range release on the active LTS line (Krypton, released 2026-08-26). Alternative considered: `v22.23.2` (Jod LTS, 2026-07-28) — also in range; the 24 line carries the longer LTS runway. No 25.x/26.x exists in dist (checked). Engines constraint re-verified from `/opt/tkv-local/OmniRoute-release-v3.8.51/package.json` (READ-ONLY): `"node": ">=22.22.2 <23 || >=24.0.0 <27"`.

**Pin mechanism:** the version is pinned by (1) the immutable per-version artifact (URL + sha256, GPG-signed sums), (2) the versioned install directory `/opt/node-v24.20.0` (nothing auto-updates it — no apt, no snap), and (3) this record's hashes.

## 4. Artifact authentication (before any install)

- `node-v24.20.0-linux-x64.tar.xz` (31,838,904 bytes) sha256 `2f2c0da162318f0de47665410c7c8c2ed3d36c8f3105de4bbc61176c70a7cbf2` — **MATCH** against nodejs.org's published `SHASUMS256.txt`.
- `SHASUMS256.txt.asc` is a clearsigned sums file: **GPG Good signature** (made 2026-08-26T14:25:36Z, EDDSA key `5BE8A3F6C8A5C01D106C0AD820B1A390B168D356`, "Antoine du Hamel", Node.js release team) verified against the official `nodejs/release-keys` `gpg/pubring.kbx` keyring (fetched from the org's GitHub). The signed payload and the `.txt` agree on every hash (only a trailing-blank-line whitespace delta; the tarball's hash line is identical in both — reconciled, not assumed).
- Transport to hxs-8 re-hashed: identical sha256 on the host (`2f2c0da1…`).

## 5. Install, smoke, post-state

Install (single sudo block, 16:04Z): extract to `/opt/node-v24.20.0` (`--strip-components=1`), `chown -R root:root`, symlinks `/usr/local/bin/{node,npm,npx}` → `/opt/node-v24.20.0/bin/…`. No package manager touched; no repo added; no service created.

Smoke (16:05:21Z, all no-write):

```text
node --version  -> v24.20.0
npm  --version  -> 11.19.0
npx  --version  -> 11.19.0
node -e (no-write eval) -> runtime: v24.20.0 linux x64 | execPath: /opt/node-v24.20.0/bin/node
engines check (evaluated by the installed runtime itself):
  v24.20.0 in range >=22.22.2 <23 || >=24.0.0 <27: true
```

Post-state: `/opt/node-v24.20.0` 208M root:root; three symlinks verified; `command -v node/npm/npx` resolve to `/usr/local/bin/…`; 0 failed units.

## 6. NTP pin (WO-authorized, `scripts/fleet/fleet-ntp-pin.sh --apply`)

Applied 2026-08-27T16:05:59Z via the hardened library script (mktemp staging, `STAGED_PATH=/tmp/.fleet-ntp-pin.COzfga4Y`, diff reviewed, `install -m 0644 root:root`, restart `systemd-timesyncd` only):

```diff
 [Time]
-#NTP=
-#FallbackNTP=ntp.ubuntu.com
+NTP=time.cloudflare.com
+FallbackNTP=
```

Post-pin evidence: server contacted ~0 s — `162.159.200.123 (time.cloudflare.com)`; `NTP=yes`, `NTPSynchronized=yes`, `Timezone=Etc/UTC`; timesyncd `active`; conf sha256 **e2b94d4b1fbdd15a0c026a97ee37d9937f8457d0a28cba1c3a0eee8c0a349dc2** — byte-identical to the four LLM hosts' pinned file: the file-level one-source proof now extends to hxs-8. The F-2 fleet divergence (hxs-8 on `ntp.ubuntu.com`) is CLOSED. No daemon-reload needed (config file only); no other service touched.

## 7. Pre/post hashes and documented inverses

| Item | Before | After | Exact inverse |
| --- | --- | --- | --- |
| Node presence | `node/nodejs/npm/npx` ABSENT; no node-ish dpkg packages | `/opt/node-v24.20.0` (208M) + 3 symlinks in `/usr/local/bin`; node v24.20.0 / npm+npx 11.19.0 | `sudo rm /usr/local/bin/node /usr/local/bin/npm /usr/local/bin/npx && sudo rm -rf /opt/node-v24.20.0 && rm -f /tmp/node-v24.20.0-linux-x64.tar.xz` (restores the exact absent pre-state) |
| Artifact | — | tarball sha256 `2f2c0da1…cbf2` on hxs-5 + hxs-8 (`/tmp`) | removed at cleanup (see §9) |
| timesyncd.conf | sha256 `e6734751…c62` (stock, all-commented `[Time]`) | sha256 `e2b94d4b…dc2` (fleet pin) | restore the stock two lines (`#NTP=`, `#FallbackNTP=ntp.ubuntu.com` — the diff in §6 is the exact two-line inverse) + `systemctl restart systemd-timesyncd` |

Rollback readiness: both inverses are one-command operations; no rollback was needed; nothing was rolled back.

## 8. Boundaries compliance

Native only (tarball under `/opt` + symlinks); NO snap, NO Docker/containers, NO apt/pip/npm installs, NO OmniRoute install or start (Trinity's separate work order), NO firewall changes, NO service changes beyond the `systemd-timesyncd` restart. Listeners unchanged post-task (22 + stub DNS only). 0 failed units throughout. Second Brain evaluation per the WO: the versioned, repeatable runtime recipe (§3-§5) is the catalog-able pattern for future service runtimes.

## 9. Sanitized sequential command log

All local commands as hxsa@hxs-5; remote as hxsa@hxs-8 over independent SSH sessions; password via execution-time askpass only; sudo via the same stdin path (hxs-8 also has passwordless sudo from preparation — the stdin path was used uniformly). Credential value appears nowhere.

| Seq | Timestamp (UTC) | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | ---: |
| 1 | 15:5x~ | hxs-5 | Read WO/CP/goal file; grep engines in `package.json` (read-only); check knowledge dir + quirks register + gpg/curl/xz presence | 0 |
| 2 | 15:5x~ | hxs-5 | Create askpass/ssh helpers (mode 700); extraction smoke test `\| wc -c` → 10 | 0 |
| 3 | 16:00:59 | hxs-8 | Pre-state probe (identity, os/uptime, runtime absence, dpkg, snap presence, xz/gzip, timesyncd.conf sha, NTP state, failed units, listeners, mem/disk) | 0 |
| 4 | 16:02~ | hxs-5 | `curl` dist/index.json (sha `46f40ad3…`); python selection: newest in-range = v24.20.0 (Krypton LTS); alt v22.23.2 recorded | 0 |
| 5 | 16:03~ | hxs-5 | `curl` tarball + SHASUMS256.txt + .asc; sha256 vs sums → **MATCH** (`2f2c0da1…`) | 0 |
| 6 | 16:03~ | hxs-5 | release-keys pubring fetch (first path 404 — corrected to `gpg/pubring.kbx`); GPG verify → **Good signature** (Antoine du Hamel, EDDSA …D356); payload-vs-txt diff reconciled (trailing blank line only) | 0 |
| 7 | 16:04~ | hxs-5→hxs-8 | Push tarball via ssh stdin; hxs-8-side sha256 → MATCH | 0 |
| 8 | 16:04~ | hxs-8 | **MUTATION** single sudo block: mkdir `/opt/node-v24.20.0`, `tar -xJf --strip-components=1`, chown root:root, 3 symlinks | 0 |
| 9 | 16:05:21 | hxs-8 | Smoke: node/npm/npx versions; no-write `node -e` eval; engines-range eval → true; layout/presence/failed-units | 0 |
| 10 | 16:05:59 | hxs-8 | **MUTATION** `fleet-ntp-pin.sh hxs-8 --apply` (askpass stdin) → staged `COzfga4Y`, diff, install, restart, verify PASS | 0 |
| 11 | 16:06:20 | hxs-8 | Final sweep: conf sha `e2b94d4b…` (fleet-identical), server cloudflare, node present, 0 failed, listeners unchanged | 0 |
| 12 | 16:07~ | hxs-5/hxs-8 | Cleanup: helpers deleted; hxs-8 `/tmp/node-*.tar.xz` removed; task-created empty `~/.gnupg` (verify side-effect) removed from hxs-5 | 0 |

## 10. Validation summary

- **What changed on hxs-8:** `/opt/node-v24.20.0` + 3 `/usr/local/bin` symlinks (new runtime, pinned); `/etc/systemd/timesyncd.conf` → fleet pin + `systemd-timesyncd` restart. Nothing else.
- **What did not change:** packages/dpkg state, apt sources, snap, firewall, listeners, services other than timesyncd, OmniRoute (not installed), backends.
- **Tests:** identity MATCH; pre-state consistent with readiness baseline (stop condition not triggered); artifact authentication PASS (sha256 + GPG chain, discrepancy reconciled); smoke PASS (versions, no-write eval, engines `true` evaluated by the runtime itself); NTP pin PASS (server + synchronized + fleet-identical file hash); 0 failed units throughout.
- **Remaining items for the lane:** Trinity's install work order proceeds against this runtime; runtime upgrades are deliberate re-runs of this recipe (manual by design); hxs-8 DIMM/DMI observations from the readiness report stand unchanged.

`PASS — TASK COMPLETE`
