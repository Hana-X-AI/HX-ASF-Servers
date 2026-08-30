#!/usr/bin/env python3
"""work_state.py — the single work-state engine for the HX factory (O1).

One implementation reads goal state. `work-status` and `goal-decompose` both
call this; neither reimplements parsing. Before this existed, each skill grepped
prose with its own regex, and both were wrong in different ways (see
governace/goals/work-state.schema.yaml for the two proven failure modes).

Commands:
    status        counts by status, plus any reconcile items
    in-progress   goals actively being worked
    next          goals ready to dispatch (approved, not blocked)
    blocked       goals blocked, with the reason
    standup       one-screen daily view
    reconcile     goals whose file and downstream evidence disagree
    --check       validate every goal against work-state.schema.yaml (exit 1 on failure)
    --json        machine output for any command above

Read-only. Stdlib + PyYAML (already a validate.py dependency). No network.
"""

import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOALS_DIR = os.path.join(ROOT, "governace", "goals")
SCHEMA = os.path.join(GOALS_DIR, "work-state.schema.yaml")

# ```yaml work-state ... ```  — the info string is what makes it addressable;
# a plain ```yaml block elsewhere in a goal must not be picked up.
BLOCK_RE = re.compile(r"^```yaml\s+work-state\s*$(.*?)^```\s*$", re.M | re.S)

SKIP = {"README.md", "_template.md"}


def _schema():
    with open(SCHEMA, encoding="utf-8") as fh:
        return yaml.safe_load(fh)["schema"]


def goal_files():
    out = []
    for p in sorted(glob.glob(os.path.join(GOALS_DIR, "*.md"))):
        if os.path.basename(p) not in SKIP:
            out.append(p)
    return out


def parse(path):
    """Return (state_dict_or_None, error_or_None) for one goal file."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    blocks = BLOCK_RE.findall(text)
    if not blocks:
        return None, "no ```yaml work-state block"
    if len(blocks) > 1:
        return None, "%d work-state blocks (exactly one required)" % len(blocks)
    try:
        data = yaml.safe_load(blocks[0])
    except Exception as e:
        return None, "work-state block is not valid YAML: %s" % e
    if not isinstance(data, dict):
        return None, "work-state block is not a mapping"
    return data, None


def load_all():
    """Return (states, problems). states = [(goal_id, dict)] sorted by id."""
    sch = _schema()
    required = [k for k, v in sch["fields"].items() if v.get("required")]
    enum = sch["fields"]["status"]["enum"]
    states, problems = [], []
    for p in goal_files():
        rel = os.path.relpath(p, ROOT)
        expect_id = os.path.basename(p)[:-3]
        data, err = parse(p)
        if err:
            problems.append("[WS-01] %s: %s" % (rel, err))
            continue
        for f in required:
            if f not in data or data[f] in (None, ""):
                problems.append("[WS-02] %s: required field %r missing" % (rel, f))
        if data.get("status") not in enum:
            problems.append("[WS-03] %s: status %r not in schema enum %s"
                            % (rel, data.get("status"), enum))
        if str(data.get("id", "")) != expect_id:
            problems.append("[WS-04] %s: id %r does not match filename %r"
                            % (rel, data.get("id"), expect_id))
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(data.get("status_date", ""))):
            problems.append("[WS-05] %s: status_date %r is not YYYY-MM-DD"
                            % (rel, data.get("status_date")))
        for ev in (data.get("evidence") or []):
            if not os.path.exists(os.path.join(ROOT, str(ev))):
                problems.append("[WS-06] %s: evidence path does not resolve: %s" % (rel, ev))
        states.append((expect_id, data))
    return states, problems


def _emit(rows, as_json, title, empty):
    if as_json:
        print(json.dumps(rows, indent=2))
        return 0
    print(title)
    print("=" * len(title))
    if not rows:
        print(empty)
        return 0
    for r in rows:
        print("\n  %s" % r["id"])
        print("     status   : %s (%s)" % (r["status"], r["status_date"]))
        print("     authority: %s" % r["authority"])
        if str(r.get("reconcile", "none")).lower() != "none":
            print("     RECONCILE: %s" % r["reconcile"])
    return 0


def main(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    cmd = argv[0] if argv else "status"

    states, problems = load_all()

    if cmd == "--check":
        for p in problems:
            print(p)
        if problems:
            print("work-state: %d problem(s) across %d goal(s)" % (len(problems), len(states)))
            return 1
        rec = sum(1 for _, s in states if str(s.get("reconcile", "none")).lower() != "none")
        print("work-state: %d goals valid against work-state.schema.yaml; "
              "%d carry an open reconcile item" % (len(states), rec))
        return 0

    if problems:
        # Report but do not hide them: a malformed block must never be reported
        # as though the goal simply had no work in progress.
        for p in problems:
            print("WARNING %s" % p, file=sys.stderr)

    rows = [dict(s, id=i) for i, s in states]
    sch = _schema()

    if cmd == "status":
        if as_json:
            print(json.dumps(rows, indent=2))
            return 0
        counts = {}
        for r in rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        print("Factory goal status")
        print("===================")
        print("Source: governace/goals/ (work-state blocks)\n")
        for st in sch["fields"]["status"]["enum"]:
            print("  %-12s %d" % (st, counts.get(st, 0)))
        print("\n  %-12s %d" % ("TOTAL", len(rows)))
        rec = [r for r in rows if str(r.get("reconcile", "none")).lower() != "none"]
        if rec:
            print("\n  %d goal(s) carry an open reconcile item — run: "
                  "python3 scripts/work_state.py reconcile" % len(rec))
        return 0

    sel = {
        "in-progress": lambda r: r["status"] == "in-progress",
        "next":        lambda r: r["status"] == "approved",
        "blocked":     lambda r: r["status"] == "blocked",
        "reconcile":   lambda r: str(r.get("reconcile", "none")).lower() != "none",
    }
    titles = {
        "in-progress": ("In-progress goals", "None in progress."),
        "next":        ("Ready to dispatch (approved)", "None ready — nothing is in `approved`."),
        "blocked":     ("Blocked goals", "None blocked."),
        "reconcile":   ("Goals needing reconciliation (governor decision)", "None — all goals agree with downstream evidence."),
    }
    if cmd in sel:
        return _emit([r for r in rows if sel[cmd](r)], as_json, *titles[cmd])

    if cmd == "standup":
        term = set(sch["terminal_statuses"])
        print("Daily standup — %d goals\n" % len(rows))
        for group, pred in (("In progress", lambda r: r["status"] == "in-progress"),
                            ("Blocked", lambda r: r["status"] == "blocked"),
                            ("Ready", lambda r: r["status"] == "approved"),
                            ("Closed", lambda r: r["status"] in term)):
            g = [r for r in rows if pred(r)]
            print("%s (%d)" % (group, len(g)))
            for r in g:
                print("   %-46s %s" % (r["id"], r["status"]))
            print("")
        rec = [r for r in rows if str(r.get("reconcile", "none")).lower() != "none"]
        if rec:
            print("Open reconcile items (%d):" % len(rec))
            for r in rec:
                print("   %-46s %s" % (r["id"], r["reconcile"]))
        return 0

    print("usage: python3 scripts/work_state.py "
          "[status|in-progress|next|blocked|standup|reconcile|--check] [--json]",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
