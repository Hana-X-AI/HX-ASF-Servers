# KDD-0021: One work-state engine (O1)

- Date: 2026-08-30
- Status: ratified
- Decider: Agent-Zero
- Related: `governace/goals/work-state.schema.yaml`, `scripts/work_state.py`, KDD-0020 (canonical skill tree — the `work-status` and `goal-decompose` skills consolidated here live under it), Codex process-optimization review `codex_20260830_1539` (O1, and F1/F6 of its defect list)

## Context

Goal status was reconstructed by grepping prose. Both consumers — the
`work-status` and `goal-decompose` skills — carried their own regex, and the
prose they read is append-only governance text that deliberately moves the
current answer into a labeled correction block while leaving the original line
in place. That convention protects history and makes state unparseable. Two
failure modes were reproduced against the live tree on 2026-08-30, before any
code was written:

1. **A COMPLETE goal was invisible.** `2026-08-27-fleet-baseline-deployment.md`
   records completion inside a labeled correction
   (`**Status:** COMPLETE — 2026-08-28`). The parser matched only the list form
   `- Status:`, so the goal parsed as `<none>` and was reported as *unknown* by
   every status command.
2. **A closed goal reported as active.** `2026-08-26-hxs3-muse-glimmer-tooling.md`
   carries `- Status: in-progress`, while its pilot state log records
   `goal COMPLETE — PASS` and `PILOT-…-001 is COMPLETE and CLOSED`. The goal's
   own line even says *"historical — see transition"* — the staleness was known
   and pointed elsewhere rather than fixed.

A third defect compounded it: `goal-decompose/SKILL.md` documented four scripts
(`status.sh`, `next.sh`, `blocked.sh`, `validate.sh`) as living in its own
`scripts/` directory. That directory was empty and always had been — the scripts
belonged to `work-status`. Anyone following the skill got "No such file or
directory".

**Correction to the source review.** The Codex review states the defect as
"work-status incorrectly reports completed goals as in progress", which reads as
a broken script. That is half the picture. `in-progress.sh` reported exactly the
goals whose status lines said `in-progress` — faithful to its input. The engine
was defective (it could not parse the correction form at all) *and* its input was
stale. Fixing only the script would have fixed neither case above.

## Options considered

1. **Harden the prose regex** to also match `**Status:**` inside correction
   blocks. Rejected: it makes the parser chase an open-ended prose grammar, and
   the newest correction block is not reliably the current one — nothing orders
   them.
2. **Rewrite goal prose so one status line is always current.** Rejected: goals
   are an append-only class (`.coderabbit.yaml`); rewriting them to suit a parser
   inverts the governance rule.
3. **Add a machine-readable state block; leave prose untouched as history.**
   **Selected.** Append-only is preserved because adding a block is an append.
4. **Introduce a workflow database or orchestration service.** Rejected, and the
   source review says the same: not before the file-based engine is proven
   insufficient.

## Decision

**D1 — One block, one reader.** Every goal carries exactly one
` ```yaml work-state ` block, specified by `governace/goals/work-state.schema.yaml`.
It is the ONLY source any tool may use for goal status. Prose above it is the
historical record and is never rewritten.

**D2 — One engine.** `scripts/work_state.py` is the single implementation:
`status`, `in-progress`, `next`, `blocked`, `standup`, `reconcile`, `--check`,
each with `--json`. The six `work-status` scripts are now thin wrappers that
`exec` it, and `goal-decompose` documents the same commands. Neither skill
reimplements parsing.

**D3 — Conflicts are recorded, not resolved.** The schema requires a
`reconcile` field. Where a goal file and downstream evidence disagree, the block
states the disagreement and names the conflicting source. Declaring a goal
complete is a governor determination; a mechanical tool must not make it. Three
goals currently carry an open reconcile item (hxs-3 muse-glimmer, omniroute
Layer 0, LightRAG hxs-4) and are surfaced by `work_state.py reconcile`.

**D4 — Enforced as SY-4.** `validate.py` runs the schema check as sub-check
**SY-4** inside the existing `governance-path` check. The check count stays
**5/5** — the same reasoning as SY-3 in KDD-0020: a sixth top-level check would
invalidate the count assertions scattered across the repository for no gain.

**D5 — Regression fixtures.** `scripts/test_work_state.py` covers the five cases
Phase 1 requires — completed-with-history, blocked, malformed, dependent/orphan,
and non-goal files — including the two production shapes above as named tests.
11 tests, wired into the CI `gates` job.

## Consequences

**Enables.** Status is now derived from a declared field rather than inferred
from prose, so the append-only convention and machine-readable state stop
fighting each other. `--json` output makes the state consumable by any later
projection without another parser. Adding a consumer is a call to one engine.

**Immediate effect.** `fleet-baseline-deployment` reports `complete` (was
invisible); `hxs3-muse-glimmer-tooling` reports `complete` (was `in-progress`).
The current picture: 4 complete, 1 done, 1 abandoned, 2 in-progress, 2 draft.

**Forecloses.** Grepping goal prose for status. A goal without a valid block
fails SY-4, so a new goal cannot be born unreadable — the template
(`governace/goals/_template.md`) now ships the block.

**Costs.** One block per goal, and a maintenance obligation: the block must be
updated when status changes. That obligation already existed; it was simply
being discharged into prose that nothing could read.

**Must be revisited if.** A goal needs richer state than a single status value
(per-milestone state, dependency edges) — the schema is versioned (`version: 1`)
for that. The `done`/`complete` duplication in the enum is inherited from the
existing goal vocabulary and deliberately not renamed here; collapsing it is a
governance change, not a mechanical one.

**Not addressed.** This KDD implements O1 and the `goal-decompose` half of the
review's F6. O2 (context packets generated from work orders), O3 (`hx gate`),
O4 (asynchronous catalog closure), O5 (hook-registration manifest), O6
(secret-boundary warn → block), O7 (skill registry) and O8 (capability
registry) are untouched and remain open.

## Amendment 1 (2026-08-30, labeled, append-only) — three defects in the shipped engine

[OPEN CORRECTION 2026-08-30, labeled, append-only — IMPLEMENTATION DEFECTS: the
decision above stands unchanged. Three defects in the code that implemented it
were found and fixed while scoping O2–O8. All three are the same class this KDD
was written to end — state that a tool reports wrongly or not at all — so they
are recorded here rather than as silent fixes. The original text is preserved.]

**A1-1 — `--json` was dead on arrival.** D2 states the six commands ship "each
with `--json`", and both SKILL.mds advertise it. Every one raised
`TypeError: Object of type date is not JSON serializable` on any non-empty
result. Cause: `status_date: 2026-08-28` is unquoted in every goal file, so
`yaml.safe_load` resolves it to `datetime.date`; the schema checks stringify it
(`str(data.get("status_date", ""))`) so WS-05 passed, but `json.dumps` has no
such coercion. `next --json` and `blocked --json` appeared to work only because
both currently select zero rows and `[]` serializes.

Fixed by normalizing at `parse()` — dates become ISO strings recursively, once,
where the state dict is built — rather than at each call site. **This is the
load-bearing choice:** the state dict is the contract O2, O3 and O8 consume, so
it must be JSON-safe by construction, not by each consumer remembering. A
`default=str` backstop in the single `_dump()` writer catches any future YAML
type without crashing a consumer mid-pipeline.

**A1-2 — `standup` silently dropped `draft` goals.** It grouped in-progress,
blocked, approved and `terminal_statuses`, with no group for
`pre_dispatch_statuses`. The header printed "10 goals" and listed 8;
`2026-08-29-oai-x-replace-meta-x` appeared nowhere at all. Fixed by adding the
Draft group **and** an accounting invariant: any status no group covers is
printed under "Ungrouped" rather than vanishing. The invariant is the durable
half — a future schema status cannot silently disappear from a report.

**A1-3 — the mirrors could not run outside the repo.** KDD-0020 requires
byte-identical mirrors, and one runtime mirror lives outside the repo at
`~/.kimi-code/skills/`. The wrappers resolved the engine as four levels up from
their own location, which is the repo root in-tree and `$HOME` in the user-scope
tree. That tree had therefore never run this engine: it still held the
pre-consolidation prose-grepping implementation, so the governor's own
`status.sh` was answering from the parser this KDD replaced — including the
phantom `goal-decompose/scripts/` directory D2 removed. Byte-identical mirrors
and location-relative root resolution are incompatible; resolution is now
`HX_REPO_ROOT`, then an upward search from the script and `$PWD`, then a loud
exit 2. A status tool must fail visibly, never report nothing.

**Root cause common to all three: the CLI layer had no tests.** The 11 fixtures
in D5 all exercised `load_all()`; none invoked `main()`, so CI was green while
every `--json` command was broken and a status report was omitting goals. The
suite now covers the CLI (17 tests). Each fix was verified by reverting it and
confirming the new test fails.

**Authority:** owner directive 2026-08-30 (process-optimization build, standalone
engineering track); Codex review `codex_20260830_1539` O1.
