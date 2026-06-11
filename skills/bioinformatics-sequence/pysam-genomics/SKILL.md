---
name: pysam-genomics
description: "Programmatically read, modify, filter, and write BAM/CRAM/VCF files"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- pysam
- bam
- sam
- htslib
- python
- variant
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.10
  - pysam>=0.22
  skills:
  - ors-bioinformatics-sequence-sam-bam-basics
sources: 'Original: bio-pysam-genomic-files (SciAgent-Skills-main genomics-bioinformatics/alignment/pysam-genomic-files);
  Adapted: modernized for pysam 0.22+ and htslib 1.19+.; Improvisions: added the canonical
  open/iteration patterns, htsidx notes for 2026.'
-->

# pysam — BAM/CRAM Python Interface

> `pysam` is the Pythonic interface to htslib: read BAM/CRAM/VCF/TBF, iterate
> alignments, call variants, and build custom pipelines. The 2026
> reality: pysam 0.22+ pairs with htslib 1.19+ and is the low-level I/O engine
> behind GATK, freebayes, and most variant callers. If you need to
> programmatically iterate through NGS files, this is the canonical way.

## When to use

- Programmatically iterate BAM alignments with Python logic.
- Extract variant or coverage data from a BAM.
- Build a custom pipeline that needs alignment-level access.
- Query regions from indexed BAM/CRAM without loading a whole file.

## When NOT to use

- You need a BAM stats summary → use `samtools stats` or `mosdepth`.
- You need variant calling → use GATK/HaplotypeCaller or freebayes.
- Visual → IGV, IGV.js, or JBrowse.

## Prerequisites

- `pysam` ≥ 0.22 (PyPI or conda)
- `htslib` ≥ 1.19 (linked automatically)

## Core workflow

1. **Open an alignment file** with `pysam.AlignmentFile`.
2. **Iterate and filter** with Python (no shell calls).
3. **Query by region** with pileup / fetch.
4. **Write** optional BAM/CRAM output.
5. **Close** explicitly or use a context manager.

## Code patterns

### Open a BAM (read)

```python
import pysam
"
bam = pysam.AlignmentFile("input.bam", "rb")
```

### Open a SAM (auto-detect gzipped)

```python
sam = pysam.AlignmentFile("input.sam", "r")
```

### Open a indexed region

Access a small region without loading the whole BAM:

```python
bam = pysam.AlignmentFile("input.bam", "rb")
for read in bam.fetch("chr1", 100_000, 200_000):
    print(read.query_name, read.reference_name, read.pos, read.cigartuples)
```

### Iterate through all alignments

```python
bam = pysam.AlignmentFile("input.bam", "rb")
for read in bam:
    # read is a pysam AlignedSegment
    if read.is_proper_pair:
        print(read.query_name, read.tlen)
```

### Filter by FLAG in Python

```python
def proper_paired(read):
    return read.is_paired and read.is_proper_pair

bam = pysam.AlignmentFile("input.bam", "rb")
proper = [r for r in bam if proper_paired(r)]
```

### Extract MAPQ, CIGAR, cigarstring

```python
for read in bam:
    print(read.query_name,
          read.mapq,
          read.cigartuples,   # [(0, 100)] = 100M
          read.cigarstring)   # "100M"
```

### Extract the aligned sequence

```python
for read in bam:
    if not read.is_unmapped:
        print(read.query_sequence[:50])  # First 50 bp
```

### Access mate information

```python
for read in bam:
    if read.is_paired and read.mate_is_unmapped:
        print(f"{read.query_name} mate is unmapped")
```

### Pileup at a position

```python
bam = pysam.AlignmentFile("input.bam", "rb")
for column in bam.pileup("chr1", 100_000, 100_001):
    for read in column.pileups:
        print(read.alignment.query_name)
```

### Write a filtered BAM

```python
with pysam.AlignmentFile("filtered.bam", "wb", header=bam.header) as out:
    for read in bam:
        if read.mapq >= 30 and read.is_proper_pair:
            out.write(read)
```

### Iterating over a tabix-indexed BED/VCF

```python
vcf = pysam.TabixFile("variants.vcf.gz")
for record in vcf.contigs:
    pass  # Use region query for actual records
```

### Read from CRAM (requires reference)

```python
cram = pysam.AlignmentFile("input.cram", "rc", reference_fasta="genome.fa")
```

### Access the header as Python dict

```python
header = bam.header.to_dict()
print(header["RG"])  # List of read groups
```

### Convert SAM to Python objects

```python
with pysam.AlignmentFile("input.sam", "r") as sam:
    for read in sam:
        # read is an AlignedSegment
        ...
```

### Get index statistics without loading

```python
index = pysam.IndexedReads(pysam.AlignmentFile("input.bam"))
```

The `Index` object is for random-access.

### Create custom tags

```python
bam = pysam.AlignmentFile("input.bam", "rb", fields=["NM", "MD", "RG"])
# Fields are automatically loaded if they exist
```

### Check if a position is covered

```python
bam = pysam.AlignmentFile("input.bam", "rb")
for col in bam.pileup("chr1", 100_000, 100_001):
    coverage = col.nsegments
    if coverage >= 10:
        print(f"Position covered: {coverage}")
```

### Extract all reads overlapping a gene

```python
# Use fetch for gene coordinates
bam = pysam.AlignmentFile("input.bam", "rb")
gene_reads = [r for r in bam.fetch("chr1", start, end)]
```

### Read group filter

```python
rg_bam = pysam.AlignmentFile("input.bam", "rb", header=header)
for read in rg_bam:
    # read.get_tag("RG") - read group from optional tags
    pass
```

## Common pitfalls

- **Forgetting to close the file.** Use a context manager (`with ...`) or close explicitly.
- **CIGAR interpretation.** `read.cigartuples` returns `(operation, length)` tuples. `0` = M, `1` = I, `2` = D.
- **MAPQ zero** means unmapped *in this alignment*, not zero quality.
- **Reference fasta for CRAM.** Must be the exact FASTA used to create the CRAM.
- **Duplicate reads being filtered.** `samtools markdup -r` is the modern way.
- **Pileup object is lazy.** If you need it, materialize it (e.g., with `list()`) otherwise it's consumed by iteration.

## Validation

- After filtering, `samtools flagstat filtered.bam` should show the expected read count.
- `read_mapq` should be >= your threshold.
- `read.is_proper_pair` checks both ends.

## Open alternatives

| Need | Tool |
|------|------|
| Shell pipeline | `samtools view`, `samtools filter` |
| Variant calling | GATK / freebayes / bcftools |
| Coverage | `mosdepth`, `samtools depth` |
| Multi-sample | `bcftools isec` |
| Pysam in R | `Rsamtools` (Bioconductor) |

## References

- pysam documentation: <https://pysam.readthedocs.io/>
- htslib: <http://www.htslib.org/>
- SAM spec: <https://samtools.github.io/hts-specs/SAMv1.pdf>
- Companion: `ors-bioinformatics-sequence-sam-bam-basics`, `ors-bioinformatics-sequence-bcftools-variant-manipulation`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `pysam-genomic-files` (SciAgent-Skills).