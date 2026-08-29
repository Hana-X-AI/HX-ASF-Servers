# PILOT-DSH-IMPL-001 — Routing Packet: Morpheus Phase C Prep → Gordon (Gate 8–10 authoring)

**Issuer:** Flash (governor), work order 27, 2026-08-29
**Executor:** Mia (Chief of Staff, KDD-0012)
**Model lane:** `omniroute/glm-5.3-flash` (GLM 5.3 Flash, Modal, via OmniRoute hxs-8)
**Nature:** Routing and coordination only. No test-plan content authored here; no lane mutation. Gordon's Gate 8–10 authoring proceeds under a separate governor work order.

---

## Routed items

| # | Source document | What it contains | Gordon's use | Key sections |
| --- | --- | --- | --- | --- |
| 1 | `pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md` | 4 families (interop/sandbox/remote/experimental) with source seams; **testability matrix (16 rows)**; open risks; knowledge-review receipt | **Primary authoring reference for Gates 8–10.** The matrix defines what is PROVABLE read-only on the frozen hxs-15 candidate vs BLOCKED-by-design, per seam | §Testability matrix (lines 311–341); families at §27–310; scope rule: candidate FROZEN during the campaign; host-status reads go through the governor, never via candidate touch |
| 2 | `pilots/PILOT-DSH-IMPL-001/10c-morpheus-rollback-ops-design.md` | Part A: rollback drill design (7 hash-anchored steps R1–R7 + trinity-shaped parity battery G-PARITY…G-HYGIENE); Part B: upgrade runbook S0–S7; Part C: Tier-1 smoke suite | **Gate 9 execution planning** (rollback drill); Part C is install-verification context only — **NOT qualification evidence** | Part A §11–84; Part B §86–107; Part C §109–151 |
| 3 | `pilots/PILOT-DSH-IMPL-001/10b-morpheus-r1-advisory-analysis.md` | 38 R1 advisories scored: 33 resolved-by-next-intake (RBI), 5 needs-upstream (vite@5.4.21/esbuild@0.21.5 lineage, interim accepted-risk); version map; next-intake action list | **Informational context only — not blocking** any Gate 8–10 claim. Affects future intake scoring, not the frozen-candidate campaign | §4 rollup (lines 99–118); §5 action list (lines 120–126) |

## Critical handling notes for Gordon

1. **Testability matrix is the scope-of-proof contract.** PROVABLE rows are verifiable read-only against the frozen hxs-15 corpus (source reads, presence/absence checks, static schema inspection, `--dump-config` without execution). BLOCKED-by-design rows require candidate mutation or execution — do not claim them; they are deferred by construction.
2. **Product 4 (Tier-1 smoke suite, 10c Part C) is labeled "install verification, NOT qualification."** Do not cite Part C probes as Gate 8–10 qualification evidence. Family 3 probes are `DEFERRED_BY_POLICY`, Family 4 probes are `ABSENT` by policy.
3. **Rollback drill (10c Part A) is design-only.** Execution is a separately-gated window with governor approval; nothing has touched hxs-15 to produce it. Plan Gate 9 against the design; execution awaits its own window.
4. **10b advisories are not a gate on the campaign.** They attach to the next intake, not to the frozen candidate (no runtime attack surface on hxs-15 per the dispositions).

## Integrity / provenance

- All three documents carry knowledge-review receipts (10 §367, 10b §128, 10c §152) and sanitized command logs.
- Products 1–4 were delivered under work orders 09a/20/21 (Morpheus, dsh lane).

## Handoff

- Routing complete. The governor issues Gordon's Gate 8–10 authoring work order separately; this packet is the reference bundle for it.
- No changes made to Gordon's lane or any test plan by this routing.
