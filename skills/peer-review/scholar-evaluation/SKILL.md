---
name: scholar-evaluation
description: "Evaluate a researcher's portfolio (CV, publications, citations, funding, mentorship, service, software, talks) for tenure, awards, recruitment, or promotion: field-normalized metrics, evidence weighting, fit assessment, and a defensible written evaluation."
license: MIT
---



<!-- metadata:
category: peer-review
version: 1.0.0
author: Pradyumna Jayaram
tags:
- peer-review
- evaluation
- cv
- h-index
- tenure
- awards
- metrics
difficulty: advanced
prerequisites:
  tools: []
  skills: []"
sources: "ORCID — public researcher identifier and record (orcid.org); OpenAlex\
  \ — open citation index and bibliometric API (openalex.org); Semantic Scholar\
  \ — open citation and paper metadata (semanticscholar.org); Google Scholar\
  \ Profiles — author-level citation metrics (scholar.google.com); Scopus Author\
  \ Profile — Elsevier's curated author metrics (scopus.com); Clarivate Web of\
  \ Science — Journal Citation Reports and InCites (webofscience.com); CWTS Leiden\
  \ Ranking — field-normalized citation indicators (leidenranking.com); DORA\
  \ — Declaration on Research Assessment (sfdora.org); CoARA — Coalition\
  \ for Advancing Research Assessment (coara.eu); NIH — Biosketch format and\
  \ guidance (grants.nih.gov); NSF — Current and Pending Support and Biosketch\
  \ format (nsf.gov); Committee on Publication Ethics (COPE) — Authorship and\
  \ contributor guidance (publicationethics.org); CRediT — Contributor Roles\
  \ Taxonomy (credit.niso.org)"
-->

# Scholar / Researcher Evaluation

> Produces a structured, criterion-anchored evaluation of a researcher's portfolio: CV, publication record with field-normalized citation metrics (h-index, i10, total citations, field-weighted citation impact), grant funding, mentorship, service, software and data outputs, invited talks, and professional conduct. Renders a defensible written evaluation suitable for tenure, promotion, awards, recruitment, or annual review. Adapted by Pradyumna Jayaram from public evaluation frameworks (DORA, CoARA), open citation indices (OpenAlex, Semantic Scholar), and funder biosketch guidance (NIH, NSF).

## When to use

- You are serving on a tenure, promotion, or reappointment committee and need a structured evaluation template.
- You are evaluating a candidate for a named award, fellowship, or honorific.
- You are recruiting for a faculty, postdoc, or industry-research position and need a comparable portfolio review.
- You are running an internal mock review for a mentee preparing a tenure or promotion case.
- You are auditing a researcher's prior work as part of a grant-collaboration due-diligence process.
- You are chairing a search committee and need a consistent framework for comparing candidates across subfields.

## When NOT to use

- For evaluating a *single paper* (use `ors-peer-review-manuscript-review`).
- For evaluating a *single grant proposal* (use `ors-peer-review-grant-review`).
- For writing the *candidate's own narrative* (CV, research statement, teaching statement) — those are authoring tasks, not evaluation tasks.
- For informal, opinion-based assessment outside any formal review framework.

## Prerequisites

- Access to the candidate's full CV, biosketch, and any narrative statements they have provided.
- Access to the relevant publication databases (OpenAlex, Semantic Scholar, Scopus, Web of Science, Google Scholar) and the candidate's ORCID profile.
- The committee's or committee chair's instructions, including the criteria to apply, weighting scheme, and any policy on external letters.
- Familiarity with the candidate's field and its norms (citation density, authorship conventions, journal and conference prestige, data and software norms).
- Familiarity with field-normalized citation metrics and their limitations (see *Code patterns*).

## Core workflow

### 1. Pre-flight checks

- Confirm the role, level, and criteria (tenure and promotion, named award, recruitment, internal review).
- Confirm the candidate's career stage and trajectory — early-career, mid-career, senior — and any field-specific norms at that stage.
- Declare any conflict of interest (personal relationship, mentorship history, recent collaboration, institutional affiliation, financial interest) **before** reading the materials in depth. If a disqualifying conflict is identified, recuse immediately.
- Note the committee's confidentiality rules: most cases are evaluated under strict non-disclosure; case materials, committee deliberations, and candidate identities must not be discussed outside the committee.
- Note the format of the deliverable: written evaluation only, written evaluation with a numerical rating, written evaluation with a vote, or a recommendation to a chair or dean.

### 2. Initial assessment (read-through)

Read the materials once without note-taking to gauge the candidate's trajectory, focus, and fit.

- What is the central scientific question or program the candidate has pursued?
- Is the trajectory coherent (a single deep program, a deliberate broadening, or a scatter)?
- Is the candidate's level of recognition appropriate to their career stage and field?
- Are there immediate red flags (authorship anomalies, missing materials, ethics concerns)?

### 3. Publication record

Build a complete and accurate publication list. Verify it against ORCID, OpenAlex, Semantic Scholar, Scopus, and the candidate's Google Scholar profile. Common discrepancies:

- Name variants (initials vs. full first name, surname changes, transliteration differences).
- Duplicate records in different databases.
- Conference papers counted inconsistently across fields.
- Preprints that have since been published in a journal.

For each entry, note:

- Type of contribution (first author, senior / corresponding author, middle author, consortium member, equal contribution).
- Venue and field norms for that venue (impact factor is a poor proxy, especially across fields).
- For multi-author papers: the candidate's actual contribution (CRediT taxonomy, see *References*).

### 4. Citation metrics — what to compute, what to interpret

Compute a small, comparable set of metrics. Do not rely on any single number; report the metric, the field, the database, and the date of the snapshot.

| Metric | Definition | Field-normalized? | Strengths | Limitations |
|---|---|---|---|---|
| **Total citations** | Sum of all citations to the candidate's papers | No | Simple, transparent | Inflated by one or two highly cited papers; field-dependent |
| **h-index** | The largest *h* such that the author has *h* papers each cited at least *h* times | No | Combines productivity and impact | Field-dependent; inflates with career length; insensitive to a single blockbuster paper |
| **i10-index** | Number of publications with at least 10 citations | No | Simple | Same field-dependence as h-index; arbitrary 10-citation threshold |
| **Field-weighted citation impact (FWCI)** | Ratio of citations received to the world average for papers of the same field, year, and document type | Yes | Comparable across fields | Sensitive to database coverage; window effects (recent papers have less time to accrue citations) |
| **Relative citation rate / percentile in field** | Author's citation count relative to others in the same field and year | Yes | Intuitive ("top 10% of co-authors in field") | Sensitive to cohort and field definition |
| **Journal-level metrics (JIF, CiteScore, SJR)** | Venue-level citation metrics | Inherently field-dependent | Used in some institutional frameworks | Highly field-dependent; mis-used as paper-level quality proxies |

**Interpretation rules of thumb**

- h-index and total-citation metrics grow with career length; do not compare a 30-year career to a 5-year career on raw numbers.
- h-index and i10 are field-dependent: mathematics and the humanities have lower median h-indices than biomedicine or computer science at the same career stage. Always pair the metric with the field.
- FWCI, percentile-in-field, and Leiden-style field-normalized indicators are appropriate when comparing across fields; they require a curated source (OpenAlex, Web of Science, Scopus).
- A high total-citation count driven by one or two papers is not a substitute for sustained productivity; check the citation distribution.
- A low h-index paired with a high FWCI on a small number of recent papers can be an early signal of an emerging leader; do not penalize a candidate for being early in their citation cycle.
- Beware of "ghost" co-authorship: large consortia, multi-author collaborations, and alphabetical author lists in some fields inflate author-level counts without indicating intellectual contribution. Check the candidate's contribution on multi-author papers.

### 5. Grant funding

- List active and completed grants: role (PI, co-PI, co-investigator, key personnel), mechanism (R01, R21, NSF standard grant, ERC Starting/Consolidator/Advanced, private foundation), total direct costs, and time commitment.
- For a tenure or promotion case, the committee's policy on funding varies: some institutions require evidence of independent funding; others allow funded collaborators to count as a partial signal.
- Look for trajectory: a first R01, a first NSF standard grant, or a first ERC award are major signals of independence; renewal or follow-on funding suggests sustained productivity.
- Note funding agencies' prestige and the competitiveness of the mechanism (e.g., NIH R01 is competitive; R03 is a small grant and is weighted differently).

### 6. Mentorship and teaching

- Number and trajectory of trainees: postdocs, PhD students, masters students, undergraduate researchers.
- Trainee outcomes: first-author papers, first-job placements, awards, fellowships.
- For a tenure case, the candidate's mentorship style, mentoring plan (if on a grant), and any formal teaching evaluations.
- For a recruitment case, the candidate's record of placing trainees in competitive positions.
- Be cautious with raw trainee counts: in some fields, lab size is constrained by funding or by the candidate's research model; in others, large labs are the norm.

### 7. Service, leadership, and recognition

- Editorial roles: editor-in-chief, deputy editor, associate editor, editorial board member, guest editor.
- Peer-review service: journal reviewer, grant-review panelist, study-section member, conference program committee.
- Professional society leadership: committee chair, elected officer.
- Conference organization: program chair, area chair, session chair.
- Awards, honors, and named lectures.
- Membership in honorific societies (e.g., National Academy of Medicine, Royal Society, IEEE Fellow).

### 8. Software, data, and other research outputs

- Open-source software contributions, with adoption metrics (GitHub stars, citations of associated papers, downstream users).
- Data deposits, with persistent identifiers (Zenodo, Figshare, domain-specific repositories).
- Pre-registrations, registered reports, and protocols.
- Patents, disclosures, and commercialization.
- Clinical guidelines, policy documents, and standards contributions.
- For computational researchers: code releases, model checkpoints, and reproducible workflows.

In fields where software and data are primary outputs (computer science, computational biology, some social sciences), these are core scholarly contributions, not ancillary.

### 9. Conduct and ethics check

- Authorship and contribution transparency: does the candidate follow CRediT or an equivalent contributor taxonomy?
- Data sharing: are there persistent identifiers and adherence to the funder's data-sharing policy?
- Conflict-of-interest disclosures: complete and up to date.
- Concerns surfaced by the candidate's prior journals, funders, or institutions: retractions, expressions of concern, corrections.
- Any record of harassment, fraud, or misconduct findings at prior institutions (relevant to recruitment; the committee's policy on this varies).

### 10. Fit and trajectory

Beyond the metrics, assess the candidate's fit for the role, award, or level.

- **For tenure**: is the candidate recognized as an independent leader in their field? Is the trajectory sustainable? Does the candidate's work align with the institution's mission?
- **For a named award**: does the candidate's contribution match the award's stated criteria? Is the candidate's work of the breadth and depth the award recognizes?
- **For recruitment**: is the candidate's research program a good match for the department's strategic priorities, current strengths, and gaps? Are there natural collaborations? Are the resource needs (start-up package, space, hiring) reasonable?
- **For promotion**: is the candidate at the typical level of their cohort in their field, ahead, or behind? Are there field-specific norms that the committee should be aware of?

### 11. Tone and ethics checks

- Constructive framing: where a candidate is weak on a criterion, identify the evidence and the implication, not the person.
- No personal attacks, sarcasm, or pejorative adjectives.
- No reference to protected characteristics or irrelevant personal information.
- No out-of-scope criteria (e.g., salary, family situation, marital status, political views).
- Do not reveal the candidate's identity in a way that breaches the committee's confidentiality rules.

### 12. Finalize the evaluation

Translate the evidence into the committee's required deliverable:

- Written narrative evaluation only.
- Written narrative plus numerical rating (e.g., 1–5 scale on each of teaching, research, service).
- Written narrative plus overall recommendation (e.g., tenure recommended, recruitment recommended, award recommended).
- For a search committee: a ranked or unranked shortlist with comparative narrative.

Be explicit about evidence-based strengths, evidence-based weaknesses, and the fit-for-role assessment. Distinguish between "this candidate is excellent for this role" and "this candidate is excellent in absolute terms" — these are not the same conclusion.

## Code patterns

### Standard evaluation skeleton

```text
================================================================================
EVALUATION OF [Candidate Name], [Current Title]
[For: tenure / promotion / award / recruitment / annual review]
================================================================================

1. Summary
----------
[3-5 sentence synopsis. State the candidate's research program, the
 trajectory, the level of recognition, and your overall assessment
 relative to the role or award.]

2. Publication record
--------------------
- Total publications: [n], in [field], as of [date].
- First-author / corresponding-author: [n].
- Citation metrics: total citations [n]; h-index [n]; i10 [n];
   FWCI [value] ([source: OpenAlex / Scopus / Web of Science]).
- Note: [field-normalized comparison; explanation of any
   unusually high or low single-paper contributions.]

3. Grant funding
----------------
[Active and completed grants, with role, mechanism, and total costs.]

4. Mentorship and teaching
--------------------------
[Trainee count, trainee outcomes, teaching evaluations if applicable.]

5. Service, leadership, and recognition
---------------------------------------
[Editorial roles, grant-panel service, awards, society leadership.]

6. Software, data, and other research outputs
---------------------------------------------
[Open-source software, data deposits, patents, guidelines, etc.]

7. Conduct and ethics
---------------------
[Authorship transparency, data sharing, conflict disclosure,
 retractions or corrections, any record of misconduct findings.]

8. Fit and trajectory
--------------------
[Explicit fit-for-role assessment. Identify the criteria the
 candidate meets, partially meets, or does not meet, with
 evidence.]

9. Strengths
------------
- [Specific strength with evidence.]
- ...

10. Areas for development
-------------------------
- [Specific weakness, why it matters for the role, what a fix
   would look like at this career stage. Frame constructively.]
- ...

11. Overall recommendation
--------------------------
[Narrative tying the evidence to the role's criteria. Numerical
 rating if required. Recommendation: e.g., "Tenure recommended
 with strong enthusiasm" / "Recruit as Assistant Professor,
 start-up package X" / "Not recommended at this time; the
 candidate should be considered again after [evidence gap]
 is addressed."]
```

### Field-normalized comparison template (when comparing across fields)

```text
| Candidate | Field | Career stage | Total pubs | h-index | FWCI | Field percentile |
|-----------|-------|--------------|------------|---------|------|------------------|
| A         | Math  | 8 yrs post-PhD| 25         | 12      | 1.4  | top 15%          |
| B         | CS    | 6 yrs post-PhD| 40         | 18      | 2.1  | top 5%           |
| C         | Bio   | 10 yrs post-PhD| 55        | 28      | 1.8  | top 10%          |
```

Use field-normalized metrics (FWCI, percentile-in-field) for cross-field comparison; do not compare raw h-indices across fields.

### Reusable evaluation rubric

| Criterion | Look for | Common failure mode |
|---|---|---|
| Publication record | Sustained productivity; appropriate authorship position; field-normalized impact | Single-blockbuster over-reliance; alphabetical-author inflation |
| Grant funding | Independent funding; trajectory; mechanism appropriateness | No independent funding; co-I on a single grant over 5 years |
| Mentorship | Trainee outcomes; sustained lab or group; evidence of mentoring style | Large lab with no published first-author papers from trainees |
| Service | Appropriate level for career stage; high-quality roles | Inflated service record (membership in many committees with no leadership) |
| Software / data | Persistent identifiers; adoption; reproducibility | "Code available upon request" |
| Conduct | Authorship transparency; no retractions; complete disclosures | Authorship anomalies; image-integrity concerns in cited work |
| Fit | Match to role criteria; trajectory sustainability | Strong on paper, weak fit for the specific role |

### Red-flag phrases to surface to the committee chair (confidential section)

- Authorship anomalies (gifted or ghost authorship; alphabetical author lists treated as equal contribution).
- Retractions or expressions of concern on key papers, with no clear explanation.
- Concerns about data or image integrity in cited prior work.
- Conflicts of interest not declared by the candidate.
- Inflated claims in the CV (papers listed but not actually published; grants listed as PI when role was co-I).
- Misrepresentation of trainee outcomes (listing a trainee as "placed" in a role they did not take).
- Misalignment between the candidate's narrative statements and their CV or publication record.

## Common pitfalls

- **Comparing raw metrics across fields**: an h-index of 25 in mathematics is exceptional; in molecular biology it is good; do not compare across fields without normalization.
- **Ignoring career stage**: a first-author Cell paper from a postdoc is not the same as a corresponding-author paper from a senior PI; calibrate expectations to stage.
- **Penalizing service**: some institutions undervalue service; a strong service record at a regional or national committee is a legitimate contribution, especially for promotion to full.
- **Ignoring software and data outputs**: in computational fields, software and data are first-class scholarly contributions; do not count only journal papers.
- **Treating impact factor as paper quality**: JIF, CiteScore, and SJR are venue-level metrics; they are a poor proxy for any individual paper's quality. DORA and CoARA both call for assessing research on its own merits, not on the journal it appears in.
- **Reading narrative statements as evidence**: the candidate's narrative is their framing of their work; the evidence is in the publication record, the funding record, and the documented outcomes.
- **Revealing identity in a blind review**: if the committee is operating under blind review, even small clues (naming a specific dataset, identifying a specific institution) can unblind you.
- **Failing to contextualize gaps**: gaps in publication record may be due to parental leave, illness, teaching load, pandemic disruption, or field-specific career events; ask the chair for the committee's policy on contextualization before penalizing.
- **Drifting on the candidate's personal characteristics**: the evaluation is on scholarship and fit, not on the candidate's personal life.

## Validation

A good written evaluation is itself a small scholarly document. Before submitting, check:

- [ ] The summary captures the candidate's program in your own words.
- [ ] Publication record verified against at least two databases and the candidate's ORCID.
- [ ] Citation metrics reported with field, database, and date of snapshot.
- [ ] Field-normalized metrics used for cross-field comparisons.
- [ ] Authorship position and contribution accounted for on multi-author papers.
- [ ] Grant funding list reflects the candidate's actual role (PI, co-PI, co-I).
- [ ] Mentorship record is concrete (trainee names, outcomes) where possible.
- [ ] Service record reflects the candidate's actual roles, not aspirational memberships.
- [ ] Software and data outputs are listed where they are core scholarly contributions.
- [ ] Conduct and ethics check is complete (authorship, retractions, disclosures).
- [ ] Fit-for-role assessment is explicit and tied to the role's criteria.
- [ ] Recommendation follows logically from the evidence.
- [ ] Confidentiality preserved (no identifying information in blind reviews; no case content shared outside the committee).
- [ ] Conflict of interest declared up front and again if a late-discovered conflict emerges.
- [ ] Tone is constructive throughout, even on a "not recommended" or "do not advance" outcome.

## Open alternatives

- **Open citation indices** (OpenAlex, Semantic Scholar, Crossref) provide free access to publication and citation data; **Scopus** and **Web of Science** are subscription products with curated author profiles and historical coverage.
- **ORCID** is the de facto open standard for researcher identification; an ORCID profile consolidates publications, grants, and reviews.
- **FWCI and field-normalized indicators** (OpenAlex, CWTS Leiden Ranking, InCites) are the open alternatives to raw h-index for cross-field comparison.
- **DORA** (Declaration on Research Assessment) and **CoARA** (Coalition for Advancing Research Assessment) provide open frameworks for evaluating research on its own merits, not on the venue in which it appears.
- **OSF, Zenodo, and domain-specific repositories** (GenBank, PDB, PRIDE, etc.) provide persistent identifiers for data, code, and protocols.
- **CRediT** (Contributor Roles Taxonomy) is the open standard for declaring author contributions.
- **AI assistants for prose polish** are useful for tightening the written evaluation, but the reviewer's judgment remains the deciding factor; do not paste confidential case materials into a third-party LLM without the committee's approval.

## References

### Internal cross-links

- `ors-peer-review-manuscript-review` — for evaluating a single paper, not a researcher's record.
- `ors-peer-review-grant-review` — for evaluating a grant proposal, not a researcher's record.
- `ors-peer-review-reviewer-response` — for the response process in a peer-review or evaluation workflow.
- `ors-scientific-writing-cv-structure` — the candidate's side of the same process.
- `ors-ethics-compliance-authorship` — authorship and contribution guidance.
- `ors-open-science-data-sharing` — data and code deposition expectations.

### External links (verifiable, public)

- ORCID: <https://orcid.org/>
- OpenAlex: <https://openalex.org/>
- Semantic Scholar: <https://www.semanticscholar.org/>
- Google Scholar Profiles: <https://scholar.google.com/>
- Scopus Author Profile: <https://www.scopus.com/freelookup/form/author.uri>
- Web of Science / InCites: <https://webofscience.com/>
- CWTS Leiden Ranking: <https://www.leidenranking.com/>
- DORA — Declaration on Research Assessment: <https://sfdora.org/>
- CoARA — Coalition for Advancing Research Assessment: <https://coara.eu/>
- NIH Biosketch format and guidance: <https://grants.nih.gov/grants/forms/format-bio-sketch.htm>
- NSF Current and Pending Support: <https://www.nsf.gov/bfa/dias/policy/cps.jsp>
- COPE Authorship and contributor guidance: <https://publicationethics.org/resources/discussion-documents/authorship>
- CRediT — Contributor Roles Taxonomy: <https://credit.niso.org/>

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Heavy rewrite of upstream scholar-evaluation skill: added field-normalized metrics table (h-index, i10, total citations, FWCI) with explicit "do not compare across fields" guardrail, added multi-author paper contribution check, added software/data outputs section, added DORA / CoARA framing for venue-independent evaluation, added CRediT cross-link, added retraction/expression-of-concern red-flag section, added fit-for-role explicit structure, added "do not paste case materials into third-party LLMs" guardrail.