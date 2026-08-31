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

## Amendment 1 (2026-08-30, labeled, append-only) — a cancelled review is a lost review

[OPEN CORRECTION 2026-08-30, labeled, append-only — CONCURRENCY: the decision
above stands. It established that the review covers the PUSHED RANGE
(`BEFORE..HEAD`) rather than the whole branch, because a whole-branch payload
grows with every push until the service drops the socket. That reasoning is
unchanged. This amendment records a consequence of it that the original decision
did not follow through, and the workflow change that closes it.]

**The defect.** `ci-cd.yml` carried `concurrency: cancel-in-progress: true`.
Combined with a pushed-range review, cancelling a run does not merely discard
that run's output — it **permanently destroys the only review that range will
ever receive**. The next run computes its own `BEFORE` from the new push and
never looks back. Whole-branch review would have been self-healing here; a
pushed-range review is not, and nothing compensated for that.

**Proven, not theoretical.** On 2026-08-30 two pushes in quick succession
cancelled the reviews of `b489216` and `d2d8a31` on branch
`feat/o5-o7-capability-manifests`. PR #7 then auto-merged on a green check that
had examined only the final commit's range. **565 insertions reached `main`
unreviewed**, including `scripts/skills_registry.py` in its entirety (224 lines),
85 lines of change to `scripts/hooks_verify.py` and 47 to `scripts/validate.py`.
The cancelled jobs terminated before their parse step, so no findings reached
the CI log and none are recoverable.

The zero-tolerance directive of 2026-08-28 makes this worse rather than better:
a gate that blocks on every finding is also a gate whose silence is read as
approval, so a review that never ran is indistinguishable from a review that
found nothing.

**The fix.** `cancel-in-progress: false`. Runs queue and execute in order, so
every pushed range is reviewed before auto-merge can observe a green check.
`gates` completes in about 15 seconds, so the queueing cost is small measured
against merging unreviewed code.

**What this does not fix.** The two ranges already merged. Reviewing them
requires a review over `a95595f..f4e20a6`, which is an owner action.

Authority: owner directive 2026-08-30 ("no more commits without my approval")
following the owner's own detection of the gap.

### Amendment 1 — correction (2026-08-30, labeled, append-only)

[OPEN CORRECTION 2026-08-30, labeled, append-only — TWO ERRORS IN AMENDMENT 1
ABOVE, found in review. The amendment's diagnosis is unchanged: a cancelled
pushed-range review is unrecoverable. Its stated fix was insufficient and two of
its figures were wrong. The original wording above is preserved as history.]

**1. `cancel-in-progress: false` does not give an ordered queue.** The amendment
says "runs queue and execute in order, so every pushed range is reviewed". That
overstates what GitHub provides. A concurrency group retains **at most one
pending run**: when one run is in progress and a second is pending, a third push
**cancels the pending one**. Rapid pushes would still have lost ranges, just
fewer of them.

There is no queue-depth or "max" setting to raise — `group` and
`cancel-in-progress` are the only keys `concurrency` accepts. The workflow now
uses `group: ci-${{ github.ref }}-${{ github.sha }}`, one group per commit, so no
run ever contends with another and none is cancelled. The cost is concurrent
runners instead of serialized ones.

**2. The insertion count and its attribution.** The amendment says "565
insertions reached `main` unreviewed". That figure is `b489216` alone. The second
cancelled range, `d2d8a31`, added 47 insertions across 3 files. **The correct
total is 612 insertions**, 565 from `b489216` (96 files, including
`scripts/skills_registry.py` entire) and 47 from `d2d8a31`
(`scripts/README.md`, `scripts/hooks/README.md`, `DOC-scripts-hooks.yaml`).

**3. Evidence identifiers, recorded for the first time.** The cancelled runs are
`33334670361` (head `b489216`) and `33334985041` (head `d2d8a31`), both on branch
`feat/o5-o7-capability-manifests`. PR #7 was **squash-merged**, so neither commit
exists on `main` as itself — their content is inside the single squash commit
`f4e20a6`. A review covering the unreviewed content must therefore address the
merged range `a95595f..f4e20a6`, not the branch shas, which is why the owner
action named in the amendment is stated against that range.

Authority: CodeRabbit review 2026-08-30; verified against the live workflow and
`gh run list` before correcting.

### Amendment 1 — second correction (2026-08-30, labeled, append-only)

[OPEN CORRECTION 2026-08-30, labeled, append-only — THE FIRST CORRECTION WAS
ALSO WRONG. It asserted: "There is no queue-depth or 'max' setting to raise —
`group` and `cancel-in-progress` are the only keys `concurrency` accepts." That
statement is FALSE and was made twice, in this record and in the workflow
comment, from stale knowledge rather than from the documentation. Both prior
texts are preserved above as history.]

**`concurrency` accepts a third key, `queue`.** Verified against the GitHub
Actions workflow-syntax reference on 2026-08-30:

- `queue: single` (the default) — at most ONE run may be pending in the group.
  This is why `cancel-in-progress: false` alone did not fix anything: a third
  push cancels the pending run.
- `queue: max` — up to **100** runs may be pending in the group. Beyond 100,
  additional runs are cancelled.
- `queue: max` with `cancel-in-progress: true` is a workflow validation error.

**Current configuration**, replacing both earlier attempts:

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: false
  queue: max
```

**Why the second attempt is also retired.** Adding `${{ github.sha }}` to the
group did prevent cancellation, but by making every push its own group nothing
ever contended — which defeats the purpose of a concurrency group and spends a
concurrent runner per push. It solved the symptom by removing the mechanism.

**The bound, stated rather than overclaimed.** Serialization holds up to 100
pending runs on one branch; beyond that GitHub cancels the excess. That ceiling
is not reachable by hand-driven pushes. The first correction's failure mode was
claiming a guarantee stronger than the platform gives, so this one names the
limit instead of implying there is none.

**Process note.** Both errors were the same class: an assertion about an
external system's current behaviour, made from memory and stated with
confidence, without consulting that system's documentation. The rule already on
record in this KDD — correlate a break with our own diff before attributing it
to a third party — has a companion: **do not assert what a third-party product
does or does not support without checking its current reference.**

Authority: CodeRabbit review 2026-08-30, twice; verified against
docs.github.com Actions workflow syntax before this correction was written.
