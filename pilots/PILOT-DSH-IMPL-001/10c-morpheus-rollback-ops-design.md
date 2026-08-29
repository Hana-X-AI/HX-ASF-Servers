# PILOT-DSH-IMPL-001 — Products 3+4: Rollback/Operations Design + Tier-1 Install Smoke Suite (10c)

**Order:** 21 (Products 2+3+4), sub-products 09c
**Issuer:** Flash (governor), 2026-08-29
**Executor:** Morpheus (dsh lifecycle steward, KDD-0009)
**Model lane:** `omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B, provider DeepInfra, via OmniRoute hxs-8)
**Debt discharged:** Phase A signed with "rollback NOT exercised" (Gate 9); this is the design the arc owes. Execution remains a gated future window — this document is off-candidate design only (no hxs-15 contact, no mutation).

---

## Part A — Rollback drill design: Phase B state → pre-Phase-B checkpoint

### A.1 Objective, model, and checkpoint identities

**Objective.** Discharge the Gate 9 debt Phase A signed with ("rollback NOT exercised"): a complete, hash-anchored, ordered drill that returns the candidate from the current Phase B state to the signed pre-Phase-B (Phase A) checkpoint, with every step reversible and verified by parity against recorded Phase A receipts. This is the DESIGN; execution is a separately-gated window with its own governor approval and command window.

**Model.** Trinity's OmniRoute Secure-Core gate battery (PILOT-OMNIROUTE-LAYER0-001 record 12): *deep parity → restart → reboot → backup-and-restore → rehearsed rollback → hygiene close-out*, each with budgets and evidence pointers, everything versioned and reversible, sanitized command log, helpers deleted at task end. Adapted for dsh: "parity" = byte/hash equality against the recorded Phase A receipts (no live backend comparison needed — the receipts ARE the baseline); "rehearsed rollback" = this drill itself, run once forward and once as a restore to prove the inverse set.

**Checkpoint identities (pre-Phase-B = Phase A signed state, from records 03 §10 / 05 §1):**

| Artifact | Phase A value (drill target) | Phase B value (drill source) |
| --- | --- | --- |
| package.json / pnpm-lock anchors | `4adbdffa…4986d7` / `6f20c268…90013e` | UNCHANGED (no corpus mutation in Phase B) |
| launcher `/usr/local/bin/dsh` / `bin.js` | `0b68259f…efcdba` / `c0226687…366c62` | UNCHANGED |
| home layer `/var/lib/dsh/cordis.patch.yml` | `14f15b72…03f6016` (root:root 0644) | `d4ac2f19…40f83f` (Phase A rows byte-preserved, Phase B rows added) |
| effective dump — headless | `dedda886…d518d34` (Phase A §12) | `6f52cd6d…` then superseded `c88664a8…ded4e` (05 §13.1 correction) |
| web artifacts | ABSENT (Phase A posture: no dist, no web service) | dist 114 files, build record, preset, 2 systemd units, forwarder |
| services | none dsh-related | `dsh-web.service` (`4e659cd5…4b6c53`), `hx-dsh-lan-forward.service` (`c3257852…57ca`) |
| session-query sqlite | absent | materialized on first search |
| bwrap/apparmor (D1) | landed Phase A (0.9.0-1ubuntu0.1 + profile) | UNCHANGED — stays through the drill |
| secret refs `/var/lib/dsh/.env`, `/etc/dsh-omniroute.env` | `596ea242…80cc` (mechanism only) | UNCHANGED/UNTOUCHED by the drill |

**Drill doctrine:** Phase A surfaces (headless CLI, seam) must survive the rollback untouched — they are the proof that the inverse set is correctly scoped. Session persistence (`/var/lib/dsh/sessions`, `profiles/headless`) is OUT of the inverse set: rollback targets the *software/configuration state*, not durable session events (a durable-session loss would violate §7 behaviors-to-preserve). The drill's restore step proves the persistence root survives a full config rollback.

### A.2 Pre-drill (freeze, backup bundle, baseline capture)

Run BEFORE any inverse; nothing in this phase mutates state.

1. **Freeze:** announce the drill window in the state log; Gordon pauses any gate campaign; no other writer may touch `/var/lib/dsh` or the two units during the window (single-writer rule).
2. **Backup bundle (tar, root-owned, sha256-recorded, stored under a drill-only dir that is itself removed at hygiene):**
   - `/var/lib/dsh/cordis.patch.yml` (Phase B content `d4ac2f19…40f83f`)
   - `/var/lib/dsh/.agent-presets/` (hx-standard preset trees)
   - `/etc/systemd/system/{dsh-web,hx-dsh-lan-forward}.service`, `/usr/local/libexec/hx-dsh-lan-forward.mjs`
   - `/opt/dsh/apps/web/dist/` (114 files) + `/opt/dsh/.dsh-build/`
   - `/var/lib/dsh/session-query.sqlite*` if present
   - A `systemctl status` snapshot of both units + a `journalctl` cursor mark (not the log contents — journal stays).
3. **Baseline capture (read-only):** re-hash every Phase A anchor artifact (table A.1), capture the CURRENT headless dump hash and the web-face smoke result (`host.describe` ok:true envelope), and record both as the drill SOURCE baseline.
4. **Pre-state declaration:** the backup bundle + this baseline table IS the rollback-of-the-rollback artifact; forward-restore (§A.5) depends only on it.

### A.3 Ordered rollback steps with per-step inverse

Ordered exactly as the Phase B record §7 groups them, so each inverse can be verified against the backup bundle hash before it is removed.

| # | Step (command, sanitized) | Inverse (restore from §A.2 bundle) | Hash anchor |
| ---: | --- | --- | --- |
| R1 | `sudo systemctl disable --now hx-dsh-lan-forward.service dsh-web.service` | `sudo systemctl enable --now` both (bundle restores unit files first if missing) | unit hashes `c3257852…57ca` / `4e659cd5…4b6c53` |
| R2 | `sudo rm /etc/systemd/system/{hx-dsh-lan-forward,dsh-web}.service /usr/local/libexec/hx-dsh-lan-forward.mjs && sudo systemctl daemon-reload` | copy bundle members back (root 0644 / 0755), `daemon-reload` | forwarder `bb618566…2cd0` |
| R3 | restore Phase A home layer: `sudo install -m 0644 -o root -g root <bundle>/cordis.patch.yml /var/lib/dsh/cordis.patch.yml` (overwrites Phase B content) | install bundle's Phase B layer copy back over it | target `14f15b72…03f6016`; source `d4ac2f19…40f83f` |
| R4 | `sudo rm -rf /var/lib/dsh/.agent-presets` | restore bundle's preset trees (root 0644) | preset `56c71037…9eb0` / `c5b863c8…4677` |
| R5 | `sudo -u dsh rm -rf /opt/dsh/apps/web/dist /opt/dsh/.dsh-build` | restore bundle dist + build record | dist 114 files; build-record file hash from Phase B §9 |
| R6 | `sudo rm -f /var/lib/dsh/session-query.sqlite*` | none required (re-materializes on first search) — record absence | n/a (auto-init artifact) |
| R7 | verification step, no mutation: re-hash anchors + headless smoke (§A.4 P1) | — | Phase A hashes |

Ordering rationale: services before their artifacts (R1 before R2/R5) so no unit ever boots from a half-removed tree; config layer before preset deletion (R3 before R4) so the running config never references a removed preset mid-drill. Every step is independently re-runnable; a drill abort at any step leaves the candidate at a known, hash-verifiable intermediate state.

### A.4 Post-rollback parity battery (trinity-shaped)

Modeled on the trinity battery (parity + restart + reboot + restore + rollback + hygiene), adapted to dsh where the parity baseline is a *recorded receipt*, not a live peer:

| Gate | Probe | Oracle (recorded Phase A receipt) | Budget |
| --- | --- | --- | --- |
| G-PARITY | re-hash launcher, bin.js, home layer, headless dump; `ss` listener sweep (no 3080, no forwarder) | `0b68259f…` / `c0226687…` / `14f15b72…` / `dedda886…`; zero Phase B listeners | ≤ 5 min |
| G-PERSIST | headless one-shot session write+read through the persistence root; verify sessions dir intact through R1–R7 | Phase A G4 durability posture (restart durability + prefix parse of record) | ≤ 5 min |
| G-RESTART | `systemctl daemon-reload`; verify zero failed units; headless smoke `dsh -p "<fixed probe>"` exit 0 | Phase A smoke exit/0-stderr posture | ≤ 5 min |
| G-REBOOT | one cold host reboot in the governor-announced window (owner may abort — honor it); after boot: 0 failed units, headless smoke re-proven, persistence intact | trinity reboot protocol (re-prove residency after boot) | window-bound |
| G-RESTORE | forward-restore the Phase B state from the §A.2 bundle (the inverse column of §A.3, in reverse order R7→R1); re-hash every artifact against Phase B anchors | `d4ac2f19…` layer, unit hashes, dist count 114, headless dump `c88664a8…` (post-correction), web-face smoke `ok:true` | ≤ 20 min |
| G-ROLLBACK-PROOF | re-run R1–R7 a second time (rollback is REHEARSED, not just run once), ending at the Phase A checkpoint again; then leave the candidate in whichever state the governor directs for the next phase | both directions hash-identical to their respective checkpoints | ≤ 20 min |
| G-HYGIENE | delete drill helper files + backup bundle only AFTER both directions verify; append the sanitized command log; state-log row closes the window | no stray files, no stray units, log complete | ≤ 5 min |

Failure handling: any gate FAIL stops the drill at the current intermediate state (which is always hash-known by construction), files a defect to Morpheus, and the window closes with the partial evidence — no silent retry.

### A.5 Forward-restore path & drill acceptance

The forward-restore path IS the inverse column of §A.3 executed in reverse (R7→R1), using only the §A.2 bundle — no network, no rebuild. This makes the drill a true two-way proof: if the restore step fails, the rollback is not reversible in practice and the drill FAILS regardless of how clean the inverse steps looked. Acceptance: the governor cites the drill record (this doc + the executed-command log + hash evidence) in the state log; handoff stays OPEN until cited. The drill's acceptance package mirrors trinity's: parity comparisons, restart/reboot timelines vs budgets, restore proof, rollback proof, hygiene close-out.

## Part B — Upgrade-path runbook for the next dsh intake

Scope: the next time HX admits a new pinned dsh snapshot (the "Evolve" lane entry). Design properties, by construction: **reversible** (every step has a named inverse), **hash-anchored** (every artifact identity recorded before and after), **inverse per step** (column 3 of the table). Global rollback posture: the S0 snapshot is the single restore source for every step; the pre-intake tree is retained until the intake is ACCEPTED, so nothing is destroyed before acceptance. This runbook is off-candidate design (no hxs-15 contact); execution is a separately-gated window.

### B.1 Step table

| # | Action (sanitized) | Inverse | Hash anchor |
| ---: | --- | --- | --- |
| S0 | **Pre-intake snapshot.** Freeze window in state log; backup bundle of the CURRENT candidate (Part A §A.2 inventory + integrity re-hash of the landed anchors table §A.1); record as the intake rollback source | none (this step creates the rollback source) | bundle sha256 manifest; re-verified anchors (`14f15b72…` layer / `d4ac2f19…` post-Phase-B, launcher `0b68259f…`, bin.js `c0226687…`, dumps `dedda886…`/`c88664a8…` — whichever is current) |
| S1 | **Admit new pinned snapshot.** Hash-verified archive ONLY (sha256 of archive == published/pinned value, verified offline against the pin record); stage to an intake dir beside the corpus — never `latest`, never an unpinned head, never a code edit over the snapshot (profile §3 pin doctrine; out-of-tree extension over core edits, §6 doctrine) | delete the intake dir | archive sha256; new `package.json` + `pnpm-lock.yaml` sha256 recorded |
| S2 | **Re-resolve / reinstall against the new snapshot** in a staging root (never in-place over the landed install). Then **diff the R1 ledger from 10b**: RBI rows must clear (re-resolution picks up range-compatible fixes — re-run audit and confirm the count drops); NUA rows re-scored (still outside importer ranges unless upstream moved); any NEW advisory gets a row before acceptance | delete staging root | new lockfile sha256; audit re-run output attached; 10b §3 row-by-row diff |
| S3 | **Rebuild built artifacts** (bin.js, web dist if carried forward) in staging; record new hashes. Built artifacts are derived — they are never edited by hand, always re-derived from the admitted snapshot | discard staging build outputs | new bin.js sha256; new dist file list + hash manifest |
| S4 | **Re-derive HX artifacts** (config-layer, NEVER code edits): hx-standard preset (223-byte asserted removal → re-derivation, R7 risk class — re-derive at EVERY intake, 10 doc §11 risk note); omniroute route row in landed compositions; the ACP HX composition if carried (10 doc §A risk: RISK_DERIVED_ARTIFACT_DRIFT). Each re-derivation diffed against its predecessor | restore predecessor artifact from S0 bundle | new preset sha256; composition-layer hashes |
| S5 | **Effective-config receipts per profile** via the native resolution path (`--dump-config` or source equivalent), redact secret VALUES while keeping reference identities and shape; hash each receipt (profile §5 mandate) | n/a (receipts are append-only evidence) | per-profile receipt sha256, recorded in state log |
| S6 | **Smoke parity vs Phase A/B baselines** — run the Part C Tier-1 suite against the staged install + the §A.4-shaped parity battery against recorded receipts (the receipts ARE the baseline) | n/a (probe-only; any FAIL aborts to S7-inverse) | probe receipts; parity comparisons attached |
| S7 | **Handoff to Gordon** with full identity material (S1–S6 receipts); governor cites acceptance in state log. Only AFTER acceptance: promote staged install, retire the pre-intake tree per the normal hygiene close-out (helpers + staging deleted at task end, trinity battery model) | restore S0 bundle in reverse step order (R-shape: services/artifacts last removed, config layer first restored) | acceptance citation; final candidate anchors table |

### B.2 Failure handling & doctrine

- **Any S-step FAIL** → stop, stay on the last good anchor state, file a defect, and either repair-forward (bounded) or execute the inverse column back to S0. No silent retry, no partial acceptance.
- **R1 debt coupling:** an intake that clears RBI rows but introduces new advisories is not a regression of this runbook — the new rows simply enter the next 10b-shaped scoring pass. The ledger is cumulative and scored, not a gate on admission itself (admission is the pin decision; the ledger scores what the pin carries).
- **Reversible-by-construction proof:** the only destructive action in the whole runbook is S7's post-acceptance retirement of the pre-intake tree, and it is gated on governor citation — so at every point before acceptance, full inverse = S0 bundle restore, with zero dependence on network or rebuild.

## Part C — Tier-1 during-install smoke suite (Product 4)

**Label: INSTALL VERIFICATION, NOT QUALIFICATION.** Bounded entry-path probes (minutes, deterministic-first) run by the installer during Phase C installs. Gordon's Gates 8–10 own qualification; this suite makes no gate claims and restates none.

### C.1 Family 1 — interop (ACP)

| Probe | Oracle | Expected receipt |
| --- | --- | --- |
| Boot the HX ACP composition from the 10 doc recipe (SEAM-INT-02 shape: `examples/acp-agent`-derived composition, `acp` row with `provider: omniroute` + catalogued model id, `persistenceRoot` set; omniroute row defaulted) as a separate process; send the ACP JSON-RPC `initialize` handshake over stdio (SEAM-INT-01: `AgentSideConnection` on stdin/stdout) | JSON-RPC `initialize` response frame arrives on stdout within the probe budget; stdout carries protocol frames only (no logger/HMR noise — README contract) | session/connection id + provider/model echo from the initialize response; exit 0 on teardown |
| Absence check: no listener introduced by the probe process (ACP is one-shot stdio per client connection, 10 doc: "no listener is introduced") | `ss` sweep during/after probe shows no new dsh-owned port | listener count 0 for the probe process |

### C.2 Family 2 — sandbox

| Probe | Oracle | Expected receipt |
| --- | --- | --- |
| Confined trivial run through the bash-sandbox path in read-only/deny mode (SEAM-SBX-05: load INSTEAD of `bash-local`, together with sandbox-local + sandbox-policy; probe command = `true`/`echo`, no writes) | exit 0; NO structured `SANDBOX_UNAVAILABLE` error (fail-closed contract: that error means confinement unavailable, which is a FAIL here, never silent unconfined execution) | `selectedRunner = bwrap` (rung 1 active per Phase A D1: bwrap 0.9.0-1ubuntu0.1 + apparmor profile); probe output empty/echo-only |
| Runner-selection reading: `PLATFORM_CHAINS` linux chain is `['bwrap', 'landlock']` and the bwrap functional probe (`spawnSync('bwrap', …, '--', 'true')`) passes (SEAM-SBX-01) | chain order and probe result as recorded at the pinned source identity | selected-runner line = bwrap; landlock unprobed-by-design (rung 2 not activated) |

### C.3 Family 3 — remote (e2b, DEFERRED_BY_POLICY)

No live-endpoint probe exists or may exist in this suite — the family's install verification IS the absence proof (10 doc: Gate 9 is a local posture proof; activation requires owner word).

| Probe | Oracle | Expected receipt |
| --- | --- | --- |
| Absence grep: zero `e2b` rows in every shipped and landed composition (corpus examples + landed `/var/lib/dsh` compositions) | match count == 0 | `e2b rows: 0` — disposition DEFERRED_BY_POLICY holds post-install |
| Fail-closed reading check: `packages/e2b/e2b/src/index.ts:140-141` still throws on absent credential reference (field name `apiKey` / env reference `E2B_API_KEY`; no value exists anywhere in HX records — reference identity only, profile §3) | source identity matches the pinned seam record | seam source hash matches pinned identity; no key material present in any dump |

### C.4 Family 4 — experimental (ABSENT by policy)

Same shape as C.3: no activation probe. EXPERIMENTAL_LAB_ONLY means the install verification proves continued absence (activation requires owner word + separate approval, profile §3).

| Probe | Oracle | Expected receipt |
| --- | --- | --- |
| Absence grep: zero `agent-team` rows in every shipped and landed composition | match count == 0 | `agent-team rows: 0` — disposition ABSENT holds post-install |
| Prerequisite-surface reading: the package's activation precondition (durable Session storage required, `agent-team/README.md:22`) is policy-blocked, not host-blocked — record that the blocker remains policy | landed stack satisfies runtime prerequisites; no row staged | disposition line: ABSENT, blocker = policy (not host state) |

### C.5 Suite-level rules

- **Time budget:** minutes per probe, bounded per family (target ≤ 5 min/family; the whole suite ≤ 25 min of an install window). Deterministic-first: every probe's oracle is an exit code, a count, a hash, or a selected-runner string — never "model output looked right".
- **Failure handling:** fail-LOUD, not fail-silent. Any probe FAIL aborts the install verification for that family, emits the structured failure receipt, and is recorded in the state log — it does NOT block or certify Gordon's gates, which run separately.
- **Evidence routing:** receipts go to the state log as install-verification evidence. They must NOT be cited as gate claims, must not restate Gordon's verdicts, and must not be treated as proof of session/persistence/tool correctness beyond the probe's own scope (profile §3: model response is never proof of mechanism correctness).
- **Boundary:** probes run only inside the install window on the candidate under installation; no probe touches production data, fleet credentials, or another host. Credential reference identities may appear in receipts; values never (profile §3).

## Knowledge-review receipt

Per KDD-0009 working order (Phase A/B/C-prep precedent):

- **Goal / work-order ids:** GOAL-DSH-IMPL-001; work order 21 (Products 2+3+4, issuer Flash 2026-08-29), sub-products 09c (rollback/ops design + Tier-1 smoke suite).
- **Target environment:** OFF-CANDIDATE design only. Zero hxs-15 contact, zero candidate mutation this session; every command/artifact identity cited is quoted from signed Phase A/B records (03/05) and the 10 doc — nothing was executed on the candidate.
- **Knowledge roots reviewed:**
  1. HX decisions/conventions root `/home/hxsa/opt/local-tkv/agent-zero-docs/projects/harness` — consulted via the Phase A Gate 9 debt record ("rollback NOT exercised", 03/state-log row), the trinity battery model (PILOT-OMNIROUTE-LAYER0-001 record 12), and profile §3/§5 mandates quoted in-text.
  2. Approved source snapshot `/opt/tkv-local/deepseek-harness-master` — anchors re-verified live this session: `package.json` `4adbdffa…4986d7`, `pnpm-lock.yaml` `6f20c268…90013e` (MATCH Phase A); source seams cited in Part C taken from the 10 doc's seam tables (which are the pinned-source citations of record).
- **Installed runtime identity:** unchanged/not touched (record-only: Node v24.20.0, pnpm 11.7.0, dsh uid 999 per Phase A/B records).
- **Effective profiles/bundles/patches:** unchanged; none emitted.
- **Persistence backend:** unchanged.
- **Upstream sources consulted:** none required — this is a design document over already-signed local evidence; no upstream fetch.
- **Allowed changes:** writes to `pilots/PILOT-DSH-IMPL-001/10c-morpheus-rollback-ops-design.md` only (Product 4 placed as Part C of this doc, as the work order permits).
- **Protected constraints honored:** no hxs-15 contact; no candidate mutation; no credential-shaped literals (secret seams quoted by reference identity only — field names and env-var names, never values); append-only governance records.
- **Required tests:** `python3 scripts/validate.py` from repo root, 4/4 PASS.
- **Known drift/conflicts:** none — corpus anchors match Phase A; drill targets match the signed checkpoint tables.
- **Rollback state:** document-only change; pre-state recoverable from git history.
- **proceed_status:** MAY_PROCEED (all fields available and consistent).

## Sanitized command log

| Command | Host | Purpose | Status |
| --- | --- | --- | --- |
| `sha256sum package.json pnpm-lock.yaml` (corpus root) | session host (corpus read) | Anchor re-verification vs Phase A record | OK — MATCH |
| `grep`/`sed` reads of pilot records 03/05/10 (checkpoint identities, seams, family dispositions) | session host (read-only) | Source material for Parts A/B/C | OK (read-only) |
| Write/edit of this document (skeleton-first, then targeted section fills) | session host | Products 3+4 | OK |
| `python3 scripts/validate.py` (repo root) | session host | Work-order gate | see close-out |

No hxs-15 contact, no candidate mutation, no install, no credential values. Drill and runbook EXECUTION remain separately-gated future windows — this session produced design only.
