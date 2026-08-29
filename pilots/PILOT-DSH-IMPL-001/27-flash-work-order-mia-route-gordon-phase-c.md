# WORK ORDER — Mia: route Morpheus Phase C prep results to Gordon for Gate 8-10 authoring

- Issuer: Flash (governor), 2026-08-29.
- Executor: Mia (Chief of Staff, KDD-0012).
- Lane: `omniroute/glm-5.3-flash` (GLM 5.3 Flash, Modal, via OmniRoute hxs-8).

## Intent

Morpheus's Phase C prep is complete — all four products delivered. Route
the testability matrix and product references to Gordon for his Gate 8-10
test plan authoring. This is coordination and routing only — you do not
write test plans or mutate Gordon's lane.

## What to route

Morpheus produced four documents:

1. **Product 1 — Phase C prep** (`pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md`):
   - 4 families (interop, sandbox, remote, experimental) with source seams
   - **Testability matrix** (16 rows) — this is what Gordon needs for Gate 8-10 authoring
   - Open risks, knowledge-review receipt

2. **Product 2 — R1 advisory analysis** (`pilots/PILOT-DSH-IMPL-001/10b-morpheus-r1-advisory-analysis.md`):
   - 38 advisories classified (33 resolved, 5 needs-upstream)
   - Informational for Gordon — not blocking

3. **Product 3 — Rollback/ops design** (`pilots/PILOT-DSH-IMPL-001/10c-morpheus-rollback-ops-design.md`):
   - Full rollback drill design (7 steps, hash-anchored)
   - Upgrade runbook (S0-S7)
   - Gordon needs this for Gate 9 execution when the campaign reaches that gate

4. **Product 4 — Tier-1 smoke suite** (in 10c, Part C):
   - Per-family probes labeled "install verification, NOT qualification"
   - Gordon should NOT confuse these with his gate claims

## What Gordon needs

- The **testability matrix** from Product 1 (§Testability matrix) — it tells
  him what is provable read-only on the frozen candidate and what is
  BLOCKED-by-design for each Gate 8-10 family.
- The **rollback/ops design** from Product 3 — for Gate 9 execution planning.
- The **R1 advisory analysis** from Product 2 — informational context.

## Your task

1. Read the three documents (targeted reads — testability matrix section,
   rollback design summary, R1 rollup).
2. Produce a routing packet for Gordon: a brief summary of what each
   document contains, what Gordon should use it for, and the exact file
   paths + section references.
3. Write the routing packet to `pilots/PILOT-DSH-IMPL-001/27-mia-routing-gordon-phase-c-prep.md`.
4. Do NOT write or modify Gordon's test plan — that's his lane.
5. Run `python3 scripts/validate.py` 4/4 PASS.
6. Report back to the governor with the routing packet reference.

## Constraints

- Coordination and routing only — you do not write test plans or mutate
  Gordon's lane.
- The governor will issue a separate work order to Gordon for Gate 8-10
  authoring once your routing packet is delivered.
- `scripts/validate.py` 4/4 after writes.
- No secret values.
- Context budget: targeted reads, not whole-file dumps.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with the routing packet file path
and validate.py output.
