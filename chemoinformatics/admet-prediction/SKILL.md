---
name: ors-chemoinformatics-admet-prediction
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
description: Predicts ADMET properties using ADMETlab 3.0 (119 endpoints with uncertainty), ADMET-AI, DeepChem MolNet, and chemprop D-MPNN with explicit handling of OECD QSAR principles, applicability domain assessment, calibration, hERG/CYP/AMES gold-standard endpoints, and PAINS / Lipinski / Ro5 / Veber / BBB druglikeness filters. Use when filtering compounds for drug-likeness, prioritizing leads by predicted safety, or building an in-house ADMET QSAR model.
tool_type: python
primary_tool: ADMETlab
sources_consulted:
  - bioSkills-main/chemoinformatics/admet-prediction/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/admetlab/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/chemprop-d-mpnn/SKILL.md
---

## Version Compatibility

Reference examples tested with: RDKit 2024.09+, requests 2.31+, DeepChem 2.8+, chemprop 2.0+ (note major API change from 1.x), admet-ai 1.3+, pandas 2.2+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# ADMET Prediction

Predict absorption, distribution, metabolism, excretion, and toxicity properties of drug candidates. ADMET prediction underpins lead selection and de-risking; calibrated, applicability-domain-aware predictions distinguish a working filter from a costly false-confidence rejection. Modern best practice combines online services (ADMETlab 3.0 with uncertainty estimates), open-source models (chemprop D-MPNN), and rule-based filters (Lipinski / Veber / BBB heuristics) -- each with known failure modes.

For PAINS / Brenk / structural alerts, see `chemoinformatics/substructure-search`. For QSAR model building from in-house data, see `chemoinformatics/qsar-modeling`.

## ADMET Model Taxonomy

| Tool | Endpoints | Architecture | Uncertainty | Access | Fails when |
|------|-----------|--------------|-------------|-------------|---------|------------|
| ADMETlab 3.0 | 119 (A,D,M,E,T + physchem + medchem) | Multi-task DMPNN + descriptors | Per-prediction | REST API (free, no auth) | Outside training distribution; metals; macrocycles |
| ADMET-AI (NVIDIA) | ~50 (focus on safety) | chemprop D-MPNN | Ensemble variance | Python package | Limited endpoints vs ADMETlab |
| DeepChem MolNet | ~30 (tox21, ToxCast, ClinTox) | Various GCN/GAT | Per-task variance | Python package | Models trained on small datasets |
| pkCSM | ~30 | Graph signatures + RF | None | Web service | Smaller training data |
| SwissADME | ~30 (filters + physchem) | Hand-curated rules | None | Web service (NO API) | Cannot batch programmatically |
| ProTox-3.0 | ~46 (toxicity) | DT + descriptors | None | Web service | Toxicity only |
| chemprop (in-house) | User-defined | D-MPNN ± descriptors | Bayesian ensemble | Python package | Requires training data |

**Decision:** For batch screening of <10k compounds with no in-house data, **ADMETlab 3.0** (free API, 119 endpoints, calibrated uncertainty) is the modern standard. For in-house QSAR on a specific endpoint with >500 measurements, train a **chemprop D-MPNN**.

## ADMETlab 3.0 API

The current standard for free ADMET prediction. 119 endpoints across 6 categories; per-prediction uncertainty.

```python
import requests
import pandas as pd

def admetlab_predict(smiles_list, endpoint='admet'):
    url = f'https://admetlab3.scbdd.com/api/{endpoint}'
    payload = {'smiles': smiles_list}
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    return pd.DataFrame(response.json())

smiles = ['CCO', 'c1ccc(C(=O)O)cc1', 'CC(=O)Oc1ccccc1C(=O)O']
results = admetlab_predict(smiles)
```

ADMETlab endpoints: Absorption (Caco-2, HIA, Pgp), Distribution (BBB+, PPB, VDss), Metabolism (CYP1A2/2C9/2C19/2D6/3A4), Excretion (CL, T1/2), Toxicity (hERG, AMES, hepatotoxicity), Drug-likeness (Lipinski, Veber, QED).

## hERG Cardiotoxicity (Gold Standard Endpoint)

hERG blockade causes QT prolongation and is the #1 reason for late-stage drug attrition.

| Model | Training data | AUC | Reference |
|-------|--------------|-----|-----------|
| Cai et al. D-MPNN + MOE | 7,889 compounds | 0.956 | Liu 2024 |
| ADMETlab 3.0 hERG | Internal | 0.92 (reported) | Fu 2024 |
| ProTox-3.0 | ProTox training | 0.86 | Banerjee 2024 |

**Triangulation:** For hERG, use ADMETlab + ProTox + literature. A single-model probability > 0.5 is NOT a kill signal.

## Lipinski / Veber / Drug-Likeness Rules

| Rule | Constraints |
|------|--------------|
| Lipinski Ro5 | MW<=500, LogP<=5, HBD<=5, HBA<=10 |
| Veber | RotBonds<=10, TPSA<=140 |
| BBB+ Pfizer CNS | TPSA<=90, MW<=500, HBD<=3 |

```python
from rdkit.Chem import Descriptors, Lipinski, QED

def druglike_score(mol):
    return {
        'MW': Descriptors.MolWt(mol),
        'LogP': Descriptors.MolLogP(mol),
        'HBD': Lipinski.NumHDonors(mol),
        'HBA': Lipinski.NumHAcceptors(mol),
        'TPSA': Descriptors.TPSA(mol),
        'RotBonds': Lipinski.NumRotatableBonds(mol),
        'QED': round(QED.qed(mol), 2),
    }
```

## References

- Fu et al., *Nucleic Acids Res.* 52:W422 -- ADMETlab 3.0.
- Liu et al., 2024 -- hERG ML benchmarks.
- Lipinski et al., *Adv. Drug Deliv. Rev.* -- Rule of 5.
- Bickerton et al., *Nat. Chem.* 4:90 -- QED.

## Related Skills

- chemoinformatics/molecular-descriptors - Physicochemical descriptors
- chemoinformatics/substructure-search - PAINS / BRENK / REOS
- chemoinformatics/qsar-modeling - In-house ADMET model training