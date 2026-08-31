# Carol receipt — PR #8 three-finding corrective action

- Wave: pr8-three-finding-corrective-action
- Window: 2026-08-31T04:25:46Z
- Starting commit: `efadc93accb7585ceebe94fcc206a0bd4458fb9f`
- Result: LOCAL GATES PASS; HOSTED CODERABBIT REVIEW PENDING

## Corrections

1. `DOC-pilot-dsh-impl-001-state-log` now uses
   `source.section: §whole-document`. Rows 17–34 remain only as historical
   ingestion provenance; the current title, purpose, version, relation, and notes
   continue to describe rows 1–47.
2. `DOC-kdd-0018-raphael-registration` now separates Raphael's current agent
   execution lane, Z.ai GLM 5.2 free via OmniRoute under KDD-0013 Amendment 11,
   from LightRAG's current application LLM binding, local Chat-X on hxs-4.
   Qwen-X via OmniRoute remains historical agent-lane provenance; Meta-X via
   OmniRoute remains historical application-binding provenance. Qdrant remains
   installed but pending acceptance for Raphael activation.
3. The immutable `2026-08-31T0112Z-carol-sy8-baseline-reconciliation.md`
   receipt was restored exactly to its pre-`efadc93` state. The later 03:54:33Z
   local 21-finding reconciliation and the subsequent hosted three-major result
   now live in `2026-08-31T0354Z-carol-pr8-coderabbit-followup.md`.

## Mechanical catalog actions

- Re-minted only `DOC-pilot-dsh-impl-001-state-log` and
  `DOC-kdd-0018-raphael-registration` with `carol-mint 1.0.0`. Their source
  hashes were unchanged because this action corrected catalog semantics and
  provenance rather than source documents.
- Rebuilt `knowledge/catalog/index.yaml` with `carol-mint 1.0.0`: 344 records,
  all 344 existing titles preserved.
- Receipt files were not added to the document index; no separate receipt index
  exists.

## Local validation

- `git diff --check`: PASS.
- `python3 scripts/test_catalog_freshness.py`: PASS, 9/9 tests.
- `python3 scripts/validate.py --ci`: PASS, 5/5 checks.
- SY-8: 344 records, zero in-repo drift, zero missing in-repo sources, and zero
  baseline debt.
- Catalog mechanical validation: 344 records, index 1:1, structured fields exact,
  and all relations resolved.
- `carol-mint gate --ids DOC-pilot-dsh-impl-001-state-log,DOC-kdd-0018-raphael-registration`:
  PASS, two records checked.

## Hosted and manual gates

- Hosted CodeRabbit review: PENDING for the corrective commit produced by this
  action. This receipt does not claim hosted acceptance.
- Protected literal-credential sweep: NOT RUN. The protected ssh-info resource
  was not read. The generic repository secret-boundary scan passed with zero
  findings across 1,391 files.
- CB-01 write set: the two authorized catalog records, the rebuilt document
  index, the exact `0112Z` restoration, and the two event-specific receipts.

## Second-brain disposition

- Opportunity identified: preserve an unambiguous distinction between agent
  execution lanes, application model bindings, source extent, and receipt event
  boundaries.
- Pattern: authority-ranked catalog semantics, historical provenance retained in
  labeled fields, deterministic re-minting, and one immutable receipt per event
  window.
- Disposition: IMPLEMENTED for this corrective action; hosted acceptance remains
  pending.
