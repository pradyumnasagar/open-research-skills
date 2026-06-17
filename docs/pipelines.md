# ORS Pipelines

A **pipeline** is a sequence of ORS skills that produce a complete research
artifact (manuscript section, dataset, figure, preprint) from raw inputs.
This document is the entry point for users who want to do something with
ORS but don't yet know which skills to load.

## How pipelines work

A pipeline is **not** a skill itself. It is a recipe: a numbered list of
skill loads with the handoffs between them. The skills you load are
real, individual SKILL.md files. The pipeline just tells you in what order.

When a skill in the pipeline produces an output for the next skill, it
should write a **Material Passport** (`*.passport.json`) in the same
directory. The next skill reads the passport and resumes work without
re-deriving context.

## Reference pipelines

The following pipelines cover the most common academic workflows. Each
one is a complete, runnable recipe.

### 1. RNA-seq: FASTQ → counts → DE → figure → manuscript

A canonical 6-stage analysis.

| # | Skill | Input | Output |
|---|---|---|---|
| 1 | `bioinformatics-sequence/fastp-quality-control` | raw FASTQ | trimmed FASTQ + QC report |
| 2 | `bioinformatics-sequence/star-alignment` | trimmed FASTQ + reference FASTA | aligned BAM |
| 3 | `bioinformatics-sequence/samtools-bam-processing` | BAM | sorted/indexed BAM + flagstat |
| 4 | `bioinformatics-sequence/featurecounts-quantification` | sorted BAM + GTF | raw count matrix |
| 5 | `statistics/deseq2-differential-expression` | count matrix + metadata | DE table + volcano/MA plots |
| 6 | `scientific-visualization/figure-design` | DE table + plots | publication-quality figure |
| 7 | `scientific-writing/manuscript-structure` | figure + methods notes | manuscript draft section |

Each skill writes a passport; downstream skills load their input and the
upstream passport. The passport chain at the end of the pipeline looks
like:

```
featurecounts.passport.json → deseq2.passport.json → figure.passport.json → manuscript.passport.json
```

### 2. Systematic review: search → screen → extract → synthesize

PRISMA 2020 compliant.

| # | Skill | Input | Output |
|---|---|---|---|
| 1 | `literature-research/pubmed-search` | research question | PubMed query + initial hits |
| 2 | `literature-research/scopus-search` | research question | Scopus query + initial hits |
| 3 | `literature-research/deduplicate-and-screen` | combined hits + inclusion criteria | PRISMA flow diagram |
| 4 | `literature-research/full-text-extraction` | screened papers | extraction spreadsheet |
| 5 | `literature-research/synthesis-and-grade` | extracted data | GRADE evidence table |
| 6 | `scientific-writing/systematic-review-section` | synthesis table | manuscript section |
| 7 | `peer-review/prisma-2020-checklist` | complete pipeline | PRISMA 2020 compliance audit |

### 3. Compound screening: SMILES → ADMET → docking → hit list

For chemoinformatics / drug discovery.

| # | Skill | Input | Output |
|---|---|---|---|
| 1 | `chemoinformatics/rdkit-descriptors` | SMILES list | molecular descriptors (CSV) |
| 2 | `chemoinformatics/admet-prediction` | descriptors | ADMET profile (CSV) |
| 3 | `chemoinformatics/vina-docking` | top compounds + receptor PDB | docking scores |
| 4 | `chemoinformatics/hit-prioritization` | docking + ADMET | ranked hit list |
| 5 | `scientific-writing/figure-design` | ranked hits + structures | compound figure |
| 6 | `scientific-writing/cover-letter` | manuscript context | cover letter |

### 4. Microscopy: images → segmentation → quantification → figure

For cell biology / high-content screening.

| # | Skill | Input | Output |
|---|---|---|---|
| 1 | `image-analysis-microscopy/cellprofiler-pipeline` | raw images + segmentation model | per-cell measurements |
| 2 | `image-analysis-microscopy/qupath-annotations` | H&E or IHC images | annotation overlays |
| 3 | `statistics/dunnett-post-hoc` | per-cell measurements | statistical comparisons |
| 4 | `scientific-visualization/figure-design` | measurements + stats | figure with error bars |
| 5 | `scientific-writing/results-section` | figure + stats | results paragraph |

### 5. Grant: idea → aims → approach → budget → full proposal

NIH R01 / NSF Standard / ERC AdG style.

| # | Skill | Input | Output |
|---|---|---|---|
| 1 | `scientific-thinking/hypothesis-generation` | research area + literature | 3-5 hypotheses |
| 2 | `research-grants/specific-aims` | chosen hypothesis | 3-page specific aims |
| 3 | `research-grants/approach-section` | aims + preliminary data | approach (significance + innovation + approach) |
| 4 | `research-grants/budget-justification` | approach + personnel | budget + justification |
| 5 | `research-grants/nsf-or-nih-format-check` | full proposal | compliance audit |

## How to add a pipeline

1. Run the pipeline once end-to-end yourself, recording every skill load.
2. Write the pipeline as a markdown table (the form above) in `docs/pipelines.md`.
3. For each step, document:
   - The exact skill slug (path relative to `skills/` or `meta/`).
   - The input the skill needs.
   - The output the skill produces (and whether it writes a passport).
   - A one-line note about what could go wrong at this step.
4. Submit a PR. Include the link to the showcase run in the PR description.

## When to write a new pipeline doc vs. inline

| Case | Where |
|---|---|
| The recipe is used by > 5 different labs | `docs/pipelines.md` |
| The recipe is project-specific | Project's own README |
| The recipe is a single-skill use | The skill's own SKILL.md |

## Cross-references

- `spec/material-passport.md` — the envelope every handoff writes.
- `meta/agent-handoff/SKILL.md` — the agent-facing handoff discipline.
- `examples/` — runnable passport examples for each pipeline stage.
