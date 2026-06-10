---
name: ors-chemoinformatics-docking-rescoring
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
description: Performs ML-based protein-ligand pose prediction and scoring using DiffDock-L (diffusion-based), Boltz-1 / Boltz-2 (foundation model with affinity), Chai-1, AlphaFold3 ligand, EquiBind, TANKBind, NeuralPLexer, and hybrid workflows (DiffDock pose + GNINA rescore + PoseBusters QC). Explicit handling of when ML beats classical docking, when classical beats ML, the PB-invalid pose problem, and rescoring as the standard production hybrid. Use when modern docking is needed: foundation-model ligand-pose prediction, AI rescoring of classical poses, or scaffold-hopping in cross-docking scenarios.
tool_type: python
primary_tool: DiffDock
sources_consulted:
  - bioSkills-main/chemoinformatics/ml-docking-rescoring/SKILL.md
  - SciAgent-Skills-main/skills/structural-biology-drug-discovery/diffdock/SKILL.md
---

## Version Compatibility

Reference examples tested with: DiffDock-L (Corso 2024), Boltz-1 1.0+, Boltz-2 (Wohlwend 2025), Chai-1 0.4+, AlphaFold3 (DeepMind), EquiBind, TANKBind, GNINA 1.1+, PoseBusters 0.6+.

Before using code patterns, verify installed versions match. If versions differ:
- Python: `pip show <package>` then `help(module.function)` to check signatures
- CLI: `diffdock --version`; `boltz --version`

If code throws ImportError, AttributeError, or TypeError, introspect the installed package and adapt the example to match the actual API rather than retrying.

# ML Docking and Rescoring

Use machine learning models for protein-ligand pose prediction and affinity scoring. The field underwent a major shift in 2023-2025: foundation models (AlphaFold3, Boltz-1, Chai-1) handle protein-ligand prediction natively; diffusion-based docking (DiffDock-L) generates poses; Boltz-2 affinity module approaches FEP accuracy at 1000x speed. Critical caveat: PoseBusters (Buttenschoen 2024) showed ML methods produce ~50% physically-invalid poses despite RMSD <= 2 Å; classical methods (Vina, GOLD) produce ~5-15% invalid. The postdoc-grade workflow is hybrid: ML for pose sampling + classical rescoring + physical validation.

For classical docking, see `chemoinformatics/virtual-screening`. For pose validation (PoseBusters), see `chemoinformatics/pose-validation`. For free-energy calculations (post-docking), see `chemoinformatics/free-energy-calculations`. For PROTAC ternary complex prediction, see `chemoinformatics/protac-degraders`.

## ML Docking Method Taxonomy

| Tool | Approach | Speed | Strength | Fails when |
|------|----------|-------|----------|------------|
| DiffDock-L (Corso 2024) | Equivariant diffusion | 5s/lig GPU | Pose sampling for cross-dock | ~50% PB-invalid; OOD |
| Boltz-1 (Wohlwend 2024) | AlphaFold-style foundation | 10s GPU | Full complex prediction | DNA / RNA may be off |
| Boltz-2 (Wohlwend 2025) | Boltz-1 + affinity head | 10s GPU | Pose + affinity (Pearson 0.66 on 4-target FEP+ subset; RMSE ~1.5 kcal/mol on ChEMBL holdout) | Novel chemotype OOD |
| Chai-1 (Chai 2024) | AlphaFold-style + LM | 10s GPU | Pose 77% RMSD success on PoseBusters | Limited public |
| AlphaFold3 (DeepMind 2024) | Foundation model | API only | Pose 76% RMSD on PoseBusters | Restricted API access |
| EquiBind | Equivariant single-shot | <1s GPU | Fast pose | Lowest accuracy on PoseBusters |
| TANKBind | Distance + classifier | <1s GPU | Fast pose + score | Geometric inconsistency |
| NeuralPLexer | E3-equivariant | <1s | Fast pose | Limited adoption |
| Glide (Schrödinger) | Hybrid grid + ML rescoring | 30s GPU | Commercial SOTA | License cost |
| GNINA 1.1 CNN | Classical sampling + CNN scoring | 30s GPU | Best classical-hybrid | Limited to PDBbind chemotypes |

**Decision:** For pose prediction with structure prediction needed, **Boltz-1** (or Boltz-2 if affinity also needed) is the modern open-source SOTA. For ligand pose with known holo, **DiffDock-L + GNINA rescoring + PoseBusters** is the standard hybrid.

## Decision Tree by Scenario

| Scenario | Recommended workflow |
|----------|---------------------|
| Known holo, need fast pose | GNINA classical |
| Apo or AF-predicted protein, need pose | Boltz-1 or Chai-1 |
| Cross-docking + scaffold hopping | DiffDock-L + GNINA rescore + PoseBusters |
| Affinity prediction (replace FEP first-pass) | Boltz-2 affinity module |
| Ultralarge library (1M+) | Vina pre-filter -> GNINA on top 1% -> Boltz-2 on top 0.1% |
| Novel target family | Boltz-1 / Chai-1 (uses MSA flexibility) |
| Cofactor / metal binding | AlphaFold3 (best cofactor handling); validate with classical |
| PROTAC / bivalent | Boltz-1 / Chai-1 with multimer + constraints |
| Production with auditable poses | GNINA classical + Boltz-2 score |

## PoseBusters Problem (Critical)

PoseBusters benchmark (Buttenschoen 2024) showed:

| Tool | RMSD <= 2 Å | PB-valid | RMSD <= 2 Å AND PB-valid |
|------|-------------|----------|--------------------------|
| Vina (default) | 65% | 90% | 60% |
| GOLD | 70% | 88% | 65% |
| GNINA CNN | 73% | 85% | 65% |
| DiffDock-L | 55% | 40% | 25% |
| EquiBind | 30% | 25% | 10% |
| TANKBind | 45% | 35% | 20% |
| AlphaFold3 ligand | 76% | 65% | 55% |
| Chai-1 | 77% | 70% | 58% |
| Boltz-1 | 74% | 68% | 55% |
| Boltz-2 (with affinity) | 76% | 70% | 58% |

**Conclusion:** Modern foundation models match classical RMSD but with worse physical plausibility. Always require PB-valid + RMSD <= 2 Å.

## DiffDock-L + GNINA Hybrid Workflow (Production Standard)

**Goal:** Use DiffDock-L for fast diverse pose sampling; GNINA CNN to rescore; PoseBusters to filter.

```bash
# Step 1: DiffDock-L pose sampling
python -m inference \
    --protein_path receptor.pdb \
    --ligand_description smiles.smi \
    --out_dir diffdock_out/ \
    --samples_per_complex 40 \
    --inference_steps 20

# Step 2: GNINA CNN rescoring
gnina -r receptor.pdb -l diffdock_out/top_poses.sdf \
      --autobox_ligand reference_ligand.sdf \
      --cnn_scoring rescore \
      -o gnina_rescored.sdf.gz

# Step 3: PoseBusters QC
python -c "
from posebusters import PoseBusters
b = PoseBusters(config='dock')
df = b.bust(mol_pred='gnina_rescored.sdf.gz', mol_cond='receptor.pdb')
print(df.filter(regex='pass').sum().sum(), 'checks passed')
"
```

## Boltz-2 Affinity Prediction (Fast FEP Replacement)

**Goal:** Predict binding affinity at ~10s/ligand on GPU vs hours for FEP.

**Approach:** Submit protein + ligand to Boltz-2 with the affinity head; receive predicted pIC50 or ΔG with uncertainty.

```bash
boltz predict input.yaml --use_affinity --output_dir boltz2_out/
```

**Validation:** Boltz-2 reports Pearson 0.66 vs experimental on 4-target FEP+ subset; RMSE ~1.5 kcal/mol on ChEMBL holdout. Faster than FEP (10s vs hours) but ~3x less accurate.

## Foundation Models: Boltz-1 and Chai-1

For novel target or no MSA, the foundation models treat ligand + protein jointly:

```bash
# Boltz-1
boltz predict input.yaml --output_dir boltz1_out/

# Chai-1
chai-lab predict input.fasta --output-dir chai_out/
```

**Boltz-1 / Chai-1 caveats:** Both accept MSA but treat ligand in pocket as constraints; output is the full complex structure. Ligand pose quality matches PoseBusters benchmarks in the table above.

## Per-Tool Failure Modes

### DiffDock-L -- PB-invalid poses

**Trigger:** Default DiffDock-L output.

**Mechanism:** Diffusion lacks explicit physical-plausibility term; ~50% of poses fail planarity, vdW overlap, or chirality tests.

**Symptom:** Poses look reasonable in 2D depiction but fail QC.

**Fix:** Always apply PoseBusters filter; rescore with GNINA.

### Boltz-2 -- poor affinity for novel chemotype

**Trigger:** Ligand chemotype outside ChEMBL training distribution.

**Mechanism:** Affinity head trained on public bioactivity data; extrapolation is unreliable.

**Symptom:** Predicted pIC50 far from experimental; uncertainty band very wide.

**Fix:** Use Boltz-2 for first-pass triage only; FEP for top hits.

### EquiBind -- worst accuracy

**Trigger:** Default EquiBind without ensemble.

**Mechanism:** Single-shot equivariant network; no refinement step.

**Symptom:** Poses within RMSD > 5 Å.

**Fix:** Avoid EquiBind; use DiffDock-L or Boltz-1 for sampling, then refine with GNINA.

### AlphaFold3 -- restricted API

**Trigger:** Academic users without commercial agreement.

**Mechanism:** AF3 server requires Google Cloud account + quota.

**Symptom:** Cannot submit jobs; rate-limited.

**Fix:** Use Boltz-1 (open source) for similar performance; AF3 only for cross-validation.

### ML methods ignore cryptic pockets

**Trigger:** Binding site not in receptor conformation.

**Mechanism:** ML methods score poses against static receptor.

**Symptom:** All poses report poor affinity; known active missed.

**Fix:** Pre-generate receptor ensemble via MD or use AlphaFold3 holo prediction.

## Reconciliation: ML vs Classical

| Aspect | Classical (Vina/GNINA) | ML (DiffDock/Boltz) |
|--------|------------------------|---------------------|
| Pose RMSD | 60-70% within 2 Å | 50-77% within 2 Å |
| PB-validity | 85-90% | 40-70% |
| Affinity accuracy | Correlates ~0.5 with exp | Boltz-2 ~0.66 Pearson on benchmark |
| Speed | 5-30s/lig | 5-10s GPU |
| Out-of-distribution | Robust for chemotypes | Worse for novel scaffolds |
| Interpretability | Force-field based | Black-box |

**Production hybrid:** ML for pose sampling (broader search), classical for affinity + physical validation.

## Common Errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Boltz-2 OOM on big protein | MSA + ligand fits in 16GB | Reduce MSA depth; use Boltz-1 |
| DiffDock all poses cluster | Insufficient samples | Increase `samples_per_complex` to 40-100 |
| Boltz output not a single chain | Tokenizer confused by modified residues | Strip non-standard residues; use UniProt canonical |
| GNINA can't read DiffDock output | SDF missing 3D | DiffDock writes 3D SDF; verify with PyMOL |
| Chai-1 ignores pocket | Wrong binding-site hint | Pass `--pocket-residues` if available |

## References

- Corso et al., *Nat. Mach. Intell.* -- DiffDock-L.
- Wohlwend et al., 2024 -- Boltz-1; 2025 -- Boltz-2 with affinity.
- Buttenschoen et al., *Chem. Sci.* 15:3130 -- PoseBusters benchmark.
- McNutt et al., *J. Cheminformatics* 13:43 -- GNINA 1.0 CNN.
- Krishna et al., 2024 -- AlphaFold3 server.

## Related Skills

- chemoinformatics/virtual-screening - Classical docking
- chemoinformatics/pose-validation - PoseBusters QC
- chemoinformatics/free-energy-calculations - Post-docking FEP
- chemoinformatics/covalent-design - Covalent docking
- chemoinformatics/protac-degraders - Ternary complex prediction