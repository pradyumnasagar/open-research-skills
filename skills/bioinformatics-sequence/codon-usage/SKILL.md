---
name: codon-usage
description: "Compute codon usage frequencies, RSCU, CAI, and tRNA adaptation —"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- codon
- cai
- rscu
- gene-expression
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills:
  - ors-bioinformatics-sequence-transcription-translation
sources: 'Original: bio-codon-usage (bioSkills-main/sequence-manipulation/codon-usage);
  Adapted: 2026 CAI/RSCU formulas, modern alternative to deprecated Bio.SeqUtils.CodonUsage.;
  Improvisions: added codon harmonization for cross-species expression, 2026 open
  alternatives (DNA Chisel, GeneDesign).'
-->

# Codon Usage and Bias

> Amino acids are encoded by 1-6 synonymous codons, and organisms don't
> use them with equal probability. E. coli hates CGA, loves CGT. S.
> cerevisiae prefers CAA over CAG for glutamine. The bias is a real
> factor in heterologous expression: a human gene full of rare-for-E.coli
> codons produces poorly. This skill is the math (CAI, RSCU, ENC) and
> the modern open alternatives (DNA Chisel, GeneDesign) for codon
> optimization in 2026.

## When to use

- Predicting heterologous expression yield (high CAI in the host → likely high expression).
- Comparing codon bias across organisms.
- Designing codon-optimized coding sequences.
- Building a reference codon-usage table from a genome.

## When NOT to use

- Gene finding (use pyrodigal / bakta).
- Variant effect on protein (use SIFT / PolyPhen / AlphaMissense).

## Prerequisites

- `biopython>=1.83`
- For codon optimization: `dnachisel` (open source) or `GeneDesign` (open source)

## Core workflow

1. **Pick the right metric**: RSCU for bias *direction*, CAI for *expression* prediction, ENC for *strength* of bias.
2. **Build or load a reference codon table** (from a host genome or a published table).
3. **Compute the metric for your gene**.
4. **If optimizing**, generate a sequence that maximizes the metric while preserving amino acid sequence and avoiding restriction sites / RNA structures.

## Code patterns

### Build a codon usage table from a genome's CDS

```python
from Bio import SeqIO
from collections import Counter
from Bio.Seq import Seq

def codon_counter(cds_iter, table=1):"
    """Yield codon counts from an iterator of CDS sequences."""
    c = Counter()
    for s in cds_iter:
        s = Seq(str(s).upper())
        if len(s) % 3 != 0:
            s = s[:len(s) - len(s) % 3]
        for i in range(0, len(s), 3):
            c[str(s[i:i+3])] += 1
    return c
```

### Relative Synonymous Codon Usage (RSCU)

RSCU = (observed count of codon) / (expected count if all synonymous codons were equal).

```python
from Bio.Data import CodonTable
from collections import defaultdict

def rscu(counts: dict, table_id: int = 1) -> dict:
    t = CodonTable.unambiguous_dna_by_id[table_id]
    aa_to = defaultdict(list)
    for codon, aa in t.forward_table.items():
        aa_to[aa].append(codon)
    out = {}
    for aa, codons in aa_to.items():
        n_syn = len(codons)
        total = sum(counts.get(c, 0) for c in codons)
        if total == 0:
            for c in codons:
                out[c] = 0.0
            continue
        expected = total / n_syn
        for c in codons:
            out[c] = counts.get(c, 0) / expected if expected else 0.0
    return out
```

RSCU > 1 means the codon is used more often than expected; < 1 means less.

### Codon Adaptation Index (CAI)

CAI = geometric mean of relative adaptiveness (weight of each codon = RSCU / max RSCU for that amino acid in the reference set).

```python
import math

def cai(seq: str, ref_counts: dict, table_id: int = 1) -> float:
    t = CodonTable.unambiguous_dna_by_id[table_id]
    aa_to = defaultdict(list)
    for codon, aa in t.forward_table.items():
        aa_to[aa].append(codon)
    max_w = {}
    for aa, codons in aa_to.items():
        total = sum(ref_counts.get(c, 0) for c in codons)
        if total == 0:
            for c in codons:
                max_w[c] = 0.0
            continue
        weights = {c: ref_counts.get(c, 0) / (total / len(codons)) for c in codons}
        m = max(weights.values()) or 1.0
        for c, w in weights.items():
            max_w[c] = w / m
    s = Seq(seq.upper())
    if len(s) % 3 != 0:
        s = s[:len(s) - len(s) % 3]
    log_sum = 0.0
    n = 0
    for i in range(0, len(s), 3):
        c = str(s[i:i+3])
        w = max_w.get(c, 0.0)
        if w > 0:
            log_sum += math.log(w)
            n += 1
    return math.exp(log_sum / n) if n else 0.0
```

CAI ranges 0-1. Higher = more "host-like" codons. > 0.8 is considered highly expressed in the host.

### Effective Number of Codons (ENc)

ENc ranges 20 (extreme bias, one codon per amino acid) to 61 (no bias).
Wright 1990 formula:

```python
def enc(counts: dict, table_id: int = 1) -> float:
    from Bio.Data import CodonTable
    t = CodonTable.unambiguous_dna_by_id[table_id]
    aa_to = defaultdict(list)
    for codon, aa in t.forward_table.items():
        aa_to[aa].append(codon)

    f_vals = []
    for aa, codons in aa_to.items():
        n = len(codons)
        if n == 1:
            continue
        total = sum(counts.get(c, 0) for c in codons)
        if total <= 1:
            continue
        # homozygosity F = (n * sum(p_i^2) - 1) / (n - 1)
        p = [counts.get(c, 0) / total for c in codons]
        f = (n * sum(pi * pi for pi in p) - 1) / (n - 1)
        f_vals.append(f)

    # Wright's formula
    enc = 2 + 9 / (sum(f_vals) / len(f_vals)) if f_vals else 0
    return enc
```

### Use a published reference table (E. coli K-12)

```python
# Kazusa codon usage database provides these as text
# https://www.kazusa.or.jp/codon/
ECOLI_CODONS = {
    "ATG": 1000,   # example, replace with real counts
    "TTT":  500,
    # ... full table from Kazusa
}
```

For real work, parse the Kazusa `.txt` file or use `python_codon_tables` (PyPI).

### Codon optimization with DNA Chisel (open source)

```python
import dnachisel as dc

problem = dc.DnaOptimizationProblem(
    sequence="ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG",
    constraints=[
        dc.EnforceTranslation(),
        dc.EnforceGCContent(mini=0.4, maxi=0.6, window=50),
        dc.AvoidPattern("BsaI_site"),  # avoid restriction sites
    ],
    objectives=[dc.CodonOptimize(species="e_coli")],
)
problem.resolve()
print(problem.sequence)  # optimized sequence
```

### Codon harmonization (preserve original codon bias, not maximize)

For cross-species expression where the source organism's translation speed pattern matters, "harmonize" the sequence to use the destination's most-frequent codon for each amino acid in a way that mimics the source's translational pauses.

Tools: `codon harmonization` Python package; CHARMING web server (academic).

## Common pitfalls

- **Computing CAI on the wrong frame.** A multiple-of-3 length is the only frame that produces a real CAI.
- **RSCU of 0 for a synonymous codon that wasn't observed.** RSCU = 0 means the codon is absent in the reference; not the same as "disallowed".
- **CAI close to 1 doesn't guarantee expression.** It predicts codon *availability* for the tRNA pool, not mRNA stability, protein folding, or toxicity.
- **Optimizing for codon bias destroys mRNA structure and may introduce rare restriction sites.** Always combine with `EnforceGCContent`, `AvoidPattern`, and structure objectives.
- **Cross-species CAI comparisons are invalid.** CAI is *relative* to a reference. Pick the host's reference, not the donor's.

## Validation

- CAI is in [0, 1].
- RSCU values for synonymous codons sum to the number of synonymous codons per amino acid.
- ENc is in [20, 61].
- A codon-optimized sequence still translates to the same amino acid sequence (use `translate(to_stop=True)` to verify).

## Open alternatives

| Need | Tool |
|------|------|
| Codon optimization | `DNA Chisel`, `GeneDesign` |
| CAI/RSCU/ENc reference tables | `python_codon_tables` (PyPI), Kazusa |
| Codon harmonization | `codon-harmonization` (PyPI), CHARMING |
| Expression prediction (ML) | `CodonBERT`, `mRFP` |

## References

- Sharp & Li 1987 (CAI): <https://doi.org/10.1093/nar/15.3.1281>
- Wright 1990 (ENc): <https://doi.org/10.1093/nar/18.1.171>
- Kazusa codon DB: <https://www.kazusa.or.jp/codon/>
- DNA Chisel: <https://github.com/Edinburgh-Genome-Foundry/DnaChisel>
- Companion: `ors-bioinformatics-sequence-transcription-translation`, `ors-bioinformatics-sequence-sequence-properties`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-codon-usage` (bioSkills-main/sequence-manipulation/codon-usage).