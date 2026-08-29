# WORK ORDER — Mia: review-finding intake batch 2 (57 findings)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Mia (Chief of Staff, KDD-0012).
- Lane: `omniroute/glm-5.3-flash` (GLM 5.3 Flash, Modal, via OmniRoute hxs-8).

## Intent

A second review batch of 57 findings landed against ~20 files. Per your
charter (review-finding intake, state-log row 23): verify each finding
against current state, separate valid from stale or already-fixed, fix
what's in your lane, route engineering-lane findings back to the governor.

Many findings may already be fixed by corrections made earlier today.
Verify before routing — don't re-fix what's already done.

## The findings (57 total)

The findings cover these files and categories:

**AGENTS.md (7 findings):** Morpheus lane correction (Coder-X→Qwen 3.8 2.4T);
governor rule wording (Kimi-K3→Flash); OD-14 scope (seven→eight lanes);
work-order issuer wording; governor transition qualifier; Chris lane
historical record; Chris Qwen 3.8 Flash lane correction.

**Agent profiles (5 findings):** Carol launch command alias; Chris charter
status (activation→active for install); Chris profile model policy (Qwen
3.8 Flash→DeepSeek V4 Pro); Chris profile environment entry (hxs-9 exists
now); Morpheus profile lane field (Coder-X→Qwen 3.8 2.4T).

**Agent profiles — local lanes (2 findings):** John profile :latest tag→immutable;
Rick profile :latest tag→immutable.

**Catalog receipts (1 finding):** batchB completion metadata (manual gates pending).

**KDD-0014 (1 finding):** Chris lane correction (Qwen 3.8 Flash→DeepSeek V4 Pro).

**State log (1 finding):** row 46 timestamp (~ placeholder→actual UTC).

**Phase B activation doc (1 finding):** command-log identity match claim (headless RE-BASELINE).

**Morpheus work order 09a (1 finding):** token cap (65K→131K for new lane).

**Morpheus Phase C prep doc 10 (7 findings):** corpus anchor paths; SEAM-INT-03
risk code; readiness matrix missing commands; validation placeholder;
blocked-status values; targeted-read counts; validation evidence.

**Morpheus R1 analysis 10b (2 findings):** validation evidence; classification
rollup numbers.

**Morpheus rollback/ops 10c (3 findings):** R2 idempotent removal; validation
evidence; headless dump hash stream separation.

**Work orders (6 findings):** WO12 superseded status; WO15 superseded status;
WO16 pg_hba trust scope; WO16 ps-admin role; WO17 metadata + superseded;
WO17 SSH credential source; WO18 SSH credential source; WO19 file count;
WO19a missing findings; WO21 product 1 citation; WO21 allowed-file contract.

**Redis plan (6 findings):** default ACL user restriction; TTL no-TTL removal;
hit/miss metrics; ACL admin credential; backup atomicity; rollback cleanup.

**PostgreSQL cache plan (4 findings):** SQL keyword typos; LISTEN persistence;
ALTER DEFAULT PRIVILEGES FOR ROLE; backup dir perms 0770.

**PostgreSQL plan (2 findings):** backup dir 0770; current-state correction.

**PostgreSQL step1 evidence (1 finding):** LAN-scram→trust posture correction.

**PostgreSQL step2 evidence (2 findings):** timer-fired activation; V4 identity.

**Gordon test code (6 findings):** test_g6 boot_log rename; check_a child_seed;
invalid-edit config assertion; runner-write result recording; test_g7
telemetry separation; test_g7 determinism check; test_g7 replacement-byte
probe (same as prior F18).

## Constraints

- Verify before writing — read the actual file at the cited lines.
- If a finding is already fixed by a prior correction, skip it with a brief note.
- All governance-record changes are append-only, labeled, dated, originals preserved.
- No lane mutation — you do not fix Gordon's test code, Chris's evidence doc,
  Morpheus's Phase C docs. Characterize and route.
- `scripts/validate.py` 4/4 after any repo write.
- Render any manifest-listed .md you change.
- No secret values.
- Context budget: line-range reads and grep, not whole-file dumps.
- NOTE: Wayne (bash-zmzs1cl7) and Chris (bash-1bpezgjq) are running execution
  work orders on hxs-9. Their evidence docs may change while you work. If you
  find a conflict, note it and skip — don't edit a file being actively written.

## Evidence bar

- For each finding: pasted current-state evidence, your disposition, fix if applied.
- `validate.py` output pasted at close.
- For routed findings: characterization and recommended owning lane.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with the full disposition table.
`[TASK PAUSED — ESCALATION TO GOVERNOR]` with the named remainder.
