---
name: be-great
description: Perform exhaustive, evidence-first investigation and review for requests such as "be great," "go deep," "deep dive," "turn over every rock," "review thoroughly," or equivalent requests for the best defensible answer rather than a quick analysis. Inspect all materially relevant user-provided, local, project, historical, private, connected, and public sources available; identify authority; verify current facts; reconcile contradictions; challenge assumptions; follow downstream implications; pressure-test alternatives; and produce a clear verdict, recommendations, and durable Markdown and/or HTML artifacts when warranted.
---

# Be Great

Treat this as investigation mode, not a request for extra words.

Reach the most defensible conclusion available from the evidence, including findings that emerge only after reconciling sources, inspecting the actual environment, or challenging the initial framing.

## Core mandate

1. Define the real question or decision behind the request.
2. Establish the applicable scope, constraints, audience, and consequence of error.
3. Build the broadest materially relevant evidence set available and authorized.
4. Identify the current authority hierarchy before synthesizing.
5. Distinguish authority, primary evidence, historical evidence, secondary evidence, claims, and inference.
6. Verify unstable facts with current authoritative sources.
7. Search actively for contradictions, failure modes, stale assumptions, and disconfirming evidence.
8. Reproduce important counts, identities, versions, paths, states, and test claims when possible.
9. Follow findings into adjacent systems, decisions, ownership boundaries, and second-order effects.
10. Produce a clear verdict, evidence-based reasoning, risks, unknowns, and actionable recommendations.
11. Create a durable artifact when the work should survive the conversation.

## Investigation posture

- Prefer the correct answer over preserving the initial hypothesis.
- Prefer findings over narration of the search process.
- Prefer strong, direct evidence over a large source count.
- Prefer current authority over detailed but superseded material.
- Prefer explicit uncertainty over manufactured certainty.
- Keep investigating while a material conclusion depends on an unresolved assumption.
- Stop when remaining uncertainty is explicit and more available evidence is unlikely to change the recommendation materially.

## Phase 1: Establish the real assignment

Translate the request into an investigation charter:

- Primary question or decision
- Underlying problem the requester is trying to solve
- Intended audience
- Scope and exclusions
- Target environment or operating context
- Required deliverable and destination
- Applicable date or version
- Decision criteria
- Material assumptions
- Consequence of error

Ask only questions whose answers would materially change the investigation. Otherwise state reasonable assumptions and proceed.

Do not accept the initial framing automatically. Test whether the visible question is a symptom of a deeper issue involving authority, ownership, data, architecture, process, governance, security, chronology, or implementation state.

## Phase 2: Build the evidence map

Identify which evidence categories could change the answer:

| Source class | Typical role |
| --- | --- |
| Current owner decisions and governance | Current authority and explicit direction |
| Contracts, policies, registries, and source-of-truth records | Ratified scope, roles, boundaries, and requirements |
| As-built or runtime evidence | What is actually installed, configured, executed, or occurring |
| Current project or repository | Current implementation, tests, documentation, and history |
| User-provided and uploaded material | Task-specific facts, requirements, and context |
| Private or connected sources | Operational evidence unavailable publicly |
| Historical project material | Rationale, lessons, defects, and superseded decisions |
| Current official upstream sources | Versions, APIs, support, releases, security behavior, and recommended patterns |
| Independent primary research | Direct empirical or institutional evidence |
| Secondary public sources | Corroboration, criticism, ecosystem context, and competing interpretations |
| Inference | Reasoning that must be labeled and explained |

Inspect only materially relevant categories. Never claim to have reviewed a source class that was unavailable or not actually inspected.

## Phase 3: Determine authority

Define the source hierarchy for the specific task before drawing conclusions.

A common project hierarchy is:

1. Explicit current owner decisions and ratified governance
2. Current contracts, policies, authoritative registries, and source-of-truth records
3. Current as-built state and primary runtime evidence
4. Current official upstream specifications, repositories, and documentation
5. Current project design and implementation records
6. Historical material as evidence and lessons only
7. Secondary analysis and commentary
8. Inference

Adapt the hierarchy when the governing environment defines another order.

Do not confuse:

- authority with detail;
- target state with as-built state;
- approval history with current approval;
- test execution with proof of the behavior being claimed;
- a current-looking filename with current content;
- documentation with implementation;
- implementation with operational adoption.

Never let an older document silently override current authority merely because it is more complete.

## Phase 4: Investigate in loops

Repeat the following loop as needed:

1. Establish the current authoritative statement.
2. Gather the strongest primary evidence supporting it.
3. Gather evidence likely to contradict or constrain it.
4. Compare source authority, date, version, scope, terminology, and method.
5. Record contradictions and gaps as explicit findings.
6. Recalculate or reproduce material claims when possible.
7. Trace the implications into adjacent components and decisions.
8. Update the working conclusion.
9. Search again only where remaining uncertainty is material.

For each important conclusion, ask:

- What evidence would make this false?
- Do sources disagree about role, host, state, owner, count, path, version, API, behavior, or chronology?
- Is a plan or design being mistaken for as-built reality?
- Is historical intent being mistaken for current authority?
- Is the evidence direct, or merely adjacent to the claim?
- Can the stated count or state be reproduced from underlying records?
- Is a dependency mandatory, optional, legacy, or merely assumed?
- Does this choice create a second authority plane or ownership conflict?
- Which downstream consumer, control, or process is affected?

Escalate material contradictions into findings. Do not bury them in caveats or blend incompatible facts.

## Phase 5: Verify current and unstable facts

Verify facts that may have changed instead of relying on memory or historical documentation.

Use authoritative sources for:

- releases, versions, tags, commits, and dates;
- APIs and supported modes;
- pricing, packaging, licensing, and availability;
- compatibility and hardware or platform requirements;
- security behavior and known vulnerabilities;
- maintainership, support, and deprecation status;
- laws, rules, standards, and regulations;
- current recommended architecture or operating patterns.

Prefer official documentation, repositories, release notes, standards, filings, datasets, and responsible APIs. Use secondary sources for independent confirmation, criticism, field experience, or competing views—not as a substitute for available primary evidence.

Pin versions, dates, tags, commits, configurations, or hashes when they materially affect reproducibility.

Label information as one of:

- Verified current fact
- Source-derived historical fact
- Current owner or governance decision
- Reported but unverified claim
- Inference
- Recommendation
- Unknown or verification required

## Phase 6: Use historical material safely

Mine historical sources for:

- rationale and design intent;
- lessons and failure modes;
- invariants and reusable tests;
- unresolved decisions;
- prior assumptions and their consequences;
- deliberate retirements versus accidental omissions.

Do not copy historical environment state into the current design. Verify current versions, APIs, topology, ownership, requirements, and operating conditions independently.

Treat historical sign-offs as historical evidence, not current approval.

Trace every substantive carried-forward claim to its provenance and explain why it remains valid.

## Phase 7: Test the evidence

Maintain an evidence ledger for material claims:

| Claim | Evidence | Authority level | Date/version | Direct or inferred | Confidence | Contradiction or caveat |
| --- | --- | --- | --- | --- | --- | --- |

Evaluate each important source for:

- Authority
- Directness
- Currency
- Methodological quality
- Independence and incentives
- Specificity to the target context
- Reproducibility
- Independent corroboration

When sources conflict:

1. Confirm they concern the same scope, version, date, definition, population, and environment.
2. Prefer the more authoritative and direct source.
3. Determine whether one supersedes another.
4. Identify methodological or incentive differences.
5. Reproduce the underlying claim where possible.
6. State unresolved disagreement and reduce confidence.

Use precise states when appropriate:

- `VERIFIED`
- `CONDITIONAL`
- `VERIFICATION REQUIRED`
- `NOT ESTABLISHED`
- `CONTRADICTED`
- `SUPERSEDED`
- `OUT OF SCOPE`

## Phase 8: Follow the implications

Do not stop at a locally correct finding. Determine what it changes elsewhere.

Trace implications across applicable areas:

- architecture and interfaces;
- ownership and authority boundaries;
- data lineage, governance, retention, and privacy;
- security and access control;
- operations, observability, recovery, and support burden;
- cost, licensing, staffing, and skills;
- testing, validation, and acceptance criteria;
- migration, compatibility, and rollback;
- schedules, dependencies, and critical path;
- downstream users, systems, and decisions.

Separate each unresolved item into the correct category:

- Blocker
- Owner decision
- Implementation-time verification
- Deferred issue
- Informational observation

Do not turn every unknown into a blocker.

## Phase 9: Pressure-test recommendations

Evaluate at least these alternatives when applicable:

- Keep the current design
- Adopt the proposed path
- Adopt narrowly or partially
- Pilot under controlled conditions
- Place on the roadmap
- Retain for reference only
- Defer pending evidence or prerequisites
- Reject

For each viable option, examine:

- evidence and fit;
- prerequisites and dependencies;
- authority or ownership changes;
- operational burden;
- data and security effects;
- failure modes and blast radius;
- reversibility and switching cost;
- opportunity cost;
- conditions that would change the decision.

Deep analysis does not require recommending change. When existing design remains best, say so explicitly.

## Recommendation standard

Every recommendation must state:

- what to do;
- why the evidence supports it;
- what problem it resolves;
- what it deliberately does not resolve;
- prerequisites and dependencies;
- sequencing and ownership;
- validation or acceptance criteria;
- rollback or reversal conditions when relevant.

Prefer a small number of high-leverage, sequenced recommendations over a generic checklist.

## Artifact standard

Create a durable artifact for a substantial review, research report, architecture assessment, migration analysis, decision packet, governance review, or other result that should survive the conversation.

Before writing:

1. Inspect current project or repository documentation standards.
2. Determine the authoritative destination directory.
3. Determine required filename format, case, date/time, author/model label, and allowed characters.
4. Determine whether Markdown is authoritative, HTML is human-facing, or both are required.
5. Determine whether diagrams, tables, appendices, or a source register are required.
6. Follow the current project standard rather than a remembered convention.

If no convention exists, default to:

- lowercase filenames;
- `<agent>_<YYYYMMDD>_<HHMM>_<descriptive-slug>.md` for the agent-readable source;
- a matching `.html` for polished human review when useful;
- a descriptive title, executive verdict, evidence basis, findings, contradictions, implications, recommendations, unresolved items, and provenance;
- rendered diagrams when relationships, topology, sequence, or decision branches are materially easier to understand visually.

Use:

- Markdown for repository-native source, specifications, and agent-readable records.
- HTML for polished human review, executive reports, and decision packets.
- Both when Markdown is the source of truth and HTML is the human-facing rendering, or when project rules require both.

Do not create an artifact merely for ceremony. Create the artifact that best preserves and communicates the work.

## Default report structure

Adapt the structure to the problem. A strong default is:

1. Executive verdict
2. Scope, question, and source basis
3. Authority hierarchy
4. Findings ordered by impact
5. Contradictions, gaps, and stale assumptions
6. Architecture, operational, governance, or business implications
7. Alternatives considered
8. Recommendations and sequencing
9. Explicit non-recommendations or matters not to reopen
10. Remaining owner decisions and verification items
11. Confidence statement
12. Provenance or source appendix

Lead with the answer, not the investigation diary.

## Confidence standard

- High: direct, current, authoritative evidence with meaningful corroboration and no unresolved material contradiction
- Medium: credible evidence supports the conclusion, but gaps, assumptions, or scope limits remain
- Low: evidence is indirect, sparse, outdated, contested, or materially incomplete

Confidence describes the evidence base—not the persuasiveness of the prose.

## Completion gate

Do not finalize until all applicable checks pass:

- The real question is answered directly.
- The strongest available evidence classes were inspected.
- Current authority was identified.
- Unstable facts were verified as of a stated date.
- Historical material was not mistaken for current state.
- Target design was not mistaken for as-built state.
- Material contradictions and disconfirming evidence were investigated.
- Important counts, versions, paths, identities, and states are reproducible where possible.
- Tests are used only as evidence for behavior they actually exercise.
- Downstream and second-order implications were followed.
- Recommendations were compared against credible alternatives.
- Recommendations are concrete, sequenced, and evidence-based.
- Unknowns, owner decisions, blockers, and implementation checks are categorized correctly.
- The appropriate durable artifact was created in the correct location and format when warranted.
- Another expert could reproduce why the conclusion was reached.

If any answer is no and the gap could materially change the conclusion, continue the investigation.

## Failure modes to avoid

- Stopping at the first plausible answer
- Confusing length with depth
- Treating source volume as source quality
- Searching only for confirming evidence
- Allowing web research to overwrite explicit current project authority
- Treating archived or protected material as validated without inspection
- Treating a test suite as proof of behavior it does not test
- Inferring as-built state from a target-state document
- Repeating historical architecture after upstream conditions changed
- Hiding contradictions behind language such as “generally consistent”
- Recommending implementation before ownership boundaries are settled
- Confusing promising technology with current fit
- Assuming a review implies adoption
- Ignoring security, governance, data-loss, or irreversible-operation implications
- Producing artifacts that violate current naming, format, or destination standards
- Claiming review of sources that were unavailable or not inspected

## Final response standard

Return the smallest response that faithfully communicates the depth of the work. Include:

1. Verdict or executive conclusion
2. What matters most
3. Evidence and high-impact findings
4. Contradictions, risks, and unknowns
5. Recommendations and sequence
6. Items not recommended or not to reopen
7. Remaining verification or owner decisions
8. Links or paths to durable artifacts

Surface important discoveries during long investigations as soon as they are established. Do not make the requester wait until the end to learn about a material blocker, contradiction, or change in conclusion.
