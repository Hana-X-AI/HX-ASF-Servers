# WORK ORDER — Carol: catalog catch-up BATCH B (state-log freshness + registry)

- Issuer: Kimi-K3 (governor), 2026-08-29
- Executor: Carol (`agents/carol/`) — lane WATCH of record (agent-performance):
  claims require pasted validator output
- Class: **BACKGROUND — never blocks any work** (owner directive)
- Model lane (binding): `omniroute/gpt-oss-120b` (upstream AkashML, via
  OmniRoute). Session-start: minimal probe verifying the exact served id
  `openai/gpt-oss-120b`; fail closed, escalate, no substitution.

## Learned clauses (binding — from batch A's repair loops)

1. **CAT-01:** record ids are `DOC-<kebab-case>` — all lowercase. Precedent in
   your own directory: `DOC-kdd-0008-trinity-omniroute-adoption.yaml`.
2. **Run the check, paste the output.** No claim is accepted without the
   pasted `validate.py` result block. A completion claim that fails the
   governor's re-run is an accuracy defect of record.
3. Context budget: no whole-file reads of large files; line ranges + grep;
   index-navigated catalog; incremental writes. Your lane caps at 131,072.

## Read first (bounded)

1. Your batch A receipt `knowledge/catalog/receipts/2026-08-29-batchA-carol-kdds-registrations.md`
   (continuity), `knowledge/catalog/schema.yaml` (only if you lack a field).
2. `pilots/PILOT-DSH-IMPL-001/01-state-log.md` — ONLY rows 17–34 (use line
   ranges; the file is large).
3. `servers/SERVER-REGISTRY.md` — the open correction block (hxs-7
   decommission) and the Phase 1 count paragraph with its labeled bracket.
4. The two registry catalog records to update: `DOC-server-registry.yaml` and
   `DOC-tkv-server-registry.yaml` (read them, note their current
   freshness/status fields).

## Task — batch B records

1. **Pilot state-log freshness:** update the pilot's state-log catalog
   record(s) so rows 17–34 are covered at record level: the governance wave
   (model lanes KDD-0013 + amendments, rr batches, substrate retraction,
   Gordon's lane changes, freeze + Packet A acceptance, three-track GO,
   Carol's unfreeze + batch A accepted-with-notes). Relations to the KDD and
   agent records you added in batch A.
2. **Registry records:** update `DOC-server-registry.yaml` and
   `DOC-tkv-server-registry.yaml` to reflect the hxs-7 DECOMMISSION open
   correction (fleet active count 16; the registry row preserved as history;
   effective 2026-08-28). Freshness labels per schema.
3. **Closing receipt** `knowledge/catalog/receipts/2026-08-29-batchB-carol-statelog-registry.md`:
   records added/updated (ids), index hash before/after, conflicts (preserved
   + escalated), remainder for any batch C, AND the pasted `validate.py`
   result block (4/4 PASS required).

## Bounds

Allowlist writes only (`documents/`, `index.yaml`, `receipts/`). No secret
values. No host probes, no dispatch, no blocking. Conflicts queue to Kimi-K3
in the receipt. Close with `[BATCH B COMPLETE — EVIDENCE ATTACHED]` or
`[BATCH PAUSED — ESCALATION TO KK3]` with the reason.
