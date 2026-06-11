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
- Convention: `name` is the same as the parent folder name (relative to `skills/`). For example, `skills/bioinformatics-sequence/bwa-alignment/SKILL.md` has `name: bwa-alignment`.
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

The body is Markdown. There is no required structure — write what fits. Common sections include:

- **When to use** — explicit trigger conditions
- **Workflow** — step-by-step procedure
- **Code patterns** — copy-pasteable snippets
- **Pitfalls** — what to avoid
- **Validation** — how to confirm the work is correct
- **References** — official docs, papers, links

### Recommended body header

We recommend starting the body with an `<!-- metadata: ... -->` HTML comment that captures the ORS-specific fields that don't belong in the Anthropic-spec frontmatter:

```markdown
<!-- metadata:
  category: bioinformatics-sequence
  version: 1.0.0
  author: Pradyumna Jayaram
  tags: [bwa, alignment, sam, bam]
  difficulty: intermediate
  sources: bioSkills/sequence-alignment
-->

# BWA Alignment
```

This keeps the frontmatter minimal (Anthropic-spec compatible) while preserving the rich metadata ORS needs for indexing, search, and contributor attribution.

## Examples of valid SKILL.md files

See the 118 skills in `skills/` for the full range. A minimal one:

```yaml
---
name: my-new-skill
description: Compute GC content for a FASTA file using Biopython.
---

# My New Skill

[Body of the skill — what the agent should do when this skill is loaded.]
```

A fuller one:

```yaml
---
name: bwa-alignment
description: Align DNA sequencing reads to a reference genome using BWA-MEM, then sort, mark duplicates, and index the resulting BAM file with samtools. Use this for short-read Illumina data.
license: MIT
---

<!-- metadata:
  category: bioinformatics-sequence
  version: 1.0.0
  author: Pradyumna Jayaram
  tags: [bwa, alignment, sam, bam, illumina]
  difficulty: intermediate
  sources: bioSkills/sequence-alignment
-->

# BWA Alignment

## When to use
...
```

## Validation

Run `python scripts/validate-skills.py skills/` from the repo root. It checks:

- `name` matches the folder name
- `name` is unique repo-wide
- `name` is kebab-case ASCII
- `description` is present and non-empty
- `license` (if present) is a valid SPDX identifier
- The metadata HTML comment (if present) is well-formed

## Where the format comes from

ORS follows the [Anthropic Agent Skills specification](https://agentskills.io/specification) strictly. The only ORS-specific addition is the optional `<!-- metadata: ... -->` block in the body. This was a deliberate design choice — agents that don't know about ORS can still parse any ORS skill using only the Anthropic spec.
