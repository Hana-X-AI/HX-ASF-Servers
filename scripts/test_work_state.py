#!/usr/bin/env python3
"""test_work_state.py — regression fixtures for the work-state engine (O1).

The five cases Phase 1 requires, plus the two real defects that motivated the
engine. Cases 1 and 2 are NOT hypothetical: they are the exact shapes that made
the previous prose parser wrong in production on 2026-08-30.

Run: python3 scripts/test_work_state.py
"""

import json
import os
import re
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


class _GoalTree(unittest.TestCase):
    """Fixture plumbing: a throwaway goals/ tree with the real schema."""

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


class WorkStateFixtures(_GoalTree):
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

    def test_prose_current_status_newer_than_block_is_flagged(self):
        """WS-07: a labeled [current] status declaration newer than the block's
        status_date means the block was not advanced with the prose (the hxs-2
        and fleet-baseline silent-drift shape, corrected 2026-08-31)."""
        gid = "2026-08-31-stale-block-example"
        self.write(gid,
                   "# Goal\n\n"
                   "[Status transition 2026-08-30 [current]: COMPLETE — done.]\n\n"
                   + block(gid, status="in-progress", date="2026-08-27"))
        states, problems = work_state.load_all()
        self.assertIn(gid, dict(states))
        self.assertTrue(any(p.startswith("[WS-07]") for p in problems))

    def test_prose_current_status_not_newer_is_not_flagged(self):
        """The block is fresh (status_date equals the latest prose declaration):
        no WS-07."""
        gid = "2026-08-31-fresh-block-example"
        self.write(gid,
                   "# Goal\n\n"
                   "[Status transition 2026-08-30 [current]: COMPLETE — done.]\n\n"
                   + block(gid, status="complete", date="2026-08-30"))
        states, problems = work_state.load_all()
        self.assertIn(gid, dict(states))
        self.assertEqual(problems, [])

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


# --- case 6: the CLI layer ---------------------------------------------------
# Everything above exercises load_all(). Nothing exercised main(), so two live
# defects shipped green: every --json command crashed on a date, and `standup`
# silently dropped `draft` goals. Output formatting is part of the contract —
# a status report that omits a goal is the defect this engine exists to prevent.
class WorkStateCLI(_GoalTree):
    def run_cmd(self, *argv):
        """Invoke main() and capture stdout, as a caller would."""
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = work_state.main(list(argv))
        return rc, buf.getvalue()

    def seed(self):
        """One goal per enum status, so no command sees an empty set —
        `--json` only ever crashed on a NON-empty result."""
        for i, st in enumerate(["draft", "approved", "in-progress", "blocked",
                                "done", "complete", "abandoned"]):
            gid = "2026-08-%02d-%s" % (i + 1, st)
            self.write(gid, "# Goal\n\n" + block(gid, status=st))

    def test_json_survives_an_unquoted_status_date(self):
        """`status_date: 2026-08-28` is unquoted in every real goal file, so
        yaml.safe_load returns datetime.date. json.dumps raised TypeError and
        every --json command exited non-zero with a traceback."""
        gid = "2026-08-28-unquoted-date"
        self.write(gid, "# Goal\n\n" + block(gid, date="2026-08-28"))
        data, err = work_state.parse(os.path.join(self.goals, gid + ".md"))
        self.assertIsNone(err)
        self.assertIsInstance(data["status_date"], str)  # normalized at parse
        for cmd in ("status", "in-progress", "standup"):
            rc, out = self.run_cmd(cmd, "--json")
            self.assertEqual(rc, 0, cmd)
            json.loads(out)  # must parse, not merely not crash

    def test_every_command_emits_valid_json(self):
        self.seed()
        for cmd in ("status", "in-progress", "next", "blocked", "reconcile", "standup"):
            rc, out = self.run_cmd(cmd, "--json")
            self.assertEqual(rc, 0, cmd)
            self.assertTrue(json.loads(out) or True, cmd)

    def test_standup_accounts_for_every_goal(self):
        """The header promises a total; the groups must list that many. `draft`
        had no group, so a 10-goal standup listed 8 and reported nothing."""
        self.seed()
        _, out = self.run_cmd("standup")
        total = int(re.search(r"Daily standup — (\d+) goals", out).group(1))
        listed = len(re.findall(r"^   \S+\s{2,}\S+$", out, re.M))
        self.assertEqual(total, 7)
        self.assertEqual(listed, total)

    def test_a_status_with_no_group_is_surfaced_not_dropped(self):
        """Guards the fix itself: if the schema gains a status and standup gains
        no group for it, the goal must appear under Ungrouped."""
        self.seed()
        orig = work_state._schema

        def patched():
            sch = orig()
            sch["fields"]["status"]["enum"] = list(sch["fields"]["status"]["enum"]) + ["parked"]
            return sch
        work_state._schema = patched
        try:
            gid = "2026-08-30-parked"
            self.write(gid, "# Goal\n\n" + block(gid, status="parked"))
            _, out = self.run_cmd("standup")
            self.assertIn("Ungrouped (1)", out)
            self.assertIn(gid, out)
        finally:
            work_state._schema = orig

    def test_standup_json_shows_everything_the_text_view_shows(self):
        """Parity, not just correctness. The first fix repaired the TEXT view and
        was tested only there, so the JSON branch kept both defects: it dropped
        ungrouped rows AND the reconcile queue. A consumer rendering a standup
        from --json would have silently lost the governor's decision items —
        the same "visible in one view, invisible in another" failure the text
        fix addressed. Both views are computed once and must agree."""
        self.seed()
        gid = "2026-08-31-needs-a-call"
        self.write(gid, "# Goal\n\n" + block(gid, status="in-progress",
                                             reconcile="pilot log says complete; governor to decide"))
        _, out = self.run_cmd("standup", "--json")
        d = json.loads(out)
        grouped = sum(len(v) for v in d["groups"].values())
        self.assertEqual(grouped + len(d["ungrouped"]), d["total"])
        self.assertEqual(d["total"], 8)
        # the reconcile queue reaches JSON consumers, not only readers
        self.assertEqual([r["id"] for r in d["reconcile"]], [gid])
        # empty keys are present, so absence never has to be inferred
        _, out2 = self.run_cmd("standup", "--json")
        self.assertIn("ungrouped", json.loads(out2))

    def test_a_malformed_block_does_not_take_down_the_report(self):
        """load_all() retains schema-invalid records so validate.py sees every
        problem — but the rendering layer compared/counted them anyway. A block
        with no `status` raised KeyError and a list-valued `status` raised
        "TypeError: unhashable type", so ONE malformed goal killed every status
        command with a traceback: the whole report silenced by one bad file."""
        self.seed()
        self.write("2026-08-30-no-status",
                   "# Goal\n\n```yaml work-state\nid: 2026-08-30-no-status\n"
                   "status_date: 2026-08-30\nauthority: f\nreconcile: none\n```\n")
        self.write("2026-08-30-list-status",
                   "# Goal\n\n```yaml work-state\nid: 2026-08-30-list-status\n"
                   "status: []\nstatus_date: 2026-08-30\nauthority: f\nreconcile: none\n```\n")
        for cmd in ("status", "standup", "in-progress", "next", "blocked", "reconcile"):
            rc, _ = self.run_cmd(cmd)
            self.assertEqual(rc, 0, "%s crashed on a malformed block" % cmd)
        _, out = self.run_cmd("standup", "--json")
        d = json.loads(out)
        self.assertEqual(len(d["excluded"]), 2)
        self.assertEqual(d["total"], 7)  # the seven well-formed goals still report

    def test_exclusion_is_narrow_and_does_not_hide_a_renderable_goal(self):
        """Guards against over-correcting the fix above. A goal whose only
        problem is a dangling evidence path is still renderable and MUST stay
        in the report — dropping every goal that has any problem would recreate
        the invisible-goal defect from the other direction."""
        gid = "2026-08-30-dangling-but-renderable"
        self.write(gid, "# Goal\n\n" + block(gid, status="in-progress",
                                             extra="evidence:\n  - servers/nope.md\n"))
        self.assertTrue(any("WS-06" in p for p in work_state.load_all()[1]))
        _, out = self.run_cmd("in-progress")
        self.assertIn(gid, out)
        _, sj = self.run_cmd("standup", "--json")
        self.assertEqual(json.loads(sj)["excluded"], [])

    def test_unknown_command_exits_2(self):
        rc, _ = self.run_cmd("nonsense")
        self.assertEqual(rc, 2)

    def test_check_reports_and_fails_on_a_bad_goal(self):
        self.write("2026-08-30-broken", "# Goal\n\nno block here\n")
        rc, out = self.run_cmd("--check")
        self.assertEqual(rc, 1)
        self.assertIn("WS-01", out)


if __name__ == "__main__":
    load = unittest.TestLoader().loadTestsFromTestCase
    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestSuite([load(WorkStateFixtures), load(WorkStateCLI)]))
    sys.exit(0 if r.wasSuccessful() else 1)
