# WORK ORDER — Carol: catalog catch-up BATCH A (KDDs + agent registrations)

- Issuer: Kimi-K3 (governor), 2026-08-29
- Executor: Carol (`agents/carol/`)
- Class: **BACKGROUND — never blocks any work** (owner directive)
- Model lane (binding): `omniroute/gpt-oss-120b` (upstream AkashML, via
  OmniRoute). Session-start: minimal probe verifying the exact served id
  `openai/gpt-oss-120b`; fail closed, escalate, no substitution.

## CONTEXT BUDGET (binding — read this first)

Your lane caps at 131,072 tokens of context. Your predecessor session on this
task DIED at the ceiling after corpus-wide reads (103k of tool output). So:
- NEVER whole-file-read large files. Use line ranges (`Read` with
  offset/limit) and `Grep` to land on what you need.
- The catalog is navigated through `knowledge/catalog/index.yaml` and targeted
  reads of at most 2–3 example records — not a corpus sweep.
- Read `knowledge/catalog/schema.yaml` ONCE, then write records incrementally;
  do not re-read files you already have.
- If you estimate you are running out of room: stop reading, finish the
  records for what you have, note the remainder in your receipt.

## Read first (bounded)

1. `agents/carol/profile.md` §§catalog contract (your allowlist, provenance,
   conflict rules) — skip the rest.
2. `knowledge/catalog/schema.yaml` + at most 2 example records from
   `knowledge/catalog/documents/` (pick KDD records, e.g. DOC-kdd-0008*).
3. The seven source files for THIS batch only:
   - `knowledge/decisions/KDD-0011-rob-registration.md`
   - `knowledge/decisions/KDD-0012-mia-chief-of-staff.md`
   - `knowledge/decisions/KDD-0013-agent-model-lanes.md`
   - `agents/mia/charter.md`, `agents/mia/profile.md`
   - `agents/rob/charter.md`, `agents/rob/profile.md`

## Task — batch A records

1. One catalog document record each for **KDD-0011**, **KDD-0012**, **KDD-0013**
   (KDD-0013's record notes amendments 1–5 exist; you do not need to enumerate
   their full text — the KDD is the source).
2. Document records for the four agent registration files (`agents/mia/` ×2,
   `agents/rob/` ×2), with roster relations; Rob's record carries his source
   pointer (content sha256 `6ede0b05…f9e3` per KDD-0011).
3. Index update per your contract (id pattern, titles, structured fields exact).
4. A short batch receipt in `knowledge/catalog/receipts/` named
   `2026-08-29-batchA-carol-kdds-registrations.md`: records added (ids), index
   hash before/after, conflicts found (preserved + escalated, never resolved),
   remainder notes for batch B/C.

## Bounds

Allowlist writes only (`documents/`, `index.yaml`, `receipts/`). No secret
values (existence/owner/retrieval mechanism only). No host probes, no sub-agent
dispatch, no blocking of any lane. Questions queue to Kimi-K3 in the receipt.

## Validation + close

`python3 scripts/validate.py` from the repo root must end 4/4 PASS after your
writes. Close with the batch receipt + `[BATCH A COMPLETE — EVIDENCE ATTACHED]`,
or `[BATCH PAUSED — ESCALATION TO KK3]` with the reason.
