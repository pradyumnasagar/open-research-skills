---
name: ors-research-grants-foundation-grants
display_name: "Private Foundation Grants (Templeton, HHMI, Damon Runyon, Searle, Pew, Keck, McKnight, Packard)"
description: "Use when applying for private foundation grants: Templeton, HHMI (Investigator, Freeman Hrabowski, Hanna Gray), Damon Runyon, Searle, Pew Scholars, McKnight, Packard, Keck. Narrative-driven, no-overhead-allowed, collaboration-letter heavy."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: research-grants
tags: [foundation-grants, hhmi, templeton, damon-runyon, searle, pew, mcknight, packard, keck, narrative]
difficulty: advanced
prerequisites:
  - tools: [Foundation submission portals, eRA Commons (if co-submitted), SciENcv (for some)]
  - skills: [ors-research-grants-specific-aims, ors-research-grants-bio-sketch]
sources_consulted:
  - "HHMI: Investigator competition and Freeman Hrabowski Program (hhmi.org)"
  - "Damon Runyon Cancer Research Foundation: Scholar and related programs"
  - "Searle Scholars Program: program description and rubric"
  - "Pew Scholars Program: program description and rubric"
  - "John Templeton Foundation: program description, narrative structure, and no-overhead policy"
  - "W. M. Keck Foundation: research program description and concepts"
  - "McKnight Endowment Fund for Neuroscience: Memory and Cognitive Disorders Award"
  - "David and Lucile Packard Foundation: Packard Fellowships for Science and Engineering"
  - "Improvisions: Cross-foundation comparison table, narrative vs structural differences"
last_updated: 2026-06-10
tool_type: writing
primary_tool: human
---

# Private Foundation Grants

> A working framework for drafting or self-reviewing applications to private research foundations. The defining features of foundation grants are: (1) narrative-driven — the proposal reads more like a story than an NIH/NSF structure, (2) no-overhead or capped-overhead policies are common, and (3) collaboration letters and host-institution commitment letters are weighted heavily because the foundation relies on the candidate's own network of supporters.

## When to use

- Drafting a Templeton Foundation grant application (Templeton's narrative structure, three-stage review).
- Preparing an HHMI Investigator application (PIs only, by invitation in some cycles; the HHMI Hanna Gray and Freeman Hrabowski programs are early-career equivalents).
- Preparing a Damon Runyon Cancer Research Foundation application (Damon Runyon Scholar; specific career-stage windows).
- Preparing a Searle Scholars Program application (early-career; chemistry, biological sciences, biomedical engineering).
- Preparing a Pew Scholars application (early-career; specific research focus; Pew-Stewart Scholars for cancer research is a separate sub-program).
- Preparing a Keck Foundation research grant (usually institutional, large budget, requires concepts and ideas letters).
- Preparing a McKnight Endowment Fund for Neuroscience application (memory and cognitive disorders; scholar award).
- Preparing a Packard Fellowship application (early-career; science and engineering).
- Writing a strong Letter of Collaboration (vs. Letter of Support) — a foundation-grant specific genre.

## When NOT to use

- This is not a federal-grant skill. Foundation grants do not have the page limits or Forms-H/I structure of NIH. The narrative is more open.
- This is not a small-donor / crowd-funding / Kickstarter skill.
- This is not a corporate / industry-sponsored-research contract.
- This is not the right skill for foundation grants for trainees (those are fellowship-style; see `ors-research-grants-fellowships`).

## Prerequisites

- A narrative research plan: foundation grants prize a story, not a list of aims.
- A specific no-overhead or capped-overhead policy is expected — most of these foundations restrict or forbid indirect costs. Verify the policy before budgeting.
- Letters of collaboration from named partners, each with a specific role and commitment.
- A host institution (or institution-affiliated foundation) that will receive the grant and provide accounting. Most of these foundations do not fund individuals directly.

## Core workflow

1. **Inventory the foundation landscape.** A foundation portfolio is built around the candidate's career stage and research area:
   - **Early career (postdoc, assistant professor):** Searle, Pew, Packard, Damon Runyon (for cancer), HHMI Hanna Gray / Freeman Hrabowski.
   - **Established investigator (associate / full professor):** HHMI Investigator, Keck, McKnight, Templeton.
   - **Specific fields:** Damon Runyon (cancer), McKnight (neuroscience), Pew-Stewart (cancer), Keck (high-risk, high-impact), Templeton (foundational questions at the boundary of science and religion / philosophy / human progress).

2. **Verify eligibility and the current call.** Each foundation's program description, eligibility, and submission window change annually. Many of these foundations have an internal nomination or letter of intent step before the full proposal is invited.

3. **Read the foundation's rubric for "what they fund."** Each foundation has a distinct thesis. Pew Scholars emphasizes "outstanding investigators in health and biomedical sciences." Damon Runyon emphasizes "young scientists conducting basic and translational research that has the potential to impact cancer." Templeton emphasizes "Big Questions." Keck emphasizes "high-risk, potentially transformative research." The narrative must be tailored.

4. **Draft the narrative first, then the budget.** Foundation grants reward a coherent research story more than a granular budget. The budget is constrained by the no-overhead / capped-overhead policy and is built after the narrative is solid.

5. **Coordinate Letters of Collaboration.** Each collaborator writes a Letter of Collaboration (LoC), not a Letter of Support. The LoC names the collaboration, the role, the time commitment, the materials, and the in-kind or cash support. LoCs are short (≤1 page). Letters of Support from non-collaborators are also common (e.g., department chair, mentor).

6. **Build the host-institution commitment.** Most foundations require the host institution to sign a commitment letter that documents the institution's acceptance of the no-overhead policy, the candidate's appointment, and the lab space.

7. **Submit per the foundation's portal.** Foundations vary in their submission infrastructure; some use InfoReady, some use Foundation Portal, some use a custom system. Verify the current portal at the time of submission.

8. **Plan resubmission.** Most of these foundations have an annual cycle. A rejected application can be revised and resubmitted in the next cycle, often with new preliminary data.

## Document patterns

### Foundation research narrative (generic; adaptable)

```markdown
# Title

## Opening hook (0.5 page)
- The question that drives the work. Why this question
  is the right question to ask now.

## Background and significance (1–2 pages)
- What is known. What is unknown. Why the unknown is a
  barrier to progress.

## Aims / Approach (2–4 pages)
- The work plan. Use narrative, not bullet lists, where possible.
- Specific methods. Expected outcomes. Decision rules.

## Preliminary data (1–2 pages)
- The candidate's own preliminary work that grounds the proposal.
- For early-career: include the postdoc's first-author work.

## Why this is the right group / candidate (0.5 page)
- Track record, expertise, collaborators.

## Timeline (0.5 page)
- Multi-year plan.

## Budget narrative (1 page)
- Cash and in-kind.
- Justification for major categories.
```

### Templeton-specific "Big Questions" framing

```markdown
# The Big Question

## The question (1 paragraph)
- The question that, if answered, would re-shape the way
  we think about [X]. Templeton funds foundational questions,
  not just important ones.

## Why this is a foundational question (1 paragraph)
- The implications across multiple domains
  (science, philosophy, theology, human progress).

## The candidate's plan to address it (1–2 pages)
- The specific experiments, surveys, or conceptual work.

## Expected outcomes and impact (0.5 page)
- What the world will have if the work is funded.
```

### Letter of Collaboration (generic template, ≤1 page)

```text
[Letterhead of the collaborator's institution]

To: [Foundation] Review Committee

I am writing to confirm my collaboration on [PI name]'s proposal
"[proposal title]" submitted to [Foundation].

My role in this project is to:
- [Specific role, e.g., provide the cohort / reagent / analysis /
  training / infrastructure access]
- [Specific deliverable, e.g., n=200 participants enrolled, with
  consent]

My commitment includes:
- [X]% effort
- Access to [resource, dataset, equipment]
- [In-kind or cash support, if any]

I confirm that this collaboration is appropriate to my
institution's policies and that I have the resources to
support this commitment.

Sincerely,
[Name, title, institution]
```

### Foundation portfolio comparison (sample table)

| Foundation | Career stage | Field | Indirect cost | Annual $ | Duration | Note |
|------------|--------------|-------|---------------|----------|----------|------|
| HHMI Investigator | Established | All | None (paid direct) | Variable | 7 yr | By nomination |
| HHMI Hanna Gray | Asst. Prof. / postdoc | Biomed | None | Up to $1.5M | 8 yr | Career-stage focus |
| HHMI Freeman Hrabowski | Asst. Prof. | All | None | Up to $1.5M | 10 yr | Universities inclusive |
| Damon Runyon | Postdoc / early faculty | Cancer | None | Variable | 5 yr | No concurrent NIH/NSF |
| Searle | Asst. Prof. | Chem, bio, BME | Capped | $300K | 3 yr | US-based |
| Pew Scholars | Asst. Prof. | Health, biomed | Capped | $300K | 4 yr | Pew-Stewart = cancer |
| Packard | Asst. Prof. | Sci, eng | Capped | $875K | 5 yr | 16 winners/yr |
| Keck | Senior PI | All | Capped | Variable | Variable | Invited LOI |
| McKnight Scholar | Asst. Prof. | Neuroscience | Capped | $75K/yr | 3 yr | Memory & cognition |
| Templeton | Asst.–Full | Foundations | None / capped | $50K–$5M | Variable | Narrative-heavy |

## Common pitfalls

- **Generic "we are passionate about..." opening.** Foundation reviewers read hundreds of these. Open with the specific question, not the candidate's autobiography.
- **No-overhead ignored in the budget.** Foundations that disallow overhead must have direct-only budgets; padding indirect to the institutional rate is a screen-out.
- **Letter of Support that is a Letter of Reference.** A Letter of Support from a non-collaborator is different from a Letter of Collaboration. Using the wrong letter genre is a flag.
- **Over-reliance on the candidate's own data without collaborator commitments.** The foundation wants to see the network.
- **No integration with the foundation's mission.** Each foundation has a thesis. A Pew application that does not address Pew's mission, or a Templeton application that does not articulate the Big Question, is a rejection.
- **Letter of collaboration from someone not actually a collaborator.** A signature on a letter that the candidate has never worked with the person is a screen-out for any reviewer who checks.
- **Multi-page CV / biosketch.** Most of these foundations have a CV in a specific format; many limit it to a specific page count. Verify the format.
- **Submitting without a nomination / pre-application step.** Many of these foundations require a Letter of Intent, a nomination, or a department-level pre-screening. Verify the step.

## Validation

- The narrative is research-first, not candidate-autobiography-first.
- The budget is direct-only (or capped-overhead) per the foundation's policy.
- Each Letter of Collaboration names a specific role, deliverable, and time commitment.
- The host-institution commitment letter documents acceptance of the no-overhead policy.
- The submission passes the foundation's portal format check.

## Open alternatives

- **Foundation grants vs. federal grants.** Foundation grants are typically smaller, more narrative, and more flexible than federal grants. Federal grants are the source of mass-scale research funding; foundations are the source of high-risk / high-impact / high-narrative research. The candidate usually pursues both.
- **HHMI Investigator vs. R01.** HHMI Investigators are PI-equivalent and have HHMI-funded salaries and research; this is a different model than R01. HHMI Investigators are not eligible for some federal mechanisms in the same way.
- **Open vs. restricted foundations.** Most major research foundations in this skill are private / restricted. The closest open alternatives are federal mechanisms (NIH R01, NSF Standard Research Proposal, ERC) that fund similar work. There is no "open" alternative to a Damon Runyon Scholar or Packard Fellowship specifically.

## References

- HHMI: [HHMI Investigator Program](https://www.hhmi.org/programs/investigator-program) and [Hanna Gray Fellows Program](https://www.hhmi.org/programs/hanna-h-gray-fellows-program).
- Damon Runyon Cancer Research Foundation: [Scholar Award and others](https://www.damonrunyon.org/for-researchers).
- Searle Scholars Program: [Program description](https://searlescholars.org/).
- Pew Scholars: [Pew Scholars Program in the Biomedical Sciences](https://www.pewtrusts.org/en/projects/pew-scholars-program-in-the-biomedical-sciences).
- David and Lucile Packard Foundation: [Packard Fellowships for Science and Engineering](https://www.packard.org/grant-fellowship-for-science-and-engineering/).
- W. M. Keck Foundation: [Research Program](https://www.wmkeck.org/grant-programs/research).
- McKnight Endowment Fund for Neuroscience: [Scholar Award](https://www.mcknight.org/our-work/our-awards/).
- John Templeton Foundation: [Grant programs](https://www.templeton.org/grants).
- Doris Duke Charitable Foundation: [Fund to Retain Clinical Scientists and others](https://www.dorisduke.org/).

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram.