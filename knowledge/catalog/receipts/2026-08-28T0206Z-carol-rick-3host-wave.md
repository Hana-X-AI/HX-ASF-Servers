[CATALOG RECEIPT]

Run: 2026-08-28T0206Z  Agent: Carol  Tier: T-standard (rick-3host wave)
Trigger: Kimi-K3 governor dispatch — catalog rick's hxs-11/20/21
baseline wave + registry/standard updates + the F-2 sweep (provenance:
OmniRoute pilot state log rows 55-56, 2026-08-28T01:28Z/01:34Z — row
55: rick's three-host receipt, 3/3 baseline-green (hxs-11 PASS
post-maintenance, hxs-20 REPORT at .220/hostname hx-20, hxs-21 REPORT
at .21 outside the fleet block; the two governor WO-addressing
assumptions corrected by evidence with both values kept; TOFU-
with-corroboration pins ×2 + PINNED-NEW-VERIFIED ×1; SB flags ×2
record-only); row 56: batch-11 receipt cited (293), the governor's
registry writes in both copies + fleet-standard gained the two hosts,
THIS wave dispatched). Carry-forward: receipt
2026-08-28T0126Z-carol-batch11.md + validate.py 4/4 PASS at 01:26Z.
No mid-run drift on any source this run.

Added (3):
- DOC-fleet-baseline-hxs11-20-21-2026-08-28 — servers/2026-08-28-
  fleet-baseline-hxs11-20-21.md (mint per dispatch item 1): rick's
  three-host baseline wave evidence (commission
  rick-fleet-baseline-20260828-01 on owner word; window 01:09Z-01:23Z;
  PASS — TASK COMPLETE, 3/3 verdicts 1 PASS 2 REPORT 0 FAIL): hxs-11
  .210 PASS (identity MATCH the 08-12 discovery, host key
  PINNED-NEW-VERIFIED vs the owner console record, 8/8 vs the
  official standard); hxs-20 REPORT (baseline green — live at .220
  with hostname hx-20, the WO's .219 wrong per the .199+N pattern,
  first-live machine-id, TOFU-with-corroboration D-record pin, 8/8 vs
  the run-standard); hxs-21 REPORT (baseline green — live at .21
  OUTSIDE the .200-.214 block, the WO's .220 was hx-20, TOFU D-record
  pin, 8/8); both REPORTs CLOSED via the governor's registry/standard
  updates (state log row 56). Mutations only the two sanctioned
  classes (NTP pin ×3 — conf sha256 e2b94d4b… extending the
  one-source proof to 15 in-scope hosts, mask align ×3); selftest
  43/43 at both gates; zero secret values (author's literal sweep 0).
  notes.owner_items_20260828 carries SB ENABLED on hxs-11 + hxs-21 as
  owner-lane record-only items (same class as hxs-6 — the fleet's
  SB-on set is now hxs-6, hxs-7, hxs-11, hxs-21), the hxs-21
  update-mechanism REPORT (44 recorded vs 0 live after the
  00:43:18Z reboot — mechanism not established), and the addressing/
  hostname registration calls (CLOSED at the registry level; rename/
  re-address never a sanctioned class). evidence, adopted,
  agent-evidence. sha256 2b3d10967477af6c2641b58a1f076fe986c77ecc5527d0bfa6069b965bef3a5a.
- DOC-tkv-hxs20-pre-work-results — /opt/tkv-local/servers/hxs-20/
  pre-work-results.md (MINT per dispatch item 2 — the file created by
  rick's wave; the FIRST record for the host): the agent
  re-verification record — first-live machine-id 7b5cd0b8…, the
  TOFU-with-corroboration D-record (no fingerprint existed in any HX
  record; the live ED25519 key pinned ONLY on immediate corroboration
  vs the owner-supplied discovery — SHA256:ZUEHfcFL+1Ru070e163g0uJDT7eOwlQh3MW8NZF3Mco
  recorded for strict pinning, a mismatch must halt; fingerprints are
  public host-key material, NO credential material exists in the
  file), the real address .220 with hostname hx-20 (the .199+N
  pattern break), first-live hardware facts (i5-7500, 2×16 GB
  Samsung, single NVMe 238.5G), passwordless sudo live, SB disabled,
  the two sanctioned mutations. pre-work, adopted, agent-evidence.
  sha256 a7eb6eaa19e6b89567c70bab3334531cc77d88f4e1e8bc9a636ec5fd346ae75c.
- DOC-tkv-hxs21-pre-work-results — /opt/tkv-local/servers/hxs-21/
  pre-work-results.md (MINT per dispatch item 2 — same class): the
  agent re-verification record — first-live machine-id 773a4517…,
  TOFU D-record pin (SHA256:3ygj6lZMictGTCBZuq1R04VbnECUN4XS0Lq2Pr3gYk8),
  the real address .21 OUTSIDE the fleet block, first-live hardware
  (i5-7500, 2×16 GB Hynix mixed revisions, single NVMe 238.5G),
  passwordless sudo live, Secure Boot ENABLED record-only (hxs-6
  class), the two sanctioned mutations, the 44->0 updates drift
  (mechanism not established, owner maintenance lane). pre-work,
  adopted, agent-evidence. sha256 2976b449ec3c2031716d6e886555dcd7ac550c241959fa56717759443306ccd7.

Updated (8):
- DOC-tkv-hxs11-pre-work-results — dispatch item 2 (re-hash): the
  FIRST refresh-by-prepend recorded (rick's 2026-08-28 re-verification
  section on top; the original 2026-08 preparation record + its
  owner-console fingerprint preserved verbatim below): verdict REPORT
  — baseline green; host-key ceremony PINNED-NEW-VERIFIED (the live
  fingerprint EXACTLY MATCHED the owner console record preserved in
  this file); machine-id MATCH the 08-12 discovery; post-maintenance
  boot 00:43:32Z; SB ENABLED record-only (hxs-6 class); NTP pinned
  01:15:38Z + masks 01:15:39Z; 8 PASS 0 FAIL vs the OFFICIAL standard
  (hxs-11 IS declared server-default — the wave WO's all-three-absent
  claim was wrong for hxs-11; the governor's standard amendment note
  carries the open correction); 5 upgradable (maintenance lane).
  Re-hash 1358c6b3… -> 1c8356e12417a1bafe6b8248f2f78275800739ca00aa477fb080034472319d25;
  declared_purpose + version extended; freshness historical ->
  current (the top layer is a current verified live-state assessment;
  the below-marker original keeps its historical-as-found truth
  state); notes.refresh_20260828 added.
- DOC-fleet-script-library — dispatch item 3 (manifest re-digest):
  fleet-standard.yaml 4c298ea6… -> bf306604… the ONLY changed file
  of the nine: hxs-20 + hxs-21 ADDED to server-default (source lines
  41-42, VERIFIED PRESENT) with the dated amendment note — hxs-11 was
  ALREADY declared (the governor's WO wrongly said all three were
  absent — rick's F-2 corrected it, open note); hxs-20 lives at .220
  (hostname hx-20) and hxs-21 at .21 — the .199+N pattern does NOT
  hold for these two (source lines 127-131, VERIFIED PRESENT).
  Manifest digest 5cf28812… -> f797a0f267ab29354054633497334839d701bab398b3b059197d121e68bd116a;
  the closing-wave digest 5cf28812… reproduced EXACTLY from the
  recorded per-file hashes before recomputation (construction
  re-validated); README + 7 scripts == recorded values.
- DOC-server-registry — dispatch item 4 (re-hash + notes): the new
  rows and notes recorded — hxs-20 row ADDED (hx-20.hx.local.arpa,
  .220, i5-7500, 32 GB Samsung @2400 first live reading, 238.5 GB
  NVMe, COMPLETE first live inventory, MCP services replacing hxs-7,
  FastMCP runtime + custom HX MCP servers target, READY
  baseline-green); hxs-21 row ADDED (hxs-21.hx.local.arpa, .21
  outside the block, i5-7500, 32 GB Hynix mixed revisions, COMPLETE
  first live inventory, Standby — designated future control-plane
  machine (owner advisory: eventually replaces the hxs-5 machine),
  none assigned yet, READY baseline-green); hxs-7 row note (hxs-20
  ONLINE 2026-08-28 baseline-green); hxs-cp note (hxs-21 online at
  .21); the dated ADDRESSING NOTE (.199+N pattern break recorded —
  hxs-20 at .220 hostname hx-20, hxs-21 at .21 outside the block,
  verified live by rick's wave) — all VERIFIED PRESENT; the registry
  now carries 17 rows. Re-hash ad521ff9… -> f1d50bebfb372a2081df22f8640de785bbd84107fe969269d12bd46a7b10d327;
  notes.hxs20_hxs21_rows_20260828.
- DOC-tkv-server-registry — dispatch item 4 (re-hash + notes): the
  same rows/notes mirrored in the TKV file (ALL VERIFIED PRESENT);
  re-hash d6cbdfa3… -> 5c8b00b8a6aa5bec973d3b46ad500155c4fd03c172e1b10bc830615859db995d;
  notes.hxs20_hxs21_rows_20260828; the record STAYS SUPERSEDED
  pointing consumers to DOC-server-registry (authority preserved).
- DOC-pilot-omniroute-state-log — advanced rows 1–54 -> 1–56
  (dispatch item 6); re-hash f500dc90… -> 91cc8b3f148d62f8f94da9999e339812d1c184323db520df4bdd2f95aedfb146.
  Rows absorbed: 55 (01:28Z — rick's three-host receipt: 3/3
  baseline-green with the addressing corrections and the TOFU pins;
  SB flags ×2) and 56 (01:34Z — the batch-11 receipt cited at 293;
  the governor's registry writes in both copies + fleet-standard
  gained the two hosts; THIS rick-wave catalog wave dispatched with
  her F-2 shorthand sweep riding it). Describes note + hash chain
  extended; validated_at 2026-08-28T01:36Z; close re-verification
  02:04Z == live.
- F-2 SWEEP (dispatch item 5 — 10 records, labeled corrections):
  the unlabeled '23:4xZ' shorthand in the rr47_20260827 note openings
  swept to the exact 2026-08-27T23:40Z with a labeled correction per
  record (never silently rewritten): DOC-agent-trinity-profile,
  DOC-fleet-baseline-wave-2026-08-27, DOC-goal-omniroute-layer1-
  secure-core, DOC-goal-omniroute-trinity-layer0,
  DOC-pilot-fleet-baseline-wo-02-rick-baseline,
  DOC-pilot-omniroute-control-manifest,
  DOC-pilot-omniroute-decision-19-kk3-gate,
  DOC-pilot-omniroute-ev-08-capability-ledger,
  DOC-pilot-omniroute-ev-p2-providers-protocol,
  DOC-pilot-omniroute-wo-07-rick-node (the two already-fixed records
  — wo-09 (batch-10) and both state logs (batch-11) — carry the
  labeled form from their own waves). validated_at refreshed on all
  10. Post-sweep grep: no UNLABELED '23:4xZ' instance remains in the
  catalog (only the labeled-correction quotations and the state-log
  record's quote of the governor's batch-11 item itself).

Linked (new relation edges):
- DOC-fleet-baseline-hxs11-20-21-2026-08-28: evidences the 3-host
  baseline; produced_by rick; references the 08-27 wave evidence
  (pattern + doc shape), DOC-fleet-script-library (tooling + the
  run-standard mechanism), DOC-pilot-omniroute-state-log (rows
  54-56), the three pre-work records (refresh/mint family),
  DOC-server-registry (the F-1 closure); risks hxs-11 (SB + pending
  updates), risks hxs-21 (SB + block placement + update mechanism),
  risks hxs-20 (hostname hx-20 — rename not sanctioned).
- DOC-tkv-hxs20/hxs21-pre-work-results: describes the host;
  references the wave evidence, DOC-server-registry (the new row),
  the owner-supplied discovery (free entity — not cataloged), the
  TKV mirror record.

Flagged (each with provenance):
- F-1 (uncataloged owner-supplied discoveries): servers/hxs-20/
  discovery.md and servers/hxs-21/discovery.md exist in the repo
  (owner-supplied interactive evidence 2026-08-28 — the identity
  basis the TOFU ceremonies corroborated against) and have NO catalog
  records — outside this wave's dispatched scope (the dispatch covers
  the pre-work records); flagged for the governor, catalogs when
  supplied to a wave.
- F-2 (validator FAIL caught and fixed in-run — recorded openly):
  the first close run (2026-08-28T02:04:40Z) FAILED CAT-03 on one
  index line — DOC-tkv-hxs11-pre-work-results freshness 'historical'
  != record 'current' (the freshness flip was applied to the record
  but the graded index line was missed); fixed in-run (the index
  line now reads current) and re-run PASS 4/4 (02:06:17Z). The
  transient FAIL state never entered any record.
- F-3 (standing owner-lane): SB-on set is now hxs-6, hxs-7, hxs-11,
  hxs-21 (owner BIOS decisions); hxs-20 hostname hx-20 and hxs-21's
  .21 block placement (owner/governor registration calls — rename/
  re-address never a sanctioned class); hxs-21 update-application
  mechanism + hxs-11's 5 pending updates (owner maintenance lane);
  the standing items from row 52 (backup-encryption-wrapper, the
  DSH-gated items, the hxs-6 storage-op dual gate, L1-M3 gate GO).
- No contradictions beyond the preserved flags. No secret values
  cataloged (the TOFU fingerprints are public host-key material;
  self-sweep of all touched files: 0 hits).

Rejected / not cataloged (recorded dispositions, profile §4):
- The owner-supplied hxs-20/hxs-21 discovery docs — next-wave
  candidates (F-1), not silently minted outside the dispatched scope.
- The session run-standard (official + 2 class lines, sha256
  d53b7b3a…) — a transient execution artifact of rick's session,
  recorded by hash in the evidence doc and this receipt; not a
  cataloged artifact (the official file carries the hosts now).

Freshness: all 11 touched records current at 2026-08-28T01:36Z
validations; close re-verification 02:04Z == live for all 11 (zero
residual drift). Two freshness transitions: DOC-tkv-hxs11-pre-work-
results historical -> current (the refresh layer; index line synced
in-run per F-2).

Follow-ups:
- RECEIPT CITATION: the governor cites this receipt in the OmniRoute
  pilot state log per profile §7 (expected row 57); then the batch-11
  commit per row 54 (both receipts landed).
- NEXT-WAVE candidates (F-1): the owner-supplied hxs-20/hxs-21
  discovery records (mint when dispatched).
- Governor-side standing: the batch-11 commit; the L1-M3 gate
  dispatch on the owner's word; the hxs-6 storage-op dual gate.
- Owner items: SB-on hosts (BIOS), hxs-20 rename / hxs-21 placement,
  the hxs-21 update mechanism + hxs-11 pending updates (maintenance
  lane), the standing row-52 items.
- Standing: ledger records re-hash on any ledger edit; corpus
  manifest re-hash 2026-09-24 unchanged.

Verification (T-standard scope):
- Write set: 11/11 records parse; required fields + enums OK; record
  sha256 == live source for all 11 at close (the three mints at
  mint-time hashes; the eight updates re-verified 02:04Z == live —
  zero residual drift); the library manifest-digest construction
  re-validated by exact reproduction of the prior recorded digest
  before recomputation; index 1:1 for all touched ids — line fields
  exact INCLUDING titles (3 new lines in sort order; the OmniRoute
  log title to rows 1–56; the hxs-11 freshness line synced — see
  F-2); DOC relation targets of all touched records resolve
  (CAT-04); self-sweep of all touched files against the secret
  patterns: 0 hits.
- Full-catalog self-check: 296 records parsed, unique ids; index
  count 296 == lines 296 == records 296.
- scripts/validate.py run TWICE this wave: (a) 2026-08-28T02:04:40Z
  — catalog-mechanical FAIL, 1 finding (CAT-03 freshness mismatch on
  the hxs-11 index line — caught and fixed in-run, F-2 above);
  (b) 2026-08-28T02:06:17Z — PASS 4/4: wiki-sync 48/48 in sync;
  fixture-suite 57 tests OK + 10/10 manifest; catalog-mechanical 296
  records, index 1:1 (296 ids, 1184 line-field values exact; titles
  exact 288/296 — 8 compressed, informational, the standing 8),
  relations resolve, CAT-07 295 locations resolve (1
  protected-resource exempt), CAT-08 0 violations (24 raw-path
  targets, all noted); secret-boundary 711 files, 0 hits; confirmed
  02:07:20Z after the index-header label set. 4 manual gates noted
  (CAT-10..15, CAT-20..22, CB-01, literal-credential sweep).

Index: updated (sha256 8bf196aabd8c1a50362aedafc543640df8f4585bf51812caae8edc28c9de3cbc;
3 added, 8 updated + 1 freshness-line sync (F-2); count 293 -> 296;
header rewritten with this run's provenance, label 2026-08-28T0206Z).

Result: PASS WITH FLAGS — REVIEW REQUIRED (296 records; validate.py
4/4; rick's three-host wave is catalog-complete — evidence + 3
pre-work records (1 refreshed, 2 minted), registry/standard/library
current, the F-2 sweep executed — flags F-1..F-3 above, each with
provenance: F-1 is the owner-supplied discoveries for the next wave,
F-2 is the in-run index-line fix recorded openly, F-3 stands
owner-lane).
