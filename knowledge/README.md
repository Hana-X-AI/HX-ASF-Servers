# Knowledge

The single knowledge home for the HX AI Software Factory. If a fact, decision, issue,
or lesson matters beyond one conversation, it lives here.

## What lives where

- `decisions/KDD-NNNN-<slug>.md` — Key Decision Documents, one per decision, numbered
  in order. Never renumber.
- `issues.md` — open issues and action items. One file until it hurts.
- `lessons-learned.md` — what we learned and what changes because of it.

## Truth-state labels

Every infrastructure fact here carries a label: `TARGET-STATE`, `AS-BUILT`,
`DISCOVERED`, `PROPOSED`, or `LEGACY`. Rules:

- A design document is TARGET-STATE, not evidence of installation.
- DISCOVERED claims need evidence and a date.
- Historical material is LEGACY: mine it for rationale, never copy its environment
  state as current truth.

## Writing conventions

- Plain Markdown. Filenames are lowercase except for the required uppercase
  `KDD-NNNN` prefix on decision files.
- Date every entry (YYYY-MM-DD).
- Reference goals and KDDs by their codes (`KDD-0003`), not by retelling them.
