# WORK ORDER — Morpheus: fix G6-18 test environment permission issue

- Issuer: Flash (governor), 2026-08-29.
- Executor: Morpheus (dsh lifecycle steward, KDD-0009).
- Lane: `omniroute/qwen-x` (Qwen-X, local, hxs-1).
- Target: hxs-15 (192.168.50.214).

## The defect

G6-18 (live recomposition) fails because dsh (running as user `dsh`) cannot
write to `cordis.patch.yml` owned by `hxsa` (mode 0644). The last-good
config restore fails with EACCES.

## The permanent fix

This is a test-environment permission issue, not a dsh code bug. The fix
is to ensure test-created files are writable by both users:

1. In the test runner's conftest or the run-phase-b.sh script, set
   `umask 000` before pytest runs so all created files are mode 0666
   (world-writable). The scratch directories are already 0777.
2. Verify: after the fix, re-run G6-18 only:
   `cd /home/hxsa/gordon/phase-b && OMNIROUTE_API_KEY=$(sudo cat /var/lib/dsh/.env | grep OMNIROUTE_API_KEY | cut -d= -f2) python3 -m pytest test_g6_orchestration.py::test_g6_18_live_recomposition -ra`
3. Paste the test output. Report PASS or FAIL.

## Constraints

- Fix the test environment (umask), NOT the dsh source code.
- Do NOT investigate the other defects (G6-01 through G6-19 exit-code issue,
  G6-11 schedule events). Those are separate work orders.
- SSH: askpass pattern (HX_SSH_PASSWORD from .local.env, 0700 helper,
  deleted after).
- Do NOT read the state log or work orders. Just fix and test.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with the umask fix applied and the
G6-18 test result pasted.
