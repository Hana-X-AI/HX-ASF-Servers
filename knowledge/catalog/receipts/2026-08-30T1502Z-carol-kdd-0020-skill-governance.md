# Carol receipt — kdd-0020-skill-governance

- Wave: kdd-0020-skill-governance
- Window: 2026-08-30T15:02:13Z (carol-mint 1.0.0)
- Result: **PASS — CATALOG CURRENT** (340 records; validate.py 5/5; 3 new records, 7 re-mints)

## Records

- `DOC-kdd-0020-canonical-skill-tree` — governace/decisions/KDD-0020-canonical-skill-tree-and-mattpocock-batch.md — cano (sha 94c9defbaa5b…, validated_at 2026-08-30T15:01:07Z, freshness current)
- `DOC-repo-governance-claude-md` — CLAUDE.md — Claude Code session entry point to the AGENTS.md authority (sha f232870b97e9…, validated_at 2026-08-30T15:01:07Z, freshness current)
- `DOC-scripts-skills-sync` — scripts/skills_sync.py — canonical skill tree + tool-scope mirror sync (SY-3) (sha 383b81e49119…, validated_at 2026-08-30T15:01:07Z, freshness current)
- `DOC-repo-governance-agents-md` — HX-ASF-Servers AGENTS.md — repository governance, skills, communication contract (sha c93b099746d1…, validated_at 2026-08-29T10:04:50Z, freshness current)
- `DOC-coderabbit-config` — .coderabbit.yaml — CodeRabbit review configuration (p8, owner-ratified 2026-08-2 (sha 21d9dcb95f0b…, validated_at 2026-08-30T15:05:00Z, freshness current)
- `DOC-scripts-hooks` — scripts/hooks/ — Kimi Code hook script system (secret-boundary U5/UD4 pilot; val (sha 8954004f92fd…, validated_at 2026-08-30T15:05:00Z, freshness current)
- `DOC-agent-bailey-profile` — Agent profile — bailey (full operating contract) (sha 0f0fcb6e753c…, validated_at 2026-08-30T15:05:00Z, freshness current)
- `DOC-kdd-0019-bailey-registration` — KDD-0019: Bailey registration — Sr. AI Testing Engineer (sha be1c8f16d8ff…, validated_at 2026-08-30T15:05:00Z, freshness current)
- `DOC-scripts-validate-py` — scripts/validate.py — single local validation command (ratified UD1 validation c (sha 14a29288524d…, validated_at 2026-08-30T15:05:00Z, freshness current)
- `DOC-skill-ai-test-generation` — .agents/skills/ai-test-generation/SKILL.md — AI test-generation skill (Bailey) (sha 666fc41b6b31…, validated_at 2026-08-30T15:05:00Z, freshness current)

## Validator

python3 scripts/validate.py — PASS 5/5 (wiki-sync 84/84; governance-path SY-2+SY-3; fixture-suite 57 tests; catalog-mechanical 340 records; secret-boundary 1353 files, 0 hits)

## Flags

- **Pre-existing stale backlog, NOT closed by this wave (reported, not fixed).**
  `carol-mint sweep-stale` lists **93** records whose recorded sha256 no longer
  matches their live source, plus one `SOURCE-MISSING`
  (`DOC-fleet-script-library` → `scripts/fleet`, a directory, not a file). None
  of these were introduced by this wave — all ten records in this receipt are
  clean in `sweep-stale`. `validate.py` does not grade record-vs-source hashes,
  so the backlog is not a gate failure; it is a freshness debt for a dedicated
  Carol consolidation wave under a governor work order.
- **Three records carry no `hash_history` field** (`DOC-coderabbit-config`,
  `DOC-scripts-hooks`, `DOC-scripts-validate-py`). Their `sha256` was refreshed
  in place. The field was absent before this wave and was deliberately NOT
  introduced — adding a new field shape to existing records is outside this
  wave's scope.
- **`DOC-repo-governance-agents-md` keeps its prose-form `hash_history`** under
  the top-level `notes:` block (not the list form used elsewhere). The new entry
  was appended in that record's existing arrow-chain format rather than
  converting the field.
- **No catalog record was created for the archify pointer stubs** in the two
  mirrors, deliberately. Every `canonical_location` enters `validate.py`'s
  CAT-08 `canon_locations` set, where a raw-path relation target matching one is
  a graded failure; the stubs are generated artifacts, not cataloged documents
  (KDD-0020 D3).

## Provenance of the seven adopted skills

`mattpocock/skills` @ `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76` (MIT,
Copyright (c) 2026 Matt Pocock), pinned in `skills-lock.json` v2 by upstream path
and upstream SHA-256. Three were adopted-as-corrected per AGENTS.md
§"Adoption of provided documents" — `grilling` (capped at 5 questions per round),
`domain-modeling` (decisions are KDDs, never `docs/adr/`), and `grill-with-docs`
(description corrected from "relentless"). Each correction is recorded in its own
SKILL.md under "Provenance and corrections".

The installer's original `computedHash` values are preserved verbatim in
`skills-lock.json` as `installerComputedHash`, marked provenance-only and never
verified: the algorithm is not reproducible from this repository (it matches
neither the upstream nor the installed SKILL.md digest), so no value was
fabricated for the two skills added by hand.
