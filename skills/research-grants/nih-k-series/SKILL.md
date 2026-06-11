---

name: nih-k-series
description: "Use when planning or drafting an NIH mentored career-development award (K01, K08, K23, K99/R00, K25, K22, K07): Candidate Section, Mentorship Plan, Training Plan, Sponsor/Co-Sponsor statements, and the K99-to-R00 transition logic. Anchored to the K Kiosk on the NIH website and current Forms-H/I."
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

# NIH K-Series Mentored Career Awards

> A working framework for planning, drafting, and self-reviewing a mentored career-development award (K-series). The K-series is a contract between a candidate, a primary mentor, a sponsoring institution, and a funding IC about how three to five years of protected time will convert a trainee into an independent investigator.

## When to use

- Choosing among the K mechanisms (K01, K08, K23, K99/R00, K25, K22) and matching the mechanism to the candidate's background.
- Drafting the Candidate Section (background, career goals, training plan, rationale for the K mechanism).
- Building a Mentorship Team (primary sponsor, co-sponsor, advisory committee) and writing the Sponsor/Co-Sponsor statements.
- Constructing the Training Plan (courses, workshops, technical visits, "didactic" vs. "hands-on" split).
- Writing the Research Plan that lives *under* the Training Plan — the K research plan is a smaller, more focused version of an R01 Research Strategy.
- Managing the K99-to-R00 transition: the R00 phase is not funded by the K99 award; it requires an R00 application via the awarding IC.

## When NOT to use

- This is not the F-series (pre-doctoral or post-doctoral fellowship). F awards are trainee-initiated and use the F-specific application package; K awards are mentored, with a sponsor and a more structured training plan.
- This is not the R-series. The K Research Plan is shorter and more didactic; the K's central value is the candidate section and the mentorship plan.
- This is not a Cover-letter/Letter-of-Support skill — see the institution's sponsored-research office for the institutional commitment letter templates.

## Prerequisites

- A primary sponsor with funded R01-equivalent research and a track record of prior mentees who transitioned to independence.
- A candidate whose terminal degree and career stage match the K mechanism's eligibility window — verify against the K Kiosk eligibility block for the specific K-code, not generic K-award language.
- A clear institutional commitment letter from the department chair or dean that documents protected time (typically 75% effort, or 50% for certain surgical specialties), lab space, and start-up.
- A draft Specific Aims page for the Research Plan (see `ors-research-grants-specific-aims`).

## Core workflow

1. **Pick the K mechanism from the K Kiosk.** The choice is driven by candidate background, not by topic. Common axes:
   - K01 — general mentored research scientist development; no degree requirement; some ICs restrict to specific topics.
   - K08 — mentored clinical scientist research career development; the candidate's Research Plan must be in a basic or translational area.
   - K23 — mentored patient-oriented research career development; the Research Plan must involve human subjects.
   - K99/R00 — pathway to independence: up to 2 years mentored (K99) followed by up to 3 years independent (R00) at a different or same institution. The candidate must be ≤ a stated number of years from the terminal degree or postdoc start (verify current window on the K Kiosk).
   - K25 — mentored quantitative research development; the candidate's prior field is quantitative/engineering.
   - K22 — transition award; candidate must already be in a position that doesn't yet have R01-eligible support.

2. **Verify the K99/R00 window** before drafting. The NIH updates the postdoc-years window periodically. Do not rely on a window from a prior cycle.

3. **Build the mentorship team before drafting the plan.** Primary sponsor (funded, prior mentees), co-sponsor (often a methods expert complementary to the sponsor), and 2–4 person advisory committee (often including a biostatistician and an industry / clinical translation contact, depending on the Research Plan). Confirm each named mentor's role and effort.

4. **Draft the Candidate Section first.** This is the single most important attachment. The reviewer is buying the candidate, not the science. Include: short bio, prior training, gap analysis (what skills the candidate has vs. what the Research Plan requires), career goals (3–5 yr and 5–10 yr), and how the K will close the gap.

5. **Draft the Training Plan in parallel.** A Training Plan without a Candidate Section is unfocused; a Candidate Section without a Training Plan is a wish. Match each training activity to a specific gap. Common components: formal coursework (degree program, certificate, biostatistics or bioinformatics); workshops; structured mentor meetings; technical rotations or visits; shadowing; teaching if relevant to the candidate's career path.

6. **Draft the Sponsor/Co-Sponsor statements.** Sponsors describe their mentorship philosophy, prior mentees' outcomes, the specific mentoring activities they will perform, and the candidate's preparation. Co-sponsors describe their role in complementing the sponsor (a method, a model, a population access).

7. **Draft the Research Plan (Specific Aims + Approach) under the Training Plan's logic.** The Research Plan is shorter than an R01; typical page budgets are 6–12 pages for the Research Plan, varying by mechanism and FOA. Verify the FOA. The Plan must be tractable for a partially-trained candidate, with each Aim tied to a learning objective.

8. **Build the Budget.** K awards are typically modular and the budget is restricted; salary is capped, fringe benefits apply, and research costs are usually modest. Verify the current cap and any FOA-specific deviations.

9. **Assemble the Letters of Support.** Sponsor, Co-Sponsor, Advisory Committee members, and the institutional commitment letter. The institutional letter must be specific (protected effort %, space, dollars), not generic.

10. **Plan the K99-to-R00 transition (if applicable) from day one.** The R00 phase requires a separate application from the R00 institution to the awarding IC, and the R00 must start within the K99 end date + transition window. Many K99 awards are never converted to R00 because the candidate's start-up package, position, or R00 application is not ready by the time the K99 ends. Plan the R00 logistics before the K99 is funded.

## Document patterns

### Candidate Section skeleton

```markdown
# Candidate Information

## Background
- Terminal degree(s), year, institution.
- Postdoc(s), year, mentor, project.
- Prior funding (F31, F32, R36; private fellowships).
- 3–5 representative first-author publications with a sentence
  on the candidate's contribution.

## Career Goals and Objectives
- Short-term (3–5 years): [the K period].
- Long-term (5–10 years): [the independent research program].

## Training During the K Period
- Skills to acquire, mapped to gaps.
- Didactic plan.
- Mentorship team and roles.

## Rationale for the K Mechanism
- Why this K (not F, not R, not K99 if the candidate is
  already R-eligible).
- Why the K-resourced protected time is needed.
```

### Training Plan table (a common reviewer-friendly format)

| Gap | Activity | Mentor responsible | Timing (months) | Evaluation |
|-----|----------|--------------------|-----------------|------------|
| Single-cell RNA-seq | Hands-on rotation, bioinformatics course | Co-Sponsor X | 1–6 | QC report on benchmark dataset |
| Survival analysis | Course, weekly clinicostatistics meetings | Sponsor Y | 3–12 | Capstone project |
| Clinical trial design | CTSA course, observer on DSMB | Mentor Z | 6–18 | Mock DSMB review |

### Sponsor statement skeleton

```markdown
# Sponsor Statement

## Mentor qualifications
- Funding history (current R01 or equivalent; prior mentees).

## Mentorship plan
- Meeting cadence (weekly 1:1; lab meeting attendance).
- Authorship convention.
- Career-development activities for the candidate.

## Candidate preparation
- Strengths and gaps (sponsor's view).

## Research Plan fit
- The candidate's role on each Aim.

## Mentee outcomes
- Prior mentees: name, years, current position, first-author papers.
```

### K99-to-R00 transition checklist (internal use)

```text
[ ] K99 start date: ___
[ ] K99 end date: ___
[ ] R00 institution identified: ___
[ ] R00 start-up negotiated: ___
[ ] R00 position title (PI-eligible at R00 institution): ___
[ ] R00 research plan: continuity from K99, with at least one new Aim
[ ] R00 application materials prepared (typically the same as a
    small R01 with a transition narrative)
[ ] R00 submitted to the awarding IC before the K99 end date
[ ] Just-in-time and human-subjects materials at the R00 institution
```

## Common pitfalls

- **Choosing the wrong K mechanism.** A K23 (patient-oriented) Research Plan that doesn't involve human subjects will be returned without review. A K08 (basic/translational) with a clinical-trial-heavy plan will be flagged.
- **Candidate Section that lists publications but not gaps.** Reviewers want the gap-to-training map. A long CV with no "this is what I don't yet know" is a rejected K.
- **Sponsor statement that is a CV dump.** Reviewers want the mentorship philosophy, the candidate's role, and prior mentee outcomes.
- **Training Plan that is a course catalogue, not a gap map.** Tie each activity to a specific skill gap in the Candidate Section.
- **Institutional commitment letter that does not commit.** "The institution supports Dr. X" without protected time, space, or dollars is a flag. The letter must state the protected time as a percentage and the salary support mechanism.
- **K99 research plan that cannot survive the move.** A K99 that depends on a single collaborator's cohort or a single piece of equipment at the K99 institution will not transition cleanly. Build at least one Aim that travels.
- **Missed the R00 application window.** Plan the R00 6–9 months before the K99 end date. The R00 application is the moment of conversion; do not treat the K99 award letter as the R00 guarantee.
- **No advisory committee.** A single-sponsor K is fragile. Reviewers want 2–4 additional named advisors with specific roles.

## Validation

- The K mechanism matches the candidate's degree, postdoc history, and Research Plan topic.
- The Candidate Section articulates gaps, the Training Plan closes them, and the Sponsor statement confirms the closure plan.
- The Research Plan is shorter and more didactic than an R01; it is feasible for a candidate with the planned training, not for the sponsor.
- The institutional letter commits to a specific protected time, specific space, and (where relevant) specific dollars.
- K99 candidates: the R00 transition is on a calendar; the R00 institution, position, and start-up package are identifiable.

## Open alternatives

- **K Kiosk vs. IC-specific announcements.** The K Kiosk is the canonical entry point, but each IC (NCI, NIAID, NHLBI, NINDS, etc.) publishes its own FOA or participates in a parent announcement with institute-specific clauses. Always read the IC's FOA before drafting.
- **K99/R00 vs. K22.** K22 is a transition mechanism that some ICs use in place of (or in addition to) K99. Differences are IC-specific.
- **ORCID vs. SciENcv biosketch.** SciENcv generates the K biosketch format; ORCID is the persistent identifier. Use both.

## References

- NIH: [K Kiosk — Career Development Awards](https://grants.nih.gov/training/career-development-awards.htm) — mechanism descriptions, eligibility, and program announcements.
- NIH: [SF424 Application Guide — Career Development Award instructions](https://grants.nih.gov/grants/how-to-apply-application-guide.html).
- NIH: [Forms-H/I application package](https://grants.nih.gov/grants/forms.htm).
- NIH: [Early Stage Investigator (ESI) policy](https://grants.nih.gov/policy/early-stage/policy.htm) — relevant to K99/R00 and to R01 timing.
- NIH: [K99/R00 frequently asked questions](https://researchtraining.nih.gov/) — current program page on the NIH research training website.
- NIH: [eRA Commons](https://era.nih.gov/).

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram.