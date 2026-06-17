# ORS Skill Format

A `SKILL.md` file is a YAML-frontmatter + Markdown body. The frontmatter contract is a strict subset of the [Anthropic Agent Skills specification](https://agentskills.io/specification) plus a few ORS-specific conventions.

## Required frontmatter

```yaml
---
name: <unique-kebab-case-slug>
description: <one or two sentences — what the skill does and when to use it>
---
```

### `name`

- Unique across the whole repo. No two skills may share a `name`.
- Lowercase ASCII letters, digits, and hyphens. No leading/trailing hyphens.
- Convention: `name` is the same as the parent folder name (relative to `skills/` or `meta/`). For example, `skills/bioinformatics-sequence/bwa-alignment/SKILL.md` has `name: bwa-alignment`.
- Length: 1–64 characters.

### `description`

- A single sentence (or two short ones) that explains what the skill does and when to use it.
- Length: 1–1024 characters. The Agent Skills spec recommends ≤200 chars.
- This field is the **primary routing signal** for AI agents. An agent reads the description to decide whether to load the skill. Be specific.

## Optional frontmatter

```yaml
---
name: bwa-alignment
description: Align DNA sequencing reads to a reference genome using BWA-MEM.
license: MIT
---
```

### `license`

- SPDX identifier. Default is `MIT` (the repo's license). Include this only when a skill has its own license different from the repo.
- Valid SPDX identifiers: <https://spdx.org/licenses/>

## Body

The body is Markdown. **As of v0.4.0 the following body sub-sections are required** (the validator enforces them):

| Section | Purpose |
|---|---|
| `## When to use` | Trigger conditions for loading the skill |
| `## When NOT to use` | Anti-triggers; where another skill fits better |
| `## Hard rules` | Domain constraints this skill guarantees (see below) |
| `## Cross-references` | Slug-resolved links to related ORS skills |
| `## Changelog` | Version history |

Other commonly-used sections include `## Workflow`, `## Code patterns`, `## Pitfalls`, `## Validation`, `## References`. These are recommended but not enforced.

### Recommended body header

We recommend starting the body with an `<!-- metadata: ... -->` HTML comment that captures the ORS-specific fields that don't belong in the Anthropic-spec frontmatter:

```markdown
<!-- metadata:
  category: bioinformatics-sequence
  version: 1.0.0
  author: Pradyumna Jayaram
  oversight: medium
  tags: [bwa, alignment, sam, bam]
  difficulty: intermediate
  sources: bioSkills/sequence-alignment
-->

# BWA Alignment
```

### The `oversight` field

Defines how much **user verification** the skill's output requires before downstream use. Four levels:

| Level | Meaning | When to use |
|---|---|---|
| `very-high` | Output may fabricate facts. The agent **must** verify against source material before citing. | Generative skills (e.g., literature review synthesis, hypothesis generation, manuscript drafting) |
| `high` | Output may contain plausible-but-wrong details. The agent **should** spot-check. | Mixed generative + deterministic skills (e.g., systematic review, citation audit, peer review) |
| `medium` | Output is reliable for structure but not for content specifics. The agent may trust the framework, verify the content. | Procedural / advisory skills (e.g., manuscript structure, brainstorming, response to reviewers) |
| `low` | Output is deterministic or mechanical. The agent may trust without checking. | Script-driven skills (e.g., format conversion, sequence alignment, citation extraction) |

The validator enforces this enumeration. Authors may backfill `oversight: medium` for existing skills via `scripts/validate-skills.py --backfill`.

## Required body sub-sections

### `## Hard rules`

Every ORS skill must enumerate the constraints it guarantees. Three **base rules** are required of every skill:

1. **No fabricated citations** — every cited work must resolve to a verifiable record (DOI, PMID, arXiv ID, ISBN, URL with retrieval date, or stable identifier).
2. **No claim without provenance** — every quantitative or factual claim must point to a file, line, table, figure, or external source the agent can show.
3. **No silent failure** — every script invocation, API call, or tool use must declare its exit status and what to do on non-zero.

Skills extend this list with domain-specific rules. Examples:

- `systematic-review` adds: "PRISMA 2020 flow diagram mandatory; search strategy must be reproducible."
- `manuscript-review` adds: "EQUATOR-Network checklist applied to manuscript type; missing items flagged as major issues."
- `bwa-alignment` adds: "Read group (@RG) tags populated; duplicate marking precedes variant calling."

The validator requires the three base rules to appear (case-insensitive substring match on the rule title) but does not enforce specific extensions.

### `## Cross-references`

A bullet list of related ORS skills, using **kebab-case slugs**. Each line is `- <slug> — <one-line description>`. The validator resolves every slug against `skills/` and `meta/`.

```markdown
## Cross-references

- systematic-review — full PRISMA 2020 systematic review with screening.
- citation-management — Zotero / BibTeX / DOI workflows.
- meta/integrity-audit — 7-mode AI failure-mode checklist applied before publish.
```

Slugs are resolved as `<slug>` against `skills/*/<slug>/SKILL.md` and against `meta/<slug>/SKILL.md`. A missing slug fails validation.

## Examples of valid SKILL.md files

A minimal one:

```yaml
---
name: my-new-skill
description: Compute GC content for a FASTA file using Biopython.
---

# My New Skill

## When to use
…

## When NOT to use
…

## Hard rules

1. **No fabricated citations** — …
2. **No claim without provenance** — …
3. **No silent failure** — …

## Cross-references

- reverse-complement — strand-aware DNA / RNA operations.

## Changelog

- **1.0.0** (2026-XX-XX) — Initial release.
```

A fuller one:

```yaml
---
name: bwa-alignment
description: Align Illumina short reads to a reference genome using BWA-MEM, then sort, mark duplicates, and index the resulting BAM file with samtools. Use this for short-read Illumina data.
license: MIT
---

<!-- metadata:
  category: bioinformatics-sequence
  version: 1.0.0
  author: Pradyumna Jayaram
  oversight: low
  tags: [bwa, alignment, sam, bam, illumina]
  difficulty: intermediate
  sources: bioSkills/sequence-alignment
-->

# BWA Alignment

## When to use
…

## Hard rules

1. **No fabricated citations** — …
2. **No claim without provenance** — …
3. **No silent failure** — …

**Domain extensions:**

- Read group (@RG) tags populated before alignment.
- Duplicate marking (samtools markdup) precedes variant calling.

## Cross-references

- sam-bam-basics — SAM/BAM format foundations.
- samtools-bam-processing — sort, index, mark duplicates with samtools.
- hisat2-alignment — splice-aware alternative for RNA-seq.

## Changelog

- **1.0.0** (2026-XX-XX) — Initial release.
```

## Validation

Run `python scripts/validate-skills.py skills/ meta/` from the repo root. As of v0.4.0 it enforces:

- `name` matches the folder name
- `name` is unique repo-wide
- `name` is kebab-case ASCII
- `description` is present and non-empty
- `license` (if present) is a valid SPDX identifier
- The metadata HTML comment (if present) is well-formed
- `<!-- metadata: ... -->` includes `oversight` with one of `very-high | high | medium | low`
- `## Hard rules` section is present and contains the three base rule titles
- `## Cross-references` section is present and every slug resolves

To backfill `oversight: medium` on existing skills that lack it: `python scripts/validate-skills.py skills/ --backfill`.

## Where the format comes from

ORS follows the [Anthropic Agent Skills specification](https://agentskills.io/specification) strictly. The only ORS-specific additions are:

1. The optional `<!-- metadata: ... -->` block in the body (since v0.1.0).
2. The `## Hard rules` and `## Cross-references` body sub-sections (since v0.4.0).
3. The `oversight` metadata field (since v0.4.0).

The integrity layer added in v0.4.0 is grounded in published scholarly practice: PRISMA 2020, EQUATOR Network reporting guidelines, ICMJE recommendations, COPE peer-review guidelines, and the research literature on AI-assisted research failure modes (Lu et al. *Nature* 651:914–919, 2026; Zhao et al. arXiv:2505.07723, 2025). No verbatim prose or structural patterns are derived from any third-party skill repository.
