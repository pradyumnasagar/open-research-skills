---
name: cross-reference-mapper
description: "Discover and maintain `## Cross-references` between ORS skills. Given a new or edited skill, suggest related skills (same category, shared tags, complementary workflows). Verify all xref slugs resolve to existing SKILL.md files. Use when adding a new skill, when sibling skills move, or when an audit reveals dangling xrefs."
license: MIT
---
<!-- metadata:
  oversight: low
  version: 1.0.0
  author: ORS maintainers
  tags: [meta, cross-references, navigation, catalog]
  difficulty: intermediate
-->

# Cross-Reference Mapper

The ORS catalog is a graph: 100+ skills in 18+ categories that should be
navigable by clicking between them. This skill produces and maintains the
`## Cross-references` section in each skill's body.

## When to use

- Adding a new skill — generate its `## Cross-references` from the catalog.
- Adding a new category — propagate the change to all sibling skills.
- Renaming a skill — find every xref that references it and rewrite.
- Auditing the catalog — find dangling xrefs (slugs that don't resolve).
- Answering "what skills should I use for X?" — produce a curated trail.

## When NOT to use

- Reading or using an existing skill (load that skill directly).
- Auditing for content quality (use `meta/integrity-audit`).

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

## How xrefs work

Every `## Cross-references` section is a flat bullet list:

```text
Example xref section (these slugs are illustrative, not validated):

  ## Cross-references

  - systematic-review — full PRISMA 2020 systematic review with screening.
  - citation-management — Zotero / BibTeX / DOI workflows.
  - meta/integrity-audit — 7-mode AI failure-mode checklist applied before publish.
```

A slug resolves if either `skills/<category>/<slug>/SKILL.md` exists
**or** `meta/<slug>/SKILL.md` exists. The `meta/` prefix in the bullet
disambiguates.

## Generating xrefs for a new skill

When a new SKILL.md is added, generate its `## Cross-references` from
three sources, in priority order:

### 1. Same-category siblings

List all other skills in `skills/<category>/` with a one-line description
taken from each skill's frontmatter `description` (first sentence).

If the category has only one skill (this one), skip — go to source 2.

### 2. Tag-overlapping skills

If the new skill has tags `["rna-seq", "alignment"]`, find all other
skills whose tags overlap by ≥1. Score each candidate by:
- 3 points per shared tag
- +1 if same category
- -2 if very different oversight level (one is generative, one is mechanical)
- +2 if both reference each other in their `## Related Skills` or similar

Take the top 5 by score.

### 3. Workflow-complementary skills

These are skills that handle a *later* stage of the same pipeline:
- For a wet-lab protocol skill, list the analysis skills that consume its
  output.
- For an analysis skill, list the visualization / writing skills that
  consume its output.
- For a writing skill, list the literature-research skills that feed it.

## Verifying existing xrefs

Run from the repo root:

```bash
python scripts/validate-skills.py skills/   # xrefs are validated by this
```

A failing xref means the slug was renamed or the skill was moved. To fix:

1. Identify the renamed/moved skill in the diff.
2. Find every xref that references the old slug.
3. Rewrite to use the new slug.

A common cause: a skill is moved from `skills/<cat>/old-name/` to
`skills/<cat>/new-name/` (or to `meta/`). All xrefs must be updated.

## Cross-reference style guide

**Good:**
```
- bwa-alignment — BWA-MEM short-read aligner; standard for Illumina DNA-seq.
- samtools-bam-processing — SAM/BAM manipulation; downstream of all aligners.
- star-alignment — spliced aligner for RNA-seq; alternative to BWA for RNA.
```

**Bad:**
```
- bwa-alignment
- samtools-bam-processing
- star-alignment
```

The one-line description tells the reader whether to click through. A bare
slug forces them to load every skill to find the relevant one.

## Validation

A skill's xrefs are valid when:
- Every slug in the section resolves to an existing `SKILL.md`.
- Each line has the form `- <slug> — <description>` (em-dash separator).
- The skill does NOT xref itself.

## Cross-references

- meta/roadmap-author — use this skill as the final step of authoring.
- meta/integrity-audit — finds dangling xrefs as part of mode 6 (version drift).
- meta/release-management — version bumps should trigger an xref re-verification.

## Changelog

- **1.0.0** (2026-06-17) — Initial release. Algorithm distilled from the
  cross-reference patterns used by the bulk-migration of 116 existing skills.
