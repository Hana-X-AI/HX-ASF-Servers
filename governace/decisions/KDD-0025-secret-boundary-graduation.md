# KDD-0025: The secret-boundary graduation test, and why the flip is still the owner's (O6)

- Date: 2026-08-30
- Status: ratified (evidence); **the warn → block flip is NOT taken — owner decision**
- Decider: Agent-Zero (owner decision UD4, 2026-08-25, authorized the graduation)
- Related: `scripts/hooks/secret-boundary.sh`, `scripts/hooks/secret-boundary.mode`,
  `scripts/validate.py`, `governace/secret-boundary-corpus.yaml`,
  `scripts/test_secret_boundary.py`, KDD-0023 (SY-5 governs the mode file),
  Codex process-optimization review `codex_20260830_1539` (O6)

## Context

`secret-boundary.mode` has read `warn` since 2026-08-25 — **five days** as of
this decision on 2026-08-30. The hook's own header says graduation to `block` is
"a one-word edit after the pilot week". That week has not yet elapsed; it ends
around 2026-09-01. What is missing is not elapsed time but measurement: nothing
in those five days measured the hook's behaviour, and the review's O6 asks for
exactly that — *"Graduate secret-boundary to block only after a regression suite
proves acceptable false-positive rates."*

**The suite did not exist.** `tests/` contains a README marked "STATUS: FUTURE".
The only recorded testing is a one-off of 6 standalone cases in state-log row 61
(2026-08-25) that was never committed as a script.

**Three false positives are on record, and none came from the hook.** All three
came from `validate.py`'s repo-wide sweep, which is *already blocking in CI*:

| # | Where | What tripped it |
|---|---|---|
| 1 | `servers/hxs-3/configuration.md:107` | password-assignment prose — CI red four times (DSH row 5) |
| 2 | `gordon/phase-a/gordon_util.py:75` | a comment describing the scanner's own pattern (DSH rows 16, 20) |
| 3 | `PILOT-OMNIROUTE-LAYER0-001` row 40 | an owner directive clause in assignment-style prose |

**The cost was not inconvenience.** Twice a false positive forced an
**append-only record to be edited in place**: DSH row 5 and OMNIROUTE row 40 were
both de-patterned to clear the gate. DSH row 5 states that restoring the original
is not possible, because doing so would re-trip the scanner. A scanner that flags
prose does not merely annoy — it forced two governance violations and made one
of them permanent.

## Findings

**F1 — Two implementations, disagreeing on four of five rules.** The hook scans
tool payloads in bash; `validate.py` scans files in Python. They were written
separately and nothing compared them.

| rule | hook | validate.py (before) |
|---|---|---|
| PEM | `BEGIN [A-Z ]*PRIVATE KEY` | `BEGIN [A-Z0-9 ]*PRIVATE KEY` |
| Slack | `xox[baprs]-[A-Za-z0-9-]{10,}` | `xox[baprs]-` — bare prefix |
| password | bounded charset, `{6,}` | `\S+` — any non-space |
| allowance | present | **absent** |

`validate.py` was the broader one and is the blocking one. That is the whole
explanation for why all three incidents came from it.

**F2 — The hook's allowance was nearly dead code.** It ran `grep -Eo`, which
emits only the matched fragment, and then filtered that fragment for
`REDACTED|withheld|never printed|askpass`. A sanitizing word anywhere else in the
sentence never reached the filter. `password: supplied by the askpass helper` —
a reference to the ratified mechanism — was a hit. Measured, not inferred: it is
case `fp-askpass-mechanism` in the corpus, which the hook failed before this
change.

**F3 — The corpus cannot be stored in plain text.** A file of things that look
like credentials trips the scanners it tests on every run. The only escapes are
exempting the file — which is how a scanner stops being trusted — or weakening
the patterns. Cases are therefore base64 with a plain-language `description`, and
a test asserts the corpus file itself produces zero hits.

## Decision

**D1 — The corpus is the contract.** `governace/secret-boundary-corpus.yaml`
holds 14 cases: 6 credential shapes that must flag, 8 prose and sanitized forms
that must not. The three recorded incidents are represented by shape — their
originals are unrecoverable by design, per DSH row 5.

**D2 — Both implementations run against it.** `scripts/test_secret_boundary.py`
executes every case against the hook (as a real payload, via bash) and against
`validate.py` (via the real `_secret_scan`, not a reimplementation — an earlier
draft reimplemented the patterns in the test and went stale the moment the
password rule moved, reporting a live credential as unflagged). A parity test
asserts the two agree on every case, so a fix to one cannot silently leave the
other behind. Wired into CI gates.

**D3 — A password value must look like a credential.** Every recorded false
positive was an English word standing where a value would go: `field`,
`assignment`, `supplied`, `set`. A value now counts only if it carries a digit or
punctuation, or is at least 16 characters. The allowance is tested against the
whole line, not the matched fragment.

**STATED BOUND:** an all-lowercase passphrase under 16 characters with no digit
or punctuation is not caught by this generic net. That is a deliberate trade.
Flagging prose is the worse failure — it forced two append-only violations — and
the generic net was never the last line: the hook's layer 2 reads the literal HX
credential at execution time, and the governor-only literal sweep is a standing
manual gate.

**D4 — Safety proven by differential, not by assertion.** The old and new pattern
sets were run over every file in the repository (1,384 scanned). The narrowing
loses exactly **two** hits, and both are comments *inside the two scanners*
describing the false-positive class — incident #2's shape, reproducing live. The
new scanner reports **zero hits repo-wide**. No real detection is lost.

**D5 — THE FLIP IS NOT TAKEN.** `secret-boundary.mode` still reads `warn`, and a
test asserts it. This decision delivers the evidence UD4 asked for; it does not
consume the authorization. Graduation makes one hook able to halt a write
mid-session, and that is an owner decision made against evidence, not a side
effect of producing the evidence.

## What the owner needs in order to decide

- **For:** the corpus is green on both implementations; the two are now
  reconciled and pinned against divergence; every recorded incident is covered;
  the narrowing costs nothing measurable repo-wide.
- **Against:** the corpus is 14 cases, not a field-measured false-positive rate.
  It proves the *known* failure modes are handled, not that no unknown one
  exists. The recorded incidents span five days of one project's history.
- **Reversal is cheap.** The flip is one word in `secret-boundary.mode`, and
  SY-5 pins that file's content and digest, so a change in either direction is
  visible in the gate rather than silent.

**Recommendation: flip it once the pilot week completes (~2026-09-01) with the
corpus green in CI.** The evidence is good and the reversal is cheap, but the
corpus has existed for hours. Running the remaining days of the pilot with the
reconciled patterns in CI turns "the known failure modes are handled" into "no
new ones surfaced under real traffic", which is the claim graduation actually
rests on. That also honours UD4's own condition rather than pre-empting it.

## Consequences

**Enables.** The two scanners can no longer drift apart unnoticed. The
false-positive class that forced two append-only violations is regression-tested.

**Forecloses.** Flipping the mode without evidence, and "fixing" a false positive
by editing the record it flagged.

**Costs.** The corpus must grow when a new false-positive class is found. That is
the intended maintenance: a case added is cheaper than a governance record
rewritten.

**Must be revisited if.** A false positive appears that the corpus does not
cover, or a real credential shape is found that the narrowed patterns miss — the
stated bound in D3 is the first place to look.
