# ARCHIVE — 2026-08-31 template consolidation

Status: RETIRED 2026-08-31.

`governace/templates/` is the single centralized template directory. The KDD
template previously lived both as `governace/templates/kdd.md` and as
`governace/decisions/KDD-0000-template.md`. The two were byte-identical; the
decisions-directory copy was the stray duplicate and has been retired here.

The catalog record `DOC-kdd-0000-template` was re-pointed to
`governace/templates/kdd.md` (the canonical location).

Original path: `governace/decisions/KDD-0000-template.md`.

---

Also retired here: `pilots/_templates/` (work-order.yaml + context-packet.yaml),
the tool-scope mirror of `governace/templates/pilot/`. The mirror was archived
2026-08-31 and is no longer maintained; the canonical pilot templates remain at
`governace/templates/pilot/`. Catalog records `DOC-pilot-templates-work-order`
and `DOC-pilot-templates-context-packet` were re-pointed to the canonical paths.
