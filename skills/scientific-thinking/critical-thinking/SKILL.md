---

name: critical-thinking
description: "Evaluate scientific claims and evidence quality. Use for assessing experimental design validity, identifying biases and confounders, applying evidence grading frameworks (GRADE, Cochrane ROB), or teaching critical analysis."
license: MIT
---




<!-- metadata:
category: scientific-thinking
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - scientific-thinking
  - research
difficulty: intermediate
-->

# Scientific Critical Thinking

> Critical thinking in science is the systematic evaluation of evidence quality, methodological rigor, and logical validity. It's not about being contrarian—it's about being appropriately skeptical, recognizing the difference between strong and weak evidence, and understanding what conclusions are actually supported by the data. This skill provides frameworks for evaluating research claims, identifying biases, and applying evidence grading systems used in evidence-based medicine and meta-research.

## When to use

- Reviewing a research paper or manuscript for methodological quality
- Evaluating the strength of evidence for a clinical or policy decision
- Assessing whether a study's conclusions are supported by its data
- Identifying potential biases, confounders, or methodological flaws
- Applying GRADE or Cochrane Risk of Bias assessments
- Teaching critical analysis skills to students or trainees
- Evaluating media reports of scientific findings
- Conducting or peer-reviewing systematic reviews

## When NOT to use

- For generating new research ideas (use ors-scientific-thinking-brainstorming)
- For developing testable hypotheses (use ors-scientific-thinking-hypothesis-generation)
- For statistical analysis of your own data (use domain-specific analysis skills)
- For writing a peer review (use ors-scientific-writing-peer-review)
- For general fact-checking or debunking misinformation (different scope)

## Prerequisites

- Basic understanding of study designs (RCT, cohort, case-control, cross-sectional)
- Familiarity with statistical concepts (p-values, confidence intervals, effect sizes)
- Knowledge of your specific research domain
- Willingness to challenge claims, including your own prior beliefs
- Access to the study or report being evaluated

## Core workflow

### 1. Identify the claim and its strength

Begin by clearly stating what is being claimed:

- **Type of claim:** Causal? Associational? Descriptive? Predictive?
- **Strength of claim:** Proven? Likely? Suggested? Possible?
- **Scope:** General population? Specific subgroup? Specific conditions?
- **Quote the claim** exactly as stated (avoid paraphrasing)

### 2. Assess study design and methodology

Evaluate whether the design can support the claim:

**Design hierarchy for intervention questions:**
- Systematic reviews/meta-analyses of RCTs (highest)
- Randomized controlled trials
- Cohort studies
- Case-control studies
- Cross-sectional studies
- Case series/reports
- Expert opinion (lowest)

**Important:** Higher-level designs aren't always higher quality. A well-conducted observational study can be stronger than a poorly-conducted RCT.

**For causal claims specifically:**
- Can the design support causal inference? (RCT > quasi-experimental > observational)
- Are there credible alternative explanations?
- Is temporality established? (cause precedes effect)

### 3. Evaluate internal validity

Can we trust the causal inference within this study?

**Check for:**
- **Randomization quality** (sequence generation, allocation concealment)
- **Blinding** (participants, providers, outcome assessors)
- **Control groups** (appropriate? active control vs. placebo vs. no treatment?)
- **Baseline comparability** (are groups similar at start?)
- **Attrition patterns** (differential dropout? intention-to-treat analysis?)
- **Adherence and protocol deviations**

### 4. Assess external validity

Do results generalize beyond the study sample?

**Consider:**
- **Sample representativeness** (who was included vs. excluded?)
- **Setting** (academic medical center vs. community? single site vs. multi-site?)
- **Conditions** (do they match the target application?)
- **Population characteristics** (age, sex, comorbidities, severity)
- **Temporal context** (when was the study done? still relevant?)

### 5. Screen for biases

Systematically check for common sources of bias:

**Selection biases:**
- Sampling bias (non-representative sample)
- Volunteer bias (self-selection)
- Attrition bias (differential dropout)"
- Survivorship bias (only "survivors" visible)
- Referral bias (clinic-based recruitment)

**Measurement biases:**
- Observer bias (expectations influence observations)
- Recall bias (retrospective reports systematically inaccurate)
- Social desirability bias (responses biased toward acceptability)
- Instrument bias (measurement tool systematically errs)
- Misclassification bias (exposure or outcome misclassified)

**Analysis biases:**
- **P-hacking:** Multiple analyses conducted until significance emerges
- **HARKing:** Hypotheses stated after seeing results (Hypothesizing After Results are Known)
- **Garden of forking paths:** Multiple analysis choices, only significant ones reported
- **Cherry-picking:** Selective reporting of outcomes or analyses
- **Outcome switching:** Non-significant outcomes replaced with significant ones
- **Subgroup fishing:** Subgroup analyses without correction for multiple testing

**Publication and reporting biases:**
- Publication bias (negative results less likely published)
- Time-lag bias (positive results published faster)
- Language bias (English-language journals over-represented)
- Citation bias (positive results cited more)

**Check for preregistration:** Did the authors register hypotheses and analysis plans before data collection? Compare registered vs. reported outcomes.

### 6. Evaluate statistical analysis

Assess the statistical methods and reporting:

**Sample size and power:**
- Was a priori power analysis conducted?
- Is sample adequate for detecting meaningful effects?
- Is the study underpowered (common problem)?
- Do significant results from small samples raise flags for inflated effect sizes?

**Statistical tests:**
- Are tests appropriate for data type and distribution?
- Were test assumptions checked and met?
- Are parametric tests justified, or should non-parametric alternatives be used?
- Is the analysis matched to study design (paired vs. independent)?

**Multiple comparisons:**
- Were multiple hypotheses tested?
- Was correction applied (Bonferroni, FDR, Holm, etc.)?
- Are primary outcomes distinguished from secondary/exploratory?
- Could findings be false positives from multiple testing?

**P-value interpretation:**
- Are p-values interpreted correctly (probability of data if null is true)?
- Is non-significance incorrectly interpreted as "no effect"?
- Is statistical significance conflated with practical importance?
- Are exact p-values reported, or only "p < .05"?
- Is there suspicious clustering just below .05 (p-hacking indicator)?

**Effect sizes and confidence intervals:**
- Are effect sizes reported alongside significance?
- Are confidence intervals provided to show precision?
- Is the effect size meaningful in practical terms?
- Are standardized effect sizes interpreted with field-specific context?

**Missing data:**
- How much data is missing?
- Is missing data mechanism considered (MCAR, MAR, MNAR)?
- How is missing data handled (deletion, imputation, maximum likelihood)?
- Could missing data bias results?

### 7. Apply evidence grading frameworks

For clinical or policy questions, use systematic grading:

**GRADE approach (for intervention questions):**

Start with study design:
- RCT = high quality (initially)
- Observational = low quality (initially)

**Downgrade for:**
- Risk of bias (serious limitations)
- Inconsistency across studies
- Indirectness (wrong population/intervention/outcome)
- Imprecision (wide confidence intervals, small samples)
- Publication bias (funnel plot asymmetry, etc.)

**Upgrade for (observational studies):**
- Large effect sizes
- Dose-response relationships
- Confounders would reduce (not increase) effect

**Final GRADE ratings:** High, Moderate, Low, Very Low

**Cochrane Risk of Bias tools:**

- **RoB 2** for randomized controlled trials
  - Domains: randomization process, deviations from intended interventions, missing outcome data, measurement of outcome, selection of reported result
  - Judgments: Low risk, Some concerns, High risk

- **ROBINS-I** for non-randomized studies
  - Domains: confounding, selection of participants, classification of interventions, deviations from intended interventions, missing data, measurement of outcomes, selection of reported result
  - Judgments: Low, Moderate, Serious, Critical risk of bias, No information

### 8. Consider Bradford Hill criteria (for causation)

When evaluating causal claims from observational evidence, apply Bradford Hill's nine criteria:

1. **Strength of association** (large effect size)
2. **Consistency** (replicated by different researchers/populations)
3. **Specificity** (specific cause → specific effect)
4. **Temporality** (cause precedes effect)
5. **Biological gradient** (dose-response relationship)
6. **Plausibility** (mechanistically reasonable)
7. **Coherence** (fits with known facts)
8. **Experiment** (experimental evidence supports)
9. **Analogy** (similar cause-effect relationships known)

**Important:** These are not rigid requirements—none is necessary or sufficient individually. They provide a framework for weighing evidence.

### 9. Check for logical fallacies

Identify reasoning errors in scientific arguments:

**Causation fallacies:**
- Post hoc ergo propter hoc ("B followed A, so A caused B")
- Correlation = causation
- Reverse causation
- Single cause fallacy

**Generalization fallacies:**
- Hasty generalization (broad conclusions from small samples)
- Anecdotal fallacy
- Cherry-picking
- Ecological fallacy (group patterns applied to individuals)

**Statistical fallacies:**
- Base rate neglect
- Texas sharpshooter (finding patterns in noise)
- Multiple comparisons without correction
- Prosecutor's fallacy (confusing P(E|H) with P(H|E))
- Simpson's paradox (confounding by subgroups)

**Science-specific fallacies:**
- Galileo gambit ("They laughed at Galileo, so my fringe idea is correct")
- Argument from ignorance ("Not proven false, so true")
- Nirvana fallacy (rejecting imperfect solutions)
- Unfalsifiability (making untestable claims)

### 10. Synthesize and provide structured feedback

Organize your evaluation:

**Structure:**
1. **Summary:** Brief overview of what was evaluated
2. **Strengths:** What was done well (important for credibility and learning)
3. **Concerns:** Issues organized by severity
   - Critical issues (threaten validity of main conclusions)
   - Important issues (affect interpretation but not fatally)
   - Minor issues (worth noting but don't change conclusions)
4. **Specific recommendations:** Actionable suggestions for improvement
5. **Overall assessment:** Balanced conclusion about evidence quality

**Be:**
- **Constructive:** Identify strengths as well as weaknesses
- **Specific:** Point to specific instances (table numbers, section titles)
- **Proportionate:** Match criticism severity to issue importance
- **Consistent:** Apply same criteria across all studies
- **Contextual:** Acknowledge practical and ethical constraints

## Code patterns

### GRADE evidence profile template

```
Question: Does [intervention] improve [outcome] in [population]?

Study Design: [RCTs, observational, etc.]
Number of Studies: [N]
Number of Participants: [N]

Quality Assessment:
- Risk of Bias: [Serious / Not serious]
- Inconsistency: [Serious / Not serious]
- Indirectness: [Serious / Not serious]
- Imprecision: [Serious / Not serious]
- Publication Bias: [Serious / Not serious]

Effect Size: [RR, OR, MD with 95% CI]
Dose-Response: [Yes / No]
Confounders: [Would reduce / Increase / Unclear effect]

GRADE Rating: [High / Moderate / Low / Very Low]
Conclusion: [Brief statement of evidence quality and direction]
```

### Risk of Bias assessment checklist (RoB 2)

```
Study: [Author, Year]

Domain 1: Randomization process
- Was allocation sequence random? [Yes / No / Unclear]
- Was allocation concealed? [Yes / No / Unclear]
- Were baseline differences suggesting problem? [Yes / No / Unclear]
Judgment: [Low / Some concerns / High]

Domain 2: Deviations from intended interventions
- Were participants aware of assignment? [Yes / No / Unclear]
- Were carers aware of assignment? [Yes / No / Unclear]
- Were deviations balanced? [Yes / No / Unclear]
Judgment: [Low / Some concerns / High]

[Continue for all 5 domains]

Overall Risk of Bias: [Low / Some concerns / High]
```

### Common p-hacking indicators

- Cluster of p-values just below 0.05 (p-curve analysis)
- Unusual ratio of significant to non-significant results
- Vague or flexible analysis descriptions
- No preregistration or analysis plan
- Selective reporting of outcomes
- Many "exploratory" analyses in confirmatory context

## Common pitfalls

- **Confirmation bias:** Accepting evidence that confirms your beliefs, rejecting disconfirming evidence
- **Authority bias:** Accepting claims from prestigious researchers/journals without scrutiny
- **Novelty bias:** Overvaluing new or surprising findings
- **Hype cycle:** Believing press releases about breakthrough discoveries
- **Ignoring context:** Judging studies without considering field-specific norms
- **Methodolatry:** Worshiping methods over substance (e.g., "it's an RCT so it must be right")
- **False balance:** Treating fringe views and established science as equally credible
- **Over-criticism:** Being so skeptical that you reject all evidence, including strong evidence
- **Missing the forest for the trees:** Focusing on minor flaws while missing major issues

## Validation

How to know your critical evaluation was thorough:

- You've systematically checked all major bias categories
- You've applied appropriate evidence grading frameworks
- You've identified both strengths and weaknesses
- Your feedback is specific and actionable
- You've considered context and feasibility constraints
- You've distinguished fatal flaws from minor limitations
- You've assessed whether conclusions are proportional to evidence
- Your evaluation is balanced and proportionate to issue severity

## Open alternatives

All major evidence grading frameworks referenced (GRADE, Cochrane RoB 2, ROBINS-I, Newcastle-Ottawa Scale, AMSTAR) are freely available open-access tools. Training materials are available at training.cochrane.org and gradeworkinggroup.org.

## References

- **Related ors-* skills:**
  - ors-scientific-thinking-brainstorming (for generating ideas)
  - ors-scientific-thinking-hypothesis-generation (for developing hypotheses)
  - ors-scientific-thinking-failure-handling (for handling negative results)
  - ors-scientific-writing-peer-review (for writing peer reviews)

- **External resources:**
  - GRADE Working Group (gradeworkinggroup.org)
  - Cochrane Training (training.cochrane.org)
  - STROBE Statement (strobe-statement.org)
  - CONSORT Statement (consort-statement.org)
  - PRISMA Statement (prisma-statement.org)
  - EQUATOR Network (equator-network.org) - reporting guidelines
  - Reproducibility Project: Cancer (osf.io/reproducibility)
  - Meta-Research Center (metaresearch.org)

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram, integrating GRADE methodology, Cochrane Risk of Bias tools, Bradford Hill criteria, and established frameworks for bias detection and evidence evaluation in scientific research.