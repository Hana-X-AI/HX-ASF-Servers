# WORK ORDER — Gordon: Gates 6–7 execution (RESUME on assigned lane)

- Issuer: Kimi-K3 (governor), 2026-08-28 — pilot state-log rows 24–27
- Executor: Gordon (KDD-0010), independent dsh qualification specialist
- **Model lane (binding):** DeepSeek V4 Pro — `omniroute/deepseek-v4-pro`
  (`openrouter/deepseek/deepseek-v4-pro-0813`, upstream provider StreamLake,
  via OmniRoute hxs-8) — owner directive 2026-08-28, route probed live
  (`ROUTE-OK`). Deterministic oracles remain your first tool. On lane failure:
  stop, escalate, no substitution. [Amended 2026-08-28, labeled: originally
  issued for Qwen-X (`omniroute/qwen-x`, hxs-1, digest `766cd946…99d8a`) —
  superseded by the owner's same-day directive; original preserved here.]

## Read first (mandatory, in order)

1. `agents/gordon/profile.md` and `agents/gordon/charter.md` — your operating contract.
2. `pilots/PILOT-DSH-IMPL-001/01-state-log.md` rows 14–27 — arc state, including:
   the power outage, the post-outage verification, Morpheus's accepted freeze
   (row 25), and the substrate retraction (row 27) that stopped the previous
   moonshot-substrate session before any Phase B verdict was recorded.
3. `pilots/PILOT-DSH-IMPL-001/05-morpheus-phase-b-activation.md` §9/§10 (handoff
   receipt: RPC envelope, WS downlinks, watch items) and §13 (fresh freeze block
   2026-08-28T21:18–24Z + OPEN CORRECTION: headless dump re-baselined to
   `c88664a8…`; F5 note: headless `--dump-config` emits a benign 76-byte stderr
   warning — keep stdout and stderr SEPARATE in any dump hashing).
4. `pilots/PILOT-DSH-IMPL-001/06-gordon-phase-b-testplan.md` (43 rows: Gate 6 ×23,
   Gate 7 ×20) and runbook `pilots/PILOT-DSH-IMPL-001/gordon/phase-b/README.md`.

## Task

Execute the full 43-row Gates 6–7 campaign on hxs-15 against the frozen Phase B
candidate (dsh 0.1.1-rc.2), Gate 6 then Gate 7, with durable evidence and
verdicts in your completion language.

Your prior session converted the eight BLOCKED-at-authoring rows to executable
code and hardened the suite (committed as 204ed65, plus your post-commit edits
to `gordon/phase-b/conftest.py` and `test_g6_orchestration.py` — those
uncommitted edits are YOURS; verify and keep them). A governor robustness patch
also landed (transport-failure guards in the G7-05/G7-10 live legs, G7-08
settings-file ordering + revision guards, HTTPError body parsing, OTLP
truncated-header handling, acp/sdk driver summary guarantees, collect_until
error tolerance). The suite as committed+edited is your campaign basis.

Campaign start: your own independent freeze against Morpheus's §13.2/§10
identities (profile §8 step 3). Any mismatch: STOP before the first test.

Rulings of record: the eight formerly-blocked rows (G7-04/06/08/14/15/16/17/19)
execute against Morpheus's §10 envelope; any row whose envelope or overlay
cannot be traced goes BLOCKED with discovery output, never guessed. Non-mutating
Playwright/Chromium channel pre-check in preflight; if the channel is blocked,
G7-12 goes BLOCKED with the dependency named. Fixture overlays only where the
plan designates (hooks/mcp fixture-overlay; schedule/jobs/session-query through
the REAL home). G7-19 telemetry against the localhost OTLP fixture — no cloud.
Queue-transient discipline: 4 attempts, 45 s spacing; persistent failure records
FAIL with transcripts, never suppressed.

## Bounds

hxs-15 only; executor hxs-5 as hxsa. SSH via your own SSH_ASKPASS helper (0700)
reading the credential-record row from
`/home/hxsa/opt/local-tkv/agent-zero-docs/keys.md/ssh-info.md` at execution time
only; SSH_ASKPASS_REQUIRE=force + DISPLAY; StrictHostKeyChecking=yes; `sudo -n`
on-host; helper deleted at end. Execute + install test tooling ONLY — no
configuration changes anywhere (candidate, services, units, home layer); every
defect routes to Morpheus. Secrets never-valued; your de-patterning writer
first, manual sweep second.

## Required

All 43 rows dispositioned — no silent skips, no BLOCKED/NOT_RUN→PASS
conversions; coverage-ledger Phase B section updated **append-only** — every
original NOT_RUN/PENDING row preserved with its provenance, and the final
dispositions plus the §13.2 freeze identity appended as dated, explicitly
labeled records (open corrections), never in-place rewrites [amended 2026-08-28,
labeled: this line originally instructed that the ledger be "flipped with the
§13.2 freeze identity populated" — non-compliant with append-only governance;
original wording preserved here]; `[GATE VERDICT — Gate 6 — …]` and `[GATE VERDICT — Gate 7 — …]`;
campaign close per profile §12.3; end-of-campaign tree fingerprint against the
freeze; carried rows (G2-10/G5-10 via G7-01/G7-12; G4-06(b) at G7-07)
dispositioned; defects filed to Morpheus with severity. Evidence contract per
profile §13 (test ID, candidate identity, environment identity, entry path,
observed result, oracle source, disposition, artifact pointer);
evidence-ledger.jsonl; per-gate JUnit XML; final secret sweep clean.
`python3 scripts/validate.py` from the repo root must end 4/4 PASS after your
repo writes.

## Escalation

Credential material in any artifact; candidate writes outside scratch/product
storage; identity drift vs the freeze; any P0/P1 defect — stop, preserve,
escalate. Driver-lane (currently DeepSeek V4 Pro per amendment 2 to the
launch order [form note 2026-08-29, labeled, Mia per Flash work order 19 —
F14: "Qwen-X" is the superseded lane; the failure-classification behavior is
unchanged, only the lane name is corrected]) failures are characterized
separately from candidate defects.

Close with `[CAMPAIGN COMPLETE — EVIDENCE ATTACHED]` plus per-gate verdicts and
the campaign integrity fingerprint, or `[CAMPAIGN PAUSED — ESCALATION TO KK3]`
with the reason.
