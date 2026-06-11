# Multi-skill workflows

Some research tasks span multiple skill categories. This example walks through a realistic end-to-end workflow that uses **5 ORS skills** in sequence.

## The task

> A graduate student has just generated ChIP-seq data for a transcription factor. They need to go from raw reads to a manuscript draft in 3 weeks.

## The skills used

1. **`bioinformatics-sequence/fastp-workflow`** — QC and adapter trimming
2. **`bioinformatics-sequence/bwa-alignment`** — Align to reference
3. **`bioinformatics-sequence/sam-bam-basics`** — Sort, index, deduplicate
4. **`bioinformatics-sequence/pileup-generation`** — Call peaks
5. **`scientific-writing/manuscript-structure`** — Draft the methods section
6. **`scientific-thinking/hypothesis-generation`** — Frame the introduction

## The agent prompt

```python
import pathlib
from anthropic import Anthropic

def load_skill(rel_path: str) -> str:
    return pathlib.Path(f"skills/{rel_path}/SKILL.md").read_text().split("---", 2)[2].strip()

# Load all 6 skills into one system prompt
skills_text = "\n\n---\n\n".join([
    load_skill("bioinformatics-sequence/fastp-workflow"),
    load_skill("bioinformatics-sequence/bwa-alignment"),
    load_skill("bioinformatics-sequence/sam-bam-basics"),
    load_skill("bioinformatics-sequence/pileup-generation"),
    load_skill("scientific-writing/manuscript-structure"),
    load_skill("scientific-thinking/hypothesis-generation"),
])

client = Anthropic()
response = client.messages.create(
    model="claude-opus-4-8",
    max_tokens=8192,
    system=f"""You are a research assistant for a graduate student working on a ChIP-seq project.

You have the following 6 ORS skills loaded. Use them in the order they appear, in the order the workflow demands.

{skills_text}

When the user asks for a step, follow the relevant skill's workflow exactly.
When the user asks for a step outside the loaded skills, ask which skill to load.""",
    messages=[{"role": "user", "content": """
    I just got back FASTQ files from the sequencer:
    - sample_CTCF_rep1_R1.fastq.gz
    - sample_CTCF_rep1_R2.fastq.gz
    - sample_CTCF_rep2_R1.fastq.gz
    - sample_CTCF_rep2_R2.fastq.gz
    - input_CTCF_R1.fastq.gz
    - input_CTCF_R2.fastq.gz

    The reference genome is at /refs/GRCh38.fa with the index already built.

    Help me go from raw reads to a draft methods section.
    """}]
)
print(response.content[0].text)
```

## What the agent will do

1. **Step 1 (using `fastp-workflow`):** Suggest running `fastp` on all 6 files, with sensible defaults for ChIP-seq (detect adapters, trim 5', filter low-quality reads).
2. **Step 2 (using `bwa-alignment`):** Align trimmed reads to GRCh38 with `bwa mem`, output to BAM.
3. **Step 3 (using `sam-bam-basics`):** Sort, mark duplicates, index with `samtools`.
4. **Step 4 (using `pileup-generation`):** Call peaks with `MACS3` or equivalent.
5. **Step 5 (using `scientific-thinking/hypothesis-generation`):** Frame the introduction around the biological question.
6. **Step 6 (using `scientific-writing/manuscript-structure`):** Draft the methods section with the exact commands run.

Each step will be grounded in the skill's code patterns and pitfalls.

## Why this works

- **Skills are independent.** Each one knows its own workflow; the agent doesn't have to reason from scratch.
- **Skills compose.** The output of one (e.g., "trimmed reads") becomes the input to the next (e.g., "align trimmed reads").
- **No hallucination.** Every command, parameter, and tool version comes from a verified source documented in the skill.
- **The agent stays focused.** Without the skills, the agent might invent tool names, skip QC, or write a generic methods section. With the skills, it follows the actual procedure a postdoc would.

## Variations

- **Smaller context window?** Load only the skill for the current step. Use the routing pattern from `api-integration.md`.
- **Different organism?** The skills are tool-agnostic — they describe the workflow, not the specific reference. Swap GRCh38 for `GRCm39` (mouse), `danRer11` (zebrafish), etc.
- **Different assay?** Load the ATAC-seq skills (`bioinformatics-sequence` and the planned `bioinformatics-omics` category) instead of the ChIP-seq skills.

## Anti-pattern

Don't load 20+ skills at once. The model gets confused about which skill applies and the response quality drops. If you need 20 skills, route them — let the agent pick which one to load for each step.
