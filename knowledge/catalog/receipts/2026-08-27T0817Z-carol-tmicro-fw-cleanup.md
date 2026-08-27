[CATALOG RECEIPT]
Run: 2026-08-27T0817Z Agent: Carol Trigger: Kimi-K3 governor — T-micro-with-bundle-budget run "F-W cleanup" (4 tasks, ratified ≤15 min budget; provenance: OmniRoute pilot log row 17 + hxs-2 log row 54, cleanup of the 0726Z wave's flags F-W1/F-W2/F-W3 + state-log advances)
Tier: T-micro (4-task bundle under the owner-ratified ≤15 min budget, profile §10 bundle calibration). Scope read: run-tier block, the five write-set records, index.yaml lookups for the touched ids.

Added: none.

Updated (5):
- DOC-assessment-second-brain-feature-review — F-W1 CLOSED. Re-hashed for the governor's batch-18 F2 precision edit: `367ff64a…` → `a69f2696a2d4a6d2f41ab873f845ca2e0a8001c83d10da19fd0f03672981979e`. The §4 fleet-matrix line ("hxs-1 through hxs-4 all-PASS on the llm-host rules; hxs-8 is 1 PASS plus one honest REPORT — NTP still ntp.ubuntu.com, unchanged, the owner's pending call") VERIFIED PRESENT at source line 51. Chain step + provenance recorded in notes.batch18_f2_rehash.
- DOC-agent-trinity-profile — F-W2 CLOSED. One line appended to notes.source_remnants: the carried-open commit-42a13fedef8b…-wording flag is SUPERSEDED BY notes.commit_wording_resolution (row-9 governor fixes, already RESOLVED there); wording at source lines 110-118 / ~179 refreshed 2026-08-27, flag closed (batch-18 F3). Rest of the field preserved as history. Source re-hash: UNCHANGED `4954c02b…` (no source edit this wave).
- DOC-tkv-corpus-ubuntu — F-W3 CLOSED. Names-only manifest regenerated per the record's checksum_method convention (.git/.idea excluded): `962683e0…` → `a9d9f3e47b68d3d7125685929db3116e08662e8f982465f168f3455cf9e5ffa8`; file count 2,127 → 2,162. Method PROVEN before adoption: the pipeline (`find /opt/tkv-local/ubuntu -type f -not -path '*/.git/*' -not -path '*/.idea/*' | sort | sha256sum` — absolute paths, en_US.UTF-8 sort) reproduces the prior 962683e0… digest exactly on the pre-addition subset, and the sibling DOC-tkv-corpus-ollama digest d2545086… was reproduced exactly as an independent known-answer. New items noted with date in notes.corpus_addition_20260827: ubuntu_mcp_server-master (briefed F-W3 scope, 21 files incl.; cataloged separately as DOC-tkv-corpus-ubuntu-mcp-server) and refs-ubuntu-24.04 (mid-run arrival, 14 files — see Flagged).
- DOC-pilot-omniroute-state-log — advanced rows 1–16 → 1–18: `406be95f…` → `63b4716ef7d9b70f5cf894d19af72b3309f17e73c388cef72b5007a14aa8ca44`. Briefed target 1–17 overtaken mid-run by row 18 (08:02Z, ledger P5 COMPLETE + citation contract PROVEN 4.0% vs 35.6%, P7 dispatched); transient 7bbf98b4… (rows 1-17, 08:01-08:06Z) recorded, never cataloged.
- DOC-pilot-hxs2-state-log — advanced rows 1–53 → 1–55: `f981c931…` → `7e83466d4592d7cfdcf8850a18c89dbbb08a2b2bb48b922281c45f3aaf4f3c08`. Briefed target 1–54 overtaken mid-run by row 55 (07:54Z, owner ratifies the recommendation set); transient b65a7419… (rows 1-54, 08:01-08:06Z) recorded, never cataloged.

Linked: none new.

Flagged (each with provenance):
- MID-RUN DRIFT (governor + owner/rick lanes live during this run): three forced re-mint cycles. OmniRoute log row 18 landed 08:02Z; hxs-2 log row 55 landed 07:54Z; the ubuntu corpus tree gained refs-ubuntu-24.04 (rick's owner-ratified reference pack, hxs-2 log row 55 — 14 files incl. MANIFEST.md with per-file sha256) at 07:5x-08:0xZ, after the 2,148-file mcp-server-state mint. All three records re-minted at close content per the living-log doctrine; transient states recorded openly in the records' hash chains.
- F-TMICRO-TIME (over-target path): ~35 min end-to-end (dispatch 07:42:46Z → close 08:17Z) vs the ratified ≤15 min bundle budget. Causes: the F-W3 method-reproduction investigation (the 2026-08-25 pipeline was under-documented — now pinned exactly in notes.checksum_method) plus the three mid-run re-mint cycles above. Precedent: the 2026-08-27T0030Z run's ~28 min on the same churn class. Informational; logged for the boundary calibration.
- Carry-forward dependency: this run's minted hashes are current as of 08:15Z. The ledger partitions P6/P7 are in flight and the refs-ubuntu-24.04 commission is still growing — the two state-log records and the ubuntu corpus record will go hash-stale on the next appends (expected next-wave advance scope, per the living-log convention).

Rejected: none.

Freshness: no state changes — all five records stay `current`; validated_at 2026-08-27T08:01:00Z (wave stamp; final verification 08:15Z recorded here).

Follow-ups:
- hxs-2 log row 55: the Second Brain review cadence was RATIFIED by the owner — DOC-assessment-second-brain-feature-review's notes.cadence_owner_pending flips at the NEXT wave (explicitly queued there by the governor, not this wave's write set).
- refs-ubuntu-24.04: pack still growing under rick's in-flight commission; its standalone catalog disposition ("Carol catalogs after" per row 55) + the corpus record's next manifest re-hash ride the next wave.
- Ledger partitions P6/P7 (and P5..P8 completions + the Wave-0B handoff) — state-log advance scope for the next wave (already pre-flagged in the OmniRoute record).
- Full-catalog validate.py at the next T-standard/T-full; carry-forward window (0726Z, 4/4 PASS) runs to 2026-08-28T07:26Z.

Verification (T-micro scope — write set only): 73/73 PASS — YAML parse + schema required fields (5/5 records); record sha256 == live source/manifest (4 file-backed + 1 directory manifest at 2,162 files); index 1:1 on title/type/authority_level/freshness/canonical_location (5/5); all DOC-* relation targets of the touched records resolve in documents/ + index (42/42); index document_count 260 == 260 entries (0 added this wave). Carry-forward: validate.py 4/4 PASS per receipt 2026-08-27T0726Z, inside its 24 h window — cited, not re-run (T-micro rule).

Index: updated (sha256 abd5df8f75aaaa4f2e427cbf172b1cd8dbff2c3501a006ab1901d0cedf304e20) — header stamped 2026-08-27T0815Z, 0 added / 5 updated; two state-log title row-windows synced (1–18, 1–55).

Result: PASS — CATALOG CURRENT

## Addendum (2026-08-27, review batch 21: locale-pinned reproduction)

For exact cross-locale reproduction, the documented manifest pipeline is pinned with the locale set on every step: `env LC_ALL=en_US.UTF-8 find /opt/tkv-local/ubuntu -type f -not -path '*/.git/*' -not -path '*/.idea/*' | env LC_ALL=en_US.UTF-8 sort | sha256sum`. Governor-verified 2026-08-27: this exact form reproduces `a9d9f3e47b68d3d7125685929db3116e08662e8f982465f168f3455cf9e5ffa8` byte-identically (only `sort` is locale-sensitive; the pinning costs nothing and removes ambiguity). The original line's "en_US.UTF-8 sort" is preserved above.
