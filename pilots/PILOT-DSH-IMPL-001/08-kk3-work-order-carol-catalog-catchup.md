# WORK ORDER — Carol: catalog catch-up (background-class)

- Issuer: Kimi-K3 (governor), 2026-08-29 — pilot state-log rows 17–30 window
- Executor: Carol (documentation and knowledge steward; `agents/carol/`)
- Class: **BACKGROUND — never blocks any work** (owner directive 2026-08-29:
  "you can run carol but not on the critical path, she can run in the
  background but does not block any work")
- Model lane (binding): `omniroute/gpt-oss-120b`
  (`openrouter/openai/gpt-oss-120b`, upstream AkashML, via OmniRoute hxs-8) —
  owner-assigned 2026-08-28, KDD-0013 amendment 4. Session-start: verify the
  exact served-model id with a minimal probe; fail closed on mismatch or an
  unhealthy endpoint, escalate to Kimi-K3, no substitution.

## Read first (mandatory)

1. `agents/carol/profile.md` and `agents/carol/charter.md` — your contract:
   writes scoped to the catalog allowlist (`knowledge/catalog/documents/`,
   `index.yaml`, `receipts/`, `retrieval-packages/`; schema, tests, README
   read-only); provenance to source document and section mandatory; conflicts
   preserved and escalated, never guess-resolved; no secret values (existence,
   owner, retrieval mechanism only); no sub-agent dispatch; no host probes.
2. `knowledge/catalog/` — schema.yaml, existing records, receipts: match the
   established forms exactly (id patterns, field names, truth-state labels).
3. `scripts/validate.py` output contract — the catalog-mechanical gate
   (schema/required/enums/source.section, index 1:1, relations resolve,
   CAT-07/CAT-08) must stay green after your writes.

## Task — catch up the frozen window (2026-08-28)

While you were frozen the factory produced a governance wave. Catalog it, with
receipts, per your standing contract:

1. **KDD-0011** (Rob registration), **KDD-0012** (Mia, Chief of Staff),
   **KDD-0013** (per-agent model lanes) including amendments 1–5 — one catalog
   document record each, relations to the agents they govern and to OD-14.
2. **Agent registrations**: `agents/mia/` (charter + profile) and
   `agents/rob/` (charter + profile) — document records + roster relation;
   Rob's source profile pointer (content sha256 `6ede0b05…f9e3`, KDD-0011).
3. **DSH pilot state log rows 17–30** (`pilots/PILOT-DSH-IMPL-001/01-state-log.md`)
   — the wave: model lanes ratified, rr batches, substrate retraction, Gordon's
   lane changes, freeze/Packet A acceptance, your own unfreeze. Update the
   pilot's state-log record(s) and relations accordingly.
4. **hxs-7 decommission** — `servers/SERVER-REGISTRY.md` open correction of
   record; fleet-standard.yaml count note; fleet active count 16.
5. **Lane changes of the window**: Gordon Qwen-X → DeepSeek V4 Pro
   (StreamLake); Trinity/Rob/Mia GLM 5.3 Flash (Modal); Carol Chat-X →
   gpt-oss-120b (AkashML) — reflect amendment 3/4 identities and the FIVE-lane
   OD-14 metering scope.
6. **Closing receipt** in `receipts/`: what was ingested, records added/updated
   (ids + index hash), conflicts found (preserved, escalated — never resolved
   by guessing), anything you could not verify.

## Background-class rules (binding)

- You do not interrupt, hold, or block any lane. No gate or handoff waits on
  your output; the pilot state log stays authoritative until your receipts land.
- Questions, conflicts, and ambiguities queue to Kimi-K3 IN YOUR RECEIPT —
  never to the owner directly, never to another lane.
- If a source contradicts itself, preserve both, authority-rank, escalate.

## Validation + close

`python3 scripts/validate.py` from the repo root must end **4/4 PASS** after
your writes (catalog-mechanical included). Close with your standard catalog
receipt plus `[TASK COMPLETE — EVIDENCE ATTACHED]`, or
`[TASK PAUSED — ESCALATION TO KK3]` with the reason.
