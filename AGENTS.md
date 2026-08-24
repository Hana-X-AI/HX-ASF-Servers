# AGENTS.md

## Skills and trigger words

Ten owner-installed skills govern how work is done in this repository. They live in
`.kimi-code/skills/` (project scope) and also at user scope in `~/.kimi-code/skills/`.

- **be-great** — owner trigger: **"be great"**. Exhaustive, evidence-first investigation:
  establish authority, verify current facts, reconcile contradictions, follow downstream
  implications, pressure-test alternatives, and deliver a defensible verdict.
- **be-smart** — owner trigger: **"be smart"**. Clear, concise, actionable communication
  contract: banned phrases, reference-point codes, hard operational boundaries, and the
  `scr` / `eli` / `foc` / `ref` aliases.
- **evidence-first-research** — owner trigger: **"recon"**. Rigorous, source-grounded
  research with primary-source preference, an evidence ledger, explicit confidence
  levels, and traceable citations.
- **eli5** — owner trigger: **"eli5"**. Report in plain ASD-STE100-style English:
  short sentences, one idea per sentence, jargon explained immediately, and only what
  was done, whether it worked, and what to do next. Governs reporting style only —
  code, commands, and paths stay exact.
- **bro** — owner trigger: **"bro"**. Restate the last reply in plain human language,
  no jargon.
- **wait-what** — owner trigger: **"wait what"**. Re-pitch the message that lost the
  owner, with the missing context, in ASD-STE100-style English.
- **quick** — owner trigger: **"quick"**. Answer fast: action first, numbered steps,
  one next step, no preamble.
- **human** — owner trigger: **"casual"**. Talk like a friend: warmer, write like
  you speak.
- **corp** — owner trigger: **"formal"**. Executive-summary tone, formal business
  English.
- **copy** — owner trigger: **"punchy"**. Rewrite as ad copy: hooks first, short
  lines, sell do not explain.

When the owner uses a trigger word, invoke the matching skill first and follow its
workflow in full — do not partially apply it. Project agents and sub-agents working in
this repository must honor these skills as well.

Default reporting voice: **corporate** (executive-summary tone). A voice trigger
overrides the default for that reply; when style skills conflict, the owner's most
recent explicit trigger wins.

## Communication contract

Always on, distilled from the **be-smart** skill (say "be smart" to load the full
contract with examples).

- Banned phrases: "load-bearing", "worth stating plainly", "here's the honest truth",
  "the real tension", "carry the argument".
- No flattery, no decorative headings or emoji, no motivational language. State each
  idea once. No em-dash chaining. No analogies for what is in front of us.
- Lead with the answer; end with the required action or next step.
- Reference codes for 3+ items: `F` findings, `D` decisions, `O` options, `R` risks,
  `Q` questions, `A` actions (`F1`, `D2`, ...). Keep codes stable across the
  conversation; follow-ups like "keep D1, reject O2" are valid.
- Hard boundaries: requested scope only; no unasked refactors, cleanup, or speculative
  abstractions; no completion claims without evidence; never add a co-author to
  commits.
- Aliases (expand only as exact standalone tokens): `scr` = simplify, compress, and
  repeat the response; `eli` = explain like I'm 18, simpler and shorter; `foc` = boil
  down to the one thing that matters; `ref` = rewrite with reference points.

## The ASD-STE100 rule

ASD-STE100 is a real writing standard from the 1980s aviation industry. Aircraft
maintenance manuals are written in it so that mechanics — often non-native English
speakers — cannot misread an instruction.

When a skill or reply calls for ASD-STE100-style English (for example **eli5** or
**wait-what**), apply its rules:

- limited, approved vocabulary;
- active voice;
- short sentences;
- one idea per sentence;
- no metaphors or figures of speech.

## Technical knowledge

The technical knowledge base for all agents lives at `/opt/tkv-local`. At the start of
every assignment, the assigned agent must survey the material relevant to its task
there using the **be-great** skill (evidence-first investigation) before acting.

Its contents are reference material, not current truth: verify versions, state, and
applicability against the live environment before converting them into configuration,
and label them per the truth-state rules.

## Documentation conventions

- Use workflow diagrams (process flow, dataflow) in documentation where they make a
  process or relationship materially easier for a human to read. Default format:
  Mermaid in Markdown, rendered in the HTML output.
- Major documents — specs, designs, READMEs, and other human-facing decision or
  reference documents — are delivered in both `.md` (agent-readable source of truth)
  and a matching `.html` (human-facing rendering). Not every document: logs, notes,
  and routine records stay Markdown-only.

## Adoption of provided documents

Documents supplied for adoption are inputs to review, not gospel. Before a provided
document becomes part of this repository's operating material:

- verify its claims against current evidence and ratified authority;
- reconcile conflicts instead of blending them;
- bring it up to our standards: truth-state labels, naming, the communication
  contract, and the documentation conventions above;
- record provenance and the corrections made.

Quality applies to inputs and outputs alike. Historical evidence records (for example
as-found discovery files) keep their provenance and are corrected openly per the
server records contract, never silently rewritten.
