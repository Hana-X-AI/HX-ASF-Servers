# WORK ORDER — Morpheus: parallel off-candidate package (Phase C prep + R1 + ops design + Tier-1 suite)

- Issuer: Kimi-K3 (governor), 2026-08-29 — pipelined with Gordon's Gates 6–7
  campaign (owner: "this should not be serial activity"; review feedback
  2026-08-29 confirming M runs in parallel with G's testing)
- Executor: Morpheus (dsh lifecycle steward, KDD-0009)
- Model lane (binding): `omniroute/coder-x` (`ollama-local/hx-qwen3.6-coderx-64k`,
  hxs-2, manifest digest `ec9ebe08a82447f7440fd8cba07b406f6972c19ea7fa0cfd53ea8055ff28a9f1`,
  via OmniRoute hxs-8, KDD-0013). Session-start: verify the backend digest
  fail-closed per KDD-0013; stop-and-escalate on failure, no substitution.

## HARD BOUNDARY (absolute, campaign integrity)

Gordon's Gates 6–7 campaign is running against the FROZEN Phase B candidate on
hxs-15. You make **NO candidate mutation of any kind** — no config, service,
unit, tree, cache, or profile-root writes on hxs-15 — until the governor
declares a fix window or the campaign closes with its fingerprint intact. Any
hxs-15 read-only status need goes through the governor, never direct. Violation
voids Gordon's campaign and is a lane breach.

## Read first (mandatory)

1. `agents/morpheus/profile.md` and `charter.md` — your contract.
2. `pilots/PILOT-DSH-IMPL-001/01-state-log.md` rows 13–30 — arc state incl. the
   freeze (row 25) and your own §13 correction block.
3. Your records: `03-morpheus-phase-a-install.md` (R1, R2, R4) and
   `05-morpheus-phase-b-activation.md` (§5 families, §10 handoff, §12 risks).
4. The plan `agent-zero-docs/projects/Deepseek/2026-08-28-dsh-full-implementation-plan.md`
   — Phase C scope (Gates 8–10: interop, sandboxing, remote + experimental,
   platform proof).

## Products (all off-candidate: corpus + repo documents only)

1. **Phase C preparation** (`pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md`):
   source-grounded design for the Gates 8–10 families from the pinned corpus
   `/opt/tkv-local/deepseek-harness-master` — per family: source seam
   (file:line), activation mechanism on the native composition layer, host
   prerequisites, risk class, and **testability notes for Gordon's Gate 8–10
   authoring** (what is provable, what is BLOCKED-by-design and why).
2. **R1 advisory-debt intake analysis** (section in the same doc): the 38
   pinned-snapshot advisories — map each to its fixed upstream version, check
   compatibility against the pinned lockfile's constraints (OFFLINE analysis;
   NO lockfile rewrite, NO install), and classify: resolved-by-next-intake /
   needs-upstream-action / accepted-risk-with-rationale. Ready for the next
   authorized upstream intake.
3. **Rollback/operations design** (same doc): the Gate 9 rollback exercise the
   arc owes (Phase A signed with "rollback NOT exercised") — full rollback
   drill design from the current Phase B state to the pre-Phase-B checkpoint,
   modeled on trinity's OmniRoute gate battery (parity + restart + reboot +
   restore + rollback + hygiene); plus the upgrade-path runbook for the next
   dsh intake (reversible, hash-anchored, inverse per step).
4. **Tier-1 during-install smoke suite** (owner-ratified three-tier model,
   2026-08-29): a defined per-step smoke set for Phase C installs — per family,
   a bounded entry-path probe (minutes, deterministic-first), each labeled
   "install verification, NOT qualification". It must NOT restate Gordon's
   gate claims. Format: table per family — probe, oracle, expected receipt.

## Standby duty

If Gordon files defects mid-campaign (visible in the state log or his evidence),
you may ANALYZE and PREPARE fixes off-candidate (staged patch + evidence +
inverse). Application waits for a governor-declared fix window or campaign
close — the D1/D3 pattern. Never apply, never contact the candidate.

## Repo rules

`python3 scripts/validate.py` must end 4/4 PASS after your writes (no
credential-shaped literals; scanner is zero-tolerance). Append-only everywhere:
your Phase A/B records are amended only by labeled correction.

## Validation + close

Deliverables: the prep document above + your knowledge-review receipt (first)
+ sanitized command log. Close with `[TASK COMPLETE — EVIDENCE ATTACHED]`, or
`[TASK PAUSED — ESCALATION TO KK3]` with the reason.
