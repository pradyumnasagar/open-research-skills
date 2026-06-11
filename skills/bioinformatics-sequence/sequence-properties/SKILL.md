---

name: sequence-properties
description: "Compute GC content, molecular weight, melting temperature, isoelectric point, and instability index for DNA, RNA, and protein sequences."
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

# Sequence Properties

> Six numbers tell you almost everything about a sequence: length, GC
> fraction, molecular weight, melting temperature (DNA), isoelectric point
> (protein), instability index (protein). This skill is the canonical
> computation, the formula citations, and the 2026 modern-API reality in
> `Bio.SeqUtils` 1.83+.

## When to use

- Pre-alignment sanity checks (a sequence with 90% Ns is not real).
- Primer/probe design: Tm, GC, hairpin, dimer.
- Protein characterization: MW, pI, instability, aromaticity, GRAVY.
- Genome composition: GC content by window, by chromosome, by gene.

## When NOT to use

- Production primer design → use `primer3-py` (handles salt, oligo concentration, mismatches).
- Genome-wide GC → use `bedtools nuc` or `computeGCBias` (deepTools).
- Protein domain detection → use InterProScan or `pyhmmer`.

## Prerequisites

- `biopython>=1.83`
- For protein: `Bio.SeqUtils.ProtParam`
- For DNA/RNA: `Bio.SeqUtils` (nt utilities)

## Core workflow

1. **Identify the molecule type** (DNA, RNA, protein).
2. **Pick the right utility module** — `ProtParam` is for protein, the rest of `Bio.SeqUtils` for DNA/RNA.
3. **Compute the canonical properties** for that type.
4. **Cite the formula** in your methods section.

## Code patterns

### DNA / RNA: GC, MW, Tm

```python
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction
from Bio.SeqUtils.MolecularWeight import MolecularWeight
"
s = Seq("ATGCATGCATGCATGCATGC")
print(f"length: {len(s)}")
print(f"GC: {gc_fraction(s):.3f}")  # 0.5

mw_double = MolecularWeight(s)         # double-stranded MW
print(f"ds MW: {mw_double:.1f} Da")
```

### DNA Tm (Wallace rule for short oligos)

For very short oligos (<14 nt), Tm is roughly `2 * (A+T) + 4 * (G+C)`:

```python
def tm_wallace(seq: str) -> float:
    s = seq.upper()
    return 2 * (s.count("A") + s.count("T")) + 4 * (s.count("G") + s.count("C"))
```

### DNA Tm (Marmur / nearest-neighbor for longer oligos)

Use `primer3-py` for production work — see the primer-design reference. The
nearest-neighbor model (SantaLucia 1998) is the 2026 standard.

```python
# In production: primer3-py
import primer3
tm = primer3.calc_tm("ATGCATGCATGCATGC")
```

### Protein: MW, pI, instability, aromaticity, GRAVY

```python
from Bio.Seq import Seq
from Bio.SeqUtils.ProtParam import ProteinAnalysis

pa = ProteinAnalysis(str(Seq("MGEKLPVRLNVMGYEEDILKQHKWLRNVQTLKDGIVFVD")))

print(f"length: {len(pa.sequence)}")
print(f"MW: {pa.molecular_weight():.1f} Da")
print(f"pI: {pa.isoelectric_point():.2f}")
print(f"instability_index: {pa.instability_index():.1f}")  # <40 stable
print(f"aromaticity: {pa.aromaticity():.3f}")
print(f"gravy: {pa.gravy():.3f}")  # Grand average of hydropathy
```

### Amino acid percent composition

```python
print(pa.get_amino_acids_percent())
# {'A': 0.07, 'C': 0.02, ...}
```

### Secondary structure fraction (Chou-Fasman)

```python
print(pa.secondary_structure_fraction())  # (helix, turn, sheet)
```

### GC content by sliding window

```python
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction

def gc_window(seq: Seq, window: int = 100, step: int = 50):
    s = str(seq)
    out = []
    for i in range(0, len(s) - window + 1, step):
        out.append((i, gc_fraction(Seq(s[i:i+window]))))
    return out
```

### CpG observed/expected

`CpG O/E = (CpG count) / (C count × G count / N)`. Used in vertebrate
methylation studies.

```python
def cpg_oe(s: str) -> float:
    s = s.upper()
    c = s.count("C")
    g = s.count("G")
    cg = s.count("CG")
    n = c + g
    if c == 0 or g == 0 or n == 0:
        return 0.0
    return cg * n / (c * g)
```

### DNA / RNA / protein ambiguity

`gc_fraction` excludes `N` automatically. If you need a denominator that
includes Ns, normalize manually:

```python
def gc_with_n(s: str) -> float:
    s = s.upper()
    denom = sum(1 for b in s if b in "ACGTNU")
    gc = sum(1 for b in s if b in "GC")
    return gc / denom if denom else 0.0
```

## Common pitfalls

- **`Bio.SeqUtils.GC` vs `gc_fraction`.** In 1.80+, the canonical function is `gc_fraction(seq)`. Older code uses `GC(seq)`. The new function returns a fraction; old returned a percentage.
- **Wallace Tm is wrong for oligos > 14 nt.** Use nearest-neighbor (SantaLucia 1998) for production.
- **Tm calculation is salt-, oligo-concentration-, and Mg2+-dependent.** A "Tm" without conditions is meaningless. `primer3-py` handles this.
- **Instability index is for *in vitro* stability** of a purified protein, not cellular half-life. Don't conflate.
- **GRAVY negative = hydrophilic, positive = hydrophobic.** The sign convention trips people up.

## Validation

- Length: `len(seq) == len(str(seq))`.
- GC: 0 ≤ GC ≤ 1.
- pI: amino acid distribution implies a pI; verify with the expected range for the protein class (e.g., basic proteins have pI > 7).
- MW: protein MW = sum of residue masses + 18 (water). `ProteinAnalysis` accounts for this.

## Open alternatives

| Need | Tool |
|------|------|
| Production primer Tm | `primer3-py` |
| Genome-wide GC | `bedtools nuc`, `deeptools computeGCBias` |
| Protein domain + pI + GO | InterProScan, UniProt |
| Codon usage | `Bio.SeqUtils.CodonUsage` (see codon-usage skill) |

## References

- Biopython ProtParam: <https://biopython.org/docs/latest/api/Bio.SeqUtils.ProtParam.html>
- SantaLucia 1998 nearest-neighbor Tm: <https://doi.org/10.1073/pnas.95.4.1460>
- ExPASy ProtParam: <https://web.expasy.org/protparam/>
- Companion: `ors-bioinformatics-sequence-codon-usage`, `ors-bioinformatics-sequence-reverse-complement`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-sequence-properties` (bioSkills-main/sequence-manipulation/sequence-properties).