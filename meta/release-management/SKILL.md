---
name: release-management
description: "Version, changelog, and marketplace workflow for ORS skills. Semver discipline, breaking-change protocol, marketplace.json update, README refresh, and the v0.X.Y → v1.0.0 graduation criteria. Use when bumping a skill version, publishing a release, or upgrading the ORS package version."
license: MIT
---
<!-- metadata:
  oversight: low
  version: 1.0.0
  author: ORS maintainers
  tags: [meta, release, versioning, semver, marketplace]
  difficulty: intermediate
-->

# Release Management

The ORS release workflow — when and how to bump versions, what goes in
changelogs, how the marketplace.json is updated, and the criteria for
graduating a skill from beta to stable.

## When to use

- Bumping a skill's `version` field after an edit.
- Releasing a new ORS package version (v0.X.Y).
- Updating the marketplace manifest.
- Deciding whether a change is a patch, minor, or major bump.
- Closing out a milestone that spans many skills.

## When NOT to use

- Adding a new skill from scratch (use `meta/roadmap-author`).
- Auditing a skill for content issues (use `meta/integrity-audit`).
- Validating the local tree (use `scripts/validate-skills.py`).

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

## Semver for skills

ORS uses [Semantic Versioning](https://semver.org/) per-skill AND for the
package as a whole.

### Per-skill semver (in `<!-- metadata -->` block)

| Bump | When |
|------|------|
| **patch** (1.0.X) | Typos, broken links, single-line clarifications, no content change |
| **minor** (1.X.0) | New domain rule, new code pattern, new tool, new section |
| **major** (X.0.0) | Incompatible change — slug rename, schema change, removed feature |

**Rule:** A change to the `description` field is *always* at least a minor
bump, because it changes the trigger surface that Claude uses to decide
whether to load the skill.

**Rule:** A change to the `category` field is *always* major — it moves
the skill in the catalog and breaks cross-references that hardcoded the
category.

### Package semver (root `marketplace.json`)

| Bump | When |
|------|------|
| **patch** (0.0.X) | Bug fixes, validation-script fixes, doc clarifications |
| **minor** (0.X.0) | New skill added, meta skill added, schema extension (additive only) |
| **major** (X.0.0) | Schema break, removed skill, mandatory migration of existing skills |

## The release workflow

For each release:

1. **Identify the changes.** Run `git diff --stat <previous-tag>..HEAD` to
   see what changed. Group changes by skill.
2. **Decide the bumps.** Apply the semver table above to each skill. Decide
   the package bump from the highest individual bump plus the overall
   schema impact.
3. **Update each affected SKILL.md.** Bump `version` in the metadata block,
   prepend an entry to `## Changelog`. The changelog entry must be
   one-line and concrete: "Added `## Pitfalls` section listing 5 common
   errors", not "Various improvements".
4. **Update `marketplace.json`.** Bump `version` at the package level. Add
   the new/changed skills to the `plugins` array. Verify the JSON schema
   matches the latest Claude Code marketplace spec.
5. **Run the full validator.** `python scripts/validate-skills.py skills/`
   must exit 0 across the entire repo. If it fails, the release is blocked.
6. **Run the integrity audit.** Load `meta/integrity-audit` and run it on
   every changed SKILL.md. Any FAIL blocks the release.
7. **Tag the release.** `git tag -a v0.X.Y -m "<summary>"`. Push tags:
   `git push origin v0.X.Y`.
8. **Refresh the README.** If the package version, total skill count, or
   top-level structure changed, update the README counts and the
   "What's new" section.

## Changelog discipline

Changelog entries must be:

- **Concrete** — "Added `## Pitfalls` section with 5 entries" not "Improvements".
- **One line per change** — easier to scan, easier to bisect.
- **In past tense** — "Added", "Fixed", "Changed", "Removed".
- **Tagged with category** — optional but recommended for package-level
  changelogs (skill, schema, validator, docs).

**Bad:**
```
- 1.1.0 — Various improvements
```

**Good:**
```
- **1.1.0** (2026-06-17) — Added `## Pitfalls` section with 5 entries;
  fixed broken DOI for Smith 2023; clarified `oversight` guidance.
```

## Graduation criteria (v0.X.Y → v1.0.0)

ORS graduates to v1.0.0 when:

- [ ] Schema has been stable for 30 days with no breaking changes proposed.
- [ ] Validator passes cleanly on the full 100+ skill catalog.
- [ ] At least one reference skill per category has been published
      (`skills/<category>/<skill>/SKILL.md` with full v0.4.0 conformance).
- [ ] All 5 meta skills are present and stable.
- [ ] README has a complete "How to use" section with a real example.
- [ ] A showcase example (load 3 skills in sequence to do a real task) is
      documented and reproducible.
- [ ] Marketplace.json validates against the Claude Code schema.

## Breaking-change protocol

If a release requires existing skills to change (e.g. a schema extension
that mandates new fields):

1. **Co-write the migration script.** Add `scripts/migrate-vX-to-vY.py`.
2. **Run on a copy first.** Verify the script is idempotent and produces
   no regressions in `python scripts/validate-skills.py`.
3. **Document in the changelog.** "BREAKING: X changed; run
   `python scripts/migrate-vX-to-vY.py skills/` to upgrade."
4. **Run on main.** Commit the migration + the schema change in a single
   atomic commit so users can bisect.
5. **Tag clearly.** `git tag -a vX.Y.0 -m "BREAKING: ..."`.

## Cross-references

- roadmap-author — produces new skills; use this skill to release them.
- integrity-audit — final-pass check before any release.
- cross-reference-mapper — verify xref slugs before tagging.

## Changelog

- **1.0.0** (2026-06-17) — Initial release. Distilled from the v0.2.0 → v0.4.0
  migration experience and the ARS-comparison release workflow.
