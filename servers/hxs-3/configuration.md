# hxs-3 — Configured State

**Phase:** Owner-authorized server implementation
**Configuration date:** 2026-08-27 (record date; implementation executed 2026-08-26 → 2026-08-27 across milestones M1/M4/M7/M5/M8 of `PILOT-HXS3-MUSE-GLIMMER-TOOLING-001`)
**Assigned role:** Agent intelligence (copied from `SERVER-REGISTRY.md`, owner-ratified 2026-08-13)
**Primary workload / model:** **Meta-X tooling-inference backend** — Ollama `muse-glimmer:30b` (frozen digest `de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1`), operating profile alias `hx-muse-glimmer-64k` (digest `9dffb015db409f44713b7c5a9ab5413e140c41eb4e72eac7ca753ce1b99de7da`, ctx 65536, resident Forever), per the owner-commissioned goal `GOAL-HXS3-MUSE-GLIMMER-001` and KDD-0007.
**Approved by:** Agent-Zero (owner) — goal approved 2026-08-26; M8 sign-off gate approved 2026-08-27 (pilot state log row 23)

> Registry note (divergence recorded openly, not resolved by this record): the
> `SERVER-REGISTRY.md` Workload / Model field for hxs-3 still reads the
> 2026-08-13 target-state "gpt-oss-20b TP=2; LightRAG graph & retrieval". The
> owner-commissioned Muse Glimmer pilot (explicit owner instruction, the higher
> authority) configured the workload recorded here instead. The registry is
> owner-maintained and was not edited by the pilot (hxs-1 F-REG-1 class —
> owner-side item). gpt-oss remains a task-shaped control per KDD-0007, not the
> configured workload.

## Discovery Reference

```text
servers/hxs-3/discovery.md
```

As-found record dated 2026-08-12; preserved unchanged (sha256 verified at this
record's writing and cited in `15-esme-m8-signoff.md`). Do not modify the
discovery record.

## Role Objective

- hxs-3 is the factory's primary **tooling-inference backend** (fleet call-sign
  **Meta-X**, blueprint §8) for the RAG pipeline: a **sequential,
  one-tool-call-per-turn specialist** per KDD-0007. The model proposes at most
  one tool call per turn and never authorizes or executes; KK3 retains
  orchestration, parallelization-above-the-model, acceptance, and evidence.
  `parallel_tool_calling: false` is registered as a first-class capability
  LIMIT in the Second Brain catalog record `DOC-backend-meta-x` (status
  `candidate` until the owner's M8 ACCEPT, then `active` — governor's lane).

## Final Configuration

### Operating System

- Hostname: `hxs-3`
- OS: Ubuntu 24.04.4 LTS (noble); kernel `7.0.0-30-generic` (HWE); DKMS
  `nvidia/580.173.02` installed for kernels 7.0.0-28 and 7.0.0-30
- Suspend targets masked ×4: `suspend`, `hibernate`, `hybrid-sleep`,
  `suspend-then-hibernate` (blueprint mask set; verified masked at M8)
- Secure Boot: disabled (owner standing directive — never enable)
- Wi-Fi: rfkill soft block with boot persistence (owner D4; rick M1)
- Time: `Etc/UTC`, NTP active and synchronized (fleet pass
  2026-08-26T23:52:40Z; named source time.cloudflare.com per the fleet record)

### Network

- IPv4: `192.168.50.202/24` on `eno1` (MAC `40:8d:5c:e7:d0:e5`); gateway
  `192.168.50.1` (static)
- Listening services / ports: `*:11434` (Ollama, wildcard with loopback
  preserved), `:22` (sshd), loopback stub DNS `:53`, llama-server internal
  loopback only — nothing else
- Firewall: **none** (owner rule 2026-08-26 — ufw present but inactive; nft
  and iptables filter rulesets empty). The private LAN `192.168.50.0/24`
  itself is the exposure boundary (blueprint §5); the O1 monitoring tripwire
  (store-policy `:cloud` scan, any appearance = automatic finding) is the
  named residual until an authenticating gateway (owner decision) fronts the
  backends

### Storage

- Filesystems: root ext4 on 3.6 TB NVMe (`/dev/nvme0n1p2`), 3.4 TB free;
  1.8 TB SATA SSD unallocated (discovery, untouched)
- Role-specific layout: Ollama model store on root ext4 per blueprint D1 —
  `/usr/share/ollama/.ollama/models` (`ollama:ollama`), 17 GB across the
  frozen artifact and aliases (shared blobs)

### GPU / Accelerators

- 2× PNY RTX 5060 Ti (GB206, PNY `196e:143e`), 16,311 MiB each (32,622 MiB
  aggregate); no integrated graphics
- Driver: NVIDIA 580.173.02 (retain-and-validate; DKMS for both installed
  kernels); zero Xid across all pilot evidence
- Relevant configuration: both cards wired PCIe **x8** against the x16 device
  max (Gen3 8.0 GT/s negotiated under load — the x8 width is the hard ceiling,
  measured M4/M7; idle Gen1 readings are ASPM downshift). Discovery's VF BAR /
  Above-4G note stands (non-fatal)

### Role-Specific Software

- Software: Ollama **0.32.15** (pinned at M4; binary == server;
  `/usr/local/bin/ollama`; upstream 0.33.0 deliberately not taken — fleet
  consistency, F-J4)
- Frozen artifact: `muse-glimmer:30b` digest
  `de878ce33ad81d060001db1469a02eebe4d86f0ad58cfe52dc062fdcbe4464c1` — dense
  27.9B (52 blocks), Q4_K_M, max context 131,072, capabilities
  completion/vision/tools/thinking, renderer/parser `glimmer` with the ATEM
  tool parser, CLIP projector "Muse Glimmer Hf" 1.92B Q4_K_M, Apache-2.0
  (publisher-declared)
- Aliases (all FROM the frozen artifact with manifest layer-equality proofs,
  M7 §7): `hx-muse-glimmer` (`472ad84e752d…`, baked params only),
  `hx-muse-glimmer-32k` (`09c4f825ac2f…`), **`hx-muse-glimmer-64k`
  (`9dffb015db40…` — the D5 operating profile, resident)**, `hx-muse-glimmer-128k`
  (`17fe5b804838…`, qualified extended). Baked sampling everywhere:
  `temperature 1, top_k 64, top_p 0.95` (native defaults; the A01 rule)
- Configuration paths:
  - `/etc/systemd/system/ollama.service` (reviewed-installer unit; sha256 `11758d46…1dbd3`)
  - `/etc/systemd/system/ollama.service.d/hx3.conf` (sha256 `07824e4e…e7d5`):
    `OLLAMA_HOST=0.0.0.0` (loopback preserved), `OLLAMA_NUM_PARALLEL=1`,
    `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_CONTEXT_LENGTH=65536`;
    `OLLAMA_NO_CLOUD` was removed 2026-08-26 by the ratified fleet web-search
    enablement (owner signin per host; blueprint §5 honest-enforcement shape)
  - `/usr/local/libexec/hx-ollama-preload` (sha256 `b1798130…fe08`): bounded
    phases — ≤208 s API wait + ≤300 s single-attempt load + ≤30 s exact
    alias+digest `/api/ps` assertion = 538 s worst case, `keep_alive=-1`
  - `/etc/systemd/system/ollama-preload.service` (sha256 `3b0e00b6…a5f6`):
    oneshot, `TimeoutStartSec=600`, enabled at boot — 300 s under the 900 s
    D5 recovery SLO
- Web search: ACTIVE (owner decision 2026-08-26); no `:cloud` tags in the
  store (policy + tripwire; verified at M8)

### Services

| Service | Purpose | Enabled | Active |
| ------- | ------- | ------- | ------ |
| `ollama.service` | Ollama 0.32.15 server, LAN-scoped (`*:11434`) | yes | yes (running; `NRestarts=0`) |
| `ollama-preload.service` | Boot-time pin of `hx-muse-glimmer-64k` (`keep_alive=-1`) + exact alias+digest assertion | yes | yes (exited; `Result=success`) |

## Validation

```text
[x] Base system healthy        — rick M1 13/13 (04-rick-hxs3-os-readiness.md); 0 failed units after every M8 reboot
[x] Network healthy            — M1; M8 boundary proof (listener shape, LAN 200, no firewall) — 15-esme §5
[x] Storage healthy            — 3.4 TB free; model store intact across 3 cold reboots — 15-esme §3/§4
[x] Role-specific runtime healthy — M4 install 19/19 (07-esme); M7 ladder 3 rungs PASS (09-esme)
[x] Required services active   — both units enabled+active, NRestarts=0, preload Result=success ×3 boots — 15-esme §4
[x] Assigned workload validated — identity freeze (M4); capacity 32K/64K/128K (M7); tooling contract + one-call-per-turn enforcement (M5, 12-esme); persistence 3/3 cold reboots with no human action, consumer-proof end-to-end (M8, 15-esme)
```

Open validation gap (recorded, owner disposition required): goal SC-06
(multimodal image-input probes with the projector loaded) has no executed
evidence in the pilot record — reconciled OPEN at M8 §8; not a defect of the
configured state.

## Material Change Record

| Timestamp (UTC) | Previous State | Change | Files / Commands | Validation | Rollback | Unresolved Issues |
| --------------- | -------------- | ------ | ---------------- | ---------- | -------- | ----------------- |
| 2026-08-26T05:13Z | No Ollama; baseline OS | M1 OS readiness: suspend masks ×4, rfkill Wi-Fi block, no-firewall verification (rick) | `04-rick-hxs3-os-readiness.md` | 13/13 PASS, governor live-verified | Inverse per M1 record | F-08 tz drift (closed by fleet pass below) |
| 2026-08-26T06:28Z | No Ollama | M4: Ollama 0.32.15 pinned install; exact-tag pull + full identity freeze; `hx-muse-glimmer` alias; hx3.conf; preload script+unit at D5 budgets | `07-esme-m4-install.md` (byte-copies + hashes) | 19/19 PASS | `07-esme §11` (units/config inverse; tag removal approval-gated) | F-J1 watchdog class (monitor); F-J2 VRAM-default ctx (owned by M7) |
| 2026-08-26T07:19Z | `OLLAMA_NO_CLOUD=1` in hx3.conf | Fleet web-search enablement (owner): NO_CLOUD removed fleet-wide; per-host owner signin; blueprint §5 amended with the honest enforcement shape | hx3.conf (sha256 → `07824e4e…e7d5`); state log row 12 | Governor-verified; `disable_ollama_cloud` absent verified | Re-add NO_CLOUD (owner decision only) | O1 residual named (LAN-open API incl. `/api/pull`; tripwire until gateway) |
| 2026-08-26T07:58Z | ctx = VRAM-based default 32768 | M7: three rung aliases FROM the frozen artifact (digest-equality proofs); preload + hx3.conf repointed to `-64k`; `OLLAMA_CONTEXT_LENGTH=65536` | `09-esme-m7-ladder-profiles.md` (versioned diffs, pre/post hashes) | 3 rungs CAPACITY PASS; needle found 95% at every rung | `09-esme §13` (script/drop-in restore; rung aliases tags-only removal) | F-M7-1 FROM-digest syntax limitation (0.32.15); F-M7-2 scheduler sizing note |
| 2026-08-26T23:52:40Z | `America/Panama` | Fleet time pass (rick, owner one-source directive): `Etc/UTC`, NTP synchronized | `servers/2026-08-26-fleet-time-and-mask-pass.md`; state log row 19 | Three-view verified | — | Running ollama process formatted EST cosmetically until its next restart (closed at M8 cycle 1) |
| 2026-08-27T02:10Z | Candidate | M8 sign-off gate: persistence proof 3/3 cold reboots (no human action, 98 s boot→ready deterministic); endpoint boundary proof; consumer-proof task; this record | `15-esme-m8-signoff.md` | This gate (all PASS) | Nothing to roll back — no baseline change in M8 | SC-06 OPEN (above); registry workload-field divergence (owner-side) |

## Sources

- `servers/hxs-3/discovery.md` (as-found, 2026-08-12; preserved)
- `pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/`: `01-state-log.md` (rows 1–23), `04-rick-hxs3-os-readiness.md`, `07-esme-m4-install.md`, `09-esme-m7-ladder-profiles.md`, `12-esme-m5-validation.md` (+ Addendum A), `15-esme-m8-signoff.md`
- `goals/2026-08-26-hxs3-muse-glimmer-tooling.md` (owner decisions D1–D8; SC-01…SC-08)
- `knowledge/decisions/KDD-0007-hxs3-muse-glimmer-tooling-adoption.md`
- `servers/BLUEPRINT-llm-server.md` (§2–§6 planes; §8 Meta-X consumer contract)
- `servers/SERVER-REGISTRY.md` (assigned role; owner-maintained)
- `servers/2026-08-26-fleet-time-and-mask-pass.md`
