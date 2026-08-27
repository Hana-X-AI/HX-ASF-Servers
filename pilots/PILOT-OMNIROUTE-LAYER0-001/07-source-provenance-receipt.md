# OmniRoute v3.8.51 — Source Provenance Receipt (Wave 0B)

| Field | Value |
| --- | --- |
| Date | 2026-08-27 (UTC) |
| Program | PILOT-OMNIROUTE-LAYER0-001 (p11) |
| Receipt by | Kimi-K3 (governor) — deterministic verification, no model inference used for any fact below |
| Identity verdict | **VERIFIED — content-sensitive proof: the local snapshot is byte-for-byte identical to upstream `diegosouzapw/OmniRoute@42a13fedef8b…` (release/v3.8.51 at snapshot time)** |

Truth-state labels: VERIFIED / REPORTED / INFERRED / NOT-ESTABLISHED / RECORD.

## 1. Identity

| Item | Value | State |
| --- | --- | --- |
| Local source path | `/opt/tkv-local/OmniRoute-release-v3.8.51` | VERIFIED (exists; cataloged DOC-tkv-corpus-omniroute) |
| Package version | `3.8.51` (`package.json` `"version": "3.8.51"`) | VERIFIED |
| Reported branch | `release/v3.8.51` | **VERIFIED** — it is the upstream DEFAULT branch |
| Reported commit | `42a13fedef8bb6806c1c4382b2c65539e871e88c` | **VERIFIED — content-identical** (proof in §3) |
| Commit upstream date/message | 2026-08-26T16:43:58Z, "fix(search): properly resolve configured search connection in /v1/responses pipe" | VERIFIED (GitHub API) |
| Branch head at verification | `c9f11d86b55d…` — upstream has moved past the snapshot (expected; snapshot pinned at 42a13fe) | VERIFIED (GitHub API) |
| Git metadata in local tree | ABSENT (no `.git`) — local tree alone cannot prove upstream identity | FACT (method used instead: content comparison) |
| Acquisition method | Owner download from a Drive share ("My Drive/HX-File-Share/operations/OmniRoute-release-v3.8.51" per the candidate manifest) | RECORD (owner-supplied) |
| Source file count | 13,098 files (`.git` excluded) | VERIFIED |
| Content-sensitive manifest | sha256 `085fb94b7d76c34291daea9ab792cbee8df60d83a5c64ee874e4f0b35e6b535d` — per-file `<sha256>  <relpath>` lines, LC_ALL=C sorted, trailing newline (method of record; supersedes the earlier names-only digest c5a65089…) | VERIFIED |
| `package-lock.json` | sha256 `58a9d07124dc06e6b46c4aecd41e1245102aafb0787d46d02d9de23f3ad9bb5f` | VERIFIED (present, root) |
| `package.json` | sha256 `fe6c7dbebe5709a2b42296d19bc6280aee620ccc3d3e5a1161fa27439a328045` | VERIFIED |

## 2. License, instructions, requirements

- **License: MIT** (`LICENSE`, © 2026 diegosouzapw) — VERIFIED. Third-party notices: package-lock carries the dependency tree (Layer-1 review input).
- **Node engine requirement:** `>=22.22.2 <23 || >=24.0.0 <27` (package.json `engines`; matches the candidate manifest) — VERIFIED. hxs-8 has NO node/npm today (rick's readiness evidence) — the single Layer-1 dependency.
- **Instruction files:** 3× `AGENTS.md` (root + 2 nested), 87× `CLAUDE.md`/`GEMINI.md` across the tree — VERIFIED by inventory. All are upstream-project guidance for working ON OmniRoute; all read-only here; any HX-side use is reviewed at Layer 1 before adoption (repo AGENTS.md adoption rule).
- **Top-level layout:** `src/`, `packages/`, `config/`, `docker/`, `electron/`, `docs/`, `examples/`, `open-sse/`, `@omniroute/`, `skills/`, `tests/`, `bin/`, `scripts/`, `public/`, `changelog.d/`, `contrib/`, `images/` — Next.js 16 standalone build per the root AGENTS.md (dev port 20128).

## 3. Content-sensitive identity proof (the p11 bar)

Method (deterministic, reproducible):

1. Local per-file manifest: 13,098 files hashed (sha256), zero errors — digest in §1.
2. Upstream tree at the reported commit fetched via GitHub API (`git/trees/42a13fe…?recursive=1`): 15,406 entries, **13,098 blobs, truncated: false**.
3. Per-file content comparison using **git blob identity** (sha1 of `blob <len>\0<content>`) local vs upstream:

| Check | Result |
| --- | --- |
| Content-identical | **13,098 / 13,098** |
| Upstream-only (missing locally) | 0 |
| Local-only (extra) | 0 |
| Content differs | 0 |
| Read errors | 0 |

Conclusion: the local snapshot is **byte-for-byte identical** to upstream `release/v3.8.51@42a13fedef8b…`. The candidate documents' pinned identity is upheld by content-sensitive proof, not by package-version inference.

## 4. Contradictions and limitations (preserved, ranked)

1. **Bundled documentation version drift (VERIFIED):** several `docs/ops/*.md` reference `3.8.40`/`3.8.50` (e.g. VM_DEPLOYMENT_GUIDE, TUNNELS_GUIDE, DATABASE_GUIDE, FLY_IO_DEPLOYMENT_GUIDE). Resolution per the plan's own rule: package metadata, lockfile, commit, and this receipt outrank document frontmatter.
2. **Snapshot age:** upstream head is one commit past the snapshot (`c9f11d86…` vs `42a13fe…`). The pinned identity is the snapshot's; upgrade decisions are Layer-3+/owner territory (OD-11 production-version policy).
3. **Acquisition channel** is RECORD (owner Drive share) — content equality with upstream closes the provenance gap the channel leaves; nothing further required for Layer 0.
4. **NOT-ESTABLISHED:** none remaining for source identity. Runtime behavior, capability surface (the ledger, next), and deployment fitness are separate questions with their own evidence.

## 5. Downstream effect

- The capability ledger (next Wave 0B task set) may cite this commit as `VERIFIED` source identity in every entry's provenance fields.
- The catalog record DOC-tkv-corpus-omniroute gains the content-sensitive manifest digest + this verification at the next Carol wave (superseding the names-only digest, method of record preserved in notes).
