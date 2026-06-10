# open-research-skills

> A curated collection of research-domain skills for AI agents.
> Authored by **Pradyumna Jayaram**, 2026.

`open-research-skills` (ORS) is a comprehensive skill library for AI agents working alongside researchers, academics, graduate students, postdocs, and R&D engineers. It covers the full lifecycle of research: literature search → experimental design → analysis → writing → publication → grant writing → mentorship → ethics.

## What is a "skill"?

Each subfolder contains a `SKILL.md` file that an AI agent reads to gain deep, domain-specific knowledge. Skills include worked code patterns, 2026-current tool versions, anti-patterns, open-source alternatives to commercial tools, and validation steps. They are **not** raw documentation dumps — they are opinionated, pragmatic, and ready to use.

## Current Status (v0.2.0)

**18 categories, 118 skills** — See `INDEX.md` for the full table.

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

## How to install

The skills are plain markdown + YAML. There is **nothing to compile, install, or run** — your AI agent just needs to be told where the skills live and how to load them.

### 1. Clone the repository

```bash
git clone https://github.com/pradyumnasagar/open-research-skills.git
cd open-research-skills
```

Or with SSH:

```bash
git clone git@github.com:pradyumnasagar/open-research-skills.git
cd open-research-skills
```

You can also install it as a git submodule inside another project:

```bash
git submodule add git@github.com:pradyumnasagar/open-research-skills.git .skills/open-research-skills
```

### 2. Point your agent at it

The exact mechanism depends on your agent runtime. The general idea is the same: tell the agent where the `SKILL.md` files live and let it read the ones it needs.

**Claude Code (CLI) — point the agent at the repo**

The simplest approach is to start Claude Code with the repo as the working directory (or as a parent). Claude will discover `SKILL.md` files automatically when they're relevant to the conversation:

```bash
# Either way works — the agent will pick up the SKILL.md files
cd open-research-skills
claude

# Or add it as a subdirectory of an existing project
cd ~/myproject
claude    # Claude will see ../open-research-skills/*/SKILL.md
```

You can also mention a specific skill by name in your prompt, e.g.:

> "Use the ors-bwa-alignment skill to align these reads."

**Cursor / Continue / Cody / Aider / Windsurf / other IDE agents**

Add the repo (or a subset of categories) to the agent's context sources. Most agents let you drop a folder into a "skills" or "rules" panel. The `SKILL.md` files are valid markdown and will be read as instructions.

**Claude API / Anthropic SDK / Bedrock / Vertex — use the skills as system context**

Read the `SKILL.md` files yourself and concatenate them into the `system` parameter of your API call. Example for a single skill:

```python
import pathlib

skill = pathlib.Path("open-research-skills/scientific-writing/manuscript-structure/SKILL.md").read_text()

response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=4096,
    system=f"You are a research assistant. Use the following skill:\n\n{skill}",
    messages=[{"role": "user", "content": "Help me write the methods section for a ChIP-seq paper."}]
)
```

For multi-skill workflows, concatenate the frontmatter of all relevant skills (frontmatter is the YAML between `---` markers) into a routing prompt, and only inject the full `SKILL.md` of the skill the agent ends up using.

**Custom agents / LangChain / LlamaIndex / OpenAI Assistants**

Use any of the standard "load documents → chunk → inject into context" patterns. The `SKILL.md` files are small (most are 200–500 lines, ~5–15 KB) so they fit comfortably in a single retrieval-augmented context window.

### 3. Pin a version (recommended for reproducibility)

Tag the release you depend on:

```bash
git clone --branch v0.2.0 https://github.com/pradyumnasagar/open-research-skills.git
```

…then update at your own cadence by `git pull`-ing later. We follow [semantic versioning](https://semver.org/) — a new minor version (0.3.0) will add categories without breaking existing skills.

### 4. Verify the install

```bash
# How many skills did you get?
find open-research-skills -name "SKILL.md" | wc -l
# Expected on v0.2.0: 118
```

## How to use

Once the agent has the skills loaded, the workflow is:

1. **Describe the task** in your prompt (e.g. "Help me draft an R01 specific aims page").
2. The agent matches the task to one or more `ors-*` skills (the frontmatter's `description:` field is written for this).
3. The agent reads the full `SKILL.md`, follows the workflow, uses the code patterns, avoids the pitfalls, and runs the validation.

The frontmatter tells the agent:

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

MIT. See `LICENSE`. All 18 category subfolders and the root `CONTRIBUTING.md`, `SCHEMA.md`, `TAXONOMY.md` files are original work by Pradyumna Jayaram.

## Contributing

See `CONTRIBUTING.md` and the schema in `SCHEMA.md`. Short version:

1. Use the template at `_templates/SKILL-TEMPLATE.md`.
2. Folder name = `name:` in frontmatter = `ors-<category>-<skill-slug>`.
3. Author: Pradyumna Jayaram (or co-author in PR).
4. No verbatim copying. Cite sources. No hallucination.
5. Open alternatives for commercial tools.

## Versioning

**v0.1.0** (2026-06-10) — Initial release with 58 skills across 6 source-mapped categories.
**v0.2.0** (2026-06-10) — Gap-build round with 60 additional skills across 12 new categories, including K-Dense-style skills for thinking, peer review, literature, visualization, and humanizer workflows.

## Repository layout

```
open-research-skills/
├── README.md                  # this file
├── LICENSE                    # MIT
├── CONTRIBUTING.md            # how to add a skill
├── SCHEMA.md                  # frontmatter schema
├── TAXONOMY.md                # category list
├── INDEX.md                   # per-skill table (118 rows)
├── CHANGELOG.md               # release notes
├── ROADMAP.md                 # what's done / what's next
├── _templates/
│   └── SKILL-TEMPLATE.md      # copy this to make a new skill
├── bioinformatics-sequence/   # category folders (one per category)
├── career-navigation/
├── chemoinformatics/
├── data-engineering/
├── ethics-compliance/
├── humanizer-skills/
├── image-analysis-microscopy/
├── lab-automation/
├── literature-research/
├── machine-learning-bio/
├── mentorship-teaching/
├── open-science/
├── peer-review/
├── research-grants/
├── scientific-communication/
├── scientific-thinking/
├── scientific-visualization/
└── scientific-writing/
```

## Index

See `INDEX.md` for a per-skill table (slug, description, difficulty).
