---
name: ors-bioinformatics-sequence-bowtie2-alignment
display_name: "Bowtie2 Alignment for ChIP-seq / ATAC-seq"
description: "Align short reads to a reference with Bowtie2 — the standard aligner for ChIP-seq, ATAC-seq, and other short-fragment applications where sensitivity for short indels matters less than speed."
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: bioinformatics-sequence
tags: [bowtie2, alignment, chip-seq, atac-seq, short-read]
difficulty: intermediate
prerequisites:
  tools: [bowtie2>=2.5, samtools>=1.19]
  skills: [ors-bioinformatics-sequence-fastp-workflow]
sources_consulted:
  - "Original: bio-bowtie2-alignment (bioSkills-main/read-alignment/bowtie2-alignment); Adapted: 2026 Bowtie2 2.5.x flag updates, added ATAC-seq-specific notes."
  - "Improvisions: added modern nf-core/chipseq and nf-core/atacseq integration pointers."
last_updated: 2026-06-10
---

# Bowtie2 Alignment for ChIP-seq / ATAC-seq

> Bowtie2 is the workhorse for ChIP-seq, ATAC-seq, and other short-fragment
> applications. It's faster than BWA-MEM for reads ≤ 100 bp and handles
> gapped alignment with reasonable sensitivity. The 2026 reality: Bowtie2
> is still the default in most ChIP-seq and ATAC-seq pipelines, with
> STAR and BWA-MEM2 as alternatives for specific use cases.

## When to use

- ChIP-seq / CUT&RUN / CUT&Tag alignment.
- ATAC-seq alignment (with `--local` for Tn5 soft-clipping).
- Whole-genome bisulfite-seq (with `--no-mixed --no-discordant`).
- Any read length 50-150 bp where speed matters.

## When NOT to use

- Long reads → use `minimap2`.
- Variant calling on whole-genome data → use `bwa-mem` or `bwa-mem2`.
- RNA-seq splice alignment → use `STAR` or `HISAT2`.

## Prerequisites

- `bowtie2` ≥ 2.5
- `samtools` ≥ 1.19
- Reference FASTA + Bowtie2 index (`bowtie2-build`)

## Code patterns

### Index the reference

```bash
bowtie2-build --threads 8 reference/genome.fa genome_bt2
# Creates genome_bt2.{1,2,3,4,rev.1,rev.2}
```

For very large genomes, use the `--large-index` flag.

### Paired-end alignment (ChIP-seq default)

```bash
bowtie2 -p 16 --no-mixed --no-discordant \
    -x genome_bt2 \
    -1 reads_R1.fq.gz -2 reads_R2.fq.gz \
    --rg-id sample1 --rg SM:sample1 --rg PL:ILLUMINA \
    --rg LB:lib1 |
  samtools sort -@ 8 -m 4G -o sample1.bam -
samtools index sample1.bam
```

`--no-mixed --no-discordant` ensures that only properly paired reads are reported; useful for fragment length analysis.

### Single-end alignment (CUT&RUN, ATAC-seq)

```bash
bowtie2 -p 16 --local -x genome_bt2 -U reads.fq.gz |
  samtools sort -@ 8 -o s1.bam -
samtools index s1.bam
```

`--local` enables soft-clipping at read ends, which is essential for Tn5 transposase-cut reads in ATAC-seq.

### `--very-sensitive` for low-input or divergent samples

```bash
bowtie2 --very-sensitive-local -p 16 -x bt2 -1 R1.fq -2 R2.fq | \
  samtools sort -@ 8 -o s.bam -
```

Sensitivity levels: `--fast`, `--sensitive` (default), `--very-sensitive`. Time increases roughly 2x between levels.

### Allow unpaired reads from a paired run

Drop `--no-mixed --no-discordant` if you want to keep the unpaired mates:

```bash
bowtie2 -p 16 -x bt2 -1 R1.fq -2 R2.fq | samtools sort -@ 8 -o s.bam -
```

### ATAC-seq specific: soft-clip Tn5, keep mitochondrial reads but flag them later

```bash
bowtie2 -p 16 --local --no-mixed --no-discordant -X 2000 \
    -x bt2 -1 R1.fq.gz -2 R2.fq.gz |
  samtools sort -@ 8 -o s.bam -
```

Then mark duplicates and remove chrM with:

```bash
samtools view -h s.bam | grep -v chrM | samtools view -b -o s.no_chrM.bam
samtools index s.no_chrM.bam
```

### Read group in the header (for downstream tools)

```bash
bowtie2 -p 16 --rg-id s1 --rg SM:s1 --rg PL:ILLUMINA --rg LB:lib1 \
    -x bt2 -1 R1.fq -2 R2.fq | samtools sort -@ 8 -o s.bam -
```

### Insert size distribution (for ChIP-seq fragment QC)

```bash
samtools view -f 2 s.bam | awk '{print $9}' | sort -n | uniq -c > insert_sizes.txt
```

### nf-core integration

`nf-core/chipseq` and `nf-core/atacseq` default to Bowtie2. No CLI changes needed.

## Common pitfalls

- **Using `--end-to-end` for ATAC-seq.** Tn5 transposase inserts at precise offsets and the read may start with the transposon sequence, so `--local` is required.
- **No read group.** Downstream tools (MACS2, deepTools) often require `@RG` headers.
- **Allowing `--no-mixed --no-discordant` for very low input.** If most of your reads are unpaired, this discards them. Drop these flags.
- **Indexing the wrong reference.** Bowtie2 indexes are large (`.bt2` files). Keep them in a `reference/` directory.
- **Confusing Bowtie1 and Bowtie2.** Bowtie1 is ungapped; for ChIP/ATAC, you almost always want Bowtie2.

## Validation

- `samtools flagstat s.bam` — should show high mapping rate (≥80% for ChIP-seq, ≥95% for ATAC-seq excluding chrM).
- `samtools view -c -f 2 s.bam` — properly-paired count.
- Insert size histogram: ChIP-seq TF should peak at ~150-300 bp; nucleosome-depleted ChIP-seq at ~50-100 bp; ATAC-seq at sub-nucleosomal + nucleosomal modes.
- `samtools view -F 4 s.bam | wc -l` — mapped reads.

## Open alternatives

| Need | Tool |
|------|------|
| RNA-seq splice-aware | `STAR`, `HISAT2` |
| WGS variant calling | `bwa-mem`, `bwa-mem2` |
| Long reads | `minimap2` |
| ChIP-seq peak caller | `MACS2`, `MACS3` |
| ATAC-seq peak caller | `MACS2`, `Genrich` |

## References

- Bowtie2 paper: Langmead & Salzberg 2012, *Nature Methods* — `10.1038/nmeth.1923`
- Bowtie2 manual: <http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml>
- Companion: `ors-bioinformatics-sequence-bwa-alignment`, `ors-bioinformatics-sequence-bwa-mem2-alignment`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-bowtie2-alignment` (bioSkills-main/read-alignment/bowtie2-alignment).
