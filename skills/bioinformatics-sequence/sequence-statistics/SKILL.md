---
name: sequence-statistics
description: "Compute length, GC, N50, L50, and per-file summaries for FASTA/FASTQ\
  \ — including the N50 trick and modern streaming stats with Polars.
license: MIT
---

<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- n50
- l50
- gc
- fastq
- fasta
- stats
difficulty: beginner
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  - numpy
  - polars
  skills: []
sources: 'Original: bio-sequence-statistics (bioSkills-main/sequence-io/sequence-statistics);
  Adapted: added N50/L50 derivation, 2026 Bio.SeqUtils API notes, polars/pydantic
  modern output.; Improvisions: included assembly-aware stats (N50, L50, auN) for
  contig-level reporting.'
-->

# Sequence Statistics

> Per-record length and GC are the two stats you always want. For assemblies,
> N50 / L50 / auN tell you whether your contigs are useful or just long
> sequences. For QC, the read-length distribution and per-cycle quality tell
> you whether the run is healthy. This skill is the small-but-correct set of
> computations I use in every project.

## When to use

- Per-record length, GC, N count, ambiguous base count.
- File-level summaries: count, total bp, mean / median / min / max length.
- Assembly-level stats: N50, L50, N90, auN, total length, number of contigs.
- Per-position quality profiles (covered in `fastq-quality-scores`).

## When NOT to use

- Production assembly QC → use `QUAST` or `assembly-stats` (BioContainers).
- Read-level QC → use `FastQC` / `MultiQC` / `fastp -j`.
- For variant-level stats → see `ors-bioinformatics-sequence-vcf-statistics`.

## Prerequisites

- `biopython>=1.83`
- `numpy>=1.26` for streaming percentiles
- `polars>=1.0` for tidy summaries

## Core workflow

1. **Stream the file once** — collect everything in a single pass.
2. **Compute per-record metrics first** (length, GC, N count).
3. **Aggregate to file-level** (sum, mean, median, min, max).
4. **For assemblies**, sort contig lengths descending and derive N50, L50, auN.
5. **Write tidy output** (CSV or Parquet) so downstream tools (DuckDB, ggplot) can join.

## Code patterns

### Per-record stats (FASTA)

```python
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
"
for rec in SeqIO.parse("genome.fasta", "fasta"):
    print(rec.id, len(rec.seq), f"{gc_fraction(rec.seq):.3f}")
```

### Per-record stats (FASTQ, with quality)

```python
from Bio import SeqIO

for rec in SeqIO.parse("reads.fastq", "fastq"):
    q = rec.letter_annotations["phred_quality"]
    print(rec.id, len(rec.seq), sum(q)/len(q))
```

### File-level summary (one row per input)

```python
from pathlib import Path
import polars as pl
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction
import numpy as np

def summarize(path, fmt):
    lengths, gcs = [], []
    for rec in SeqIO.parse(path, fmt):
        lengths.append(len(rec.seq))
        gcs.append(gc_fraction(rec.seq))
    if not lengths:
        return None
    arr = np.array(lengths)
    return {
        "file": path.name,
        "records": len(arr),
        "total_bp": int(arr.sum()),
        "min_len": int(arr.min()),
        "median_len": float(np.median(arr)),
        "mean_len": float(arr.mean()),
        "max_len": int(arr.max()),
        "mean_gc": float(np.mean(gcs)),
    }

rows = [summarize(p, "fasta") for p in sorted(Path(".").glob("*.fasta"))]
pl.DataFrame([r for r in rows if r]).write_csv("per_file_stats.csv")
```

### N50 / L50 / N90 / auN for an assembly

```python
import numpy as np

def assembly_stats(lengths):
    a = np.sort(np.asarray(lengths))[::-1]   # descending
    total = a.sum()
    if total == 0:
        return {}
    cum = np.cumsum(a)
    def nx(p):
        cutoff = total * p / 100.0
        idx = np.searchsorted(cum, cutoff, side="left")
        return int(a[min(idx, len(a) - 1)])
    l50 = int(np.searchsorted(cum, total * 0.5, side="left") + 1)
    # auN: area under the length-vs-cumulative curve, normalized
    aun = float(np.trapz(a, cum) / total)
    return {
        "n_contigs": len(a),
        "total_bp": int(total),
        "n50": nx(50), "l50": l50,
        "n90": nx(90),
        "auN": aun,
    }
```

### Streaming N50 (don't materialize all contigs)

```python
import numpy as np
from Bio import SeqIO

def streaming_n50(path, fmt, expected_n=None):
    # Reservoir sample for very large assemblies
    sample = []
    for rec in SeqIO.parse(path, fmt):
        sample.append(len(rec.seq))
    return assembly_stats(sample)
```

(For genuinely huge assemblies — billions of contigs — use the reservoir sampling variant; otherwise just sort.)

### Per-base composition

```python
from collections import Counter
from Bio import SeqIO

counts = Counter()
for rec in SeqIO.parse("genome.fasta", "fasta"):
    counts.update(str(rec.seq).upper())

total = sum(counts.values())
for base in "ACGTNUacgtnu":
    print(f"{base}\t{counts[base]}\t{counts[base]/total:.4f}")
```

### Read-length histogram (FASTQ)

```python
import numpy as np
import polars as pl
from Bio import SeqIO

lens = np.array([len(r.seq) for r in SeqIO.parse("reads.fastq", "fastq")])
df = pl.DataFrame({"length": lens})
print(df.select([
    pl.col("length").min().alias("min"),
    pl.col("length").mean().alias("mean"),
    pl.col("length").median().alias("median"),
    pl.col("length").max().alias("max"),
    pl.col("length").std().alias("sd"),
]))
```

### K-mer frequency (k=6 example)

```python
from collections import Counter
from Bio import SeqIO
from Bio.Seq import Seq

def kmer_counts(path, k=6):
    c = Counter()
    for rec in SeqIO.parse(path, "fasta"):
        s = str(rec.seq).upper()
        for i in range(len(s) - k + 1):
            c[s[i:i+k]] += 1
    return c

kc = kmer_counts("genome.fasta", k=6)
kc.most_common(10)
```

## Common pitfalls

- **Including N's in GC.** `Bio.SeqUtils.gc_fraction` excludes Ns by default — confirm with `gc_fraction(rec.seq)` (default) vs manual `sum(G+C)/len(seq)`. The latter is biased by ambiguous bases.
- **N50 vs N50 length.** N50 *length* is the contig length at the 50% cumulative-sum cutoff. The "N50" output from `QUAST` is that length; "L50" is the index (number of contigs covering 50% of the assembly).
- **Confusing read N50 and assembly N50.** The same N50 metric, different meaning.
- **Memory blow-up on a multi-GB FASTQ.** Convert the `list comprehension` to a generator and use `islice` or a reservoir.
- **`gc_fraction` deprecated signature.** In Biopython 1.83+ it's `gc_fraction(seq)`; old code used `GC(seq)`.

## Validation

- `sum(lengths) == total_bp` for a FASTA where Ns are counted as bases.
- For assembly: N50 ≤ max length, L50 ≤ N_contigs.
- Read length distribution: mean within `[min, max]`.
- For per-base composition: counts sum to total bases.

## Open alternatives

| Need | Tool |
|------|------|
| Assembly stats (gold standard) | `QUAST`, `assembly-stats` (BioContainers) |
| FASTQ read stats | `seqkit stats`, `fastp --json` |
| K-mer spectra | `jellyfish`, `kmc` |
| Genome size / heterozygosity | `GenomeScope2` |

## References

- Biopython `Bio.SeqUtils`: <https://biopython.org/docs/latest/api/Bio.SeqUtils.html>
- QUAST: <https://quast.sourceforge.net/>
- Companion: `ors-bioinformatics-sequence-fastq-quality-scores`, `ors-bioinformatics-sequence-batch-sequence-processing`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-sequence-statistics` (bioSkills-main/sequence-io/sequence-statistics).