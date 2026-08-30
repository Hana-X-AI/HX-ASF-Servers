# CLAUDE.md

**`AGENTS.md` is the governance authority for this repository. Read it before
doing any work here.** This file exists so a Claude Code session loads that
authority automatically; it summarizes only what is easiest to get wrong, and
never supersedes `AGENTS.md`. Where the two appear to differ, `AGENTS.md` wins
and this file is the defect.

## What this repository is

The control plane for a 16-server AI infrastructure fleet (`hxs-1`…`hxs-21`,
LAN `192.168.50.0/24`), operated by Hana-X. It holds almost no runtime code:
goals, decisions, work orders, evidence records, and the agent roster that
executes them. Work flows goal (`governace/goals/`) → work order + context
packet (`pilots/PILOT-*/`) → execution by a named agent in its lane
(`agents/<name>/`) → evidence under `servers/<host>/` → governor verification
checklist → Carol catalog receipt → append-only state-log row.

Note the directory spelling: **`governace/`** is canonical and deliberate.
`validate.py` check SY-2 fails the repo if a `governance/` fork appears. Do not
"fix" it.

## Before you change anything

Run the single validator. It is read-only and takes about a minute:

```bash
python3 scripts/validate.py            # full repo — must be 5/5 PASS
python3 scripts/validate.py --changed <path> [<path>...]   # scoped
```

`5/5 PASS` is the standing bar. The checks are wiki-sync, governance-path
(SY-2 canonical spelling + SY-3 skill-mirror sync), fixture-suite,
catalog-mechanical, and secret-boundary. Four MANUAL GATE lines are printed but
never graded — they are governor judgment, not something you can satisfy here.

## Rules that are easy to violate

**Truth-state labels.** Every factual claim about infrastructure carries one of
`TARGET-STATE`, `AS-BUILT`, `DISCOVERED`, `PROPOSED`, `LEGACY`. A design
document is not evidence that something is installed. Runtime claims need
current evidence with a date.

**Append-only records.** KDDs (`governace/decisions/`), dated goals, state logs
(`pilots/**/*-state-log.md`), evidence, receipts, and status reports are
append-only. Never rewrite them. Corrections land as a labeled block that
preserves the original verbatim:

```
[OPEN CORRECTION <YYYY-MM-DD>, labeled, append-only — <WHAT CHANGED>: <the
correction>. The original wording above is preserved as history. Authority:
<KDD / owner directive>.]
```

Live artifacts are the opposite — `AGENTS.md`, `.agents/skills/**`,
`governace/process/**`, `governace/templates/**`, and agent profiles are
corrected **in place**; Git preserves the history. The full artifact-class split
is codified in `.coderabbit.yaml` `path_instructions`.

**Dual format.** Major documents ship `.md` (source of truth) plus a generated
`.html`. Add the `.md` to `scripts/wiki/manifest.txt`, then run
`python3 scripts/wiki/render.py`. **Never hand-edit an `.html` file** — it is
generated, and `render.py --check` will fail.

**Reconcile every count.** Any numeric claim you touch (skill counts, host
lists, lane counts, hashes, dates) must be reconciled against its source before
you write it. A count that cannot be reconciled does not ship. See the
governor-edit preflight in `governace/process/governor-verification-checklist.md`.

**Commits.** Never add a co-author trailer. This is an explicit standing rule in
the `AGENTS.md` communication contract.

**Secrets.** Zero secret values in any artifact, ever — existence, owner, and
retrieval mechanism only. The catalog and the evidence records follow the same
rule.

## Skills

Thirty skills live canonically in **`.agents/skills/`** (KDD-0020).
`.kimi-code/skills/` and `.claude/skills/` are **generated mirrors**.

Author and edit skills only in `.agents/skills/`, then:

```bash
python3 scripts/skills_sync.py --write   # rebuild both mirrors
python3 scripts/skills_sync.py --check   # verify; validate.py SY-3 enforces it
```

Editing a mirror is always wrong — the next sync overwrites it and SY-3 fails
until then. `archify` is canonical-only (a Node CLI, not a prompt skill); the
mirrors carry a pointer stub.

`AGENTS.md` §"Skills and trigger words" is the authoritative inventory and lists
each skill's owner trigger word. To change the effective set, amend that
inventory — do not add skills silently.

## Hooks

`.claude/settings.json` registers five repo hooks. They are the same governed
scripts Kimi Code uses, so they are single-sourced in `scripts/hooks/`:

| Hook | Event | Mode |
|---|---|---|
| `secret-boundary.sh` | PreToolUse `Write\|Edit\|Bash` | mode file; `warn` today, `block` on graduation |
| `validate-changed.sh` | PostToolUse `Write\|Edit` | advisory |
| `agent-creation-check.sh` | PostToolUse `Write\|Edit` | advisory |
| `render-sync.sh` | PostToolUse `Write\|Edit` | advisory |
| `test-log-append.sh` | PostToolUse `Write\|Edit` | advisory |
| `governor-gate.sh` | PostToolUse `Write\|Edit` | advisory |

The four advisory hooks read the edited path from the JSON key `path` (the Kimi
Code payload shape). Claude Code sends `tool_input.file_path` instead, so they
are wrapped in `scripts/hooks/claude-payload-shim.sh`, which translates one
shape into the other. `secret-boundary.sh` is registered **without** the shim —
it greps the whole payload for secret patterns and needs it unmodified.

Advisory hooks always exit 0; they are feedback, not gates. The hard gate is
CI's `gates` job plus `validate.py`.

## Approval discipline

Proceed when the ratified rules, process, and audit trail for a step are in
place — approval is pre-granted. Halt and escalate only for potential serious
harm: destructive or irreversible actions, governance changes, new external
shared state, or scope expansion. When in doubt, act reversibly and report
rather than pause.
