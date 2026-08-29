# PILOT-DSH-IMPL-001 — Phase C Prep: Candidate Seams & Activation

**Order:** 09b (rescoped from work order 09)
**Issuer:** Kimi-K3 (governor), 2026-08-29
**Executor:** Morpheus (dsh lifecycle steward, WATCH lane)
**Model:** `omniroute/coder-x` (hxs-2, digest `ec9ebe08…a9f1`)
**Parent records:** 03 Phase A prep (interop/activation), 05 Phase B prep (testing/validation/rollback framework)
**Corpus path (read-only):** `/opt/tkv-local/deepseek-harness-master`

---

## Purpose

Per the [Phase C prep plan — PILOT-DSH-IMPL-001] section "Phase C Scope" (Gates 8–10):

This product provides, for each activation candidate identified in Phase A/Gate 7:

1. **Exact source seams** from the pinned harness corpus (`file:line`).
2. **Activation mechanism** on the native composition layer (cordis class + pattern), matching the Phases A/B template: `patch-interop`, `patch-sandbox`, `deploy-remote`.
3. **Host prerequisites** for each seam and its deployment target.
4. **Risk classification** from the Phase B taxonomy (`RISK_*`).

This document also supplies **read-only testability notes for Gordon's Gate 8–10 authoring**, stating what is provable on hxs-15's frozen corpus, and what is BLOCKED-by-design (no candidate mutation).

---

## Product families (Gates 8–10 scope)

Each family maps to a Phase C gate cluster from the plan:

| Gate range | Family           | Purpose                                  |
| ---------- | ---------------- | -------------------------------------- |
| Gates 8a   | interop          | Cross-seam coordination & injection     |
| Gates 8b   | sandboxing       | Harness-level isolation & capability caps |
| Gates 9    | remote           | Remote endpoint + model discovery        |
| Gates 10   | experimental     | Feature-flagged experimentation layer     |

---

## Family 1: I/O interop (Gates 8a)

### Source seams

<!-- Filled by targeted reads of harness corpus — see 03 Phase A pattern -->

### Activation mechanism

<!-- Cordis patch-interop class + per-family description -->

### Host prerequisites

<!-- Required packages / daemon state on each target host -->

### Risk classification

<!-- RISK_* code from Phase B taxonomy, with one-line rationale -->

---

## Family 2: Sandbox activation (Gates 8b)

### Source seams

### Activation mechanism

### Host prerequisites

### Risk classification

---

## Family 3: Remote endpoint deployment (Gate 9)

### Source seams

### Activation mechanism

### Host prerequisites

### Risk classification

---

## Family 4: Experimental layer (Gate 10)

### Source seams


### Activation mechanism


### Host prerequisites


### Risk classification



## Testability matrix (Gordon's Gate 8–10 authoring reference)

<!-- Filled family by family as each is researched. One row per seam/activation pair -->

| Family    | Seam ID     | Provability | BLOCKED-by-design? | Rationale                               |
| --------- | ----------- | ----------- | ---------------- | ------------------------------------- |
| interop   | (to fill)   | TBD         | —                | —                                       |
| sandbox   | (to fill)   | TBD         | —                | —                                       |
| remote    | (to fill)   | TBD         | —                | —                                       |
| experimental | (to fill) | TBD         | —                | —                                       |

Each PROVABLE row lists exact command(s)/test(s) Gordon can run read-only
against the frozen hxs-15 corpus to validate readiness. Each BLOCKED-by-design
row notes what requires candidate mutation and why those are deferred.

## Open risks & items (Phase C pre-check)

<!-- Filled at last, after all families assessed -->

- [ ] Risk gap: <!-- pending family fill -->
- [ ] Validation scope: <!-- partial doc risk if target reads exceeded token cap -->

## Knowledge-review receipt

Per KDD-0009 working order for Morpheus sessions (Phase A/B precedent):

- **Receipt emitter**: This session closes first. The governor's receiving agent
  scans `pilots/PILOT-DSH-IMPL-001` for new material and catalogs it into
  `/home/hxsa/opt/HX-ASF-Servers/knowledge/catalog/PILOT-DSH-IMPL-001`.
- **Content**: Phase C prep findings (candidate seams, activation mechanism,
  risk taxonomy applied to Gates 8–10).
- **Citation format**: `PILOT-DSH-IMPL-001/10-morpheus-phase-c-prep.md` with
  section path and line ranges.

## Sanitized command log

All harness-side commands executed read-only against the corpus. Any mutations
are limited to new document files under this pilot project in `pilots/`.

| Command | Host   | Purpose                    | Status    |
| ------- | ------ | -------------------------- | --------- |
| —       | —      | (to be filled on execution) | pending   |

---

**Previous product:** 05 Phase B prep (testing/validation, rollback)
**Next product:** 09c Phase C fill (targeted reads & seed writes per family)
**Closed by:** [executor to record]

