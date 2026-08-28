# Trinity — L1-M3 Secure Core Gate Record: OmniRoute v3.8.51 on hxs-8 (parity deep, restart ×2, cold reboot, restore, rollback, hygiene)

| Field | Value |
| --- | --- |
| Work order | WO-L1-GATE-001 (`11-work-order-trinity-gate.yaml` + `12-context-packet-trinity-gate.yaml`) |
| Goal | GOAL-OMNIROUTE-L1-SECURE-CORE (`goals/2026-08-27-omniroute-layer1-secure-core.md`) |
| Agent | Trinity (OmniRoute lifecycle engineer), session trinity-l1-gate-20260828-01 (1 of 2 budgeted) |
| Target | hxs-8 (192.168.50.207) — ONLY; the four LLM backends read-only |
| Executor | hxs-5 (192.168.50.204) |
| Execution window | 2026-08-28T05:36Z – 06:42Z (all times UTC); cold-reboot window per owner GO ~05:30Z (state log rows 66–67) |
| Result | **PASS — TASK COMPLETE** (all six gate tests executed; G6 carries two recorded plaintext-residue exceptions for owner rotation; acceptance reconciliation §10) |

Truth-state labels: FACT = live-verified this session (command + result in §13 or cited) · SOURCE = verified in the pinned corpus at the cited line · AUTHORITY = owner/governance decision · INFERENCE = producer reasoning, labeled in place. No secret value appears anywhere in this record — secrets are referenced by name, mechanism, file mode, and sha256 only.

## 1. Startup receipt

```text
[TRINITY KNOWLEDGE REVIEW COMPLETE]
Agent: Trinity
Goal Contract: GOAL-OMNIROUTE-L1-SECURE-CORE v1 (WO-L1-GATE-001, milestone L1-M3)
Target Host/Environment: hxs-8 (192.168.50.207) — VERIFIED (hostname/peer/machine-id/host-key)
Source Corpus: /opt/tkv-local/OmniRoute-release-v3.8.51 (DOC-tkv-corpus-omniroute, read-only)
Reviewed At: 2026-08-28T05:36–06:00Z
Source Identity: VERIFIED 2026-08-27 by content-sensitive proof (state log row 6); bind mechanics re-verified in corpus this session
Installed Identity: omniroute v3.8.51 active+enabled Type=notify NRestarts=0; unit hashes match install record; secrets drop-in 0600 hash 05638010… (owner password reset 2026-08-27T18:20–18:26Z, governor-recorded row 50)
Relevant Knowledge: runtime-env.mjs:169-179 (OMNIROUTE_HOSTNAME is the bind knob); standalone-server-ws.mjs (single listener + READY); liveServer.ts:630-658 (LiveWS loopback default, background-gated off); managementPassword.ts (bcrypt, JSON-encoded settings); peer-stamp.mjs (real-peer locality); DOC-backend-qwen-x/coder-x/meta-x/chat-x
Allowed Change Surfaces: hxs-8 only — 30-bind drop-in, loopback-listener component + unit, gate evidence; four backends read-only; corpus read-only
Known Drift/Risks: owner OpenRouter "main" connection + 1 glm-5.3-flash call (owner-dispositioned row 48, USD 100 cap); /v1/models surface 1,496 incl. cloud catalogs (same disposition); hxsa bash_history holds management password ×21 (owner-lane; rotation decided); Qwen-X/Coder-X evicted at session start (tags digests match; parity loads them)
Rollback Ready: YES — bind inverse = remove 30-bind drop-in + loopback unit (rehearsed in G5)
Task May Proceed: YES
```

## 2. Authority, identity, pre-state

Owner authorizations exercised [AUTHORITY]: OD-12 (Layer 1), OD-04 (native, never Docker), OD-08 amended (all four backends; Chat-X parity waived as posture-blocked), OD-13 (secrets rule + amendment), OD-07 (LAN-only + OmniRoute authN/authZ + no host firewall), OD-09 (plaintext snapshots; encryption wrapper owner-decided NOT REQUIRED 2026-08-28, row 66). Cold reboot PRE-APPROVED (governor-announced window NOW; hxs-1 D6 precedent).

Identity verified live 05:48Z before any mutation [FACT]:

| Check | Expected | Observed | Result |
| --- | --- | --- | --- |
| Hostname | hxs-8 | hxs-8 | MATCH |
| Peer | SSH from hxs-5 (192.168.50.204) to 192.168.50.207 | `$SSH_CONNECTION` peer 192.168.50.204 → .207 | MATCH |
| Machine ID | 91086d5265a74450b7c2047b3b7ca2ae | 91086d5265a74450b7c2047b3b7ca2ae | MATCH |
| Host key | pinned in hxs-5 `~/.ssh/known_hosts` line 20 | `StrictHostKeyChecking=yes`, connection accepted | MATCH |

Access mechanics: askpass helper READ the credential at execution time from the credential-record row of `/home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md` (`awk -F'|'` on the `SSH password` row, markdown backticks stripped; smoke check `wc -c` = 10). Never printed/logged/stored; helper deleted at task end (§13 seq 30). sudo on hxs-8 and backend hosts: passwordless, used as `sudo -n`. Backend hosts (hxs-1..hxs-4) reached with the same pinned-key + askpass pattern for READ-ONLY re-proofs (G3); host keys confirmed pinned (`ssh-keygen -F`) before first contact.

Pre-state [FACT] (05:49–06:05Z):

- Service: `omniroute.service` active+enabled, `Type=notify`, `NotifyAccess=all`, `NRestarts=0`, `ActiveEnterTimestamp` 2026-08-27T18:26:01Z (see the owner-reset lineage below); `omniroute-backup.timer` active+enabled.
- Unit hashes: all six install-era hashes match `03-trinity-l1-install.md` §4 EXCEPT the secrets drop-in: live `05638010ce7a6645…`, 0600 root:root. Reconciled [FACT]: the owner ran `/tmp/omni-pw-reset.sh` interactively 2026-08-27T18:20:54Z–18:26:07Z (sudo journal), resetting the management (dashboard) password and restarting the service; the governor recorded the hardened 0600 mode and the `05638010…` content hash at row 50; the scripts have since been removed by the owner (`stat`: absent). Drop-in metadata (names + lengths only): `JWT_SECRET/API_KEY_SECRET/STORAGE_ENCRYPTION_KEY` 64 chars each, `INITIAL_PASSWORD` 9 chars.
- `/opt/omniroute/ops/.hx-client-key` 0600 root:root, sha256 `d8aa9c37…` — matches the install record.
- Listeners: `0.0.0.0:20128` (app), loopback DNS, sshd; interfaces `lo` + `eno1` only (no LiveWS listener — `OMNIROUTE_DISABLE_BACKGROUND_SERVICES=true` gates it, as designed at install).
- Env names only (12): `NODE_ENV, DATA_DIR, HOSTNAME, PORT, OMNIROUTE_MIGRATIONS_DIR, OMNIROUTE_MEMORY_MB, OMNIROUTE_DISABLE_BACKGROUND_SERVICES, NEXT_TELEMETRY_DISABLED` + the four secret names.
- DB: `integrity_check ok`; `secrets` namespace **0 rows**; posture rows all `false`/`true` as deployed; management password JSON-encoded 60-char **bcrypt** (`$2` prefix, pattern-verified; an earlier probe artifact — raw-value prefix check on the JSON-encoded form — was corrected and re-proven); migrations 160; `usage_history` 4 rows (3 install parity + 1 owner call, below); connections 5 (below); `cloud_agent_credentials` 0 rows; `api_keys` 2 rows.
- **Owner-added connection** [FACT + AUTHORITY]: `main` (id `dc25257c-715a-4955-83a0-5c3dc5218034`, provider `openrouter`, is_active=1, test_status=active, api_key `enc:v1:` ciphertext) and one routed cloud test call (`z-ai/glm-5.3-flash`, 25/222 tokens, attributed to the HX client key id `5a2aefa4…`). Disposition: owner-decided (state log row 48: OpenRouter spending limit USD 100; OR key accepted as-is; no gateway model allowlist directed). Distinct providers: `ollama-local`, `openrouter`; `:cloud`-tagged connections 0.
- `/v1/models` with the HX key: **1,496 entries** — the 22 `hx-` alias entries unchanged, **zero `hx-qwen3.5` entries** (Chat-X posture holds), plus the OpenRouter catalog (934), built-in presets and auto-combos. The ollama prefixes also carry the backends' raw upstream tags and embedding models (product model sync against the registered backends; the alias-only convention is enforced by consumers per the backend records, not by the gateway).
- Backend identity from hxs-8 (pre-gate): Qwen-X evicted, tags digest `766cd9469fb4` MATCH; Coder-X evicted, tags digest `ec9ebe08a824` MATCH; Meta-X resident, digest `9dffb015db40` MATCH (size == size_vram); Chat-X rc=7 connection refused — loopback-only posture CONFIRMED.
- Management login functional with the CURRENT drop-in `INITIAL_PASSWORD` (owner-reset value; extracted remote-side, never echoed): HTTP 200 — drop-in↔DB consistency proven.

## 3. PRE-GATE — primary-listener rebind (context-packet current_state note)

Design [FACT as deployed; mechanism SOURCE-cited]: the product binds exactly one HTTP listener (Next standalone `server.js` via `server-ws.mjs`); `scripts/build/runtime-env.mjs:177` maps `OMNIROUTE_HOSTNAME` → `HOSTNAME` (default `0.0.0.0`) — the supported bind knob. No native second-listener knob exists (corpus-wide sweep). The rebind is therefore: (a) a versioned drop-in setting `OMNIROUTE_HOSTNAME=192.168.50.207`, leaving the install-era drop-ins untouched (hashes preserved), and (b) a separate HX loopback listener — a raw-TCP proxy `127.0.0.1:20128` → `192.168.50.207:20128` under its own systemd unit — preserving loopback semantics for local clients (peer-stamp sees the real peer `127.0.0.1`; the proxy adds no forwarding headers, terminates no TLS, logs no payload; only local processes can connect).

New versioned artifacts (staged on hxs-5, pushed, hash-verified identical on hxs-8) [FACT]:

| File | Mode | sha256 |
| --- | --- | --- |
| `/etc/systemd/system/omniroute.service.d/30-v3.8.51-bind.conf` | 0644 root:root | `1ce348abed34d4b34be7795fb6c28a6b458134a62cc53bd92e3258e903f9a557` |
| `/opt/omniroute/ops/loopback-listener.mjs` | 0755 root:root | `38de600679271c231ea98b362dc36814ea92f75782593a85f358dea5cf004f4f` |
| `/etc/systemd/system/omniroute-loopback.service` | 0644 root:root | `c0e60b9c3618003a644ec216c6c34f2163f87ad501cefb95c76ba048a1fd8d99` |

Restart sequence (this gate's own, distinct from G2's two) 06:06:51Z–06:06:57Z [FACT]: `daemon-reload` → `systemctl restart omniroute.service` (589 ms wall; READY accepted under `Type=notify`) → primary listener `192.168.50.207:20128` only, `0.0.0.0:20128` gone → `systemctl enable --now omniroute-loopback.service` → `127.0.0.1:20128` up.

Post-bind verification battery [FACT]:

| Check | Loopback | LAN IP (from hxs-8) | LAN (from hxs-5) |
| --- | --- | --- | --- |
| `/healthz` | 200 | 200 | 200 |
| anon `/api/settings` | 401 | 401 | 401 |
| anon `/v1/models` | 401 | 401 | 401 |
| anon `/api/monitoring/health` | 2 keys | — | 2 keys |
| management `/api/monitoring/health` | 25 keys | — | — |
| management login (fresh cookie) | 200 | — | — |
| `/v1/models` with HX key | 200 | — | — |

Non-LAN interfaces unexposed [FACT]: the host has exactly `lo` + `eno1`; the only `:20128` listeners are `192.168.50.207` and `127.0.0.1`; no wildcard bind remains. Posture rows still effective via management settings read (`cloudEnabled:false, skillsEnabled:false, mcpEnabled:false, a2aEnabled:false, memoryEnabled:false, tailscaleEnabled:false, requireLogin:true`).

## 4. G1 — parity deep (gate item 3)

Three distinct known-answer tasks per reachable backend, identical parameters both ways (`temperature=0, max_tokens=2048, stream=false`; strictly sequential — Qwen-X serializes admission, `DOC-backend-qwen-x`): T1 short (`Compute 6*7…` → `42`), T2 structured output (capital-of-France as a JSON object → `{"answer": "Paris"}`), T3 longer generation (first 10 primes → `2, 3, 5, …, 29`). Direct = backend `:11434/v1/chat/completions` (model = operating 64k alias); routed = `127.0.0.1:20128/v1/chat/completions` with the HX client key (model `ollama-local/<alias>:latest`, via the new loopback listener) [FACT]:

| Backend | Task | Direct (content/finish/pt/ct/tt) | Routed (content/finish/pt/ct/tt) | Verdict |
| --- | --- | --- | --- | --- |
| Qwen-X | T1 | `42` · stop · 99/32/131 | `42` · stop · 99/32/131 | IDENTICAL |
| Qwen-X | T2 | `{"answer": "Paris"}` · stop · 111/55/166 | `{"answer": "Paris"}` · stop · 111/55/166 | IDENTICAL |
| Qwen-X | T3 | primes · stop · 110/120/230 | primes · stop · 110/120/230 | IDENTICAL |
| Coder-X | T1 | `42` · stop · 25/134/159 | `42` · stop · 25/134/159 | IDENTICAL |
| Coder-X | T2 | `{"answer": "Paris"}` · stop · 37/237/274 | `{"answer": "Paris"}` · stop · 37/237/274 | IDENTICAL |
| Coder-X | T3 | primes · stop · 36/905/941 | primes · stop · 36/905/941 | IDENTICAL |
| Meta-X | T1 | `42` · stop · 71/62/133 | `42` · stop · 71/63/134 | content/finish identical; usage Δ1 (see control) |
| Meta-X | T2 | `{"answer":"Paris"}` · stop · 83/178/261 | `{"answer": "Paris"}` · stop · 83/144/227 | JSON-insignificant whitespace + thinking-token variance (see control) |
| Meta-X | T3 | primes · stop · 81/341/422 | primes · stop · 81/341/422 | IDENTICAL |
| Chat-X | — | — | — | POSTURE-BLOCKED (loopback-only; waived per OD-08 amendment — not a failure) |

**Control experiment** (variance attribution, 4 calls, Meta-X T1+T2 direct×2/routed×2) [FACT]: T1 all four calls identical (71/63/134). T2: **direct-vs-direct disagreed** (`{"answer":"Paris"}` 83/178/261 vs `{"answer": "Paris"}` 83/144/227) while both routed calls matched each other and the second direct call. Verdict [FACT + INFERENCE]: the variance is MODEL-SIDE nondeterminism on Meta-X (muse-glimmer thinking chains diverge run-to-run even at temperature 0; the direct path disagrees with itself by the same magnitudes), NOT a routed-vs-direct systematic difference. Routed behavior is faithful: known answer correct and semantically identical on every task, finish `stop` everywhere, prompt-token accounting identical in every pair. Parity stop condition NOT triggered — no systematic path difference exists; evidence attached.

**Usage accounting** [FACT]: `usage_history` 4 → 13 across the battery — exactly the 9 routed calls, one per backend-model per task, with `tokens_input/tokens_output/latency_ms/ttft_ms` and api-key attribution (`api_key_id 5a2aefa4…`).

**Recorded behavior — gateway semantic cache** [FACT]: `semantic_cache` holds the 9 battery responses; byte-identical repeat requests are cache-served and write NO usage row (the 4 control routed calls are absent from `usage_history`; a nonce-busted call incremented both tables 13→14 / 9→10). Discipline applied thereafter: every routing proof in G2/G3/G5 carries a unique nonce, guaranteeing a genuine backend round-trip and a `usage_history` delta. Parity validity unaffected: all 9 battery routed calls were cache-misses (first occurrence).

## 5. G2 — restart ×2 (gate item 6, part 1)

Two `systemctl restart omniroute.service` cycles [FACT]:

| Item | Restart 1 (06:18:48Z) | Restart 2 (06:19:31Z) |
| --- | --- | --- |
| Wall to active (READY under `Type=notify`) | **526 ms** | **547 ms** |
| Budget (`TimeoutStartSec`) | 180,000 ms | 180,000 ms |
| Listeners after | {192.168.50.207, 127.0.0.1}:20128 only | same |
| Loopback unit | active throughout (independent lifecycle) | active throughout |
| `/healthz` loopback + LAN | 200 / 200 | 200 / 200 |
| Identity guard (8 hashes: unit, drop-ins ×3, loopback unit + script, `server.js`, `server-ws.mjs`) | all unchanged | (carried — verified again in G5/G6) |
| Connections | 5 (4 active; Chat-X inactive by posture) | 5 |
| Posture rows | effective | effective |
| Routed proof (nonce, genuine backend call) | Qwen-X `42` · stop · 117/32/149 | Meta-X `42` · stop · 83/102/185 |
| `usage_history` | 14 → 15 | 15 → 16 |

Journal since gate start: no watchdog kills, no OOM; each stop logs `Failed with result 'exit-code'` — the product exits 143 (SIGTERM) on shutdown, the same cosmetic unit-semantics quirk recorded at install (observation §11.6; service returns active every time).

## 6. G3 — cold reboot (gate item 6, part 2)

Pre-reboot backend snapshot from their hosts 06:21Z [FACT]: hxs-1 Qwen-X resident digest `766cd9469fb4`; hxs-2 Coder-X evicted (tags digest `ec9ebe08a824`); hxs-3 Meta-X resident digest `9dffb015db40`; hxs-4 Chat-X resident on `127.0.0.1:11434` only, digest `5936a390c6c2` (all four ollama services active; hxs-1..hxs-3 preload units `Result=success`; hxs-4 has no preload unit — residency via its own posture, record-only).

Timeline [FACT]:

| Mark | Time (UTC) | Delta |
| --- | --- | --- |
| `systemctl reboot` issued | 06:22:27 | — |
| Host boot (uptime -s; new boot-id `9f32db05…`, was `e492546c…`) | 06:22:50 | 23 s |
| `omniroute.service` Started (auto, no human action) | 06:22:59 | 32 s |
| `omniroute-loopback.service` Started + listening | 06:22:59 | 32 s |
| SSH answering (identity re-verified: hostname, machine-id, peer) | 06:23:04 | 37 s |
| Routing re-verified ×3 (below) | 06:24–06:25 | ≈2.5 min |

Post-reboot verification [FACT]: all three units active+enabled with zero human action; `NRestarts=0`; listeners exactly {192.168.50.207, 127.0.0.1}:20128; `/healthz` 200 loopback + LAN; anon settings 401; anon monitoring 2-key; management login 200; posture rows effective; `integrity_check ok`; connections 5. Routed nonce proofs: Qwen-X `42`/stop/150, Coder-X `42`/stop/240 (fresh load — it was evicted pre-reboot), Meta-X `42`/stop/187; `usage_history` 16 → 19.

Backend residency re-proven FROM THEIR HOSTS (read-only: `hostname`, `boot_id`, `systemctl is-active ollama`, `ss` listener, `/api/ps`, `/api/tags`) 06:25–06:26Z [FACT]:

| Host | Backend | Service | Listener | Resident | Digest | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| hxs-1 (.200) | Qwen-X | active | `*:11434` | yes (size == size_vram) | `766cd9469fb4` | PASS |
| hxs-2 (.201) | Coder-X | active | `*:11434` | yes (loaded by the G3 routed proof) | `ec9ebe08a824` | PASS |
| hxs-3 (.202) | Meta-X | active | `*:11434` | yes (size == size_vram) | `9dffb015db40` | PASS |
| hxs-4 (.203) | Chat-X | active | `127.0.0.1:11434` ONLY | yes (loopback) | `5936a390c6c2` | PASS — posture holds |

All four backend `boot_id`s unchanged across hxs-8's reboot (their hosts never went down — as designed). No backend host was changed in any way (verify-only commands).

## 7. G4 — backup/restore (gate item 5, part 1)

Snapshot [FACT]: `systemctl start omniroute-backup.service` 06:26:17Z → `SNAPSHOT_OK …/storage-20260828062617.sqlite bytes=2887680 kept=4` (integrity-gated, `Result=success`; the 03:17Z timer snapshot also present — the schedule runs as designed).

Restore to SCRATCH DATA_DIR (live data never touched) [FACT]:

1. `/opt/omniroute/restore-drill/` (0750 omniroute) created; snapshot copied to `restore-drill/storage.sqlite` — sha256 `d1b70274…` identical both sides.
2. Throwaway instance: versioned `omniroute-drill.service` (`Type=notify`, `DATA_DIR=/opt/omniroute/restore-drill`, `PORT=20228`, `OMNIROUTE_HOSTNAME=127.0.0.1`, `OMNIROUTE_ENABLE_LIVE_WS=0`, same hardening shape; its drop-in a mechanical root-only `cp --preserve` of the 0600 secrets drop-in, hash-identical — so JWT/encryption semantics match the restored DB). Started 06:27Z — READY in 414 ms, listener `127.0.0.1:20228` only.
3. **The restored state answers** through the product's own API: `/healthz` 200; anon settings 401; **management login 200** (restored bcrypt + live JWT secret agree); `GET /api/providers` returns **all five registered connections with correct ids** (4 HX + `main`); `/v1/models` with the HX client key 200 (api_keys restored).
4. DB-level probes on the scratch file: `integrity_check ok`; `secrets` namespace **0 rows**; posture rows intact; connection api_key classes correct (`main` = `enc:v1:` ciphertext, 4 HX = absent); `usage_history` = 19 (exact snapshot state); migrations 160; `:cloud` hits 0.
5. Teardown: drill stopped/disabled, unit + drop-ins + scratch dir + drill cookie removed, `daemon-reload`; live service verified untouched (pids, listeners, `usage_history` still 19, integrity ok).

## 8. G5 — rollback drill (gate item 5, part 2)

Rehearsal of the documented inverse to a checkpoint and forward again, live, without loss. The full install inverse (store wipe, unregistration) would risk the backends, so per the work order the data-plane inverse was proven on the scratch copy (G4), and the live rehearsal covered this gate's own change (the bind posture), whose checkpoint is the pre-gate `0.0.0.0` state [FACT]:

| Leg | Time | Actions | Result |
| --- | --- | --- | --- |
| ROLLBACK to checkpoint | 06:29:16Z | `disable --now omniroute-loopback.service`; `rm 30-v3.8.51-bind.conf`; `daemon-reload`; `restart omniroute.service` (507 ms) | Checkpoint restored exactly: single listener `0.0.0.0:20128`; `/healthz` 200; routed nonce proof Coder-X `42`/stop/250; `usage_history` 19 → 20 |
| FORWARD to design | 06:30:11Z | Re-push 3 artifacts from hxs-5 (hashes byte-identical: `1ce348ab/38de6006/c0e60b9c`); `daemon-reload`; `restart` (517 ms); `enable --now omniroute-loopback.service` | Design restored: {192.168.50.207, 127.0.0.1}:20128; health 200 ×2; anon 401; routed nonce proof Qwen-X `42`/stop/149; `usage_history` 20 → 21 |

No-loss proof [FACT]: connections 5 (4 active) throughout; `integrity_check ok` at every step; posture rows unchanged; `usage_history` monotonic 19 → 20 → 21; the DB was never replaced — the gate's change is config-only. Every other install inverse remains a recorded one-command-class operation against hashes (`03-trinity-l1-install.md` §11), with the data inverse now proven end-to-end (G4).

## 9. G6 — hygiene close-out (gate item 7 + secrets rule)

| Check | Evidence | Verdict |
| --- | --- | --- |
| `:cloud` tags (O1 tripwire) | distinct providers `[ollama-local, openrouter]`; `:cloud`-tagged connections 0; `cloud_agent_credentials` 0 rows; full-DB scan — **0 `:cloud` hits across every table/column**; no cloud/conductor/tunnel env names | PASS (literal tripwire) |
| Cloud reachability (honest scope note) | owner-dispositioned `main` openrouter connection (row 48: USD 100 cap, key accepted as-is, no allowlist directed); 934-entry OR catalog in `/v1/models`; 1 owner test call in `usage_history` | owner-accepted state — presented for ACCEPT, not a gate defect |
| Agent surfaces | MCP POST 503 (mgmt) / 401 (anon); A2A `{code:-32000, disabled}`; plugins `[]`; skills registry empty; 9router + mux `not_installed`; no tunnel processes; conductor env unset; posture rows `cloudEnabled/skills/mcp/a2a/memory/tailscale:false` | PASS |
| Secrets at rest | `secrets` namespace 0 rows; zero plaintext-class connection credentials (`enc:v1:` or absent); management password JSON-encoded 60-char bcrypt (`$2`, pattern-verified); drop-in 0600 root:root `05638010…`; key file 0600 `d8aa9c37…`; `server.env` 4 lines, no secret names (version marker only); HX key value 0 journal hits | PASS with two recorded exceptions below |
| Recorded exception E1 (owner-lane) | current management password value appears **×21** in the owner's interactive `/home/hxsa/.bash_history` on hxs-8 (0600, owner-only file; count-only probe, value never copied). Disposition: owner already decided "distinct dashboard password at next rotation" (row 48) — rotation + history scrub retires it | recorded for owner action |
| Recorded exception E2 (executor-lane, mine) | the same value appears in **4 sudo journal lines** on hxs-8 (05:56/06:07/06:24/06:27Z) — my login probes used `sudo env PW=<value> python3 …`, and sudo logs the env assignment. Root-readable journal only; no value reached any artifact, ev/ capture, or model context (the one context probe was redacted pre-output). Method corrected mid-session (remote-side extraction only). Remediation: same owner rotation + journal vacuum at the owner's discretion; journal is tamper-evident by design and entries were NOT altered | recorded openly; corrected |
| Loopback + LAN posture | final listeners {192.168.50.207, 127.0.0.1}:20128; hxs-5 LAN battery: `/healthz` 200, anon settings 401, anon monitoring 2-key; layered health (`/api/health`, `/api/health/ping` latencyMs 0–1) green on loopback + LAN | PASS |

Final live state [FACT]: all three units active; connections 5 (4 active); `usage_history` 21; `integrity_check ok`; backups kept=4 (2 drill + 03:17Z timer + gate snapshot); management session logged out (200; stateless-JWT nuance carried from install §12.1 — the executor cookie jar was destroyed, practical exposure closed); all `tri-*` session files removed from hxs-8 `/tmp`.

## 10. Acceptance reconciliation (goal gate items 1–7)

| # | Gate item | Evidence | Verdict |
| --- | --- | --- | --- |
| 1 | Runtime: Node in engines, systemd up after reboot with no human action, native (no Docker) | Node v24.20.0 (`>=24.0.0 <27`); G3 cold reboot — service Started 06:22:59Z auto, `NRestarts=0`; native systemd units | PASS |
| 2 | Secrets: no plaintext at rest (DB, repo, world-readable units, logs/artifacts); OD-13 mechanism | §2, §9: 0 plaintext rows; `enc:v1:`; 0600 drop-in hash-recorded; bcrypt at rest; STORAGE_ENCRYPTION_KEY active (owner's `main` key encrypted); zero secret values in this record — with E1/E2 recorded residue exceptions (owner rotation disposes) | PASS (deployment design) + 2 recorded exceptions |
| 3 | Routing: 4 backends registered with identity evidence; direct-vs-routed parity; usage accounting visible | §2 (registration + identity), §4 (parity deep ×3 tasks ×3 reachable backends; Chat-X waived posture-blocked per OD-08 amendment; usage_history rows 5–13 attributed) | PASS |
| 4 | Health: layered surface with documented auth split | §3, §9: `/healthz`, `/api/health`, `/api/health/ping` 200; anon 2-key vs management 25-key monitoring split; loopback + LAN | PASS |
| 5 | Backup/rollback: snapshot restores to a working state; rollback documented + rehearsed | §7 (snapshot → scratch working state answering via API + DB, integrity ok), §8 (checkpoint rollback + forward live, zero loss; install inverses recorded §11 of the install record) | PASS |
| 6 | Restart ×2 + one cold reboot, four-backend routing intact | §5 (526/547 ms vs 180 s budget; routing proof each), §6 (auto-start 32 s after boot; ×3 routed proofs; backend residencies re-proven from their hosts) | PASS |
| 7 | No cloud models, no `:cloud` tags; no agent-like surfaces | §9: zero `:cloud` anywhere (full-DB scan); agent surfaces disabled. Scope note: cloud models are REACHABLE through the owner-added, owner-dispositioned OpenRouter connection (row 48: USD 100 cap; no allowlist directed) — the goal's local-model-only posture for HX workloads stands by consumer convention; the literal tripwire passes | PASS with the owner-dispositioned scope note |

## 11. Findings, drift, residual risks

1. **Owner OpenRouter connection** [FACT + AUTHORITY]: `main` (openrouter, active, `enc:v1:` key) + full OR catalog in the model surface + 1 test call attributed to the HX client key. Dispositioned by the owner (row 48). Residual: any holder of an HX client-plane key can select cloud models; the owner explicitly directed no allowlist. Presented for ACCEPT.
2. **E1/E2 plaintext residue** [FACT]: §9. Neither touches the deployment design; both retire with the owner-decided rotation. E2 was my error; method corrected; recorded openly.
3. **Gateway semantic cache** [FACT]: byte-identical repeats are cache-served and skip usage logging (§4). Verification discipline: nonce-bust any proof call. Layer-2+ may want this characterized (cache policy is Layer-2 scope).
4. **Model-surface enrichment** [FACT]: `/v1/models` now also surfaces the backends' raw upstream tags and embedding models (product model sync). The alias-only consumer convention (`DOC-backend-*`) is unaffected; `hx-qwen3.5` still zero.
5. **Chat-X `test_status` display quirk** [FACT, carried from install §12.2]: row reads `active` while `is_active=0` and the endpoint is demonstrably loopback-only. Upstream SEV-4 display semantics; effective posture correct (zero models surfaced).
6. **Exit-code cosmetic** [FACT]: the product exits 143 (SIGTERM) on unit stop → systemd logs `Failed with result 'exit-code'` on every stop (install-era too). Service returns active every time; `SuccessExitStatus=143` would silence it (candidate for a future unit revision; not applied — minimal-change rule).
7. **Coder-X residency dynamics** [FACT]: hxs-2's model evicts between uses (MAX_LOADED_MODELS=1 + other consumers, e.g. embeddings); identity holds via tags digest; first call after eviction pays a load. Pre-M8 host per the standing deferral (row 66).
8. Residual risks for the owner: none high/critical beyond the recorded E1/E2 rotation item and the row-48 OpenRouter posture.

## 12. Second Brain evaluation (per the work order)

1. Opportunity identified: **yes** — the gate pattern generalized to a traffic plane: parity + restart + reboot + restore + rollback + hygiene as the reusable acceptance battery for future services; hxs-8's `configuration.md` is the second of its class.
2. Roadmap capability/pattern: capability registration through the Second Brain catalog — the acceptance battery and this record become catalog content at handoff; the backend records gained their first end-to-end routed-consumer evidence.
3. Disposition: **implemented** — the battery ran and is fully evidenced here; `servers/hxs-8/configuration.md` written per `servers/AGENTS.md`; this document goes to Carol for catalog receipt; handoff stays OPEN until the receipt is cited in the pilot state log.
4. Evidence/reasoning: every future service gets signed off by this battery, not by vibes.

## 13. Sanitized sequential command log

All local commands as hxsa@hxs-5; remote as hxsa@<target> over independent SSH sessions (pinned host keys, `StrictHostKeyChecking=yes`); SSH password via execution-time askpass only (never argv/history/logs); sudo `sudo -n`; the management password and HX client key extracted remote-side into shell variables and never echoed (one early method error — `sudo env PW=…` — logged the value into 4 sudo journal lines; corrected, recorded §9-E2). No credential value appears in any command or output below.

| Seq | Time (UTC) | Where | Command (sanitized) | Exit |
| ---: | --- | --- | --- | --- |
| 1 | 05:36–05:47 | hxs-5 | Read charter/profile/WO/CP/install/goal/servers-AGENTS/template/state-log 66–67; be-great survey of the pinned corpus (bind knob runtime-env.mjs:177, server-ws/liveServer/peer-stamp/managementPassword mechanics); known_hosts pin checks ×5 | 0 |
| 2 | 05:48 | hxs-5 | Create askpass + ssh helpers (0700); smoke `wc -c` → 10 | 0 |
| 3 | 05:48 | hxs-8 | Identity probe (hostname/peer/machine-id MATCH; sudo -n OK) | 0 |
| 4 | 05:49 | hxs-8 | Pre-state: unit states, 7 file hashes, drop-in modes, env NAMES, listeners, interfaces, key-file hash | 0 |
| 5 | 05:50–05:52 | hxs-8 | Lineage probes: omniroute journal 17:30Z–19:30Z (owner reset trace), sudo journal, drop-in metadata (names+lengths only) | 0 |
| 6 | 05:53–05:56 | hxs-8 | Residue sweep (`/tmp` scripts absent; `server.env` class; history count-only 21); management login probes (400 field-bug → 200 after awk fix); cookie jar 0600 root | 0→1→0 |
| 7 | 05:58 | hxs-8 | Read-only DB probe (schema, integrity, secrets ns 0, posture, connections ×5, usage 4, cloud sweeps 0) | 0 |
| 8 | 06:00–06:02 | hxs-8 | Password-format re-probe (probe artifact resolved: JSON-encoded bcrypt TRUE); `/v1/models` counts (1,496; 22 hx-; 0 hx-qwen3.5; 934 openrouter) | 0 |
| 9 | 06:04 | hxs-8 | Backend identity from hxs-8: Qwen-X/Coder-X tags digests MATCH (evicted), Meta-X resident MATCH, Chat-X rc=7 posture | 0 |
| 10 | 06:05–06:06 | hxs-5→hxs-8 | **MUTATION** stage + push 30-bind.conf + loopback-listener.mjs + omniroute-loopback.service; syntax check; install root-owned; hashes verified identical | 0 |
| 11 | 06:06:51–57 | hxs-8 | **MUTATION** daemon-reload; restart omniroute (589 ms); enable --now loopback unit; listeners {207, lo}:20128; healthz 200 ×2 | 0 |
| 12 | 06:07–06:08 | hxs-8 | Post-bind battery: anon 401s, monitoring 2/25 split, mgmt login 200, keyed models 200, posture effective | 0 |
| 13 | 06:10 | hxs-5 | LAN battery vs 192.168.50.207 (healthz 200; settings 401; mon 2-key; models 401) | 0 |
| 14 | 06:11–06:13 | hxs-8 | G1 parity battery (9 tasks direct+routed, sequential, temp 0): Qwen-X/Coder-X 6/6 identical; Meta-X content parity with thinking-token variance ×2 | 0 |
| 15 | 06:14 | hxs-8 | G1 control (Meta-X direct×2/routed×2): direct pair self-disagrees — variance model-side, proven | 0 |
| 16 | 06:15–06:16 | hxs-8 | usage_history evidence (9 rows attributed, 4→13); recount; semantic-cache discovery | 0 |
| 17 | 06:17 | hxs-8 | Cache probe: semantic_cache 9; nonce-bust call → usage 14 / cache 10 (cache behavior characterized) | 0 |
| 18 | 06:18:48 | hxs-8 | **MUTATION** G2 restart 1 (526 ms): guards intact; routed nonce Qwen-X 42/stop/149; usage 14→15 | 0 |
| 19 | 06:19:31 | hxs-8 | **MUTATION** G2 restart 2 (547 ms): guards intact; routed nonce Meta-X 42/stop/185; usage 15→16; journal scan (143-exit quirk only) | 0 |
| 20 | 06:21 | hxs-5→hxs-1..4 | Pre-reboot backend snapshot (read-only): services active, listeners, ps/tags digests; hxs-4 preload-unit check (absent, record-only) | 0 |
| 21 | 06:22:27 | hxs-8 | **MUTATION** `systemctl reboot` (pre-approved window) | 0 |
| 22 | 06:22:50–06:23:04 | hxs-8 | Cold reboot: new boot-id; SSH back in 37 s; identity re-verified | 0 |
| 23 | 06:23 | hxs-8 | Auto-start proof: 3 units active+enabled, no human action; listeners correct; health green; boot→READY 32 s | 0 |
| 24 | 06:24–06:25 | hxs-8 | Post-reboot: mgmt login 200; posture effective; routed nonce ×3 (Qwen-X 150, Coder-X 240, Meta-X 187); usage 16→19; integrity ok | 0 |
| 25 | 06:25–06:26 | hxs-5→hxs-1..4 | Backend residency re-proofs from their hosts (read-only): all four PASS; boot-ids unchanged | 0 |
| 26 | 06:26:17 | hxs-8 | **MUTATION** G4 snapshot: `systemctl start omniroute-backup.service` → SNAPSHOT_OK bytes=2887680 kept=4 | 0 |
| 27 | 06:27 | hxs-8 | **MUTATION** G4 scratch restore + drill boot (414 ms, 127.0.0.1:20228): copy hash-identical; drill answers (login 200, 5 connections, keyed models 200); DB proofs (integrity ok, secrets 0, usage 19) | 0 |
| 28 | 06:28–06:29 | hxs-8 | **MUTATION (inverse)** G4 teardown: drill unit + drop-ins + scratch dir removed; live verified untouched (usage 19) | 0 |
| 29 | 06:29:16–06:30:11 | hxs-8 | **MUTATION + inverse** G5: rollback leg (disable loopback, rm 30-bind, restart 507 ms → 0.0.0.0 checkpoint, routed proof, usage 19→20); forward leg (re-push hashes identical, restart 517 ms, design restored, routed proof, usage 20→21) | 0 |
| 30 | 06:31–06:35 | hxs-8 | G6 sweeps: `:cloud` 0 everywhere; agent surfaces (MCP 503, A2A −32000, plugins [], skills [], services not_installed, tunnels none); secrets final (0 rows, enc:v1, bcrypt TRUE, 0600 hashes); journal leak scans (key 0; pw 4 = my E2, context identified redacted); health surface; final state; logout 200; cookie + tri-* cleanup | 0 |
| 31 | 06:38 | hxs-5 | Corpus post-state witness → `f1d3b283…` byte-identical (read-only honored) | 0 |
| 32 | 06:39–06:42 | hxs-5 | `servers/hxs-8/configuration.md` + this record written; helper + staging cleanup; final verification | 0 |

## 14. Pre/post hashes and inverses for this gate's changes

| Change | Pre-state | Post-state (evidence) | Exact inverse |
| --- | --- | --- | --- |
| `30-v3.8.51-bind.conf` | absent | `1ce348ab…` (§3) | `sudo rm /etc/systemd/system/omniroute.service.d/30-v3.8.51-bind.conf && sudo systemctl daemon-reload && sudo systemctl restart omniroute.service` — rehearsed G5 |
| `omniroute-loopback.service` + `loopback-listener.mjs` | absent | `c0e60b9c…` / `38de6006…` (§3) | `sudo systemctl disable --now omniroute-loopback.service && sudo rm /etc/systemd/system/omniroute-loopback.service /opt/omniroute/ops/loopback-listener.mjs && sudo systemctl daemon-reload` — rehearsed G5 (disable leg) |
| Drill unit + drop-ins + scratch dir (G4) | absent | created, proven, REMOVED | already inverted (§7 step 5) |
| Corpus read-only | `f1d3b283…` (install witnesses) | `f1d3b283…` (06:38Z) | none needed — never mutated |

Install-era inverses stand as recorded in `03-trinity-l1-install.md` §11; the data-plane inverse (snapshot → working state) is now proven end-to-end (§7).

## 15. Task May Proceed receipt / handoff

```text
[TRINITY TASK COMPLETE — L1-M3 SECURE CORE GATE]
Agent: Trinity
Work Order: WO-L1-GATE-001 (GOAL-OMNIROUTE-L1-SECURE-CORE, milestone L1-M3)
Target: hxs-8 (192.168.50.207) — identity verified (hostname/peer/machine-id/host-key) before and after the reboot
PRE-GATE: primary listener rebound 0.0.0.0:20128 -> 192.168.50.207:20128 (OMNIROUTE_HOSTNAME,
  30-v3.8.51-bind.conf 1ce348ab…) + separate loopback listener (omniroute-loopback.service c0e60b9c…,
  loopback-listener.mjs 38de6006…); non-LAN interfaces unexposed; authN/authZ intact; evidence §3
G1 parity deep: PASS — 3 known-answer tasks × 3 reachable backends direct-vs-routed; content and
  finish identical everywhere; token accounting identical except Meta-X thinking-chain variance
  PROVEN model-side by the direct×2 control; usage_history evidences all 9 routed calls; Chat-X
  posture-blocked per OD-08 amendment (not a failure)
G2 restart ×2: PASS — 526/547 ms vs 180,000 ms budget; identity guard + routing intact each time
G3 cold reboot: PASS — down 37 s; auto-start 32 s after boot with no human action; routing intact;
  four backends' residencies re-proven FROM THEIR HOSTS (digests match; Chat-X loopback-only holds)
G4 backup/restore: PASS — snapshot 06:26:17Z; restored to a scratch DATA_DIR and BOOTED; the
  restored state answers (login, 5 connections, keyed models; integrity ok; secrets 0 rows;
  usage 19); live data never touched; drill removed
G5 rollback drill: PASS — checkpoint rollback (0.0.0.0 restored) and forward again (design restored,
  hashes identical) with zero loss; data-plane inverse proven on scratch (G4)
G6 hygiene: PASS with two recorded exceptions — zero :cloud anywhere; agent surfaces disabled;
  secrets mechanism verified; loopback+LAN posture as designed; E1 owner bash_history ×21 and
  E2 executor sudo-journal ×4 (both the current management password; owner rotation disposes)
Source Corpus: read-only honored — manifest f1d3b283… identical at 06:38Z
Secrets (OD-13): existence + mechanism only; zero values in any artifact
Retry budget: transient 0 of 1 used; sessions 1 of 2
Stop conditions hit: NONE (parity control resolved the only anomaly; no routing, restore, or
  secrets-design regression; no :cloud tags; no scope exceedance)
Recommended state: ACCEPT — handoff to Carol for catalog receipt (handoff OPEN until cited in the
  pilot state log); owner-lane items: management-password rotation (retires E1/E2), row-48
  OpenRouter posture as accepted
```

`PASS — TASK COMPLETE`
