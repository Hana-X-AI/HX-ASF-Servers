[CATALOG RECEIPT]

Run: 2026-08-28T0452Z  Agent: Carol  Tier: T-standard (registry-scope
wave)
Trigger: Kimi-K3 governor dispatch — registry-record scope sync (rr CI
findings; the registry source gained the Phase-1 footer scope line
today — governor edit, repo only: 'Phase 1 (discovery): COMPLETE,
verified 2026-08-13 — 15 of 15 records accepted (historical baseline
scope: the original fifteen-server fleet). Current registry: 17 rows
accepted — hxs-20 and hxs-21 added 2026-08-28 after rick's first live
inventory (baseline-green; their discovery records cataloged as
DOC-hxs20-discovery and DOC-hxs21-discovery)'; the TKV copy has no
count line). Carry-forward: receipt
2026-08-28T0352Z-carol-living-contract.md + validate.py 4/4 PASS at
03:52Z. Tooling: scripts/catalog/carol-mint v1.0.0 used for the
mechanical re-hashes (adoption dogfood — the tool's single-writer
flock on knowledge/catalog/.mint.lock + atomic temp+rename writes;
its test suite re-run at wave start: 15 passed, 0 failed). Receipt
authored by the agent per dispatch. No mid-run drift on any source
this run.

Added (0): none — document_count stays 298.

Updated (2):
- DOC-server-registry — dispatch item 1 (three parts + tool re-mint):
  (a) the exception-note correction in
  notes.current_state_exception_20260828 (labeled append): class (a)
  DEPLOYED and owner-accepted workloads = hxs-1 and hxs-3 ONLY (they
  carry the literal 'CURRENT-STATE:' prefix); class (b) owner-advised
  ROLE changes with NO deployment claim = hxs-5 (control plane) AND
  hxs-7 (replaced by hxs-20, same advisory) — the batch-11 note's
  single-class list (hxs-1/hxs-3/hxs-5 under one class) is the
  superseded era form, preserved as history; hxs-5 carries no
  CURRENT-STATE: prefix and hxs-7 belongs with it. The LOCATION
  correction in the same note (labeled): the REPO source carries the
  exception ONLY on the TARGET-STATE header bullet (repo line 14,
  VERIFIED this run — the earlier Rules-line occurrence is gone);
  the TKV mirror carries it on the manual-approval rule line (tkv
  line 10, VERIFIED this run). (b) scope sync to the 17-row registry:
  title now '17 rows (hxs-1..hxs-15 + hxs-20 + hxs-21 added
  2026-08-28, baseline-green)'; declared_purpose carries the 17 rows
  with the two newest cataloged (DOC-hxs20-discovery /
  DOC-hxs21-discovery), the amended two-class exception, and the
  Phase-1 footer scope line (source lines 98-101, VERIFIED PRESENT);
  version now includes 2026-08-28; applies_to.hosts += hxs-20 +
  hxs-21; applies_to.fqdns += hxs-20.hx.local.arpa +
  hxs-21.hx.local.arpa (router-DNS-verified canonical FQDNs).
  (c) RE-MINT via carol-mint (single-writer lock + atomic write):
  ace0fb39… -> 00e2ab28a0b477ddbf47b1d7bd1d5cb15b05a8b3741778b39c352de4e8ab3627
  — the Phase-1 footer edit; stamp notes.minted_by 'carol-mint 1.0.0
  @ 2026-08-28T04:48:23Z — re-mint ace0fb39c340… -> 00e2ab28a0b4…';
  notes.scope_sync_20260828 records the full wave.
- DOC-tkv-server-registry — dispatch item 2 (tool re-mint,
  confirm-current): the TKV file is UNCHANGED since the batch-7
  re-hash — b0726e46… == live, verified before stamping; the tool
  stamped the freshness-only re-mint (validated_at
  2026-08-28T04:48:23Z; notes.minted_by 'carol-mint 1.0.0 @
  2026-08-28T04:48:23Z — re-mint freshness-only — confirm current
  (TKV unchanged since the batch-7 re-hash)'); freshness stays
  superseded; the record STAYS SUPERSEDED pointing consumers to
  DOC-server-registry.

Index: the DOC-server-registry line's title synced to the 17-row
record title (graded field); the updated-field write-set wording
rewritten for this wave (0 added, 2 updated + the tooling note);
count 298 unchanged. NOTE on tooling scope: `carol-mint index` was
DELIBERATELY NOT used for the index rebuild — its full rebuild
regenerates every title line from the records and would overwrite
the standing-8 compressed index titles (the maintained compressed
lookup surface, informational since ratification); hand-editing the
one title line + the header preserved that surface. Flagged for the
governor (see F-1).

Living-record note (dispatch item 3): the OmniRoute pilot state-log
record is LEFT at its consolidation point per the owner-ratified
contract (freshness 'living'; LAST CONSOLIDATION 2026-08-28T03:35Z
at f46d6c1f…, rows 1-61). The log has since advanced (rows 62-64
landed) — 'source may be ahead' by design; rows 62-64 ride the NEXT
consolidation (daily 04:00Z when changed; work-arc close; owner
call — profile §12). No per-wave re-mint was performed on it.

Linked (no new relation edges this wave — all updates are content/
hash maintenance on existing records).

Flagged (each with provenance):
- F-1 (tooling surface decision, for the governor): `carol-mint
  index` regenerates all 298 title lines from the records — using it
  would silently overwrite the standing-8 compressed index titles
  (the maintained compressed lookup surface the validator reports
  informationally: titles exact 290/298 today, 8 compressed). The
  tool was used only for the two re-mints + the write-set gate (its
  dispatched scope); the index title sync + header were hand-edited.
  The dogfood is otherwise clean: lock held, atomic writes, stamps
  present on both records, gate PASS (2 records checked), full
  validate.py 4/4. If the compressed-title surface is to survive
  tool adoption, `carol-mint index` needs a preserve-titles mode or
  the surface needs an owner decision to retire it.
- F-2 (standing owner-lane, unchanged): backup-encryption-wrapper
  UNDECIDED; the hxs-6 storage-op strengthened gate (owner GO +
  device-map approval + the LVM-topology proof); the SB-on set
  hxs-6/7/11/21 (record-only); hx-20 rename / hxs-21 .21 placement
  (network decisions); the hxs-21 update mechanism; the DSH-gated
  items; the living-record consolidation cadence (rows 62-64
  pending, above).
- No contradictions beyond the preserved flags. No secret values
  cataloged (self-sweep of all touched files: 0 hits).

Rejected / not cataloged (recorded dispositions, profile §4):
- `carol-mint index` full rebuild — declined this wave (F-1; the
  compressed-title surface would be overwritten without an owner
  decision).
- Rows 62-64 of the OmniRoute state log — deliberately not re-minted
  (the living contract; they ride the next consolidation).

Freshness: both touched records current at the tool's re-mint stamps
(2026-08-28T04:48:23Z); close re-verification 04:54Z == live for
both (zero residual drift). No freshness transitions
(DOC-tkv-server-registry stays superseded by design; the four
state-log records stay living per the contract).

Follow-ups:
- RECEIPT CITATION: the governor cites this receipt in the OmniRoute
  pilot state log per profile §7 (expected row 65 — which the LIVING
  record absorbs at the NEXT consolidation, not a per-wave re-mint).
- Governor decisions pending: F-1 (`carol-mint index`
  preserve-titles mode vs retiring the compressed-title surface);
  the batch-7 + contract commit (row 61's queue).
- Governor-side standing: the L1-M3 gate dispatch on the owner's
  word; the hxs-6 storage-op strengthened gate; the living
  consolidation (daily 04:00Z when changed / arc close / owner call
  — `carol-mint consolidate` is the mechanized path).
- Standing for all non-living records: ledger records re-hash on any
  ledger edit; corpus manifest re-hash 2026-09-24 unchanged.

Verification (T-standard scope):
- Write set: 2/2 records parse; required fields + enums OK; record
  sha256 == live source for both at close (the repo re-mint at
  00e2ab28… and the TKV confirm at b0726e46…, both re-verified
  04:54Z == live — zero residual drift); index 1:1 for both touched
  ids — line fields exact INCLUDING the synced 17-row title; DOC
  relation targets of both records resolve (CAT-04); self-sweep of
  all touched files against the secret patterns: 0 hits.
- Write-set gate: `carol-mint gate --ids DOC-server-registry,
  DOC-tkv-server-registry` — PASS (2 records checked; the tool's
  own ladder: parse, required fields, freshness enum, index 1:1,
  relation targets, canonical_location on disk).
- Full-catalog self-check: 298 records parsed, unique ids; index
  count 298 == lines 298 == records 298.
- scripts/validate.py at close (2026-08-28T04:54:23Z, after all
  writes): PASS 4/4 — wiki-sync 48/48 in sync; fixture-suite 57
  tests OK + 10/10 manifest; catalog-mechanical 298 records, index
  1:1 (298 ids, 1192 line-field values exact; titles exact 290/298
  — 8 compressed, informational, the standing 8), relations
  resolve, CAT-07 297 locations resolve (1 protected-resource
  exempt), CAT-08 0 violations (24 raw-path targets, all noted);
  secret-boundary 722 files, 0 hits. 4 manual gates noted
  (CAT-10..15, CAT-20..22, CB-01, literal-credential sweep).

Index: updated (sha256 61c17b74c3456c7be2f28af97c0b7fe2ebaff4e25e360d1c5632b1c83e356f2b;
0 added, 2 updated (the DOC-server-registry title line synced; the
header rewritten with this run's provenance, label 2026-08-28T0452Z);
count 298 unchanged).

Result: PASS WITH FLAGS — REVIEW REQUIRED (298 records; validate.py
4/4; the registry scope is synchronized to the 17-row reality and
the exception note matches the source exactly — flags F-1..F-2
above, each with provenance: F-1 is the tooling-surface decision for
the governor, F-2 stands owner-lane).
