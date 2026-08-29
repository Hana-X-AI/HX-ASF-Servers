# WORK ORDER — Morpheus: Products 2+3+4 (R1 analysis + rollback/ops + Tier-1)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Morpheus (dsh lifecycle steward, KDD-0009).
- Lane: `omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B, provider DeepInfra, via OmniRoute hxs-8).
- Product 1 (Phase C prep) is COMPLETE and governor-accepted.

## Intent

Three off-candidate documents, all read-only analysis against the pinned
corpus `/opt/tkv-local/deepseek-harness-master`. No hxs-15 contact.
No candidate mutation.

## Product 2 — R1 advisory-debt intake analysis (09b)

38 pinned-snapshot advisories from Phase A (row 7: 15H/20M/3L). For each:
- Map to its fixed upstream version (if one exists)
- Check compatibility against the pinned lockfile's constraints (OFFLINE — no lockfile rewrite, no install)
- Classify: resolved-by-next-intake / needs-upstream-action / accepted-risk-with-rationale

Write to: `pilots/PILOT-DSH-IMPL-001/10b-morpheus-r1-advisory-analysis.md`

## Product 3 — Rollback/operations design (09c)

Gate 9 rollback exercise the arc owes (Phase A signed with "rollback NOT exercised").
- Full rollback drill design from current Phase B state to pre-Phase-B checkpoint
- Modeled on trinity's OmniRoute gate battery (parity + restart + reboot + restore + rollback + hygiene)
- Upgrade-path runbook for the next dsh intake (reversible, hash-anchored, inverse per step)

Write to: `pilots/PILOT-DSH-IMPL-001/10c-morpheus-rollback-ops-design.md`

## Product 4 — Tier-1 during-install smoke suite (09c)

Per-family bounded entry-path probe for Phase C installs. For each family
from Product 1: a bounded entry-path probe (minutes, deterministic-first),
labeled "install verification, NOT qualification". Must NOT restate
Gordon's gate claims. Format: table per family — probe, oracle, expected receipt.

Write to: same doc as Product 3 (§Tier-1 section) or a separate section.

## Discipline

- Write-first + incremental writes: create each doc skeleton first, fill targeted sections after.
- Targeted reads only: at most 2-3 corpus files per section. Never broad surveys.
- 131K context on this lane — more headroom, but don't waste it.
- If context tightens: stop, close per the completion gates, name the remainder.

## Hard boundary (unchanged, absolute)

NO candidate mutation of any kind on hxs-15. No hxs-15 contact at all.

## Constraints

- Read-only against `/opt/tkv-local/deepseek-harness-master`.
- Only write to the three doc files listed above.
- `python3 scripts/validate.py` 4/4 after writes.
- No credential-shaped literals. Append-only for governance records.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` only when ALL three products are
written with all sections filled AND validate.py 4/4 PASS is pasted.
`[TASK PAUSED — ESCALATION TO GOVERNOR]` with the named remainder otherwise.
