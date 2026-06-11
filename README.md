# open-research-skills
[![DOI](https://sandbox.zenodo.org/badge/1265757749.svg)](https://handle.test.datacite.org/10.5072/zenodo.512325)

> A curated collection of research-domain skills for AI agents.
> Authored by **Pradyumna Jayaram**, 2026.

`open-research-skills` (ORS) is a comprehensive skill library for AI agents working alongside researchers, academics, graduate students, postdocs, and R&D engineers. It covers the full lifecycle of research:

```
literature search → experimental design → analysis → writing → publication → grant writing → mentorship → ethics
```

## Current status (v0.3.0)

**18 categories, 118 skills** — see `INDEX.md` for the per-skill table.

| Category | Skills | Description |
|---|---|---|
| `bioinformatics-sequence` | 23 | FASTA/FASTQ/BAM/VCF, alignment, QC, Biopython |
| `chemoinformatics` | 19 | RDKit, ADMET, virtual screening, retrosynthesis, generative design |
| `research-grants` | 9 | NIH R01/K, NSF, ERC, fellowships, foundations, DARPA |
| `lab-automation` | 6 | Opentrons/PyLabRobot, ELNs (eLabFTW/Chemotion/openBIS) |
| `career-navigation` | 6 | Academic CV, tenure, industry transition, interview prep |
| `scientific-communication` | 5 | Talks, posters, podcasts, press releases, elevator pitch |
| `open-science` | 5 | FAIR data, preprints, preregistration, code release, licensing |
| `scientific-writing` | 5 | Manuscript structure, cover letters, rebuttals, AI disclosure |
| `scientific-thinking` | 5 | Brainstorming, critical thinking, hypothesis generation, perspective tour, failure handling |
| `scientific-visualization` | 5 | Figure design, schematics, slides, posters, color & accessibility |
| `literature-research` | 5 | Literature search, systematic review, citation management, paper lookup |
| `mentorship-teaching` | 4 | Onboarding, goal setting, syllabus, course design |
| `image-analysis-microscopy` | 4 | CellProfiler, QuPath, ImageJ/Fiji, best practices |
| `machine-learning-bio` | 4 | Protein LMs, DL for genomics, AlphaFold, scRNA-seq DL |
| `ethics-compliance` | 4 | IRB protocols, data privacy, AI disclosure, image integrity |
| `peer-review` | 4 | Manuscript review, grant review, scholar evaluation, reviewer response |
| `humanizer-skills` | 4 | Scientific voice, AI disclosure, text humanizing, AI detection awareness |
| `data-engineering` | 1 | Snakemake pipeline management |

## Installation

### Option 1: Claude Code plugin (recommended)

```bash
/plugin marketplace add pradyumnasagar/open-research-skills
/plugin install ors-research@pradyumnasagar
/plugin install ors-bioinformatics@pradyumnasagar
/plugin install ors-career-ethics@pradyumnasagar
```

Then in a chat:

```
> Use the bwa-alignment skill to align these reads to GRCh38.
```

### Option 2: git clone

```bash
git clone https://github.com/pradyumnasagar/open-research-skills.git
cd open-research-skills
claude
```

In the chat, reference skills by name. The agent reads the relevant `SKILL.md` from `skills/`.

### Option 3: programmatic use

See `examples/api-integration.md` for Python, TypeScript, AWS Bedrock, and Google Vertex examples.

## Layout

```
open-research-skills/
├── README.md                # this file
├── LICENSE                  # MIT
├── AGENTS.md                # agent/contributor guide
├── CONTRIBUTING.md          # alias for GitHub "Contribute" button
├── CHANGELOG.md             # release notes
├── ROADMAP.md               # what's done, what's next
├── INDEX.md                 # per-skill table
├── SCHEMA.md                # legacy frontmatter spec (see spec/skill-format.md)
├── TAXONOMY.md              # legacy taxonomy (see spec/category-taxonomy.md)
├── THIRD_PARTY_NOTICES.md   # upstream attributions
│
├── .claude-plugin/
│   └── marketplace.json     # Claude Code plugin marketplace manifest
│
├── spec/                    # ORS specification
│   ├── README.md
│   ├── skill-format.md      # frontmatter spec
│   └── category-taxonomy.md # 18 categories
│
├── template/
│   └── SKILL.md             # template for new skills
│
├── examples/                # worked examples
│   ├── README.md
│   ├── claude-code-installation.md
│   ├── api-integration.md
│   └── multi-skill-workflow.md
│
├── scripts/                 # repo automation
│   ├── README.md
│   ├── validate-skills.py
│   └── build-index.py
│
├── tests/                   # test suite
│   └── ...
│
└── skills/                  # all 118 skills, organized in 18 categories
    ├── AGENTS.md            # skill-authoring guide
    ├── bioinformatics-sequence/  (23 skills)
    ├── chemoinformatics/         (19 skills)
    ├── research-grants/          (9 skills)
    └── ... (15 more categories)
```

## How a skill is structured

```yaml
---
name: <kebab-case-slug>
description: <one or two sentences — what & when>
license: MIT        # optional
---

<!-- metadata: (optional) -->

# Skill Title

> Tagline

## When to use
## Workflow
## Code patterns
## Pitfalls
## Validation
## References
```

The full spec is in [`spec/skill-format.md`](spec/skill-format.md). The minimal contract is `name` + `description`, matching the [Anthropic Agent Skills specification](https://agentskills.io/specification). ORS adds an optional `<!-- metadata: ... -->` block in the body for category, version, author, and tags.

## How this was made

ORS was authored by Pradyumna Jayaram in June 2026, adapting patterns from 5 upstream sources. **No prose was copied verbatim.** Every `SKILL.md` carries a `sources` field in its metadata block listing what was consulted. See `THIRD_PARTY_NOTICES.md` for the full attribution.

## Upcoming (v0.4.0)

Additional categories to be built:

- `bioinformatics-omics` (ATAC-seq, ChIP-seq, scRNA-seq, spatial transcriptomics)
- `structural-biology` (PyMOL, ChimeraX, MD, AlphaFold integration)
- `epidemiological-genomics` (pathogen genomics, outbreak analysis)
- `ecological-genomics` (metagenomics, eDNA)
- `phylogenetics` (IQ-TREE, BEAST, pangenomes)
- `clinical-translation` (clinical trials, IND/NDA, regulatory pathways)

## License

MIT. All 118 skills are original work by Pradyumna Jayaram. See `LICENSE` and `THIRD_PARTY_NOTICES.md`.

## Contributing

See `AGENTS.md` and `skills/AGENTS.md`. The short version:

1. Copy `template/SKILL.md` to `skills/<category>/<your-slug>/SKILL.md`.
2. Fill in `name`, `description`, and the body.
3. Run `python scripts/validate-skills.py skills/`.
4. Run `python scripts/build-index.py`.
5. Open a PR.

## Versioning

**v0.1.0** (2026-06-10) — Initial release with 58 skills across 6 source-mapped categories.
**v0.2.0** (2026-06-10) — Gap-build with 60 additional skills across 12 new categories.
**v0.3.0** (2026-06-11) — Restructure to match Anthropic skills pattern. Skills moved into `skills/`, frontmatter simplified, `.claude-plugin/marketplace.json` added for plugin install, `spec/`, `template/`, `examples/`, `scripts/`, `tests/`, `.github/workflows/` added.

## Index

See `INDEX.md`.
