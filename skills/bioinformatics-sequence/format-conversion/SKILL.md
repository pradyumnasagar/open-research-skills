---
name: format-conversion
description: "Convert between sequence and annotation formats using Biopython SeqIO.convert and custom writers — including batch, lossy, and round-trip-safe patterns."
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- seqio
- fasta
- genbank
- embl
- fastq
- conversion
difficulty: beginner
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills: []"
sources: "Original: bio-format-conversion (bioSkills-main/sequence-io/format-conversion);\
  \ Adapted: pruned the 'convert' pitfalls, added 2026-era notes on round-trip-safe\
  \ formats and seqkit open alternative.; Improvisions: new lossless-vs-lossy table,\
  \ recommendations for EMBL → GenBank via UniParc."
-->

# Sequence Format Conversion

> Format conversion looks trivial — call `SeqIO.convert` and you're done — but
> it isn't. FASTA is *sequence-only*; GenBank/EMBL/INSDC carry annotation
> (features, qualifiers, references); FASTQ carries quality. Crossing those
> boundaries is a one-way trip. This skill is the safe path: which conversions
> are lossless, which lose annotation, and how to batch the safe ones at
> scale.

## When to use

- Switching between FASTA and GenBank for a tool that requires one or the other.
- Converting a directory of `.gb` → `.fasta` for BLAST.
- Converting EMBL → GenBank for NCBI submission compatibility.
- Stripping quality from FASTQ for tools that need FASTA.

## When NOT to use

- Format conversions that need re-validation (e.g., a GenBank you got from a third party — see the `bio-format-validation` skill from `read-qc`).
- Lossy round-trips where you actually need the annotation back: don't go FASTA → GenBank and expect features.

## Prerequisites

- `biopython>=1.83`
- For large-scale batch: `seqkit` (C) is far faster than Python.

## Core workflow

1. **Decide if the conversion is lossless.** Cross-format only when features don't matter, or when both formats are annotation-aware.
2. **Use `SeqIO.convert(src, src_fmt, dst, dst_fmt)`** — it returns the record count and handles buffered I/O.
3. **For streaming, prefer parse + write** when you need to filter or modify on the way through.
4. **Always set explicit formats** — never rely on extension sniffing alone.

## Lossless vs. lossy

| From → To | Sequence | Annotation | Quality |
|-----------|----------|------------|---------|
| FASTA → GenBank | ✓ | ✗ (none to start) | ✗ |
| GenBank → FASTA | ✓ | ✗ (dropped) | ✗ |
| GenBank → EMBL | ✓ | ✓ | ✗ |
| EMBL → GenBank | ✓ | ✓ (with caveats) | ✗ |
| FASTQ → FASTA | ✓ | n/a | ✗ |
| FASTQ → FASTQ (re-encode) | ✓ | n/a | ✓ (re-encoded to Phred+33) |
| GFF3 → BED | n/a | partial (gene-level only) | n/a |

## Code patterns

### GenBank → FASTA (annotation dropped)

```python
from Bio import SeqIO

n = SeqIO.convert("input.gb", "genbank", "out.fasta", "fasta")
print(f"Converted {n} records (annotation discarded)")
```

### FASTA → GenBank (skeleton record, no features)

```python
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

recs = []
for r in SeqIO.parse("input.fasta", "fasta"):
    recs.append(SeqRecord(Seq(str(r.seq)), id=r.id, description=r.description,
                          annotations={"molecule_type": "DNA"}))

SeqIO.write(recs, "out.gb", "genbank")
```

Note: NCBI's tbl2asn will reject records without `molecule_type` and other minimal metadata. Add a translation table annotation if you'll submit.

### EMBL → GenBank

```python
from Bio import SeqIO

n = SeqIO.convert("input.embl", "embl", "out.gb", "genbank")
print(f"Converted {n} records (qualifiers mapped to GenBank qualifiers)")
```

EMBL → GenBank is lossy in edge cases (e.g., `/translation` table differences); always re-validate before submission.

### FASTQ → FASTA (drop quality)

```python
from Bio import SeqIO
SeqIO.write(SeqIO.parse("reads.fastq", "fastq"), "reads.fasta", "fasta")
```

### FASTA → FASTQ (dummy Q-scores)

There's no canonical way — FASTQ *requires* quality. Common convention: write a constant Q40 (ASCII `I`):

```python
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

def fasta_to_fastq_q40(in_fa: str, out_fq: str):
    with open(out_fq, "w") as out:
        for r in SeqIO.parse(in_fa, "fasta"):
            quals = [40] * len(r.seq)
            r.letter_annotations["phred_quality"] = quals
            SeqIO.write(r, out, "fastq")
```

### Batch convert a directory

```python
from pathlib import Path
from Bio import SeqIO

for gb in sorted(Path("genbank").glob("*.gb")):
    out = Path("fasta") / (gb.stem + ".fasta")
    n = SeqIO.convert(str(gb), "genbank", str(out), "fasta")
    print(f"{gb.name} -> {out.name}: {n}")
```

### Streaming with a filter (length ≥ 500 bp)

```python
from Bio import SeqIO

def long_records(path, fmt, min_len=500):
    for r in SeqIO.parse(path, fmt):
        if len(r.seq) >= min_len:
            yield r

SeqIO.write(long_records("input.gb", "genbank"), "long_only.fasta", "fasta")
```

### Re-encode legacy FASTQ to Phred+33

```python
from Bio import SeqIO

records = SeqIO.parse("legacy.fastq", "fastq-illumina")
SeqIO.write(records, "modern.fastq", "fastq")
```

## Common pitfalls

- **GenBank round-trip loses qualifiers not mapped 1-to-1.** Always diff before assuming a clean round-trip.
- **`SeqIO.convert` returns 0 silently** if the source format is wrong. Always `assert n > 0` in pipelines.
- **FASTQ → FASTA can produce files with non-IUPAC characters** if the FASTQ had ambiguity codes. Decide whether to clean first.
- **`molecule_type` annotation missing** → GenBank writers will warn or reject.
- **Don't write features onto a `Seq` from a `SeqIO.parse(... "fasta")` record** — the `seq` is a `Seq` but the record's `features` list is empty by design.

## Validation

- After conversion, `grep -c '^>' out.fasta` equals the record count.
- For GenBank → FASTA → GenBank, compare `Bio.SeqIO.parse()` record counts and IDs.
- For FASTQ re-encoding, re-parse with `fastq` and confirm `letter_annotations["phred_quality"]` are all 40 in the dummy case.

## Open alternatives

| Need | Tool |
|------|------|
| Bulk FASTA → GenBank for tbl2asn | NCBI `tbl2asn` |
| Sequence-only format conversion at scale | `seqkit convert` (C, very fast) |
| FASTA quality inspection | `seqkit fx2tab` |
| Annotation-aware conversion | `gff3_to_genbank` from `pycbio` |

## References

- Biopython convert formats table: <https://biopython.org/wiki/SeqIO#File_Formats>
- INSDC feature table: <https://www.insdc.org/submitting-standards/feature-table/>
- Companion: `ors-bioinformatics-sequence-batch-sequence-processing`, `ors-bioinformatics-sequence-read-write-sequences`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-format-conversion` (bioSkills-main/sequence-io/format-conversion).