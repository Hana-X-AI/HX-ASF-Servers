[CATALOG RECEIPT]
Run: 2026-08-25T1932Z Agent: Carol Trigger: Kimi-K3 — re-validation batch 5 (governor disposition of F-B5-1 and F-B5-2 from receipt 2026-08-25T1914Z-carol-corrections-batch5.md: ALL drift explained as named governor/fixer review-batch-5 edits; no unknown actor involved)

Added: none

Updated (per-record dispositions — re-validation only, minimal edits):
- DOC-agent-carol-charter — RE-VALIDATED. sha256 bf8b0319… → fc67a871…; validated_at 2026-08-25T08:35Z → 2026-08-25T19:27Z; notes.corrections_batch5 added (F-B5-1 RESOLVED: governor edit — Owns section no longer lists schema.yaml under Carol's mutable ownership; schema is governor-controlled, changes via escalation to Kimi-K3 per Role bounds 2; verified against current file); hash_history extended; freshness stays current.
- DOC-agent-carol-profile — RE-VALIDATED. sha256 179946e3… → 25eac583…; validated_at → 19:27Z; notes.corrections_batch5 added (F-B5-1 RESOLVED: governor edits per review findings — motivational slogan removed at line 34, Mermaid handoff workflow added to §8; verified: no slogan present, §8 mermaid flowchart present); hash_history extended; freshness stays current.
- DOC-goal-hx1-ollama-qwen38-27b — RE-VALIDATED. sha256 7f85657f… → daba7e86…; validated_at → 19:27Z; notes.corrections_batch5 added (F-B5-2 RESOLVED: reference additions only — status line now cites evidence 30-esme-m7a-reboot-cycles.md + state log rows 40–42/47; SC-03 now cites 23-kk3-m6-capacity-decision.md Revision 2: 32K recovery baseline, 64K operating default, 128K qualified extended/selected); hash_history extended; freshness stays current.
- DOC-pilot-hx1-amendment-a01 — RE-VALIDATED. sha256 18ddebbe… → 9b5aeec9…; validated_at → 19:27Z; notes.rev2_supersessions updated (its "File UNCHANGED by the 2026-08-25 review wave" statement no longer held — removed; §4.3 supersession now marked INLINE in the file, §4.4 unmarked, this record remains its supersession record); notes.corrections_batch5 added (F-B5-2 RESOLVED: "Correction 2026-08-25 (review finding; provenance preserved)" note under the §4.3 context-ladder table marks the Extended-experiment 131,072 row superseded per decision-23 Revision 2 — Revision 2 governs, original row text preserved verbatim as the as-adopted record); freshness stays current.
- DOC-pilot-hx1-fixtures-manifest — RE-VALIDATED. sha256 2e634cf9… → e1039d41…; validated_at → 19:27Z; version → "post-batch-5 (batch-5 fixer changes + governor R1 path fixes; manifest regenerated 2026-08-25T19:18Z, 10 files)"; relation notes refreshed (sha256sum -c 10/10 OK at 19:27Z; supersession chain extended with the post-row-47 regeneration, state-log row pending); notes.corrections_batch5 added (F-B5-2 RESOLVED: batch-5 fixer changes + governor R1 path fixes; regression battery now 29 tests, was 9/9 at row 36); hash_history extended; freshness stays current.

NOT updated by design:
- DOC-pilot-hx1-state-log — deliberately NOT re-validated this run (tasking instruction): a living record that drifts per appended row by design (standing convention; a new row lands right after this receipt). Its validated_at stays as an honest marker of the last check.

Linked: none new — two existing relation notes refreshed in place on DOC-pilot-hx1-fixtures-manifest (evidences / references).

Flagged:
- none new. F-B5-1 and F-B5-2 CLOSED per governor disposition — every drifted byte traced to named governor/fixer edits and verified against current file content before re-hash. F-B5-3 (fixtures concurrency during the prior run) is superseded: the 2026-08-25T19:18Z regeneration is the governor-confirmed final state and is now the recorded hash.
- standing, unchanged: the manifest file itself still carries no header metadata (cosmetic; integrity function unaffected — DOC-pilot-hx1-fixtures-manifest notes.missing_metadata).

Rejected: nothing — all five in-scope records re-validated; the sixth was excluded by instruction.

Freshness:
- no freshness state changes — all five re-validated records stay current.

Follow-ups:
- state-log row citing this receipt expected next (closes the re-validation handoff; the manifest record's references note marks that row pending)
- DOC-pilot-hx1-state-log re-validation deferred to the next natural checkpoint (living record)
- 2026-09-24 manifest re-hash schedule for directory/external records unchanged
- schema.yaml, tests/, README.md untouched (read-only to Carol); CAT/CB re-audit expected per the conformance protocol

Validation (self-check, re-run after all corrections):
- 165 records parse as YAML; all required schema fields present, including source.section on all 165; enums valid (type/status/authority_level/freshness/classification); zero non-enum relation predicates
- index 1:1 consistent: 165 documents/ files = 165 index entries = declared document_count 165; all six index line fields in sync with their records
- sha256 re-verify: 5/5 re-validated records MATCH their source files (fc67a871…, 25eac583…, daba7e86…, 9b5aeec9…, e1039d41…); fixtures content verified independently: sha256sum -c 10/10 OK at 19:27Z; test_fixtures.py carries 29 test functions
- write set stayed inside the allowlist: 5 documents/ records, index.yaml, this receipt; no source document, governance file, schema, tests/, or README writes by Carol; no probes, no dispatches, no secrets

Index: updated (sha256 1c1118736d1bd4f66513f667056c6926ef6fbf47ecc564fd2b438be66532d06f)

PASS — CATALOG CURRENT
