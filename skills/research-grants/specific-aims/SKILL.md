---

name: specific-aims
description: "Use when drafting or revising the NIH Specific Aims page (1 page) for an R01, R21, R03, F-series, or K-series: concrete structure, opening-paragraph formula, Aim-construction pattern, decision rules, common failure modes."
license: MIT
---




<!-- metadata:
category: research-grants
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - research-grants
  - research
difficulty: intermediate
-->

# NIH Specific Aims Page (1 page)

> A working framework for drafting and revising the NIH Specific Aims page. The Specific Aims page is the single most-revised document in any NIH submission; it is the first thing the reviewer reads, the only thing many reviewers re-read, and the document that drives the Approach. A focused 1-page Aims is the difference between a focused 12-page Approach and a 12-page shopping list.

## When to use

- Drafting the 1-page Specific Aims page for an NIH R01, R21, R03, R33, U01, or similar research grant.
- Drafting the 1-page Specific Aims for an F-series (F30, F31, F32) or K-series application.
- Self-reviewing a draft Aims page and identifying whether it is a 5-year plan or a 1-page wish list.
- Iterating from v1 to a publishable v5.
- Reviewing a colleague's Aims and giving structured feedback.

## When NOT to use

- This is not the Research Strategy. The Aims page is the cover page for the Research Strategy. The Research Strategy (Significance / Innovation / Approach) is a separate document.
- This is not the Abstract. The Abstract is 30 lines, contains the public-health relevance, and is a separate attachment. The Aims page is a 1-page document.
- This is not a Specific Aims page for a non-NIH mechanism (NSF, ERC, DARPA). Other mechanisms have their own structural conventions; the structural points in this skill transfer, the rhetoric does not.
- This is not the right skill for a project narrative, a project summary, or a public-health-relevance statement (each is a separate NIH attachment with its own constraints).

## Prerequisites

- A working knowledge of the FOA's Specific Aims page limit (1 page is the default; some FOAs differ).
- A central hypothesis or a central aim — the single sentence the project is about.
- A 4–5 year timeline (for R01) or a 3–5 year timeline (for K / F).
- Preliminary data that supports the central hypothesis, even if modest.

## Core workflow

1. **Write the take-home sentence first.** The take-home sentence is the central claim of the project. If the take-home sentence cannot be written in one sentence, the Aims are not focused. Test the sentence against three rules: (1) it is a claim, not a topic; (2) it has a verb that asserts; (3) it is falsifiable.

2. **Choose the number of Aims.** The default is 2–3 Aims. One Aim is sometimes appropriate (small R03, R21, F30, F31, F32). Four Aims is rare and risky. The number of Aims is a strategic choice: too many Aims diffuse the project; too few Aims leave the reviewer wanting more.

3. **Order the Aims.** Aim 1 should be the most-supportive Aim — the Aim that, if successful, most strongly supports the central hypothesis. Aim 2 builds on Aim 1. Aim 3 is the most ambitious or the most risky. A reviewer reading only the first Aim should still be convinced the project is worth funding.

4. **For each Aim, write the rationale, the approach, and the decision rule.**
   - **Rationale** (2 sentences): what is known, what is missing.
   - **Approach** (4–6 sentences): model, perturbation, readout, n, analysis, expected outcome.
   - **Decision rule** (1 sentence): under what observation is the Aim considered "supported" or "rejected."

5. **Write the opening paragraph (gap + centrality).** The opening paragraph is the most-revised part of the Aims page. It must:
   - Open with a clinical or biological problem the reviewer cares about.
   - State the gap in current knowledge.
   - State the central hypothesis.
   - State the long-term goal and the project's role in it.

6. **Write the closing paragraph (payoff + team + why now).** The closing paragraph is short (3–4 sentences):
   - What advances if the project succeeds.
   - Why the lab is positioned.
   - What the next-stage project is (R01 → R01; K → R; F → K).

7. **Self-review against the page budget.** A 1-page Aims page is approximately 550–650 words including the title. Anything above 700 words is too long. Cut.

8. **Read aloud.** Read the Aims aloud at a measured pace. The reading time should be ~3.5–4 minutes. If it is shorter, the Aims is too thin. If it is longer, the Aims is too long.

9. **Iterate.** The Aims is the most-revised document. Plan 3–5 drafts before submission.

## Document patterns

### Specific Aims page template (1 page)

```markdown
# Title (the title itself is part of the 1 page)

## Opening paragraph (gap + centrality; ~7–10 sentences)
- Sentence 1: The clinical or biological problem.
- Sentence 2: Why it is unsolved.
- Sentence 3: The barrier (a specific mechanistic or technical gap).
- Sentence 4: The central hypothesis.
- Sentence 5: The long-term goal.
- Sentence 6: The objective of this application.
- Sentence 7: The team's prior work that grounds this proposal.
- Sentence 8 (optional): The institute / FOA alignment.

## Aim 1 (3–5 lines each: rationale, approach, decision rule)
**Aim 1: [verb-driven title, e.g., Determine whether X regulates Y in Z].**
- Rationale: ...
- Approach: ...
- Expected outcome / decision rule: ...

## Aim 2 ...
## Aim 3 (optional) ...

## Closing paragraph (payoff + team + why now; ~4 sentences)
- Payoff: if the aims work, the field will have ...
- Team: we are positioned because ...
- Next stage: this R01 lays the groundwork for ...
- Why now: a specific recent advance (a paper, a reagent, a dataset) makes this feasible.
```

### Aim 1 construction (concrete)

```markdown
**Aim 1: Test whether [molecule X] regulates [process Y] in [model Z].**
- Rationale: Prior work shows X is required for Y (Ref 1, 2), but
  whether X is sufficient, and the mechanism by which X acts on Y,
  is unknown. We will test sufficiency using a gain-of-function
  perturbation in Z.
- Approach: We will use a doxycycline-inducible X transgene in Z
  (n=12 per group, 4 cohorts). We will measure Y by [assay] at
  0/1/2/4 weeks and quantify with a [linear mixed model]. We will
  test sufficiency (Aim 1a) and necessity via conditional knockout
  (Aim 1b).
- Expected outcome / decision rule: Aim 1 will be considered
  supported if X overexpression increases Y by ≥1.5x (p<0.01) and
  X knockout reduces Y by ≥50% in the same model. If Aim 1 is
  supported, we will proceed to Aim 2 (mechanism).
```

### Central hypothesis test (3-rule test)

```text
Rule 1 (claim, not topic):
  FAIL: "We are studying mRNA methylation in glioblastoma."
  PASS: "N6-methyladenosine on MYC mRNA drives treatment resistance
        in glioblastoma, and targeting the methyltransferase reverses
        it in xenografts."

Rule 2 (asserting verb):
  FAIL: "We will explore / discuss / investigate / look at..."
  PASS: "We will determine / test / show / demonstrate / cause / predict / establish."

Rule 3 (falsifiable):
  FAIL: "We will study how cells respond to stress."
  PASS: "Heat shock factor 1 activation is required for survival
        after 42°C for 30 minutes in primary cortical neurons."
```

### Opening paragraph formula (in order)

```text
[Sentence 1: The clinical or biological problem, in 1 sentence.]
[Sentence 2: The state of current practice or knowledge.]
[Sentence 3: The specific gap (a missing mechanism, a missing dataset,
            a missing reagent).]
[Sentence 4: The barrier the gap imposes (why the field cannot progress
            past this).]
[Sentence 5: The central hypothesis, falsifiable.]
[Sentence 6: The long-term goal of the lab (programmatic direction).]
[Sentence 7: The objective of this application (the specific question
            addressed in this proposal).]
[Sentence 8: The team's prior work (one or two citations).]
```

### Closing paragraph formula

```text
[Sentence 1: Payoff — if the aims work, the field will have X, Y, Z.]
[Sentence 2: The team's positioning — we are positioned because of
            [prior work, expertise, infrastructure, collaborators].]
[Sentence 3: The next stage — this R01 lays the groundwork for
            [next R01, next translation, next application].]
[Sentence 4: Why now — a specific recent advance makes this feasible
            (cite a paper, a reagent, a dataset).]
```

### Page-budget check (1 page)

```text
- Title (line 1): 1 line.
- Opening paragraph: 6–10 sentences.
- Aims: 3–5 sentences each; 2–3 Aims; total ~10–18 sentences.
- Closing paragraph: 3–4 sentences.
- Total: ~600 words.
- Aims page that is shorter than 500 words is too thin.
- Aims page that is longer than 700 words is too long.
```

## Common pitfalls

- **Topic, not claim.** "We will study X" is a topic. "We will determine whether X causes Y in Z" is a claim. The reviewer is buying a claim, not a topic.
- **Three Aims with no decision rule.** Aims without decision rules are aspirations, not experiments. A reviewer cannot tell when an Aim has succeeded or failed.
- **Aim 1 is the most ambitious Aim.** Aims should be ordered from the most-supportive to the most-ambitious. Aim 1 should be the Aim that, if it works, makes the rest of the project worth doing.
- **Opening paragraph that opens with the lab.** The opening paragraph opens with the problem, not with the lab. "Our lab has studied..." wastes the first sentence.
- **Aims that depend on Aim 2.** Aims must be independently fundable. If Aim 1 cannot be evaluated without Aim 2's results, the Aims are not independent.
- **Closing paragraph that does not say "why now."** "Why now" is the discriminator between an application and a wish list. A specific recent paper, reagent, or dataset must be cited.
- **Title that wastes a noun.** "Studies on..." titles waste a noun that could be a claim. Use a verb-driven title.
- **Aims page that reads as a method list.** The Aims is about questions, not about assays. The Approach is where the methods live.
- **Inconsistent language between Aims page and Approach.** If the Aims page promises "we will determine X causes Y," the Approach must include a causal test. Aims and Approach should be co-revisioned.

## Validation

- The Aims page is 1 page (≈600 words, single-spaced, 0.5"–1" margins, NIH-compliant font).
- The central hypothesis passes the 3-rule test (claim, asserting verb, falsifiable).
- Each Aim has a rationale, an approach, and a decision rule.
- Aim 1 is the most-supportive Aim (the Aim that, if it works, makes the rest worth doing).
- Aims are independently fundable.
- The opening paragraph opens with the problem, not with the lab.
- The closing paragraph includes a "why now" sentence.
- Reading the Aims aloud takes 3.5–4 minutes.
- A reviewer who reads only the Aims can summarize the project in one sentence.

## Open alternatives

- **NIH Forms-H/I vs. older Forms-G.** Forms-H/I is the current package; Forms-G had slightly different page conventions. Always use the current package per the FOA.
- **1-page vs. 2-page Aims for K-series.** Some K-series FOAs allow a 1-page Aims; verify the FOA. The structure is the same; the budget is different.
- **Alternative: Specific Aims is not a substitute for the abstract.** The abstract is a 30-line, separately-scored attachment. The Aims page is the substantive document. Draft both.

## References

- NIH: [Forms-H/I application package](https://grants.nih.gov/grants/forms.htm) — Specific Aims page is the first attachment after the Project Narrative.
- NIH: [SF424 (R&R) Application Guide](https://grants.nih.gov/grants/how-to-apply-application-guide.html) — Specific Aims section.
- NIH: [Grants Policy Statement (NIH GPS)](https://grants.nih.gov/policy/nihgps/index.htm) — current revision.
- NIH: [RePORTER and RePORT matchmaker](https://reporter.nih.gov/) — funded-Aim examples and study section mapping.
- NIH: [NIH Peer Review Process](https://grants.nih.gov/grants/peer-review.htm) — review criteria (Significance, Investigator(s), Innovation, Approach, Environment).

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram.