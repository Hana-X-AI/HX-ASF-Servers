#!/usr/bin/env python3
"""HX-ASF-Servers single local validation command.

Purpose
-------
One read-only repo-root command that runs every mechanized check the factory
has ratified, and honestly labels the checks that remain human judgment as
MANUAL GATE lines. It consolidates: the wiki dual-format sync check, the
fixture regression suite + hash manifest, the catalog mechanical battery
(CAT-01/03/04/07/08 per knowledge/catalog/tests/cat-001-acceptance.md), and
the generic secret-boundary sweep.

Ratification
------------
Owner decisions UD1 (validation contract: one read-only repo-root command,
honest MANUAL GATE labels) and UD2 (bounded implementation of this script),
2026-08-25 — pilot state log row 60 (pilots/PILOT-HX1-OLLAMA-QWEN27B-001/
09-state-log.md); unified recommendations U1/U2.

Read-only contract
------------------
This command NEVER writes, formats, renders, catalogs, or otherwise mutates
the repository or anything outside it. It only checks and reports. All child
Python processes run with -B and PYTHONDONTWRITEBYTECODE=1 (no .pyc writes);
sha256sum -c is verify-only; catalog/YAML files are opened read-only. It never
reads protected credential material — the literal-credential sweep against the
protected ssh-info file is a governor-only MANUAL GATE and is deliberately NOT
part of this command.

Exit codes
----------
  0  every mechanized check PASS (manual gates are noted, never graded)
  1  any mechanized check FAIL
  2  usage error (bad arguments, or a --changed path outside / not in the repo)

Usage
-----
  python3 scripts/validate.py                  full-repo validation (default)
  python3 scripts/validate.py --changed P [P..]  scoped validation of changed
                                               repo-relative (or absolute)
                                               paths:
      wiki manifest member  -> wiki-sync check
      pilot fixtures file   -> fixture-suite check
      knowledge/catalog/**  -> catalog-mechanical check
      anything else         -> secret-boundary sweep on that file

Hook rule
---------
Hooks (U3 advisory validation hook, U5 secret-boundary hook, and any future
gate) MUST call THIS command rather than reimplementing individual checks —
one contract, one place to fix a check. Deterministic: same tree, same result.
"""
import glob
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES_DIR = os.path.join("pilots", "PILOT-HX1-OLLAMA-QWEN27B-001", "fixtures")
CATALOG_DIR = os.path.join("knowledge", "catalog")
WIKI_MANIFEST = os.path.join("scripts", "wiki", "manifest.txt")
# Canonical skill tree first; the rest are its tool-scope mirrors (SY-3).
SKILL_TREES = (os.path.join(".agents", "skills"),
               os.path.join(".kimi-code", "skills"),
               os.path.join(".claude", "skills"))

DOC_ID_RE = re.compile(r"^DOC-[a-z0-9]+(-[a-z0-9]+)*$")
URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")

# Generic high-signal secret patterns only (UD1: no literal-credential sweep
# here). Tuned so prose ("passwordless sudo", "a hash of a secret is...",
# receipts' historical REDACTED mentions) does not match.
SECRET_PATTERNS = [
    ("private-key block", re.compile(r"BEGIN [A-Z0-9 ]*PRIVATE KEY")),
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Slack token", re.compile(r"xox[baprs]-")),
    ("GitHub PAT", re.compile(r"ghp_[0-9A-Za-z]{36}")),
    ("password assignment", re.compile(r"(?i)\bpassword\s*[:=]\s*\S+")),
]
SECRET_SKIP_DIRS = {".git", "__pycache__"}

MANUAL_GATES = [
    ("CAT-10..15", "known-answer retrieval (owner-ratified golden-question "
                   "corpus) — judgment: correctness + source refs + freshness "
                   "labels; run by the governor per cat-001-acceptance.md"),
    ("CAT-20..22", "judgment checks (freshness audit, conflict preservation, "
                   "retrieval-package economy) — not mechanizable"),
    ("CB-01", "write-set audit — needs run-window context (what the session "
              "was authorized to touch); run by the governor at handoff"),
    ("literal-credential sweep", "governor-only check against the protected "
                                 "ssh-info file; NEVER part of this command "
                                 "(protected content is never read here)"),
]

MAX_FINDINGS_SHOWN = 20


class Check:
    def __init__(self, name):
        self.name = name
        self.ok = True
        self.detail = []    # summary lines (always printed)
        self.findings = []  # failure lines (printed on FAIL, capped)

    def fail(self, msg):
        self.ok = False
        self.findings.append(msg)

    def render(self):
        status = "PASS" if self.ok else "FAIL"
        lines = ["%s  %s — %s" % (status, self.name, self.detail[0] if self.detail else "")]
        lines.extend("        " + d for d in self.detail[1:])
        if not self.ok:
            shown = self.findings[:MAX_FINDINGS_SHOWN]
            lines.extend("  FAIL  " + f for f in shown)
            if len(self.findings) > MAX_FINDINGS_SHOWN:
                lines.append("  FAIL  ... and %d more" % (len(self.findings) - MAX_FINDINGS_SHOWN))
        return lines


def _env():
    return dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


# ---------------------------------------------------------------- check 1: wiki
def check_wiki():
    c = Check("wiki-sync")
    p = subprocess.run([sys.executable, "-B", os.path.join("scripts", "wiki", "render.py"), "--check"],
                       cwd=ROOT, env=_env(), capture_output=True, text=True)
    out = p.stdout.splitlines()
    total = len(out)
    ok = sum(1 for l in out if l.split(None, 1) and l.split(None, 1)[0] == "OK")
    c.detail.append("render.py --check: %d/%d manifest documents in sync" % (ok, total))
    if p.returncode != 0:
        for l in out:
            if l.split(None, 1) and l.split(None, 1)[0] != "OK":
                c.fail(l.strip())
        c.fail("render.py --check exited %d" % p.returncode)
    return c


# ------------------------------------------- repo-layout invariants (SY-2/SY-3)
# Two canonical-path invariants share this check because they are the same class
# of failure: a second tree quietly forking a canonical one.
#   SY-2  governace/ (owner-sanctioned spelling) is CANONICAL. governance/ is the
#         rejected fork and must never exist.
#   SY-3  .agents/skills/ is the CANONICAL skill tree (KDD-0020). The tool-scope
#         mirrors .kimi-code/skills/ and .claude/skills/ must match it exactly,
#         or an agent reads a stale skill depending on which harness launched it.
# SY-3 delegates to scripts/skills_sync.py rather than reimplementing the
# comparison — the same single-source rule the hooks follow.
def check_governance_path():
    c = Check("governance-path")
    canonical = os.path.join(ROOT, "governace")
    fork = os.path.join(ROOT, "governance")
    if os.path.isdir(fork):
        c.fail("[SY-2] fork exists: %s (canonical spelling is governace/)" % fork)
    if not os.path.isdir(canonical):
        c.fail("[SY-2] canonical governance tree missing: %s" % canonical)
    sy2_ok = c.ok

    problems, skills, mirrors = [], [], []
    try:
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import skills_sync
        mirrors = list(skills_sync.MIRRORS)
        stub_only = ", ".join(skills_sync.STUB_ONLY)
        problems, skills = skills_sync.plan()
    except Exception as e:  # a broken sync module must not pass vacuously
        c.fail("[SY-3] skills_sync unavailable: %s" % e)
        stub_only = "unknown"
    finally:
        if sys.path and sys.path[0] == os.path.join(ROOT, "scripts"):
            sys.path.pop(0)
    for p in problems:
        c.fail(p)

    if c.ok:
        c.detail.append("SY-2 governace/ canonical, governance/ fork absent; "
                        "SY-3 %d skills canonical at .agents/skills/, %d tool-scope "
                        "mirrors in sync (%s stub-only)"
                        % (len(skills), len(mirrors), stub_only))
    else:
        # Per-file findings are capped by MAX_FINDINGS_SHOWN, so name the
        # affected mirror roots here — this line always prints, and it is what
        # tells the reader WHERE to look when the finding list is truncated.
        by_mirror = []
        for m in mirrors:
            n = sum(1 for p in problems if (" %s/" % m) in p or p.endswith(" %s" % m))
            if n:
                by_mirror.append("%s (%d)" % (m, n))
        where = "; drifted: " + ", ".join(by_mirror) if by_mirror else ""
        c.detail.append("repo-layout invariants failed — SY-2 %s, SY-3 %d problem(s)%s"
                        % ("OK" if sy2_ok else "FAIL", len(problems), where))
        c.detail.append("skills repair: python3 scripts/skills_sync.py --write "
                        "(canonical .agents/skills/ is authoritative; mirrors are rebuilt from it)")
    return c


# ----------------------------------------------------------- check 2: fixtures
def check_fixtures():
    c = Check("fixture-suite")
    p1 = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q", "test_fixtures.py"],
                        cwd=os.path.join(ROOT, FIXTURES_DIR), env=_env(),
                        capture_output=True, text=True)
    m = re.search(r"Ran (\d+) test", p1.stderr)
    ran = m.group(1) if m else "?"
    ut_ok = p1.returncode == 0 and re.search(r"^OK", p1.stderr, re.M) is not None
    if not ut_ok:
        c.fail("unittest exited %d: %s" % (p1.returncode, (p1.stderr.strip().splitlines() or [""])[-1]))
    # GNU sha256sum -c exits 0 on improperly formatted manifest lines (it only
    # warns and skips them), so strictness is enforced here: every manifest
    # entry must verify, warnings and short counts are failures.
    with open(os.path.join(ROOT, FIXTURES_DIR, "sha256sums.txt"), encoding="utf-8") as fh:
        expected = sum(1 for l in fh if l.strip())
    p2 = subprocess.run(["sha256sum", "-c", "sha256sums.txt"],
                        cwd=os.path.join(ROOT, FIXTURES_DIR), env=_env(),
                        capture_output=True, text=True)
    lines = [l for l in p2.stdout.splitlines() if l.strip()]
    ok_n = sum(1 for l in lines if l.rstrip().endswith(": OK"))
    bad = [l for l in lines if not l.rstrip().endswith(": OK")]
    if p2.returncode != 0:
        for l in bad or ["sha256sum -c exited %d" % p2.returncode]:
            c.fail("hash manifest: %s" % l)
    for w in p2.stderr.splitlines():
        if w.strip():
            c.fail("hash manifest: %s" % w.strip())
    if ok_n != expected:
        c.fail("hash manifest: %d/%d entries verified — every manifest entry must verify" % (ok_n, expected))
    c.detail.append("unittest %s tests OK; sha256sums %d/%d verified" % (ran, ok_n, expected))
    return c


# ------------------------------------------------------------ check 3: catalog
def _load_yaml(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def check_catalog(portable=False):
    c = Check("catalog-mechanical")
    cat = os.path.join(ROOT, CATALOG_DIR)
    try:
        schema = _load_yaml(os.path.join(cat, "schema.yaml"))
        fields = schema["schema"]["fields"]
        required = [k for k, v in fields.items() if isinstance(v, dict) and v.get("required") is True]
        enums = {
            "type": fields["type"]["enum"],
            "status": fields["status"]["enum"],
            "authority_level": fields["authority_level"]["enum"],
            "security.classification": fields["security"]["fields"]["classification"]["enum"],
            "validation.freshness": fields["validation"]["fields"]["freshness"]["enum"],
            "relations predicate": fields["relations"]["item"]["predicate"]["enum"],
        }
        line_fields = schema["index"]["line_fields"]
    except Exception as e:  # schema itself broken: everything downstream is moot
        c.fail("[CAT-01] schema.yaml unreadable: %s" % e)
        c.detail.append("schema.yaml unreadable")
        return c

    files = sorted(glob.glob(os.path.join(cat, "documents", "DOC-*.yaml")))
    records = {}   # id -> (relpath, record)
    for path in files:
        rel = os.path.relpath(path, ROOT)
        try:
            doc = _load_yaml(path)
        except Exception as e:
            c.fail("[CAT-01] %s: YAML parse error: %s" % (rel, e))
            continue
        rec = doc.get("document") if isinstance(doc, dict) else None
        if not isinstance(rec, dict):
            c.fail("[CAT-01] %s: no 'document' mapping at root" % rel)
            continue
        rid = str(rec.get("id", ""))
        for f in required:
            if f not in rec or rec[f] is None:
                c.fail("[CAT-01] %s: required field %r missing" % (rel, f))
        if not DOC_ID_RE.match(rid):
            c.fail("[CAT-01] %s: id %r is not DOC-<kebab-case>" % (rel, rid))
        if rid in records:
            c.fail("[CAT-03] %s: duplicate id %s (also in %s)" % (rel, rid, records[rid][0]))
        records[rid] = (rel, rec)
        for key, allowed in (("type", enums["type"]), ("status", enums["status"]),
                             ("authority_level", enums["authority_level"])):
            if key in rec and rec[key] not in allowed:
                c.fail("[CAT-01] %s: %s %r not in schema enum" % (rel, key, rec[key]))
        sec = rec.get("security") or {}
        if "classification" in sec and sec["classification"] not in enums["security.classification"]:
            c.fail("[CAT-01] %s: security.classification %r not in schema enum" % (rel, sec["classification"]))
        val = rec.get("validation") or {}
        if "freshness" in val and val["freshness"] not in enums["validation.freshness"]:
            c.fail("[CAT-01] %s: validation.freshness %r not in schema enum" % (rel, val["freshness"]))
        if not (rec.get("source") or {}).get("section"):
            c.fail("[CAT-01] %s: source.section missing (provenance anchor required)" % rel)
        for i, reln in enumerate(rec.get("relations") or []):
            pred = (reln or {}).get("predicate")
            tgt = str((reln or {}).get("target", "")).strip()
            if pred not in enums["relations predicate"]:
                c.fail("[CAT-01] %s: relations[%d] predicate %r not in schema enum" % (rel, i, pred))
            if not tgt:
                c.fail("[CAT-01] %s: relations[%d] has no target" % (rel, i))

    # CAT-03: index 1:1 — id sets exact, structured line fields exact.
    # Index titles are a maintained compressed lookup surface (5/175 differ in
    # wording from record titles at ratification time); title exact-match is
    # reported informationally, not graded. All other line fields are graded.
    idx_doc = _load_yaml(os.path.join(cat, "index.yaml"))
    idx_lines = (idx_doc or {}).get("index", {}).get("documents", []) or []
    idx_by_id = {}
    for ln in idx_lines:
        if not isinstance(ln, dict) or "id" not in ln:
            c.fail("[CAT-03] index.yaml: line without id: %r" % (ln,))
            continue
        for f in line_fields:
            if f not in ln:
                c.fail("[CAT-03] index.yaml %s: line field %r missing" % (ln["id"], f))
        idx_by_id[str(ln["id"])] = ln
    for rid in sorted(set(idx_by_id) - set(records)):
        c.fail("[CAT-03] index line %s has no documents/ file (dangling)" % rid)
    for rid in sorted(set(records) - set(idx_by_id)):
        c.fail("[CAT-03] %s missing from index.yaml (orphan)" % records[rid][0])
    titles_exact = 0
    graded = 0
    for rid, ln in sorted(idx_by_id.items()):
        if rid not in records:
            continue
        rec = records[rid][1]
        pairs = {"type": rec.get("type"),
                 "authority_level": rec.get("authority_level"),
                 "freshness": (rec.get("validation") or {}).get("freshness"),
                 "canonical_location": rec.get("canonical_location")}
        for f, v in pairs.items():
            graded += 1
            if str(ln.get(f)) != str(v):
                c.fail("[CAT-03] index %s: %s %r != record %r" % (rid, f, ln.get(f), v))
        if str(ln.get("title")) == str(rec.get("title")):
            titles_exact += 1

    # CAT-04: relation targets that are DOC ids resolve to existing records.
    unresolved = 0
    for rid, (rel, rec) in sorted(records.items()):
        for reln in rec.get("relations") or []:
            tgt = str((reln or {}).get("target", "")).strip()
            if DOC_ID_RE.match(tgt) and tgt not in records:
                unresolved += 1
                c.fail("[CAT-04] %s: relation target %s does not resolve" % (rel, tgt))

    # CAT-07: every canonical_location exists on disk. Exempt: pure external
    # URLs, and protected-resource records (access-restricted locations carry a
    # flagged, explained note in the record itself; never stat protected paths).
    loc_checked = loc_url = loc_protected = loc_skipped = 0
    canon_locations = set()
    for rid, (rel, rec) in sorted(records.items()):
        loc = str(rec.get("canonical_location", "")).strip()
        canon_locations.add(os.path.normpath(loc))
        if loc.startswith("/"):
            canon_locations.add(os.path.normpath(loc))
        else:
            canon_locations.add(os.path.normpath(os.path.join(ROOT, loc)))
        if URL_RE.match(loc):
            loc_url += 1
        elif rec.get("type") == "protected-resource":
            loc_protected += 1
        else:
            loc_checked += 1
            probe = loc if os.path.isabs(loc) else os.path.join(ROOT, loc)
            if portable:
                # --ci: canonical_location is anchored to the governor host by
                # design (repo home + /opt/tkv-local); existence is unverifiable
                # off-host, so the probe is skipped, not failed.
                loc_skipped += 1
            elif not os.path.exists(probe):
                c.fail("[CAT-07] %s: canonical_location does not resolve: %s" % (rel, loc))

    # CAT-08: raw-path relation targets. A target is a raw path when it is a
    # bare filesystem path (contains '/', no spaces, not a DOC id) — prose
    # entity names that merely contain '/' are free-entity targets per schema.
    # Violation: the path points at a cataloged artifact (must be a DOC id),
    # or the raw path carries no explanatory note (cat-001 pass rule).
    raw_total = raw_noted = 0
    for rid, (rel, rec) in sorted(records.items()):
        for reln in rec.get("relations") or []:
            tgt = str((reln or {}).get("target", "")).strip()
            if "/" not in tgt or " " in tgt or DOC_ID_RE.match(tgt):
                continue
            raw_total += 1
            cands = {os.path.normpath(tgt), os.path.normpath(os.path.join(ROOT, tgt))}
            if cands & canon_locations:
                c.fail("[CAT-08] %s: raw-path target %r points at a cataloged artifact — use its DOC id" % (rel, tgt))
            elif str((reln or {}).get("note", "")).strip():
                raw_noted += 1
            else:
                c.fail("[CAT-08] %s: raw-path target %r without explanatory note" % (rel, tgt))

    n = len(records)
    c.detail.append("%d records: schema/required/enums/source.section OK; "
                    "index 1:1 (%d ids, %d structured line-field values exact; "
                    "titles exact %d/%d — %d compressed, informational)"
                    % (n, len(idx_by_id), graded, titles_exact, len(idx_by_id),
                       len(idx_by_id) - titles_exact))
    if portable:
        c.detail.append("relations resolve (CAT-04); CAT-07: existence probe "
                        "SKIPPED for %d locations (--ci portable mode — paths are "
                        "host-anchored by design; %d external URLs exempt, %d "
                        "protected-resource exempt); CAT-08 raw-path violations 0 "
                        "(%d raw-path targets, %d noted uncataloged)"
                        % (loc_skipped, loc_url, loc_protected, raw_total, raw_noted))
    else:
        c.detail.append("relations resolve (CAT-04); CAT-07: %d locations resolve "
                        "(%d external URLs exempt, %d protected-resource exempt); "
                        "CAT-08 raw-path violations 0 (%d raw-path targets, %d noted uncataloged)"
                        % (loc_checked, loc_url, loc_protected, raw_total, raw_noted))
    return c


def check_catalog_portable():
    return check_catalog(portable=True)


# -------------------------------------------------------- check 4: secret sweep
def _secret_scan(paths):
    hits, scanned = [], 0
    for path in paths:
        try:
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError:
            continue
        if b"\x00" in data:
            continue  # binary
        scanned += 1
        text = data.decode("utf-8", "replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, rx in SECRET_PATTERNS:
                if rx.search(line):
                    hits.append("%s:%d: %s pattern" % (os.path.relpath(path, ROOT), lineno, label))
    return hits, scanned


def check_secrets(scope_files=None):
    c = Check("secret-boundary")
    if scope_files is None:
        paths = []
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = sorted(d for d in dirs if d not in SECRET_SKIP_DIRS)
            for f in sorted(files):
                if f.endswith(".pyc"):
                    continue
                paths.append(os.path.join(base, f))
        scope_desc = "repo-wide"
    else:
        paths = sorted(scope_files)
        scope_desc = "scoped (%d file%s)" % (len(paths), "s" if len(paths) != 1 else "")
    hits, scanned = _secret_scan(paths)
    c.detail.append("%s: %d files scanned, %d hits" % (scope_desc, scanned, len(hits)))
    for h in hits:
        c.fail(h)
    return c


CHECKS_FULL = [check_wiki, check_governance_path, check_fixtures, check_catalog, check_secrets]


def _wiki_manifest_members():
    members = set()
    with open(os.path.join(ROOT, WIKI_MANIFEST), encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                members.add(os.path.normpath(line))
    return members


def scoped_checks(changed):
    """Map --changed paths to checks; returns (check_fns, sweep_files)."""
    wiki_members = _wiki_manifest_members()
    want = {"wiki": False, "layout": False, "fixtures": False, "catalog": False}
    sweep = []
    for p in changed:
        rel = os.path.normpath(os.path.relpath(p, ROOT)) if os.path.isabs(p) else os.path.normpath(p)
        if rel.startswith("..") or os.path.isabs(rel):
            raise ValueError("path outside repository: %s" % p)
        if not os.path.exists(os.path.join(ROOT, rel)):
            raise ValueError("path does not exist: %s" % p)
        if rel == os.path.normpath(WIKI_MANIFEST) or rel in wiki_members or \
                os.path.splitext(rel)[0] + ".md" in wiki_members:
            want["wiki"] = True                      # render.py --check covers all; it is fast
        elif rel.startswith(os.path.normpath(FIXTURES_DIR) + os.sep):
            want["fixtures"] = True
        elif rel.startswith(os.path.normpath(CATALOG_DIR) + os.sep):
            want["catalog"] = True
        elif any(rel.startswith(os.path.normpath(t) + os.sep) for t in SKILL_TREES):
            # A skill edit in any tree can desync the mirrors (SY-3); it is also
            # ordinary content, so it still gets the secret sweep.
            want["layout"] = True
            sweep.append(os.path.join(ROOT, rel))
        else:
            sweep.append(os.path.join(ROOT, rel))
    fns = []
    if want["wiki"]:
        fns.append(check_wiki)
    if want["layout"]:
        fns.append(check_governance_path)
    if want["fixtures"]:
        fns.append(check_fixtures)
    if want["catalog"]:
        fns.append(check_catalog)
    if sweep:
        fns.append(lambda: check_secrets(sweep))
    return fns


def main(argv):
    if not argv:
        mode = "full repo"
        fns = CHECKS_FULL
    elif argv[0] == "--changed" and len(argv) > 1:
        try:
            fns = scoped_checks(argv[1:])
        except ValueError as e:
            print("usage error: %s" % e, file=sys.stderr)
            return 2
        mode = "--changed (%d path%s)" % (len(argv) - 1, "s" if len(argv) > 2 else "")
        if not fns:
            print("usage error: no checkable paths given", file=sys.stderr)
            return 2
    elif argv[0] == "--ci":
        fns = [check_wiki, check_governance_path, check_fixtures, check_catalog_portable, check_secrets]
        mode = "ci (portable catalog: CAT-07 existence probe skipped — paths are host-anchored by design)"
    else:
        print("usage: python3 scripts/validate.py [--changed <path> [path...]] [--ci]", file=sys.stderr)
        return 2

    print("HX-ASF validate — read-only local validation (UD1/UD2, 2026-08-25) — mode: %s" % mode)
    failed = []
    for fn in fns:
        check = fn()
        for line in check.render():
            print(line)
        if not check.ok:
            failed.append(check.name)
    for gid, desc in MANUAL_GATES:
        print("MANUAL GATE  %s — %s" % (gid, desc))
    if failed:
        print("RESULT: FAIL — %s (exit 1)" % ", ".join(failed))
        return 1
    print("RESULT: PASS — %d/%d checks, %d manual gates noted (exit 0)"
          % (len(fns), len(fns), len(MANUAL_GATES)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
