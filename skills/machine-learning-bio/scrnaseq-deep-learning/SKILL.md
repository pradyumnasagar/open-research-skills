---
name: scrnaseq-deep-learning
description: "Use scVI, scANVI, totalVI, scGPT, Geneformer, and scFoundation for single-cell"
license: MIT
---



<!-- metadata:
category: machine-learning-bio
version: 1.0.0
author: Pradyumna Jayaram
tags:
- scvi
- scgpt
- geneformer
- scrnaseq
- batch-correction
- foundation-model
difficulty: intermediate
prerequisites:
  tools:
  - python
  - scanpy
  - scvi-tools
  - torch
  - torch-geometric
  - transformers
  skills: []
sources: 'Original: scVI (Lopez et al. 2018); Adapted: foundational scRNA-seq VAE
  patterns, batch correction workflow; Original: scGPT (Liu et al. 2023); Adapted:
  transformer embedding for downstream tasks; Original: Geneformer (Theodoris et al.
  2023); Adapted: gene expression foundation model fine-tuning; Original: scFoundation
  (Zhao et al. 2023); Adapted: multi-scale architecture, evaluation framework; Improvisions:
  GPU sizing guide, evaluation metric choice, perturbation prediction workflows'
-->

# Deep Learning for scRNA-seq

> Deep learning models treat single-cell RNA-seq as a dimensionality reduction, batch correction, or transfer learning problem. This skill covers the canonical architectures: VAEs (scVI, scANVI) for count data, transformers (scGPT, Geneformer, scFoundation) as sequence/attention priors, and latent-space models for integration and batch correction. It matches the model to your task and gives you a working training pipeline plus validation.

## When to use

- You have 5–10 scRNA-seq batches from different conditions or experiments and need a corrected, batch-integrated expression matrix for joint analysis.
- You have one highly labeled dataset (e.g., 10x Genomics PBMC with cell-type labels) and want to predict labels on a new, unlabeled dataset (label transfer).
- You have perturbation data (drug, CRISPR, genotype) and want to predict the expression of the perturbation from a baseline.
- You have 100+ cells and want to use foundation model embeddings (from scGPT or Geneformer) as input to a downstream classifier for a rare cell type.
- You need to predict RNA velocity but the spliced / unspliced counts are too sparse or noisy for standard scVelo.

## When NOT to use

- You have a pure visualization goal (UMAP / t-SNE). Use Scanpy or Seurat with standard PCA on HVGs; no need to train a model.
- You only need clustering / annotation. Graph-based clustering (Louvain / Leiden on kNN-UMAP) is sufficient and faster.
- You are doing differential expression (DE) between two conditions. Use DESeq2 or edgeR (they assume counts are Poisson/negative binomial and are calibrated); scVI's DE is not calibrated to statistical thresholds.
- You are inferring trajectory; standard RNA velocity is the established baseline. Deep learning extensions are not yet routine for primary use cases.
- You have <100 cells. Deep models need statistics; use BBKNN or Seurat's method for small experiments.

## Prerequisites

```bash
# Core scRNA-seq ecosystem
pip install scanpy scvi-tools

# scVI and friends
pip install scvi-tools[extra]  # includes scvi-tools dependencies

# Transformers for Geneformer / scGPT
pip install transformers torch-geometric

# Optional but useful for full model pipeline
pip install torch lightning-pytorch

# GPU check"
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
```

Hardware baselines (rough; verify against each repo):

- scVI fine-tuning (10k cells, ~20k genes): 8–16 GB VRAM.
- scGPT embedding extraction (full transformer): 24–40 GB VRAM.
- Geneformer (base model): 32 GB+ VRAM.
- Multi-batch training (50k cells): 32 GB+ VRAM.

Conceptual prerequisites: know that a gene count matrix is a high-dimensional noisy observation (like a document in bag-of-words NLP), and a batch effect is a non-biological covariate that a deep model can learn to regress out. Foundation models pre-train on the entire transcriptome; fine-tuning on your small labeled set works because the model already knows genes co-express at cell-type level.

## Core workflow

### 1. Pick the model

| Task | Default model | Why |
|------|---------------|-----|
| Batch correction / integration | scVI / scANVI | VAE + known batch covariates; designed for this |
| Label transfer | scANVI (with a labeled dataset) | Transferable latent space |
| Cell type annotation | scANVI / scFoundation | Classifier on latent space + cell-type embeddings |
| Perturbation prediction | scVI (as autoencoder), scGPT | Autoencoder to predict perturbed state from baseline |
| Gene expression foundation model | Geneformer / scGPT | Transformer language model trained on >1M cells |
| Visualization-quality embeddings | scVI latent space / scGPT geneformer-CLS | Often better than PCA |
| Gene clustering / co-expression | scGPT geneformer-attention | Attention scores = gene-gene relationships |

### 2. Prepare the input Scanpy AnnData object

A deep model runs on a normalized count matrix (not raw counts) and assumes a common gene set across batches.

```python
import scanpy as sc

# Basic QC: quality control for each dataset in the multi-batch case
def standard_qc(adata):
    adata.var['mt'] = adata.var_names.str.startswith('MT-')  # mitochondrial genes
    adata.var['ribo'] = adata.var_names.str.startswith(('RPS', 'RPL'))  # ribosomal
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt', 'ribo'], percent_top=None, log1p=False, inplace=True)
    adata = adata[adata.obs.pct_counts_mt < 20, :]  # filter high MT
    adata = adata[adata.obs.n_genes_by_counts > 200, :]  # filter low gene cells
    return adata

# Normalization (total-count normalize, log1p) before training
def normalize_adata(adata):
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    # Choose highly variable genes (HVGs) to improve signal-to-noise
    sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
    adata = adata[:, adata.var.highly_variable]
    return adata
```

### 3. Train scVI for batch correction

scVI is the canonical VAE model; it learns a latent space that pools gene expression across biological variation but removes batch effects by conditioning on the batch index.

```python
import scvi
from scanpy import AnnData

# Basic training
model = scvi.model.SCVI(
    adata,
    n_hidden=128,
    n_latent=30,
    gene_likelihood="nb",
    latent_distribution="normal",
    # If you have batch labels:
    # batch_key="batch"  # name of obs column with batch indices
)
model.train(
    max_epochs=300,
    use_gpu=True,
    batch_size=256,
    early_stopping=True,
    check_val_every_n_epoch=10
)

# Encode (get corrected expression)
latent = model.get_latent_representation()
adata.obsm["X_scVI"] = latent

# Save / load
model.save("scVI_model.pth")
model = scvi.model.SCVI.load("scVI_model.pth", adata)
```

For scANVI (the successor with hierarchical priors), the pattern is similar but uses `scvi.model.SCANVI` and often includes a classifier on the latent space.

### 4. scGPT foundation model training

scGPT treats gene expression as a language: each cell is a document, each gene is a word. It's a transformer architecture with masked language modeling.

```python
import scgpt  # pip install scgpt

# Pre-trained or train your own
model = scgpt.SCGPT.load_pretrained("species-Human")  # or Human or Mus_musculus

# Fine-tune on your dataset
model.train(
    adata,
    max_epochs=100,
    batch_size=128,
    # Include batch information for context
    batch_key="batch",
    # Only train the adapter layers or unfreeze certain layers
    freeze=True,
    lr=1e-4
)

# Extract embeddings for downstream classification
adata.obsm["X_scGPT"] = model.get_embeddings(adata)
```

### 5. Geneformer fine-tuning

Geneformer is the foundation model pre-trained on 30M cells; it uses a standard transformer architecture.

```python
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

# Geneformer pre-trained model
model_id = "bert-base"  # but see geneformer repo for actual ID
model = AutoModelForMaskedLM.from_pretrained(model_id)
# You may need geneformer's own tokenizer
# from geneformer import GeneformerTokenizer
# tok = GeneformerTokenizer.from_pretrained("gennomer/geneformer")

# Tokenization: pad all cells to the same length or use truncation
def tokenize_for_geneformer(adata, max_len=1000):
    # Each gene index becomes a token; pad to max_len
    cell_tokens = adata.X.argmax(axis=1).tolist()  # pseudocode; adjust as needed
    return tok(cell_tokens, padding="max_length", truncation=True, max_length=max_len)

# Training loop: this will vary; check the Geneformer papers for exact architecture
# Typically: fine-tune the CLS token or last hidden state on cell-type classification
```

### 6. Label transfer from a reference atlas

scANVI is optimized for this scenario: you train on a reference atlas with cell types, then project new cells onto the same latent space and predict.

```python
# Use ScanVI to train on a reference atlas (e.g., Human Cell Atlas)
model = scvi.model.SCANVI(
    ref_adata,
    labels_key="cell_type",  # reference cell-type labels
    unlabeled_category="unlabeled"  # new datasets will be unlabeled
)
model.train()

# Load a new dataset and project
adata = scvi.data.read("new_dataset.h5ad")
adata.obs["cell_type"] = "unlabeled"
model.setup_anndata(adata)  # setup for inference only
latent = model.get_latent_representation(adata)
# Predict cell types
cell_types = model.predict(adata)
```

### 7. Evaluate batch correction

The standard quantitative metric is **ASW (Average Silhouette Width)** between batches in the latent space:

- Good ASW (~0.8–0.9): batches are well separated in biological, not batch-driven, space.
- Poor ASW (~0.4): batches are still batch-driven; the model failed to learn biological variation.

```python
from sklearn.metrics import silhouette_score
import numpy as np

def evaluate_batch_correction(adata, batch_key, use_rep="X_scVI"):
    """Compute ASW for batch in the specified representation."""
    batches = adata.obs[batch_key].astype("category").cat.codes
    # Use only the HVGs for ASW
    emb = adata.obsm[use_rep]
    emb = emb[:, adata.var.highly_variable]
    return silhouette_score(emb, batches)
```

Qualitative: UMAP / t-SNE plots should cluster by cell type, not batch.

## Code patterns

### Train with validation split

```python
from scvi import data
import numpy as np

# Split training / validation
n_cells = adata.n_obs
n_train = int(n_cells * 0.8)
ix = np.arange(n_cells)
np.random.shuffle(ix)
adata_train = adata[ix[:n_train], :].copy()
adata_val = adata[ix[n_train:], :].copy()

# Reformat for scVI (single AnnData)
adata = adata_train.concatenate(adata_val)
adata.obs['is_train'] = ['train'] * len(adata_train) + ['val'] * len(adata_val)

# Train
model = scvi.model.SCVI(adata)
model.train(
    max_epochs=300,
    use_gpu=True,
    batch_size=256,
    check_val_every_n_epoch=10,
    # callbacks can include early stopping
)
```

### Classify on latent space

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Split in latent space
X = adata.obsm["X_scVI"]
y = adata.obs["cell_type"].astype('category')
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train a classifier on the corrected expression
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
score = clf.score(X_test, y_test)
print(f"Accuracy: {score:.3f}")
```

### Foundation model downstream analysis

```python
# Differential gene expression using foundation model embeddings
# Treat gene expression as a language task: are the tokens for this gene different
# between conditions in the attention heads?

# Use the attention patterns to find co-expressed genes
# Example: aggregate attention across all cells for gene pair (i,j)
# High attention -> co-expressed

def coexpressed_genes(model, gene_i, n_return=10):
    """Find genes co-expressed with gene_i using attention weights."""
    # This varies by model; see model-specific doc for attention extraction
    attn_weights = model.get_attention_weights_for_gene(gene_i)
    genes = sorted(zip(attn_weights, model.all_genes), key=lambda x: -x[0])
    return [g[1] for g in genes[:n_return]]
```

### GPU memory saving tricks

```python
# For scVI: enable gradient checkpointing
model = scvi.model.SCVI(adata, use_gpu=True)
model._module.enable_checkpointing()  # if available; depends on version

# For large gene sets: do not train on all genes
# Standard: use top 2000 HVGs

# For Geneformer: use mixed precision training
from torch.cuda.amp import autocast
with autocast():
    outputs = model(input_ids, attention_mask)
```

## Common pitfalls

- **Training on batch labels as continuous.** scVI expects batch as a categorical index, not a continuous value. One-hot encode or use integers.
- **Using raw counts as input.** Deep models (except Geneformer / scGPT) assume normalized, log-transformed counts. Do not feed raw UMI counts directly.
- **Overfitting on small batch sizes.** If you have 5,000 cells, batch size of 256 is fine. If you have 1,000, batch size 128 may overfit; try batch size 64 and monitor training loss.
- **Forgetting that batch correction removes biological signal.** Aggressive batch correction (e.g., using the batch covariate as a strong prior) can remove real biological differences between experiments. Monitor the corrected space with known markers.
- **Geneformer-specific:** It uses a fixed vocabulary. Make sure the new dataset uses the same set of genes as the pre-trained model.
- **Not saving the model and associated transforms.** You will not be able to decode or project new cells later without the same training normalization.
- **Ignoring evaluation on a held-out batch.** When integrating multiple batches, evaluate on one that was held out of training to ensure the model generalizes.
- **Training a VAE and using it directly for DE.** VAEs are probabilistic models; the ELBO (evidence lower bound) is not a calibrated p-value. Use standard tools for DE inference.

## Validation

- **Batch metrics:** ASW, BCH (batch clustering entropy), and clustering metrics (NMI with batch labels). If these are not improved over the input space, the model failed.
- **Cell-type metrics:** If you have cell-type labels, compute accuracy or AUC on a held-out fold in the latent space. Deep models should outperform PCA-based methods.
- **Prediction metrics:** For label transfer, use held-out labels from the reference (if any) and compute accuracy on the new dataset.
- **Downstream tasks:** Test model performance (e.g., differential expression, clustering, rare cell type detection) in the corrected space vs. raw space.
- **Visualization:** Compare UMAP / t-SNE plots: clusters should match known biology in the corrected space and should be more compact / less batch-driven.
- **Perturbation prediction:** Compare predicted vs observed perturbation effects in a ground-truth validation set.

## Open alternatives

- **scVI / scANVI:** The VAE standard; designed for count data and batch integration.
- **Geneformer:** Transformer-based foundation model (Theodoris et al., Nature 2023); pre-trained on 30M cells.
- **scGPT:** Also transformer-based; Liu et al.; includes masking, domain classification, gene importance.
- **scFoundation:** Another transformer-based model; Zhao et al.; multi-scale architecture.
- **totalVI:** VAE with protein integration (multi-modal); from the authors of scVI.
- **Seurat v4:** Uses neural nets (weights learned from scVI) for batch correction in the standard Seurat pipeline.
- **Closed alternative:** CellVoyager (Veloxity) — commercial package for visualization and clustering.

## References

- Lopez et al., 2018, *Nature Methods* — scVI (the foundational VAE for scRNA-seq).
- Chen et al., 2020 — scANVI (the Bayesian VAE extension).
- Theodoris et al., 2023, *Nature* — Geneformer (transformer foundation model).
- Liu et al., 2023 — scGPT (transformer with masking).
- Zhao et al., 2023 — scFoundation (multi-scale transformer).
- Yosef et al., 2013, *Nature Biotechnology* — standard Scanpy reference (not deep learning, but the ecosystem).
- Hafemeister & Satija — Seurat v4 (includes neural net modules).

## Related Skills

- `bioinformatics-omics/scrnaseq-pipeline` — preprocessing, QC, and analysis with traditional methods
- `machine-learning-bio/deep-learning-genomics` — foundation models for DNA
- `machine-learning-bio/protein-language-models` — foundation models for protein

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from scVI (Lopez et al. 2018), Geneformer (Theodoris et al. 2023), and scGPT (Liu et al. 2023) papers; added practical fine-tuning workflow, GPU sizing guidelines, batch-correction evaluation rubric, and label transfer patterns.