---

name: cover-letter
description: "Crafts a cover letter to a biomedical journal editor: addressing the editor, novelty statement, suggested and recommended-against reviewers, conflicts of interest, what not to say, and how to respond to a desk-rejection for 'out of scope'."
license: MIT
---




<!-- metadata:
category: scientific-writing
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - scientific-writing
  - research
difficulty: intermediate
-->

# Cover Letter to Journal Editor

> The cover letter is the first document the editor reads and the only document written directly to the editor. It is the place to make the case for novelty, fit, and integrity — and to disclose anything the manuscript text cannot disclose. A well-crafted cover letter can move a borderline-fit manuscript into the review queue; a poorly crafted one can move a clearly fit manuscript into the desk-reject pile. This skill encodes the structure, the disclosures, the reviewer suggestions, and the response to an "out of scope" decision.

## When to use

- Submitting a primary research article, brief report, or methods paper to a peer-reviewed biomedical journal.
- Resubmitting to a different journal after a prior desk-rejection.
- Requesting transfer-of-review (use of an existing peer-review file from a previous journal).
- Responding to an editorial "out of scope" or "not a fit" decision.
- Requesting a specific handling editor (e.g., an editor with relevant expertise).

## When NOT to use

- For conference abstracts (use the conference template; no cover letter).
- For book chapters (different norms; consult the publisher).
- For preprint server submissions (no cover letter required).
- For corrigenda or errata (no cover letter; use the journal's correction form).
- For clinical case reports (some journals require a cover letter, but the form is shorter and the novelty case is different).

## Prerequisites

- Completed manuscript draft with finalized title, abstract, and author list.
- Decision on target journal (or a shortlist of two, with the first-choice named in the letter).
- ICMJE authorship confirmation from all co-authors.
- Conflict-of-interest disclosures collected from all co-authors.
- A short list of 4-6 suggested reviewers and 1-2 recommended-against reviewers (journal-dependent).

## Core workflow

### 1. Identify the handling editor by name

If the journal lists handling editors by subject area (most Nature-family, PLOS, BMC, and Cell-family journals do), address the cover letter to the specific editor whose scope matches the manuscript. Generic "Dear Editor" letters are acceptable but signal that the authors did not read the journal's editorial scope page.

### 2. Open with a one-sentence identification of the manuscript and the submission type

Sentence 1: title, authors, and submission category. This sentence exists so the editor does not have to open the manuscript file to know what is being submitted.

### 3. State the novelty in one or two sentences

The novelty statement is the core of the cover letter. It answers: "Why is this manuscript different from the 20 others the editor has on the desk this week?" The novelty must be specific (a number, a mechanism, a population) and not generic ("we report a comprehensive analysis of...").

### 4. State the fit in one sentence

The fit sentence answers: "Why this journal?" It is the link between the novelty and the journal's scope. For high-impact general journals, the fit sentence is often: "To our knowledge, this is the first [broad claim type] and we believe it will interest [journal-name's] broad readership." For specialty journals, the fit sentence is more specific.

### 5. Disclose everything that must be disclosed

The cover letter is the place to disclose:
- Conflicts of interest (financial, personal, institutional).
- Funding sources.
- Preprint posting (with DOI and date).
- Prior conference presentation.
- Prior submission to another journal (and the outcome, if relevant).
- Any author with a dual affiliation that may bias the review.
- Patient or animal study ethics approval (often also in Methods, but a cover-letter note is good practice).

### 6. Suggest reviewers and recommended-against reviewers

Most biomedical journals request suggested reviewers; some also accept recommended-against reviewers. The journal's editorial system will often have a separate field for this; the cover letter can include a short list as a back-up.

### 7. Close with a courteous line and the corresponding author contact

Close with: "Thank you for considering our manuscript for [journal-name]. We look forward to your decision." Include the corresponding author's email and ORCID.

## Code patterns

### Standard cover letter template

```
[Date]

[Editor's name and title]
[Journal name]
[Editorial office address]

Dear Dr. [Last name],

We are pleased to submit our manuscript entitled "[Title]" for
consideration as a [Article / Brief Report / Research Letter] in
[Journal name]. The work is co-first-authored by [Name 1] and
[Name 2] and the full author list is [Last names et al.].

In this study, we show that [one-sentence novelty statement, with a
specific number, mechanism, or population]. [Optional second sentence:
how the result advances the field.] To our knowledge, this is the
first [broad claim] and we believe it will interest [Journal name]'s
readership in [field].

The manuscript is not under consideration at any other journal, and
all authors have approved the submitted version. We confirm that the
study was conducted in accordance with [IRB / IACUC / Helsinki]
guidelines under protocol [number]. All authors declare no conflicts
of interest. Funding was provided by [funder, grant number].

[If applicable: A preprint of this manuscript was posted on bioRxiv
on [date] (DOI: ...). The work was presented in part at [conference,
date].]

We suggest the following potential reviewers, all of whom have
relevant expertise and have not collaborated with us in the past 5
years: [Name, affiliation, email]. We respectfully request that
[Name, affiliation] not be considered as a reviewer, because [brief
reason — active collaboration / co-authorship within 5 years /
competing work].

Thank you for considering our manuscript for [Journal name]. Please
direct correspondence to [corresponding author name, email, ORCID].

Sincerely,
[Corresponding author name, title, affiliation]
```

### Worked example: clinical-trial cover letter (NEJM-style)

```
January 15, 2026

Dr. Jane Smith
Editor-in-Chief
The New England Journal of Medicine
10 Shattuck Street
Boston, MA 02115

Dear Dr. Smith,

We are pleased to submit our manuscript entitled "STM2457 plus
temozolomide for METTL3-high recurrent glioblastoma: a phase 2
randomized controlled trial" for consideration as an Original
Article in The New England Journal of Medicine. The work was
co-led by Dr. A. Lee, Dr. B. Park, and Dr. C. Wu, with the full
author list provided in the manuscript.

In this randomized, double-blind, placebo-controlled trial of 172
patients with METTL3-high recurrent glioblastoma, the addition of
the oral METTL3 inhibitor STM2457 to temozolomide improved median
overall survival from 11.2 to 14.8 months (HR 0.71, 95% CI
0.55-0.92; P=.008). To our knowledge, this is the first phase 2
trial of a METTL3 inhibitor in glioblastoma and the first
biomarker-enriched trial in this disease.

The study was conducted in accordance with the Declaration of
Helsinki under IRB protocols [numbers]. All patients provided
written informed consent. The trial is registered at
ClinicalTrials.gov (NCT########). The full protocol and
statistical analysis plan are provided as supplemental files.

All authors declare no competing financial interests. The trial
was funded by the National Cancer Institute (R01CA########) with
drug and placebo supplied by [Sponsor]. The funder had no role in
study design, data analysis, or manuscript preparation.

We suggest the following potential reviewers with relevant
expertise in glioblastoma clinical trials and RNA-biology
therapeutics: [Name 1, affiliation, email], [Name 2, ...], [Name
3, ...], [Name 4, ...]. We respectfully request that Dr. X. Zhang
not be considered, as he is a current co-investigator on a
competing trial.

Thank you for considering our manuscript. We look forward to your
decision.

Sincerely,
Aisha Lee, MD, PhD
Department of Neuro-Oncology
[Institution]
aisha.lee@institution.edu
ORCID: 0000-0000-0000-0000
```

### Worked example: basic-science cover letter (Nature-style)

```
January 15, 2026

Dr. [Handling Editor Name]
Editor, [Specialty], Nature
[Editorial address]

Dear Dr. [Last name],

We wish to submit our manuscript entitled "A single-cell atlas of
METTL3-dependent m6A deposition in the aging mouse hippocampus"
for consideration as an Article in Nature. This work is a
collaboration between [Lab 1] and [Lab 2]; the full author list
is provided in the manuscript.

In this study, we combined single-nucleus RNA-sequencing with
m6A-immunoprecipitation (snRNA-m6A-seq) to profile m6A deposition
across 1.2 million single nuclei from the hippocampus of young
(3-month) and old (24-month) mice. We identify an age-associated
shift in METTL3-dependent m6A marks on transcripts encoding
synaptic components, and we show that conditional knockout of
Mettl3 in the dentate gyrus rescues age-related synaptic
deficits. To our knowledge, this is the first single-cell
m6A-atlas of the aging brain and the first demonstration that
restoring METTL3-dependent m6A deposition reverses synaptic
decline in vivo.

The manuscript has not been published and is not under
consideration elsewhere. A preprint was posted on bioRxiv on
December 1, 2025 (DOI: 10.1101/2025.12.01.123456). The work was
presented in part at the Society for Neuroscience Annual Meeting
in November 2025. All animal procedures were approved by the
[Institution] IACUC under protocol [number].

All authors declare no conflicts of interest. Funding was
provided by NIH grants R01AG######## (to A. Lee) and
R01GM######## (to B. Park). A. Lee is a co-founder of [Company X]
and holds equity; this is disclosed in the manuscript. The
company had no role in the design or analysis of the study.

We suggest the following potential reviewers, all with expertise
in RNA modifications, single-cell genomics, or hippocampal
physiology: [4-6 names with affiliations and emails]. We
respectfully note that Dr. Y. Tanaka has an active competing
manuscript on a similar topic and we request that he not be
considered.

Thank you for your time and consideration.

Sincerely,
Aisha Lee, MD, PhD
[Institution]
[Email, ORCID]
```

### Reviewer suggestion discipline

Good reviewer suggestions have four properties:
1. **Recent relevant publication** (last 3-5 years) in the topic of the manuscript.
2. **No collaboration in the last 5 years** (no co-authorship, no grant, no close mentee relationship).
3. **Email is current and institutional** (verify by checking the reviewer's current institution page).
4. **Diversity of geography and perspective** (avoid suggesting four reviewers from the same lab network).

Common pitfalls in reviewer suggestion:
- Suggesting a former mentor or close collaborator (the editor may verify).
- Suggesting reviewers from the authors' own institution (the editor will reject these).
- Suggesting reviewers who work in the exact same niche (potential bias).
- Suggesting reviewers from a competing group with a paper in press (the editor may exclude them).
- Failing to verify the email (the editor cannot deliver the invitation).

### Recommended-against reviewers

Some journals (e.g., Nature, Science, Cell-family, PLOS) accept a short list of "non-preferred" reviewers. The reasons must be specific and non-adversarial:
- Active co-authorship in the last 5 years.
- Direct grant funding from the same agency with overlapping aims.
- Competing manuscript in press or recent publication on the same question.
- Prior unresolved dispute or allegation of bias.

Do not list recommended-against reviewers as a way to block critical voices. The editor may ignore the request, and the request itself can be a flag of editorial risk.

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| "Dear Editor" without a name | Signals the author did not identify the handling editor | Address a specific editor by name and title |
| Novelty statement is generic ("we provide a comprehensive analysis") | Editor has read this sentence 20 times today | Lead with a number, a specific mechanism, or a specific population |
| Cover letter repeats the abstract | Editor has not asked for the abstract; it's in the manuscript | Use the cover letter for novelty, fit, disclosures — not for content |
| Suggests reviewers from the same institution as the authors | Editor will reject the suggestions | Cross-check institutional affiliations |
| Fails to disclose a prior submission to another journal | The editor may discover it during the review process | Disclose transparently in the cover letter |
| Hedges the novelty ("we believe our study may contribute") | Editors prefer a confident novelty statement | State the novelty in declarative terms |
| Lists too many reviewers (10+) | Editor will pick 2-3 anyway; the rest is wasted | Suggest 4-6 strong candidates |
| Lists no recommended-against reviewers when a competing group exists | A reviewer from the competing group will deliver a hostile review | Disclose the competing group transparently |
| No funding disclosure in the cover letter | Many journals require the cover letter to mirror the manuscript | Mirror the manuscript's Funding and COI sections |
| Generic "we look forward to hearing from you" | Forgettable close | Add a specific next step: "We are available to provide additional data or analyses as needed" |

## Response to an "out of scope" decision

A desk-rejection for "out of scope" or "not a fit for our readership" is one of the most common editorial decisions. The cover letter is not the right place to argue against the decision; the right place is a polite, brief response.

### Standard response template

```
Dear Dr. [Editor name],

Thank you for letting us know your editorial decision on our
manuscript "[Title]". We appreciate the time your team spent
considering our work.

We respectfully disagree with the assessment that the manuscript
is out of scope for [Journal name]. [One or two sentences on
why: prior articles in the journal on similar topics, the broad
interest of the question, the mechanism's relevance to a
readership that includes [discipline].]

[Optional: We would be willing to expand the discussion of [topic
X] to make the relevance to [Journal name]'s readership more
explicit.]

We would therefore like to request that the editorial team
reconsider the decision. If after reconsideration the editorial
team still feels the work is a better fit elsewhere, we would
welcome a transfer-of-review recommendation to [specific other
journal].

Thank you again for your consideration.

Sincerely,
[Corresponding author]
```

If the journal offers a transfer-of-review service (e.g., BMC, Nature, PLOS, eLife), use it: the existing peer-review file moves with the manuscript, saving 2-4 months. If the editor does not offer a transfer, request one explicitly.

## Validation

A cover letter passes validation when:

- The handling editor is named and addressed by name.
- The novelty statement is specific (a number, a mechanism, a population) and not generic.
- The fit sentence is present and explicit.
- All ICMJE-required disclosures (authorship confirmation, ethics approval, conflicts of interest, funding, prior presentation, prior submission, preprint) are included.
- The suggested-reviewer list has 4-6 candidates with current institutional emails, no collaborators, no co-authors in the last 5 years.
- The recommended-against-reviewer list (if used) has specific, non-adversarial reasons.
- The corresponding author's contact email and ORCID are present.
- The cover letter is a single page; if it runs to two pages, the disclosures are excessive.

## Open alternatives

For commercial submission systems, the open alternatives are:

| Commercial / journal-specific | Open alternative |
|------------------------------|------------------|
| Editorial Manager (Aries) | Open Journal Systems (OJS), Janeway |
| ScholarOne Manuscripts | OJS |
| eJournalPress | OJS |

The cover letter content itself is independent of the submission system.

## References

- ICMJE Recommendations. icmje.org/icmje-recommendations.pdf
- Nature author guidelines. nature.com/nature-portfolio/editorial-policies/submission
- Science author information. science.org/content/page/information-authors
- Cell author guidelines. cell.com/cell/authors
- BMJ cover letter guidance. bmj.com/about-bmj/resources-authors
- COPE conflict-of-interest framework. publicationethics.org
- COPE authorship discussion document. publicationethics.org/authorship

## Related Skills

- ors-scientific-writing-manuscript-structure — for the manuscript that the cover letter introduces.
- ors-scientific-writing-rebuttal-letter — for the rebuttal after peer review.
- ors-scientific-writing-response-to-reviewers — for the point-by-point response document.
- ors-scientific-writing-ai-disclosure-writing — for the AI/LLM usage statement.
- ors-ethics-compliance-coi-disclosure — for the broader conflict-of-interest framework.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Consolidated public cover-letter guidance (ICMJE, Nature/Science/Cell author pages, COPE). Worked examples for clinical-trial and basic-science submissions; suggested-reviewer and recommended-against-reviewer discipline; "out of scope" response template. No specific journal policies are quoted verbatim; all sources are publicly accessible.