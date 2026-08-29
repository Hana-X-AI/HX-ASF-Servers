# Read-Only Project Capability Assessment — Hooks, Skills, MCP, Marketplace Plugins

| Field | Value |
| --- | --- |
| Date | 2026-08-25 |
| Author | Kimi-K3 (governor), under owner directive "Read-Only Project Capability Assessment" |
| Operating boundary | READ-ONLY honored: no files created/edited/moved/deleted, no capabilities installed/enabled/configured, no mutating commands executed, no opportunity treated as authorization. The only artifacts produced are this report and its conventional `.html` rendering (dual-format convention, ratified 2026-08-25). Queued follow-ups outside this directive's scope: Carol cataloging, wiki-manifest inclusion, state-log citation, and every adoption decision below — all await owner word. |
| Report destination | Owner template arrived with `[INSERT REPORT DESTINATION]` unfilled; placed per repo convention at `knowledge/assessments/2026-08-25-capability-assessment-read-only.md` |
| Product facts verified | Kimi Code official docs fetched 2026-08-25: hooks (`customization/hooks.html`), MCP (`customization/mcp.html`) |
| Companion directive | "Standing Directive: Second Brain Roadmap Integration" (owner, 2026-08-25) — ratified into AGENTS.md; section 11 of this report answers it for every item |

## 1. Executive summary

The project's agent workflow is strong on discipline and thin on deterministic
enforcement at the tool layer. The four highest-value opportunities are small,
boring, and enforce things we already agreed to do by hand: a **secret-boundary
pre-write hook** (O1), a **wiki-sync hook** (O2), a **work-order authoring skill**
(O4), and an **evidence-verification skill** (O5). Two pilots are worth their
verification cost: a **fixtures hash/test hook** (O3) and a **read-only,
write-disabled filesystem MCP scoped to `/opt/tkv-local`** (O7). Everything
database-shaped, remote-model-shaped, or plugin-shaped is deferred with named
triggers (O8, O9) or rejected outright. No marketplace plugin is recommended for
adoption: no measured gap exists that built-ins, hooks, skills, or the approved
Bash/SSH pattern do not already close.

## 2. Project areas reviewed

- Agent roster and lane model (`agents/`: kimi-k3, john, rick, carol; charters/profiles)
- Governor workflows: work orders, context packets, evidence verification, state log
- Carol lane: catalog (172 records), receipts, retrieval packages, CAT-001/CB-001 batteries
- Fixture harness (`fixtures/`, 57-test regression battery, sha256 manifest)
- Scripts (`scripts/`: fleet-control README conventions; `scripts/wiki/` renderer + manifest, 29 dual-format documents)
- Skills: 10 owner skills at project and user scope + 3 built-ins
- MCP: project `.kimi-code/mcp.json` (one staged, disabled server: `mobbin`), no user-scope mcp.json
- Hooks: none configured (`config.toml` carries no `[[hooks]]`)
- Plugins: no plugins directory; none installed
- Infrastructure posture: hxs-1 Ollama loopback-only (ratified SC-07), hxs-5 session host, SSH fleet pattern (no Ansible), askpass read-at-execution pattern (ratified 2026-08-25)

## 3. Current capability inventory

| Layer | What exists today | Evidence |
| --- | --- | --- |
| Skills | be-great, be-smart, bro, copy, corp, eli5, evidence-first-research, human, quick, wait-what (project + user scope); built-ins: check-kimi-code-docs, update-config, write-goal | `~/.kimi-code/skills/`, repo `.kimi-code/skills/` |
| MCP | `mobbin` HTTP server staged but `enabled: false` (design-reference pilot, needs OAuth) | repo `.kimi-code/mcp.json` |
| Hooks | None | `~/.kimi-code/config.toml` (no `[[hooks]]`) |
| Plugins | None | no `~/.kimi-code/plugins` |
| Deterministic gates | CAT-001 acceptance battery (incl. CAT-05 secret sweep, CAT-07/08), CB-001 Carol bounds audit, test_fixtures.py (57 tests), sha256 manifests, render.py `--check` | repo `knowledge/catalog/tests/`, `fixtures/`, `scripts/wiki/` |
| Fleet access | Approved Bash/SSH pattern, askpass read-at-execution, NOPASSWD sudo (F-M5-2, owner-accepted) | `scripts/README.md`, pilot evidence |
| External review | CodeRabbit / GitHub Copilot review batches (7 batches dispositioned this week) | state log rows 33–52 |

## 4. Opportunity matrix

| ID | Capability | Need addressed | Value | Integration | Risk | Disposition | Trigger/phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O1 | PreToolUse secret-boundary hook | Secrets have reached temp files twice (F-M5-1; 0600 extractions ×2) | High — blocks the incident class at write time | `[[hooks]]` user config → repo script | Low (fail-open design; false positives on evidence docs) | **Adopt (pilot)** | Now, owner approval |
| O2 | PostToolUse wiki-sync hook | HTML/MD sync is manual; AGENTS.html already drifted once | Medium — removes a drift class deterministically | Same pattern as O1 | Very low (idempotent renderer) | **Adopt (pilot)** | Now, owner approval |
| O3 | PostToolUse fixtures hash/test hook | Manifest drift if a fixture edit skips re-hash/tests | Medium — makes the existing discipline automatic | Same pattern | Low (test suite is seconds; 30 s cap) | **Pilot** | After O1/O2 prove the pattern |
| O4 | Work-order authoring skill | WO/CP YAML is hand-written per milestone (10+ this week) | Medium — standardizes, shortens, fewer omissions | `.kimi-code/skills/` project scope | Very low (documentation) | **Adopt** | Now |
| O5 | Evidence-verification skill | Governor's receipt-check ritual is identical every run | Medium — one checklist, less governor variance | `.kimi-code/skills/` | Very low | **Adopt** | Now |
| O6 | Catalog-query skill | R2 verdict header (ratified) changes how packets are requested/consumed | Low-Medium | `.kimi-code/skills/` | Low | **Pilot** | First R2-gated retrieval cycle |
| O7 | Read-only filesystem MCP scoped to `/opt/tkv-local` | TKV surveys run through Bash with discipline-only read bounds | Medium — tool-layer read-only, matches Carol's no-probe bound | stdio MCP, project mcp.json | Medium (node/npx dependency; YOLO auto-approval interplay; trust prompt) | **Pilot** | Verify deps + YOLO behavior first |
| O8 | Ollama MCP for hxs-1 | Structured model access for agents | High but conflicts with ratified loopback-only posture (SC-07) | Would need a network path | High (new exposure surface) | **Defer** | Owner D1/OmniRoute decision |
| O9 | Catalog DB / vector-graph index (PostgreSQL/Qdrant/Neo4j MCP) | Richer catalog queries | Unproven need; file-backed passes CAT at 19× economy | MCP or service | Medium (premature complexity) | **Defer** | Second Brain G-06 benchmark trigger |
| O10 | Git/GitHub, SSH/fleet, utility MCPs; generic plugins | Convenience only | Below threshold | — | — | **Reject** | — |

## 5. Detail on the significant opportunities

### O1 — PreToolUse secret-boundary hook (hooks)

1. **Need/limitation:** F-M5-1 (secret in a temp log, contained <1 min) and two
   sessions independently creating 0600 temp-secret files. Discipline contained
   every instance; nothing *prevents* the class. Second Brain doc Principle 2:
   where failure must be constrained, use deterministic controls, not judgment.
2. **Proposal:** `[[hooks]]` entry — `event = "PreToolUse"`, `matcher = "Write|Edit|Bash"`,
   `command = /home/hxsa/opt/HX-ASF-Servers/scripts/hooks/secret-boundary.sh` (new,
   reviewed, repo-versioned script; only the registration lives in user
   `config.toml`). The script parses the stdin JSON's `tool_input` and fires on
   three layers: (1) generic credential patterns (PEM blocks, token formats,
   live-looking password assignments, with a REDACTED/withheld allowance); (2) the
   literal HX credential, read at execution from the protected source, never stored
   or printed; (3) the protected source referenced as a copy-verb argument
   (`cat|cp|dd|tee|scp|rsync|tar` … `ssh-info.md`) — the path-based copy class,
   with read-at-execution patterns (awk/sed/grep) explicitly allowed. Exits `2`
   (block) with a stderr reason on hit, `0` otherwise. Detection guarantee, stated
   plainly (corrected 2026-08-26 per review finding): the hook sees only what is
   present in a matched tool's payload; it does not see content moved through
   channels outside Write/Edit/Bash, encoded or obfuscated payloads, or copy paths
   that avoid the named verbs.
3. **Purpose/value:** converts containment-after-the-fact into prevention-at-write-time
   **at the payload boundary** — the demonstrated incident class (secret literal,
   pattern-shaped material, or a protected-source copy attempt present in a
   Write/Edit/Bash payload) is caught before execution. It is NOT a guarantee
   against every exfiltration path (field 5), and CAT-05 remains the whole-catalog
   post-hoc net.
4. **Integration:** hook event before tool execution; script in `scripts/hooks/`
   beside the wiki renderer; complements CAT-05 (post-hoc sweep) as a pre-hoc gate.
5. **Dependencies/permissions/security:** hooks execute shell on hxs-5 at every
   matching tool call — the script must be repo-reviewed like code, carry no
   secrets, log no payload content, and stay under a 5–10 s timeout. **The hook
   system is fail-open by design** (script error/timeout = allow, per official
   docs): this is an interception layer, never the sole barrier — CAT-05, the
   protected-resource convention, and owner attestation remain the boundary.
   Boundary documented per review finding: the guarantee is detection of secret
   material present in matched tool payloads plus the named protected-source copy
   verbs; it does not cover (a) content moved outside Write/Edit/Bash payloads,
   (b) encoded/obfuscated content, (c) copy verbs outside the named set, (d) the
   human editor channel — hooks fire on agent tool calls only.
6. **Overlap/conflict:** none with existing gates (they are post-hoc); false
   positive class = evidence documents quoting pattern-shaped strings — mitigate
   with a REDACTED/withheld allowance list and pattern precision.
7. **Disposition:** adopt (pilot).
8. **Evidence:** F-M5-1 record; state-log rows 52–53 (0600 extraction class);
   hooks.html (PreToolUse blockable, exit-2 semantics, fail-open caution).
9. **Phase/trigger:** immediately upon owner approval; graduate from warn-mode to
   block-mode after one clean week.
10. **Second Brain effect:** advances the roadmap's deterministic-controls
    principle and its secret-quarantine pattern (§9 risk table) with zero new
    architecture. Standing-directive disposition: **recommended for this
    iteration** upon approval.

### O2 — PostToolUse wiki-sync hook (hooks)

1. **Need:** dual-format ratified today; sync currently depends on someone
   remembering to re-render — AGENTS.html drifted within hours of the first wave.
2. **Proposal:** `PostToolUse` hook, `matcher = "Edit|Write"`; script maps the
   edited path against `scripts/wiki/manifest.txt` and re-renders just that file
   via `scripts/wiki/render.py <file>`.
3. **Value:** drift class eliminated at the source; `--check` stays as the audit.
4. **Integration:** post-tool observation event with an idempotent side effect;
   no main-flow impact (fail-open acceptable by design here).
5. **Dependencies/security:** same hook-execution considerations as O1; renderer
   is stdlib and sub-second per file; timeout 10 s.
6. **Overlap:** none; the manual re-render convention remains as fallback.
7. **Disposition:** adopt (pilot).
8. **Evidence:** today's dual-format implementation (state-log row 55); observed
   same-day drift; hooks.html (PostToolUse observation semantics).
9. **Phase:** with O1.
10. **Second Brain effect:** keeps the canonical record and its human rendering
    synchronized — Principle 3 (externalized, maintainable state). Disposition:
    **recommended for this iteration** upon approval.

### O3 — PostToolUse fixtures hash/test hook (hooks)

- Need: fixture edits must always end with re-hash + green suite; twice this week
  that ordering depended on the operator. Proposal: PostToolUse matcher
  `Edit|Write`, path filter `fixtures/*.py` → run BOTH commands from the fixtures
  directory (`cd pilots/PILOT-HX1-OLLAMA-QWEN27B-001/fixtures && sha256sum *.py >
  sha256sums.txt && python3 -m unittest -q test_fixtures.py`, 30 s cap) — hashing
  reads the intended fixture Python files and the checksum file is written in the
  fixtures location (corrected 2026-08-26 per review finding). Disposition: **pilot after O1/O2**
  prove the hook pattern; risk: an ill-timed auto-test mid-multi-edit is noise —
  acceptable, observation-only. Second Brain effect: regression fixtures are the
  roadmap's "repeated failure → regression fixture" mechanism; this makes their
  upkeep automatic. Disposition: **recommended for next iteration.**

### O4 — Work-order authoring skill (skills)

1. **Need:** every milestone hand-crafts the same WO/CP YAML; structure is stable,
   authoring is repetitive, and omissions (controlling sources, boundaries,
   receipt expectations) have needed governor corrections.
2. **Proposal:** project skill `dispatch` encoding the WO/CP templates, the
   controlling-sources checklist (role TKV + `/opt/tkv-local/servers/<host>/` +
   catalog retrieval + registry), the boundaries vocabulary (askpass
   read-at-execution, verify-identity-first, no-hardcoding), and — per the new
   standing directive — the mandatory Second Brain opportunity evaluation block.
3. **Value:** fewer omissions, faster commissioning, the standing directive
   enforced structurally instead of by memory.
4. **Integration:** `.kimi-code/skills/dispatch/` project scope, invoked by the
   governor at milestone staging.
5. **Dependencies/security:** none beyond the skills system; content is
   documentation, not executable code.
6. **Overlap:** complements agent profiles (they consume work orders; the skill
   authors them).
7. **Disposition:** adopt.
8. **Evidence:** 10+ work orders authored this week with identical structure;
   correction findings aimed at packet completeness.
9. **Phase:** now.
10. **Second Brain effect:** carries the standing directive's mandatory
    evaluation into every future dispatch; pattern-library candidate
    (dispatch-pattern) once used twice. Disposition: **implemented-as-skill
    recommended upon approval.**

### O5 — Evidence-verification skill (skills)

- Need: the governor's verification ritual (artifact exists → receipt line →
  FAIL/BLOCKED token context check → secret sweep → WO/CP hash integrity →
  deliverable claims vs live state) is identical for every milestone and lives
  only in governor habit. Proposal: project skill `receipt-check` encoding the
  checklist with the escalation rules (when a token is benign vs a stop).
  Disposition: **adopt now.** Second Brain effect: the handoff-receipt contract
  made teachable and uniform; pairs with O4. Disposition: **recommended for this
  iteration upon approval.**

### O6 — Catalog-query skill (skills)

- Need: R2 (ratified today) makes `suitable_for_execution` verdict headers
  mandatory on retrieval packages; agents need a standard way to request and
  read packets. Proposal: a small `catalog-query` skill (request format, verdict
  header semantics, truth-state labels, escalation on `false`). Disposition:
  **pilot after the first R2-gated retrieval cycle** proves the packet format
  in practice; writing it earlier would codify an untested format. Second Brain
  effect: direct roadmap advancement (scoped retrieval stage). Disposition:
  **deliberately deferred one iteration, trigger named.**

### O7 — Read-only filesystem MCP for `/opt/tkv-local` (MCP)

1. **Need:** AGENTS.md requires TKV surveys per assignment; they run through
   Bash, where read-only intent is discipline, not enforcement. Carol's bound
   ("no host probes"; documents-only) would be stronger if the tool layer itself
   could not write.
2. **Proposal:** stdio MCP server (official `@modelcontextprotocol/server-filesystem`
   class) rooted at `/opt/tkv-local`, registered in **project** `.kimi-code/mcp.json`,
   with `disabledTools` covering every write/move/delete tool the server exposes
   and matching `[[permission.rules]]` deny entries in `config.toml`.
3. **Value:** read-only guaranteed at the tool layer for the entire TKV surface;
   cleaner provenance for surveys; the mobbin precedent proves the config path.
4. **Integration:** project mcp.json (workspace trust prompt reviewed at enable
   time — defaults to *Don't trust*, which is correct); consumption by Carol and
   lane agents during surveys.
5. **Dependencies/security:** (a) requires `node`/`npx` on hxs-5 — **unverified,
   check first**; (b) **YOLO mode auto-approves MCP tool calls** (official docs)
   and our sessions run yolo — the `disabledTools` blocklist and deny rules are
   therefore the real enforcement, and their behavior under yolo must be
   empirically verified in the pilot before any reliance; (c) stdio servers
   execute local commands at session start — only enable in the trusted repo
   context; (d) no secrets in server env.
6. **Overlap:** none — it does not replace Bash for host work (out of its root).
7. **Disposition:** pilot, gated on the two verifications.
8. **Evidence:** mcp.html (config format, disabledTools, permission rules, YOLO
   note, trust prompt); AGENTS.md TKV survey requirement; Carol charter bounds.
9. **Phase:** pilot after O1–O5 land; verifications are the entry criteria.
10. **Second Brain effect:** the "retrieve before investigating" stage gains a
    bounded access path consistent with the steward's bounds. Disposition:
    **recommended for a future iteration (pilot), trigger = dependency
    verification.**

### O8 — Ollama MCP for hxs-1 (MCP)

- Need: structured model access for agents would be cleaner than curl-over-SSH.
  Blocking reality: the model is **loopback-only by ratified security posture**
  (SC-07; remote refusal proven in M5 evidence). Any MCP path requires a network
  route to the model — a new exposure surface that contradicts the posture and
  intersects the owner's open D1/OmniRoute remote-consumption decision
  (`governace/issue-tracking/issues.md`). Disposition: **defer**; trigger = the owner's
  D1/OmniRoute ruling, at which point MCP-over-that-approved-channel becomes the
  evaluation. Second Brain effect: none now; noted so the roadmap's "act" stage
  has a clean integration point when the owner opens remote access. Disposition:
  **deliberately deferred, owner decision is the trigger.**

### O9 — Catalog database / vector or graph index (MCP or service)

- Need: none measured — file-backed catalog passes CAT at 19× retrieval economy;
  the Second Brain document itself defers storage selection (G-06) and lists
  PostgreSQL/Qdrant/Neo4j as explicit non-actions until benchmarks prove a gap.
  Disposition: **defer**, trigger = a failed benchmark against the approved
  query corpus (exact/relationship retrieval falling short), evaluated with the
  ratified §6 tool rubric + tool decision record. Second Brain effect: this *is*
  a named roadmap item; the assessment confirms its gate is unmet. Disposition:
  **deliberately deferred, benchmark-triggered.**

## 6. Architecture and workflow implications

- Hooks introduce the first user-scope configuration dependency (`config.toml`)
  in a workflow that is otherwise repo-contained. Mitigation: hook *scripts* live
  in the repo under `scripts/hooks/` (versioned, reviewed); `config.toml` holds
  only registrations, documented in an onboarding note. Hook fail-open semantics
  mean none of these hooks may ever be cited as a sole control — they are
  interceptions layered on discipline and post-hoc gates.
- Skills are pure additions to the project scope; they change nothing about
  existing lanes and require no runtime changes.
- MCP (O7) is the only proposal that adds a runtime process. Project-scope
  registration keeps it repo-boundary-visible through the workspace trust
  prompt; the pilot's verification items are mandatory before reliance.
- Nothing in O1–O7 touches hxs-1, the model, the catalog schema, or ratified
  security posture. O8/O9 stay parked behind owner decisions.

## 7. Security and permission considerations

- Hook commands execute on hxs-5 on every matching tool event: scripts must be
  repo-reviewed, secret-free, output-nothing-sensitive, and bounded (5–30 s).
- Hooks are fail-open (docs): alerts and lightweight interception only; the
  permission/approval layer and post-hoc gates remain the barriers.
- MCP in YOLO mode auto-approves tool calls (docs): enforcement for O7 must be
  `disabledTools` + deny permission rules, empirically verified in pilot before
  reliance. No `mcp__*` wildcard allow rules.
- Project-level stdio MCP servers execute commands at session start: enable only
  within the trusted repo context; review the trust prompt deliberately.
- Marketplace plugins are third-party code: none adopted; any future candidate
  goes through the §6 tool rubric + hard gates + owner approval (new external
  shared state is serious-harm class under the approval discipline).
- No proposal stores, moves, or exposes secrets; O1 exists precisely to shrink
  the secret incident class.

## 8. Prioritized recommendations

1. **O4 + O5 (skills, adopt now):** zero-risk, immediate standardization value.
2. **O1 (hook, adopt-pilot):** the only proposal that prevents a demonstrated
   incident class; warn-mode first week, then block-mode.
3. **O2 (hook, adopt-pilot):** pairs with O1 to prove the hook pattern; removes
   an already-observed drift class.
4. **O3 (hook, pilot):** after O1/O2 settle.
5. **O7 (MCP, pilot):** only after node/npx verification and YOLO-enforcement
   verification pass.
6. **O6 (skill, pilot):** after the first R2-gated retrieval cycle.
7. **O8, O9 (deferred):** triggers named (owner D1 ruling; G-06 benchmark).

## 9. Explicit non-recommendations

- **No marketplace plugins** — no measured gap; any future candidate faces the
  tool rubric and hard gates first.
- **No git/GitHub, SSH/fleet, or utility MCP servers** — Bash/SSH/git plus
  built-ins (FetchURL, cron) are sufficient and already audited.
- **No hooks for state logging, dispatching, or judgment calls** — hooks are
  mechanical; governance decisions stay with the governor.
- **No blocking-style reliance on any hook** — fail-open design (docs); never a
  sole barrier.
- **No Ollama MCP, no database/vector/graph work, no always-on automation** —
  deferred with named triggers (O8, O9); the Second Brain document's non-actions
  stand.
- **No changes to the ten-skill communication library** — sufficient as-is.

## 10. Open questions and required owner decisions

- Q-A: approve O4+O5 skill authoring and O1/O2 hook pilot (scripts in
  `scripts/hooks/`, registrations in user `config.toml`)?
- Q-B: may the pilot verify `node`/`npx` presence and the YOLO-vs-deny-rule
  behavior on hxs-5 (read-only checks only)?
- Q-C: placement convention for hook registrations — documented in repo
  onboarding (`scripts/hooks/README.md`) while staying user-scope config?
- Q-D: confirm this report's follow-ups may proceed: Carol cataloging,
  wiki-manifest inclusion + render, state-log citation (all outside the
  read-only directive's scope).
- Q-E: D1/OmniRoute stays the gate for any model-access integration (O8) —
  confirm that remains parked.

## 11. Second Brain opportunity assessment (standing directive)

**Was a Second Brain opportunity identified in this work?** Yes — three.

1. **Deterministic boundaries (Principle 2 / §9 risk table):** O1/O2/O3 convert
   three judgment-maintained disciplines into deterministic interceptions.
   Disposition: O1/O2 recommended for this iteration upon owner approval; O3
   next iteration. Evidence: incident and drift classes documented above.
2. **Pattern library (§4):** O4 and O5 are proto-patterns (dispatch-pattern,
   verification-pattern). Disposition: implement as skills now; promote to
   formal pattern records after two validated uses, per the library's own
   promotion rule — no library build-out (deferred capability D5 in the
   guidance assessment).
3. **Bounded retrieval access (Stage 1 / Stage 7):** O6 and O7 strengthen the
   retrieve-before-investigating stage without new architecture. Disposition:
   both deliberately deferred one iteration with named triggers (packet-format
   proof; dependency + YOLO verifications).

Everything else in the roadmap — database selection (G-06), vector/graph
indexes, always-on automation, remote model access — stays deferred behind its
own named gate; this assessment changes none of them. The report's own
production followed the roadmap loop: produced from validated knowledge,
placed by convention, and queued for Carol's catalog receipt as the handoff
closure.

## 12. Provenance

Official product documentation fetched 2026-08-25: Kimi Code hooks page
(`https://www.kimi.com/code/docs/en/kimi-code-cli/customization/hooks.html`) and
MCP page (`https://www.kimi.com/code/docs/en/kimi-code-cli/customization/mcp.html`).
Project evidence: repo `.kimi-code/mcp.json`, `~/.kimi-code/` inventory,
`config.toml` section scan (names only), `scripts/README.md`, AGENTS.md
conventions, state-log rows 33–57, `governace/issue-tracking/issues.md`, Carol catalog records.
Read-only boundary confirmed: the only filesystem writes in this assignment are
this report and its `.html` rendering.
