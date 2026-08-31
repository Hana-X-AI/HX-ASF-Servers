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

from collections.abc import Mapping
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINT = os.path.join(ROOT, "scripts", "catalog", "carol-mint")
BASELINE = os.path.join(ROOT, "governace", "catalog-freshness-baseline.yaml")


HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def baseline():
    """Return ({id: pinned entry}, problems) for the known-drift ledger."""
    problems = []
    if not os.path.isfile(BASELINE):
        return {}, ["[CF-05] catalog freshness baseline missing: %s" % BASELINE]
    import yaml
    try:
        with open(BASELINE, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except Exception as e:
        return {}, ["[CF-05] baseline unreadable: %s" % e]
    if not isinstance(data, Mapping):
        return {}, ["[CF-05] baseline top level must be a mapping"]
    if data.get("schema_version") != 1:
        problems.append("[CF-05] baseline schema_version must be 1")
    rows = data.get("entries")
    if not isinstance(rows, list):
        return {}, problems + ["[CF-05] baseline entries must be a list"]
    if data.get("count") != len(rows):
        problems.append("[CF-05] baseline count %r != %d entries" %
                        (data.get("count"), len(rows)))
    entries = {}
    required = ("id", "canonical_location", "recorded_source_sha256",
                "source_sha256_at_baseline", "catalog_record_sha256")
    for i, row in enumerate(rows):
        if not isinstance(row, Mapping):
            problems.append("[CF-05] baseline entry %d is not a mapping" % i)
            continue
        missing = [key for key in required if not row.get(key)]
        if missing:
            problems.append("[CF-05] baseline entry %d missing: %s" %
                            (i, ", ".join(missing)))
            continue
        doc_id = str(row["id"])
        if doc_id in entries:
            problems.append("[CF-05] duplicate baseline id: %s" % doc_id)
            continue
        for key in required[2:]:
            if not HASH_RE.match(str(row[key])):
                problems.append("[CF-05] %s: %s is not a full sha256" %
                                (doc_id, key))
        entries[doc_id] = row
    return entries, problems


def _carol_mint():
    """Import carol-mint, which has no .py extension. Module-level code is
    constants and defs behind a __main__ guard, so importing runs nothing."""
    # carol-mint's historical default is the governor-host checkout. A clean CI
    # runner has no /home/hxsa tree, so bind this imported instance to the
    # checkout being validated unless a test deliberately supplies an override.
    catalog_root = os.environ.get(
        "CAROL_MINT_ROOT", os.path.join(ROOT, "knowledge", "catalog"))
    prior_root = os.environ.get("CAROL_MINT_ROOT")
    os.environ["CAROL_MINT_ROOT"] = catalog_root
    try:
        loader = SourceFileLoader("carol_mint", MINT)
        spec = spec_from_loader("carol_mint", loader)
        mod = module_from_spec(spec)
        loader.exec_module(mod)
    finally:
        if prior_root is None:
            os.environ.pop("CAROL_MINT_ROOT", None)
        else:
            os.environ["CAROL_MINT_ROOT"] = prior_root
    return mod


def tracked_repo_sources():
    """Return repo-relative source paths whose records SY-8 grades."""
    cm = _carol_mint()
    paths = set()
    for doc_id, record_path in cm.iter_records():
        try:
            record = cm.load_yaml(record_path)
            if not isinstance(record, Mapping) or not isinstance(record.get("document"), Mapping):
                raise ValueError("catalog document mapping missing")
            doc = record["document"]
        except Exception as e:
            raise RuntimeError("catalog record %s unreadable: %s" % (doc_id, e)) from e
        source = doc.get("canonical_location")
        if not source or not cm.is_repo_source(source):
            continue
        probe = os.path.abspath(cm.resolve_source(source))
        paths.add(os.path.normpath(os.path.relpath(probe, ROOT)))
    return paths


def plan():
    """Return (summary, problems)."""
    problems, notes = [], {"drift": 0, "gone": 0, "offhost": 0, "living": 0,
                            "dir": 0, "baselined": 0, "total": 0}
    known, baseline_problems = baseline()
    problems.extend(baseline_problems)
    try:
        cm = _carol_mint()
    except Exception as e:
        return "catalog-freshness: carol-mint unavailable", ["[CF-00] %s" % e]

    seen = set()
    for doc_id, record_path in cm.iter_records():
        notes["total"] += 1
        seen.add(doc_id)
        try:
            doc = cm.load_record(doc_id)["document"]
        except SystemExit:
            problems.append("[CF-00] %s: record unreadable" % doc_id)
            continue
        src = doc.get("canonical_location")
        if not src:
            problems.append("[CF-02] %s: no canonical_location" % doc_id)
            continue

        probe = cm.resolve_source(src)
        in_repo = cm.is_repo_source(src)

        if not in_repo:
            # Host-anchored. Its hash is only meaningful on the governor host,
            # so it is counted and never graded — the same reasoning that makes
            # CAT-07 skip its existence probe under --ci.
            notes["offhost"] += 1
            if doc_id in known:
                problems.append("[CF-05] %s: baseline entries must reference an "
                                "in-repo file" % doc_id)
            continue

        if os.path.isdir(probe):
            # A record may catalog a DIRECTORY (scripts/fleet, the omniroute
            # ledger). CAT-07 probes with os.path.exists and accepts these; a
            # directory has no content hash, so it is counted, not graded.
            # Checking isfile alone reported all ten as missing sources.
            notes["dir"] += 1
            if doc_id in known:
                problems.append("[CF-05] %s: baseline entries cannot reference a "
                                "directory" % doc_id)
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
            if doc_id in known:
                problems.append("[CF-05] %s: record is reconciled; remove its stale "
                                "baseline entry" % doc_id)
            continue
        if (doc.get("validation") or {}).get("freshness") == "living":
            notes["living"] += 1
            continue
        if doc_id in known:
            entry = known[doc_id]
            pin_problems = []
            checks = (
                ("canonical_location", str(src)),
                ("recorded_source_sha256", str(doc.get("sha256", ""))),
                ("source_sha256_at_baseline", live),
                ("catalog_record_sha256", cm.sha256_file(record_path)),
            )
            for key, actual in checks:
                if str(entry.get(key, "")) != actual:
                    pin_problems.append("%s changed" % key)
            if pin_problems:
                notes["drift"] += 1
                problems.append("[CF-01] %s: changed after baselining (%s) — reconcile "
                                "the record and remove its baseline entry" %
                                (doc_id, ", ".join(pin_problems)))
            else:
                notes["baselined"] += 1
            continue
        notes["drift"] += 1
        problems.append("[CF-01] %s: record sha256 %s… does not match %s (%s…) — "
                        "re-mint: python3 scripts/catalog/carol-mint re-mint %s"
                        % (doc_id, str(doc.get("sha256", ""))[:12], src, live[:12], doc_id))

    for doc_id in sorted(set(known) - seen):
        problems.append("[CF-05] %s: baseline id has no catalog record" % doc_id)

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
