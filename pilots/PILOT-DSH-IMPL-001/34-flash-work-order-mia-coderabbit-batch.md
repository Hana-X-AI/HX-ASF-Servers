# WORK ORDER — Mia: CodeRabbit batch (35 findings, append-only governance corrections)

- Issuer: Flash (governor), 2026-08-29.
- Executor: Mia (Chief of Staff, KDD-0012).
- Lane: `omniroute/glm-5.3-flash`.

## Intent

CodeRabbit found 35 issues. The dominant pattern: Mia's earlier mechanical
fix replaced "Kimi-K3" with "the governor" in profiles and charters via
find-and-replace. CodeRabbit correctly flags this as silently rewriting
governance history — the append-only convention requires preserving the
original wording and adding a labeled correction. Many findings ask to
restore the original Kimi-K3 text and append the governor routing as a
labeled correction block.

## The findings (35 total)

### Category A — Restore Kimi-K3 wording + append correction (majority)
These ask to preserve the prior "Kimi-K3" authority wording in dated, labeled
correction blocks alongside the new "the governor" routing. Apply to:
- agents/carol/charter.md line 19
- agents/carol/profile.md line 3
- agents/chris/charter.md line 52
- agents/chris/profile.md line 30
- agents/gordon/charter.md line 26
- agents/gordon/profile.md line 24
- agents/john/charter.md line 52
- agents/morpheus/charter.md line 29
- agents/rick/charter.md line 44
- agents/rob/charter.md lines 40-41
- agents/trinity/charter.md line 33
- agents/trinity/profile.md lines 69-71, 333
- agents/mia/charter.md lines 17-18
- agents/mia/profile.md line 24

**IMPORTANT:** Mia's mechanical fix already replaced Kimi-K3 with "the
governor" in these files. CodeRabbit wants the original wording restored
with the governor routing appended as a labeled correction. However —
this is a judgment call. The governor transition is a ratified governance
change (AGENTS.md, KDD-0013 amendment 7/8). The append-only convention
applies to governance RECORDS (KDDs, state logs, evidence docs). Agent
profiles and charters are OPERATIVE documents, not historical records —
they should reflect current authority. The original Kimi-K3 wording is
preserved in the git history and in the AGENTS.md correction blocks.

**Your approach:** For each finding in this category, add a brief labeled
note at the top of the affected section: "[CORRECTION 2026-08-29: authority
references updated from Kimi-K3 to the governor per AGENTS.md transition.
Original wording preserved in git history and AGENTS.md correction blocks.]"
Do NOT restore the old Kimi-K3 text in place — the profiles should read
with current authority. This satisfies the append-only spirit without
making the profiles unreadable.

### Category B — Grammar/typo fixes
- agents/mia/charter.md line 31: "under a the governor-issued" → "under a governor-issued"
- agents/mia/profile.md line 58: same "a the governor-issued" → "a governor-issued"
- agents/mia/profile.md line 109: "a direct the governor → agent" → "a direct governor → agent"
- agents/rick/profile.md line 152: "from the governor work order" — check for duplicated "the"
- agents/trinity/profile.md line 207: "under a the governor-issued" → "under a governor-issued"

Fix these directly — they're clear typos from the find-and-replace.

### Category C — YAML description quoting
- agents/mia/charter.md line 3: colon in "governor: plans" needs quoting
- agents/rob/charter.md line 3: colon in description needs quoting
- agents/trinity/charter.md line 3: colon in "engineer: designs" needs quoting

Check each charter's YAML frontmatter. If the description field contains a
colon, wrap it in quotes so YAML parses correctly.

### Category D — "K3-dispatched" class label
- agents/mia/profile.md line 23: "K3-dispatched" is stale
- agents/morpheus/profile.md line 23: same

Replace "K3-dispatched" with "governor-dispatched" in the Class field.

### Category E — SSH credential handling
- agents/morpheus/profile.md lines 143-145: SSH credential instructions should not instruct to grep/display
- agents/trinity/profile.md lines 267-269: same

Update the SSH credential instructions to read the value into a shell
variable without printing it. Replace "grep for the variable" with "read
the value into a shell variable without printing it (e.g., source the file
or use a non-echoing extraction)".

### Category F — Template and specific issues
- agents/_template/charter.md lines 8-10: preserve previous status/lane ordering — the template was rewritten, CodeRabbit wants the old preserved. SKIP — the template is a template, not a governance record. It should reflect the current standard.
- agents/kimi-k3/charter.md line 9: separate Kimi-K3 identity from governor role, add family value. The charter currently says "Family: Above all (governor)" — this is correct per KDD-0016. SKIP — already compliant.
- agents/gordon/profile.md lines 145-146: prohibition on modifying test files — CodeRabbit says Gordon owns test plans so shouldn't be forbidden from modifying test files. Check: the prohibition says "Never modify candidate configuration or test files." But Gordon's charter says he can install test tooling. The prohibition is about CANDIDATE test files (the dsh source's tests), not Gordon's own test suite. Fix: clarify "Never modify CANDIDATE configuration or CANDIDATE test files — Gordon's own test suite is his to maintain."
- agents/rick/profile.md line 18: "No content amendments" is stale after the model-lane correction. Fix: update the revision row to note the amendment.
- agents/rick/profile.md line 112: authority record append-only correction. Same as Category A — add labeled note.
- AGENTS.md lines 243-245: OD-14 allowlist has both moonshot-ai/kimi-k3 and the OpenRouter governor lane. Reconcile to one authoritative provider lane. Per AGENTS.md correction blocks, the governor lane is now GLM 5.2 then Flash/DeepSeek V4 Flash — moonshot is superseded. Add a labeled note that the moonshot lane is superseded.

## Constraints

- All governance-record changes are append-only, labeled, dated.
- `scripts/validate.py` 4/4 after writes.
- Render any manifest-listed .md you change.
- No secret values.
- Context budget: targeted edits.

## Close

`[TASK COMPLETE — EVIDENCE ATTACHED]` with a table: finding, file, status (fixed/skipped), action taken. validate.py output pasted.
