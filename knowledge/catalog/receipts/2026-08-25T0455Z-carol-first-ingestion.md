[CATALOG RECEIPT]
Run: 2026-08-25T0455Z Agent: Carol Trigger: Kimi-K3 dispatch — first ingestion run (owner amendment 2026-08-25; state log row 28)
Note: the pilot stayed live through this run. This receipt closed at 2026-08-25T0525Z and covers the mid-run revision wave (state log rows 30–34) in the same run.

Added: (62 records, all new — first ingestion)

Repo governance (11)
- DOC-repo-governance-agents-md — repository AGENTS.md: skills, communication contract, stewardship amendment, Secure Boot directive
- DOC-agents-roster-readme — agents/README.md roster authority + explicit agent-authority precedence rule (rev hash ef8b1c1c…)
- DOC-agent-rick-charter / DOC-agent-john-charter / DOC-agent-kimi-k3-charter / DOC-agent-carol-charter — lane charters (type charter per updated schema)
- DOC-agent-rick-profile / DOC-agent-john-profile / DOC-agent-kimi-k3-profile / DOC-agent-carol-profile — full operating contracts (carol profile rev hash 77384cfe…: receipt naming fixed, rejected status added)

Goal (1)
- DOC-goal-hx1-ollama-qwen38-27b — durable goal record; status line current with the owner profile disposition (32K recovery / 64K operating / 128K extended; M6b running→complete; M7 staging next)

Pilot corpus PILOT-HX1-OLLAMA-QWEN27B-001 (32)
- DOC-pilot-hx1-plan — adopted plan (rev hash 0d740a49…: §5.3 Extended row RESOLVED to the Rev-2 rule; §6.5 blocks marked non-executable provenance)
- DOC-pilot-hx1-amendment-a01 — Amendment A01 adopted 2026-08-25 (supersedes plan §6.5 ONLY; §4.3 131,072-row and §4.4 bare-alias identity since superseded by Rev-2 — recorded)
- DOC-pilot-hx1-state-log — governor transition log rows 1–34 (living log; hash captured 05:25Z)
- DOC-pilot-hx1-decision-23-m6-capacity — KK3 gate REVISION 2: three qualified profiles (32K recovery / 64K operating / 128K explicit-select); v1 freeze superseded before execution; needle corrected to 30,015
- DOC-pilot-hx1-fixtures-manifest — fixtures/sha256sums.txt (9/9 verified OK at ingestion)
- Work orders (all produced_by kimi-k3, each governing its paired deliverables): DOC-pilot-hx1-wo-01-rick-m1, -wo-05-rick-m2, -wo-10-john-m4, -wo-14-john-m5, -wo-17-john-m5b, -wo-20-john-m6, -wo-24-rick-pre-m7, -wo-27-john-m6b (arrived mid-run 04:56Z; discharged row 34)
- Context packets: DOC-pilot-hx1-cp-02a-rick-m1, -cp-06-rick-m2, -cp-11-john-m4, -cp-15-john-m5, -cp-18-john-m5b, -cp-21-john-m6, -cp-25-rick-pre-m7 (carries the review-batch superseded_note), -cp-28-john-m6b (arrived mid-run)
- Evidence: DOC-pilot-hx1-ev-03-rick-tkv-receipt (M1, proceed YES); -ev-04-rick-inventory (M1 immutable baseline); -ev-07-rick-os-readiness (M2, 13/13); -ev-08-rick-risk-handoff (signed 00:15Z); -ev-12-esme-m4-install (15/15; concurrency annotation per review batch); -ev-13-esme-rollback (runbook; Layer D scoped per review batch); -ev-16-esme-m5-validation (7/7 on sampled-profile alias — comparison, NOT acceptance); -ev-19-esme-m5b-conformance (Phase A frozen; M4 identities SUPERSEDED; 32K acceptance); -ev-22-esme-m6-capacity-ladder (both rungs PASS; prefill header corrected per review batch); -ev-26-rick-pre-m7-readiness (12/12; A01 §7 SATISFIED; handoff row 29 open pending this receipt); -ev-29-esme-m6b-profiles (aliases + 64K operating default proven; handoff row 34 open pending this receipt)

TKV server records (6)
- DOC-tkv-servers-records-contract; DOC-tkv-servers-readme; DOC-tkv-server-registry (15 rows, Phase 1 COMPLETE / Phase 2 READY); DOC-tkv-hxs1-discovery (as-found 2026-08-11, historical-as-found); DOC-tkv-hxs1-driver-results (2026-08-12, historical-as-found); DOC-tkv-hxs1-pre-work-results (declared gap, accepted)

Corpus (2)
- DOC-tkv-corpus-ubuntu — /opt/tkv-local/ubuntu (ubuntu.com-main; 2,127-file name-manifest hash)
- DOC-tkv-corpus-ollama — /opt/tkv-local/ollama (v0.32.11 snapshot + research; 1,816-file name-manifest hash; aging — version drift disclosed)

Protected resource (1)
- DOC-protected-ssh-info-hxs1 — existence, owner (Agent Zero), askpass retrieval pattern ONLY; contents never accessed; contains_secret_values: true

Amendment origin (1)
- DOC-a01-origin-codex-20260824-2125 — Codex original of A01; historical; superseded_by the adopted repo copy (body verified verbatim except one cosmetic separator cell)

Knowledge base (9)
- DOC-knowledge-readme; DOC-knowledge-issues; DOC-knowledge-lessons-learned; DOC-knowledge-network (aging — FQDN state unverified since 2026-08-24); DOC-kdd-0000-template; DOC-kdd-0001-kimi-k3-meta-agent; DOC-kdd-0002-goal-setting-guidance; DOC-kdd-0003-ollama-audit-pilot; DOC-kdd-0004-hx1-qwen-pilot-adoption

Updated: (during this run, after the mid-run review wave — records revised in place with prior hashes preserved in notes)
- DOC-pilot-hx1-decision-23-m6-capacity — rewritten for Revision 2 (v1 hash 2925b26c… → Rev-2 7cb2dc31… → review-batch 1bc756cb…, chain recorded)
- DOC-pilot-hx1-plan — re-hashed 0d740a49…; §5.3/§6.5 correction notes
- DOC-pilot-hx1-cp-25-rick-pre-m7 — re-hashed d8d0f404…; appended superseded_note recorded
- DOC-pilot-hx1-ev-22 / -ev-12 / -ev-13 — re-hashed; review-batch annotations recorded (prefill header; command-log concurrency; Layer D scope)
- DOC-goal-hx1-ollama-qwen38-27b — re-hashed 69f6193d…; status line now current with Rev-2
- DOC-agent-carol-profile / DOC-agents-roster-readme — re-hashed; review-batch changes recorded
- DOC-pilot-hx1-amendment-a01 — file unchanged; Rev-2 supersession notes added to the record
- DOC-pilot-hx1-wo-24-rick-pre-m7 — Rev-2 M7-objective context noted (WO file unchanged)
- Four charter records re-typed profile→charter per the updated schema (row 33's pending item, closed)
- DOC-pilot-hx1-state-log — re-hashed twice as rows 30–34 landed (1c821971… → 04984ccf… → 16b8fe64…)
- index.yaml — rebuilt twice (59 → 62 documents)

Linked: (principal edges; full graph in the records)
- amendment-a01 -[supersedes]-> plan (§6.5 ONLY — verified via in-place banner + adoption header)
- amendment-a01 -[produced_by]-> DOC-a01-origin-codex-20260824-2125 (verbatim adoption; one cosmetic separator-cell diff recorded)
- decision-23 Rev-2 -[decides]-> three-profile disposition; -[supersedes]-> A01 §4.3 131,072-row + §4.4 bare-alias identity + M6 v1 freeze (before execution); -[depends_on]-> ev-22, ev-19, ev-16 (as tasked and verified in the decision's Evidence field); -[governs]-> wo-27 (M6b) and M7 scope
- Work orders 01/05/10/14/17/20/24/27 -[produced_by]-> kimi-k3; -[governs]-> paired deliverables (01→03/04; 05→07/08; 10→12/13; 14→16; 17→19; 20→22; 24→26; 27→29)
- ev-19 -[supersedes]-> Modelfile dac63d7c…d1df and alias digest 23508b9c…185a8 (M4, recorded in ev-12) — VERIFIED in 19 §4; Phase A 4869ce80…/db2c6206… CURRENT
- ev-29 -[supersedes]-> bare alias hx-qwen3.8-27b (retired, tags only — implements Rev-2's A01 §4.4 supersession)
- ev-07 -[references]-> discovery (PCIe x16/x4 re-confirmation; state log row 27)
- All pilot work orders -[depends_on]-> DOC-protected-ssh-info-hxs1 (askpass path)
- KDD-0001→kimi-k3 profile; KDD-0004→plan/goal; state log rows 29/34 -[depends_on]-> this receipt

Flagged: (each with provenance; nothing guess-resolved)
- F1 §6.5 supersession chain — VERIFIED as tasked: plan.md §6.5 banner (now also marked non-executable provenance), A01 adoption header 'Plan impact', state log row 16 CONFLICT + M5b disposition, 19 §4 supersession table. Chain complete and consistent.
- F2 x4/x16 provenance correction — VERIFIED: discovery.md (2026-08-11) already recorded 02:00.0 x16 / 81:00.0 x4-of-max-x16; 07 §6.3 re-captured identical widths 2026-08-25; state log row 27 corrected the M2 'new FACT' framing to 're-confirmed'. Records AGREE. Link SPEED differs (2.5 GT/s idle vs Gen4) — power-state variance, not a contradiction.
- F3 discovery freshness vs live state — LABELED: discovery is historical-as-found and valid as such; mutable lines stale against later events: '34 packages upgradable' (08-11; kernel 7.0.0-30 staged by 08-25), 'no Ollama installed' (0.32.15 at M4), Wi-Fi enabled-DOWN (soft-blocked pre-M7). Record preserved unchanged per the server records contract.
- F4 pre-work-results declared gap — CONFIRMED deliberate declaration, not an oversight; retrospective pointer recorded.
- F5 TASKING DISCREPANCY — dispatch stated 26-rick-pre-m7-readiness.md 'does not exist yet (in flight)'. Verified complete on disk 04:41Z (signed 04:37Z, 12/12 PASS); state log row 29 (04:43Z) records pre-M7 complete, handoff OPEN pending Carol's receipt. Ingested in full; this receipt closes row 29's condition. Kimi-K3 to reference this receipt in the state log (Carol does not write the governor's log).
- F6 A01 origin vs adopted copy — 'verbatim' claim verified at content level; exactly one cosmetic markdown separator-cell differs (§4.3 table). Recorded.
- F7 Registry hxs-1 row stale wording — 'Qwen 3.8 27B — unreleased, slot reserved' vs released-and-deployed reality; KDD-0004 explicitly required no registry amendment. Governance-tolerated stale text; owner decision and live evidence outrank the row. Escalate to Kimi-K3 for awareness; refresh at next registry amendment.
- F8 Phase-3 guard tension — registry retains 'Phase 3 mutation guard hard-locked' while the owner-authorized pilot configures hxs-1's ratified workload. Owner directive outranks the guard text (no contradiction to resolve), BUT hxs-1's configured state lives only in the pilot corpus until hxs-1/configuration.md is created at M8 (owner-approved, row 28). ESCALATED to Kimi-K3; review at M8.
- F9 Missing metadata — fixtures/sha256sums.txt carries no header (date/author/scope) — context only via state log rows 21/24. Observed out of scope: /opt/tkv-local/README.md describes the 'Bench Studio Ownership Kit', not the vault — misleading vault-root README. driver-results.md is a headerless raw capture (acceptable per server records README evidence rules).
- F10 network.md aging — FQDN state DISCOVERED 2026-08-24 (NXDOMAIN after router restart; recovered same morning); unverified since. Review 2026-09-01.
- F11 Corpus drift — ollama corpus snapshot v0.32.11 vs installed 0.32.15 (hxs-1) and 0.32.9 (hxs-4, open issue D2). Record labeled aging; drift already disclosed in every john receipt.
- F12 Hash chains verified — WO-20 dd1e8e59…→d3b82a5c… (rows 19→22); fixtures manifest 3204614a…→38a9ac24… (rows 21→24); decision-23 2925b26c…→7cb2dc31…→1bc756cb… (v1→Rev-2→review correction). All intact; preserved as history.
- F13 MID-RUN REVISION WAVE — the pilot advanced during ingestion: rows 30–34 landed 04:56–05:16Z, including the owner profile disposition (Rev-2 supersedes the M6 v1 freeze BEFORE EXECUTION — the '131,072 frozen conditional on M7' state this run was dispatched under is no longer governing; M7 now validates the always-on 64K operating profile + 128K profile-switch mechanics, fallback 32K recovery), the M6b milestone commissioned and completed, the CodeRabbit review batch (8 documents corrected), the schema/profile updates (charter type, rejected status, receipt naming), and the owner-directed TKV-wide catalog sweep (run 2). All wave artifacts were ingested in-run; records revised with hash chains preserved. Row 33's pending item for Carol (four charter-record type updates + index population check) is CLOSED by this run.

Rejected: none. Every supplied document received a recorded disposition.
Deferred (observed, out of run-1 scope — queued for the owner-directed run-2 sweep per state log row 32): agents/john/codex_20260824_0205_ollama-directory-reconnaissance-inventory.md (john charter's foundational evidence); agents/kimi-k3/goal-setting-guidance.md (KDD-0002 adopted artifact); agents/_template/; goals/README.md, goals/_template.md, goals/2026-08-24-ollama-audit-hxs4.md, goals/2026-08-24-ollama-audit-hxs5.md; pilots/PILOT-KK3-JOHN-OLLAMA-AUDIT-001/ and -002/ trees; HX-ASF-Servers/servers/ tree; scripts/README.md, tests/README.md, pilots/README.md; fixtures/*.py (covered by DOC-pilot-hx1-fixtures-manifest); /opt/tkv-local/dns-fqdn/hx-local-dns-and-fqdn-access.md; /opt/tkv-local/README.md (F9); the Claude-Opus-5 hxs-1 discovery retrospective referenced by pre-work-results.md; all other /opt/tkv-local top-level trees (~90K files — corpus-level records per row 32).

Freshness: (closing assignments)
- historical: DOC-tkv-hxs1-discovery, DOC-tkv-hxs1-driver-results, DOC-a01-origin-codex-20260824-2125
- aging: DOC-knowledge-network (F10), DOC-tkv-corpus-ollama (F11)
- stale-detail-on-historical-record: discovery mutable lines (F3)
- current: all other 57 records

Follow-ups:
- IMMEDIATE (handoff closure): Kimi-K3 to reference this receipt in 09-state-log.md — closes the pre-M7 handoff (row 29, for 26-rick-pre-m7-readiness.md) and the M6b handoff (row 34, for 29-esme-m6b-profiles.md).
- ESCALATED TO KIMI-K3: F8 (Phase-3 guard timing; review at M8 when hxs-1/configuration.md is created), F7 (registry wording awareness), F13 (Rev-2 supersession is now the governing context rule — all future packets must cite 32K/64K/128K profiles, not the v1 freeze).
- Run 2 (owner-directed, state log row 32): TKV-wide catalog sweep — corpus-level records for all source-snapshot trees, document-level for HX-operational trees (servers, dns-fqdn, file-share, skills, governance material), plus this receipt's Deferred list. .git excluded.
- 2026-09-01: recheck FQDN state (DOC-knowledge-network); review knowledge/issues.md items.
- 2026-09-24: re-hash corpus manifests (ubuntu, ollama) or on any corpus update.
- At M7: Wi-Fi-disable persistence empirical confirmation (ev-26); M7 validates the 64K operating profile + 128K profile-switch mechanics (Rev-2); re-ingest M7 evidence and resolve the decision record's condition.
- At M8: ingest hxs-1/configuration.md (closes F8); registry row wording (F7); unified evidence index; fixtures manifest re-check after the fixer session lands (row 33).
- Fixture findings: a fixer session with regression tests was dispatched (row 33); sha256sums.txt will change — re-ingest on landing.
- Open owner question carried (not Carol's to resolve): 192.168.50.220 foreign client presence on hxs-1 — M7 exclusive-window entry condition (ev-26 §9, ev-29 §13).
- parse_kv fixture defect carried to the KK3 fixture decision (ev-29 §13).

Index: updated (sha256 416b00dfcdde0a5e436424c2c4c8fb474180d88a1c8c0cfea179252a012f8f1f) — 62 documents indexed; population verified against documents/ (62/62, schema-valid).

Completion: PASS WITH FLAGS — REVIEW REQUIRED
