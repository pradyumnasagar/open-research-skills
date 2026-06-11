---
name: irb-protocol
description: "Use when writing, reviewing, or revising an Institutional Review Board"
license: MIT
---



<!-- metadata:
category: ethics-compliance
version: 1.0.0
author: Pradyumna Jayaram
tags:
- irb
- common-rule
- belmont
- informed-consent
- human-subjects
- vulnerable-populations
difficulty: advanced
prerequisites:
  tools: []
  skills: []
sources: 'Original: 45 CFR 46 (Common Rule, revised eff. 2019-01-21); Adapted: synthesized
  into protocol-writing workflow; Original: The Belmont Report (1979, OHRP); Adapted:
  principles translated into protocol sections; Original: OHRP Guidance on Reviewing
  and Reporting Unanticipated Problems; Adapted: reportable-events checklist; Improvisions:
  reviewer-psychology section, decision-matrix for review level, modern electronic-IRB
  notes (IRBNet, Cayuse, Huron)'
-->

# IRB Protocol Writing
"
> An IRB protocol is the formal document that tells an Institutional Review Board (IRB) exactly what you intend to do with human participants, why the benefits justify the risks, and how you will protect the people who agree to take part. A good protocol reads as a risk-managed research plan: every claim about risk has a mitigation beside it, every claim about consent has a procedure behind it, and every claim about vulnerable participants has a subpart reference. This skill encodes the Common Rule's required elements, the Belmont Report's three principles, the subparts for vulnerable populations, the three review levels (exempt, expedited, convened board), and the psychological patterns that distinguish a protocol an IRB will approve in one round from one that gets bounced for "deferred" or "stipulations."

## When to use

- Drafting a new IRB protocol for a study that recruits human participants, accesses identifiable data, or analyzes biospecimens.
- Responding to IRB stipulations (a "stip" letter) and turning a "deferred" or "tabled" protocol into an approval.
- Preparing a reliance package for a single IRB (sIRB) on a multi-site study.
- Writing the protocol sections that journals and funders ask to see (Methods, Ethics Statement, Trial Registration).
- Training a new lab member or coordinator on what the IRB actually wants in a protocol.

## When NOT to use

- The study is not human-subjects research under 45 CFR 46 (e.g., de-identified secondary data meeting Safe Harbor, or publicly available datasets with no interaction). Use `ors-ethics-compliance-data-privacy` instead.
- You need an IACUC protocol for vertebrate animal work. That is a separate federal regime (USDA Animal Welfare Act, PHS Policy on Humane Care).
- You need a clinical-trial registration on ClinicalTrials.gov. That is a separate workflow from IRB approval; this skill covers the protocol, not the registration.
- The question is whether an activity is "research" or "quality improvement." That is a determination, not a protocol — start with your IRB's "Is it research?" decision tool, then come back.

## Prerequisites

- A research question that is final enough to be described as a specific aim.
- A study design (observational, interventional, secondary data analysis, biospecimen) — you do not need the final sample size, but you need the recruitment strategy.
- Knowledge of your institution's electronic IRB system (IRBNet, Cayuse Huron, Kuali Research, or local equivalent) — final submission is system-specific, this skill is content-agnostic.
- Familiarity with the three Belmont principles (Respect for Persons, Beneficence, Justice) and the current Common Rule (revised 2018, effective 2019-01-21). If you are new to either, read the OHRP Belmont Report and 45 CFR 46 before drafting.

## Core workflow

1. **Confirm human-subjects status.** If the activity is not "research" under 45 CFR 46.102 or does not involve "human subjects" as defined there, you do not need an IRB protocol — you may need a formal non-research determination from your IRB office. If it is research with human subjects, this skill applies.

2. **Decide the review level** (this determines protocol depth). The three review levels in the Common Rule are:
   - **Exempt** (45 CFR 46.104): one or more of eight exempt categories applies. Even exempt studies must be claimed via the IRB, not self-declared.
   - **Expedited** (63 FR 60364, incorporated by reference in 45 CFR 46.110): no more than minimal risk, and the research appears in one or more of seven expedited categories. Reviewed by the IRB chair or a designated reviewer.
   - **Convened (full) board**: greater than minimal risk, or does not fit the exempt/expedited categories. Reviewed by the convened IRB at a scheduled meeting.
   The decision tree is in 45 CFR 46.110. Most academic protocols are either exempt or expedited; only a minority require convened review.

3. **Map your study to the Belmont principles** before writing a single section. For each of the three principles, write one sentence describing how your protocol satisfies it:
   - **Respect for Persons**: voluntary, informed consent (or appropriate waiver).
   - **Beneficence**: do no harm, maximize benefits over risks.
   - **Justice**: fair distribution of the burdens and benefits of research.
   A protocol that does not satisfy all three at the sentence level will not satisfy them at the page level.

4. **Draft the protocol using the IRB's required elements** (45 CFR 46.108(a) for IRB authority, 45 CFR 46.116 for consent). The sections below are the working order; reorder to match your IRB's electronic-system template (most templates rearrange them, but the elements are constant).

5. **Write the consent document in parallel.** A complete protocol without a draft consent form invites an IRB "defer" or stipulations. The consent must contain the eight required elements at 45 CFR 46.116(a) and the six additional elements at 45 CFR 46.116(b) if applicable, plus a "key information" section at 45 CFR 46.116(a)(5)(i) at the top.

6. **For vulnerable populations, add the relevant subpart(s):**
   - **Subpart B** (45 CFR 46 Subpart B): pregnant women, fetuses, neonates.
   - **Subpart C** (45 CFR 46 Subpart C): prisoners — note that OHRP must be consulted and the IRB must include a prisoner or prisoner-advocate member for any prisoner research.
   - **Subpart D** (45 CFR 46 Subpart D): children — the four risk/benefit categories (46.404, 46.405, 46.406, 46.407) determine the consent and assent procedures.

7. **Pre-review with a colleague who has served on an IRB.** One non-IRB-member reader is the cheapest improvement you can make. They will catch jargon, missing risk mitigations, and consent forms that do not match the protocol.

8. **Submit and respond to the IRB letter.** The three possible outcomes are: approved, approved with stipulations (minor edits, no re-review), or deferred (substantive concerns, full-board re-review). Treat the letter as a checklist, not a debate.

9. **For multi-site studies, prepare a sIRB reliance package.** The 2018 Common Rule requires U.S. federally funded multi-site studies to use a single IRB (45 CFR 46.114). Most institutions use SMART IRB as the reliance agreement.

10. **Maintain the protocol after approval.** Amendments, continuing review (where still required), and reportable events (unanticipated problems, noncompliance, suspensions) all require IRB notification under 45 CFR 46.108(a)(4).

## Code patterns

This skill produces documents, not code. The patterns below are the canonical text structures for each protocol section. Adapt the wording; do not copy it verbatim.

### Pattern 1 — Protocol title page

```
Title: [Specific Aim in One Sentence]
Short title: [Acronym or 5-7 word phrase for the consent form]
Principal Investigator: [Name, degree, department, ORCID]
Co-Investigators: [Names, roles]
Institution: [FWA-holding institution, FWA number]
Funding: [Sponsor and grant number, or "Investigator-Initiated, Unfunded"]
Version: [v0.1 — DRAFT, v1.0 — IRB submission, v1.1 — post-stipulation]
Date: [Date of this version]
```

### Pattern 2 — Specific aims and background (the "why")

The IRB must see the scientific justification for the risk the study imposes. The minimum is one paragraph per aim plus a literature-anchored background. Do not assume the IRB members are content experts in your subspecialty — explain why the question is worth answering in plain language, then cite the preliminary data or literature that supports the design.

### Pattern 3 — Study design and methods

Structure this as a numbered sequence of events in the participant's life: screening, consent, enrollment, intervention or data collection, follow-up, exit, data analysis. The IRB reads this as a timeline and looks for the moment a participant is at risk.

### Pattern 4 — Inclusion and exclusion criteria

Express criteria as bullet points, not prose. For each exclusion, name the safety or scientific reason. The IRB will not approve "convenience" exclusions without a justification.

### Pattern 5 — Risks, mitigations, and benefits

Use a three-column table: Risk | Likelihood and severity | Mitigation. Pair every risk with a mitigation. Pair every benefit with the population that receives it. The IRB will write a stipulation if the benefits are not clearly distributed to the population that bears the risk (the Justice principle).

### Pattern 6 — Consent process

The consent section in the protocol must describe *how* consent is obtained, not just *that* it is obtained. Specify: who approaches the participant, in what setting, with what materials, after what waiting period, with what opportunity for questions. If consent is waived, cite 45 CFR 46.116(f) and walk through all four waiver criteria.

### Pattern 7 — Consent document (companion to the protocol)

The consent form itself must have:
- A "key information" section at the top (45 CFR 46.116(a)(5)(i)) — 5-7 bullet points the participant can read in 90 seconds.
- The eight required elements at 46.116(a)(1)-(8).
- Any applicable additional elements at 46.116(b)(1)-(6).
- A signature block for the participant and the person obtaining consent.
- An authorization line for any optional activities (biospecimen storage, future contact, data sharing).

### Pattern 8 — Data and safety monitoring

For minimal-risk studies, the PI is typically the monitor. For greater-than-minimal-risk studies, a Data and Safety Monitoring Board (DSMB) or Monitoring Plan is required. The protocol section should name: who monitors, what they monitor (AEs, SAEs, protocol deviations, data quality), on what schedule, and what stopping rules apply.

### Pattern 9 — Reportable events

List the events the PI will report to the IRB, the report window, and the channel. The standard categories are: unanticipated problems involving risks to participants or others (UPIRSO), serious noncompliance, continuing noncompliance, protocol deviations that are not noncompliance, suspensions by any other body (sponsor, FDA, DSMB), and any complaint by a participant that cannot be resolved by the study team.

## The Three-Bucket Decision: What Review Level You Are Aiming For

Most protocols sit in one of three buckets, and the bucket you are aiming for determines the level of detail, the time to approval, and the changes that will draw stipulations.

**Bucket 1 — Exempt (45 CFR 46.104).** Studies that fit one or more of the eight exempt categories. Examples: anonymous survey of non-sensitive topics; secondary analysis of data recorded in such a manner that subjects cannot be identified; benign behavioral interventions with no deception. Exempt studies can be approved in days, often without a full board meeting. The catch: the protocol still has to make the case for exempt status, and the IRB office can disagree. The protocol should name the specific exempt category and the evidence that fits it.

**Bucket 2 — Expedited (45 CFR 46.110).** Studies that are no more than minimal risk and fit one or more of the seven expedited categories. Examples: blood draws from healthy adults within volume limits; non-invasive specimen collection; survey or interview of non-sensitive topics; analysis of existing data with identifiers. Expedited review is done by the IRB chair or a designated experienced reviewer, not the convened board, and is typically faster than convened review.

**Bucket 3 — Convened (full) board.** Studies that are greater than minimal risk, or that involve vulnerable populations in ways the subparts restrict, or that use deception, or that require an Investigational New Drug or Investigational Device Exemption (IND/IDE). Convened review happens at a scheduled board meeting; the protocol is read by all members; the discussion is recorded in minutes; the outcome is one of approved, approved with stipulations, deferred, or disapproved.

The bucket you target affects every section. An exempt protocol for an anonymous survey does not need a Data Safety Monitoring Plan; a phase-1 first-in-human trial does. A protocol that targets the wrong bucket is a flag for an experienced IRB reviewer and an automatic re-write.

## The Reviewer Psychology: What an Experienced IRB Member Looks For

An experienced IRB member reads 50-200 protocols a year. They have seen every shortcut, every boilerplate paragraph, and every sign that the PI has thought carefully about the participants. They look for five things, in order.

1. **Is the PI's reasoning coherent?** Does the protocol describe a specific aim that is itself a research question, or is it a vague "we plan to study" paragraph? Coherent reasoning earns trust; vague reasoning earns stipulations.
2. **Are the risks paired with mitigations?** A risk listed without a mitigation tells the reviewer the PI has not thought about the participant. Pair every risk with a mitigation; the reviewer reads the protocol as a risk-managed plan.
3. **Is the consent process concrete?** The reviewer looks for who, when, where, with what materials, after what waiting period, with what opportunity for questions. A consent process that is described in one sentence ("we will obtain consent") is a stipulation.
4. **Are the vulnerable populations handled correctly?** The reviewer checks the subpart by subpart. A children study that does not cite 46.404, 46.405, 46.406, or 46.407 is a flag.
5. **Is the protocol internally consistent?** The protocol's study design, consent form, recruitment materials, and IRB-system summary must all say the same thing. A protocol that says 30 minutes in the design and 60 minutes in the consent is a flag.

A protocol that addresses all five earns approval in one round. A protocol that addresses four of five earns a stipulations letter. A protocol that addresses three of five earns a deferral. A protocol that addresses fewer earns a re-write or a rejection.

## Subpart Reference Card

A protocol that involves any of the four vulnerable-population subparts must cite the subpart and the specific section. The most common error is treating the subparts as a single list; they are not.

- **Subpart B — Pregnant women, fetuses, neonates.** Section 46.204 is the default-allowed research category; it requires minimal risk, no prospect of direct benefit, and the prospect of generalizable knowledge. Sections 46.205 and 46.206 cover greater-risk research. The institutional default for pregnancy research is 46.204; the other sections require additional IRB findings.
- **Subpart C — Prisoners.** Section 46.306 is the default-allowed category; it requires that the research has the prospect of direct benefit or, in the alternative, minimal risk and generalizable knowledge. Section 46.305 lists categories that are automatically allowed (e.g., research on the conditions of incarceration). OHRP must be consulted and the IRB must include a prisoner or prisoner-advocate member. Most academic institutions have a separate "prisoner research" checklist.
- **Subpart D — Children.** Four risk categories: 46.404 (minimal risk), 46.405 (greater than minimal risk with prospect of direct benefit), 46.406 (greater than minimal risk with no prospect of direct benefit but likely to yield generalizable knowledge, requires parental permission of both parents and assent of the child), 46.407 (not otherwise approvable, requires HHS consultation and public review). The choice of category is determined by the protocol's risk profile, not the protocol's preference.

The single most common subpart error is using 46.404 for a study that is not actually minimal risk. If the protocol is greater than minimal risk, the choice is 46.405 or 46.406; the IRB will not approve under 46.404.

## Common pitfalls

- **"Self-declared exempt."** A study is not exempt because the PI thinks it is; it is exempt because the IRB has applied one of the eight categories at 45 CFR 46.104 and issued a determination letter. Self-declaring is a Common Rule violation.
- **Risk listed without mitigation.** "Risk of breach of confidentiality" is a phrase the IRB has read a thousand times. It must be followed by: encryption at rest and in transit, role-based access, de-identification before analysis, data use agreements, and breach-notification procedures.
- **Consent that does not match the protocol.** A protocol that describes a 30-minute interview paired with a consent form that says "this will take 90 minutes" is an automatic stip. Cross-check the consent duration, procedures, and risks against the protocol's "study design" section.
- **Waiver of consent without the four criteria.** 45 CFR 46.116(f) requires that the research involves no more than minimal risk, that the waiver does not adversely affect participants' rights and welfare, that the research could not practicably be done without the waiver, and that participants are provided with relevant information after participation. All four must be addressed, in that order.
- **Subpart C lapses.** Prisoner research has its own approval pathway and IRB composition rules. If a participant becomes incarcerated during a study, the rules change. Most institutions have a separate "prisoner research" checklist.
- **Children without the right risk category.** Subpart D classifies child research into four categories (46.404 minimal risk, 46.405 greater than minimal risk with prospect of direct benefit, 46.406 greater than minimal risk with no prospect of direct benefit but likely to yield generalizable knowledge, 46.407 not otherwise approvable). Choosing the wrong category is a common error.
- **"Continuing review" treated as a check-the-box.** Since the 2018 Common Rule eliminated continuing review for most minimal-risk studies, many PIs assume they do not need to do anything. But the protocol still requires annual updates, amendment reporting, and UPIRSO reporting on a different cadence.
- **Vague "we will de-identify the data."** "De-identified" is a defined term in HIPAA; if HIPAA applies, the protocol must specify the method (Safe Harbor vs Expert Determination) and the specific identifiers removed.
- **No description of the consent *setting*.** A consent obtained at the bedside in the hour after surgery is qualitatively different from a consent obtained in a private research office a week later. The IRB will want the setting, the timing, and the opportunity for the participant to consult family or a primary-care provider.
- **No return of results plan.** For biospecimen studies and genomic research, the IRB increasingly expects a statement on whether and how clinically actionable results are returned to participants. A protocol that says nothing defaults to "no return," which may itself need justification.
- **Conflict of interest not disclosed.** PI has equity in the device company under study, or receives royalties from the assay. The IRB will require a management plan; an unstated conflict is grounds for suspension.

## Validation

- The protocol answers, in one sentence each: who are the participants, what do they do, what are the risks, what are the benefits, how is consent obtained, and who monitors safety.
- Every risk has a paired mitigation in the same paragraph or table row.
- Every vulnerable population in the study is mapped to the correct subpart, with the specific category cited.
- The consent document's key information section is a 90-second read.
- The protocol has been read by a colleague who has served on an IRB and has been revised to address their comments.
- For multi-site studies, a sIRB has been selected and a reliance plan is in place.
- The protocol version in the IRB system matches the protocol version in the consent form matches the version in the trial registry.

## Open alternatives

- **Electronic IRB systems:** IRBNet, Cayuse Huron, Kuali Research, InfoEd. All are commercial, all have similar feature sets; selection is usually institution-wide.
- **Reliance agreements:** SMART IRB (free, NIH-supported master reliance agreement), IRBchoice, individual reliance agreements. SMART IRB is the de facto standard for NIH-funded multi-site research.
- **Consent form builders:** Many eIRB systems include a consent template library; some institutions supplement with the OPENeX consent template or the PRISMA-compliant consent templates. Open-consent-template projects exist but are not as well curated.

## References

- 45 CFR 46 (Common Rule, revised eff. 2019-01-21), particularly Subparts A, B, C, D.
- The Belmont Report (1979), Office for Human Research Protections (OHRP).
- 45 CFR 164.514 (HIPAA de-identification) — referenced in consent and data sections.
- OHRP Guidance on Reviewing and Reporting Unanticipated Problems Involving Risks to Subjects or Others and Adverse Events (2007, still referenced).
- SMART IRB — master reliance agreement for sIRB arrangements.
- 63 FR 60364 — categories of research that may be reviewed by the IRB through an expedited procedure.
- Related skills: `ors-ethics-compliance-data-privacy` (HIPAA, GDPR, de-identification), `ors-scientific-writing-imrad-drafting` (manuscript Ethics Statement), `ors-clinical-decision-regulatory` (FDA-regulated research).

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesized from 45 CFR 46 (Common Rule, 2018 revision), The Belmont Report (OHRP, 1979), and OHRP guidance on reportable events. Reviewer-psychology section is original.