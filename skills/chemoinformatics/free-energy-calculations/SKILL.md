---
name: free-energy-calculations
description: "Performs alchemical free-energy calculations including relative binding"
license: MIT
---



<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: bioSkills-main/chemoinformatics/free-energy-calculations/SKILL.md
-->

## Version Compatibility

Reference examples tested with: OpenFE 1.7+, OpenMM 8.1+, GROMACS 2024+, AMBER pmemd 22+, alchemlyb 2.1+, pymbar 4.0+, RDKit 2024.09+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` to check signatures
- CLI: `openfe --version`; `gmx --version`; `pmemd.cuda --version`

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# Free Energy Calculations

Predict binding affinity differences (RBFE) or absolute binding affinities (ABFE) using alchemical free-energy methods. FEP+ (Schrödinger) is the commercial industry standard; OpenFE (Open Free Energy) is the open-source reference. Modern best practice achieves 1-2 kcal/mol RMSE vs experimental for well-set-up RBFE on rigid receptors. Boltz-2 affinity module (Wohlwend 2025) approaches FEP accuracy at 1000x speed on benchmarks, but FEP remains gold standard for production lead optimization.

For docking input poses, see `chemoinformatics/virtual-screening`. For pose validation before FEP, see `chemoinformatics/pose-validation`. For ML alternatives, see `chemoinformatics/docking-rescoring`.

## FEP Method Taxonomy

| Method | Cost / pair | Accuracy | Use case | Fails when |
|--------|-------------|----------|----------|------------|
| FEP+ (Schrödinger) | hours-days GPU | 1-2 kcal/mol RMSE | Commercial lead opt | License cost |
| OpenFE RBFE | hours-days GPU | comparable to FEP+ | Open-source RBFE | Setup less mature |
| OpenFE ABFE | days GPU | 2-3 kcal/mol RMSE | Absolute affinity | Slower; setup care |
| GROMACS RBFE | hours-days GPU | 1-2 kcal/mol | Power users | Manual setup is error-prone |
| AMBER pmemd RBFE | hours-days GPU | 1-2 kcal/mol | Tradition | Manual setup |
| MM/PBSA | minutes | 3-5 kcal/mol RMSE | Endpoint, fast | Limited accuracy |
| MM/GBSA | minutes | 3-5 kcal/mol RMSE | Endpoint, faster | Same caveats |
| Boltz-2 affinity | seconds GPU | 0.66 Pearson on FEP subset | ML alternative; 1000x faster | Novel chemotypes |

**Decision:** For lead-optimization SAR validation, **OpenFE RBFE** (open) or **FEP+** (commercial) is the standard. For prospective discovery, MM/GBSA is a fast first-pass.

## Decision Tree by Scenario

| Scenario | Recommended workflow |
|----------|---------------------|
| Rank close analogs (R-group SAR) | RBFE via OpenFE (cycle: lig1↔lig2↔lig3) |
| Cross-scaffold ranking | ABFE per ligand; or coordinated RBFE with star network |
| Lead optimization 10-50 compounds | RBFE; perturbation-graph design |
| Single ligand affinity | ABFE (no reference needed) |
| Quick first-pass on top 1k | MM/GBSA after docking |
| Novel scaffold prospective | Boltz-2 affinity + FEP confirmation on top |
| Selectivity (target vs off-target) | RBFE on both proteins; report delta-delta-G |
| Allosteric vs orthosteric | ABFE comparable; check pose stability with MD |
| Ions / metal centers | Specialized force field (ZAFF, MCPB.py); not standard FEP |

## Thermodynamic Cycle

```
   target:lig1     --delta-G_bound-->    target:lig2
       |                                    |
   delta-G_free (in solvent)         delta-G_free
       v                                    v
   target + lig1     --delta-G_unbound-->  target + lig2
```

`delta-delta-G = (delta-G_bound) - (delta-G_unbound)`

This is the binding free energy difference between lig1 and lig2 to the target.

## OpenFE RBFE Workflow

**Goal:** Set up an RBFE calculation between two congeneric ligands in a protein pocket.

**Approach:** Build OpenFE components (protein, ligand1, ligand2, solvent), define a transformation mapping atoms between ligands, instantiate a `RelativeHybridTopologyProtocol`, then execute.

```python
from openfe import SmallMoleculeComponent, ProteinComponent, SolventComponent
from openfe.protocols.openmm_rfe import RelativeHybridTopologyProtocol

# Build components
protein = ProteinComponent.from_pdb_file('protein.pdb')
lig1 = SmallMoleculeComponent.from_smiles('CCO')
lig2 = SmallMoleculeComponent.from_smiles('CC(=O)O')
solvent = SolventComponent()

# Define transformation (atom mapping)
from openfe.setup import atom_mapping
mapper = atom_mapping.lomap_mapper
mapping = mapper.suggest_mappings(lig1, lig2)[0]

# Run protocol
protocol = RelativeHybridTopologyProtocol(...)
```

## Lambda Window Scheduling

Alchemical transformations are evaluated at multiple lambda values (typically 11-21 windows). Key parameters:

| Parameter | Default | Why |
|-----------|---------|-----|
| `lambda_windows` | 11 | 0, 0.1, 0.2, ..., 1.0 |
| `soft_core_alpha` | 0.5 | Soft-core potential for vdW |
| `soft_core_beta` | 12.0 | Beta parameter |
| `restraint_type` | 'flat-bottom' | Restrain ligand in pocket |
| `replicas` | 3 | Per-window for convergence |

## MBAR / BAR Analysis

After running windows, estimate free energy via Multistate Bennett Acceptance Ratio (MBAR) or BAR (Bennett Acceptance Ratio):

```python
from alchemlyb.workflows import ABFE
from alchemlyb.estimators import MBAR, BAR

# Reduce energy matrices to per-window time series
# Then estimate
mbar = MBAR()
mbar.fit(u_n=np.array([...]), N_k=np.array([...]))
delta_g = mbar.delta_f_
```

## Cycle Closure Validation

For three ligands (A, B, C), perturbations A→B, B→C, C→A should sum to zero. Cycle closure error measures force-field + setup quality:

```python
# Cycle closure: dG(A->B) + dG(B->C) + dG(C->A) should = 0
# If > 0.5 kcal/mol, suspect setup issues:
# - Bad atom mapping
# - Force field parameters
# - Convergence (need longer sampling)
```

## REST2 Enhanced Sampling

Replica Exchange with Solute Tempering (REST2) enhances sampling of ligand conformations. Use when ligands have buried rotatable bonds.

```python
# In OpenFE, set:
protocol.settings.rest2 = True
protocol.settings.n_replicas_solute = 8
```

## Per-Tool Failure Modes

### OpenFE setup error

**Trigger:** `MappingError` during setup.

**Mechanism:** Atom mapping failed because scaffold mismatch.

**Symptom:** No mappings returned.

**Fix:** Manual atom mapping; verify both ligands have common core; Lomap settings.

### Poor convergence

**Trigger:** `MBAR` reports high uncertainty (> 1 kcal/mol).

**Mechanism:** Sampling insufficient; ligand conformational space not explored.

**Symptom:** Different windows give inconsistent estimates.

**Fix:** Increase simulation length per window (2-5 ns); check for buried rotatable bonds (REST2); verify restraints not too tight.

### Force field failure -- net charge change

**Trigger:** Ligand A is neutral, B is charged (or vice versa).

**Mechanism:** Charged perturbations need different water models; counterion handling affects results.

**Symptom:** RBFE error 2-3 kcal/mol.

**Fix:** Add decoupling of counterion; use specialized protocols for charged perturbations.

### Pose change mid-simulation

**Trigger:** Ligand leaves pocket in MD.

**Mechanism:** Restraint too weak; pose from docking was not stable.

**Symptom:** Simulation artifacts; free energy unreliable.

**Fix:** Tighten flat-bottom restraint; re-dock and validate; use ensemble of starting poses.

## References

- Ross et al., *J. Chem. Theory Comput.* -- OpenFE 1.0.
- Wang et al., *J. Am. Chem. Soc.* -- FEP+ methodology.
- Wohlwend et al., 2025 -- Boltz-2 affinity module.

## Related Skills

- chemoinformatics/virtual-screening - Input pose generation
- chemoinformatics/pose-validation - Pose QC before FEP
- chemoinformatics/docking-rescoring - ML alternatives
- chemoinformatics/covalent-design - Covalent FEP setup"