---

name: transcription-translation
description: "Transcribe DNA to RNA (and back), translate coding sequences to protein using NCBI codon tables, and pick the right genetic code for mitochondria, plastids, or non-standard organisms."
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

# Transcription and Translation
"
> Transcribe is "T → U". Translate is "3 bases → 1 amino acid". The whole
> problem is picking the right codon table — there are 27 NCBI genetic
> codes, and picking the wrong one for a mitochondrial gene silently
> produces a wrong protein. This skill is the canonical patterns, the
> `cds=True` strictness check, and the codon-table index.

## When to use

- mRNA from a coding sequence.
- Protein sequence from a CDS (or whole genome, for prokaryotes).
- Reverse transcription (mRNA → cDNA, U → T).
- Verifying that a predicted ORF really is a CDS (no internal stops, correct frame).

## When NOT to use

- Gene finding (de novo ORF detection) → use `pyrodigal`, `prodigal`, or `MetaGeneAnnotator`.
- Genome annotation → use `bakta` or `prokka`.
- For translation with frameshifts / selenocysteine → custom logic with NCBITSite.

## Prerequisites

- `biopython>=1.83`

## Core workflow

1. **Pick the codon table** — NCBI table 1 is the standard genetic code.
2. **Get the CDS** — either a feature from GenBank, or your own extracted ORF.
3. **Translate** with `cds=True` if you want validation; `cds=False` for "translate whatever".
4. **Verify** — length divisible by 3, no internal stops (or stops are expected for selenocysteine / pyrrolysine).

## NCBI codon tables (most common, 2026)

| ID | Name | Use |
|----|------|-----|
| 1 | Standard | Most organisms |
| 2 | Vertebrate Mitochondrial | Human mtDNA, mouse mtDNA |
| 3 | Yeast Mitochondrial | S. cerevisiae mtDNA |
| 4 | Mold / Protozoan / Coelenterate Mitochondrial | Invertebrate mtDNA |
| 5 | Invertebrate Mitochondrial | Many invertebrate mtDNAs |
| 6 | Ciliate Nuclear | Tetrahymena, Paramecium |
| 11 | Bacterial, Archaeal and Plant Plastid | Chloroplasts, bacteria |

Full list: <https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi>

## Code patterns

### Basic transcription and translation

```python
from Bio.Seq import Seq

coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
mrna = coding_dna.transcribe()              # T → U
protein = coding_dna.translate()            # MAIVMGR*
```

### Strict CDS validation (cds=True)

```python
protein = coding_dna.translate(cds=True)
```

This raises `Bio.Data.CodonTable.TranslationError` if:
- Length is not a multiple of 3.
- The CDS doesn't start with ATG.
- The CDS doesn't end with a stop codon (TAA, TAG, TGA).

For mitochondrial code (table 2), stop codons are different (AGA, AGG, TAA, etc.):

```python
protein = coding_dna.translate(table=2, cds=True)
```

### Reverse transcription (mRNA → cDNA)

```python
mrna = Seq("AUGGCCAUUGUAA")
cdna = mrna.back_transcribe()    # U → T
```

### Translate a non-standard genetic code

```python
# Vertebrate mitochondrial
protein = coding_dna.translate(table=2)

# Yeast mitochondrial
protein = coding_dna.translate(table=3)
```

### Translate to stop (drop the trailing stop)

```python
protein = coding_dna.translate(to_stop=True)  # MAIVMGR
```

### Translate with full table object

```python
from Bio.Data import CodonTable

std = CodonTable.unambiguous_dna_by_id[1]      # standard
mt = CodonTable.unambiguous_dna_by_id[2]       # vertebrate mt

print(std.stop_codons)   # ['TAA', 'TAG', 'TGA']
print(mt.stop_codons)    # ['TAA', 'TAG', 'AGA', 'AGG']
print(std.start_codons)  # ['TTG', 'CTG', 'ATG'] (alt starts in bacteria)
```

### Extract CDS from GenBank and translate

```python
from Bio import SeqIO

rec = next(SeqIO.parse("chr1.gb", "genbank"))
for feat in rec.features:
    if feat.type == "CDS":
        nt = feat.extract(rec.seq)
        protein = nt.translate(cds=True)   # raises if feature is malformed
        print(feat.qualifiers.get("gene", ["?"])[0], protein[:30])
```

### Six-frame translation (for ORF finding)

```python
def six_frames(seq: str, table: int = 1) -> list[str]:
    from Bio.Seq import Seq
    s = Seq(seq)
    rc = s.reverse_complement()
    return [str(s[i:].translate(table=table)) for i in range(3)] + \
           [str(rc[i:].translate(table=table)) for i in range(3)]
```

### Validate a predicted ORF

```python
def validate_cds(seq: str, table: int = 1) -> bool:
    from Bio.Seq import Seq
    s = Seq(seq)
    if len(s) % 3 != 0:
        return False
    if not s.upper().startswith("ATG"):
        return False
    try:
        s.translate(table=table, cds=True)
        return True
    except Exception:
        return False
```

## Common pitfalls

- **Translating raw genomic DNA.** Eukaryotic genes have introns. Use the CDS feature, not the whole gene.
- **Wrong codon table for mitochondria.** In vertebrate mtDNA, AGA and AGG are stops, not Arg. In standard code, they code for Arg.
- **`cds=True` is strict.** A genuine prokaryotic CDS that uses GTG as a start will fail. Use `cds=False` if you allow alternative starts.
- **Frame confusion.** A 900 bp CDS is 300 aa. If you get 297 or 303, your frame is off by 1.
- **Forgetting `to_stop=True`** leaves the stop codon as `*` in the protein. Decide whether you want it.

## Validation

- Length of protein ≈ length of CDS / 3.
- First amino acid is `M` (or fM in mitochondria).
- Last character is `*` if you didn't use `to_stop=True`.
- For a real CDS, no internal `*`.

## Open alternatives

| Need | Tool |
|------|------|
| Gene finding (prokaryotic) | `pyrodigal`, `prodigal` |
| Genome annotation | `bakta`, `prokka` |
| Codon usage bias | `Bio.SeqUtils.CodonUsage` (see codon-usage skill) |
| Six-frame ORF display | `EMBOSS getorf`, `ORFfinder` |

## References

- Biopython translation: <https://biopython.org/docs/latest/api/Bio.Seq.html#Bio.Seq.Seq.translate>
- NCBI genetic codes: <https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi>
- Companion: `ors-bioinformatics-sequence-codon-usage`, `ors-bioinformatics-sequence-sequence-properties`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-transcription-translation` (bioSkills-main/sequence-manipulation/transcription-translation).