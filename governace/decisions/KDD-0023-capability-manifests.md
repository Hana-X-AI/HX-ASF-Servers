# KDD-0023: Declare capabilities, then verify them (O5, O7)

- Date: 2026-08-30
- Status: ratified
- Decider: Agent-Zero
- Related: `governace/hooks/manifest.yaml`, `scripts/hooks_verify.py`,
  `scripts/skills_registry.py`, KDD-0020 (canonical skill tree; this mechanizes
  its Amendment 2 item 1), KDD-0021 (the same declare-then-verify shape applied
  to goal state), Codex process-optimization review `codex_20260830_1539`
  (O5, O7, and F5/F6 of its defect list)

## Context

Two capability classes were declared in prose and verified by nobody.

**Hooks.** Three tables claimed to list them and all three were wrong on
2026-08-30. `CLAUDE.md` said "five repo hooks" above a six-row table and "the
four advisory hooks" when there were five. `scripts/README.md` listed two.
`DOC-scripts-hooks.yaml` recorded two and carried a component checksum for
`validate-changed.sh` that no longer matched the file. Nothing compared any of
them to the live registrations, in either scope.

Three failure modes were reachable and none would have announced itself:

1. **The silent no-op.** The five advisory hooks read the edited path from the
   Kimi payload key `path`. Claude Code sends `tool_input.file_path`, and the
   literal string `"path"` never appears inside `"file_path"`, so an unshimmed
   hook matches nothing and exits 0. A disabled guardrail and a clean run are
   the same observation.
2. **The blinded scanner.** `secret-boundary.sh` greps the whole raw payload.
   Wrapping it in the shim — which rewrites the payload to a bare
   `{"path": ...}` — would blind it while leaving it registered and green.
3. **The ungoverned switch.** `scripts/hooks/secret-boundary.mode` is a
   five-byte file whose single word decides whether the one enforcing hook can
   block. It was group-writable and its content was asserted nowhere.

**Skills.** SY-3 proves the mirrors are byte-identical. It executes nothing and
reads no frontmatter, which is exactly how `goal-decompose` shipped a SKILL.md
documenting four scripts in a `scripts/` directory that was empty and always had
been: every false claim was mirrored faithfully to both mirrors. Anyone
following the skill got "No such file or directory". KDD-0020 Amendment 2
recorded that reconciling the `AGENTS.md` inventory against `.agents/skills/`
was "NOT yet mechanized — performed manually"; nothing in the repository read
`AGENTS.md` at all, so the 30/30 match was maintained by hand and true by
coincidence.

## Options considered

1. **More prose tables, better maintained.** Rejected: three already existed and
   all three were wrong. The defect is not carelessness, it is that no reader
   and no check ever compared them to reality.
2. **Make the hooks enforcing so failures are loud.** Rejected: it treats the
   symptom. A hook that is not registered cannot fail loudly, because it does
   not run at all.
3. **Declare each capability in one machine-readable file and verify the
   declaration against the live state.** **Selected.** Same shape as KDD-0021:
   one declaration, one reader, enforced as a `validate.py` sub-check.
4. **A capability database or service.** Rejected, and the source review says
   the same: not before the file-based approach is proven insufficient.

## Decision

**D1 — One hook declaration.** `governace/hooks/manifest.yaml` declares every
hook: event, matcher, `enforcement` (advisory or enforcing), `shim` requirement,
`min_timeout`, `sha256`, and the scopes it belongs to. It also governs the
payload shim's digest — the shim is not a hook, but a broken shim turns all five
advisory hooks into silent no-ops without touching any hook — and the content
AND digest of the mode file.

**D2 — Both registration scopes, asymmetrically.** `scripts/hooks_verify.py`
compares the manifest against `.claude/settings.json` (in Git, deterministic,
CI-verified) and `~/.kimi-code/config.toml` (user scope, outside Git). A missing
user-scope file is **reported, never failed**: CI has no such file and must not
claim it verified user-scope state. A missing in-Git file is a **hard failure** —
deleting it unregisters every hook at once and must never pass clean.

**D3 — Registration is structural, not textual.** A hook path that merely
appears in a command string is not a hook that runs. The verifier tokenizes the
command and requires the hook at `argv[0]`, or at `argv[1]` behind the shim. A
hook echoed or passed as data is reported, not counted.

**D4 — The user config is read narrowly, on purpose.** `~/.kimi-code/config.toml`
holds live provider credentials beside the `[[hooks]]` blocks. The parser is a
line scanner that reads `event`, `matcher`, `command` and `timeout` inside
`[[hooks]]` and nothing else. It is deliberately NOT a general TOML load, and
two regression tests assert that no credential, `api_key` or `base_url` can
reach a summary, a problem message, or the parsed registrations.

**D5 — Skills declare only what the inventory cannot know.** `AGENTS.md`
§"Skills and trigger words" remains the single authority for owner and trigger
words (KDD-0020 D3). `scripts/skills_registry.py` READS them from there and
reconciles; it does not duplicate them into frontmatter. Frontmatter carries
`maturity`, `required_files` and `smoke`.

This overrides the source review's O7 wording, which proposed putting triggers
and owners in the registry. A second copy of a ratified inventory needs its own
sync check and becomes a second authority plane for the same fact — the defect
this optimization set exists to remove. The registry is the *reconciler* of the
inventory, not a rival to it.

**D6 — A skill that ships something runnable must smoke it or say why not.**
Reference material has nothing to execute, so demanding a skip reason for a
format document would be boilerplate that teaches a reader nothing. `archify`
declines with its reason (its vendored suite resolves paths to a parent
directory that has never existed in this repository); `diagnosing-bugs` declines
because its `.sh` is a template that blocks on human input, and CI shellchecks
it instead.

**D7 — Enforced as SY-5 and SY-6.** Both run inside the existing
`governance-path` check. The check count stays **5/5** — the same reasoning as
SY-3 and SY-4: a sixth top-level check would invalidate the count assertions
scattered across the repository for no gain. Smokes execute skill commands, so
they run as their own CI step rather than inside the read-only validator.

## Consequences

**Enables.** "Is this hook actually running?" and "does this skill actually
work?" become answerable by a command instead of by reading three tables and
trusting one. The prose tables survive as reader summaries and are now labelled
as such: where a table and its manifest disagree, the table is the defect.

**Immediate effect.** Six hooks reconciled across both scopes. Thirty skills
reconciled 1:1 against the `AGENTS.md` inventory, mechanizing KDD-0020 Amendment
2 item 1. `CLAUDE.md`, `scripts/README.md`, `tests/README.md`,
`scripts/hooks/README.md` and `DOC-scripts-hooks.yaml` corrected against the new
checks. The duplicated component checksums in the catalog record were removed
rather than repaired: they now live in the manifest, where SY-5 verifies them
against the real files on every run.

**Forecloses.** Adding a hook by editing one scope. Registering a Claude hook
without the shim. Flipping the enforcement switch as an unnoticed one-word edit —
graduation to `block` is O6 and must land with the regression corpus that
justifies it. Shipping a skill that documents files it does not contain.

**Costs.** A hook or skill change now touches its declaration too. That is the
point; it was previously possible to change either and have every check stay
green.

**Also delivered.** CI shellcheck extended past `scripts/hooks/*.sh` to
`.agents/skills/*/scripts/*.sh` — seven skill shell scripts were linted by
nothing. It found a real flag on its first run: SC1003 in the terminal-escape
sanitizer's own test, where `\\` is a literal backslash forming the OSC-8 string
terminator. Correct as written, so a targeted suppression with the reason
recorded, not a weakened test.

**Must be revisited if.** A third registration scope appears, or a runtime stops
accepting `.claude/settings.json`. `min_timeout` is a floor, not an equality
check, because the two scopes legitimately tune differently; if they ever must
match, that is a schema change here.

**Not addressed.** O2 (context packets generated from work orders), O3
(`hx gate`), O4 (asynchronous catalog closure) and O8 (capability registry)
remain open. O6 (secret-boundary warn → block) is unblocked but not taken: the
mode file's content is now declared, so the flip is visible, but the
false-positive regression corpus that justifies it does not exist yet.
