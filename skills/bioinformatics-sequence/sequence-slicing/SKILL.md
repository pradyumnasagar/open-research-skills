---

name: sequence-slicing
description: "Slice, subset, and extract regions from sequences and SeqRecords — including feature extraction, fuzzy ends, and the location algebra behind GenBank features."
license: MIT
---




<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
  - bioinformatics-sequence
  - research
difficulty: intermediate
-->

# Sequence Slicing and Subsetting

> Slicing a string is intuitive. Slicing a biological sequence is not —
> coordinates may be 0-based or 1-based, strand may be reversed, features"
> may span exon junctions, and "fuzzy" ends (e.g., `>100..<200`) are real
> GenBank syntax. This skill is the algebra: which slice gives you what,
> and how to extract a region with the right strand in 2026.

## When to use

- Extracting a gene/CDS/exon from a chromosome sequence.
- Slicing reads or contigs by position.
- Computing intersection of two locations (e.g., variant overlaps a gene).
- Fuzzy-end handling (next-generation sequencing produces `5'..<200`).

## When NOT to use

- Production genomic region queries → use `pyranges` or `pysam` with a BED file.
- Whole-genome windowed stats → use `bedtools` or `deeptools`.

## Prerequisites

- `biopython>=1.83`
- For 1-based / 0-based conversion discipline, see below.

## Core workflow

1. **Decide the coordinate system.** Biopython `FeatureLocation` is **0-based, end-exclusive**, matching BED and Python. GenBank flat files are 1-based, end-inclusive.
2. **For a GenBank feature**, use `feature.extract(record.seq)` — Biopython handles strand for you.
3. **For a manual region**, slice with Python: `record.seq[start:end]`.
4. **For compound locations** (e.g., joins across exons), `extract` walks the parts.

## Coordinate systems

| Tool / format | 0/1-based | Start | End |
|---------------|----------|-------|-----|
| Biopython `FeatureLocation` | 0-based | inclusive | exclusive |
| Python `seq[a:b]` | 0-based | inclusive | exclusive |
| GenBank flat file | 1-based | inclusive | inclusive |
| BED | 0-based | inclusive | exclusive |
| GFF3 | 1-based | inclusive | inclusive |
| VCF | 1-based | inclusive | (length-1) |

**The single most common bug** in bioinformatics code is a 1-based / 0-based
off-by-one. Pick a convention and stick to it.

## Code patterns

### Slice a record

```python
from Bio import SeqIO

rec = next(SeqIO.parse("chr1.fasta", "fasta"))
seq = rec.seq[1000:2000]   # 1000 bp window, 0-based
```

### Extract a feature (Biopython handles strand)

```python
for feat in rec.features:
    if feat.type == "CDS":
        nt = feat.extract(rec.seq)  # always in 5'→3' of the feature's strand
        protein = nt.translate()
        print(feat.qualifiers.get("gene", ["?"])[0], protein)
```

### Manual CDS extraction (start, end, strand)

```python
from Bio.Seq import Seq

def extract_region(seq, start, end, strand):
    sub = seq[start:end]
    return sub.reverse_complement() if strand == -1 else sub

extract_region(rec.seq, 1000, 1500, strand=-1)
```

### Compound location (multi-exon)

```python
from Bio.SeqFeature import CompoundLocation

# join(100..200, 300..400)
loc = CompoundLocation([
    FeatureLocation(100, 200, strand=1),
    FeatureLocation(300, 400, strand=1),
])
nt = loc.extract(rec.seq)  # concatenates both parts
```

### Fuzzy-end locations (next-gen sequencing)

GenBank uses `>` and `<` for unknown bounds. Biopython supports them with `BeforePosition` / `AfterPosition`:

```python
from Bio.SeqFeature import FeatureLocation, BeforePosition

# >100..200  (start unknown, somewhere before 100)
loc = FeatureLocation(BeforePosition(100), 200)
```

### Find which features overlap a window

```python
def overlapping(feat, start, end):
    return not (feat.location.end <= start or feat.location.start >= end)

hits = [f for f in rec.features if overlapping(f, 1000, 2000)]
```

### Construct a SimpleLocation and check strand

```python
from Bio.SeqFeature import SimpleLocation

loc = SimpleLocation(100, 200, strand=1)
print(loc.start, loc.end, loc.strand)   # 100 200 1
```

### Convert 1-based GenBank coords to 0-based Python

```python
def gb_to_python(start_gb, end_gb):
    # GenBank: 1-based inclusive; Python: 0-based exclusive
    return start_gb - 1, end_gb
```

### Slice a FASTQ read

```python
from Bio import SeqIO

rec = next(SeqIO.parse("reads.fastq", "fastq"))
subseq = rec.seq[10:50]   # a 40 bp window
```

### Take a sub-record (preserves ID and metadata)

```python
sub = rec[1000:2000]
print(sub.id, sub.description)
```

## Common pitfalls

- **1-based GenBank vs 0-based Python.** Always convert explicitly.
- **End-exclusive Python vs end-inclusive GenBank.** `seq[99:199]` is 100 bp, but GenBank would write it as `100..199`.
- **Forgetting strand on manual extraction.** `seq[start:end]` always returns the + strand. To get the - strand, `.reverse_complement()`.
- **Fuzzy bounds silently coerced.** `BeforePosition` and `AfterPosition` are real; don't pretend they're integers.
- **Slicing a `Seq` vs slicing a `SeqRecord`.** Slicing a record returns a new `SeqRecord` (preserves ID/description). Slicing a `Seq` returns a `Seq`.

## Validation

- `len(rec.seq[1000:2000]) == 1000`.
- For a CDS feature, the extracted length should be a multiple of 3.
- Round-trip: `loc.extract(rec.seq)` length equals the sum of the location parts.

## Open alternatives

| Need | Tool |
|------|------|
| Production genomic windows | `pyranges`, `polars-bio` |
| BED-style intersections | `bedtools intersect` |
| Tabix region queries | `pysam.TabixFile.fetch(...)` |
| Variant overlap with genes | `pyensembl`, `gffutils` |

## References

- Biopython `SeqFeature`: <https://biopython.org/docs/latest/api/Bio.SeqFeature.html>
- Location algebra: <https://biopython.org/docs/latest/Tutorial.html#sec:locations>
- Companion: `ors-bioinformatics-sequence-seq-objects`, `ors-bioinformatics-omics-genome-intervals-*` skills.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-sequence-slicing` (bioSkills-main/sequence-manipulation/sequence-slicing).