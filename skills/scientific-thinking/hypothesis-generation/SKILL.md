---

name: hypothesis-generation
description: "Generate testable hypotheses from literature and observation. Use for converting research gaps, contradictory findings, cross-domain analogies, or clinical observations into falsifiable predictions for experimental design."
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

# Hypothesis Generation

> Hypothesis generation is the bridge between observation and experimentation. A good hypothesis transforms vague curiosity into a testable prediction, making explicit what you expect to happen, why, and under what conditions. This skill provides frameworks for converting research gaps, contradictory findings, and cross-domain insights into falsifiable statements that drive experimental design and scientific progress.

## When to use

- Identifying testable predictions from literature gaps or contradictions
- Converting brainstorming ideas into experimentally tractable questions
- Formulating hypotheses from clinical or observational patterns
- Developing grant-specific aims with clear predictions
- Designing experiments to distinguish between competing theories
- Applying cross-domain analogies to generate novel predictions
- Moving from exploratory analysis to confirmatory testing

## When NOT to use

- Early-stage exploration without clear direction (use brainstorming)
- Evaluating evidence quality of existing hypotheses (use critical thinking)
- Confirming established knowledge (that's verification, not hypothesis generation)
- When a phenomenon is already well-explained and no gap exists
- For purely descriptive research without predictive component

## Prerequisites

- Sufficient domain knowledge to understand the current state of research
- Familiarity with relevant literature and open questions
- Basic understanding of experimental design principles
- Access to data or observations to build upon
- Awareness of competing theories or explanations in the field

## Core workflow

### 1. Identify the hypothesis source

Determine where the hypothesis idea originates:

**Knowledge gaps in literature**
- What questions remain unanswered?
- What has been overlooked or insufficiently studied?
- What contradictions exist between studies?

**Contradictory findings**
- Studies that report opposing results
- Inconsistent effect sizes across populations
- Conflicting mechanistic explanations

**Cross-domain analogies**
- Insights from other fields that might apply
- Biological parallels to engineering solutions
- Methodological advances from adjacent areas

**Methodological advances**
- New techniques that enable previously impossible tests
- More precise measurements or manipulations
- Scale or resolution improvements

**Clinical or observational patterns**
- Unexpected observations in practice
- Patient/subject patterns noticed but unexplained
- Natural experiments or quasi-experiments

**Theoretical predictions**
- Predictions from models that need testing
- Implications of established theories
- Boundary conditions not yet explored

### 2. Specify the hypothesis anatomy

A well-formed hypothesis has five components:

**1. Variables**
- Independent variable (what you manipulate or vary)
- Dependent variable (what you measure)
- Control variables (what you hold constant)

**2. Directional prediction**
- What you expect to happen
- Specific direction (increase/decrease, positive/negative)
- Magnitude or effect size expectations

**3. Mechanism (if causal)**
- Why you expect this to happen
- Underlying causal chain
- Theoretical basis for the prediction

**4. Scope/conditions**
- When the hypothesis applies
- Boundary conditions
- Populations, settings, or contexts

**5. Operationalization**
- How each variable will be measured
- Cutoffs or thresholds for categorization
- Specific experimental protocols

**Template:**"
> "We hypothesize that [IV] will [directionally affect] [DV] in [population/samples], because [mechanism], and this will be measured by [operationalization]."

### 3. Apply the falsifiability test

Following Popper's criterion, a hypothesis must be falsifiable:

**Questions to ask:**
- Could the hypothesis be proven wrong by observation?
- Is there a conceivable result that would contradict it?
- Are the variables operacionais in a way that allows rejection?

**Types of unfalsifiable hypotheses to avoid:**
- No clear prediction (too vague)
- Invulnerable to disconfirmation (always interprets结果是"支持")
- Tautological (true by definition)
- Untestable with available methods

**Making hypotheses falsifiable:**
- Specify exact predictions, not just direction
- State magnitude expectations
- Define rejection criteria in advance
- Identify alternative explanations

### 4. Design a test

How would you test this hypothesis?

**Requirements:**
- An experiment or observation that could yield conflicting results
- A way to measure the dependent variable
- Appropriate controls
- Sufficient sample/power

**Design considerations:**
- What design can differentiate this from alternatives?
- What would confirm? What would falsify?
- What are plausible confounds?
- How will you handle ambiguity in results?

### 5. Specify alternatives and boundary conditions

A strong hypothesis acknowledges:

**Competing hypotheses**
- What else could explain the results?
- What are the leading alternatives?
- How does this hypothesis differ?

**Boundary conditions**
- When would you expect this not to hold?
- What are the limits of the prediction?
- What contextual factors matter?

**Effect size expectations**
- What magnitude of effect makes the hypothesis "true"?
- What magnitude suggests falsification?
- Is the effect clinically/practically significant?

## Code patterns

### Hypothesis specification template

```
HYPOTHESIS: [Number]

Variables:
- Independent variable: [precise definition]
- Dependent variable: [precise definition]
- Control variables: [list]

Prediction:
- We expect [IV] to [increase/decrease] [DV] by approximately [magnitude/percentage].

Mechanism:
- [IV] affects [DV] through [mechanism], based on [theory/prior work].

Scope:
- This prediction applies to [population/context].
- We expect this in [conditions], but not when [conditions].

Operationalization:
- [IV] will be operationalized as: [specific measurement]
- [DV] will be operationalized as: [specific measurement]

Rejection criteria:
- If [observed result], we reject the hypothesis.

Alternative explanations:
1. [Competing hypothesis 1]
2. [Competing hypothesis 2]
```

### Example: From gap to hypothesis

**Source:** Two studies on mitochondrial function in aging report conflicting results - one shows decline, one shows no change.

**Gap:** Why the inconsistency? One uses tissue homogenates, one uses single cells.

**Hypothesis Generation:**

```
HYPOTHESIS 1: Tissue-level measurements obscure cell-type heterogeneity
in mitochondrial function decline during aging.

Variables:
- Independent variable: Measurement scale (tissue homogenate vs. single cell)
- Dependent variable: Mitochondrial function (ATP production rate)
- Control variables: Age, species, tissue type

Prediction: Single-cell measurements will reveal significant
age-related decline that tissue homogenates obscure by averaging
across cell subpopulations with different function trajectories.

Mechanism: Cell-to-cell variation increases with age; averaging
masks decline in high-function cells by diluting with low-function cells.

Scope: Applicable to post-mitotic tissues (neurons, muscle).
Not applicable to proliferating tissues with ongoing stem cell input.

Rejection criteria: If single-cell measurements show no greater
age-related decline than tissue homogenates, reject hypothesis.
```

### Contradictory findings resolution framework

```
CONFLICT RESOLUTION: [Citation A] vs. [Citation B]

Both studies claim:
- Study A: [Claim]
- Study B: [Opposing claim]

Potential explanations:
1. Population differences (species, age, sex)
2. Methodological differences (assay, timing)
3. Context differences (in vivo vs. in vitro)
4. Statistical artifacts (power, analysis)

HYPOTHESIS to resolve:
We hypothesize that [variable X] explains the discrepancy,
specifically [prediction].
```

### From clinical observation to hypothesis

```
CLINICAL OBSERVATION:
[Describe unexpected pattern noticed in practice]

PATTERN TO EXPLAIN:
[What was observed]

LEADING HYPOTHESES:
1. [Potential explanation 1]
2. [Potential explanation 2]

HYPOTHESIS TO TEST:
We hypothesize that [specific mechanism], based on
[observations from basic science / analogous conditions].

Testable prediction:
[What would we expect to see if this is correct?]
```

## Common pitfalls

- **Vague predictions:** "X affects Y" is not a hypothesis; "X increases Y by 20-30%" is.
- **Unfalsifiable wording:** Avoid "may," "could," or "might" when making predictions.
- **Mechanical application:** Don't force every observation into hypothesis form when it's better described as an exploratory finding.
- **Missing mechanism:** Without a plausible mechanism, predictions are arbitrary.
- **Ignoring alternatives:** Strong hypotheses specify what's being distinguished from.
- **Unrealistic scope:** Start with narrowly testable hypotheses before combining.
- **Shoehorning:** Don't try to find evidence FOR your hypothesis; design tests that could falsify it.
- **Neglecting boundary conditions:** Specify when your hypothesis should NOT hold.

## Validation

How to know your hypothesis generation was successful:

- The hypothesis is stated as a specific, testable prediction
- Variables are clearly defined and operacionalized
- The hypothesis could be falsified by a plausible outcome
- There's a clear experimental design to test it
- Alternative explanations are acknowledged
- The scope and boundary conditions are specified
- The mechanism or theoretical basis is provided
- Effect size expectations are stated
- The hypothesis addresses a genuine gap or contradiction

## References

- **Related ors-* skills:**
  - ors-scientific-thinking-brainstorming (for initial exploration)
  - ors-scientific-thinking-critical-thinking (for evaluation)
  - ors-scientific-thinking-perspective-tour (for multi-perspective framing)
  - ors-scientific-thinking-failure-handling (if results are negative)
  - ors-research-grants-specific-aims (for hypothesis in grant context)

- **External resources:**
  - Popper, K.R.. The Logic of Scientific Discovery
  - Lakatos, I.. Falsification and the Methodology of Scientific Research Programmes
  - CONSORT Statement - hypothesis reporting in trials
  - STROBE Statement - hypothesis reporting in observational studies

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram, integrating Popper's falsifiability criterion, Lakatos's research programmes, and structured frameworks for converting knowledge gaps and contradictions into testable hypotheses.