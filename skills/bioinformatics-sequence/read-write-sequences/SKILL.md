---
name: read-write-sequences
description: "Read and write FASTA, FASTQ, GenBank, EMBL using Biopython SeqIO — including indexed random access, conversion, and 2026 best practices."
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
- fastq
- genbank
- embl
difficulty: beginner
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills: []
sources: 'Original: bio-read-sequences + bio-write-sequences (bioSkills-main/sequence-io/);
  Adapted: merged read+write into one canonical skill, added 2026 SeqIO.index() guidance.;
  Improvisions: included indexed random-access example, modern format strings table.'
-->

# Read and Write Sequence Files

> `SeqIO` is the I/O workhorse of Biopython. Three functions cover 90% of
> the work: `parse` (streaming), `index` (random access by ID), and
> `write` (single or batch). The remainder is `convert` for the times you
> don't need to touch the records. This skill is the cheat sheet I keep
> open.

## When to use

- Streaming reads from FASTA/FASTQ/GenBank/EMBL.
- Random access to a record by ID (huge files).
- Writing records back out, optionally after modification.
- Format conversion without touching record content.

## When NOT to use

- BAM/SAM/CRAM/VCF → use `pysam` (see `ors-bioinformatics-sequence-pysam-genomics`).
- gzipped BAM/CRAM with random access → `pysam.AlignmentFile`.
- For >10 GB files, consider `pyfastx` (faster than Biopython for FASTA).

## Prerequisites

- `biopython>=1.83`
- For indexed random access on BGZF FASTA, Biopython 1.83+ supports `index()` on `.bgz`.

## Format strings (cheat sheet)

| Format | String | Notes |
|--------|--------|-------|"
| FASTA | `"fasta"` | Sequence only, single-line or wrapped |
| FASTQ (Sanger / Illumina 1.8+) | `"fastq"` | Phred+33 |
| FASTQ (Illumina 1.3-1.7) | `"fastq-illumina"` | Phred+64 |
| FASTQ (Solexa) | `"fastq-solexa"` | Solexa+64 |
| GenBank | `"genbank"` | Annotation + sequence |
| EMBL | `"embl"` | EBI submission format |
| SwissProt | `"swiss"` | UniProt curated |
| UniProt XML | `"uniprot-xml"` | EBI download |
| GFF3 | `"gff3"` | Genome features, not sequence records |
| GTF | `"gtf"` | Gene transfer format |
| ABI | `"abi"` | Sanger trace |
| Phylip | `"phylip"` | Alignment |
| Clustal | `"clustal"` | Alignment |
| Stockholm | `"stockholm"` | Pfam/Rfam |
| Tab-delimited | `"tab"` | ID, seq, optional qualifiers |

## Code patterns

### Stream parse

```python
from Bio import SeqIO

for rec in SeqIO.parse("input.fasta", "fasta"):
    # rec.id, rec.description, rec.seq
    ...
```

### List parse (small files only)

```python
records = list(SeqIO.parse("small.fasta", "fasta"))
```

### Indexed random access (huge FASTA)

```python
from Bio import SeqIO

db = SeqIO.index("large.fasta", "fasta")
seq = db["target_id"].seq
db.close()
```

For persistent index (no rebuild on next open):

```python
db = SeqIO.index_db("large.idx", "large.fasta", "fasta")
```

### Indexed BGZF random access

```python
db = SeqIO.index("indexable.fasta.bgz", "fasta")
```

### Write records (single file, multiple records)

```python
from Bio import SeqIO

SeqIO.write(records, "out.fasta", "fasta")
```

The return value is the number of records written.

### Write one record at a time

```python
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

with open("out.fasta", "w") as fh:
    rec = SeqRecord(Seq("ACGT"), id="seq1", description="example")
    SeqIO.write(rec, fh, "fasta")
```

### Append records across formats (streaming)

```python
from Bio import SeqIO

def stream_to_fasta(in_path, in_fmt, out_path):
    with open(out_path, "w") as out:
        for rec in SeqIO.parse(in_path, in_fmt):
            # modify rec if needed
            SeqIO.write(rec, out, "fasta")
```

### Convert without touching records

```python
from Bio import SeqIO
n = SeqIO.convert("in.gb", "genbank", "out.fasta", "fasta")
print(f"Converted {n} records")
```

### Handle FASTA with wrapped multi-line sequences

Biopython auto-handles wrapped FASTA in `parse()`; `record.seq` is always the full sequence.

### Parse GenBank with features

```python
from Bio import SeqIO

for rec in SeqIO.parse("annotation.gb", "genbank"):
    for feat in rec.features:
        if feat.type == "CDS":
            gene = feat.qualifiers.get("gene", ["?"])[0]
            print(gene, feat.location)
```

### Parse BLAST tab output

```python
from Bio import SeqIO
for qresult in SeqIO.parse("blast.tab", "blast-tab"):
    for hsp in qresult:
        ...
```

`blast-tab` parses the tabular `-outfmt 6`.

### Truncate IDs to first whitespace

```python
def short_id(rec):
    rec.id = rec.id.split()[0]
    rec.description = ""
    return rec
```

## Common pitfalls

- **Mixing parse() with index() and forgetting to close the index.** Index files hold file handles; use a context manager or explicit `close()`.
- **Indexed access on a `.fasta.gz` (plain gzip) fails.** Convert to BGZF first.
- **Write format mismatch.** If you parsed with `"fastq-illumina"` and wrote with `"fastq"`, Biopython re-encodes qualities. Usually fine, but worth being explicit.
- **Mismatched record count from `SeqIO.convert`.** Returns 0 silently if source format is wrong. `assert n > 0`.
- **Header pollution.** FASTA identifiers stop at first whitespace; multi-word descriptions go into `description`. If you write a record with both `id="seq1 chr1"` and a description, downstream tools will see `seq1` as the ID.

## Validation

- `n_records_in == n_records_out` for round-trips.
- For indexed access: `db["known_id"].seq == expected_seq`.
- For GenBank round-trips: `len(features_in) == len(features_out)`, modulo per-format feature filtering.

## Open alternatives

| Need | Tool |
|------|------|
| Faster FASTA parsing | `pyfastx` |
| Format conversion at scale | `seqkit convert`, `bioawk` |
| Random access to huge FASTA | `samtools faidx` + bgzip |
| GFF/GTF parsing | `gffutils`, `pyranges` |

## References

- Biopython SeqIO: <https://biopython.org/docs/latest/api/Bio.SeqIO.html>
- Format list: <https://biopython.org/wiki/SeqIO#File_Formats>
- Companion: `ors-bioinformatics-sequence-format-conversion`, `ors-bioinformatics-sequence-compressed-sequence-files`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-read-sequences` and `bio-write-sequences` (bioSkills-main/sequence-io/).