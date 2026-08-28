"""Gordon Phase B — pytest configuration and shared harness (Gates 6-7).

Reuses the Phase A machinery (gordon_util: env contract, runner, evidence,
session-log parsing, queue-transient discipline, de-patterning writer) and
adds the web/API helpers the Gate 7 surface needs. Static artifact; executes
on hxs-15 only after the governor releases it.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

PHASE_A_DIR = Path(__file__).resolve().parent.parent / "phase-a"
sys.path.insert(0, str(PHASE_A_DIR))

from gordon_util import (  # noqa: E402
    Cfg,
    Evidence,
    base_env,
    blocked,
    candidate_argv,
    epoch_header,
    events_of_type,
    find_session_artifacts,
    key_source_available,
    latest_request_header,
    nonce,
    read_file_bytes,
    read_session_log,
    render_fixture,
    run_candidate,
    sandbox_unavailable,
    seqs_contiguous,
)

from test_g3_providers import (  # noqa: E402
    register_call,
    require_routing_inputs,
    run_routed_headless,
    seam_fixture_for,
    seam_provider,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def cfg() -> Cfg:
    return Cfg.from_env()


@pytest.fixture(scope="session")
def evidence(cfg: Cfg, tmp_path_factory) -> Evidence:
    root = cfg.evidence_dir
    try:
        root.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        root = tmp_path_factory.mktemp("evidence-b")
    return Evidence(root)


@pytest.fixture()
def rec(evidence: Evidence, request: pytest.FixtureRequest):
    class _Rec:
        def __init__(self) -> None:
            self.commands: list = []
            self.artifacts: list[str] = []

        def artifact(self, name: str, content: str | bytes) -> str:
            path = evidence.artifact(request.node.nodeid.split("::")[-1], name, content)
            self.artifacts.append(path)
            return path

        def finish(self, disposition: str, oracle: str, observed: str, note: str = "") -> None:
            evidence.record(
                request.node.nodeid,
                disposition=disposition,
                oracle=oracle,
                observed=observed,
                commands=self.commands,
                artifacts=self.artifacts,
                note=note,
            )

    return _Rec()


def _dsh_writable_dir(tag: str) -> Path:
    import uuid

    root = Path("/var/tmp/gordon-run-b")
    root.mkdir(parents=True, exist_ok=True)
    root.chmod(0o777)
    path = root / f"{tag}-{uuid.uuid4().hex[:10]}"
    path.mkdir()
    path.chmod(0o777)
    return path


@pytest.fixture()
def scratch_home(cfg: Cfg) -> Path:
    home = _dsh_writable_dir("home") / "dsh-home"
    home.mkdir()
    home.chmod(0o777)
    return home


@pytest.fixture()
def scratch_env(scratch_home: Path) -> dict[str, str]:
    return {"HOME": str(scratch_home), "DSH_HOME": str(scratch_home)}


@pytest.fixture()
def workspace(cfg: Cfg) -> Path:
    ws = _dsh_writable_dir("ws") / "workspace"
    ws.mkdir()
    ws.chmod(0o777)
    return ws


# --------------------------------------------------------------------------
# Web boot harness (Gate 7)
# --------------------------------------------------------------------------

class WebBoot:
    """A web-profile boot on loopback with an OS-assigned port.

    Lifecycle: start(), wait_bound(), http_get(path), stop() (SIGTERM → 0 per
    profile-boot.ts:221). The boot runs as the service user through the same
    env -i wrapper as every other candidate invocation.
    """

    def __init__(self, cfg: Cfg, env_extra: dict[str, str], cwd: str, patches: list[str] | None = None):
        self.cfg = cfg
        env = base_env(cfg, env_extra)
        args = ["--profile", "web", "--host", "127.0.0.1", "--port", "0"]
        for patch in patches or []:
            args[1:1] = []  # no-op guard; patches are launcher flags below
        argv_tail = []
        for patch in patches or []:
            argv_tail += ["--patch", patch]
        self.argv = candidate_argv(cfg, ["--profile", "web", *argv_tail,
                                         "--host", "127.0.0.1", "--port", "0"], env)
        self.cwd = cwd
        self.proc: subprocess.Popen | None = None
        self.port: int | None = None
        self._stdout: list[str] = []
        self._stderr: list[str] = []

    def start(self) -> None:
        self.proc = subprocess.Popen(
            self.argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, cwd=self.cwd,
        )

    def wait_bound(self, timeout: float = 90.0) -> bool:
        """The web app reports its bound address; discover the port by probing
        the process's listeners once it announces readiness or a listener
        appears. Falls back to parsing the boot log for the port."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                return False
            port = self._discover_port()
            if port:
                self.port = port
                return True
            time.sleep(1.5)
        return False

    def _discover_port(self) -> int | None:
        if self.proc is None:
            return None
        try:
            out = subprocess.run(
                ["ss", "-tlnp"], capture_output=True, text=True, timeout=10
            ).stdout
            for line in out.splitlines():
                if str(self.proc.pid) in line and "127.0.0.1:" in line:
                    match = re.search(r"127\.0\.0\.1:(\d+)", line)
                    if match:
                        return int(match.group(1))
        except (OSError, subprocess.SubprocessError):
            pass
        return None

    def http_get(self, path: str, timeout: float = 10.0) -> tuple[int, str]:
        assert self.port, "web boot not bound"
        try:
            with urllib.request.urlopen(
                f"http://127.0.0.1:{self.port}{path}", timeout=timeout
            ) as resp:
                return resp.status, resp.read().decode(errors="replace")
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read().decode(errors="replace")

    def stop(self) -> int:
        if self.proc is None:
            return -1
        if self.proc.poll() is None:
            self.proc.send_signal(signal.SIGTERM)
        try:
            out, _ = self.proc.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            out, _ = self.proc.communicate()
        self._stdout.append(out or "")
        return self.proc.returncode

    def boot_log(self) -> str:
        return "".join(self._stdout)


@pytest.fixture()
def web_boot(cfg: Cfg):
    def _make(env_extra: dict[str, str], cwd: str, patches: list[str] | None = None) -> WebBoot:
        boot = WebBoot(cfg, env_extra, cwd, patches)
        boot.start()
        return boot

    return _make


def routed_task(marker: str, tool_hint: str = "") -> str:
    hint = f" {tool_hint}" if tool_hint else ""
    return (f"{hint}Reply with exactly this token and nothing else: {marker}".strip())


def cooperate(cfg, scratch_home, scratch_env, workspace, rec, tag, task, check,
              env_extra=None, timeout=420.0, model_key="coder"):
    """Model-cooperation runner (Phase B): up to three recorded attempts with
    queue-transient spacing; check(scratch_home, run, marker) -> (ok, detail)
    where ok may be the string "SANDBOX-D1"."""
    from gordon_util import is_queue_transient

    require_routing_inputs(cfg, model_key)
    attempts = []
    for attempt in range(1, int(os.environ.get("GORDON_QUEUE_ATTEMPTS", "3")) + 1):
        marker = f"GORDON-{tag}A{attempt}-{nonce()}"
        patch = seam_fixture_for(cfg, scratch_home, model_key=model_key, max_retries=1)
        run = run_routed_headless(
            cfg, scratch_env, workspace, patch, task.replace("__MARKER__", marker),
            timeout=timeout, env_extra=env_extra,
        )
        rec.commands.append(run)
        register_call(cfg, {"tag": f"{tag}A{attempt}", "model_key": model_key,
                            "model_id": cfg.model_ids()[model_key], "marker": marker,
                            "ts": int(time.time()), "exit": run.exit_code})
        ok, detail = check(scratch_home, run, marker)
        attempts.append(f"attempt{attempt}: exit={run.exit_code}; {detail}")
        if ok == "SANDBOX-D1":
            return "SANDBOX-D1", " | ".join(attempts)
        if ok:
            return True, " | ".join(attempts)
        if is_queue_transient(run):
            time.sleep(float(os.environ.get("GORDON_QUEUE_SPACING_S", "25")))
    return False, " | ".join(attempts)


def latest_log(cfg, scratch_home) -> dict:
    artifacts = find_session_artifacts(scratch_home, cfg)
    return read_session_log(cfg, artifacts[-1]) if artifacts else {"records": []}


def log_text(log: dict) -> str:
    return json.dumps(log.get("records", []))


def finish_coop(rec, result, observed, oracle, note=""):
    if result == "SANDBOX-D1":
        rec.finish("BLOCKED",
                   oracle + " — requires a usable sandbox backend (defect D1 window semantics)",
                   observed, note="retest semantics per D1 retest record")
        blocked("sandbox backend absent (defect D1 semantics)")
    rec.finish("PASS" if result else "FAIL", oracle, observed, note=note)
