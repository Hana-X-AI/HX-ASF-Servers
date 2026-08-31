# Carol receipt - PR #8 systemic history corrective action

- Wave: pr8-systemic-history-corrective-action
- Window: 2026-08-31T04:54:58Z
- Starting commit: `709ea26890aded24ce13b65b1edf1208b5d6d6f7`
- Result: LOCAL GATES PASS; HOSTED REVIEW PENDING

## Finding dispositions

1. ACCEPTED - the freshness-history defect was systemic. Seventeen records had
   a freshness-only `notes.minted_by` event without an exact current-SHA,
   timestamp, and reason match in `document.hash_history`. Each missing event
   was appended once using its existing mint evidence. Existing events and
   ordering were preserved.
2. ACCEPTED - `DOC-kdd-0013-agent-model-lanes` now includes `bailey`
   immediately before `gordon`, matching KDD-0013 Amendments 11-12.
3. ACCEPTED - `DOC-knowledge-agent-performance` now identifies James as the
   current governor maintainer and Agent Zero as ratifier. A note preserves
   Kimi-K3 as the historical governor who seeded and maintained the earlier
   ledger; existing source attribution and reconciliation evidence remain.
4. ACCEPTED - `DOC-pilot-omniroute-19-kimi-code-provider-setup` now identifies
   James as the current governor maintainer. `source.author` remains Kimi-K3
   (governor), and existing history, provenance, and audit evidence remain.
5. ACCEPTED - `catalog_freshness.baseline()` now requires the YAML top level to
   be a `collections.abc.Mapping` before field access. Null, list, and scalar
   roots return a controlled `[CF-05]` problem.
6. ACCEPTED - `tracked_repo_sources()` now raises a contextual unreadable-record
   failure instead of silently omitting it. `validate.scoped_checks()` therefore
   selects the governance/SY-8 path; the separate import-failure regression is
   retained.
7. ACCEPTED AND ALREADY PRESENT AT START - the `0425Z` receipt chronology
   clarification was complete in starting commit `709ea268`. This cycle verified
   that receipt as unchanged and did not repeat or rewrite the correction.

## Rejected finding

- REJECTED - no edit was made to
  `2026-08-31T0112Z-carol-sy8-baseline-reconciliation.md`.
- Evidence: `DOC-backend-qwen-x` is already enclosed in backticks and contains
  hyphens, not underscores. The visible underscore is in the later truncated
  title fragment `Q4_`, not the cited identifier.
- The receipt remains byte-identical with SHA-256
  `653710f9fe6c864bf236003a39be317f46683eba691873d9138cefa1af374cc6`.

## Systemic history repair

The 17 corrected records are:

- `DOC-ci-cd-workflow`
- `DOC-goal-fleet-baseline-deployment`
- `DOC-goal-hxs2-qwen36-coderx-backend`
- `DOC-goal-lightrag-hxs4`
- `DOC-goal-omniroute-layer1-secure-core`
- `DOC-hxs3-configuration`
- `DOC-kdd-0013-agent-model-lanes`
- `DOC-kdd-0018-raphael-registration`
- `DOC-knowledge-agent-performance`
- `DOC-knowledge-issues`
- `DOC-knowledge-network`
- `DOC-pilot-dsh-impl-001-state-log`
- `DOC-pilot-hx1-state-log`
- `DOC-pilot-hxs3-ev-12-esme-m5-validation`
- `DOC-pilot-omniroute-19-kimi-code-provider-setup`
- `DOC-pilot-omniroute-control-manifest`
- `DOC-server-registry`

Post-repair audit: 17 freshness-only mint candidates; zero candidates lacking
their exact current-SHA, timestamp, and reason history event. For all 17,
`document.sha256`, `validation.validated_at`, and `notes.minted_by` are unchanged
from the starting commit.

## Root cause and regression coverage

- `scripts/catalog/carol-mint` previously called `append_hash_history()` only
  when the source SHA changed and deduplicated list events by SHA alone. Prose
  history used the same SHA-only behavior through a short-hash substring check.
- A re-mint now captures one timestamp for validation, history, and mint
  evidence; every actual re-mint records a history event, including same-hash
  freshness changes.
- List and prose histories deduplicate only an identical SHA, timestamp, and
  reason event. List-form predecessor detection remains hash-based.
- Fixture coverage now proves same-hash freshness recording and exact-event
  idempotence for both list and prose forms.

## Catalog mechanics

- No metadata-only correction was passed through `carol-mint re-mint`; no new
  timestamps or source hashes were generated.
- The index was rebuilt in an isolated catalog from all current records and
  compared without its generated `updated` field. Structured content matched
  exactly: 344 records. No index change was retained.
- Targeted `carol-mint gate` result: PASS for all 17 changed catalog records.

## Local validation

- `git diff --check`: PASS.
- `python3 scripts/test_catalog_freshness.py`: PASS, 11/11 tests.
- `bash scripts/catalog/test-carol-mint.sh`: PASS, 17/17 checks.
- `python3 scripts/catalog_freshness.py --json`: PASS; 344 records, zero
  in-repo drift, zero missing in-repo sources, zero baseline debt, no problems.
- `python3 scripts/validate.py --ci`: PASS, 5/5 checks.
- Catalog mechanical validation: 344 records, index 1:1, structured fields
  exact, and all relations resolved.
- Exact freshness-history audit: 17 candidates, zero missing exact events.
- Immutable `0112Z` receipt SHA-256: PASS.

## Security and write set

- Protected literal-credential sweep: NOT RUN. The protected ssh-info resource
  was not read.
- The generic repository secret-boundary scan ran through `validate.py --ci`:
  1,392 files scanned, zero findings.
- CB-01 write set: 17 catalog records, four implementation/test files, and this
  receipt. `knowledge/catalog/index.yaml`, the `0425Z` receipt, the immutable
  `0112Z` receipt, source documents, governance decisions, and generated HTML
  were not changed.

## Second-brain disposition

- Opportunity identified: make catalog freshness history complete and
  mechanically reproducible instead of relying on review-time reconstruction.
- Pattern: authority-ranked provenance with exact immutable events and
  fail-closed catalog discovery.
- Disposition: IMPLEMENTED in the current corrective scope.
- Evidence: 17 missing events reduced to zero, exact-event regressions pass in
  both history forms, and all catalog and repository gates pass. No broader
  roadmap change is required.

## Hosted status

- One commit and one push remain pending.
- PR #8 must remain open, draft, unmerged, and without auto-merge.
- The workflow tied to the exact pushed HEAD will be monitored once. Any
  remaining major finding will be reported without a second commit or push.