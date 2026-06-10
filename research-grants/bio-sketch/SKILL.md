---
name: ors-research-grants-bio-sketch
display_name: "NIH/NSF Biographical Sketch via SciENcv"
description: "Use when generating an NIH or NSF Biographical Sketch in SciENcv (current format): personal statement, contribution statements (new 2025 NIH format), positions and honors, research support. Covers NIH vs NSF differences."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: research-grants
tags: [bio-sketch, sciencv, orcid, biosketch, personal-statement, contributions]
difficulty: intermediate
prerequisites:
  - tools: [SciENcv (my.ncbi.nlm.nih.gov), eRA Commons, ORCID, MyBibliography]
  - skills: [ors-research-grants-nih-r01, ors-research-grants-nsf-standard, ors-research-grants-nih-k-series]
sources_consulted:
  - "NIH: Biosketch format and instructions (grants.nih.gov/grants/forms.htm)"
  - "NIH: SciENcv FAQ and personal-statement / contribution-statement guidance"
  - "NIH: Format change in 2021 (Personal Statement expanded; Contributions to Science section retained); subsequent refinements"
  - "NSF: Biographical Sketch format and SciENcv NSF format"
  - "Improvisions: Side-by-side NIH vs NSF comparison, the contribution-statement pattern, the SciENcv-edit-then-export workflow"
last_updated: 2026-06-10
tool_type: writing
primary_tool: human
---

# NIH/NSF Biographical Sketch via SciENcv

> A working framework for generating the NIH or NSF Biographical Sketch in SciENcv (Science Experts Network Curriculum Vitae). The biosketch is the second-most-revised document in any NIH submission (after the Specific Aims). SciENcv is the canonical generator for both NIH and NSF biosketches; the format is agency-specific. This skill covers the current format, the new contribution-statement pattern, the personal-statement pattern, and the NIH vs NSF differences.

## When to use

- Creating or updating an NIH Biographical Sketch via SciENcv for an R01, R21, K-series, or F-series application.
- Creating or updating an NSF Biographical Sketch via SciENcv for a Standard Research Proposal, CAREER, RAPID, EAGER, or research-equipment proposal.
- Drafting the Personal Statement (NIH) and its NSF equivalents.
- Drafting Contribution Statements (NIH) — the post-2021 change that allows up to 4 contributions per PI.
- Linking SciENcv to ORCID, eRA Commons, and MyBibliography for automatic data pulls.
- Mapping the same source data to both NIH and NSF biosketches without duplicating data entry.

## When NOT to use

- This is not the right skill for the Research Strategy or the Specific Aims.
- This is not the right skill for the Biosketch used in DOD CDMRP, ERC, or DARPA BAA — those have their own CV/biosketch formats.
- This is not the right skill for the ResearchGate, Google Scholar, or institutional CV.
- This is not the right skill for the candidate's personal website or LinkedIn profile.

## Prerequisites

- An ORCID iD. ORCID is the persistent identifier that links SciENcv, MyBibliography, and federal-grant submissions.
- An eRA Commons account (for NIH submissions) or a NSF account (for NSF submissions). SciENcv can be used without an eRA Commons account, but the export to an application will require linkage.
- A MyBibliography (NIH's reference manager) populated with the candidate's publications, including preprints, journal articles, book chapters, and datasets.
- The candidate's funding history: past and current grants, with dates, funding-IC, and total direct costs.

## Core workflow

1. **Decide which agency's format is being generated.** The NIH biosketch has Personal Statement, Positions and Honors, Contributions to Science, and Research Support sections. The NSF biosketch has a different structure (see comparison table). SciENcv supports both, but the formats are not interchangeable.

2. **Link ORCID, eRA Commons (if applicable), and MyBibliography** in SciENcv. The data flow is: ORCID = identity, MyBibliography = publications, eRA Commons = federal grants. With these three linked, SciENcv auto-populates most biosketch fields.

3. **Draft the Personal Statement (NIH).** The Personal Statement is a short narrative (≤1 page) that explains how the candidate is positioned for the proposed project. It is not a CV summary; it is a 4-paragraph argument linking the candidate's prior work to the proposed work.

4. **Draft the Contribution Statements (NIH).** The post-2021 NIH biosketch allows up to 4 Contribution Statements. Each Contribution Statement is a 1-page narrative that frames a research line, lists up to 4 representative publications, and describes the candidate's role on those publications. The 4 contributions are typically organized as research lines (e.g., "X pathway in cancer," "Y methodology development," "Z clinical translation").

5. **Confirm the Positions and Honors section** is complete with academic appointments, training history, and relevant honors (with year).

6. **Confirm the Research Support section** is complete with current and completed support, including project number, dates, total direct costs, and the candidate's role (PI, Co-I, Subaward PI). NIH requires this section; do not omit it.

7. **Generate the PDF** via SciENcv. SciENcv produces a PDF that meets the agency's format requirements. The PDF is the artifact that is uploaded into ASSIST (NIH) or Research.gov / FastLane (NSF).

8. **Verify the format.** Each agency has specific format requirements (font, margin, page limit). The SciENcv default is generally compliant, but a manual check is necessary if the candidate has hand-edited sections.

9. **Co-review with the Research Strategy.** The Personal Statement cites the proposed project and names the team; the Contribution Statements should align with the Aims. A Personal Statement that names "Dr. X, an expert in CRISPR" but no CRISPR Aim in the Aims is a flag.

## Document patterns

### Personal Statement (NIH; ≤1 page)

```markdown
# Personal Statement

## Sentence 1: The candidate's research theme.
## Paragraph 1: Why the candidate is positioned.
- Prior training and degrees.
- Prior funding and key publications.
- Mentorship record (if K or F).

## Paragraph 2: How the candidate's prior work connects to the proposed project.
- 2–4 representative publications with a one-sentence role description.
- The prior work that grounds the Aims.

## Paragraph 3: The team and the role on the project.
- The candidate's specific role (PI, Co-I, Lead of Aim X).
- The collaborators / co-investigators and their role.

## Paragraph 4: The institutional environment.
- The institution's resources, the department, the cores, the
  clinical infrastructure (if relevant).
```

### Contribution Statement (NIH; 1 page each, up to 4 total)

```markdown
# Contribution to Science 1: [Title, e.g., "Elucidating the role of X in Y"]

## Background and significance (3–4 sentences)
- Why this contribution matters.

## Key findings (3–5 sentences)
- The substantive findings the candidate made.

## Representative publications (up to 4)
1. [Pub #1, full citation]. [One sentence on the candidate's role.]
2. [Pub #2, full citation]. [One sentence on the candidate's role.]
3. [Pub #3, full citation]. [One sentence on the candidate's role.]
4. [Pub #4, full citation]. [One sentence on the candidate's role.]
```

### Research Support (NIH; complete list of current and completed)

```markdown
## Current Support
- [Grant #], [Funding IC], [Project Title]
  Period: [start] – [end], Total direct costs: $[X]
  Role: PI / Co-I / Subaward PI
  Goal: [One sentence on the project goal.]

- ...

## Completed Support (last 3 years)
- ...
```

### NSF biosketch structure (current)

The NSF biosketch in SciENcv has these sections, in this order:

```markdown
# Biographical Sketch

## (a) Professional Preparation
- [PhD, postdoc, etc., institution, year]

## (b) Appointments
- [Current and prior positions]

## (c) Products
- (i) Up to 5 products most closely related to the proposed project
- (ii) Up to 5 other significant products, whether or not related
- (iii) Optional: additional products (datasets, software, etc.)

## (d) Synergistic Activities
- 1 paragraph on activities that complement the proposed work
  (mentoring, K-12 outreach, professional service, etc.)

## (e) Collaborators & Other Affiliations
- Single-page template from the current PAPPG
- Information on collaborators, foreign partners, advisors, etc.
```

### NIH vs NSF biosketch comparison (one-page view)

| Element | NIH | NSF |
|---------|-----|-----|
| Page limit | 5 pages | 3 pages (Standard Research Proposal) |
| Personal statement | Yes (≤1 page) | No direct equivalent (replaced by Products + Synergistic Activities) |
| Contributions to Science | Yes (up to 4 statements) | No direct equivalent |
| Research Support | Yes (current + completed) | No direct equivalent (covered by Current and Pending Support, separate document) |
| Synergistic Activities | No | Yes (1 paragraph) |
| Professional Preparation | Part of Positions and Honors | Yes (own section) |
| Products | Not a section; embedded in Contributions | Yes (up to 5 closest + 5 other) |
| Collaborators & Other Affiliations | In Other Support / Foreign components (separate forms) | Yes (PAPPG single-page template) |
| Format generator | SciENcv | SciENcv |
| Persistent identifier | ORCID | ORCID |
| Page-by-page font/margin | NIH-standard | PAPPG-defined |

### SciENcv edit-then-export checklist

```text
[ ] ORCID linked.
[ ] eRA Commons linked (for NIH).
[ ] MyBibliography populated.
[ ] Personal Statement: 4 paragraphs, ≤1 page, names the proposed project.
[ ] Contribution Statements: up to 4 statements, each with up to 4 publications
    and the candidate's role.
[ ] Positions and Honors: complete with year.
[ ] Research Support: current and completed; project number, dates, costs, role.
[ ] Generated PDF: NIH format.
[ ] Generated PDF: NSF format (if needed).
[ ] Format check: page limit, font, margin, no orphaned section headers.
[ ] Co-reviewed with the Aims: Personal Statement names the proposed project's
    Aims and team.
```

## Common pitfalls

- **Personal Statement that rehashes the CV.** The Personal Statement is a narrative, not a list. The CV lives in MyBibliography.
- **Contribution Statements that list 4 papers with no narrative.** Each contribution is a story; the papers are evidence. A contribution without a narrative is a flagged line in the biosketch.
- **Personal Statement that does not name the proposed project.** A reviewer reading the Personal Statement and the Aims should be able to map one to the other.
- **Research Support section that omits current support.** The Research Support section is required and is reviewed for overlap with the proposed project. Omitting a current grant is a flag.
- **NIH biosketch submitted in NSF format (or vice versa).** The two are not interchangeable. SciENcv generates both; verify the format before submission.
- **Contributions that duplicate Aims from a prior rejected submission without updating.** Contribution statements must be current; they are reviewed against the publication record.
- **Foreign collaborations not declared.** The biosketch is one of the documents where foreign-component status is checked. The Other Support / Foreign components disclosure is a separate form.
- **For K and F applications: mentorship record missing.** K and F biosketches must include the mentorship / training history, including the postdoc / graduate mentor's name, dates, and the candidate's role on resulting publications.
- **Page-limit over-runs.** The NIH biosketch is 5 pages. The NSF biosketch in a Standard Research Proposal is 3 pages. The format is enforced.
- **Hand-edited PDF that no longer matches SciENcv.** Once a candidate hand-edits the PDF, the link to the source data is broken. Use SciENcv as the canonical source.

## Validation

- The biosketch is at the agency's page limit.
- The Personal Statement (NIH) names the proposed project and the candidate's role.
- The Contribution Statements (NIH) are each ≤1 page with up to 4 representative publications.
- The Research Support (NIH) is complete with current and completed support.
- The NSF biosketch has the 5 sections in the right order.
- The Synergistic Activities (NSF) is 1 paragraph on mentorship / outreach / service.
- SciENcv's source data is linked to ORCID, MyBibliography, and eRA Commons (NIH).
- The biosketch is co-revisioned with the Specific Aims / Project Description.
- The PDF passes the agency's submission-portal format check.

## Open alternatives

- **SciENcv vs. ORCID alone.** ORCID alone is a persistent identifier, not a CV generator. SciENcv generates the agency's required format from ORCID-linked data.
- **NIH biosketch (5 pp) vs. NIH Other Support (1 pp per project).** The Other Support form is a separate disclosure (current and pending support, foreign components). It is a different document.
- **NSF SciENcv vs. NSF fillable PDF.** NSF accepts SciENcv; the fillable PDF is being phased down. Use SciENcv.
- **MyBibliography vs. ORCID Works.** MyBibliography is the NIH reference manager; ORCID Works is the ORCID record. Link them so updates propagate.
- **ORCID iD vs. eRA Commons ID.** ORCID is global; eRA Commons is NIH-specific. Link them in SciENcv so the export uses the correct IDs.

## References

- NIH: [Biosketch format and instructions](https://grants.nih.gov/grants/forms.htm) — current NIH biosketch format.
- NIH: [SciENcv](https://www.ncbi.nlm.nih.gov/sciencv/) — the biosketch generator.
- NIH: [MyBibliography](https://www.ncbi.nlm.nih.gov/books/NBK53595/) — NIH's reference manager.
- NIH: [eRA Commons](https://era.nih.gov/) — federal-grant submission and award system.
- NIH: [Other Support format](https://grants.nih.gov/grants/forms.htm) — separate from the biosketch; current and pending support.
- NSF: [Biographical Sketch and Current and Pending Support](https://www.nsf.gov/bfa/dias/policy/pappg) — current PAPPG Chapter II.D.2.h.
- NSF: [PAPPG](https://www.nsf.gov/bfa/dias/policy/pappg) — current edition.
- ORCID: [ORCID iD registry](https://orcid.org/) — persistent identifier.
- NCBI: [SciENcv FAQ](https://www.ncbi.nlm.nih.gov/sciencv/faq/) — usage and linkage guidance.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram.