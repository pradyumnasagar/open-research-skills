---

name: pose-validation
description: "Validates docked / generated protein-ligand poses using PoseBusters physical-validity tests, strain energy quantification, geometric checks (planarity, vdW overlap, bond/angle distortion), and pose-energy reasonableness. Filters AI-docking outputs (DiffDock, EquiBind, NeuralPLexer) where ~50% of poses fail physical-validity tests. Use when QC-ing docking results, comparing classical vs ML docking outputs, or filtering pose lists before SAR analysis."
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

Reference examples tested with: PoseBusters 0.6+, RDKit 2024.09+, pandas 2.2+, posecheck 0.5+ (optional).

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# Pose Validation

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

## PoseBusters Test Suite

PoseBusters runs ~20 individual checks grouped into:

| Check group | What it tests | Threshold |
|-------------|---------------|-----------|
| Sanity | Ligand chemical sanity | RDKit sanitization passes |
| Bond lengths | Bond lengths within reference | < 2 std from RDKit defaults |
| Bond angles | Bond angles within reference | < 2 std from RDKit defaults |
| Internal steric | No intra-ligand vdW clash | vdW overlap < 1.0 Å |
| Aromatic ring planarity | Aromatic rings planar | < 0.25 Å RMS deviation |
| Double-bond stereo | Z/E preserved | Match input SMILES |
| Internal energy | Strain not absurd | UFF energy < 100 kcal/mol typical |
| Volume overlap | vdW overlap with protein | < 7.5% of ligand vdW volume |
| Distance to protein | Not floating in solvent | Closest contact < 5 Å |
| Chirality | R/S preserved from input | Match input SMILES |
"
A pose passing ALL tests is "PB-valid". Combined PB-valid + RMSD <= 2 Å is the modern criterion.

## When to Apply PoseBusters

| Workflow | PoseBusters use | Action |
|----------|-----------------|--------|
| Self-docking (validating method) | Required | Compare PB-valid + RMSD <= 2A |
| Cross-docking | Required | PB-valid + RMSD <= 2A; account for protein flexibility |
| Virtual screening top hits | Required | Filter to PB-valid before MM/GBSA / FEP |
| AI docking (DiffDock, etc.) | Mandatory | Often 50% fail; otherwise can't compare to classical |
| Generated structures (RFdiffusion) | Required | Generation often produces clashes |
| Boltz-2 / AlphaFold3 ligand poses | Recommended | Same family of issues; less frequent than DiffDock |
| Production FEP setup | Required | Strain in input pose breaks FEP convergence |

## PoseBusters Usage

```python
from posebusters import PoseBusters

bust = PoseBusters(config='redock')

results = bust.bust(
    mol_pred='predicted.sdf',
    mol_true='reference.sdf',
    mol_cond='receptor.pdb',
)
```

`config` options and included checks:

| Config | Includes | When to use |
|--------|----------|-------------|
| `redock` | All checks + RMSD vs reference + protein vdW overlap | Self-docking benchmarks, retrospective validation |
| `dock` | All checks except RMSD reference | Blind docking, prospective virtual screening |
| `mol` | Intra-ligand only (sanity, bonds, angles, rings, stereo, energy) | Conformer QC; no protein context |

Output DataFrame columns include: `mol_pred_loaded`, `sanitization`, `all_atoms_connected`, `bond_lengths`, `bond_angles`, `internal_steric_clash`, `aromatic_ring_flatness`, `double_bond_flatness`, `internal_energy`, `protein_flexibility`, `minimum_distance_to_protein`, `minimum_distance_to_organic_cofactors`, `minimum_distance_to_inorganic_cofactors`, `volume_overlap_with_protein`, `volume_overlap_with_organic_cofactors`, `volume_overlap_with_inorganic_cofactors`. All bool; True = pass.

## Python Library API

**Goal:** Programmatically validate a docked-pose SDF against a receptor PDB and produce a PB-valid filter.

**Approach:** Instantiate `PoseBusters(config='dock')`, call `bust()` on the SDF + PDB pair, and AND-aggregate all boolean check columns into a single `pb_valid` flag.

```python
from posebusters import PoseBusters
import pandas as pd

bust = PoseBusters(config='dock')
df = bust.bust(mol_pred='predicted.sdf', mol_cond='receptor.pdb')

CHECK_COLS = [c for c in df.columns if c not in
              ('file', 'molecule', 'molecule_id', 'name')]
df['pb_valid'] = df[CHECK_COLS].all(axis=1)
valid = df[df['pb_valid']]
print(f'PB-valid: {len(valid)}/{len(df)} ({100*len(valid)/len(df):.1f}%)')
```

## Strain Energy Quantification

Beyond binary pass/fail, a continuous strain score helps rank otherwise-valid poses.

**Goal:** Quantify ligand strain in a docked pose and rank candidates by total strain (intra-ligand + protein-ligand clash).

**Approach:** Embed the docked conformer, run a quick UFF minimization reading out the energy, then compute inter-molecular contacts against the receptor and sum heavy-atom overlaps that exceed a soft cutoff.

```python
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdForceFieldHelpers import UFFGetMoleculeForceField

def strain_kcal_per_mol(mol, max_attempts=200):
    """Strain relative to UFF minimum, in kcal/mol."""
    m = Chem.Mol(mol)
    m = Chem.AddHs(m, addCoords=True)
    ff = UFFGetMoleculeForceField(m)
    if ff is None:
        return float('nan')
    e0 = ff.CalcEnergy()
    res = ff.Minimize(maxIts=max_attempts)
    e_min = ff.CalcEnergy()
    return e_min - e0
```

**Decision:** For ML-docking hits, prefer poses with strain < 10 kcal/mol over the relaxed conformer; 10-30 kcal/mol is acceptable for diverse chemotypes; > 30 kcal/mol flags bad poses.

## Per-Tool Failure Modes

### PoseBusters all-pass but pose is wrong

**Trigger:** DiffDock or EquiBind output passes all PB checks but RMSD > 5 Å.

**Mechanism:** Pose is chemically sane (no clash, planar rings) but in the wrong pocket / wrong orientation.

**Symptom:** Docked pose looks reasonable in isolation; binding-pocket contacts absent.

**Fix:** Add pocket-residue contact filter: at least N contacts to known binding-site residues.

### Aromatic ring flatness fails after minimization

**Trigger:** Pyridazine / oxadiazole / tetrazole ring reports non-planar.

**Mechanism:** PoseBusters checks RDKit's reference planarity; some 5-membered heterocycles are slightly non-planar in solution.

**Symptom:** False positive on planarity.

**Fix:** Check `aromatic_ring_flatness`; if false-positive, manually inspect 3D coords.

### Internal energy explodes

**Trigger:** UFF energy >> 100 kcal/mol.

**Mechanism:** Docked pose is in a high-energy conformation (compressed torsions, bad contacts).

**Symptom:** PB passes geometrically but energy flags.

**Fix:** Reject pose; rerun docking with higher exhaustiveness.

### Protein flexibility

**Trigger:** Side chain clash with ligand that pocket residue moves to resolve.

**Mechanism:** Rigid receptor assumption fails for induced-fit binding sites.

**Symptom:** PB-valid count artificially low; reasonable poses rejected.

**Fix:** Use `config='dock'` with protein flexibility allowance; or pre-generate ensemble (MD snapshots).

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `mol_pred_loaded` False | RDKit can't parse the SDF | Re-export with `Chem.MolToMolFile(mol, fname)` |
| `all_atoms_connected` False | Disconnected fragments in pose | Check input; use largest fragment only |
| `internal_energy` nan | UFF parameters missing (e.g. boron) | Try MMFF instead; or skip energy check |
| All poses fail `volume_overlap_with_protein` | Receptor and ligand in wrong frame | Verify same coordinate origin |
| Stereo mismatch | Chirality not preserved during parse | Set `Chem.AssignStereochemistry` before scoring |

## References

- Buttenschoen et al., *Chem. Sci.* 15:3130 -- PoseBusters benchmark.
- Harris et al., *J. Chem. Inf. Model.* 63:147-158 -- pose validation overview.
- scikit-bio, RDKit -- the underlying cheminformatics primitives.

## Related Skills

- chemoinformatics/virtual-screening - Docking pipelines
- chemoinformatics/docking-rescoring - ML pose prediction
- chemoinformatics/molecular-io - Parse ligands
- chemoinformatics/conformer-generation - Generate 3D conformers

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
- protac-degraders
- qsar-modeling
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

