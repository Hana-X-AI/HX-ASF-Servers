#!/usr/bin/env python3
"""skills_registry.py — prove the skill set is real, not just named (O7).

SY-3 (skills_sync.py) proves the mirrors are byte-identical copies. It executes
nothing and reads no frontmatter, which is why `goal-decompose` shipped a SKILL.md
documenting four scripts in an empty `scripts/` directory: everything it claimed
was mirrored faithfully, and none of it existed. Anyone following the skill got
"No such file or directory".

This check answers the questions SY-3 cannot:

  SK-01/02  does every skill declare the fields a registry needs?
  SK-03     does every file a skill declares as required actually exist?
  SK-04     do two skills claim the same owner trigger word?
  SK-05     does the AGENTS.md inventory reconcile 1:1 with .agents/skills/?
  SK-06     does each active skill's smoke command still succeed?

WHERE THE DATA LIVES, AND WHY
`AGENTS.md` §"Skills and trigger words" is ratified as THE global skill
inventory (KDD-0020 D3: "this section IS the global skill inventory"). Owner and
trigger words are therefore read FROM it and are deliberately NOT duplicated
into frontmatter — a second copy would need its own sync check and would be a
second authority plane for the same fact, which is the defect this whole
optimization set exists to remove.

Frontmatter carries only what the inventory cannot know: `maturity`,
`required_files`, and `smoke`.

This mechanizes KDD-0020 Amendment 2 item 1, which that amendment recorded as
"NOT yet mechanized — the 30/30/30 reconciliation was performed manually".

Usage:
    python3 scripts/skills_registry.py [--smoke] [--json]

`--smoke` executes each active skill's smoke command. Off by default so the
check stays fast and side-effect-free for validate.py; CI runs it explicitly.

`plan()` returns (summary, problems), matching skills_sync.plan() and
hooks_verify.plan() so validate.py folds all three in identically.
"""

import json
import os
import re
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANONICAL = os.path.join(ROOT, ".agents", "skills")
AGENTS_MD = os.path.join(ROOT, "AGENTS.md")

REQUIRED_FIELDS = ("name", "description", "maturity")
MATURITY = ("proposed", "pilot", "active", "deprecated")

# - **name** — owner trigger: **"a" / "b"**.
# - **name** (Owner) — owner trigger: **"a"**.        (the QA skills carry a lane owner)
INVENTORY_RE = re.compile(
    r'^- \*\*([a-z0-9-]+)\*\*(?:\s*\(([^)]+)\))?\s*— owner trigger:\s*\*\*(.+?)\*\*\.',
    re.M | re.S)


def inventory():
    """{name: {owner, triggers}} parsed from the ratified AGENTS.md section."""
    with open(AGENTS_MD, encoding="utf-8") as fh:
        text = fh.read()
    if "## Skills and trigger words" not in text:
        return {}
    section = text.split("## Skills and trigger words", 1)[1].split("\n## ", 1)[0]
    out = {}
    for name, owner, raw in INVENTORY_RE.findall(section):
        triggers = [t.strip().lower()
                    for t in re.findall(r'"([^"]+)"', re.sub(r"\s+", " ", raw))]
        out[name] = {"owner": (owner or "").strip() or None, "triggers": triggers}
    return out


def frontmatter(path):
    """(dict_or_None, error_or_None) for one SKILL.md."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith("---"):
        return None, "no YAML frontmatter"
    try:
        end = text.index("\n---", 3)
    except ValueError:
        return None, "frontmatter block is not closed"
    try:
        data = yaml.safe_load(text[3:end])
    except Exception as e:
        return None, "frontmatter is not valid YAML: %s" % e
    if not isinstance(data, dict):
        return None, "frontmatter is not a mapping"
    return data, None


def skills():
    return sorted(d for d in os.listdir(CANONICAL)
                  if os.path.isdir(os.path.join(CANONICAL, d)))


RUNNABLE_SUFFIXES = (".sh", ".mjs", ".js", ".py")


def _ships_executable(name, fm):
    """True when a required file is a script or carries the exec bit."""
    for req in (fm.get("required_files") or []):
        path = os.path.join(CANONICAL, name, str(req))
        if str(req).endswith(RUNNABLE_SUFFIXES) or (
                os.path.isfile(path) and os.access(path, os.X_OK)):
            return True
    return False


def _run_smoke(name, command, problems):
    try:
        proc = subprocess.run(command, shell=True, cwd=ROOT, timeout=120,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except subprocess.TimeoutExpired:
        problems.append("[SK-06] %s: smoke timed out after 120s" % name)
        return False
    if proc.returncode != 0:
        tail = proc.stdout.decode("utf-8", "replace").strip().splitlines()
        problems.append("[SK-06] %s: smoke exited %d — %s"
                        % (name, proc.returncode, tail[-1] if tail else "no output"))
        return False
    return True


def plan(run_smoke=False):
    """Return (summary, problems)."""
    problems = []
    inv = inventory()
    names = skills()
    seen_triggers = {}
    smoked = skipped = 0

    for name in names:
        rel = os.path.join(".agents", "skills", name, "SKILL.md")
        path = os.path.join(CANONICAL, name, "SKILL.md")
        if not os.path.isfile(path):
            problems.append("[SK-01] %s: no SKILL.md" % name)
            continue
        fm, err = frontmatter(path)
        if err:
            problems.append("[SK-01] %s: %s" % (rel, err))
            continue
        for field in REQUIRED_FIELDS:
            if not fm.get(field):
                problems.append("[SK-02] %s: required frontmatter field %r missing"
                                % (rel, field))
        if fm.get("name") and fm["name"] != name:
            problems.append("[SK-02] %s: frontmatter name %r does not match its directory"
                            % (rel, fm["name"]))
        if fm.get("maturity") and fm["maturity"] not in MATURITY:
            problems.append("[SK-02] %s: maturity %r not in %s"
                            % (rel, fm["maturity"], list(MATURITY)))

        # SK-03 — the goal-decompose defect: a skill that documents files it
        # does not ship. Mirroring copies the claim faithfully either way.
        for req in (fm.get("required_files") or []):
            if not os.path.isfile(os.path.join(CANONICAL, name, str(req))):
                problems.append("[SK-03] %s: required_files entry does not exist: %s"
                                % (name, req))

        # SK-04 — two skills answering the same word is ambiguous dispatch.
        for trig in inv.get(name, {}).get("triggers", []):
            if trig in seen_triggers and seen_triggers[trig] != name:
                problems.append("[SK-04] trigger %r is claimed by both %s and %s"
                                % (trig, seen_triggers[trig], name))
            seen_triggers[trig] = name

        if run_smoke and fm.get("maturity") == "active":
            cmd = fm.get("smoke")
            if cmd:
                if _run_smoke(name, cmd, problems):
                    smoked += 1
            else:
                # A skill that ships something RUNNABLE must either smoke it or
                # say in writing why it cannot. Reference material — a format
                # doc, an agents/openai.yaml — has nothing to execute, so
                # demanding a skip reason for it would be boilerplate that
                # teaches a reader nothing.
                if _ships_executable(name, fm) and not fm.get("smoke_skip_reason"):
                    problems.append("[SK-06] %s: ships an executable but declares no "
                                    "smoke and no smoke_skip_reason" % name)
                skipped += 1

    # SK-05 — KDD-0020 Amendment 2 item 1. Nothing read AGENTS.md before this;
    # the 30/30 match was maintained by hand and true only by coincidence.
    missing = sorted(set(names) - set(inv))
    extra = sorted(set(inv) - set(names))
    for m in missing:
        problems.append("[SK-05] %s exists in .agents/skills/ but is not in the "
                        "AGENTS.md inventory" % m)
    for e in extra:
        problems.append("[SK-05] %s is in the AGENTS.md inventory but has no "
                        ".agents/skills/ directory" % e)

    summary = ("skills-registry: %d skills, inventory %d/%d reconciled, %d trigger words"
               % (len(names), len(inv) - len(extra), len(names), len(seen_triggers)))
    if run_smoke:
        summary += "; smoke %d run, %d declined" % (smoked, skipped)
    return summary, problems


def main(argv):
    run_smoke = "--smoke" in argv
    summary, problems = plan(run_smoke=run_smoke)
    if "--json" in argv:
        print(json.dumps({"summary": summary, "problems": problems}, indent=2))
        return 1 if problems else 0
    for p in problems:
        print(p)
    print(summary)
    if problems:
        print("skills-registry: %d problem(s)" % len(problems))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
