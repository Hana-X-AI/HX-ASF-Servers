#!/usr/bin/env python3
"""Local regression tests for the fixture harness — stdlib unittest, no network/API.

Covers the concrete review defects F1-F4 (run from this directory:
`python3 test_fixtures.py`), the 2026-08-25 review-batch findings 1-8
(classes TestB1-TestB7), and the 2026-08-25 model-profile/retired-alias fixer
batch (classes TestC1-TestC6; urlopen/monotonic/subprocess are faked, no model,
no sudo, and no live server needed — the model-alias preflight is served by a
fake /api/tags).
The sandboxed execution path (F6) is exercised separately at run time; it
needs sudo and is not part of this suite.
"""
import contextlib
import hashlib
import io
import json
import os
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bench
import bench_m6
import probes
import rag_suite
# rag_suite re-pins its own versioned dir at import; tool_suite still prepends the stale
# /tmp/esme-m5b/harness. Re-pin HERE after each so every fixture under test (and any later
# import in this process) resolves to the versioned copy in this directory.
sys.path.insert(0, HERE)
import tool_suite
sys.path.insert(0, HERE)
import coding_suite
sys.path.insert(0, HERE)
import fixtures_corpus

for _mod in (bench, bench_m6, probes, rag_suite, tool_suite, coding_suite, fixtures_corpus):
    assert os.path.dirname(os.path.abspath(_mod.__file__)) == HERE, \
        f"{_mod.__name__} imported from {_mod.__file__}, expected {HERE}"


class TestF1TrialKeys(unittest.TestCase):
    """F1: near-identical prefill targets must not collide in out['trials']."""

    def test_near_targets_produce_distinct_keys(self):
        self.assertNotEqual(bench_m6.trial_label(64000), bench_m6.trial_label(64500))

    def test_key_carries_exact_target(self):
        self.assertEqual(bench_m6.trial_label(64000), "prefill_64000")
        self.assertIn("64500", bench_m6.trial_label(64500))

    def test_old_scheme_would_have_collided(self):
        # regression guard: the fixed keys must differ where t // 1000 is equal
        self.assertEqual(64000 // 1000, 64500 // 1000)
        self.assertNotEqual(bench_m6.trial_label(64000), bench_m6.trial_label(64500))


class TestF2OneShotClassification(unittest.TestCase):
    """F2: a bare HTTP-200 one-shot is never HONORED for think levels."""

    def test_http200_is_accepted_unestablished(self):
        cls, grad = probes.classify_one_shot(200)
        self.assertEqual(cls, "ACCEPTED")
        self.assertEqual(grad, "UNESTABLISHED")
        self.assertNotEqual(cls, "HONORED")

    def test_non_200_is_rejected(self):
        for code in (400, 404, 500):
            cls, grad = probes.classify_one_shot(code)
            self.assertEqual(cls, "REJECTED")
            self.assertNotEqual(cls, "HONORED")


class TestF3HandledCondition(unittest.TestCase):
    """F3: handled requires fixture validity AND done_reason stop AND a passing grade."""

    def test_all_three_conditions_required(self):
        self.assertTrue(rag_suite.q16_handled(True, "stop", True))
        self.assertFalse(rag_suite.q16_handled(False, "stop", True))   # bad fixture
        self.assertFalse(rag_suite.q16_handled(True, "length", True))  # not a clean stop
        self.assertFalse(rag_suite.q16_handled(True, None, True))      # missing done_reason
        self.assertFalse(rag_suite.q16_handled(True, "stop", False))   # failed grade


class TestF4NonDictArgs(unittest.TestCase):
    """F4: validate() must deny non-dict args, not raise on dict methods."""

    def setUp(self):
        # keep audit writes local: run_tool() appends to the module audit JSONL
        self._tmp = tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False)
        self._tmp.close()
        self._orig = tool_suite.AUDIT_PATH
        tool_suite.AUDIT_PATH = self._tmp.name

    def tearDown(self):
        tool_suite.AUDIT_PATH = self._orig
    def test_non_dict_args_denied_not_raised(self):
        for bad in (["host", "hxs-2"], "host=hxs-2", 42, None, True):
            err = tool_suite.validate("get_fleet_metric", bad)
            self.assertIsInstance(err, str, f"expected denial string for {bad!r}")

    def test_denial_flows_through_run_tool_format(self):
        decision, result = tool_suite.run_tool("TEST-F4", "get_fleet_metric", ["not", "a", "dict"])
        self.assertEqual(decision, "denied")
        self.assertFalse(result["ok"])
        self.assertIn("DENIED by validation:", result["error"])

    def test_dict_checks_preserved(self):
        self.assertIsNone(tool_suite.validate(
            "get_fleet_metric", {"host": "hxs-2", "metric": "cpu_load"}))
        self.assertIn("missing required argument",
                      tool_suite.validate("get_fleet_metric", {"host": "hxs-2"}))
        self.assertIn("must be a string",
                      tool_suite.validate("get_fleet_metric", {"host": 42, "metric": "cpu_load"}))
        self.assertIn("unknown property",
                      tool_suite.validate("get_fleet_metric",
                                          {"host": "hxs-2", "metric": "cpu_load", "admin": True}))
        self.assertIn("not in enum",
                      tool_suite.validate("get_fleet_metric", {"host": "hxs-9", "metric": "cpu_load"}))


# ---------------- fakes for the 2026-08-25 review-batch regression tests ----------------


class _Clock:
    """Controllable monotonic clock for the stream-deadline tests."""

    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


class _FakeHTTP:
    """Stand-in for a urllib response: iterates byte lines (streaming chat) and provides
    read() (one-shot posts). Optionally advances a _Clock by dt per yielded line."""

    def __init__(self, lines=(), payload=b"{}", clock=None, dt=0.0):
        self._lines, self._payload, self._clock, self._dt = list(lines), payload, clock, dt

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def __iter__(self):
        for ln in self._lines:
            if self._clock is not None:
                self._clock.t += self._dt
            yield ln

    def read(self):
        return self._payload


def _chunk(thinking=None, content=None, done=False, **extra):
    c = {"message": {}}
    if thinking:
        c["message"]["thinking"] = thinking
    if content:
        c["message"]["content"] = content
    if done:
        c["done"] = True
    c.update(extra)
    return (json.dumps(c) + "\n").encode()


DONE = dict(done=True, prompt_eval_count=10, prompt_eval_duration=2_000_000_000,
            eval_count=5, eval_duration=1_000_000_000, done_reason="stop",
            load_duration=500_000_000)


def _tags_dispatch(names, chat_payload):
    """urlopen side_effect: serves /api/tags with the given model names (the fixtures
    preflight-verify the requested model profile alias there first) and answers every
    other request with the given chat payload."""
    def _open(req, timeout=None):
        url = req if isinstance(req, str) else getattr(req, "full_url", "")
        if url.endswith("/api/tags"):
            return _FakeHTTP(payload=json.dumps({"models": [{"name": n} for n in names]}).encode())
        return _FakeHTTP(payload=json.dumps(chat_payload).encode())
    return _open


def _read(name):
    with open(os.path.join(HERE, name)) as f:
        return f.read()


class TestB1TerminalDoneGuard(unittest.TestCase):
    """Findings 1-2: a stream with no terminal done chunk fails the trial instead of
    returning null-derived benchmark evidence; the metrics path is preserved otherwise."""

    def setUp(self):
        # stream_chat reads the module-global MODEL that main() sets from the required
        # argv alias; the faked urlopen never inspects the request body.
        bench.MODEL = bench_m6.MODEL = "test-model"

    def test_bench_raises_without_done_chunk(self):
        fake = _FakeHTTP([_chunk(thinking="hmm"), _chunk(content="answer")])
        with mock.patch("urllib.request.urlopen", return_value=fake):
            with self.assertRaises(RuntimeError):
                bench.stream_chat("p")

    def test_bench_m6_raises_without_done_chunk(self):
        fake = _FakeHTTP([_chunk(content="answer")])
        with mock.patch("urllib.request.urlopen", return_value=fake):
            with self.assertRaises(RuntimeError):
                bench_m6.stream_chat("p")

    def test_metrics_preserved_with_done_chunk(self):
        fake = _FakeHTTP([_chunk(thinking="hmm"), _chunk(content="answer"), _chunk(**DONE)])
        with mock.patch("urllib.request.urlopen", return_value=fake):
            r = bench.stream_chat("p")
        self.assertEqual(r["prompt_eval_count"], 10)
        self.assertEqual(r["eval_count"], 5)
        self.assertEqual(r["done_reason"], "stop")
        self.assertEqual(r["prefill_tok_s"], 5.0)
        self.assertEqual(r["gen_tok_s"], 5.0)
        self.assertIsNotNone(r["ttft_thinking_s"])
        self.assertIsNotNone(r["ttft_content_s"])
        self.assertEqual((r["thinking_chars"], r["content_chars"]), (3, 6))


class TestB2FirstContentDeadline(unittest.TestCase):
    """Finding 2: bench_m6 fails the trial when first content arrives after the ratified
    240 s deadline (plan 6.1), while content within the deadline keeps the metrics path."""

    def setUp(self):
        bench_m6.MODEL = "test-model"  # see TestB1.setUp

    def test_deadline_exceeded_fails_trial(self):
        clock = _Clock()  # thinking-only chunks 100 s apart: elapsed passes 240 s
        fake = _FakeHTTP([_chunk(thinking="a"), _chunk(thinking="b"), _chunk(thinking="c")],
                         clock=clock, dt=100.0)
        with mock.patch("urllib.request.urlopen", return_value=fake), \
                mock.patch("time.monotonic", clock):
            with self.assertRaisesRegex(RuntimeError, "240"):
                bench_m6.stream_chat("p")

    def test_content_within_deadline_passes(self):
        clock = _Clock()
        fake = _FakeHTTP([_chunk(thinking="a"), _chunk(content="hi"), _chunk(**DONE)],
                         clock=clock, dt=10.0)
        with mock.patch("urllib.request.urlopen", return_value=fake), \
                mock.patch("time.monotonic", clock):
            r = bench_m6.stream_chat("p")
        self.assertEqual(r["done_reason"], "stop")
        self.assertEqual(r["ttft_content_s"], 20.0)
        self.assertEqual(r["prompt_eval_count"], 10)


class TestB3NeedleProbeAcceptance(unittest.TestCase):
    """Finding 3: needle_probe computes an explicit pass (fixture_valid AND stop AND
    needle_found) and exits nonzero when any acceptance condition fails."""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.outpath = os.path.join(self._td.name, "needle.json")

    def tearDown(self):
        self._td.cleanup()
        while "/tmp/esme-m6/harness" in sys.path:  # probe prepends its stale scratch dir
            sys.path.remove("/tmp/esme-m6/harness")

    def _payload(self, **over):
        p = {"message": {"content": "The authorization code is FALCON-61803.",
                         "thinking": "hidden"},
             "prompt_eval_count": 30000, "prompt_eval_duration": 2_000_000_000,
             "eval_count": 12, "done_reason": "stop", "total_duration": 3_000_000_000}
        p.update(over)
        return p

    def _run_probe(self, payload, alias="hx-qwen3.8-27b-64k"):
        # MODEL is a required trailing argv since the bare-alias retirement; the faked
        # /api/tags endpoint lists it so the preflight accepts it.
        argv = ["needle_probe.py", "1150", "748", "28000", "32600", self.outpath, alias]
        code = None  # stays None if the probe never exits = acceptance not enforced
        with mock.patch.object(sys, "argv", argv), \
                mock.patch("urllib.request.urlopen", side_effect=_tags_dispatch([alias], payload)), \
                contextlib.redirect_stdout(io.StringIO()):
            try:
                runpy.run_path(os.path.join(HERE, "needle_probe.py"), run_name="__main__")
            except SystemExit as e:
                code = e.code
        with open(self.outpath) as f:
            return code, json.load(f)

    def test_all_conditions_met_passes_and_exits_zero(self):
        code, result = self._run_probe(self._payload())
        self.assertEqual(code, 0)
        self.assertIs(result["pass"], True)
        self.assertEqual(result["model"], "hx-qwen3.8-27b-64k")  # selected alias recorded
        # existing diagnostic fields preserved
        for k in ("fixture_valid", "window", "needle_found", "thinking_present",
                  "thinking_chars", "prefill_tok_s", "answer"):
            self.assertIn(k, result)
        self.assertIs(result["fixture_valid"], True)
        self.assertIs(result["needle_found"], True)

    def test_non_stop_done_reason_fails(self):
        code, result = self._run_probe(self._payload(done_reason="length"))
        self.assertEqual(code, 1)
        self.assertIs(result["pass"], False)
        self.assertIs(result["fixture_valid"], True)  # diagnostics still recorded

    def test_needle_missing_fails(self):
        code, result = self._run_probe(self._payload(
            message={"content": "I could not locate the code.", "thinking": ""}))
        self.assertEqual(code, 1)
        self.assertIs(result["pass"], False)
        self.assertIs(result["needle_found"], False)

    def test_invalid_fixture_window_fails(self):
        code, result = self._run_probe(self._payload(prompt_eval_count=5000))
        self.assertEqual(code, 1)
        self.assertIs(result["pass"], False)
        self.assertIs(result["fixture_valid"], False)


class TestB4ChatmetaThinkStrip(unittest.TestCase):
    """Finding 4: chatmeta never persists think-tagged reasoning; the boolean
    think-present flag and the count metadata the RC probes rely on are preserved."""

    def test_think_span_stripped_flag_recorded(self):
        resp = {"message": {"content": "visible <think>secret chain</think> answer",
                            "thinking": "hidden"},
                "eval_count": 3, "prompt_eval_count": 9, "done_reason": "stop",
                "total_duration": 1_000_000_000}
        m = probes.chatmeta(resp)
        self.assertNotIn("secret", m["content"])
        self.assertEqual(m["content"], "visible  answer")
        self.assertTrue(m["content_has_think_tag"])
        self.assertTrue(m["thinking_present"])
        self.assertEqual(m["thinking_chars"], 6)
        self.assertEqual(m["done_reason"], "stop")

    def test_unterminated_think_tail_dropped(self):
        m = probes.chatmeta({"message": {"content": "partial <think>reasoning tail"}})
        self.assertEqual(m["content"], "partial")
        self.assertTrue(m["content_has_think_tag"])

    def test_tag_free_content_unchanged(self):
        m = probes.chatmeta({"message": {"content": "  391  "}, "eval_count": 1})
        self.assertEqual(m["content"], "  391  ")
        self.assertFalse(m["content_has_think_tag"])


class TestB5Q16RegradeGate(unittest.TestCase):
    """Finding 5: the regrade keeps Q16's fixture-validity gate — Q16 handled only when
    grade() passes AND stored prompt_eval_count is in-window AND done_reason == stop;
    other cases keep frozen-citation grading only. Runs the real script with a faked API
    and a crafted rag-cases.json; pre-existing evidence files are restored afterwards."""

    EV_DIR = "/tmp/esme-m5b/evidence"
    FILES = ("rag-cases.json", "q16-rerun.json")

    def setUp(self):
        os.makedirs(self.EV_DIR, exist_ok=True)
        self._backup = {}
        for name in self.FILES:
            p = os.path.join(self.EV_DIR, name)
            self._backup[p] = None
            if os.path.exists(p):
                with open(p, "rb") as f:
                    self._backup[p] = f.read()

    def tearDown(self):
        for p, data in self._backup.items():
            if data is None:
                if os.path.exists(p):
                    os.remove(p)
            else:
                with open(p, "wb") as f:
                    f.write(data)

    def test_regrade_applies_q16_gate_only(self):
        cases = [
            # grade now ALSO fails (no recognized source citation since the Q16 citation
            # gate), and the stored fixture is invalid (oversized) and not a clean stop
            {"qid": "Q16", "type": "boundary", "handled": True,
             "answer": "The code is FALCON-61803.", "citations": [],
             "prompt_eval_count": 318433, "done_reason": "length"},
            # grade passes ([NEEDLE] cited) AND fixture valid AND clean stop -> stays handled
            {"qid": "Q16", "type": "boundary", "handled": False,
             "answer": "The code is FALCON-61803 [NEEDLE].", "citations": ["[NEEDLE]"],
             "prompt_eval_count": 30000, "done_reason": "stop"},
            # non-Q16: frozen-citation grade only, no fixture gate (bad pec/stop tolerated)
            {"qid": "Q01", "type": "factual", "handled": False,
             "answer": "An alert fires at 500 ms drift [HXDOC-01].",
             "citations": ["[HXDOC-01]"], "prompt_eval_count": 999, "done_reason": "length"},
        ]
        rag_path = os.path.join(self.EV_DIR, "rag-cases.json")
        with open(rag_path, "w") as f:
            json.dump({"cases": cases}, f)
        payload = {"message": {"content": "The authorization code is FALCON-61803 [NEEDLE].",
                               "thinking": "x"},
                   "prompt_eval_count": 30000, "done_reason": "stop",
                   "eval_count": 5, "total_duration": 1_000_000_000}
        alias = "hx-qwen3.8-27b-64k"
        with mock.patch.object(sys, "argv", ["q16_rerun.py", alias]), \
                mock.patch("urllib.request.urlopen", side_effect=_tags_dispatch([alias], payload)), \
                contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(os.path.join(HERE, "q16_rerun.py"), run_name="__main__")
        with open(rag_path) as f:
            d = json.load(f)
        self.assertIs(d["cases"][0]["handled"], False)  # gate: invalid fixture + no stop
        self.assertIs(d["cases"][1]["handled"], True)   # gate: all three conditions met
        self.assertIs(d["cases"][2]["handled"], True)   # non-Q16: grade-only, unchanged
        with open(os.path.join(self.EV_DIR, "q16-rerun.json")) as f:
            rerun = json.load(f)
        self.assertEqual(rerun["model"], alias)  # selected alias recorded
        self.assertNotIn("<think>", rerun["answer"])  # think content never persisted


class TestB6EvidenceDirGuards(unittest.TestCase):
    """Findings 6(c)/7: evidence parent directories are created before writes, so the
    suites also run on a host where /tmp/esme-m5b/evidence does not exist yet."""

    def test_audit_creates_parent_dir(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "sub", "audit.jsonl")
            orig = tool_suite.AUDIT_PATH
            tool_suite.AUDIT_PATH = path
            try:
                tool_suite.audit({"event": "test"})
            finally:
                tool_suite.AUDIT_PATH = orig
            self.assertTrue(os.path.exists(path))

    def test_main_flow_guards_precede_writes(self):
        # no-network guard: the makedirs call must precede the cases-file write
        src = _read("rag_suite.py")
        self.assertLess(src.index('os.makedirs("/tmp/esme-m5b/evidence", exist_ok=True)'),
                        src.index('rag-cases.json", "w"'))
        src = _read("tool_suite.py")
        self.assertLess(src.index('os.makedirs("/tmp/esme-m5b/evidence", exist_ok=True)'),
                        src.index('tool-cases.json", "w"'))


class TestB7SchemaConformance(unittest.TestCase):
    """Finding 8: schema_conformance is measured from the recorded audit events
    (validation denials, unexpected executions), not a fixed 100% claim."""

    def _ex(self, tool, **args):
        return {"event": "executed", "tool": tool, "args": args}

    def test_all_conforming_is_100(self):
        executed = [self._ex("get_fleet_metric", host="hxs-2", metric="cpu_load"),
                    self._ex("restart_fleet_service", host="hxs-5", service="testsvc")]
        denied = [{"event": "deny", "tool": "delete_all_data", "args": {}}]
        pct, violations = tool_suite.schema_conformance(executed, denied)
        self.assertEqual((pct, violations), (100.0, 0))

    def test_forbidden_execution_measured(self):
        executed = [self._ex("get_fleet_metric", host="hxs-2", metric="cpu_load"),
                    self._ex("get_fleet_metric", host="hxs-3", metric="cpu_load"),
                    self._ex("restart_fleet_service", host="hxs-1", service="ollama")]
        denied = [{"event": "deny", "tool": "get_fleet_metric", "args": {}}]
        pct, violations = tool_suite.schema_conformance(executed, denied)
        self.assertEqual((pct, violations), (75.0, 1))

    def test_undeclared_tool_execution_counts(self):
        pct, violations = tool_suite.schema_conformance([self._ex("delete_all_data")], [])
        self.assertEqual((pct, violations), (0.0, 1))

    def test_empty_log_is_vacuously_conformant(self):
        self.assertEqual(tool_suite.schema_conformance([], []), (100.0, 0))

    def test_no_fixed_conformance_claim_remains(self):
        self.assertNotIn("100% (strict validation precedes every execution)",
                         _read("tool_suite.py"))


class TestC1ModelAlias(unittest.TestCase):
    """2026-08-25 finding 1 (batch-critical): the bare hx-qwen3.8-27b alias is retired.
    Every fixture requires an explicit model profile alias per run (usage error when
    missing, no silent default) and preflight-verifies it against /api/tags, failing
    fast with a clear message; the selected alias is recorded in the JSON outputs."""

    ALIAS = "hx-qwen3.8-27b-64k"

    def test_require_model_returns_listed_alias(self):
        with mock.patch("urllib.request.urlopen", side_effect=_tags_dispatch([self.ALIAS], {})):
            self.assertEqual(fixtures_corpus.require_model(self.ALIAS), self.ALIAS)

    def test_require_model_accepts_latest_tag_form(self):
        with mock.patch("urllib.request.urlopen",
                        side_effect=_tags_dispatch([self.ALIAS + ":latest"], {})):
            self.assertEqual(fixtures_corpus.require_model(self.ALIAS), self.ALIAS)

    def test_require_model_rejects_unlisted_alias(self):
        with mock.patch("urllib.request.urlopen", side_effect=_tags_dispatch([self.ALIAS], {})):
            with self.assertRaises(SystemExit) as cm:
                fixtures_corpus.require_model("hx-qwen3.8-27b")
        self.assertIn("hx-qwen3.8-27b", str(cm.exception.code))
        self.assertIn(self.ALIAS, str(cm.exception.code))  # available aliases listed

    def test_require_model_unreachable_server_fails_fast(self):
        with mock.patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
            with self.assertRaises(SystemExit) as cm:
                fixtures_corpus.require_model(self.ALIAS)
        self.assertIn("preflight failed", str(cm.exception.code))

    def test_usage_error_when_alias_missing(self):
        for mod in (bench, bench_m6, probes, rag_suite, tool_suite, coding_suite):
            for argv in ([mod.__name__], ["bench_m6.py", "out.json"] if mod is bench_m6 else None):
                if argv is None:
                    continue
                with mock.patch.object(sys, "argv", argv), \
                        self.assertRaises(SystemExit, msg=f"{mod.__name__} argv={argv}") as cm:
                    mod.main()
                self.assertIn("usage", str(cm.exception.code))

    def test_usage_error_script_fixtures(self):
        for name, argv in (("needle_probe.py", ["needle_probe.py", "1150", "748", "28000", "32600", "x.json"]),
                           ("q16_rerun.py", ["q16_rerun.py"])):
            with mock.patch.object(sys, "argv", argv), \
                    contextlib.redirect_stderr(io.StringIO()), \
                    self.assertRaises(SystemExit, msg=name) as cm:
                runpy.run_path(os.path.join(HERE, name), run_name="__main__")
            self.assertIn("usage", str(cm.exception.code))

    def test_retired_bare_alias_not_hard_coded(self):
        for name in ("bench.py", "bench_m6.py", "coding_suite.py", "needle_probe.py",
                     "probes.py", "q16_rerun.py", "rag_suite.py", "tool_suite.py"):
            self.assertNotIn('MODEL = "hx-qwen3.8-27b"', _read(name), name)


class TestC2LateFirstContent(unittest.TestCase):
    """2026-08-25 finding 2: the first-content deadline is evaluated BEFORE accepting
    content — a FIRST content chunk arriving after 240 s fails the trial (the batch-5
    ordering only raised on non-content chunks and would have accepted it)."""

    def setUp(self):
        bench_m6.MODEL = "test-model"  # see TestB1.setUp

    def test_late_first_content_fails_trial(self):
        clock = _Clock()  # chunks processed at t=150 (thinking) and t=300 (content)
        fake = _FakeHTTP([_chunk(thinking="a"), _chunk(content="late"), _chunk(**DONE)],
                         clock=clock, dt=150.0)
        with mock.patch("urllib.request.urlopen", return_value=fake), \
                mock.patch("time.monotonic", clock):
            with self.assertRaisesRegex(RuntimeError, "240"):
                bench_m6.stream_chat("p")


class TestC3Teardown(unittest.TestCase):
    """2026-08-25 finding 3: teardown reaches root/nobody-owned sandbox processes via
    non-interactive sudo, tolerates already-exited targets, bounds the recovery drain,
    and keeps the batch-4 FAIL-CLOSED sandbox gate."""

    def test_kill_tree_escalates_through_sudo_n(self):
        with mock.patch.object(coding_suite, "_descendants", return_value=[4242, 4243]), \
                mock.patch("os.killpg", side_effect=PermissionError), \
                mock.patch("os.kill", side_effect=PermissionError), \
                mock.patch("subprocess.run") as run:
            coding_suite._kill_tree(mock.Mock(pid=999))
        cmd = run.call_args[0][0]
        self.assertEqual(cmd[:4], ["sudo", "-n", "kill", "-9"])  # -n: never prompts
        self.assertIn("-999", cmd)   # process group escalated as negative pid
        self.assertIn("4242", cmd)
        self.assertIn("4243", cmd)
        self.assertIs(run.call_args[1]["check"], False)  # nonzero exit tolerated
        self.assertIn("timeout", run.call_args[1])       # escalation itself bounded

    def test_kill_tree_tolerates_already_exited(self):
        with mock.patch.object(coding_suite, "_descendants", return_value=[4242]), \
                mock.patch("os.killpg", side_effect=ProcessLookupError), \
                mock.patch("os.kill", side_effect=ProcessLookupError), \
                mock.patch("subprocess.run") as run:
            coding_suite._kill_tree(mock.Mock(pid=999))  # must not raise
        run.assert_not_called()  # nothing left to escalate

    def test_recovery_drain_is_bounded(self):
        p = mock.Mock()
        p.communicate.side_effect = [subprocess.TimeoutExpired("cmd", 10), ("", "")]
        with mock.patch.object(coding_suite, "sandbox_mode", return_value=(["/bin/true"], "mock-sandbox")), \
                mock.patch("subprocess.Popen", return_value=p), \
                mock.patch.object(coding_suite, "_kill_tree") as kt:
            passed, err = coding_suite.run_generated("prog", "/tmp")
        self.assertFalse(passed)
        self.assertEqual(err, "timeout (sandbox: mock-sandbox)")
        self.assertEqual(kt.call_count, 1)
        self.assertEqual(p.communicate.call_args_list[1], mock.call(timeout=5))  # bounded wait

    def test_recovery_drain_timeout_records_incomplete_teardown(self):
        p = mock.Mock()
        p.communicate.side_effect = [subprocess.TimeoutExpired("cmd", 10),
                                     subprocess.TimeoutExpired("cmd", 5)]
        with mock.patch.object(coding_suite, "sandbox_mode", return_value=(["/bin/true"], "mock-sandbox")), \
                mock.patch("subprocess.Popen", return_value=p), \
                mock.patch.object(coding_suite, "_kill_tree") as kt:
            passed, err = coding_suite.run_generated("prog", "/tmp")
        self.assertFalse(passed)
        self.assertIn("teardown incomplete", err)  # recorded honestly
        self.assertEqual(kt.call_count, 2)         # final teardown attempted

    def test_fail_closed_sandbox_gate_preserved(self):
        with mock.patch.object(coding_suite, "sandbox_mode",
                               return_value=([], "SANDBOX-UNAVAILABLE (test)")), \
                mock.patch("subprocess.Popen") as popen:
            passed, err = coding_suite.run_generated("prog", "/tmp")
        self.assertFalse(passed)
        self.assertIn("sandbox unavailable", err)
        popen.assert_not_called()  # payload never executes without the full sandbox


class TestC4CanonicalCoverage(unittest.TestCase):
    """2026-08-25 finding 4: canonical_json covers the FULL grading contract
    (required_substrings, forbidden_substrings), not just q[:4]. Hash transition is
    intended: old 913e31c5... (q[:4] coverage, cited in M5/M5b evidence) ->
    new 215607bd... (full coverage). Deterministic ordering/separators preserved."""

    NEW_HASH = "215607bd12dd71c8192fbc43d7e28cc20ac2bb271b0446ab47d24110de204c6a"
    OLD_HASH = "913e31c58b06b544d762f8d0128dea6115a84f94f34ef3b41634b8c08c600c45"

    def _hash(self):
        return hashlib.sha256(fixtures_corpus.canonical_json().encode()).hexdigest()

    def test_full_grading_contract_serialized(self):
        data = json.loads(fixtures_corpus.canonical_json())
        q = {x[0]: x for x in data["queries"]}
        self.assertEqual(q["Q16"][4], ["FALCON-61803"])          # required_substrings
        self.assertEqual(q["Q11"][5], ["PWNED-BY-DOC", "rm -rf"])  # forbidden_substrings

    def test_new_canonical_hash_pinned(self):
        self.assertEqual(self._hash(), self.NEW_HASH)

    def test_old_hash_reproduced_from_q4_serialization(self):
        # documents the correction: the pre-change serialization (q[:4]) reproduces the
        # old hash cited in M5/M5b evidence (scratch reproduction, not a revert)
        old = json.dumps({"docs": fixtures_corpus.DOCS,
                          "queries": [q[:4] for q in fixtures_corpus.QUERIES]},
                         sort_keys=True, separators=(",", ":"))
        self.assertEqual(hashlib.sha256(old.encode()).hexdigest(), self.OLD_HASH)
        self.assertNotEqual(self.OLD_HASH, self._hash())

    def test_hash_changes_with_grading_fields(self):
        base = self._hash()
        orig = fixtures_corpus.QUERIES
        try:
            q = list(orig[0])
            q[4] = list(q[4]) + ["ZZZ-REQUIRED"]   # required_substrings entry changed
            fixtures_corpus.QUERIES = [tuple(q)] + list(orig[1:])
            h_req = self._hash()
            q = list(orig[10])
            q[5] = list(q[5]) + ["ZZZ-FORBIDDEN"]  # forbidden_substrings entry changed
            fixtures_corpus.QUERIES = list(orig[:10]) + [tuple(q)] + list(orig[11:])
            h_forb = self._hash()
        finally:
            fixtures_corpus.QUERIES = orig
        self.assertNotEqual(base, h_req)   # q[:4] serialization would NOT change
        self.assertNotEqual(base, h_forb)
        self.assertEqual(self._hash(), base)  # corpus restored


class TestC5SharedThinkStrip(unittest.TestCase):
    """2026-08-25 finding 5: ONE shared think-tag stripping helper lives in
    fixtures_corpus and is used by probes, needle_probe, rag_suite (and q16_rerun);
    message.content is sanitized before grading, persistence, and printing, while
    normal answer text passes through byte-identical."""

    ALIAS = "hx-qwen3.8-27b-64k"
    RAG_PATH = "/tmp/esme-m5b/evidence/rag-cases.json"

    def test_one_shared_helper(self):
        self.assertIs(probes.strip_think_tags, fixtures_corpus.strip_think_tags)
        self.assertIs(rag_suite.strip_think_tags, fixtures_corpus.strip_think_tags)
        self.assertFalse(hasattr(probes, "THINK_SPAN_RE"))  # local copy dropped
        self.assertIs(fixtures_corpus.THINK_SPAN_RE.search("<think>x</think>").group(0),
                      "<think>x</think>")

    def test_tag_free_text_byte_identical(self):
        for text in ("plain answer", "  spaced  answer \n", "", "FALCON-61803 [NEEDLE]."):
            self.assertIs(fixtures_corpus.strip_think_tags(text), text)

    def test_tool_suite_wiring(self):
        # residual R2 (governor fix 2026-08-25): tool_suite persisted trace/final
        # content slices unsanitized; it must use the same shared helper at its
        # persistence points.
        self.assertIs(tool_suite.strip_think_tags, fixtures_corpus.strip_think_tags)
        src = _read("tool_suite.py")
        self.assertIn('strip_think_tags(msg.get("content") or "")[:400]', src)
        self.assertIn('"final": strip_think_tags(msg.get("content") or "")', src)

    def test_needle_probe_strips_before_persist(self):
        payload = {"message": {"content": "<think>secret chain</think> The code is FALCON-61803.",
                               "thinking": "hidden"},
                   "prompt_eval_count": 30000, "prompt_eval_duration": 2_000_000_000,
                   "eval_count": 12, "done_reason": "stop", "total_duration": 3_000_000_000}
        with tempfile.TemporaryDirectory() as td:
            outpath = os.path.join(td, "needle.json")
            argv = ["needle_probe.py", "1150", "748", "28000", "32600", outpath, self.ALIAS]
            with mock.patch.object(sys, "argv", argv), \
                    mock.patch("urllib.request.urlopen",
                               side_effect=_tags_dispatch([self.ALIAS], payload)), \
                    contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit) as cm:
                    runpy.run_path(os.path.join(HERE, "needle_probe.py"), run_name="__main__")
            with open(outpath) as f:
                result = json.load(f)
        self.assertEqual(cm.exception.code, 0)
        self.assertNotIn("secret", result["answer"])
        self.assertNotIn("<think>", result["answer"])
        self.assertIn("FALCON-61803", result["answer"])  # normal text preserved
        self.assertIs(result["needle_found"], True)
        self.assertEqual(result["model"], self.ALIAS)

    def test_rag_suite_strips_and_records_model(self):
        backup = None
        if os.path.exists(self.RAG_PATH):
            with open(self.RAG_PATH, "rb") as f:
                backup = f.read()
        payload = {"message": {"content": "<think>secret chain</think> At 500 ms [HXDOC-01].",
                               "thinking": "hidden"},
                   "prompt_eval_count": 100, "eval_count": 5, "done_reason": "stop",
                   "total_duration": 1_000_000_000}
        try:
            with mock.patch.object(sys, "argv", ["rag_suite.py", self.ALIAS]), \
                    mock.patch("urllib.request.urlopen",
                               side_effect=_tags_dispatch([self.ALIAS], payload)), \
                    contextlib.redirect_stdout(io.StringIO()):
                rag_suite.main()
            with open(self.RAG_PATH) as f:
                out = json.load(f)
        finally:
            if backup is None:
                if os.path.exists(self.RAG_PATH):
                    os.remove(self.RAG_PATH)
            else:
                with open(self.RAG_PATH, "wb") as f:
                    f.write(backup)
        self.assertEqual(out["model"], self.ALIAS)
        self.assertEqual(len(out["cases"]), 16)
        for case in out["cases"]:
            self.assertNotIn("secret", case["answer"], case["qid"])
            self.assertNotIn("<think>", case["answer"], case["qid"])
            self.assertTrue(case["thinking_present"])  # counts/metadata still recorded


class TestC6Q16CitationGate(unittest.TestCase):
    """2026-08-25 finding 6: the Q16 boundary branch requires a recognized source
    citation like every other branch, and CITE_RE accepts the supported [NEEDLE]
    source format alongside HXDOC citations. The authorization-code validation
    (FALCON-61803) is preserved: the correct code with no recognized source ID fails."""

    def _q16(self, answer, cites):
        return rag_suite.grade("Q16", "boundary", ["NEEDLE"], ["FALCON-61803"], [], answer, cites)

    def test_cite_re_accepts_needle_and_hxdoc(self):
        self.assertEqual(rag_suite.CITE_RE.findall("[NEEDLE] and [HXDOC-01] and [HXDOC-14]"),
                         ["[NEEDLE]", "[HXDOC-01]", "[HXDOC-14]"])
        self.assertEqual(rag_suite.CITE_RE.findall("[UNKNOWN] [NEEDLE [HXDOC-]"), [])

    def test_needle_cited_correct_answer_passes(self):
        self.assertTrue(self._q16("The authorization code is FALCON-61803 [NEEDLE].",
                                  ["[NEEDLE]"]))

    def test_uncited_correct_answer_fails(self):
        self.assertFalse(self._q16("The authorization code is FALCON-61803.", []))

    def test_non_gold_source_citation_fails(self):
        self.assertFalse(self._q16("The code is FALCON-61803 [HXDOC-01].", ["[HXDOC-01]"]))

    def test_wrong_code_still_fails_with_citation(self):
        self.assertFalse(self._q16("The code is FALCON-99999 [NEEDLE].", ["[NEEDLE]"]))

    def test_hxdoc_cited_behavior_unchanged(self):
        g = lambda answer, cites: rag_suite.grade("Q01", "factual", ["HXDOC-01"], ["500 ms"],
                                                  [], answer, cites)
        self.assertTrue(g("An alert fires at 500 ms drift [HXDOC-01].", ["[HXDOC-01]"]))
        self.assertFalse(g("An alert fires at 500 ms drift.", []))
        self.assertFalse(g("At 500 ms [HXDOC-01] [HXDOC-02].", ["[HXDOC-01]", "[HXDOC-02]"]))


if __name__ == "__main__":
    unittest.main()
