---
name: filter-sequences
description: "Filter FASTA/FASTQ records by length, identity, regex on headers, GC\
  \ window, complexity, and custom predicates — streaming with Biopython 1.83+.
license: MIT
---

<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- filter
- regex
- gc
- length
- fastq
- fasta
difficulty: beginner
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills:
  - ors-bioinformatics-sequence-fastq-quality-scores
sources: 'Original: bio-filter-sequences (bioSkills-main/sequence-io/filter-sequences);
  Adapted: tightened to streaming-only patterns, added 2026 regex tips for header
  parsing.; Improvisions: added complexity filter (Shannon entropy), 2026 seqkit open
  alternative.'
-->

# Filter Sequences by Criteria
"
> Filtering is the most common "preprocessing" step you'll write. The
> canonical mistake is to filter twice — once to compute, again to write.
> Stream records through a chain of predicate generators and write the
> survivors once. This skill is the predicate catalog: length, GC, identity
> (regex on headers), N content, complexity, and how to compose them.

## When to use

- Selecting reads/contigs by length, GC, N count, or complexity.
- Subsetting FASTA by header pattern (e.g., keep only `chr[1-9XY]`, drop `chrUn_*`).
- Removing low-complexity reads (e.g., poly-A runs) before assembly.
- Filtering paired FASTQ — see the paired-end skill for sync filtering.

## When NOT to use

- Adapter/quality trimming → use `fastp` (single-tool, much faster).
- Host/contaminant screening → use `kraken2`, `minimap2` against a host DB, or `nf-core` modules.
- For UMI dedup → `umi-tools dedup` or `fab` are better than custom code.

## Prerequisites

- `biopython>=1.83`, `regex>=2024.5` (better Unicode support than `re`).
- For high-throughput filtering: `seqkit` (C) is ~50x faster.

## Core workflow

1. **Define your predicates** as composable Python functions returning `bool`.
2. **Wrap them in a generator chain** so the file is read once.
3. **Stream the survivors to disk** with `SeqIO.write`.
4. **Always log how many records you kept vs dropped** — for reproducibility.

## Code patterns

### Length filter (FASTA)

```python
from Bio import SeqIO

def length_filter(records, min_len=500, max_len=10_000_000):
    for rec in records:
        if min_len <= len(rec.seq) <= max_len:
            yield rec

with open("filtered.fasta", "w") as out:
    n_in = n_out = 0
    for rec in SeqIO.parse("input.fasta", "fasta"):
        n_in += 1
        if min_len := 500 <= len(rec.seq):
            SeqIO.write(rec, out, "fasta")
            n_out += 1
print(f"Kept {n_out}/{n_in} records")
```

(Prefer the explicit form for clarity — the example above shows the structural pattern.)

### Identity filter (regex on header)

```python
import regex
from Bio import SeqIO

keep_pattern = regex.compile(r"^chr(1[0-9]|2[0-2]|[1-9]|X|Y|M)$")

def keep_chrom(rec, pat=keep_pattern):
    return bool(pat.match(rec.id))

with open("primary.fasta", "w") as out:
    SeqIO.write(r for r in SeqIO.parse("genome.fasta", "fasta") if keep_chrom(r)),
                out, "fasta")
```

### GC window filter

```python
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

def gc_window(rec, lo=0.30, hi=0.70):
    return lo <= gc_fraction(rec.seq) <= hi

SeqIO.write((r for r in SeqIO.parse("asm.fasta", "fasta") if gc_window(r)),
            "asm_gc_filtered.fasta", "fasta")
```

### N content filter

```python
def max_n(rec, max_frac=0.05):
    s = str(rec.seq).upper()
    if not s:
        return False
    return (s.count("N") / len(s)) <= max_frac
```

### Quality filter (FASTQ)

```python
def min_mean_quality(rec, min_q=30):
    q = rec.letter_annotations["phred_quality"]
    return (sum(q) / len(q)) >= min_q
```

### Complexity filter (Shannon entropy over a window)

Useful for removing low-complexity reads that escape length filters:

```python
import math
from collections import Counter

def entropy(s, k=4):
    """k-mer Shannon entropy; > ~2 bits usually means 'not junk' for k=4."""
    if len(s) < k:
        return 0.0
    counts = Counter(s[i:i+k] for i in range(len(s) - k + 1))
    total = sum(counts.values())
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def complex_enough(rec, min_entropy=1.8, k=4):
    return entropy(str(rec.seq).upper(), k=k) >= min_entropy
```

### Composition predicates (composition)

```python
from functools import reduce

def keep(rec, preds):
    return all(p(rec) for p in preds)

predicates = [lambda r: min_length(r, 1000), lambda r: max_n(r, 0.01), gc_window]
SeqIO.write((r for r in SeqIO.parse("in.fasta", "fasta") if keep(r, predicates)),
            "out.fasta", "fasta")
```

### Drop empty records after trim

```python
def non_empty(rec):
    return len(rec.seq) > 0
```

## Common pitfalls

- **Forgetting the file was modified in place.** Filter chains should always be pure functions of `rec -> bool`.
- **GC skew from Ns.** Use `Bio.SeqUtils.gc_fraction` (excludes Ns) or normalize manually.
- **Regex on headers is brittle.** `^chr(\d+|X|Y|M)$` matches `chr1` but not `CHR1`; decide and be explicit.
- **Streaming into a list defeats the purpose.** Use generator expressions inside `SeqIO.write`.
- **Length filter on FASTQ before QC trim** is wrong order. Trim first, then filter.

## Validation

- After every filter, the input count ≥ output count.
- For paired filtering, mate counts in R1 and R2 match.
- Spot-check: a few records from the output satisfy every predicate.
- For complexity, an obvious junk read (e.g., `AAAAAAAAAA...`) has entropy ~0 and is dropped.

## Open alternatives

| Need | Tool |
|------|------|
| Sequence filtering at scale | `seqkit seq -m 500 -M 5000 in.fasta` |
| Regex header subset | `samtools view -b in.bam chr1 chr2 ...` (for BAM) |
| Complexity filter | `bbduk.sh entropy=0.5` (BBTools) |
| N-content filter | `seqkit seq -g -G 0.05` (drop GC > 5% — actually means min GC, see docs) |

## References

- Biopython sequence utilities: <https://biopython.org/docs/latest/api/Bio.SeqUtils.html>
- `regex` package: <https://pypi.org/project/regex/>
- Companion: `ors-bioinformatics-sequence-fastq-quality-scores`, `ors-bioinformatics-sequence-paired-end-fastq`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-filter-sequences` (bioSkills-main/sequence-io/filter-sequences).