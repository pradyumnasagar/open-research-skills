# open-research-skills specification

This directory contains the ORS specification. It is intentionally short — most of the specification is shared with the upstream **Agent Skills specification** published at <https://agentskills.io/specification>.

## What's in here

| File | Purpose |
|---|---|
| `skill-format.md` | The minimal frontmatter required for a `SKILL.md` to be valid in ORS. |
| `category-taxonomy.md` | The 18 ORS categories, what each contains, and the order of categories. |

## How ORS fits the broader skill ecosystem

- The Anthropic **Agent Skills specification** (<https://agentskills.io/specification>) defines the universal frontmatter contract: `name` and `description` are required, everything else is convention.
- ORS follows that contract strictly. Every `SKILL.md` in this repo MUST have `name` and `description`.
- ORS adds a small, research-domain-specific layer on top:
  - **One of 18 categories** (see `category-taxonomy.md`).
  - **An optional `license:` field** in frontmatter. Default is MIT.
  - **An optional `<!-- metadata: ... -->` block** in the body for category, version, author, tags.

## Where to put a new skill

Copy `template/SKILL.md` to `skills/<category>/<your-skill-slug>/SKILL.md` and fill in the frontmatter and body. The `name` field MUST be unique repo-wide and MUST use kebab-case ASCII. The folder name MUST match the slug portion of the name.

## Versioning

The repo follows [semantic versioning](https://semver.org/):

- **Major (1.0.0 → 2.0.0)** — break the frontmatter contract, remove or rename categories.
- **Minor (1.0.0 → 1.1.0)** — add new categories, add new skills, schema additions that are backwards compatible.
- **Patch (1.0.0 → 1.0.1)** — fix typos, update tooling versions inside skills, add validation tests.

## License

This specification is MIT-licensed. See `/LICENSE` in the repo root.
