# Retrieval package — hxs-1 for milestone M7

Package: `2026-08-25-hxs1-m7-package` · Producer: Carol · Produced: 2026-08-25T06:12:00Z · Revised: 2026-08-25T08:30:00Z (governor batch C16 — conflict entries C1–C7 gained per-source section anchors and explicit per-side freshness labels; content and authority ranking preserved)
Query: what an agent needs to know about hxs-1 for M7 — boot path, network, Wi-Fi state, GPU/driver posture, frozen model profiles, SLOs, constraints.
Scope rule: facts only, each with source and freshness. Conflicts flagged, not filtered. M7 = cold-reboot validation of the always-on 64K operating profile + 128K profile-switch mechanics, fallback 32K recovery [source: DOC-pilot-hx1-decision-23-m6-capacity §M7 implication; current].

## 1. Identity and network

- Host `hxs-1` == `HX-1` (identity declared; hxs-1 authoritative in evidence) [source: DOC-pilot-hx1-decision-23-m6-capacity §Host identity declaration; current].
- IP `192.168.50.200`, FQDN `hxs-1.hx.local.arpa`; registry role: Deep reasoning & synthesis — Qwen 3.8 27B [source: DOC-tkv-server-registry; current] [source: DOC-tkv-hxs1-discovery §Identity; historical-as-found — identity lines still match live state].
- DNS: router `HX-Router` `192.168.50.1` dnsmasq, domain `hx.local.arpa`; clients must use `192.168.50.1` as resolver [source: DOC-tkv-dns-fqdn-hx-local-dns; aging — unverified since the 2026-08-24 router-restart NXDOMAIN incident, recovered same morning per DOC-knowledge-network; aging].
- Ollama API is loopback-only; remote connection refused (proven M4/M5) [source: DOC-pilot-hx1-ev-12-esme-m4-install §4.3; current] [source: DOC-pilot-hx1-ev-16-esme-m5-validation §4.6; current — labeled comparison evidence].
- OPEN: foreign local client `192.168.50.220` present on hxs-1 (2 SSH sessions, 3 users at pre-M7) — owner question open; it is an M7 exclusive-window entry condition [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §9 via DOC-pilot-hx1-state-log row 29; current] [source: DOC-pilot-hx1-ev-29-esme-m6b-profiles §13; current].

## 2. Boot path

- Boot path sane for M7 reboots; `networkd-wait-online` residue clears on next boot (R-023 closed: 08-17 carrier loss was planned maintenance; no remediation) [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §6; current] [source: DOC-pilot-hx1-state-log row 14; current].
- Suspend targets masked with rollback since M2 [source: DOC-pilot-hx1-ev-07-rick-os-readiness §4; current].
- Ollama boots to the preloaded 64K operating profile: preload script and `hx1.conf` drop-in repointed (versioned one-line edits); residency Forever, 100% GPU [source: DOC-pilot-hx1-ev-29-esme-m6b-profiles §4, §7; current].
- D5 recovery credible: worst case ~75–90s measured at M4; 49.8s vs 900s SLO measured at M5 [source: DOC-pilot-hx1-ev-12-esme-m4-install §9; current] [source: DOC-pilot-hx1-ev-16-esme-m5-validation §4.5; current — comparison evidence].
- Secure Boot stays disabled — standing owner directive, do not enable [source: DOC-repo-governance-agents-md §Infrastructure posture directives; current] [source: DOC-pilot-hx1-state-log row 5 (D2); current].

## 3. Wi-Fi state

- Wi-Fi DISABLED 2026-08-25 per owner directive: rfkill sysfs soft-block `rfkill1`, management-path proof clean before mutation; persisted across boots via systemd-rfkill saved state; empirical confirmation is an M7 reboot-1 check; exact inverse: `echo 1 > rfkill1/state` [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §4; current].
- As-found state was DOWN-but-enabled (2026-08-11) — historical, superseded by the disable [source: DOC-tkv-hxs1-discovery; historical-as-found].

## 4. GPU/driver posture

- 2x RTX 4070 Ti SUPER, 16,376 MiB each; driver `580.173.02` retain-and-validate (owner decision D3) [source: DOC-pilot-hx1-ev-07-rick-os-readiness §6.1; current] [source: DOC-tkv-hxs1-driver-results; historical-as-found].
- PCIe caveat: GPU at `02:00.0` x16, GPU at `81:00.0` x4 of max x16 — known since discovery 2026-08-11, re-confirmed M2 and under M6 load; structural, not a fault [source: DOC-tkv-hxs1-discovery; historical-as-found] [source: DOC-pilot-hx1-ev-07-rick-os-readiness §6.3; current] [source: DOC-pilot-hx1-state-log row 27; current].
- Link speed varies with power state (2.5 GT/s idle vs Gen4) — not a contradiction [source: DOC-pilot-hx1-ev-07-rick-os-readiness §6.3 via catalog flag F2; current].
- NVRM `iovaspace` assertions classified MONITOR-ONLY: 0 Xid ever, 468 lines deterministic lifecycle bookkeeping; AER 0; M7 escalate triggers set [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §5; current].
- GPU compute util oscillation between cards under load is expected layer-split behavior; equal 50/50 utilization is a non-goal [source: DOC-pilot-hx1-state-log row 23 (owner EAM); current] [source: DOC-pilot-hx1-plan §1.3; current].
- Access model R-014 proven as installed (ollama:ollama under world-rw nodes; recorded, NOT modified); owner rejected `/dev/nvidia*` hardening — no future hardening proposals [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §3.1; current] [source: DOC-pilot-hx1-state-log row 10; current].

## 5. Frozen model profiles (Rev-2 disposition governs)

- Base model: `qwen3.8:27b` GGUF non-MLX, Q4_K_M 17.74 GB, digest `22130167c4c2` frozen at M4; baseline approved by Agent Zero [source: DOC-pilot-hx1-ev-12-esme-m4-install §4.4; current] [source: DOC-kdd-0004-hx1-qwen-pilot-adoption; current].
- Phase A (32K recovery): Modelfile sha256 `4869ce80…3165e`, alias digest `db2c6206…f645510` — CURRENT; supersedes M4 identities `dac63d7c…1d1df` / `23508b9c…185a8` [source: DOC-pilot-hx1-ev-19-esme-m5b-conformance §3–4; current].
- Three named aliases live with digest equality vs frozen references: `hx-qwen3.8-27b-32k` (`db2c6206…`), `-64k` (`766cd946…`), `-128k` (`94b83a1e…`); host resident at `-64k`, ctx 65536, 100% GPU, Forever; bare alias `hx-qwen3.8-27b` retired tags-only with deterministic inverse [source: DOC-pilot-hx1-ev-29-esme-m6b-profiles §3, §5, §7; current].
- Profile dispositions: 32K = frozen recovery baseline; 64K = preferred operating (always-on); 128K = qualified extended, explicitly selected; 256K out of pilot; the v1 single-context freeze was superseded BEFORE execution [source: DOC-pilot-hx1-decision-23-m6-capacity §Revision 2 / §Profile dispositions / §Supersessions recorded; current].
- Qualification evidence: 65,536 PASS (f16 KV, 19.06 GiB, needle 62,255); 131,072 PASS (f16, 21.81 GiB, needle 124,395, ~4.4 GiB headroom); D8 flat at all rungs; KV cost linear 45,056 B/token; 32K needle corrected to 30,015 (M5b Phase A) [source: DOC-pilot-hx1-ev-22-esme-m6-capacity-ladder §3–4; current] [source: DOC-pilot-hx1-decision-23-m6-capacity §Ladder results; current].
- Evidence-precision rule (owner-mandated): no measured accuracy regression in the needle test and D8 suites — NOT blanket accuracy immunity [source: DOC-pilot-hx1-decision-23-m6-capacity §Precision of the evidence claim; current].
- 128K harness requirements ratified into plan §6.1; recorded, no client built [source: DOC-pilot-hx1-ev-29-esme-m6b-profiles §10; current].
- Digest swap requires a controlled unload (F-M5B-1) — applies to any M7 profile switch [source: DOC-pilot-hx1-ev-19-esme-m5b-conformance §5 via state log row 20; current].
- Ollama version `0.32.15` on hxs-1 [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §3; current]. Note: TKV ollama corpus snapshot is v0.32.11 — aging reference, not truth [source: DOC-tkv-corpus-ollama; aging].

## 6. SLOs

- D5 readiness SLO (owner-confirmed): detect ≤2 min, recover ≤15 min, one bounded recovery attempt [source: DOC-pilot-hx1-state-log row 10; current].
- M6b handoff and pre-M7 handoff CLOSED by Carol run-1 receipt (state log row 35); M7 may stage once owner reboot approvals + exclusive window are set [source: DOC-pilot-hx1-state-log rows 34–35; current] [source: DOC-goal-hx1-ollama-qwen38-27b §Status; current].

## 7. Constraints (M7 entry and conduct)

- Each reboot individually owner-approved; 3 cold reboots + 24h soak per goal; one bounded correction per failed correctable gate [source: DOC-goal-hx1-ollama-qwen38-27b §Constraints; current].
- M7 validates the always-on 64K operating profile + 128K profile-switch mechanics; fallback 32K recovery; fallback triggers recorded in the decision record [source: DOC-pilot-hx1-decision-23-m6-capacity §M7 implication, §Fallback triggers; current].
- `OLLAMA_NO_CLOUD=1` confirmed [source: DOC-pilot-hx1-state-log row 10 (D6); current].
- No direct (non-loopback) API exposure; MLX out of scope except later separate benchmark [source: DOC-goal-hx1-ollama-qwen38-27b §Scope and target; current].
- Per-host TKV records (`/opt/tkv-local/servers/<host>/`) are controlling sources for all future work orders as historical as-found cross-checks, never current truth [source: DOC-pilot-hx1-state-log row 27; current].
- Wi-Fi disable persistence must be empirically confirmed at M7 reboot 1 [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §4.4–4.5; current].

## 8. Conflicts and flags (preserved, authority-ranked)

- C1 Registry wording stale: SERVER-REGISTRY hxs-1 row still says "Qwen 3.8 27B — unreleased, slot reserved" [source: DOC-tkv-server-registry §Registry row hxs-1; current record — row wording stale per catalog flag F-REG-1] vs released-and-deployed reality [source: DOC-pilot-hx1-state-log row 13; current]. KDD-0004 explicitly required no registry amendment; owner decision + live evidence outrank the row. Refresh at next registry amendment [catalog flag F7].
- C2 Phase-3 guard tension: registry retains "Phase 3 mutation guard hard-locked" [source: DOC-tkv-server-registry §Phase 1 Gate — historical (Phase 3 guard text); current — guard retained as record] while the owner-authorized pilot configures hxs-1's ratified workload [source: DOC-pilot-hx1-state-log row 28; current]; owner directive outranks the guard text. hxs-1's configured state lives only in the pilot corpus until `hxs-1/configuration.md` is created at M8 (owner-approved) [catalog flag F8 — review at M8].
- C3 M5 validation was executed on the sampled-profile alias: retained as harness/recovery/security/benchmark + Phase-B comparison evidence, NOT acceptance (A01) [source: DOC-pilot-hx1-ev-16-esme-m5-validation §4; current — relabeled comparison-only per A01]; acceptance evidence is M5b 32K Phase A [source: DOC-pilot-hx1-ev-19-esme-m5b-conformance §8; current]. A01 outranks the M5 execution basis.
- C4 plan §6.5 sampling values superseded by A01 §4.2 [source: DOC-pilot-hx1-plan §6.5; current — section marked non-executable historical provenance] [source: DOC-pilot-hx1-amendment-a01 §4.2; current — scoped supersession of §6.5 only]; A01 §4.3 131,072-row and §4.4 bare-alias identity superseded by Rev-2 — cite Rev-2 profiles, never the v1 freeze [source: DOC-pilot-hx1-decision-23-m6-capacity §Supersessions recorded; current]. Rev-2 outranks A01 rows; A01 outranks plan §6.5.
- C5 Discovery mutable lines stale against later events ("34 packages upgradable", "no Ollama installed", Wi-Fi DOWN-enabled) [source: DOC-tkv-hxs1-discovery §whole-document; historical-as-found; catalog flag F3] vs later state [source: DOC-pilot-hx1-ev-26-rick-pre-m7-readiness §3–4; current] [source: DOC-pilot-hx1-ev-12-esme-m4-install §4; current] — record remains valid as historical-as-found; later changes, not errors. Live evidence outranks the as-found lines for current state.
- C6 hxsa NOPASSWD sudo (ALL:ALL) on hxs-1 recorded as risk observation F-M5-2; no action per owner no-hardening stance [source: DOC-pilot-hx1-state-log row 17; current] [source: DOC-pilot-hx1-ev-16-esme-m5-validation §Findings F-M5-2; current].
- C7 Credential note: SSH access to hxs-1 uses the protected resource `ssh-info.md` (existence/owner/askpass retrieval only; contents never accessed) [source: DOC-protected-ssh-info-hxs1 §whole-document; current].

## Economy note (CAT-22)

This package substitutes for reading the raw corpus for M7 context: the pilot evidence set (26/29/23/22/19/12/16/07), goal, plan, state log (37 rows), registry, discovery, and DNS records — several hundred KB of source — compressed to the facts above with provenance intact. Raw sources remain authoritative; follow the DOC-ids when full sections are needed.
