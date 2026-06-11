---
name: compressed-sequence-files
description: "Read and write gzip, bzip2, and BGZF-compressed FASTA/FASTQ using Python"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- bgzf
- gzip
- compression
- fasta
- fastq
difficulty: beginner
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills: []
sources: 'Original: bio-compressed-files (bioSkills-main/sequence-io/compressed-files);
  Adapted: trimmed mode-table, added 2025-2026 BGZF guidance, added SeqKit/HTSlib
  open alternatives.; Improvisions: new auto-detect helper, htslib bgzip recommendation
  for BAM/VCF pipelines.'
-->

# Compressed Sequence Files (gzip / bzip2 / BGZF)

> Every modern sequencing deliverable is compressed, but only **BGZF** is
> indexable. If you ever need to seek into a `.fasta.gz` from Python — for
> `SeqIO.index()`, region queries, or `tabix`-style lookups — you must convert
> it to BGZF first. This skill covers the three formats you'll actually meet,
> the `'rt'/'wt'` text-mode trap, and when to reach for `htslib bgzip` instead.

## When to use

- Reading or writing `.fasta.gz`, `.fastq.gz`, `.fasta.bz2` in Python.
- Producing or consuming indexable compressed FASTA (BGZF).
- Building pipelines that need random access into compressed records.

## When NOT to use
"
- Plain uncompressed FASTA — open with `SeqIO.parse(path, "fasta")` directly.
- BAM/CRAM/VCF BGZF: use `pysam` (see `ors-bioinformatics-sequence-pysam-genomics`).
- Whole-genome-scale index needs → use `samtools faidx` + bgzip, not Biopython.

## Prerequisites

- `biopython>=1.83` (ships `Bio.bgzf`).
- For production BGZF: `htslib` ≥ 1.19 (`bgzip` + `tabix`).
- For bzip2: Python's stdlib `bz2`.

## Core workflow

1. **Open in text mode** (`'rt'` / `'wt'`). The parser expects text. `'rb'` will trip on a bytes-vs-str `TypeError`.
2. **Pick the format by use case**:
   - `.gz` → archive only, not indexable.
   - `.bz2` → smaller but slower; archive only.
   - `.bgz` → indexable via `SeqIO.index()`; native for BAM/VCF/tabix.
3. **For new pipelines, prefer BGZF** unless you have a hard reason to use plain gzip.
4. **For BAM/VCF, always use `htslib bgzip`** — its blocks are HTSlib-compatible; Biopython's BGZF works but is slower on huge files.

## Code patterns

### Read gzipped FASTA

```python
import gzip
from Bio import SeqIO

with gzip.open("sequences.fasta.gz", "rt") as fh:
    for rec in SeqIO.parse(fh, "fasta"):
        print(rec.id, len(rec.seq))
```

### Read bzip2

```python
import bz2
from Bio import SeqIO

with bz2.open("reads.fastq.bz2", "rt") as fh:
    recs = list(SeqIO.parse(fh, "fastq"))
```

### Write gzipped output

```python
import gzip
from Bio import SeqIO

with gzip.open("clean.fasta.gz", "wt") as out:
    SeqIO.write(records, out, "fasta")
```

### Read BGZF (text path) and via `bgzf.open`

```python
from Bio import SeqIO, bgzf

# Either works
for rec in SeqIO.parse("seqs.fasta.bgz", "fasta"):
    ...

with bgzf.open("seqs.fasta.bgz", "rt") as fh:
    for rec in SeqIO.parse(fh, "fasta"):
        ...
```

### Write BGZF for downstream indexing

```python
from Bio import SeqIO, bgzf

with bgzf.open("indexable.fasta.bgz", "wt") as out:
    SeqIO.write(SeqIO.parse("raw.fasta", "fasta"), out, "fasta")
```

### Index a BGZF file (random access by record ID)

```python
from Bio import SeqIO

db = SeqIO.index("seqs.fasta.bgz", "fasta")
print(db["target_id"].seq)
db.close()

# Or persistent on-disk index for huge files
db = SeqIO.index_db("seqs.idx", "seqs.fasta.bgz", "fasta")
```

### Auto-detect by extension (single entry point)

```python
from pathlib import Path
import gzip, bz2
from Bio import SeqIO, bgzf

def open_seq(path: str, fmt: str):
    p = Path(path)
    sfx = "".join(p.suffixes).lower()
    if sfx.endswith(".bgz") or sfx.endswith(".bgzf"):
        fh = bgzf.open(p, "rt")
    elif sfx.endswith(".gz") or sfx.endswith(".bgzf"):
        fh = gzip.open(p, "rt")
    elif sfx.endswith(".bz2"):
        fh = bz2.open(p, "rt")
    else:
        fh = open(p, "r")
    return SeqIO.parse(fh, fmt)
```

### Convert plain gzip to indexable BGZF

```python
import gzip
from Bio import SeqIO, bgzf

with gzip.open("input.fasta.gz", "rt") as src, \
     bgzf.open("indexable.fasta.bgz", "wt") as dst:
    SeqIO.write(SeqIO.parse(src, "fasta"), dst, "fasta")
```

### Low-memory record count (FASTA)

```python
import gzip
from Bio.SeqIO.FastaIO import SimpleFastaParser

with gzip.open("sequences.fasta.gz", "rt") as fh:
    n = sum(1 for _ in SimpleFastaParser(fh))
print(f"{n} sequences")
```

## Common pitfalls

- **Using `'rb'` instead of `'rt'`.** You'll get `TypeError: a bytes-like object is required, not 'str'`.
- **Expecting `SeqIO.index()` to work on plain `.gz`.** It does not — convert to BGZF first.
- **Mixing Biopython BGZF with `htslib bgzip` blocks.** They are wire-compatible for FASTA, but for `.vcf.gz`/`.bcf` use `htslib bgzip` end-to-end to avoid rare edge cases.
- **Decompressing to disk then re-reading.** Wastes 3-4x disk. Stream from the compressed handle.
- **`.bz2` is *slow*.** For long-term archives, yes; for active work, prefer BGZF.

## Validation

- File ends with the correct magic: `gzip` → `1f 8b`, `bzip2` → `42 5a`, BGZF → `1f 8b 08 04` (with extra fields).
- After BGZF write, `SeqIO.index("out.bgz", "fasta")["known_id"]` returns the same record.
- Round-trip: `bgzf open → gzip open` byte counts differ only by BGZF block overhead.

## Open alternatives

| Need | Open tool | Why |
|------|-----------|-----|
| Indexable compressed FASTA | `htslib bgzip` (≥ 1.19) | BAM/VCF-compatible blocks |
| Fast stats on `.fasta.gz` | `seqkit stats -j 8 *.fasta.gz` | Much faster than Python |
| Random access by region | `samtools faidx regions.fa.gz` + bgzip | Standard, battle-tested |
| BGZF block dump | `bgzip -b 0 -d out.fa.gz` | Inspect block boundaries |

## References

- BGZF spec: <https://samtools.github.io/hts-specs/SAMv1.pdf> (section 4)
- HTSlib bgzip: <http://www.htslib.org/doc/bgzip.html>
- Biopython bgzf: <https://biopython.org/docs/latest/api/Bio.bgzf.html>
- Companion: `ors-bioinformatics-sequence-pysam-genomics`, `ors-bioinformatics-sequence-samtools-bam-processing`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-compressed-files` (bioSkills-main/sequence-io/compressed-files).