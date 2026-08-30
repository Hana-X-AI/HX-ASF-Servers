---
name: evidence-first-research
description: Conduct rigorous, current, source-grounded research and produce defensible findings, comparisons, recommendations, or decision briefs. Use when a request calls for research, investigation, recon, deep analysis, fact-checking, technology or vendor evaluation, literature review, current-state assessment, or any answer where source quality, traceability, uncertainty, contradictions, and actionable conclusions materially matter. The owner trigger word is "recon" — when the user says "recon", treat it as a direct request to run this skill.
maturity: active
---

# Evidence-First Research

## Objective

Produce the best defensible answer supported by relevant evidence. Optimize for correctness, traceability, decision usefulness, and honest uncertainty—not source volume or confident prose.

## Operating principles

1. Begin with the decision or question the research must support.
2. Inspect available first-party, private, local, and user-provided sources before broad public search when they are authoritative for the task.
3. Use current public sources whenever facts may have changed.
4. Prefer primary evidence over commentary about that evidence.
5. Separate verified facts, source claims, analysis, inference, and recommendations.
6. Reconcile contradictions instead of hiding them.
7. Search for disconfirming evidence and material constraints.
8. Match research depth to consequence, uncertainty, and reversibility.
9. Cite claims close to where they appear.
10. State what remains unknown and why it matters.

## Phase 1: Frame the assignment

Translate the request into a compact research charter:

- Primary question or decision
- Intended audience
- Scope and exclusions
- Required deliverable
- Time horizon or “as of” date
- Decision criteria
- Material assumptions
- Consequence of error

Ask a clarifying question only when the missing answer would materially change the research path or recommendation. Otherwise, state reasonable assumptions and proceed.

Classify the research depth:

| Level | Use when | Minimum standard |
| --- | --- | --- |
| Rapid | Low-risk orientation or simple fact check | One authoritative source; verify unstable facts |
| Standard | Comparison, recommendation, or operational decision | Multiple relevant sources; primary-source preference; contradiction check |
| Deep | Strategic, expensive, high-risk, contested, or technically complex decision | Broad source coverage; independent corroboration; adversarial search; explicit uncertainty and limitations |

## Phase 2: Build the evidence plan

Decompose the primary question into answerable subquestions. For each subquestion, identify:

- Evidence required
- Best source class
- Search terms or repositories
- Freshness requirement
- Validation method
- Completion condition

Use this source hierarchy unless the task requires a justified exception:

1. User-provided artifacts and authoritative internal records
2. Official specifications, documentation, filings, standards, datasets, and repositories
3. Peer-reviewed papers and reputable institutional research
4. Direct statements or data from responsible organizations
5. High-quality independent analysis and established reporting
6. Community discussions, reviews, forums, and social posts for experience signals only
7. Aggregators and search snippets for discovery, not final support

Treat vendor marketing as evidence of the vendor’s claim, not independent proof that the claim is true.

## Phase 3: Retrieve deliberately

Search in expanding rings:

1. Inspect supplied files, connected sources, and the target repository.
2. Locate the canonical primary source.
3. Find independent corroboration.
4. Search for limitations, failures, disputes, security concerns, and contrary findings.
5. Follow citations backward to original evidence.
6. Stop when additional sources no longer change a material conclusion or confidence level.

For technical research:

- Prefer official documentation, source code, release notes, issue trackers, standards, and research papers.
- Verify version, release date, support status, license, platform constraints, and deprecations.
- Distinguish documented capability from demonstrated behavior.
- Inspect the actual target environment before declaring fit.

For products, vendors, or platforms:

- Verify current pricing, packaging, availability, limits, contract assumptions, and regional constraints.
- Separate must-have requirements from differentiators.
- Include switching cost, operating burden, lock-in, maturity, and failure modes.

For legal, medical, financial, security, or other high-stakes topics:

- Use current authoritative sources.
- Make jurisdiction, date, and applicability explicit.
- Avoid presenting general information as individualized professional advice.

## Phase 4: Evaluate every material source

Assess sources using the following dimensions:

| Dimension | Questions |
| --- | --- |
| Authority | Is this the original or responsible source? |
| Directness | Does it directly support the claim? |
| Currency | Is it current enough for the decision? |
| Method | Are data collection and analysis credible? |
| Independence | Does the source have incentives or conflicts? |
| Specificity | Does it apply to the exact product, version, population, or context? |
| Corroboration | Do independent sources agree? |

Do not use a source merely because it ranks highly in search results. Do not cite a page that mentions the topic but fails to support the specific claim.

## Phase 5: Maintain an evidence ledger

Track material claims during research:

| Claim | Evidence | Source class | Date/version | Confidence | Contradictions or caveats |
| --- | --- | --- | --- | --- | --- |

Label each conclusion internally as:

- Verified fact: directly supported by reliable evidence
- Reported claim: attributed to a source but not independently verified
- Inference: reasoned from evidence; identify the reasoning
- Recommendation: judgment based on facts, criteria, tradeoffs, and assumptions
- Unknown: unresolved or unavailable evidence

Never convert an inference into a fact through wording alone.

## Phase 6: Reconcile contradictions

When sources disagree:

1. Confirm they address the same version, date, population, definition, and scope.
2. Prefer direct and methodologically stronger evidence.
3. Check whether one source supersedes another.
4. Identify incentives, omissions, and measurement differences.
5. State the disagreement when it cannot be resolved.
6. Reduce confidence rather than forcing false certainty.

Actively test the emerging conclusion:

- What evidence would prove this wrong?
- Which assumption carries the most risk?
- Is there a simpler explanation?
- Are negative results missing because of publication or selection bias?
- Does the recommendation still hold under a reasonable downside scenario?

## Phase 7: Synthesize for the decision

Lead with the answer, not the research diary. Use the smallest structure that makes the decision clear:

1. Bottom line
2. Key findings
3. Evidence and reasoning
4. Tradeoffs, risks, and constraints
5. Recommendation or options
6. Unknowns and next validation steps

For comparisons, use explicit criteria and consistent scoring. Do not create a numeric score unless the weights and evidence justify it.

For recommendations, specify one of the following when applicable:

- Adopt
- Adopt narrowly
- Pilot
- Roadmap
- Reference only
- Defer
- Reject

Explain what would change the recommendation.

## Confidence standard

Assign confidence only to material conclusions:

- High: direct, current, authoritative evidence with meaningful corroboration and no unresolved material contradiction
- Medium: credible evidence supports the conclusion, but one or more gaps, assumptions, or scope limits remain
- Low: sparse, indirect, outdated, contested, or materially incomplete evidence

Confidence describes the evidence base, not the strength of the writing.

## Citation standard

- Cite every unstable, disputed, quantitative, or consequential factual claim.
- Place citations immediately after the supported claim.
- Link to the original source whenever possible.
- Include publication or update dates when freshness matters.
- Do not cite search-result pages or snippets as evidence.
- Keep quotations short and use paraphrase for synthesis.
- Preserve source distinctions when several sources support different parts of a sentence.

## Completion gate

Do not declare the research complete until all applicable checks pass:

- The primary question is answered directly.
- Material subquestions are resolved or identified as unknown.
- Unstable facts are current as of a stated date.
- Primary sources were used where available.
- Important claims are traceable to evidence.
- Contradictory and disconfirming evidence was considered.
- Facts, claims, inferences, and recommendations are distinguishable.
- Constraints and failure modes are visible.
- The recommendation follows from stated criteria.
- Remaining uncertainty and next steps are explicit.

## Failure modes to avoid

- Source collecting without synthesis
- Treating search snippets as evidence
- Using many weak sources instead of a few strong ones
- Assuming newer always means better
- Confusing popularity with fit
- Repeating vendor claims as verified facts
- Ignoring the user’s actual environment or constraints
- Hiding contradictions in vague language
- Providing false precision or unjustified scores
- Citing sources that do not support the adjacent claim
- Recommending adoption merely because a technology is promising
- Continuing to search after findings have stabilized without a decision-relevant reason

## Default output template

```markdown
# Research title

## Bottom line

[Direct answer and recommendation.]

## Key findings

- [Finding with evidence and citation.]
- [Finding with evidence and citation.]

## Analysis

[Reasoning, comparisons, and material context.]

## Risks and constraints

- [Risk, likelihood or relevance, and mitigation.]

## Recommendation

[Decision, scope, rationale, and conditions.]

## Confidence and unknowns

[Confidence by material conclusion and unresolved questions.]

## Next steps

1. [Highest-value validation or action.]
2. [Next action.]
```

Adapt the structure to the audience. Keep executive summaries concise while preserving enough evidence for a reviewer to audit the conclusion.
