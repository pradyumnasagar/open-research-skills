---
name: ors-chemoinformatics-generative-design
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
description: Designs novel molecules using REINVENT 4 (de novo, scaffold decoration, linker design, R-group, molecular optimization), MolMIM, Diffusion-based generators (DiGress, DiffSMol), and JT-VAE with explicit handling of multi-parameter optimization (MPO), goal-directed scoring functions, transfer/reinforcement/curriculum learning, synthetic accessibility scoring, and chemical space exploration vs exploitation. Use when designing new chemical matter against a target, decorating a scaffold, linking fragments, or optimizing a hit for multiple ADMET / activity properties simultaneously.
tool_type: python
primary_tool: REINVENT
sources_consulted:
  - bioSkills-main/chemoinformatics/generative-design/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/reinvent/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/molmim/SKILL.md
---

## Version Compatibility

Reference examples tested with: REINVENT 4.0+, RDKit 2024.09+, PyTorch 2.1+, MolMIM (NVIDIA BioNeMo), chemprop 2.0+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# Generative Molecular Design

Generate novel molecules biased toward desired properties using deep generative models. REINVENT 4 (Loeffler 2024, AstraZeneca) is the open-source production-grade framework, supporting 4 generation modes (de novo, scaffold decoration, linker design, molecular optimization) and 3 learning algorithms (transfer learning, reinforcement learning, curriculum learning). The art of generative design is in the **scoring function**: poorly-designed scoring rewards uninteresting molecules, while well-designed scoring captures both activity and developability.

For QSAR/scoring models that feed generative design, see `chemoinformatics/qsar-modeling`. For synthetic feasibility, see `chemoinformatics/retrosynthesis`. For library enumeration as alternative, see `chemoinformatics/reaction-enumeration`.

## Generator Mode Taxonomy

| Mode | Input | Output | Use case | Fails when |
|------|-------|--------|----------|------------|
| De novo | Empty seed or training set | Novel molecules | Wide chemical space exploration | Synthetic feasibility weak |
| Scaffold decoration | Scaffold + attachment points | Decorated molecules | Series expansion | Diversity limited by scaffold |
| Linker design | 2 fragments | Linker molecules | PROTAC, ternary complex | Few linker geometric options |
| R-group replacement | Scaffold + existing R-groups | New R-group set | Optimize one position | Single-position only |
| Molecular optimization | Lead molecule | Improved analogs | Lead optimization | Improvement window narrow |
| Constrained generation | Hard constraints (MW, fragments) | Compliant molecules | Patent / IP design | Constraints overly restrictive |

## Learning Algorithm Taxonomy

| Algorithm | Use | Pro | Con |
|-----------|-----|-----|-----|
| Transfer learning (TL) | Adapt prior model to focused training set | Stable, simple | Limited optimization power |
| Reinforcement learning (RL) | Reward-driven generation | Powerful for MPO | Reward hacking risk |
| Curriculum learning (CL) | Gradual constraint introduction | Better convergence | Slower; tuning sensitive |

## Decision Tree by Scenario

| Scenario | Generator | Algorithm | Scoring |
|----------|-----------|-----------|---------|
| New target, no SAR | De novo | RL on docking score | Glide / Vina + QED |
| Series expansion | Scaffold decoration | TL on series + RL | QSAR ensemble + QED |
| PROTAC linker | Linker design | RL on ternary complex | DC50 surrogate |
| Lead optimization MPO | Molecular optimization | CL with staged constraints | Multi-task: activity + ADMET |
| Diverse hit set | De novo with diversity bonus | RL + Tanimoto distance to known | Activity + diversity |
| Patent space carve-out | Constrained de novo | RL + structural constraints | Activity + novelty |
| Hit-to-lead | R-group replacement | TL on lead + RL | Activity + Lipinski |
| ADMET-aware design | De novo or optimization | RL | hERG + CYP + AMES + QED |

## REINVENT 4 Setup

REINVENT 4 uses a TOML configuration file specifying generator, algorithm, prior model, and scoring functions.

```toml
[parameters]
prior_file = "priors/reinvent.prior"
agent_file = "priors/reinvent.prior"
batch_size = 64
unique_sequences = true

[[stage]]
max_steps = 1000
chkpt_file = "checkpoints/agent.chkpt"

[[stage.scoring.component]]
name = "QED"

[[stage.scoring.component]]
name = "custom_activity"
weight = 1.0
```

## Multi-Parameter Optimization (MPO)

The art of generative design lies in the scoring function. Common components:

| Component | Purpose | Reference |
|-----------|---------|-----------|
| QED | Drug-likeness | Bickerton 2012 |
| SAScore | Synthetic accessibility | Ertl 2009 |
| Activity QSAR | Target binding | chemprop model |
| hERG | Cardiotox | ADMETlab 3.0 |
| Lipinski | Rule of 5 | Lipinski 1997 |
| Tanimoto distance | Diversity from known actives | RDKit |

**Critical pitfall:** Reward hacking. If activity model is biased, generator produces structures that exploit the bias. Mitigations:
- Use ensemble of models (5+)
- Constrain to chemically reasonable substructures
- Validate top-100 by orthogonal in silico methods (docking, FEP)

## MolMIM (NVIDIA BioNeMo)

MolMIM is a property-guided latent-variable model:

```python
from molmint import MolMIM
from rdkit import Chem

model = MolMIM()
smiles = 'CCO'
optimized = model.optimize(smiles, target_logp=2.5, target_sas=2.0)
mol = Chem.MolFromSmiles(optimized)
```

**Strength:** Continuous property optimization in latent space. **Weakness:** Latent space not always semantically meaningful.

## Diffusion-Based Generators (DiffSMol, DiGress)

Diffusion models generate molecules by iteratively denoising:

```python
# DiffSMol / DiGress pseudo-API; verify against current release.
# from diffsmol import generate
# mols = generate(n_samples=1000, scaffold='aryl_sulfonamide')
```

**Strength:** State-of-the-art sample quality on MOSES benchmark. **Weakness:** Slower than RL; harder to condition on multiple objectives.

## JT-VAE (Latent-Space Optimization)

Junction Tree VAE optimizes in latent space then decodes:

```python
# Pseudo-API
# from jtvae import optimize
# best_mol = optimize(smiles='CCO', target='activity', iterations=100)
```

**Strength:** Smooth latent space for optimization. **Weakness:** Outdated vs transformers; reconstruction quality lower.

## Per-Tool Failure Modes

### REINVENT -- reward hacking

**Trigger:** Generated molecules score high but don't bind target.

**Mechanism:** Generator exploits QSAR model weaknesses (e.g., simple features that correlate spuriously).

**Symptom:** Top-100 in silico but 0% hit rate in vitro.

**Fix:** Ensemble of 5+ scoring models; structural diversity constraint; orthogonal validation (docking).

### Scaffold decoration -- diversity loss

**Trigger:** After 1000 REINVENT steps, all generated molecules are near-same scaffold.

**Mechanism:** Generator converges to local optimum.

**Symptom:** Generated SMILES have Tanimoto > 0.9 to scaffold.

**Fix:** Add Tanimoto distance to known actives as bonus; restart with new seed; increase stochasticity.

### Generative vs docking mismatch

**Trigger:** Generated molecules have high predicted QED but Vina score = 0.

**Mechanism:** Generator not aware of binding pocket geometry.

**Symptom:** Synthesizable but non-binders.

**Fix:** Add docking score (Vina or GNINA) to scoring function; dock top candidates as filter.

### MolMIM -- discontinuous objective

**Trigger:** Optimizing a property with sharp boundaries (e.g., exactly 1 sulfonamide).

**Mechanism:** Latent-space optimization uses smooth gradient; sharp objectives don't have it.

**Symptom:** Generator oscillates around target.

**Fix:** Use reward-style scoring instead of property-distance; post-filter for hard constraints.

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `reinvent` exits with OOM | Prior model too large for GPU | Use smaller prior; CPU mode |
| All generated molecules identical | Mode collapse | Reset agent; add diversity bonus |
| Generated SMILES invalid | Tokenizer mismatch | Update reinvent to latest version; validate SMILES post-gen |
| MPO components all zero | Components missing from TOML | Re-check TOML section names |
| QED 1.0 but no synthesis | QED rewards unrealistic features | Add SAScore; run retrosynthesis filter |

## References

- Loeffler et al., *J. Cheminform.* -- REINVENT 4.
- Sanchez-Lengeling et al., *ACS Cent. Sci.* -- generative chemistry review.
- Jin et al. -- JT-VAE.

## Related Skills

- chemoinformatics/qsar-modeling - Scoring models
- chemoinformatics/retrosynthesis - Synthetic feasibility
- chemoinformatics/reaction-enumeration - Library enumeration alternative
- chemoinformatics/protac-degraders - Linker design for PROTACs
