---
name: ors-machine-learning-bio-deep-learning-genomics
display_name: "Deep Learning for Genomics"
description: Use CNNs (DeepBind, Basset), RNNs, and transformers (DNABERT, HyenaDNA, Evo, Nucleotide Transformer) for genomic sequence analysis. Use when predicting TF binding, chromatin profiles, splicing, or noncoding variant effects from raw sequence.
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: machine-learning-bio
tags: [deepbind, genomics, cnn, transformer, dnabert, hyenadna]
difficulty: intermediate
prerequisites:
  tools: [python, pytorch, keras, biotite, pybedtools, bedtools2]
  skills: []
sources_consulted:
  - "Original: DeepBind (Alipanahi et al. 2015 Nat. Biotechnol.); Adapted: CNN workflow, TF binding / motif discovery framing"
  - "Original: DNABERT (github.com/3011git/DeepBug); Adapted: practical fine-tuning, variant calling use case"
  - "Original: HyenaDNA (Nature Methods 2024); Adapted: fast tokenization patterns"
  - "Original: Nouaille et al. / Hertzano et al. — Nucleotide Transformer; Adapted: embedding extraction"
  - "Improvisions: model selection rubric, GPU baselines, multi-modal context"
last_updated: 2026-06-10
---

# Deep Learning for Genomics

> DNA is inherently a sequence: the same convolutional and self-attention architectures that revolutionized NLP now power genomic function prediction. This skill maps the canonical architectures (CNN to transformer) to the tasks you will face — binding site prediction, chromatin profiling, variant effect, and functional noncoding element discovery. It gives you a working pipeline and the decision framework to pick between tools when they overlap.

## When to use

- You want to predict transcription-factor binding from DNA sequence alone (no ChIP-seq label is available or you need an *in silico* filter).
- You need to score variant effect in noncoding regions where there is no experimental data — transformer models give you a learned prior.
- You need to generate per-base functional annotations along the genome and your only input is the reference + alt alleles.
- You want to pull embeddings from a pre-trained foundation model to use as features in a downstream classifier.
- You are building a chromatin assay-to-sequence model (the inverse of TF binding: given histone marks, where is the gene?).

## When NOT to use

- The task is purely variant calling from reads (not sequence). Use traditional variant callers (GATK, FreeBayes) combined with deep-learning post-filtering, not a genomic sequence model.
- You have enough high-quality ChIP-seq / ATAC-seq data to train a supervised model — DeepBind / Basset models are good but your data will always beat a generic model on your system.
- The functional question is about splicing (exon definition, NMD, splice-site conservation). Use splice-score models (MaxEntScan, MMSplice) specifically.
- The signal is very short or very local (<10 bp). CNNs are overkill for simple motif counts or k-mer filters, but you can use a shallow CNN to learn a kernel.
- You need interpretability or PWM / MEME-level motif discovery. CNN filter visualization works but is not the same as a rigorous de novo motif find; use meme-suite for discovery and the CNN for scoring.

## Prerequisites

```bash
# Core deep-learning frameworks
pip install torch keras tensorflow

# Sequence handling utilities
pip install biotite pyfaidx scikit-bio

# Big genome tools
pip install pybedtools  # requires bedtools2 installed separately

# For DNABERT: a full model run is ~10-20 GB GPU memory for the full model
pip install dna-nlp  # or follow github.com/3011git/DeepBug

# For HyenaDNA and other foundation models
pip install hyena-dna  # check the repo for installation
pip install transformers

# GPU CUDA verification
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
```

Hardware baselines (rough; verify against each repo):

- DeepBind-sized CNNs (single-task): 4–8 GB VRAM.
- DNABERT / HyenaDNA fine-tuning: 16–40 GB VRAM.
- Full foundation model inference: ≥24 GB (the full model weights + forward + gradient storage).
- Embedding extraction only (no backward pass): half the memory of forward.

Conceptual prerequisites: know the difference between a **k-mer convolution kernel** learned from data vs. a known PWM (position-weight matrix), and understand that "zero-shot" for genomics means predicting function for a TF or variant type that the model has never seen in training — this is inherently harder than a model with full annotation.

## Core workflow

### 1. Pick the model architecture

| Task | Default model | Why |
|------|---------------|-----|
| Binding site prediction | DeepBind / Basset | Proven on ChIP-seq; CNN kernels directly learn PWMs |
| Variant effect in regulatory DNA | Nucleotide Transformer / DNABERT | Transformer gives contextual embeddings; pre-trained on 100M+ motifs / genomes |
| Full-genome functional annotation | DNABERT-2 / Evo | Token-level classification across entire chromosomes |
| Embedding extraction for downstream | Any foundation model (DNABERT, NT, HyenaDNA) | Use the [CLS] token or mean-pool |
| Long-sequence modeling (>2 kb) | HyenaDNA / Evo | Recurrence / state-space; linear in sequence length |
| Multi-modal (DNA + RNA + protein) | scGPT / Geneformer cross-modal | Outside scope; see single-cell skill |

### 2. Basic CNN binding prediction (DeepBind-style)

The 2015 DeepBind paper showed that a small 1D CNN on one-hot DNA can match PWM-based tools. This is the baseline reference architecture.

```python
import torch, torch.nn as nn

class DeepBindCNN(nn.Module):
    def __init__(self, seq_len=200, n_classes=1, conv_dims=[128, 64], kernel_sizes=[15, 11]):
        super().__init__()
        self.convs = nn.ModuleList([
            nn.Conv1d(4, d, k) for d, k in zip(conv_dims, kernel_sizes)
        ])
        self.pool = nn.AdaptiveMaxPool1d(1)
        self.fc = nn.Linear(sum(conv_dims), n_classes)

    def forward(self, x):  # x: (B, 4, L)
        h = torch.cat([torch.relu(conv(x)) for conv in self.convs], dim=1)
        h = self.pool(h).squeeze(-1)
        return self.fc(h)
```

Training typical: BCEWithLogitsLoss (for binding yes/no) or CrossEntropy (for multi-class). Use BAsset / `train_bigwig.py` from the DeepBind repo for data preprocessing.

### 3. Encode a genome for transformer ingestion

DNABERT and HyenaDNA diverge in tokenization. In general, use a k-mer tokenizer (di-nucleotide or tri-nucleotide, not per-base).

```python
def kmer_tokenize(seq, k=3):
    """Convert DNA to k-mer token indices. Standard: k=3 (codons) or k=2 (dinucleotides)."""
    seq = seq.upper().replace("N", "A")  # mask ambiguous bases
    kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
    # Map each k-mer to an integer via hash or lookup table
    return kmers

# For DNABERT, use the built-in tokenizer
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("dna bert-base")
enc = tok("ACGTACGT...", return_tensors="pt")
```

The k-mer tokenizer is important: per-base tokenization produces a vocabulary size of 4 (plus special tokens). k-mer vocabulary is 4^k — 3-mer → 64 tokens, which is enough for a model to learn di-nucleotide / tri-nucleotide interactions.

### 4. Per-base variant effect scoring

The standard pattern: forward pass for ref vs. alt, take the difference at the changed position.

```python
def score_variant(ref_seq, alt_seq, position, model, tokenizer):
    """
    Return a score difference (alt - ref) at position (0-indexed).
    The model is a token-level classifier or MLM.
    """
    # Tokenize both sequences
    ref_enc = tokenizer(ref_seq, return_tensors="pt")
    alt_enc = tokenizer(alt_seq, return_tensors="pt")

    with torch.no_grad():
        ref_out = model(**ref_enc).logits[0, position]
        alt_out = model(**alt_enc).logits[0, position]

    # For binary classification: sigmoid (ref) -> prob, same for alt
    ref_prob = torch.sigmoid(ref_out)
    alt_prob = torch.sigmoid(alt_out)
    return (alt_prob - ref_prob).item()  # positive = alt increases predicted function
```

Variant-effect models are evaluated by: AUC against functional assays (ChIP-seq, eCLIP, GWAS hits), not by absolute scores. Use a held-out benchmark set (ProteinGym for proteins, a held-out TF for DNA) to calibrate.

### 5. Embedding extraction from a foundation model

Use this as input to any downstream classifier that takes sequence features.

```python
import torch
from transformers import AutoModel, AutoTokenizer

model_name = "InstaDeepAI/nucleotide-transformer-v2-100m-6t-30k"  # or dna-bert, hyena-dna
tok = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).eval()

def get_embedding(seq, layer=-1):
    """Return a per-token embedding, `layer` from the last hidden state."""
    enc = tok(seq, return_tensors="pt")
    with torch.no_grad():
        out = model(**enc, output_hidden_states=True)
    hidden = out.hidden_states[layer]
    # Average over sequence (or use CLS token)
    mask = enc["attention_mask"].unsqueeze(-1).float()
    avg = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1)
    return avg.squeeze(0).numpy()
```

The embedding dimension varies: 256–768 typically for small models, 1280 for large. Check the model card.

### 6. Whole-genome annotation pipeline (sketch)

For annotation of an entire chromosome, chunk, batch, and write to BED/bigWig.

```python
# Pseudo-code: chunk + batch + save as BED
import numpy as np
from pybedtools import BedTool

def annotate_genome(genome_fasta, model, tokenizer, chunk_size=512, step=256):
    """Yield per-base scores across the whole chromosome."""
    seq = load_genome(genome_fasta)  # pyfaidx or Biotite
    scores = []
    for i in range(0, len(seq) - chunk_size, step):
        chunk = seq[i:i+chunk_size]
        scores.append(predict_one(chunk))
    # Flatten and save as bigWig or BEDGraph
    return np.concatenate(scores)
```

This is expensive. For whole-genome runs, use DNABERT's `--BedGraph` flag if the tool has one, or subsample. You will not annotate the human genome at single-base resolution in a single run — plan for chunking.

## Code patterns

### Visualizing learned CNN filters as PWMs (DeepBind interpretability)

```python
def filter_to_pwm(conv_weight):
    """conv_weight: (4, kernel_size). Convert to PWM-like view."""
    return conv_weight.T.abs() / conv_weight.T.abs().sum(dim=1, keepdim=True)

# Plot with logomaker or Biopython SeqLogo
import logomaker
logo = logomaker.Logo(filter_to_pwm(model.convs[0].weight.detach().numpy()), shade_below=0.5)
```

### Convert BED to training regions

```python
import pybedtools

def bed_to_training_chunks(bed_file, genome_fasta, window=200):
    """Yield (sequence, label) pairs from BED intervals."""
    bt = pybedtools.BedTool(bed_file)
    genome = pyfaidx.Fasta(genome_fasta)
    for interval in bt:
        start, end = interval.start, interval.end
        # pad to window
        pad_before = (window - (end - start)) // 2
        pad_after = window - (end - start) - pad_before
        seq = genome[interval.chrom][start - pad_before:end + pad_after].seq
        label = float(interval.score) if interval.score else 1.0  # assume positive class
        yield seq.upper(), label
```

### GPU memory saving for long sequences

```python
# Gradient checkpointing for long sequences (no model changes needed)
from torch.utils.checkpoint import checkpoint_sequential

model = AutoModel.from_pretrained("hyena-dna")
model gradients = [p.requires_grad for p in model.parameters()]

def forward_with_checkpoint(seq):
    # Split the model into two halves for checkpointing
    modules = [model.embed + model.encoder.layer[:6], model.encoder.layer[6:]]
    return checkpoint_sequential(modules, 2, seq)
```

## Common pitfalls

- **One-hot encoding is memory-expensive for long sequences.** Use k-mer tokenization; one-hot of 100kb → 400k floats; k-mer → 64 × 100k.
- **Ignoring strand.** DNA has no intrinsic orientation — double the model capacity (forward / reverse complement) or pre-reverse complement your sequences. Basset does this internally; not all tools do.
- **Mixing up model types.** A masked language model (MLM) such as DNABERT trained with [MASK] tokens is different from a sequence-to-label classifier which predicts a scalar at [CLS]. The MLM gives you per-position logits; theClassifier aggregates to a single prediction. Both are "transformers" but the outputs differ.
- **Assuming the model sees the right strand.** Some tools expect the sequence as-written, others reverse-complement automatically. Check the repo.
- **Training on the same genome the model was pre-trained on.** If you train on hg38 and the model was trained on hg38 for "genome modeling", you are learning the residual, not the function. Split by chromosome or hold out entire chromosomes.
- **Overfitting small TF ChIP-seq.** If you have <5,000 peaks, a CNN may memorize; use transfer learning, augment by reverse complement, or use a pre-trained model as a frozen feature extractor.
- **Not using a proper negative set.** Random negatives (shuffled sequences) are too easy. Use conservation-matched negatives or flanks of the positive peaks.

## Validation

- **Held-out ChIP-seq.** Split peaks by chromosome, train on chr1-22, validate on chrM or chrY.
- **Variant-effect benchmarks.** Use held-out GWAS variant sets (the variant was not in the training set of the model). Compute AUC / Precision-Recall.
- **Motif recovery.** Run a CNN filter visualization; if it matches a known PWM in JASPAR, you have an interpretability signal.
- **Per-base functional annotation.** Run on a region with known functional data not used in training (e.g. an ENCODE tier 1 enhancer), compare predicted accessibility against the assay.
- **Downstream classifier.** Use the extracted embeddings as input to a simple logistic regression on a held-out functional task. If embeddings are randomly distributed, the model learned nothing useful. If logistic regression on frozen embeddings beats random, the model is useful.

## Open alternatives

- **DeepBind:** The original (Alipanahi et al. 2015). Closed academic license but widely reproduced. Basset is the open successor with a fully convolutional architecture.
- **DNABERT:** Open weights (GitHub: `3011git/DeepBug`). Fine-tuning requires GPU but the model is reproducible.
- **HyenaDNA:** Open (Nature Methods 2024). Linear-time for long sequences; competes with token-level transformers.
- **Nucleotide Transformer:** Open weights (InstaDeepAI). Pre-trained on 100M+ genomes; use for embedding extraction.
- **Evo:** From Character.AI / a]6]S. High-quality genome model but check the license.
- **Non-deep options:** FIMO / meme-suite for PWM scanning; linear SVM or XGBoost on k-mer features for baseline classification (faster than CNN, interpretable).

## References

- Alipanahi et al., 2015, *Nature Biotechnology* — DeepBind (the landmark CNN for TF binding).
- Kelley et al., 2016, *Genome Research* — Basset (open CNN for chromatin accessibility).
- Zhou et al., 2023 — DNABERT (transformer for DNA).
- Nguyen et al., 2024, *Nature Methods* — HyenaDNA (state-space model for long sequences).
- Zhou et al., 2023 — Nucleotide Transformer (InstaDeepAI; 100M+ pre-training).
- Varadi et al. — JASPAR for PWM ground truth.
- Quinlan & Pennock — bedtools2 for BED manipulation.
- Scherp et al. — pyfaidx for FASTA access.
- The ENCODE Consortium — ChIP-seq / ATAC-seq benchmarks.

## Related Skills

- `machine-learning-bio/alphafold-structure-prediction` — protein structural counterpart (embedding extraction from protein language model)
- `machine-learning-bio/scrnaseq-deep-learning` — single-cell RNA-seq foundation models (Geneformer, scGPT)
- `bioinformatics-sequence/fasta-fastq-io` — sequence I/O (input preparation)
- `bioinformatics-omics/chip-seq-analysis` — ChIP-seq (the experimental data for binding prediction)
- `bioinformatics-omics/atac-seq-analysis` — ATAC-seq (the accessibility assay)

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from DeepBind paper, DNABERT repo, and HyenaDNA paper; added practical k-mer tokenization and variant-scoring pipeline, GPU baselines, and model-selection rubric.