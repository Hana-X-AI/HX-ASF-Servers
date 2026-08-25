#!/usr/bin/env python3
"""Coding suite (AC-013) — RECONSTRUCTED v1.0.0 task set, M5b Phase A run.

Same 10 tasks as 16-esme-m5-validation.md (clamp, reverse_words, parse_kv, fib,
is_palindrome, dedupe, second_largest, run_length_encode, balance_parens, moving_average)
with fixed signatures and stdlib assertions. Generation: native Phase A defaults
(thinking ON; no sampling overrides; no num_predict). Extraction: first ```python fenced
block from the final-answer content (thinking never inspected or persisted). Execution:
subprocess, 10 s timeout, scratch dir. D8 rule: >=80% passing + evaluator review.

Execution sandbox (bounded, stdlib/OS-native only — generated code is untrusted).
  POLICY (fail-closed, 2026-08-25): the payload runs ONLY when the full
  nobody+netns+pidns sandbox probes available; otherwise the task fails as
  sandbox-unavailable and the payload is NOT executed (no sudo-only or
  unsandboxed fallback modes).
  ENFORCED when probing succeeds (recorded per run):
  - unprivileged identity: uid/gid 65534 (nobody) via `sudo -n ... setpriv`.
  - network isolation: `unshare -n` (fresh network namespace — no route at all).
  - PID namespace: `unshare --pid --fork` — the payload is init of a new
    namespace; its descendant tree dies with the namespace on completion,
    failure, or kill (verified 2026-08-25: detached setsid children are reaped
    at teardown). Belt-and-braces: own session + /proc-snapshot tree-kill after
    every run (sudo re-groups its payload), escalated through `sudo -n kill`
    for root/nobody-owned targets our uid cannot signal.
  - scrubbed environment: only PATH and HOME (the scratch dir) are set.
  - resource limits: CPU 8 s and address space 1 GiB, bound on the payload itself
    via `prlimit ... --` (hard == soft) inside the chain; looser pre-exec rlimits
    on the wrapper stay as defense in depth.
  - fresh temp working dir per task, made nobody-accessible (0777) for the run.
  NOT ENFORCED: filesystem isolation (the host fs stays readable/writable per
  nobody's permissions; /tmp is world-writable), seccomp/syscall filtering, IPC
  namespace. Bounded subprocess sandbox, not a container system.

Usage: coding_suite.py MODEL  (MODEL = ratified model profile alias, e.g. hx-qwen3.8-27b-64k)
"""
import json, os, re, resource, shutil, signal, subprocess, sys, tempfile, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # versioned fixtures dir
from fixtures_corpus import require_model

API = "http://127.0.0.1:11434/api/chat"
# MODEL is set per run in main() from the required argv alias (no silent default).

TASKS = [
    {"id": "clamp",
     "prompt": "Write a Python function `clamp(value, lo, hi)` that returns value bounded to the inclusive range [lo, hi]. Reply with one ```python code block only.",
     "tests": "assert clamp(5,1,3)==3\nassert clamp(0,1,3)==1\nassert clamp(2,1,3)==2\nassert clamp(-7,-5,5)==-5\nassert clamp(2.5,0,10)==2.5\n"},
    {"id": "reverse_words",
     "prompt": "Write a Python function `reverse_words(sentence)` that reverses the order of words, splitting on any whitespace and joining with single spaces. Reply with one ```python code block only.",
     "tests": "assert reverse_words('the quick brown fox')=='fox brown quick the'\nassert reverse_words('hello')=='hello'\nassert reverse_words('  a   b  ')=='b a'\n"},
    {"id": "parse_kv",
     "prompt": "Write a Python function `parse_kv(text)` that parses lines of the form 'key=value' into a dict, skipping blank lines and lines without '='. Whitespace around keys is stripped. Reply with one ```python code block only.",
     "tests": "assert parse_kv('a=1\\nb=2')=={'a':'1','b':'2'}\nassert parse_kv('a=1\\n\\nnoequals\\nb = 2')=={'a':'1','b':'2'}\nassert parse_kv('')=={}\nassert parse_kv('x=a=b')=={'x':'a=b'}\n"},
    {"id": "fib",
     "prompt": "Write a Python function `fib(n)` returning the n-th Fibonacci number with fib(0)==0 and fib(1)==1. Reply with one ```python code block only.",
     "tests": "assert fib(0)==0\nassert fib(1)==1\nassert fib(2)==1\nassert fib(10)==55\nassert fib(20)==6765\n"},
    {"id": "is_palindrome",
     "prompt": "Write a Python function `is_palindrome(s)` that returns True if the string reads the same forwards and backwards, ignoring case and non-alphanumeric characters. Reply with one ```python code block only.",
     "tests": "assert is_palindrome('racecar')\nassert is_palindrome('A man, a plan, a canal: Panama')\nassert not is_palindrome('hello')\nassert is_palindrome('')\n"},
    {"id": "dedupe",
     "prompt": "Write a Python function `dedupe(items)` that removes duplicates while preserving first-occurrence order. Reply with one ```python code block only.",
     "tests": "assert dedupe([1,2,2,3,1])==[1,2,3]\nassert dedupe([])==[]\nassert dedupe(['a','a','b'])==['a','b']\n"},
    {"id": "second_largest",
     "prompt": "Write a Python function `second_largest(nums)` that returns the second largest DISTINCT value in the list, and raises ValueError if fewer than two distinct values exist. Reply with one ```python code block only.",
     "tests": "assert second_largest([1,3,2])==2\nassert second_largest([5,5,5,4])==4\nassert second_largest([10,9])==9\nimport pytest_ish\nfor bad in ([7],[4,4,4]):\n    try:\n        second_largest(bad)\n        raise SystemExit('expected ValueError')\n    except ValueError:\n        pass\n".replace("import pytest_ish\n", ""),
     },
    {"id": "run_length_encode",
     "prompt": "Write a Python function `run_length_encode(s)` that returns run-length encoding as a list of (char, count) tuples. Reply with one ```python code block only.",
     "tests": "assert run_length_encode('aaabbc')==[('a',3),('b',2),('c',1)]\nassert run_length_encode('')==[]\nassert run_length_encode('xyz')==[('x',1),('y',1),('z',1)]\n"},
    {"id": "balance_parens",
     "prompt": "Write a Python function `balance_parens(s)` that returns True if all '()' brackets in the string are balanced and properly nested, ignoring other characters. Reply with one ```python code block only.",
     "tests": "assert balance_parens('(a(b)c)')\nassert balance_parens('')\nassert not balance_parens(')(')\nassert not balance_parens('(()')\nassert balance_parens('no parens')\n"},
    {"id": "moving_average",
     "prompt": "Write a Python function `moving_average(values, window)` returning the list of moving averages rounded to 2 decimals. If window >= len(values), return a single-element list with the overall average. Raise ValueError for window < 1. Return [] for empty values. Reply with one ```python code block only.",
     "tests": "assert moving_average([1,2,3,4],2)==[1.5,2.5,3.5]\nassert moving_average([1,2,3],5)==[2.0]\nassert moving_average([],3)==[]\ntry:\n    moving_average([1,2],0)\n    raise SystemExit('expected ValueError')\nexcept ValueError:\n    pass\n"},
]

FENCE_RE = re.compile(r"```python\s*\n(.*?)```", re.S)

NOBODY = "65534"  # uid/gid nobody
_SANDBOX = None


def _probe(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def sandbox_mode():
    """Fail-closed sandbox selection (2026-08-25): only the full nobody+netns+pidns
    configuration may execute payloads. Returns (prefix, mode); prefix == [] means
    the required sandbox is unavailable and run_generated must NOT execute."""
    global _SANDBOX
    if _SANDBOX is None:
        if shutil.which("sudo") and shutil.which("unshare") and shutil.which("setpriv") \
                and _probe(["sudo", "-n", "unshare", "-n", "--pid", "--fork", "true"]):
            _SANDBOX = (["sudo", "-n", "unshare", "-n", "--pid", "--fork", "setpriv",
                         "--reuid", NOBODY, "--regid", NOBODY, "--clear-groups"],
                        "nobody+netns+pidns")
        else:
            _SANDBOX = ([], "SANDBOX-UNAVAILABLE (need sudo -n, unshare net+pid ns, setpriv) — payload NOT executed")
    return _SANDBOX


def _limits():
    # defense in depth on the wrapper; the payload's own limits come from prlimit
    # (sudo/PAM do not reliably propagate pre-exec rlimits to the command)
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_AS, (1 << 31, 1 << 31))


def _limit_prefix():
    """prlimit wrapper that binds the payload itself (hard == soft)."""
    if shutil.which("prlimit"):
        return ["prlimit", "--cpu=8:8", f"--as={1 << 30}:{1 << 30}", "--"]
    return []  # preexec rlimits on the wrapper remain as the only bound


def _descendants(pid):
    """All descendant PIDs of pid via /proc (Linux); [] if unreadable."""
    ppid_of = {}
    try:
        for entry in os.listdir("/proc"):
            if entry.isdigit():
                try:
                    with open(f"/proc/{entry}/stat") as f:
                        ppid_of[int(entry)] = int(f.read().rsplit(")", 1)[1].split()[1])
                except (OSError, IndexError, ValueError):
                    continue
    except OSError:
        return []
    out, stack = [], [pid]
    while stack:
        parent = stack.pop()
        for p, pp in ppid_of.items():
            if pp == parent:
                out.append(p)
                stack.append(p)
    return out


def _kill_tree(p):
    """SIGKILL the child's process group AND its descendants; never raises.

    sudo re-groups its payload into a new process group, so killpg alone orphans it;
    the descendant set is snapshotted from /proc before the kill, while the ppid
    chain is still intact. Targets owned by root or nobody are beyond our uid —
    those are escalated through non-interactive sudo (`sudo -n kill -9`, negative
    PID for the process group): -n never prompts, so a missing sudo rule fails
    fast instead of hanging teardown. Already-exited targets are tolerated
    (ProcessLookupError, and kill's nonzero exit via check=False). Teardown is
    best-effort: a kill that still cannot be delivered is reported honestly by
    run_generated's bounded drain, not hidden.
    """
    victims = _descendants(p.pid)
    escalate = []
    for target in ([p.pid] if p.pid else []):
        try:
            os.killpg(target, signal.SIGKILL)
        except ProcessLookupError:
            pass  # already exited
        except PermissionError:
            escalate.append(-target)  # root-owned process group: escalate below
    for v in victims:
        try:
            os.kill(v, signal.SIGKILL)
        except ProcessLookupError:
            pass  # already exited
        except PermissionError:
            escalate.append(v)  # root/nobody-owned sandbox process: escalate below
    if escalate:
        try:
            subprocess.run(["sudo", "-n", "kill", "-9", "--"] + [str(x) for x in escalate],
                           capture_output=True, timeout=15, check=False)
        except (OSError, subprocess.TimeoutExpired):
            pass


def run_generated(prog, cwd, timeout=10):
    """Run generated code + assertions sandboxed; return (passed, err)."""
    prefix, mode = sandbox_mode()
    if not prefix:
        return False, f"sandbox unavailable: {mode}"
    cmd = prefix + _limit_prefix() + [sys.executable, prog]
    env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": cwd}
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, text=True,
                         start_new_session=True, preexec_fn=_limits)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        _kill_tree(p)
        try:
            p.communicate(timeout=5)  # bounded recovery drain after the kill
        except subprocess.TimeoutExpired:
            _kill_tree(p)  # final teardown; the incomplete drain is recorded honestly
            return False, (f"timeout; post-kill drain exceeded its 5 s bound "
                           f"(teardown incomplete) (sandbox: {mode})")
        return False, f"timeout (sandbox: {mode})"
    passed = p.returncode == 0 and "ALL_TESTS_PASSED" in out
    return passed, "" if passed else (err or "")[-300:]


def chat(prompt, timeout=180):
    body = json.dumps({"model": MODEL, "stream": False,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(API, data=body, headers={"Content-Type": "application/json"})
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read())
    msg = resp.get("message", {})
    thinking_chars = len(msg.get("thinking") or "")  # counted, never persisted (A01 5.2)
    return (msg.get("content") or "", thinking_chars,
            resp.get("eval_count"), round(time.monotonic() - t0, 2))


def main():
    global MODEL
    if len(sys.argv) != 2:
        sys.exit("usage: coding_suite.py MODEL  (ratified model profile alias, e.g. hx-qwen3.8-27b-64k)")
    MODEL = require_model(sys.argv[1])
    results = []
    for task in TASKS:
        content, tchars, evals, wall = chat(task["prompt"])
        m = FENCE_RE.search(content)
        if not m:
            results.append({"id": task["id"], "passed": False, "reason": "no python fence",
                            "thinking_chars": tchars, "eval_count": evals, "wall_s": wall})
            print(f"{task['id']}: FAIL no-fence", flush=True)
            continue
        code = m.group(1)
        with tempfile.TemporaryDirectory() as td:
            prog = os.path.join(td, "sol.py")
            with open(prog, "w") as f:
                f.write(code + "\n\n" + task["tests"] + "\nprint('ALL_TESTS_PASSED')\n")
            os.chmod(td, 0o777)   # nobody must be able to enter/write the scratch dir
            os.chmod(prog, 0o644)
            passed, err = run_generated(prog, td)
        results.append({"id": task["id"], "passed": passed, "reason": "" if passed else err,
                        "code": code, "thinking_chars": tchars, "eval_count": evals, "wall_s": wall})
        print(f"{task['id']}: {'PASS' if passed else 'FAIL ' + err[:120]}", flush=True)
    npass = sum(1 for r in results if r["passed"])
    ev_dir = "/tmp/esme-m5b/evidence"
    os.makedirs(ev_dir, exist_ok=True)
    ev_path = os.path.join(ev_dir, time.strftime("coding-summary-%Y%m%dT%H%M%SZ", time.gmtime()) + ".json")
    with open(ev_path, "w") as f:
        json.dump({"model": MODEL, "thinking": "native-default-on", "sampling_overrides": None,
                   "sandbox": sandbox_mode()[1],
                   "passed": npass, "total": len(results), "results": results}, f, indent=1)
    print(json.dumps({"passed": npass, "total": len(results), "sandbox": sandbox_mode()[1],
                      "evidence": ev_path}))


if __name__ == "__main__":
    main()
