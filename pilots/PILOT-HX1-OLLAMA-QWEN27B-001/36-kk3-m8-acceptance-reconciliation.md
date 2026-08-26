# M8 — Acceptance Reconciliation and Sign-off Package (PILOT-HX1-OLLAMA-QWEN27B-001)

| Field | Value |
| --- | --- |
| Milestone | M8 — final evidence reconciliation, KK3 gate, owner sign-off (SC-09) |
| Date | 2026-08-26 |
| Governor | Kimi-K3 |
| Goal | `goals/2026-08-24-hx1-ollama-qwen38-27b.md` (GOAL-HX1-QWEN38-001) |
| Decision requested | Owner verdict: **ACCEPT / ACCEPT WITH CONDITIONS / REJECT** (section 9) |
| Companion record | `/opt/tkv-local/servers/hxs-1/configuration.md` (server records contract, Phase 2 — owner-ratified into M8 at state-log row 28) |

## 1. Acceptance matrix (goal §Success conditions)

| SC | Property | Expected result | Verdict | Principal evidence |
| --- | --- | --- | --- | --- |
| SC-01 | Model identity frozen | Exact approved artifact recorded | **PASS** | Phase A alias frozen at M5b (digest `db2c6206…`, Modelfile sha256 `4869ce80…3165e`, Q4_K_M 17.74 GB); three owner-ratified profiles frozen at M6b with digest equality (32k `db2c6206…`, 64k `766cd946…`, 128k `94b83a1e…`) — 19-esme §identity, 29-esme §2; rows 20, 34 |
| SC-02 | GPU placement | Both GPUs allocated; no unapproved CPU fallback | **PASS** | 100% VRAM resident at every rung (32K: 10364+10502 MiB; 128K: 14,290+14,250 MiB); layer-split compute alternation explained and accepted (row 23); zero CPU-fallback events — 12/19/22-esme; live `/api/ps` (size == size_vram) |
| SC-03 | Largest stable context | Largest passing setting frozen | **PASS (as ratified, Revision 2)** | Three profiles: 32K recovery baseline, 64K operating default, 128K qualified extended (owner disposition); capacity+quality PASS at all rungs (needle 30,015 / 62,255 / 124,395 tokens; D8 flat; KV linear 45,056 B/token; 128K ≈4.4 GiB headroom) — 22-esme, 23-kk3 Rev 2, 29-esme; rows 24–25, 30 |
| SC-04 | Boot recovery | Model resident and ready each reboot, no manual action | **PASS** | AC-007 3/3 cold reboots, 60 s boot→ready deterministic ×3 (15× under the 900 s D5 SLO), zero intervention post-reboot, NRestarts=0, loopback-only; kernel 7.0.0-28→30 transition with driver re-proof (DKMS both); unplanned real-world confirmation 2026-08-25 (site power cut: 56 s autonomous recovery) — 30-esme; rows 42, 47 |
| SC-05 | 24 h soak | No unexplained unload/OOM/fallback/Xid/restart loop | **DEFERRED BY OWNER** (not waived) | Owner directive 2026-08-25: M7b deferred to backlog (`knowledge/issues.md`); AC-008/AC-016 evidence absent by decision; M8 scope adjusted accordingly — rows 40, 53 |
| SC-06 | Workload quality | Owner-confirmed thresholds met | **PASS** | D8 thresholds owner-confirmed (row 14). M5 7/7 suites (sampled alias): recall 1.000, groundedness 100%, tools 24/24 conformant + 100% denial, coding 10/10, recovery 49.8 s vs 900 s. M5b re-run at A01 native defaults: recall 1.000, groundedness 100% + no-answer/poison 100%, tools 100% denial + conformance, coding 9/10 (parse_kv test-contract mismatch disclosed, not tuned) — 16-esme, 19-esme; rows 17, 20 |
| SC-07 | Exposure | Loopback-only or approved authenticated gateway | **PASS** | Remote API refused (TCP 11434 connection refused from hxs-5 while TCP 22 open); CORS 403 to foreign origins, localhost-only allowlist; OLLAMA_NO_CLOUD=1 — 16-esme S01–S03; verified again post-outage 2026-08-25 |
| SC-08 | Context contract | Effective context matches frozen setting | **PASS** | `num_ctx` effective per `/api/ps context_length` at every profile (65,536 at the 64K operating profile — verified live 2026-08-26) — 29-esme §residency; PILOT-002 note honored |
| SC-09 | Process | Complete sanitized packages; KK3 gate; owner sign-off | **GATE HELD — OWNER VERDICT PENDING** | This package; every deliverable sanitized (per-artifact sweeps + repo-wide validator secret scan, 405 files, 0 hits; literal-credential sweep CLEAN); handoffs closed by Carol receipts throughout — rows 28–62 |

## 2. Deviations, incidents, and corrections (full register)

| ID | What happened | Disposition | Evidence |
| --- | --- | --- | --- |
| F-M5-1 | SSH secret briefly in a temp evidence log | Contained <1 min; no remote copies; repo verified clean; rotation REJECTED by owner (standing) | 16-esme; row 17, 40 |
| F-M5-2 | hxsa NOPASSWD sudo (ALL:ALL) found | Recorded as risk observation; owner no-hardening stance — no action | 16-esme; row 17 |
| F-M6-3 | Foreign client 192.168.50.220 during M6 | Closed — it was the owner (nvidia-smi trail + needle test) | rows 24, 40 |
| D8 parse_kv | Coding suite 9/10 at M5b | Test-contract mismatch disclosed, not tuned; thresholds still PASS | 19-esme; row 20 |
| F-M6B-2 | LimitNOFILE dropped in a candidate drop-in | Caught by frozen-hash cross-check pre-deployment; process worked | 29-esme; row 34 |
| F-M7A-1 | rfkill save-file quote 0 vs 1 | Record corrected openly (conclusion correct, digit wrong) | 30-esme; row 42 |
| F-M7A-2 | Watchdog WARN pair once per cold load | Classified deterministic; recommended expected-class for monitors | 30-esme; row 42 |
| A01 chain | §6.5/§4.3/§4.4 superseded by Rev 2 and M6b | All three marked inline at source; catalog relations section-scoped | plan, A01; rows 30, 33, 52 |
| Path accident | agents/carol nested under agents/john (17:46Z 08-25) | Restored; owner confirmed accidental; ratified as correct state | rows 48–49 |
| Preload budget | TimeoutStartUSec 20min vs 900 s D5; unbounded retries | Fixed (600 s unit; 538 s worst-case script) and governor-verified live | 35-esme; rows 52, 57 |
| Credential source | ssh-info.md moved to `keys.md/` 239-line guide (owner reorg) | All consumers re-pointed; catalog record updated; rotation-conflict recorded per §9 (owner standing governs) | rows 61–62 |
| Review batches 1–8 | ~60 findings across docs, catalog, fixtures, renderer | All dispositioned (fixed / skipped-with-reason / rejected-with-authority); regressions at 57 fixture + 12 renderer tests | rows 33, 36, 43–46, 48, 51–52, 62 |

## 3. Residual risk register (accepted, with controls)

| Risk | State | Control / note |
| --- | --- | --- |
| NVRM iovaspace assertions | MONITOR-ONLY (0 Xid ever) | Escalate triggers set (any Xid; assertions outside lifecycle windows) — 26-rick; monitors must scope Xid to NVRM (NIC "XID 64a" false positive noted, row 47) |
| Cold-load timing | Bounded by config, not measured (no-reboot scope) | `--max-time 300` + `TimeoutStartSec=600` — 35-esme limitation recorded |
| PCIe x4 vs x16 (GPU2) | Known since 2026-08-11; equal utilization is a non-goal | Recorded; workload evidence unaffected — discovery; 22-esme |
| Wi-Fi re-enablement | rfkill soft-block persisted ×4 incl. unplanned power loss | Inverse documented (`echo 1 > rfkill1/state`) — 26-rick; row 47 |
| Kernel regression | 7.0.0-30 proven; -28 remains GRUB recovery | DKMS built for both; rollback requires owner-approved reboot — 30-esme §rollback |
| BIOS unoptimized (MSI) | Owner's own note; informational | Owner task; no pilot dependency |
| 256K context | Unproven; excluded from pilot | Owner disposition (Rev 2) |
| Credential in plaintext guide | Owner standing no-rotation; guide itself recommends rotation | Conflict recorded authority-ranked (owner governs); protected-resource conventions hold; U5 hook pilot now intercepts payload leaks |

## 4. Rollback state (as of sign-off)

- 32K frozen recovery baseline: alias `hx-qwen3.8-27b-32k`, digest `db2c6206…` (reversible from frozen Modelfile, deterministic inverse proven).
- Operating profile: `hx-qwen3.8-27b-64k` (preload + hx1.conf point here; one-line versioned inverses).
- Bare alias: retired tags-only; inverse = re-create from 32K Modelfile (digest reproduces).
- Application/config layer: full inverse per 13-esme layers A–D (runtime-only unless approved model-data deletion — approval-gated).
- Kernel layer: GRUB previous entry (7.0.0-28, DKMS ready).

## 5. Final gate evidence (2026-08-26, this package)

- Live hxs-1: both units active; resident `hx-qwen3.8-27b-64k` digest `766cd9469fb4`, 20,463,789,012 B 100% VRAM, ctx 65,536; `TimeoutStartUSec=10min`; rfkill1 state 0; zero Xid this boot; uptime since 2026-08-25T16:23Z.
- `scripts/validate.py` (ratified UD1): **PASS 4/4** — wiki 32/32, fixtures 57 tests + manifest, catalog mechanical (180 records), secret sweep 0 hits.
- CAT-10..15 (owner-ratified golden corpus) reaffirmed from records: all six known answers present with provenance.
- Governor literal-credential sweep (manual gate): CLEAN.

## 6. Second Brain disposition (standing directive, mandatory)

1. **Opportunities identified during this pilot:** yes — the pilot itself produced the Second Brain's first operating slice.
2. **Capabilities/patterns applied:** Carol steward + catalog (owner amendment), provenance-backed records and receipts closing every handoff, golden-question battery (CAT-10..15, owner-ratified), retrieval packages (19× measured economy), truth-state/conflict preservation (C8 worked example), lessons codified into CAT-07/08.
3. **Dispositions:** implemented (catalog, receipts, batteries, packages); recommended for future iterations (pattern library candidates from lessons; R2 execution gate in live use from next package); deliberately deferred (databases/indexes, always-on automation, API/SDK — gates unmet).
4. **Evidence/reasoning:** catalog at 180 records, CAT/CB green, CB-01 bounds PASS every run; the roadmap's vertical slice is operating, so no gate opens as a side effect of this sign-off.

## 7. What this sign-off does NOT do

Does not close SC-05 (soak stays backlogged pending owner); does not open remote
access (loopback-only posture stands; owner D1/OmniRoute is the gate); does not
authorize 256K experiments, fleet rollout, fine-tuning, MLX work, or any new host
change; does not change the no-hardening posture.

## 8. KK3 gate verdict

All ratified success conditions are PASS, PASS-as-ratified, or owner-deferred with
the deferral recorded as such (not waived). Incidents are contained, disclosed, and
either corrected or accepted by the owner. Evidence is complete, sanitized,
receipt-closed, and reproducible (state-log rows 1–62; catalog 180 records).
**The governor recommends ACCEPT.**

## 9. Owner decision

- [x] **ACCEPT** — pilot closed as PASS (SC-05 deferred-by-owner recorded).
- [ ] **ACCEPT WITH CONDITIONS** — conditions: ______________________
- [ ] **REJECT** — grounds: ______________________

Signed: **Jarvis Richardson** (verbatim owner verdict: "I jarvis Richardson Accept M8")  Date: **2026-08-26**

## 10. Provenance

Goal file + plan (ratified versions); evidence artifacts 03–35 in this directory;
decision record 23-kk3 Rev 2; amendment A01 (+ inline markings); state-log rows
1–62; catalog records and receipts (index `2275606f…`); live verification
2026-08-26 (section 5); server records contract (`/opt/tkv-local/servers/AGENTS.md`).
