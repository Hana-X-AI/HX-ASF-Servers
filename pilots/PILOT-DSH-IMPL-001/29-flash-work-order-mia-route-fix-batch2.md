# WORK ORDER — Mia: route + fix findings to Morpheus, Gordon, Chris, Wayne lanes

- Issuer: Flash (governor), 2026-08-29.
- Executor: Mia (Chief of Staff, KDD-0012).
- Lane: `omniroute/glm-5.3-flash` (GLM 5.3 Flash, Modal, via OmniRoute hxs-8).

## Intent

32 findings from review batch 2 were routed to three engineering lanes. Your job:
fix what you can within your management lane (governance records, work-order
metadata, plan documents that are NOT engineering evidence docs), and
characterize the rest for governor-issued work orders to the owning lanes.

## What you CAN fix (your lane — management, not engineering)

These are plan documents, work-order records, and governance metadata —
not engineering evidence or test code:

**Morpheus docs (fix directly):**
- F19: 10-morpheus-phase-c-prep.md line 424 — fix corpus anchor paths to root-level package.json/pnpm-lock.yaml, or annotate packages/ as intentional
- F20: 10-morpheus-phase-c-prep.md line 108 — change risk code to RISK_OUT_OF_TREE_COMPONENT, keep "adjacent" in rationale
- F22: 10-morpheus-phase-c-prep.md line 430 — replace "see result below" placeholder with actual validate.py 4/4 PASS output
- F25: 10b-morpheus-r1-advisory-analysis.md line 157 — replace "see close-out" with actual validate.py 4/4 PASS output
- F26: 10b-morpheus-r1-advisory-analysis.md lines 105-106 — fix rollup to RBI=34, NUA=4
- F27: 10c-morpheus-rollback-ops-design.md line 57 — use `rm -f` for idempotent removal
- F28: 10c-morpheus-rollback-ops-design.md line 179 — replace placeholder with actual validate.py 4/4 PASS output

**Morpheus docs (ROUTE to Morpheus — engineering judgment needed):**
- F21: 10-morpheus-phase-c-prep.md lines 339-341 — add bounded read-only commands per PROVABLE row, or revise the closing claim. This requires Morpheus's corpus knowledge.
- F23: 10-morpheus-phase-c-prep.md lines 323-324 — adopt Partial/Yes blocked-status taxonomy. Requires understanding each row's provability.
- F24: 10-morpheus-phase-c-prep.md lines 426-428 — reconcile targeted-read counts with 2-3 file limit. Requires Morpheus's session knowledge.
- F29: 10c-morpheus-rollback-ops-design.md line 47 — hash stdout only, keep stderr separate. Requires understanding the headless dump mechanics.

**Gordon test code (ROUTE to Gordon — his lane):**
- F42: test_g6_orchestration.py lines 704-705 — rename boot_log to exit_code
- F43: test_g6_orchestration.py lines 441-442 — add `and not child_seed` to check_a
- F44: test_g6_orchestration.py lines 686-691 — assert fallbackMaxWords:11 retained after invalid edit
- F45: test_g6_orchestration.py lines 623-627 — record write result before raising
- F46: test_g7_surfaces.py lines 1280-1286 — separate FEEDBACK_ONLY and FULL captures
- F47: test_g7_surfaces.py lines 717-722 — re-read session log for determinism check
- F48: test_g7_surfaces.py line 501 — compute replacement-byte count in separate variable

**Chris/Wayne plan docs (fix directly — these are plans, not evidence):**
- F49: cache-integration-plan.md — fix SQL typos DEFALLT→DEFAULT, FUNCTIOM→FUNCTION, INSIRT→INSERT
- F50: cache-integration-plan.md lines 368-369 — note that LISTEN needs persistent client (add a labeled note; execution-time fix)
- F51: cache-integration-plan.md lines 187-188 — add FOR ROLE to ALTER DEFAULT PRIVILEGES
- F52: pg-implementation-plan.md line 363 — change backup dir to 0770
- F53: pg-implementation-plan.md lines 430-431 — add labeled correction: PG 18.6 installed/active
- F57: redis-plan.md line 141 — add /usr/local/bin/hx-redis-health.sh to rollback cleanup
- F58: redis-plan.md lines 110-116 — remove no-TTL option, all classes get finite TTL
- F60: redis-plan.md lines 120-121 — use keyspace_hits/keyspace_misses instead of commandstats
- F61: redis-plan.md lines 62-63 — restrict cache-service commands (not +@all), admin credential mechanism reference only
- F62: redis-plan.md lines 81-95 — add atomic versioned backup set note, record Redis package version

**Chris evidence docs (ROUTE to Chris — his lane):**
- F54: step1.md lines 350-352 — label LAN-scram as historical, append trust posture correction
- F55: step2.md lines 140-145 — V6 timer-fired activation evidence or downgrade claim
- F56: step2.md lines 117-125 — V4 current_user identity evidence

**Wayne Redis plan (already fixed on live system by governor — update plan to match):**
- F41/F59: redis-plan.md lines 48-49 — default user restricted (ALREADY FIXED on hxs-9 — update plan to match as-built)

## What you CANNOT fix

- Gordon's test code (F42–F48) — his lane. Route only.
- Chris's evidence docs (F54–F56) — his lane. Route only.
- Morpheus engineering judgment findings (F21, F23, F24, F29) — his lane. Route only.

## Constraints

- All governance-record changes are append-only, labeled, dated, originals preserved.
- No lane mutation — you do not edit Gordon's test files or Chris's evidence docs.
- `scripts/validate.py` 4/4 after writes. Render any manifest-listed .md you change.
- No secret values.
- Context budget: targeted reads, not whole-file dumps.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with the disposition table and validate.py output.