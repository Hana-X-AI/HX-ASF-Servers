#!/usr/bin/env python3
"""Regression tests for SY-8 catalog freshness and its pinned debt ledger."""

import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import yaml

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "catalog_freshness.py"
MINT = HERE / "catalog" / "carol-mint"
VALIDATE = HERE / "validate.py"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("catalog_freshness_tested", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_validate():
    spec = importlib.util.spec_from_file_location("validate_tested", VALIDATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class CatalogFreshnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.docs = self.root / "knowledge" / "catalog" / "documents"
        self.docs.mkdir(parents=True)
        self.source = self.root / "source.md"
        self.source.write_text("before\n", encoding="utf-8")
        self.record = self.docs / "DOC-one.yaml"
        self.write_record(sha(self.source))
        self.baseline_path = self.root / "governace" / "catalog-freshness-baseline.yaml"
        self.baseline_path.parent.mkdir()
        self.write_baseline()

    def tearDown(self):
        self.tmp.cleanup()

    def write_record(self, recorded_sha):
        data = {"document": {
            "id": "DOC-one",
            "canonical_location": str(self.source),
            "sha256": recorded_sha,
            "validation": {"freshness": "current"},
        }}
        self.record.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def write_baseline(self, count=1, **overrides):
        entry = {
            "id": "DOC-one",
            "canonical_location": str(self.source),
            "recorded_source_sha256": yaml.safe_load(self.record.read_text())["document"]["sha256"],
            "source_sha256_at_baseline": sha(self.source),
            "catalog_record_sha256": sha(self.record),
        }
        entry.update(overrides)
        data = {"schema_version": 1, "baseline_date": "2026-08-30",
                "count": count, "entries": [entry]}
        self.baseline_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def plan(self):
        mod = load_module()
        env = {"CAROL_MINT_ROOT": str(self.root / "knowledge" / "catalog"),
               "CAROL_MINT_REPO_ROOT": str(self.root)}
        with mock.patch.object(mod, "ROOT", str(self.root)), \
             mock.patch.object(mod, "MINT", str(MINT)), \
             mock.patch.object(mod, "BASELINE", str(self.baseline_path)), \
             mock.patch.dict(os.environ, env, clear=False):
            return mod.plan()

    def test_isolated_clean_interpreter_loads_carol_mint(self):
        proc = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), "--json"],
            cwd=HERE.parent, text=True, capture_output=True)
        self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)
        self.assertNotIn("importlib", proc.stdout + proc.stderr)
        self.assertNotIn("carol-mint unavailable", proc.stdout + proc.stderr)

    def test_baseline_entries_rejects_missing_null_and_non_lists(self):
        invalid_values = (None, {}, "", 0)
        for value in invalid_values:
            with self.subTest(entries=value):
                data = {"schema_version": 1, "baseline_date": "2026-08-30",
                        "count": 0, "entries": value}
                self.baseline_path.write_text(
                    yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
                _summary, problems = self.plan()
                self.assertTrue(any("entries must be a list" in p for p in problems))

        data = {"schema_version": 1, "baseline_date": "2026-08-30", "count": 0}
        self.baseline_path.write_text(
            yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        _summary, problems = self.plan()
        self.assertTrue(any("entries must be a list" in p for p in problems))

    def test_changed_scope_forces_governance_when_source_discovery_fails(self):
        mod = load_validate()
        real_import = __import__

        def fail_catalog_import(name, *args, **kwargs):
            if name == "catalog_freshness":
                raise ImportError("synthetic catalog discovery failure")
            return real_import(name, *args, **kwargs)

        with mock.patch("builtins.__import__", side_effect=fail_catalog_import):
            checks = mod.scoped_checks([str(VALIDATE)])
        self.assertIn(mod.check_governance_path, checks)

    def test_unchanged_known_drift_is_reported_not_failed(self):
        old = "0" * 64
        self.write_record(old)
        self.write_baseline(recorded_source_sha256=old)
        summary, problems = self.plan()
        self.assertEqual([], problems)
        self.assertIn("1 baselined", summary)

    def test_tracked_repo_sources_returns_repo_relative_path(self):
        mod = load_module()
        env = {"CAROL_MINT_ROOT": str(self.root / "knowledge" / "catalog"),
               "CAROL_MINT_REPO_ROOT": str(self.root)}
        with mock.patch.object(mod, "ROOT", str(self.root)), \
             mock.patch.object(mod, "MINT", str(MINT)), \
             mock.patch.dict(os.environ, env, clear=False):
            self.assertEqual({"source.md"}, mod.tracked_repo_sources())

    def test_source_change_after_baseline_fails(self):
        old = "0" * 64
        self.write_record(old)
        self.write_baseline(recorded_source_sha256=old)
        self.source.write_text("after\n", encoding="utf-8")
        _summary, problems = self.plan()
        self.assertTrue(any("source_sha256_at_baseline changed" in p for p in problems))

    def test_record_change_after_baseline_fails(self):
        old = "0" * 64
        self.write_record(old)
        self.write_baseline(recorded_source_sha256=old)
        with self.record.open("a", encoding="utf-8") as fh:
            fh.write("notes: changed\n")
        _summary, problems = self.plan()
        self.assertTrue(any("catalog_record_sha256 changed" in p for p in problems))

    def test_reconciled_record_requires_baseline_removal(self):
        self.write_baseline()
        _summary, problems = self.plan()
        self.assertTrue(any("record is reconciled" in p for p in problems))

    def test_baseline_count_is_graded(self):
        old = "0" * 64
        self.write_record(old)
        self.write_baseline(count=2, recorded_source_sha256=old)
        _summary, problems = self.plan()
        self.assertTrue(any("baseline count" in p for p in problems))


if __name__ == "__main__":
    unittest.main(verbosity=2)
