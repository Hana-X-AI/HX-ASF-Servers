#!/usr/bin/env python3
"""catalog_freshness.py — does the catalog still describe the current files? (SY-8)

`validate.py`'s catalog-mechanical check verifies schema, required fields,
enums, index 1:1, relation resolution and location existence. It never compares
a record's recorded `sha256` to its source. `carol-mint sweep-stale` does, but
nothing wired it into the validator.

The consequence was measured on 2026-08-30: **42 in-repo records had drifted
from their live files while `validate.py` reported 5/5 PASS**. A catalog that
does not describe the current files is the failure mode the catalog exists to
prevent, and it was invisible to the gate.

THREE CATEGORIES, GRADED DIFFERENTLY. Treating them alike is why this was not
already a check — a blanket sweep is 99 findings on a healthy repository, which
is indistinguishable from noise.

  CF-01  in-repo drift        FAIL. The record and the file are both here and
                              they disagree. Re-mint fixes it.
  CF-02  in-repo source gone  FAIL. A record points at a repo path that no
                              longer exists — a rename or delete that left the
                              record behind.
  CF-03  off-host source      REPORT. `canonical_location` under /opt/tkv-local
                              or another host-anchored path. Unverifiable from a
                              clone, exactly as CAT-07's probe is skipped under
                              --ci. Failing these would make the check pass only
                              on the governor's own machine.
  CF-04  living record        REPORT. `freshness: living` records are expected
                              to drift between consolidations by design; that is
                              what `carol-mint consolidate` is for.
  (dir)  cataloged directory REPORT. A directory has no content hash. CAT-07
                              accepts these; probing with isfile instead of
                              exists reported all ten of them as missing.

Hashing and record loading are imported from `scripts/catalog/carol-mint`, not
reimplemented — one contract, one place to fix a check.

Usage:
    python3 scripts/catalog_freshness.py [--json]

`plan()` returns (summary, problems) to match skills_sync, hooks_verify,
skills_registry and work_order.

Read-only. No network.
"""

import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINT = os.path.join(ROOT, "scripts", "catalog", "carol-mint")
BASELINE = os.path.join(ROOT, "governace", "catalog-freshness-baseline.yaml")


def baseline():
    """Ids whose drift predates this check. Reported, not failed — see the
    file's own header for why re-minting all of them would be worse."""
    if not os.path.isfile(BASELINE):
        return set()
    import yaml
    with open(BASELINE, encoding="utf-8") as fh:
        return set(yaml.safe_load(fh).get("ids") or [])


def _carol_mint():
    """Import carol-mint, which has no .py extension. Module-level code is
    constants and defs behind a __main__ guard, so importing runs nothing."""
    spec = importlib.util.spec_from_loader(
        "carol_mint", importlib.machinery.SourceFileLoader("carol_mint", MINT))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def plan():
    """Return (summary, problems)."""
    problems, notes = [], {"drift": 0, "gone": 0, "offhost": 0, "living": 0,
                            "dir": 0, "baselined": 0, "total": 0}
    known = baseline()
    try:
        cm = _carol_mint()
    except Exception as e:
        return "catalog-freshness: carol-mint unavailable", ["[CF-00] %s" % e]

    for doc_id, _path in cm.iter_records():
        notes["total"] += 1
        try:
            doc = cm.load_record(doc_id)["document"]
        except SystemExit:
            problems.append("[CF-00] %s: record unreadable" % doc_id)
            continue
        src = doc.get("canonical_location")
        if not src:
            problems.append("[CF-02] %s: no canonical_location" % doc_id)
            continue

        probe = src if os.path.isabs(src) else os.path.join(ROOT, src)
        in_repo = os.path.abspath(probe).startswith(ROOT + os.sep)

        if not in_repo:
            # Host-anchored. Its hash is only meaningful on the governor host,
            # so it is counted and never graded — the same reasoning that makes
            # CAT-07 skip its existence probe under --ci.
            notes["offhost"] += 1
            continue

        if os.path.isdir(probe):
            # A record may catalog a DIRECTORY (scripts/fleet, the omniroute
            # ledger). CAT-07 probes with os.path.exists and accepts these; a
            # directory has no content hash, so it is counted, not graded.
            # Checking isfile alone reported all ten as missing sources.
            notes["dir"] += 1
            continue

        if not os.path.exists(probe):
            if in_repo:
                notes["gone"] += 1
                problems.append("[CF-02] %s: canonical_location is inside the repo but "
                                "does not exist: %s" % (doc_id, src))
            else:
                notes["offhost"] += 1
            continue

        live = cm.sha256_file(probe)
        if live == doc.get("sha256", ""):
            continue
        if (doc.get("validation") or {}).get("freshness") == "living":
            notes["living"] += 1
            continue
        if doc_id in known:
            notes["baselined"] += 1
            continue
        notes["drift"] += 1
        problems.append("[CF-01] %s: record sha256 %s… does not match %s (%s…) — "
                        "re-mint: python3 scripts/catalog/carol-mint re-mint %s"
                        % (doc_id, str(doc.get("sha256", ""))[:12], src, live[:12], doc_id))

    summary = ("catalog-freshness: %d records — %d in-repo drift, %d in-repo source "
               "missing; not graded: %d off-host, %d directory, %d living, "
               "%d baselined (pre-existing backlog)"
               % (notes["total"], notes["drift"], notes["gone"],
                  notes["offhost"], notes["dir"], notes["living"],
                  notes["baselined"]))
    return summary, problems


def main(argv):
    summary, problems = plan()
    if "--json" in argv:
        print(json.dumps({"summary": summary, "problems": problems}, indent=2))
        return 1 if problems else 0
    for p in problems:
        print(p)
    print(summary)
    if problems:
        print("catalog-freshness: %d problem(s)" % len(problems))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
