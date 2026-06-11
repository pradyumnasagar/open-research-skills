---
name: chemoinformatics-retrosynthesis
description: "Performs retrosynthetic planning using AiZynthFinder (MCTS, template-based),
  Chemformer (template-free transformer), ASKCOS, and emerging RetroSynFormer with
  explicit handling of route scoring, building-block availability (eMolecules, Enamine,
  Mcule), forward prediction validation (Molecular Transformer), and disconnection-aware
  multi-objective search (MO-MCTS). Use when assessing synthetic feasibility of generated
  or selected molecules, planning multi-step syntheses, building synthesis-aware design
  pipelines, or screening libraries for retro-route feasibility.
license: MIT
---

<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: bioSkills-main/chemoinformatics/retrosynthesis/SKILL.md; SciAgent-Skills-main/skills/structural-biology-drug-discovery/aizynthfinder/SKILL.md
-->

## Version Compatibility

Reference examples tested with: AiZynthFinder 4.4+, Chemformer 1.3+, RDKit 2024.09+, RDChiral 1.1+, Aizynthtrain 1.0+, ASKCOS Lite 0.5+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures
- CLI: `aizynthcli --version`

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# Retrosynthesis

Plan synthetic routes from a target molecule back to commercially-available building blocks. AiZynthFinder 4.0 is the open-source production-grade tool: Monte Carlo Tree Search (MCTS) + template-based expansion + multi-objective scoring (MO-MCTS). Chemformer is the template-free transformer alternative. ASKCOS is the academic reference. Modern best practice combines retrosynthesis with **forward validation** (the predicted route should also predict the target from starting materials via Molecular Transformer) and building-block availability.

For generative design pipelines that need synthetic feasibility, see `chemoinformatics/generative-design`. For reaction enumeration (forward direction), see `chemoinformatics/reaction-enumeration`.

## Method Taxonomy

| Tool | Approach | Strength | Fails when |
|------|----------|----------|------------|
| AiZynthFinder 4.0 | Template-based MCTS | Open, scalable, well-validated | Beyond template coverage |
| Chemformer | Template-free transformer | Novel disconnections | Less interpretable |
| ASKCOS | Template-based + neural | MIT-quality academic standard | Setup complexity |
| Molecular Transformer | Forward + retro transformer | Single SMILES-to-SMILES | Less robust OOD |
| IBM RXN | Cloud service | High quality | API access required |

**Decision:** For most users, **AiZynthFinder 4.4 with USPTO + USPTO-50k templates** is the open-source standard. For high-stakes routes, validate with Molecular Transformer forward prediction.

## AiZynthFinder Setup

**Goal:** Configure AiZynthFinder with USPTO templates and a building-block stock; run MCTS retrosynthesis on a target SMILES.

**Approach:** Build a configuration dict pointing to policy templates and a stock HDF5, instantiate `AiZynthFinder`, set the target SMILES, then call `tree_search()` followed by `build_routes()`.

```python
from aizynthfinder.aizynthfinder import AiZynthFinder

config_dict = {
    'policy': {
        'files': {
            'uspto': ['policy/uspto_model.onnx', 'templates/uspto_templates.csv'],
        }
    },
    'stock': {
        'files': {
            'zinc': 'stock/zinc.h5',
        }
    },
    'finder': {
        'algorithm': 'mcts',
        'iteration_limit': 100,
        'time_limit': 120,
    }
}

finder = AiZynthFinder(configdict=config_dict)
finder.target_smiles = 'CC(=O)Nc1ccc(C(=O)Nc2cccc(C(F)(F)F)c2)cc1'
finder.tree_search()
finder.build_routes()
```

## Route Output Analysis

```python
for route in finder.routes:
    print(f'Depth: {route.depth}, Score: {route.score:.2f}')
    print(f'In-stock: {sum(node.in_stock for node in route.leafs())}')
    print(f'Building blocks: {[node.smiles for node in route.leafs()]}')
```

Critical metrics:
- **Depth**: synthetic steps (1-3 typical for medchem)
- **Score**: AiZynthFinder route score (0-1)
- **In-stock**: how many leaf nodes are commercially available

## Route Scoring (MO-MCTS)

AiZynthFinder 4.0 supports multi-objective scoring:

```python
config_dict['finder']['algorithm'] = 'mo_mcts'
config_dict['finder']['mo_mcts'] = {
    'objectives': [
        {'name': 'state_score', 'weight': 0.5},
        {'name': 'broken_bonds_score', 'weight': 0.3},
        {'name': 'route_length', 'weight': 0.2, 'maximize': False},
    ]
}
```

## Building Block Stocks

| Stock | Compounds | Source | Cost-tier |
|-------|-----------|--------|-----------|
| ZINC clean leads | 250k | ZINC22 | Various |
| Enamine Building Blocks | 200k+ | Enamine | $$ |
| Enamine REAL | 29B (make-on-demand) | Enamine | $$$ |
| Mcule | 25M | Mcule | $$ |
| eMolecules | 16M | eMolecules | $$ |
| ChemBridge | 1M | ChemBridge | $$ |

```bash
aizynthtrain build-stock --input zinc_building_blocks.smi --output zinc.h5
```

## Forward Validation with Molecular Transformer

```python
from molecular_transformer import predict_forward

precursors = route.leafs()
predicted_product = predict_forward(precursors)
match = (Chem.CanonSmiles(predicted_product) == 
         Chem.CanonSmiles(finder.target_smiles))
```

Routes where the forward prediction reproduces the target are highest confidence. ~30-50% of AiZynthFinder routes pass forward validation.

## Template-Free with Chemformer

```python
from chemformer import Chemformer

cf = Chemformer.load_pretrained('USPTO_RETROSYNTHESIS_TEMPLATE_FREE')
predictions = cf.predict('CC(=O)Nc1ccc(C(=O)Nc2cccc(C(F)(F)F)c2)cc1',
                         beam_search=10)
```

**Trade-off:** Template-free is more flexible but harder to debug. Combining with AiZynthFinder template MCTS gives best of both.

## Disconnection-Aware Design (DAD)

```bash
aizynthcli --smiles compounds.smi --output routes.json \
           --config config.yaml --policy uspto --stock zinc
```

For each compound, returns top-K routes. Score-feasibility for generative design:"
- "Synthesizable" = in-stock leaves >= 2 in best route
- "Routable" = at least one route depth <= 5
- "Easy" = at least one route depth <= 3 with all leaves in-stock

## References

- Saigiridharan et al., *J. Cheminform.* 16:57 -- AiZynthFinder 4.0.
- Irwin et al., 2022 -- Chemformer.
- Schwaller et al. -- Molecular Transformer.

## Related Skills

- chemoinformatics/generative-design - Generative design with feasibility scoring
- chemoinformatics/reaction-enumeration - Forward direction
- chemoinformatics/scaffold-analysis - R-group decomposition