# Roadmap — open-research-skills

## Status: 2026-06-10 (v0.2.0 complete)

| Status | Category | Skills | Notes |
|---|---|---|---|
| ✅ Done | bioinformatics-sequence | 23 | FASTA/FASTQ/BAM/VCF, alignment, QC, Biopython |
| ✅ Done | chemoinformatics | 19 | RDKit-centric, virtual screening, ADMET, PROTACs |
| ✅ Done | lab-automation | 6 | Opentrons, PyLabRobot, ELNs (Chemotion/eLabFTW/openBIS) |
| ✅ Done | mentorship-teaching | 4 | Onboarding, goal setting, syllabus, course design |
| ✅ Done | scientific-communication | 5 | Talks, posters, podcasts, press, pitch |
| ✅ Done | data-engineering | 1 | Snakemake (curated) |
| ✅ Done | open-science | 5 | FAIR data, preprints, preregistration, code release, licensing |
| ✅ Done | research-grants | 9 | NIH R01/K, NSF, ERC, fellowships, foundations, DARPA |
| ✅ Done | ethics-compliance | 4 | IRB, data privacy, AI disclosure, image integrity |
| ✅ Done | career-navigation | 6 | Academic CV, tenure, industry transition, interview prep |
| ✅ Done | scientific-writing | 5 | Manuscript structure, cover letters, rebuttals, AI disclosure |
| ✅ Done | image-analysis-microscopy | 4 | CellProfiler, QuPath, ImageJ/Fiji, best practices |
| ✅ Done | machine-learning-bio | 4 | Protein LMs, DL for genomics, AlphaFold, scRNA-seq DL |
| ✅ Done | scientific-thinking | 5 | Brainstorming, critical thinking, hypothesis generation, perspective tour, failure handling |
| ✅ Done | peer-review | 4 | Manuscript review, grant review, scholar evaluation, reviewer response |
| ✅ Done | literature-research | 5 | Literature search, systematic review, citation management, paper lookup, scoping review |
| ✅ Done | scientific-visualization | 5 | Figure design, schematics, slides, posters, color & accessibility |
| ✅ Done | humanizer-skills | 4 | Scientific voice, AI disclosure, text humanizing, AI detection awareness |

**Total delivered: 118 skills across 18 categories**

## Completed Releases

### v0.1.0 — 2026-06-10 (initial release)
- 6 categories, 58 skills
- Source-mapped inventory from 5 upstream collections: SciAgent-Skills, academic-research-skills, bioSkills, scientific-agent-skills, academic-research-skills-codex
- Original structure: bioinformatics-sequence, chemoinformatics, lab-automation, mentorship-teaching, scientific-communication, data-engineering

### v0.2.0 — 2026-06-10 (gap-build + K-Dense expansion)
- 12 additional categories, 60 new skills (total 118)
- Gap-fill: All missing categories from original inventory
- K-Dense-style addition: Thinking, peer review, literature, visualization, humanizer
- No verbatim copying from any source; only public frameworks and agency guidelines
- Authoring: All skills by Pradyumna Jayaram under MIT license

## Considered for v0.3.0

Categories that have not yet been built:

- **bioinformatics-omics** — ATAC-seq, ChIP-seq, CUT&RUN, scRNA-seq, spatial transcriptomics (the bioSkills source has these but as full tutorials — would require condensing)
- **structural-biology** — PyMOL, ChimeraX, MDAnalysis, GROMACS, AlphaFold integration (protein LMs skill exists as entry point)
- **epidemiological-genomics** — Pathogen genomics, outbreak analysis, surveillance (medium effort, narrow audience)
- **ecological-genomics** — Metagenomics, eDNA, environmental sampling (medium effort, narrow audience)
- **phylogenetics** — IQ-TREE, BEAST, RAxML, tree visualization, dN/dS analysis (foundation exists in bioinformatics-sequence)
- **clinical-translation** — Clinical trials design, IND/NDA, regulatory pathways, GCP (clinical domain gap)
- **statistics-bio** — Biostatistics for biology (power analysis, mixed models, survival analysis, multiple testing)

## Conventions
- One category = one folder
- One skill = one subfolder with `SKILL.md`
- Naming: `ors-<category>-<slug>` in frontmatter `name:` field
- Folder name = slug only (no `ors-`, no category prefix)
- All skills have: name, display_name, description, version, author, maintained_by, license, category, tags, difficulty, prerequisites, sources_consulted, last_updated
- All skills authored by Pradyumna Jayaram
- No verbatim copying from any source; only verifiable public frameworks, agency guidelines, and reference materials
