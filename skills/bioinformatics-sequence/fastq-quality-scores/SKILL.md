---
name: quality-scores
description: "Access, filter, and trim Phred quality scores in FASTQ reads using Biopython\
  \ 1.83+ — including per-position profiles and encoding auto-detection.
license: MIT
---

<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- fastq
- phred
- quality
- trimming
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills: []
sources: 'Original: bio-fastq-quality (bioSkills-main/sequence-io/fastq-quality);
  Adapted: rewritten prose, 2026 Phred+33 dominance note, added streaming percentiles
  with NumPy.; Improvisions: replaced verbose quality-encoding detection with a 10-line
  ASCII-range heuristic, added fastp open alternative.'
-->

# FASTQ Quality Scores

> Quality scores are the currency of trust in sequencing data. Every filter
> you set — `Q20`, `Q30`, sliding-window trim — is a bet that bases above
> that threshold are usable for downstream variant calls, assemblies, and
> quantification. This skill covers reading Phred scores from FASTQ, building
> per-position profiles, and the three encodings you might still meet in
> 2026 (Sanger, Solexa, Illumina 1.3-1.7).

## When to use

- Computing per-read mean quality, per-position mean quality, or quality histograms.
- Filtering reads by mean or minimum quality.
- Trimming 3' ends or sliding-window trimming when no FASTP/Cutadapt step exists.
- Converting legacy Illumina/Solexa FASTQ to Phred+33.

## When NOT to use

- Production FASTQ QC → use `fastp` (`ors-bioinformatics-sequence-fastp-workflow`), `fastqc` + `MultiQC`, or `nf-core` modules.
- Adapter trimming → use `fastp` or `Trim Galore` (CUTADAPT).
- UMI handling → use `umis`/`umitools` (see `ors-bioinformatics-sequence-umi-processing`).

## Prerequisites

- `biopython>=1.83`, `numpy>=1.26`.
- For production work: `fastp` ≥ 0.23.

## Core workflow
"
1. **Read with `SeqIO.parse(..., "fastq")`** — Phred+33 is the default in Biopython 1.83+.
2. **Pull quality via `record.letter_annotations["phred_quality"]`** — it's a list of ints aligned 1-to-1 with the bases.
3. **Compute per-read and per-position aggregates** in a single streaming pass.
4. **Filter with a generator** — don't materialize the full file unless you must.
5. **For trimming**, use sliding-window Trimmomatic-style logic or hand off to `fastp`.

## Code patterns

### Read quality scores

```python
from Bio import SeqIO

for rec in SeqIO.parse("reads.fastq", "fastq"):
    quals = rec.letter_annotations["phred_quality"]
    # Process quals, which is a list[int] aligned with bases
```

### Mean quality per read

```python
def mean_q(rec):
    q = rec.letter_annotations["phred_quality"]
    return sum(q) / len(q)

for rec in SeqIO.parse("reads.fastq", "fastq"):
    print(f"{rec.id}\t{mean_q(rec):.1f}")
```

### Filter reads by mean quality

```python
from Bio import SeqIO

def keep(rec, min_mean=30):
    q = rec.letter_annotations["phred_quality"]
    return (sum(q) / len(q)) >= min_mean

with open("q30.fastq", "w") as out:
    SeqIO.write((r for r in SeqIO.parse("reads.fastq", "fastq") if keep(r)),
                out, "fastq")
```

### 3' trimming (drop trailing low-quality bases)

```python
def trim_3p(rec, min_q=20):
    q = rec.letter_annotations["phred_quality"]
    cut = len(q)
    for i in range(len(q) - 1, -1, -1):
        if q[i] >= min_q:
            cut = i + 1
            break
    return rec[:cut] if cut > 0 else None

from Bio import SeqIO
SeqIO.write((trim_3p(r) for r in SeqIO.parse("reads.fastq", "fastq") if trim_3p(r)),
            "trimmed.fastq", "fastq")
```

### Sliding-window trim (Trimmomatic LEADING/TRAILING style)

```python
def sliding_window_trim(rec, window=4, min_avg=20):
    q = rec.letter_annotations["phred_quality"]
    n = len(q)
    for i in range(n - window + 1):
        if sum(q[i:i+window]) / window < min_avg:
            return rec[:i] if i > 0 else None
    return rec
```

### Per-position mean quality (full FASTQ in one pass)

```python
from collections import defaultdict
from Bio import SeqIO

by_pos = defaultdict(list)
for rec in SeqIO.parse("reads.fastq", "fastq"):
    for i, q in enumerate(rec.letter_annotations["phred_quality"]):
        by_pos[i].append(q)

# Print first 30 positions
for i in range(30):
    vals = by_pos[i]
    print(f"pos {i}\tmean={sum(vals)/len(vals):.1f}\tn={len(vals)}")
```

### Percentile quality profile with NumPy

```python
import numpy as np
from Bio import SeqIO

# Read all qualities into a 2D matrix (padded with -1 if reads differ in length)
maxlen = 0
rows = []
for rec in SeqIO.parse("reads.fastq", "fastq"):
    q = rec.letter_annotations["phred_quality"]
    rows.append(q)
    maxlen = max(maxlen, len(q))

mat = np.full((len(rows), maxlen), -1, dtype=np.int16)
for i, q in enumerate(rows):
    mat[i, :len(q)] = q

mask = mat >= 0
p50 = np.where(mask, mat, np.nan)
print("per-position Q50:", np.nanpercentile(p50, 50, axis=0)[:20])
```

### Detect FASTQ quality encoding (Sanger / Solexa / Illumina 1.3+)

```python
def detect_encoding(path: str, sample=4000) -> str:
    mn = 126
    with open(path) as fh:
        i = n = 0
        for line in fh:
            if i % 4 == 3:
                mn = min(mn, min(ord(c) for c in line.rstrip()))
                n += 1
                if n >= sample:
                    break
            i += 1
    if mn < 59:   return "fastq"            # Sanger / Illumina 1.8+ (Phred+33)
    if mn < 64:   return "fastq-solexa"     # Solexa+64
    return "fastq-illumina"                 # Illumina 1.3-1.7 (Phred+64)
```

### Convert legacy FASTQ to Phred+33

```python
from Bio import SeqIO

# Read old variant, write as standard
records = SeqIO.parse("legacy.fastq", detect_encoding("legacy.fastq"))
SeqIO.write(records, "modern.fastq", "fastq")
```

## Common pitfalls

- **Wrong FASTQ variant string.** `KeyError: 'phred_quality'` → not Phred+33; try `fastq-illumina` or `fastq-solexa`.
- **Aggressive trimming collapses reads to 0 length.** Always check `len(rec) > 0` after trim and skip empties.
- **Confusing `record.letter_annotations["phred_quality"]` with `record.seq`.** Quality is *not* in the sequence; it's a parallel list of ints.
- **Forgetting reads are variable length** when building a 2D NumPy matrix. Pad with a sentinel (`-1` or `NaN`) and mask.
- **Solexa scores are *not* Phred** for low values. The encoding differs below Q14 — don't compare raw integers.

## Validation

- After a `Q30` filter, the output mean quality (across all kept reads) is ≥ 30.
- A per-position profile shows the expected Illumina decay at read 3' end.
- Round-trip: a converted FASTQ, re-detected, returns `"fastq"` (Phred+33).

## Open alternatives

| Need | Tool | Notes |
|------|------|-------|
| Single-pass FASTQ QC + trim | `fastp` ≥ 0.23 | 10-50x faster than Python, reports HTML/JSON |
| Detailed per-base reports | `FastQC` + `MultiQC` | Standard in nf-core pipelines |
| UMI-aware trimming | `umitools trim` | Handles UMI + adapter in one pass |
| Long-read quality | `NanoPlot`, `PycoQC` | ONT/PacBio specific |

## References

- Phred+33 / Solexa encoding table: <https://en.wikipedia.org/wiki/Phred_quality_score>
- Biopython QualityIO: <https://biopython.org/docs/latest/api/Bio.SeqIO.QualityIO.html>
- fastp paper: Chen et al., 2018, *Bioinformatics* — `10.1093/bioinformatics/bty560`
- Companion: `ors-bioinformatics-sequence-fastp-workflow`, `ors-bioinformatics-sequence-umi-processing`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-fastq-quality` (bioSkills-main/sequence-io/fastq-quality).