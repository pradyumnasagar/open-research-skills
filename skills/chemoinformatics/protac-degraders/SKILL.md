---
name: protac-degraders
description: "Designs PROTACs, molecular glues, and bivalent degraders with explicit"
license: MIT
---



<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: bioSkills-main/chemoinformatics/protac-degraders/SKILL.md; SciAgent-Skills-main/skills/structural-biology-drug-discovery/protac-rd/SKILL.md
-->

## Version Compatibility

Reference examples tested with: PRosettaC (web service), DeepTernary 1.0+, AlphaFold3 (constraints-enabled), Boltz-1 / Boltz-2, RDKit 2024.09+, OpenMM 8.1+ (for ternary MD).

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# PROTAC and Bivalent Degrader Design

Design bifunctional molecules (PROTACs) that recruit an E3 ubiquitin ligase to a target protein, inducing target ubiquitination and proteasomal degradation. PROTACs differ from traditional drugs: a stable **ternary complex** (target + PROTAC + E3) is required, not just target binding. The PROTAC field exploded post-2020 with clinical successes (ARV-471 estrogen-receptor degrader, ARV-110 androgen-receptor degrader). Postdoc-grade PROTAC design balances **target ligand binding**, **E3 ligand binding**, **linker geometry** (length, rigidity, chemistry), **cooperativity** (positive = ternary stable; negative = hook effect), and **cell permeability** (PROTACs are 800-1500 Da, often Lipinski-violating).

For target ligand design, see `chemoinformatics/virtual-screening` and `chemoinformatics/admet-prediction`. For linker-only enumeration, see `chemoinformatics/reaction-enumeration`. For generative linker design, see `chemoinformatics/generative-design`.

## E3 Ligase Choice

| E3 ligase | Ligand series | Best at | Limitations |
|-----------|---------------|---------|-------------|
| VHL | VL-269 | Surface-exposed targets | Tissue-restricted expression |
| CRBN (cereblon) | thalidomide, pomalidomide | Broad tissue expression | Off-target neosubstrates (IKZF1, SALL4) |
| IAP (XIAP, cIAP1) | SMAC mimetics (LCL161) | Apoptotic / IAP targets | Limited target scope |
| MDM2 | nutlin / idasanutlin | TP53 pathway | Limited target diversity |
| KEAP1 | DDB1-DCAF15-Keap1 | NRF2 pathway | Specialized use |
| RNF114 | EN450 | Newer; under exploration | Limited tooling |

**Decision:** For first-generation PROTAC, **CRBN (cereblon)** is the most-developed. **VHL** is second-most-developed (more selective; tissue-restricted).

## Linker Design Principles

| Property | Range | Effect |
|----------|-------|--------|
| Linker length | 8-30 atoms | Critical; geometry-dependent |
| Linker rigidity | Flexible (PEG) vs rigid (piperazine) | Higher rigidity reduces entropy penalty |
| Linker chemistry | PEG, alkyl, piperazine, triazole, ether, amide | PEG common; rigid for tighter binding |
| Click chemistry compatibility | Triazole compatible | Easy synthesis |
| MW range | PROTAC 800-1500 Da | Lipinski-violating but accepted |
| Polar atoms | 1-5 per linker | Permeability vs solubility balance |
"
**Critical:** "Goldilocks linker length" is target-specific. Too short = ternary clash; too long = ternary entropy too high. Typically 12-20 atoms for surface-exposed targets.

## Decision Tree by Scenario

| Goal | E3 / linker | Tools |
|------|-------------|-------|
| First-generation PROTAC, surface-exposed target | CRBN + PEG linker (10-15 atoms) | PRosettaC for ternary prediction |
| Selective degrader (avoid off-target) | VHL + rigid linker | PRosettaC + cellular validation |
| BTK / IAP family targets | IAP-based PROTAC | Standard pipelines |
| Novel target, no cryptic | Multiple E3 / linker variants | Combinatorial design + PRosettaC |
| Molecular glue (non-PROTAC) | CRBN-based | Distinct mechanism |

## Ternary Complex Prediction Tools

| Tool | Approach | Strength | Fails when |
|------|----------|----------|------------|
| PRosettaC | Rosetta-based protein-protein docking | Industry standard | Slow; needs crystal structures |
| DeepTernary | ML-based | Fast; no crystal required | Limited accuracy for new targets |
| AlphaFold3 (with constraints) | Foundation model | Excellent when co-crystal of binary available | API-restricted |
| Boltz-1 / Boltz-2 | Foundation model | Open source; multimer support | Larger than AF3 in some benchmarks |
| MOE | Commercial | GUI + scriptable | License cost |

```python
# Conceptual PRosettaC workflow
# prc -target target.pdb -e3 crbn.pdb -linker-protac protac.smi \
#     -output ternary.pdb
```

## Cooperativity (Alpha)

Cooperativity measures whether the PROTAC binds target+E3 more tightly than the sum of binary bindings:

```
alpha = Kd(binary) / Kd(ternary) * 1
```

| alpha | Interpretation | Action |
|-------|----------------|--------|
| > 10 | Strong cooperativity | Excellent candidate |
| 1-10 | Moderate | Iterative optimization |
| < 1 | Negative (anticooperative) | Re-design |

Cooperativity > 5 is desirable for cellular activity. Negative cooperativity suggests linker too long or attachment geometry wrong.

## DC50 / Dmax Characterization

- **DC50**: concentration for 50% target degradation
- **Dmax**: maximum degradation achievable (0-100%)
- **Hook effect**: PROTAC activity drops at high concentration (binary complexes dominate over ternary)

```python
# Cellular degradation assay (Western blot or reporter)
# Measure DC50 (e.g. 10 nM) and Dmax (e.g. 90% at 1 uM)
# If Dmax plateaus < 80% at high conc, check hook effect
```

## PROTAC Databases

| Database | URL | Compounds |
|----------|-----|-----------|
| PROTAC-DB | http://protacdb.weizmann.ac.il/ | ~5000 published PROTACs |
| EU-OPENSCREEN | Various | Curated |

## Per-Tool Failure Modes

### Hook effect at clinical dose

**Trigger:** Bell-shaped degradation curve in cellular assay.

**Mechanism:** At high PROTAC concentration, binary complexes dominate over ternary; productive degradation only happens at moderate concentration.

**Symptom:** Dmax falls at high PROTAC; therapeutic window narrow.

**Fix:** Reduce dose; or re-design linker to favor ternary.

### Negative cooperativity

**Trigger:** PROTAC binds target with similar Kd to parent ligand, but ternary unstable.

**Mechanism:** Linker geometry puts target and E3 in unfavorable orientation.

**Symptom:** Cellular degradation absent despite binary binding.

**Fix:** PRosettaC-driven linker re-design; consider rigid linker.

### Cellular permeability poor

**Trigger:** PROTAC active in lysate but not in cells.

**Mechanism:** MW > 1000 Da often violates cellular permeability rules.

**Symptom:** Cellular DC50 >> biochemical Kd.

**Fix:** Reduce MW; switch to rigid linker (smaller); use "PROTAC-to-drug" libraries optimized for permeability.

## References

- Békés et al. -- PROTAC review.
- Gadd et al. -- BRD4 degraders.
- Bondeson et al. -- CRBN-based PROTACs.

## Related Skills

- chemoinformatics/virtual-screening - Target ligand design
- chemoinformatics/retrosynthesis - Synthesizability
- chemoinformatics/generative-design - Generative linker design
- chemoinformatics/covalent-design - Covalent E3 ligands