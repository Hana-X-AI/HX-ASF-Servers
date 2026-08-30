#!/usr/bin/env python3
"""test_hooks_verify.py — regression fixtures for the hook manifest check (O5).

A verifier that cannot fail is worth nothing, so every check here is proved by
introducing the drift it is meant to catch. The shim and secret-boundary cases
are the load-bearing ones: both failure modes are SILENT in production — an
unshimmed advisory hook exits 0 having matched nothing, and a credential leak
from the user-scope config would not announce itself.

Run: python3 scripts/test_hooks_verify.py
"""

import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hooks_verify  # noqa: E402

REAL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLAUDE_TEMPLATE = {
    "hooks": {
        "PreToolUse": [{"matcher": "Write|Edit|Bash", "hooks": [
            {"type": "command", "timeout": 20,
             "command": '"$D/scripts/hooks/secret-boundary.sh"'}]}],
        "PostToolUse": [{"matcher": "Write|Edit", "hooks": [
            {"type": "command", "timeout": 120,
             "command": '"$D/scripts/hooks/claude-payload-shim.sh" '
                        '"$D/scripts/hooks/validate-changed.sh"'}]}],
    }
}

KIMI_TEMPLATE = """\
[[hooks]]
event = "PreToolUse"
matcher = "Write|Edit|Bash"
command = "{root}/scripts/hooks/secret-boundary.sh"
timeout = 10

[[hooks]]
event = "PostToolUse"
matcher = "Write|Edit"
command = "{root}/scripts/hooks/validate-changed.sh"
timeout = 30

[providers.omniroute]
type = "openai"
base_url = "http://192.168.50.207:20128/v1"
api_key = "sk-NOT-A-REAL-KEY-fixture-only-000000"
"""

FAKE_CREDENTIAL = "sk-NOT-A-REAL-KEY-fixture-only-000000"


class HooksVerify(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, "scripts", "hooks"))
        os.makedirs(os.path.join(self.tmp, "governace", "hooks"))
        os.makedirs(os.path.join(self.tmp, ".claude"))
        # Real hook scripts, so the digests in the fixture manifest are real.
        for f in ("secret-boundary.sh", "validate-changed.sh", "claude-payload-shim.sh"):
            shutil.copy(os.path.join(REAL_ROOT, "scripts", "hooks", f),
                        os.path.join(self.tmp, "scripts", "hooks", f))
        with open(os.path.join(self.tmp, "scripts", "hooks", "secret-boundary.mode"),
                  "w", encoding="utf-8") as fh:
            fh.write("warn\n")

        self._saved = (hooks_verify.ROOT, hooks_verify.MANIFEST,
                       hooks_verify.CLAUDE_SETTINGS, hooks_verify.KIMI_CONFIG)
        hooks_verify.ROOT = self.tmp
        hooks_verify.MANIFEST = os.path.join(self.tmp, "governace", "hooks", "manifest.yaml")
        hooks_verify.CLAUDE_SETTINGS = os.path.join(self.tmp, ".claude", "settings.json")
        hooks_verify.KIMI_CONFIG = os.path.join(self.tmp, "kimi-config.toml")

        self.write_manifest()
        self.write_claude(CLAUDE_TEMPLATE)
        self.write_kimi(KIMI_TEMPLATE.format(root=self.tmp))

    def tearDown(self):
        (hooks_verify.ROOT, hooks_verify.MANIFEST,
         hooks_verify.CLAUDE_SETTINGS, hooks_verify.KIMI_CONFIG) = self._saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    def sha(self, rel):
        return hooks_verify._sha256(os.path.join(self.tmp, rel))

    def write_manifest(self, **over):
        man = {
            "version": 1,
            "hooks": [
                {"name": "secret-boundary", "script": "scripts/hooks/secret-boundary.sh",
                 "event": "PreToolUse", "matcher": "Write|Edit|Bash",
                 "enforcement": "enforcing", "shim": "never", "min_timeout": 10,
                 "sha256": self.sha("scripts/hooks/secret-boundary.sh"),
                 "scopes": ["claude", "kimi"]},
                {"name": "validate-changed", "script": "scripts/hooks/validate-changed.sh",
                 "event": "PostToolUse", "matcher": "Write|Edit",
                 "enforcement": "advisory", "shim": "claude-only", "min_timeout": 30,
                 "sha256": self.sha("scripts/hooks/validate-changed.sh"),
                 "scopes": ["claude", "kimi"]},
            ],
            "helpers": [
                {"name": "claude-payload-shim", "script": "scripts/hooks/claude-payload-shim.sh",
                 "sha256": self.sha("scripts/hooks/claude-payload-shim.sh")},
            ],
            "mode_files": [
                {"path": "scripts/hooks/secret-boundary.mode", "expected": "warn",
                 "sha256": self.sha("scripts/hooks/secret-boundary.mode")},
            ],
        }
        man.update(over)
        import yaml
        with open(hooks_verify.MANIFEST, "w", encoding="utf-8") as fh:
            yaml.safe_dump(man, fh, sort_keys=False)

    def write_claude(self, data):
        with open(hooks_verify.CLAUDE_SETTINGS, "w", encoding="utf-8") as fh:
            json.dump(data, fh)

    def write_kimi(self, text):
        with open(hooks_verify.KIMI_CONFIG, "w", encoding="utf-8") as fh:
            fh.write(text)

    def problems(self):
        return hooks_verify.plan()[1]

    def codes(self):
        return {p.split("]")[0].lstrip("[") for p in self.problems()}

    # --- baseline ------------------------------------------------------------
    def test_a_correct_configuration_is_clean(self):
        self.assertEqual(self.problems(), [])

    # --- the silent failures -------------------------------------------------
    def test_a_claude_hook_registered_without_the_shim_is_caught(self):
        """The worst failure mode: Claude sends tool_input.file_path, the hook
        greps for "path", matches nothing, exits 0. Indistinguishable from a
        clean run."""
        d = json.loads(json.dumps(CLAUDE_TEMPLATE))
        d["hooks"]["PostToolUse"][0]["hooks"][0]["command"] = \
            '"$D/scripts/hooks/validate-changed.sh"'
        self.write_claude(d)
        self.assertIn("HK-05", self.codes())

    def test_secret_boundary_must_not_be_shimmed(self):
        """It greps the WHOLE raw payload; the shim rewrites the payload to a
        bare {"path": ...} and would blind it."""
        d = json.loads(json.dumps(CLAUDE_TEMPLATE))
        d["hooks"]["PreToolUse"][0]["hooks"][0]["command"] = \
            '"$D/scripts/hooks/claude-payload-shim.sh" "$D/scripts/hooks/secret-boundary.sh"'
        self.write_claude(d)
        self.assertIn("HK-05", self.codes())

    # --- drift ---------------------------------------------------------------
    def test_a_declared_hook_that_is_not_registered_is_caught(self):
        d = json.loads(json.dumps(CLAUDE_TEMPLATE))
        del d["hooks"]["PostToolUse"]
        self.write_claude(d)
        self.assertIn("HK-07", self.codes())

    def test_an_undeclared_registration_is_caught(self):
        d = json.loads(json.dumps(CLAUDE_TEMPLATE))
        d["hooks"]["PostToolUse"][0]["hooks"].append(
            {"type": "command", "timeout": 30,
             "command": '"$D/scripts/hooks/rogue-hook.sh"'})
        self.write_claude(d)
        self.assertIn("HK-02", self.codes())

    def test_a_modified_hook_script_is_caught(self):
        with open(os.path.join(self.tmp, "scripts/hooks/validate-changed.sh"),
                  "a", encoding="utf-8") as fh:
            fh.write("\n# tampered\n")
        self.assertIn("HK-09", self.codes())

    def test_a_wrong_event_or_matcher_is_caught(self):
        d = json.loads(json.dumps(CLAUDE_TEMPLATE))
        d["hooks"]["PostToolUse"][0]["matcher"] = "Write"
        self.write_claude(d)
        self.assertIn("HK-04", self.codes())

    def test_a_timeout_below_the_floor_is_caught(self):
        """A hook killed mid-run looks exactly like one that found nothing."""
        d = json.loads(json.dumps(CLAUDE_TEMPLATE))
        d["hooks"]["PostToolUse"][0]["hooks"][0]["timeout"] = 5
        self.write_claude(d)
        self.assertIn("HK-06", self.codes())

    # --- the enforcement switch ---------------------------------------------
    def test_flipping_the_mode_file_is_caught(self):
        """warn -> block is the O6 graduation decision. It must not be possible
        to make it as an unnoticed one-word edit."""
        with open(os.path.join(self.tmp, "scripts/hooks/secret-boundary.mode"),
                  "w", encoding="utf-8") as fh:
            fh.write("block\n")
        self.assertTrue({"HK-11", "HK-12"} & self.codes())

    # --- user scope ----------------------------------------------------------
    def test_a_missing_user_scope_config_is_reported_not_failed(self):
        """CI has no ~/.kimi-code/config.toml and must never claim it verified
        user-scope state."""
        os.remove(hooks_verify.KIMI_CONFIG)
        summary, problems = hooks_verify.plan()
        self.assertEqual(problems, [])
        self.assertIn("not present on this machine", summary)

    def test_user_scope_drift_is_caught(self):
        self.write_kimi(KIMI_TEMPLATE.format(root=self.tmp).replace(
            'timeout = 30', 'timeout = 2'))
        self.assertIn("HK-06", self.codes())

    # --- the secret boundary -------------------------------------------------
    def test_no_credential_from_the_user_config_reaches_any_output(self):
        """~/.kimi-code/config.toml holds live provider credentials next to the
        hook blocks. The parser reads [[hooks]] only; nothing else may surface
        in a summary, a problem message, or the parsed registrations."""
        self.write_kimi(KIMI_TEMPLATE.format(root=self.tmp).replace(
            'timeout = 30', 'timeout = 2'))          # force problems to be generated
        summary, problems = hooks_verify.plan()
        blob = summary + "\n".join(problems) + json.dumps(
            hooks_verify._kimi_registrations())
        self.assertNotIn(FAKE_CREDENTIAL, blob)
        self.assertNotIn("api_key", blob)
        self.assertNotIn("base_url", blob)

    def test_provider_blocks_are_not_parsed_as_hooks(self):
        """A [providers.*] table following a [[hooks]] block must terminate it,
        or its keys would be absorbed into the previous hook."""
        regs = hooks_verify._kimi_registrations()
        self.assertEqual(len(regs), 2)
        self.assertTrue(all(r[2] and r[2].endswith(".sh") for r in regs))


if __name__ == "__main__":
    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(HooksVerify))
    sys.exit(0 if r.wasSuccessful() else 1)
