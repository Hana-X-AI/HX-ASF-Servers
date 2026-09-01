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

import datetime
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

# A "current" status declaration in goal prose. Two forms are in use:
#   [Status transition 2026-08-29 [current]: COMPLETE ...
#   [CURRENT STATUS 2026-08-30, labeled ... PARTIAL / IN-PROGRESS: ...
# The block must not be older than the latest such declaration — a stale block
# is the exact "block says in-progress, prose says COMPLETE" defect WS-07 catches.
STATUS_MARKER_RE = re.compile(
    r"\[\s*(?:Status transition\s+(\d{4}-\d{2}-\d{2})\s*\[current\]|"
    r"CURRENT STATUS\s+(\d{4}-\d{2}-\d{2}))",
    re.I,
)

SKIP = {"README.md", "_template.md"}


def _schema():
    with open(SCHEMA, encoding="utf-8") as fh:
        return yaml.safe_load(fh)["schema"]


def goal_files():
    out = []
    for p in sorted(glob.glob(os.path.join(GOALS_DIR, "**", "*.md"),
                              recursive=True)):
        if os.path.basename(p) not in SKIP:
            out.append(p)
    return out


def _plain(value):
    """Coerce YAML scalars into JSON-safe primitives, recursively.

    `status_date: 2026-08-28` is unquoted in every goal file, so yaml.safe_load
    resolves it to datetime.date. The schema checks stringify it, so the state
    looked fine — but json.dumps does not, and every --json command died with
    "Object of type date is not JSON serializable". The state dict is the
    contract O2/O3/O8 consume, so it is normalized HERE, once, rather than at
    each consumer.
    """
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    return value


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
    return _plain(data), None


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
        # WS-07: a labeled "current" status declaration in the prose newer than
        # the block's status_date means the block was not advanced when the
        # prose was. This is the silent-drift class a `reconcile: none` let
        # through (hxs2-coderx and fleet-baseline, corrected 2026-08-31).
        try:
            with open(p, encoding="utf-8") as fh:
                prose = BLOCK_RE.sub("", fh.read())
            if re.match(r"^\d{4}-\d{2}-\d{2}$", str(data.get("status_date", ""))):
                block_date = datetime.date.fromisoformat(str(data["status_date"]))
                marker_dates = {
                    datetime.date.fromisoformat(d)
                    for m in STATUS_MARKER_RE.finditer(prose)
                    for d in m.groups() if d
                }
                if marker_dates:
                    latest = max(marker_dates)
                    if latest > block_date:
                        problems.append(
                            "[WS-07] %s: prose status declaration %s is newer than the "
                            "work-state block status_date %s — reconcile the block"
                            % (rel, latest.isoformat(), block_date.isoformat()))
        except (OSError, ValueError):
            pass
        states.append((expect_id, data))
    states.sort(key=lambda t: t[0])
    return states, problems


def _dump(rows):
    """One JSON writer. default=str is a backstop: parse() already normalizes
    the shapes we know about, so anything reaching here is a new YAML type that
    must still not crash a consumer mid-pipeline."""
    print(json.dumps(rows, indent=2, default=str))
    return 0


def _emit(rows, as_json, title, empty):
    if as_json:
        return _dump(rows)
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

    # A record whose `status` is absent or non-scalar cannot be counted,
    # grouped, or compared. Before this guard one such block raised KeyError
    # (missing status) or TypeError: unhashable type (list-valued status) and
    # took down EVERY status command with a traceback — one malformed goal
    # silencing the whole report, which is precisely the failure this engine
    # exists to prevent.
    #
    # load_all() deliberately still returns these records: validate.py needs
    # every problem, so the exclusion belongs here, in the rendering layer. It
    # is also deliberately NARROW — only unrenderable records are held back. A
    # goal whose sole problem is, say, a dangling evidence path still appears
    # in every report, because dropping it would recreate the "goal invisible
    # to a status report" defect from the other direction.
    excluded = [r for r in rows if not isinstance(r.get("status"), str)]
    if excluded:
        rows = [r for r in rows if isinstance(r.get("status"), str)]
        for r in excluded:
            print("WARNING [WS-03] %s: status %r cannot be rendered; excluded "
                  "from this report (run --check)" % (r["id"], r.get("status")),
                  file=sys.stderr)

    if cmd == "status":
        if as_json:
            return _dump(rows)
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
        pre = set(sch["pre_dispatch_statuses"])
        defs = [
            ("In progress", lambda r: r["status"] == "in-progress"),
            ("Blocked",     lambda r: r["status"] == "blocked"),
            ("Ready",       lambda r: r["status"] == "approved"),
            ("Draft",       lambda r: r["status"] in pre),
            ("Closed",      lambda r: r["status"] in term),
        ]
        # Compute ONCE and render twice. When the two views were computed
        # separately the JSON silently lost both the ungrouped rows and the
        # reconcile queue — the same "visible in one view, invisible in
        # another" defect this command was just fixed for. A consumer building
        # a standup from --json must see exactly what a reader sees.
        groups = [(name, [r for r in rows if pred(r)]) for name, pred in defs]
        seen = {r["id"] for _, g in groups for r in g}
        ungrouped = [r for r in rows if r["id"] not in seen]
        rec = [r for r in rows if str(r.get("reconcile", "none")).lower() != "none"]

        if as_json:
            return _dump({
                "total": len(rows),
                "groups": dict(groups),
                # Always present, even when empty: a consumer must not have to
                # infer that a key's absence means "none".
                "ungrouped": ungrouped,
                "reconcile": rec,
                "excluded": excluded,
            })

        print("Daily standup — %d goals\n" % len(rows))
        for group, g in groups:
            print("%s (%d)" % (group, len(g)))
            for r in g:
                print("   %-46s %s" % (r["id"], r["status"]))
            print("")
        # The header promises a total; the groups must account for it. `draft`
        # had no group, so a 10-goal standup listed 8 and said nothing — the
        # same "goal invisible to a status report" defect KDD-0021 was written
        # to end. Any status the groups above do not cover surfaces here rather
        # than vanishing.
        if ungrouped:
            print("Ungrouped (%d) — status not covered by any standup group:" % len(ungrouped))
            for r in ungrouped:
                print("   %-46s %s" % (r["id"], r["status"]))
            print("")
        if excluded:
            print("Excluded (%d) — malformed work-state block, run --check:" % len(excluded))
            for r in excluded:
                print("   %-46s status=%r" % (r["id"], r.get("status")))
            print("")
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
