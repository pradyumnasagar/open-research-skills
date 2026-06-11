---

name: hisat2-alignment
description: "Splice-aware RNA-seq alignment with HISAT2 — fast, memory-efficient, and the default in many bulk RNA-seq pipelines alongside STAR."
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

# HISAT2 RNA-seq Alignment

> HISAT2 (Hierarchical Indexing for Spliced Alignment of Transcripts 2) is
> the fast, memory-efficient RNA-seq aligner that uses a hierarchical
> FM-index. It's the right choice when STAR's RAM cost is too high or when
> you want a balance of speed and accuracy. The 2026 reality: STAR is the
> gold standard for novel-junction discovery; HISAT2 is the fast standard
> for known-junction discovery and low-RAM environments.

## When to use

- Bulk RNA-seq alignment to a reference transcriptome/genome.
- Small-genome RNA-seq where STAR's index cost is too high.
- 3' tag-seq (e.g., Lexogen QuantSeq) with appropriate flag settings.
- Long RNA-seq (>250 bp reads, e.g., ONT cDNA).

## When NOT to use

- De novo transcript assembly → use `STAR` (better novel junction discovery).
- DNA-seq variant calling → use `bwa-mem` or `bwa-mem2`.
- Long reads → use `minimap2` with `-ax splice`.

## Prerequisites

- `hisat2` ≥ 2.2
- `samtools` ≥ 1.19
- Reference FASTA + HISAT2 index
- For best sensitivity: known splice sites from a GTF file

## Core workflow

1. **Extract splice sites and exons from a GTF** to build a sensitive index.
2. **Build the HISAT2 index** (`hisat2-build` or `hisat2-build-s` with known splice sites).
3. **Align** with `hisat2 --dta` for downstream transcriptome assembly (StringTie / Cufflinks) or `--no-spliced-alignment` for general use.
4. **Sort and index** the BAM with `samtools`.

## Code patterns

### Extract splice sites and exons from a GTF

```bash
hisat2_extract_splice_sites.py genes.gtf > splice_sites.txt
hisat2_extract_exons.py genes.gtf > exons.txt
```

### Build a sensitive index (with known splice sites)

```bash
hisat2-build -p 16 --ss splice_sites.txt --exon exons.txt reference/genome.fa genome_hs2
```

### Build a basic index (no annotation, faster)

```bash
hisat2-build -p 16 reference/genome.fa genome_hs2
```

### Paired-end alignment (typical bulk RNA-seq)

```bash
hisat2 -p 16 --dta -x genome_hs2 \
    -1 reads_R1.fq.gz -2 reads_R2.fq.gz \
    --rg-id sample1 --rg SM:sample1 --rg PL:ILLUMINA --rg LB:lib1 \
    -S sample1.sam
samtools sort -@ 8 -o sample1.bam sample1.sam
samtools index sample1.bam
rm sample1.sam
```

`--dta` (downstream-transcriptome-assembly) is required if you'll run StringTie; it reports alignments tailored to transcript assembly.

### Single-end alignment

```bash
hisat2 -p 16 --dta -x genome_hs2 -U reads.fq.gz --rg-id s1 --rg SM:s1 |
  samtools sort -@ 8 -o s1.bam -
```

### rRNA-aware alignment (filter rRNA first, or use `--un-gz` to drop)

```bash
hisat2 -p 16 --dta --un-gz unmapped.fq.gz -x genome_hs2 -1 R1.fq -2 R2.fq |
  samtools sort -@ 8 -o s.bam -
```

`--un-gz` writes reads that didn't align (often rRNA or contaminant) for downstream QC.

### Strand-specific libraries (dUTP / Ligation)

HISAT2 doesn't natively set XS tags; the convention is to use `featureCounts` or `StringTie` to infer strand from spliced alignments. For library prep-specific strand:

```bash
# Ligation protocol (Illumina TruSeq stranded)
# HISAT2 reports XS:A:+ / XS:A:- via the spliced alignment orientation
# featureCounts -s 2 (reverse stranded) will pick this up
```

### Long-read cDNA (ONT / PacBio Iso-Seq)

```bash
hisat2 -p 16 --dta -x genome_hs2 -U iso_seq.fq.gz --no-temp-splicesite |
  samtools sort -@ 8 -o iso.bam -
```

### nf-core integration

`nf-core/rnaseq` defaults to STAR. To use HISAT2, pass `--aligner hisat2` on the CLI.

## Common pitfalls

- **Forgetting `--dta` for transcriptome assembly.** StringTie/Cufflinks require the special scoring.
- **Building an index without splice sites.** The basic index works but is less sensitive for novel junctions.
- **Mixing up `--rna-strandness` (legacy flag removed in 2.2).** In HISAT2 2.2+, use downstream tools (`featureCounts -s`) to handle strand.
- **Not using `--rg-id`.** `featureCounts` and `StringTie` need read groups for multi-sample merges.
- **STAR's memory cost is too high → HISAT2 with low sensitivity.** If STAR fails on RAM, HISAT2 with the basic index will also miss junctions. Consider subsampling reads or using a known-splice-site index.

## Validation

- `samtools flagstat s.bam` — high mapping rate expected (≥80% for human bulk RNA-seq).
- `samtools view -c -f 2 s.bam` — properly-paired count.
- `samtools view s.bam | grep -c 'N:M:'` — spliced alignment count (look for `N` in CIGAR).
- `samtools view s.bam | awk '$6 ~ /N/' | wc -l` — spliced reads.
- rRNA fraction should be < 10% for poly-A selected, < 25% for ribo-depleted.

## Open alternatives

| Need | Tool |
|------|------|
| Best novel junction discovery | `STAR` |
| Lower memory footprint | `HISAT2` (this skill) |
| Long-read cDNA | `minimap2 -ax splice:hq` |
| Pseudo-alignment (transcripts only) | `salmon`, `kallisto` |
| Standard bulk RNA-seq | `nf-core/rnaseq` (default STAR, --aligner hisat2 optional) |

## References

- HISAT2 paper: Kim et al. 2019, *Nature Methods* — `10.1038/s41587-019-0201-4`
- HISAT2 manual: <http://daehwankimlab.github.io/hisat2/manual/>
- Companion: `ors-bioinformatics-sequence-star-alignment`, `ors-bioinformatics-sequence-bwa-alignment`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-hisat2-alignment` (bioSkills-main/read-alignment/hisat2-alignment)."