---
name: seq-objects
description: "Master the Seq, MutableSeq, and SeqRecord objects — slicing, immutability,"
license: MIT
---



<!-- metadata:
category: bioinformatics-sequence
version: 1.0.0
author: Pradyumna Jayaram
tags:
- biopython
- seq
- seqrecord
- alphabets
- slicing
difficulty: beginner
prerequisites:
  tools:
  - python>=3.10
  - biopython>=1.83
  skills: []
sources: 'Original: bio-seq-objects (bioSkills-main/sequence-manipulation/seq-objects);
  Adapted: 2026 alphabet-IUPAC reality, MutableSeq patterns for in-place edits, SeqRecord
  feature handling.; Improvisions: added reverse-complement tie-in, parity with Bio.SeqUtils
  1.83+.'
-->

# Biopython Seq and SeqRecord Objects

> `Seq` is a string with a memory. It knows it's a biological sequence, so it
> understands complementarity, transcription, and translation. `SeqRecord`
> wraps `Seq` with an ID, a description, annotations, and a list of
> features. This skill is the 101 on both — and the alphabet deprecation
> story that has confused newcomers since Biopython 1.80.

## When to use

- Wrapping a plain Python string as a biological sequence.
- Slicing and indexing with biological semantics (`.complement()`, `.reverse_complement()`).
- Carrying per-record metadata: ID, description, annotations, features, dbxrefs.
- In-place edits via `MutableSeq`.

## When NOT to use

- Plain string manipulation — use Python str. `Seq` is for biology.
- Massive-scale sequence ops → use `pyfastx` or `parasail` for kernels.
- File-level work → see `ors-bioinformatics-sequence-read-write-sequences`.

## Prerequisites

- `biopython>=1.83`

## Core workflow

1. **Create a `Seq` from a string.**
2. **Index / slice** like a string.
3. **Wrap in a `SeqRecord`** for I/O, feature handling, and metadata.
4. **Mutate in place with `MutableSeq`** only when you really need it.
5. **Convert back to `str`** only at the file boundary or the Bio.* API edge.

## Code patterns

### Construct a Seq

```python
from Bio.Seq import Seq
"
s = Seq("ACGTACGT")
print(s.complement())         # TGCATGCA
print(s.reverse_complement()) # TACGTACG... actually ACGTACGT (palindrome in this case)
```

### The `IUPAC` ambiguity alphabet (2026 reality)

Since Biopython 1.80, **alphabet objects are deprecated**. The new API is the
`Bio.Seq` + `Bio.SeqUtils` functions, which assume IUPAC by default:

```python
from Bio.Seq import Seq

s = Seq("ACGTNRYWSKMBDHV")     # 15 IUPAC codes
print(s.complement())           # full IUPAC complement table
```

If you're on older code that imports `Bio.Alphabet`, you'll see deprecation
warnings. Migrate to:

```python
# Old
from Bio.Alphabet import IUPAC
s = Seq("ACGT", IUPAC.unambiguous_dna)

# New
s = Seq("ACGT")  # assumed unambiguous DNA
```

### MutableSeq — in-place editing

```python
from Bio.Seq import MutableSeq

m = MutableSeq("ACGTACGT")
m[3] = "N"
print(m)        # ACGNACGT
m.reverse()
print(m)        # TGCANGCA
```

Convert back to immutable with:

```python
s = m.toseq()
```

### SeqRecord with metadata

```python
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

rec = SeqRecord(
    Seq("ATGAAATAA"),
    id="seq1",
    name="seq1",
    description="example cDNA",
    annotations={"molecule_type": "mRNA", "organism": "Homo sapiens"},
    dbxrefs=["Project:PRJNA1"],
)
```

### Add features to a SeqRecord

```python
from Bio.SeqFeature import SeqFeature, FeatureLocation, BeforePosition, AfterPosition

cds = SeqFeature(
    location=FeatureLocation(0, 9, strand=1),
    type="CDS",
    qualifiers={"gene": ["ABC1"], "transl_table": [1]},
)
rec.features.append(cds)
```

### Slicing semantics

```python
s = Seq("ACGTACGT")
s[2:5]              # 'GTA'  (Seq, not str)
s[0:3:2]            # 'AG'   (step)
s[-3:]              # 'CGT'  (Seq, supports negative indexing)
```

### Concatenation

```python
Seq("ACGT") + Seq("AAAA")
# Seq('ACGTAAAA')

# Don't concat SeqRecord — use Biopython's `concat` carefully
```

### Complement vs reverse-complement — the 5'/3' mental model

```python
s = Seq("ATGC")
s.complement()            # TACG (still 5'→3' but antiparallel)
s.reverse_complement()    # GCAT (5'→3' of the opposite strand)
```

When in doubt about orientation, **always** use `reverse_complement()` to get
back to "5' to 3' on the opposite strand". The plain `.complement()` keeps
the original coordinate frame.

### Translate, transcribe

```python
coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")
coding_dna.transcribe()           # mRNA (U for T)
coding_dna.translate()            # MAIVMGR* — uses table 1
coding_dna.translate(table="Vertebrate Mitochondrial")
coding_dna.translate(to_stop=True) # 'MAIVMGR'
```

### Equality and hashing

`Seq` hashes to the same value as the underlying string. Two `Seq("ACGT")`
from different alphabets compare equal in 1.83+.

```python
Seq("ACGT") == "ACGT"   # True
hash(Seq("ACGT")) == hash("ACGT")  # True
```

## Common pitfalls

- **`Seq` is not a `str` in some methods.** Some stdlib functions (`"".join(...)`) will reject it. Cast with `str(s)` when in doubt.
- **Complement vs reverse-complement confusion.** Use `.reverse_complement()` for mRNA/cDNA work, not `.complement()`.
- **Translating genomic DNA directly.** Eukaryotic genes have introns — don't translate raw genomic DNA. Use `feature.extract(rec.seq).translate()` for CDS features.
- **MutableSeq leaks.** Convert back to `Seq` with `m.toseq()` before handing the object to a function that assumes immutability.
- **In-place edits to a record's `.seq` don't update features.** If you mutate the `Seq`, the feature coordinates may no longer match.

## Validation

- `len(rec.seq) == len(str(rec.seq))`.
- `record.seq == record.seq` round-trip identity.
- After `MutableSeq` → `Seq`, the new `Seq` is truly immutable (you can't assign `s[0] = "A"`).

## Open alternatives

| Need | Tool |
|------|------|
| Pure-Python DNA ops | `primer3-py.calc_hairpin`, custom code |
| Fast string ops | `pyfastx.Fasta` (C-accelerated) |
| RNA secondary structure | `ViennaRNA` (`python-RNA` bindings) |
| Protein sequences | `Bio.Seq` + `Bio.SeqUtils.ProtParam` |

## References

- Biopython `Seq` tutorial: <https://biopython.org/docs/latest/Tutorial.html#chapter3>
- IUPAC codes: <https://www.bioinformatics.org/sms/iupac.html>
- Companion: `ors-bioinformatics-sequence-reverse-complement`, `ors-bioinformatics-sequence-transcription-translation`.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram from `bio-seq-objects` (bioSkills-main/sequence-manipulation/seq-objects).