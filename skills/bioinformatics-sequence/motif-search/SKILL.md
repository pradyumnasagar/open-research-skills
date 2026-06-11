---
name: motif-search
description: "Find patterns, motifs, and binding sites in DNA/RNA/protein sequences"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- regex
- motif
- pwm
- jaspar
- binding-site
difficulty: intermediate
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  - regex>=2024.5
  skills:
  - ors-bioinformatics-sequence-seq-objects
sources: 'Original: bio-motif-search (bioSkills-main/sequence-manipulation/motif-search);
  Adapted: Bio.motifs 2026 status, added JASPAR 2024 fetch, modern alternative is
  pyjaspar.; Improvisions: added position weight matrix scanning, de novo motif discovery
  pointer (MEME, STREME).'
-->

# Motif and Pattern Search
"
> Three kinds of "motif" hide in sequences: a literal pattern (TATA box),
> an IUPAC consensus (RRRYYCC, the poly-A signal), or a statistical profile
> (a JASPAR PWM for a TF). Each demands a different tool. This skill covers
> regex / IUPAC exact search, position weight matrix scanning, and the
> modern 2026 open databases.

## When to use

- Finding a known regulatory element in a sequence (TATA box, Kozak, poly-A).
- Scanning a promoter for a transcription factor binding site.
- Confirming an enzyme recognition site in a designed construct.
- Searching for a protein motif (PROSITE, Pfam) with a regex.

## When NOT to use

- De novo motif discovery from ChIP-seq → use `MEME` / `STREME`.
- Genome-wide PWM scan → use `MOODS`, `FIMO`, or `pyMOODS`.
- Protein domain detection → use `pyhmmer` or `InterProScan`.

## Prerequisites

- `biopython>=1.83`
- For advanced regex: `regex` package (supports fuzzy matching, IUPAC natively).
- For JASPAR motifs: `pyjaspar` (modern replacement for Biopython's JASPAR module).
- For genome-wide scans: `MOODS` (C++) or `FIMO` (MEME Suite).

## Core workflow

1. **Decide the motif type**: literal, IUPAC, or PWM.
2. **For literal/IUPAC**: regex is fastest.
3. **For PWM**: convert to a log-odds matrix, scan with a sliding window.
4. **Validate hits biologically** (one perfect match in a 10 kb promoter is suspicious; a 7/8 match with a known co-factor is meaningful).

## Code patterns

### Literal motif (regex)

```python
import re
from Bio import SeqIO

seq = str(next(SeqIO.parse("promoter.fasta", "fasta")).seq)
for m in re.finditer(r"TATAAA", seq):
    print(f"TATA box at {m.start()}")
```

### IUPAC consensus

IUPAC codes are valid regex characters *except* a few that collide with regex syntax (`*`, `?`, `(`, `)`). Use Biopython's IUPAC-to-regex helper:

```python
from Bio.Data.IUPACData import ambiguous_dna_values

def iupac_to_regex(motif: str) -> str:
    """Convert IUPAC DNA to a regex character class."""
    return "".join(f"[{ambiguous_dna_values[c]}]" for c in motif.upper())

pat = re.compile(iupac_to_regex("RRRYYCC"))  # poly-A signal
for m in pat.finditer(seq):
    print(m.start(), m.group())
```

### Reverse-strand search

Many regulatory motifs are on the antisense strand:

```python
def find_on_both_strands(seq: str, motif_regex):
    rc = str(Seq(seq).reverse_complement())
    for strand, s in (("+", seq), ("-", rc)):
        for m in motif_regex.finditer(s):
            print(f"{strand}\t{m.start()}\t{m.group()}")
```

### PROSITE-style protein motif

```python
psp = re.compile(r"G.{1,2}GV[AGST]G[AGILV]KT")  # P-loop NTP-binding
for m in psp.finditer(str(protein.seq)):
    print(m.start(), m.group())
```

### Fuzzy matching (sequencing errors)

`regex` package supports approximate matching with `e<=N` for up to N edits:

```python
import regex
for m in regex.finditer(r"(TATAAA){e<=1}", seq):
    print(m.start(), m.group(), m.fuzzy_counts)
```

### Position Weight Matrix (PWM) from a JASPAR-style count matrix

```python
import numpy as np
from Bio import motifs

counts = motifs.CountsMatrix(
    [
        [10,  3,  1,  2],   # A
        [ 2,  8,  1,  3],   # C
        [ 1,  2,  9,  2],   # G
        [ 1,  2,  3,  7],   # T
    ],
    alphabet="ACGT",
)
pwm = counts.normalize(pseudocounts=0.5)
pssm = pwm.log_odds()    # log2 odds vs uniform
```

### Scan a sequence with a PSSM

```python
threshold = 5.0
for pos, score in pssm.search(seq, threshold=threshold, both=True):
    print(f"hit at {pos}, score={score:.2f}")
```

### Load a JASPAR motif (modern, 2026)

```python
import pyjaspar

# pyjaspar 2.x supports JASPAR 2024 releases
motif = pyjaspar.get_motif_by_id("MA0006.1")  # Arnt
pwm = motif.profile_matrix   # 4 x len
```

### Reverse-complement-aware PWM scan (TF binding is double-stranded)

```python
# Biopython's `search(both=True)` already does this
hits = list(pssm.search(seq, threshold=6.0, both=True))
```

### Find all occurrences of restriction sites

```python
from Bio.Restriction import EcoRI, BamHI, HindIII

sites = []
for enz in (EcoRI, BamHI, HindIII):
    for hit in enz.search(seq):
        sites.append((hit, enz))
```

## Common pitfalls

- **IUPAC in regex breaks silently.** `[ACGT]` works, but `R` alone is just a literal `R`. Always use the Biopython IUPAC-to-regex helper.
- **PWM scan without background correction** gives wrong scores. Always use log-odds (PWM), not raw frequencies.
- **JASPAR 2024 release restructured motif IDs** — old `MA0006.1` may be `MA0006.2`. `pyjaspar` handles aliases.
- **TATA box at position 0 is a false positive.** It's probably the start of a sequence header; offset by 50+ bp from a TSS.
- **Single PWM hit ≠ functional binding site.** Combine with chromatin accessibility (ATAC-seq), conservation (phastCons), and co-factor motifs for credible predictions.

## Validation

- For known motifs, the hit count is in the expected ballpark (e.g., a TATA box should appear in ~30-50% of vertebrate Pol II promoters, not 100%).
- For a PSSM, scan a known positive sequence first to confirm the threshold.
- Forward- and reverse-strand hits should be roughly equal in a random sequence (motif symmetry test).

## Open alternatives

| Need | Tool |
|------|------|
| Genome-wide PWM scan | `FIMO` (MEME Suite), `MOODS` |
| JASPAR motif access | `pyjaspar`, JASPAR REST API |
| De novo motif discovery | `MEME`, `STREME` |
| ChIP-seq peaks → motifs | `HOMER`, `MEME-ChIP` |
| Restriction enzyme mapping | `Bio.Restriction`, `REmatch` |

## References

- Biopython `Bio.motifs`: <https://biopython.org/docs/latest/api/Bio.motifs.html>
- JASPAR 2024: <https://jaspar.genereg.net/>
- MEME Suite: <https://meme-suite.org/meme/>
- pyjaspar: <https://github.com/asntech/pyjaspar>
- Companion: `ors-bioinformatics-sequence-seq-objects`, `ors-bioinformatics-functional-motif-*` skills.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-motif-search` (bioSkills-main/sequence-manipulation/motif-search).