---
name: failure-handling
description: "Handle negative results, failed experiments, preregistration violations, and replication failures. Use for reporting null findings, deciding when to revise vs. discard hypotheses, and connecting to preregistration and registered reports."
license: MIT
---



<!-- metadata:
category: scientific-thinking
version: 1.0.0
author: Pradyumna Jayaram
tags:
- negative-results
- replication
- preregistration
- hypothesis-revision
- scientific-integrity
difficulty: intermediate
prerequisites:
  tools: []
  skills:
  - ors-scientific-thinking-critical-thinking
  - ors-scientific-thinking-hypothesis-generation"
sources: "Lakatos, I.. Falsification and the Methodology of Scientific Research Programmes;\
  \ Open Science Collaboration. Estimating the reproducibility of psychological science.\
  \ Science 349; Nosek, B.A. et al.. Preregistration is hard, and worthwhile. Trends\
  \ in Cognitive Sciences; Munaf\xF2, M.R. et al.. A manifesto for reproducible science.\
  \ Nature Human Behaviour 1; Errington, T.M. et al.. Reproducibility in Cancer Biology:\
  \ Challenges for assessing replicability; Chambers, C.D. et al.. Registered Reports\
  \ - Realigning incentives in scientific publishing"
-->

# Failure Handling

> Failed experiments and negative results are not failures of science—they are the core of how science self-corrects. The skill is not in avoiding failure but in handling it well: distinguishing between a robust negative result and a failed experiment, knowing when to revise a hypothesis versus when to discard it, and reporting findings transparently so that other researchers can build on them. This skill provides frameworks for interpreting, reporting, and responding to results that didn't go as expected, with explicit connections to preregistration and registered reports.

## When to use

- An experiment produced null or unexpected results
- A preregistered hypothesis was not supported
- A replication attempt failed
- Results are ambiguous and need careful interpretation
- You're deciding whether to revise or abandon a hypothesis
- Writing up a "failure to replicate" or null result
- Responding to reviewer concerns about preregistration violations
- Designing follow-up studies after a negative finding

## When NOT to use

- You have a clear positive result (use domain-specific reporting skills)
- The "failure" is actually a methodological issue that invalidates the experiment (debug first)
- You're at the very start of hypothesis generation (use hypothesis generation)
- The result is interesting but exploratory (use exploration skills)
- You need a critique of someone else's work (use critical thinking)

## Prerequisites

- Pre-registered protocol or clear a priori plan (for proper interpretation)
- Documentation of methods, conditions, and data
- Understanding of the original hypothesis
- Access to the full dataset, not just summary statistics
- Statistical literacy to interpret results correctly
- Willingness to update beliefs in light of evidence

## Core workflow

### 1. Characterize the result

First, clearly characterize what happened:

**Type of result:**
- Null result (predicted effect absent)
- Opposite result (predicted direction reversed)
- Partial result (effect present but smaller/weaker)
- Unexpected additional finding
- Inconclusive (too noisy, underpowered, or ambiguous)

**Strength of evidence:**
- Pre-registered and well-powered
- Exploratory with appropriate caveats
- Underpowered and ambiguous
- Multiple replications attempted
- Single study with high uncertainty

**Distinguish:**
- A robust null result (well-powered, pre-registered, no effects found)
- A failed experiment (technical issues, confounders, inadequate design)
- An inconclusive result (insufficient data to evaluate)

### 2. Diagnose the discrepancy

If the result differs from prediction, consider systematically:

**Methodological explanations:**
- Power was insufficient to detect real effect
- Measurement was noisy or imprecise
- Operationalization missed the theoretical construct
- Sample characteristics differed from prior work
- Experimental conditions were not comparable

**Theoretical explanations:**
- The hypothesis is wrong in some specific
- Boundary conditions weren't met
- The mechanism doesn't operate as predicted
- The effect is real but smaller than hypothesized
- Conflicting factors masked the effect

**Sampling/population explanations:**
- Different populations respond differently
- Cohort effects (temporal changes)
- Selection effects in recruitment
- Population heterogeneity

**Chance explanations:**
- Type I error in original study
- Type II error in current study
- Random variation around true effect

### 3. Decide: revise, replicate, or abandon

Based on diagnosis, choose a path:

**Revise the hypothesis (keep but refine)**
- Core mechanism still plausible but specific prediction was off
- Boundary conditions were mis-specified
- Effect size was overestimated
- A more precise version is testable

**Replicate with corrections**
- Methodological issues in the original can be fixed
- Pre-register the replication with explicit plan
- Increase power or precision
- Test in a different sample/population

**Abandon the hypothesis**
- Strong, well-powered null result
- Theoretical basis is undermined
- Replications consistently fail
- Competing explanation better fits the data

**Publish the negative result**
- Pre-registered and well-powered
- Novel, important hypothesis tested
- Useful for meta-analysis and future research
- Counteracts publication bias

### 4. Write up transparently

Frame the report around what was expected, what was observed, and why:

**Structure:**
- Pre-registered hypothesis and prediction
- Methods (including any deviations from protocol)
- Results (clear, with effect sizes and confidence intervals)
- Possible explanations for discrepancy
- Implications for theory and future research

**Avoid:**
- HARKing (reframing as if you predicted the null)
- Hiding the failure (acknowledge it clearly)
- Overreaching (claiming more than the data support)
- Speculation as fact (clearly label as interpretation)

### 5. Update beliefs and plan next steps

After processing the result:

**Update your model of the world**
- What do you now believe?
- What's still uncertain?
- What would resolve the uncertainty?

**Plan next steps**
- Additional experiments to test revised hypothesis
- Pre-registration of follow-up
- Communication with collaborators and lab
- Possible collaborations with others

## Code patterns

### Negative result reporting template

```
TITLE: [Clear, descriptive title indicating null/negative finding]

ABSTRACT:
- Background: [What was expected based on prior work]
- Methods: [Study design, sample, key measures]
- Results: [Clear statement of what was found]
- Conclusions: [Implications and what this means]

INTRODUCTION:
- Prior evidence for hypothesis: [Summary]
- Theoretical basis: [Why this was expected]
- Aims: [Pre-registered prediction]

METHODS:
- Pre-registration: [OSF link, AsPredicted, etc.]
- Deviations from pre-registration: [List, with justification]
- Power analysis: [Effect size, alpha, power achieved]
- Sample: [Recruitment, exclusions, final N]

RESULTS:
- Primary outcome: [Effect size, 95% CI, p-value]
- Secondary outcomes: [Listed with effects]
- Sensitivity analyses: [What changes if assumptions vary]
- Exploratory analyses: [Clearly labeled]

DISCUSSION:
- Summary: [What was found]
- Possible explanations: [Listed systematically]
- Implications: [For theory, future research]
- Limitations: [Acknowledged honestly]
```

### Discrepancy diagnosis worksheet

```
ORIGINAL HYPOTHESIS: [Statement]

OBSERVED RESULT: [What actually happened]

SYSTEMATIC EXPLANATION CHECKLIST:

Methodological:
- [ ] Power adequate? [Yes/No; analysis]
- [ ] Measurement valid and reliable? [Notes]
- [ ] Operationalization matches theory? [Notes]
- [ ] Sample appropriate? [Notes]
- [ ] Conditions comparable to prior work? [Notes]

Theoretical:
- [ ] Mechanism still plausible? [Notes]
- [ ] Boundary conditions met? [Notes]
- [ ] Effect size realistic? [Notes]
- [ ] Conflicting factors plausible? [Notes]

Sampling/Population:
- [ ] Population similar to prior? [Notes]
- [ ] Cohort effects plausible? [Notes]
- [ ] Selection effects? [Notes]

Chance:
- [ ] Original study Type I error possible? [Notes]
- [ ] Current study Type II error possible? [Notes]
- [ ] Random variation plausible? [Notes]

MOST LIKELY EXPLANATION: [Based on weight of evidence]

ACTION: [Revise / Replicate / Abandon / Publish negative]
```

### Decision framework

```
IS THE NULL RESULT ROBUST?
    |
    +-- No (underpowered, exploratory)
    |   -> Replicate with corrections
    |   -> Pre-register the replication
    |
    +-- Yes (well-powered, pre-registered, well-conducted)
        |
        +-- Replications also null
        |   -> ABANDON hypothesis
        |   -> Publish negative result
        |
        +-- Mixed findings
            -> REVISE hypothesis
            -> Test refined version

IS THERE A PLAUSIBLE METHODOLOGICAL EXPLANATION?
    |
    +-- Yes
    |   -> REPLICATE with corrections
    |   -> Be explicit about what was fixed
    |
    +-- No clear methodological issue
        -> Consider theoretical revisions
        -> Test boundary conditions
```

### Failure-to-replicate paper structure

```
1. Introduction
   - Original finding and its impact
   - Why replication matters
   - Pre-registered replication plan

2. Methods
   - Pre-registration details
   - Sample, power, design
   - Deviations from pre-registration

3. Results
   - Primary outcome (with effect size and CI)
   - Comparison to original effect size
   - Equivalence/bayesian analysis if applicable

4. Discussion
   - Possible explanations for discrepancy
     (Methods, sample, context, theory)
   - Implications for original finding
   - What we can conclude
   - What remains uncertain

5. Conclusion
   - Clear statement of what was replicated
     and what was not
```

### Handling preregistration violations

```
DEVIATION: [Describe the deviation from pre-registration]

JUSTIFICATION: [Why this was necessary]

DISCOVERY: [When and how was this identified]

DOCUMENTATION:
- Pre-registration: [Link]
- Updated plan: [Link, if applicable]
- Date of deviation: [Date]

REPORTING:
- In paper, explicitly note the deviation
- Explain rationale
- Show both pre-registered and revised analyses if possible
- Discuss implications

LESSON LEARNED: [For future pre-registrations]
```

## Common pitfalls

- **Treating null as failure:** A pre-registered null result is a successful experiment, not a failure.
- **HARKing:** Reframing post-hoc to look like the null was predicted.
- **Hiding the deviation:** Not reporting deviations from pre-registration undermines credibility.
- **Abandoning too quickly:** A single null result may be a fluke or methodological issue.
- **Holding on too long:** Continuing to defend a hypothesis against strong contrary evidence.
- **Overinterpreting ambiguity:** Treating inconclusive results as definitive.
- **Confirmation bias in reverse:** Treating a single null as disproving well-established work.
- **Missing the opportunity:** Negative results are valuable; failing to publish them wastes information.
- **Blaming methodology:** Sometimes the hypothesis is wrong; check your priors.
- **Forgetting to update:** Beliefs should change with evidence; otherwise, why test?

## Validation

How to know failure handling was successful:

- The result is clearly characterized (null, partial, opposite, etc.)
- Multiple possible explanations were systematically considered
- A clear decision was made (revise, replicate, abandon, publish)
- The writeup is honest and transparent about what was expected vs. observed
- Pre-registration status and any deviations are clearly noted
- The implications for theory and future research are discussed
- The result is published or shared in a venue that handles negative results
- Your model of the world has been updated accordingly
- The negative result will be useful to other researchers

## Open alternatives

For publishing negative results, multiple open-access venues exist:
- PLOS ONE accepts well-conducted null findings
- BMC Research Notes
- Journal of Articles in Support of the Null Hypothesis
- F1000Research for rapid publication
- OSF Preprints for open sharing

For preregistration, free services include:
- OSF (Open Science Framework) Registries
- AsPredicted
- ClinicalTrials.gov for clinical trials

## References

- **Related ors-* skills:**
  - ors-scientific-thinking-critical-thinking (for evaluating evidence)
  - ors-scientific-thinking-hypothesis-generation (for revising hypotheses)
  - ors-scientific-thinking-brainstorming (for new directions)
  - ors-scientific-writing-peer-review (for reviewer responses)

- **External resources:**
  - Lakatos, I.. Falsification and the Methodology of Scientific Research Programmes
  - Open Science Collaboration. Estimating the reproducibility of psychological science. Science 349
  - Nosek, B.A. et al.. Preregistration is hard, and worthwhile. Trends in Cognitive Sciences
  - Munafò, M.R. et al.. A manifesto for reproducible science. Nature Human Behaviour 1
  - Errington, T.M. et al.. Reproducibility in Cancer Biology
  - Chambers, C.D. et al.. Registered Reports
  - OSF (osf.io) - preregistration platform
  - COS (cos.io) - Center for Open Science guidelines

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram, integrating frameworks for hypothesis revision from Lakatos, reproducibility findings from the Open Science Collaboration, and best practices for negative result reporting and preregistration.