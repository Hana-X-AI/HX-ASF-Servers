# WORK ORDER — Mia: hxs-9 PostgreSQL implementation plan (planning only)

- Issuer: Kimi-K3 (governor), 2026-08-29 — owner directive: "Owned system
  doesn't exist yet: create an implementation plan, via Mia"
- Executor: Mia (Chief of Staff, KDD-0012) — planning and coordination; you
  produce a PLAN, not an implementation
- Model lane (binding): `omniroute/glm-5.3-flash` (upstream Modal, via
  OmniRoute, KDD-0013 amendment 3). Session-start: verify the exact served id
  `z-ai/glm-5.3-flash` with a minimal probe; fail closed, escalate, no
  substitution.

## Read first (bounded)

1. `agents/mia/charter.md` + `agents/mia/profile.md` — your contract.
2. `agents/chris/charter.md` + `agents/chris/profile.md` — the accountable
   lane this plan serves (KDD-0014): single instance, no replication/HA, MCP
   on HOLD, credential store `.local.env`, backup discipline, runtime bounds
   (concurrency 1, PT1H), activation gates.
3. `servers/SERVER-REGISTRY.md` hxs-9 row — target-state "State services:
   PostgreSQL + Redis; LiteLLM database; LangGraph checkpoints".
4. Verified live fact of record (post-outage check 2026-08-28): hxs-9
   (192.168.50.208) runs **no PostgreSQL today** — no units, no 5432
   listener, no /etc/postgresql. Baseline: server-default class, 8/8 PASS.
5. `servers/hxs-15/2026-08-28-dsh-runtime-prep.md` and
   `pilots/PILOT-OMNIROUTE-LAYER0-001/01-rick-l1-node-runtime.md` — the
   factory's proven native-install evidence patterns (artifact
   authentication, pre/post hashes, inverses, sanitized command logs).

## Product — `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md`

A complete, execution-ready plan for ONE PostgreSQL instance on hxs-9,
native on systemd (owner rule: no Docker/containers), that a later
owner-approved work order can hand to an executor. Required content:

1. **Scope pin:** PostgreSQL ONLY. Redis and any LiteLLM/LangGraph
   consumption are OUT (separate lanes/decisions). Chris's lane bounds
   (KDD-0014) govern the end state.
2. **Install design:** PostgreSQL version for Ubuntu 24.04 (noble) with
   source/pin rationale (apt noble repo vs postgresql.org repo — evaluate
   both, recommend one, evidence-based); artifact/dpkg provenance
   expectations; pre-state capture; per-step inverses.
3. **Configuration baseline:** minimal secure-by-default posture consistent
   with HX rules — listen on the LAN interface ONLY as authorized (the LAN
   is the boundary; no host firewall per owner rule 2026-08-26), no 0.0.0.0
   wildcard unless owner-ratified, md5/scram password auth (no trust),
   logging baseline, data directory layout.
4. **Roles/service accounts bootstrap:** least-required model — admin role,
   application role(s) named by purpose (LiteLLM/LangGraph consumption is a
   FUTURE consumer; design the roles but create nothing beyond the plan).
5. **Credential model:** entries and variable names for
   `/home/hxsa/opt/local-tkv/agent-zero-docs/.local.env` (Chris's store) —
   mechanism only, no values in the plan.
6. **Backup design:** pg_dump schedule (systemd timer — the factory's native
   shape), destination path + retention, pre/post validation per Chris's
   hooks, restore-test procedure and its first drill date.
7. **Health monitoring:** the 15-minute evaluation interval realized as a
   systemd timer with a bounded check script (availability, connections,
   locks, storage, backup status) — alert path to Mia/Kimi-K3; no automatic
   production changes.
8. **Validation suite (Tier 1, per the ratified tiered model):** per-step
   install-verification smokes with pass/fail receipts — service up, role
   connect, write/read round-trip in a scratch database, backup produces a
   listable archive, restore drill to a test database.
9. **Rollback:** full inverse from any point (packages, data, config,
   timers, credential entries).
10. **Work-breakdown for execution:** ordered steps with the evidence each
    must produce, the agent assignment per step (rick for OS-plane package/
    systemd work? chris post-activation for DB-internal work? — recommend,
    with rationale, consistent with lane bounds), and the owner checkpoints
    you recommend.

## Bounds

You PLAN and COORDINATE — you do not execute, touch hxs-9, or dispatch
(Agentalert: distribution happens only under a Kimi-K3-issued work order).
Every claim about hxs-9 comes from the records above or is labeled
unverified. `python3 scripts/validate.py` 4/4 PASS after your writes; paste
the result. Report in your [MIA STATUS REPORT] shape.

Close with `[TASK COMPLETE — EVIDENCE ATTACHED]` or
`[TASK PAUSED — ESCALATION TO KK3]` with the reason.
