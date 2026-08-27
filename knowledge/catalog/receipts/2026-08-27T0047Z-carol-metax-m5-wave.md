# Catalog receipt — 2026-08-27T0047Z-carol-metax-m5-wave.md

| Field | Value |
| --- | --- |
| Run | Carol **T-standard** — Meta-X M5 wave |
| Dispatch | Governor brief 2026-08-27T~00:38Z (governor-verified hxs-2 state log row 38 + hxs-3 state log row 21, both 2026-08-27T00:38Z) |
| Write set | 6 records + index (1 added, 5 updated) |
| Window | 2026-08-27T00:38Z → 01:02Z |
| Result | **PASS — CATALOG CURRENT** |

## Records

| Record | Action | Hash before | Hash after |
| --- | --- | --- | --- |
| DOC-pilot-hxs3-ev-12-esme-m5-validation | NEW — pilots/PILOT-HXS3-MUSE-GLIMMER-TOOLING-001/12-esme-m5-validation.md (PASS — TASK COMPLETE; 380-line main body + Addendum A, 531 lines); type evidence, status adopted, authority agent-evidence; provenance hxs-3 log row 20 (2026-08-27T00:07Z, M5 COMPLETE governor-verified) + row 21 (2026-08-27T00:38Z, batch-13 dispositions). Suites per the owner-ratified bars: tool protocol 14/14 — 100% forbidden/malformed denied + 100.0% schema conformance + 0 raw ATEM; one-call-per-turn 100% ENFORCED incl. the OC07 live rejection (2 multi-call responses seen, 2 rejected, 0 leaked, accepted calls serial); structured output 20/20 = 100%; system-policy 22/22 = 100% (2 disclosed evaluator adjudications); denial 100% (16 denied decisions, 0 executions); reasoning_strength + parallel_tool_calls REPORTED probe-only. Batch-13 fixes verified incorporated: 19-reviewed count (F2), UNKNOWN labels (F3), T-DENY reconciliation (F4), 18:42 conversion + EST=-01/UTC=-02 scoping (F5) | — (new) | 2ef342045aa6a44ca8aa51e68b0a4a64667f3c04ae5cacee815450e8dc12462f |
| DOC-pilot-hxs3-wo-10-john-m5 | FLIPPED active -> adopted (DISCHARGED — milestone complete, M7-pair convention); title synced; governs edge to the new deliverable record added (deferred at the in-execution cataloging); validated_at 2026-08-27T00:47Z; source hash re-verified UNCHANGED at the flip | 0519e93e68d886865495f916d1ae227d93e7c99a730ffd4d7b70f70951a00dba | 0519e93e68d886865495f916d1ae227d93e7c99a730ffd4d7b70f70951a00dba (unchanged — source untouched) |
| DOC-pilot-hxs3-cp-11-john-m5 | FLIPPED active -> adopted (DISCHARGED, with the paired WO); title synced; governs edge added (evidence-contract-satisfied wording per the CP-09 precedent); validated_at 2026-08-27T00:47Z; source hash re-verified UNCHANGED | 9b4849da2500da547737cacfe8ff37f203e762caa5e12ab19229bae4c71a86c8 | 9b4849da2500da547737cacfe8ff37f203e762caa5e12ab19229bae4c71a86c8 (unchanged — source untouched) |
| DOC-fleet-time-and-mask-pass | RE-HASH dispatched per hxs-2 log row 38 ("governor's uptime edit post-dates her 00:33Z verification"): recomputed against the current source — **UNCHANGED**; chain step + CONFLICT FLAG appended to notes.mid_run_correction (see F-W1); validated_at 2026-08-27T00:47Z | 26a46cf01023a4ef8ed71cd3b460ed4f71f35f7c028569ceb276a31a5daf9baf | 26a46cf01023a4ef8ed71cd3b460ed4f71f35f7c028569ceb276a31a5daf9baf (unchanged — see F-W1) |
| DOC-pilot-hxs2-state-log | Advanced rows 1–37 -> 1–38 (row 38, 00:38Z: fleet-pass receipt 0030Z cited at 240 records + review batch-13 dispositions — F1/F2/F5/F7 VALID fixed, F3/F4 ALREADY SATISFIED, F6 PARTIALLY VALID fixed differently with evidence, F-TMICRO-TIME over-target flag + this wave queued); title/version/relation-target windows synced; living-document hash chain extended | 910cef53d30da562d78b2c5d6e7aff10e2b0f8f0ca5a1c1cc2073f9b7efdf3ba | 9baf140e2a7e350584dadc550cb977b8e6ab6e7300cab626478727b1cd9edc06 |
| DOC-pilot-hxs3-state-log | Advanced rows 1–20 -> 1–21 (row 21, 00:38Z: fleet-pass receipt cited + batch-13 hxs-3-side dispositions — F2 19-reviewed fixed with grouping rule, F3/F4 already satisfied, F5 timestamps fixed, F6 fleet-doc uptime corrected by governor + M5 handoff OPEN pending this wave); title/version/relation-target windows synced; living-document hash chain extended | 50631411b1262b348db47cc792a47b650b3abfe522f322dc5c1ecc7e1cc4501f | 994cbed6927a0f01da0956458ff75a6508f04ed8384148b94f33dfde75531b21 |

Index: 1 entry added (alphabetical position, after DOC-pilot-hxs3-ev-09-esme-m7-ladder-profiles), 4 title syncs (both state logs + the flipped M5 pair), header `updated` rewritten for this run, `document_count` bumped; count 240 -> 241.

## Linked

- `governs`: DOC-pilot-hxs3-wo-10-john-m5 -> DOC-pilot-hxs3-ev-12-esme-m5-validation; DOC-pilot-hxs3-cp-11-john-m5 -> DOC-pilot-hxs3-ev-12-esme-m5-validation (M7-pair convention — edges deferred at the in-execution cataloging, added at the flip).
- New record relations: evidences -> WO-10 / CP-11 / DOC-goal-hxs3-muse-glimmer-tooling (SC-05 invariant enforcement-proven; D8 material delivered); produced_by -> john; references -> DOC-pilot-hxs3-ev-09-esme-m7-ladder-profiles (frozen identity basis), DOC-kdd-0007 (the contract under test), DOC-pilot-hx1-ev-16/-ev-19 (execution + evaluator-review standards), DOC-pilot-hx1-fixtures-manifest (10/10 ×2 sessions), DOC-fleet-time-and-mask-pass (TZ conversion mid-close-out, A.4); risks -> F-M5-3/F-M5-4 (prompt-dependent discipline; /v1 multi-call capability — the gate must travel with the path).

## Checks (T-standard scope: write set + full-catalog self-check + one validate.py at close)

- Write set: YAML parse + required fields + enum values (type/status/authority/predicates/security) + record sha256 == live source sha256 + index 1:1 (id, title, type, authority_level, freshness, canonical_location) + relation targets resolve: **6/6 PASS**.
- Full-catalog self-check: 241/241 records parse; counts header 241 == index entries 241 == documents/ files 241 == parsed 241; index 1:1 across the full catalog (no orphans, no dangling lines); every DOC-id relation target in all 241 records resolves: **PASS**.
- `python3 scripts/validate.py` at close (2026-08-27T01:01Z): **PASS 4/4 (exit 0)** — wiki-sync 38/38 in sync; fixture-suite 57 tests OK + sha256sums 10/10; catalog-mechanical 241 records (964 structured line-field values exact; CAT-04 relations resolve; CAT-07 240 locations resolve + 1 protected-resource exempt; CAT-08 0 violations); secret-boundary 542 files scanned, 0 hits; 4 manual gates noted (CAT-10..15, CAT-20..22, CB-01, literal-credential sweep — governor-side, never graded here).

## Flagged

- **F-W1 (dispatch-premise conflict — preserved, authority-ranked, not guess-resolved; profile §9):** the brief and hxs-2 log row 38 premise that the governor's batch-13 line-139 uptime correction "landed AFTER your 00:33Z verification" does not hold against the live evidence: the fleet doc's mtime is 2026-08-27T00:26:10.25Z and its live sha256 is byte-identical to the recorded 26a46cf0… — the batch-13 uptime content at line 139 ("~40 min" vs the second 23:17Z reboot, incl. the explicit "Batch-13 note:" sentence) was already present in the bytes hashed at 00:26:10Z and verified at 00:33Z. The record's hash stands verified-current; the chain step and this flag are recorded in notes.mid_run_correction. For the governor's disposition (a row-38 wording correction is the governor's call, not Carol's).
- **F-W2 (superseded citation, disclosed):** hxs-3 log row 20 cites deliverable sha256 e37c2ec8…db5c1 — the pre-batch-13 bytes. The cataloged source is the 00:21:43Z batch-13-incorporated version (2ef34204…, mtime 00:21:43Z, stable through cataloging); the chain is disclosed in the new record's notes.hash_chain, never silently dropped (server records contract).
- **Sanitization class (contained at source):** the deliverable discloses two transcript-only credential-row exposures (F-M5-8, session -01; Addendum A.6, session -02) — value in no file, command line, or artifact. No credential material is quoted or stored anywhere in the catalog (profile §6). The standing owner-rotation advice remains pending OUTSIDE the catalog lane; carried here as a flag only.

## Freshness

- DOC-pilot-hxs3-wo-10-john-m5, DOC-pilot-hxs3-cp-11-john-m5: active -> adopted (DISCHARGED — milestone complete).
- DOC-pilot-hxs2-state-log (rows 1–38), DOC-pilot-hxs3-state-log (rows 1–21), DOC-fleet-time-and-mask-pass: current, re-validated 2026-08-27T00:47Z.
- Rejected: none. No supplied document was left without a disposition.

## Follow-ups

- **Meta-X M5 handoff closure:** per the context-packet handoff clause and the dispatch, the Meta-X M5 handoff CLOSES when the governor cites THIS receipt in the hxs-3 state log (profile §7) — OPEN until that citation lands.
- M8 sign-off gate: DOC-pilot-hxs3-ev-12-esme-m5-validation is the quality grounds; review_due set accordingly on the flipped pair and the new record.
- Owner D8 reasoning_strength operating decision: mapping evidence delivered (native think bool + low/medium/high/max; xhigh HTTP 400 natively; /v1 accepts incl. xhigh→max but never surfaces the trace).
- KK3 adapter contract: F-M5-3/F-M5-4 (gate on any serving path; the flag is a probe), F-M5-5 (always attach retry budgets), SP17-class phrasing (policy-prompt option).
- rick's plane: F-M5-1 /tmp boot-clear mechanism on hxs-3 (evidence must leave the host immediately — discipline already adopted by john).
- F-1 hxs-4 sleep masks: carried, queued for the first authorized hxs-4 session (DOC-fleet-time-and-mask-pass review_due).

## Carry-forward

validate.py 4/4 PASS at 2026-08-27T01:01Z — a new 24 h citation window opens with this receipt (superseding the 2026-08-26T2026Z chain carried by the 0030Z T-micro). Cycle time ~24 min end-to-end for the 6-record / 5-task bundle — T-standard class per the owner-ratified bundle calibration (4–5-task bundles dispatch T-standard); no over-target condition applies to this tier. No git commit (owner gate; commits happen in governor waves).

`PASS — CATALOG CURRENT`

## Addendum (2026-08-27, review batch: stray character)

The Dispatch field's `2026-08-27T~00:38Z` contains a stray tilde — a typo. The exact dispatch time is **2026-08-27T00:38Z** (matching the cited state-log rows 38/21 later on the same line). Original line preserved per the receipts-are-append-only convention; provenance checks should read the dispatch time as 2026-08-27T00:38Z.
