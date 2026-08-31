#!/usr/bin/env python3
"""test_secret_boundary.py — the evidence O6 needs before warn -> block.

`scripts/hooks/secret-boundary.mode` has said "warn" since 2026-08-25, with a
header promising graduation "after the pilot week". Nothing measured anything in
that week or the five after it. Making the one enforcing hook able to stop a
write mid-session is not a one-word edit; it is a claim about its false-positive
rate, and this suite is the evidence for that claim.

TWO IMPLEMENTATIONS, ONE CORPUS. `scripts/hooks/secret-boundary.sh` scans tool
payloads in bash; `scripts/validate.py` scans files in Python. They were written
separately and disagree on four of five patterns — validate.py is broader, is
already blocking in CI, and produced all three recorded false positives while the
hook produced none. Every case in
`governace/secret-boundary-corpus.yaml` is run against BOTH, so the two cannot
drift apart silently again.

THE COST OF A FALSE POSITIVE HERE IS NOT AN INCONVENIENCE. Twice, a false
positive forced an edit to an append-only record: DSH state-log row 5 and
PILOT-OMNIROUTE-LAYER0-001 row 40 were both de-patterned in place to clear the
gate. Row 5 records that restoring the original is not possible because it would
re-trip the scanner. A blocking scanner that flags prose does not merely annoy;
it forces governance violations.

Run: python3 scripts/test_secret_boundary.py
"""

import base64
import json
import os
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "governace", "secret-boundary-corpus.yaml")
HOOK = os.path.join(ROOT, "scripts", "hooks", "secret-boundary.sh")

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import validate  # noqa: E402


def corpus():
    with open(CORPUS, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def text_of(case):
    """Cases are base64 so this corpus does not trip the scanners it tests."""
    return base64.b64decode(case["text"]).decode("utf-8")


def validate_flags(text):
    """True when validate.py flags the text.

    This calls the REAL `_secret_scan` on a temp file rather than re-applying
    SECRET_PATTERNS here. An earlier version did the latter and silently went
    stale the moment the password rule moved out of that list — it reported a
    live credential as unflagged while the scanner caught it correctly. A test
    that reimplements the thing it tests measures the reimplementation.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(text + "\n")
        path = fh.name
    try:
        hits, _scanned = validate._secret_scan([path])
        return bool(hits)
    finally:
        os.unlink(path)


def hook_flags(text):
    """True when the hook flags a payload carrying the text.

    The hook reads a tool payload on stdin and greps the whole thing, so the
    text is embedded the way a Write would carry it.
    """
    payload = '{"tool_input": {"file_path": "note.md", "content": %s}}' % _json(text)
    proc = subprocess.run(["bash", HOOK], input=payload, text=True,
                          capture_output=True, timeout=30)
    # warn mode: exit 0 with the finding on stdout. block mode: exit 2.
    return proc.returncode == 2 or "secret-boundary" in proc.stdout.lower()


def _json(text):
    return json.dumps(text)


class SecretBoundaryCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = corpus()
        cls.cases = cls.corpus["cases"]

    def test_the_corpus_itself_contains_no_plaintext_trigger(self):
        """The corpus is base64 precisely so it does not trip the scanners it
        tests. If a case were ever added in plain text, this file would start
        failing the repo-wide sweep and someone would 'fix' it by exempting the
        file — which is how a scanner stops being trusted."""
        hits, _ = validate._secret_scan([CORPUS])
        self.assertEqual(hits, [], "plaintext trigger inside the corpus file")

    def test_real_credential_shapes_are_flagged_by_both(self):
        for case in self.cases:
            if case["verdict"] != "must_flag":
                continue
            text = text_of(case)
            with self.subTest(case=case["id"]):
                self.assertTrue(validate_flags(text),
                                "validate.py missed %s" % case["id"])
                self.assertTrue(hook_flags(text),
                                "the hook missed %s" % case["id"])

    def test_prose_about_credentials_is_flagged_by_neither(self):
        """Every one of these is a recorded incident shape or a sanitized form.
        A blocking scanner that flags them forces append-only edits."""
        for case in self.cases:
            if case["verdict"] != "must_not_flag":
                continue
            text = text_of(case)
            with self.subTest(case=case["id"]):
                self.assertFalse(validate_flags(text),
                                 "validate.py false-positives on %s: %s"
                                 % (case["id"], case["description"].strip()[:70]))
                self.assertFalse(hook_flags(text),
                                 "the hook false-positives on %s" % case["id"])

    def test_the_two_implementations_agree_on_every_case(self):
        """They were written separately and disagreed on four of five patterns.
        Parity is the property that keeps a fix to one from silently leaving the
        other behind."""
        for case in self.cases:
            text = text_of(case)
            with self.subTest(case=case["id"]):
                self.assertEqual(validate_flags(text), hook_flags(text),
                                 "implementations disagree on %s" % case["id"])

    def test_the_mode_file_still_reads_warn(self):
        """Graduation is an owner decision backed by this suite, not a side
        effect of writing it. SY-5 pins the mode file's content and digest, so
        the flip is visible; this asserts the suite has not quietly performed
        it."""
        mode = open(os.path.join(ROOT, self.corpus["mode_file"]),
                    encoding="utf-8").read().strip()
        self.assertEqual(mode, self.corpus["current_mode"])
        self.assertEqual(mode, "warn")


if __name__ == "__main__":
    r = unittest.TextTestRunner(verbosity=2).run(
        unittest.TestLoader().loadTestsFromTestCase(SecretBoundaryCorpus))
    sys.exit(0 if r.wasSuccessful() else 1)
