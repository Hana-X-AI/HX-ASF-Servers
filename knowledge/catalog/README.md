# Catalog — the HX second brain

The start of a second brain for the whole HX team — humans and agents
(owner, 2026-08-25). Stewarded by **Carol** (`agents/carol/`); governed by the
"Documentation governance and knowledge stewardship" section of `AGENTS.md`.

A question about a server, FQDN, service, configuration, dependency, or prior
decision should be answerable from here — from validated, provenance-backed
knowledge — without rereading the repository or repeating completed reconnaissance.

Governing principle: **retrieve before investigating; reuse before recomputing;
verify before trusting; catalog before closing.**

## What lives where

- `schema.yaml` — the document-record schema (v1). Changed only through Carol's
  profile governance.
- `index.yaml` — the fast lookup surface: one line per cataloged document (id,
  title, type, authority, freshness, location).
- `documents/DOC-<slug>.yaml` — one machine-readable record per cataloged document:
  identity, purpose, labeled inference, applies-to, authority and supersession,
  security classification, relationships, freshness, checksum, canonical location.
- `receipts/` — Carol's catalog receipts. Every ingestion or update produces one;
  a material handoff is incomplete until its receipt exists and is referenced in
  the governing log.
- `retrieval-packages/` — focused, provenance-tagged query answers produced per
  Carol's profile §5 (facts with source refs and freshness, conflicts flagged,
  token-bounded) instead of whole collections.

## Rules of the house

- Originals are never edited. The catalog describes and connects; sources stay
  authoritative and unchanged.
- Every fact traces to a source document and section. No provenance, no entry.
- Conflicts are preserved with both claims, authority-ranked, and escalated —
  never guess-resolved.
- Truth-state labels from `knowledge/README.md` apply; historical as-found records
  are precedent and cross-check, never current truth.
- No secret values here — protected resources are recorded by existence, owner,
  and retrieval mechanism only.

## How to use it

- **Humans and agents, reading:** start at `index.yaml`, follow to the document
  record, then to the source only if needed. If the answer isn't here, that's a
  catalog gap — report it.
- **Kimi-K3, assigning work:** consult the catalog first; cite consulted records
  in context packets; request a focused retrieval package from Carol instead of
  loading whole collections.
- **Agents, closing work:** return new reusable facts and artifacts; the handoff
  completes when Carol's receipt lands.
- **Owner, supplying documents:** every supplied document gets a recorded
  disposition — cataloged, linked, flagged, or rejected with reason.
