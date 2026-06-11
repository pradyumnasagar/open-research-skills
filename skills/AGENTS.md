# Skills authoring guide

This file is the **contributor guide for adding a new skill under `skills/`**. Read `/AGENTS.md` at the repo root first — it has the high-level policy. Read this file when you actually need to add or modify a skill.

## Workflow for adding a new skill

1. **Pick the right category.** Open `spec/category-taxonomy.md` and find the closest match. If none of the 18 fit, see the "Adding a new category" section there.
2. **Copy `template/SKILL.md`** to `skills/<category>/<your-skill-slug>/SKILL.md`. The folder name MUST be the kebab-case ASCII slug.
3. **Fill in the frontmatter.** `name` MUST match the folder name and MUST be unique repo-wide. `description` is the routing signal — write it carefully.
4. **Fill in the body metadata block** right under the title with category, version, author, tags, difficulty, sources.
5. **Write the body.** Follow the template sections but use what fits. Include validation steps.
6. **Run `python scripts/validate-skills.py skills/`** from the repo root. Fix any errors.
7. **Run `python scripts/build-index.py`** to regenerate `INDEX.md` with your new skill.
8. **Open a PR.**

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

## Validation

Two scripts enforce the contract:

- `python scripts/validate-skills.py skills/` — checks frontmatter, naming, uniqueness.
- `python scripts/build-index.py` — regenerates `INDEX.md`.

Both run in CI (`.github/workflows/validate.yml`).

## Local testing

Once a skill is in place, you can test it by:

1. `cd` to the repo root.
2. Start Claude Code in that directory: `claude`.
3. In the chat, reference the skill by its name, e.g. "Use the `bwa-alignment` skill to align these reads."
4. Confirm Claude loads and follows the skill.
