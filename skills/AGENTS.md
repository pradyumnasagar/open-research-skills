# Skills authoring guide

This file is the **contributor guide for adding a new skill under `skills/`**. Read `/AGENTS.md` at the repo root first — it has the high-level policy. Read this file when you actually need to add or modify a skill.

## Workflow for adding a new skill

1. **Pick the right category.** Open `spec/category-taxonomy.md` and find the closest match. If none of the 18 fit, see the "Adding a new category" section there. If the skill cuts across multiple categories, it goes under `meta/` instead.
2. **Copy `template/SKILL.md`** to `skills/<category>/<your-skill-slug>/SKILL.md` (or `meta/<your-skill-slug>/SKILL.md`).
3. **Fill in the frontmatter.** `name` MUST match the folder name and MUST be unique repo-wide. `description` is the routing signal — write it carefully.
4. **Fill in the body metadata block** with category, version, author, **oversight** (very-high | high | medium | low), tags, difficulty, sources. See the `oversight` decision table below.
5. **Write the body sections.** The four mandatory sections are: `## When to use`, `## Hard rules`, `## Cross-references`, `## Changelog`. Add more (workflow, code patterns, pitfalls, validation, references) as needed.
6. **Add cross-references.** Every skill should list at least 2-3 slugs of related skills. Use the bare slug (folder name), not a path.
7. **Run `python scripts/validate-skills.py skills/`** from the repo root. Fix any errors. The validator checks all four required sections, the three base hard rules, and that every cross-reference slug resolves to a real skill.
8. **Run `python scripts/build-index.py`** to regenerate `INDEX.md` with your new skill.
9. **Open a PR.**

## Naming rules

- **Folder name:** lowercase kebab-case ASCII, no leading/trailing hyphens, no version numbers, no author names.
- **Good:** `bwa-alignment`, `pysam-genomics`, `rdkit-fingerprint`, `fastq-quality-scores`.
- **Bad:** `BWA_Alignment` (uppercase, underscore), `bwa-alignment-v2` (version in name), `li-2023-pysam` (author + year in name).

## Skill body guidance

A skill is **not** raw documentation. It's a recipe the agent follows.

- **Lead with when to use.** The agent is matching your skill to a user request. Be specific.
- **Include code patterns.** Snippets > prose. Every snippet should be runnable in isolation.
- **List pitfalls.** What goes wrong if the agent follows the obvious path? Name it.
- **Specify validation.** How does the agent know the work is done? What does success look like?
- **Cite sources.** If you adapted material from an upstream skill, list it in the metadata `sources` field.

## Frontmatter

The full schema is in `spec/skill-format.md`. Short version:

```yaml
---
name: <kebab-case-slug, unique repo-wide>
description: <one or two sentences, ≤200 chars recommended>
license: <SPDX identifier, optional, defaults to MIT>
---
```

That's it. Everything else (category, version, author, tags, difficulty, sources) goes in the `<!-- metadata: ... -->` block at the top of the body.

## What NOT to do

- **Don't copy verbatim from copyrighted sources.** Always rewrite in your own words. Cite the source.
- **Don't use the upstream author's name in the frontmatter or folder.** All skills in this repo are authored by Pradyumna Jayaram unless explicitly co-authored in a PR.
- **Don't add Co-Authored-By: AI-assistant lines to commits.** This is a Pradyumna-Jayaram-authored repo.
- **Don't claim to support a tool version you haven't verified.** If you say "works with BWA 0.7.17", you've actually tested it.
- **Don't add a skill that overlaps significantly with an existing one.** If you think one is missing, open an issue first.

## The four mandatory body sections

The validator (`scripts/validate-skills.py`) rejects skills missing any of these:

1. **`## When to use`** — 2-5 bullet triggers. The agent matches these against user requests. Be specific. Include a "When NOT to use" subsection if the skill overlaps with another.
2. **`## Hard rules`** — the three base rules (no fabricated citations, no claim without provenance, no silent failure) PLUS any domain-specific rules. Use the exact phrasing of the base rules; the validator checks substrings.
3. **`## Cross-references`** — list of `- <slug> — description` lines. Every slug must resolve to a folder under `skills/` or `meta/`. This is the mesh that lets the agent chain skills.
4. **`## Changelog`** — start with `- **1.0.0** (YYYY-MM-DD) — Initial release.` and add a line per breaking change.

## Setting `oversight`

`oversight` in the metadata block declares how much human review the skill's output requires. Pick conservatively.

| Level     | Use when                                                                | Examples                                          |
| --------- | ----------------------------------------------------------------------- | ------------------------------------------------- |
| very-high | The output drives a clinical, regulatory, or safety-critical decision.  | Patient-facing dosing, IRB protocol drafts,      |
|           | Mistakes are hard to roll back.                                          | consent forms, clinical report writing.           |
| high      | The output is a published artefact whose author will be on record.      | Grant proposals, peer review reports,             |
|           | Plagiarism, hallucination, or miscalibration would damage reputation.   | scientific-writing outputs, statistical analyses.|
| medium    | The output is a working artefact (analysis script, draft figure) that   | Most day-to-day skills.                           |
|           | the user will review and iterate on.                                     |                                                   |
| low       | The output is a throwaway convenience (a one-liner, a doc lookup,        | API parameter recall, file-renaming recipes.      |
|           | a quick syntactic check). Mistakes are cheap to detect.                 |                                                   |

Default to `medium` if unsure. The `meta/integrity-audit` skill is `very-high` because it audits other skills' integrity.

## Validation

Two scripts enforce the contract:

- `python scripts/validate-skills.py skills/` — checks frontmatter, naming, uniqueness, the four mandatory sections, the three base hard rules, `oversight`, and that every cross-reference slug resolves to a real skill.
- `python scripts/build-index.py` — regenerates `INDEX.md`.

Both run in CI (`.github/workflows/validate.yml`).

## Local testing

Once a skill is in place, you can test it by:

1. `cd` to the repo root.
2. Start Claude Code in that directory: `claude`.
3. In the chat, reference the skill by its name, e.g. "Use the `bwa-alignment` skill to align these reads."
4. Confirm Claude loads and follows the skill.
