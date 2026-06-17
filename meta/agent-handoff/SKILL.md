---
name: agent-handoff
description: "Pass work between ORS skills with a Material Passport — a structured JSON envelope that captures inputs, outputs, decisions, and provenance so a downstream skill can resume without re-deriving context. Use when one skill produces output that another skill must consume, especially across category boundaries (e.g. analysis → writing, sequencing → statistics)."
license: MIT
---
<!-- metadata:
  oversight: low
  version: 1.0.0
  author: ORS maintainers
  tags: [meta, handoff, provenance, interop, pipelines]
  difficulty: advanced
-->

# Agent Handoff

When one ORS skill produces output that another skill must consume, the
two skills need a structured envelope — a **Material Passport** — to pass
work cleanly. This skill defines the envelope schema and the discipline
for using it.

## When to use

- Skill A produces files / claims / data that skill B will use downstream.
- A multi-step pipeline spans 3+ skills (e.g. sequencing → QC → statistics
  → visualization → writing).
- An agent's context window is about to be lost (session restart, model
  switch) and the work must be resumable from disk.
- A reviewer needs to understand what a previous agent decided and why.

## When NOT to use

- A single skill handles the whole task (no handoff needed).
- A pipeline is best expressed as a Snakemake / Nextflow workflow (use the
  workflow engine, not ad-hoc handoffs).
- The "handoff" is a one-line pointer in a chat (no envelope needed).

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

## The Material Passport

A Material Passport is a JSON file that travels alongside the artifacts
produced by a skill. It is named `<run-id>.passport.json` and lives in
the same directory as the primary output.

### Schema (v1)

```json
{
  "schema_version": "1.0.0",
  "passport_id": "uuid-v4",
  "created_at": "2026-06-17T12:34:56Z",
  "produced_by": {
    "skill": "bwa-alignment",
    "skill_version": "1.2.0",
    "agent": "claude-opus-4-8",
    "session_id": "uuid-v4"
  },
  "inputs": [
    {
      "type": "fastq",
      "path": "data/sampleA_R1.fastq.gz",
      "sha256": "abc123...",
      "source": "ENA accession ERR123456"
    }
  ],
  "outputs": [
    {
      "type": "bam",
      "path": "results/sampleA.sorted.bam",
      "sha256": "def456...",
      "size_bytes": 12345678
    }
  ],
  "decisions": [
    {
      "step": "alignment",
      "choice": "bwa-mem",
      "alternatives_considered": ["bowtie2", "minimap2"],
      "rationale": "BWA-MEM is the canonical aligner for Illumina short DNA-seq reads; minimap2 is preferred for long reads (ONT/PacBio)."
    }
  ],
  "parameters": {
    "threads": 8,
    "min_mapq": 20
  },
  "errors": [
    {
      "step": "sort",
      "tool": "samtools",
      "exit_code": 0,
      "stderr_excerpt": ""
    }
  ],
  "consumed_passports": [],
  "downstream_hints": {
    "next_skills": ["samtools-bam-processing", "gatk-variant-calling"],
    "expected_inputs": ["bam", "bam-index"]
  }
}
```

### Required fields

- `schema_version` — bump on breaking changes to the schema.
- `passport_id` — UUIDv4, globally unique.
- `created_at` — ISO-8601 timestamp.
- `produced_by.skill` — slug of the skill that created this passport.
- `produced_by.skill_version` — version of the producing skill.
- `inputs[]` — every input the skill consumed, with path + sha256.
- `outputs[]` — every output the skill produced, with path + sha256.
- `decisions[]` — every non-obvious choice the skill made, with
  alternatives and rationale.
- `errors[]` — every external call's exit code, with stderr excerpt.
- `downstream_hints.next_skills` — slugs of skills that consume this
  passport's outputs.

### Recommended fields

- `produced_by.agent` — which model produced the work.
- `produced_by.session_id` — the agent session, for traceability.
- `parameters` — every parameter the skill was given.
- `consumed_passports[]` — IDs of upstream passports this skill consumed
  (forms a DAG).

## When to write a passport

Write a passport for **every** output directory the skill creates. The
passport is the source of truth for "what did the skill actually do?"

Exceptions (where a passport is overkill):
- The output is a single throwaway chart for a chat answer.
- The skill is purely advisory (no files written).
- The skill is a reformat / re-export of an existing artifact (chain
  the upstream passport instead).

## Handoff protocol

When skill B consumes skill A's output:

1. B looks for `<run-id>.passport.json` in the same directory as the
   input file.
2. If found, B reads `produced_by.skill` and `produced_by.skill_version`
   to verify B's expectations match A's actual behavior.
3. B reads `errors[]` and **fails loudly** if any error is non-zero.
4. B reads `decisions[]` so the user can see what A decided without
   re-loading A.
5. B writes its own passport, including `consumed_passports` referencing
   A's passport_id.

If the passport is missing but the input file is present, B **prompts**
the user: "I see a BAM file from an unknown upstream. Continue without
provenance, or do you have a passport?"

## Validation

A handoff is valid when:
- The producing skill wrote a passport to the same directory as its output.
- The consuming skill loaded the passport before processing the input.
- The consuming skill's passport references the producing passport in
  `consumed_passports[]`.
- The chain of `consumed_passports` forms a DAG (no cycles).

## Cross-references

- roadmap-author — every skill's `## Code patterns` should show passport
  writing.
- integrity-audit — mode 4 (missing provenance) flags handoffs without
  passports.
- release-management — passport schema version follows the package
  version.

## Changelog

- **1.0.0** (2026-06-17) — Initial release. Material Passport schema
  distilled from inter-skill handoff patterns observed in the v0.4.0
  bulk migration.
