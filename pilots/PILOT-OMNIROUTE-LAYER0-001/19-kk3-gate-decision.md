# KK3 Gate Decision — OmniRoute Layer 0 (Wave 0C close)

| Field | Value |
| --- | --- |
| Date | 2026-08-27 (UTC) |
| Governor | Kimi-K3 |
| Program | PILOT-OMNIROUTE-LAYER0-001 (p11) |
| Decision | **PASS — Layer 0 COMPLETE** |

## Basis

| Component | Evidence |
| --- | --- |
| Authority reconciled | Trinity ratified O1 (KDD-0008), roster updated, lane bounded; no candidate document stood as authority |
| Source identity | VERIFIED by content-sensitive proof — 13,098/13,098 git-blob identical to upstream `diegosouzapw/OmniRoute@42a13fedef8b…` |
| Capability ledger | 367 entries, 8 partitions, 1,325 source refs, dispositions 229/74/35/12/9/8; every reference producer-verified; governor spot-checks 8/8 on all partitions |
| Program reconciliation | `09-reconciled-program-packet.md`; corrected `10-control-manifest.yaml` |
| Independent verification | `18-independent-verification-report.md` — **Qwen-X: VERIFIED, zero artifact discrepancies** (recounts exact, 25/25 sample refs, schema exact, 40/40 structured verdicts sound, key numbers re-derived from corpus independently) |
| Catalog | 271 records, validator 4/4 PASS, receipts closing every handoff |
| hxs-8 | ONLINE, readiness evidence delivered (SUITABLE-WITH-FINDINGS; Node the single Layer-1 dependency) |

## Validation against p11's acceptance criteria (all PASS)

Trinity's roster state accurately represented (candidate → ratified, dated). Candidate documents reconciled, never copied as authority. Coder-X identity/status/endpoint/profile/health/limits verified per task (0 identity failures; one eviction handled by re-verification, never substitution). No cloud model or remote inference anywhere. Source identity reported with honest limits, then proven. Source instructions/metadata/lockfile/license reviewed. Ledger reproducible from exact references (deterministic recount matches). Every capability has owner/risk/test/dependency/disposition. Every owner decision has a blocking boundary (OD register). No host or service mutation occurred (zero). No deployment command ran. hxs-8 recorded as selected with its offline→online transition truthful (maintenance reboots + rick's readiness). No secret value in prompts, logs, evidence, reports, catalog records, or model context (swept; the two credential classes are policy-denied). All artifacts pass repository validation (validate.py 4/4; render --check in sync). Independent verification complete and separate from production (Qwen-X ≠ Coder-X hosts). Carol's handoffs all receipted and cited. This decision is recorded with exact evidence.

## Conditions carried forward (not failures — boundaries)

1. **OD-13 is a hard Layer-1 requirement** (owner-ratified): env-provision `JWT_SECRET` + `API_KEY_SECRET` and set `STORAGE_ENCRYPTION_KEY`; never accept the product's plaintext defaults.
2. Backup encryption and cloud upload are treated as **nonexistent** (write-only encryption; dead endpoint) — OD-09 plans around them.
3. Agent-like surfaces stay disabled: copilot driver (executes model output as host CLI), Conductor hub, cloud agents/CLI, tunnels, MITM bridge — 8 BLOCKED entries stand unless the owner explicitly reverses one.
4. Disabled-by-default is **not code-enforced** for skills execution and background jobs — Layer-1 config must set them explicitly.
5. No ATEM routing assumption for Meta-X (no adapter exists in v3.8.51).
6. hxs-8 host-dependent work still requires the owner's OD-03 acknowledgement of rick's readiness evidence.
7. Coder-X remains catalog-status candidate until its M8 — per-task identity/health verification is mandatory on every use.

## Decision

**PASS — Layer 0 COMPLETE.** The foundation is correct, reproducible, reviewable, and independent-verified. Recommended next gate: the owner's review of `11-owner-decision-packet.md` and, on his word, OD-12 — explicit Layer 1 authorization (the only door to installation). **Layer 0 completion does not authorize Layer 1.**

## Provenance note

`/opt/tkv-local/deepseek-harness-master` exists as reference material. KDD-0006's scope is a *deployed* DeepSeek Harness (none exists anywhere) — the corpus item is inert reference, no contradiction.
