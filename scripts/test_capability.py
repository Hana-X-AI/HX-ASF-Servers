#!/usr/bin/env python3
"""test_capability.py — regression fixtures for the capability registry (O8).

The substring test is the one that earns its place. `_agent_mentions_hold` first
matched "hold" anywhere in a charter, and `deleted_threshold` in quinn's profile
contains it — so the check silently exonerated the exact agent it was written to
flag. A guard that reports clean because of a coincidental substring is worse
than no guard.

Run: python3 scripts/test_capability.py
"""

import os
import shutil
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capability  # noqa: E402


def cap(**over):
    base = {
        "capability": "some-mcp", "installed": False, "service_active": False,
        "advertised_to_agents": False, "approved_for_use": False,
        "owner_hold": True, "security_review": "not-started", "reconcile": "none",
    }
    base.update(over)
    return base


class Capability(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, "governace", "capabilities"))
        os.makedirs(os.path.join(self.tmp, "agents"))
        self._saved = (capability.ROOT, capability.REGISTRY, capability.AGENTS_DIR)
        capability.ROOT = self.tmp
        capability.REGISTRY = os.path.join(self.tmp, "governace", "capabilities",
                                           "registry.yaml")
        capability.AGENTS_DIR = os.path.join(self.tmp, "agents")

    def tearDown(self):
        capability.ROOT, capability.REGISTRY, capability.AGENTS_DIR = self._saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_registry(self, caps, hold=True, gates=None):
        reg = {"version": 1,
               "mcp": {"owner_hold": {"active": hold}, "capabilities": caps},
               "activation_gates": gates or [], "plugins": {"installed": []}}
        with open(capability.REGISTRY, "w", encoding="utf-8") as fh:
            yaml.safe_dump(reg, fh, sort_keys=False)

    def write_agent(self, name, charter):
        d = os.path.join(capability.AGENTS_DIR, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "charter.md"), "w", encoding="utf-8") as fh:
            fh.write(charter)
        with open(os.path.join(d, "profile.md"), "w", encoding="utf-8") as fh:
            fh.write(charter)

    def codes(self):
        return {p.split("]")[0].lstrip("[") for p in capability.plan()[1]}

    # --- invariants inside the registry: always fail -------------------------
    def test_a_held_capability_may_not_be_advertised(self):
        self.write_registry([cap(advertised_to_agents=True)])
        self.assertIn("CP-01", self.codes())

    def test_a_held_capability_may_not_be_approved(self):
        self.write_registry([cap(approved_for_use=True)])
        self.assertIn("CP-01", self.codes())

    def test_a_service_cannot_be_active_without_being_installed(self):
        self.write_registry([cap(service_active=True, owner_hold=False)])
        self.assertIn("CP-02", self.codes())

    def test_approval_is_not_a_side_effect_of_installation(self):
        self.write_registry([cap(installed=True, owner_hold=False,
                                 approved_for_use=True,
                                 security_review="not-started")])
        self.assertIn("CP-03", self.codes())

    def test_a_clean_registry_is_clean(self):
        self.write_registry([cap()])
        self.assertEqual(capability.plan()[1], [])

    # --- the substring defect ------------------------------------------------
    def test_a_word_containing_hold_does_not_count_as_mentioning_the_hold(self):
        """`deleted_threshold` contains "hold". Matching it as a hold mention
        exonerated quinn, the agent whose charter has no hold at all."""
        self.write_agent("quinn", "# quinn\n\n- **Optimizers:** deleted_threshold,\n"
                                  "  indexing_threshold, vacuum_min_vector_number\n")
        self.write_registry([cap(owning_agent="quinn")])
        self.assertIn("CP-06", self.codes())

    def test_a_real_hold_line_is_recognised(self):
        self.write_agent("chris", "# chris\n\n- **MCP surfaces — HOLD** (owner "
                                  "directive 2026-08-29): deferred.\n")
        self.write_registry([cap(owning_agent="chris")])
        self.assertNotIn("CP-06", self.codes())

    # --- external contradictions: reported only when acknowledged ------------
    def test_an_unacknowledged_contradiction_blocks(self):
        self.write_agent("quinn", "# quinn\n\nno hold language here\n")
        self.write_registry([cap(owning_agent="quinn", reconcile="none")])
        problems = capability.plan()[1]
        self.assertTrue(problems)
        self.assertTrue(all(" REPORTED " not in p for p in problems), problems)

    def test_an_acknowledged_contradiction_reports_and_does_not_block(self):
        """Deciding between two ratified records is a governor act. The tool
        surfaces the conflict; it must not hold the gate red until someone
        picks one."""
        self.write_agent("quinn", "# quinn\n\nno hold language here\n")
        self.write_registry([cap(owning_agent="quinn",
                                 reconcile="CONTRADICTION, unresolved. KDD-0017 "
                                           "carries no hold; system-mapping says "
                                           "no MCP is deployed. Governor call.")])
        problems = capability.plan()[1]
        self.assertTrue(problems)
        self.assertTrue(all(" REPORTED " in p for p in problems), problems)

    def test_the_global_hold_binds_a_capability_that_omits_its_own_field(self):
        """An owner-wide directive is not opt-out. Checking only the local
        owner_hold let a capability with the field unset be advertised while the
        global hold was active — the exact thing the hold exists to prevent."""
        c = cap(advertised_to_agents=True)
        del c["owner_hold"]
        self.write_registry([c], hold=True)
        problems = capability.plan()[1]
        self.assertTrue(any("CP-01" in p and "global" in p for p in problems), problems)

    def test_an_arbitrary_reconcile_string_cannot_silence_a_finding(self):
        """Accepting any non-"none" text turned the escape hatch into a mute
        button: one word would downgrade a blocking finding to REPORTED."""
        self.write_agent("quinn", "# quinn\n\nno hold language here\n")
        for weak in ("acknowledged", "known", "CONTRADICTION", "see above",
                     "this is a long enough sentence to pass a length check alone"):
            self.write_registry([cap(owning_agent="quinn", reconcile=weak)])
            problems = capability.plan()[1]
            self.assertTrue(any("CP-04" in p for p in problems),
                            "reconcile %r was accepted" % weak)
            self.assertTrue(any(" REPORTED " not in p for p in problems),
                            "reconcile %r silenced the finding" % weak)

    def test_a_reconcile_note_citing_a_ratified_record_is_accepted(self):
        self.write_agent("quinn", "# quinn\n\nno hold language here\n")
        self.write_registry([cap(owning_agent="quinn",
                                 reconcile="CONTRADICTION, unresolved. KDD-0017 "
                                           "carries no hold while "
                                           "servers/system-mapping.md says no MCP is "
                                           "deployed. Governor determination.")])
        problems = capability.plan()[1]
        self.assertFalse(any("CP-04" in p for p in problems), problems)
        self.assertTrue(all(" REPORTED " in p for p in problems), problems)

    def test_list_mode_reports_a_missing_registry_instead_of_crashing(self):
        """check mode reported CP-00; list mode raised FileNotFoundError on the
        same condition."""
        import contextlib
        import io as _io
        if os.path.isfile(capability.REGISTRY):
            os.remove(capability.REGISTRY)
        buf = _io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = capability.main(["list"])      # must not raise
        self.assertEqual(rc, 1)
        self.assertIn("CP-00", buf.getvalue())

    def test_an_unregistered_owning_agent_is_caught(self):
        self.write_registry([cap(owning_agent="sage")])
        self.assertIn("CP-05", self.codes())


if __name__ == "__main__":
    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(Capability))
    sys.exit(0 if r.wasSuccessful() else 1)
