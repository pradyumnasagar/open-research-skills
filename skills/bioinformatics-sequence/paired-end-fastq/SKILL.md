---
name: paired-end-fastq
description: "Keep R1/R2 reads in lockstep — synchronize iteration, filter pairs"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- fastq
- paired-end
- illumina
- sequencing
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  - seqkit
  skills:
  - ors-bioinformatics-sequence-fastq-quality-scores
sources: 'Original: bio-paired-end-fastq (bioSkills-main/sequence-io/paired-end-fastq);
  Adapted: modernized for 2026, added deinterleave patterns and seqkit open alternative.;
  Improvisions: added the ''do NOT sort FASTQ files'' warning, modern UMI handling
  pointer.'
-->

# Paired-End FASTQ Handling

> Paired-end reads are two halves of a story: R1 and R2 must travel together.
> Sort by read ID, shuffle wrong, and your aligner will silently lose half
> your fragments. This skill covers the canonical operations: synchronized"
> iteration, paired filtering, interleaving, deinterleaving, and the "never
> sort FASTQ" rule that everyone learns the hard way.

## When to use

- You have `*_R1.fastq.gz` and `*_R2.fastq.gz` and need to keep them in sync.
- You want to apply a quality filter to both mates and keep pairs together (not orphan reads).
- You need to interleave (`>interleaved.fastq`) for a tool that requires it, or deinterleave an interleaved file.

## When NOT to use

- Your tool already accepts `--r1` and `--r2` separately — just hand it both paths and let it stream.
- Long-read (ONT/PacBio) data — no pairing.
- For UMI-aware paired handling, use `umitools` or `fastp` (not Biopython).

## Prerequisites

- `biopython>=1.83`
- `seqkit` ≥ 2.8 (fast deinterleave / interleave in shell)
- For production QC + trim: `fastp` ≥ 0.23

## Core workflow

1. **Never sort FASTQ files by record ID.** Order is load-bearing for downstream aligners that assume R1[i] pairs with R2[i]. Use `seqkit pair` or upstream tools.
2. **Iterate R1 and R2 in lockstep** with `zip()` (when you trust order) or by ID lookup (when you don't).
3. **Filter pairs together** — never drop a read from R1 without checking R2.
4. **For interleaving**, alternate R1/R2 records into a single FASTQ.

## Code patterns

### Synchronized iteration (assumes sorted R1/R2)

```python
from Bio import SeqIO

r1 = SeqIO.parse("sample_R1.fastq.gz", "fastq")
r2 = SeqIO.parse("sample_R2.fastq.gz", "fastq")

for rec1, rec2 in zip(r1, r2):
    # Process pair — same fragment, opposite strands
    ...
```

### Paired quality filter (drop pair if either mate fails)

```python
from Bio import SeqIO

def mean_q(rec):
    q = rec.letter_annotations["phred_quality"]
    return sum(q) / len(q)

def paired_filter(r1_path, r2_path, out_r1, out_r2, min_mean=30):
    r1_it = SeqIO.parse(r1_path, "fastq")
    r2_it = SeqIO.parse(r2_path, "fastq")
    with open(out_r1, "w") as o1, open(out_r2, "w") as o2:
        for rec1, rec2 in zip(r1_it, r2_it):
            if mean_q(rec1) >= min_mean and mean_q(rec2) >= min_mean:
                SeqIO.write(rec1, o1, "fastq")
                SeqIO.write(rec2, o2, "fastq")

paired_filter("R1.fastq", "R2.fastq", "clean_R1.fastq", "clean_R2.fastq")
```

### Paired length filter (both mates must pass)

```python
def both_long(rec1, rec2, min_len=50):
    return len(rec1.seq) >= min_len and len(rec2.seq) >= min_len
```

### Interleave R1 and R2 into a single FASTQ

```python
from Bio import SeqIO

def interleave(r1_path, r2_path, out_path):
    r1 = SeqIO.parse(r1_path, "fastq")
    r2 = SeqIO.parse(r2_path, "fastq")
    with open(out_path, "w") as out:
        for rec1, rec2 in zip(r1, r2):
            SeqIO.write(rec1, out, "fastq")
            SeqIO.write(rec2, out, "fastq")

interleave("R1.fastq", "R2.fastq", "interleaved.fastq")
```

### Deinterleave a single FASTQ

```python
from Bio import SeqIO
from itertools import islice

def deinterleave(in_path, out_r1, out_r2):
    it = SeqIO.parse(in_path, "fastq")
    with open(out_r1, "w") as o1, open(out_r2, "w") as o2:
        for even, rec in enumerate(it):
            (o1 if even % 2 == 0 else o2).write(rec.format("fastq"))

deinterleave("interleaved.fastq", "out_R1.fastq", "out_R2.fastq")
```

### Count pairs (sanity check)

```python
from Bio import SeqIO
def count_pairs(r1, r2):
    n1 = sum(1 for _ in SeqIO.parse(r1, "fastq"))
    n2 = sum(1 for _ in SeqIO.parse(r2, "fastq"))
    assert n1 == n2, f"Mate count mismatch: {n1} vs {n2}"
    return n1
```

### Repair out-of-sync mates (same ID, different order)

Use this only when R1 and R2 are guaranteed same-IDs but order is shuffled. O(N) memory:

```python
from Bio import SeqIO
from collections import defaultdict

def index_mates(path):
    return {r.id: r for r in SeqIO.parse(path, "fastq")}

r1 = index_mates("R1.fastq")
r2 = index_mates("R2.fastq")
common = sorted(set(r1) & set(r2))
print(f"Pair ID intersection: {len(common)} pairs")
```

For millions of reads, prefer `seqkit pair -1 R1.fq.gz -2 R2.fq.gz`.

## Common pitfalls

- **Sorting FASTQ files by ID.** Downstream aligners assume R1[i] pairs with R2[i] when files are positionally aligned. Sorting breaks this contract.
- **Orphaned reads after filtering.** If your filter drops an R1 read but keeps the R2 mate, your BAM will have singletons. Either drop the pair or write them to a separate `*.singletons.fastq` for tools that accept it (e.g., `bwa mem -p` with `--include-unpaired`).
- **Mate ID mismatches from upstream tools.** Some pipelines append `/1` or `/2` to one mate but not the other. Normalize first.
- **Reading `.fastq.gz` without `gzip`.** Biopython's `SeqIO.parse` handles `.gz` natively, but if you wrap with `gzip.open`, you must use text mode (`'rt'`).
- **Streaming both files into the same `zip`.** A subtle off-by-one at the end of file is possible if mate counts differ. Always `assert` or count.

## Validation

- Mate counts match: `n_records(R1) == n_records(R2)`.
- After paired filter, no orphans: `n_records(out_R1) == n_records(out_R2)`.
- After deinterleave, `n_records(R1) + n_records(R2) == n_records(interleaved)`.
- For ID-locked repair, intersection size matches the smaller of the two input sets.

## Open alternatives

| Need | Tool |
|------|------|
| Deinterleave / interleave at scale | `seqkit pair` or `seqkit interleave` / `seqkit deinterleave` |
| Paired QC + trim + report | `fastp -i in.R1.fq.gz -I in.R2.fq.gz -o out.R1.fq.gz -O out.R2.fq.gz` |
| Repair unsorted pairs | `seqkit pair -1 R1.fq -2 R2.fq -O repaired` |
| UMI extraction | `umitools extract --bc-pattern=NNNN --read2-in=R2.fq --read1-out=R1.fq ...` |

## References

- `seqkit pair`: <https://bioinf.shenwei.me/seqkit/usage/#pair>
- fastp paired mode: <https://github.com/OpenGene/fastp#paired-input>
- Companion: `ors-bioinformatics-sequence-fastp-workflow`, `ors-bioinformatics-sequence-umi-processing`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-paired-end-fastq` (bioSkills-main/sequence-io/paired-end-fastq).