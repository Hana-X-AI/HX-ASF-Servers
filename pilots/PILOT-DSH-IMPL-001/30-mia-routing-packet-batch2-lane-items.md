# Routing packet — review batch 2 lane-owned items (Mia, per Flash work order 29)

**Prepared by:** Mia (Chief of Staff, KDD-0012), 2026-08-29, lane
`omniroute/glm-5.3-flash` via OmniRoute hxs-8.
**Status:** CHARACTERIZED, NOT EXECUTED. Each item below is routed to its
owning lane and requires a governor-issued work order before the lane acts.
Management-lane findings F19/F20/F22/F25/F26/F27/F28 (Morpheus plan docs) and
F41/F49–F53/F57–F62 (Chris/Wayne plan docs, incl. F59 as-built note) were fixed
directly by Mia in the same window; fixes are labeled, dated, append-only in
the target files.

## A. Route to MORPHEUS (dsh lifecycle lane) — engineering judgment on his own docs

| # | Target | Characterization | Expected fix shape |
| --- | --- | --- | --- |
| F21 | `10-morpheus-phase-c-prep.md` lines 339–341 | Readiness matrix promises per-row commands/tests that the sanitized command log does not contain for every PROVABLE row. Which rows can be backed by a bounded read-only command is a call only Morpheus can make against the corpus. | Add one bounded read-only command per PROVABLE row, or revise the closing claim to match what was actually run. |
| F23 | `10-morpheus-phase-c-prep.md` lines 323–324 | Blocked-status taxonomy is coarser than the finding's Partial/Yes split; deciding per row whether static posture is provable (Partial) vs activation blocked (Yes) requires his session knowledge. | Adopt the Partial/Yes blocked-status taxonomy per row, or rebut with row-level rationale. |
| F24 | `10-morpheus-phase-c-prep.md` lines 426–428 | The 09a work order caps corpus reads at 2–3 files per family; the command log shows 4–6 targeted reads per family. Whether these were authorized exceptions or a cap breach is his record to reconcile. | Reconcile counts against the cap: identify the governor exception if one existed, or record the deviation openly. |
| F29 | `10c-morpheus-rollback-ops-design.md` line 47 | Baseline-capture design hashes stdout+stderr together for the headless dump; stderr must stay separate or a stderr write taints the hash anchor. How the dump subprocess is invoked is his mechanics. | Redesign capture to hash stdout only, keep stderr as a separate artifact. |

## B. Route to GORDON (platform QA lane) — his test code, Phase B suite

| # | Target | Characterization | Expected fix shape |
| --- | --- | --- | --- |
| F42 | `gordon/phase-b/test_g6_orchestration.py` 704–705 | `boot.stop()` result bound to a name (`boot_log`) that does not describe the value (an exit code); later validation reads the wrong semantic. | Rename `boot_log` → `exit_code`, validate consistently. |
| F43 | `test_g6_orchestration.py` 441–442 | `check_a` success condition omits `child_seed`; a run with child seeding present but exit 0 + child_seen would falsely pass. | Add `and not child_seed` to the condition. |
| F44 | `test_g6_orchestration.py` 686–691 | Invalid-edit path never re-reads active config to confirm `fallbackMaxWords:11` survived; the retention property is unasserted. | Retrieve active config after invalid edit; assert `fallbackMaxWords:11` retained. |
| F45 | `test_g6_orchestration.py` 623–627 | On runner-write failure the exception is raised before `rec.finish` records the write result, losing the receipt. | Record write result into `rec.finish` before raising. |
| F46 | `gordon/phase-b/test_g7_surfaces.py` 1280–1286 | FEEDBACK_ONLY and FULL telemetry captures share a port/files, so captures can contaminate each other. | Separate captures on distinct ports/files. |
| F47 | `test_g7_surfaces.py` 717–722 | Determinism check compares against the in-memory initial fold rather than a fresh re-read of the session log; not a true determinism comparison. | Re-read the session log separately and compare against that. |
| F48 | `test_g7_surfaces.py` line 501 | Replacement-byte count computed inline in an f-string; use the actual three-byte U+FFFD sequence and a separate variable. | Compute count in a separate variable using the real 3-byte sequence. |

## C. Route to CHRIS (PostgreSQL lane) — his evidence docs (evidence = lane-owned)

| # | Target | Characterization | Expected fix shape |
| --- | --- | --- | --- |
| F54 | `2026-08-29-postgresql-install-step1.md` 350–350ff | Capability/pattern statement reflects the LAN-scram-bound era without a historical label; current trust posture differs. | Label LAN-scram statement HISTORICAL; append dated trust-posture correction. |
| F55 | `2026-08-29-postgresql-install-step2.md` 140–145 | V6 receipt does not show timer-fired activation (LAST/PASSED unpopulated); as written it over-claims. | Capture timer-fired activation with populated LAST/PASSED, or downgrade the claim to service-level smoke. |
| F56 | `2026-08-29-postgresql-install-step2.md` 117–125 | V4 identity evidence lacks `current_user` capture for INSERT/SELECT; identity of the acting role is unproven. | Record `current_user` for INSERT/SELECT; grant `ps-scratch` privileges if the probe shows they are missing. |

## Routing note

All items above are OUTSIDE my lane: B and C are engineering evidence/test
artifacts, A requires Morpheus's corpus/session knowledge. No lane file was
touched for any of them. Recommended sequencing: Gordon's F42–F48 (Phase B
suite correctness, blocks Gate evidence quality), Chris's F54–F56 (evidence
receipts), Morpheus's F21/F23/F24/F29 (design-record reconciliation) — order
among them is the governor's call.
