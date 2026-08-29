# WORK ORDER — Morpheus: fill Phase C prep doc (Product 1, new lane)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Morpheus (dsh lifecycle steward, KDD-0009).
- Lane: `omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B, provider DeepInfra, via OmniRoute hxs-8).
- Controlling work order: 09a (as corrected for the new lane).

## Intent

Fill the placeholder sections in `pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md`.
The skeleton already exists with all section headings. Your job is to fill each
section with source-grounded content from the pinned corpus.

## What to fill

For each of the 4 families (I/O interop, Sandbox, Remote endpoint, Experimental):

1. **Source seams** — exact file:line references in `/opt/tkv-local/deepseek-harness-master`
2. **Activation mechanism** — cordis class + pattern per your Phase A/B template
3. **Host prerequisites** — required packages/daemon state on target hosts
4. **Risk classification** — RISK_* code from your Phase B taxonomy with one-line rationale

Then fill:
- **Testability matrix** — one row per seam: what Gordon can prove read-only, what is BLOCKED-by-design
- **Open risks & items** — filled last, after all families assessed
- **Knowledge-review receipt** — your working-order receipt
- **Sanitized command log** — any read-only commands you ran against the corpus

## Discipline (from 09a, still binding)

- Write-first + incremental writes: save the document after each family is filled.
- Targeted reads only: at most 2-3 corpus files per family. Never broad surveys.
- 131K context on this lane (2x Coder-X) — more headroom, but don't waste it.
- If context tightens: stop reading, close per the completion gates below.

## Hard boundary (unchanged, absolute)

NO candidate mutation of any kind on hxs-15. Gordon's campaign is running
against the frozen candidate. No hxs-15 contact at all this session. Any
read-only status need goes through the governor.

## Constraints

- Read-only against `/opt/tkv-local/deepseek-harness-master` — no writes there.
- Only write to `pilots/PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md`.
- `python3 scripts/validate.py` 4/4 after writes.
- No credential-shaped literals.
- Append-only for governance records; labeled corrections only.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` only when ALL sections are filled
(every family row, testability matrix, risks, receipt, command log) AND
validate.py 4/4 PASS is pasted.

`[TASK PAUSED — ESCALATION TO GOVERNOR]` with the named remainder if
anything blocks or the context budget is exhausted. Never put a completion
marker on partial content.
