---
name: samtools-bam-processing
description: "Process BAM files with samtools — sort, index, merge, flagstat, mark duplicates, fixmate, depth, filter, and stream — the standard CLI toolkit for 2026."
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- samtools
- bam
- sam
- sorting
- indexing
- markdup
difficulty: intermediate
prerequisites:
  tools:
  - samtools>=1.19
  - bcftools>=1.19
  skills:
  - ors-bioinformatics-sequence-sam-bam-basics"
sources: "Original: bio-samtools-bam-processing (SciAgent-Skills genomics-bioinformatics/alignment/samtools-bam-processing);\
  \ Adapted: modernized to samtools 1.19+ pipeline, added correct BAM processing workflow.;\
  \ Improvisions: added the canonical alignment → sort → fixmate →\
  \ markdup → sort → index workflow."
-->

# samtools BAM Processing

> samtools is the workhorse of NGS data processing. The CLI commands are
> designed to stream, so you can pipe `bwa mem | samtools sort` without touching
> disk. This skill covers the complete BAM processing workflow — the correct
> order of operations — and the modern samtools 1.19+ pipeline.

## When to use

- Sorting and indexing BAMs after alignment.
- Getting alignment statistics.
- Marking duplicates.
- Fixing mate information for properly-paired requirements.
- Extracting subsets by FLAG, MAPQ, region.

## When NOT to use

- You need alignment-level filtering → see `pysam` for Python.
- You need variant calling → see GATK / bcftools.
- Visual → use IGV.

## Prerequisites

- `samtools` ≥ 1.19
- `bcftools` ≥ 1.19 (always installed together)
- Reference FASTA + `.fai`

## Core workflow

1. **Align** → SAM.
2. **Sort by name** (`samtools sort -n`) → coordinate sort needs name-sorted first.
3. **Fixmate** (`samtools fixmate`) → sets the mate information.
4. **Sort by coordinate** (`samtools sort`) → final coordinate-sorted BAM.
5. **Mark duplicates** (`samtools markdup -r`) → remove optical duplicates.
6. **Index** (`samtools index`) → enable random access.

The correct order: align → name-sort → fixmate → coordinate-sort → markdup → index.

## Code patterns

### Coordinate sort

```bash
samtools sort -@ 8 -m 4G -o output.sorted.bam input.bam
samtools index output.sorted.bam
```

- `-@ 8` threads.
- `-m 4G` memory per thread.
- `-o` writes to specified output, not just stdout.

### Name sort (for fixmate input)

```bash
samtools sort -n -@ 8 -o output.name.bam input.sam
```

### Fixmate (set mate information for properly-paired requirement)

```bash
samtools fixmate -m -O bam input.name.bam fixed.bam
samtools sort -@ 8 -o fixed.sorted.bam fixed.bam
```

`fixmate -m` enables "mark shorter by more different" (for GATK compatibility), and -O bam produces BAM output directly.

### Mark duplicates (modern samtools 1.16+)

```bash
samtools markdup -r -s -t -v 1 \
    input.sorted.bam output.dedup.bam
samtools index output.dedup.bam
```

- `-r` REMOVE duplicates (not just mark).
- `-s` print statistics to stderr.
- `-t` mark duplicate tags (MC, ms).
- `-v` verbose.

### Fixmate → coordinate sort → markdup pipeline

```bash
# Full pipeline (all from alignment output)
bwa mem -t 16 -M ref.fa R1.fq R2.fq |
  samtools sort -n -@ 8 |
  samtools fixmate -m -O bam - |
  samtools sort -@ 8 -O bam |
  samtools markdup -r -@ 8 - output.bam
samtools index output.bam
```

### samtools flagstat

```bash
samtools flagstat input.bam | tail -10
# Shows mapped, paired, properly-paired, duplicate counts
```

### samtools stats

```bash
samtools stats input.bam
# Full alignment statistics
```

### Extract coverage depth per base

```bash
samtools depth input.bam > depth.tsv
```

### Per-base coverage, only positions >= 10x

```bash
samtools depth -aa -d 1000 input.bam | awk '$3>=10' > cov10.tsv
```

### Filter by MAPQ

```bash
samtools view -q 30 -b input.bam > q30.bam
```

### Extract properly paired reads

```bash
samtools view -F 4 -f 2 -b input.bam > proper.bam
```

### Extract primary alignments only

```bash
samtools view -F 256 -b input.bam > primary.bam
```

### Merge BAMs

```bash
samtools merge -@ 8 -o merged.bam input1.bam input2.bam
samtools index merged.bam
```

### Split BAM by read group

```bash
samtools split -f '%*_%!.bam' -d input.bam
```

### Extract alignments to chromosome

```bash
samtools view -b chr1 input.bam > chr1.bam
samtools index chr1.bam
```

### Tabix region query

Requires a BED file and tabix index:

```bash
tabix -p bed input.vcf.gz
tabix input.vcf.gz chr1:1000-2000
```

### Concatenate BAMs (when same sample, different lane)

```bash
samtools cat -o merged.bam lane1.bam lane2.bam
samtools index merged.bam
```

### Validate an index

```bash
# Index is built alongside BAM
ls -la input.bam.bai  # or input.bam.csi
```

## The standard pipeline (full example)

```bash
# 1. Align
bwa mem -t 16 -M -R "@RG\tID:sample1\tSM:sample1" \
    ref.fa R1.fq.gz R2.fq.gz |

# 2. Name sort (needed for fixmate)
  samtools sort -n -@ 8 |

# 3. Fixmate (set mate positions, mark duplicate tags)
  samtools fixmate -m -O bam - |

# 4. Coordinate sort
  samtools sort -@ 8 -O bam |

# 5. Mark duplicates
  samtools markdup -r -@ 8 - output.bam

# 6. Index
samtools index output.bam
```

Check at each step with `samtools flagstat`.

## Common pitfalls

- **Forgetting to fixmate.** Without fixmate, paired reads may not have FLAG 2 (proper pair) set correctly.
- **Sorting out of order.** Always name-sort before fixmate, then coordinate-sort after.
- **Duplicate marking too early.** Mark before coordinate sort leads to wrong duplicate detection.
- **Index required but missing.** `samtools view -b sample.bam chr1:10-10000` fails without an index.
- **Memory for sorting.** `-m 4G` is reasonable; smaller values may cause sort failure on large files.

## Validation

- `samtools flagstat sample.bam` shows read counts and properly-paired.
- After fixmate, FLAG 2 should be set on properly-paired reads that previously lacked it.
- After dedup, duplicate count in flagstat should be non-zero only if duplicates were present.
- After index, `samtools view -b sample.bam chr1:0-100` should return reads.

## Open alternatives

| Need | Tool |
|------|------|
| GPU deduplication | nvidia/parabricks (closed) |
| Multi-threaded sort | `sambamba` (legacy alternative) |
| In-Python filtering | `pysam` |
| Full pipeline | `nf-core/sarek`, `GATK` best practices |

## References

- samtools manual: <http://www.htslib.org/doc/samtools.html>
- SAM format spec: <https://samtools.github.io/hts-specs/SAMv1.pdf>
- GATK Best Practices: <https://gatk.broadinstitute.org/hc/en-us/articles/360035894711-About-GATK3>
- Companion: `ors-bioinformatics-sequence-bwa-alignment`, `ors-bioinformatics-sequence-pysam-genomics`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `samtools-bam-processing` (SciAgent-Skills).