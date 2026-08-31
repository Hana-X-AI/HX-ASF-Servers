#!/usr/bin/env python3
"""test_work_order.py — regression fixtures for the work-order engine (O2).

The grandfathering rule is the one to get right in both directions. A schema
that failed 28 completed pilot records for lacking a field invented after they
were written would force an append-only violation; a schema that grandfathers
everything would never bind anything. Both directions are tested.

Run: python3 scripts/test_work_order.py
"""

import io
import json
import os
import shutil
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import work_order  # noqa: E402

REAL_SCHEMA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "governace", "templates", "pilot",
                           "work-order.schema.yaml")

FULL = {
    "schema_version": 1,
    "task_id": "WO-FIX-AGENT-M1-001",
    "parent_goal": "GOAL-FIX-001",
    "milestone": "M1 — a milestone",
    "assigned_agent": "rick / Rick",
    "objective": "Do the thing. Acceptance: the thing is done.",
    "boundaries": ["Files touched: one", "Stop when: two"],
    "owner_authorizations": ["Owner 2026-08-30: approved"],
    "controlling_sources": ["some-record.md"],
    "deliverable": "01-rick-thing.md",
    "deliverable_destination": ["pilots/PILOT-FIX-001/01-rick-thing.md"],
}


class WorkOrders(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.pilot = os.path.join(self.tmp, "pilots", "PILOT-FIX-001")
        os.makedirs(self.pilot)
        sch_dir = os.path.join(self.tmp, "governace", "templates", "pilot")
        os.makedirs(sch_dir)
        shutil.copy(REAL_SCHEMA, os.path.join(sch_dir, "work-order.schema.yaml"))

        self._saved = (work_order.ROOT, work_order.PILOTS, work_order.SCHEMA)
        work_order.ROOT = self.tmp
        work_order.PILOTS = os.path.join(self.tmp, "pilots")
        work_order.SCHEMA = os.path.join(sch_dir, "work-order.schema.yaml")

    def tearDown(self):
        work_order.ROOT, work_order.PILOTS, work_order.SCHEMA = self._saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, name, obj, wrap=True):
        path = os.path.join(self.pilot, name)
        with open(path, "w", encoding="utf-8") as fh:
            yaml.safe_dump({"work_order": obj} if wrap else obj, fh, sort_keys=False)
        return path

    def codes(self):
        return {p.split("]")[0].lstrip("[") for p in work_order.load_all()[2]}

    # --- shapes --------------------------------------------------------------
    def test_a_complete_v1_order_is_clean(self):
        self.write("01-work-order-rick-m1.yaml", FULL)
        orders, buckets, problems = work_order.load_all()
        self.assertEqual(problems, [])
        self.assertEqual(buckets["structured-v1"], 1)

    def test_a_v1_order_missing_a_required_field_fails(self):
        wo = dict(FULL)
        del wo["deliverable_destination"]
        self.write("01-work-order-rick-m1.yaml", wo)
        self.assertIn("WO-02", self.codes())

    def test_a_legacy_order_is_NOT_failed_for_fields_that_postdate_it(self):
        """deliverable_destination was added to the template on 2026-08-29.
        28 completed pilot records cannot carry it, and failing them would force
        rewriting append-only history to satisfy a parser written afterwards."""
        wo = dict(FULL)
        del wo["schema_version"]
        del wo["deliverable_destination"]
        del wo["boundaries"]
        self.write("01-work-order-rick-m1.yaml", wo)
        orders, buckets, problems = work_order.load_all()
        self.assertEqual(problems, [])
        self.assertEqual(buckets["structured-legacy"], 1)

    def test_a_legacy_order_still_needs_an_id(self):
        """Grandfathering is not a blanket pass. `hx gate <id>` (O3) has nothing
        to resolve without one, so addressability is enforced for every shape."""
        wo = dict(FULL)
        del wo["schema_version"]
        del wo["task_id"]
        self.write("01-work-order-rick-m1.yaml", wo)
        self.assertIn("WO-05", self.codes())

    def test_the_older_flat_convention_is_addressable(self):
        """Two work orders use a flat `id:`/`executor:` shape with no
        `work_order:` key. They carry an id, so they resolve — reading them as
        unparseable would have hidden two real work orders."""
        self.write("01-work-order-rick-flat.yaml",
                   {"id": "WO-02-fleet-baseline", "executor": "rick",
                    "milestone": "BASELINE-1"}, wrap=False)
        orders, buckets, problems = work_order.load_all()
        self.assertEqual(problems, [])
        self.assertEqual(buckets["flat-legacy"], 1)
        self.assertEqual(orders[0][0], "WO-02-fleet-baseline")

    def test_two_files_claiming_one_id_is_ambiguous_dispatch(self):
        self.write("01-work-order-a.yaml", FULL)
        self.write("02-work-order-b.yaml", FULL)
        self.assertIn("WO-04", self.codes())

    def test_markdown_orders_are_counted_not_parsed(self):
        with open(os.path.join(self.pilot, "03-flash-work-order-carol.md"),
                  "w", encoding="utf-8") as fh:
            fh.write("# WORK ORDER — Carol: catalog batch\n\n## Intent\nprose\n")
        orders, buckets, problems = work_order.load_all()
        self.assertEqual(problems, [])
        self.assertEqual(buckets["prose-legacy"], 1)

    def test_templates_are_not_work_orders(self):
        tdir = os.path.join(self.tmp, "pilots", "_templates")
        os.makedirs(tdir)
        with open(os.path.join(tdir, "work-order.yaml"), "w", encoding="utf-8") as fh:
            yaml.safe_dump({"work_order": {"task_id": "WO-<PILOT>-<AGENT>-<M>-NNN"}}, fh)
        orders, buckets, problems = work_order.load_all()
        self.assertEqual(orders, [])
        self.assertEqual(problems, [])

    # --- generation ----------------------------------------------------------
    def test_projected_fields_are_copies_not_restatements(self):
        """The hand-maintained packets were lossy: for the one real matched pair
        in the repo, the packet carried 3 of 8 boundaries and 1 of 4 owner
        authorizations. A generated packet carries all of them."""
        self.write("01-work-order-rick-m1.yaml", FULL)
        packet, err = work_order.context_packet("WO-FIX-AGENT-M1-001")
        self.assertIsNone(err)
        cp = packet["context_packet"]
        self.assertEqual(cp["goal_id"], FULL["parent_goal"])
        self.assertEqual(cp["work_order_id"], FULL["task_id"])
        self.assertEqual(cp["milestone"], FULL["milestone"])
        self.assertEqual(cp["objective"], FULL["objective"])
        self.assertEqual(cp["constraints"], FULL["boundaries"])
        self.assertEqual(cp["owner_decisions"], FULL["owner_authorizations"])
        self.assertEqual(cp["consulted_records"], FULL["controlling_sources"])

    def test_authored_fields_are_placeholders_not_invented(self):
        """current_state is live host facts verified AT PACKET TIME. Generating
        a plausible-looking value would be the worst possible outcome: a packet
        that reads complete while asserting unverified state."""
        self.write("01-work-order-rick-m1.yaml", FULL)
        cp = work_order.context_packet("WO-FIX-AGENT-M1-001")[0]["context_packet"]
        for field in ("goal_version", "session_id"):
            self.assertIn("<authored:", str(cp[field]))
        for v in cp["current_state"].values():
            self.assertIn("<authored:", v)
        self.assertIn("<authored:", cp["evidence_requirements"][0])

    def test_a_declared_schema_version_must_be_one_the_engine_knows(self):
        """Presence, not truthiness. `schema_version: 0` and `false` are falsy
        and were silently grandfathered as legacy; `2` is truthy and was
        silently accepted as v1."""
        for bad in (0, False, None, 2, "1"):
            wo = dict(FULL)
            wo["schema_version"] = bad
            self.write("01-work-order-rick-m1.yaml", wo)
            _, buckets, problems = work_order.load_all()
            self.assertTrue(any("WO-01" in p for p in problems),
                            "schema_version %r was accepted" % (bad,))
            self.assertEqual(buckets["structured-v1"], 0)

    def test_a_non_string_id_does_not_crash_the_engine(self):
        """A YAML list here raised "unhashable type" on the duplicate-id test
        and took down every command — the crash class the work-state engine
        shipped with."""
        for bad in ([1, 2], {"a": 1}, ""):
            wo = dict(FULL)
            wo["task_id"] = bad
            self.write("01-work-order-rick-m1.yaml", wo)
            orders, _, problems = work_order.load_all()   # must not raise
            self.assertTrue(any("WO-07" in p or "WO-02" in p for p in problems),
                            "task_id %r produced no finding" % (bad,))

    def test_deliverable_destination_must_hold_a_concrete_path(self):
        """The template ships an instruction line beside the real path, and an
        unfilled placeholder keeps its <brackets>. Both satisfy a presence check
        while giving checklist step 1 nothing to probe."""
        for bad in (["verify: ls <destination> shows the artifact before acceptance"],
                    ["<exact repo-relative path where each deliverable must land>"],
                    ["/absolute/path/outside/the/repo.md"]):
            wo = dict(FULL)
            wo["deliverable_destination"] = bad
            self.write("01-work-order-rick-m1.yaml", wo)
            self.assertIn("WO-06", self.codes())
        wo = dict(FULL)
        wo["deliverable_destination"] = [
            "pilots/PILOT-FIX-001/01-rick-thing.md",
            "verify: ls <destination> shows the artifact before acceptance"]
        self.write("01-work-order-rick-m1.yaml", wo)
        self.assertEqual(work_order.load_all()[2], [])

    def test_generating_for_an_unknown_id_is_an_error(self):
        packet, err = work_order.context_packet("WO-DOES-NOT-EXIST")
        self.assertIsNone(packet)
        self.assertIn("no work order", err)


if __name__ == "__main__":
    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(WorkOrders))
    sys.exit(0 if r.wasSuccessful() else 1)
