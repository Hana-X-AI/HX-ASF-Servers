# KDD-0020: Canonical skill tree at `.agents/skills/` and the mattpocock skill batch

- Date: 2026-08-30
- Status: ratified
- Decider: Agent-Zero
- Related: KDD-0019 (Bailey registration — QA skills subset, path superseded by this KDD), KDD-0016 (agent taxonomy and standard template), `AGENTS.md` §"Skills and trigger words" (the global skill inventory), `AGENTS.md` §"Adoption of provided documents", `scripts/hooks/README.md` (skill registration checklist)

## Context

Commit `fdbe905` installed five skills from `mattpocock/skills` into
`.agents/skills/` together with a `skills-lock.json` pin. Three defects
followed from that installation, all found by inspection on 2026-08-30:

- **F1 — ungoverned location.** `AGENTS.md` stated that skills live in
  `.kimi-code/skills/` and that its inventory section *is* the global skill
  inventory ("To change the effective set, amend this inventory"). The five new
  skills sat in a directory no document in the repository referenced, were
  absent from the inventory, and carried no KDD. The prior skill batch was
  ratified by KDD-0019; this one was not.
- **F2 — unresolvable dependencies.** `grill-with-docs/SKILL.md` and
  `triage/SKILL.md` both instruct the model to call the Skill tool for
  `grilling` and `domain-modeling`. Neither skill existed in the repository or
  at user scope, so `grill-with-docs` — a two-line wrapper with no other content
  — was inert as installed.
- **F3 — a directive conflict.** Upstream `grill-me` is a one-line wrapper that
  delegates to `grilling`, whose interview is explicitly unbounded
  ("relentlessly", "ask the whole frontier in one round"). This repository's
  `grill-me` is an independent rewrite carrying the owner's directive of
  2026-08-30 limiting the scope-lock interview to five questions. Installing
  `grilling` unamended would have reopened the uncapped interview under a
  different skill name.

A fourth problem was structural rather than defect-driven. Skills had one home,
`.kimi-code/skills/`, which only Kimi Code reads. Claude Code reads
`.claude/skills/`. With work now running through more than one harness, a single
tool-specific directory cannot be the canonical home without making the skill
set depend on which harness launched the session.

## Options considered

1. **Move the five into `.kimi-code/skills/` and drop `grill-with-docs`.**
   Smallest change, matches `AGENTS.md` as written, no restructuring.
   Rejected: leaves the canonical home tool-specific, so a Claude Code session
   still sees no skills, and the problem returns with the next harness.
2. **Make `.agents/skills/` canonical with symlinked tool-scope views.**
   No duplication and drift is impossible. Rejected: this repository has a
   recorded flattened-symlink failure class (PILOT-DSH-IMPL-001, Morpheus Phase
   A survey found eight flattened symlinks in an upstream export), and a link
   does not survive export or archiving.
3. **Make `.agents/skills/` canonical with generated copies as tool-scope
   mirrors, enforced by a validator check.** Costs disk and needs a drift gate.
   **Selected.**
4. **Install `grilling` and `domain-modeling` raw to resolve the dangling
   references.** Rejected on its own; adopted only in the corrected form below,
   per `AGENTS.md` §"Adoption of provided documents".

## Decision

**D1 — Canonical skill tree.** `.agents/skills/` is the canonical home of every
skill. `.kimi-code/skills/` (Kimi Code) and `.claude/skills/` (Claude Code) are
**generated mirrors**. Skills are authored and edited only in the canonical
tree; mirrors are rebuilt with `python3 scripts/skills_sync.py --write`.

**D2 — Drift is a graded failure.** `scripts/skills_sync.py --check` compares
every mirror against the canonical tree byte-for-byte. `validate.py` runs it as
sub-check **SY-3** inside the existing `governance-path` check, which is renamed
in purpose to *repo-layout invariants* — SY-2 (the `governace/` canonical
spelling) and SY-3 are the same failure class: a second tree quietly forking a
canonical one. The check count stays **5/5**; no new top-level check was added,
because the count is asserted in 23 places across 14 files, several of them
append-only records, and a rename of that scale buys nothing.

**D3 — `archify` is canonical-only.** `archify` is a Node CLI of 168 files and
6.8 MB, invoked by path rather than loaded into a model's context. The mirrors
carry a generated pointer stub, not a copy. Mirroring it would have tripled it
to roughly 21 MB and added about 336 tracked files for no review value. The
stubs are deliberately given **no catalog record and no `canonical_location`
key**: every catalog `canonical_location` enters `validate.py`'s CAT-08
`canon_locations` set, where a raw-path relation target matching one is a graded
failure.

**D4 — Inventory.** The `AGENTS.md` global skill inventory grows from
twenty-three to **thirty** skills. The seven additions are `handoff`,
`writing-for-agents`, `triage`, `diagnosing-bugs`, `grill-with-docs`,
`grilling`, and `domain-modeling`. The inventory, the prose count, and the
canonical directory are reconciled at 30/30/30.

**D5 — Adoption corrections.** `grilling` and `domain-modeling` are adopted
**as corrected**, not as supplied:

- `grilling` is capped at **five questions per round**, with the remainder
  folded into explicit stated assumptions. It carries a binding precedence rule:
  `grill-me` is the only factory scope-lock gate, and neither `grilling` nor
  `grill-with-docs` satisfies it. The owner's 5-question limit applies to every
  interview path in this repository, not only to `grill-me`.
- `domain-modeling` carries a binding placement rule: inside HX-ASF-Servers,
  decisions are append-only KDDs under `governace/decisions/`, never `docs/adr/`,
  and factory vocabulary lives in Carol's catalog, not a root `CONTEXT.md`. The
  upstream layout applies only to application projects in Rob's lane.
- `grill-with-docs` is retained, its description corrected from "relentless" to
  match the capped behavior it now invokes.

Each correction is recorded in the skill's own `SKILL.md` under "Provenance and
corrections", with the upstream commit and licence.

**D6 — Provenance.** All seven skills derive from `mattpocock/skills` at
upstream commit `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` (MIT, Copyright (c)
2026 Matt Pocock), pinned by path and content hash in `skills-lock.json`.

## Consequences

**Enables.** One skill set regardless of harness. A Claude Code session and a
Kimi Code session now load identical skills, and adding a third harness is one
entry in `skills_sync.py` `MIRRORS`. The dangling `grilling` and
`domain-modeling` references in `triage` and `grill-with-docs` resolve, so both
skills function as written.

**Forecloses.** Editing a skill inside `.kimi-code/skills/` or `.claude/skills/`
— such an edit is overwritten by the next sync and fails SY-3 until it is. The
`.coderabbit.yaml` path instructions mark both mirrors as generated so review
comments land on the canonical file instead.

**Costs.** Roughly 1.1 MB and about 100 tracked files for the two mirrors, and
one sync step in the skill registration checklist
(`scripts/hooks/README.md` step 4).

**Must be revisited if.** A harness appears that reads a third path (add it to
`MIRRORS`); `archify` stops being invoked by path and becomes a context-loaded
skill (the D3 stub exception no longer holds); or the owner revisits the
5-question interview limit, which is currently applied uniformly across
`grill-me`, `grilling`, and `grill-with-docs`.

**Deliberately not changed.** `knowledge/assessments/2026-08-25-capability-assessment-read-only.md`
names `.kimi-code/skills/` in four places. It is a dated point-in-time
assessment that was accurate on 2026-08-25 and is left as historical record,
not rewritten. `KDD-0019` received a labeled append-only correction rather than
an edit, since ratified KDDs are append-only.

## Amendment 1 (2026-08-30, labeled, append-only)

[OPEN CORRECTION 2026-08-30, labeled, append-only — ADOPTION PASS EXTENDED FROM
THREE SKILLS TO FIVE: decision **D5** above records `grilling`,
`domain-modeling`, and `grill-with-docs` as adopted-as-corrected. The CI
CodeRabbit gate on commit `fdbe905` returned three blocking findings against two
skills that this KDD had reviewed only for the dangling-dependency defect (F2),
not against the full standard required by AGENTS.md §"Adoption of provided
documents". All three were verified against the files before being actioned;
all three were real. D5 is extended, and the corrected set is now FIVE:

1. `triage` — step 5 did not repeat the mandatory AI disclaimer, so the
   `ready-for-human` and `wontfix` posting paths could violate the rule stated
   at the top of that same skill (CodeRabbit major).
2. `triage` — step 1(a) treated any domain-concept match as an
   already-implemented `wontfix`, closing requests whose implementation is only
   partial or adjacent (CodeRabbit major).
3. `diagnosing-bugs` — `hitl-loop.template.sh` captured every answer with a
   single-line `read`, so a pasted stack trace silently lost everything after
   the first newline (CodeRabbit minor). A `capture_multi` helper was added and
   the error-message prompt switched to it; `sanitize` still collapses newlines,
   so the documented KEY=VALUE contract is unchanged. Verified by injecting a
   three-line stack trace: three lines captured, one KEY=VALUE line emitted.

Process finding of record: the intake review in D5 was incomplete. Corrections
were applied to the three skills whose defects were found by inspection, while
`triage` and `diagnosing-bugs` were reviewed only for the dependency problem.
The gate caught what the adoption pass missed. Per-skill provenance blocks now
exist for all five. `skills-lock.json` marks five of seven `hxCorrected`.
Authority: CodeRabbit CI gate (run 33316342207) + owner direction 2026-08-30.]

## Amendment 2 (2026-08-30, labeled, append-only) — Codex audit disposition

[OPEN CORRECTION 2026-08-30, labeled, append-only — EXTERNAL AUDIT F7/A5
REVIEWED AND SUPERSEDED BY THIS KDD: the full-repository audit
`codex_20260830_1510_hx-asf-servers-full-repository-audit.md` raises **F7**
("the open skills branch creates a second skills authority plane") and
recommends **A5** ("adopt each selected skill into `.kimi-code/skills/` … and
reject the `.agents/skills/` parallel root"). Owner decision 2026-08-30: **keep
KDD-0020; A5 is not actioned as written.**

**Why the audit reads that way.** Its provenance records `Open skills branch
head: fdbe905` and a clean clone synchronized with `origin/main`. It therefore
evaluated the branch BEFORE the KDD-0020 commit (`e8fc5c2`). At `fdbe905` the
finding was correct and is the same defect this KDD opens with as F1.

**Why the finding no longer holds.** F7's stated objection is a second root
"that current inventory, catalog, triggers, and validation do not govern." All
four are now governed: the `AGENTS.md` inventory is amended and reconciled at
30/30/30 with trigger words per skill (D4); `KDD-0020` ratifies the batch;
catalog records, provenance, and a Carol receipt exist; and `validate.py`
sub-check SY-3 enforces the canonical tree and its mirrors mechanically (D2).
The audit's reasoning is satisfied even though its remedy is not followed.

**Binding instruction for audit item A2 (semantic validators).** A2 proposes two
skill clauses that CONTRADICT this KDD and must not be implemented verbatim:
"23-skill inventory equals canonical skill directories" and "no unexpected skill
roots such as `.agents/skills/`". Restated against KDD-0020, the correct checks
are:

1. the `AGENTS.md` inventory count equals the number of directories in
   `.agents/skills/` (currently 30, not 23);
2. no skill root exists outside `.agents/skills/` and its two DECLARED mirrors
   `.kimi-code/skills/` and `.claude/skills/`;
3. every mirror matches canonical byte-for-byte.

Items 2 and 3 are already implemented as SY-3 (`scripts/skills_sync.py`, called
from `check_governance_path`). Item 1 is NOT yet mechanized — the 30/30/30
reconciliation was performed manually in this change and is a candidate for the
A2 branch.

**Unaffected audit items.** F1 (registry/system-map contradictions), F2
(correction chains in current-state files), F3 (stale `4/4 PASS` requirements),
F4–F6, and recommendations A1/A3/A4 stand and are NOT addressed by this KDD.
Two were independently spot-verified while reviewing the audit: hxs-8 RAM is
16 GB in `servers/SERVER-REGISTRY.md` and 48 GB in `servers/system-mapping.md`
(F1 confirmed), and 17 live files still reference `4/4 PASS` (F3 confirmed,
larger than the six the audit lists). They belong to the narrow
semantic-reconciliation branch the audit recommends, not to this one.

Authority: owner decision 2026-08-30 ("Keep KDD-0020 … i agree"); audit
reviewed, not rejected.]
