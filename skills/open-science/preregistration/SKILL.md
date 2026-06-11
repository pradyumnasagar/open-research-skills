---
name: preregistration
description: "Use when preregistering a study design (hypothesis, methods, analysis plan) before data collection on OSF Registries or AsPredicted, applying for ClinicalTrials.gov registration for interventional trials, or submitting a Registered Report."
license: MIT
---



<!-- metadata:
category: open-science
version: 1.0.0
author: Pradyumna Jayaram
tags:
- preregistration
- osf
- aspredicted
- registered-reports
- clinicaltrials.gov
difficulty: intermediate
prerequisites:
  tools:
  - web-browser
  - orcid
  - latex-or-word
  skills: []"
sources: "Original: OSF Registries help and documentation (https://osf.io/registries).;\
  \ Original: AsPredicted.org template and FAQ (https://aspredicted.org/).; Original:\
  \ ClinicalTrials.gov registration (https://clinicaltrials.gov/).; Original: Open\
  \ Science Framework (https://osf.io/).; Original: Registered Reports — cRedi\
  \ (https://cos.io/rr/).; Original: SPIRIT 2013 statement for clinical trial protocols.;\
  \ Original: CONSORT 2010 for reporting.; Improvisions: Pradyumna Jayaram —\
  \ OSF template comparison, AsPredicted vs OSF decision tree, clinical-trial registration\
  \ flowchart, Registered Report format comparison (1/2/3)."
-->

# Preregistration

> Preregistration is the act of publicly committing to a research plan — hypothesis, primary outcome, sample size, and analysis — **before** data are collected. It is a powerful anti-dashboarding measure (the "fishing" / "p-hacking" problem) and is now mandated or strongly recommended by many funders (US Office of Science and Technology Policy 2023 memo; the UK Reproducibility Network; the NIH analytic guide). This skill covers OSF Registries, AsPredicted, ClinicalTrials.gov (required for US clinical trials), and Registered Reports — the four preregistration pathways.

## When to use

- **Confirming a study design** before data collection starts — to commit to analysis.
- Responding to reviewers or funder concerns about **p-hacking / analytic flexibility**.
- Required **ClinicalTrials.gov registration** for any interventional trial with a US site, NIH-funded, or FDA-regulated.
- Submitting a **Registered Report** (peer review of the protocol before results).
- Applying for a grant that asks for a **preregistration plan**.
- Planning a **replication study** where the design must match the original.

## When NOT to use

- For **preprints** (posting a completed manuscript) — see `ors-open-science-preprints`.
- For **data deposits** without a study plan — see `ors-open-science-fair-data`.
- For **code release** (no hypothesis) — see `ors-open-science-code-release`.
- For exploratory / pilot / feasibility work that is intended to generate hypotheses. Preregistration is for **confirmatory** research.
- After data are already collected — preregistration is a pre-data commitment. You cannot preregister after the fact.
- For purely observational / database / secondary-data analyses — these often use **analytic pre-registration** (specifying the analysis plan, not the data collection) on OSF.

## Prerequisites

- A **complete study protocol** (hypothesis, primary outcome, sample size, analysis plan).
- ORCID iD for all authors (required for OSF and AsPredicted).
- IRB/IACUC approval number (or proof of exemption) — most registries ask for it.
- For ClinicalTrials.gov: a Unique Trial Identifier (NCT number, if an amendment) or a sponsor-designated protocol.

## Core workflow

1. **Write the study protocol and analysis plan.** Use a template (see "Document patterns" below). Be specific: sample size N, primary outcome variable, primary analysis model, alpha, power, correction for multiple comparisons.
2. **Choose the platform.** Use the decision tree:
   - **Basic**: AsPredicted — simplest (one page, 10 questions).
   - **Standard**: OSF Registries — most comprehensive, searchable, indexed in Crossref.
   - **Regulated**: ClinicalTrials.gov — required by law for US interventional trials.
   - **Publishing**: Registered Report format via a participating journal.
3. **Upload to the platform.** Fill in the structured fields; attach the protocol as a PDF.
4. **Timestamp.** The platform mints a DOI and date stamps the record. This is your proof of priority.
5. **Collect the data.** Do **not** look at the primary outcome until data collection is complete. No peeking (or disclose that you peeked).
6. **Run the analysis as specified.** If the analysis must change, disclose the change and explain why. Post-hoc changes are allowed but must be disclosed in the paper.
7. **Link the preregistration to the paper.** Include the DOI in the final manuscript; cite the preregistration in the methods. Check the box in the journal submission system.
8. **Update the record** for any changes (protocol amendments, sample-size re-estimation, analytic modifications).

## Document patterns

### Pattern 1: OSF vs AsPredicted vs ClinicalTrials.gov decision tree

```
Is this a US-regulated interventional clinical trial?
├── YES → ClinicalTrials.gov (required by law)
│         • Interventional (drug, device, gene therapy, etc.)
│         • US site OR NIH-funded OR FDA-regulated
│         • Must register BEFORE first patient enrolled
│         • Required fields: NCT number, recruitment status,
│           primary/secondary outcomes, analysis plan
└── NO  → Is this for a Registered Report (journal publication)?
         ├── YES → Use the Registered Report format from the target journal
         │        (e.g., Cortex, Open Science Framework, BMJ Open Science)
         │        • Journal sends protocol out for peer review
         │        • In-principle acceptance conditional on methods
         │        • Results paper gets fast-track if methods are sound
         └── NO  → Does the field expect a one-page confirmation?
                  ├── YES → AsPredicted (simplest, 10 questions)
                  │       • Common in psychology, social sciences, behavioral bio
                  │       • Lightweight, fast (~15 min to complete)
                  │       • No DOI (but has a unique URL and timestamp)
                  └── NO  → OSF Registries (full-featured)
                        • DOI ( searchable in Crossref)
                        • 50+ fields, all searchable
                        • Templates for different designs (RCT, survey, etc.)
                        • The default for biology, neuroscience, most fields
```

### Pattern 2: The minimum preregistration fields (any platform)

Every preregistration must include:

1. **Hypothesis** (what you are testing)
2. **Primary outcome** (exactly what you will measure)
3. **Sample size** (N, or stopping rule)
4. **Inclusion/exclusion criteria** (who is in the study)
5. **Analysis plan** (the statistical model)

Optional but recommended:

- **Secondary outcomes** (exploratory outcomes)
- **Power calculation** (alpha, power, effect-size assumption)
- **Correction for multiple comparisons** (correction method: Bonferroni, FDR, etc.)
- **Exclusion criteria** (how you handle missing data, outliers)
- **Data exclusions** (any QC criteria decided before seeing the data)
- **Analysis software** (R, Python, JASP, etc.)

### Pattern 3: OSF Registries preregistration template (abbreviated)

Most OSF fields map to this skeleton:

```markdown
# Title
[Hypothesis in one sentence.]

# Hypothesis
[State the directional hypothesis: "We predict that X will increase Y..."]

# Primary outcome
[Name the variable; how it will be measured; units.]

# Secondary outcomes
[Optional: list up to 3 secondary exploratory outcomes.]

# Inclusion criteria
- Age range: [...]
- Population: [...]
- Other: [...]

# Exclusion criteria
- [...]
# Sample size
- Target N: [...]
- Power calculation: 80% power to detect d = [...] at α = 0.05

# Analysis plan
- Primary test: [e.g., linear mixed model with fixed effect of GROUP, random effect of SUBJECT]
- Covariates: [age, sex, baseline score]
- Alpha: 0.05 (two-tailed)

# Exclusion rules
- Any samples with < 80% missing data will be excluded.
- Outliers identified as > 3 SD from the mean will be flagged
  and sensitivity analyses run with and without them.

# Known deviations from the analysis plan
[None to date / Will be added if the protocol changes]

# IRB approval
- Protocol #[...] obtained from [Institutional Review Board name]
- Approval date: [...]
```

### Pattern 4: AsPredicted (10 questions)

AsPredicted simplifies to 10 questions:

1. **What is the hypothesis?** (1 sentence)
2. **What are the variables?**
   - Independent variable(s):
   - Dependent variable(s):
3. **How many participants will you collect data from?** (N, or description of stopping rule)
4. **When are you going to collect the data?** (dates or "continuous")
5. **Is this a between- or within-subjects design?**
6. **What analysis will you run to test the hypothesis?** (specify the test, e.g., "t-test", "mixed-effects model")
7. **What does that analysis tell you?**
8. **Any other analysis?** (list any secondary/ exploratory)
9. **How can we contact you?** (email, ORCID)
10. **Anything else?**

### Pattern 5: ClinicalTrials.gov required fields

For US interventional trials, you must register:

| Field | Description |
|-------|-------------|
| Unique Trial Identifier | NCT number (assigned on first save) |
| Brief Title | ≤ 120 characters |
| Official Title | Full title |
| Study Type | Interventional |
| Primary Outcome | Variable, measurement, time point |
| Secondary Outcomes | Up to 10 |
| Arms / Interventions | Drug, device, procedure |
| Eligibility | Inclusion/exclusion criteria |
| Contact / Sponsor | Name, phone, email |
| Recruitment Status | Not yet recruiting / Recruiting / Completed / etc. |
| Study Start Date | Expected first enrollment |
| Primary Completion Date | Expected last enrollment |
| Completion Date | Expected final data collection |
| Summary / Description | ≤ 5000 characters |
| Study Design | Allocation, masking, intervention model |
| Masking | Who is blinded |
| Intervention Model | Single group, parallel, crossover |
| Number of Arms | 1, 2, 3+ |
| Primary Purpose | Treatment, prevention, diagnostic, etc. |

Register **before** first patient enrolled. Updates required within 21 days of a change (recruitment status, primary outcome, sample size). Results must be posted within 12 months of the primary completion date.

### Pattern 6: Registered Report formats

Registered Reports come in three "formats" (not versions, but stages):

| Format | What is reviewed | What is guaranteed |
|--------|-------------------|---------------------|
| **Stage 1 (Protocol)** | The study design, hypothesis, methods, analysis | **In-principle acceptance** — if you run the study as specified, the results paper will be published (subject to minor review). |
| **Stage 2 (Results)** | The results, with the protocol in the supplement | Peer review of the full paper. |
| **Stage 3 (Registered Report)** | Protocol + Results in one submission | **Two-stage review** — protocol reviewed first, then results after data are collected. |

Most journals offer **Stage 1** as the default. The workflow is:

```
1. Submit protocol (preregistration + analysis plan)
2. Stage 1 peer review → in-principle acceptance (IPA) or revise and resubmit
3. Collect data (do not look at results yet)
4. Submit results paper with protocol in supplement
5. Stage 2 peer review → publication OR major concerns (rare if IPA was given)
```

Journals that offer Registered Reports include:

- **Cortex** (and other Center for Open Science partner journals)
- **eLife** (exceptions apply)
- **BMJ Open Science**
- **F1000Research**
- **Royal Society Open Science**
- **Open Science Framework** journals

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| **Preregistering after data collection** | Not allowed; it's post-hoc, not pre-registration | Preregister BEFORE any data are touched. |
| **Changing the analysis without disclosure** | Reviewers consider this undisclosed p-hacking | Any post-hoc changes go in the paper's limitations section with explanation. |
| **AsPredicted for a clinical trial** | Not legally sufficient for FDA/NIH registration | Use ClinicalTrials.gov for US interventional trials. |
| **No sample-size justification** | Underpowered studies are the norm; reviewers ask | Include a power calculation (G*Power, R, or simulation). |
| **Vague primary outcome** | "We will measure gene expression" is not specific | "mRNA levels of gene X in peripheral blood monocytes, measured by qRT-PCR, normalized to GAPDH." |
| **Not disclosing peeked data** | Reviewers assume you looked; they will ask in review | Write: "One interim analysis was conducted at N = X; the study continued as planned because..." |
| **No IRB number** | Most journals require it; will be asked in review | Get IRB approval before preregistering. |
| **Confusing preregistration with clinical trial registration** | Different requirements, different platforms | Clinical trials go to ClinicalTrials.gov. |
| **Registered Report rejected at Stage 1** | The design or analysis was not sound | Revise per reviewer feedback; don't skip to a Stage 2 submission elsewhere without disclosing. |
| **"We did not preregister" in a preregistered study** | The journal's check box will catch this | Either preregister or say "preregistered, DOI: ..." in the methods. |
| **Including exploratory outcomes as primary** | This is p-hacking; reviewers see through it | Distinguish primary (confirmatory) from secondary (exploratory). The primary outcome gets the formal alpha; the rest are treated as hypothesis-generating. |
| **Using an unregistered change as a limitation** | The fix is to disclose, not hide | Add a section "Deviations from the preregistered protocol" in the paper. |

## Validation

A preregistration is complete when:

- [ ] The hypothesis is stated as a directional prediction (not a question).
- [ ] The primary outcome is defined with exact variable name, measurement method, and time point.
- [ ] The sample size is justified with a power calculation (or an explicit Bayesian stopping rule).
- [ ] The analysis model is named (e.g., "linear mixed model", "two-sample t-test", "Cox proportional hazards").
- [ ] The platform has minted a timestamp and (for OSF) a DOI.
- [ ] All co-authors are listed and have approved the submission.
- [ ] The IRB/IACUC number is included.
- [ ] The preregistration is linked in the final manuscript (DOI in the methods).
- [ ] Any changes from the plan are disclosed in the final paper.

## Open alternatives

| Commercial / restricted service | Open alternative | Trade-off |
|----------------------------------|------------------|-----------|
| ClinicalTrials.gov (required, free) | — | Required for US trials; no alternative. |
| AsPredicted (free) | OSF Registries (also free) | OSF is more comprehensive; AsPredicted is simpler. |
| PROSPERO (systematic reviews) | OSF Preregistration for systematic review protocols | PROSPERO is domain-specific for systematic reviews; OSF is general. |
| REDCap (clinical data capture) | OpenClinica, Castor EDC | REDCap is free for academics; OpenClinica and Castor are also free for academics. |
| SurveyMonkey (surveys) | Qualtrics (institutional license), Limesurvey (open-source) | Limesurvey is self-hosted, free; SurveyMonkey has a free tier. |
| Dropbox Paper (collaborative writing) | HackMD / HedgeDoc, Quarto, Manubot | Manubot is git-native, versioned. |

## References

- OSF Registries help: https://osf.io/registries
- OSF Preregistration templates: https://osf.io/prereg
- AsPredicted: https://aspredicted.org/
- AsPredicted FAQ: https://aspredicted.org/faq
- ClinicalTrials.gov: https://clinicaltrials.gov/
- ClinicalTrials.gov FAQs: https://clinicaltrials.gov/ctk/about-trials
- Registered Reports (cRedi): https://cos.io/rr/
- Registered Reports overview: https://cos.io/rr/
- SPIRIT 2013 statement: https://www.spirit-statement.org/
- CONSORT 2010: https://www.consort-statement.org/
- NIH Analytic Guide: supports preregistration for secondary analysis.
- US OSTP 2023 memo: requires federally funded trials to register.
- UK Reproducibility Network recommendations: https://ukrn.org/
- G*Power: https://gpower.software.informer.com/

## Related skills

- `ors-open-science-preprints` — to post the results after data collection.
- `ors-open-science-fair-data` — to deposit the data after the paper is published.
- `ors-open-science-code-release` — to release the code used in the analysis.
- `ors-omics-statistics-` (multiple skills) — for statistical analysis methods.
- `ors-bioinformatics-clinical-` (multiple) — for clinical data handling.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesised OSF Registries help; AsPredicted FAQ; ClinicalTrials.gov fields; SPIRIT 2013; Registered Reports info (cRedi); NIH analytic guide; US OSTP memo. OSF vs AsPredicted vs ClinicalTrials decision tree; OSF template skeleton; AsPredicted 10 questions; Registered Report format comparison are original compositions.