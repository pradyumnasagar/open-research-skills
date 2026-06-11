---

name: manuscript-structure
description: "Section-by-section guidance for biomedical manuscripts using the IMRAD frame (Introduction, Methods, Results, Discussion), title and abstract strategies, figure/table selection, citation styles, and reporting checklists (CONSORT, STROBE, PRISMA, ARRIVE 2.0, MIAME, MINSEQE)."
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

# Manuscript Structure (IMRAD)

> A biomedical research manuscript is a contract between the authors and the reader: the authors promise to state a question, describe how they answered it, show what they found, and explain what the finding means. IMRAD (Introduction, Methods, Results, Discussion) is the dominant contract across biomedicine because it makes that promise auditable. This skill encodes the section-by-section moves, the title and abstract strategies that vary by journal, the figure/table selection logic, the citation style choices, and the reporting checklists that increasingly gate publication.

## When to use

- Drafting a primary research article for a biomedical journal.
- Restructuring a methods-heavy or results-heavy manuscript to match the journal's IMRAD expectation.
- Choosing between abstract formats (unstructured vs. structured) for the target journal.
- Selecting which reporting checklist (CONSORT, STROBE, PRISMA, ARRIVE 2.0, MIAME, MINSEQE) is required.
- Deciding whether to follow Vancouver (numeric), APA (author-date), or Harvard-style citation format.

## When NOT to use

- For review articles, opinion pieces, or commentaries (different structural conventions).
- For pure clinical case reports (CARE checklist; not the IMRAD frame).
- For computational-only methods papers (often follow a different Results→Validation flow).
- For humanities or social-science manuscripts (IMRaD still common but with different rhetorical norms).

## Prerequisites

- Completed study with primary data, or completed re-analysis with clearly stated inputs.
- Decision (or shortlist) of target journal(s) before locking structure.
- Reporting checklist selected before writing the Methods section."
- Co-author agreement on author order and on which data are "primary" vs. "supplementary."

## Core workflow

### 1. Pick the target journal before writing

The IMRAD frame is universal, but the word limits, figure caps, abstract style, citation format, and reporting-checklist expectations all vary by journal. Lock the target journal — or a shortlist of two — before drafting. The journal's "Author Guidelines" page resolves more structural questions than any style guide.

### 2. Select the reporting checklist before drafting Methods

Match the study design to the checklist:

| Study design | Checklist | Source |
|--------------|-----------|--------|
| Randomized clinical trial | CONSORT 2010 (+ relevant extension) | consort-statement.org |
| Observational epidemiology | STROBE | strobe-statement.org |
| Systematic review / meta-analysis | PRISMA 2020 | prisma-statement.org |
| Animal preclinical research | ARRIVE 2.0 | arriveguidelines.org |
| Microarray experiment | MIAME | fg.ed.ac.uk/miame |
| RNA-seq / sequencing-based expression | MINSEQE | fg.edu.au/MINSEQE |
| Diagnostic accuracy study | STARD | stard-statement.org |
| Case report | CARE | care-statement.org |
| Prediction model development | TRIPOD | tripod-statement.org |

The checklist is a Methods-section outline, not an afterthought. Filling it out first forces a methods draft that is auditable.

### 3. Draft the title last, not first

The title is the most-visited sentence in the paper. Draft it after the Results and Discussion are stable, so the title reflects what the manuscript actually claims. Title strategies by venue are in the Code Patterns section.

### 4. Build the Results section around the figures, not the other way around

In a typical biomedical manuscript, each Results subsection corresponds to one main figure (or one main table). The narrative arc is: "We observed X (Fig. 1). To test whether X was due to Y, we did Z (Fig. 2). We found that..." Drafting the figure legends first forces the authors to commit to a claim per figure, which in turn forces a clear Results narrative.

### 5. Draft the Discussion in four moves

A clean biomedical Discussion follows four moves in order:
1. **Main finding in plain words** (one or two sentences, no jargon).
2. **Comparison to prior work** (how the result advances, confirms, or contradicts the field).
3. **Mechanism or interpretation** (a proposed explanation, with caveats).
4. **Limitations and next steps** (honest, specific, and not buried in a final paragraph).

### 6. Match the citation style to the journal

Citation style is set by the journal, not by the authors. Common biomedical styles:

| Style | In-text format | Reference list | Typical journals |
|-------|----------------|----------------|------------------|
| Vancouver (numeric) | [1], [2,3] | Numbered, ordered by appearance | ICMJE family, NEJM, Lancet, JAMA, BMJ |
| APA (author-date) | (Smith, 2020) | Alphabetical by first author | Some psychology and nursing journals |
| Harvard (author-date) | (Smith, 2020) | Alphabetical by first author | Some public-health and European journals |
| Nature/Numbered | Superscripted numbers | Numbered, ordered by appearance | Nature family |
| Science/Numbered | (1), (2) in text or superscript | Numbered, alphabetical first-author | Science family |

A manuscript submitted to a Vancouver-style journal must be reformatted in any author-date system before submission. Many journals will desk-reject a manuscript that uses the wrong citation style.

## Code patterns

### Title strategies by venue

| Venue | Default title style | Length cap | Worked example |
|-------|---------------------|------------|----------------|
| Nature | One-sentence declarative claim (no question marks) | 75 characters | "A single-cell atlas of the aging mouse hippocampus" |
| Science | Descriptive noun phrase, often 2 lines | 90 characters | "Microbial succession during soil restoration follows deterministic trajectories" |
| Cell | Declarative or descriptive | 100 characters | "BRD4 phase separation regulates lineage-specifying enhancers" |
| NEJM | Declarative claim in plain words | ~85 characters | "Tirzepatide for the Treatment of Obstructive Sleep Apnea" |
| Lancet | Declarative claim in plain words | ~85 characters | "Routine molecular profiling in advanced solid tumours" |
| PLOS Medicine | Two-part: subtitle after colon | 200 characters | "Vaccination coverage in sub-Saharan Africa: a retrospective analysis of DHS data, 2010-2022" |
| eLife | Descriptive noun phrase | 120 characters | "A conserved kinase couples cell polarity to nutrient uptake in C. elegans" |
| JAMA | Declarative or descriptive | ~90 characters | "Effect of community-wide salt substitution on cardiovascular events and death" |

The "rhetorical question title" ("Why does X cause Y?") is a common anti-pattern in lower-impact journals and is generally avoided by the top-tier general-interest journals.

### Abstract structure: unstructured vs. structured

**Unstructured abstract** (Nature, Science, Cell style)
- One paragraph, ~150-200 words.
- Opens with the question, ends with the implication.
- No labeled subheadings.
- Author writes: the 30-second elevator pitch, expanded to a paragraph.

**Structured abstract** (clinical journals, ICMJE-recommended)
- Labeled subheadings: Background, Methods, Results, Conclusions.
- Word limits per section, set by journal (e.g., JAMA: Background 2-3 sentences, Methods 3-4 sentences, Results 5-6 sentences, Conclusions 2-3 sentences).
- Required by most clinical journals (NEJM, Lancet, JAMA, BMJ, Ann Intern Med).
- Often optional or discouraged in basic-science journals (Nature, Science, Cell).

**Worked example: structured abstract for a clinical trial (JAMA, ~350 words)**

> **Importance:** Glioblastoma is the most aggressive primary brain tumor in adults, and recurrence after temozolomide chemotherapy is nearly universal. There is no approved second-line therapy that meaningfully extends survival.
>
> **Objective:** To determine whether the addition of the METTL3 inhibitor STM2457 to temozolomide improves overall survival in patients with recurrent glioblastoma harboring high tumor METTL3 expression.
>
> **Design, Setting, and Participants:** Phase 2 randomized, double-blind, placebo-controlled trial conducted at 12 academic medical centers between March 2021 and October 2024. Participants were adults (≥18 years) with histologically confirmed glioblastoma, first recurrence after temozolomide, and high METTL3 expression by immunohistochemistry. Follow-up was 24 months.
>
> **Interventions:** STM2457 5 mg orally daily + temozolomide 150 mg/m² every 28 days (n=86) vs. placebo + temozolomide (n=86).
>
> **Main Outcomes and Measures:** Primary: overall survival. Secondary: progression-free survival, objective response rate, treatment-related adverse events grade ≥3.
>
> **Results:** Among 172 randomized patients (median age 59 years; 62% male), median overall survival was 14.8 months (95% CI 12.6-17.1) in the STM2457 arm vs. 11.2 months (95% CI 9.7-12.9) in the placebo arm (HR 0.71, 95% CI 0.55-0.92; P=.008). Grade ≥3 adverse events occurred in 31% of STM2457-arm patients and 28% of placebo-arm patients.
>
> **Conclusions and Relevance:** In patients with METTL3-high recurrent glioblastoma, the addition of STM2457 to temozolomide improved overall survival with a manageable safety profile. These findings support a phase 3 trial in biomarker-enriched patients.

### Figure/table selection logic

| Content type | Use a Figure | Use a Table |
|--------------|-------------|-------------|
| Time-series or dose-response curves | Yes (line graph) | No |
| Group comparison with many categories | Yes (bar or violin plot) | No (unless the table is the canonical form) |
| Patient demographics (clinical trial) | No (table is canonical) | Yes (CONSORT requires Table 1) |
| Flow of participants (CONSORT diagram) | Yes (figure is canonical) | No |
| Multiple multivariate models with coefficients | Maybe (forest plot) | Often yes (full model table) |
| Schema of mechanism | Yes (cartoon figure) | No |
| Single-gene mutation list (oncoprint) | Yes (oncoprint figure) | No |
| Demographic cross-tabulation | No (figure is wrong) | Yes |
| Comparison of methods | Often table | Sometimes figure |
| High-dimensional data (PCA, UMAP) | Yes | No |

The rule of thumb: tables are for the reader who needs the exact number; figures are for the reader who needs the pattern. A 50-row table of patient demographics should never become a heatmap; a 5-row table of mean expression values should never become a bar plot.

### Vancouver reference formatting (ICMJE)

> 1. Lee JS, Kim S, Hur S, et al. METTL3-dependent m6A modification of MYC mRNA drives glioblastoma resistance to temozolomide. Cancer Cell. 2023;41(7):1314-1328.e8. doi:10.1016/j.ccell.2023.06.005
>
> 2. Hanahan D, Weinberg RA. Hallmarks of cancer: the next generation. Cell. 2011;144(5):646-674. doi:10.1016/j.cell.2011.02.013
>
> 3. ENCODE Project Consortium. Expanded encyclopaedias of DNA elements in the human and mouse genomes. Nature. 2020;583(7818):699-710. doi:10.1038/s41586-020-2493-4

### APA 7 reference formatting (author-date)

> Hanahan, D., & Weinberg, R. A. (2011). Hallmarks of cancer: the next generation. *Cell*, *144*(5), 646-674. https://doi.org/10.1016/j.cell.2011.02.013
>
> Lee, J. S., Kim, S., & Hur, S. (2023). METTL3-dependent m6A modification of MYC mRNA drives glioblastoma resistance to temozolomide. *Cancer Cell*, *41*(7), 1314-1328.e8. https://doi.org/10.1016/j.ccell.2023.06.005

### Reporting checklist example: ARRIVE 2.0 essentials

The ARRIVE 2.0 essential items (animal research) are 21 items covering: study design, sample size, inclusion/exclusion criteria, randomization, blinding, statistical methods, experimental animals, experimental procedures, results (numbers analyzed, summary, adverse events), and interpretation. The 10 "Recommended" items add granularity. The checklist is filled out at manuscript draft time and submitted as a supplemental file. Most Nature-family, PLOS, eLife, and Cell-family journals require it for animal studies.

### Reporting checklist example: CONSORT 2010 essentials

CONSORT 2010 has 25 items covering: title/abstract (randomized trial identified), introduction (trial design, objectives, hypotheses), methods (trial design, participants, interventions, outcomes, sample size, randomization, blinding, statistical methods), results (participant flow, recruitment, baseline data, numbers analyzed, outcomes, ancillary analyses, harms), discussion (limitations, generalizability, interpretation), and other (registration, protocol, funding). A CONSORT flow diagram (Figure 1) is required and shows the flow of participants through enrollment, allocation, follow-up, and analysis.

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| Title is a question | Top-tier journals rarely accept question-mark titles | Convert to declarative: "X causes Y in Z" |
| Methods before reporting checklist | Methods section is missing required items (e.g., randomization method for trials) | Fill out the matching checklist first; let it drive the Methods draft |
| Discussion has no Limitations paragraph | Reviewers interpret silence as concealment | End with explicit, specific limitations and how they constrain the claim |
| Results repeat Methods | "We performed Western blot..." belongs in Methods, not Results | Methods says what was done; Results says what was found |
| Discussion over-claims the mechanism | A correlation becomes "we have shown that X drives Y" | Use hedging language: "is consistent with," "supports the hypothesis that," "suggests a role for" |
| Citation style wrong for the target journal | Desk-rejection | Always read the journal's reference style guide before submission |
| Figures built before the manuscript is drafted | Figures show uncalibrated analyses, not the claim | Lock the figure set after the Results section is drafted |
| Abstract says "we will discuss" | Submission of a manuscript that has not been written | Draft the abstract last, when the manuscript is finished |
| Vancouver with author-date et al. rules | Wrong abbreviation rules (e.g., "et al." vs. ", et al.") | Re-read ICMJE reference sample 1 and 37 |
| No reporting checklist submitted | Editorial return; "your manuscript does not comply with our reporting policy" | Use the journal's checklist template; submit as supplemental file |

## Validation

A manuscript draft passes structural validation when:

- The reporting checklist for the study design is fully completed and saved as a supplemental file.
- The title reflects the main finding, not the topic area.
- The abstract format matches the journal's required format (unstructured or structured, correct word count).
- The Results section has one claim per subsection, each backed by a figure or table.
- The Discussion follows the four-move structure (main finding, prior work, mechanism, limitations).
- The reference list uses the journal's required citation style.
- The figure count is within the journal's cap (often 4-5 main figures for top-tier journals).
- All acronyms are defined at first use; the list of abbreviations is consistent.
- Author contributions follow ICMJE's four-criterion definition.
- The data-availability statement matches the data sharing policy of the journal.

## Open alternatives

For commercial reference managers, the open-source alternatives are:

| Commercial | Open alternative | Trade-off |
|-----------|-----------------|-----------|
| EndNote | Zotero + Better BibTeX, JabRef | Zotero is free; EndNote has deeper journal style integration |
| Mendeley | Zotero, Paperpile (open-source core) | Mendeley has Elsevier ownership concerns for some users |
| ReadCube Papers | Zotero + PDF reader plugin | No meaningful functionality gap for most workflows |
| SciWheel | Zotero | SciWheel has nicer collaboration UI; Zotero has stronger standards support |

For commercial writing tools, the open alternatives are:

| Commercial | Open alternative |
|-----------|-----------------|
| Grammarly | LanguageTool (open-core), write-good (linter) |
| Scrivener | pandoc + Markdown (no GUI), Joplin |
| PerfectIt | textract + custom rules, Vale (prose linter) |

## References

- ICMJE Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals. icmje.org/icmje-recommendations.pdf
- CONSORT 2010 Statement and extensions. consort-statement.org
- STROBE Statement. strobe-statement.org
- PRISMA 2020 Statement. prisma-statement.org
- ARRIVE 2.0 Guidelines. arriveguidelines.org
- MIAME standard for microarray data. fg.ed.ac.uk/miame
- MINSEQE standard for sequencing-based expression studies. fg.edu.au/MINSEQE
- STARD 2015 (diagnostic accuracy). stard-statement.org
- CARE 2017 (case reports). care-statement.org
- TRIPOD (prediction models). tripod-statement.org
- Author guidelines for Nature, Science, Cell, NEJM, Lancet, JAMA, BMJ, eLife, PLOS — searchable via each journal's "For Authors" page.

## Related Skills

- ors-scientific-writing-cover-letter — for the cover letter that accompanies a manuscript built with this structure.
- ors-scientific-writing-rebuttal-letter — for the rebuttal letter after peer review.
- ors-scientific-writing-response-to-reviewers — for the point-by-point response document.
- ors-scientific-writing-ai-disclosure-writing — for the AI/LLM usage statement required by most journals.
- ors-scientific-communication-comm-press-release — for the public-facing version of the published result.
- ors-ethics-compliance-icmje-authorship — for ICMJE authorship criteria applied to the author list.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Consolidated public IMRAD guidance, journal-specific title and abstract strategies, figure/table selection logic, and reporting-checklist pointers (CONSORT, STROBE, PRISMA, ARRIVE 2.0, MIAME, MINSEQE). All sources are publicly accessible and verifiable; no specific journal policies are quoted verbatim.