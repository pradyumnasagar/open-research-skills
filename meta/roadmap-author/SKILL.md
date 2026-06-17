---
name: roadmap-author
description: "Author a new ORS skill from scratch using the v0.4.0 schema. Produces a valid SKILL.md (frontmatter + metadata + sections) following spec/skill-format.md, guided by spec/author-guide.md, validated by scripts/validate-skills.py. Use when a user says 'add a new skill', 'create a skill for X', or 'I want to contribute a skill'."
license: MIT
---
<!-- metadata:
  oversight: low
  version: 1.0.0
  author: ORS maintainers
  tags: [meta, authoring, schema, contributing]
  difficulty: beginner
-->

# Roadmap Author

Author a new ORS skill that passes `scripts/validate-skills.py` on first run.

## When to use

- A user asks to add a new skill, contribute a skill, or extend ORS with a new
  tool, format, or workflow.
- You need a guided tour through the v0.4.0 schema (frontmatter + metadata
  block + body sections) and the validator's expectations.
- You are converting an external agent prompt or Claude skill into ORS
  format and want the resulting SKILL.md to be schema-compliant.

## When NOT to use

- The user wants to *use* an existing skill (load that skill directly).
- The skill already exists and the task is to *update* it (use
  `meta/release-management`).
- The task is to audit a skill for quality issues before publishing (use
  `meta/integrity-audit`).

## Hard rules

1. **No fabricated citations.** Every cited work must resolve to a verifiable
   record (DOI, PMID, arXiv ID, ISBN, URL with retrieval date, or stable
   identifier). If a source cannot be resolved, the skill must say so
   explicitly rather than presenting the claim as established.
2. **No claim without provenance.** Every quantitative or factual claim
   must point to a file, line, table, figure, dataset, or external source
   the agent can show. "Trust me" is not provenance.
3. **No silent failure.** Every script invocation, API call, or tool use
   must declare its exit status and what to do on non-zero. A skill that
   silently swallows errors is a violation.

## Author workflow

A new skill goes through 6 steps. Skipping steps produces skills that fail
the validator or don't fit the catalog.

### Step 1: Pick the category

Every skill belongs to one category (a subdirectory of `skills/`). Pick
the existing one that best matches the domain, or propose a new category
if the domain is genuinely missing. Categories are: `bioinformatics-sequence`,
`chemoinformatics`, `clinical-research`, `data-engineering`, `experimental-design`,
`hypothesis-generation`, `imaging`, `literature-research`, `meta`,
`pharmacology`, `scientific-communication`, `scientific-writing`,
`statistics`, `structural-biology`, `systems-biology`,
`visualization-and-figure-prep`, `workflow-and-pipeline-management`,
`writing-and-drafting`.

**Rule:** The category MUST be a leaf category — do not invent sub-categories
inside a leaf. If a leaf is too coarse, propose a new leaf in a GitHub issue.

### Step 2: Pick the slug

The slug is the skill's kebab-case directory name. Rules:
- Lowercase, kebab-case (e.g. `bwa-alignment`, not `bwa_alignment` or `BWA-Alignment`).
- No version suffix in the slug. Versioning goes in the metadata block.
- No `ors-` prefix. The slug is the bare tool name.
- Must be unique across `skills/`.

**Rule:** The slug becomes the cross-reference key (see
`meta/cross-reference-mapper`). Changing the slug after publication breaks
links.

### Step 3: Write the frontmatter

The YAML frontmatter is the *Anthropic* skill spec — `name`, `description`,
optional `license`. The `description` field is what Claude sees when deciding
to load the skill, so it must:
- Start with the tool/workflow name.
- Describe the core capability in 1-2 sentences.
- State the trigger conditions (when to load).
- State the negative triggers (when NOT to load).

Maximum length: 1024 characters.

### Step 4: Write the metadata block

The `<!-- metadata: ... -->` block captures ORS-specific fields:

```yaml
<!-- metadata:
  category: <one of the leaf categories>
  oversight: <very-high | high | medium | low>
  version: <semver>
  author: <name>
  tags: [<kebab-case tags>]
  difficulty: <beginner | intermediate | advanced>
-->
```

The `oversight` field tells Claude how much to trust the skill:
- `very-high` — generative, may fabricate facts (e.g. literature review)
- `high` — mixed, may contain plausible-but-wrong details
- `medium` — framework is reliable, specifics need verification
- `low` — deterministic, mechanical (e.g. format conversion)

The `difficulty` field tells the user how much background knowledge is
required to use the skill effectively.

### Step 5: Write the body

Required body sections (in order):

1. `# <Skill Name>` — the H1, must match the frontmatter `name` in human form.
2. `## When to use` — 3-10 trigger bullets. Be specific. "Use this skill for
   any kind of analysis" is useless.
3. `## When NOT to use` — 2-5 anti-trigger bullets. Cross-reference sibling
   skills that *do* fit.
4. `## Hard rules` — the 3 base rules (cite, claim-provenance, no-silent-fail).
   Add 0-5 domain-specific rules. Domain rules are concrete, not aspirational
   ("Check exit codes on every shell call" not "Be careful").
5. `## Workflow` — the main procedure. Numbered steps, with example commands.
6. `## Code patterns` — copy-pasteable snippets, not pseudocode.
7. `## Validation` — how the user verifies the skill worked.
8. `## Cross-references` — sibling skill slugs, one per line, with a
   one-line description. See `meta/cross-reference-mapper`.
9. `## Changelog` — version history. Latest version first.

Optional sections (highly recommended): `## Pitfalls`, `## References`,
`## Decision tree`, `## Per-tool failure modes`.

### Step 6: Validate

Run from the repo root:

```bash
python scripts/validate-skills.py skills/<category>/<slug>/
```

Must exit 0. If errors, fix and re-run. Do not commit a skill that fails
validation.

## Validation

The skill is valid when:
- `python scripts/validate-skills.py <path>/` exits 0.
- The skill can be loaded by Claude without frontmatter parsing errors.
- A user reading only the description can decide whether to load it.

## Cross-references

- meta/integrity-audit — audit a draft skill against the 7-mode AI failure checklist.
- meta/release-management — version bumps, changelog discipline, marketplace sync.
- meta/cross-reference-mapper — find related skills across categories automatically.

## Related docs (not skills)

- `spec/skill-format.md` — the formal v0.4.0 schema definition.
- `spec/author-guide.md` — narrative guidance for first-time authors.

## Changelog

- **1.0.0** (2026-06-17) — Initial release. Authoring workflow distilled from
  the v0.4.0 spec and the lessons of bulk-migrating 116 existing skills.
