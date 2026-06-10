# Contributing to open-research-skills

This is **Pradyumna Jayaram's** curated collection of research-domain skills for AI agents. Contributions are welcome under the following rules.

## How to add a new skill

1. **Choose the right category** from `_meta/TAXONOMY.md`. If none fit, propose a new category in the PR description.
2. **Copy `_templates/SKILL-TEMPLATE.md`** to `<category>/<your-skill-slug>/SKILL.md`.
3. **Frontmatter** must conform to `_meta/SCHEMA.md`. The `name:` field MUST be `ors-<category-kebab>-<your-skill-slug>` and the folder name MUST match.
4. **Body** should follow the template sections but use what fits. A "Validation" section is required for any skill that ships code.
5. **Sources.** If you adapted material, fill in `sources_consulted:`. If you authored from scratch, list any references that informed the design.
6. **No hallucination.** Every tool, parameter, and external link must be verifiable. When unsure, prefer linking to the official docs over asserting behavior.
7. **Open alternatives.** If your skill references a commercial tool, list the open-source substitute in an "Open alternatives" section.

## Naming

- Folder name: lowercase kebab-case, ASCII only.
- No version numbers in folder names (use `version:` frontmatter).
- No author names in folder names.
- Skill slugs should be general ("pysam-genomics") not specific to a paper ("li-2023-pysam").

## What NOT to copy

- Verbatim text from copyrighted sources. Always rewrite in your own words.
- Author names from upstream repos. All skills are authored by Pradyumna Jayaram unless explicitly co-authored in a PR.
- Logos, trademarks, or branding of upstream tools. You may mention tools by name; that's fair use. You may not bundle their assets.

## Code of conduct

Be kind, be specific, be evidence-based. If you disagree with a design decision, link to the doc that supports your position. We are scientists.

## License

By contributing, you agree your contributions are licensed under MIT (same as this repo) and that Pradyumna Jayaram retains the right to relicense the consolidated work.
