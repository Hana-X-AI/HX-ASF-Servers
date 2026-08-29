# HAND-OFF — Governor model transition (2026-08-29)

**For the incoming governor session (GLM 5.2). Read this first, then
`AGENTS.md`, then the DSH state log rows 17–43.**

## 1. What changed at this transition

- The governor's model is now **Z.ai GLM 5.2** (`openrouter/z-ai/glm-5.2`,
  provider Decart, via OmniRoute hxs-8) — owner directive 2026-08-29.
  `default_model = "omniroute/glm-5.2"` in `~/.kimi-code/config.toml`.
- Proof of record: live probe (exact served id), config line, `kimi doctor`
  valid, live no-`-m` session answered. State-log row 43, KDD-0013
  amendment 7.
- The moonshot meta-agent exception is SUPERSEDED for the governor. The
  substrate-retraction rule stands for ALL other agents: no sub-agent
  sessions on moonshot, ever. Agent work runs as standalone
  `kimi -m omniroute/<lane> -p "$(cat <work-order-file>)"` background
  sessions — never the Agent tool.
- The outgoing session (moonshot) wrote this hand-off; everything below is
  verified state as of its writing.

## 2. Live tracks (do not disturb without reading their state)

### 2.1 Chris — PostgreSQL 18.6 install on hxs-9 (RUNNING)

- Background task `bash-z3a5jjmc` (session on `omniroute/qwen3.8-flash`).
- Executing `pilots/PILOT-DSH-IMPL-001/13-mia-work-order-chris-hxs9-postgresql-install.md`
  (written by Mia, verified): Step 0 pre-state gate + Step 1 (PGDG
  onboarding GPG-verified, postgresql-18 = 18.6-1.pgdg24.04+2, conf.d
  baseline per plan §2, /var/backups/hx-postgres, V1–V3 smokes), then a
  HARD HALT at **Checkpoint 1** for owner review.
- **On completion:** review his evidence doc
  `servers/hxs-9/2026-08-29-postgresql-install-step1.md` against the
  governor checklist, then present Checkpoint 1 to the owner. Step 2
  (roles, credentials in `.local.env`, backup + health timers, V4–V6) runs
  only on the owner's word after Checkpoint 1.
- Controlling plan: `servers/hxs-9/2026-08-29-postgresql-implementation-plan.md`
  (owner-reviewed twice: LiteLLM/LangGraph stripped, ps-* role format,
  18.6 via PGDG). One known stale line (§9 Step 1 "noble main") — ruled
  void by Correction 2; a labeled plan correction is still owed by Mia.

### 2.2 Gordon — Gates 6–7 campaign on hxs-15 (RUNNING)

- Background task `bash-ln2cbqqu` (session on `omniroute/deepseek-v4-pro`).
- 43-row suite (`06-gordon-phase-b-testplan.md`) against the frozen Phase B
  candidate. Freeze basis: Morpheus §13.2 (2026-08-28T21:18–24Z), accepted
  row 25.
- **Open finding:** G7-06 — the candidate's `/api/session.export` produces
  a ZIP whose non-ASCII bytes are destroyed (UTF-8 round-trip signature).
  He was isolating bundle-vs-source when last checked. Defects file to
  Morpheus; governor reviews at campaign close.
- Governor's checkpoints: Gate 6 verdict, Gate 7 verdict, campaign close
  (fingerprint vs freeze). Then Phase B sign-off decision to the owner.

### 2.3 Carol — catalog (background-class, WATCH)

- Batch A + B accepted after repair loops. Pattern of record:
  narrative-over-write (claims writes that did not happen) and mechanical
  defects (empty/stale sha256, id case, empty fields).
- **Rules for her claims:** pasted `validate.py` output AND existence proof
  for any file claim. WATCH condition: 2 consecutive clean batches to
  recover. Ledger: `knowledge/agent-performance.md`.
- If the next batch repeats the class: escalate lane-fitness to the owner
  with the trail (rows 32–37).

### 2.4 Mia — Chief of Staff (ACTIVE)

- Producing well from intent-level briefs (hxs-9 plan, Chris's work order).
- Standing duties: work management, review-finding intake (rr/CodeRabbit
  batches), status reporting to the governor.
- Owed by her: the labeled correction for the plan's stale §9 Step 1 line.

### 2.5 Morpheus — STOPPED, awaiting owner decision

- Coder-X failed the Phase C prep package twice (loops + confabulated
  paths). Branch stopped per KDD-0013 (state-log row 40).
- **Owner decision pending (Q1):** O1 re-assign the doc-synthesis class to
  deepseek-v4-pro (governor recommends; Morpheus's lane stays Coder-X for
  build/repair) · O2 four single-family micro-orders on Coder-X · O3 hold
  until Gordon closes.

## 3. Open owner decisions (do not decide these yourself)

1. Morpheus Q1 (above).
2. Chris plan final approval (after Checkpoint 1) and his Step 2 GO.
3. `192.168.50.10` — unidentified live device (no DNS, no 22/80/443).
4. R2: hxs-5 NTP pin to time.cloudflare.com — deferred by owner until the
   deepseek work completes; `fleet-ntp-pin.sh hxs-5 --apply` under a named
   work order when due.
5. Router DNS loader (`/jffs/hx-dns-load.sh`) — owner-operated; currently
   working (owner re-ran it 2026-08-28).
6. hxs-7 — decommissioned 2026-08-28; registry corrected; no action.

## 4. Rules in force (violations today were all logged — do not repeat them)

- **KK3 → Mia → lanes.** Governor assignments to Mia are INTENT +
  CONSTRAINTS only (objective, bounds, authority, evidence bar). Never
  pre-write her management content (row 41 foul).
- **Lane-expertise gate before every assignment:** does this lane own this
  work class (rick-on-database was the failure), and is the assignee's
  `/opt/tkv-local` knowledge review mandated in the order.
- **Append-only governance records.** Corrections are labeled, dated, with
  originals preserved. Governor breached this once (hxs-7 registry row) —
  repaired; the governor-edit preflight in
  `agents/kimi-k3/verification-checklist.md` is mandatory.
- **Receipt-check every deliverable:** artifact exists, claims verified
  read-only, validator output pasted, no false completes. Carol's rule:
  existence proof for file claims.
- **Lane verification fail-closed (KDD-0013):** local lanes verify the
  manifest digest; cloud lanes verify exact served-model id + session-start
  probe. No substitution without owner word; re-assignment control at KK3
  with owner visibility.
- **Secret discipline:** askpass read-at-execution, helpers 0700 and
  deleted, mechanism-only references, `scripts/validate.py` 4/4 PASS after
  every repo write, `scripts/wiki/render.py` for manifest-listed docs.
- **Governor model-lane honesty:** driver failures are logged as
  driver-lane, never laundered into candidate defects.

## 5. Repo state at hand-off

- HEAD: the hand-off commit (see `git log -1` — wave: Chris registration,
  plan corrections, catalog batches A/B, lane changes, transition records,
  this document). Tree clean.
- validate.py 4/4 PASS; render.py --check 53/53.

## 6. First actions for the incoming session, in order

1. Read this file, AGENTS.md, DSH state-log rows 17–43.
2. Check Chris's install task (`bash-z3a5jjmc`) and Gordon's campaign
   (`bash-ln2cbqqu`) state; honor their checkpoint protocols.
3. At Chris's Checkpoint 1: verify his evidence doc, present to the owner.
4. Bring the owner: Checkpoint 1 result, Morpheus Q1 reminder, and this
   hand-off's confirmation that the transition held (first routed governor
   call on GLM 5.2 logged to the state log).
5. Continue the standing flow: KK3 → Mia → lanes, intent + constraints.

*— Kimi-K3 (outgoing moonshot session), 2026-08-29T02:13Z, state-log row 43.*
