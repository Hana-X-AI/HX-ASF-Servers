# WORK ORDER — Mia: review-finding intake and fix routing (batch)

- Issuer: **Flash** (governor), 2026-08-29.
- Executor: **Mia** (Chief of Staff, KDD-0012).
- Lane: `omniroute/glm-5.3-flash` (GLM 5.3 Flash, Modal, via OmniRoute hxs-8).

## Intent

A review batch of 27 findings landed against 17 physical files in the
repository. [OPEN CORRECTION 2026-08-29, labeled, append-only — review
batch 2, F37: the original text read "11 files"; corrected to the actual
count of 17 physical files the findings span. Original preserved in the
work-order record of the batch.]
Per your charter (review-finding intake, owner directive 2026-08-28
state-log row 23): verify each finding against current state, separate
valid from stale or already-fixed, and route fixes to the owning lane
under a Flash-issued work order.

Some findings may already be fixed by corrections made earlier today
(plan Corrections 3/4/5, Mia work order 14, governor Step 2 execution).
Verify before routing — don't re-fix what's already done.

## The findings (27 total)

The findings cover these files:

1. `AGENTS.md` — 2 findings (KDD-0013 model-lane wording for kimi-k3 substrate; Carol frozen→background-class status)
2. `agents/README.md` — 2 findings (OD-14 scope count; governor transition qualifier)
3. `agents/mia/charter.md` + `agents/mia/profile.md` — 1 finding (add Chris to routing list)
4. `agents/trinity/profile.md` — 1 finding (route_verification schema for cloud lane)
5. `knowledge/HANDOFF-2026-08-29-governor-model-transition.md` — 1 finding (state-log row range)
6. `knowledge/agent-performance.md` — 1 finding (T0 eligibility for below-threshold rows)
7. `knowledge/catalog/receipts/2026-08-29-batchA-carol-kdds-registrations.md` — 1 finding (missing catalog record)
8. `knowledge/catalog/receipts/2026-08-29-batchB-carol-statelog-registry.md` — 1 finding (code fence language tag)
9. `knowledge/decisions/KDD-0013-agent-model-lanes.md` — 1 finding (Chris row formatting)
10. `knowledge/decisions/KDD-0014-chris-registration.md` — 2 findings (activation gate voided; D3 status conditional)
11. `pilots/PILOT-DSH-IMPL-001/07-kk3-work-order-gordon-gates-6-7-resume.md` — 1 finding (Qwen-X→DeepSeek lane reference)
12. `pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md` — 2 findings (work-order IDs; placeholder sections / stopped branch)
13. `pilots/PILOT-DSH-IMPL-001/13-mia-work-order-chris-hxs9-postgresql-install.md` — 1 finding (Rick predecessor supersession)
14. `pilots/PILOT-DSH-IMPL-001/gordon/phase-b/test_g7_surfaces.py` — 1 finding (replacement-character probe)
15. `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md` — 6 findings (noble main text; role creation in Step 1; rollback claim; plan status approval; pg_dumpall privileges; D1 apt guard)
16. `servers/hxs-9/2026-08-29-postgresql-install-step1.md` — 3 findings (pipe escaping in table; D1 reconciliation; PGDG fingerprint)

The full finding text is in the governor's session. Your job is NOT to
fix them all yourself — your job is to:
1. Read each referenced file at the cited lines
2. Verify whether the issue is still valid or already fixed
3. For valid findings you can fix within your lane (governance records, routing lists, catalog, docs): fix them
4. For valid findings in engineering lanes (gordon's test code, Chris's evidence doc, Morpheus's Phase C doc): characterize and report back to the governor for work-order issuance to the owning lane
5. Report back with a table: finding number, file, status (fixed/skipped/routed), reason

## Constraints

- Verify before writing — read the actual file at the cited lines.
- If a finding is already fixed by a prior correction, skip it with a brief note.
- All governance-record changes are append-only, labeled, dated, originals preserved.
- No lane mutation — you do not fix gordon's test code, Chris's evidence doc, or Morpheus's Phase C doc. You characterize and route.
- `scripts/validate.py` 4/4 after any repo write.
- Render any manifest-listed .md you change.
- No secret values in any artifact.
- Context budget: use line-range reads and grep, not whole-file dumps. Stop and receipt when the budget tightens.

## Authority

This work order. KDD-0012. AGENTS.md review-finding intake directive
(state-log row 23). The append-only governance-record convention.

## Evidence bar

- For each finding: pasted current-state evidence (the line(s) as they exist now), your disposition, and the fix if applied.
- `validate.py` output pasted at close.
- For routed findings: the characterization and recommended owning lane.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with the full disposition table.
`[TASK PAUSED — ESCALATION TO GOVERNOR]` with the named remainder if
anything blocks or the context budget is exhausted.
