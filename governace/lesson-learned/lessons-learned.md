# Lessons learned

Newest first. Each entry: date, context in one line, the lesson, and what changes
because of it (a convention, a checklist, a KDD, or nothing).

## Entries

- 2026-09-01 — clarification of the dispatch incident entry below: the observed
  behavior is that three workers answered that no task was active or provided and
  produced no deliverable after the submitted payloads were recorded. The earlier
  entry is preserved as the original incident record, not as proof of cause.
  **UNVERIFIED:** conversation-history inheritance, caller payload dropping,
  harness delivery loss, malformed delivery, and working-directory/context
  explanations. Each remains a hypothesis until direct evidence establishes it.
  Change: use only the observed behavior for gate decisions; keep causal claims
  labeled and do not treat any harness mechanism as proven.
- 2026-09-01 — Phase A worker dispatch gave sub-agents the full conversation
  history; they re-described the intake instead of executing the work order and
  wrote no deliverable — **a worker must receive clean, self-contained context by
  default (identity, milestone, profile/charter paths, work order + context packet,
  read/write boundaries, deliverable destination, completion marker), never inherited
  conversation history; completion is the named non-empty deliverable at its exact
  destination, never turn-end.** Change: AGENTS.md dispatch guard now requires
  clean self-contained context; a worker's turn ending is not completion.
  [UNVERIFIED ROOT CAUSE 2026-09-01, append-only: the claim that `fork_turns=none`
  cannot deliver the message is NOT proven. The observed "no task" responses may
  indicate an empty, malformed, caller-dropped, or harness-lost payload, not an
  inherent fork_turns limitation. Evidence:
  governace/status-reporting/2026-09-01-dispatch-defect-evidence.md.]
- 2026-08-25 — review batches 1-7: the same defect appeared in up to 7 fixture files
  (stale /tmp sys.path, missing makedirs, hard-coded model alias) — **scratch
  scaffolding adopted into versioned fixtures must get a hardening pass: parameterize
  paths and model, guard every write, share helpers through the pinned module.**
  Change: fixture adoption includes a parameterization/shared-module check; MODEL is
  now an explicit required alias per run (the bare-alias retirement silently broke
  every hard-coded fixture).
- 2026-08-25 — goal status lines and catalog relations pointed at raw paths with no
  evidence refs; every one became a review finding — **a claim without a reference
  decays into a finding.** Change: status claims carry evidence paths/IDs at
  authoring; CAT-001 gains CAT-07 (canonical_location resolves) and CAT-08 (relation
  targets are DOC ids for cataloged artifacts).
- 2026-08-25 — three sessions independently invented "extract secret to a 0600 temp
  file" askpass variants — each contained, each needless — **agents re-invent the
  weakest pattern that is not written down; when a pattern improves, codify the new
  one and annotate the old evidence openly.** Change: all future work orders use
  read-at-execution askpass wording (no extracted copy); 26-rick and 30-esme
  annotated as security-process exceptions.
- 2026-08-25 — the catalog stored a sha256 of the credential file — an
  offline-cracking oracle for a short password — **a hash of a secret is a
  secret-derived verifier.** Change: verifier removed (batch 6); protected-resource
  records carry existence, owner, mechanism, attestation only; CAT-05 extended to
  forbid content digests of protected files.
- 2026-08-25 — A01's adoption left blended rules (§4.3/§4.4/§6.5 vs Revision 2) that
  took three review batches to mark — **supersession is scoped and marked at the
  source at adoption time, not retrofitted.** Change: adoption wave now includes
  inline superseded markings and section-scoped catalog relations in the same wave.
- 2026-08-25 — 148 records needed source.section backfill; 27 corpus records needed
  author/freshness reclassification — **truth-state labels are cheap at ingestion and
  expensive to retrofit; label conservatively** (unverified local snapshot unless a
  verifiable upstream URL/commit exists). Change: conservative labels are the
  ingestion default; source.section expected on all new records.
- 2026-08-25 — the preload unit ran a 20-minute start timeout against a 900-second
  D5 recovery SLO; measured 56 s hid the configured 1200 s — **budget arithmetic must
  bound the configured worst case, not just the measured happy path.** Change: every
  SLO gets a configured-budget cross-check (timeouts × retries) at design review;
  bounded preload fix queued for john.
- 2026-08-25 — review batches repeated themselves, contradicted owner directives,
  re-litigated ratified acceptances, and hallucinated a digest — **findings are
  untrusted input: verify against current code and ratified authority, reject with
  reasons, spot-check repeats.** Change: none new — the verify-first gate is the
  lesson, and it held.
- 2026-08-25 — the agents/john/carol nesting broke the catalog's canonical_location
  silently for ~24 h — **canonical paths are a contract; monitor them.** Change:
  covered by CAT-07.
- 2026-08-25 — "Xid" grep matched the NIC's "XID 64a" device string; a pgrep
  self-match raised a false alarm — **monitor patterns are scoped to their source
  and tested against known-benign output.** Change: NVRM-scoped Xid noted (state log
  row 47); expected-class convention (F-M7A-2) extended.
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
