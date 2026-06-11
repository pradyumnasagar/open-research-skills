---
name: systematic-review
description: "Conduct rigorous systematic reviews and meta-analyses following PRISMA 2020, including risk-of-bias assessment, heterogeneity analysis, publication bias evaluation, and evidence grading with GRADE."
license: MIT
---



<!-- metadata:
category: literature-research
version: 1.0.0
author: Pradyumna Jayaram
tags:
- meta-analysis
- prisma
- risk-of-bias
- heterogeneity
- publication-bias
- grade-evidence
difficulty: advanced
prerequisites:
  tools:
  - R (metafor
  - robvis
  - amr)
  - RevMan
  - Covidence/Rayyan
  - Cochrane RoB 2 tool
  skills:
  - ors-literature-research-literature-search
  - ors-literature-research-citation-management"
sources: "PRISMA 2020 Statement (prisma-statement.org); Adapted: Updated to PRISMA\
  \ 2020 27-item checklist; Cochrane Handbook for Systematic Reviews of Interventions,\
  \ Chapters 8–10 (training.cochrane.org/handbook); Adapted: Modern risk-of-bias\
  \ tools, metafor code examples; GRADE Handbook (gradeworkinggroup.org); Adapted:\
  \ GRADE for certainty of evidence assessment; ROBINS-I, RoB 2, AMSTAR 2 manuals\
  \ (riskofbias.info); Adapted: Implementation in R; Higgins & Green, Cochrane Handbook\
  \ of Research Synthesis; Adapted: Modern heterogeneity statistics"
-->

# Systematic Review and Meta-Analysis

> A systematic review is a research project itself: from a focused question through comprehensive search, critical appraisal, synthesis, and quality grading. This skill covers the full pipeline from eligibility screening through meta-analysis, with attention to modern computational tools, statistical heterogeneity assessment, and transparent reporting following PRISMA 2020.

## When to use

- Answering focused "does X work in population Y?" questions where primary studies exist but need synthesis
- Quantifying pooled effects for clinical guidelines, health policy, or regulatory submissions
- Identifying gaps in evidence through risk-of-bias patterns across studies
- Computing confidence intervals around effect sizes when individual studies are underpowered
- Assessing certainty of evidence using GRADE for outcomes important to decision-makers
- Producing a defensible, reproducible review that withstands peer scrutiny in Cochrane or journals like BMJ, Lancet, JAMA

## When NOT to use

- Mapping evidence landscape in a new field — use `ors-literature-research-scoping-review` instead
- When the question is exploratory or requires narrative synthesis — systematic reviews require sufficient primary studies
- For qualitative questions or realist synthesis — use qualitative synthesis methods instead
- When resources don't allow for dual screening and risk-of-bias assessment — consider a rapid review instead
- If no randomized trials exist and non-randomized studies need critical appraisal — requires special handling (ROBINS-I)

## Prerequisites

- A completed, documented literature search following PRISMA-S (`ors-literature-research-literature-search`)
- Two independent screeners for title/abstract and full-text screening
- A statistical package (R with `metafor`, `meta`, `robvis` packages; Python with `meta-analysis` libraries)
- A risk-of-bias tool: RoB 2 for RCTs, ROBINS-I for non-randomized, ROBIS for systematic reviews
- Reference manager set up with export capability (`ors-literature-research-citation-management`)
- PRISMA 2020 flow diagram template (available from prisma-statement.org)

## Core workflow

### 1. Prepare for screening

Export references from your citation manager as CSV/Excel. Create a screening database with columns:

```
id,source,title,year,abstract,review_topic,included_by,notes
```

Define eligibility criteria using a PICO framework and convert to a screening form. Use the PICO criteria to train any machine learning-assisted screening tools (ASReview, Covidence).

### 2. Dual screening process

Process references through two independent screeners:

1. **Title/abstract screening**: Exclude obviously irrelevant papers
2. **Full-text screening**: Obtain full texts of potentially relevant papers
3. **Discrepancy resolution**: Have a third screner resolve disagreements

For small reviews (<50 papers), single screening is acceptable but should be documented.

### 3. Data extraction

Extract data from included studies into a standardized format. Use tools like Covidence, Rayyan, or REDCap. Extract:

- Study characteristics: author, year, country, setting
- Participant details: sample size, demographics
- Intervention/exposure details: dosage, duration, control
- Outcomes: effect sizes, follow-up time, adverse events
- Risk-of-bias domains: sequence generation, blinding, etc.

### 4. Risk-of-bias assessment

Use appropriate tools based on study design:

- **RoB 2.0** for randomized trials (5 domains: randomization, deviations, missing data, measurement, reporting)
- **ROBINS-I** for non-randomized studies (7 domains: bias due to confounding, study participation, interventions, missing data, outcome measurement, selection of reported results, overall)
- **ROBIS** for systematic reviews (3 phases: study identification, study evaluation, appraisal of results)

Use `robvis` in R to visualize risk-of-bias across studies:

```r
# R code for RoB 2 visualization
library(robvis)
rob2_data <- read_csv("rob2_assessments.csv")
robvis(rob2_data, type="summary")
```

### 5. Meta-analysis preparation

Prepare effect size data for meta-analysis. Common effect measures:

- **Continuous outcomes**: mean differences (MD), standardized mean differences (SMD)
- **Dichotomous outcomes**: risk ratios (RR), odds ratios (OR), risk differences (RD)
- **Time-to-event**: hazard ratios (HR)

Convert all studies to a common metric using appropriate formulas. Handle missing data carefully:

```r
# R code for SMD calculation with metafor
library(metafor)
smd_data <- escalc(measure="SMD", 
                   m1i=mean_exp, sd1i=sd_exp, n1i=n_exp,
                   m2i=mean_ctrl, sd2i=sd_ctrl, n2i=n_ctrl,
                   data=dat)
```

### 6. Assess heterogeneity

Before pooling, assess statistical heterogeneity using:

- **I² statistic**: >75% = high heterogeneity
- **τ² (tau-squared)**: between-study variance
- **Cochran's Q**: significance test for heterogeneity

Choose between fixed-effect and random-effects models based on heterogeneity:

```r
# Fixed-effect model (homogeneous)
fe_model <- rma(yi, vi, data=smd_data, method="FE")

# Random-effects model (heterogeneous)
re_model <- rma(yi, vi, data=smd_data, method="REML")

# Test for heterogeneity
rma(yi, vi, data=smd_data, test="Q")
```

### 7. Conduct meta-analysis

Pool effect sizes using appropriate model:

```r
# Random-effects meta-analysis
meta_results <- rma(yi, vi, data=smd_data, method="REML")

# Generate forest plot
forest(meta_results, slab=dat$study, 
       transf=exp, # For OR/RR
       atransf=exp, 
       header="Study [Year]",
       ilab=c("Mean (SD)", "Mean (SD)", "SMD [95% CI]"),
       ilab.xpos=c(-3.5, -2, 1),
        main="Meta-analysis of intervention effects",
        xlab="Effect size (log scale)")
```

### 8. Evaluate publication bias

Assess publication bias using multiple approaches:

- **Funnel plot**: Visual asymmetry suggests bias
- **Egger's test**: Formal statistical test
- **Trim-and-fill**: Estimate and adjust for missing studies
- **Contour-enhanced funnel plot**: Distinguish bias from small-study effects

```r
# Publication bias assessment
funnel(meta_results, level=95, 
       yaxis="seinv", # 1/SE as y-axis
       xlab="Effect Size (log SMD)",
       ylab="1/Standard Error")

# Egger's test
regtest(meta_results, model="lm")

# Trim-and-fill
tf_results <- trimfill(meta_results)
```

### 9. Conduct sensitivity analyses

Test robustness of results:

- **Subgroup analysis**: By study quality, geography, intervention type
- **Meta-regression**: Explore sources of heterogeneity
- **Leave-one-out**: Remove one study at a time
- **Different models**: Fixed vs random effects, different estimators

```r
# Subgroup analysis
subgroup <- rma(yi, vi, data=smd_data, 
                mods=~design_factor, method="REML")

# Leave-one-out analysis
leave_one_out <- lapply(1:nrow(smd_data), function(i) {
  rma(yi[-i], vi[-i], data=smd_data[-i, ], method="REML")
})
```

### 10. Grade evidence quality

Use GRADE to rate certainty of evidence:

- **Risk of bias** across studies
- **Inconsistency** (heterogeneity)
- **Indirectness** (population/intervention/outcome)
- **Imprecision** (wide confidence intervals)
- **Publication bias** (small-study effects)

Rate each outcome as:
- High certainty
- Moderate certainty
- Low certainty
- Very low certainty

```r
# GRADE assessment example
grade_assessment <- data.frame(
  outcome = c("Mortality", "Pain reduction"),
  risk_of_bias = c("Serious", "Moderate"),
  inconsistency = c("Not serious", "Serious"),
  indirectness = c("Not serious", "Not serious"),
  imprecision = c("Not serious", "Serious"),
  publication_bias = c("Unknown", "Not serious"),
  certainty = c("Moderate", "Low")
)
```

### 11. Report with PRISMA 2020

Complete the 27-item PRISMA checklist:

1. Title (systematic review/meta-analysis)
2. Abstract (structured)
3. Introduction (rationale, objectives)
4. Methods (protocol registration, eligibility criteria)
5. Methods (information sources, search strategy)
6. Methods (selection process)
7. Methods (data collection process)
8. Methods (data items, critical appraisal)
9. Methods (synthesis methods)
10. Results (study selection flow)
11. Results (study characteristics)
12. Results (risk of bias)
13. Results (synthesis results)
14. Results (additional analyses)
15. Discussion (summary of evidence)
16. Discussion (strengths)
17. Discussion (limitations)
18. Discussion (implications)
19. Discussion (generalizability)
20. Other information (registration)
21. Other information (funding)
22. Other information (supplementary)
23. Other information (appendices)
24. Other information (competeting interests)
25. Other information (authors)
26. Other information (declaration)
27. Other information (availability)

## Code patterns

### Risk-of-bias assessment with robvis

```r
# Load required packages
library(robvis)
library(readxl)

# Read RoB 2 assessments
rob2_data <- read_excel("rob2_assessments.xlsx")

# View summary
robvis(rob2_data, type="summary")

# View individual study judgments
robvis(rob2_data, type="individual")

# Export for reporting
robvis(rob2_data, type="pdf", file="rob2_summary.pdf")
```

### Meta-analysis with metafor

```r
# Load package
library(metafor)

# Calculate effect sizes
dat <- escalc(measure="RR", 
              ai=events_exp, n1i=n_exp,
              bi=events_ctrl, n2i=n_ctrl,
              data=study_data)

# Random-effects meta-analysis
res <- rma(ai, bi, n1i, n2i, 
           measure="RR", 
           data=study_data, 
           method="REML",
           slab=study$author)

# Forest plot with risk of bias
forest(res, 
       header=c("Study", "Events/Total", "Risk Ratio [95% CI]"),
       ilab=c("Events/Exp", "Events/Ctrl"),
       ilab.xpos=c(-2.5, -1.5),
       textpos=c(1.5, 0.5),
       atransf=exp,
       at=log(c(0.1, 0.5, 1, 2, 10)),
       mablas=TRUE, # Mark studies with high risk of bias
       psize=1)
```

### Publication bias funnel plot with trim-and-fill

```r
# Funnel plot
funnel(res, 
        level=95,
        yaxis="seinv",
        xlab="Log Risk Ratio",
        ylab="1/SE",
        main="Funnel Plot with Trim and Fill")

# Test for funnel plot asymmetry
regtest(res, model="lm", predictor="seinv")

# Trim and fill analysis
tf <- trimfill(res)
funnel(tf, 
        level=95,
        yaxis="seinv",
        xlab="Log Risk Ratio",
        ylab="1/SE",
        main="Funnel Plot After Trim and Fill")
```

### Subgroup analysis and meta-regression

```r
# Subgroup by study quality
subgroup <- rma(yi, vi, 
                mods=~factor(study_quality, 
                           levels=c("High", "Moderate", "Low")),
                data=dat)

# Meta-regression by year
meta_reg <- rma(yi, vi, 
                mods=year, 
                data=dat)

# Predict and plot
newdat <- data.frame(year=seq(min(dat$year), max(dat$year), length=10))
pred <- predict(meta_reg, newdat=newdat)
newdat$pred <- pred$pred
newdat$ci_lb <- pred$ci.lb
newdat$ci_ub <- pred$ci.ub

plot(dat$year, dat$yi, xlab="Year", ylab="Effect Size",
     main="Meta-regression by Year")
lines(newdat$year, newdat$pred, col="red", lwd=2)
lines(newdat$year, newdat$ci_lb, col="red", lty=2)
lines(newdat$year, newdat$ci_ub, col="red", lty=2)
```

## Common pitfalls

- **Poorly defined eligibility criteria**: Vague criteria lead to inconsistent screening decisions
- **Single screening without verification**: Dual screening catches missed papers and reduces bias
- **Ignoring heterogeneity**: Meta-analysis with high I² without exploring sources is misleading
- **Publication bias not assessed**: Results may be overly optimistic without this check
- ** GRADE not applied**: Decision-makers need certainty ratings for each outcome
- **Small study effects not distinguished from bias**: Funnel plots need careful interpretation
- **Fixed-effect model when heterogeneity exists**: This underestimates uncertainty
- **Not reporting confidence intervals**: Effect sizes without intervals are hard to interpret
- **Inadequate sensitivity analysis**: Results should be robust to different analysis approaches
- **PRISMA checklist incomplete**: Missing items lead to reviewer requests and delays

## Validation

- **PRISMA 2020 flow diagram**: Shows screening and exclusion reasons clearly
- **Risk-of-bias summary**: Graphs showing distribution of judgments across studies
- **Heterogeneity statistics**: I², τ², and Q test reported appropriately
- **Publication bias assessment**: At least funnel plot and Egger's test
- **Sensitivity analyses**: Results are robust to different approaches
- **GRADE assessment**: Each outcome rated with clear justification
- **Forest plots**: Effect sizes with confidence intervals for all studies and pooled result
- **Supplementary material**: Full data extraction tables and risk-of-bias details

## Open alternatives

| Commercial / paid | Open alternative | Trade-off |
|---|---|---|
| RevMan 5 | R with metafor, meta packages | RevMan has user interface; R is more flexible but requires coding |
| Covidence screening platform | Rayyan (free tier), ASReview (ML-assisted) | Rayyan has free academic tier; ASReview automates screening with ML |
| GRADEpro (GRADE tool) | Manual assessment in Excel, R packages | GRADEpro guides through process but costs money; manual is free |
| Review Manager (RoB tools) | R with robvis, bias package | GUI vs code approach - code is reproducible but harder to learn |
| Cochrane's software suite | Open Meta-Analyst, R packages | Cochrane has integrated workflow; open tools are modular but more work |

## References

Internal skills:
- `ors-literature-research-literature-search` — systematic search strategy
- `ors-literature-research-citation-management` — reference management
- `ors-literature-research-scoping-review` — for broad landscape reviews
- `ors-open-science-preprints` — for posting protocols and preprints

External sources:
- PRISMA 2020 Statement — prisma-statement.org
- Cochrane Handbook for Systematic Reviews of Interventions — training.cochrane.org/handbook
- RoB 2 tool — riskofbias.info
- ROBINS-I — riskofbias.info
- GRADE Working Group — gradeworkinggroup.org
- Metafor R package — metafor-project.org
- Covidence platform — covidence.org
- Rayyan screening tool — rayyan.qcri.org
- ASReview — asreview.ai

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Updated from Bioinfoskill `meta-analysis` with PRISMA 2020, modern R code examples using metafor, expanded heterogeneity assessment, publication bias detection with trim-and-fill, and GRADE evidence grading.