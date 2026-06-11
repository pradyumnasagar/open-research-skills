# open-research-skills — agent and contributor guide

> A curated collection of research-domain skills for AI agents.
> Authored by **Pradyumna Jayaram**, 2026.

This file is the entry point for AI agents and human contributors. It supersedes and replaces `CONTRIBUTING.md` (which is kept as a thin alias for the GitHub "Contribute" button).

## What this repo is

`open-research-skills` (ORS) is a comprehensive skill library for AI agents working alongside researchers, academics, graduate students, postdocs, and R&D engineers. It covers the full lifecycle of research:

```
literature search → experimental design → analysis → writing → publication → grant writing → mentorship → ethics
```

## Current status (v0.3.0)

**18 categories, 118 skills** — see `INDEX.md` for the per-skill table.

## Layout

```
open-research-skills/
├── README.md                    # main readme
├── LICENSE                      # MIT
├── AGENTS.md                    # this file
├── CONTRIBUTING.md              # alias for GitHub "Contribute" button
├── CHANGELOG.md                 # release notes
├── ROADMAP.md                   # what's done, what's next
├── INDEX.md                     # per-skill table
├── SCHEMA.md                    # frontmatter spec (legacy, see spec/)
├── TAXONOMY.md                  # 18 categories (legacy, see spec/)
├── THIRD_PARTY_NOTICES.md       # upstream attributions
│
├── .claude-plugin/              # Claude Code plugin marketplace
│   └── marketplace.json
│
├── spec/                        # ORS specification
│   ├── README.md
│   ├── skill-format.md
│   └── category-taxonomy.md
│
├── template/                    # template for new skills
│   └── SKILL.md
│
├── examples/                    # worked examples
│   ├── README.md
│   ├── claude-code-installation.md
│   ├── api-integration.md
│   └── multi-skill-workflow.md
│
├── scripts/                     # repo automation
│   ├── README.md
│   ├── validate-skills.py
│   └── build-index.py
│
├── tests/                       # test suite
│   ├── test_frontmatter.py
│   ├── test_skill_structure.py
│   └── fixtures/
│
├── .github/workflows/           # CI
│   ├── validate.yml
│   └── release.yml
│
└── skills/                      # all 118 skills, organized in 18 categories
    ├── AGENTS.md                # skill-authoring guide
    ├── bioinformatics-sequence/ # 23 skills
    ├── chemoinformatics/        # 19 skills
    ├── research-grants/         # 9 skills
    └── ... (15 more categories)
```

## Installation

### As a Claude Code plugin (recommended)

```bash
/plugin marketplace add pradyumnasagar/open-research-skills
/plugin install ors-research@pradyumnasagar
/plugin install ors-bioinformatics@pradyumnasagar
/plugin install ors-career-ethics@pradyumnasagar
```

### As a git clone

```bash
git clone https://github.com/pradyumnasagar/open-research-skills.git
cd open-research-skills
claude
```

In the chat, ask Claude to use a specific skill by name:

```
> Use the bwa-alignment skill to align these reads to GRCh38.
```

See `examples/claude-code-installation.md` for more.

### Programmatically (API)

See `examples/api-integration.md` for Python, TypeScript, Bedrock, and Vertex examples.

## Skill format

Every skill lives at `skills/<category>/<slug>/SKILL.md` and has the form:

```yaml
---
name: <kebab-case-slug>
description: <one or two sentences — what & when>
license: MIT        # optional
---

<!-- metadata: ... (optional) -->

# Skill Title

> Tagline

## When to use
## Workflow
## Code patterns
## Pitfalls
## Validation
## References
```

The full spec is in `spec/skill-format.md`.

## Adding a new skill

1. Read `skills/AGENTS.md` — the skill-authoring guide.
2. Copy `template/SKILL.md` to `skills/<category>/<your-slug>/SKILL.md`.
3. Fill in the frontmatter (`name` and `description` are required).
4. Fill in the body and the optional `<!-- metadata: ... -->` block.
5. Run `python scripts/validate-skills.py skills/` to validate.
6. Run `python scripts/build-index.py` to regenerate `INDEX.md`.
7. Open a PR.

## Adding a new category

See `spec/category-taxonomy.md` — the bar is high. Propose in an issue first.

## License

MIT. All skills authored by Pradyumna Jayaram unless explicitly co-authored in a PR. See `THIRD_PARTY_NOTICES.md` for upstream attributions.

## No AI co-authorship

This repo is authored by Pradyumna Jayaram. Commits must not include `Co-Authored-By:` lines for AI assistants.

## Versioning

Semantic versioning:

- **Major** — break the frontmatter contract, remove/rename categories.
- **Minor** — add categories, add skills, backwards-compatible schema additions.
- **Patch** — fix typos, update tooling versions, add validation tests.

Current: **v0.3.0** (restructure to match Anthropic skills pattern).
