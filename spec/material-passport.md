# Material Passport Schema (v1.0.0)

A **Material Passport** is a structured JSON envelope that travels with
every artifact produced by an ORS skill. It captures inputs, outputs,
decisions, and provenance so a downstream skill can resume work without
re-deriving context.

This document is the formal spec. For the agent-facing usage guide, see
`meta/agent-handoff/SKILL.md`.

## Why it exists

When one skill produces output that another skill consumes, the
receiving skill needs to know:

1. What input the producing skill was given.
2. What decisions the producing skill made.
3. What exit codes / errors happened.
4. Whether the producing skill's output matches what the receiving skill expects.

Without a passport, the receiving skill either re-runs upstream work
(expensive, often impossible if upstream was destructive) or proceeds
blind (silent failure). The Material Passport is the standardized answer.

## File location and naming

A Material Passport is named `<run-id>.passport.json` and lives in the
**same directory** as the primary output artifact.

- One passport per skill invocation. If a skill produces multiple
  unrelated outputs, write one passport per output.
- The `run-id` is the producing skill's own identifier (a UUIDv4 is
  recommended, but a human-readable kebab-case id is acceptable for
  short-lived runs).
- The `.passport.json` suffix is mandatory — it is how consuming skills
  detect the file.

## Schema (v1.0.0)

The full JSON Schema (Draft 2020-12) is in `spec/material-passport.schema.json`.

### Required fields

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | Semver of the passport schema. Currently `"1.0.0"`. |
| `passport_id` | string (UUIDv4) | Globally unique identifier. |
| `created_at` | string (ISO-8601) | UTC timestamp of creation. |
| `produced_by.skill` | string | Slug of the producing skill. |
| `produced_by.skill_version` | string | Version of the producing skill. |
| `inputs[]` | array of InputRecord | Every input the skill consumed. |
| `outputs[]` | array of OutputRecord | Every output the skill produced. |
| `decisions[]` | array of DecisionRecord | Non-obvious choices the skill made. |
| `errors[]` | array of ErrorRecord | External calls' exit codes and stderr excerpts. |
| `downstream_hints.next_skills[]` | array of string | Slugs of skills that can consume this passport's outputs. |

### Recommended fields

| Field | Type | Description |
|---|---|---|
| `produced_by.agent` | string | Which model produced the work (e.g. `"claude-opus-4-8"`). |
| `produced_by.session_id` | string (UUIDv4) | The agent session, for traceability. |
| `parameters` | object | Every parameter the skill was given. |
| `consumed_passports[]` | array of string | IDs of upstream passports this skill consumed. |

### InputRecord

```json
{
  "type": "fastq | bam | vcf | fasta | csv | json | text | ...",
  "path": "data/sampleA_R1.fastq.gz",
  "sha256": "abc123...",
  "source": "ENA accession ERR123456"
}
```

- `type` should match a controlled vocabulary; for unknown types use
  the file extension lowercased (e.g. `"pdf"`, `"docx"`).
- `sha256` is the SHA-256 of the file content at the time of consumption.
- `source` is a human-readable provenance pointer (accession ID, URL,
  upstream passport_id).

### OutputRecord

```json
{
  "type": "bam",
  "path": "results/sampleA.sorted.bam",
  "sha256": "def456...",
  "size_bytes": 12345678
}
```

- `size_bytes` is optional but recommended for large artifacts.

### DecisionRecord

```json
{
  "step": "alignment",
  "choice": "bwa-mem",
  "alternatives_considered": ["bowtie2", "minimap2"],
  "rationale": "BWA-MEM is the canonical aligner for Illumina short DNA-seq reads."
}
```

- `step` is a free-text label for the decision point.
- `choice` is what the skill decided.
- `alternatives_considered` is the list of other options that were
  evaluated. Empty array is acceptable if the skill did not explicitly
  consider alternatives.
- `rationale` is a short, concrete justification. **Rule:** A reviewer
  should be able to read the rationale and either agree or disagree.
  Vague rationales ("the best tool") are a schema violation.

### ErrorRecord

```json
{
  "step": "sort",
  "tool": "samtools",
  "exit_code": 0,
  "stderr_excerpt": ""
}
```

- `exit_code` MUST be 0 for non-zero exits to be acceptable in a
  successful passport.
- `stderr_excerpt` is the first ~500 chars of stderr (or full if shorter).
  Empty string is acceptable when there was no stderr output.

### consumed_passports[]

Array of passport_ids of upstream passports this skill consumed. Forms
the upstream edge in the passport DAG.

### downstream_hints.next_skills[]

Array of skill slugs that can process this passport's outputs. This is
advisory — a consuming skill is not required to be in this list, but
having it helps Claude suggest the next step.

## Example

```json
{
  "schema_version": "1.0.0",
  "passport_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2026-06-17T12:34:56Z",
  "produced_by": {
    "skill": "bwa-alignment",
    "skill_version": "1.2.0",
    "agent": "claude-opus-4-8",
    "session_id": "abc-123"
  },
  "inputs": [
    {
      "type": "fastq",
      "path": "data/sampleA_R1.fastq.gz",
      "sha256": "abc123...",
      "source": "ENA ERR123456"
    },
    {
      "type": "fasta",
      "path": "refs/genome.fa",
      "sha256": "def456...",
      "source": "GRCh38"
    }
  ],
  "outputs": [
    {
      "type": "bam",
      "path": "results/sampleA.sorted.bam",
      "sha256": "789xyz...",
      "size_bytes": 12345678
    }
  ],
  "decisions": [
    {
      "step": "alignment",
      "choice": "bwa-mem",
      "alternatives_considered": ["bowtie2", "minimap2"],
      "rationale": "BWA-MEM is the canonical aligner for Illumina short DNA-seq reads."
    }
  ],
  "parameters": {
    "threads": 8,
    "min_mapq": 20
  },
  "errors": [
    {
      "step": "alignment",
      "tool": "bwa-mem2",
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

## Validation rules

A passport is valid when:

1. All required fields are present and non-empty.
2. All `sha256` values are 64 hex characters.
3. Every `path` in `inputs[]` and `outputs[]` resolves to an existing
   file (when the passport is validated by the consuming skill).
4. Every `produced_by.skill` slug resolves to a known ORS skill.
5. Every `consumed_passports[]` entry is a known passport_id (when
   validated in a context where passports are registered).
6. The chain of `consumed_passports` forms a DAG — no cycles.

The validator script `scripts/validate-passport.py` (planned) enforces
rules 1, 2, 4, and 6.

## Versioning

The passport schema follows ORS's package semver:

- **patch** (1.0.X) — add an optional field, clarify wording.
- **minor** (1.X.0) — add a new required field, deprecate an existing
  field (consumers MUST accept both old and new).
- **major** (X.0.0) — remove a required field, rename a field, change
  the semantics of an existing field.

A passport's `schema_version` MUST match the version that produced it.
Consuming skills MUST accept passports with the same major version and
any lower minor/patch.

## Changelog

- **1.0.0** (2026-06-17) — Initial release. Schema extracted from the
  `meta/agent-handoff` skill and formalised.
