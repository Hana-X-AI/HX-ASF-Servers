# KDD-0022: CodeRabbit reviews the pushed range, not the whole branch

- Date: 2026-08-30
- Status: ratified
- Decider: Agent-Zero
- Related: `.github/workflows/ci-cd.yml`, `docs/cicd-pipeline.md`, owner directive 2026-08-28 (zero-tolerance review gate), Codex full-repository audit `codex_20260830_1510` — **this decision knowingly reverses one of its "do not reopen" items**

## Context

`coderabbit-review` failed on **every push for roughly three hours** on
2026-08-30 with `Error: WebSocket closed`. It was misdiagnosed at length as a
vendor problem: the owner was asked to check billing, seat assignment and
organization access, and regenerated the API key five times. None of that was
the cause, and the owner's own instinct — *"it was probably never broken"* —
was correct.

The cause is **review payload size**, and it was introduced by this repository,
not the vendor.

Feature branches were reviewed with `--base origin/main`, so the CLI uploads the
**entire accumulated branch diff**, which grows with every push. Commit
`e8fc5c2` (KDD-0020) added roughly 100 files of generated skill mirrors plus a
170-file vendored project to that diff. The break aligns exactly with it:

| Run | Diff uploaded | Result |
|---|---|---|
| 14:15, `fdbe905` | 15 files, 788 insertions | reviewed normally, findings returned in 4m29s |
| 15:10, `e8fc5c2` | 332 files, 14,643 insertions | `WebSocket closed` |
| 17:19 | 417 files, 1.5 MB | `WebSocket closed` in ~2s |

**Direct proof**, run against the same key, account and machine:

- a **2-file** diff progresses `setup → analyzing → reviewing` and emits
  heartbeats — the connection is stable;
- a **417-file** diff closes the socket in about two seconds.

Two intermediate fixes were attempted and did not work:

1. `path_filters` in `.coderabbit.yaml` were extended to exclude the generated
   mirrors and vendored `archify`. No effect — those filters are applied
   **server-side**, so the CLI still uploads everything. The exclusions are kept
   because they are correct on their own merits, but they do not address this.
2. `--region us` was made explicit for inline api-key auth. No effect; the
   account is US and the default was already correct. Kept as a correctness
   improvement, not a fix.

## Options considered

1. **Keep `--base origin/main`.** Preserves the audit's guidance. Rejected: the
   gate is then physically unable to run on any branch of material size, which
   is worse than a narrower review — a check that cannot execute reviews nothing.
2. **Split work into many small branches.** Would keep each diff small, but it
   is a process change imposed by a tool limit, and it does not help a branch
   that is already large.
3. **Review the pushed range (`--base-commit "$BEFORE"`).** **Selected.** Each
   push reviews only its own delta, which is exactly what the `main`-branch path
   in this same workflow already did.

## Decision

Feature-branch pushes review `BEFORE..HEAD` — the pushed range — instead of the
whole branch diff. `BEFORE` is `github.event.before`. It falls back to
`--base origin/main` when `BEFORE` is absent, all-zeros (the first push of a new
branch), or unresolvable (after a force-push). The job logs which base it chose
and the resulting file count.

### Conflict with the audit, stated plainly

The Codex audit of 2026-08-30 lists under **"What not to do"**:

> *Do not narrow feature-branch review from `origin/main` to only the latest commit.*

**This decision reverses that item**, with the owner's explicit word
("narrow it", 2026-08-30). The audit's guidance is sound in the abstract —
whole-branch review catches a defect introduced early and never fixed — but it
was written without the evidence above, and it assumes the review runs at all.
It does not, past a few hundred files. A narrower review that executes is worth
more than a broader one that cannot.

**Accepted cost.** A finding introduced in an early push and not fixed is not
re-raised by later pushes. Mitigation: the CodeRabbit GitHub App, if installed,
reviews the PR head natively and covers the accumulated diff; the deterministic
`gates` job always runs against the full tree regardless of push size; and any
branch may be re-reviewed whole by dispatching a run with the base overridden.

## Consequences

**Enables.** The review gate can execute again. Payload is bounded by a single
push rather than by branch age, so it no longer degrades as work continues.

**Forecloses.** Whole-branch review on feature branches by default.

**Must be revisited if.** The vendor raises the payload ceiling or the CLI gains
client-side path filtering (which would let `path_filters` actually reduce the
upload and make whole-branch review viable again) — at which point the audit's
original guidance should be restored.

**Process finding of record.** The failure was attributed to an external service
for three hours while the cause sat in this repository's own diff. The check
that would have found it immediately is to compare the failing run's diff size
against the last passing run's. Rule adopted: when a gate breaks immediately
after a change of ours, correlate the break with our own diff **before**
attributing it to a third party, and never ask the owner to modify an external
system on that basis until it has been ruled out.
