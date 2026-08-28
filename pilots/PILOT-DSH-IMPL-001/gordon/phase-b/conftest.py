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
def candidate_bin(cfg: Cfg) -> Path:
    """The candidate binary (mirrors phase-a conftest; authoring-gap fix of
    record 2026-08-28: the Phase B conftest referenced this fixture without
    defining it — caught at first execution-window collection, fixed here)."""
    path = Path(cfg.dsh_bin)
    if not path.exists():
        found = shutil.which("dsh")
        if found:
            return Path(found)
        blocked(f"candidate binary not at {path} and no `dsh` on PATH (Morpheus handoff pending)")
    return path


def run_as_dsh_argv(cfg: Cfg, argv: list[str], *, env_extra: dict[str, str] | None = None,
                    cwd: str | None = None, timeout: float = 300.0,
                    key_mode: str = "with-key"):
    """Run an arbitrary argv as the service user under the same controlled-env
    contract as run_candidate (used for node/Python drivers that are not the
    dsh binary itself: SDK runtimes, ACP drivers). Key by mechanism only."""
    from gordon_util import RunRecord, _runner_prefix, base_env

    env = base_env(cfg, env_extra)
    prefix = _runner_prefix(cfg)
    assignments = [f"{k}={v}" for k, v in sorted(env.items())]
    wrapper = cfg.wrapper
    if Path(wrapper).exists():
        full = prefix + [wrapper, key_mode, *assignments, "--", *argv]
    else:
        full = prefix + ["env", "-i", *assignments, *argv]
    effective_cwd = cwd or "/var/tmp"
    started = time.monotonic()
    proc = subprocess.run(full, capture_output=True, text=True,
                          cwd=effective_cwd, timeout=timeout)
    return RunRecord(
        argv=argv,
        env_names=sorted(env.keys()),
        cwd=effective_cwd,
        exit_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        duration_s=time.monotonic() - started,
    )


# --------------------------------------------------------------------------
# Web API client (Morpheus §10 envelope of record): POST /api/<ns.method>
# {"type":"client-request","rpcId","method","payload"} → server-response;
# no-envelope GET legs (session.export, WS downlinks).
# --------------------------------------------------------------------------

class ApiClient:
    """Minimal wire client for the traced /api envelope (stdlib only)."""

    def __init__(self, port: int, host: str = "127.0.0.1"):
        self.port = port
        self.host = host
        self.base = f"http://{host}:{port}"

    def rpc(self, method: str, payload: dict, timeout: float = 30.0) -> tuple[int, dict]:
        body = json.dumps({
            "type": "client-request",
            "rpcId": f"gordon-{nonce()}",
            "method": method,
            "payload": payload,
        }).encode()
        req = urllib.request.Request(
            f"{self.base}/api/{method}", data=body,
            headers={"Content-Type": "application/json"}, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode(errors="replace")
            try:
                return exc.code, json.loads(raw)
            except json.JSONDecodeError:
                return exc.code, {"_httpError": exc.code, "_body": raw[:500]}

    def get(self, path: str, timeout: float = 30.0) -> tuple[int, bytes, dict]:
        req = urllib.request.Request(f"{self.base}{path}", method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read(), dict(resp.headers)
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read(), dict(exc.headers)


class WsDownlink:
    """Minimal RFC 6455 client for the /api/events.* downlinks (stdlib only).

    Server→client frames are unmasked; client frames must be masked. Supports
    text + continuation frames, ping→pong, and close. Bounded reads only.
    """

    def __init__(self, port: int, path: str, host: str = "127.0.0.1", timeout: float = 60.0):
        import base64

        self.sock = socket.create_connection((host, port), timeout=timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        self.sock.sendall(request.encode())
        response = self._read_http_head()
        self.status = int(response.split(" ", 2)[1]) if " " in response else 0
        self.head = response

    def _read_exact(self, count: int) -> bytes:
        buf = b""
        while len(buf) < count:
            chunk = self.sock.recv(count - len(buf))
            if not chunk:
                raise ConnectionError("downlink closed mid-frame")
            buf += chunk
        return buf

    def _read_http_head(self) -> str:
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = self.sock.recv(1)
            if not chunk:
                break
            buf += chunk
            if len(buf) > 16384:
                break
        return buf.decode(errors="replace")

    def read_message(self, timeout: float = 60.0) -> dict | None:
        """Read one complete text message as JSON; None on close frame."""
        self.sock.settimeout(timeout)
        payload = b""
        while True:
            head = self._read_exact(2)
            fin = head[0] & 0x80
            opcode = head[0] & 0x0F
            length = head[1] & 0x7F
            if length == 126:
                length = int.from_bytes(self._read_exact(2), "big")
            elif length == 127:
                length = int.from_bytes(self._read_exact(8), "big")
            mask = head[1] & 0x80
            mask_key = self._read_exact(4) if mask else b""
            data = bytearray(self._read_exact(length))
            if mask:
                for i in range(length):
                    data[i] ^= mask_key[i % 4]
            if opcode == 0x8:
                return None
            if opcode == 0x9:  # ping → pong
                pong = bytearray([0x8A, 0x80 | len(data)])
                pong_key = os.urandom(4)
                pong.extend(pong_key)
                pong.extend(b ^ pong_key[i % 4] for i, b in enumerate(data))
                self.sock.sendall(bytes(pong))
                continue
            if opcode in (0x1, 0x0):
                payload += bytes(data)
                if fin:
                    return json.loads(payload.decode())

    def collect_until(self, predicate, timeout_s: float = 300.0,
                      max_frames: int = 2000) -> list[dict]:
        """Collect decoded frames until predicate(frame) or the bound elapses."""
        frames: list[dict] = []
        deadline = time.monotonic() + timeout_s
        while time.monotonic() < deadline and len(frames) < max_frames:
            try:
                frame = self.read_message(timeout=max(1.0, deadline - time.monotonic()))
            except (TimeoutError, socket.timeout, ConnectionError, json.JSONDecodeError):
                break
            if frame is None:
                break
            frames.append(frame)
            if predicate(frame):
                break
        return frames

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass


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
