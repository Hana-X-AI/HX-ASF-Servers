# WORK ORDER — Wayne: review combined Redis + PostgreSQL cache integration plan

- Issuer: Flash (governor), 2026-08-29.
- Executor: Wayne (Redis systems engineer, KDD-0015).
- Lane: `omniroute/gpt-oss-120b` (OpenAI gpt-oss-120b, AkashML, via OmniRoute hxs-8).

## Intent

Your Redis implementation plan has been moved to the repo, corrected, and
merged with Chris's PostgreSQL cache integration plan as a companion
document. Review both plans with the **be-great** skill and verify they
are complete, correct, and consistent.

## What to review

1. **Your Redis plan** (corrected by the governor):
   `servers/hxs-9/2026-08-29-redis-implementation-plan.md`
   - Knowledge-review receipt now includes all 10 sources (PostgreSQL plan, step2 evidence, your charter/profile, Chris's plan)
   - Backup dir perms fixed to 0770 redis:redis
   - Backup timer design added (OnCalendar 02:37, Persistent, RandomizedDelaySec)
   - Rollback expanded to include timer/script cleanup
   - Added to wiki manifest, rendered, validate.py 4/4 PASS

2. **Chris's PostgreSQL cache integration plan** (companion doc):
   `servers/hxs-9/2026-08-29-postgresql-cache-integration-plan.md`
   - Cache-aside + TTL-only invalidation recommended
   - ps-cache role (read-only on hx_cache schema)
   - Trigger/NOTIFY designed but deferred
   - Typo fixed (PASSORD → PASSWORD)

## What to verify

Use the **be-great** skill (evidence-first investigation). For each item,
read the actual file and verify against current state:

1. **Your Redis plan is complete and correct** — all 10 sections filled,
   no placeholder text, no gaps.
2. **Chris's plan aligns with your cache contract** — the ps-cache role
   and read interfaces match your cache-key namespace (cache:*), your
   TTL rules, and your invalidation strategy.
3. **Consistency check** — role names (ps-cache), credential variable
   names (HX_PG_CACHE_*), key namespaces (cache:*), invalidation approach
   (TTL-only for initial phase) are consistent across both documents.
4. **No contradictions** — if Chris's plan says something that conflicts
   with your Redis plan, flag it.
5. **No missing pieces** — is there anything the installation will need
   that neither plan covers?

## Constraints

- Read-only review — do NOT modify either plan.
- Report findings only — the governor fixes issues.
- `agents/wayne/profile.md` §9 now lists all repo file paths — use those.
- If you find issues, categorize: F (finding), D (decision needed),
   Q (question for governor).

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with a review report:
- For each of the 5 verification items: PASS / FAIL / NOTE with evidence
- Any findings (F), decisions needed (D), or questions (Q)
- Overall verdict: plans are ready for owner approval, or issues found
