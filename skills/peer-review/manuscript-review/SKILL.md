---
name: manuscript-review
description: "Conduct a formal peer review of a scientific manuscript for a journal: section-by-section evaluation, reporting-checklist compliance, major/minor comments, recommendation to editor."
license: MIT
---



<!-- metadata:
category: peer-review
version: 1.0.0
author: Pradyumna Jayaram
tags:
- peer-review
- manuscript
- journal
- reporting-checklist
- reviewer-recommendation
difficulty: advanced
prerequisites:
  tools: []
  skills: []"
sources: "ICMJE Recommendations for the Conduct, Reporting, Editing, and Publication\
  \ of Scholarly Work in Medical Journals (icmje.org); EQUATOR Network — reporting-guidelines\
  \ registry (equator-network.org); CONSORT 2010 / CONSORT-AI / CONSORT-Cluster extensions\
  \ (bibr.iumio.ch); STROBE Statement for observational studies (strobe-statement.org);\
  \ PRISMA 2020 Statement for systematic reviews (prisma-statement.org); ARRIVE 2.0\
  \ — Animal Research: Reporting of In Vivo Experiments (arriveguidelines.org);\
  \ MIAME — Minimum Information About a Microarray Experiment (fgcz.ch); MINSEQE\
  \ — Minimum Information about a Sequencing Experiment (grnasp.org); TRIPOD+AI\
  \ — prediction model reporting (tripod-statement.org); SPIRIT 2013 — trial\
  \ protocol reporting (spirit-statement.org); CARE 2017 — case report reporting\
  \ (care-statement.org); CHEERS 2022 — economic evaluation reporting (cheers-statement.org);\
  \ Committee on Publication Ethics (COPE) Peer Review guidance (publicationethics.org);\
  \ Elsevier — Role of a reviewer (elsevier.com/reviewers/role); Nature —\
  \ Formal peer-review guidance (nature.com/nature-portfolio/editorial-processes/peer-review)"
-->

# Manuscript Peer Review

> Produces a journal-ready peer review for a scientific manuscript: structured summary, checklist-based evaluation, major and minor issues, constructive feedback, confidential comments to the editor, and a defensible recommendation (accept / minor revision / major revision / reject). Adapted by Pradyumna Jayaram from public reporting-standards bodies (EQUATOR Network, ICMJE, COPE) and journal reviewer guidance (Elsevier, Nature).

## When to use

- You have been invited by a journal editor to review a submitted manuscript.
- You are running an internal mock review for a colleague or trainee before submission.
- You are auditing a published paper for a journal club, replication study, or post-publication review.
- You need to assess a preprint or a manuscript draft against discipline-specific reporting standards.

## When NOT to use

- For evaluating a *researcher's overall record* (use `ors-peer-review-scholar-evaluation`).
- For reviewing a *grant proposal* (use `ors-peer-review-grant-review`).
- For writing the *author's reply* to reviewers (use `ors-peer-review-reviewer-response`).
- For evaluating a single claim or a body of evidence (use `scientific-critical-thinking` or a literature-review skill).

## Prerequisites

- Discipline-appropriate expertise (methods, statistics, prior literature).
- A complete, unmarked copy of the manuscript, including figures, tables, and supplementary material.
- Access to the journal's specific reviewer guidelines (word/figure limits, recommendation scale, anonymization rules).
- Familiarity with the relevant reporting checklist (CONSORT, STROBE, PRISMA, etc.) for the manuscript type.

## Core workflow

### 1. Pre-flight checks

- Confirm the editor's deadline, scope, and any required reporting checklist.
- Declare any conflict of interest (financial, personal, institutional, recent collaboration) **before** reading the manuscript in depth. If a disqualifying conflict is identified, decline immediately.
- Decide whether the review will be single-blind, double-blind, or open; the choice governs how you sign the report and what identifying information you may include.
- Note the journal's recommendation scale (e.g., accept / minor / major / reject-and-resubmit) and the format of confidential-to-editor comments.

### 2. Initial assessment (read-through)

Read the manuscript once without note-taking to gauge scope, novelty, and fit.

- What is the central question, hypothesis, or claim?
- Are the conclusions supported by the data at first read?
- Is the manuscript within the journal's scope and quality bar?
- Are there immediate fatal flaws (plagiarism, ethics issues, broken methods)?

### 3. Reporting-checklist evaluation

Identify the manuscript's design and apply the corresponding EQUATOR Network checklist. Common mappings:

| Study type | Primary checklist | Where to look |
|---|---|---|
| Randomized controlled trial | CONSORT 2010 (+ extensions: cluster, pragmatic, non-inferiority, AI) | Methods, Results, Figure 1 flow diagram |
| Observational study (cohort, case-control, cross-sectional) | STROBE | Methods, Table 1 baseline |
| Systematic review / meta-analysis | PRISMA 2020 | Methods (search strategy), PRISMA flow diagram |
| Animal in vivo study | ARRIVE 2.0 | Methods, sample size justification |
| Microarray experiment | MIAME | Methods, GEO/SRA accession |
| RNA-seq / sequencing experiment | MINSEQE | Methods, data deposition |
| Diagnostic / prognostic prediction model | TRIPOD (+AI) | Methods, model presentation |
| Clinical trial protocol | SPIRIT 2013 | Methods, items 1–22 |
| Case report | CARE 2017 | Abstract, timeline figure, discussion |
| Economic evaluation | CHEERS 2022 | Methods (perspective, discounting), results (ICER) |

For each item in the chosen checklist, mark "addressed", "partially addressed", or "missing", and note the page/section where it appears (or should appear). Flag items that are absent as specific minor or major comments to the authors.

### 4. Section-by-section evaluation

For each section, evaluate both substance and presentation. Use the rubric in the *Code patterns* section as a reusable checklist.

**Title and abstract**

- Specific, accurate, accessible to a broad scientific audience.
- Abstract conclusions are not stronger than the data permit.
- All claims in the abstract are traceable to results in the main text.

**Introduction**

- Background is current and balanced (cites contrary findings, not just supporting ones).
- Research question / hypothesis is explicitly stated.
- The "gap" being filled is real and significant, not a manufactured problem.

**Methods**

- A competent peer could reproduce the study from the description.
- Sample-size justification (formal power analysis or pre-specified stopping rule).
- Randomization, blinding, inclusion / exclusion criteria all explicit.
- Statistical methods named with version, including correction for multiple comparisons, handling of missing data, and any pre-registration.
- For computational work: software versions, parameters, random seeds, hardware where relevant.
- Ethics: IRB / IACUC approval numbers, consent procedures, clinical-trial registration.

**Results**

- Findings are presented in a logical order; no cherry-picking.
- Effect sizes with confidence intervals, not just p-values.
- Negative or null results are reported, not buried.
- Figures and tables are self-contained (legend + units + statistical annotation).
- All figures referenced in the text and vice versa.

**Discussion**

- Conclusions are no stronger than the data.
- Limitations acknowledged, including those that affect the interpretation of the main claim.
- Findings situated in the literature, with both supporting and contradictory work cited.
- Speculation is labeled as speculation; "first to show" claims are defensible.

**References and supplementary material**

- All key recent papers cited; no excessive self-citation.
- Public data and code deposited with persistent identifiers (GEO, SRA, ENA, PRIDE, Zenodo, GitHub with release tag).

### 5. Figure and data-integrity check

- Western blots / gels / microscopy: no evidence of splicing, duplication, or contrast manipulation; raw uncropped images in supplementary.
- Statistics: error bars defined (SD vs. SEM vs. CI), n values match the text.
- Color: colorblind-accessible; legends interpretable in greyscale.
- Scale bars and axis units present.
- Image-based manuscripts (gel, blot, histology, microscopy): some publishers (e.g., *Nature* portfolio) require the *original* full-resolution image files for editorial screening. Flag obvious data-integrity concerns as a major issue and include a recommendation in the confidential section.

### 6. Tone and ethics checks

- Constructive framing: every criticism is paired with a suggestion or a question.
- No personal attacks, sarcasm, or pejorative adjectives.
- No "the authors should have done X for my own research" or out-of-scope experiments.
- No confidential comments that contradict what is said to the authors; the two halves of the report should be consistent.

### 7. Finalize recommendation

Choose a recommendation that follows from the issues identified:

- **Accept as is** — exceptional, with no substantive issues; extremely rare.
- **Minor revision** — clear soundness, but presentation, clarity, or one or two clarifications needed.
- **Major revision** — soundness could be defended with additional analyses, controls, or reframing; not a rejection.
- **Reject** — fundamental methodological flaws, scope mismatch, or insufficient contribution; explain whether resubmission would be welcome.
- **Reject without prejudice (desk-reject) — escalate to editor only**, not in the authors' section.

Be explicit in the confidential section about whether the manuscript, in your view, falls below the journal's bar irrespective of revision.

## Code patterns

### Standard review-report skeleton (used by the journal's submission system)

```text
================================================================================
REVIEW OF [Manuscript ID], "[Title]"
================================================================================

1. Summary
-----------
[2-4 sentence synopsis in your own words. State the question, the approach,
 the main finding, and your initial overall impression. Avoid copying the
 abstract verbatim.]

2. Major issues
---------------
M1. [Issue title]
    Concern: [what is wrong and why it matters]
    Suggested fix: [specific additional analysis, control, or rewrite]
    Importance: [essential / conditional]

M2. ...

3. Minor issues
---------------
m1. [Section, line, or figure number] — [concise fix or clarification]
m2. ...

4. Constructive feedback / questions for the authors
---------------------------------------------------
- [open question or suggestion that does not block publication]
- ...

5. Reporting checklist compliance
----------------------------------
Checklist applied: [e.g., CONSORT 2010]
- Item 6a (outcomes): addressed, Methods p. 8
- Item 12a (statistical methods): partially addressed; specify
  the multiple-comparison correction
- Item 23 (registration): missing; no trial registry number
- ...

6. Confidential comments to the editor
---------------------------------------
[Recommendation: Minor revision / Major revision / Reject]
[Brief rationale, any COI, citation of the journal's own standards,
  notes on data integrity, fit with the journal's bar, suitability of
  suggested reviewers, comments the editor should know but the authors
  should not see.]

7. Recommendation
-----------------
[Accept / Minor revision / Major revision / Reject]
```

### Reusable section-by-section rubric

| Section | Look for | Common failure mode |
|---|---|---|
| Abstract | Conclusions match data; no over-claiming | "Promising" results described as "definitive" |
| Introduction | Clear gap; balanced lit | Manufactured gap; uncited counter-evidence |
| Methods | Reproducible; pre-registered; stats justified | No power analysis; software versions missing |
| Results | Effect sizes + CI; negative results shown | p-values without effect size; selective panels |
| Discussion | Limitations explicit; no causal overreach | Speculation dressed as conclusion |
| Figures | Self-contained legends; colorblind-safe | Truncated axes; SEM mislabeled as SD |
| Code/data | Public with DOI | "Available upon request" |

### Red-flag phrases to surface to the editor (confidential section)

- Plagiarism or self-plagiarism (overlap with the authors' prior work without citation).
- Image manipulation in figures (e.g., spliced gel bands without demarcation).
- Data fabrication (results that cannot be reproduced from deposited data).
- Authorship disputes (ghost or guest authorship surfaced via outlier contributions).
- Ethics concerns (no IRB / IACUC, retrospective use of identifiable data without consent).
- AI / LLM-generated content (most journals now require disclosure; undisclosed substantial AI use is a publishable issue).

## Common pitfalls

- **Reading too fast**: a single-pass review of a 30-page manuscript misses buried issues. Plan a first read for novelty / soundness, a second read for checklist items, a third for figures and statistics.
- **Pursuing an out-of-scope agenda**: requesting the authors rerun the experiment with your preferred technique is not a fair request; it is a preference.
- **Vague criticism**: "the methods are weak" is un-actionable. Always pair a critique with a suggested fix.
- **Contradicting yourself**: if you tell the editor "borderline reject" but the authors' section says "minor revision," the editor will be confused. Keep the two halves aligned.
- **Revealing identity in a double-blind review**: even small clues (citing your own work, identifying the institution) can unblind you.
- **Mixing the report with the cover letter to authors**: some journals do not send the cover letter to authors; keep all substantive feedback inside the report itself.
- **Forgetting confidential comments to the editor**: things like "I have a conflict of interest to disclose" or "this manuscript does not meet the journal's bar" belong in the confidential section, not in the body of the review.

## Validation

A good review is itself a small scientific document. Before submitting, check:

- [ ] The summary is in your own words and captures the manuscript's essence in 2–4 sentences.
- [ ] Each major issue explains (a) the problem, (b) why it matters, (c) a specific remedy, and (d) its importance.
- [ ] Every reporting-checklist item has been accounted for; missing items are flagged with a clear request.
- [ ] The recommendation follows logically from the issues you have raised.
- [ ] The two halves of the report (authors / editor) are mutually consistent.
- [ ] Tone is constructive throughout, even on rejection.
- [ ] Confidentiality preserved (no sign of identity in a double-blind review; no quote of unpublished data shared in other contexts).
- [ ] Conflict of interest disclosed in the confidential section even if declared at acceptance.
- [ ] Deadline respected, or extension requested proactively.

## Open alternatives

- **Closed review platforms (e.g., Editorial Manager, ScholarOne)** are proprietary; their open-source equivalents include **Open Journal Systems (OJS)** with PKP's pre-built review workflows and **Janeway** (open-source journal hosting). For preprint-first review, consider **Review Commons** (independent refereed preprint review) and **Publons / Web of Science Reviewer Recognition** (the latter closed-source but widely used).
- **Closed reference managers (EndNote, Reference Manager)** can be replaced with open tools — **Zotero** with **Better BibTeX**, **JabRef** — that also support shared group libraries for editorial work.
- **AI assistants for "sanity-checking" a draft review** are useful for prose polish, but the evaluator's judgment remains the deciding factor; never paste unpublished manuscript text into a third-party LLM without the editor's approval.

## References

### Internal cross-links

- `ors-peer-review-grant-review` — analogous review workflow for research proposals.
- `ors-peer-review-scholar-evaluation` — for assessing an individual's record, not a single paper.
- `ors-peer-review-reviewer-response` — for the author's reply once reviews are in.
- `ors-scientific-writing-manuscript-structure` — IMRAD structure, useful for orienting what to look for.
- `ors-scientific-writing-response-to-reviewers` — author's side of the same process.
- `ors-ethics-compliance-irb` — ethics / IRB framing for the methods section.
- `ors-open-science-data-sharing` — data and code deposition expectations.

### External links (verifiable, public)

- ICMJE Recommendations: <https://www.icmje.org/icmje-recommendations.pdf>
- EQUATOR Network: <https://www.equator-network.org/>
- CONSORT: <https://www.consort-statement.org/>
- STROBE: <https://www.strobe-statement.org/>
- PRISMA 2020: <https://www.prisma-statement.org/>
- ARRIVE 2.0: <https://arriveguidelines.org/>
- MIAME (FGZC reference): <https://www.fgcz.ch/2018/09/13/MIAME.html>
- MINSEQE: <http://www.fged.org/projects/minseqe/>
- TRIPOD: <https://www.tripod-statement.org/>
- SPIRIT: <https://www.spirit-statement.org/>
- CARE: <https://www.care-statement.org/>
- CHEERS: <https://www.cheers-statement.org/>
- COPE Peer Review guidance: <https://publicationethics.org/resources/guidelines/peer-review>
- Elsevier — Role of a reviewer: <https://www.elsevier.com/reviewers/role>
- Nature — Editorial processes / peer review: <https://www.nature.com/nature-portfolio/editorial-processes/peer-review>

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Heavy rewrite of upstream peer-review skill: removed embedded schematic-generator script instructions (kept as cross-link), added EQUATOR-checklist routing table for 10 manuscript types, added image-integrity red-flag list, added journal-fit / COI / double-blind etiquette sections, replaced detailed step lists with rubric tables for faster reuse.