---
name: covalent-design
description: "Designs covalent inhibitors and warheads targeting cysteine (most common,
  ~98% of covalent drugs), lysine, serine, threonine, tyrosine, and aspartate residues,
  with explicit handling of warhead reactivity (acrylamide, chloroacetamide, vinyl
  sulfone, sulfonyl fluoride, fluorosulfate, aldehyde, boronate, nitrile), reversibility
  (kinact/Ki, t_residence), glutathione (GSH) stability, intrinsic reactivity assays,
  and covalent docking (DOCKovalent, GOLD, HCovDock). Use when designing covalent
  inhibitors for targeted covalent inhibition (TCI), KRAS G12C-style approaches, or
  rationalizing covalent SAR.
license: MIT
---

<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: bioSkills-main/chemoinformatics/covalent-design/SKILL.md; SciAgent-Skills-main/skills/structural-biology-drug-discovery/cysdb-covalent/SKILL.md
-->

## Version Compatibility

Reference examples tested with: RDKit 2024.09+, OpenEye / AutoDock Vina 1.2+ (for covalent extensions), GOLD (commercial), DOCKovalent (web service), HCovDock 1.0+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(rdkit.Chem)` to check signatures

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# Covalent Inhibitor Design
"
Design molecules that form covalent bonds with target protein residues. The "covalent revolution" made TCIs (Targeted Covalent Inhibitors) clinically validated: KRAS G12C inhibitors (sotorasib, adagrasib), BTK inhibitors (ibrutinib), and EGFR inhibitors (osimertinib) are recent successes. Postdoc-grade covalent design requires balancing **intrinsic reactivity** vs **selectivity**, **reversibility** (irreversible vs reversible covalent), and **drug-likeness** (warheads can hurt PK).

For warhead substructure filtering (in non-covalent contexts), see `chemoinformatics/substructure-search`. For non-covalent docking, see `chemoinformatics/virtual-screening`. For pose validation, see `chemoinformatics/pose-validation`.

## Reactive Residue Taxonomy

| Residue | % of covalent drugs | Reactivity | Notes |
|---------|---------------------|------------|-------|
| Cysteine | ~98% | High (nucleophile thiol) | Most accessible; preferred |
| Lysine | ~1% | Moderate (amine) | Less reactive; selective for sulfonyl fluoride |
| Serine | <1% | Low (alcohol, requires activation) | β-lactam, boronate |
| Threonine | very rare | Low | Boronate, aldehyde |
| Tyrosine | very rare | Moderate (phenol) | Sulfonyl fluoride, fluorosulfate |
| Aspartate/Glutamate | very rare | Low (carboxylate) | Aldehyde Schiff base |

Cysteine is the dominant target because:
- Soft nucleophile (matches soft electrophiles)
- Low background reactivity (rare in proteins, ~1.7%)
- Distinguishable from common nucleophiles (GSH, off-target Cys)

## Warhead Chemistry

| Warhead | SMARTS | Reactivity | Reversibility | Cys-selective |
|---------|--------|------------|---------------|----------------|
| Acrylamide | `C(=O)C=C` | Moderate (Michael acceptor) | Irreversible | Yes |
| Chloroacetamide | `C(=O)CCl` | High (SN2) | Irreversible | Yes |
| α-haloketone | `[CX3](=O)C[F,Cl,Br]` | Very high | Irreversible | Yes |
| Vinyl sulfone | `S(=O)(=O)C=C` | Moderate (Michael) | Irreversible | Yes |
| Sulfonyl fluoride | `S(=O)(=O)F` | Moderate | Irreversible | Lys/Tyr/Ser |
| Fluorosulfate (SuFEx) | `OS(=O)(=O)F` | Moderate | Irreversible | Tyr/Lys |
| Aldehyde | `C(=O)[H]` | Variable | Reversible | Cys/Lys/Ser |
| Boronate | `B(O)O` | Moderate | Reversible | Ser/Thr |
| Nitrile | `C#N` | Low | Reversible | Cys |
| Epoxide | `C1OC1` | High | Irreversible | Cys/Lys/Asp |
| Maleimide | `C(=O)N(C(=O))C=C` | Very high | Irreversible | Cys |
| Cysteine-selective heterocycle | various | Moderate | Variable | Yes |

**Practical hierarchy:** Acrylamide is the modern default for cysteine-selective TCIs. Chloroacetamide is more reactive (faster) but less selective.

## Decision Tree by Scenario

| Goal | Warhead choice | Reactivity tier |
|------|----------------|-----------------|
| Cysteine TCI, drug candidate | Acrylamide | Moderate (~kinact/Ki ~10^3-10^5 M^-1 s^-1) |
| Cysteine probe (chemical biology) | Chloroacetamide | High (~10^4-10^6 M^-1 s^-1) |
| Lysine TCI | Sulfonyl fluoride | Moderate |
| Tyrosine TCI | Fluorosulfate (SuFEx) | Moderate |
| Reversible covalent (KRAS G12C-like) | Acrylamide with α-substitution | Moderate reversibility |

## Intrinsic Reactivity Assays

A covalent inhibitor's effectiveness = (intrinsic reactivity) × (target residence time in pocket) / (off-target reactivity).

```python
WARHEAD_PATTERNS = {
    'acrylamide': Chem.MolFromSmarts('[CX3]=[CX3][CX3]=O'),
    'chloroacetamide': Chem.MolFromSmarts('[CX3](=O)C[Cl]'),
    'vinyl_sulfone': Chem.MolFromSmarts('[SX4](=O)(=O)C=C'),
    'sulfonyl_fluoride': Chem.MolFromSmarts('[SX4](=O)(=O)F'),
}

def warhead_reactivity(mol):
    hits = []
    for name, pat in WARHEAD_PATTERNS.items():
        if mol.HasSubstructMatch(pat):
            hits.append(name)
    return hits
```

## GSH Stability

Test the warhead's intrinsic reactivity against glutathione (γ-Glu-Cys-Gly) in silico before synthesis. A compound that reacts quickly with GSH reacts quickly with off-target thiols (Cys in other proteins).

```python
GSH_SMILES = 'NC(CCC(=O)NCC(=O)O)C(=O)NCC(=O)O'
GSH = Chem.MolFromSmiles(GSH_SMILES)
GSH_CYS_S = [a.GetIdx() for a in GSH.GetAtoms() if a.GetSymbol() == 'S']

# Check warhead accessibility to Cys-SH in GSH
# Use docking or compute GSH-Warhead clash as proxy
```

For experimental GSH stability: HPLC-MS with GSH (1 mM) + compound (10 µM) at 37°C; measure t1/2 (high-quality TCIs have GSH t1/2 > 4 hours).

## Reversible vs Irreversible Covalent

| Property | Irreversible | Reversible |
|----------|-------------|------------|
| Binding kinetics | Single exponential | Two-step (k_on, k_off) |
| Residence time | t_res = 1/k_inact | t_res = 1/k_off |
| Off-target risk | Higher | Lower |
| Recovery after washout | No | Yes |
| Clinical examples | afatinib, ibrutinib | sotorasib (KRAS G12C α-cyanoacrylamide) |

Reversible covalent is preferred when:
- Off-target Cys in related proteins is concern
- Long-term dosing required
- Pharmacodynamic response must be reversible

## Covalent Docking Tools

Standard Vina/GNINA cannot predict covalent adducts. Covalent-specific tools:

| Tool | Approach | Use |
|------|----------|-----|
| GOLD (CCDC) | Covalent bond constraint + ChemScore | Commercial; reliable |
| DOCKovalent | DOCK 6/7 covalent extension | Academic; web service |
| HCovDock | Hybrid covalent | Open source |
| CovSel (custom) | Enumerate covalent adducts then dock | Custom |

**Workflow:** (1) Generate covalent adduct SMILES from warhead + target residue, (2) Build 3D structure, (3) Dock with covalent constraint.

```python
# Conceptual covalent adduct generation
# Use RDKit reaction SMARTS to attach warhead to Cys-S-H
adduct_rxn = AllChem.ReactionFromSmarts(
    '[Cys-S-H:1].[CX3:2]=[CX3:3][CX3:4]=O>>[Cys-S:1][CX3:2][CX3:3][CX3:4]=O'
)
```

## Per-Tool Failure Modes

### Acrylamide too reactive in vivo

**Trigger:** Compound shows GSH t1/2 < 1 hour.

**Mechanism:** Acrylamide warhead reacts with off-target Cys.

**Symptom:** Off-target adducts, toxicity.

**Fix:** Reduce warhead reactivity (alpha-substituted acrylamide, e.g. KRAS G12C strategy); use Cyanoacrylamide for reversible covalent.

### No covalent adduct formed in MS

**Trigger:** Compound has warhead, binds pocket, but no covalent adduct observed.

**Mechanism:** Warhead geometry wrong; nucleophile not in attack position.

**Symptom:** Reversible-only binding; no time-dependent IC50 shift.

**Fix:** Visualize docked pose; check distance nucleophile to electrophile < 4 Å; align with target residue.

### Hook effect in PROTAC context

**Trigger:** PROTAC with covalent target ligand shows bell-shaped degradation curve.

**Mechanism:** At high PROTAC concentration, binary complexes (target-PROTAC, E3-PROTAC) dominate over ternary.

**Symptom:** Dmax falls at high [PROTAC]; no degradation.

**Fix:** Use lower dose window; optimize linker to favor ternary.

## References

- Lonsdale & Ward, *J. Med. Chem.* -- targeted covalent inhibitors review.
- Singh et al. -- KRAS G12C and covalent drug design.
- Gehringer & Laufer, *J. Med. Chem.* -- cysteine-targeted warheads.

## Related Skills

- chemoinformatics/substructure-search - Warhead SMARTS
- chemoinformatics/virtual-screening - Non-covalent docking
- chemoinformatics/protac-degraders - Bifunctional covalent
- chemoinformatics/pose-validation - Pose QC for covalent adducts