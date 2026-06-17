# Author's Guide to ORS Skills

This is the narrative companion to [`spec/skill-format.md`](./skill-format.md).
If you are new to ORS, read this first; the spec is the rule book, this
document is the friendly tour.

## Who this is for

You want to add a new ORS skill. You are familiar with the domain
(bioinformatics, statistics, scientific writing, etc.) and want to
distill your workflow into a reusable skill file that an AI agent can
load on demand.

You do **not** need to be a programmer. Skills are written in markdown
with YAML frontmatter; the heaviest code you'll write is a copy-pasteable
shell snippet or Python idiom.

## What "good" looks like

A good ORS skill is **specific**, **executable**, and **honest**.

- **Specific.** "Use this skill for any kind of analysis" is useless.
  "Use this skill to align Illumina short DNA-seq reads to a reference
  genome using BWA-MEM2 and produce a sorted BAM" is specific.
- **Executable.** Every recommendation in the skill should be something
  the agent can do *right now* given a terminal. If a step requires
  intuition, say so. If a step requires a non-default tool, name the tool.
- **Honest.** If a method has known failure modes (e.g. BWA-MEM2 fails on
  long reads), the skill must say so. If a tool version matters, the
  skill must pin it. If something is domain-specific, the skill must
  say it is domain-specific.

## Anatomy of a skill (the 60-second tour)

```yaml
---
name: bwa-alignment         # kebab-case slug
description: "..."          # the trigger: what & when (max 1024 chars)
license: MIT                # optional
---
<!-- metadata:
  category: bioinformatics-sequence
  oversight: low            # how much to trust the skill's specifics
  version: 1.0.0
  author: Your Name
  tags: [alignment, illumina, short-reads]
  difficulty: intermediate
-->

# BWA Alignment                            ← H1, human form of the slug

> Tagline.                                 ← single-line summary

## When to use                              ← 3-10 trigger bullets
## When NOT to use                          ← 2-5 anti-trigger bullets
## Hard rules                               ← 3 base + 0-5 domain rules
## Workflow                                 ← numbered steps
## Code patterns                            ← copy-pasteable snippets
## Pitfalls                                 ← OPTIONAL but recommended
## Validation                               ← how the user verifies success
## Cross-references                         ← sibling skill slugs
## Changelog                                ← version history
```

The full section-by-section contract is in [`spec/skill-format.md`](./skill-format.md).

## The 3 base hard rules

Every ORS skill MUST include these three rules in `## Hard rules`. They
are the contract the agent agrees to when it loads the skill.

1. **No fabricated citations.** If the skill recommends a paper, tool, or
   resource, it must be real. Use DOIs, PMIDs, arXiv IDs, or stable URLs
   the agent can verify. When in doubt, say "I am not sure if this is
   correct" rather than inventing a citation.
2. **No claim without provenance.** Every quantitative or factual claim
   must point to a file, line, table, figure, dataset, or external source
   the agent can show. "Trust me" is not provenance.
3. **No silent failure.** Every script invocation, API call, or tool use
   must declare its exit status and what to do on non-zero. A skill
   that says "run X" without saying "check that X succeeded" is in
   violation.

You may add 0-5 domain-specific rules. Domain rules are concrete, not
aspirational. "Check exit codes on every shell call" is concrete; "Be
careful" is not.

## The `oversight` field

This tells Claude how much to trust your skill's specifics.

- `very-high` — generative, may fabricate facts. Use for skills that
  produce text, like literature reviews or cover letters.
- `high` — mixed: the framework is reliable, but specific details
  (citations, parameter values) may be wrong. Use for skills that
  combine framework knowledge with variable specifics.
- `medium` — the framework is reliable, the specific commands are
  reliable, but the agent should still verify before destructive
  operations. Use for most analytical skills.
- `low` — deterministic, mechanical. Use for format conversion,
  file I/O, schema validation, etc.

When in doubt, err on the side of higher oversight. The agent will
fact-check more aggressively, which is safer.

## The `description` field is your most important sentence

The `description` in the YAML frontmatter is the trigger the agent uses
to decide whether to load your skill. It must answer three questions:

1. **What does this skill do?** (1 sentence)
2. **When should the agent load it?** (the trigger conditions)
3. **When should the agent NOT load it?** (the negative triggers)

Example (a *bad* description):

> "Alignment skill for genomics."

Example (a *good* description):

> "Align Illumina short DNA-seq reads to a reference genome using
>  BWA-MEM2 and produce a sorted, indexed BAM. Use when the user has
>  trimmed FASTQ files and a reference FASTA and wants the standard
>  short-read alignment. Do NOT use for long reads (use minimap2), for
>  spliced alignment of RNA-seq (use STAR), or for cross-species
>  alignment (use LAST)."

The good description is ~400 characters. The maximum is 1024. Aim for
300-600.

## How to test before submitting

1. **Validator.** Run `python scripts/validate-skills.py skills/<category>/<your-slug>/`.
   The validator enforces every rule in `spec/skill-format.md`. A
   skill that fails validation will not be merged.
2. **Load test.** In a chat with Claude, ask "Load the `<your-slug>`
   skill and walk me through the workflow." Does the agent follow the
   workflow? Does it respect the hard rules? If not, the skill is
   unclear — rewrite.
3. **Anti-trigger test.** Ask the agent something the skill is NOT
   designed to handle. Does the agent correctly say "this skill is not
   the right tool, use X instead"? If not, strengthen the `When NOT to
   use` section.

## Versioning your skill

Use semantic versioning:

- **patch** (1.0.X) — typo fixes, example corrections, no behavioral change.
- **minor** (1.X.0) — new code pattern, new pitfall, new xref. Backward
  compatible.
- **major** (X.0.0) — change to the workflow steps, change to the
  hard rules, change to the input/output contract.

Every version bump MUST add a `## Changelog` entry. The latest entry
MUST match the `version` field in the metadata block.

For the package-level versioning (when the whole ORS repo gets a new
release), see `meta/release-management/SKILL.md`.

## Common mistakes (and how to avoid them)

| Mistake | Why it's wrong | Fix |
|---|---|---|
| "This skill can be used for X" without saying *when* | The agent can't decide whether to load it | Be specific. "When the user has trimmed FASTQ and a reference FASTA and wants short-read alignment" |
| Recommending a tool without saying what version | Tool APIs change. v1 and v2 of a tool may have different flags. | Pin the version. "BWA-MEM2 2.2.1+" or "samtools 1.18+" |
| No `## Hard rules` | The skill has no enforceable contract | Add the 3 base rules. Add 0-5 domain-specific ones. |
| "Check that the output looks right" | "Looks right" is not a check | Specify the check. "Confirm the BAM has a BAI index of the same name" |
| Mixing tutorials with the skill | The skill is meant to be loaded, not read end-to-end | Put tutorial content in `examples/` or `docs/`. The skill itself is a reference. |
| Forgetting `## Cross-references` | Skills in isolation don't form a graph | List 2-5 sibling skills. The user can then navigate the catalog. |
| Pretending you verified something you didn't | Violates the no-claim-without-provenance rule | Say "I have not personally run this; based on the docs, it should work" |

## When to ask for a review

Submit a PR when:

- The skill passes `validate-skills.py`.
- The skill has at least one code pattern that you have personally run
  (or that you have read documentation for and noted the source).
- The skill has at least 3 cross-references to sibling skills.

A reviewer will:

- Check the description is specific enough.
- Check at least one code pattern against the cited tool's docs.
- Check that the cross-references resolve.
- Check that the `## Hard rules` are not just boilerplate.

## Related docs

- `spec/skill-format.md` — the formal spec (sections, fields, validation rules).
- `spec/category-taxonomy.md` — the 18 categories a skill can belong to.
- `spec/material-passport.md` — how skills chain via Material Passports.
- `meta/roadmap-author/SKILL.md` — the agent-facing workflow for authoring.
- `meta/integrity-audit/SKILL.md` — the 7-mode checklist to run before
  submitting the PR.
- `meta/cross-reference-mapper/SKILL.md` — how to find sibling skills.
- `meta/release-management/SKILL.md` — when your skill needs a version bump.
