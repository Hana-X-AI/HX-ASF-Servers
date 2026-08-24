# Lessons learned

Newest first. Each entry: date, context in one line, the lesson, and what changes
because of it (a convention, a checklist, a KDD, or nothing).

## Entries

- 2026-08-24 — a provided doc (`ox-alpha.md`) carried a live-looking API key under a
  false redaction note — **scan every provided document for credentials before
  adoption or use.** Change: secret scan is part of the adoption gate; key flagged
  to the owner for revocation and replacement.
- 2026-08-24 — John burned time chasing "craig", a superseded Claude Code-era
  specialist profile left at the top level of `/opt/tkv-local/ollama` — **the
  roster is `agents/`, not the knowledge vault.** Teammates and capabilities are
  resolved from `agents/` first; the vault is reference material and may hold
  stale or superseded profiles. Change: roster-first rule added to
  `agents/README.md` and John's startup protocol; the three stray craig files were
  removed from the vault top level (identical archived copies preserved under
  `implementation/archive/HX-Infrastructure-main/`); source mount `/opt/tkv` still
  holds copies pending owner cleanup.
- 2026-08-24 — Ollama audit pilot targeted hxs-5, which has no Ollama — **knowledge
  host is not workload host.** The knowledge authority (`/opt/tkv-local/ollama`)
  lives on hxs-5, and both the pilot doc and John's profile anchored the audit
  target to it. Change: intake must validate the target against SERVER-REGISTRY
  role/workload before commissioning; John's profile gains a reference-host vs
  target-host distinction.
- 2026-08-24 — no pre-flight check before the audit — **cheap existence checks run
  at intake, not during execution.** A registry lookup or `command -v ollama`
  would have ended it in seconds. Change: every goal targeting a component gets a
  pre-flight existence check (registry + one probe) recorded in the Intent and
  Authority Receipt before `GOAL_READY`.
- 2026-08-24 — John proceeded past a missing baseline — **no ratified baseline for
  the component on the target is a BLOCKED condition, not a proceed-with-gap
  condition.** Change: John's knowledge-review receipt must answer `Task May
  Proceed: NO` when authority/version for the component on the target is NOT
  ESTABLISHED, unless the goal is explicitly a conformance/absence check.
- 2026-08-24 — the governor gate verified evidence quality but not objective
  fitness — **a perfect package for a hollow goal is still a FAIL.** Change: the
  Kimi-K3 gate adds an objective-fitness question: was the goal well-posed against
  ratified authority before execution?
- 2026-08-24 — dual technical+process objectives masked the collapse of the
  technical objective — **process validation must not create pressure to continue
  when the technical premise is gone.** Change: process metrics are reported
  separately and never compensate for a failed technical objective.
