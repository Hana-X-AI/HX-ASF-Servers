"""Gordon Phase A — pytest configuration.

Disposition mapping (profile §7): pytest passed → PASS; failed → FAIL;
skipped with reason "BLOCKED: ..." → BLOCKED; skipped with reason
"NOT_RUN: ..." → NOT_RUN. Any other skip reason is recorded as NOT_RUN and
flagged for review — no silent skips.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from gordon_util import Cfg, Evidence, blocked

# Test-id → disposition record, consumed by the session finish summary.
OUTCOMES: dict[str, str] = {}


@pytest.fixture(scope="session")
def cfg() -> Cfg:
    return Cfg.from_env()


@pytest.fixture(scope="session")
def evidence(cfg: Cfg, tmp_path_factory) -> Evidence:
    root = cfg.evidence_dir
    try:
        root.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        root = tmp_path_factory.mktemp("evidence")
    return Evidence(root)


@pytest.fixture()
def rec(evidence: Evidence, request: pytest.FixtureRequest):
    """Per-test evidence recorder. Usage: rec.commands.append(run); rec.finish(...)"""

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


@pytest.fixture()
def scratch_home(cfg: Cfg, tmp_path: Path) -> Path:
    """Per-test scratch DSH_HOME. The directory must be writable by the
    service user; tmp_path is executor-owned, so chmod broadly (scratch only,
    never the candidate or the real home)."""
    home = tmp_path / "dsh-home"
    home.mkdir()
    tmp_path.chmod(0o777)
    home.chmod(0o777)
    return home


@pytest.fixture()
def scratch_env(scratch_home: Path) -> dict[str, str]:
    """env_extra routing the candidate fully into the scratch home."""
    return {"HOME": str(scratch_home), "DSH_HOME": str(scratch_home)}


@pytest.fixture()
def workspace(cfg: Cfg, tmp_path: Path) -> Path:
    """Per-test scratch working directory (the session cwd under test)."""
    ws = tmp_path / "workspace"
    ws.mkdir()
    ws.chmod(0o777)
    return ws


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    if report.passed:
        disposition = "PASS"
    elif report.failed:
        disposition = "FAIL"
    elif report.skipped:
        reason = ""
        if hasattr(report, "wasxfail"):
            reason = report.wasxfail
        elif isinstance(report.longrepr, tuple) and len(report.longrepr) >= 3:
            reason = str(report.longrepr[2])
        else:
            reason = str(report.longrepr)
        if "BLOCKED:" in reason:
            named = reason.split("BLOCKED:", 1)[1].strip()
            disposition = f"BLOCKED ({named[:120]})"
        elif "NOT_RUN:" in reason:
            disposition = "NOT_RUN (named)"
        else:
            disposition = f"NOT_RUN (unnamed skip — REVIEW): {reason[:120]}"
    else:
        disposition = "NOT_RUN"
    OUTCOMES[item.nodeid] = disposition


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if not OUTCOMES:
        return
    cfg = Cfg.from_env()
    try:
        out = cfg.evidence_dir / "pytest-outcomes.json"
        import json

        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(OUTCOMES, indent=2, sort_keys=True) + "\n")
    except OSError:
        pass


@pytest.fixture(scope="session")
def candidate_bin(cfg: Cfg) -> Path:
    path = Path(cfg.dsh_bin)
    if not path.exists():
        # Fall back to PATH discovery before declaring the dependency missing.
        found = shutil.which("dsh")
        if found:
            return Path(found)
        blocked(f"candidate binary not at {path} and no `dsh` on PATH (Morpheus handoff pending)")
    return path


@pytest.fixture(scope="session")
def source_tree(cfg: Cfg) -> Path:
    path = Path(cfg.dsh_src)
    if not (path / "package.json").exists():
        blocked(f"no source tree at {path} (GORDON_DSH_SRC); static gates cannot run")
    return path
