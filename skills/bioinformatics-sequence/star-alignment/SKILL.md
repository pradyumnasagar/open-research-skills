---
name: star-alignment
description: "Splice-aware RNA-seq alignment with STAR — the gold-standard aligner\
  \ for novel junction discovery, with 2-pass mapping and genome-generation strategies\
  \ for 2026.
license: MIT
---

<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- star
- rna-seq
- splice
- alignment
- illumina
- junction
difficulty: advanced
prerequisites:
  tools:
  - star>=2.7.11
  - samtools>=1.19
  skills:
  - ors-bioinformatics-sequence-fastp-workflow
sources: 'Original: bio-star-alignment (bioSkills-main/read-alignment/star-alignment);
  Adapted: 2026 STAR 2.7.11+ flag updates, added 2-pass mapping strategy, modern RAM
  guidance.; Improvisions: added cloud-friendly streaming notes, splice junction database
  access.'
-->

# STAR RNA-seq Alignment

> STAR (Spliced Transcripts Alignment to a Reference) is the gold standard
> for RNA-seq alignment — sensitive to novel junctions, fast, and the
> default in `nf-core/rnaseq`. The 2026 reality: STAR 2.7.11+ has improved
> memory management and 2-pass mapping is now standard for sensitive
> analyses. The cost: ~40 GB RAM for human genome index generation.

## When to use

- Bulk RNA-seq with novel junction discovery (most cases).
- Single-cell RNA-seq (`STARsolo`).
- Chimeric / fusion detection (with `--chimOutType`).
- Long-read cDNA / ONT direct RNA (use `--alignEndsType Extend...`).

## When NOT to use

- Genome with no annotation and small memory budget → use `HISAT2` (this category) or `minimap2 -ax splice`.
- DNA-seq → use `bwa-mem` or `bwa-mem2`.
- Quantification-only → use pseudo-alignment (`salmon` / `kallisto`).

## Prerequisites

- `STAR` ≥ 2.7.11
- `samtools` ≥ 1.19
- Reference FASTA + GTF
- ~40 GB RAM and 50 GB disk for human index

## Core workflow

1. **Generate the genome index** with `STAR --runMode genomeGenerate`.
2. **Align reads** with `STAR --runMode alignReads`.
3. **2-pass mapping** for sensitive novel junction discovery: first pass produces a SJ.out.tab, second pass uses it.
4. **Sort and index** the BAM (STAR can output sorted BAM directly with `--outSAMtype BAM SortedByCoordinate`).
5. **Index** the BAM with `samtools index`.

## Code patterns

### Generate the genome index (one-time, ~40 GB RAM for human)

```bash
STAR --runMode genomeGenerate \
    --runThreadN 16 \
    --genomeDir star_index/ \
    --genomeFastaFiles reference/genome.fa \
    --sjdbGTFfile reference/genes.gtf \
    --sjdbOverhang 149 \
    --genomeSAindexNbases 14
```

`--sjdbOverhang 149` for 150 bp reads; for shorter reads, set to `read_length - 1`.

### Paired-end alignment (most common)

```bash
STAR --runMode alignReads \
    --runThreadN 16 \
    --genomeDir star_index/ \
    --readFilesIn reads_R1.fq.gz reads_R2.fq.gz \
    --readFilesCommand zcat \
    --outFileNamePrefix sample1/ \
    --outSAMtype BAM SortedByCoordinate \
    --outSAMattrRGline ID:sample1 SM:sample1 PL:ILLUMINA LB:lib1 \
    --quantMode GeneCounts
```

Output:
- `sample1/Aligned.sortedByCoord.out.bam` — coordinate-sorted BAM
- `sample1/ReadsPerGene.out.tab` — gene-level counts (use this for DESeq2/edgeR)
- `sample1/SJ.out.tab` — splice junctions
- `sample1/Log.final.out` — alignment stats

### 2-pass mapping for novel junction discovery

```bash
# Pass 1: align and produce splice junctions
STAR --runMode alignReads ... --outFileNamePrefix pass1/
mv pass1/SJ.out.tab pass1_SJ.tab

# Pass 2: re-align with discovered junctions
STAR --runMode alignReads \
    --sjdbFileChrStartEnd pass1_SJ.tab \
    --genomeDir star_index_with_pass1_SJ/ \
    ... --outFileNamePrefix pass2/
```

Or use the simpler workflow: regenerate the index with the new SJ file and re-align.

### Single-cell RNA-seq (STARsolo)

```bash
STAR --runMode alignReads \
    --genomeDir star_index/ \
    --readFilesIn sc_R1.fastq.gz sc_R2.fastq.gz \
    --soloType CB_UMI_Simple \
    --soloCBstart 1 --soloCBlen 16 \
    --soloUMIstart 17 --soloUMIlen 10 \
    --soloBarcodeReadLength 0 \
    --soloCellFilter EmptyDrops_CR \
    --outFileNamePrefix sc_outs/
```

### Long-read cDNA / ONT

```bash
STAR --runMode alignReads \
    --genomeDir star_index/ \
    --readFilesIn long_reads.fq.gz \
    --outFilterMismatchNmax 5 \
    --outFilterMatchNmin 10 \
    --alignEndsType ExtendSoftClip
```

### Output sorted BAM and skip the post-alignment sort

```bash
STAR ... --outSAMtype BAM SortedByCoordinate ...
```

This writes the BAM sorted and lets you skip `samtools sort`. You still need `samtools index`.

### Multi-sample parallel alignment (shell loop)

```bash
for r1 in reads/*_R1.fq.gz; do"
  base=$(basename "$r1" _R1.fq.gz)
  r2="reads/${base}_R2.fq.gz"
  mkdir -p "star_out/${base}"
  STAR --runMode alignReads \
      --runThreadN 8 \
      --genomeDir star_index/ \
      --readFilesIn "$r1" "$r2" \
      --readFilesCommand zcat \
      --outFileNamePrefix "star_out/${base}/" \
      --outSAMtype BAM SortedByCoordinate \
      --outSAMattrRGline ID:${base} SM:${base} PL:ILLUMINA \
      --quantMode GeneCounts
done
```

### Index the output BAM

```bash
samtools index sample1/Aligned.sortedByCoord.out.bam
```

### Extract splice junctions for visualization

```bash
# Convert STAR SJ.out.tab to BED12 for IGV
awk 'BEGIN{OFS="\t"} $1 !~ /#/ {print $1, $2-1, $3, ".", $7, $4}' SJ.out.tab > sj.bed
```

## Important flags

| Flag | Purpose |
|------|---------|
| `--runThreadN` | Threads |
| `--genomeDir` | STAR index directory |
| `--readFilesCommand zcat` | Decompress `.gz` |
| `--outSAMtype BAM SortedByCoordinate` | Sorted BAM output |
| `--outSAMattrRGline` | Read group |
| `--quantMode GeneCounts` | Per-gene read counts |
| `--outFilterMismatchNoverLmax 0.1` | Max 10% mismatches (default 0.3) |
| `--outFilterMultimapNmax 1` | Unique alignments only (for some workflows) |
| `--alignSJoverhangMin 8` | Min overhang for splice junction |
| `--twopassMode Basic` | 2-pass mapping (legacy; use --sjdbFileChrStartEnd for 2.7+) |
| `--chimOutType SeparateSAMold` | Chimeric alignments (fusion detection) |

## Common pitfalls

- **Not enough RAM for human index.** `STAR --runMode genomeGenerate` needs ~40 GB. STAR 2.7.11+ has `--limitGenomeGenerateRAM` to bound it, but at the cost of slower index generation.
- **Forgetting `--readFilesCommand zcat`** for `.fq.gz` inputs. STAR will try to read them as text and fail.
- **Using a default `--sjdbOverhang`** for non-150 bp reads. Set to `read_length - 1` for best sensitivity.
- **Ignoring 2-pass mapping.** The first pass discovers novel junctions, the second pass is more sensitive. For novel transcript discovery, 2-pass is essential.
- **STARsolo barcode config.** `CBstart + CBlen` and `UMIstart + UMIlen` must match your library prep. Misconfiguration gives 0% barcodes-in-cells.

## Validation

- `samtools flagstat sample1/Aligned.sortedByCoord.out.bam` — high mapping rate (≥85% for bulk RNA-seq).
- `head sample1/Log.final.out` — look for `Uniquely mapped reads %` ≥ 75%.
- `awk '$4=="Uniquely mapped reads %"' Log.final.out` should be ≥ 70% for most samples.
- `ReadsPerGene.out.tab` should have non-zero counts for known reference genes.

## Open alternatives

| Need | Tool |
|------|------|
| Lower memory footprint | `HISAT2` |
| Pseudo-alignment (faster) | `salmon`, `kallisto` |
| Long-read cDNA | `minimap2 -ax splice:hq` |
| Production bulk RNA-seq | `nf-core/rnaseq` (default STAR) |
| Single-cell RNA-seq | `nf-core/scrnaseq` (default STARsolo), `cellranger` (10x) |

## References

- STAR paper: Dobin et al. 2013, *Bioinformatics* — `10.1093/bioinformatics/bts635`
- STAR 2.7.11+ release notes: <https://github.com/alexdobin/STAR/releases>
- Companion: `ors-bioinformatics-sequence-hisat2-alignment`, `ors-bioinformatics-omics-rna-seq-count-matrix-qc`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-star-alignment` (bioSkills-main/read-alignment/star-alignment).