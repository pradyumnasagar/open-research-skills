---
name: thesis-methods-reproducibility
description: "Use when writing or checking the Methods, figures, data, and code of a bioinformatics / microbiology / life-science PhD thesis — the FAIR data, versioned code, report-generation, figure-and-table discipline, and the reproducibility expectations that examiners probe at viva."
license: MIT
---
<!-- metadata:
  category: thesis-writing
  oversight: high
  version: 1.0.0
  author: Pradyumna Jayaram
  tags: [thesis-writing, reproducibility, fair, bioinformatics, figures]
  difficulty: advanced
-->

# Thesis Methods & Reproducibility (Bioinformatics / Microbiology)

The examiner's sharpest questions land on Methods, figures, and "could I
reproduce this?" This skill turns a thesis chapter into something reproducible:
versioned code, FAIR data, a regenerable report, disciplined figures and tables,
and a methods section that states every choice. It borrows the figure discipline
of `figure-design` and the FAIR deposit mechanics of `fair-data`.

## Hard rules

1. **No fabricated citations.** Every reference in Methods (the tool, the
   protocol, the prior parameter choice) must resolve to a verifiable record —
   a DOI, a versioned code URL, or a dated documentation page. A method that
   cites "a standard pipeline" with no version is not cited.
2. **No claim without provenance.** Every number in Results must trace to a
   dataset, a table, a figure, or a log line the agent can open. A reported
   accuracy or abundance that does not resolve to an output file is a defect.
3. **No silent failure.** Every pipeline step, script, or API call you describe
   must declare its exit status and what happens on non-zero. A methods
   section that omits a step which failed (and was quietly skipped) is a
   reproducibility violation.
4. **Reproducible by definition.** The chapter must state: the exact code,
   version, and seed; the data access + version; and the command to regenerate
   each figure. If any of the three is missing, the figure is not reproducible
   and must be flagged.

## When to use

- Writing the Methods chapter of a bioinformatics, microbiology, or
  computational life-science thesis.
- Preparing figure/table code so a reviewer can rerun it.
- The "show me how you'd reproduce Figure 4" viva rehearsal.

## When NOT to use

- The whole-thesis structure — use `thesis-structure`.
- Choosing the statistical test or a multiple-comparison correction — choose
  that outside this skill; this skill only reports the choice and its
  parameters (relevant in microbiology, where multiple comparisons dominate).
- Making thesis figures into publication-grade art — use `figure-design`.

## Prerequisites

- Working code for every method, or at least the scripts/parameters actually
  used. "What I did in a notebook, from memory" is not enough — reconstruct it
  and version it.
- The raw data and where it lives, and whether it can be shared (check data
  policies, especially human/clinical or restricted-pathogen data).

## Reproducibility checklist

**Code.**
- One repo per thesis (or per major method), with a lockfile
  (`environment.yml` / `requirements.txt` with pins, `renv`/`packrat` for R, or
  a `conda` env).
- A top-level entry point that regenerates *all* analysis outputs: `make all`
  or a Snakemake/Nextflow/Cromwell workflow (see `snakemake-workflow-engine`).
- Fixed seeds, or a recorded seed, for any stochastic step (ML, subsampling,
  rarefaction in microbiome work).
- A short `Reproducing the results` block in the thesis: exact command,
  compute + time, and what to expect as output.

**Data (FAIR).**
- **F**indable: deposited with an accession/DOI (e.g. an SRA/ENA accession for
  sequencing, a Zenodo DOI for code + processed data) or a clear "unavailable:
  reason" line.
- **A**ccessible: the access path + any access restriction, stated.
- **I**nteroperable: standard formats (FASTQ/BAM/CRAM, feature tables, not a
  private script's binary).
- **R**eusable: a provenance/lineage note — which raw data, which filters,
  which version produced the result in the figure.
- Do not fabricate a DOI or accession if you have not actually deposited it;
  say "to be deposited" and open the task.

**Figures & tables.**
- Each figure/table is produced by a committed script and listed in a
  `figures/` manifest (figure id → script → data → output). No hand-edited
  figure images without the generating script.
- Figure panels are self-describing (labels, bars/units, n, error-bar type) —
  the caption alone should let a reader interpret it (see `figure-design`).
- A master caption/legend list in the back matter matches the in-text callouts
  one-for-one.
- Table notes state units, n, and the correction method used for any
  omics-scale comparison.

## Methods-section discipline

Write Methods so a stranger reruns it:
- State **every** parameter, not just the "interesting" ones (the k in k-NN,
  the cutoff, the normalization, the read length, the genome build).
- Name the tool + version + key flags (`tool v2.1.4, --min-mapq 30`).
- For each decision, one clause of *why* — enough that the examiner can
  challenge the choice, not just note it.
- If a step failed and you adapted, say so (this is where "no silent failure"
  bites — the adapted step must be described, not hidden).

## Pitfalls

- **"As per standard protocol"** with no version — not reproducible, and an
  easy viva probe.
- **A notebook with hidden interactive state** — a figure depends on an in-run
  cell that is not in the committed version.
- **Random steps without a seed** — reruns give different numbers.
- **Hand-cropped figure images** — the generating script doesn't exist or
  doesn't match.
- **A fabricated accession** to look complete — a provenance violation; say
  "pending" instead.
- **Omitting the step that didn't work** — the classic silent failure.
- **Un-corrected multiple comparisons** in microbiome / omics abundance
  claims.

## Validation

- A clean clone of the repo + a data fetch reproduces every figure in the
  manifest, or the gap is explicitly listed as not-yet-reproduced (never
  silently assumed).
- Every quantitative claim in Results opens to a file, table, or log.
- FAIR status is stated per dataset: accession/DOI, or "unavailable: reason."
- The figure manifest's count equals the back-matter list-of-figures count.

## References

- `snakemake-workflow-engine` — choosing and building the workflow backbone
  (Snakemake / Nextflow / Cromwell) for report regeneration.
- `fair-data` — the FAIR deposit mechanics for datasets.
- `code-release` — releasing the thesis code with a version.
- `figure-design` — the figure-communication craft behind every visual.
- `image-analysis-best-practices` — the controls / replicate discipline for
  image- and microscopy-based methods.
- `samtools-bam-processing` — the concrete sequence-analysis step behind
  read-based methods.
- FAIR principles (authoritative current wording — verify against the official
  guidance, not a paraphrase).

## Cross-references

- thesis-structure — the chapter architecture this methods discipline plugs
  into.
- thesis-defense-viva — the reproducibility probes the examiner will ask.
- figure-design — the figure discipline for every visual in the thesis.
- fair-data — the deposit mechanics behind the FAIR data rule.

(For the final provenance pass over the whole methods chapter, run the
`meta/integrity-audit` skill. Content skills in this repo do not cross-reference
`meta/` slugs as bullets, so it is referenced in prose here.)

## Changelog

- **1.0.0** (2026-06-18) — Initial release. Reproducibility checklist for
  versioned code, FAIR data, and figure-manifest discipline; methods-section
  specificity rules; and the silent-failure traps, tuned for bioinformatics /
  microbiology theses.
