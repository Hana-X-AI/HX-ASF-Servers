# WORK ORDER — Carol: catalog batch (new + updated docs)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Carol (knowledge steward, bounded persistent role).
- Lane: `omniroute/gpt-oss-120b` (OpenAI gpt-oss-120b, AkashML, via OmniRoute).
- Class: background — non-blocking.

## Intent

Catalog the new and updated documents from this session. Create catalog
records and index entries for each. Verify cross-references are consistent.

## New documents to catalog

1. `servers/system-mapping.md` — HX system-to-server mapping (replaces retired
   `hxs3-workload-placement.md`). Authoritative system placement document.
2. `agents/quinn/profile.md` — Quinn (Qdrant vector database engineer) profile.
3. `agents/quinn/charter.md` — Quinn charter.
4. `knowledge/decisions/KDD-0016-agent-taxonomy-and-standard-template.md` —
   Agent family taxonomy and standard profile/charter template.
5. `knowledge/decisions/KDD-0015-wayne-registration.md` — Wayne (Redis engineer)
   registration (may already be cataloged — verify).
6. `agents/_template/profile.md` — Standard profile template (KDD-0016).
7. `agents/_template/charter.md` — Standard charter template (KDD-0016).

## Updated documents needing catalog record updates

1. `AGENTS.md` — added: archify skill (11th skill), system-to-server mapping
   section, agent family taxonomy section (KDD-0016).
2. `agents/README.md` — added: Quinn roster row, 7 new pending agents
   (sage, iris, scout, piper, ripple, erwin, nexus), system-mapping
   reference.
3. `servers/SERVER-REGISTRY.md` — added: system-mapping cross-reference rule,
   labeled correction block reconciling 8 stale rows.
4. All 11 agent profiles — normalized per KDD-0016: governor naming,
   family field, SSH sections, knowledge directory pointers, be-great
   standing directive, Mia in reporting chains.
5. All 11 agent charters — normalized per KDD-0016: frontmatter, family
   field, governor naming.

## Cross-reference verification

Verify these cross-references exist and are consistent:
- `servers/system-mapping.md` ↔ `servers/SERVER-REGISTRY.md` (bidirectional)
- `servers/system-mapping.md` ↔ `AGENTS.md` (AGENTS.md references mapping)
- `servers/system-mapping.md` ↔ `agents/README.md` (README references mapping)
- `knowledge/decisions/KDD-0016` ↔ `agents/_template/` (template follows KDD)
- `knowledge/decisions/KDD-0016` ↔ `AGENTS.md` (AGENTS.md has taxonomy section)
- `agents/quinn/` ↔ `agents/README.md` (roster row)
- `agents/quinn/` ↔ `servers/system-mapping.md` (agent assignment)
- Each agent profile ↔ `servers/system-mapping.md` (if applicable)

## Constraints

- Background-class: do not block any work.
- Knowledge-only: writes scoped to `knowledge/catalog/`.
- No secret values in catalog.
- `scripts/validate.py` 4/4 after writes.
- Context budget: targeted reads, not whole-file dumps.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with catalog receipt and validate.py output.
