# CAT-001 — Catalog acceptance battery (governor-owned)

Verifies that the catalog at `knowledge/catalog/` is *alive*: it answers questions
from provenance-backed knowledge, correctly, with boundaries intact.

Owner: Kimi-K3 (verification). Carol does not modify this file; she must pass it.
Run: after every major ingestion; results logged to the pilot state log (during the
pilot) or the governing log of the lane that requested the run.

## Mechanical checks (scripted)

| ID | Check | Procedure | Pass rule |
|---|---|---|---|
| CAT-01 | Schema conformance | Validate every `documents/*.yaml` against `schema.yaml` (required fields, enums, id format) | 100% conform |
| CAT-02 | Checksum integrity | Recompute sha256 of each record's `canonical_location`; compare to the record. Directory locations (corpus records) are exempt from file checksum — they carry a manifest-hash note and a scheduled re-hash instead. Protected-resource records whose digest is withheld by security policy (see CAT-05) are exempt from recompute — integrity by owner attestation | All file-backed records match (or a flagged, explained freshness note); corpus records carry the note and a `review_due`; withheld-digest records carry the attestation marker |
| CAT-03 | Index consistency | `documents/*.yaml` ↔ `index.yaml` entries | Exact 1:1, no orphans, no dangling lines |
| CAT-04 | Relation integrity | All DOC-id relation targets resolve; supersession chains are bidirectional | No unresolved targets; chains close (e.g., A01 ↔ plan §6.5; dac63d7c… ↔ 4869ce80…) |
| CAT-05 | Secret boundary | Pattern sweep over the whole catalog (passwords, keys, tokens, bearer material) | Zero hits; the ssh-info protected-resource record exists with existence/owner/mechanism only; no credential-derived verifier (content digest of the protected file) stored anywhere in the catalog |
| CAT-06 | Receipt completeness | Every ingestion/update run has a receipt in `receipts/` | No receipt-less catalog mutation |
| CAT-07 | Path resolution | Every record's `canonical_location` is checked for existence on disk (external URLs/URIs exempt, marked as such) | All locations resolve, or a flagged, explained note (added 2026-08-25 after the agents/john/carol nesting went silent ~24 h) |
| CAT-08 | Relation-target hygiene | Relation targets that reference artifacts are DOC ids when the artifact is cataloged; raw-path targets only for uncataloged external sources and must carry an explanatory note | No raw-path target for a cataloged artifact (added 2026-08-25; raw-path relations were a recurring review-finding class) |

## Known-answer retrieval set (the "is it alive" test)

**CAT-10..15 are the owner-ratified golden-question corpus (2026-08-25)** — closes
hx-second-brain-guidance-001 gap G-04.

Ask the catalog. Pass = correct answer **and** correct source refs **and** correct
freshness labels.

| ID | Question | Expected answer (with expected sources) |
|---|---|---|
| CAT-10 | Authoritative hostname and IP of the pilot target? | `hxs-1`, 192.168.50.200 (DOC for hxs-1 discovery; SERVER-REGISTRY) |
| CAT-11 | Current pilot alias Modelfile hash, and what did it supersede? | `4869ce80…3165e`, supersedes `dac63d7c…1d1df` (19-esme-m5b; plan §6.5 supersession by A01) |
| CAT-12 | hxs-1 NVIDIA driver and posture? | 580.173.02, retain-and-validate, D3 (driver-results; 07/08/26 records) |
| CAT-13 | Wi-Fi state on hxs-1? | Disabled 2026-08-25 via rfkill, owner directive (26-rick-pre-m7); DOWN as-found (discovery, historical-as-found) |
| CAT-14 | Pilot baseline model tag and approver? | `qwen3.8:27b` non-MLX, Agent Zero, KDD-0004 / A01 |
| CAT-15 | hxs-1 PCIe topology caveat? | GPU2 wired x4 vs x16 max — known since discovery 2026-08-11, re-confirmed under load (discovery; 07/22 records) |

## Judgment checks

| ID | Check | Pass rule |
|---|---|---|
| CAT-20 | Freshness audit | Stale facts (e.g., discovery's "34 packages upgradable", 2026-08-11) carry aging/stale/historical labels; nothing historical-as-found is marked current |
| CAT-21 | Conflict preservation | A documented disagreement (e.g., plan §6.5 sampling vs A01 §4.2) shows both claims, each with provenance and an authority rank — no silent single answer |
| CAT-22 | Retrieval-package economy | A focused query (e.g., "hxs-1 network facts for M7") returns only relevant facts with source refs — materially smaller than the raw corpus (the token-savings proof) |

## Standing rule

A catalog that cannot pass CAT-10..15 from its own records is not yet a brain —
it is a pile of YAML. Failure → flags to Carol, correction run, re-test.
