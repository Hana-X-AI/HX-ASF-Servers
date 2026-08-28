"""Gate 1 — static, build, and repository quality (test plan §5).

Every row runs against a byte-verified SCRATCH COPY of the source tree. The
candidate installation is never built, linted, or installed into: pnpm build
outputs stay inside the copy. The copy is made only after its manifest hashes
match the §3 baseline.

Profile §2: repository scripts are reviewed before first execution. The
review is a precondition recorded here; the commands themselves are the
pinned root package.json script names.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from gordon_util import blocked, run_host

REVIEW_NOTE = (
    "script review precondition: root package.json scripts and scripts/run-gates.ts "
    "reviewed at authoring against the pinned tree; re-review on any G0-07 drift"
)


@pytest.fixture(scope="module")
def scratch_copy(cfg, source_tree) -> Path:
    """Byte-verified scratch copy of the source tree (no node_modules)."""
    import hashlib

    from gordon_util import PINNED_PACKAGE_JSON_SHA256

    src_pkg = hashlib.sha256((source_tree / "package.json").read_bytes()).hexdigest()
    if src_pkg != PINNED_PACKAGE_JSON_SHA256:
        blocked("source tree manifest hash drifted from the §3 baseline before the G1 copy")
    dest = cfg.scratch / "g1-source-copy"
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source_tree,
        dest,
        ignore=shutil.ignore_patterns("node_modules", ".git", "lib", "*.tsbuildinfo"),
        symlinks=True,
    )
    # pnpm runs as the executor (test tooling) inside the copy; the candidate
    # tree is never touched.
    return dest


def _run_gate(cfg, copy: Path, rec, argv: list[str], timeout: float, oracle: str, ok_exit: int = 0):
    import os

    node_bin = str(Path(cfg.node).parent)
    run = run_host(
        argv,
        cwd=str(copy),
        timeout=timeout,
        env_extra={"CI": "true", "PATH": f"{node_bin}:{os.environ.get('PATH', '')}"},
    )
    rec.commands.append(run)
    observed = f"exit={run.exit_code}; stderr tail: {run.stderr[-600:]}"
    ok = run.exit_code == ok_exit
    rec.finish("PASS" if ok else "FAIL", oracle, observed, note=REVIEW_NOTE)
    assert ok, observed


def _pnpm(cfg, copy: Path) -> list[str]:
    pnpm = cfg.pnpm if Path(cfg.pnpm).exists() else shutil.which("pnpm")
    if not pnpm:
        blocked("no pnpm available (pinned path absent, none on PATH)")
    return [pnpm]


def test_g1_01_frozen_lockfile_install(cfg, scratch_copy, rec):
    """G1-01: pnpm install --frozen-lockfile succeeds against the pinned lockfile."""
    _run_gate(
        cfg, scratch_copy, rec,
        _pnpm(cfg, scratch_copy) + ["install", "--frozen-lockfile"],
        timeout=1800,
        oracle="pinned pnpm-lock.yaml; root package.json install script",
    )


def test_g1_02_typecheck(cfg, scratch_copy, rec):
    """G1-02: pnpm run typecheck."""
    _run_gate(cfg, scratch_copy, rec, _pnpm(cfg, scratch_copy) + ["run", "typecheck"],
              timeout=1800, oracle="root script: tsc -b tsconfig.host.json + client contracts")


def test_g1_03_lint(cfg, scratch_copy, rec):
    """G1-03: pnpm run lint (oxlint)."""
    _run_gate(cfg, scratch_copy, rec, _pnpm(cfg, scratch_copy) + ["run", "lint"],
              timeout=1800, oracle="root script: scripts/run-oxlint.ts over the tree")


def test_g1_04_build(cfg, scratch_copy, rec):
    """G1-04: pnpm run build produces lib/types and the bundled runtime."""
    _run_gate(cfg, scratch_copy, rec, _pnpm(cfg, scratch_copy) + ["run", "build"],
              timeout=2400, oracle="root script: tsx scripts/build.ts")
    bin_js = scratch_copy / "apps/cli/lib/bin.js"
    observed = f"apps/cli/lib/bin.js exists={bin_js.exists()}"
    ok = bin_js.exists()
    rec.finish("PASS" if ok else "FAIL", "apps/cli/package.json bin: lib/bin.js", observed)
    assert ok, observed


def test_g1_05_unit_tests(cfg, scratch_copy, rec):
    """G1-05: pnpm run test (keyless vitest unit tier). Skips recorded, not suppressed."""
    _run_gate(cfg, scratch_copy, rec, _pnpm(cfg, scratch_copy) + ["run", "test"],
              timeout=3600, oracle="root script vitest run; docs/testing.md unit tier")


def test_g1_06_snapshot_replay(cfg, scratch_copy, rec):
    """G1-06: pnpm run test:snapshot (keyless replay; fixtures replay on Linux)."""
    _run_gate(cfg, scratch_copy, rec, _pnpm(cfg, scratch_copy) + ["run", "test:snapshot"],
              timeout=3600, oracle="docs/testing.md snapshot tier; vitest.snapshot.config.ts")


def test_g1_07_hygiene(cfg, scratch_copy, rec):
    """G1-07: pnpm run hygiene (knip + publint + constraints + NodeNext check)."""
    _run_gate(cfg, scratch_copy, rec, _pnpm(cfg, scratch_copy) + ["run", "hygiene"],
              timeout=1800, oracle="root script: scripts/run-gates.ts hygiene")


def test_g1_08_built_bin_smoke(cfg, scratch_copy, rec):
    """G1-08: the built bin self-executes and prints the pinned version."""
    bin_js = scratch_copy / "apps/cli/lib/bin.js"
    if not bin_js.exists():
        blocked("apps/cli/lib/bin.js missing — G1-04 did not produce the bundle")
    run = run_host([cfg.node, str(bin_js), "--version"], cwd=str(scratch_copy), timeout=120)
    rec.commands.append(run)
    observed = run.stdout.strip()
    from gordon_util import PINNED_VERSION

    ok = run.exit_code == 0 and observed == PINNED_VERSION
    rec.finish("PASS" if ok else "FAIL", "apps/cli/src/bin.ts dispatch + readVersion", observed)
    assert ok, observed


def test_g1_09_repo_e2e_deferred(rec):
    """G1-09: repo real-API e2e is DEFERRED_BY_POLICY — it targets DeepSeek cloud
    (DEEPSEEK_API_KEY); the local-only doctrine bars cloud keys without an
    explicit owner word (00-goal.md boundaries). HX routed e2e is Gate 3."""
    rec.finish(
        "DEFERRED_BY_POLICY",
        "docs/testing.md e2e tier self-skips without keys; 00-goal.md local-only boundary",
        "not executed by policy",
        note="HX end-to-end provider proof runs through OmniRoute in Gate 3 instead",
    )
