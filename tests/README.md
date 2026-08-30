# Tests

STATUS: FUTURE. Placeholder, not yet operational.

Will hold validators and structure checks (for example: registry consistency and
truth-state label checks). Created when the first validation need is concrete.

## Existing test inventory (distributed across the repo)

The repo already carries substantial test coverage — it lives in dedicated
directories, not here. This index prevents the placeholder from being
misread as "no tests exist."

| Suite | Location | Tests | Runs under | Purpose |
|---|---|---|---|---|
| Wiki renderer | `scripts/wiki/test_render.py` | 12 | `validate.py` / CI | HTML render correctness |
| Fixtures regression | `pilots/PILOT-HX1-OLLAMA-QWEN27B-001/fixtures/test_fixtures.py` | 57 | `validate.py` / CI | Fixture sha256 + schema |
| Catalog minting | `scripts/catalog/test-carol-mint.sh` | — | manual | Flock single-writer minting |
| Fleet self-test | `scripts/fleet/fleet-selftest.sh` | — | manual (hxs-5) | Fleet script library offline self-test |
| Archify | `.agents/skills/archify/bin/*.test.mjs` | 83 | `archify doctor` | Skill rendering + contract |
| Gordon Gate 0–5 | `pilots/PILOT-DSH-IMPL-001/gordon/phase-a/` | — | hxs-15 only | DSH Phase A qualification |
| Gordon Gate 6–7 | `pilots/PILOT-DSH-IMPL-001/gordon/phase-b/` | — | hxs-15 only | DSH Phase B qualification |
| Gordon Gate 8–10 | `pilots/PILOT-DSH-IMPL-001/gordon/phase-b/` | — | hxs-15 only | DSH Phase C qualification (note: Phase C gates intentionally reside in `phase-b/` alongside Phase B — no separate `phase-c/` directory exists; Gordon runs all gates from phase-b) |

**Tiered verification:** `validate.py` (4 checks: wiki-sync, fixture-suite,
catalog-mechanical, secret-boundary) is the repo's automated gate, run
locally and in CI. The Gordon gate suites run on hxs-15 as Tier 2
per-phase qualification — they are not part of `validate.py` or CI by
design (tiered verification, KDD-0010).
