---
name: ors-research-grants-darpa-baa
display_name: "DARPA Broad Agency Announcement (BAA)"
description: "Use when responding to a DARPA Broad Agency Announcement: white paper vs full proposal, Heilmeier Catechism framing, program manager engagement, BAA-specific formatting, cost volume construction."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: research-grants
tags: [darpa, baa, baa-procurement, heilmeier, program-manager, white-paper, cost-volume]
difficulty: advanced
prerequisites:
  - tools: [DARPA BAA submission portal (often DSIP, SAM.gov), eRA Commons, SciENcv]
  - skills: [ors-research-grants-specific-aims, ors-research-grants-bio-sketch]
sources_consulted:
  - "DARPA: Broad Agency Announcements (BAAs) at darpa.mil/work-with-us/baa"
  - "DARPA: Heilmeier Catechism (origin: George H. Heilmeier, DARPA Director 1975-1977)"
  - "DARPA: Cost proposal guidance and SF424 R&R budget guidance"
  - "DARPA: DSIP submission portal (Defense SBIR/STTR Innovation Portal)"
  - "Improvisions: White paper vs full proposal gate decision, Heilmeier-question-by-question mapping"
last_updated: 2026-06-10
tool_type: writing
primary_tool: human
---

# DARPA Broad Agency Announcement (BAA)

> A working framework for responding to a DARPA Broad Agency Announcement. DARPA BAAs are different from NIH/NSF announcements: they are open-ended (most BAA topics stay open for years), they are reviewed by a small set of program managers, and the standard workflow is white paper → invitation to a full proposal → cost volume → negotiation → award. A BAA proposal is a procurement, not a grant in the NIH sense.

## When to use

- Identifying and reading the right BAA (DARPA offices: BTO, DSO, I2O, MTO, STO, etc.).
- Drafting a 3–5 page white paper that survives the BAA white-paper gate.
- Engaging the BAA's program manager before submission (DARPA BAA practice allows pre-white-paper outreach).
- Drafting a full proposal once invited, with Technical and Management Volumes.
- Building a Cost Volume (SF424 R&R + sub-budget detail) once invited.
- Using the Heilmeier Catechism to stress-test the proposal.
- Working with a prime contractor on a DARPA BAA team (BAAs are often responded to as teams, not as solo applicants).

## When NOT to use

- This is not a DARPA SBIR/STTR proposal. SBIR/STTR goes through the DoD SBIR portal and has its own phase structure (Phase I, Phase II, Direct-to-Phase-II). This skill covers the BAA track, not the SBIR/STTR track.
- This is not a DOD CDMRP (Congressionally Directed Medical Research Programs) proposal. CDMRP is NIH-style review with cancer and military-health funding; it is not a DARPA BAA.
- This is not a service-branch announcement (ONR, AFOSR, ARO, ACC). Service-branch basic-research announcements are similar in structure but use different BAA portals and award mechanisms.
- This is not a contract mechanism (OTA, CRADA). DARPA BAA proposals are procurement contracts, not research grants.

## Prerequisites

- A BAA that is currently open for the candidate's topic. Check the [DARPA BAA index](https://www.darpa.mil/work-with-us/baa) and the relevant office's BAA page.
- A program manager (PM) who is the right person for the topic. Read the BAA's technical POC; the PM is named in the BAA.
- A 1–2 paragraph outreach email to the PM, signed by a senior PI. PMs are not obligated to respond, but most do.
- A draft white paper that follows the BAA's structural requirements and the Heilmeier Catechism.
- A cost-volume assembly pathway: subcontracts, fringe, F&A, and any required cost-sharing or matching.

## Core workflow

1. **Read the BAA carefully.** A DARPA BAA includes the technical topic, the award instrument, the cost-volume requirements, the white-paper page limit, the full-proposal page limit, the security classification (e.g., UNCLASSIFIED, NOFORN), and the submission portal. The BAA is the rulebook for the proposal; deviations are a return without review.

2. **Identify the technical POC (the program manager) and the contracting POC.** These are listed in the BAA. The technical POC is the PM; the contracting POC handles the cost volume and the award instrument.

3. **Email the PM with a 1-paragraph project description** before white paper submission. The email is not a substitute for the white paper; it is a "does this fit your BAA?" check. Most BAA white papers that come in cold without PM awareness are screened out.

4. **Draft the white paper against the BAA's structure.** A typical DARPA white paper is 3–5 pages and contains:
   - A problem statement.
   - The proposed solution, including the technical innovation.
   - A brief work plan.
   - A budget envelope (often a single number; no detailed budget).
   - The team's relevant experience.

5. **Apply the Heilmeier Catechism to the white paper.** The Heilmeier Catechism is the canonical DARPA "what are you proposing" check. See the document patterns below.

6. **Submit the white paper and wait for the gate decision.** The white-paper gate is the highest-leverage filter. A small fraction of white papers are invited to a full proposal.

7. **Once invited, draft the Technical and Management Volumes** of the full proposal. The Technical Volume is the substantive document (often 15–25 pages, but verify). The Management Volume is a work plan with milestones, Gantt, team, and risk register.

8. **Build the Cost Volume.** The Cost Volume is the SF424 R&R with sub-budgets, plus a budget narrative, plus the contractor's certification if the proposal is led by a prime.

9. **Submit before the BAA's full-proposal due date** via the portal named in the BAA (DSIP, BAA Box, or the office's submission system).

10. **Plan for negotiation.** DARPA awards are typically negotiated before award; the negotiation can change scope, cost, and milestones. The PI should not assume the technical volume is final until the award is signed.

## Document patterns

### The Heilmeier Catechism (origin: George H. Heilmeier, DARPA Director 1975–1977)

The eight questions that, in DARPA's tradition, every BAA proposal should be able to answer. The questions are sometimes paraphrased; the substance is the same:

```markdown
1. What are you trying to do? Articulate your objectives using
   absolutely no jargon.

2. How is it done today, and what are the limits of current practice?

3. What is new in your approach and why do you think it will be
   successful?

4. If you are successful, what difference will it make? (What are
   the benefits? To whom? In what timeframe?)

5. What are the risks and the payoffs? (Risk-reward trade-off.)

6. How much will it cost? How long will it take?

7. What are the mid-term and final "exams" to check for success?

8. To ensure success, what intermediate steps would you try, and
   what are the decision points?
```

### White paper skeleton (3–5 pages)

```markdown
# Title

## Problem (0.5 page)
- The problem in DARPA-relevant framing.
- Current state of practice and its limits.
- Why DARPA should care (mission fit).

## Proposed solution (1.5–2 pages)
- The technical innovation.
- The proposed methodology.
- A reference to the Heilmeier answers (what is new, what is
  the risk, what is the payoff).

## Work plan and timeline (0.5 page)
- Phases, milestones, duration.
- Mid-term and final demonstrations.

## Team (0.25 page)
- PI, Co-PI, subcontractors, and the relevant prior work.

## Budget envelope (0.1 page)
- Total $ and the 1–2 largest categories.
- Note: do not include a detailed cost volume at the white-paper
  stage.
```

### Full proposal Technical Volume skeleton (15–25 pages, BAA-specific)

```markdown
# Title

## Problem and motivation (2 pages)
- Heilmeier answers 1, 2.

## Technical approach (8–12 pages)
- Heilmeier answer 3.
- Per task: hypothesis, method, expected outcome, alternative
  strategies.

## Impact (1 page)
- Heilmeier answer 4.
- Specific deliverable and the transition partner.

## Risk register (1 page)
- Heilmeier answer 5.
- Per-task risks, mitigations.

## Mid-term and final exams (1 page)
- Heilmeier answer 7.
- Milestones tied to go / no-go decision points.

## Team and prior work (2 pages)
- Biosketches, key papers, prior DARPA / DoD awards.

## References cited
```

### Management Volume skeleton

```markdown
# Management Plan

## Work Breakdown Structure (WBS) and milestones
## Schedule (Gantt)
## Team and roles (PI, Co-PI, subcontractors)
## Facilities and infrastructure
## Subcontractor / consultant commitments
## Risk register
## Cost-share commitments (if any)
```

### Cost Volume skeleton (SF424 R&R)

```text
Section A: Senior / Key Personnel
Section B: Other Personnel
Section C: Equipment
Section D: Travel
Section E: Participant Support Costs (if any)
Section F: Other Direct Costs
Section G: Total Direct Costs
Section H: Indirect Costs (F&A rate and base)
Section I: Total Direct + Indirect
Section J: Fee / Profit (per BAA)
Section K: Total Amount of Funding Requested
Section L: Cost-share (if any, with letter of commitment)
```

### PM outreach email (≤1 page)

```text
Subject: [BAA topic code] — short project description and question

Dr. [PM Name],

I am a [title] at [institution] working on [topic]. I am
considering submitting a white paper to the [BAA title] and
would appreciate your guidance on whether the topic is a fit.

In 2–3 sentences: [project description, the technical innovation,
the transition partner].

I can follow up with a 2-page white paper if helpful.

Thank you,
[PI]
```

## Common pitfalls

- **PM engagement skipped.** White papers submitted without a PM touch are screened out at a higher rate. The PM outreach email is the highest-leverage 30 minutes in the workflow.
- **Heilmeier answers full of jargon.** "Novel AI-driven cyber-physical platform..." is the screen-out. The Catechism is about plain language.
- **No transition partner named.** DARPA funds prototype development. A proposal without a "who will field this" answer fails the Impact question.
- **Cost Volume submitted with the white paper.** BAA white papers do not include a detailed cost volume. Including one in the white paper is a flag.
- **No mid-term / final exams.** The Heilmeier question 7 is the gate. A proposal that has milestones but no decision points (i.e., "go" is the only option) is a screen-out.
- **No risk register.** Every DARPA proposal must have a risk register per task. A single "Risks" paragraph is a flag.
- **Prime / sub relationship is unclear.** If the proposal is led by a prime with subs, the prime's cost volume must include sub-budgets. Misalignment between the prime's and sub's cost volumes is a return.
- **Submitting to the wrong BAA.** DARPA offices (BTO, DSO, I2O, MTO, STO) have distinct portfolios. A BTO-aligned topic submitted to DSO is a screen-out.
- **Classified material in an UNCLASSIFIED BAA.** Verify the BAA's classification. Submitting classified material outside the classification is a return.

## Validation

- The white paper is within the BAA's page limit and follows the BAA's structure.
- The Heilmeier Catechism is answered in plain language, with a specific transition partner named.
- The full proposal is within the BAA's Technical Volume page limit.
- The Cost Volume is internally consistent (prime + subs = total) and the F&A rate is correct.
- The submission passes the portal's format check.
- The PI and the PM have had at least one email exchange before the white paper was submitted.

## Open alternatives

- **DARPA BAA vs. ARPA-E FOA.** ARPA-E (DOE) is a sibling agency with a similar BAA-style mechanism and a similar program-manager-driven culture. The Heilmeier Catechism applies.
- **DARPA BAA vs. service-branch BAAs (ONR, AFOSR, ARO).** These are similar in spirit (BAA-style, program-manager-driven) but use different offices. ONR and AFOSR fund basic research; ARPA-funded work is higher-TRL.
- **DARPA BAA vs. SBIR/STTR.** SBIR/STTR is for small businesses; BAA is for any performer (large or small). The two have different topic cadences and different review processes.
- **Open-source submission infrastructure.** DARPA BAA submissions are portal-specific. There is no "open" alternative to the portal; the cost-volume templates are based on SF424 R&R, which is federal-standard.

## References

- DARPA: [Broad Agency Announcements (BAAs)](https://www.darpa.mil/work-with-us/baa) — BAA index, instructions, and submission portals.
- DARPA: [Heilmeier Catechism](https://www.darpa.mil/work-with-us/heilmeier-catechism) — origin, formal phrasing, and history.
- DARPA: [Defense SBIR/STTR Innovation Portal (DSIP)](https://www.darpa.mil/work-with-us/sbir-sttr-program) — SBIR/STTR (separate from BAA).
- DARPA: [Cost proposal guidance](https://www.darpa.mil/work-with-us/baa) — see the Cost Volume section of the BAA.
- U.S. Government: [SAM.gov](https://sam.gov/) — federal contracts and opportunities registry; BAAs are posted here.
- DARPA: [Offices](https://www.darpa.mil/about/offices) — BTO, DSO, I2O, MTO, STO, and others, each with their own BAA.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram.