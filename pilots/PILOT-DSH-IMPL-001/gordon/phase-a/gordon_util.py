"""Gordon Phase A — shared machinery for the Gates 0-5 qualification suite.

Static artifact authored 2026-08-28. Executes on hxs-15 only after the
governor releases it. No secrets: this module handles credential *names*
only. Values arrive via the environment at execution time and are never
read, logged, or asserted beyond presence.

Dispositions (profile §7): PASS / FAIL / BLOCKED / NOT_RUN /
NOT_APPLICABLE / NOT_IN_PINNED_VERSION / AVAILABLE_DISABLED /
EXPERIMENTAL_LAB_ONLY / DEFERRED_BY_POLICY.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SUITE_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = SUITE_DIR / "fixtures"

# Pinned review baseline (gordon profile §3 — ratified HX contract).
PINNED_VERSION = "0.1.1-rc.2"
PINNED_PACKAGE_JSON_SHA256 = "4adbdffa373754a048a214c5de3ec0671ac6e1f3c1521ec5b37e8fad1a4986d7"
PINNED_PNPM_LOCK_SHA256 = "6f20c268e76df1294c16f016ab10a7fa1271608b4db0f4fafe8f7c21ec90013e"
PINNED_NODE = "v24.20.0"
PINNED_PNPM = "11.7.0"

# Environment variable names this suite reads. None of these hold secrets in
# the repository; the only secret-adjacent one is the *name* of the variable
# that will carry the OmniRoute client key at execution time. Defaults reflect
# Morpheus's landed Phase A install (03-morpheus-phase-a-install.md §10).
ENV_DEFAULTS: dict[str, str] = {
    "GORDON_DSH_BIN": "/usr/local/bin/dsh",
    "GORDON_DSH_ROOT": "/opt/dsh",
    "GORDON_DSH_SRC": "/opt/dsh",
    "GORDON_NODE": "/opt/node-v24.20.0/bin/node",
    "GORDON_PNPM": "/opt/node-v24.20.0/bin/pnpm",
    "GORDON_DSH_USER": "dsh",
    "GORDON_DSH_UID": "999",
    "GORDON_REAL_HOME": "/var/lib/dsh",
    "GORDON_SCRATCH": "/var/lib/dsh/gordon",
    "GORDON_EVIDENCE_DIR": "",  # default: <scratch>/evidence
    "GORDON_OMNI_BASE_URL": "http://192.168.50.207:20128/v1",
    "GORDON_OMNI_KEY_ENV": "OMNIROUTE_API_KEY",
    "GORDON_SEAM": "auto",  # auto (→ pi-ai, the landed native seam) | pi-ai | deepseek | custom
    "GORDON_RUNNER": "auto",  # auto | direct | runuser | sudo
    "GORDON_USAGE_DIR": "",  # default: <scratch>/omni-usage
    "GORDON_MODEL_QWEN": "ollama-local/hx-qwen3.8-27b-64k:latest",
    "GORDON_MODEL_CODER": "ollama-local/hx-qwen3.6-coderx-64k:latest",
    "GORDON_MODEL_META": "ollama-local/hx-muse-glimmer-64k:latest",
    "GORDON_CUSTOM_ROW_ID": "",  # custom seam: composed row id of the adapter
    "GORDON_HOST": "192.168.50.214",
}


def blocked(reason: str) -> None:
    """Skip the current test with a BLOCKED disposition and a named reason."""
    import pytest

    pytest.skip(f"BLOCKED: {reason}")


@dataclass(frozen=True)
class Cfg:
    """Resolved environment contract for one suite run."""

    values: dict[str, str]

    @classmethod
    def from_env(cls) -> "Cfg":
        values = {name: os.environ.get(name, default) for name, default in ENV_DEFAULTS.items()}
        return cls(values)

    def __getattr__(self, name: str) -> str:
        key = f"GORDON_{name.upper()}"
        try:
            return self.values[key]
        except KeyError:
            raise AttributeError(name) from None

    @property
    def scratch(self) -> Path:
        return Path(self.values["GORDON_SCRATCH"])

    @property
    def evidence_dir(self) -> Path:
        return Path(self.values["GORDON_EVIDENCE_DIR"] or str(self.scratch / "evidence"))

    @property
    def usage_dir(self) -> Path:
        return Path(self.values["GORDON_USAGE_DIR"] or str(self.scratch / "omni-usage"))

    @property
    def omni_key_env_name(self) -> str:
        return self.values["GORDON_OMNI_KEY_ENV"]

    def omni_key_present(self) -> bool:
        """Presence check only. The value is never read."""
        return bool(os.environ.get(self.omni_key_env_name))

    def model_ids(self) -> dict[str, str]:
        return {
            "qwen": self.values["GORDON_MODEL_QWEN"],
            "coder": self.values["GORDON_MODEL_CODER"],
            "meta": self.values["GORDON_MODEL_META"],
        }


@dataclass
class RunRecord:
    """One executed command: the §13 evidence atom."""

    argv: list[str]
    env_names: list[str]
    cwd: str
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float

    def to_json(self) -> dict[str, Any]:
        return {
            "argv": self.argv,
            "env_names": self.env_names,
            "cwd": self.cwd,
            "exit_code": self.exit_code,
            "stdout_tail": self.stdout[-4000:],
            "stderr_tail": self.stderr[-4000:],
            "duration_s": round(self.duration_s, 3),
        }


def _runner_prefix(cfg: Cfg) -> list[str]:
    """How the candidate is invoked as the service user.

    auto: root → runuser; already the service user → direct; otherwise sudo -n.
    """
    mode = cfg.runner
    user = cfg.dsh_user
    if mode == "direct":
        return []
    if mode == "runuser":
        return ["runuser", "-u", user, "--"]
    if mode == "sudo":
        return ["sudo", "-n", "-u", user, "--"]
    # auto
    if os.geteuid() == 0:
        return ["runuser", "-u", user, "--"]
    if _whoami() == user:
        return []
    if shutil.which("sudo") and subprocess.run(
        ["sudo", "-n", "-u", user, "true"], capture_output=True
    ).returncode == 0:
        return ["sudo", "-n", "-u", user, "--"]
    blocked(
        f"cannot invoke the candidate as user {user!r}: executor is not root, "
        f"not {user!r}, and passwordless sudo -u {user} is unavailable"
    )
    return []  # unreachable: blocked() skips the test


def _whoami() -> str:
    return subprocess.run(["id", "-un"], capture_output=True, text=True).stdout.strip()


def base_env(cfg: Cfg, extra: dict[str, str] | None = None) -> dict[str, str]:
    """Controlled environment for candidate invocations.

    Only named variables pass through. The OmniRoute key travels exclusively
    under the variable named by GORDON_OMNI_KEY_ENV, if the governor exported
    it; its value is never touched here.
    """
    node_bin = str(Path(cfg.node).parent)
    env: dict[str, str] = {
        "PATH": f"{node_bin}:/usr/local/bin:/usr/bin:/bin",
        "HOME": f"/home/{cfg.dsh_user}",
        "LANG": "C.UTF-8",
        # Telemetry must stay off unless a test opts in explicitly.
        "DSH_TELEMETRY_DISABLED": "1",
    }
    key_value = os.environ.get(cfg.omni_key_env_name)
    if key_value is not None:
        env[cfg.omni_key_env_name] = key_value
    if extra:
        env.update(extra)
    return env


def candidate_argv(
    cfg: Cfg, args: list[str], env: dict[str, str], runner: list[str] | None = None
) -> list[str]:
    """Full wrapped argv: privilege prefix + `env -i` + controlled assignments.

    Shared by run_candidate and the signal-drill Popen sites so every candidate
    process sees exactly the same environment discipline under sudo env_reset.
    """
    prefix = _runner_prefix(cfg) if runner is None else runner
    assignments = [f"{key}={value}" for key, value in sorted(env.items())]
    return prefix + ["env", "-i", *assignments, cfg.dsh_bin, *args]


def run_candidate(
    cfg: Cfg,
    args: list[str],
    *,
    env_extra: dict[str, str] | None = None,
    cwd: str | None = None,
    timeout: float = 180.0,
    runner: list[str] | None = None,
) -> RunRecord:
    """Run the candidate binary as the service user and record the atom.

    The assignment list rides INSIDE the privilege wrapper
    (`sudo -n -u dsh -- env -i K=V ... dsh ...`): sudo's env_reset would strip
    subprocess-side variables, and the dsh process must see exactly the
    controlled set (Morpheus's execution contract, receipt §10).
    """
    env = base_env(cfg, env_extra)
    argv = candidate_argv(cfg, args, env, runner)
    started = time.monotonic()
    proc = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        cwd=cwd or str(cfg.scratch),
        timeout=timeout,
    )
    return RunRecord(
        argv=[cfg.dsh_bin, *args],
        env_names=sorted(env.keys()),
        cwd=cwd or str(cfg.scratch),
        exit_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        duration_s=time.monotonic() - started,
    )


def run_host(
    argv: list[str],
    *,
    timeout: float = 120.0,
    cwd: str | None = None,
    env_extra: dict[str, str] | None = None,
) -> RunRecord:
    """Run a plain host command (not the candidate) as the executor."""
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    started = time.monotonic()
    proc = subprocess.run(argv, capture_output=True, text=True, cwd=cwd, timeout=timeout, env=env)
    return RunRecord(
        argv=argv,
        env_names=sorted(env_extra.keys()) if env_extra else [],
        cwd=cwd or "",
        exit_code=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        duration_s=time.monotonic() - started,
    )


class Evidence:
    """§13 evidence recorder: one JSON record per test, artifacts alongside."""

    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.ledger_path = self.root / "evidence-ledger.jsonl"
        self.identity: dict[str, Any] = {}

    def set_identity(self, identity: dict[str, Any]) -> None:
        self.identity = identity
        (self.root / "candidate-identity.json").write_text(
            json.dumps(identity, indent=2, sort_keys=True) + "\n"
        )

    def artifact(self, test_id: str, name: str, content: str | bytes) -> str:
        safe = re.sub(r"[^A-Za-z0-9_.-]", "_", f"{test_id}-{name}")
        path = self.root / safe
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content)
        return str(path)

    def record(
        self,
        test_id: str,
        *,
        disposition: str,
        oracle: str,
        observed: str,
        commands: list[RunRecord] | None = None,
        artifacts: list[str] | None = None,
        note: str = "",
    ) -> None:
        entry = {
            "test_id": test_id,
            "disposition": disposition,
            "oracle": oracle,
            "observed": observed,
            "candidate_identity": self.identity,
            "environment": {
                "host": "hxs-15",
                "host_ip": ENV_DEFAULTS["GORDON_HOST"],
                "user": "dsh",
                "recorded_at_epoch": int(time.time()),
            },
            "commands": [c.to_json() for c in (commands or [])],
            "artifacts": artifacts or [],
            "note": note,
        }
        with self.ledger_path.open("a") as fh:
            fh.write(json.dumps(entry, sort_keys=True) + "\n")


def nonce() -> str:
    """Unique per-run nonce: defeats OmniRoute's semantic cache (Trinity gate
    record: byte-identical repeats are cache-served with no usage row)."""
    return uuid.uuid4().hex[:12]


def render_fixture(name: str, mapping: dict[str, str], dest_dir: Path) -> Path:
    """Render a fixture template with runtime values into the scratch area."""
    template = (FIXTURES_DIR / name).read_text()
    for key, value in mapping.items():
        template = template.replace(f"__{key}__", value)
    leftovers = re.findall(r"__[A-Z_]+__", template)
    if leftovers:
        blocked(f"fixture {name} has unresolved placeholders: {sorted(set(leftovers))}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = dest_dir / name.replace(".tmpl", "")
    out.write_text(template)
    return out


# --------------------------------------------------------------------------
# Session artifact helpers (oracles: session-persistence-jsonl/src/format.ts)
# --------------------------------------------------------------------------

def project_key(cwd: str) -> str:
    """Python port of format.ts projectKey(): readable, lossy, `--<slug>--`."""
    readable = []
    separator_run = False
    for ch in cwd:
        code = ord(ch)
        if ch in "/\\:":
            if not separator_run:
                readable.append("-")
            separator_run = True
        elif ch != "~" and re.match(r"[A-Za-z0-9._-]", ch):
            readable.append(ch)
            separator_run = False
        else:
            readable.append(f"~{code:04X}")
            separator_run = False
    slug = "".join(readable).lstrip("-") or "root"
    return f"--{slug[:251]}--"


def encode_segment(raw: str) -> str:
    """Python port of format.ts encodeSegment()."""
    if raw == "":
        raise ValueError("cannot encode an empty path segment")
    if raw == ".":
        return "~002E"
    if raw == "..":
        return "~002E~002E"
    out = []
    for ch in raw:
        if ch != "~" and re.match(r"[A-Za-z0-9._-]", ch):
            out.append(ch)
        else:
            out.append(f"~{ord(ch):04X}")
    return "".join(out)


def _by_mtime(paths: list[Path]) -> list[Path]:
    """Newest last: call sites take [-1] for the latest run's artifact.
    Session ids are random (`session-<uuid>`), so lexical order is not recency."""
    def mt(path: Path) -> float:
        try:
            return path.stat().st_mtime
        except OSError:
            return 0.0

    return sorted(paths, key=mt)


def find_session_artifacts(home: Path, cfg: "Cfg | None" = None) -> list[Path]:
    """List session artifacts under a harness home, oldest to newest.

    The persistence backend creates its root mode 0700 owned by the service
    user (session-persistence-jsonl/src/index.ts:536), so a non-root,
    non-service-user executor cannot enumerate it directly. With `cfg` given,
    fall back to a runner-assisted staged copy (scratch only).
    """
    root = home / "sessions"
    try:
        if root.is_dir():
            found = list(root.rglob("session.jsonl.zstd")) + list(root.rglob("session.jsonl"))
            if found:
                return _by_mtime(found)
            return []
        if cfg is None:
            return []
    except PermissionError:
        if cfg is None:
            raise
    if cfg is None:
        return []
    return _stage_artifacts_as_service_user(cfg, home)


def _stage_artifacts_as_service_user(cfg: "Cfg", home: Path) -> list[Path]:
    """Runner-assisted artifact staging: list with the service user's rights,
    copy into an executor-readable staging dir, return the staged paths.

    Staging lives under the Gordon scratch area and is rebuilt per call, so a
    staged copy always reflects the artifact at listing time.
    """
    import hashlib

    prefix = _runner_prefix(cfg)
    staging = cfg.scratch / "staged" / hashlib.sha256(str(home).encode()).hexdigest()[:12]
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True, exist_ok=True)
    staging.chmod(0o777)
    find = subprocess.run(
        prefix + ["find", str(home / "sessions"), "-type", "f", "(", "-name",
                  "session.jsonl", "-o", "-name", "session.jsonl.zstd", ")"],
        capture_output=True, text=True, timeout=60,
    )
    staged: list[Path] = []
    for line in find.stdout.splitlines():
        source = line.strip()
        if not source:
            continue
        dest = staging / (hashlib.sha256(source.encode()).hexdigest()[:16] + "-" + Path(source).name)
        # -p preserves mtime: the recency ordering find_session_artifacts
        # returns must reflect the artifact, not the copy time.
        copied = subprocess.run(prefix + ["cp", "-p", source, str(dest)], capture_output=True, timeout=60)
        if copied.returncode == 0:
            staged.append(dest)
    return _by_mtime(staged)


def read_file_bytes(cfg: "Cfg", path: Path) -> bytes:
    """Read bytes, falling back to a runner-assisted cat for dsh-owned files."""
    try:
        return path.read_bytes()
    except PermissionError:
        prefix = _runner_prefix(cfg)
        proc = subprocess.run(prefix + ["cat", str(path)], capture_output=True, timeout=60)
        if proc.returncode != 0:
            blocked(f"cannot read {path} even as {cfg.dsh_user}: {proc.stderr[-200:]!r}")
        return proc.stdout


def zstd_decode(cfg: Cfg, path: Path) -> bytes:
    """Decode a .jsonl.zstd artifact.

    Primary: the candidate's own Node `node:zlib` streaming decompressor
    (handles the concatenated-frame container written by the backend).
    Fallback: the `zstd` CLI. Otherwise BLOCKED with the dependency named.
    """
    decoder = SUITE_DIR / "fixtures" / "decode-zstd.mjs"
    if Path(cfg.node).exists() and decoder.exists():
        proc = subprocess.run(
            [cfg.node, str(decoder), str(path)], capture_output=True, timeout=60
        )
        if proc.returncode == 0:
            return proc.stdout
    if shutil.which("zstd"):
        proc = subprocess.run(["zstd", "-dc", str(path)], capture_output=True, timeout=60)
        if proc.returncode == 0:
            return proc.stdout
    blocked(
        "no zstd decoder available: candidate node:zlib decode failed and no zstd CLI on PATH"
    )
    return b""  # unreachable: blocked() skips the test


def read_session_log(cfg: Cfg, path: Path) -> dict[str, Any]:
    """Parse one session artifact into header + event records.

    Returns {"header": dict, "records": list, "torn_tail": bool}. Packed rows
    (`text-chunks`/`reasoning-chunks`/`tool-call-chunks`, format.ts chunk-rows)
    are kept as records with `seq0`; `expand_seqs` reconstructs member seqs for
    contiguity checks. A trailing fragment without newline is a torn tail, per
    the scanner's finish() semantics.
    """
    raw = read_file_bytes(cfg, path) if path.suffix != ".zstd" else zstd_decode(cfg, path)
    torn_tail = bool(raw) and not raw.endswith(b"\n")
    lines = [ln for ln in raw.split(b"\n") if ln.strip()]
    if not lines:
        return {"header": None, "records": [], "torn_tail": torn_tail, "error": "empty log"}
    try:
        header = json.loads(lines[0])
    except json.JSONDecodeError:
        return {"header": None, "records": [], "torn_tail": torn_tail, "error": "bad header JSON"}
    records = []
    errors = []
    for i, line in enumerate(lines[1:], start=2):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            errors.append(f"line {i}: unparsable record")
    return {
        "header": header,
        "records": records,
        "torn_tail": torn_tail,
        "parse_errors": errors,
    }


def expand_seqs(records: list[dict[str, Any]]) -> list[int]:
    """Expand plain `seq` events and packed `seq0` rows into the event seq list."""
    seqs: list[int] = []
    for rec in records:
        if "seq" in rec:
            seqs.append(rec["seq"])
        elif "seq0" in rec:
            count = 1
            data = rec.get("data")
            if isinstance(data, dict):
                for value in data.values():
                    if isinstance(value, list):
                        count = max(count, len(value))
            seqs.extend(range(rec["seq0"], rec["seq0"] + count))
    return seqs


def seqs_contiguous(records: list[dict[str, Any]]) -> tuple[bool, str]:
    """Scanner rule (format.ts consumeEventLine): event k has seq k."""
    seqs = expand_seqs(records)
    for expected, got in enumerate(seqs):
        if got != expected:
            return False, f"seq gap at index {expected}: got {got}"
    return True, f"{len(seqs)} events contiguous from 0"


def events_of_type(records: list[dict[str, Any]], type_name: str) -> list[dict[str, Any]]:
    return [r for r in records if r.get("type") == type_name]


def latest_request_header(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    headers = events_of_type(records, "request/header")
    return headers[-1] if headers else None
