---
name: ors-open-science-fair-data
display_name: "FAIR Data Principles"
description: Use when designing a data management plan, choosing a repository, structuring metadata, or making research data Findable, Accessible, Interoperable, and Reusable per Wilkinson et al. 2016.
version: 1.0.0
author: Pradyumna Jayaram
maintained_by: Pradyumna Jayaram
license: MIT
category: open-science
tags: [fair, data-management, metadata, repositories, reproducibility, open-data]
difficulty: intermediate
prerequisites:
  tools: [git, zenodo-cli OR web-browser, schema.org OR DATS validator, orcid]
  skills: []
sources_consulted:
  - "Original: Wilkinson et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data 3:160018."
  - "Original: GO-FAIR initiative (https://www.go-fair.org/fair-principles/)."
  - "Original: FAIRsharing registry (https://fairsharing.org/)."
  - "Original: Creative Commons CC-BY 4.0 license (https://creativecommons.org/licenses/by/4.0/)."
  - "Original: NIH Genomic Data Sharing Policy 2014 + 2023 update."
  - "Original: ELIXIR FAIR Cookbook (https://elixir-europe.org/services/fair-cookbook)."
  - "Improvisions: Pradyumna Jayaram — domain-specific metadata checklist (MIAME/MINSEQE/MIAPE/MIxS/REMBI), repository selection decision tree, and FAIRness self-assessment rubric."
last_updated: 2026-06-10
---

# FAIR Data Principles

> The FAIR principles — Findable, Accessible, Interoperable, Reusable — are a 15-point framework for making research data usable by humans and machines. Originally published by Wilkinson et al. in 2016 (Sci Data 3:160018), FAIR is now the de-facto policy language for funders (NIH, ERC, Wellcome, Horizon Europe), journals (Nature, PLOS, Science), and institutional data-management plans. This skill provides a decision tree for choosing a metadata standard, a repository, and a license, plus a self-assessment rubric to grade any dataset.

## When to use

- Drafting a **Data Management Plan (DMP)** for NIH, NSF, ERC, Wellcome, or Horizon Europe.
- Choosing a **domain repository** (GEO, SRA, ENA, PRIDE, MetaboLights, BioImage Archive, EMDB, PDB, GenBank) versus a generalist one (Zenodo, Figshare, Dryad).
- Writing a **metadata file** for a sequencing, proteomics, metabolomics, imaging, or structural dataset.
- Preparing a **data availability statement** for a manuscript.
- Auditing an existing dataset against the 15 FAIR sub-principles (F1–F4, A1–A2, I1–I3, R1–R1.3).
- Responding to reviewers who say "data not available" or "metadata insufficient."

## When NOT to use

- For **code release** (not data) — see `ors-open-science-code-release`.
- For **licensing decisions** specifically — see `ors-open-science-licensing`.
- For **privacy/HIPAA/GDPR** of human-subject data — see `ors-ethics-compliance-` (separate skill).
- For data that is genuinely **embargoed, classified, or commercially sensitive** — FAIR is aspirational; restrictions change F/A.

## Prerequisites

- ORCID iD for the data author (https://orcid.org/).
- Familiarity with the data type (sequencing reads, mass spec peaks, microscope images, etc.).
- A decision on license: CC0 or CC-BY-4.0 are the FAIR defaults; see `ors-open-science-licensing`.
- Repository account (Zenodo, ENA, PRIDE, etc.).

## Core workflow

1. **Identify data type and minimum information standard.** Match the assay to the MIxS-style checklist (see "Document patterns" below).
2. **Choose domain repository first, generalist second.** Use a community-curated repository if one exists; fall back to Zenodo/Figshare for non-standard outputs (figures, code, supplementary files).
3. **Reserve a persistent identifier (PID).** Obtain a DOI from the repository at submission time. PIDs make the data findable AND citable.
4. **Write machine-readable metadata.** Use the repository's required schema (e.g., MINSEQE for RNA-seq, MIAPE for proteomics, REMBI for bioimaging, SDRF for proteomics).
5. **Apply an open license.** CC0 or CC-BY-4.0 for data; CC-BY-4.0 preferred when attribution is desired.
6. **Use a standard access protocol.** HTTPS download is acceptable; controlled-access human data uses dbGaP/EGA with a Data Access Committee.
7. **Link data to publication and code.** Include the dataset DOI in the paper, and the paper DOI in the dataset record (bidirectional citation).
8. **Self-assess with the FAIR rubric** in the "Validation" section.

## Document patterns

### Pattern 1: The 15 FAIR sub-principles (Wilkinson 2016)

| Group | ID | Sub-principle |
|-------|----|--------------|
| **Findable** | F1 | (Meta)data are assigned a globally unique and persistent identifier. |
| | F2 | Data are described with rich metadata. |
| | F3 | Metadata clearly and explicitly include the identifier of the data they describe. |
| | F4 | (Meta)data are registered or indexed in a searchable resource. |
| **Accessible** | A1 | (Meta)data are retrievable by their identifier using a standardised communications protocol. |
| | A1.1 | The protocol is open, free, and universally implementable. |
| | A1.2 | The protocol allows for an authentication and authorisation procedure where necessary. |
| | A2 | Metadata are accessible, even when the data are no longer available. |
| **Interoperable** | I1 | (Meta)data use a formal, accessible, shared, and broadly applicable language for knowledge representation. |
| | I2 | (Meta)data use vocabularies that follow FAIR principles. |
| | I3 | (Meta)data include qualified references to other (meta)data. |
| **Reusable** | R1 | (Meta)data are richly described with a plurality of accurate and relevant attributes. |
| | R1.1 | (Meta)data are released with a clear and accessible data usage license. |
| | R1.2 | (Meta)data are associated with detailed provenance. |
| | R1.3 | (Meta)data meet domain-relevant community standards. |

### Pattern 2: Domain-specific minimum-information standards

| Assay / data type | Standard | Notes |
|-------------------|----------|-------|
| Microarray expression | **MIAME** | Minimum Information About a Microarray Experiment (FGED). |
| RNA-seq | **MINSEQE** | Minimum Information about a Sequencing Experiment. |
| Proteomics (MS) | **MIAPE-MS** | Minimum Information About a Proteomics Experiment. |
| Proteomics (gel/in-gel) | **MIAPE-GE** | |
| Glycomics | **MIRAGE** | |
| Metabolomics (MS) | **MIAPE-MS** + **MetaboLights** mandatory | |
| Metabolomics (NMR) | **MIAPE-NMR** | |
| Genomics/metagenomics | **MIxS** (GSC) | GSC: Genomic Standards Consortium. |
| Bioimaging | **REMBI** (2021) | Recommended Metadata for Biological Images. |
| Light microscopy | **OME-XML / OME-TIFF** | Open Microscopy Environment. |
| Flow cytometry | **MIFlowCyt** (FCS) | |
| Stem cells | **MISFISHIE** | |
| Sample metadata (any -omics) | **SDRF-Proteomics**, **ENA sample checklist**, **ENA library** | Sample-Data-Relationship File. |
| Computational models | **MIASE / SED-ML / COMBINE** | |
| 3D structures | **PDBx/mmCIF** | |
| Crystallography | **mmCIF + structure factors** | Deposited in PDB. |
| NMR structures | **BMRB** | |
| Cryo-EM | **EMDB + PDB** | Map + model; both required for full deposit. |
| Genomic sequence | **GenBank/EMBL/DDBJ flatfile** | INSDC coordinated. |

### Pattern 3: Repository selection decision tree

```
Is there a community-curated domain repository for this data type?
├── YES → use it (GEO/SRA/ENA for seq, PRIDE for MS-proteomics,
│         MetaboLights for metabolomics, BioImage Archive for images,
│         EMDB+PDB for structures, GenBank for annotated sequences)
│         • Domain repos enforce metadata standards (R1.3)
│         • Domain repos mint DOIs
│         • Domain repos are indexed in EBI/NCBI portals (F4)
└── NO  → use a generalist repository:
          • Zenodo (CERN-hosted, 50 GB per record, GitHub integration)
          • Figshare (DPI, 5 GB free, 20 GB institutional)
          • Dryad (data-only, curation fee, 300 GB)
          • Dataverse (institutional option)
          → Generalist repos still mint DOIs; you supply metadata.
```

### Pattern 4: A minimal FAIR data availability statement (for a manuscript)

> "Raw RNA-seq reads (fastq) are deposited at the NCBI Sequence Read Archive under BioProject accession PRJNA123456 (reviewer link: https://dataview.ncbi.nlm.nih.gov/...). Processed count matrices, sample metadata, and differential expression tables are deposited at Zenodo (DOI: 10.5281/zenodo.1234567). Analysis code and the Snakemake workflow are archived at Zenodo (DOI: 10.5281/zenodo.7654321). All data are released under CC-BY-4.0; code under MIT."

## Common pitfalls

| Pitfall | Why it fails | Fix |
|---------|-------------|-----|
| **Data on a personal/lab website** | No PID, no metadata, no long-term preservation (A1, A2) | Deposit in Zenodo/Figshare to mint a DOI. |
| **Data in a journal supplement** | Journal supplements disappear with the journal subscription; not a PID (F1, A2) | Deposit independently; link via DOI in the data-availability statement. |
| **Metadata in a free-text README** | Not machine-readable (I1, I2) | Use the repository's controlled vocabulary (e.g., SDRF-Proteomics, ENA sample checklist). |
| **License missing** | Fails R1.1; cannot be reused legally | Apply CC0 (data) or CC-BY-4.0 (data) at deposit time. |
| **Controlled vocabulary bypassed** (e.g., free-text "liver" instead of UBERON:0002107) | I2 fails; not interoperable | Use ontology IDs: UBERON (anatomy), ChEBI (chemicals), NCBI Taxonomy (organisms), EFO (experimental factors). |
| **Human data on an open server** | Legal/ethical breach (HIPAA, GDPR) | Use controlled access: dbGaP (US) or EGA (EU). |
| **"Available upon reasonable request"** | Wilkinson 2016 and most funder mandates (NIH 2023, Horizon Europe) treat this as **non-compliance** | Actually deposit; or, if a Data Access Committee is genuinely required, state the DAC and the access procedure explicitly. |
| **No link from paper to data** | F3 fails; metadata doesn't reference the data | Include the DOI in the data-availability statement. |
| **No link from data to paper** | I3 fails; data don't reference the paper | Update the Zenodo record with the published DOI after publication. |
| **Metadata describes file format, not content** | "Fastq.gz, 12 GB" is not R1 | Describe sample, organism, assay, library prep, instrument, read length, depth. |
| **Reusing data without citation** | Open data still needs attribution (CC-BY) | Cite by DOI; provide a `CITATION.cff` or `CREDITS` file. |

## Validation

A quick FAIR self-assessment. Score 1 point per satisfied sub-principle (max 15). Most journals expect ≥ 12/15 for a "data paper."

**Findable (max 4)**
- [ ] F1: DOI or accession ID assigned?
- [ ] F2: Metadata file is human-readable, ideally > 20 fields?
- [ ] F3: Metadata explicitly includes the data DOI/accession?
- [ ] F4: Indexed in a searchable resource (Google Dataset Search, FAIRsharing, re3data)?

**Accessible (max 4)**
- [ ] A1: Retrievable by identifier over HTTPS?
- [ ] A1.1: Protocol open, free, universal?
- [ ] A1.2: Access protocol supports auth where required (e.g., dbGaP/EGA)?
- [ ] A2: Metadata persists even if data is withdrawn?

**Interoperable (max 3)**
- [ ] I1: Format is open and broadly supported (e.g., fastq.gz, mzML, OME-TIFF)?
- [ ] I2: Vocabularies are shared/FAIR (ontologies, not free text)?
- [ ] I3: Qualified cross-references to other datasets/publications?

**Reusable (max 4)**
- [ ] R1: Rich attributes (sample, instrument, protocol, software versions)?
- [ ] R1.1: License declared (CC0, CC-BY-4.0)?
- [ ] R1.2: Provenance captured (workflow, parameters, versions)?
- [ ] R1.3: Meets community standard (MIAME/MINSEQE/MIAPE/MIxS/REMBI/etc.)?

**Total: ____ / 15**

## Open alternatives

| Commercial / restricted tool | Open alternative | Trade-off |
|------------------------------|------------------|-----------|
| Geneious (Biomatters) | Benchling (cloud) or pure CLI (BWA + samtools + IGV desktop) | Benchling is open for academics; Geneious is closed-source. |
| PRIDE Inspector (proprietary build) | OpenMS TOPPView, pyOpenMS | All open source; UI differs. |
| Web-based METADATA editors (e.g., Genedata Expressionist) | ENA Webin, BioSample submission, SDRF-Proteomics text editor | ENA is free; manual but standards-compliant. |
| Cloud-locked data (AWS-only, Google-only) | Zenodo, EBI, NCBI, S3 with a DOI in FAIRsharing | Use cloud only for embargoed data; public data should be domain-repository first. |

## References

- Wilkinson, M. D. et al.. **The FAIR Guiding Principles for scientific data management and stewardship.** *Scientific Data* 3, 160018. doi:10.1038/sdata.2016.18.
- GO-FAIR — FAIR principles official site: https://www.go-fair.org/fair-principles/
- FAIRsharing (registry of standards, databases, policies): https://fairsharing.org/
- re3data (Registry of Research Data Repositories): https://www.re3data.org/
- ELIXIR FAIR Cookbook: https://elixir-europe.org/services/fair-cookbook
- FORCE11 FAIR Principles: https://force11.org/info/the-fair-data-principles/
- Creative Commons license chooser: https://creativecommons.org/choose/
- NIH Genomic Data Sharing Policy: https://sharing.nih.gov/genomic-data-sharing-policy
- Genomic Standards Consortium (MIxS checklists): https://gensc.org/mixs/
- EBI MetaboLights: https://www.ebi.ac.uk/metabolights/
- EBI PRIDE (proteomics): https://www.ebi.ac.uk/pride/
- NCBI GEO / SRA: https://www.ncbi.nlm.nih.gov/geo/ and https://www.ncbi.nlm.nih.gov/sra
- ENA (European Nucleotide Archive): https://www.ebi.ac.uk/ena
- BioImage Archive: https://www.ebi.ac.uk/bioimage-archive/
- EMDB / PDB: https://www.ebi.ac.uk/emdb/ and https://www.rcsb.org/
- Zenodo: https://zenodo.org/
- FAIR Data Maturity Model (Research Data Alliance): https://www.rd-alliance.org/

## Related skills

- `ors-open-science-licensing` — picking CC0 / CC-BY / CC-BY-SA for the dataset.
- `ors-open-science-code-release` — releasing the code that produced the data.
- `ors-open-science-preprints` — pairing a data deposit with a preprint for early citation.
- `ors-data-engineering-dvc-data-version-control` — DVC for large file versioning.

## Changelog

- 1.0.0 (2026-06-10): Initial adaptation by Pradyumna Jayaram. Synthesised Wilkinson et al. 2016 (the canonical source); GO-FAIR; FAIRsharing; ELIXIR FAIR Cookbook; domain standards (MIAME, MINSEQE, MIAPE, MIRAGE, MIxS, REMBI, MIASE); major repositories (ENA, GEO/SRA, PRIDE, MetaboLights, BioImage Archive, EMDB, PDB, GenBank, Zenodo). Decision tree, 15-sub-principle table, and self-assessment rubric are original compositions.
