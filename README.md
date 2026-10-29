# open-research-skills
[![DOI](https://zenodo.org/badge/1265757749.svg)](https://doi.org/10.5281/zenodo.20769989)

> A curated collection of research-domain skills for AI agents.
> Authored by **Pradyumna Jayaram**, 2026.

`open-research-skills` (ORS) is a comprehensive skill library for AI agents working alongside researchers, academics, graduate students, postdocs, and R&D engineers. It covers the full lifecycle of research:

```
literature search → experimental design → analysis → writing → publication → grant writing → mentorship → ethics
```

## Current status (v0.5.0)

**19 categories, 123 skills + 5 meta skills** — see `INDEX.md` for the per-skill table.

| Category | Skills | Description |
|---|---|---|
| `bioinformatics-sequence` | 23 | FASTA/FASTQ/BAM/VCF, alignment, QC, Biopython |
| `chemoinformatics` | 19 | RDKit, ADMET, virtual screening, retrosynthesis, generative design |
| `research-grants` | 11 | NIH R01/K, NSF, ERC, fellowships, foundations, DARPA, India, proposal craft |
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
| `thesis-writing` | 3 | Monograph / article-based structure, methods & reproducibility, viva defense |
| `data-engineering` | 1 | Snakemake pipeline management |

### Meta skills (5)

Cross-cutting skills that orchestrate or audit the domain skills. Loaded
for authoring, pre-publish audits, and inter-skill handoffs.

| Meta skill | Role |
|---|---|
| `meta/roadmap-author` | Author a new ORS skill from scratch (template + author guide + validator). |
| `meta/integrity-audit` | 7-mode AI failure-mode checklist applied before any publish / release / merge. |
| `meta/release-management` | Semver discipline, changelog, marketplace.json update, graduation criteria. |
| `meta/cross-reference-mapper` | Generate and verify `## Cross-references` between skills. |
| `meta/agent-handoff` | Material Passport schema for inter-skill handoffs. |

## Installation

### Option 1: Claude Code plugin (recommended)

```bash
/plugin marketplace add pradyumnasagar/open-research-skills
/plugin install ors-research@pradyumnasagar
/plugin install ors-bioinformatics@pradyumnasagar
/plugin install ors-career-ethics@pradyumnasagar
/plugin install ors-meta@pradyumnasagar
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
│   ├── category-taxonomy.md # 19 categories
│   ├── material-passport.md # Material Passport spec (v1.0.0)
│   └── material-passport.schema.json  # JSON Schema (Draft 2020-12)
│
├── docs/
│   └── pipelines.md         # end-to-end reference pipelines
│
├── template/
│   └── SKILL.md             # template for new skills
│
├── examples/                # worked examples
│   ├── README.md
│   ├── claude-code-installation.md
│   ├── api-integration.md
│   ├── multi-skill-workflow.md
│   ├── showcase-rnaseq-mini.md
│   ├── Makefile
│   └── bwa-alignment.passport.json
│
├── scripts/                 # repo automation
│   ├── README.md
│   ├── validate-skills.py
│   ├── validate-passport.py
│   ├── build-index.py
│   └── bulk-migrate-v0.4.0.py
│
├── tests/                   # test suite
│   └── ...
│
├── skills/                  # all 123 skills, organized in 19 categories
│   ├── AGENTS.md            # skill-authoring guide
│   ├── bioinformatics-sequence/  (23 skills)
│   ├── chemoinformatics/         (19 skills)
│   ├── research-grants/          (9 skills)
│   └── ... (15 more categories)
│
└── meta/                    # 5 cross-cutting meta skills
    ├── roadmap-author/
    ├── integrity-audit/
    ├── release-management/
    ├── cross-reference-mapper/
    └── agent-handoff/
```

## How a skill is structured

```yaml
---
name: <kebab-case-slug>
description: <one or two sentences — what & when>
license: MIT        # optional
---

<!-- metadata:
  category: <one of 19 leaf categories>
  oversight: very-high | high | medium | low
  version: <semver>
  author: <name>
  tags: [<kebab-case tags>]
  difficulty: beginner | intermediate | advanced
-->

# Skill Title

> Tagline

## When to use
## When NOT to use
## Hard rules
## Workflow
## Code patterns
## Validation
## Cross-references
## Changelog
```

The full spec is in [`spec/skill-format.md`](spec/skill-format.md). The
minimal contract is `name` + `description`, matching the
[Anthropic Agent Skills specification](https://agentskills.io/specification).
ORS v0.4.0 adds a `<!-- metadata: ... -->` block in the body and requires
`## Hard rules`, `## Cross-references`, and `## Changelog` sections.

## How this was made

ORS was authored by Pradyumna Jayaram in June 2026, adapting patterns from 5 upstream sources. **No prose was copied verbatim.** Every `SKILL.md` carries a `sources` field in its metadata block listing what was consulted. See `THIRD_PARTY_NOTICES.md` for the full attribution.

## Upcoming (v0.6.0 and beyond)

Additional categories to be built:

- `bioinformatics-omics` (ATAC-seq, ChIP-seq, scRNA-seq, spatial transcriptomics)
- `structural-biology` (PyMOL, ChimeraX, MD, AlphaFold integration)
- `epidemiological-genomics` (pathogen genomics, outbreak analysis)
- `ecological-genomics` (metagenomics, eDNA)
- `phylogenetics` (IQ-TREE, BEAST, pangenomes)
- `clinical-translation` (clinical trials, IND/NDA, regulatory pathways)

For the current v0.5.0 release, see [What's new in v0.5.0](#whats-new-in-v050) below; the v0.4.0 notes remain in [What's new in v0.4.0](#whats-new-in-v040).

## License

MIT. All 123 skills are original work by Pradyumna Jayaram. See `LICENSE` and `THIRD_PARTY_NOTICES.md`.

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
**v0.4.0** (2026-06-17) — Spec hardening + meta skills. v0.4.0 schema with `## Hard rules`, `## When NOT to use`, `## Cross-references`, `## Changelog` sections; canonical `<!-- metadata: ... -->` block with `oversight`, `version`, `author`, `tags`, `difficulty`; 5 meta skills (`roadmap-author`, `integrity-audit`, `release-management`, `cross-reference-mapper`, `agent-handoff`); Material Passport schema (`spec/material-passport.md` + `spec/material-passport.schema.json`) with example and `scripts/validate-passport.py`; pipeline reference (`docs/pipelines.md`); runnable showcase (`examples/showcase-rnaseq-mini.md` + `examples/Makefile`); validator (`scripts/validate-skills.py`) enforces the new schema across all 118 + 5 skills.
**v0.5.0** (2026-06-18) — New `thesis-writing` category (3 skills: monograph / article-based structure, methods & reproducibility, viva defense) and 2 new `research-grants` skills (`indian-grant-ecosystem`, `grant-proposal-craft`). 123 content skills across 19 categories.

## What's new in v0.5.0

- **New `thesis-writing` category** — 3 skills for doctoral theses in
  bioinformatics and the life sciences:
  - `thesis-structure` — monograph vs article-based, IMRaD chapter spine,
    front/back matter, and a structure workflow.
  - `thesis-methods-reproducibility` — versioned code, FAIR data, figure
    manifests, and self-describing panels for bioinformatics pipelines.
  - `thesis-defense-viva` — viva question-set building, presentation script,
    and "when stuck" recovery moves.
- **Indian grant ecosystem** — `research-grants/indian-grant-ecosystem`
  maps the national funding landscape (VGST, NRF, PMRG, OIM, ISTIP,
  IndiaBioscience, ICMR, BIRAC) with scheme-selection workflow and budget
  discipline. Indicative figures throughout; every number is labeled as
  directional, and agency sites are the source of truth.
- **Grant proposal craft** — `research-grants/grant-proposal-craft` codifies
  the four scoring dimensions (novelty, usefulness, methodology, who) plus
  section-by-section writing guidance, SMART objectives, pitfall planning,
  and Gantt / budget discipline.
- **Package bump to 0.5.0** — validator now accepts the new
  `category: thesis-writing`; INDEX regenerated (123 skills / 19 categories);
  plugin registration updated (`.claude-plugin/marketplace.json`,
  `plugin.json`).

## What's new in v0.4.0

- **Spec hardening** — every skill now has a `<!-- metadata: ... -->` block
  recording its category, oversight level, version, author, tags, and
  difficulty. The validator enforces required sections: `## Hard rules`,
  `## Cross-references`, `## Changelog`. See `spec/skill-format.md`.
- **Hard rules** — every skill states 3 base rules (no fabricated citations,
  no claim without provenance, no silent failure) plus 0-5 domain-specific
  rules. These are the **contract** an agent agrees to when loading the skill.
- **5 meta skills** — cross-cutting orchestration patterns that don't fit
  any single domain. See [Meta skills](#meta-skills-5) above.
- **Material Passport** — a JSON envelope that travels with every artifact,
  capturing inputs, outputs, decisions, errors, and provenance. Lets one
  skill's output feed another without re-deriving context. See
  `spec/material-passport.md` and `examples/bwa-alignment.passport.json`.
- **Pipelines** — `docs/pipelines.md` documents 5 end-to-end reference
  pipelines (RNA-seq, systematic review, compound screening, microscopy,
  grant writing), each linking the skills and the passports between them.
- **Runnable showcase** — `examples/showcase-rnaseq-mini.md` + `examples/Makefile`
  walks a user through a 4-skill, 4-passport pipeline that produces a
  volcano plot from synthetic FASTQ in < 5 minutes.
- **Release discipline** — `meta/release-management/SKILL.md` codifies the
  semver workflow: per-skill bumps, package bumps, changelog discipline,
  breaking-change protocol, and the v1.0.0 graduation criteria.
- **Integrity audit** — `meta/integrity-audit/SKILL.md` provides a 7-mode
  checklist (fabricated citations, silent failures, scope creep, missing
  provenance, unsupervised writes, version drift, hallucinated APIs) to
  run before any publish / release / merge.

## Index

See `INDEX.md`.
