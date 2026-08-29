# PILOT-DSH-IMPL-001 — Product 2: R1 Advisory-Debt Intake Analysis (10b)

**Order:** 21 (Products 2+3+4), sub-product 09b
**Issuer:** Flash (governor), 2026-08-29
**Executor:** Morpheus (dsh lifecycle steward, KDD-0009)
**Model lane:** `omniroute/qwen3.8-2.4t-a95b` (Qwen 3.8 2.4T A95B, provider DeepInfra, via OmniRoute hxs-8)
**Corpus (read-only):** `/opt/tkv-local/deepseek-harness-master` — anchors re-verified this session: `package.json` sha256 `4adbdffa…4986d7`, `pnpm-lock.yaml` sha256 `6f20c268…90013e` (MATCH Phase A record; snapshot `0.1.1-rc.2`)
**Risk register anchor:** R1 (upstream advisory debt of the pinned snapshot — Phase A record §4/§12, state-log row 7: 38 advisories, 15H/20M/3L)

---

## 1. Purpose & method

**Purpose.** Discharge the Phase A R1 promise ("re-examine at the next upstream intake — Evolve lane"): map every one of the 38 pinned-snapshot advisories to its fixed upstream version (if one exists), check whether that fix is compatible with the pinned lockfile's constraints **offline**, and classify each instance so the next dsh intake starts from a scored ledger instead of a raw audit count.

**Method (all read-only; no hxs-15 contact, no lockfile rewrite, no install):**

1. **Corpus anchors re-verified first** (this session): `package.json` `4adbdffa…4986d7`, `pnpm-lock.yaml` `6f20c268…90013e` — MATCH the Phase A record, so the 38-advisory snapshot still corresponds to this exact tree (`node_modules/` absent — the corpus carries no installed state; all analysis is metadata-level).
2. **Advisory → fix mapping:** GitHub Advisory Database API (`/advisories?ecosystem=npm&affects=<pkg@pinned-version>`), queried read-only from the session host. `first_patched_version` per affected package taken as "the fixed upstream version".
3. **Importer chain:** parsed offline from the pinned `pnpm-lock.yaml` `snapshots:` section (who depends on each affected package, with which resolved version).
4. **Constraint compatibility:** importer version ranges read from npm-registry package metadata (read-only metadata fetch); a fix is *range-compatible* when the first patched version satisfies the importer's declared range, so a plain re-resolution at the next intake can pick it up without any range edit.
5. **Withdrawn advisories:** flagged and excluded from the scored ledger (see §2 note on GHSA-gv7w-rqvm-qjhr).

**Classification definitions (work-order classes):**

- **resolved-by-next-intake** — a first-patched version exists AND is range-compatible with the importer's constraint; a routine re-resolution at the next intake clears it with no upstream code action required from HX.
- **needs-upstream-action** — a fix exists but cannot be reached within the pinned constraint set (fix lies outside the importer's range, or only exists at a major bump the importer has not made); clearance requires an upstream move first.
- **accepted-risk-with-rationale** — risk knowingly carried into the next intake window, with the Phase A exposure rationale (and any interim posture) recorded. No instance stands alone in this class (§4) — it is the interim posture *attached* to the needs-upstream-action rows, exactly as Phase A accepted it.

## 2. Ledger reconciliation (38 instances ↔ Phase A count)

Phase A captured `pnpm audit` → **38 advisories (15 high / 20 moderate / 3 low)**, exit 1, with a per-package severity table (03 §4, state-log row 7). One note before the table: **GHSA-gv7w-rqvm-qjhr** (esbuild, high) is **WITHDRAWN** in the GitHub Advisory Database; withdrawn advisories are excluded from the scored ledger. This is what keeps the bookkeeping exact: the two GHSAs the API still returns for esbuild@0.21.5/0.25.12 minus the withdrawn one leaves exactly the single moderate instance Phase A counted, and every other package matches its Phase A multiplicity.

| Package @ pinned version | Advisories touching it | Phase A severity rows | Matches Phase A |
| --- | --- | --- | --- |
| brace-expansion @ 2.1.2, 5.0.6 | 3jxr, mh99, rgw5 (all high; 3jxr affects 5.0.6 only — 2.1.2 already at its patched version, hence 5 vulnerable ranges, not 6) | ×5 high ranges | ✔ |
| fast-uri @ 3.1.3 | 7p8r, v2hh (high) | ×2 high | ✔ |
| ip-address @ 10.2.0 | mwp4 (high); 22jq, 4xrf (moderate) | ×1 high, ×2 moderate | ✔ |
| js-yaml @ 4.2.0 | 5p4m, 52cp (high) | ×2 high | ✔ |
| nanoid @ 3.3.12 | 28wg, 2v37 (high) | ×2 high | ✔ |
| postcss @ 8.5.15 | r28c (high), fxqj (moderate) | ×1 high, ×1 moderate | ✔ |
| undici @ 7.28.0 | 4cwx (high); 8xcm, jr45, m8rv, v3r7 (moderate) | ×1 high, ×4 moderate | ✔ |
| vite @ 5.4.21 | fx2h (high); 4w7w, v6wh (moderate). vite@6.4.3 / @8.0.16 also pinned and **clean** | ×1 high, ×2 moderate | ✔ |
| @hono/node-server @ 1.19.14 | frvp (moderate) | ×1 moderate | ✔ |
| dompurify @ 3.4.11 | 55q2 (moderate), c2j3 (low) | ×1 moderate, ×1 low | ✔ |
| esbuild @ 0.21.5 (0.25.12/0.28.1 clean) | 67mh (moderate); gv7w (high, **withdrawn** — excluded) | ×1 moderate | ✔ |
| hono @ 4.12.29 | 54fx, 8j4g, f23p (moderate); 79qm (low) | ×3 moderate, ×1 low | ✔ |
| mermaid @ 11.16.0 | rhh3, 6x64, 3rrr, 2v8p (moderate); c4c3 (low) | ×4 moderate, ×1 low | ✔ |
| protobufjs @ 7.6.4 | j3f2 (moderate) | ×1 moderate | ✔ |

**Total: 36 unique GHSAs (+1 withdrawn, excluded) → 38 scored instances = 15 high / 20 moderate / 3 low.** Reconciled exactly with the Phase A audit.

## 3. Fixed-version map (per advisory)

Pinned version and importer chain taken from the pinned `pnpm-lock.yaml` (`snapshots:`); importer ranges from npm-registry metadata of the pinned importer versions. Class: **RBI** = resolved-by-next-intake; **NUA** = needs-upstream-action (interim accepted-risk rationale attached, §4).

| # | GHSA | Sev | Package @ pinned | First patched | Importer chain (range) | Fix in range? | Class |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | GHSA-3jxr-9vmj-r5cp | high | brace-expansion @ 5.0.6 (2.1.2 already fixed AT this version) | 2.1.2 / 5.0.7 | minimatch@10.2.5 (`^5.0.5`) | ✔ 5.0.7 | RBI |
| 2 | GHSA-mh99-v99m-4gvg | high | brace-expansion @ 2.1.2 + 5.0.6 | 2.1.3 / 5.0.8 | minimatch@9.0.9 (`^2.0.2`), minimatch@10.2.5 (`^5.0.5`) | ✔ both | RBI |
| 3 | GHSA-rgw5-rvv9-x895 | high | brace-expansion @ 2.1.2 + 5.0.6 | 2.1.4 / 5.0.9 | same as above | ✔ both | RBI |
| 4 | GHSA-v2hh-gcrm-f6hx | high | fast-uri @ 3.1.3 | 3.1.4 | ajv@8.20.0 (`^3.0.1`) ← MCP SDK / eslint / ajv-formats | ✔ | RBI |
| 5 | GHSA-7p8r-x3mc-p8w7 | high | fast-uri @ 3.1.3 | 3.1.5 | same | ✔ | RBI |
| 6 | GHSA-mwp4-54f8-5fhr | high | ip-address @ 10.2.0 | 10.3.1 | express-rate-limit@8.5.2 (`^10.2.0`) ← MCP SDK (`^8.2.1`) | ✔ | RBI |
| 7 | GHSA-22jq-vg5j-6vgg | medium | ip-address @ 10.2.0 | 10.2.1 | same | ✔ | RBI |
| 8 | GHSA-4xrf-jv44-h6hh | medium | ip-address @ 10.2.0 | 10.2.2 | same | ✔ | RBI |
| 9 | GHSA-5p4m-2wfm-xmqj | high | js-yaml @ 4.2.0 | 3.15.1 / 4.3.1 | DIRECT: root + apps/cli `^4.2.0` | ✔ 4.3.1 (⚠ summary notes a CVE fix "not backported" while the advisory lists 4.3.1 — verify at intake, §5) | RBI |
| 10 | GHSA-52cp-r559-cp3m | high | js-yaml @ 4.2.0 | 3.15.0 / 4.3.0 | same | ✔ | RBI |
| 11 | GHSA-28wg-ghj8-5hjv | high | nanoid @ 3.3.12 | 3.3.16 | postcss@8.5.15 (`^3.3.12`) | ✔ | RBI |
| 12 | GHSA-2v37-7h3g-55p8 | high | nanoid @ 3.3.12 | 3.3.18 | same | ✔ | RBI |
| 13 | GHSA-r28c-9q8g-f849 | high | postcss @ 8.5.15 | 8.5.18 | vite@5.4.21 (`^8.4.43`), vitepress (`^8`), @vue/compiler-sfc (`^8.5.15`) | ✔ all | RBI |
| 14 | GHSA-fxqj-rqcc-2cmp | medium | postcss @ 8.5.15 | 8.5.23 | same | ✔ all | RBI |
| 15 | GHSA-4cwx-7wf7-3272 | high | undici @ 7.28.0 | 7.29.0 | e2b@2.29.1 (`^7.25.0`), jsdom@29.1.1 (`^7.25.0`) ← vitest | ✔ | RBI |
| 16 | GHSA-8xcm-r25x-g524 | medium | undici @ 7.28.0 | 7.29.0 | same | ✔ | RBI |
| 17 | GHSA-jr45-8vmc-qm54 | medium | undici @ 7.28.0 | 7.29.0 | same | ✔ | RBI |
| 18 | GHSA-m8rv-5g2x-5cg5 | medium | undici @ 7.28.0 | 7.29.0 | same | ✔ | RBI |
| 19 | GHSA-v3r7-h72x-cjcm | medium | undici @ 7.28.0 | 7.29.0 | same | ✔ | RBI |
| 20 | GHSA-fx2h-pf6j-xcff | high | vite @ 5.4.21 (6.4.3 / 8.0.16 copies CLEAN) | 6.4.3 / 8.0.16 | vitepress@1.6.4 docs chain — 5.x line has no fix; fix requires vite ≥ 6.4.3 | ✘ | NUA |
| 21 | GHSA-v6wh-96g9-6wx3 | medium | vite @ 5.4.21 (via launch-editor; Windows UNC vector) | 6.4.3 | same | ✘ | NUA |
| 22 | GHSA-4w7w-66w2-5vf9 | medium | vite @ 5.4.21 | 6.4.2 | same | ✘ | NUA |
| 23 | GHSA-55q2-fjhq-7xh7 | medium | dompurify @ 3.4.11 | 3.4.13 | mermaid@11.16.0 (`^3.3.3`) | ✔ | RBI |
| 24 | GHSA-c2j3-45gr-mqc4 | low | dompurify @ 3.4.11 | 3.4.12 | same | ✔ | RBI |
| 25 | GHSA-67mh-4wv8-2f99 | medium | esbuild @ 0.21.5 (0.25.12/0.28.1 CLEAN) | 0.25.0 | vite@5.4.21 (`^0.21.3`) — fix lies outside range | ✘ | NUA |
| — | GHSA-gv7w-rqvm-qjhr | (high) | esbuild | — | **WITHDRAWN in GHSA DB — excluded from scored ledger (§2)** | — | — |
| 26 | GHSA-54fx-42gc-7vw4 | medium | hono @ 4.12.29 | 4.12.34 | MCP SDK (`^4.11.4`), @hono/node-server (`^4`) | ✔ | RBI |
| 27 | GHSA-8j4g-w8fx-2239 | medium | hono @ 4.12.29 | 4.12.34 | same | ✔ | RBI |
| 28 | GHSA-f23p-vx2j-j53r | medium | hono @ 4.12.29 | 4.12.34 | same | ✔ | RBI |
| 29 | GHSA-79qm-7rj5-m7r9 | low | hono @ 4.12.29 | 4.12.34 | same | ✔ | RBI |
| 30 | GHSA-frvp-7c67-39w9 | medium | @hono/node-server @ 1.19.14 | 1.19.15 | MCP SDK (`^1.19.9`); Windows-only traversal vector | ✔ | RBI |
| 31 | GHSA-rhh3-jpg6-66xh | medium | mermaid @ 11.16.0 | 11.16.1 | vitepress-plugin-mermaid@2.0.17 (`10 \|\| 11`) ← website direct | ✔ | RBI |
| 32 | GHSA-3rrr-jr9j-h3q3 | medium | mermaid @ 11.16.0 | 11.16.1 | same | ✔ | RBI |
| 33 | GHSA-6x64-9x62-f2gx | medium | mermaid @ 11.16.0 | 11.16.1 | same | ✔ | RBI |
| 34 | GHSA-2v8p-3f2j-5mp7 | medium | mermaid @ 11.16.0 | 11.16.1 | same | ✔ | RBI |
| 35 | GHSA-c4c3-pg64-4m4v | low | mermaid @ 11.16.0 | 11.16.1 | same | ✔ | RBI |
| 36 | GHSA-j3f2-48v5-ccww | medium | protobufjs @ 7.6.4 | 7.6.5 | @google/genai@1.52.0 (`^7.5.4`) ← pi-ai@0.82.1 optional Google backend | ✔ | RBI |

**36 unique GHSAs = 38 scored instances** (rows 2 and 3 each cover both pinned brace-expansion versions). Clean pinned versions noted in-line: vite@6.4.3, vite@8.0.16, esbuild@0.25.12/0.28.1.

## 4. Classification rollup & exposure rationale

**Rollup (38 scored instances):** [OPEN CORRECTION 2026-08-29, labeled,
append-only — review batch 2, F26: the RBI/NUA instance counts were corrected
33→34 and 5→4 to match the detailed classification ledger; GHSA column already
consistent.]

| Class | Instances | GHSAs |
| --- | ---: | --- |
| resolved-by-next-intake (RBI) | 34 | 27 |
| needs-upstream-action (NUA, interim accepted-risk attached) | 4 | 4 (all in the vite@5.4.21 / esbuild@0.21.5 lineage) |
| accepted-risk-with-rationale (standalone) | 0 | — |
| excluded (withdrawn) | 0 scored | 1 (gv7w) |

**RBI rationale (33 instances).** Every first-patched version satisfies the range declared by the importer pinned in `pnpm-lock.yaml` — most inside the same major (e.g. undici 7.28.0→7.29.0, hono 4.12.29→4.12.34, mermaid 11.16.0→11.16.1, dompurify 3.4.11→3.4.13, postcss 8.5.15→8.5.23, nanoid 3.3.12→3.3.18, fast-uri 3.1.3→3.1.5, ip-address 10.2.0→10.3.1, protobufjs 7.6.4→7.6.5, @hono/node-server 1.19.14→1.19.15, js-yaml 4.2.0→4.3.1). A routine re-resolution at the next intake (the corpus's own `pnpm install` path, re-run under its fresh lockfile) clears them without any HX range edit. These include all 14 high-severity instances outside the vite-5/esbuild-0.21 lineage.

**NUA rationale (5 instances — the entire docs/dev-tool lineage).** The vite@5.4.21 rows (1 high: `server.fs.deny` bypass on Windows alternate paths; 2 moderate: launch-editor UNC NTLMv2 disclosure + one other) and the esbuild@0.21.5 row (moderate: dev-server cross-origin request read) have fixes only at vite ≥ 6.4.2 / esbuild ≥ 0.25.0 — outside the ranges that pin them (`vitepress@1.6.4`'s vite-5 line; vite@5.4.21's own `^0.21.3`). Clearance therefore requires an upstream move: vitepress's next release that accepts vite ≥ 6.4.3. Until then the **Phase A accepted-risk stance carries**, restated with this intake-time evidence:

- These instances sit in the **docs/build-time chain** (vitepress → plugin-mermaid → mermaid → dompurify; esbuild via vite's dev pipeline). The dsh runtime (headless CLI, web service, sdk) never serves the website tree; there is no runtime attack surface on hxs-15.
- The two Windows-specific vectors (`server.fs.deny` alternate paths, launch-editor UNC) have **no Linux applicability** on the hxs-15 host — recorded as posture, not assumed.
- Phase A's exposure notes (§4 of record 03) already dispositioned every package class: build-time/docs-chain only; hono/@hono/node-server enter via MCP SDK which is not mounted (zero servers, Phase B); js-yaml parses root/dsh-authored configs, not attacker input; undici/brace-expansion/nanoid/fast-uri/ip-address/protobufjs are transitive. Nothing in this intake analysis weakens or contradicts those dispositions — it converts them from audit-line judgment into a scored, version-mapped ledger.

**Why no standalone accepted-risk rows:** the work-order's third class exists for advisories with no fix path at all. Here every advisory has a first-patched version; the five NUA rows simply cannot be reached without an upstream move first — the accepted-risk stance is their *interim posture*, attached and reasoned, not a standalone disposition.

## 5. Next-intake action list

1. **Re-run `pnpm audit` against the new snapshot** and diff against this ledger: every RBI row must be gone or mapped to a new advisory; every NUA row must be re-evaluated against the new pinned versions.
2. **js-yaml verify-before-close (row 9):** the advisory summary for GHSA-5p4m-2wfm-xmqj states the CVE fix was "not backported" while the advisory metadata lists 4.3.1 as first-patched. If re-resolution lands on 4.3.x, confirm the actual fix content (changelog/diff) before striking the row.
3. **NUA watch (rows 20–22, 25):** re-check whether vitepress has moved off the vite-5 line. If the intake snapshot still pins vite@5.4.21, the five rows carry forward with this same rationale; if upstream has moved, they convert to RBI automatically.
4. **Withdrawn-advisory hygiene:** GHSA-gv7w-rqvm-qjhr stays excluded unless re-instated; a future audit delta mentioning it must cite its withdrawn status.
5. **Derived-composition rule (unchanged):** the intake re-derives HX artifacts (hx-standard preset, ACP composition if landed) per RISK_DERIVED_ARTIFACT_DRIFT — the advisory map here does not change that rule, it only scores the dependency half.

## 6. Knowledge-review receipt

Per KDD-0009 working order (Phase A/B/C-prep precedent):

- **Goal / work-order ids:** GOAL-DSH-IMPL-001; work order 21 (Products 2+3+4, issuer Flash 2026-08-29), sub-product 09b.
- **Target environment:** OFF-CANDIDATE analysis only. Zero hxs-15 contact, zero candidate mutation this session; corpus read-only from this host.
- **Knowledge roots reviewed:**
  1. HX decisions/conventions root `/home/hxsa/opt/local-tkv/agent-zero-docs/projects/harness` — consulted via the Phase A record's R1 disposition (03 §4/§12) which already carried the exposure rationale; no new plan text needed.
  2. Approved source snapshot `/opt/tkv-local/deepseek-harness-master` — anchors re-verified live this session: `package.json` `4adbdffa…4986d7`, `pnpm-lock.yaml` `6f20c268…90013e` (MATCH Phase A); `node_modules/` absent (metadata-level analysis, as intended).
- **Installed runtime identity:** unchanged/not touched (record-only: Node v24.20.0, pnpm 11.7.0, dsh uid 999 per Phase A/B records).
- **Effective profiles/bundles/patches:** unchanged; none emitted.
- **Persistence backend:** unchanged.
- **Upstream sources consulted:** GitHub Advisory Database API + npm-registry metadata (read-only, version-mapping only); pinned local corpus for importer chains. No upstream fetch of package code.
- **Allowed changes:** writes to `pilots/PILOT-DSH-IMPL-001/10b-morpheus-r1-advisory-analysis.md` only.
- **Protected constraints honored:** no lockfile rewrite, no install, no hxs-15 contact; no credential-shaped literals (none exist in this analysis surface); append-only governance records.
- **Required tests:** `python3 scripts/validate.py` from repo root, 4/4 PASS.
- **Known drift/conflicts:** one advisory-metadata inconsistency noted of record (row 9, js-yaml); one withdrawn advisory excluded (§2). No corpus drift — anchors match.
- **Rollback state:** document-only change; pre-state recoverable from git history.
- **proceed_status:** MAY_PROCEED (all fields available and consistent).

## 7. Sanitized command log

| Command | Host | Purpose | Status |
| --- | --- | --- | --- |
| `sha256sum package.json pnpm-lock.yaml` (corpus root) | session host (corpus read) | Anchor re-verification vs Phase A record | OK — MATCH |
| `grep`/`python3` parse of `pnpm-lock.yaml` `snapshots:` section | session host (corpus read) | Pinned versions of 14 affected packages + importer chains | OK (read-only) |
| GitHub Advisory API `affects=<pkg@pinned>` × ~20 queries (read-only) | session host → public API | GHSA ids, severities, first_patched_version, withdrawn flags | OK |
| npm-registry metadata reads for pinned importer versions | session host → public API | Declared ranges (`^7.25.0`, `^4.11.4`, etc.) for compatibility check | OK (read-only) |
| Write/edit of this document (+ skeleton-first) | session host | Product 2 | OK |
| `python3 scripts/validate.py` (repo root) | session host | Work-order gate | PASS — 4/4 checks (wiki-sync render --check, fixture-suite, catalog-mechanical, secret-boundary), manual gates noted, exit 0 — 2026-08-29 [OPEN CORRECTION 2026-08-29, labeled, append-only — review batch 2, F25: placeholder "see close-out" replaced with the actual gate result of record.] |

No hxs-15 contact, no candidate mutation, no install/lockfile rewrite, no credential values.
