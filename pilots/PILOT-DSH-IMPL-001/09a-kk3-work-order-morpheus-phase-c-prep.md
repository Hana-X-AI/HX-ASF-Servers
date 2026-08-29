# WORK ORDER — Morpheus: Phase C prep, PRODUCT 1 ONLY (write-first)

- Issuer: Flash (governor), 2026-08-29 — rescoped from work order 09 after
  the driver-lane failure of record (state-log row 34)
- Executor: Morpheus (dsh lifecycle steward, KDD-0009)
- Model lane (binding): `omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B,
  provider DeepInfra, via OmniRoute hxs-8) — owner-assigned 2026-08-29,
  CLI-verified live (served id `qwen/qwen3.8-2.4t-a95b`, `MORPHEUS_LANE_OK`).
  Supersedes Coder-X (two consecutive failures, state-log rows 34/40 — branch
  was STOPPED per KDD-0013; Q1 resolved by the lane change).
  Session-start: verify the served-model id fail-closed; stop and
  escalate on failure, no substitution.

**LANE CORRECTION (2026-08-29, labeled, append-only):** this order's
original model lane was `omniroute/coder-x` (hxs-2, digest `ec9ebe08…a9f1`).
Coder-X failed twice on this work order (read-loop + confabulated paths,
state-log rows 34/40). The owner changed Morpheus's lane to Qwen 3.8 2.4T
A95B via DeepInfra on 2026-08-29. The Coder-X lane reference is preserved
as history above; the binding lane is now `omniroute/qwen3.8-2.4t-a95b`.
Q1 of record (state-log row 40: O1/O2/O3) is CLOSED — the lane change
supersedes all three options.

## WRITE-FIRST DISCIPLINE (binding — this is the failure fix)

Your lane caps at 65,536 tokens. Your predecessor session read-looped until
the ceiling and died with nothing written. [OPEN CORRECTION 2026-08-29,
labeled, append-only, review batch 2 F18: the 65,536 cap figure above was
written for the original Coder-X lane and is HISTORICAL — the current lane,
`omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B), caps at 131K output
tokens per the OmniRoute route of record. The write-first discipline below
stands unchanged.] So this order INVERTS the flow:

1. **Write the skeleton FIRST** — create
   `pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md` with all section
   headings and per-family placeholder rows BEFORE any corpus reading. The
   skeleton comes from this work order and your own records, which you already
   know (you are the author of 03 and 05).
2. **Targeted reads only** — at most 2–3 corpus files per family, and only to
   fill a specific placeholder. Never broad surveys, never whole lockfile
   reads, never re-reads.
3. **Incremental writes** — save the document after each family is filled.
   If the context tightens: stop reading and close per the completion gates
   below. [Corrected 2026-08-29, labeled: this clause originally read "A
   partial document with a completion marker BEATS a dead session with none" —
   that invited false completes; the gates below now govern, original wording
   preserved here.]

## HARD BOUNDARY (unchanged, absolute)

NO candidate mutation of any kind on hxs-15 — Gordon's campaign is running
against the frozen candidate. No hxs-15 contact at all this session. Any
read-only status need goes through the governor.

## Product — Phase C preparation (the doc above)

Per Phase C family (Gates 8–10 scope per the plan: interop, sandboxing,
remote + experimental, platform proof), one table row:

- source seam (file:line in the pinned corpus `/opt/tkv-local/deepseek-harness-master`),
- activation mechanism on the native composition layer (cordis.patch.yml class,
  per your Phase A/B pattern),
- host prerequisites,
- risk class,
- **testability note for Gordon's Gate 8–10 authoring**: what is provable,
  what is BLOCKED-by-design and why.

End the doc with: risks/open items, your knowledge-review receipt (emitted
first in your working order but recorded in the doc), and a sanitized command
log. R1 analysis and the rollback/Tier-1 designs are OUT of this order —
separate sessions (09b/09c) on your evidence.

## Repo rules

`python3 scripts/validate.py` from the repo root must end 4/4 PASS after your
writes; paste the result block. No credential-shaped literals. Your Phase A/B
records are not touched by this order.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with the doc path and section list —
reserved for a document containing ALL required sections (every Phase C
family row, risks/open items, knowledge-review receipt, command log) and the
pasted validate.py result. Incomplete work ends with
`[TASK PAUSED — ESCALATION TO KK3]` and the remainder NAMED — never with a
completion marker on partial content. [Corrected 2026-08-29, labeled: this
section originally allowed "a clean partial close … is an acceptable outcome"
under the completion marker — superseded by the gates above, original wording
preserved here.] Append-only, labeled corrections remain mandatory for all
governance records.
