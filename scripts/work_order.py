#!/usr/bin/env python3
"""work_order.py — one canonical work order; the context packet is generated (O2).

The two dispatch artifacts carried the same facts twice, by hand. Of a context
packet's 15 fields, 7 are pure copies of the work order, 3 are lossy
restatements, `handoff` is a constant string repo-wide, and only 4 carry
information the work order does not have. The work-order template says the quiet
part itself: the packet's objective is "<Restated from the work order>".

A restatement maintained by hand is a copy that drifts, and it had. In
PILOT-HXS3-MUSE-GLIMMER-TOOLING-001 the paired files already disagreed on
`milestone` — the work order says "M5 — functional validation: ..." and the
packet says "M5 — ... on Meta-X".

Commands:
    list              every work order, structured and legacy
    show <id>         one work order
    context-packet <id>   generate the packet from the work order
    --check           validate structured work orders against the schema
    --json            machine output for any command above

THREE REPRESENTATIONS, not two. 28 work orders use the nested `work_order:`
mapping, 2 use an older flat `id:`/`executor:` convention, and 31 (all
PILOT-DSH-IMPL-001) are free Markdown prose. Only orders declaring
`schema_version: 1` are held to the full field set; the rest predate the schema
and are checked for a unique id only, because `deliverable_destination` was
added to the template on 2026-08-29 and 28 completed pilot records cannot carry
a field invented after they were written. Rewriting them to satisfy a parser
would be the append-only violation this repository keeps having to correct.

Read-only — `context-packet` writes to stdout, never to a file. Stdlib + PyYAML.
"""

import glob
import io
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PILOTS = os.path.join(ROOT, "pilots")
SCHEMA = os.path.join(ROOT, "governace", "templates", "pilot", "work-order.schema.yaml")

# Templates are not work orders.
SKIP_DIRS = ("_templates",)

# The only work-order schema version this engine understands.
SCHEMA_VERSION = 1


def _schema():
    with open(SCHEMA, encoding="utf-8") as fh:
        return yaml.safe_load(fh)["schema"]


def work_order_files():
    """(structured_yaml_paths, legacy_prose_paths)."""
    structured, legacy = [], []
    for path in sorted(glob.glob(os.path.join(PILOTS, "**", "*work-order*"),
                                 recursive=True)):
        if not os.path.isfile(path):
            continue
        rel = os.path.relpath(path, ROOT)
        if any(("/%s/" % d) in "/" + rel for d in SKIP_DIRS):
            continue
        (structured if path.endswith((".yaml", ".yml")) else legacy).append(path)
    return structured, legacy


def parse(path):
    """(work_order_dict, shape, error) — shape is how this file is written.

    THREE shapes exist in the repository, not two:
      structured-v1      `work_order:` mapping declaring `schema_version: 1`
      structured-legacy  `work_order:` mapping, written before the schema
      flat-legacy        top-level `id:`/`executor:` keys, an older convention
    Markdown work orders are classed prose-legacy and never reach here.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except Exception as e:
        return None, None, "not valid YAML: %s" % e
    if not isinstance(data, dict):
        return None, None, "file is not a mapping"
    wo = data.get("work_order")
    if isinstance(wo, dict):
        # PRESENCE, not truthiness. `schema_version: 0` / `false` / `null` are
        # falsy and were being silently grandfathered as legacy; `2` is truthy
        # and was being silently accepted as 1. A declared version the schema
        # does not know is an error, not a default.
        if "schema_version" in wo:
            if wo["schema_version"] != SCHEMA_VERSION:
                return wo, None, ("schema_version %r is not %d"
                                  % (wo["schema_version"], SCHEMA_VERSION))
            return wo, "structured-v1", None
        return wo, "structured-legacy", None
    if wo is not None:
        return None, None, "`work_order:` is not a mapping"
    # The older flat convention still carries an id, so it stays addressable.
    if data.get("id"):
        return data, "flat-legacy", None
    return None, None, "no `work_order:` mapping and no top-level `id:`"


def _concrete_destinations(value):
    """Repo-relative paths a gate can actually probe.

    Drops the template's own "verify: ..." instruction line and any entry still
    carrying an unfilled <placeholder>. Absolute paths are rejected too: a
    destination is repo-relative by contract, and an absolute one would only
    resolve on the machine that wrote it.
    """
    items = [value] if isinstance(value, str) else (value or [])
    out = []
    for item in items:
        if not isinstance(item, str):
            continue
        s = item.strip()
        if not s or s.lower().startswith("verify:") or "<" in s or os.path.isabs(s):
            continue
        out.append(s)
    return out


def load_all():
    """Return (orders, buckets, problems).

    orders  = [(id, dict, rel, shape)]
    buckets = {shape: count}

    ONLY structured-v1 is held to the full required-field set. Everything else
    predates the schema: `deliverable_destination` was added to the template on
    2026-08-29 (QA-audit SY-3), so 28 historical work orders cannot carry it,
    and failing them would demand rewriting completed pilot records to satisfy a
    parser written afterwards — the append-only violation this repository keeps
    having to correct. Legacy shapes are still checked for the ONE property O3
    needs: a unique id, so `hx gate <id>` can resolve them.
    """
    sch = _schema()
    fields = sch["fields"]
    required = [k for k, v in fields.items() if v.get("required")]
    pattern = re.compile(fields["task_id"]["pattern"])

    structured, legacy_paths = work_order_files()
    orders, problems, seen = [], [], {}
    buckets = {"structured-v1": 0, "structured-legacy": 0,
               "flat-legacy": 0, "prose-legacy": len(legacy_paths)}

    for path in structured:
        rel = os.path.relpath(path, ROOT)
        wo, shape, err = parse(path)
        if err:
            problems.append("[WO-01] %s: %s" % (rel, err))
            continue
        buckets[shape] = buckets.get(shape, 0) + 1

        if shape == "structured-v1":
            for f in required:
                if f not in wo or wo[f] in (None, "", []):
                    problems.append("[WO-02] %s: required field %r missing" % (rel, f))
            # Presence is not enough for the one field checklist step 1 depends
            # on. The template ships an instruction line beside the real path
            # ("verify: ls <destination> ..."), and a placeholder still carries
            # its <angle brackets>. Either satisfies a presence check while
            # giving the gate nothing to look for.
            if "deliverable_destination" in wo:
                concrete = _concrete_destinations(wo["deliverable_destination"])
                if not concrete:
                    problems.append("[WO-06] %s: deliverable_destination has no "
                                    "concrete repo-relative path — checklist step 1 "
                                    "cannot be checked against an instruction line "
                                    "or an unfilled placeholder" % rel)
            tid = wo.get("task_id")
            if tid and not pattern.match(str(tid)):
                problems.append("[WO-03] %s: task_id %r does not match %s"
                                % (rel, tid, fields["task_id"]["pattern"]))
        else:
            # Addressability only. `task_id` (nested) or `id` (flat).
            tid = wo.get("task_id") or wo.get("id")
            if not tid:
                problems.append("[WO-05] %s: %s work order carries no id, so "
                                "`hx gate <id>` cannot address it" % (rel, shape))

        tid = wo.get("task_id") or wo.get("id")
        if tid is not None and not isinstance(tid, str):
            # A YAML list or mapping here raises "unhashable type" on the `in
            # seen` test below and takes down every command — the same crash
            # class the work-state engine shipped with.
            problems.append("[WO-07] %s: id must be a string, got %s"
                            % (rel, type(tid).__name__))
            tid = None
        elif isinstance(tid, str) and not tid.strip():
            problems.append("[WO-07] %s: id is empty" % rel)
            tid = None
        if tid:
            if tid in seen:
                # `hx gate <id>` resolves by id; two files answering to one id
                # is ambiguous dispatch, not untidiness.
                problems.append("[WO-04] id %r is claimed by both %s and %s"
                                % (tid, seen[tid], rel))
            else:
                seen[tid] = rel
        orders.append((tid or rel, wo, rel, shape))

    return orders, buckets, problems


def find(task_id):
    orders, _, _ = load_all()
    for tid, wo, rel, _shape in orders:
        if tid == task_id:
            return wo, rel
    return None, None


def _role_from_agent(agent):
    """The packet's `role` is the work order's assigned_agent in packet voice."""
    return "producer (%s)" % agent if agent else "producer"


def context_packet(task_id):
    """Project a context packet from the work order. (dict, error)."""
    sch = _schema()
    wo, rel = find(task_id)
    if wo is None:
        return None, "no work order with task_id %r" % task_id

    packet = {}
    for src, dst in sch["projections"].items():
        if src not in wo:
            continue
        value = wo[src]
        if dst == "role":
            value = _role_from_agent(value)
        packet[dst] = value

    # Authored, not projected: these carry information the work order does not
    # have. They are emitted as explicit placeholders so a generated packet is
    # never mistaken for a complete one.
    packet["goal_version"] = "<authored: goal version at dispatch>"
    packet["session_id"] = "<authored: <agent>-<milestone>-<yyyymmdd>-<nn>>"
    packet["current_state"] = {
        "host": "<authored: hostname (IP), OS, kernel — verified AT PACKET TIME>",
        "key_identities": "<authored: frozen aliases/digests/versions>",
        "relevant_config": "<authored: current values the change touches>",
        "units_or_services": "<authored: states that must hold at completion>",
    }
    packet["evidence_requirements"] = [
        "<authored: pre/post hashes, diffs, command outputs, journal excerpts>",
    ]
    packet["handoff"] = [
        "Deliverable %s goes to Carol for catalog receipt" % wo.get("deliverable", "<NN-...>"),
    ]
    packet["second_brain_evaluation"] = (
        "See the governing work order — the packet does not re-decide it")

    ordered = ["goal_id", "goal_version", "work_order_id", "session_id", "role",
               "milestone", "objective", "current_state", "owner_decisions",
               "constraints", "evidence_requirements", "consulted_records",
               "handoff", "second_brain_evaluation"]
    out = {k: packet[k] for k in ordered if k in packet}
    for k, v in packet.items():
        out.setdefault(k, v)
    return {"context_packet": out}, None


def _dump(obj):
    print(json.dumps(obj, indent=2, default=str))
    return 0


def main(argv):
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    cmd = argv[0] if argv else "list"

    if cmd == "--check":
        orders, buckets, problems = load_all()
        for p in problems:
            print(p)
        if problems:
            print("work-order: %d problem(s) across %d order(s)"
                  % (len(problems), len(orders)))
            return 1
        print("work-order: %d addressable orders — %s (only structured-v1 is held to "
              "the full field set; older shapes predate the schema and are checked for "
              "a unique id only)"
              % (len(orders), ", ".join("%d %s" % (v, k)
                                        for k, v in buckets.items() if v)))
        return 0

    orders, buckets, problems = load_all()
    for p in problems:
        print("WARNING %s" % p, file=sys.stderr)

    if cmd == "list":
        rows = [{"id": i, "file": rel, "shape": shape,
                 "agent": wo.get("assigned_agent") or wo.get("executor"),
                 "milestone": wo.get("milestone")}
                for i, wo, rel, shape in orders]
        if as_json:
            return _dump({"orders": rows, "shapes": buckets})
        print("Work orders")
        print("===========")
        for r in rows:
            print("\n  %-34s %s" % (r["id"], r["shape"]))
            print("     file    : %s" % r["file"])
            print("     agent   : %s" % r["agent"])
        print("\n  %s" % ", ".join("%d %s" % (v, k) for k, v in buckets.items() if v))
        print("  prose-legacy are PILOT-DSH-IMPL-001 Markdown orders: reported, "
              "never failed, never rewritten.")
        return 0

    if cmd == "show" and len(argv) > 1:
        wo, rel = find(argv[1])
        if wo is None:
            print("no work order with task_id %r" % argv[1], file=sys.stderr)
            return 1
        return _dump({"file": rel, "work_order": wo}) if as_json else _dump(wo)

    if cmd == "context-packet" and len(argv) > 1:
        packet, err = context_packet(argv[1])
        if err:
            print(err, file=sys.stderr)
            return 1
        if as_json:
            return _dump(packet)
        buf = io.StringIO()
        yaml.safe_dump(packet, buf, sort_keys=False, allow_unicode=True,
                       width=100, default_flow_style=False)
        print("# GENERATED from the work order by scripts/work_order.py (O2).")
        print("# Projected fields are copies — edit the WORK ORDER, not this file.")
        print("# Fields marked <authored: ...> carry information the work order")
        print("# does not have and must be filled in before dispatch.")
        print(buf.getvalue(), end="")
        return 0

    print("usage: python3 scripts/work_order.py "
          "[list|show <id>|context-packet <id>|--check] [--json]", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
