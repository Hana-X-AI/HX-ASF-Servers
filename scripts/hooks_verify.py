#!/usr/bin/env python3
"""hooks_verify.py — compare the declared hook set to what is registered (O5).

`governace/hooks/manifest.yaml` declares the hooks. This compares it against:

  claude  .claude/settings.json  — in Git, deterministic, verified in CI.
  kimi    ~/.kimi-code/config.toml — user scope, OUTSIDE Git. ADVISORY: absent
          on a fresh machine and absent in CI, so a missing file is reported,
          never failed. CI must not claim it verified user-scope state.

Before this existed, three prose tables claimed to list the hooks and all three
disagreed, while nothing compared any of them to the live registrations. A hook
could be renamed, unregistered, or reduced to a silent no-op with every check
still green.

SECRET BOUNDARY. ~/.kimi-code/config.toml also holds live provider credentials.
This module extracts `[[hooks]]` blocks and reads only `event`, `matcher`,
`command` and `timeout` from them. No other line is parsed, echoed, stored, or
included in any problem message, and problem messages quote only hook names and
script paths. Do not widen this parser to a general TOML load.

Usage:
    python3 scripts/hooks_verify.py [--check] [--json]

`plan()` returns (summary, problems) so validate.py folds it in the same way it
folds skills_sync.plan() — one contract, one place to fix a check.

Read-only. Stdlib + PyYAML. No network.

ON THE PyYAML DEPENDENCY (reviewed 2026-08-30). A stdlib-only manifest format
was proposed and declined. PyYAML is already required by this module's own
caller — validate.py imports it at module scope — and by work_state.py,
skills_registry.py and carol-mint. Every governance artifact in this repository
is YAML: the catalog records, work-state.schema.yaml, the pilot templates.
Inventing a bespoke stdlib format for exactly one governance file would make it
the only artifact a reader cannot open with the same expectations as its
neighbours, and would cost the manifest its comments — which is where its
reasoning lives. The dependency is not new here; it is the house standard.
"""

import json
import os
import re
import shlex
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "governace", "hooks", "manifest.yaml")
CLAUDE_SETTINGS = os.path.join(ROOT, ".claude", "settings.json")
KIMI_CONFIG = os.path.expanduser("~/.kimi-code/config.toml")

SHIM = "claude-payload-shim.sh"
# Hook scripts are addressed by basename in both registration formats.
SCRIPT_RE = re.compile(r"scripts/hooks/([A-Za-z0-9_-]+\.sh)$")


def parse_command(cmd):
    """(target_basename, shimmed, error) from a registration command.

    Structural, not a substring search. A hook that merely APPEARS in the
    command text — echoed, commented, or passed as data — is not a hook that
    runs, and treating the two alike would let a disabled guardrail verify
    clean. The hook must be argv[0], or argv[1] with the shim at argv[0].
    """
    try:
        argv = shlex.split(cmd)
    except ValueError as e:
        return None, False, "command is not parseable: %s" % e
    if not argv:
        return None, False, "empty command"

    def script_of(tok):
        m = SCRIPT_RE.search(tok)
        return m.group(1) if m else None

    first = script_of(argv[0])
    if first == SHIM:
        second = script_of(argv[1]) if len(argv) > 1 else None
        if not second:
            return None, True, "%s is invoked with no hook script argument" % SHIM
        return second, True, None
    if first:
        # A hook script named anywhere BUT in invocation position is data, not
        # an invocation; say so rather than silently counting it as registered.
        for tok in argv[1:]:
            if script_of(tok):
                return first, False, ("extra hook script %r appears as an argument to %r"
                                      % (script_of(tok), first))
        return first, False, None
    return None, False, "command does not invoke a scripts/hooks/*.sh script"


def _sha256(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest():
    with open(MANIFEST, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _claude_registrations():
    """[(event, matcher, target_basename, shimmed, timeout)] from settings.json."""
    if not os.path.isfile(CLAUDE_SETTINGS):
        return None
    with open(CLAUDE_SETTINGS, encoding="utf-8") as fh:
        data = json.load(fh)
    out = []
    for event, entries in (data.get("hooks") or {}).items():
        for entry in entries or []:
            for hook in entry.get("hooks") or []:
                target, shimmed, err = parse_command(hook.get("command", ""))
                out.append((event, entry.get("matcher"), target, shimmed,
                            hook.get("timeout"), err))
    return out


def _kimi_registrations():
    """Same shape, from the user-scope TOML.

    Deliberately a narrow line scanner rather than a TOML parse: this file also
    holds provider credentials, and nothing outside a [[hooks]] block is read.
    """
    if not os.path.isfile(KIMI_CONFIG):
        return None
    out, cur, in_hook = [], {}, False
    with open(KIMI_CONFIG, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if line == "[[hooks]]":
                if in_hook and cur:
                    out.append(cur)
                cur, in_hook = {}, True
                continue
            if line.startswith("[") and line != "[[hooks]]":
                if in_hook and cur:
                    out.append(cur)
                cur, in_hook = {}, False
                continue
            if not in_hook:
                continue
            m = re.match(r'^(event|matcher|command|timeout)\s*=\s*(.+)$', line)
            if m:
                key, val = m.group(1), m.group(2).strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                cur[key] = val
    if in_hook and cur:
        out.append(cur)
    reg = []
    for h in out:
        target, shimmed, err = parse_command(h.get("command", ""))
        timeout = h.get("timeout")
        try:
            timeout = int(timeout) if timeout is not None else None
        except ValueError:
            timeout = None
        reg.append((h.get("event"), h.get("matcher"), target, shimmed, timeout, err))
    return reg


# claude is in Git and must always be verifiable; kimi is user scope and is not
# present in CI or on a fresh machine.
ADVISORY_SCOPES = ("kimi",)


def _check_scope(scope, declared, registered, problems):
    """Compare one scope. `registered is None` means the file is absent."""
    if registered is None:
        if scope in ADVISORY_SCOPES:
            return "%s: not present on this machine (advisory scope, not verified)" % scope
        # A deterministic, in-Git scope that has vanished is a failure, not a
        # note. Reporting it as "not verified" would let deleting
        # .claude/settings.json — unregistering every hook at once — pass clean.
        problems.append("[HK-13] %s: no registration file at %s; the in-Git scope must "
                        "always be verifiable" % (scope, os.path.relpath(
                            CLAUDE_SETTINGS if scope == "claude" else "", ROOT)))
        return "%s: registration file MISSING" % scope

    want = {d["name"]: d for d in declared if scope in (d.get("scopes") or [])}
    seen = {}
    for event, matcher, target, shimmed, timeout, err in registered:
        if err:
            problems.append("[HK-01] %s: %s" % (scope, err))
        if not target:
            continue
        name = target[:-3]
        if name == SHIM[:-3]:
            continue  # the shim is never itself a registered hook
        if name not in want:
            problems.append("[HK-02] %s: %s is registered but not declared in the manifest"
                            % (scope, name))
            continue
        seen[name] = True
        d = want[name]
        if event != d["event"]:
            problems.append("[HK-03] %s: %s registered on %s, manifest declares %s"
                            % (scope, name, event, d["event"]))
        if matcher != d["matcher"]:
            problems.append("[HK-04] %s: %s matcher %r, manifest declares %r"
                            % (scope, name, matcher, d["matcher"]))
        # The shim rule is the difference that silently disables guardrails.
        need_shim = d["shim"] == "claude-only" and scope == "claude"
        if d["shim"] == "never" and shimmed:
            problems.append("[HK-05] %s: %s must NOT be shimmed — it reads the raw payload"
                            % (scope, name))
        elif need_shim and not shimmed:
            problems.append("[HK-05] %s: %s is registered without %s; Claude sends "
                            "tool_input.file_path and the hook would silently no-op"
                            % (scope, name, SHIM))
        elif d["shim"] == "claude-only" and scope == "kimi" and shimmed:
            problems.append("[HK-05] %s: %s must not be shimmed in this scope"
                            % (scope, name))
        floor = d.get("min_timeout")
        if floor is not None and (timeout is None or int(timeout) < int(floor)):
            problems.append("[HK-06] %s: %s timeout %r is below the %ss floor — a hook "
                            "killed mid-run looks identical to one that found nothing"
                            % (scope, name, timeout, floor))

    for name in want:
        if name not in seen:
            problems.append("[HK-07] %s: %s is declared but NOT registered" % (scope, name))
    return "%s: %d/%d declared hooks registered" % (scope, len(seen), len(want))


def plan():
    """Return (summary, problems). Mirrors skills_sync.plan()."""
    problems, notes = [], []
    if not os.path.isfile(MANIFEST):
        return "hooks: manifest missing", ["[HK-00] %s not found" % MANIFEST]
    man = manifest()
    declared = man.get("hooks") or []

    # Every declared script exists and matches its pinned digest. A swapped hook
    # is indistinguishable from a working one at the registration layer.
    for entry in declared + (man.get("helpers") or []):
        path = os.path.join(ROOT, entry["script"])
        if not os.path.isfile(path):
            problems.append("[HK-08] %s: declared script missing" % entry["script"])
            continue
        live = _sha256(path)
        if live != entry.get("sha256"):
            problems.append("[HK-09] %s: sha256 %s… does not match the manifest %s…"
                            % (entry["script"], live[:12], str(entry.get("sha256"))[:12]))

    # The enforcement switch: content AND digest.
    for mf in (man.get("mode_files") or []):
        path = os.path.join(ROOT, mf["path"])
        if not os.path.isfile(path):
            problems.append("[HK-10] %s: declared mode file missing" % mf["path"])
            continue
        value = open(path, encoding="utf-8").read().strip()
        if value != mf.get("expected"):
            problems.append("[HK-11] %s: mode is %r, manifest declares %r — changing the "
                            "enforcement switch is a ratified decision, not an edit"
                            % (mf["path"], value, mf.get("expected")))
        live = _sha256(path)
        if live != mf.get("sha256"):
            problems.append("[HK-12] %s: sha256 %s… does not match the manifest %s…"
                            % (mf["path"], live[:12], str(mf.get("sha256"))[:12]))

    notes.append(_check_scope("claude", declared, _claude_registrations(), problems))
    notes.append(_check_scope("kimi", declared, _kimi_registrations(), problems))

    summary = "hooks: %d declared; %s" % (len(declared), "; ".join(notes))
    return summary, problems


def main(argv):
    as_json = "--json" in argv
    summary, problems = plan()
    if as_json:
        print(json.dumps({"summary": summary, "problems": problems}, indent=2))
        return 1 if problems else 0
    for p in problems:
        print(p)
    print(summary)
    if problems:
        print("hooks-verify: %d problem(s)" % len(problems))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
