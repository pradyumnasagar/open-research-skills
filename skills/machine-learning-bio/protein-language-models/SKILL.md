---

name: protein-language-models
description: "Use ESM-2, ESMFold, ProtTrans, AlphaFold 2/3, Boltz-1, RoseTTAFold and OmegaFold for protein embeddings, zero-shot mutational-effect prediction, and 3D structure prediction. Use when scoring variants without a structure, designing mutant libraries, or predicting conformations."
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

# Protein Language Models
"
> Protein language models (pLMs) treat amino-acid sequences as a "language" learned at scale from UniProt. They power three things you will do in practice: dense embeddings of arbitrary proteins, zero-shot predictions of variant effects (log-probability ratios), and (when coupled with a structure head) full 3D structure prediction. This skill picks the right model for each task, sets up the environment, and gives copy-pasteable code for the canonical workflows.

## When to use

- You need a single embedding vector per protein for clustering, retrieval, or as input to a downstream classifier.
- You want a fast, structure-free prior on missense variants (pathogenicity screening, mutational-scan design, protein engineering).
- You want to predict a 3D structure and you have either (a) a good MSA from UniClust/UniRef/metagenomics, or (b) you are willing to use Boltz-1 / ESMFold which need no MSA.
- You need to fine-tune a small ESM-2 head on a labeled set of variants, fluorescence, stability, or binding data.
- You want to query the AlphaFold Database (AFDB) for a structure before running your own prediction.

## When NOT to use

- The biological question is a single-mutation thermodynamic quantity (ΔΔG) that needs physics-level accuracy. pLMs rank variants but are not ΔΔG calculators. Combine with FoldX / Rosetta if you need kcal/mol estimates.
- The structure is a designed de novo protein whose template distribution is far from UniProt — predictions may be confidently wrong (high pLDDT, low actual accuracy).
- You only need a domain annotation. Use InterPro / Pfam HMMs (see `bioinformatics-functional` skills).
- The question is about disordered regions — pLMs generally do not handle IDRs well; AlphaFold returns low pLDDT, which is the correct answer, not a failure.

## Prerequisites

Environment:

```bash
# Core
pip install torch transformers fair-esm biotite py3Dmol
# For Boltz-1 (follow the repo for CUDA wheels)
pip install boltz  # or install from github.com/jwohlwend/boltz
# For AlphaFold 2/3 inference
git clone https://github.com/google-deepmind/alphafold3.git
# MSA search
# Install MMseqs2 (https://github.com/soedinglab/MMseqs2) for fast homology search
conda install -c bioconda mmseqs2
```

Hardware baselines (rough; verify against the model's repo):

- ESM-2 8M-150M: a single modern GPU (8 GB VRAM) is plenty for inference.
- ESM-2 650M-15B and ESMFold: ≥24 GB VRAM; ESMFold-15B is 60+ GB.
- AlphaFold 2 inference (monomer): one A100 (80 GB) for a single sequence, 2-6 hours with full MSA.
- Boltz-1: roughly 1×-2× AF2 cost; check the Boltz-1 repo for current numbers.

Conceptual prerequisites: comfortable with MSA depth / coevolution intuition, the difference between pLDDT (per-residue) and PAE (pairwise), and the idea that "log-likelihood" is a relative quantity, not an absolute fitness.

## Core workflow

### 1. Pick the model

| Task | Default model | Why |
|------|---------------|-----|
| Embedding (small) | ESM-2 150M (`facebook/esm2_t30_150M_UR50D`) | Good quality / cost ratio; HF-native |
| Embedding (best) | ESM-2 650M or 3B | Saturates retrieval benchmarks |
| Zero-shot variant effect | ESM-2 (masked-MLM pseudo log-likelihood) | Standard approach from ESM-1v / Tranception / ESM-2 papers |
| Single-sequence structure | ESMFold | No MSA needed; fast; 3B/15B tradeoffs |
| Highest-accuracy structure, MSA available | AlphaFold 2/3 or Boltz-1 | MSA-driven; AF3 also handles complexes, ligands, nucleic acids |
| Highest-accuracy structure, MSA unavailable | Boltz-1 or ESMFold | Both designed for MSA-free or MSA-augmented regimes |
| Designed de novo scaffolds | RoseTTAFold All-Atom or RFdiffusion outputs | Outside scope; this skill stops at the inference step |

### 2. Run a baseline embedding job

```python
import torch
from transformers import AutoTokenizer, AutoModel

model_id = "facebook/esm2_t30_150M_UR50D"
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModel.from_pretrained(model_id).eval()

seqs = ["MKKAVINGEQIRSISDLHQTLKKELALPEYYGENLDALWDALTGWVEYPLVLEWR",
        "MSEQNNTEMTFIQTFADADQKLLEKKRKLELEKDKENYDKFRQKLR"]

with torch.no_grad():
    inputs = tok(seqs, return_tensors="pt", padding=True, truncation=True, max_length=1022)
    out = model(**inputs)

# Mean-pooled embedding per sequence (excluding special tokens + padding)
mask = inputs["attention_mask"].unsqueeze(-1).float()
emb = (out.last_hidden_state * mask).sum(1) / mask.sum(1).clamp(min=1)
print(emb.shape)  # (n_seqs, hidden_size)
```

### 3. Zero-shot mutational effect

The canonical recipe is the **masked-marginal pseudo-log-likelihood**: for each position, mask it, score the wildtype vs. the variant marginals, sum the log-probability differences. This is what Tranception, ESM-1v, and ESM-2 zero-shot work build on.

```python
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForMaskedLM

model_id = "facebook/esm2_t12_35M_UR50D"  # use 150M/650M for quality
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForMaskedLM.from_pretrained(model_id).eval()

AA = "ACDEFGHIKLMNPQRSTVWY"

def score_variant(seq, position, mutant_aa):
    """Return log P(mutant) - log P(wildtype) at `position`."""
    assert seq[position] != mutant_aa
    masked = list(seq)
    original_aa = masked[position]
    masked[position] = tok.mask_token
    inputs = tok("".join(masked), return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits[0, position + 1]  # +1 for CLS
    probs = F.softmax(logits, dim=-1)
    wt = tok.convert_tokens_to_ids(original_aa)
    mt = tok.convert_tokens_to_ids(mutant_aa)
    return (probs[mt] / probs[wt]).log().item()  # positive = mutant preferred

# Aggregate across all positions for a multi-mutant library
def library_score(seq, mutations):
    """mutations: list of (pos_0idx, mutant_aa)."""
    return sum(score_variant(seq, p, m) for p, m in mutations)
```

Notes:
- A positive score means the model finds the variant more probable than WT under its prior. Treat as a **ranking signal**, not a probability.
- Sum across positions is the simplest aggregate. Papers also use site-independent sums, top-k truncation, or weight by predicted structural context.
- For DMS-style benchmarks, the model is evaluated by Spearman / AUC against measured fitness — never trust absolute values.

### 4. Single-sequence structure prediction with ESMFold

```python
from transformers import AutoTokenizer, EsmForProteinFolding

# ESMFold weights are large; first download can take 1-2 GB
tok = AutoTokenizer.from_pretrained("facebook/esmfold_v1")
model = EsmForProteinFolding.from_pretrained("facebook/esmfold_v1", low_cpu_mem_usage=True)
model = model.eval().cuda() if torch.cuda.is_available() else model.eval()

with torch.no_grad():
    outputs = model.infer_pdb("MKKAVINGEQIRSISDLHQTLKKELALPEYYGENLDALWDALTGWVEYPLVLEWR")

with open("prediction.pdb", "w") as f:
    f.write(outputs)
```

For visualization in a notebook:

```python
import py3Dmol
view = py3Dmol.view(width=600, height=400)
view.addModel(open("prediction.pdb").read(), "pdb")
view.setStyle({"cartoon": {"colorscheme": "pLDDT"}})  # color by pLDDT
view.zoomTo()
view.show()
```

### 5. AlphaFold / Boltz-1 with an MSA

For AlphaFold 2/3, the heavy lift is the MSA. The community standard is **MMseqs2** in colab-style mode against UniRef + BFD / metagenomics databases.

```bash
# 1. MSA via MMseqs2 (or use the ColabFold server script locally)
python -m colabfold.batch \
    --input_dir fasta_in/ \
    --output_dir out/ \
    --num-models 5 \
    --num-recycle 3 \
    --model-type alphafold2_multimer_v3   # or auto
```

For Boltz-1:

```bash
# Boltz-1 accepts a YAML with sequences, modifications, ligands
cat > my_target.yaml <<'YAML'
sequences:
  - protein:
      id: A
      sequence: MKKAVINGEQIRSISDLHQTLKKELALPEYYGENLDALWDALTGWVEYPLVLEWR
YAML

boltz predict my_target.yaml --out_dir boltz_out --use_msa_server
```

### 6. Querying the AlphaFold Database (AFDB)

Before running your own prediction, check whether AFDB already has a structure for your UniProt accession. AFDB provides confidence metrics in the same .pdb / .cif files (B-factor = pLDDT).

```python
import requests

def afdb_pdb(uniprot_acc):
    """Download AFDB predicted PDB by UniProt accession."""
    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_acc}-F1-model_v6.pdb"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text

pdb = afdb_pdb("P53_HUMAN".replace("_", ""))  # example; use real accession e.g. P04637
# or download the CIF with /files/AF-<ACC>-F1-model_v6.cif
```

For programmatic queries of AFDB / EBI's API, see the EBI AlphaFold endpoint documentation. Bulk downloads: `https://ftp.ebi.ac.uk/pub/databases/alphafold/`.

### 7. Fine-tuning a small head

Common pattern: freeze ESM-2 body, train a regression/classification head on labeled protein data (stability, fluorescence, binding, variant effect).

```python
import torch, torch.nn as nn
from transformers import AutoModel

backbone = AutoModel.from_pretrained("facebook/esm2_t12_35M_UR50D")
for p in backbone.parameters():
    p.requires_grad = False

class ESM2Regressor(nn.Module):
    def __init__(self, hidden=480, n_out=1):
        super().__init__()
        self.body = backbone
        self.head = nn.Sequential(nn.Linear(hidden, hidden), nn.ReLU(), nn.Linear(hidden, n_out))
    def forward(self, input_ids, attention_mask):
        h = self.body(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
        m = attention_mask.unsqueeze(-1).float()
        pooled = (h * m).sum(1) / m.sum(1).clamp(min=1)
        return self.head(pooled).squeeze(-1)

model = ESM2Regressor()
# Train with standard PyTorch loop; bf16 mixed precision is usually a win.
```

For larger training runs, use LoRA via `peft` instead of full unfreezing.

## Code patterns

### Parse a PDB and pull pLDDT from B-factor

```python
from biotite.structure.io.pdb import PDBFile

def mean_plddt(pdb_path):
    s = PDBFile.read(pdb_path).get_structure(model=1)
    # pLDDT is stored in B-factor in AF / ESMFold outputs
    return float(s.b_factor.mean())

def per_residue_plddt(pdb_path):
    s = PDBFile.read(pdb_path).get_structure(model=1)
    return {r.res_id: float(r.b_factor) for r in s if r.atom_name == "CA"}
```

### PAE / pLDDT interpretation rules of thumb

- pLDDT > 90: very high confidence (backbone trace reliable).
- 70 < pLDDT < 90: confident; usually correct.
- 50 < pLDDT < 70: low confidence; treat as a "could be anything" prediction.
- pLDDT < 50: likely disordered — the model is telling you "do not trust the coordinates".
- PAE: low PAE (≤ 5 Å) between two residues → they are confidently placed relative to each other. A domain with low pLDDT but low intra-domain PAE is still a well-defined ensemble of conformations.

### Batch embedding without OOM

```python
def embed_in_chunks(seqs, model, tok, batch_size=8, max_len=1022):
    out = []
    for i in range(0, len(seqs), batch_size):
        chunk = seqs[i:i+batch_size]
        enc = tok(chunk, return_tensors="pt", padding=True, truncation=True, max_length=max_len)
        with torch.no_grad():
            h = model(**enc).last_hidden_state
        m = enc["attention_mask"].unsqueeze(-1).float()
        pooled = (h * m).sum(1) / m.sum(1).clamp(min=1)
        out.append(pooled.cpu())
    return torch.cat(out, dim=0)
```

## Common pitfalls

- **Treating zero-shot scores as probabilities.** They are not. Calibrate on a known-positive / known-negative set if you need a threshold.
- **Mean-pooling with padding tokens.** Always mask before mean-pool; otherwise short sequences are biased toward whatever padding the tokenizer adds.
- **Confusing embedding similarity with functional similarity.** Two proteins can have near-identical ESM-2 embeddings and completely different functions, especially for short motifs.
- **Trusting a single AlphaFold model.** Run ≥3 seeds and check pLDDT/PAE. A single prediction with a confident-looking cartoon can still be wrong; use the spread as a diagnostic.
- **MSA contamination.** A near-identical PDB hit in the MSA biases AF2/3. Remove very close templates for *de novo* designs.
- **Long proteins.** ESM-2 context is 1022 residues (positions + specials). For longer proteins, use sliding windows or split into domains.
- **Mixing up AF2 monomer / multimer flags.** Multimer inference is more expensive and uses different model weights; do not run a multimer job on a monomer.
- **Boltz-1 confidence interpretation.** Boltz-1 reports its own confidence score; the absolute numbers are not directly comparable to AF2 pLDDT.

## Validation

- For embeddings: check a known homologous family clusters together (UMAP / t-SNE) and a shuffled sequence is far from its parent.
- For zero-shot variant effects: hold out a ProteinGym DMS assay, compute Spearman, compare to published baselines.
- For ESMFold / AF / Boltz: run on a target with a known experimental structure (e.g. a monomer from the PDB whose structure is not in the training MSA) and compute TM-score / RMSD. Anything over ~70% confident on a >50-residue known fold should land within ~3 Å Cα RMSD.
- For fine-tuning: split by sequence identity (MMseqs2 cluster at 30–50% identity), never random-split.
- For AFDB queries: confirm the downloaded model matches the UniProt canonical isoform; AFDB has fragments and isoform-specific entries.

## Open alternatives

- AlphaFold 3 and Boltz-1 are the open-weights defaults for the highest-accuracy regime.
- ESMFold replaces AlphaFold 2's MSA module with a single-sequence pLM head — open, fast, and license-friendly.
- For designed proteins / de novo backbones, RoseTTAFold All-Atom and RFdiffusion (Baker lab) are the open counterparts to commercial design tools.
- The `fair-esm` package (Meta) is fully open. `transformers` (Hugging Face) hosts the same ESM-2 checkpoints with a more conventional API.
- For MSA generation: ColabFold's `colabfold_batch` script is the open standard; the AlphaFold Server (DeepMind-hosted) is a closed alternative that hides MSA generation behind a web UI.

## References

- Lin et al., 2023 — ESM-2 (Meta AI). See the ESM GitHub repo: `facebookresearch/esm`.
- Rives et al., 2021 — ESM-1b / single-protein language models (predecessor; widely cited for biological findings).
- Jumper et al., 2021, *Nature* — AlphaFold 2. Repo: `google-deepmind/alphafold`.
- Abramson et al., 2024, *Nature* — AlphaFold 3. Repo: `google-deepmind/alphafold3`.
- Wohlwend et al., 2024 — Boltz-1. Repo: `jwohlwend/boltz`.
- Baek et al., 2021 — RoseTTAFold (Baker lab).
- Wu et al., 2022 — OmegaFold (HeliXon).
- Varadi et al. — AlphaFold Database (EMBL-EBI). `https://alphafold.ebi.ac.uk`.
- Notin et al. — ProteinGym benchmarks for variant-effect prediction.
- Steinegger & Söding — MMseqs2 (used as the canonical MSA backend).
- Mirdita et al. — ColabFold (MSA + AF2 inference pipeline).

## Related Skills

- `machine-learning-bio/alphafold-structure-prediction` — deep dive on AF2/3 / Boltz-1 inputs, pLDDT/PAE, multimer
- `machine-learning-bio/scrnaseq-deep-learning` — scVI / scGPT / Geneformer (complementary domain models)
- `chemoinformatics/molecular-descriptors` — small-molecule embedding counterpart
- `scientific-computing/...` — GPU sizing and inference benchmarking

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from Meta ESM docs, AlphaFold papers, and Boltz-1 repo; added HuggingFace-native patterns, fine-tuning recipe, AFDB query patterns, and zero-shot variant-effect loop.