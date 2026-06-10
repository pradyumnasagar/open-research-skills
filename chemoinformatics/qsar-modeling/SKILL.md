---
name: ors-chemoinformatics-qsar-modeling
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
description: Builds QSAR / QSPR models using chemprop D-MPNN, MolFormer, Uni-Mol, ChemBERTa, random forest baselines, and Gaussian processes with explicit handling of OECD 5 principles, applicability domain (kNN, leverage, conformal prediction, Mahalanobis), scaffold-balanced splits, ensemble uncertainty, calibration (Platt, isotonic), feature importance (SHAP, atomic attribution), and prospective validation. Use when building target-specific predictive models from in-house bioassay data, ADMET endpoints, or selectivity profiles.
tool_type: python
primary_tool: chemprop
sources_consulted:
  - bioSkills-main/chemoinformatics/qsar-modeling/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/chemprop-d-mpnn/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/chemberta/SKILL.md
---

## Version Compatibility

Reference examples tested with: chemprop 2.0+ (major API change from 1.x), RDKit 2024.09+, scikit-learn 1.4+, MAPIE 0.8+ (conformal prediction), shap 0.44+, pytorch 2.1+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` to check signatures
- CLI: `chemprop train --help`

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# QSAR Modeling

Build quantitative structure-activity relationship models from molecular structure inputs. The choice of model + featurization + split strategy determines whether the model captures real chemical signal or memorizes the training data. chemprop D-MPNN is the modern open-source standard; transformer-based methods (MolFormer, Uni-Mol) compete on benchmarks. The OECD 5 principles structure the model for regulatory acceptance.

For descriptor/fingerprint choices, see `chemoinformatics/molecular-descriptors`. For ADMET-specific QSAR, see `chemoinformatics/admet-prediction`.

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
- chemoinformatics/admet-prediction - ADMET QSAR