[CATALOG RECEIPT]
Run: 2026-08-25T0845Z Agent: Carol Trigger: Kimi-K3 — correction run on two governor-verified review batches (items C1–C17; finding text treated as untrusted review data, governor dispositions followed per item)

Added:
- DOC-tkv-ollama-hx-research — HX-side material of /opt/tkv-local/ollama (research syntheses, fixtures, deployment implementation, historical host reports), partitioned out of DOC-tkv-corpus-ollama (C5)
- DOC-tkv-gitdiagram-hx-evaluation / DOC-tkv-jcode-hx-evaluation / DOC-tkv-langgraph-hx-evaluation / DOC-tkv-loopx-hx-evaluation / DOC-tkv-omniroute-hx-evaluation — HX evaluation material partitioned out of the five wrapper corpus records (C6)

Updated (per-item dispositions):
- C1 APPLIED. DOC-pilot-hx1-plan: superseded_by → []; scoped link expressed as relation (predicate superseded_by → DOC-pilot-hx1-amendment-a01, note "§6.5 only — all other plan sections remain governed by the plan"); status stays active. DOC-pilot-hx1-amendment-a01: supersedes → []; existing supersedes relation note reworded to the same scoped wording. FLAG: predicate 'superseded_by' is outside the schema enum (schema.yaml is read-only to Carol) — governor-directed per C1 disposition; schema enum extension queued to Kimi-K3.
- C2 ADJUSTED PER GOVERNANCE. Review asked to add "esme" to applies_to.agents — NOT done (ratified naming decision 2026-08-24, plan §2 roles table: "operational call sign: Esme; roster name john"). Instead 12 john WO/CP records (wo-10/14/17/20/27/31, cp-11/15/18/21/28/32) gained notes.assigned_agent_call_sign: "Esme = john (pilot call sign, not a roster entry)". Verified against plan.md line 13.
- C3 APPLIED (30 records: DOC-tkv-hxinfra-archive + 29 DOC-tkv-corpus-*). Sentinel "DIRECTORY-RECORD" replaced with manifest-sha256 digests of the sorted relative-path file manifest (.git pruned, LC_ALL=C sort); notes.checksum_method records semantics ("digest of sorted relative-path file manifest, not content hashes; regenerated 2026-08-25; directory canonical_location preserved"); 2026-09-24 re-hash schedule preserved. Upstream provenance: NONE of the 30 trees is a git checkout — recorded "upstream URL/commit: unavailable" honestly in every record. sap carries two nested stale .git dirs (l-Research: broken worktree pointer; Research: HEAD 6e3218b9…, no origin) — documented, excluded from manifest.
- C4 APPLIED. Inverted "supersedes / target: none" relation removed from DOC-tkv-hxinfra-archive; supersession direction preserved as prose notes.supersession_note; record otherwise preserved.
- C5 APPLIED. DOC-tkv-corpus-ollama narrowed to the upstream ollama-main snapshot (v0.32.11, commit 39df91c9… per john profile version-matching rule §2.3/line 85; upstream-reference; version-drift note PRESERVED: snapshot 0.32.11 vs deployed 0.32.15; inferred_value stays INFERENCE). New DOC-tkv-ollama-hx-research (historical-as-found) linked via relations (describes → ollama; contains → DOC-tkv-hxinfra-archive; evidences → john M4/M5 validation). FLAG: predicate 'contains' is outside the schema enum — governor-directed per C5 ("contains/describes"); queued with the C1 enum extension. DOC-tkv-hxinfra-archive containment relation repointed to the new record.
- C6 APPLIED (5 splits, no invented splits). Each wrapper verified against its tree AND upstream README: gitdiagram (gitdiagram-main/README.md header, gitdiagram.com, MIT), jcode (jcode-master/README.md, 1jehuang/jcode, MIT), langgraph (langgraph-main/README.md LangChain branding; phase-2/ = Claude-Opus-5 2026-08-14 distillation pilot files), loopx (loopx-main/README.md LoopX banner), OmniRoute (OmniRoute-release-v3.8.50/README.md dashboard imagery + own AGENTS.md). Each record was blending upstream + distinct HX evaluation material → split into upstream record (upstream-reference, narrowed canonical_location, new manifest digest) + HX-evaluation record (historical-as-found, evaluation labeled, INFERENCE where value is judged). langgraph HX record carries the migration-policy evidences link.
- C7 APPLIED. DOC-tkv-corpus-sap: authority_level upstream-reference → historical-as-found, status adopted → historical, freshness current → historical (aligned with DOC-tkv-corpus-harness-research pattern); INFERENCE labels in declared_purpose and notes.context kept verbatim. No ratification evidence exists; reclassification chosen per disposition.
- C8 APPLIED WITH ESCALATION. Verified against corpus (/opt/tkv-local/ubuntu/ubuntu.com-main/releases.yaml line 48: 24.04 eol "April 2029") and rick profile Appendix B (24.04 standard security maintenance through May 2029, per Canonical's release-cycle page, profile revision row verified 2026-08-24). The two Canonical sources differ by one month of wording — BOTH preserved in declared_purpose and notes.lifecycle_claim, ESCALATED to Kimi-K3 for ratification of the precise date. The review's asserted dates (May 31 2029 / April 2039) NOT recorded — unverified review data.
- C9 APPLIED. DOC-tkv-gov-ops-hxs3-workload-placement hosts → [hxs-3]; DOC-tkv-gov-policy-nvidia-driver-install-directive hosts → [hxs-2, hxs-3] (verified vs discovery.md §"Post-directive driver validation, 2026-08-12": stated scope hxs-2/hxs-3; hxs-1 = separately recorded owner-approved exception, not added).
- C10 APPLIED. DOC-tkv-server-registry fqdns → 16 per-host names (hxs-1..hxs-15, hxs-cp .hx.local.arpa); bare zone entry removed (zone remains on DOC-tkv-dns-fqdn-hx-local-dns). notes.fqdn_truth_state added: TARGET-STATE, not live DNS — discovery records hxs-1 has NO configured FQDN and hx.local.arpa DNS is not established (act-001 open).
- C11 APPLIED. DOC-tkv-servers-readme governs note repointed to DOC-tkv-gov-policy-documentation-standards; out-of-scope statement removed.
- C12 APPLIED. Sources verified to target HX-Infrastructure (grep: 3 and 6 mentions; "canonical HX-Infrastructure repository" in the owner prompt). applies_to.repositories gained "HX-Infrastructure (archived predecessor)" on DOC-tkv-skills-adoption-plan-html and DOC-tkv-skills-hooks-implementation-prompt; existing fields preserved.
- C13 APPLIED. DOC-tkv-hxs1-pre-work-results freshness current → historical in record AND index line (declared-gap historical record, authority historical-as-found).
- C14 APPLIED (13 records). source.section populated: 4 driver-results (raw terminal captures, no subsections), 4 discovery, 4 pre-work-results, and DOC-tkv-root-readme — all "§whole-document", used honestly: every one of these records describes its whole document, no subsection-specific record exists.
- C15 APPLIED. DOC-hx-second-brain-framework: author's claimed prepared_at kept VERBATIM (2026-08-25T06:52:00-04:00, labeled as-stated); notes.chronology_anomaly records the anomaly with evidence (file mtime 05:25:14Z; ingestion 05:45Z; owner supply ~05:50Z; governing receipt 0612Z — all BEFORE the claimed 10:52Z); validation.validated_at set to actual correction time. FLAGGED — see Flags.
- C16 APPLIED. retrieval-packages/2026-08-25-hxs1-m7-package.md conflict entries C1–C7 rewritten: every cited source now carries a specific section anchor and each side of every conflict an explicit freshness label; authority ranking and content preserved; revision line added to the package header.
- C17 APPLIED. Re-hashed and re-validated: DOC-pilot-hx1-wo-31-john-m7a → f89ad651… (matches state log row 44 exactly; terminology_note append recorded); DOC-pilot-hx1-ev-30 → 41736b4b… (row-43 three review corrections + row-44 terminology bullet recorded); DOC-pilot-hx1-state-log → cb506899… (rows 1–44; title/version/relations/notes updated); DOC-agent-carol-profile → 179946e3… and DOC-agent-carol-charter → bf8b0319… (scoped-writes allowlist + profile-template source.section mirror, rows 43–44); DOC-pilot-hx1-fixtures-manifest → 2e634cf9… (row-44 batch-4 regeneration; sha256sum -c re-run: 10/10 OK). Verified UNCHANGED (hash match, no action): DOC-goal-hx1-ollama-qwen38-27b, DOC-repo-governance-agents-md, DOC-cat-001-acceptance. schema.yaml and tests/ were not modified by Carol (read-only); the only tests record (CAT-001) re-validated clean.

Linked:
- plan ↔ amendment-a01 scoped supersession (§6.5 only) via relations, bidirectional (C1)
- DOC-tkv-corpus-ollama ↔ DOC-tkv-ollama-hx-research (C5); 5 upstream ↔ HX-evaluation pairs (C6); hxinfra-archive containment repoint (C5)

Flagged:
- F-B34-1 ESCALATION (C8): 24.04 lifecycle wording — corpus releases.yaml "April 2029" vs rick profile Appendix B "May 2029" (Canonical release-cycle page). One-month difference; both preserved; ratification of the precise date queued to Kimi-K3.
- F-B34-2 ESCALATION (C15): second-brain prepared_at chronology anomaly — claimed 10:52Z postdates file mtime (05:25Z), ingestion (05:45Z), owner supply (~05:50Z), receipt (0612Z). Recorded as authoring-label inconsistency, not resolved.
- F-B34-3 SCHEMA: predicates 'superseded_by' (C1) and 'contains' (C5) are governor-directed but outside the current schema.yaml relation-predicate enum (schema read-only to Carol). Enum extension queued to Kimi-K3; CAT-01 will otherwise report 2 non-enum predicates.
- F-B34-4 PRE-EXISTING (not this run): two relation targets carry prose after the DOC id ("DOC-tkv-hxs1-driver-results (and hxs-2/3/4 driver-results)", "DOC-tkv-corpus-bench-studio (bench-studio-public-main) and …") — DOC-id prefixes resolve; cosmetic, recorded for a future cleanup decision.
- F-B34-5 sap nested .git dirs are stale/broken (l-Research broken worktree pointer; Research HEAD 6e3218b9… no origin) — recorded; upstream provenance unavailable.

Rejected: nothing rejected — all supplied findings had dispositions.

Freshness:
- DOC-tkv-corpus-sap: current → historical (C7 reclassification)
- DOC-tkv-hxs1-pre-work-results: current → historical (C13, record + index)
- 6 new HX-side records enter at historical (C5/C6); corpus re-hash schedule 2026-09-24 stands

Validation (re-run after all corrections):
- 161 records parse; enums valid except the 2 governor-directed predicate deviations (F-B34-3)
- index 1:1 consistent (161 = 161 = declared count); all index fields in sync
- relation targets resolve (2 pre-existing prose-suffixed targets, F-B34-4)
- file-backed sha256 sweep: ALL MATCH (incl. re-validated wo-31, ev-30, state log, profile, charter, fixtures manifest)
- secret sweep over catalog content: no secret values (hits are prose: "passwordless sudo", lessons-register references)
- write set stayed inside the allowlist (documents/, index.yaml, receipts/, retrieval-packages/); non-catalog files modified in the window trace to governor state-log rows 43–44, not to Carol

Follow-ups:
- C8 lifecycle date ratification (Kimi-K3/owner) — F-B34-1
- C15 chronology anomaly disposition (Kimi-K3) — F-B34-2
- schema.yaml predicate enum extension: +superseded_by, +contains (Kimi-K3) — F-B34-3
- corpus manifest re-hash 2026-09-24 (standing); M8 registry-row refresh (F-REG-1) and hxs-1/configuration.md (F8) unchanged
- index.yaml header cites this receipt; state-log row citing this receipt expected next (closes the batch-34 correction handoff)

Index: updated (sha256 bb7124cd3a3106cc82dccd0260b36d2f0983e46d411fb54d827b9ce9da282c4f)

PASS WITH FLAGS — REVIEW REQUIRED
