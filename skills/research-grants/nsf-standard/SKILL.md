---
name: nsf-standard
description: "Use when planning, drafting, or revising an NSF Standard Research Proposal:
  Project Description (15 pp), Data Management Plan, Postdoc Mentoring Plan, Broader
  Impacts, biographical sketch via SciENcv, and current PAPPG compliance.
license: MIT
---

<!-- metadata:
category: research-grants
version: 1.0.0
author: Pradyumna Jayaram
tags:
- nsf
- pappg
- project-description
- broader-impacts
- biographical-sketch
- sciencv
difficulty: advanced
prerequisites:
  tools:
  - SciENcv
  - Research.gov
  - FastLane
  skills:
  - ors-research-grants-bio-sketch
sources: 'NSF: Proposal & Award Policies & Procedures Guide (PAPPG), current edition;
  NSF: biographical sketch / SciENcv guidance; NSF: Data Management Plan policy and
  revised 2-page DMP template; NSF: Postdoctoral Researcher Mentoring Plan requirement;
  Improvisions: explicit Broader Impacts vs. Intellectual Merits separation, PAPPG
  versioning check'
-->

# NSF Standard Research Proposal

> A working framework for assembling, self-reviewing, and submitting an NSF Standard Research Proposal under the current Proposal & Award Policies & Procedures Guide (PAPPG). The default scope is a single-PI research proposal to a single program; CAREER, RAPID, EAGER, and IUCRC have additional rules noted where relevant.

## When to use

- Drafting a new unsolicited or program-targeted Standard Research Proposal.
- Building the Project Description (15 pages) under the two-merit-review framework: Intellectual Merit and Broader Impacts.
- Writing a 2-page Data Management Plan (DMP) and a 1-page Postdoc Mentoring Plan (if postdocs are on the budget).
- Preparing a biographical sketch via SciENcv in the current format.
- Verifying PAPPG compliance — current PAPPG edition, page limits, font, margins, section order.

## When NOT to use
"
- This is not a CAREER proposal. CAREER adds the "Facilitating Career Development" and "Departmental Letter" attachments and has its own 3-year minimum budget and educator/early-career review framework.
- This is not an IUCRC or a center proposal.
- This is not a fellowship. NSF GRFP and similar fellowship proposals use a different package (see `ors-research-grants-fellowships`).
- This is not the equipment or conference-proposal track, which have shorter limits.

## Prerequisites

- A working knowledge of the current PAPPG edition. Verify the PAPPG version on the [NSF PAPPG page](https://www.nsf.gov/bfa/dias/policy/pappg) before drafting; the version number changes on a schedule and the page limits, font, and required sections can change with it.
- A program announcement or program description (PD) to anchor the proposal to. Unsolicited proposals are possible for some programs; most are now program-targeted.
- A list of senior personnel whose biographical sketches are needed (each goes through SciENcv).
- A draft project description outline that explicitly tags each section as Intellectual Merit and/or Broader Impacts.

## Core workflow

1. **Confirm the PAPPG edition.** The PAPPG is the canonical rulebook. The current edition's effective date, page-limit changes, and format requirements are binding. Do not draft from a 2-year-old template.

2. **Confirm the program announcement.** Identify the program officer, the program description text, and the submission window. If the call has a "Dear Colleague Letter" (DCL), read it; DCLs can override PDs.

3. **Outline the Project Description with both merit reviews visible.** The Project Description must address both Intellectual Merit and Broader Impacts explicitly. Many programs have a separate "Broader Impacts" plan as a sub-section. The two must not be conflated. A common failure mode is a single "impacts" paragraph in the conclusion; the PAPPG expects broader impacts to be designed, evaluated, and resourced.

4. **Draft the Project Description at the page budget defined by the program.** The default Standard Research Proposal Project Description is 15 pages. Some programs reduce it; some allow more. The text budget excludes the Data Management Plan and Postdoc Mentoring Plan, which are separate documents.

5. **Draft the Results from Prior NSF Support** if the PI has NSF support in the last 5 years. This is a required section, even for new PIs, when applicable; it is the second-most-failed requirement (after Broader Impacts).

6. **Draft the Data Management Plan (≤2 pages).** The 2023 PAPPG update standardized the 2-page DMP; describe the data, the metadata, the storage and backup, the preservation plan, the access policy, and the roles. State the standards used. If relevant, state the repository (GenBank, PDB, an NSF-funded data repository, a discipline-specific repository).

7. **Draft the Postdoc Mentoring Plan (1 page) if any postdoc is on the budget.** Describe mentoring activities, professional development, supervision of the postdoc's research, and career development. The plan is not the postdoc's research plan; it is the postdoc's mentoring plan.

8. **Build the budget** on the SF424 (R&R) budget form. NSF allows budget categories that mirror the federal standard. Justify personnel, equipment >$5K, travel, materials, and any subaward / participant support costs.

9. **Build the biographical sketch for each senior person via SciENcv.** The biosketch format is defined by the PAPPG and changes less often than the Project Description. See `ors-research-grants-bio-sketch` for the format and the new contribution-statement fields.

10. **Run a self-review pass against the PAPPG and the program announcement's review criteria.** NSF review criteria are Intellectual Merit and Broader Impacts; both are scored 1–5 (or Excellent–Poor in some programs) and a "very good" project with a weak Broader Impacts plan will not be funded.

## Document patterns

### Project Description skeleton (15 pages default)

```markdown
# Project Description

## Overview (1 page)
- Problem statement and significance.
- Intellectual Merit in 2–3 sentences.
- Broader Impacts in 2–3 sentences.
- The team's prior work that grounds this proposal.

## Background and significance (2–3 pages)
- What is known and unknown.
- Why now.

## Research plan, Aim-by-Aim (8–10 pages)
- Aim 1: question, hypothesis, methods, expected outcomes,
  decision rule, alternative strategies.
- Aim 2: ...
- Aim 3 (if present): ...

## Broader Impacts (1–2 pages)
- Audience and need.
- Activities and their design.
- Assessment and evaluation.
- Personnel and budget allocated.

## Results from Prior NSF Support (variable length, but ≤5 pp total within the
 Project Description)
- For each prior award: title, dates, summary of results,
  publications, products (datasets, software), the next-stage plan.

## References Cited (no page limit; not part of Project Description)
```

### Broader Impacts design (a checklist)

```text
[ ] Specific audience identified (K-12 students, community
    partners, museum visitors, industry, policy makers, etc.)
[ ] Activities designed for that audience (curriculum module,
    workshop, internship, open-source release, public dataset,
    clinical guideline, etc.)
[ ] Personnel responsible and effort allocated
[ ] Partner institution / external collaborator (if any)
[ ] Deliverables and timeline
[ ] Assessment plan (how will you know it worked)
[ ] Sustainability (what survives the grant)
[ ] Budget line items (Broader Impacts are not free; review
    committees look for budgeted effort)
```

### Data Management Plan skeleton (2 pages)

```markdown
# Data Management Plan

## Data types
- [Types, expected volume, format]

## Metadata and standards
- [Domain standards, controlled vocabularies, file naming]

## Storage and backup during the project
- [Institutional storage, backup cadence, access controls]

## Preservation and access
- [Repository name, accession plan, embargoes]

## Roles and responsibilities
- [PI, data steward, students]

## Plans for re-use and downstream impact
```

### Postdoc Mentoring Plan skeleton (1 page)

```markdown
# Postdoctoral Researcher Mentoring Plan

## Mentoring activities (1:1 meetings, journal clubs)
## Professional development (grant writing, mentoring, teaching)
## Research supervision (ownership, attribution)
## Career development plan
## Integration with the lab / project
## Performance evaluation cadence
```

## Common pitfalls

- **Stating Broader Impacts as a single paragraph in the conclusion.** The PAPPG expects a designed, budgeted, evaluated broader-impacts plan. PIs who treat it as a postscript are screened out.
- **Conflating Intellectual Merit and Broader Impacts.** Aims are typically intellectual-merit work; broader-impacts activities are typically separate and may share personnel. Keep them separable in the Project Description.
- **Missing or weak Results from Prior NSF Support.** A prior award with a 3-line "we did the work" summary, no publications, no datasets, and no plan is the canonical screen-out.
- **DMP that says "data will be available upon request."** PAPPG expects a named repository and a preservation plan. "Upon request" is not a DMP.
- **Postdoc on the budget with no Postdoc Mentoring Plan.** The proposal is returned without review.
- **Page-limit over-runs.** The Project Description has a hard limit. Reviewers do not read beyond it; the proposal is administratively returned for over-runs in many programs.
- **Font, margin, and PDF issues.** PAPPG specifies font (often 11 pt or 10 pt for figures), margin (1 inch), and PDF/A or non-PDF issues. Verify the format requirements in the current PAPPG.
- **Single-PI proposal with no collaborator letter or external partner commitment.** A project that requires a sample cohort, a beamline, or a survey platform with no letter of collaboration is a flag.

## Validation

- Project Description is at the program's page limit.
- Both Intellectual Merit and Broader Impacts are explicitly addressed.
- The Broader Impacts plan has a budgeted effort line and an assessment plan.
- The Data Management Plan is ≤2 pages and names a repository.
- The Postdoc Mentoring Plan is present if a postdoc is on the budget.
- The biographical sketches are generated via SciENcv in the current format.
- The submission passes NSF's format validation in Research.gov or FastLane.

## Open alternatives

- **Research.gov vs. FastLane.** Both are NSF submission portals; Research.gov is the newer system. Either is acceptable; the institution's sponsored-research office usually has a preference.
- **SciENcv vs. NSF fillable PDF.** NSF accepts SciENcv-generated biosketches; the fillable PDF is being phased down. Use SciENcv (see `ors-research-grants-bio-sketch`).
- **Open repositories vs. proprietary.** Most DMPs should default to discipline-specific, open repositories (GenBank, PDB, OpenNeuro, ProteinDB, etc.). For long-tail data types, NSF-funded data infrastructure such as [DataONE](https://www.dataone.org/) is the canonical general-purpose option.

## References

- NSF: [Proposal & Award Policies & Procedures Guide (PAPPG)](https://www.nsf.gov/bfa/dias/policy/pappg) — current edition.
- NSF: [Proposal Preparation Instructions](https://www.nsf.gov/bfa/dias/policy/pappg) — the PAPPG Chapter II.A is the proposal-prep section.
- NSF: [Biographical Sketch and Current and Pending Support](https://www.nsf.gov/bfa/dias/policy/pappg) — see current PAPPG Chapter II.D.2.h.
- NSF: [Data Management Plan policy](https://www.nsf.gov/bfa/dias/policy/pappg) — see current PAPPG Chapter II.D.4.
- NSF: [Postdoctoral Researcher Mentoring Plan](https://www.nsf.gov/bfa/dias/policy/pappg) — see current PAPPG Chapter II.D.5.
- NSF: [SciENcv guidance for NSF](https://www.ncbi.nlm.nih.gov/sciencv/) — NCBI SciENcv NSF format.
- NSF: [Program Solicitations](https://www.nsf.gov/funding/programs.jsp) — program index.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram.