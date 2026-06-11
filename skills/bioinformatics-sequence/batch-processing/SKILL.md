---
name: batch-processing
description: "Process many FASTA/FASTQ/GenBank files in batch — merge, split,"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- seqio
- batch
- fasta
- fastq
- automation
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills: []
sources: 'Original: bio-batch-processing (bioSkills-main/sequence-io/batch-processing);
  Adapted: rewritten prose, added streaming memory tips, 2025-2026 Biopython 1.83+
  API notes, dropped multiprocessing deep-dive in favor of Polars-friendly patterns.;
  Improvisions: new ''aggregate to Parquet'' pattern, 2026-era guidance on nf-core
  and BioContainers for true production batch jobs.'
-->

# Batch Sequence File Processing

> When you have 5 files, a `for` loop is enough. When you have 5,000, you need
> streaming iterators, a single-pass design, and a deterministic way to merge,
> split, and summarize. This skill is the playbook for the in-between zone —
> Python, Biopython `SeqIO`, and the `pathlib` patterns I reach for daily.

## When to use

- You have a directory tree of FASTA/FASTQ/GenBank files and need to merge them, split them, convert formats, or compute aggregate stats.
- You need to organize records by some attribute (sample ID, GC content, taxonomy prefix) into per-bin output files.
- You're prototyping before porting to nf-core / Snakemake and want a clear Python baseline.

## When NOT to use

- Real production pipelines at petabyte scale — use `nf-core/rnaseq`, `nf-core/sarek`, or Snakemake with `pysam`-backed streaming.
- Variant-level work (use the variant-calling skills in this category instead).
- Tasks that are fundamentally one-file — see the individual `read-sequences`/`write-sequences` skills.

## Prerequisites

- Python 3.10+
- `biopython>=1.83` (`pip install biopython`)
- For Parquet/Polars summaries: `polars>=1.0`

## Core workflow

1. **Inventory first.** Use `Path.glob()` (recursive when needed) to enumerate inputs. Always sort the result — `glob` order is filesystem-dependent.
2. **Stream, don't slurp.** Wrap file iteration in a generator that yields `SeqRecord` objects; never build a list of millions of records in memory.
3. **Compute on the way through.** Aggregate counters and statistics in a single pass.
4. **Write once.** `SeqIO.write` accepts an iterator, so the read pipeline can feed the write pipeline directly.
5. **Persist summaries as Parquet/CSV** for downstream analysis (Polars, pandas, DuckDB).

## Code patterns

### Stream and count across a directory

```python
from pathlib import Path
from Bio import SeqIO

def count_records(directory: Path, pattern: str, fmt: str):
    for fp in sorted(directory.glob(pattern)):
        n = sum(1 for _ in SeqIO.parse(fp, fmt))"
        yield {"file": fp.name, "records": n, "format": fmt}

for row in count_records(Path("data/"), "*.fasta.gz", "fasta"):
    print(row)
```

### Merge with provenance in the description

When the source file matters later (downstream filters, audits), tag each record:

```python
from pathlib import Path
from Bio import SeqIO

def with_source(directory: Path, pattern: str, fmt: str):
    for fp in sorted(directory.glob(pattern)):
        for rec in SeqIO.parse(fp, fmt):
            rec.description = f"{rec.description} [source={fp.name}]"
            yield rec

n = SeqIO.write(with_source(Path("data/"), "*.fa", "fasta"),
                "merged.fasta", "fasta")
print(f"Wrote {n} records")
```

### Split a huge FASTA into N-record chunks

```python
from itertools import islice
from Bio import SeqIO

def split_by_count(in_path: str, fmt: str, n_per_file: int, prefix: str):
    it = SeqIO.parse(in_path, fmt)
    i = 0
    while True:
        batch = list(islice(it, n_per_file))
        if not batch:
            return
        i += 1
        out = f"{prefix}_{i:04d}.{fmt}"
        SeqIO.write(batch, out, fmt)
        print(f"{out}: {len(batch)} records")

split_by_count("huge.fasta", "fasta", 10_000, "chunk")
```

### Split by sample/chromosome prefix

```python
from collections import defaultdict
from Bio import SeqIO

groups = defaultdict(list)
for rec in SeqIO.parse("input.fasta", "fasta"):
    groups[rec.id.split("|")[0]].append(rec)

for prefix, recs in groups.items():
    SeqIO.write(recs, f"{prefix}.fasta", "fasta")
```

### Batch format convert

```python
from pathlib import Path
for gb in sorted(Path("genbank").glob("*.gb")):
    out = Path("fasta") / gb.with_suffix(".fasta").name
    n = SeqIO.convert(str(gb), "genbank", str(out), "fasta")
    print(f"{gb.name} -> {out.name}: {n}")
```

### Aggregate per-file stats to Parquet

```python
from pathlib import Path
import polars as pl
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

rows = []
for fa in sorted(Path("data/").glob("*.fasta")):
    lengths = [len(r.seq) for r in SeqIO.parse(fa, "fasta")]
    if not lengths:
        continue
    rows.append({
        "file": fa.name,
        "n_records": len(lengths),
        "total_bp": sum(lengths),
        "min_len": min(lengths),
        "median_len": sorted(lengths)[len(lengths) // 2],
        "max_len": max(lengths),
    })

pl.DataFrame(rows).write_parquet("summary.parquet")
```

### Organize by GC content bin

```python
from pathlib import Path
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

high, low = Path("high_gc"), Path("low_gc")
high.mkdir(exist_ok=True)
low.mkdir(exist_ok=True)

for fa in Path("input").glob("*.fasta"):
    recs = list(SeqIO.parse(fa, "fasta"))
    avg_gc = sum(gc_fraction(r.seq) for r in recs) / len(recs)
    dest = high if avg_gc >= 0.55 else low
    SeqIO.write(recs, dest / fa.name, "fasta")
```

### Parallel count with `concurrent.futures`

`ThreadPoolExecutor` is usually fine for I/O-bound sequence parsing; switch to `ProcessPoolExecutor` if you do CPU-heavy work per record (translation, alignment, etc.).

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from Bio import SeqIO

def count(fp: Path) -> tuple[str, int]:
    return fp.name, sum(1 for _ in SeqIO.parse(fp, "fastq"))

with ThreadPoolExecutor(max_workers=8) as ex:
    for name, n in ex.map(count, sorted(Path(".").glob("*.fastq.gz"))):
        print(f"{name}\t{n}")
```

## Common pitfalls

- **Memory blow-up on `list(SeqIO.parse(...))`.** If the file is >1 GB, materialize only the records you need; otherwise stream.
- **Non-deterministic order.** `Path.glob()` results are not guaranteed sorted. Always `sorted()`.
- **Hidden `'.fasta.gz'` formats.** `SeqIO` reads `.gz` natively, but you must pass `"fasta"` (not `"fasta-gz"`) and accept the slower text path.
- **Empty `summary.csv` writes.** Don't write a header if `summaries` is empty — handle the zero-record case.
- **Mixing GenBank and FASTA with the same parser.** Use `SeqIO.convert(src, src_fmt, dst, dst_fmt)` for format-boundary code; it returns record count for free.

## Validation

- Run a row-count check: total records out equals total records in (modulo your filter).
- For round-trip conversions (GenBank → FASTA → GenBank), verify the FASTA round-trips back to a valid GenBank.
- Spot-check: `head -n 4 merged.fasta | grep '^>'` should show the `[source=...]` provenance tags.

## Open alternatives

- **`nf-core` modules** for production: `nf-core/modules` has a `samtools_faidx` and `seqkit_stats` you can call directly.
- **SeqKit** (`seqkit stats *.fasta`) is faster than Python for stats-only tasks and is installed in most BioContainers images.
- **SeqKit + GNU parallel** if you want shell-only batch processing: `seqkit stats -j 8 *.fasta | tee summary.tsv`.

## References

- Biopython `SeqIO` tutorial: <https://biopython.org/wiki/SeqIO>
- Polars IO docs: <https://pola-rs.github.io/polars/py-polars/html/reference/io.html>
- Companion: `ors-bioinformatics-sequence-compressed-sequence-files` for `.gz`/`.bgz` handling.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-batch-processing` (bioSkills-main/sequence-io/batch-processing).