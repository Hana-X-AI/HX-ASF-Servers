# Carol — T-standard receipt: M5 deliverable + CI/CD wave

```text
[CATALOG RECEIPT]
Run: 2026-08-26T2026Z Agent: Carol Trigger: Kimi-K3 governor brief — Coder-X M5
deliverable wave (T-standard): M5 deliverable landing (hxs-2 state log row 31),
state-log advances, p8 CI/CD documents (row 33), OmniRoute F1 disposition (row 32)
```

- Tier: **T-standard** (governor-named at dispatch): write set + full-catalog
  self-check + one `scripts/validate.py` at close.
- Carry-forward window: **clean** — cited per receipt
  `2026-08-26T1957Z-carol-tmicro-omniroute-reingest.md` (validate.py 4/4 PASS,
  window un-poisoned at hxs-2 row 32). No FAIL since; window holds.
- Provenance: hxs-2 state log rows **31** (M5 COMPLETE — PASS, handoff OPEN
  pending this receipt), **32** (OmniRoute F1/F2 dispositions, validate.py 4/4),
  **33** (p8 CI/CD live, two owner-pending items); hxs-3 state log row **17**
  (Meta-X M5 BLOCKED — hxs-3 LAN loss, owner check requested).

## Added (4 records)

- **DOC-pilot-hxs2-ev-16-esme-m5-validation** — `16-esme-m5-validation.md`,
  Esme M5 functional validation on Coder-X. type evidence, authority
  agent-evidence, status adopted. sha256
  `351e25edf3cfc73a1eb3ce45c8ec4bc1bda5aa5b811bf1abd12d52f9efd14cbc`.
  Content per the governor-verified deliverable: **AC-013 coding PASS 10/10 =
  100%** vs the ratified ≥90% specialist bar (versioned v1.0.0 set) with
  mandatory evaluator review — every solution read in full, concur 10/10, zero
  gaming; **AC-012 tool protocol PASS** — 0 forbidden/malformed executed of 51
  audit events (100% denied rule) + **100% schema conformance of 29 recorded
  decisions** (bar ≥95%), duplicate mutation exactly once, loop terminates,
  EF04 raw-False corrected by evaluator judgment (hxs-1 M5b class, disclosed,
  no re-run); **AC-009 API readiness PASS**; **vision probes evidence-only** (4
  deterministic stdlib PNGs, sha256-recorded; V1/V2 exact, V3 `HK52`, V4
  `65482`) labeled RECORD for the owner's deferred D8-vision decision;
  **F-M5-1** residency eviction of the Forever pin under
  `OLLAMA_MAX_LOADED_MODELS=1` by interactive bare-alias use — explained (zero
  ERROR/Xid/OOM), restored via the frozen preload path in 17 s, monitor
  recommendation (`/api/ps` name+digest monitor with auto re-pin + alias
  discipline) routed to M8/owner; identity guard at close EXACT
  (`ec9ebe08a824…`, size == size_vram 17,815,411,094, ctx 65536, Forever);
  zero NEW Xid (all-boots stays 1 = F-M6-0).
- **DOC-ci-cd-workflow** — `.github/workflows/ci-cd.yml`, p8 pipeline
  definition (owner-ratified 2026-08-26). type **contract** (schema judgment —
  see Typing below), authority ratified-governance, status active. sha256
  `9dbe6070ac81706b2b0c8596f7cbe67ac6c64dd9491c904ad6fcbc1b09c7eafc`.
- **DOC-coderabbit-config** — `.coderabbit.yaml`, CodeRabbit review
  configuration, keys verified against the live official schema.v2. type
  **contract** (review-policy configuration), ratified-governance, active.
  sha256 `c958d82cd483eec56055d37fe6325c4b9ca2bd4577a474da4c09981e36c26297`.
- **DOC-cicd-pipeline-doc** — `docs/cicd-pipeline.md`, human-facing pipeline
  doc. type **runbook**, ratified-governance, active. sha256
  `6b99bae481a2655906c20737eaa3928bc9b66839ca4d12bfcba265f59673434c`.
  Dual-format convention: ONE record for the Markdown source of truth; the
  rendered sibling `docs/cicd-pipeline.html` exists (render.py-managed,
  manifest line 42) and is not separately cataloged.

## Updated (5 records)

- **DOC-pilot-hxs2-wo-14-john-m5** — IN-EXECUTION → **DISCHARGED**: status
  active → adopted; title de-commissioned (M5 COMPLETE PASS, row 31);
  **governs edge added** → DOC-pilot-hxs2-ev-16-esme-m5-validation (the edge
  deferred at the in-execution cataloging, per the M7-pair convention);
  review_due → discharged-contract; notes.status_convention records the flip.
  Source unchanged — sha256 `03dd3d4f…` re-verified against the live artifact.
- **DOC-pilot-hxs2-cp-15-john-m5** — same flip with the paired WO: adopted,
  governs edge added → ev-16, discharged-contract review_due. Source unchanged
  — sha256 `c5642d1a…` re-verified.
- **DOC-pilot-hxs2-state-log** — advanced to rows **1–33** (living-document
  drift rule): sha256 `ba0db561…` →
  `c3bc1502f00896fb1a806ef248e28768ea5b47e7029298e27c4b2d83f185f40d`; title,
  version, describes target + note (rows 30–33 summarized), and the
  notes.living_document hash chain extended (`→ c3bc1502… (rows 1–33,
  2026-08-26T20:08Z)`).
- **DOC-pilot-hxs3-state-log** — advanced to rows **1–17**: sha256
  `1f57374d…` →
  `11b3dd75fff447f7a6fb187d9f2c2bd5e0ce207ba6486c4264a02c3e17b384b0`; row 17
  summarized (M5 BLOCKED — hxs-3 lost on LAN mid-session; frozen-state
  re-proof mandatory before any resume; **the Meta-X M5 WO/CP stay
  in-execution — no deliverable exists to catalog at this wave**).
- **DOC-tkv-corpus-omniroute** — `notes.reorg_history` appended with the **F1
  disposition** (governor, hxs-2 row 32): the surviving v3.8.50 tree at
  `/opt/tkv-local/OmniRoute_old/.OmniRoute-release-v3.8.50-replacement-backup`
  (identity-confirmed by receipt 2026-08-26T1957Z — names-only manifest
  reproduces the prior digest `1fdb6f36…` exactly) is **left in place as the
  owner's safety copy, NOT separately cataloged**; existence + identity proof
  recorded in the note only. F2 (nested v3.8.51 duplicate, manifest-identical)
  noted, not cataloged. Record sha256/canonical_location unchanged (v3.8.51
  tree untouched; notes-only edit), validated_at bumped.

## Linked (relations)

- wo-14 —governs→ ev-16; cp-15 —governs→ ev-16 (M7-pair deferred edges,
  added at this landing).
- ev-16: evidences M5 COMPLETE (row 31); produced_by john; references
  hx1-ev-16 (execution precedent), hx1-ev-19 (EF04/evaluator standard),
  hxs2-ev-07 (frozen identity), hxs2-ev-08-ladder (operating profile),
  hxs2-ev-08-xid31 (armed watch), DOC-backend-coder-x (quality record behind
  candidate status); depends_on fixtures manifest; risks F-M5-1, F-M5-4,
  F-M5-2.
- ci-cd-workflow: references cicd-pipeline-doc + coderabbit-config;
  depends_on DOC-scripts-validate-py, DOC-scripts-wiki-dual-format-render,
  fixtures manifest; governs the repo change flow; produced_by kimi-k3.
- coderabbit-config: configures the CodeRabbit CLI review (+ future App);
  references the upstream schema.v2 URL (noted, not cataloged).
- cicd-pipeline-doc: describes ci-cd-workflow; references coderabbit-config.

## Typing (schema judgment, per the brief's contract/config class)

- `ci-cd.yml` → **contract**: the ratified, machine-enforced quality-gate
  contract binding how changes enter the repo (DOC-blueprint-llm-server
  class), not a how-to.
- `.coderabbit.yaml` → **contract**: the normative review-policy half of the
  gate (path_instructions restate standing repo rules as enforced criteria).
- `cicd-pipeline.md` → **runbook**: the human operator surface (setup,
  lifecycle, deviations D1–D4) — the validate.py/render.py tooling precedent.
- Judgment recorded in each record's `notes.typing_judgment`.

## Flagged (informational — no contradictions)

- **F-wave-1 (owner-pending, from row 33):** CI green + smoke merge await the
  owner's decision on the Alert-2 uncommitted-tree commit wave (5
  wiki-manifest docs exist only in that tree); `CODERABBIT_API_KEY` web-UI
  secret add is the owner's action — the review leg skips cleanly by design
  until then. Recorded in DOC-ci-cd-workflow `notes.pending_items`.
- **F-wave-2 (hxs-3, from row 17):** Meta-X M5 BLOCKED on the hxs-3 LAN loss;
  owner physical/IPMI check requested. hxs-3 M5 WO/CP records unchanged
  (in-execution). If the host rebooted, frozen-state re-proof is mandatory
  before suites resume.
- **F-wave-3 (evidence routing):** F-M5-1 monitor recommendation
  (`/api/ps` name+digest + auto re-pin; interactive alias discipline) is
  routed to M8/owner via the deliverable and the ev-16 risks edges — no
  catalog action beyond recording.
- Secret boundary: no secret values in any new/updated record; the CI/CD
  documents name secrets only as mechanisms (CODERABBIT_API_KEY, GITHUB_TOKEN,
  PAT note) — profile §6 honored. validate.py secret-boundary: 535 files, 0
  hits.

## Rejected

- None. Every wave item cataloged; the two non-cataloged OmniRoute trees
  (v3.8.50 backup, nested v3.8.51 duplicate) carry explicit governor
  dispositions recorded in DOC-tkv-corpus-omniroute notes (not rejections —
  deliberate non-cataloging with provenance).

## Freshness

- wo-14/cp-15: current (discharged contracts, adopted).
- Both state-log records: current at rows 1–33 / 1–17 (living logs; re-hash on
  every re-ingestion).
- All four new records: current.

## Verification (T-standard scope)

- **Write set (9 records):** all parse; required fields + source.section
  present; 8 file-backed sha256 values re-verified against the live artifacts
  (ev-16 `351e25ed…`, workflow `9dbe6070…`, config `c958d82c…`, doc
  `6b99bae4…`, wo-14 `03dd3d4f…`, cp-15 `c5642d1a…`, hxs-2 log `c3bc1502…`,
  hxs-3 log `11b3dd75…`); the corpus record's canonical directory exists with
  digest unchanged (notes-only edit). All write-set relation targets resolve;
  governs edges and flips spot-checked.
- **Full-catalog self-check:** 239/239 records parse; index 1:1 id sets exact;
  956 structured line-field values exact; header document_count 239, updated
  stamp 2026-08-26T2026Z; zero dangling DOC-id relation targets catalog-wide.
- **validate.py at close:** **PASS — 4/4 checks (exit 0)**: wiki-sync 38/38 in
  sync (incl. docs/cicd-pipeline.md), fixture-suite 57 tests OK + sha256sums
  10/10, catalog-mechanical 239 records (CAT-01/03/04/07/08 green; 238
  locations resolve + 1 protected-resource exempt), secret-boundary 0 hits.
  4 manual gates noted (governor-owned, incl. CB-01 write-set audit).

## Follow-ups

- The **Coder-X M5 handoff CLOSES when the governor cites this receipt in the
  hxs-2 state log** (profile §7; row 31's handoff-OPEN clause).
- CODERABBIT_API_KEY activation + Alert-2 commit wave: owner actions (row 33);
  re-ingest the workflow/doc records if the pipeline text changes.
- hxs-3 M5: on access return, john resumes from tool-protocol after
  frozen-state re-proof (row 17); the deliverable cataloging follows at its
  landing.
- Corpus manifest re-hash due 2026-09-24 (standing from the 1957Z run).

## Index

- updated (sha256
  `ff282a6c179066e803209866f5984ce2ab3780178bda0af6b46f9a3abe5ff31d`);
  4 entries added (alphabetical placement), 4 lines updated (wo-14/cp-15
  titles, both state-log row windows), header bumped; document_count
  **235 → 239**.

No git commit (owner gate). Originals untouched — all hashing read-only;
catalog writes scoped to the allowlist (`documents/`, `index.yaml`,
`receipts/`).

```text
[INGEST/QUERY COMPLETE — RECEIPT ATTACHED]
PASS — CATALOG CURRENT
```
