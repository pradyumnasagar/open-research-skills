---

name: reverse-complement
description: "Compute reverse complements, complements, and strand-aware operations on DNA/RNA — including IUPAC ambiguity support, batch processing, and the orientation trap."
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

# Reverse Complement and Strand Operations

> Reverse-complement is the single most error-prone operation in genomics
> scripting. Get the orientation wrong and your gene is on the opposite
> strand, your primer doesn't match, your probe is a hairpin. This skill
> gives you the right call for every case: complement vs reverse-complement,
> IUPAC ambiguity handling, batch processing, and the"
> "which strand am I on?" sanity checks.

## When to use

- Computing reverse complements of DNA/RNA for primer/probe design.
- Translating minus-strand genes.
- Converting a feature's coordinates from one strand to the other.
- Building batch reverse-complement pipelines for FASTA/FASTQ.

## When NOT to use

- You actually want just the complement (preserving 5'→3' direction) — use `.complement()`.
- For very high-throughput reverse-complement (millions of reads), use `seqkit` or `pyfastx`.

## Prerequisites

- `biopython>=1.83`
- For shell-scale: `seqkit seq -r` (reverse) and `seqkit seq -p` (reverse-complement)

## Core workflow

1. **Decide: complement or reverse-complement?**
2. **Use `Bio.Seq`'s built-in methods** (which handle IUPAC ambiguity correctly).
3. **For batch**, stream records through a generator.
4. **Always log a sanity check** (e.g., reverse-complement of reverse-complement is the original).

## The orientation decision

| You have | You want | Method |
|----------|----------|--------|
| Coding strand (sense) | mRNA sequence | `.transcribe()` |
| Coding strand (sense) | Protein | `.translate()` |
| Template strand (antisense) | Coding strand | `.reverse_complement()` first, then `.transcribe()` |
| mRNA | cDNA (T for U) | `.back_transcribe()` |
| Coding strand, want other strand's sequence | Other strand | `.reverse_complement()` |

## Code patterns

### Basic reverse complement

```python
from Bio.Seq import Seq

s = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
s.reverse_complement()
# Seq('CTATCGGGCACCCTTTCAGCGGCCCATTACAATGGCCAT')
```

### Complement (no reversal)

```python
s = Seq("ATGC")
s.complement()   # Seq('TACG') — still 5'→3', just base-paired
```

### IUPAC ambiguity is built-in

```python
s = Seq("ATGNRYWSKM")
s.reverse_complement()
# Seq('MKRSWYNCAT') — all ambiguity codes are handled
```

IUPAC complement table:

| A | T | C | G | R | Y | S | W | K | M | B | D | H | V | N |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T | A | G | C | Y | R | S | W | M | K | V | H | D | B | N |

### RNA reverse complement

```python
from Bio.Seq import Seq

rna = Seq("AUGCCAUUG")  # 5' → 3' mRNA
rna.reverse_complement_rna()  # 5' → 3' of the antisense strand
```

Or transcribe to DNA first:

```python
dna = rna.back_transcribe()
dna.reverse_complement()
```

### Reverse-complement every record in a FASTA

```python
from Bio import SeqIO

def rc_records(in_path, out_path):
    with open(out_path, "w") as out:
        for rec in SeqIO.parse(in_path, "fasta"):
            rec.seq = rec.seq.reverse_complement()
            rec.id = f"{rec.id}_rc"
            rec.description = "reverse complement"
            SeqIO.write(rec, out, "fasta")

rc_records("input.fasta", "rc.fasta")
```

### Batch with Polars/streaming

```python
from Bio import SeqIO

with open("rc.fasta", "w") as out:
    for rec in SeqIO.parse("primers.fasta", "fasta"):
        rec.seq = rec.seq.reverse_complement()
        SeqIO.write(rec, out, "fasta")
```

### Sanity check: revcomp of revcomp is identity

```python
def assert_revcomp_identity(s):
    assert s == s.reverse_complement().reverse_complement()
```

### Extract a feature and reverse-complement

```python
from Bio import SeqIO

rec = next(SeqIO.parse("chr1.gb", "genbank"))
for feat in rec.features:
    if feat.type == "CDS" and feat.location.strand == -1:
        nt = feat.extract(rec.seq)
        cds = nt.reverse_complement()  # now on + strand
        print(cds.translate())
```

### Reverse-complement a region of a chromosome

```python
def rc_region(record, start, end):
    return record.seq[start:end].reverse_complement()
```

## Common pitfalls

- **Complement instead of reverse-complement.** The most common bug. If you're on the minus strand and you call `.complement()`, you'll be working on the wrong strand.
- **Lowercase sequences.** `.reverse_complement()` works on lowercase; just remember the output is whatever case the input was.
- **RNA vs DNA.** `reverse_complement()` is for DNA. For RNA, use `reverse_complement_rna()` or transcribe first.
- **Strand annotation lost.** If you take `feature.extract(record.seq)`, the extracted `Seq` is a fresh sequence and the feature's `strand` info is gone. Reverse-complement explicitly when you need to flip strand.
- **Assuming IUPAC ambiguity in hand-rolled code.** Don't write your own `s.translate(str.maketrans("ACGT", "TGCA"))` — it breaks on `N`, `R`, `Y`, etc.

## Validation

- `s.reverse_complement().reverse_complement() == s`.
- The first base of the reverse-complement is the complement of the last base of the input.
- Length is preserved.
- GC content is preserved (`gc_fraction` of input and rc are equal).

## Open alternatives

| Need | Tool |
|------|------|
| FASTA reverse-complement at scale | `seqkit seq -p -r in.fasta` |
| FASTX reverse-complement | `seqtk seq -r in.fq` |
| Reverse-complement in shell pipeline | `bioawk -c fastx '{print ">"$name"_rc\n"revcomp($seq)}' in.fasta` |
| Reverse-complement on huge genome | `pyfastx` (C-accelerated) |

## References

- Biopython reverse-complement: <https://biopython.org/docs/latest/api/Bio.Seq.html>
- IUPAC codes: <https://www.bioinformatics.org/sms/iupac.html>
- Companion: `ors-bioinformatics-sequence-seq-objects`, `ors-bioinformatics-sequence-transcription-translation`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-reverse-complement` (bioSkills-main/sequence-manipulation/reverse-complement).