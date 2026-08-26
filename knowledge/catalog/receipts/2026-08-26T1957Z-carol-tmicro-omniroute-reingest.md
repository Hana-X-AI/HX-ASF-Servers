# Carol — T-micro receipt: OmniRoute re-ingest (F-M5C-1)

- Run: T-micro, 2 records, single purpose (retarget + re-hash after owner-lane reorg)
- Trigger: governor brief 2026-08-26 (hxs-2 log row 30; CAT-07 FAIL F-M5C-1)
- Window: 2026-08-26T19:46–19:57Z (end-to-end ≤ 5 min target met)

## Write set (documents/) — before → after

### DOC-tkv-corpus-omniroute
- canonical_location: `/opt/tkv-local/OmniRoute/OmniRoute-release-v3.8.50` → `/opt/tkv-local/OmniRoute-release-v3.8.51`
- sha256 (names-only manifest, own convention): `1fdb6f3600e4091a751b71cfeb897f2a6a081f2b7657bfd859948b4530e894ac` → `c5a65089935284a2c245612ece37c27e7cebfee39cd09e163a5d4ff5c48c6fc3`
- File count: 11,590 (v3.8.50) → 13,098 (v3.8.51), .git internals excluded
- Method reproduction verified: identical pipeline reproduces the prior v3.8.50 digest exactly on the surviving backup copy (see F1)
- Upstream identity of new tree: package.json `"version": "3.8.51"`, README.md dashboard header, own AGENTS.md/CLAUDE.md
- Title/declared_purpose/version updated to v3.8.51; provenance note appended; prior digest + path preserved in `notes.reorg_history`

### DOC-tkv-omniroute-hx-evaluation
- canonical_location: `/opt/tkv-local/OmniRoute` → `/opt/tkv-local/OmniRoute_old`
- sha256 (content-sensitive manifest, own convention): `737ba78e57e1a2f8da87920f757536169039df55604b74dbc17e2826c373392a` → unchanged (recomputed at new location; four HTMLs byte-identical, manifest identical)
- File count: 4 → 4 (wrapper minus upstream release trees and .git)
- Method variant verified against the known pre-reorg digest before adoption (paths relative to wrapper root, no `./` prefix, LC_ALL=C path order, two-space sha256sum lines, trailing newline, manifest digested)
- Title/declared_purpose updated; provenance note appended; prior path preserved in `notes.reorg_history`

### index.yaml
- Both entries updated 1:1 (title, canonical_location); document_count 235 unchanged (no adds/removes)

## T-micro verification (write set)
- Parse + required fields: both records parse, no missing required fields
- Hashes: both record sha256 values equal the recomputed manifests
- Index 1:1: title/type/authority_level/freshness/canonical_location exact for both ids
- Relation targets: `DOC-tkv-corpus-omniroute` ↔ `DOC-tkv-omniroute-hx-evaluation` resolve mutually; one non-id raw target carried noted as before

## validate.py at close
- Baseline (pre-edit): FAIL — exactly the two CAT-07 orphan locations; all other checks PASS
- Final: **PASS — 4/4 checks (exit 0)**; CAT-07 green; wiki-sync, fixture-suite, secret-boundary PASS; 4 manual gates noted (governor-owned, incl. CB-01 write-set audit)

## Findings for the governor
- F1: The "removed" v3.8.50 tree survives as `/opt/tkv-local/OmniRoute_old/.OmniRoute-release-v3.8.50-replacement-backup/` (11,590 files; names-only manifest reproduces the prior DOC-tkv-corpus-omniroute digest `1fdb6f36…` exactly — identity confirmed, not merely appearance). The brief's "v3.8.50 gone entirely" needs amendment. Record 2's documented scope excludes it as upstream content; a disposition (catalog as historical v3.8.50 record? delete? leave noted?) is the governor's call — outside this write set.
- F2: The nested `OmniRoute_old/OmniRoute-release-v3.8.51/` duplicate is names-manifest-identical to the top-level v3.8.51 (digest `c5a65089…` both). Not cataloged separately, per brief.

No git commit (owner gate). Originals untouched — all hashing read-only.

PASS — CATALOG CURRENT
