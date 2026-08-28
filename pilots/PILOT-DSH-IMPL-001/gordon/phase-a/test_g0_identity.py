"""Gate 0 — provenance and candidate identity (test plan §4).

The candidate is frozen here before any other gate runs (profile §8.3): the
live identity is discovered, recorded, and checked against the review
baseline. A drift at re-check voids the campaign (G0-07).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from gordon_util import (
    PINNED_NODE,
    PINNED_PACKAGE_JSON_SHA256,
    PINNED_PNPM,
    PINNED_PNPM_LOCK_SHA256,
    PINNED_VERSION,
    blocked,
    run_candidate,
    run_host,
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def test_g0_01_manifest_hashes(cfg, source_tree, rec):
    """G0-01: package.json + pnpm-lock.yaml hashes == profile §3 baseline."""
    pkg = _sha256(source_tree / "package.json")
    lock_path = source_tree / "pnpm-lock.yaml"
    if not lock_path.exists():
        blocked(f"{lock_path} absent from the on-host source tree")
    lock = _sha256(lock_path)
    observed = f"package.json={pkg} pnpm-lock.yaml={lock}"
    rec.artifact("hashes.txt", observed + "\n")
    ok = pkg == PINNED_PACKAGE_JSON_SHA256 and lock == PINNED_PNPM_LOCK_SHA256
    rec.finish(
        "PASS" if ok else "FAIL",
        "profile §3 pinned manifest hashes",
        observed,
    )
    assert ok, observed


def test_g0_02_manifest_fields(cfg, source_tree, rec):
    """G0-02: version, packageManager, engines == pinned manifest values."""
    root = json.loads((source_tree / "package.json").read_text())
    cli = json.loads((source_tree / "apps/cli/package.json").read_text())
    observed = {
        "root_version": root.get("version"),
        "cli_version": cli.get("version"),
        "packageManager": root.get("packageManager"),
        "engines_node": (root.get("engines") or {}).get("node"),
        "cli_bin": (cli.get("bin") or {}).get("dsh"),
    }
    rec.artifact("manifest-fields.json", json.dumps(observed, indent=2))
    ok = (
        observed["root_version"] == PINNED_VERSION
        and observed["cli_version"] == PINNED_VERSION
        and observed["packageManager"] == f"pnpm@{PINNED_PNPM}"
        and observed["engines_node"] == "^22.19.0 || >=24.0.0"
        and observed["cli_bin"] == "lib/bin.js"
    )
    rec.finish("PASS" if ok else "FAIL", "pinned root + apps/cli package.json", json.dumps(observed))
    assert ok, observed


def test_g0_03_runtime_versions(cfg, rec):
    """G0-03: Node v24.20.0 and pnpm 11.7.0 on host paths."""
    node = run_host([cfg.node, "--version"])
    rec.commands.append(node)
    observed = f"node={node.stdout.strip()}"
    pnpm_ok = True
    if Path(cfg.pnpm).exists():
        pnpm = run_host([cfg.pnpm, "--version"])
        rec.commands.append(pnpm)
        observed += f" pnpm={pnpm.stdout.strip()}"
        pnpm_ok = pnpm.stdout.strip() == PINNED_PNPM
    else:
        observed += " pnpm=ABSENT-AT-PINNED-PATH"
        pnpm = run_host(["pnpm", "--version"])
        rec.commands.append(pnpm)
        if pnpm.exit_code == 0:
            observed += f" (PATH pnpm={pnpm.stdout.strip()})"
            pnpm_ok = pnpm.stdout.strip() == PINNED_PNPM
    ok = node.stdout.strip() == PINNED_NODE and pnpm_ok
    rec.finish("PASS" if ok else "FAIL", "plan facts + rick prep receipt", observed)
    assert ok, observed


def test_g0_04_dsh_version(cfg, candidate_bin, scratch_env, rec):
    """G0-04: `dsh --version` prints the pinned package version."""
    run = run_candidate(cfg, ["--version"], env_extra=scratch_env)
    rec.commands.append(run)
    observed = run.stdout.strip()
    ok = run.exit_code == 0 and observed == PINNED_VERSION
    rec.finish("PASS" if ok else "FAIL", "apps/cli/src/bin.ts readVersion + pinned apps/cli/package.json", observed)
    assert ok, observed


def test_g0_05_identity_freeze(cfg, candidate_bin, evidence, rec):
    """G0-05: discover and freeze the live candidate identity (§8.3)."""
    identity = {
        "dsh_bin": str(candidate_bin),
        "dsh_root": cfg.dsh_root,
        "dsh_src": cfg.dsh_src,
        "real_home": cfg.values["GORDON_REAL_HOME"],
        "service_user": cfg.dsh_user,
        "service_uid": cfg.dsh_uid,
        "review_baseline_version": PINNED_VERSION,
    }
    listing = run_host(["ls", "-la", cfg.dsh_root], timeout=30)
    rec.commands.append(listing)
    rec.artifact("install-root-ls.txt", listing.stdout + listing.stderr)
    id_run = run_host(["id", cfg.dsh_user], timeout=30)
    rec.commands.append(id_run)
    identity["id_dsh"] = id_run.stdout.strip()
    evidence.set_identity(identity)
    ok = listing.exit_code == 0 and id_run.exit_code == 0
    rec.finish(
        "PASS" if ok else "FAIL",
        "profile §8.3 freeze rule",
        f"identity frozen: {json.dumps(identity)}",
    )
    assert ok


def test_g0_06_service_user_confinement(cfg, rec):
    """G0-06: dsh is uid 999 and holds no sudo."""
    id_run = run_host(["id", "-u", cfg.dsh_user], timeout=30)
    rec.commands.append(id_run)
    uid_ok = id_run.stdout.strip() == cfg.dsh_uid
    sudo_probe = run_host(
        ["su", "-s", "/bin/bash", cfg.dsh_user, "-c", "sudo -n true"],
        timeout=30,
    )
    rec.commands.append(sudo_probe)
    observed = f"uid={id_run.stdout.strip()} sudo_probe_exit={sudo_probe.exit_code}"
    ok = uid_ok and sudo_probe.exit_code != 0
    rec.finish("PASS" if ok else "FAIL", "plan key context; rick prep receipt", observed)
    assert ok, observed


def test_g0_07_tree_fingerprint(cfg, candidate_bin, rec):
    """G0-07: fingerprint install + source trees for the end-of-campaign drift check."""
    targets = [p for p in [cfg.dsh_root, cfg.dsh_src] if Path(p).exists()]
    if not targets:
        blocked("neither GORDON_DSH_ROOT nor GORDON_DSH_SRC exists on host")
    digest = hashlib.sha256()
    count = 0
    for target in targets:
        for path in sorted(Path(target).rglob("*")):
            if path.is_file() and not path.is_symlink() and "node_modules" not in path.parts:
                try:
                    digest.update(str(path).encode())
                    digest.update(path.read_bytes())
                    count += 1
                except OSError:
                    continue
    fp = f"{digest.hexdigest()} files={count}"
    rec.artifact("tree-fingerprint.txt", fp + "\n")
    rec.finish("PASS", "profile §5: a moving candidate voids results", fp,
               note="re-verify at campaign end; drift = stop + escalate")
