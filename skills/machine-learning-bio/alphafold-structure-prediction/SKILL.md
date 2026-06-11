---

name: alphafold-structure-prediction
description: "Run AlphaFold 2/3 and Boltz-1 for protein structure prediction, including MSA generation with MMseqs2/JackHMMER, pLDDT/PAE interpretation, multimer prediction, and querying the AlphaFold Database (AFDB)."
license: MIT
---




<!-- metadata:
category: machine-learning-bio
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - machine-learning-bio
  - research
difficulty: intermediate
-->

# AlphaFold & Boltz-1 Structure Prediction

> Modern protein structure prediction runs in two stages: build a deep multiple-sequence alignment (MSA) capturing evolutionary covariation, then feed it to AlphaFold 2/3 or Boltz-1. This skill walks you through both, the differences between models, how to interpret the confidence outputs (pLDDT, PAE), and how to query the AlphaFold Database (AFDB) before running your own prediction. It also covers the practical pitfalls that distinguish a confident structure from a confidently-wrong one.

## When to use

- You have a protein sequence and need a structural model (monomer or multimer).
- You need to evaluate a de novo or engineered design (after backbone generation, before wet-lab validation).
- You want to score conformational change between two states and have an MSA.
- You need a structural prior for downstream MD, docking, or functional annotation.
- You want to build a protein–ligand or protein–nucleic-acid complex model (AF3 / Boltz-1 handle this; AF2 monomer-only).

## When NOT to use
"
- The protein is fully disordered and remains disordered under all conditions — AF returns a low-pLDDT "ribbon" which is correct, not a failure; do not interpret it as a fold.
- The mutation of interest is in a disordered region and you care about the structural effect — AF2/3 are not ΔΔG predictors.
- You have high-resolution cryo-EM or X-ray data — use experimental coordinates, not predictions.
- The target is a small molecule. Use docking (Vina, DiffDock) or chemoinformatics tools, not a protein structure predictor.
- The sequence is from a very divergent organism with no relatives in UniRef / BFD / metagenomics — MSA depth will be insufficient, and AF will degrade gracefully but with low confidence. Switch to a single-sequence pLM-based predictor (ESMFold) for a sanity check.

## Prerequisites

```bash
# AlphaFold 3 — install from official repo
git clone https://github.com/google-deepmind/alphafold3.git
# Follow the repo's install instructions; weights require acceptance of license

# AlphaFold 2 — install via Docker (recommended)
docker pull google-deepmind/alphafold

# Boltz-1 — install from source
git clone https://github.com/jwohlwend/boltz.git
cd boltz && pip install -e .

# MSA search
# MMseqs2 (fast, default for colabfold)
conda install -c bioconda mmseqs2

# HHblits / JackHMMER (alternative MSA backends)
conda install -c bioconda hhsuite
conda install -c bioconda jackhmmer

# Downstream analysis
pip install biotite py3Dmol
```

Hardware baselines (rough; verify against each repo):

- AlphaFold 2 monomer, full MSA, recycling=3: a single A100 80 GB takes 2-6 hours per sequence.
- AlphaFold 2 multimer: 1.5–2× monomer cost.
- AlphaFold 3: roughly comparable to AF2 multimer; complex size scales cost.
- Boltz-1: usually faster than AF2/3; can fit shorter proteins on a single 24 GB GPU.
- MMseqs2 MSA generation: CPU-bound; 1-15 minutes for a typical protein.

Conceptual prerequisites: understand that MSA depth is the dominant driver of AF2/3 accuracy, pLDDT is a per-residue self-assessment (calibrated but not perfect), and PAE is the only useful signal for *relative* domain placement.

## Core workflow

### 1. Decide which model to use

| Task | Default |
|------|---------|
| Monomer, deep MSA available | AlphaFold 2/3 or Boltz-1 |
| Monomer, no / shallow MSA | ESMFold or Boltz-1 (`--use_msa_server` off) |
| Multimer (protein-protein) | AlphaFold 2 multimer or AlphaFold 3 |
| Multimer with nucleic acid or ligand | AlphaFold 3 or Boltz-1 (closed AlphaFold 3 server is the only full option for some modifications) |
| Bulk predictions (hundreds of proteins) | ColabFold batch + Boltz-1 |
| Replacement of PDB hit in MSA | Strip near-identical templates from MSA (`--max_template_date`) |

If you only need a quick sanity check and have no MSA: ESMFold (see `protein-language-models` skill). If you have a deep MSA and care about confidence: AlphaFold.

### 2. Check the AlphaFold Database first

Always check whether AFDB already has a structure for your UniProt accession. AFDB contains many millions of predicted structures, each with a per-residue pLDDT and PAE.

```python
import requests

def afdb_pdb(uniprot_acc, model_version="v6"):
    """Download AFDB PDB by UniProt accession (canonical isoform)."""
    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_acc}-F1-model_{model_version}.pdb"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

# Example: download the canonical human p53
pdb_text = afdb_pdb("P04637")
with open("p53_afdb.pdb", "w") as f:
    f.write(pdb_text)
```

Notes:
- The accession must be the canonical UniProt accession (not a secondary ID or isoform). Use the `accession` field from UniProt's API.
- Bulk downloads: `https://ftp.ebi.ac.uk/pub/databases/alphafold/`.
- Confidence is encoded in the B-factor (CA, CB, etc.) of the PDB — `pLDDT = B-factor` for AFDB models.

### 3. Generate an MSA with MMseqs2 (the ColabFold approach)

This is the standard fast path. It searches UniRef + BFD / metagenomics and returns a3m-formatted MSAs.

```bash
# Single sequence search via colabfold_batch
colabfold_batch \
    --input_dir fasta_in/ \
    --output_dir out_msa/ \
    --num-msa 256 \
    --num-extra-ssa 512 \
    --pair-mode unpaired
```

For batch runs on a cluster, wrap this in a job script. MMseqs2 is CPU-bound; a typical protein (200-500 aa) finishes in 5-15 minutes on a single core. For large metagenomics databases, plan for 30+ minutes.

### 4. AlphaFold 2/3 inference

AlphaFold 3 is the modern default for new work. Its input format is a YAML file describing sequences, modifications, and ligands.

```yaml
# AF3 input example
sequences:
  - protein:
      id: A
      sequence: MKKAVINGEQIRSISDLHQTLKKELALPEYYGENLDALWDALTGWVEYPLVLEWR
  - protein:
      id: B
      sequence: MGSKMSTAAVSHPLSSSSGFGSSSSGNSPNSVFKRGGSGGGSSVHNMDLDYPLTGSGSGGSD...

# Optional: ligand
# - ligand:
#     id: G
#     smiles: "CC(=O)Oc1ccccc1C(=O)O"
```

```bash
# Run AlphaFold 3
python run_alphafold.py \
    --json_path input.json \
    --model_dir $AF3_MODEL_DIR \
    --output_dir out/ \
    --db_dir $ALPHAFOLD_DB_DIR
```

For AlphaFold 2 in Docker:

```bash
docker run \
    -v /path/to/alphafold_dbs:/data/db \
    -v /path/to/fasta_in:/data/inputs \
    -v /path/to/out:/data/outputs \
    google-deepmind/alphafold \
    --data_dir=/data/db \
    --fasta_paths=/data/inputs/my_protein.fasta \
    --model_preset=monomer \
    --max_template_date=2024-01-01
```

### 5. Boltz-1 inference

Boltz-1 is faster than AF2/3 and handles the same complex scenarios. It also has a `--use_msa_server` mode that submits to a hosted MSA server (free for non-commercial use, check the repo).

```bash
cat > my_target.yaml <<'YAML'
sequences:
  - protein:
      id: A
      sequence: MKKAVINGEQIRSISDLHQTLKKELALPEYYGENLDALWDALTGWVEYPLVLEWR
YAML

boltz predict my_target.yaml --out_dir boltz_out --use_msa_server
```

Boltz-1 confidence output:
- A model confidence score per residue (analogous to pLDDT; not directly numerically equivalent).
- Pairwise PAE matrix in `.npz` form.
- See the Boltz-1 README for the exact file layout — it changes between versions.

### 6. Interpret pLDDT and PAE

**pLDDT (per-residue):**
- > 90: very high confidence; backbone trace and side-chain orientation reliable.
- 70-90: confident; usually correct but side chains may be off.
- 50-70: low confidence; treat as a rough model.
- < 50: likely disordered — the model is reporting "I do not know"; do not interpret as a real fold.

**PAE (pairwise):**
- Low PAE between two regions means they are placed relative to each other confidently.
- High PAE (>= 20 Å) between domains means relative orientation is uncertain — the model has placed each domain correctly but their connection is not.
- A "L"-shaped PAE matrix with a low block on the diagonal is the classic pattern: each domain is well-folded but their relative orientation is not.

```python
import numpy as np

def interpret_pae(pae):
    """Return mean off-diagonal PAE (domain-coupling confidence)."""
    n = pae.shape[0]
    off = pae - np.diag(np.diag(pae))  # zero diagonal
    return float(off.sum() / (n * (n - 1)))
```

### 7. Multimer / complex prediction

For AF2 multimer, set `--model_preset=multimer`. Run multiple seeds (≥5) and cluster the predicted interfaces — the model is stochastic. Confidence comes from `ipTM` (interface predicted TM-score), not the per-residue pLDDT.

For AF3 / Boltz-1, declare all chains in the input YAML and set the same model preset. The PAE is the most informative plot: a low-PAE block between two chain IDs means a confident interface.

### 8. Validate the result

- Compute pLDDT distribution: if your average pLDDT is < 70, the prediction is uninformative.
- Visualize PAE: if it is "all red" (high PAE everywhere), the model is uncertain.
- Compute MolProbity / clash score: predicted structures can have steric clashes that you must clean up before using them in MD or docking.
- If the predicted structure disagrees with a known template (e.g. an AlphaFold prediction disagrees with a solved crystal structure), the experimental structure wins. Predictions are priors, not facts.
- For multimer, compute the interface TM-score (iTM) and dockQ if you have a reference.

## Code patterns

### Parse pLDDT and PAE from an AF2 output

```python
import json
import numpy as np

def load_af2_confidence(output_dir, model_idx=0):
    """AF2 outputs: 'ranking_debug.json' has iptm+ptm, 'pae' folder has PAE per model."""
    with open(f"{output_dir}/ranking_debug.json") as f:
        rank = json.load(f)
    # 'iptm' is interface TM, 'ptm' is global TM, 'ranking_confidence' is the rank metric
    pae = np.load(f"{output_dir}/predicted_aligned_error_v1/model_{model_idx + 1}.npz")["pae"]
    return rank["iptm+ptm"], pae
```

### Build a quick PAE heatmap

```python
import matplotlib.pyplot as plt

def plot_pae(pae, chain_breaks=None):
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(pae, cmap="bwr", vmin=0, vmax=30, origin="lower")
    if chain_breaks:
        for b in chain_breaks:
            ax.axvline(b, color="black", lw=0.5)
            ax.axhline(b, color="black", lw=0.5)
    plt.colorbar(im, label="PAE (Å)")
    plt.title("Predicted Aligned Error")
    return fig
```

### Strip near-identical templates for a *de novo* design

```bash
# In colabfold_batch / AF2, set --max_template_date to a date before any near-template
# exists, OR provide an empty --template_dir
colabfold_batch \
    --input_dir fasta_in/ \
    --output_dir out/ \
    --max_template_date 2020-01-01 \
    --templates_off
```

### Strip PDB hits from MSA before AF2 inference (rare but useful for fair tests)

```python
def filter_msa_to_no_pdb_hits(a3m_path, pdb_hits, output_path):
    with open(a3m_path) as f:
        lines = f.readlines()
    keep = []
    header, seq = None, None
    for line in lines:
        if line.startswith(">"):
            if seq is not None and header not in pdb_hits:
                keep.append(header)
                keep.append(seq)
            header = line
            seq = ""
        else:
            seq += line
    with open(output_path, "w") as f:
        f.writelines(keep)
```

## Common pitfalls

- **MSA contamination for *de novo* design.** A near-identical PDB hit biases AF heavily. Strip templates and consider removing very close homologs.
- **Treating pLDDT as "accuracy".** pLDDT is the model's predicted IDR / fold likelihood, not the actual RMSD to ground truth. Highly disordered regions can have pLDDT < 50 and that is correct.
- **Reading the B-factor as something other than pLDDT.** For AF2/3 / Boltz-1 outputs, B-factor = per-residue confidence. For ESMFold, same convention. For experimental PDBs, B-factor is the experimental B-factor.
- **Using a monomer preset for a complex.** AF2 monomer will fold each chain independently and ignore the complex. Use multimer.
- **Multimer interface confidence is `ipTM`, not pLDDT.** A high pLDDT chain with low ipTM is a confident monomer with no confident complex.
- **Forgetting to set recycling depth.** Recycling > 1 lets the model refine; for "default" runs, recycling=3 is the standard.
- **MSA depth collapse.** A sequence from a divergent organism with shallow MSA will degrade all models. Switch to ESMFold or relax the E-value threshold.
- **Disordered regions.** Both AF and Boltz-1 return pLDDT < 50 for disordered tails / linkers. Do not interpret the coordinates.

## Validation

- **Run on a known target.** If you have an experimental structure for a similar protein, run AF on the same sequence and compute TM-score to the experimental structure. The closer to the truth, the higher the TM-score.
- **Confidence consistency.** Run 3-5 seeds. If pLDDT and PAE are stable across seeds, the model is confident. If they diverge, the model is uncertain.
- **Sanity check the secondary structure.** Predict the secondary structure independently (PSIPRED) and compare. If the predicted helix/sheet pattern agrees, you have a working model.
- **Use a different chain pair for multimer.** Run the multimer twice with different chain orderings; if the interface differs, the model is not confident about which way the complex forms.
- **Cross-check with ESMFold.** A high-ESMFold-pLDDT region that is low in AF (or vice versa) is a useful diagnostic. Sometimes a region is foldable in isolation but not in the full protein context.

## Open alternatives

- **AlphaFold 2/3 vs. Boltz-1:** AF is the reference; Boltz-1 is faster, simpler to install, and has comparable accuracy on monomers but a less mature code base.
- **RoseTTAFold All-Atom (RFAA):** From the Baker lab; handles complexes and modifications with a different model architecture.
- **OmegaFold:** Single-sequence pLM-based predictor; open, fast, no MSA required.
- **ESMFold:** Single-sequence pLM-based; open, fast, easier to deploy than AF; lower peak accuracy but a strong MSA-free baseline.
- **Chai-1:** Another open structure predictor with strong benchmark performance. Check the latest benchmarks before committing to a single tool.
- **Closed alternative:** AlphaFold Server (DeepMind-hosted) — web UI only, free for academic use, no command-line control.

## References

- Jumper et al., 2021, *Nature* — AlphaFold 2 (the landmark). See the AF2 repo.
- Abramson et al., 2024, *Nature* — AlphaFold 3 (architecture, training, performance). Repo: `google-deepmind/alphafold3`.
- Wohlwend et al., 2024 — Boltz-1. Repo: `jwohlwend/boltz`.
- Baek et al., 2021, *Science* — RoseTTAFold (Baker lab).
- Wu et al., 2022 — OmegaFold (HeliXon).
- Varadi et al. — AlphaFold Database (EMBL-EBI). `https://alphafold.ebi.ac.uk`.
- Steinegger & Söding — MMseqs2 (the canonical MSA backend).
- Mirdita et al. — ColabFold (the canonical AF2 + MSA pipeline).
- Mirdita et al., 2022 — `py3Dmol` (the canonical web-friendly structure viewer).

## Related Skills

- `machine-learning-bio/protein-language-models` — ESM-2 / ESMFold (single-sequence predictor) and embedding extraction
- `structural-biology/...` — companion skills for structure I/O, MD, docking
- `chemoinformatics/docking-rescoring` — using predicted structures as receptor inputs for docking

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from Jumper et al. 2021, Abramson et al. 2024, the Boltz-1 repo, and ColabFold docs; added multimer guidance, AFDB query patterns, validation rubric, and confidence-interpretation rules of thumb.