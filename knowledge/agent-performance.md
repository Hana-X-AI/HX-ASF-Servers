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
| kimi-k3 (governor) | gates/orchestration | continuous | — | TKV-sources miss (row 27); 13-min foreground sequencing defect; 1 buggy test assertion (self-caught) | n/a (self-scored) | n/a | defects owned in lessons file |

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
| (next review after 5 triaged items) | | | | | |
