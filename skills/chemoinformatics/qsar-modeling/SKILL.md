---

name: qsar-modeling
description: "Builds QSAR / QSPR models using chemprop D-MPNN, MolFormer, Uni-Mol, ChemBERTa, random forest baselines, and Gaussian processes with explicit handling of OECD 5 principles, applicability domain (kNN, leverage, conformal prediction, Mahalanobis), scaffold-balanced splits, ensemble uncertainty, calibration (Platt, isotonic), feature importance (SHAP, atomic attribution), and prospective validation. Use when building target-specific predictive models from in-house bioassay data, ADMET endpoints, or selectivity profiles."
license: MIT
---
<!-- metadata:
  category: chemoinformatics
  oversight: low
  version: 1.0.0
  author: Pradyumna Jayaram
  tags: [chemoinformatics, research]
  difficulty: intermediate
-->

## Version Compatibility

Reference examples tested with: chemprop 2.0+ (major API change from 1.x), RDKit 2024.09+, scikit-learn 1.4+, MAPIE 0.8+ (conformal prediction), shap 0.44+, pytorch 2.1+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` to check signatures
- CLI: `chemprop train --help`

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# QSAR Modeling

## Hard rules

1. **No fabricated citations.** Every cited work must resolve to a verifiable
2. **No claim without provenance.** Every quantitative or factual claim
3. **No silent failure.** Every script invocation, API call, or tool use must declare its exit status and what to do on non-zero. A skill that silently swallows errors is a violation.

## When to use

Load this skill when the user asks a question that matches its declared
trigger conditions (see the frontmatter `description` for the most common
ones). Do not load it for questions outside its scope — defer to the
appropriate ORS skill instead.

## When NOT to use

Do not load this skill if the question is in a sibling skill's domain
(see `## Cross-references`), if the user explicitly asks for a different
tool, or if the task is outside the skill's declared category.

## Model Taxonomy

| Model | Architecture | Use case | Fails when |
|-------|--------------|----------|------------|
| Random Forest + ECFP4 | Classical baseline | Small data (<200 compounds) | Saturates at ~AUC 0.85 |
| chemprop D-MPNN | Directed message passing | Modern default; 100-10k compounds | Very small datasets (<100) |
| MolFormer | Transformer (87M params) | Large public data | Compute overhead |
| Uni-Mol | 3D-aware transformer | 3D-relevant endpoints | Requires 3D conformers |
| Gaussian Process + ECFP4 | Probabilistic | Active learning | O(N^3) scaling |

**Decision:** For 200-10k compounds, **chemprop 2.0 D-MPNN** is the modern standard. For <200 compounds, **Random Forest + ECFP4** is competitive.

## chemprop 2.0 Training (CLI)

**Goal:** Train a chemprop D-MPNN ensemble with scaffold-balanced split.

```bash
chemprop train \
    --data-path data.csv \
    --task-type classification \
    --save-dir model_dir \
    --molecule-featurizers rdkit_2d_normalized \
    --num-folds 5 \
    --ensemble-size 5 \
    --epochs 50 \
    --batch-size 128 \
    --split scaffold_balanced \
    --split-sizes 0.8 0.1 0.1
```

## OECD 5 Principles

1. **Defined endpoint**: specific bioassay, units, threshold definitions
2. **Unambiguous algorithm**: reproducible code, fixed seeds
3. **Defined applicability domain (AD)**: where the model is valid
4. **Appropriate statistical validation**: external test set, cross-validation
5. **Mechanistic interpretation**: biological/chemical rationale

## Applicability Domain Methods

| Method | Definition | Pro |
|--------|-----------|-----|
| Ensemble variance | Std across N-model predictions | Built-in to chemprop |
| kNN distance | Mean Tanimoto to k nearest in training | Easy to interpret |
| Leverage | Hat matrix diagonal | Statistical |

**Operational rule:** Set `--ensemble-size 5` at training; at predict time, flag predictions with ensemble std > P95 as out-of-AD.

## References

- Yang et al., *J. Chem. Inf. Model.* 59:3370 -- chemprop scaffold split.
- OECD -- QSAR validation principles.

## Related Skills

- chemoinformatics/molecular-descriptors - Features
- chemoinformatics/molecular-standardization - Critical upstream
- chemoinformatics/admet-prediction - ADMET QSAR"

## Cross-references

Other skills in this category:

- admet-prediction
- conformer-generation
- covalent-design
- docking-rescoring
- free-energy-calculations
- generative-design
- molecular-descriptors
- molecular-io
- molecular-standardization
- pharmacophore-modeling
- pose-validation
- protac-degraders
- retrosynthesis
- scaffold-analysis
- shape-similarity
- similarity-searching
- substructure-search
- virtual-screening

## Changelog

- **1.1.0** (migration) — Bulk-migrated to v0.4.0 schema: canonical
  metadata block, base Hard rules, Cross-references. Body content
  unchanged; author should review and fill in any domain-specific
  extensions to the Hard rules.
- **1.0.0** — Initial release.

