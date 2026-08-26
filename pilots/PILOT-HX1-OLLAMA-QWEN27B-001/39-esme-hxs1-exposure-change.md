# 39 — Esme: hxs-1 fleet-scoped endpoint exposure change (SC-07a)

| Field | Value |
| --- | --- |
| Report ID | 39-esme-hxs1-exposure-change |
| Work order | WO-HX1-JOHN-EXP-001 (`37-work-order-john-exposure.yaml`) |
| Context packet | `38-context-packet-john-exposure.yaml` (session john-exp-20260826-01) |
| Agent | john / Esme (Ollama specialist, profile-briefed sub-agent) |
| Target host | `hxs-1` (192.168.50.200), Ubuntu 24.04.4 LTS, kernel 7.0.0-30-generic |
| Session host | `hxs-5` (192.168.50.204) — all remote actions via SSH `hxsa@192.168.50.200` |
| Authority | Owner directive 2026-08-26 (goal file SC-07a amendment; hxs-2 goal D2); this exposure change is approved; NOT authorized: reboot, model-store/identity change, any other service change, package installs, kernel/driver changes |
| Window (UTC) | 2026-08-26 03:22:49 → 03:39 (change window 03:33:57 → 03:38) |
| Installed/server version | Ollama **0.32.15** (`/usr/local/bin/ollama` == `/api/version` == M6B/35-esme record) |
| Outcome | **PASS — TASK COMPLETE** (see §11; one containment disclosure F-EXP-1, one evidence-gap disclosure F-EXP-2) |

Host identity verified before any action (FACT, 03:30:29Z): `hostname`=`hxs-1`, `hostname -I`=`192.168.50.200`, SSH peer=`192.168.50.204` (hxs-5), `sudo -n` OK, `ollama`+`ollama-preload` enabled/active.

## 1. Knowledge review

```text
[KNOWLEDGE REVIEW COMPLETE]
Host: hxs-5 (session); target hxs-1 (192.168.50.200)
Source: /opt/tkv-local/ollama
Reviewed At: 2026-08-26T03:24Z
Relevant Files: ollama-main/envconfig/config.go (Host() parsing, bare "0.0.0.0" -> port
  default 11434, ConnectableHost loopback mapping); ollama-main/docs/faq.mdx ("expose on
  my network" + systemd Environment procedure = the authorized change path);
  research/ (hxs-1 corpus, cross-check only); pilot 29-esme-m6b-profiles.md (frozen
  identity + preload contract); 35-esme-preload-budget.md (TimeoutStartSec=600, script
  worst case 538 s); goal file SC-07/SC-07a; 09-state-log rows 52/57/61 (askpass
  read-at-execution pattern ratified; credential-record location)
Authority/Version Identified: owner directive 2026-08-26 (SC-07a); Ollama 0.32.15
  (binary == server, reconciled live); frozen identity hx-qwen3.8-27b-64k:latest digest
  766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a
Applicable Tests/Runbooks: faq.mdx systemd procedure; 29-esme §7 identity assertions;
  35-esme budget contract
Contradictions or Gaps: none for the change. Frozen-file continuity verified live:
  hx1.conf pre-hash == 29-esme frozen 163003b1...; ollama-preload.service == 35-esme post
  8ce6d9c1...; hx-ollama-preload == 35-esme post 95f174da... . Disclosures §10.
Task May Proceed: YES
```

## 2. Test definition (recorded 03:33Z, before first mutation)

| ID | Property | Expected | Pass rule | Result |
| --- | --- | --- | --- | --- |
| T1 | Loopback API survives bind change | `127.0.0.1:11434/api/version` = `{"version":"0.32.15"}` | exact JSON, exit 0 | **PASS** (03:34:21Z, attempt 4 of a bounded 10-probe loop — GPU re-discovery delayed first responses ~21 s; no failure) |
| T2 | Listener fleet-scoped | `0.0.0.0:11434` listening | `ss -lnt` line present | **PASS** — `LISTEN *:11434` (03:34Z) |
| T3 | Frozen-identity guard | `/api/ps` identical: name, digest, size=size_vram=20463789012, ctx 65536 | exact field equality after preload re-run AND at end | **PASS** (§5; both checkpoints) |
| T4 | ufw ruleset exact + order before enable | [1] 22/tcp ← 192.168.50.0/24, [2] 11434/tcp ← 192.168.50.0/24, default deny incoming | exact, SSH first | **PASS** (`ufw show added` + `user.rules` content, §6.1) |
| T5 | SSH survives ufw enable | fresh ssh prints `hxs-1` | exit 0 + output | **PASS** (03:37:47Z) |
| T6 | LAN reachability from hxs-5 | `192.168.50.200:11434/api/version` = `{"version":"0.32.15"}` | exact JSON | **PASS** (03:37Z) |
| T7 | Preload unit re-run | rc=0, `Result=success`, journal `OK - hx-qwen3.8-27b-64k resident`, < 600 s | all true | **PASS** (auto-run 48 s cold + explicit re-run 0.03 s, §7) |
| T8 | Journal hygiene | no error-level lines; zero Xid | empty error set | **PASS** (§8; NVRM chatter analyzed — platform-normal, precedent-proven) |
| T9 | File integrity / diff exactness | diff = OLLAMA_HOST line only; preload unit+script hashes unchanged | exact | **PASS** (§9) |
| T10 | NRestarts accounting | record pre/post | recorded | **PASS** — 0 pre, 0 post |

Expected transitional state (declared in plan): after `systemctl restart ollama.service` the runner unloads and `/api/ps` is EMPTY until the preload unit reloads the model. Observed exactly so (03:34:0xZ empty; resident again 03:34:46Z).

## 3. Pre-state (FACT, 03:30–03:31Z)

### 3.1 Service configuration

- `ollama version is 0.32.15`; binary `/usr/local/bin/ollama`; `ExecStart=/usr/local/bin/ollama serve`; `User=ollama`; `FragmentPath=/etc/systemd/system/ollama.service`; `DropInPaths=/etc/systemd/system/ollama.service.d/hx1.conf`; `NRestarts=0`.
- Effective environment (pre): `... OLLAMA_HOST=127.0.0.1:11434 OLLAMA_KEEP_ALIVE=-1 OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_NUM_PARALLEL=1 OLLAMA_CONTEXT_LENGTH=65536 OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=f16 OLLAMA_NO_CLOUD=1 CUDA_VISIBLE_DEVICES=GPU-2ace9bfc-…,GPU-d675a1cd-…`.
- Listeners (pre, `ss -lntp`): `127.0.0.1:11434` (ollama), `0.0.0.0:22` + `[::]:22` (sshd), loopback-only rest (`systemd-resolve` 53, `llama-server` 45431). No other LAN-exposed service — ufw default-deny incoming affects nothing else.
- ufw (pre): `Status: inactive` (`status verbose` and `status numbered`), expected per context packet.
- GPUs: 2 × RTX 4070 Ti SUPER 16376 MiB; runner pid 1736 using 11494 + 11880 MiB.
- Preload unit: `ActiveState=active (exited)`, `Result=success`, `ExecMainStatus=0`, `TimeoutStartUSec=10min`.

### 3.2 Touched/frozen files — pre-change sha256

| File | sha256 (pre) | Provenance check |
| --- | --- | --- |
| `/etc/systemd/system/ollama.service.d/hx1.conf` (touched) | `163003b16dbd2a88879e7febd9c3d3a3629b74977e85ff263ccab098a58d96c2` | == 29-esme M6B frozen — no drift |
| `/etc/systemd/system/ollama-preload.service` (frozen witness) | `8ce6d9c113f42439a79a90a8f8bd55f7c90959079034610d42187184e4fa4305` | == 35-esme post-change — no drift |
| `/usr/local/libexec/hx-ollama-preload` (frozen witness) | `95f174da30d38e9854e4c0e10c2a23fff8e224aecd8f633405fb89387d427cb7` | == 35-esme post-change — no drift |

### 3.3 Pre-change drop-in (byte-copy retained here; root:root 0644, 499 B)

```ini
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_KEEP_ALIVE=-1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_CONTEXT_LENGTH=65536"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=f16"
Environment="OLLAMA_NO_CLOUD=1"
Environment="CUDA_VISIBLE_DEVICES=GPU-2ace9bfc-3a2d-f5b9-d270-82d043f8a7b7,GPU-d675a1cd-7d3d-0903-3b1b-7d95f321a0a9"
Restart=always
RestartSec=3
TimeoutStartSec=300
LimitNOFILE=65535
```

### 3.4 Frozen identity (pre) — `/api/ps` 03:31Z

```json
{"models":[{"name":"hx-qwen3.8-27b-64k:latest","model":"hx-qwen3.8-27b-64k:latest","size":20463789012,"digest":"766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a","details":{"parent_model":"","format":"gguf","family":"qwen35","families":["qwen35"],"parameter_size":"27.3B","quantization_level":"Q4_K_M"},"expires_at":"2318-12-05T21:47:02.903047553Z","size_vram":20463789012,"context_length":65536}]}
```

`ollama ps` (pre): `hx-qwen3.8-27b-64k:latest  766cd9469fb4  20 GB  100% GPU  65536  Forever`.

## 4. Mutation 1 — bind change (03:33:57Z)

### 4.1 Unified diff (the only change to any Ollama file)

```diff
--- hx1.conf.PRE	2026-08-26 03:33:04 +0000
+++ hx1.conf.POST	2026-08-26 03:33:30 +0000
@@ -1,5 +1,5 @@
 [Service]
-Environment="OLLAMA_HOST=127.0.0.1:11434"
+Environment="OLLAMA_HOST=0.0.0.0"
 Environment="OLLAMA_KEEP_ALIVE=-1"
 Environment="OLLAMA_MAX_LOADED_MODELS=1"
 Environment="OLLAMA_NUM_PARALLEL=1"
```

`OLLAMA_HOST=0.0.0.0` (bare IP, per the work order verbatim): version-matched source (`envconfig/config.go` `Host()`) assigns the default port 11434 to a bare IP — effective bind `0.0.0.0:11434`, which includes loopback. Server confirms at startup: `server config … OLLAMA_HOST:http://0.0.0.0:11434`, `Listening on [::]:11434 (version 0.32.15)` (journal, 03:33:58Z).

### 4.2 Actions

1. Local byte-copy `hx1.conf.PRE` pulled via `sudo -n cat` over ssh — local sha256 == remote frozen `163003b1…` (integrity of the rollback copy proven).
2. `hx1.conf.POST` authored locally from the byte-copy (sed of exactly the one line); local diff verified one-line; local sha256 `f732f9db…`.
3. Transferred via `cat`-over-ssh to `/tmp/hx1.conf.esme-exp`; `sudo -n install -m 0644 -o root -g root` onto `hx1.conf`; temp removed.
4. Installed hash verified: `f732f9dbbbc159c4b471e34856e0b1642243badca6160e04dae6e0e1e9116144` (491 B, root:root 0644).
5. `sudo -n systemctl daemon-reload` (03:33:57Z); `sudo -n systemctl restart ollama.service` (03:33:58Z, rc=0) — **only** `ollama.service` restarted by me. No reboot. No other service touched.
6. Effective environment now: `OLLAMA_HOST=0.0.0.0` (systemctl show, FACT); service `active/running`; `NRestarts=0`.

## 5. Frozen-identity guard — before/after proof (T3)

Guard fields compared programmatically (pre 03:31Z vs post 03:35Z, re-verified 03:38Z):

| Field | Pre | Post (after reload) | Verdict |
| --- | --- | --- | --- |
| `name` | `hx-qwen3.8-27b-64k:latest` | `hx-qwen3.8-27b-64k:latest` | MATCH |
| `digest` | `766cd9469fb47c42890616880772f2647fcfe4656b7550e5cc37ab186cc99d8a` | identical | MATCH |
| `size` | 20463789012 | 20463789012 | MATCH |
| `size_vram` | 20463789012 (100% VRAM) | 20463789012 (100% VRAM) | MATCH |
| `context_length` | 65536 | 65536 | MATCH |
| `details` (family/params/quant) | qwen35 / 27.3B / Q4_K_M | identical | MATCH |
| `ollama ps` | 100% GPU, 65536, Forever | 100% GPU, 65536, Forever | MATCH |

`expires_at` moved `2318-12-05T21:47:02Z` → `2318-12-06T03:22:18Z`: keep_alive=-1 sentinel recomputed at runner start (03:34:46Z); recorded, not a guard field. New runner pid 6454, VRAM footprint 11494 + 11880 MiB == pre. **IDENTITY GUARD: PASS — no drift; no restore triggered.**

## 6. Mutation 2 — ufw boundary (03:36–03:37Z)

### 6.1 Staged rules and order verification BEFORE enable (T4 gate)

Commands (in this order): `ufw allow from 192.168.50.0/24 to any port 22 proto tcp` → "Rules updated"; `ufw allow from 192.168.50.0/24 to any port 11434 proto tcp` → "Rules updated"; `ufw default deny incoming` → "Default incoming policy changed to 'deny'".

`ufw status` does not display staged rules while inactive, so order was verified two ways before enabling (FACT 03:36Z):

```text
$ ufw show added
Added user rules (see 'ufw status' for running firewall):
ufw allow from 192.168.50.0/24 to any port 22 proto tcp
ufw allow from 192.168.50.0/24 to any port 11434 proto tcp
```

`/etc/ufw/user.rules` RULES section (full content captured in evidence): exactly two tuples — `allow tcp 22 … -s 192.168.50.0/24 -j ACCEPT` **first**, then `allow tcp 11434 … -s 192.168.50.0/24 -j ACCEPT`; no pre-existing user rules (pre-state = inactive + empty ruleset, consistent with the context packet expectation). `/etc/default/ufw`: `DEFAULT_INPUT_POLICY="DROP"`, `DEFAULT_OUTPUT_POLICY="ACCEPT"`, `DEFAULT_FORWARD_POLICY="DROP"`.

### 6.2 Ruleset as applied (after `ufw --force enable`, 03:37Z)

```text
Firewall is active and enabled on system startup

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    192.168.50.0/24
[ 2] 11434/tcp                  ALLOW IN    192.168.50.0/24

Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
```

Post-enable file hashes: `user.rules dad0b09d9b62666c7c06d1ac9216df10e7feb93ccf054d50510dcc5eb5c49d6e` (staged→enable unchanged), `user6.rules 028886bbab99bb6a7d8a4c16853dada474d248f5d9c769d869263582351ea12d` (regenerated by enable; no v6 user rules), `/etc/default/ufw 07db07bb07e5ac1388707b7c59dabfbce8ad06d5001236248fbf3f93b79c2ed7` (stock policies, not rewritten), `/etc/ufw/ufw.conf 254cb3ad232ca318498ed64ffaee96e2659e0e67228602b644b6357cd26c7e58` (`ENABLED=yes`).

## 7. Preload unit re-run (T7)

Two runs, both in evidence:

1. **Auto-run via `Requires=ollama.service` propagation** during the mandated restart (same mechanism as M6B): started 03:33:58Z, bounded retry absorbed the listener/GPU-discovery race (one `curl: (7)`, five `curl: (28)` — info-level, F-M6-1 class), then `hx-ollama-preload: OK - hx-qwen3.8-27b-64k resident` at **03:34:46Z** (48 s cold, within the 538 s script worst case and 600 s unit budget).
2. **Explicit authorized re-run** `sudo -n systemctl restart ollama-preload.service` (03:35:01Z): rc=0, 0.03 s (model already resident), `Result=success`, `ExecMainStatus=0`, `active (exited)`, journal `OK - hx-qwen3.8-27b-64k resident`.

## 8. Journal, GPU, NRestarts (T8, T10)

- `journalctl -p err --since 2026-08-26T03:30` (system-wide): `-- No entries --`.
- Xid: **0** lines today (`journalctl -k | grep -c Xid`). Stop condition not triggered.
- NVRM: 63 lines, ALL confined to the runner restart window 03:33:58–03:34:36Z, signatures `iovaspaceDestruct_IMPL: left-over mappings` / `nvAssertFailedNoLog: pIOVAS != NULL @ io_vaspace.c:592/601`. Precedent-proven platform chatter: the identical signature set appears at this boot's driver-load/runner-start (2026-08-25 16:23:26Z, 44 lines) on the signed-off configuration (driver 580.173.02 open kernel module). No Xid, no error-level entries, model reloaded to identical 100%-VRAM residency. Assessment: benign on this platform; recorded, not a regression of this change.
- Ollama journal excerpt (change window, request-log lines elided): clean stop 03:33:57Z → start 03:33:58Z (`OLLAMA_HOST:http://0.0.0.0:11434`, `Listening on [::]:11434`) → GPU discovery (both 4070 Ti SUPER, driver 13.0) → llama-server start 03:34:39Z → `model loaded` 03:34:45Z → preload generate 200 in 9.71 s → resident.
- `NRestarts=0` pre and post (manual restart does not increment; no auto-restart occurred).
- Boot path: `ollama` + `ollama-preload` still `enabled`; ufw now `enabled on system startup` (authorized "ufw ruleset + enable") — at boot ufw's staged ruleset permits 22+11434 from the /24, so SSH and the fleet endpoint survive a future reboot; nothing else in the boot path was modified.

## 9. File hash summary (pre → post)

| File | Pre | Post | Change |
| --- | --- | --- | --- |
| `/etc/systemd/system/ollama.service.d/hx1.conf` | `163003b1…58d96c2` | `f732f9db…e9116144` | one line (§4.1 diff) |
| `/etc/systemd/system/ollama-preload.service` | `8ce6d9c1…4fa4305` | `8ce6d9c1…4fa4305` | unchanged (frozen witness) |
| `/usr/local/libexec/hx-ollama-preload` | `95f174da…d427cb7` | `95f174da…d427cb7` | unchanged (frozen witness) |
| `/etc/ufw/user.rules` | (see F-EXP-2) | `dad0b09d…c49d6e` | +2 rules (§6.1 content) |
| `/etc/ufw/user6.rules` | (see F-EXP-2) | `028886bb…ea12d` | regenerated, no v6 rules |
| `/etc/ufw/ufw.conf` | (see F-EXP-2) | `254cb3ad…c7e58` | `ENABLED=yes` |
| `/etc/default/ufw` | (see F-EXP-2) | `07db07bb…c2ed7` | unchanged content (stock DROP/ACCEPT/DROP) |

Model store untouched (no pull/create/delete; `total blobs: 9`, `total unused blobs removed: 0` at startup). No package installs, no kernel/driver change, no reboot.

## 10. Disclosures (open per profile §15)

- **F-EXP-1 (secret-handling incident — contained, disclosed):** at ~03:24Z a structure-probe awk mask on the credential record was too narrow and one credential-table row (username/password) was echoed once into this session's transcript. Containment within ~1 minute: the retained task output log was sanitized to `REDACTED` and swept; no command line, remote file, evidence file, or this document carries the value (swept). Residual, owner decision required: the value persists in the harness's own session transcripts (wire.jsonl of this and earlier sessions — pre-existing exposure predating this task, 3 occurrences found in one older session file), which I did not edit (live runtime state, outside my evidence scope). The guide's "Required owner security action" (rotate + replace plaintext record) remains on record; owner's standing no-rotation call governs. Root cause: my probe design; corrective applied — the askpass helper (ratified read-at-execution pattern) was used for ALL authentication thereafter; no further exposure.
- **F-EXP-2 (evidence gap — mitigated, disclosed):** pre-mutation sha256 of the `/etc/ufw/*` files was not captured before staging the rules (the work-order pre-state requirement for ufw was "ufw status numbered", which WAS captured: `Status: inactive`). Mitigation: post-stage content of `user.rules` proves the pre-state ruleset was empty (exactly the two added tuples between `### RULES ###` markers; `user6.rules` untouched until enable; `/etc/default/ufw` stock policies unchanged). Recorded honestly; does not affect rollback (rollback = `ufw disable`, returning to the captured inactive state).
- **NVRM note:** §8 — not an error, precedent-proven; surfaced so future Xid/NVRM scans baseline correctly.

## 11. Reachability matrix (post-change, all FACT)

| Path | Probe | Result | Verdict |
| --- | --- | --- | --- |
| Loopback (hxs-1 → 127.0.0.1:11434) | `curl /api/version` | `{"version":"0.32.15"}` (03:34:21Z, re-verified 03:37Z) | **PASS** |
| LAN (hxs-5 → 192.168.50.200:11434) | `curl /api/version` from 192.168.50.204 | `{"version":"0.32.15"}` (03:37Z) | **PASS** |
| SSH (hxs-5 → hxs-1:22, fresh session post-enable) | `ssh … 'hostname'` | `hxs-1` (03:37:47Z); every subsequent command in this log is additional proof | **PASS** |
| Preload unit re-run | §7 | rc=0, `Result=success`, `OK - hx-qwen3.8-27b-64k resident` | **PASS** |
| Identity/residency | §5 | identical guard fields, 100% VRAM, Forever | **PASS** |
| Boundary negative case (non-/24 source) | not executed — no authorized host outside the /24 to probe from; boundary is ruleset-evidenced (§6.2: two /24-scoped allows + default deny incoming) | — | **NOT RUN (limitation)** |

## 12. Rollback inverse (byte-exact)

Pre-change byte-copy of `hx1.conf` is embedded in §3.3 (sha256 `163003b16dbd2a88879e7febd9c3d3a3629b74977e85ff263ccab098a58d96c2`). Inverse procedure (est. < 90 s, no reboot):

```bash
# on hxs-1, via the same ssh + sudo -n path
sudo install -m 0644 -o root -g root <hx1.conf.PRE> /etc/systemd/system/ollama.service.d/hx1.conf
sudo systemctl daemon-reload
sudo systemctl restart ollama.service
sudo systemctl restart ollama-preload.service   # restore residency (bounded, 538 s worst)
# verify: /api/ps == §3.4 identity block; ss shows 127.0.0.1:11434 only
sudo ufw disable                                 # pre-state was inactive
# verify: ufw status -> inactive; fresh ssh OK; curl 127.0.0.1:11434/api/version -> 0.32.15
```

Rollback restores: loopback-only bind, frozen identity (unchanged by design), ufw inactive. Nothing in this change is irreversible.

## 13. Command log (sequential; all times UTC; secrets absent by construction)

| # | Time | Where | Command (sanitized) | Exit | Evidence |
| ---: | --- | --- | --- | --- | --- |
| 1 | 03:22:49 | hxs-5 | `hostname; date; ssh -V` → hxs-5, OpenSSH 9.6p1 | 0 | §1 |
| 2 | 03:22–24 | hxs-5 | TKV survey `/opt/tkv-local/ollama` (dirs; `envconfig/config.go` Host(); `docs/faq.mdx` exposure+systemd procedure) | 0 | §1 |
| 3 | 03:23–24 | hxs-5 | Read WO-37/CP-38, 29-esme, 35-esme, goal SC-07a, state-log rows 52/57/61 | 0 | §1 |
| 4 | 03:24 | hxs-5 | credential-record structure probe — F-EXP-1 echo; sanitize retained log + sweep | 0 | §10 |
| 5 | 03:29–30 | hxs-5 | `mkdir -m 700 /tmp/esme-exp-20260826`; askpass helper written (0700, `sh -n` OK) — reads credential-record row at execution | 0 | §10 |
| 6 | 03:30:29 | ssh hxs-1 | identity: `hostname`=hxs-1, `hostname -I`=.200, peer=.204, `sudo -n true` OK, units enabled/active | 0 | header |
| 7 | 03:31 | ssh hxs-1 | pre-state A: `ollama --version` 0.32.15; `systemctl cat/show ollama`; sha256 of 3 files | 0 | §3.1/3.2 |
| 8 | 03:31 | ssh hxs-1 | pre-state B: `ss -lntp`; `ufw status verbose/numbered` (inactive); `/api/version` `/api/ps` `/api/tags`; `ollama ps` | 0 | §3.1/3.4 |
| 9 | 03:31 | ssh hxs-1 | pre-state C: `nvidia-smi`; preload unit state; journal tail; Xid/NVRM scan (empty) | 0 | §3.1 |
| 10 | 03:33:04 | ssh hxs-1→hxs-5 | byte-copy `hx1.conf.PRE` (sha256 == frozen) + `api-ps.PRE.json` | 0 | §4.2 |
| 11 | 03:33:30 | hxs-5 | author `hx1.conf.POST`; one-line diff; local hashes | 0 | §4.1 |
| 12 | 03:33:57–58 | ssh hxs-1 | install POST (`sudo -n install`); hash verified `f732f9db…`; `daemon-reload`; `restart ollama.service` rc=0; effective env shows `OLLAMA_HOST=0.0.0.0`; `NRestarts=0` | 0 | §4.2 |
| 13 | 03:34:0x–21 | ssh hxs-1 | T2 `ss -lnt` `*:11434`; T1 loopback probe loop (3 × curl (28) during GPU re-discovery, then 200 0.32.15); transitional `/api/ps` empty; runner gone | 0 | §2/§4 |
| 14 | 03:33:58–03:34:46 | hxs-1 (unit) | preload auto-run via `Requires=`; bounded retries absorbed; `OK - hx-qwen3.8-27b-64k resident` (48 s cold) | 0 | §7 |
| 15 | 03:35:01 | ssh hxs-1 | `sudo -n systemctl restart ollama-preload.service` rc=0, 0.03 s, `Result=success` | 0 | §7 |
| 16 | 03:35 | ssh hxs-1 + hxs-5 | T3 guard compare pre vs post `/api/ps` → all fields MATCH; `ollama ps`; VRAM 11494+11880 | 0 | §5 |
| 17 | 03:36 | ssh hxs-1 | ufw: allow 22/tcp ← /24; allow 11434/tcp ← /24; default deny incoming (each "Rules updated"/"policy changed") | 0 | §6.1 |
| 18 | 03:36 | ssh hxs-1 | T4 gate: `ufw show added` (22 first, 11434 second); `user.rules` content; sha256 post-stage | 0 | §6.1 |
| 19 | 03:37 | ssh hxs-1 | `ufw --force enable` → active; `status numbered` [1] 22 [2] 11434; post-enable hashes; loopback 200 | 0 | §6.2 |
| 20 | 03:37 | hxs-5 | T6: `curl http://192.168.50.200:11434/api/version` → `{"version":"0.32.15"}` | 0 | §11 |
| 21 | 03:37:47 | hxs-5→hxs-1 | T5: fresh ssh `hostname` → `hxs-1` | 0 | §11 |
| 22 | 03:38 | ssh hxs-1 | final: `/api/ps` identical; `journalctl -p err` none; Xid=0; NVRM=63 (window-bound); `NRestarts=0`; enablement unchanged; post hashes | 0 | §8/§9 |
| 23 | 03:38–39 | ssh hxs-1 | NVRM precedent (boot-window identical signatures) + signature census | 0 | §8/§10 |
| 24 | 03:39+ | hxs-5 | write this deliverable; delete askpass helper + transient workspace; verify deletion; secret sweep of deliverable | 0 | §14 |

## 14. Cleanup and hygiene

- Askpass helper `/tmp/esme-exp-20260826/askpass.sh` and the transient workspace are deleted at task end (deletion verified); the helper never stored the credential — it read the credential-record table row at execution time only (ratified pattern, state-log row 52).
- This document contains no secret values (swept). LAN addresses shown are ratified fleet facts.
- Remote temp file `/tmp/hx1.conf.esme-exp` removed during install (step 12).

## 15. Validation summary

- **What changed:** `hx1.conf` one line (`OLLAMA_HOST=127.0.0.1:11434` → `0.0.0.0`, effective `0.0.0.0:11434`); ufw inactive → active with exactly [1] 22/tcp ← 192.168.50.0/24, [2] 11434/tcp ← 192.168.50.0/24, default deny incoming, enabled on startup.
- **What did not change:** frozen identity (digest `766cd9469fb4…8cc99d8a`, 20,463,789,012 B, 100% VRAM, ctx 65536, Forever); preload unit + script (hashes unchanged); model store (9 blobs, untouched); Ollama 0.32.15; driver 580.173.02; kernel; boot enablement of both units; no reboot; no other service.
- **Tested / passed:** T1–T10 (10/10), reachability matrix 5/5 executed rows PASS; negative-boundary probe NOT RUN (limitation, ruleset-evidenced instead).
- **Current endpoint/security state:** listener `*:11434`; loopback verified working; LAN reachable from hxs-5; SSH reachable; ufw active (deny incoming default, /24-scoped allows); no error-level journal; 0 Xid.
- **Rollback readiness:** byte-copy embedded (§3.3) + inverse procedure (§12); nothing irreversible.
- **Remaining risks/decisions:** F-EXP-1 residual (credential value in harness transcripts — owner rotation decision, standing no-rotation governs); negative-boundary probe requires an authorized out-of-subnet host; NVRM chatter baselined for future scans.
- **Second Brain evaluation:** opportunity identified — scoped-exposure change executed as a versioned, evidenced pattern (first post-closure posture change on a signed-off host). Disposition: **implemented** — full provenance trail (SC-07a amendment → WO-37/CP-38 → this evidence → catalog re-validation at handoff), per the work order's own evaluation.
- **Handoff:** to Carol for catalog receipt; handoff OPEN until the receipt is cited in `09-state-log.md`.

```text
Task: WO-HX1-JOHN-EXP-001 — hxs-1 fleet-scoped endpoint exposure (SC-07a)
Identity guard: PASS (no drift, no restore)
Reachability: loopback PASS / LAN PASS / SSH PASS / preload PASS / journal clean
Stop conditions hit: NONE (one bounded correction attempt unused)
Task May Proceed: YES
```

`PASS — TASK COMPLETE`
