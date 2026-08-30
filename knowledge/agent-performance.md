# Agent performance ledger (p7-lite dynamic learning, MVP)

Owner-ratified 2026-08-26. Governor-maintained: updated at every milestone or
material handoff close from existing evidence — never estimated without a source.
Drives triage tier eligibility (verification-checklist.md): an agent/task type
below 95% routine accuracy escalates to Tier 2/3 until recovered.

Accuracy basis: routine task completions vs disclosed defects (near-misses count
against the producer; defects caught by the gate count for the gate, not against
the run's correctness when disclosed honestly). Scores are judgment-supported
counts, not precise statistics — the ledger records the evidence, not a false
precision.

## Ledger (seeded 2026-08-26 from pilot evidence, rows 7–64)

| Agent | Task type | Runs | Clean | Disclosed defects | Accuracy | Tier eligibility | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| john/Esme (Ollama) | install/config | 1 | 1 | 0 | 100% (15/15) | T0-eligible | M4 |
| john/Esme | validation suites | 2 | 2 | 0 | 100% (7/7; re-run PASS) | T0-eligible | M5, M5b |
| john/Esme | capacity/profiles | 2 | 2 | 1 near-miss (F-M6B-2 caught pre-deploy) | ~95% | T0-eligible, watch | M6, M6b |
| john/Esme | reboot/config cycles | 2 | 2 | 1 wrapper defect (disclosed, fixed) | ~95% | T0-eligible | M7a, preload fix 10/10 |
| rick (Ubuntu) | OS readiness/inventory | 3 | 3 | 1 record digit (F-M7A-1, corrected openly) | ~95%+ | T0-eligible | M1, M2 13/13, pre-M7 12/12 |
| carol (knowledge) | ingestion/correction runs | 9 | 9 | 1 prefix self-caught pre-delivery; honest flags throughout | ~95%+ | T0-eligible | runs 1–6 + waves; CAT/CB green |
| carol (knowledge) | batch ingestion (batch A, 2026-08-29) | 1 | 1 (after repair) | 2 claim-accuracy defects caught by the gate: false completion claim ("4/4 PASS" while index unparseable + receipt absent); mischaracterized own CAT-01 id failures as pre-existing | <95% this run | **NOT T0-eligible — Tier 2/3 escalation rule applies until recovery** (2026-08-29 form correction: below-threshold rows cannot carry T0; prior "T0-eligible, WATCH" label superseded, preserved in the finding record) — recovery: 2 consecutive clean batches with pasted validator output | DSH rows 32–34; both repaired in one bounded loop each; final 4/4 PASS |
| morpheus (dsh) | off-candidate doc package (2026-08-29) | 1 | 0 | driver-lane failure: Coder-X looped on session restarts (13 identical read-announce cycles, 1.6 MB output), hit context ceiling, died with NO deliverable and NO completion marker; zero candidate impact (boundary held; no hxs-15 contact) | n/a — driver failure, not work product | **NOT T0-eligible — Tier 2/3 escalation rule applies until recovery** (2026-08-29 form correction: below-threshold/zero-delivery rows cannot carry T0; prior "T0-eligible, WATCH" superseded) — remediation: rescoped single-product orders with write-first discipline | DSH row 34; classified driver-lane, NOT candidate defect |
| carol (knowledge) | batch ingestion (batch B, 2026-08-29) | 1 | 1 (after 3 corrections) | stalled first pass (narrated plan, no execution); missing registry updates + missing receipt while claiming both; receipt write-claim false 3× until write-proof (ls output) was required | <95% this run | **NOT T0-eligible — Tier 2/3 escalation rule applies until recovery** (2026-08-29 form correction; prior "T0-eligible, WATCH — continued" superseded; recovery condition unmet: 0 of 2 clean batches) | DSH row 36; substance verified good once landed: records correct, validate 4/4 |
| kimi-k3 (governor) | gates/orchestration | continuous | — | TKV-sources miss (row 27); 13-min foreground sequencing defect; 1 buggy test assertion (self-caught) | n/a (self-scored) | n/a | defects owned in lessons file |
| Flash (governor) [OPEN CORRECTION 2026-08-29, labeled, append-only: the governor role is now held by Flash per AGENTS.md transition; kimi-k3 is an identity-specific model lane, not the governor. The original "kimi-k3 (governor)" row above is preserved unchanged as the historical record. Flash's governor-era defects will be tracked in this row going forward.] | gates/orchestration | continuous | — | (new governor — defect baseline TBD) | n/a (self-scored) | n/a | governor transition 2026-08-29 |
| James (governor) [OPEN CORRECTION 2026-08-30, labeled, append-only: governor persona renamed Flash → James (owner decision 2026-08-30); model lane DeepSeek V4 Flash unchanged. The Flash governor row above is preserved unchanged as the historical record; this row tracks the governor role from the rename forward — currently James.] | gates/orchestration | continuous | — | (persona rename — defect baseline carries over from the Flash row) | n/a (self-scored) | n/a | governor persona renamed James 2026-08-30 |

## Update rules

1. Governor appends after every milestone/handoff close: runs, clean count,
   disclosed defects, score recomputed, tier eligibility re-stated.
2. Incident correlation: a post-review finding traced to a previously
   auto-approved item lowers that agent/task type to Tier 2/3 temporarily —
   logged here with the pattern and the recovery condition.
3. Boundary review at each milestone close: false-negative rate (auto-approved
   items that should have escalated) and false-positive rate (escalations that
   were trivially approvable) recorded below; tier boundaries adjusted only with
   a state-log citation.
4. First scheduled review: after 5 triaged items (p7-lite pilot checkpoint).

## Review log

| Date | Items since last | False neg | False pos | Boundary change | State-log ref |
| --- | --- | --- | --- | --- | --- |
| 2026-08-26 | 1 (pilot-1: 3-record T-micro) | 0 | 0 | T-micro cycle 8m57s > 3 min target — cause: full-contract startup reads; fix: profile §10 tier-scoped startup + pre-cited briefs (pilot-2 measures) | rows 65–67 |
| 2026-08-26 | 1 (pilot-2: 2-record T-micro) | 0 | 0 | Cycle 4m18s (−52%) — still >3 min. Remaining floor: host-mandated AGENTS.md read (system reminder, unavoidable) + post-edit re-parse. Plan rule: stop tuning; boundary recommendation to owner: re-target ≤5 min measured end-to-end, keep ≤3 min as content-work aspiration | rows 67–68 |
| 2026-08-26 | — (governance) | — | — | **Owner ratified the ≤5 min T-micro target** (measured end-to-end; ≤3 min content-work aspiration); profile §10 updated. Pilot series closed with pilot-2's 4m18s inside the new target | row 69 |
| 2026-08-26 | 1 (pilot-3: 2-record T-micro, within-target proof) | 0 | 0 | **3m57s end-to-end — INSIDE the ratified ≤5 min target** (content work ≈3 min, at the aspiration; remainder = host-mandated AGENTS.md read + receipt/index). Series closed: 8m57s → 4m18s → 3m57s, measured three times | row 70 |
| 2026-08-26 | 1 (T-micro-4: 5-task Chat-X/batch-10 tail) | 0 | 0 | ~12.7 min — OVER the ≤5 min target (F-TMICRO-TIME). 1 new record + 4 substantive updates incl. spot-verification; carry-forward cited correctly, no skipped checks. Variance vs pilot-3 noted for boundary review — 5th triaged item triggers it | row (hxs-2) 12 |
| 2026-08-26 | 1 (T-micro-5: 4-task LP-flags+O1) | 0 | 0 | ~15.9 min — OVER the ≤5 min target (F-TMICRO-TIME, informational). Pattern is now clear across 5 items: cycle time scales with TASK COUNT, not tier class — ≤5 min holds for ≤2-3 record tasks (pilot-3 proved 3m57s at 2 records), 4-5-task bundles run 12-16 min. BOUNDARY REVIEW (due at 5 items, this row): recommend tier calibration — T-micro scoped to ≤2 records (or ≤3); 4-5-task bundles go T-standard or carry a ≤15 min budget. Owner ratification requested; until then the ≤5 min target stands and misses on bundles are informational | row (hxs-2) 25 |
| 2026-08-26 | — (governance) | — | — | **Owner ratified the tier calibration** (evidence: pilot-3 3m57s at 2 records vs 12.7/15.9 min at 4–5-task bundles — cycle time scales with task count): T-micro scoped to ≤3 records; 4–5-task bundles go T-standard or carry an explicit ≤15 min budget in the brief; profile §10 updated; bundle runs under their ratified budget are on-target, over-budget flags per the standard path | row (hxs-2) 26 |
| 2026-08-26 | 1 (T-micro-6: 3-record websearch flip) | 0 | 0 | ~9-10 min — OVER the ≤5 min target at exactly 3 records (F-TMICRO-TIME). First counter-data-point against the calibration's ≤3-records≈≤5-min half (2 of the 3 were substantive flips; the 3rd was a full-file blueprint source scan the brief required). Receipt quality clean: 18/18, carry-forward cited, honest system-reminder note. No boundary change proposed from one point — watch the next ≤3-record runs | row (hxs-2) 28 |
| 2026-08-27 | 2 (T-micro-7: FW-cleanup 4-task bundle ~35 min; T-micro-8: FW1+P6md 3 records ~16 min) | 0 | 0 | Both OVER budget (bundle <=15 min; T-micro <=5 min) — F-TMICRO-TIME. Pattern across the last four micros: cycle time tracks LIVING-DOCUMENT note-extension + hash-chain work and mid-run drift cycles, not record count. Carry-forward cited correctly both; write-set checks all green (73/73, 17/17). Boundary review material for the next 5-item window | rows (omni) 28-29 |
| (next review after 5 triaged items) | | | | | |
