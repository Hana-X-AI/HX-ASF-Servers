#!/usr/bin/env python3
"""test_work_state.py — regression fixtures for the work-state engine (O1).

The five cases Phase 1 requires, plus the two real defects that motivated the
engine. Cases 1 and 2 are NOT hypothetical: they are the exact shapes that made
the previous prose parser wrong in production on 2026-08-30.

Run: python3 scripts/test_work_state.py
"""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import work_state  # noqa: E402

SCHEMA_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "governace", "goals", "work-state.schema.yaml")


def block(gid, status="in-progress", date="2026-08-30",
          auth="fixture", reconcile="none", extra=""):
    return ("```yaml work-state\n"
            "id: %s\nstatus: %s\nstatus_date: %s\nauthority: %s\nreconcile: %s\n%s"
            "```\n" % (gid, status, date, auth, reconcile, extra))


class WorkStateFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.goals = os.path.join(self.tmp, "governace", "goals")
        os.makedirs(self.goals)
        shutil.copy(SCHEMA_SRC, os.path.join(self.goals, "work-state.schema.yaml"))
        self._root, self._dir, self._schema = (
            work_state.ROOT, work_state.GOALS_DIR, work_state.SCHEMA)
        work_state.ROOT = self.tmp
        work_state.GOALS_DIR = self.goals
        work_state.SCHEMA = os.path.join(self.goals, "work-state.schema.yaml")

    def tearDown(self):
        work_state.ROOT, work_state.GOALS_DIR, work_state.SCHEMA = (
            self._root, self._dir, self._schema)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, gid, body):
        with open(os.path.join(self.goals, gid + ".md"), "w", encoding="utf-8") as fh:
            fh.write(body)

    # --- case 1: completed-with-history -------------------------------------
    def test_completed_recorded_only_in_a_correction_block(self):
        """The fleet-baseline shape. Completion lives in an append-only labeled
        correction, and the original `- Status:` line is absent or stale. The old
        prose parser returned <none> and the goal vanished from every report."""
        gid = "2026-08-27-fleet-baseline-deployment"
        self.write(gid,
                   "# Goal\n\n"
                   "[OPEN CORRECTION 2026-08-29, append-only: **Status:** COMPLETE — 2026-08-28.]\n\n"
                   + block(gid, status="complete", date="2026-08-28",
                           auth="labeled correction 2026-08-29"))
        states, problems = work_state.load_all()
        self.assertEqual(problems, [])
        self.assertEqual(dict(states)[gid]["status"], "complete")

    def test_stale_prose_line_does_not_win_over_the_block(self):
        """The hxs-3 shape: prose says in-progress, the pilot log says COMPLETE.
        The block is authoritative; prose is history."""
        gid = "2026-08-26-hxs3-muse-glimmer-tooling"
        self.write(gid,
                   "# Goal\n\n- Status: **in-progress — M0 authorized**\n\n"
                   + block(gid, status="complete", date="2026-08-27", auth="pilot state log"))
        self.assertEqual(dict(work_state.load_all()[0])[gid]["status"], "complete")

    # --- case 2: blocked ----------------------------------------------------
    def test_blocked_goal_is_selected_and_carries_its_reason(self):
        gid = "2026-08-30-blocked-example"
        self.write(gid, "# Goal\n\n" + block(gid, status="blocked",
                                             reconcile="waiting on owner word"))
        st = dict(work_state.load_all()[0])[gid]
        self.assertEqual(st["status"], "blocked")
        self.assertNotEqual(str(st["reconcile"]).lower(), "none")

    # --- case 3: malformed --------------------------------------------------
    def test_missing_block_is_a_problem_not_a_silent_unknown(self):
        gid = "2026-08-30-no-block"
        self.write(gid, "# Goal\n\n- Status: in-progress\n")
        states, problems = work_state.load_all()
        self.assertTrue(any("WS-01" in p for p in problems), problems)
        self.assertNotIn(gid, dict(states))

    def test_bad_yaml_is_reported(self):
        gid = "2026-08-30-bad-yaml"
        self.write(gid, "# Goal\n\n```yaml work-state\nid: [unclosed\n```\n")
        self.assertTrue(any("WS-01" in p for p in work_state.load_all()[1]))

    def test_status_outside_the_enum_is_rejected(self):
        gid = "2026-08-30-bad-status"
        self.write(gid, "# Goal\n\n" + block(gid, status="finished-ish"))
        self.assertTrue(any("WS-03" in p for p in work_state.load_all()[1]))

    def test_two_blocks_is_rejected(self):
        gid = "2026-08-30-two-blocks"
        self.write(gid, "# Goal\n\n" + block(gid) + "\n" + block(gid))
        self.assertTrue(any("WS-01" in p for p in work_state.load_all()[1]))

    def test_bad_status_date_is_rejected(self):
        gid = "2026-08-30-bad-date"
        self.write(gid, "# Goal\n\n" + block(gid, date="August 30"))
        self.assertTrue(any("WS-05" in p for p in work_state.load_all()[1]))

    # --- case 4: dependent / orphan -----------------------------------------
    def test_id_must_match_filename_so_a_rename_cannot_orphan_the_block(self):
        self.write("2026-08-30-renamed", "# Goal\n\n" + block("2026-08-30-old-name"))
        self.assertTrue(any("WS-04" in p for p in work_state.load_all()[1]))

    def test_evidence_paths_must_resolve(self):
        gid = "2026-08-30-dangling-evidence"
        self.write(gid, "# Goal\n\n" + block(gid, extra="evidence:\n  - servers/does-not-exist.md\n"))
        self.assertTrue(any("WS-06" in p for p in work_state.load_all()[1]))

    # --- case 5: README/_template are not goals -----------------------------
    def test_readme_and_template_are_not_treated_as_goals(self):
        self.write("README", "# Goals index\n")
        self.write("_template", "# Template\n")
        gid = "2026-08-30-real"
        self.write(gid, "# Goal\n\n" + block(gid))
        states, problems = work_state.load_all()
        self.assertEqual(problems, [])
        self.assertEqual([i for i, _ in states], [gid])


if __name__ == "__main__":
    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(WorkStateFixtures))
    sys.exit(0 if r.wasSuccessful() else 1)
