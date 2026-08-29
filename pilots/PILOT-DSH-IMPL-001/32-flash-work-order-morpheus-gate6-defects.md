# WORK ORDER — Morpheus: diagnose and fix Gate 6 defects (governor fix window)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Morpheus (dsh lifecycle steward, KDD-0009).
- Lane: `omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B, DeepInfra, via OmniRoute).
- Target: hxs-15 (192.168.50.214).
- Authority: Governor fix window — the hard boundary is lifted for defect fixes only. Campaign fingerprint must be preserved after fixes.

## Intent

Gordon ran Gate 6 (23 tests, 55s). 7 PASS, 14 FAIL, 2 SKIP. Three defect categories:

### Defect 1 — Systemic exit-code/headless-completion (9 tests affected)

**Tests:** G6-01, G6-02, G6-04, G6-05, G6-08, G6-10, G6-12, G6-14, G6-19

**Symptom:** In all 9 tests, the dsh process performs the tool activity (markers seen, tool calls present, evidence in the session log), but exits with code 1 every time. The oracle checks the exit code and fails. The actual work appears to have been done — the failure is in the exit/completion path, not the feature.

**Gordon's assessment:** Systemic exit-code/headless-completion candidate defect — not 9 independent feature failures. A single fix in the exit path could clear all 9.

**Your job:** Diagnose why dsh exits with code 1 when the session work is complete. Check the headless profile's completion handling — does it expect a specific exit signal? Is there a turn-end vs session-end mismatch? Is the exit code 1 coming from the dsh process itself, the model API call, or a shell wrapper? Once diagnosed, fix it.

### Defect 2 — Schedule events missing (1 test)

**Test:** G6-11 (schedule_one_shot)

**Symptom:** `schedule_change_events=0`, elapsed 1s. The schedule fixture was mounted but no schedule events were produced.

**Your job:** Diagnose why the schedule plugin doesn't emit events. Check if the fixture-mounted schedule row is correctly loaded, if the reminder instruction reaches the model, and if the schedule event is durably logged.

### Defect 3 — Live recomposition doesn't retain last-good config (1 test)

**Test:** G6-18 (live_recomposition)

**Symptom:** After injecting an invalid edit to the composition target, health returns 200 (server stays up) but `last_good_retained=False` — the candidate accepted or dropped the invalid recomposition instead of retaining the last-good config.

**Your job:** Diagnose the recomposition fallback behavior. When an invalid composition is submitted, does the harness keep the last-good config or replace it? Fix the fallback to retain last-good.

### Blocked item (not a defect — environment setup)

G6-17 is BLOCKED on missing `/var/lib/dsh/gordon/g1-source-copy`. This needs a G1 run in this window to re-establish the source copy. Run G1 first, then G6-17 can be dispositioned.

## Constraints

- Fix window: you may mutate the candidate on hxs-15 to fix defects.
- After fixes: re-run the affected tests to verify the fix.
- Campaign fingerprint: record the state before and after fixes. Gordon will re-run Gate 6 to confirm.
- Do NOT touch test files — those are Gordon's lane.
- `scripts/validate.py` 4/4 after any repo writes.
- SSH: askpass pattern (HX_SSH_PASSWORD from .local.env, 0700 helper, deleted after).
- The test files are at `/home/hxsa/gordon/phase-b/` on hxs-15.
- Run tests with: `cd /home/hxsa/gordon/phase-b && OMNIROUTE_API_KEY=$(sudo cat /var/lib/dsh/.env | grep OMNIROUTE_API_KEY | cut -d= -f2) python3 -m pytest test_g6_orchestration.py -ra`

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with: diagnosis per defect, fix applied, test results after fix, fingerprint before/after.
`[TASK PAUSED — ESCALATION TO GOVERNOR]` if diagnosis requires more than the fix window allows.
