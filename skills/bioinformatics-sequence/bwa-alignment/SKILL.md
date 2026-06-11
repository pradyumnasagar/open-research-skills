---
name: bwa-alignment
description: "Align Illumina short reads to a reference genome with BWA-MEM —\
  \ including index, MEM algorithm, paired-end, alt-contig handling, and 2026 best\
  \ practices.
license: MIT
---

<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- bwa
- bwa-mem
- alignment
- illumina
- short-read
- sam
- bam
difficulty: intermediate
prerequisites:
  tools:
  - bwa>=0.7.17
  - samtools>=1.19
  - reference-index
  skills:
  - ors-bioinformatics-sequence-sam-bam-basics
  - ors-bioinformatics-sequence-fastp-workflow
sources: 'Original: bio-bwa-alignment (bioSkills-main/read-alignment/bwa-alignment);
  Adapted: 2026 BWA-MEM2 alternative, alt-aware alignment (GRCh38), added `-K` and
  `-Y` flag explanations.; Improvisions: added 2026 recommendation to default to BWA-MEM2,
  nf-core integration.'
-->

# BWA-MEM Short-Read Alignment

> BWA-MEM is the workhorse short-read aligner: fast, sensitive, and the
> default in most production pipelines since 2015. BWA-MEM2 is the 2024+
> drop-in replacement with multi-threading and ~2-3x speedup on large
> genomes. This skill covers the canonical workflow: index, align,
> sort/index, mark duplicates — and the flags that matter for variant
> calling.

## When to use

- Aligning Illumina short reads (100-300 bp) to a reference genome.
- Paired-end or single-end DNA-seq, exome, low-pass WGS.
- Building a BAM for variant calling, coverage analysis, or visualization.

## When NOT to use

- Long reads (ONT/PacBio) → use `minimap2` (see `ors-bioinformatics-sequence-minimap2-alignment`).
- RNA-seq → use `STAR` or `HISAT2` (splice-aware).
- Bisulfite-seq → use `bismark`, `bwameth`, or `bwa-meth`.
- ChIP-seq / ATAC-seq → BWA-MEM works, but Bowtie2 may be slightly faster for short reads.

## Prerequisites

- `bwa` ≥ 0.7.17 (or `bwa-mem2` ≥ 2.2.1)
- `samtools` ≥ 1.19
- Reference FASTA + FASTA index (`.fai`)
- BWA index files (`.bwt`, `.pac`, `.ann`, `.amb`)
- Trimmed reads (run `fastp` first)

## Core workflow

1. **Index the reference** with `bwa index` (one-time per reference).
2. **Align** with `bwa mem -t <threads> -M -K <ref> <R1> [<R2>]`.
3. **Stream the SAM output** through `samtools sort` to a coordinate-sorted BAM.
4. **Index the BAM** with `samtools index`.
5. **Mark duplicates** before variant calling (see `ors-bioinformatics-sequence-duplicate-handling`).

## Code patterns

### Build the index (one-time, several minutes for human)

```bash
bwa index -p genome_bwa reference/genome.fa
# Creates genome_bwa.{amb,ann,bwt,pac,sa}
```

Or for BWA-MEM2:

```bash
bwa-mem2 index reference/genome.fa
# Creates genome.fa.{0123,amb,ann,bwt,pac}
```

### Paired-end alignment, coordinate-sorted BAM

```bash
bwa mem -t 16 -M -K 100000000 -R '@RG\tID:sample1\tSM:sample1\tPL:ILLUMINA\tLB:lib1' \
    reference/genome.fa \
    reads/sample1_R1.trimmed.fastq.gz \
    reads/sample1_R2.trimmed.fastq.gz |
  samtools sort -@ 8 -m 4G -o sample1.sorted.bam -
samtools index sample1.sorted.bam
```

### Single-end alignment

```bash
bwa mem -t 16 -M -R '@RG\tID:s1\tSM:s1' ref.fa reads.fq.gz |
  samtools sort -@ 8 -o s1.bam -
samtools index s1.bam
```

### Align to a GRCh38 reference with ALT contigs

For human GRCh38 (or T2T-CHM13), use BWA-MEM's `-j` for ALT-aware soft clipping, and remember that ALT contigs cause false duplicate mappings without special handling.

```bash
bwa mem -t 16 -M -K 100M -j ref.fa sample_R1.fq.gz sample_R2.fq.gz | \
  samtools fixmate -m -O bam - sample.fixmate.bam
samtools sort -@ 8 -o sample.sorted.bam sample.fixmate.bam
samtools markdup -r - sample.dedup.bam  # -r removes ALT duplicates
samtools index sample.dedup.bam
```

`samtools markdup -r` is the modern (samtools ≥ 1.16) way to drop ALT-mapped duplicates from a BAM aligned to GRCh38.

### BWA-MEM2 with same interface

```bash
bwa-mem2 mem -t 16 -M -K 100M ref.fa R1.fq.gz R2.fq.gz |
  samtools sort -@ 8 -o out.bam -
```

### Mark duplicates with samblaster (alternative to `samtools markdup`)

`samblaster` is ~3x faster than `samtools markdup` on typical inputs:

```bash
bwa mem -t 16 -M ref.fa R1.fq.gz R2.fq.gz |
  samblaster |
  samtools sort -@ 8 -o out.bam -
```

### Convert SAM to BAM and stream (saves disk)

```bash
bwa mem -t 8 ref.fa R1.fq.gz R2.fq.gz |
  samtools view -bS - > out.bam
```

### Pull unmapped reads

```bash
samtools view -b -f 4 sample.bam > sample.unmapped.bam
```

### Pull properly-paired, primary alignments only

```bash
samtools view -b -f 2 -F 256 sample.bam > sample.proper.bam
```

### Quick alignment stats

```bash
samtools flagstat sample.bam
samtools coverage sample.bam
```

### Run BWA-MEM on a batch of samples (shell loop)

```bash
for r1 in reads/*_R1.trimmed.fq.gz; do"
  base=$(basename "$r1" _R1.trimmed.fq.gz)
  r2="reads/${base}_R2.trimmed.fq.gz"
  bwa mem -t 16 -M -R "@RG\tID:${base}\tSM:${base}" ref.fa "$r1" "$r2" |
    samtools sort -@ 8 -o "bam/${base}.bam" -
  samtools index "bam/${base}.bam"
done
```

## Important flags explained

| Flag | Meaning | When to use |
|------|---------|-------------|
| `-t N` | Threads | Always (match your cores) |
| `-M` | Picard-compatibility (mark shorter splits as secondary) | Always for variant calling |
| `-K 100000000` | Min seed length (100M = no chunking) | Default for high-quality data; reduce for noisy |
| `-Y` | Use soft clipping for supplementary | Required for downstream variant callers like GATK |
| `-j` | ALT-aware soft clipping | GRCh38 only |
| `-R '@RG\t...'` | Read group header | Required for joint variant calling |
| `-L 100,5` | Clamp penalty | Lower for spliced alignments |
| `-k 19` | Min seed length | Default 19; reduce to 17 for very short inserts |
| `-a` | Output all alignments (not just best) | For diagnostic / chimeric detection |

## Common pitfalls

- **Forgetting the read group (`-R`).** GATK and most variant callers refuse BAMs without an `@RG` line.
- **Using `bwa aln` for short reads.** `bwa mem` is now the default for reads ≥ 70 bp; `bwa aln` is for very short legacy data.
- **Aligning to an un-indexed reference.** BWA's index is a separate step. A missing `.bwt` → cryptic error.
- **Sorting by read name instead of coordinate.** `samtools sort` defaults to coordinate. Use `samtools sort -n` only for `fixmate` input.
- **Mark duplicates before coordinate sort.** The correct order is: align → sort by name → `samtools fixmate` → sort by coordinate → mark duplicates.
- **Aligning to GRCh38 with `-j` but forgetting `markdup -r`.** ALT contigs cause over-duplication; the `-r` flag is critical.

## Validation

- `samtools flagstat sample.bam` — should show >90% mapped for human WGS, 70-85% for exome.
- `samtools coverage sample.bam` — average depth should match sequencing depth expectation.
- `samtools view -c -f 2 sample.bam` — properly-paired count should be near total mapped for paired-end.
- `samtools view -c -F 256 sample.bam` — primary alignment count (no secondary).
- Insert size distribution: `samtools view sample.bam | awk '{print $9}' | sort -n | uniq -c` — should peak near the library insert size.

## Open alternatives

| Need | Tool |
|------|------|
| Drop-in BWA-MEM replacement, faster | `bwa-mem2` (2-3x speedup) |
| ChIP-seq / ATAC-seq | `bowtie2` |
| Long reads | `minimap2` |
| Splice-aware RNA | `STAR`, `HISAT2` |
| Production WGS pipeline | `nf-core/sarek` (includes BWA-MEM2) |

## References

- BWA manual: <http://bio-bwa.sourceforge.net/bwa.shtml>
- BWA-MEM paper: Li 2013, *Bioinformatics* — `10.1093/bioinformatics/bts635`
- BWA-MEM2 paper: Vasimuddin et al. 2019 — `10.1109/HPEC.2019.8916176`
- Companion: `ors-bioinformatics-sequence-samtools-bam-processing`, `ors-bioinformatics-sequence-bwa-mem2-alignment`, `ors-bioinformatics-sequence-fastp-workflow`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-bwa-alignment` (bioSkills-main/read-alignment/bwa-alignment).