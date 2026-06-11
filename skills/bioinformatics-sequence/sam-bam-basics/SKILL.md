---
name: sam-bam-basics
description: "Understand the SAM format header, alignment records, FLAGs, MAPQ, CIGAR,"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- sam
- bam
- flag
- mapq
- cigar
- format
difficulty: beginner
prerequisites:
  tools:
  - samtools>=1.19
  skills: []
sources: 'Original: bio-sam-bam-basics (bioSkills-main/alignment-files/sam-bam-basics);
  Adapted: tightened SAM/BAM conventions, added 2026 samtools view flags.; Improvisions:
  added the canonical SAM field table, FLAG decode examples, PAF comparison.'
-->

# SAM / BAM File Basics

> Every aligner produces SAM (text) or BAM (binary). The format is the
> lingua franca of short-read genomics. If you understand the SAM line
> format — QNAME through the optional fields — you can debug anything: why
> reads are unmapped, why a variant isn't callable, or why your count matrix
> has fewer reads than expected. This skill is the 101.

## When to use

- Understanding why reads aligned (or didn't).
- Filtering BAMs by FLAG, MAPQ, CIGAR.
- Extracting specific read subsets for downstream tools.
- Converting SAM ↔ BAM and adding custom tags.

## When NOT to use

- You need BAM statistics — see `bam-statistics` skill.
- You need to filter duplicates — see `duplicate-handling` skill.
- Visualizing alignments — use IGV, samtools tview, or a browser.

## Prerequisites

- `samtools` ≥ 1.19
- For programmatic work: `pysam` (see `pysam-genomics` skill)

## The SAM line format

```
QNAME FLAG RNAME POS CIGAR SEQ QUAL TAGS
```

| Field | Content | Example |
|-------|---------|---------|
| QNAME | Read name | `HISEQ:XX:123:CGT...` |
| FLAG | Bitwise OR flags | `99` = paired + proper + reverse + mate-reverse |
| RNAME | Reference | `chr1`, `*` if unmapped |
| POS | 1-based leftmost | `12345678`, `0` if unmapped |
| CIGAR | Alignment | `100M`, `50S50M`, `*` for unmapped |
| SEQ | Sequence | `ACGT...`, `*` if no SEQ |
| QUAL | Phred quality | `IIII...`, `*` if no QUAL |
| TAGS | Optional fields | `NM:i:5 MD:Z:50 GA:G...` |

## The canonical optional tags

| Tag | Type | Meaning |
|-----|------|--------|
| `NM` | `i` | Edit distance (total mismatches + indels) |
| `MD` | `Z` | MD:Z string for SNPs |
| `RG` | `Z` | Read group (from input `@RG`) |
| `AS` | `i` | Alignment score |
| `XS` | `A` | Strand for RNA (`+` or `-`) |
| `XP` | `Z` | Alternative alignment positions |
| `YI` | `Z` | Old read group (Illumina) |
| `MC` | `Z` | Mate CIGAR |
| `MQ` | `i` | Mate MAPQ |
| `PG` | `Z` | Program that produced this alignment |

## Common FLAGs (binary decode)

Use `samtools flags 99` to decode or encode:

| Flag | Binary | Meaning |
|------|--------|----------|
| 1 | 000000000001 | paired |
| 2 | 000000000010 | proper paired |
| 4 | 000000000100 | unmapped |
| 8 | 000000001000 | mate unmapped |
| 16 | 000000010000 | reverse strand |
| 32 | 000000100000 | mate reverse strand |
| 64 | 000001000000 | first in pair |
| 128 | 000010000000 | second in pair |
| 256 | 000100000000 | secondary alignment |
| 512 | 001000000000 | QC fail |
| 1024 | 010000000000 | duplicate |
| 2048 | 100000000000 | supplementary alignment |

## Code patterns

### View a BAM as SAM (text)

```bash
samtools view -h input.bam | head -20
```

### Convert SAM to BAM

```bash
samtools view -bS input.sam > output.bam
```

### Extract mapped reads

```bash
samtools view -F 4 -b input.bam > mapped.bam
# -F 4 = exclude FLAG 4 (unmapped)
```

### Extract unmapped reads

```bash
samtools view -f 4 -b input.bam > unmapped.bam
# -f 4 = require FLAG 4 (unmapped)
```

### Extract properly paired reads

```bash
samtools view -F 4 -f 2 -b input.bam > proper.bam
```

### Extract reads with MAPQ >= 30

```bash
samtools view -q 30 -b input.bam > q30.bam
```

### Extract primary alignments only

```bash
samtools view -F 256 -b input.bam > primary.bam
```

### Extract alignments to chromosome 1

```bash
samtools view -b chr1 input.bam > chr1.bam
```

### Extract reads by read name

```bash"
samtools view -h input.bam | grep "read_name" | samtools view -bS - > reads.bam
```

### Convert BED to SAM/BAM (via BEDTools if needed)

BEDTools: `bedtools bedtobam -bed12 input.bed -g genome.txt > output.bam`

### Decode a FLAG to readable string

```bash
samtools flags 99
# 99 = PAIRED|PROPER_PAIRED|REVERSE|MREVERSE
```

### Sort by name (for fixmate)

```bash
samtools sort -n input.bam -o input.name.bam
samtools index input.name.bam
```

### Sort by coordinate (default)

```bash
samtools sort -o input.coord.bam input.bam
samtools index input.coord.bam
```

### Build a header from scratch

```bash
samtools view -H input.bam
# Shows @HD, @SQ, @RG, @PG lines
```

### Add a read group to the header

```bash
samtools addreplacerg -r "@RG\tID:sample1\tSM:sample1\tPL:ILLUMINA" -o out.bam in.bam
samtools index out.bam
```

### Extract strand-specific information

For RNA-seq, the XS tag indicates strand:

```bash
samtools view input.bam | awk '$20 ~ /XS:A:[+-]/ {print $20}'
```

## Coordinate systems

| System | Start | End | Used by |
|--------|-------|-----|-------|
| SAM/BAM (POS) | 1-based | inclusive | SAM/BAM |
| BED | 0-based | exclusive | UCSC, BEDTools |
| VCF | 1-based | inclusive | VCF |
| Python | 0-based | exclusive | All Python libraries |
| GFF3 | 1-based | inclusive | GFF3 |

## Common pitfalls

- **0-based vs 1-based confusion.** SAM POS is 1-based. Python slice is 0-based. Convert explicitly.
- **CIGAR interpretation.** `50M` = 50 matches. `10S40M` = 10 soft-clipped + 40 matches.
- **Primary/secondary alignment.** FLAG 256 means secondary (split read aligned elsewhere). Often not what you want.
- **Supplementary.** FLAG 2048 means supplementary alignment (chimeric).
- **Duplicate markings are recommendations, not truth.** `samtools markdup` is the canonical; confirm before filtering.
- **MAPQ = 255** from bowtie2 means "aligner can't calculate a good MAPQ" — not "very high confidence".

## Validation

- After any filter, use `samtools flagstat` to check read counts.
- After `samtools view -F 4`, no reads should have FLAG bit 4.
- Coordinate-sorted BAM must be indexed (`samtools index`) before `samtools tview` or region queries.

## Open alternatives

| Need | Tool |
|------|------|
| PAF (minimap2 output) | Convert to SAM with `paftools`, or use `minimap2 -a` for SAM |
| CRAM (compressed) | `samtools view -C` |
| HTSJDK (JVM) | Use Picard from GATK |
| Genome-wide statistics | `samtools stats`, `mosdepth` |

## References

- SAM spec: <https://samtools.github.io/hts-specs/SAMv1.pdf>
- samtools manual: <http://www.htslib.org/doc/samtools.html>
- Companion: `ors-bioinformatics-sequence-bam-statistics`, `ors-bioinformatics-sequence-pysam-genomics`

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-sam-bam-basics` (bioSkills-main/alignment-files/sam-bam-basics).