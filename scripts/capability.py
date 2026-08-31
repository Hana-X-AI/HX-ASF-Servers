#!/usr/bin/env python3
"""capability.py — enforce capability lifecycle states (O8, SY-9).

`governace/capabilities/registry.yaml` keeps "installed", "service_active",
"advertised_to_agents" and "approved_for_use" as four separate fields. This
enforces the invariants between them, and — the part that matters — checks the
declared owner hold against what the agent charters actually say.

The review's requirement was: "Enforce the owner hold at discovery/routing, not
only in prose." Prose is exactly where it lived. An owner-wide MCP hold sits in
servers/system-mapping.md while four agents' charters describe MCP surfaces they
own, two of them with no mention of the hold at all and one specifying a systemd
unit and an install command. Nothing compared the two.

  CP-01  a capability under owner_hold is advertised or approved
  CP-02  service_active without installed
  CP-03  approved_for_use without a completed security_review
  CP-04  a recorded contradiction with no reconcile text, or the reverse
  CP-05  an owning agent that is not registered
  CP-06  the hold is declared, but an owning agent's charter never mentions it

CP-01/02/03 are invariants INSIDE the registry and always fail. CP-05 and CP-06
are contradictions with records OUTSIDE it: they are REPORTED when the registry
already states the conflict and names the ratified record it collides with, and
they FAIL when it does not. Registering an unacknowledged contradiction as
resolved would overwrite a ratified KDD, and choosing between two ratified
records is a governor act. Same rule as work-state's `reconcile` field: the tool
surfaces the conflict and never settles it.

Usage:
    python3 scripts/capability.py [list|check] [--json]

Read-only. Stdlib + PyYAML. No network.
"""

import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(ROOT, "governace", "capabilities", "registry.yaml")
AGENTS_DIR = os.path.join(ROOT, "agents")

# A line that mentions MCP *and* carries the word "hold" on its own. Substring
# matching was tried first and was worse than useless: `deleted_threshold` in
# quinn's profile contains "hold", so the check silently exonerated the exact
# agent it was written to flag.
HOLD_LINE = re.compile(r"(?i)mcp.*\bhold(s|ing)?\b|\bhold(s|ing)?\b.*mcp")


def registry():
    with open(REGISTRY, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _agent_mentions_hold(agent):
    """True when the agent's charter or profile says anything about a hold."""
    for name in ("charter.md", "profile.md"):
        path = os.path.join(AGENTS_DIR, agent, name)
        if not os.path.isfile(path):
            continue
        for line in open(path, encoding="utf-8", errors="replace"):
            if HOLD_LINE.search(line):
                return True
    return False


# A contradiction is ACKNOWLEDGED only when the text names the ratified record
# it collides with. Accepting any non-"none" string let a single word — say
# "acknowledged" — silence a blocking finding, which turns the escape hatch into
# a mute button. Same reasoning as the SY-8 baseline: downgrading a finding has
# to cost a visible, arguable statement.
AUTHORITY_REF = re.compile(r"KDD-\d{3,4}|DOC-[a-z0-9-]+|[\w./-]+\.(md|ya?ml)|"
                           r"state-log row \d+|owner directive \d{4}-\d{2}-\d{2}")
MIN_RECONCILE_CHARS = 60


def _acknowledged(rec):
    """True when a reconcile note is substantive AND cites what it conflicts with."""
    if not isinstance(rec, str):
        return False
    s = " ".join(rec.split())
    if s.lower() in ("", "none"):
        return False
    return len(s) >= MIN_RECONCILE_CHARS and bool(AUTHORITY_REF.search(s))


def _agent_registered(agent):
    return os.path.isdir(os.path.join(AGENTS_DIR, agent))


def plan():
    """Return (summary, problems)."""
    problems = []
    if not os.path.isfile(REGISTRY):
        return "capability: registry missing", ["[CP-00] %s not found" % REGISTRY]
    reg = registry()
    mcp = reg.get("mcp") or {}
    hold_active = bool((mcp.get("owner_hold") or {}).get("active"))
    caps = mcp.get("capabilities") or []
    contradictions = 0

    for c in caps:
        name = c.get("capability", "<unnamed>")

        # CP-01 — the invariant the whole registry exists for. The GLOBAL hold
        # binds too: a capability cannot escape an owner-wide directive by
        # omitting its own owner_hold field or setting it false. Checking only
        # the local field let an unset capability be advertised under an active
        # hold, which is the exact thing the hold exists to prevent.
        effective_hold = bool(c.get("owner_hold")) or hold_active
        if effective_hold:
            scope = "capability" if c.get("owner_hold") else "global mcp.owner_hold"
            for field in ("advertised_to_agents", "approved_for_use"):
                if c.get(field):
                    problems.append("[CP-01] %s: %s is active but %s is true — a held "
                                    "capability must not be offered to agents"
                                    % (name, scope, field))

        # CP-02 — running without being installed is incoherent.
        if c.get("service_active") and not c.get("installed"):
            problems.append("[CP-02] %s: service_active without installed" % name)

        # CP-03 — approval is not a side effect of installation.
        if c.get("approved_for_use") and c.get("security_review") != "complete":
            problems.append("[CP-03] %s: approved_for_use with security_review %r"
                            % (name, c.get("security_review")))

        rec = str(c.get("reconcile", "none")).strip()
        if rec.lower() != "none":
            contradictions += 1
            if not _acknowledged(rec):
                problems.append("[CP-04] %s: reconcile text does not name the ratified "
                                "record it conflicts with, so it cannot downgrade a "
                                "finding — cite the KDD, record id or path" % name)

        explained = _acknowledged(rec)
        agent = c.get("owning_agent")
        if agent:
            if not _agent_registered(agent):
                problems.append("[CP-05]%s %s: owning_agent %r has no agents/%s/ "
                                "directory — an unregistered owner"
                                % ("" if not explained else " REPORTED",
                                   name, agent, agent))
            elif hold_active and not _agent_mentions_hold(agent):
                problems.append("[CP-06]%s %s: the MCP hold is active but %s's "
                                "charter and profile never mention it"
                                % ("" if not explained else " REPORTED",
                                   name, agent))

    gates = reg.get("activation_gates") or []
    for g in gates:
        if g.get("activated") and not g.get("condition"):
            problems.append("[CP-04] activation gate for %s is activated with no "
                            "recorded condition" % g.get("agent"))

    summary = ("capability: %d MCP surfaces (hold %s), %d recorded contradictions, "
               "%d activation gates, %d plugins installed"
               % (len(caps), "ACTIVE" if hold_active else "lifted", contradictions,
                  len(gates), len((reg.get("plugins") or {}).get("installed") or [])))
    return summary, problems


def main(argv):
    as_json = "--json" in argv
    cmd = next((a for a in argv if not a.startswith("--")), "check")
    summary, problems = plan()

    if cmd == "list":
        if not os.path.isfile(REGISTRY):
            # check mode reports this as CP-00; list mode used to raise
            # FileNotFoundError. Same condition, same answer.
            print(summary)
            for p in problems:
                print(p)
            return 1
        reg = registry()
        if as_json:
            print(json.dumps(reg, indent=2, default=str))
            return 0
        print("Capabilities")
        print("============")
        for c in (reg.get("mcp") or {}).get("capabilities") or []:
            print("\n  %s  [%s]" % (c.get("capability"), c.get("host", "?")))
            print("     installed=%s service_active=%s advertised=%s approved=%s hold=%s"
                  % (c.get("installed"), c.get("service_active"),
                     c.get("advertised_to_agents"), c.get("approved_for_use"),
                     c.get("owner_hold")))
            if str(c.get("reconcile", "none")).lower() != "none":
                print("     RECONCILE: %s" % " ".join(str(c["reconcile"]).split())[:150])
        print("\n  %s" % summary)
        return 0

    if as_json:
        print(json.dumps({"summary": summary, "problems": problems}, indent=2))
        return 1 if any(" REPORTED " not in p for p in problems) else 0
    for p in problems:
        print(p)
    print(summary)
    # An EXTERNAL contradiction the registry already states, with the conflicting
    # ratified record named, is a governor decision item — not a defect this tool
    # can fix. It stays visible and does not hold the gate red forever. A finding
    # with no reconcile text has not been acknowledged by anyone and does block.
    blocking = [p for p in problems if " REPORTED " not in p]
    if blocking:
        print("capability: %d problem(s)" % len(blocking))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
