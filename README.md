# open-research-skills

> A curated collection of research-domain skills for AI agents.
> Authored by **Pradyumna Jayaram**, 2026.

`open-research-skills` (ORS) is a comprehensive skill library for AI agents working alongside researchers, academics, graduate students, postdocs, and R&D engineers. It covers the full lifecycle of research: literature search → experimental design → analysis → writing → publication → grant writing → mentorship → ethics.

## What is a "skill"?

Each subfolder contains a `SKILL.md` file that an AI agent reads to gain deep, domain-specific knowledge. Skills include worked code patterns, 2026-current tool versions, anti-patterns, open-source alternatives to commercial tools, and validation steps. They are **not** raw documentation dumps — they are opinionated, pragmatic, and ready to use.

## Current Status (v0.2.0)

**18 categories, 117 skills** — See `INDEX.md` for the full table.

| Category | Skills | Description |
|---|---|---|
| `bioinformatics-sequence` | 23 | FASTA/FASTQ/BAM/VCF, alignment, QC, Biopython |
| `chemoinformatics` | 19 | RDKit, ADMET, virtual screening, retrosynthesis, generative design |
| `lab-automation` | 6 | Opentrons/PyLabRobot, ELNs (eLabFTW/Chemotion/openBIS) |
| `mentorship-teaching` | 4 | Onboarding, goal setting, syllabus, course design |
| `scientific-communication` | 5 | Talks, posters, podcasts, press releases, elevator pitch |
| `data-engineering` | 1 | Snakemake pipeline management |
| `open-science` | 5 | FAIR data, preprints, preregistration, code release, licensing |
| `research-grants` | 9 | NIH R01/K, NSF, ERC, fellowships, foundations, DARPA |
| `ethics-compliance` | 4 | IRB protocols, data privacy, AI disclosure, image integrity |
| `career-navigation` | 6 | Academic CV, tenure, industry transition, interview prep |
| `scientific-writing` | 5 | Manuscript structure, cover letters, rebuttals, AI disclosure |
| `image-analysis-microscopy` | 4 | CellProfiler, QuPath, ImageJ/Fiji, best practices |
| `machine-learning-bio` | 4 | Protein LMs, DL for genomics, AlphaFold, scRNA-seq DL |
| `scientific-thinking` | 5 | Brainstorming, critical thinking, hypothesis generation, perspective tour, failure handling |
| `peer-review` | 4 | Manuscript review, grant review, scholar evaluation, reviewer response |
| `literature-research` | 5 | Literature search, systematic review, citation management, paper lookup |
| `scientific-visualization` | 5 | Figure design, schematics, slides, posters, color & accessibility |
| `humanizer-skills` | 4 | Scientific voice, AI disclosure, text humanizing, AI detection awareness |

## Upcoming v0.3.0 (planned)

Additional categories to be built:
- bioinformatics-omics (ATAC-seq, ChIP-seq, scRNA-seq, spatial transcriptomics)
- structural-biology (PyMOL, ChimeraX, MD, AlphaFold integration)
- epidemiological-genomics (pathogen genomics, outbreak analysis)
- ecological-genomics (metagenomics, eDNA)
- phylogenetics (IQ-TREE, BEAST, pangenomes)
- clinical-translation (clinical trials, IND/NDA, regulatory pathways)

## How to use

Each skill is self-contained. The agent reads `SKILL.md` and follows it. The frontmatter tells the agent:

- **When** the skill applies (`description`, `when to use` section)
- **What** tools to use (frontmatter `prerequisites.tools`)
- **What** other ORS skills it depends on (frontmatter `prerequisites.skills`)
- **What** open alternatives exist if a commercial tool is referenced

The body sections give the agent: the canonical workflow, code patterns, common pitfalls, validation, references, changelog.

## How this was made

ORS was authored by Pradyumna Jayaram in June 2026, adapting material from 5 upstream sources:

- **bioSkills** (https://github.com/GPTomics/bioSkills) — MIT
- **SciAgent-Skills** — open license
- **academic-research-skills** — CC BY-NC 4.0
- **scientific-agent-skills** — open license (originally K-Dense Inc.)
- **academic-research-skills-codex** — open license

Every `SKILL.md` carries a `sources_consulted:` block listing exactly which upstream sources informed it and what was changed. **No prose is copied verbatim.** Code patterns that are canonical (e.g. `bwa mem | samtools sort`) are kept structurally similar because that's the standard pattern, but are re-annotated and surrounded by original prose.

Gap skills (e.g. grant writing, ethics, mentorship, open science) were authored from scratch using public, verifiable sources only — NIH/NSF/ICMJE/COPE/PRISMA/FAIR Principles/spirit-statement.org/ICH-GCP/etc.

## License

MIT. See `LICENSE`. All 18 category subfolders and the `_meta/`, `_templates/`, `_inventory/` directories are original work by Pradyumna Jayaram.

## Contributing

See `CONTRIBUTING.md` and the schema in `_meta/SCHEMA.md`. Short version:

1. Use the template at `_templates/SKILL-TEMPLATE.md`.
2. Folder name = `name:` in frontmatter = `ors-<category>-<skill-slug>`.
3. Author: Pradyumna Jayaram (or co-author in PR).
4. No verbatim copying. Cite sources. No hallucination.
5. Open alternatives for commercial tools.

## Versioning

**v0.1.0** (2026-06-10) — Initial release with 58 skills across 7 source-mapped categories.  
**v0.2.0** (2026-06-10) — Gap-build round with 59 additional skills across 11 new categories, including K-Dense-style skills for thinking, peer review, literature, visualization, and humanizer workflows.

## Index

See `INDEX.md` for a per-skill table (path, name, description, difficulty).
