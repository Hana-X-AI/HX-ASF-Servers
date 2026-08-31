# KDD-0024: Two-stage closure — cataloguing does not gate acceptance (O4)

- Date: 2026-08-30
- Status: ratified
- Decider: Agent-Zero (owner directive 2026-08-30)
- Related: `AGENTS.md` §Documentation governance, `governace/process/governor-verification-checklist.md`
  step 10, both `context-packet.yaml` templates, KDD-0013 Amendment 5,
  KDD-0021 (work-state engine), KDD-0023 (declare-then-verify), Codex
  process-optimization review `codex_20260830_1539` (O4, F3)

## Context

Two ratified directives contradicted each other for five days, and neither cited
the other.

**2026-08-25** — `AGENTS.md`, documentation-governance amendment:

> A material handoff is **incomplete without Carol's catalog receipt**,
> referenced in the governing log.

Restated as step 10 of the governor verification checklist ("the handoff stays
OPEN until her catalog receipt is cited in the state log. Only then the
acceptance row and goal-status update") and baked as a constant `handoff:` string
into every context packet the factory issues.

**2026-08-29** — KDD-0013 Amendment 5, owner directive lifting Carol's freeze:

> her gpt-oss-120b lane is ACTIVE for catalog catch-up, asynchronous — **no gate,
> handoff, or lane blocks on her output**

The second uses the exact word — *handoff* — that the first makes conditional on
Carol. `AGENTS.md` was never amended. The context-packet template kept shipping
the blocking string. Step 10 kept gating the acceptance row.

**The blocking rule was already failing in practice.** Catalog receipt
`2026-08-27T0030Z-carol-tmicro-fleet-time-pass.md` line 33 records: *"Row 20's M5
handoff is OPEN — cataloging 12-esme-m5-validation.md is queued to a future wave,
outside this T-micro's write set."* A handoff parked open because a background
agent's write set was scoped elsewhere — the exact stall this decision removes.

One partial reconciliation existed: the checklist's Tier 0 row reads *"Accept
after gate; T-micro Carol run (background)"*. It is scoped to one triage tier and
sits three sections below the step 10 text it contradicts.

## Options considered

1. **Keep the blocking rule and amend KDD-0013 Amendment 5.** Rejected by the
   owner directive below.
2. **Drop the receipt requirement.** Rejected: the catalog is the retrieval
   surface the whole factory reads before acting. Not requiring the receipt
   would trade a scheduling problem for a knowledge problem.
3. **Split the handoff into two independent states.** **Selected.** The receipt
   stays required; waiting on it does not.
4. **Add the new states to the goal work-state enum.** Rejected — see D4.

## Decision

**Owner directive, 2026-08-30:** *"do not let non critical path work block
critical path this goes for agents also."* That settles the contradiction in
favour of KDD-0013 Amendment 5. `AGENTS.md`'s 2026-08-25 line is superseded for
routine work and preserved as written.

**D1 — Two independent states.** `execution_accepted`: evidence produced,
deterministic gates passed. The work is done, the acceptance row is written, the
goal status updates, and the next work order may dispatch. `catalog_pending` /
`catalog_complete`: the knowledge projection, tracked separately, never gating.

**D2 — The receipt is still required.** This is a sequencing change, not a
removal. A deliverable that never reaches `catalog_complete` is visible as an
open catalog item; it is simply not holding a lane shut while it waits.

**D3 — Synchronous exception, deliberately narrow.** A change to **authority,
security, schemas, agent identities, or reusable platform knowledge** takes the
receipt before closure. Those are the classes where acting on a stale catalog
does real harm rather than costing time. Everything else batches at merge or the
scheduled consolidation window. Where the class is unclear, treat it as
synchronous — the failure mode of over-including is a delay, and of
under-including is a wrong decision made from a stale catalog.

**D4 — The goal work-state schema is NOT extended.** The plan for this phase
proposed adding the new states to `work-state.schema.yaml` at `version: 2`. That
is the wrong level. That schema carries GOAL status; `execution_accepted` is a
HANDOFF state at work-order granularity. Adding it to the goal enum would
conflate two levels and require renaming a ratified vocabulary — which the schema
itself warns against. The handoff state lives where the handoff lives: the gate
receipt emitted by `hx gate` (O3), which already returns `outcome:
execution_accepted` with `catalog_state` as a separate field it never waits on.

**D5 — Amended in all three places, append-only.** `AGENTS.md`, checklist step
10, and the `handoff:` constant in both context-packet templates. Leaving any one
of them would leave the blocking rule asserted somewhere after its retirement —
the failure pattern this repository has had to correct repeatedly, most recently
when a header was fixed and the procedure below it was not.

## Consequences

**Enables.** A lane closes when its work is done and its gates pass. Carol's
queue depth stops determining factory throughput, which is what
background-class was supposed to mean since 2026-08-29.

**Immediate effect.** The contradiction between two ratified records is resolved
by owner directive rather than left for a reader to adjudicate. `hx gate` already
emits both states, so no code change is required by this decision — the code was
written to it and the governance now says the same thing.

**Forecloses.** Reading "catalog before closing" as "cataloguing blocks closing"
for routine work.

**Costs.** The catalog trails execution for routine changes. Bounded by the
consolidation window and visible as `catalog_pending`; SY-8 (catalog freshness)
independently reports records that have drifted from their sources.

**Must be revisited if.** The synchronous exception list proves too narrow — a
decision made from a stale catalog for a class not on it — or `catalog_pending`
items accumulate faster than consolidation clears them.

**Not addressed.** O6 (secret-boundary warn → block) is the last open item from
the review. It is unblocked — SY-5 declares the mode file's content and digest,
so a flip is visible rather than a silent one-word edit — but the false-positive
regression corpus that would justify graduating it does not exist yet.

## Amendment 1 (2026-08-30, labeled, append-only) — D5 named the wrong artifact class

[OPEN CORRECTION 2026-08-30, labeled, append-only — D5 above reads "Amended in
all three places, append-only." The requirement to amend all three places is
correct and stands. **The artifact class is wrong**, and it was applied wrongly
when this decision landed. The original D5 text is preserved above.]

`CLAUDE.md` and this repository's artifact-class policy (`.coderabbit.yaml`
`path_instructions`) are explicit: **`AGENTS.md`, `governace/process/**`,
`governace/templates/**`, `.agents/skills/**` and agent profiles are LIVE
artifacts, corrected IN PLACE — Git preserves the history.** Append-only applies
to KDDs, dated goals, state logs, evidence, receipts and status reports.

**All three places D5 names are live artifacts** — `AGENTS.md`,
`governace/process/**`, and `governace/templates/**` are each named in the
policy above. Two of them, `AGENTS.md` and the governor verification checklist,
were nonetheless amended with `[OPEN CORRECTION ...]` blocks that quoted the
retired rule inline, so each asserted the retired procedure and its replacement
in the same breath — the precise reading hazard this repository has had to fix
repeatedly, and which this decision's own D5 cites as its reason for amending
everywhere. The two context-packet templates were rewritten in place from the
start, which was correct.

**Corrected on 2026-08-30:**

- `AGENTS.md` — the retired line and its correction block are replaced by the
  two-stage rule stated directly, with a one-line revision note.
- `governace/process/governor-verification-checklist.md` step 10 — same
  treatment; the quoted "handoff stays OPEN" procedure is gone from the live
  step and survives in Git and in this KDD's Context section.
- Both `context-packet.yaml` templates — these are also live artifacts and were
  already rewritten in place rather than annotated, which was correct.

**This KDD stays append-only**, which is why this correction is an amendment
rather than an edit to D5.

**Also corrected here:** the templates did not carry the unclear-class fallback
that D3 and the checklist both state. Added to both copies — where the change
class is unclear or arguable, treat it as synchronous.

Authority: the `CLAUDE.md` artifact-class policy and the `.coderabbit.yaml`
`path_instructions` that codify it — `AGENTS.md` carries the instruction
"Correct directly; Git preserves history. Do not demand append-only
amendments." The defect was surfaced by an automated review on 2026-08-30;
a review tool finds, it does not ratify.
