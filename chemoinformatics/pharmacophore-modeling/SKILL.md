---
name: ors-chemoinformatics-pharmacophore-modeling
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
description: Builds and applies 3D pharmacophore models using RDKit Pharm3D, the apo2ph4 receptor-based workflow, Pharmer / Pharmit (search), and PharmacoForge (diffusion-based generation), covering ligand-based pharmacophore (from active set alignment) and receptor-based pharmacophore (from binding pocket geometry). Explicit handling of feature types, geometric tolerances, partial matching, and pharmacophore-based virtual screening. Use when identifying scaffold-hopping candidates, building shape-and-feature search queries, or transferring SAR across chemotypes.
tool_type: python
primary_tool: RDKit
sources_consulted:
  - bioSkills-main/chemoinformatics/pharmacophore-modeling/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/rdkit-cheminformatics/SKILL.md
---

## Version Compatibility

Reference examples tested with: RDKit 2024.09+, pharmer / pharmit (web service), PharmIT 1.1+, plip 2.4+ (interaction analysis).

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show rdkit` then `help(rdkit.Chem.Pharm3D)` to check signatures

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# Pharmacophore Modeling

Build 3D pharmacophore queries that capture the essential interaction features of a ligand-target binding event. A pharmacophore is the *spatial arrangement of pharmacophore features* (donor, acceptor, hydrophobe, aromatic, charged) sufficient for activity, abstracted from any specific chemotype. Used for scaffold-hopping (find compounds with different scaffold but matching pharmacophore), virtual screening (faster than docking), and cross-target SAR transfer. Modern best practice: derive pharmacophore from co-crystal structure if available (receptor-based; apo2ph4 workflow of Heider et al 2023) or align actives if no crystal (ligand-based). Diffusion-based generation (PharmacoForge) lets pharmacophore drive de novo design.

For 2D scaffold-based searches, see `chemoinformatics/scaffold-analysis`. For 3D shape similarity, see `chemoinformatics/shape-similarity`. For protein-ligand interaction analysis, see `chemoinformatics/virtual-screening`.

## Pharmacophore Feature Types

| Feature | RDKit code | Definition | Geometric tolerance |
|---------|------------|------------|----------------------|
| H-bond donor | D | -OH, -NH | 1.0-1.5 Å |
| H-bond acceptor | A | sp2 O / N (lone pair) | 1.0-1.5 Å |
| Hydrophobe | H | sp3 C / aromatic ring centroid | 1.5-2.0 Å |
| Aromatic ring | R | Aromatic ring centroid + normal | 1.0-1.5 Å |
| Positive ionizable | P | -NH3+, -NR3+ | 1.0-1.5 Å |
| Negative ionizable | N | -COO-, -SO3- | 1.0-1.5 Å |
| Halogen | X | Cl, Br, I (halogen bond donor) | 1.0-1.5 Å |
| Metal coordination | M | sp/sp2 N/O near metal | 0.5-1.0 Å |

Tolerances are pharmacophore-feature distance windows in the search. Tighter tolerances = fewer hits but more specific.

## Method Taxonomy

| Method | Origin | Use case | Fails when |
|--------|--------|----------|------------|
| Ligand-based (LBP) | Catalyst, MOE, RDKit Pharm3D | Multiple actives, no crystal | <3 actives; flexible actives |
| Receptor-based (RBP) | apo2ph4, LigandScout | Co-crystal available | Apo structure (use AlphaFold3 or Boltz) |
| Common pharmacophore | Pharm3D `EmbedPharmacophore` | Consensus from active set | Diverse actives confound alignment |
| Diffusion-based (PharmacoForge) | Flynn et al 2025 | De novo generation with pharmacophore prior | Pretrained model required |
| Active learning pharmacophore | Catalyst variant | Iterative refinement | Custom; not standard |

## Decision Tree by Scenario

| Scenario | Method | Tools |
|----------|--------|-------|
| Co-crystal structure available | Receptor-based | apo2ph4 + Pharmer/Pharmit |
| Multiple active compounds, no crystal | Ligand-based common pharmacophore | RDKit Pharm3D `EmbedPharmacophore` |
| Single active compound | Single-conformer pharmacophore | RDKit Pharm3D from bioactive conformer |
| Scaffold hopping prospective | Receptor-based + shape filter | apo2ph4 + ROCS |
| Cross-target SAR transfer | Common pharmacophore across targets | Manual + LigandScout |
| De novo design with pharmacophore | PharmacoForge | Diffusion-based generation |
| Library pre-filtering | Pharmacophore screen | Pharmit search |

## Ligand-Based Pharmacophore (RDKit Pharm3D)

**Goal:** Extract a common pharmacophore from a set of bioactive compounds.

**Approach:** Embed actives, extract per-molecule features, then build a target pharmacophore with distance bounds capturing cross-active variability.

```python
from rdkit import Chem
from rdkit.Chem import AllChem, ChemicalFeatures
from rdkit.Chem.Pharm3D import Pharmacophore
from rdkit.RDPaths import RDDataDir
import os

fdef_file = os.path.join(RDDataDir, 'BaseFeatures.fdef')
factory = ChemicalFeatures.BuildFeatureFactory(fdef_file)

active_smiles = ['CC(C)c1ccc(C(=O)NCc2ccccn2)cc1',
                 'CCC(C)c1ccc(C(=O)NCc2ccccn2)cc1']
active_mols = [Chem.AddHs(Chem.MolFromSmiles(s)) for s in active_smiles]
for m in active_mols:
    AllChem.EmbedMolecule(m, AllChem.ETKDGv3())
    AllChem.MMFFOptimizeMolecule(m)

feature_lists = [factory.GetFeaturesForMol(m) for m in active_mols]

# Example 2-feature pharmacophore (Aromatic + Donor) with a 3.5-5.0 A band
feature_types = ['Aromatic', 'Donor']
pharmacophore = Pharmacophore.Pharmacophore(feature_types)
pharmacophore.setLowerBound(0, 1, 3.5)
pharmacophore.setUpperBound(0, 1, 5.0)
```

`BaseFeatures.fdef` (RDKit-shipped) defines feature SMARTS. For drug-like pharmacophores, this is the standard starting point.

## Receptor-Based Pharmacophore (apo2ph4 workflow)

**Goal:** Derive a pharmacophore from a protein binding-pocket structure without requiring a bound ligand.

**Approach:** Identify hot-spots (donor / acceptor / hydrophobe regions) from protein geometry; assemble into a pharmacophore. apo2ph4 (Heider et al 2023) describes this pipeline.

```bash
# Conceptual apo2ph4-style workflow; verify the exact CLI against the published release.
apo2ph4 -pdb receptor.pdb \
        -site_residues 'A:100,A:101,A:104,A:108' \
        -output pharmacophore.ph4
```

When a co-crystal ligand is available, **derive pharmacophore directly from the ligand binding pose**: each ligand feature in contact with a complementary protein residue is part of the pharmacophore.

```python
from plip.basic import config
```

PLIP (Protein-Ligand Interaction Profiler) extracts per-residue interactions; use to build the pharmacophore manually from contacts (H-bond, hydrophobic, salt bridge, π-stacking).

## Pharmer / Pharmit (Web Service)

For library screening with a `.ph4` pharmacophore:

- **Pharmer** (Koes 2012): open-source pharmacophore search; efficient indexing
- **Pharmit** (Sunseri 2016): web-based frontend, integrates Pharmer with vendor catalogs (Enamine, Mcule, ZINC)

```bash
# Pharmit provides a REST API for batch search
curl -X POST https://pharmit.csb.pitt.edu/api/search \
     -H 'Content-Type: application/json' \
     -d '{"pharmacophore": "...", "library": "enamine-real", "max_hits": 1000}'
```

For open-source Pharmer, install via conda; programmatic interface in Python.

## Diffusion-Based Pharmacophore Generation (PharmacoForge)

PharmacoForge (Flynn et al 2025) generates molecules conditioned on a pharmacophore using a diffusion model. Use when de novo design is needed and a pharmacophore constraint is desired.

```python
# PharmacoForge pseudo-API; verify against the published release.
# from pharmaco_forge import generate
# mols = generate(
#     pharmacophore='ph4_file',
#     n_molecules=1000,
#     scaffold_hint='aryl_sulfonamide',
# )
```

## Per-Tool Failure Modes

### Ligand-based pharmacophore -- too few actives

**Trigger:** Active set < 5 compounds with diverse chemotypes.

**Mechanism:** Common pharmacophore requires shared features; small active sets don't converge.

**Symptom:** All-atom pharmacophore is too permissive; thousands of hits with random features.

**Fix:** Use receptor-based pharmacophore if crystal available; or pick 1 bioactive conformer as single template.

### apo2ph4 -- ambiguous pocket definition

**Trigger:** Binding site contains multiple sub-pockets; user-specified residues span all.

**Mechanism:** Hot-spot detection over generalizes.

**Symptom:** Pharmacophore has too many features; nothing matches in real library.

**Fix:** Manually curate sub-pocket; pass focused residue list (3-6 residues in active site).

### Pharmer / Pharmit -- too few hits

**Trigger:** Pharmacophore strict; library small.

**Mechanism:** Geometric tolerance + feature count filter compounds aggressively.

**Symptom:** < 10 hits returned for large library.

**Fix:** Increase tolerance by 0.5-1.0 Å; remove 1 least-essential feature; verify pharmacophore geometry.

### Pharmacophore match but binder is inactive

**Trigger:** Compound matches pharmacophore but IC50 > 10 µM.

**Mechanism:** Pharmacophore captures necessary features but not sufficient (strain, dynamics, off-target).

**Symptom:** False positive in screen.

**Fix:** Combine pharmacophore with shape (ROCS color) and physchem filters.

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `EmbedPharmacophore` returns no match | Distance bounds too tight | Widen by 1 Å |
| Feature SMARTS not recognized | Custom fdef file required | Verify against `BaseFeatures.fdef` |
| Stereochemistry not in pharmacophore | Default RDKit features ignore stereo | Use PLIP for stereo-aware contact analysis |
| PLIP can't find interactions | Wrong residue numbering | Check PDB numbering vs UniProt offset |
| Pharmer hangs on large library | In-memory index for big libraries | Use Pharmer with --disk-index flag |

## References

- Heider et al., *J. Chem. Inf. Model.* 63:147-158 -- apo2ph4 receptor-based pharmacophore.
- Flynn et al., *Front. Bioinform.* -- PharmacoForge diffusion-based generation.
- Koes et al., *J. Chem. Inf. Model.* 52:1159 -- Pharmer.
- Sunseri et al., *J. Mol. Graph. Model.* -- Pharmit web service.
- Wermuth et al. -- IUPAC pharmacophore definition.

## Related Skills

- chemoinformatics/scaffold-analysis - 2D scaffold analysis
- chemoinformatics/shape-similarity - 3D shape
- chemoinformatics/similarity-searching - 2D similarity
- chemoinformatics/virtual-screening - Docking as alternative
- chemoinformatics/conformer-generation - 3D conformers for active alignment
- chemoinformatics/generative-design - Generative models with pharmacophore conditioning